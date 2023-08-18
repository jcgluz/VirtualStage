###############################################################
###############################################################
#
#   VirtualStage Platform - a virtual stage for virtual actors
#
#   Copyright (C): 2020-2023, Joao Carlos Gluz
#   Contact:  João Carlos Gluz (jcgluz@gmail.com)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#
#********************************************************
#
#   Module:     SocialActions
#   Purpose:    Social actions to interact with friends and groups
#   Author:     João Carlos Gluz 
#
###############################################################
###############################################################

""" Module SocialActions - Social actions to interact with friends and groups
    Functions:
        seek_groups(acid, srchtxt)
        seek_people(acid, srchtxt)
        look_friend_status(acid, friendid)
        look_group_members(acid, grpname)
        look_group_roles(acid, grpname)
        look_my_friends(acid)
        look_my_groups(acid)
        activate_group(acid,grpname)
        invite_to_group(acid, avname, grpid, grprole=None, grprole1=None, grprole2=None)
        join_group(acid,grpidname)
        leave_group(acid,grpname)

"""

import ActorController as ac

#region SocialActions

def seek_groups(acid, srchtxt):
    """ Search  groups in virtual world.

    Args:

        acid:       str with unique global identifier of actor;
        srchtxt:    str with name or part of name of group to search for.

    Returns:
     
        On fail, returns None.
        
        On success, returns an list of 'group' perception records containing 
        information about the groups found in virtual world. These records have 
        the following format:  
            ['group', id, name, num_members]
        where:  id is the unique global id of group; 
                name is the name of group; 
                num_member is the current number of members of group.
                
        On success, this action also adds 'group' retrieved records to the 
        perception base.            

        All perception records fields are strings.          
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SocObsActs.LookForGroupsAction(srchtxt)
    except:
        return None

def seek_people(acid, srchtxt):
    """ Search directory of people in virtual world.

    Args:

        acid:       str with unique global identifier of actor;
        srchtxt:    str with name or part of name of people to search for.

    Returns:
     
        On fail, returns None.
        
        On success, returns a list of 'person' perception records containing 
        information about people found in virtual world. These records have 
        the following format:  
            ['person', id, name, first_name, last_name, status]
        where:  id is the unique global id of person; 
                name is the full name of person; 
                first_name and last_name are, resp., first and last name of
                person;
                status can be: 'online' or 'offline'.
                
        On success, this action also adds 'person' retrieved records to the 
        perception base.            

        All perception records fields are strings.          
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SocObsActs.LookForPeopleAction(srchtxt)
    except:
        return None

def look_friend_status(acid, friendid):
    """ Show status info about friend.

    Args:

        acid:       str with unique global identifier of actor;
        friendid:   str with unique id of friend.

    Returns:
     
        On fail, returns None.
        
        On success, returns a 'myfriend_status' perception record containing 
        status information about friend. This record records has the following 
        format:  
            ['myfriend_status", id, status, rgnhandle, x, y, z]

        where:  id is the unique global id of friend; 
                status of friend in virt. world, can be: 'online' or 'offline';
                rgnhandle, x, y, z: optional fields, filled if status='online',
                    rgnhandle is the handle of region where friend is located,
                    x, y, z is the local position of friend in this region.
                    
        On success, this action also adds the 'myfriend_status' record to the 
        perception base.            

        All perception records fields are strings.          
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SocObsActs.LookFriendStatusAction(friendid)
    except:
        return None

def look_group_members(acid, grpidname):
    """ Show members of some group.

    Args:

        acid:       str with unique global identifier of actor;
        grpidname:  str with name or unique id of group.

    Returns:
     
        On fail, returns None.
        
        On success, returns an list of 'group_member' perception records containing 
        information about members of group. These records have the following 
        format:  
            ['group_member', grpid, memberid, status, title, is_owner]
        where:  grpid is the unique global id of group; 
                memberid is the unique global id of member; 
                status is the online status of member in virt. world;
                title is the title of member in group;
                is_owner, 'true' if member is group owner, 'false' otherwise.
                
        On success, this action also adds the 'group_member' records to the 
        perception base.            

        All perception records fields are strings.          
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SocObsActs.LookGroupMembersAction(grpidname)
    except:
        return None

