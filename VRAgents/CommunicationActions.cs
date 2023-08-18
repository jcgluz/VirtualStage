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
//   Class:     CommunicationActions 
//   Purpose:   To implement actions for the agent to be able to communicate
//              with others avatars on virtual world 
//   Author:    João Carlos Gluz 
//
//***********************************************************************
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
#if USE_LIBREMETAVERSE_VR_LIB
using LibreMetaverse;
using LibreMetaverse.Packets;
#else
using OpenMetaverse;
using OpenMetaverse.Packets;
#endif

#if USE_LIBREMETAVERSE_VR_LIB
namespace LibreMetaverse
#else
namespace OpenMetaverse
#endif
{
    public class CommunicationActions : Actions
    {
        public CommunicationActions(VRAgentController agent) : base(agent)
        {
            agent.Avatars.AvatarPickerReply += AvatarPickerReplyHandler;
        }

        public List<List<string>> LookForMsgs()
        {
            List<List<string>> results = new List<List<string>>();
            lock (Agent.RecvdVRMsgsLock) {
                results = Agent.RecvdVRMsgs;
                Agent.RecvdVRMsgs = new List<List<string>>();
            }
            return VRAgentController.ok("last recvd VR msgs", results);
        }

        public List<List<string>> LookForMsgs(string argtype)
        {
            if (String.IsNullOrEmpty(argtype)) {
                return LookForMsgs();
            }
            List<List<string>> results = new List<List<string>>();
            lock (Agent.RecvdVRMsgsLock) {
                Agent.RecvdVRMsgs.RemoveAll(msg => {
                        // index 0 of list has the type of msg (imsg, chatmsg or codemsg)
                        if (msg[VRMsgFld.Typ] == argtype) { results.Add(msg); return true; } 
                        else return false;
                    }
                );
            }
            return VRAgentController.ok("last recvd VR msgs", results);
        }

        public List<List<string>> LookForMsgsFrom(string argtype, string argopt, string argval)
        {
            List<List<string>> results = new List<List<string>>();
            if (String.IsNullOrEmpty(argtype) && String.IsNullOrEmpty(argval)) {
                return LookForMsgs();
            }
            if (String.IsNullOrEmpty(argtype)) {
                if (String.IsNullOrEmpty(argopt))
                    return VRAgentController.ok("invalid param 2 - no msgs", results);
                if (argopt.ToLower() == "name") {
                    lock (Agent.RecvdVRMsgsLock) {
                        Agent.RecvdVRMsgs.RemoveAll(msg => {
                            // Field 1 (VRMsgFld.FrmNam) of msg has source name (avatar or object)
                            if (msg[VRMsgFld.FrmNam] == argval) 
                                { results.Add(msg); return true; } 
                            else return false;
                        }
                        );
                    }
                } else if (argopt.ToLower() == "id") {
                    lock (Agent.RecvdVRMsgsLock) {
                        Agent.RecvdVRMsgs.RemoveAll(msg => {
                            // Field 3 (VRMsgFld.FrmID) of msg has source ID (avatar or object)
                            if (msg[VRMsgFld.FrmID] == argval) 
                                { results.Add(msg); return true; } 
                            else return false;
                        }
                        );
                    }
                } else {
                    return VRAgentController.ok("invalid param 2 - no msgs", results);
                }
                return VRAgentController.ok("last recvd VR msgs", results);
            }

            if (argopt.ToLower()=="name") {
                lock (Agent.RecvdVRMsgsLock) {
                    Agent.RecvdVRMsgs.RemoveAll( msg => {
                            // Field 0 (VRMsgFld.Typ) of msg has type of msg (imsg, chatmsg or codemsg)
                            // Field 1 (VRMsgFld.FrmNam) of msg has source name (avatar or object)
                            if (msg[VRMsgFld.Typ] ==argtype && msg[VRMsgFld.FrmNam] ==argval) 
                                {results.Add(msg);return true; } 
                            else return false;  
                        }
                    );
                }
            } else if (argopt.ToLower()=="id") {
                lock (Agent.RecvdVRMsgsLock) {
                    Agent.RecvdVRMsgs.RemoveAll(msg => {
                            // Field 0 (VRMsgFld.Typ) of msg has type of msg (imsg, chatmsg or codemsg)
                            // Field 3 (VRMsgFld.FrmID) of msg has source ID (avatar or object)
                            if (msg[VRMsgFld.Typ] ==argtype && msg[VRMsgFld.FrmID] ==argval)
                                    { results.Add(msg); return true; } 
                            else return false;
                        }
                    );
                }
            } else {
                return VRAgentController.ok("invalid option - no msgs", results);
            }
            return VRAgentController.ok("last recvd VR msgs", results);
        }

        public List<List<string>> LookForCodeMsgs(string argcode)
        {
            List<List<string>> results = new List<List<string>>();
            if (String.IsNullOrEmpty(argcode))
                return VRAgentController.ok("invalid param - no msgs",results);
            lock (Agent.RecvdVRMsgsLock) {
                Agent.RecvdVRMsgs.RemoveAll(msg => {
                        // Field 0 (VRMsgFld.Typ) of msg has type of msg (imsg, chatmsg or codmsg)
                        // Field 8 (VRMsgFld.CodeTyp) of msg has the code of code msgs
                        if (msg[VRMsgFld.Typ]=="codemsg" && msg[VRMsgFld.CodeTyp]==argcode)
                                { results.Add(msg); return true; } 
                        else return false;
                    }
                );
            }
            return VRAgentController.ok("last recvd code msgs", results);
        }



        public List<List<string>> LookForCodeMsgsFrom(string argcode, string argopt, string argval)
        {
            List<List<string>> results = new List<List<string>>();
            if (String.IsNullOrEmpty(argcode) || String.IsNullOrEmpty(argopt) ||
                String.IsNullOrEmpty(argval))
                return VRAgentController.ok("invalid params - no msgs", results);
            if (argopt.ToLower()=="name") {
                lock (Agent.RecvdVRMsgsLock) {
                    Agent.RecvdVRMsgs.RemoveAll( msg => {
                            // Field 0 (VRMsgFld.Typ) of msg has type of msg (imsg, chatmsg or codemsg)
                            // Field 1 (VRMsgFld.FrmNam) of msg has source name (avatar or object)
                            // Field 8 (VRMsgFld.CodeTyp) of msg has the code of code msgs
                            if (msg[VRMsgFld.Typ] =="codemsg" && msg[VRMsgFld.FrmNam] ==argval
                                && msg[VRMsgFld.CodeTyp]==argcode) 
                                    {results.Add(msg);return true; } 
                            else return false;  
                        }
                    );
                }
            } else if (argopt.ToLower()=="id") {
                lock (Agent.RecvdVRMsgsLock) {
                    Agent.RecvdVRMsgs.RemoveAll(msg => {
                            // Field 0 (VRMsgFld.Typ) of msg has type of msg (imsg, chatmsg or codemsg)
                            // Field 3 (VRMsgFld.FrmID) of msg has source ID (avatar or object)
                            // Field 8 (VRMsgFld.CodeTyp) of msg has the code of code msgs
                            if (msg[VRMsgFld.Typ] =="codemsg" && msg[VRMsgFld.FrmID] ==argval
                                && msg[VRMsgFld.CodeTyp] == argcode)
                                    { results.Add(msg); return true; } 
                            else return false;
                        }
                    );
                }
            } else {
                return VRAgentController.ok("invalid option - no msgs",results);
            }
            return VRAgentController.ok("last recvd code msgs", results);
        }


        public bool ChatAction(string argchann, string argtype, string argmsg)
        {
            int channel = 0;
            if (!Int32.TryParse(argchann, out channel)) {
                return (VRAgentController.fail("param 1 invalid channel"));
            }
            if (argtype == "say")
                Agent.Self.Chat(argmsg, channel, ChatType.Normal);
            else if (argtype == "shout")
                Agent.Self.Chat(argmsg, channel, ChatType.Shout);
            else if (argtype == "whisper")
                Agent.Self.Chat(argmsg, channel, ChatType.Whisper);
            else
                return VRAgentController.fail("param 2 invalid option");
            return VRAgentController.ok("sending chatmsg");
        }

        public bool SayAction(int argchann, string argmsg)
        {
            Agent.Self.Chat(argmsg, argchann, ChatType.Normal);
            return VRAgentController.ok("saying msg");
        }

        public bool ShoutAction(int argchann, string argmsg)
        {
            Agent.Self.Chat(argmsg, argchann, ChatType.Shout);
            return VRAgentController.ok("shouting msg");
        }

        public bool WhisperAction(int argchann, string argmsg)
        {
            Agent.Self.Chat(argmsg, argchann, ChatType.Whisper);
            return VRAgentController.ok("whispering msg");
        }


        string ToAvatarName = String.Empty;
        ManualResetEvent NameSearchEvent = new ManualResetEvent(false);
        Dictionary<string, UUID> Name2Key = new Dictionary<string, UUID>();

        public bool SendInstMsgAction(string argavname, string argmsg)
        {
            ToAvatarName = argavname;
            if (!Name2Key.ContainsKey(ToAvatarName.ToLower())) {
                // Send the Query
                Agent.Avatars.RequestAvatarNameSearch(ToAvatarName, UUID.Random());
                NameSearchEvent.WaitOne(6000, false);
            }
            if (Name2Key.ContainsKey(ToAvatarName.ToLower())) {
                UUID id = Name2Key[ToAvatarName.ToLower()];
                Agent.Self.InstantMessage(id, argmsg);
                return VRAgentController.ok("sending instmsg");
            } else {
                return VRAgentController.fail("avatar not found");
            }
        }

        public bool SendInstMsgAction(string argavname, string argmsg, string argsessid)
        {
            UUID sessionID;
            if (!UUID.TryParse(argsessid, out sessionID))
                return VRAgentController.fail("invalid session id");
            ToAvatarName = argavname;
            if (!Name2Key.ContainsKey(ToAvatarName.ToLower())) {
                // Send the Query
                Agent.Avatars.RequestAvatarNameSearch(ToAvatarName, UUID.Random());
                NameSearchEvent.WaitOne(6000, false);
            }
            if (Name2Key.ContainsKey(ToAvatarName.ToLower())) {
                UUID id = Name2Key[ToAvatarName.ToLower()];
                Agent.Self.InstantMessage(id, argmsg, sessionID);
                return VRAgentController.ok("sending instmsg");
            } else {
                return VRAgentController.fail("avatar not found");
            }
        }


        public bool SendCodeMsgAction(string argcode, string argavname, 
                string arggrpsesid, string argmsg)
        {
            InstantMessageDialog imsgtyp;
            if (!IMsgTypes.TryGetValue(argcode, out imsgtyp))
                return VRAgentController.fail("param 1 invalid code");
            UUID groupSessionID;
            if (!UUID.TryParse(arggrpsesid, out groupSessionID))
                return VRAgentController.fail("param 3 invalid session id");

            ToAvatarName = argavname;
            if (!Name2Key.ContainsKey(ToAvatarName.ToLower())) {
                // Send the Query
                Agent.Avatars.RequestAvatarNameSearch(ToAvatarName, UUID.Random());
                NameSearchEvent.WaitOne(6000, false);
            }
            if (Name2Key.ContainsKey(ToAvatarName.ToLower())) {
                UUID id = Name2Key[ToAvatarName.ToLower()];
                Agent.Self.InstantMessage(Agent.Self.Name, 
                    id, argmsg, groupSessionID,
                    imsgtyp, InstantMessageOnline.Offline, 
                    Agent.Self.SimPosition,
                    UUID.Zero, Utils.EmptyBytes);
                return VRAgentController.ok("sending codemsg");
            } else {
                return VRAgentController.fail("avatar not found");
            }
        }

        private ManualResetEvent WaitForJoinGroupChat = new ManualResetEvent(false);

        public bool SendMsgToGroupAction(string arggrp, string argmsg)
        {
            UUID toGroupID = UUID.Zero;
            if (!UUID.TryParse(arggrp, out toGroupID)) {
                return VRAgentController.fail("param 1 error");
            }
            if (argmsg.Length > 1023) {
                argmsg = argmsg.Remove(1023);
            }
            Agent.Self.GroupChatJoined += GroupChatJoinedHandler;
            if (!Agent.Self.GroupChatSessions.ContainsKey(toGroupID)) {
                WaitForJoinGroupChat.Reset();
                Agent.Self.RequestJoinGroupChat(toGroupID);
            } else {
                WaitForJoinGroupChat.Set();
            }
            if (WaitForJoinGroupChat.WaitOne(20000, false)) {
                Agent.Self.InstantMessageGroup(toGroupID, argmsg);
            } else {
                return VRAgentController.fail("timeout to join group");
            }
            Agent.Self.GroupChatJoined -= GroupChatJoinedHandler;
            return VRAgentController.ok("msg sent to group");
        }

        void GroupChatJoinedHandler(object sender, GroupChatJoinedEventArgs grpchatev)
        {
            if (grpchatev.Success) {
                WaitForJoinGroupChat.Set();
            }
        }

        void AvatarPickerReplyHandler(object sender, AvatarPickerReplyEventArgs avpickev)
        {
            foreach (KeyValuePair<UUID, string> kvp in avpickev.Avatars) {
                if (kvp.Value.ToLower() == ToAvatarName.ToLower()) {
                    Name2Key[ToAvatarName.ToLower()] = kvp.Key;
                    NameSearchEvent.Set();
                    return;
                }
            }
        }

    }
}
