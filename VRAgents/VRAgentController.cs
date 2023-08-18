//***********************************************************************
//
//  VirtualStage Platform - a virtual stage for virtual actors
//  VRAgents -  C# library for developing agents able to operate in
//              OpenSimulator virtual worlds
//
//  Copyright (C): 2020-2023, Joao Carlos Gluz
//  Contact:  João Carlos Gluz (jcgluz@gmail.com)
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <https://www.gnu.org/licenses/>.
//
//***********************************************************************
//
//   Class:     VRAgentController 
//   Purpose:   All VR actions that the agent can execute and the perceptions
//              and beliefs (memories) bases that the agent can access are
//              implemented by classes of VRAgents library. These classes are
//              included as parts of the VRAgentController class, so this class
//              can control how the agent execute VR actions and how it access
//              its beliefs and perceptions. This class also handle VR events
//              sent by OpenSimulator to the agent. The VRAgentController class
//              was defined as a subclass of GridClient class of LibOpenMetaverse
//              library, to allow it to expose all functionality of OpenSimulator
//              grid clients to the VR actions classes. Thus, VRAgents agents
//              operate as clients (like VR viewers) of OpenMetaverse grids. 
//   Author:    João Carlos Gluz 
//
//***********************************************************************

using System;
using System.Collections.Generic;
using System.Collections;
using System.Threading;
using System.Reflection;
using System.Xml;
#if USE_LIBREMETAVERSE_VR_LIB
using LibreMetaverse;
using LibreMetaverse.Packets;
using LibreMetaverse.Utilities;
#else
using OpenMetaverse;
using OpenMetaverse.Packets;
using OpenMetaverse.Utilities;
#endif
//using System.Diagnostics;



