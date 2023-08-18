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
#   Module:     MoveActions
#   Purpose:    Actions to move the avatar controlled by the actor
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

""" Module MoveActions - Actions to move the avatar controlled by the actor
    Functions:
        backward(acid, val=None, unit=None)
        forward(acid, val=None, unit=None)
        leftward(acid, val=None, unit=None)
        rightward(acid, val=None, unit=None)
        upward(acid)
        downward(acid)
        go_home(acid)
        set_home(acid)
        stop_follow(acid)
        stop_walk_to(acid)
        fly(acid, startstop)
        run(acid, startstop)
        jump(acid,startstop)
        do_motion(acid, motion)
        follow(acid, targetid)
        fly_to(acid, x, y, z, maxtoim, unit)
        tele_to(acid, x, y, z=None)
        tele_to_landmark(acid, landmark)
        tele_to_rgn(acid, rgn, x, y, z=None)
        walk_to(acid, x, y, z=None)

"""

import ActorController as ac

#region MovementActions

def backward(acid, val=None, unit=None):
    """ Move the avatar backwards

    Args:
        acid:   str with unique global identifier of actor
        Optional:
            val:    int with seconds/meters to move backward
            unit:   can be 'sec' or 'mt'
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        if val==None and unit==None:
            result= agent.MoveActs.BackwardAction()
        else:
            result= agent.MoveActs.BackwardAction(val,unit)
    except:
        result= False
    return result

def forward(acid, val=None, unit=None):
    """ Move the avatar forward

    Args:
        acid:   str with unique global identifier of actor
        Optional args:
            val:    int with seconds/meters to move forward
            unit:   can be 'sec' or 'mt'
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        if val==None and unit==None:
            result= agent.MoveActs.ForwardAction()
        else:
            result= agent.MoveActs.ForwardAction(val,unit)
    except:
        result= False
    return result
  
  
def leftward(acid, val=None, unit=None):
    """ Move the avatar to the left

    Args:

        acid:   str with unique global identifier of actor
        Optional args:
            val:    int with seconds/meters to move left
            unit:   can be 'sec' or 'mt'
        
    Returns:    
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        if val==None and unit==None:
            result= agent.MoveActs.LeftwardAction()
        else:
            result= agent.MoveActs.LeftwardAction(val,unit)
    except:
        result= False
    return result

    
def rightward(acid, val=None, unit=None):
    """ Move the avatar to the right

    Args:
        acid:   str with unique global identifier of actor
        Optional args:
            val:    int with seconds/meters to move right
            unit:   can be 'sec' or 'mt'
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        if val==None and unit==None:
            result= agent.MoveActs.RightwardAction()
        else:
            result= agent.MoveActs.RightwardAction(val,unit)
    except:
        result= False
    return result
  
  
def upward(acid):
    """ Move avatar to up

    Args:
        acid:   str with unique global identifier of actor
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        result= agent.MoveActs.MotionAction("up")
    except:
        result= False
    return result
  
  
def downward(acid):
    """ Move the avatar down

    Args:
        acid:   str with unique global identifier of actor
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        result= agent.MoveActs.MotionAction("down")
    except:
        result= False
    return result
 
 
def go_home(acid):
    """ Teleport/move the avatar to home location, if defined

    Args:
        acid:   str with unique global identifier of actor
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        result= agent.MoveActs.GoHomeAction()
    except:
        result= False
    return result
 
 
def set_home(acid):
    """ Set current position as avatar home location's

    Args:
        acid:   str with unique global identifier of actor
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        result= agent.MoveActs.SetHomeAction()
    except:
        result= False
    return result
  
  
def stop_follow(acid):
    """ Stop following another avatar

    Args:
        acid:   str with unique global identifier of actor
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        result= agent.MoveActs.StopFollowAction()
    except:
        result= False
    return result
 
 
def stop_walk_to(acid):
    """ Stop walking to a place

    Args:
        acid:   str with unique global identifier of actor
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        result= agent.MoveActs.StopWalkToAction()
    except:
        result= False
    return result