def look_group_roles(acid, grpidname):
    """ Show roles of some group.

    Args:

        acid:       str with unique global identifier of actor;
        grpidname:  str with name or unique id of group.

    Returns:
     
        On fail, returns None.
        
        On success, returns an list of 'group_role' perception records containing 
        information about roles of group. These records have the following 
        format:  
            ['group_role', grpid, name, title, descr]
        where:  grpid is the unique global id of group; 
                name is the name of the role; 
                title associated with role;
                descr is the description of role.
                
        On success, this action also adds the 'group_role' records to the 
        perception base.            

        All perception records fields are strings.          
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SocObsActs.LookGroupRolesAction(grpidname)
    except:
        return None

def look_my_friends(acid):
    """ Search for my friends in virtual world.

    Args:

        acid:       str with unique global identifier of actor;

    Returns:
     
        On fail, returns None.
        
        On success, returns a list of 'myfriend' perception records containing 
        information about friends found in virtual world. These records have 
        the following format:  
            ['myfriend', id, name, status, see_me_online, see_me_on_map,
                alter_my_objs, see_friend_online, see_friend_on_map,
                alter_friend_objs]
        where:  id is the unique global id of friend; 
                name is the full name of friend; 
                status of friend in virt. world, can be: 'online' or 'offline';
                see_me_online, see_me_on_map, alter_my_objs: rights from friend
                    to me, 'true' if friend can, resp., see me online, see me on 
                    map or modify my objects, 'false' otherwise; 
                see_friend_online, see_friend_on_map, alter_friend_objs: rights from
                    me to friend, 'true' if I can, resp., see friend online, see 
                    friend on map or alter friend objs, 'false' otherwise.
                    
        On success, this action also adds 'myfriend' retrieved records to the 
        perception base.            

        All perception records fields are strings.          
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SocObsActs.LookMyFriendsAction()
    except:
        return None

def look_my_groups(acid):
    """ Show avatar's groups.

    Args:

        acid:       str with unique global identifier of actor;

    Returns:
     
        On fail, returns None.
        
        On success, returns an list of 'mygroup' perception records containing 
        information about avatar's groups. These records have the following 
        format:  
            ['mygroup', id, name, num_members]
        where:  id is the unique global id of group; 
                name is the name of group; 
                num_member is the current number of members of group.
                
        On success, this action also adds 'mygroup' retrieved records to the 
        perception base.            

        All perception records fields are strings.          
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SocObsActs.LookMyGroupsAction()
    except:
        return None


def activate_group(acid,grpidname):
    """ Set a group as current active group.

    Args:

        acid:       str with unique global identifier of actor;
        grpidname:  str with name or unique id of group to be activated.

    Returns:
     
        On fail, returns false. 
        On success, true.
        
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SocModActs.ActivateGroupAction(grpidname)
    except:
        return False

def invite_to_group(acid, avname, grpidname, grprole=None, 
                    grprole1=None, grprole2=None):
    """ Invites an user (avatar) to a group.

    Args:

        acid:       str with unique global identifier of actor;
        avname:     str with name of user's avatar;
        grpidname:  str with name or unique id of group.
        grprole, grprole1, grprole2:    optional str args with unique ids of
                    group roles the user is invited.

    Returns:
     
        On fail, returns false. 
        On success, true.
        
    """

    try:
        agent = ac.get_agctl(acid)
        if grprole==None and grprole1==None and grprole2==None:
            result= agent.SocModActs.InviteGroupAction(avname,grpidname)
        elif grprole1==None and grprole2==None:
            result= agent.SocModActs.InviteGroupAction(avname,grpidname,grprole)
        elif grprole2==None:
            result= agent.SocModActs.InviteGroupAction(avname,grpidname,grprole,grprole1)
        else:
            result= agent.SocModActs.InviteGroupAction(avname,grpidname,grprole,grprole1,grprole2)
    except:
        result= False
    return result
def join_group(acid,grpidname):
    """ Attempt to join a group.

    Args:

        acid:       str with unique global identifier of actor;
        grpidname:  str with name or unique id of group.

    Returns:
     
        On fail, returns false. 
        On success, true.
        
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SocModActs.JoinGroupAction(grpidname)
    except:
        return False

def leave_group(acid,grpidname):
    """ Attempt to leave a group.

    Args:

        acid:       str with unique global identifier of actor;
        grpidname:  str with name or unique id of group.

    Returns:
     
        On fail, returns false. 
        On success, true.
        
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SocModActs.LeaveGroupAction(grpidname)
    except:
        return False

#endregion

