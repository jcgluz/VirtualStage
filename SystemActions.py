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
#   Module:     SystemActions
#   Purpose:    Execute system actions
#   Author:     João Carlos Gluz
#
#
###############################################################
###############################################################

""" Module SystemActions - Execute system actions
    Functions:
        get_attach_points(acid)
        get_msg_codes(acid)
        get_mat_types(acid)
        get_prim_types(acid)
        get_std_anims(acid)
        get_tree_types(acid)
        set_log_level(acid,level)
        pause_for(acid, seconds)
        pause(acid)
        resume(acid)

"""

import ActorController as ac

#region SystemActions

def get_attach_points(acid):
    """ Return names of my attachments points

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.
        On success, returns a list of attachment point names.       
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SysActs.GetAttachPointsAction()
    except:
        return None

def get_msg_codes(acid):
    """ Return names of message codes used in instant message communicaiton

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.
        On success, returns a list of message codes names.      
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SysActs.GetMsgCodesAction()
    except:
        return None

def get_mat_types(acid):
    """ Return names of standard material types used in objects

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.
        On success, returns a list of material types names.     
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SysActs.GetMatTypesAction()
    except:
        return None

def get_prim_types(acid):
    """ Return names of standard primitive types of objects

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.
        On success, returns a list of primitive types names.        
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SysActs.GetPrimTypesAction()
    except:
        return None

def get_std_anims(acid):
    """ Return names of standard animations

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.
        On success, returns a list of standard animation names.     
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SysActs.GetStdAnimsAction()
    except:
        return None

def get_tree_types(acid):
    """ Return names of standard types of trees

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.
        On success, returns a list of standard trees names.     
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SysActs.GetTreeTypesAction()
    except:
        return None

def set_log_level(acid,level):
    """ Set logging level 

    Args:
        acid:   str with unique global identifier of actor.
        level:  str with level of logging, can be: 
                'none' (disable logging), 'info', 'warn',
                'error' or 'debug'

    Returns:    
        On fail, returns False
        On success, True        
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SysActs.SetLogLevelAction(level)
    except:
        return False

def pause_for(acid, seconds):
    """ Makes actor's avatar sleeps (stops operation) for a given 
        number of seconds.

    Args:
        acid:       str with unique global identifier of actor;
        seconds:    str with number of seconds (an int value) to sleep.

    Returns:     
        On fail, returns false. 
        On success, true.
        
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.SleepAction(seconds)
    except:
        return False


def pause(acid):
    """ Pause operation of actor's avatar 

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns False
        On success, True        
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SysActs.PauseAction('start')
    except:
        return False

def resume(acid):
    """ Resume actor's avatar operation. 

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns False
        On success, True        
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SysActs.PauseAction('stop')
    except:
        return False