def fly(acid, startstop):
    """ Start/stop fly mode

    Args:
        acid:       str with unique global identifier of actor
        startstop:  can be 'start' or 'stop'
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        result= agent.MoveActs.FlyAction(startstop)
    except:
        result= False
    return result
 
 
def run(acid, startstop):
    """ Start/stop run mode

    Args:
        acid:       str with unique global identifier of actor
        startstop:  can be 'start' or 'stop'
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        result= agent.MoveActs.RunAction(startstop)
    except:
        result= False
    return result
    
def jump(acid,startstop):
    """ Start/stop jumping

    Args:
        acid:       str with unique global identifier of actor
        startstop:  can be 'start' or 'stop'
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.PosActs.JumpAction(startstop)
    except:
        return False


def do_motion(acid, motion):
    """ Execute low level motion actions

    Args:

        acid:   str with unique global identifier of actor
        motion: can be 'forward','back','right,'left','up','down','turn_left,'turn_right',
                'nudge_forward','nudge_back','nudge_right','nudge_left','finish_anim',
                'pitch_pos','pitch_neg','yaw_pos','yaw_neg','stop','sit','stand',
                'stop_on','stop_off','sit_on','sit_off','stand_on','stand_off',
                'fly_on','fly_off','turn_left_on','turn_left_off','turn_right_on',
                'turn_right_off','run_on','run_off','fast_at_on','fast_at_off',
                'fast_left_on','fast_left_off','fast_up_on','fast_up_off','away_on' or
                'away_off'
        
    Returns:
     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        result= agent.MoveActs.MotionAction(motion)
    except:
        result= False
    return result
    
def follow(acid, avname):
    """ Start following avatar with name avid

    Args:

        acid:   str with unique global identifier of actor
        avid:   str with the name of avatar to be followed
        
    Returns:
     
        On fail, returns False
        On success, True
            
    """
    
    try:
        agent = ac.get_agctl(acid)
        result= agent.MoveActs.FollowAction(avname)
    except:
        result= False
    return result
    
def fly_to(acid, x, y, z, maxtim, unit):
    """ Fly avatar towards position x,y,z for a maximum maxtim sec/ms

    Args:

        acid:   str with unique global identifier of actor
        x,y,z:  float with X,Y,Z coordinates to fly to
        maxtim: float with max flying time (in seconds/ms)
        unit:   can be 'sec' or 'ms'
        
    Returns:
     
        On fail, returns False
        On success, True
            
    """
    
    try:
        agent = ac.get_agctl(acid)
        result= agent.MoveActs.FlyToAction(x,y,z,maxtim,unit)
    except:
        result= False
    return result
    
def tele_to(acid, x, y, z=None):
    """ Teleport the avatar toward the specified position x,y (z is optional)

    Args:

        acid:   str with unique global identifier of actor
        x,y,z:  floats with X,Y,Z coordinates to teleport to
        
    Returns:
     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        if z==None:
            result= agent.MoveActs.TeleToAction(x,y)
        else:
            result= agent.MoveActs.TeleToAction(x,y,z)
    except:
        result= False
    return result
    
def tele_to_landmark(acid, landmarkid):
    """ Teleport the avatar a previously specified landmark

    Args:

        acid:       str with unique global identifier of actor
        landmarkid: str with global identifier of landmark
        
    Returns:
     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.MoveActs.TeleToLandmarkAction(landmarkid)
    except:
        return False

def tele_to_rgn(acid, rgn, x, y, z=None):
    """ Teleport the avatar to x,y (z optional) position in region rgn

    Args:

        acid:   str with unique global identifier of actor
        rgn:    str with name of region to teleport to
        x,y,z:  floats with X,Y,Z coordinates to teleport to
        
    Returns:
     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        if z==None:
            result= agent.MoveActs.TeleToRgnAction(rgn,x,y)
        else:
            result= agent.MoveActs.TeleToRgnAction(x,y,z)
    except:
        result= False
    return result
    
def walk_to(acid, x, y, z=None):
    """ Use the autopilot sim function to move the avatar to a new position
    
    Args:

        acid:   str with unique global identifier of actor
        x,y:    floats with X,Y coordinates to walk to
        z:      optional float arg with Z coordinate to walk to
        
    Returns:
     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        if z==None:
            result= agent.MoveActs.WalkToAction(x,y)
        else:
            result= agent.MoveActs.WalkToAction(x,y,z)
    except:
        result= False
    return result
    
#endregion

