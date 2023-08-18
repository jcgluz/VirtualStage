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
//   Class:     Actions 
//   Purpose:   This superclass implements some methods and fields used
//              by other action classes
//   Author:    João Carlos Gluz 
//
//***********************************************************************


using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

#if USE_LIBREMETAVERSE_VR_LIB
namespace LibreMetaverse
#else
namespace OpenMetaverse
#endif
{

    public enum RezActionObjType : int
    {
        prim = 0,
        tree = 1,
        grass = 2,
        item = 3,
        invalid = 255
    }

    public class Actions
    {
        public VRAgentController Agent;

        // Dictionaries that need "manual" initialization
        public Dictionary<string, PrimType> PrimTypes = new Dictionary<string, PrimType>();
        public Dictionary<string, Tree> TreeTypes = new Dictionary<string, Tree>();
        public Dictionary<string, Grass> GrassTypes = new Dictionary<string, Grass>();
        public Dictionary<string, Material> MatTypes = new Dictionary<string, Material>();
        public Dictionary<string, AttachmentPoint> AttachPoints = new Dictionary<string, AttachmentPoint>();
        public Dictionary<string, InstantMessageDialog> IMsgTypes = new Dictionary<string, InstantMessageDialog>();

        // Dictionaries with "automatic" initialization
        public Dictionary<UUID, string> StdAnimations = new Dictionary<UUID, string>(Animations.ToDictionary());

        public Actions(VRAgentController agent)
        {
            Agent = agent;

            // Dictionaries that need "manual" initialization
            MatTypes.Add("flesh", Material.Flesh);
            MatTypes.Add("glass", Material.Glass);
            MatTypes.Add("light", Material.Light);
            MatTypes.Add("metal", Material.Metal);
            MatTypes.Add("plastic", Material.Plastic);
            MatTypes.Add("rubber", Material.Rubber);
            MatTypes.Add("stone", Material.Stone);
            MatTypes.Add("wood", Material.Wood);

            PrimTypes.Add("box", PrimType.Box);
            PrimTypes.Add("cylinder", PrimType.Cylinder);
            PrimTypes.Add("prism", PrimType.Prism);
            PrimTypes.Add("sphere", PrimType.Sphere);
            PrimTypes.Add("torus", PrimType.Torus);
            PrimTypes.Add("tube", PrimType.Tube);
            PrimTypes.Add("ring", PrimType.Ring);
            PrimTypes.Add("sculpt", PrimType.Sculpt);
            PrimTypes.Add("mesh", PrimType.Mesh);
            PrimTypes.Add("unknown", PrimType.Unknown);

            TreeTypes.Add("pine1", Tree.Pine1);
            TreeTypes.Add("oak", Tree.Oak);
            TreeTypes.Add("tropicalbush1", Tree.TropicalBush1);
            TreeTypes.Add("palm1", Tree.Palm1);
            TreeTypes.Add("dogwood", Tree.Dogwood);
            TreeTypes.Add("tropicalbush2", Tree.TropicalBush2);
            TreeTypes.Add("palm2", Tree.Palm2);
            TreeTypes.Add("cypress1", Tree.Cypress1);
            TreeTypes.Add("cypress2", Tree.Cypress2);
            TreeTypes.Add("pine2", Tree.Pine2);
            TreeTypes.Add("plumeria", Tree.Plumeria);
            TreeTypes.Add("winterpine1", Tree.WinterPine1);
            TreeTypes.Add("winteraspen", Tree.WinterAspen);
            TreeTypes.Add("winterpine2", Tree.WinterPine2);
            TreeTypes.Add("eucalyptus", Tree.Eucalyptus);
            TreeTypes.Add("fern", Tree.Fern);
            TreeTypes.Add("eelgrass", Tree.Eelgrass);
            TreeTypes.Add("seasword", Tree.SeaSword);
            TreeTypes.Add("kelp1", Tree.Kelp1);
            TreeTypes.Add("beachgrass1", Tree.BeachGrass1);
            TreeTypes.Add("kelp2", Tree.Kelp2);

            GrassTypes.Add("grass0", Grass.Grass0);
            GrassTypes.Add("grass1", Grass.Grass1);
            GrassTypes.Add("grass2", Grass.Grass2);
            GrassTypes.Add("grass3", Grass.Grass3);
            GrassTypes.Add("grass4", Grass.Grass4);
            GrassTypes.Add("undergrowth1", Grass.Undergrowth1);

            AttachPoints.Add("default", AttachmentPoint.Default);
            AttachPoints.Add("chest", AttachmentPoint.Chest);
            AttachPoints.Add("head", AttachmentPoint.Skull);
            AttachPoints.Add("left_shoulder", AttachmentPoint.LeftShoulder);
            AttachPoints.Add("right_shoulder", AttachmentPoint.RightShoulder);
            AttachPoints.Add("left_hand", AttachmentPoint.LeftHand);
            AttachPoints.Add("right_hand", AttachmentPoint.RightHand);
            AttachPoints.Add("left_foot", AttachmentPoint.LeftFoot);
            AttachPoints.Add("right_foot", AttachmentPoint.RightFoot);
            AttachPoints.Add("back", AttachmentPoint.Spine);
            AttachPoints.Add("pelvis", AttachmentPoint.Pelvis);
            AttachPoints.Add("mouth", AttachmentPoint.Mouth);
            AttachPoints.Add("chin", AttachmentPoint.Chin);
            AttachPoints.Add("left_ear", AttachmentPoint.LeftEar);
            AttachPoints.Add("right_ear", AttachmentPoint.RightEar);
            AttachPoints.Add("left_eye", AttachmentPoint.LeftEyeball);
            AttachPoints.Add("right_eye", AttachmentPoint.RightEyeball);
            AttachPoints.Add("nose", AttachmentPoint.Nose);
            AttachPoints.Add("right_upper_arm", AttachmentPoint.RightUpperArm);
            AttachPoints.Add("right_lower_arm", AttachmentPoint.RightForearm);
            AttachPoints.Add("left_upper_arm", AttachmentPoint.LeftUpperArm);
            AttachPoints.Add("left_lower_arm", AttachmentPoint.LeftForearm);
            AttachPoints.Add("right_hip", AttachmentPoint.RightHip);
            AttachPoints.Add("right_upper_leg", AttachmentPoint.RightUpperLeg);
            AttachPoints.Add("right_lower_leg", AttachmentPoint.RightLowerLeg);
            AttachPoints.Add("left_hip", AttachmentPoint.LeftHip);
            AttachPoints.Add("left_upper_leg", AttachmentPoint.LeftUpperLeg);
            AttachPoints.Add("left_lower_leg", AttachmentPoint.LeftForearm);
            AttachPoints.Add("belly", AttachmentPoint.Stomach);
            AttachPoints.Add("left_pec", AttachmentPoint.LeftPec);
            AttachPoints.Add("right_pec", AttachmentPoint.RightPec);
            AttachPoints.Add("neck", AttachmentPoint.Neck);
            AttachPoints.Add("center", AttachmentPoint.Root);

            IMsgTypes.Add("message_from_agent", InstantMessageDialog.MessageFromAgent);
            IMsgTypes.Add("message_box", InstantMessageDialog.MessageBox);
            IMsgTypes.Add("group_invitation", InstantMessageDialog.GroupInvitation);
            IMsgTypes.Add("inventory_offered", InstantMessageDialog.InventoryOffered);
            IMsgTypes.Add("inventory_accepted", InstantMessageDialog.InventoryAccepted);
            IMsgTypes.Add("inventory_declined", InstantMessageDialog.InventoryDeclined);
            IMsgTypes.Add("group_vote", InstantMessageDialog.GroupVote);
            IMsgTypes.Add("task_inventory_offered", InstantMessageDialog.TaskInventoryOffered);
            IMsgTypes.Add("task_inventory_accepted", InstantMessageDialog.TaskInventoryAccepted);
            IMsgTypes.Add("task_inventory_declined", InstantMessageDialog.TaskInventoryDeclined);
            IMsgTypes.Add("new_user_default", InstantMessageDialog.NewUserDefault);
            IMsgTypes.Add("session_add", InstantMessageDialog.SessionAdd);
            IMsgTypes.Add("session_offline_add", InstantMessageDialog.SessionOfflineAdd);
            IMsgTypes.Add("session_group_start", InstantMessageDialog.SessionGroupStart);
            IMsgTypes.Add("session_cardless_start", InstantMessageDialog.SessionCardlessStart);
            IMsgTypes.Add("session_send", InstantMessageDialog.SessionSend);
            IMsgTypes.Add("session_drop", InstantMessageDialog.SessionDrop);
            IMsgTypes.Add("message_from_object", InstantMessageDialog.MessageFromObject);
            IMsgTypes.Add("busy_auto_response", InstantMessageDialog.BusyAutoResponse);
            IMsgTypes.Add("console_and_chat_history", InstantMessageDialog.ConsoleAndChatHistory);
            IMsgTypes.Add("request_teleport", InstantMessageDialog.RequestTeleport);
            IMsgTypes.Add("accept_teleport", InstantMessageDialog.AcceptTeleport);
            IMsgTypes.Add("deny_teleport", InstantMessageDialog.DenyTeleport);
            IMsgTypes.Add("god_like_request_teleport", InstantMessageDialog.GodLikeRequestTeleport);
            IMsgTypes.Add("request_lure", InstantMessageDialog.RequestLure);
            IMsgTypes.Add("goto_url", InstantMessageDialog.GotoUrl);
            IMsgTypes.Add("session911start", InstantMessageDialog.Session911Start);
            IMsgTypes.Add("lure911", InstantMessageDialog.Lure911);
            IMsgTypes.Add("from_task_as_alert", InstantMessageDialog.FromTaskAsAlert);
            IMsgTypes.Add("group_notice", InstantMessageDialog.GroupNotice);
            IMsgTypes.Add("group_notice_inventory_accepted", InstantMessageDialog.GroupNoticeInventoryAccepted);
            IMsgTypes.Add("group_notice_inventory_declined", InstantMessageDialog.GroupNoticeInventoryDeclined);
            IMsgTypes.Add("group_invitation_accept", InstantMessageDialog.GroupInvitationAccept);
            IMsgTypes.Add("group_invitation_decline", InstantMessageDialog.GroupInvitationDecline);
            IMsgTypes.Add("group_notice_requested", InstantMessageDialog.GroupNoticeRequested);
            IMsgTypes.Add("friendship_offered", InstantMessageDialog.FriendshipOffered);
            IMsgTypes.Add("friendship_accepted", InstantMessageDialog.FriendshipAccepted);
            IMsgTypes.Add("friendship_declined", InstantMessageDialog.FriendshipDeclined);
            IMsgTypes.Add("start_typing", InstantMessageDialog.StartTyping);
            IMsgTypes.Add("stop_typing", InstantMessageDialog.StopTyping);
        }


    }
}
