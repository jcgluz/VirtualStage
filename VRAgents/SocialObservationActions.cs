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
//   Class:     SocialObservationActions 
//   Purpose:   To implement actions for agents be able to observe the
//              state of their social relationships with other avatars
//              on virtual world.
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
    public class SocialObservationActions : Actions
    {
        public SocialObservationActions(VRAgentController agent) : base(agent)
        {
        }

        public List<List<string>> LookMyFriendsAction()
        {
            PerceptList percepts = new PerceptList();
            List<List<string>> results = new List<List<string>>();
            string avid = Agent.Self.AgentID.ToString();
            if (Agent.Friends.FriendList.Count > 0) {
                Agent.Friends.FriendList.ForEach(delegate (FriendInfo friend) {
                    results.Add(percepts.Add("myfriend",
                                    friend.UUID.ToString(),
                                    friend.Name,
                                    friend.IsOnline? "online":"offline",
                                    friend.CanSeeMeOnline.ToString(),
                                    friend.CanSeeMeOnMap.ToString(),
                                    friend.CanModifyMyObjects.ToString(),
                                    friend.CanSeeThemOnline.ToString(),
                                    friend.CanSeeThemOnMap.ToString(),
                                    friend.CanModifyTheirObjects.ToString()
                                    ));
                    });
            }
            if (percepts.Count>0)
                Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("retrieved friends list",results);
        }

        ManualResetEvent Wait_Friend = new ManualResetEvent(false);

        public List<string> LookFriendStatusAction(string argfrienduid)
        {
            UUID friendID;
            if (!UUID.TryParse(argfrienduid, out friendID))
                return null;
            PerceptList percepts = new PerceptList();
            List<string> result = null;
            EventHandler<FriendFoundReplyEventArgs> friendFoundHandler =
                delegate (object sender, FriendFoundReplyEventArgs friendFound) {
                    if (!friendFound.RegionHandle.Equals(0)) {
                        result = percepts.Add("myfriend_status", 
                                    argfrienduid, "online",
                                    friendFound.RegionHandle.ToString(),
                                    friendFound.Location.X.ToString(),
                                    friendFound.Location.Y.ToString(),
                                    friendFound.Location.Z.ToString());
                    } else {
                        result = percepts.Add("myfriend_status", 
                                    argfrienduid, "offline");
                    }
                    Wait_Friend.Set();
                };
            Wait_Friend.Reset();
            Agent.Friends.FriendFoundReply += friendFoundHandler;
            Agent.Friends.MapFriend(friendID);
            if (!Wait_Friend.WaitOne(10000, false)) {
                Agent.Friends.FriendFoundReply -= friendFoundHandler;
                return null;
            }
            Agent.Friends.FriendFoundReply -= friendFoundHandler;
            if (percepts.Count > 0) {
                Agent.PerceptsBase.Update(percepts);
                return result;
            } else {
                return null;
            }
        }

        public List<List<string>> LookMyGroupsAction()
        {
            PerceptList percepts = new PerceptList();
            List<List<string>> results = new List<List<string>>();
            Agent.ReloadGroupsCache();
            if (null == Agent.GroupsCache)
                return null;
            if (0 == Agent.GroupsCache.Count)
                return null;
            foreach (Group group in Agent.GroupsCache.Values) {
                results.Add(percepts.Add("mygroup", group.ID.ToString(),
                                group.Name.ToString(),
                                group.GroupMembershipCount.ToString()
                            ));
            }
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("retrieved list of my groups", results);
        }

        PerceptList GroupMembers_Percepts = new PerceptList();
        List<List<string>> GroupMembers_Results = new List<List<string>>();
        private ManualResetEvent Wait_GroupMembers = new ManualResetEvent(false);
        private UUID GroupMembers_GroupUUID;
        private UUID GroupMembers_RequestID;

        public List<List<string>> LookGroupMembersAction(string arggrpidname)
        {
            GroupMembers_GroupUUID = Agent.GroupName2UUID(arggrpidname);
            if (UUID.Zero == GroupMembers_GroupUUID) {
                return VRAgentController.nulcoll("param 1 error");
            }
            Wait_GroupMembers.Reset();
            Agent.Groups.GroupMembersReply += GroupMembersReplyHandler;
            GroupMembers_RequestID = Agent.Groups.RequestGroupMembers(GroupMembers_GroupUUID);
            if (!Wait_GroupMembers.WaitOne(30000, false)) {
                Agent.Groups.GroupMembersReply -= GroupMembersReplyHandler;
                return VRAgentController.nulcoll("timeout to get group");
            }
            Agent.Groups.GroupMembersReply -= GroupMembersReplyHandler;
            if (GroupMembers_Percepts.Count > 0) {
                Agent.PerceptsBase.Update(GroupMembers_Percepts);
                return VRAgentController.ok("get group members",GroupMembers_Results);
            } else {
                return VRAgentController.nulcoll("no members in group");
            }
        }

        private void GroupMembersReplyHandler(object sender, GroupMembersReplyEventArgs grpmembev)
        {
            if (grpmembev.RequestID == GroupMembers_RequestID) {
                if (grpmembev.Members.Count > 0)
                    foreach (KeyValuePair<UUID, GroupMember> member in grpmembev.Members)
                        GroupMembers_Results.Add(
                            GroupMembers_Percepts.Add(
                                "group_member", 
                                GroupMembers_GroupUUID.ToString(), 
                                member.Key.ToString(),
                                member.Value.OnlineStatus.ToString(),
                                member.Value.Title.ToString(),
                                member.Value.IsOwner.ToString()));
                Wait_GroupMembers.Set();
            }
        }

        PerceptList GroupRoles_Percepts = new PerceptList();
        List<List<string>> GroupRoles_Results = new List<List<string>>();
        private ManualResetEvent Wait_GroupRoles = new ManualResetEvent(false);
        private UUID GroupRoles_GroupUUID;
        private UUID GroupRoles_RequestID;

        public List<List<string>> LookGroupRolesAction(string arggrpidname)
        {
            GroupRoles_GroupUUID = Agent.GroupName2UUID(arggrpidname);
            if (UUID.Zero == GroupRoles_GroupUUID) {
                return VRAgentController.nulcoll("param 1 error");
            }
            Agent.Groups.GroupRoleDataReply += GroupRolesReplyHandler;
            GroupRoles_RequestID = Agent.Groups.RequestGroupRoles(GroupRoles_GroupUUID);
            if (!Wait_GroupRoles.WaitOne(30000, false)) {
                Wait_GroupRoles.Reset();
                Agent.Groups.GroupRoleDataReply += GroupRolesReplyHandler;
                return VRAgentController.nulcoll("timeout to get group roles");
            }
            Wait_GroupRoles.Reset();
            Agent.Groups.GroupRoleDataReply += GroupRolesReplyHandler;
            if (GroupRoles_Percepts.Count > 0)
                Agent.PerceptsBase.Update(GroupRoles_Percepts);
            return VRAgentController.ok("group roles list", GroupRoles_Results);
        }

        void GroupRolesReplyHandler(object sender, GroupRolesDataReplyEventArgs grprolesev)
        {
            if (grprolesev.RequestID == GroupRoles_RequestID) {
                GroupRoles_Percepts.Add("mygroup",
                                GroupRoles_GroupUUID.ToString() );
                GroupRoles_Percepts.Add("group", GroupRoles_GroupUUID.ToString() );
                if (grprolesev.Roles.Count > 0)
                    foreach (KeyValuePair<UUID, GroupRole> role in grprolesev.Roles) {
                        GroupRoles_Results.Add(GroupRoles_Percepts.Add(
                                    "group_role", 
                                    GroupRoles_GroupUUID.ToString() ,
                                    role.Value.Name.ToString() , 
                                    role.Value.Title.ToString(),
                                    role.Value.Description.ToString()
                                ));
                    }
                GroupRoles_Percepts.Add("roles_count", 
                        GroupRoles_GroupUUID.ToString() ,
                        grprolesev.Roles.Count.ToString() );
                Wait_GroupRoles.Set();
            }
        }

        ManualResetEvent Wait_SearchGroups = new ManualResetEvent(false);
        PerceptList SearchGroups_Percepts = new PerceptList();
        List<List<string>> SearchGroups_Results = new List<List<string>>();

        public List<List<string>> LookForGroupsAction(string argsrchtxt)
        {
            Wait_SearchGroups.Reset();
            Agent.Directory.DirGroupsReply += SearchGroupsReplyHandler;
            // send the request to the directory manager
            Agent.Directory.StartGroupSearch(argsrchtxt, 0);
            if (!(Wait_SearchGroups.WaitOne(20000, false) && Agent.Network.Connected)) {
                Agent.Directory.DirGroupsReply -= SearchGroupsReplyHandler;
                return VRAgentController.nulcoll("timeout to get groups");
            }
            Agent.Directory.DirGroupsReply -= SearchGroupsReplyHandler;
            if (SearchGroups_Percepts.Count > 0)
                Agent.PerceptsBase.Update(SearchGroups_Percepts);
            return VRAgentController.ok("groups list",SearchGroups_Results);
        }

        void SearchGroupsReplyHandler(object sender, DirGroupsReplyEventArgs dirgrpsev)
        {
            if (dirgrpsev.MatchedGroups.Count > 0) {
                foreach (DirectoryManager.GroupSearchData group in dirgrpsev.MatchedGroups) {
                    SearchGroups_Results.Add(SearchGroups_Percepts.Add(
                                            "group", group.GroupID.ToString(),
                                            group.GroupName.ToString(),
                                            group.Members.ToString()
                                        ));
                }
            }
            Wait_SearchGroups.Set();
        }

        private ManualResetEvent Wait_PeopleSearch = new ManualResetEvent(false);
        PerceptList PeopleSearch_Percepts = new PerceptList();
        List<List<string>> PeopleSearch_Results = new List<List<string>>();

        public List<List<string>> LookForPeopleAction(string argsearchtxt)
        {
            Wait_PeopleSearch.Reset();
            Agent.Directory.DirPeopleReply += SearchPeopleReplyHandler;
            // send the request to the directory manager
            Agent.Directory.StartPeopleSearch(argsearchtxt, 0);
            if (!(Wait_PeopleSearch.WaitOne(20000, false) &&
                Agent.Network.Connected)) {
                Agent.Directory.DirPeopleReply -= SearchPeopleReplyHandler;
                return VRAgentController.nulcoll("timeout to get people");
            }
            Agent.Directory.DirPeopleReply -= SearchPeopleReplyHandler;
            if (PeopleSearch_Percepts.Count > 0)
                Agent.PerceptsBase.Update(PeopleSearch_Percepts);
            return VRAgentController.ok("people list",PeopleSearch_Results);
        }

        void SearchPeopleReplyHandler(object sender, DirPeopleReplyEventArgs dirpeoplev)
        {
            string avname;
            if (dirpeoplev.MatchedPeople.Count > 0) {
                foreach (DirectoryManager.AgentSearchData agent in dirpeoplev.MatchedPeople) {
                    avname = agent.FirstName + " " + agent.LastName;
                    PeopleSearch_Results.Add(PeopleSearch_Percepts.Add(
                                                "person", agent.AgentID.ToString(),
                                                avname, agent.FirstName,
                                                agent.LastName,
                                                (agent.Online)?"online":"offline"
                                            ));
                }
            }
            Wait_PeopleSearch.Set();
        }


    }
}
