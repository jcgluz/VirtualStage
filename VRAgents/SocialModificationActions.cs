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
//   Class:     SocialModificationActions 
//   Purpose:   To implement actions for agents be able to modify their
//              social relationships with other avatars on virtual world
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
    public class SocialModificationActions : Actions
    {
        public SocialModificationActions(VRAgentController agent) : base(agent)
        {
        }

        private ManualResetEvent ActivateGroupEvent = new ManualResetEvent(false);
        string ActiveGroup;

        public bool ActivateGroupAction(string arggrpidname)
        {
            ActiveGroup = string.Empty;
            UUID groupUUID = Agent.GroupName2UUID(arggrpidname);
            if (UUID.Zero != groupUUID) {
                EventHandler<PacketReceivedEventArgs> pcallback = AgentDataUpdateHandler;
                Agent.Network.RegisterCallback(PacketType.AgentDataUpdate, pcallback);
                Agent.Groups.ActivateGroup(groupUUID);
                ActivateGroupEvent.WaitOne(30000, false);
                Agent.Network.UnregisterCallback(PacketType.AgentDataUpdate, pcallback);
                ActivateGroupEvent.Reset();
                /* A.Biondi 
                 * TODO: Handle titles choosing.
                 */
                if (String.IsNullOrEmpty(ActiveGroup))
                    return VRAgentController.fail("cannot activate group");
                return VRAgentController.ok("group activated");
            }
            return VRAgentController.fail("not group member");
        }

        private void AgentDataUpdateHandler(object sender, PacketReceivedEventArgs agupdev)
        {
            AgentDataUpdatePacket agupddata = (AgentDataUpdatePacket)agupdev.Packet;
            if (agupddata.AgentData.AgentID == Agent.Self.AgentID) {
                ActiveGroup = Utils.BytesToString(agupddata.AgentData.GroupName) + 
                    " ( " + Utils.BytesToString(agupddata.AgentData.GroupTitle) + " )";
                ActivateGroupEvent.Set();
            }
        }


        public bool InviteGroupAction(string argavname, 
                        string arggrpidname)
        {
            return InviteGroupAction(argavname, arggrpidname, "", "", "");
        }

        public bool InviteGroupAction(string argavname,
                        string arggrpidname, string arggrprole)
        {
            return InviteGroupAction(argavname, arggrpidname, arggrprole, "", "");
        }

        public bool InviteGroupAction(string argavname,
                        string arggrpidname, string arggrprole1,
                        string arggrprole2)
        {
            return InviteGroupAction(argavname, arggrpidname, arggrprole1, arggrprole2, "");
        }

        public bool InviteGroupAction(string argavname,
                        string arggrpidname, string arggrprole1, 
                        string arggrprole2, string arggrprole3)
        {
            UUID avatar = UUID.Zero;
            UUID group = UUID.Zero;
            UUID role = UUID.Zero;
            List<UUID> roles = new List<UUID>();
            if (!UUID.TryParse(argavname, out avatar))
                return VRAgentController.fail("param 1 error");
            group = Agent.GroupName2UUID(arggrpidname);
            if (UUID.Zero == group)
                return VRAgentController.fail("param 2 error");
            roles.Add(UUID.Zero);
            if (UUID.TryParse(arggrprole1, out role))
                roles.Add(role);
            if (UUID.TryParse(arggrprole2, out role))
                roles.Add(role);
            if (UUID.TryParse(arggrprole3, out role))
                roles.Add(role);
            Agent.Groups.Invite(group, roles, avatar);
            return VRAgentController.ok("invited");
        }

        ManualResetEvent WaitForGroupsSearchEvent = new ManualResetEvent(false);
        private UUID SearchGroupsQueryID = UUID.Zero;
        private UUID ResolvedGroupID;
        private string SearchGroupName;
        private string ResolvedGroupName;
        private bool JoinedGroup;

        public bool JoinGroupAction(string arggrpidname)
        {
            SearchGroupName = String.Empty;
            ResolvedGroupID = UUID.Zero;
            ResolvedGroupName = String.Empty;
            if (UUID.TryParse((arggrpidname), out ResolvedGroupID)) {
                ResolvedGroupName = arggrpidname;
            } else {
                Agent.Directory.DirGroupsReply += JoinSearchGroupsReplyHandler;
                SearchGroupName = arggrpidname;
                SearchGroupsQueryID = Agent.Directory.StartGroupSearch(SearchGroupName, 0);
                WaitForGroupsSearchEvent.WaitOne(60000, false);
                Agent.Directory.DirGroupsReply -= JoinSearchGroupsReplyHandler;
                WaitForGroupsSearchEvent.Reset();
                if (ResolvedGroupID == UUID.Zero)
                    return VRAgentController.fail("group not found");
            }
            Agent.Groups.GroupJoinedReply += GroupJoinedHandler;
            Agent.Groups.RequestJoinGroup(ResolvedGroupID);
            WaitForGroupsSearchEvent.WaitOne(60000, false);
            Agent.Groups.GroupJoinedReply -= GroupJoinedHandler;
            WaitForGroupsSearchEvent.Reset();
            Agent.ReloadGroupsCache();
            if (JoinedGroup)
                return VRAgentController.ok("joined the group");
            return VRAgentController.fail("unable to join");
        }

        void JoinSearchGroupsReplyHandler(object sender, DirGroupsReplyEventArgs dirgrpev)
        {
            if (SearchGroupsQueryID != dirgrpev.QueryID)
                return;
            SearchGroupsQueryID = UUID.Zero;
            if (dirgrpev.MatchedGroups.Count > 1) {
                /* A.Biondi 
                * The Group search doesn't work as someone could expect...
                * It'll give back to you a long list of groups even if the 
                * searchText (groupName) matches exactly one of the groups 
                * names present on the server, so we need to check each results.
                */
                foreach (DirectoryManager.GroupSearchData groupRetrieved in dirgrpev.MatchedGroups) {
                    if (groupRetrieved.GroupName.ToLower() == SearchGroupName.ToLower()) {
                        ResolvedGroupID = groupRetrieved.GroupID;
                        ResolvedGroupName = groupRetrieved.GroupName;
                        break;
                    }
                }
            }
            WaitForGroupsSearchEvent.Set();
        }

        void GroupJoinedHandler(object sender, GroupOperationEventArgs grpoperev)
        {
            Console.WriteLine(Agent.ToString() + (grpoperev.Success ? " joined " : " failed to join ") + grpoperev.GroupID.ToString());

            /* A.Biondi 
             * This code is not necessary because it is yet present in the 
             * GroupCommand.cs as well. So the new group will be activated by 
             * the mentioned command. If the GroupCommand.cs would change, 
             * just uncomment the following two lines.
                
            if (success)
            {
                Console.WriteLine(Client.ToString() + " setting " + groupID.ToString() + " as the active group");
                Client.Groups.ActivateGroup(groupID);
            }
                
            */
            JoinedGroup = grpoperev.Success;
            WaitForGroupsSearchEvent.Set();
        }

        ManualResetEvent WaitForLeaveGroupEvent = new ManualResetEvent(false);
        private bool LeftGroup;

        public bool LeaveGroupAction(string arggrpidname)
        {
            UUID groupUUID = Agent.GroupName2UUID(arggrpidname);
            if (UUID.Zero != groupUUID) {
                Agent.Groups.GroupLeaveReply += GroupLeaveReplyHandler;
                Agent.Groups.LeaveGroup(groupUUID);
                WaitForLeaveGroupEvent.WaitOne(30000, false);
                Agent.Groups.GroupLeaveReply -= GroupLeaveReplyHandler;
                WaitForLeaveGroupEvent.Reset();
                Agent.ReloadGroupsCache();
                if (LeftGroup)
                    return VRAgentController.ok("left group");
                return VRAgentController.fail("cannot leave group");
            }
            return VRAgentController.fail("not group member");
        }

        void GroupLeaveReplyHandler(object sender, GroupOperationEventArgs grpleavev)
        {
            LeftGroup = grpleavev.Success;
            WaitForLeaveGroupEvent.Set();
        }


    }
}