#if USE_LIBREMETAVERSE_VR_LIB
namespace LibreMetaverse
#else
namespace OpenMetaverse
#endif
{
    public static class VRMsgFld
    {
        public const int Typ=0;         // type of msg: 'instmsg', 'chatmsg' or 'codemsg'
        public const int FrmNam = 1;
        public const int Cont = 2;
        public const int FrmID = 3;
        public const int TimStmp = 4;
        public const int PosX = 5;
        public const int PosY = 6;
        public const int PosZ = 7;
        public const int CodeTyp = 8;   // specific for codemsg messages
        public const int ChatTyp = 8;   // specific for chatmsg messages
        public const int GrpSes = 9;    // specific for codemsg messages
        public const int AudLev = 9;    // specific for chatmsg messages
        public const int GrpSesId = 10; // specific for codemsg messages
        public const int SrcTyp = 10;   // specific for chatmsg messages
    }

    public class VRAgentController : GridClient
    {
        public Dictionary<UUID, AvatarAppearancePacket> Appearances = 
                    new Dictionary<UUID, AvatarAppearancePacket>();
        public List<TimerTask> TimerTasks = new List<TimerTask>();
        public Dictionary<UUID, Group> GroupsCache = null;
        private ManualResetEvent GroupsEvent = new ManualResetEvent(false);

        public MovementActions MoveActs;
        public PositionActions PosActs;
        public ModificationActions ModActs;
        public CommunicationActions CommActs;
        public ObservationActions ObsActs;
        public SelfObservationActions SelfObsActs;
        public SelfModificationActions SelfModActs;
        public SocialObservationActions SocObsActs;
        public SocialModificationActions SocModActs;
        public SystemActions SysActs;

        public PerceptionsBase PerceptsBase = new PerceptionsBase();
        public Perceptions Percepts;

        public BeliefsBase BelsBase = new BeliefsBase();
        public Beliefs Bels;

        public bool Running = true;

        public VRAgentManager VRAgentManager;

        public InventoryFolder CurrentDirectory = null;
        private System.Timers.Timer TimerUpdate;

        public object RecvdVRMsgsLock = new object();
        public List<List<string>> RecvdVRMsgs = new List<List<string>>();

        public object DetcdVREventsLock = new object();
        public List<List<string>> DetcdVREvents = new List<List<string>>();


        public Dictionary<InstantMessageDialog, string> IMsgNames = 
                    new Dictionary<InstantMessageDialog, string>();

        public VRAgentController(VRAgentManager manager)
        {
            VRAgentManager = manager;
            TimerUpdate = new System.Timers.Timer(500);

            Settings.LOG_LEVEL = Helpers.LogLevel.Debug;
            Settings.LOG_RESENDS = false;
            Settings.STORE_LAND_PATCHES = true;
            Settings.ALWAYS_DECODE_OBJECTS = true;
            Settings.ALWAYS_REQUEST_OBJECTS = true;
            Settings.SEND_AGENT_UPDATES = true;
            Settings.USE_ASSET_CACHE = true;

            TimerUpdate.Elapsed +=
                new System.Timers.ElapsedEventHandler(TimerUpdateEvHandler);

            Network.RegisterCallback(PacketType.AgentDataUpdate, AgentDataUpdateCallback);
            Network.RegisterCallback(PacketType.AvatarAppearance, AvatarAppearanceCallback);
            Network.RegisterCallback(PacketType.AlertMessage, AlertMessageCallback);

            Network.LoginProgress +=
                    new EventHandler<LoginProgressEventArgs>(LoginProgressEvHandler);
            Network.SimChanged +=
                    new EventHandler<SimChangedEventArgs>(SimChangedEvHandler);

            Objects.AvatarUpdate += 
                    new EventHandler<AvatarUpdateEventArgs>(AvatarUpdateEvHandler);
            Objects.TerseObjectUpdate += 
                    new EventHandler<TerseObjectUpdateEventArgs>(TerseObjectUpdateEvHandler);

            Self.IM += 
                    new EventHandler<InstantMessageEventArgs>(InstantMessageEvHandler);
            Self.ChatFromSimulator += 
                    new EventHandler<ChatEventArgs>(ChatEvHandler);
            Self.MeanCollision +=
                    new EventHandler<MeanCollisionEventArgs>(MeanCollisionEvHandler);
            Self.RegionCrossed +=
                    new EventHandler<RegionCrossedEventArgs>(RegionCrossedEvHandler);

            Inventory.InventoryObjectOffered +=
                    new EventHandler<InventoryObjectOfferedEventArgs>(InventoryObjectOfferedEvHandler);

            MoveActs = new MovementActions(this);
            PosActs = new PositionActions(this);
            ModActs = new ModificationActions(this);
            CommActs = new CommunicationActions(this);
            ObsActs = new ObservationActions(this);
            SelfObsActs = new SelfObservationActions(this);
            SelfModActs = new SelfModificationActions(this);
            SocObsActs = new SocialObservationActions(this);
            SocModActs = new SocialModificationActions(this);

            SysActs = new SystemActions(this);

            Percepts = new Perceptions(this);
            Bels = new Beliefs(this);


            IMsgNames.Add(InstantMessageDialog.MessageFromAgent, "text");
            IMsgNames.Add(InstantMessageDialog.MessageBox, "message_box");
            IMsgNames.Add(InstantMessageDialog.GroupInvitation, "group_invitation");
            IMsgNames.Add(InstantMessageDialog.InventoryOffered, "inventory_offered");
            IMsgNames.Add(InstantMessageDialog.InventoryAccepted, "inventory_accepted");
            IMsgNames.Add(InstantMessageDialog.InventoryDeclined, "inventory_declined");
            IMsgNames.Add(InstantMessageDialog.GroupVote, "group_vote");
            IMsgNames.Add(InstantMessageDialog.TaskInventoryOffered, "task_inventory_offered");
            IMsgNames.Add(InstantMessageDialog.TaskInventoryAccepted, "task_inventory_accepted");
            IMsgNames.Add(InstantMessageDialog.TaskInventoryDeclined, "task_inventory_declined");
            IMsgNames.Add(InstantMessageDialog.NewUserDefault, "new_user_default");
            IMsgNames.Add(InstantMessageDialog.SessionAdd, "session_add");
            IMsgNames.Add(InstantMessageDialog.SessionOfflineAdd, "session_offline_add");
            IMsgNames.Add(InstantMessageDialog.SessionGroupStart, "session_group_start");
            IMsgNames.Add(InstantMessageDialog.SessionCardlessStart, "session_cardless_start");
            IMsgNames.Add(InstantMessageDialog.SessionSend, "session_send");
            IMsgNames.Add(InstantMessageDialog.SessionDrop, "session_drop");
            IMsgNames.Add(InstantMessageDialog.MessageFromObject, "message_from_object");
            IMsgNames.Add(InstantMessageDialog.BusyAutoResponse, "busy_auto_response");
            IMsgNames.Add(InstantMessageDialog.ConsoleAndChatHistory, "console_and_chat_history");
            IMsgNames.Add(InstantMessageDialog.RequestTeleport, "request_teleport");
            IMsgNames.Add(InstantMessageDialog.AcceptTeleport, "accept_teleport");
            IMsgNames.Add(InstantMessageDialog.DenyTeleport, "deny_teleport");
            IMsgNames.Add(InstantMessageDialog.GodLikeRequestTeleport, "god_like_request_teleport");
            IMsgNames.Add(InstantMessageDialog.RequestLure, "request_lure");
            IMsgNames.Add(InstantMessageDialog.GotoUrl, "goto_url");
            IMsgNames.Add(InstantMessageDialog.Session911Start, "session_911_start");
            IMsgNames.Add(InstantMessageDialog.Lure911, "lure_911");
            IMsgNames.Add(InstantMessageDialog.FromTaskAsAlert, "from_task_as_alert");
            IMsgNames.Add(InstantMessageDialog.GroupNotice, "group_notice");
            IMsgNames.Add(InstantMessageDialog.GroupNoticeInventoryAccepted, "group_notice_inventory_accepted");
            IMsgNames.Add(InstantMessageDialog.GroupNoticeInventoryDeclined, "group_notice_inventory_declined");
            IMsgNames.Add(InstantMessageDialog.GroupInvitationAccept, "group_invitation_accept");
            IMsgNames.Add(InstantMessageDialog.GroupInvitationDecline, "group_invitation_decline");
            IMsgNames.Add(InstantMessageDialog.GroupNoticeRequested, "group_notice_requested");
            IMsgNames.Add(InstantMessageDialog.FriendshipOffered, "friendship_offered");
            IMsgNames.Add(InstantMessageDialog.FriendshipAccepted, "friendship_accepted");
            IMsgNames.Add(InstantMessageDialog.FriendshipDeclined, "friendship_declined");
            IMsgNames.Add(InstantMessageDialog.StartTyping, "start_typing");
            IMsgNames.Add(InstantMessageDialog.StopTyping, "stop_typing");

            TimerUpdate.Start();
        }

        public static string LastFailMsg = null;
        public static string LastOKMsg = null;
        public static bool LastActionOK = true;
        public static bool LastActionException = false;

        public static bool fail(string failmsg)
        {
            LastFailMsg = failmsg;
            LastOKMsg = null;
            LastActionOK = false;
            LastActionException = false;
            return false;
        }
        public static bool fail(Exception ex)
        {
            LastFailMsg = ex.Message;
            LastOKMsg = null;
            LastActionOK = false;
            LastActionException = true;
            return false;
        }

        public static string nulstr(string failmsg)
        {
            VRAgentController.fail(failmsg);
            return null;
        }
        public static List<string> nullst(string failmsg)
        {
            VRAgentController.fail(failmsg);
            return null;
        }
        public static List<List<string>> nulcoll(string failmsg)
        {
            VRAgentController.fail(failmsg);
            return null;
        }
        public static bool ok(string okmsg)
        {
            LastFailMsg = null;
            LastOKMsg = okmsg;
            LastActionOK = true;
            LastActionException = false;
            return true;
        }
        public static string ok(string okmsg, string okresult)
        {
            VRAgentController.ok(okmsg);
            return okresult;
        }
        public static List<string> ok(string okmsg, List<string> okresult)
        {
            VRAgentController.ok(okmsg);
            return okresult;
        }
        public static List<List<string>> ok(string okmsg, List<List<string>> okresult)
        {
            VRAgentController.ok(okmsg);
            return okresult;
        }

        void TerseObjectUpdateEvHandler(object sender, TerseObjectUpdateEventArgs objupdev)
        {
            if (objupdev.Prim.LocalID == Self.LocalID) {
                SetDefaultCamera();
            }
        }

        void AvatarUpdateEvHandler(object sender, AvatarUpdateEventArgs avupdev)
        {
            if (avupdev.Avatar.LocalID == Self.LocalID) {
                SetDefaultCamera();
            }
        }

        void SimChangedEvHandler(object sender, SimChangedEventArgs simchgev)
        {
            Self.Movement.SetFOVVerticalAngle(Utils.TWO_PI - 0.05f);
        }

        public void SetDefaultCamera()
        {
            // SetCamera 5m behind the avatar
            Self.Movement.Camera.LookAt(
                Self.SimPosition + new Vector3(-5, 0, 0) * Self.Movement.BodyRotation,
                Self.SimPosition
            );
        }

        void InstantMessageEvHandler(object sender, InstantMessageEventArgs msgev)
        {
            List<string> msg = new List<string>();
            if (msgev.IM.Dialog==InstantMessageDialog.MessageFromAgent) {
                // Field 0 (VrMsgFld.Typ): type of msg='instmsg'
                msg.Add("instmsg");
                // Field 1 (VrMsgFld.FrmNam): name of source agent/avatar
                msg.Add(msgev.IM.FromAgentName.ToString());
                // Field 2 (VrMsgFld.Cont): message content
                msg.Add(msgev.IM.Message);
                // Field 3 (VrMsgFld.FrmId): ID of source agent/avatar
                msg.Add(msgev.IM.FromAgentID.ToString().ToLower());
                // Field 4 (VrMsgFld.TimStmp): time when recvd msg in fmt YYYY-MM-ddTHH:MM:SS
                msg.Add(msgev.IM.Timestamp.ToString("s"));
                // Fields 5,6,7 (VrMsgFld.PosX,PosY,PosZ): X,Y,Z coords of source agent/avatar
                msg.Add(msgev.IM.Position.X.ToString());
                msg.Add(msgev.IM.Position.Y.ToString());
                msg.Add(msgev.IM.Position.Z.ToString());
                lock (RecvdVRMsgsLock) {
                    RecvdVRMsgs.Add(msg);
                }
            } else {
                string imsgcode;
                if (!IMsgNames.TryGetValue(msgev.IM.Dialog, out imsgcode))
                    return;
                string groupsession = msgev.IM.GroupIM ? "group" : "session";
                // Field 0 (VrMsgFld.Typ): type of msg='codemsg'
                msg.Add("codemsg");
                // Field 1 (VrMsgFld.FrmNam): name of source agent/avatar
                msg.Add(msgev.IM.FromAgentName.ToString());
                // Field 2 (VrMsgFld.Cont): message content
                msg.Add(msgev.IM.Message);
                // Field 3 (VrMsgFld.FrmId): ID of source agent/avatar
                msg.Add(msgev.IM.FromAgentID.ToString().ToLower());
                // Field 4 (VrMsgFld.TimStmp): time when recvd msg in fmt YYYY-MM-ddTHH:MM:SS
                msg.Add(msgev.IM.Timestamp.ToString("s"));
                // Fields 5,6,7 (VrMsgFld.PosX,PosY,PosZ): X,Y,Z coords of source agent/avatar
                msg.Add(msgev.IM.Position.X.ToString());
                msg.Add(msgev.IM.Position.Y.ToString());
                msg.Add(msgev.IM.Position.Z.ToString());
                // Field 8 (VrMsgFld.CodeTyp): type of codemsg (specific for code msgs)
                msg.Add(imsgcode);
                // Field 9 (VrMsgFld.GrpSes): indicates if it is 'group' or 'session' (specific for code msgs)
                msg.Add(groupsession);
                // Field 10 (VrMsgFld.GrpSesId): ID of group, for 'group' codemsg or 
                // ID of session for 'session' codemsg (specific for code msgs)
                msg.Add(msgev.IM.IMSessionID.ToString());
                lock (RecvdVRMsgsLock) {
                    RecvdVRMsgs.Add(msg);
                }
            }
        }


        void ChatEvHandler(object sender, ChatEventArgs chatev)
        {
            string chattype;
            if (chatev.Type == ChatType.Normal)
                chattype = "say";
            else if (chatev.Type == ChatType.Shout)
                chattype = "shout";
            else if (chatev.Type == ChatType.Whisper)
                chattype = "whisper";
            else
                return;
            if (chatev.Message == "")
                return; //WTF???? why do i get empty messages which are not the above types				
            List<string> msg = new List<string>();
            // Field 0 (VrMsgFld.Typ): type of msg='chatmsg'
            msg.Add("chatmsg");
            // Field 1 (VrMsgFld.FrmNam): name of source agent/avatar
            msg.Add(chatev.FromName.ToString());
            // Field 2 (VrMsgFld.Cont): message content
            msg.Add(chatev.Message);
            // Field 3 (VrMsgFld.FrmId): ID of source agent/avatar
            msg.Add(chatev.SourceID.ToString().ToLower());
            // Field 4 (VrMsgFld.TimStmp): time when recvd msg in fmt YYYY-MM-ddTHH:MM:SS
            msg.Add(DateTime.Now.ToString("s"));
            // Fields 5,6,7 (VrMsgFld.PosX,PosY,PosZ): X,Y,Z coords of source agent/avatar
            msg.Add(chatev.Position.X.ToString());
            msg.Add(chatev.Position.Y.ToString());
            msg.Add(chatev.Position.Z.ToString());
            // Field 8 (VrMsgFld.ChatTyp): type of chatmsg (specific for chat 
            // msgs: whisper, say, shout)
            msg.Add(chattype);
            // Field 9 (VrMsgFld.AudLev): audible level of chatmsg (specific for chat 
            // msgs: not, barely, fully)
            msg.Add(chatev.AudibleLevel.ToString().ToLower());
            // Field 10 (VrMsgFld.SrcTyp): source type of chatmsg (specific for chat 
            // msgs: system, agent, object)
            msg.Add(chatev.SourceType.ToString().ToLower());
            lock (RecvdVRMsgsLock) {
                RecvdVRMsgs.Add(msg);
            }

        }

        void MeanCollisionEvHandler(object sender, MeanCollisionEventArgs meancoll)
        {
            Console.WriteLine("Collision with: {0}, type: {1}, magnitude: {2}, time: {3}, victim",
                            meancoll.Aggressor.ToString(), meancoll.Type.ToString().ToLower(), meancoll.Magnitude.ToString(),
                            meancoll.Time.ToString(), meancoll.Victim.ToString());
            List<string> vrev = new List<string>();
            vrev.Add("collis");
            vrev.Add(meancoll.Aggressor.ToString());
            vrev.Add(meancoll.Type.ToString().ToLower());
            vrev.Add(meancoll.Magnitude.ToString());
            vrev.Add(meancoll.Victim.ToString());
            vrev.Add(meancoll.Time.ToShortDateString() + " " + meancoll.Time.ToShortTimeString());
            lock (DetcdVREventsLock) {
                DetcdVREvents.Add(vrev);
            }
        }

        void RegionCrossedEvHandler(object sender, RegionCrossedEventArgs rgncrossev)
        {
            Console.WriteLine("Crossed to region: {0}, from region: {1}",
                            rgncrossev.NewSimulator.ToString(), rgncrossev.OldSimulator.ToString());
            //string msg = "region_crossed( '" + rgncrossev.NewSimulator.ToString() + "','" + 
            //            rgncrossev.OldSimulator.ToString() + "').";
            List<string> vrev = new List<string>();
            vrev.Add("crossrgn");
            vrev.Add(rgncrossev.NewSimulator.ToString());
            vrev.Add(rgncrossev.OldSimulator.ToString());
            lock (DetcdVREventsLock) {
                DetcdVREvents.Add(vrev);
            }
        }

        public void LoginProgressEvHandler(object sender, LoginProgressEventArgs lognprogev)
        {
            if (lognprogev.Status == LoginStatus.Success) {
                // Start in the inventory root folder.
                CurrentDirectory = Inventory.Store.RootFolder;
            }
        }

        public void ReloadGroupsCache()
        {
            Groups.CurrentGroups +=
                new EventHandler<CurrentGroupsEventArgs>(CurrentGroupsEvHandler);
            Groups.RequestCurrentGroups();
            GroupsEvent.WaitOne(10000, false);
            Groups.CurrentGroups -= CurrentGroupsEvHandler;
            GroupsEvent.Reset();
        }

        void CurrentGroupsEvHandler(object sender, CurrentGroupsEventArgs currgrpev)
        {
            if (null == GroupsCache)
                GroupsCache = currgrpev.Groups;
            else
                lock (GroupsCache) { GroupsCache = currgrpev.Groups; }
            GroupsEvent.Set();
        }

        public UUID GroupName2UUID(String groupName)
        {
            UUID tryUUID;
            if (UUID.TryParse(groupName, out tryUUID))
                return tryUUID;
            if (null == GroupsCache) {
                ReloadGroupsCache();
                if (null == GroupsCache)
                    return UUID.Zero;
            }
            lock (GroupsCache) {
                if (GroupsCache.Count > 0) {
                    foreach (Group currentGroup in GroupsCache.Values)
                        if (currentGroup.Name.ToLower() == groupName.ToLower())
                            return currentGroup.ID;
                }
            }
            return UUID.Zero;
        }


        private void TimerUpdateEvHandler(object sender, System.Timers.ElapsedEventArgs timupdev)
        {
            lock (TimerTasks) {
                foreach (TimerTask tt in TimerTasks) {
                    if (tt.Active)
                        tt.RunTask();
                }
            }
        }

        private void AgentDataUpdateCallback(object sender, PacketReceivedEventArgs agupdev)
        {
            AgentDataUpdatePacket p = (AgentDataUpdatePacket)agupdev.Packet;
            if (p.AgentData.AgentID == agupdev.Simulator.Client.Self.AgentID) {

            }
        }

        private void AvatarAppearanceCallback(object sender, PacketReceivedEventArgs avappearev)
        {
            Packet packet = avappearev.Packet;
            AvatarAppearancePacket appearance = (AvatarAppearancePacket)packet;
            lock (Appearances) Appearances[appearance.Sender.ID] = appearance;
        }

        private void AlertMessageCallback(object sender, PacketReceivedEventArgs alrtmsgev)
        {
            Packet packet = alrtmsgev.Packet;
            AlertMessagePacket message = (AlertMessagePacket)packet;
            Logger.Log("[AlertMessage] " + Utils.BytesToString(message.AlertData.Message), Helpers.LogLevel.Info, this);
        }

        private void InventoryObjectOfferedEvHandler(object sender, InventoryObjectOfferedEventArgs invobjoffev)
        {
            invobjoffev.Accept = true;
            return;
        }





    }
}
