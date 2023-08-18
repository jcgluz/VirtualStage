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
#   Module:     AppearanceActions
#   Purpose:    Actions to view and/or modify the appearance of the
#               avatar controlled by the actor
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

""" Module AppearanceActions - Actions to view and/or modify 
        the appearance of the avatar controlled by the actor
    Functions:
        look_my_info(acid)
        look_my_attachments(acid)
        look_my_wearables(acid)
        attach(acid, attpoint, item)
        detach(acid, item)
        set_appearance(acid, rebake)
        take_off(acid, item)
        wear(acid, opt, itemfold)

"""

import ActorController as ac


def look_my_info(acid):
    """ Return information about the avatar controlled by the actor.

    Args:
        acid:   str with unique global identifier of actor.

    Returns:    
        On fail, returns None.        
        On success, returns an 'myinfo' perception record containing 
        information about my avatar. Perception records are list of 
        strings, 'myinfo' record have the following
        format: 
            ['myinfo', acid, name, fstnam, lstnam, locid, access, 
                health, balanc, siton, actgrp, grppow]                  
        where: name is the full name of this avatar
            fstnam is the first name of this avatar
            lstnam is the last name of this avatar
            locid is the avatar ID, local to the current region
            access is the access level of this avatar, usually M, PG or A
            health is the health level of this avatar 
            balanc is the current monetary balance of this avatar
            siton is the local ID of the prim this avatar is sitting on
            actgrp the UUID of the avatar active group
            grppow the avatar powers in the currently active group
        On success, this action also adds the 'myinfo' record to the
        perception base.            
        All perception records fields are strings.          
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyInfoAction()
    except:
        return None
        
def look_my_attachments(acid):
    """ Retrieve information about the attachments of the avatart
        controlled by the actor.

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.      
        On success, returns an list of 'myattach' perception records containing 
        information about the avatar attachments. Inventory perception records 
        are lists of strings, 'myattach' records have the following format:  
            ['myattach', id, type, subtype, localid, point, X, Y, Z, SX, SY, SZ]
        where:  id is the unique global id of folder/item; 
                type can be 'prim', 'tree' or 'grass'; 
                subtype is the type of primitive, tree or grass;
                point is where the attachment is connected to avatar's body;
                localid is the local id of attachment;
                x,y,z are X,Y,Z coordinates of attachment;
                sx,sy,sz are the scale (size) of attachment in X,Y,Z axis.               
        On success, this action also adds 'myattach' retrieved records to the 
        perception base.            
        All perception records fields are strings.          
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyAttachmentsAction()
    except:
        return None
        

def look_my_wearables(acid):
    """ Retrieve information about the wearables (clothes and similar
        items) of the avatar controlled by the actor.

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.      
        On success, returns an list of 'mywearable' perception records containing 
        information about the avatar wearables. Inventory perception records 
        are lists of strings, 'mywearable' records have the following format:  
            ['mywearable', id, weartype, assetype, assetname, assetid]
        where:  id is the unique global id of wearable;
            weartype is the type of the wearable item;
            assetype is the type of the asset;
            assetname is the name of asset in the inventory;
            assetid is the unique id of asset in inventory.                
        On success, this action also adds 'mywearable' retrieved records to the 
        perception base.            
        All perception records fields are strings.          
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyWearablesAction()
    except:
        return None
        

def attach(acid, attpoint, itempath):
    """ Attach the item identified by itempath arg to the point
        of avatar's body identified by attpoint arg.

    Args:

        acid:       str with unique global identifier of actor;
        attpoint:   point of avatar's body where attach item, can be:
                        'default', 'chest', 'head', 'left_shoulder',
                        'right_shoulder', 'left_hand', 'right_hand',
                        'left_foot', 'right_foot', 'back', 'pelvis', 
                        'mouth', 'chin', 'left_ear', 'right_ear', 
                        'left_eye', 'right_eye', 'nose', 'right_upper_arm', 
                        'right_lower_arm', 'left_upper_arm', 'left_lower_arm',
                        'right_hip', 'right_upper_leg', 'right_lower_leg',
                        'left_hip', 'left_upper_leg', 'left_lower_leg',
                        'belly', 'left_pec', 'right_pec', 'neck', 'center',
        itempath:   path (in avatar's inventory) of item to be attached.

    Returns:
     
        On fail, returns false. 
        On success, true.
        
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.AttachAction(attpoint,itempath)
    except:
        return False

def detach(acid, itempath):
    """ Detach the item identified by itempath arg from avatar's body.

    Args:

        acid:       str with unique global identifier of actor;
        itempath:   path (in avatar's inventory) of item to be detached.

    Returns:
     
        On fail, returns false. 
        On success, true.
        
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.DetachAction(itempath)
    except:
        return False

def set_appearance(acid, rebake):
    """ Set avatar current appearance to appearance last stored on simulator.

    Args:

        acid:       str with unique global identifier of actor;
        rebake:     boolean, if true force texture rebaking.

    Returns:
     
        On fail, returns false. 
        On success, true.
        
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.SetAppearanceAction(rebake)
    except:
        return False

def take_off(acid, itempath):
    """ Take off an item being weared.

    Args:

        acid:       str with unique global identifier of actor;
        itempath:   str with path to item to be taken off.

    Returns:
     
        On fail, returns false. 
        On success, true.
        
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.TakeOffAction(itempath)
    except:
        return False

def wear(acid, opt, path):
    """ Wear outfits from an inventory folder or an outfit from inventory item.

    Args:

        acid:       str with unique global identifier of actor;
        opt:        str that identifies if to wear outfits from folder 
                    or item, can be: 'item' or 'folder'
        path:       str with path to item or folder with outfit to be worn.

    Returns:
     
        On fail, returns False. 
        On success, True.
        
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.WearAction(opt,path)
    except:
        return False




