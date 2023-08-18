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
#   Module:     PositionActions
#   Purpose:    Actions to view and/or change the positioning
#               of avatar controlled by the actor
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

""" Module PositionActions - Actions to view and/or change 
        positioning of avatar controlled by the actor
    Functions:
        look_my_region(acid)
        look_my_height(acid)
        look_my_wind(acid)
        look_my_position(acid)
        look_my_rotation(acid)
        look_my_velocity(acid)
        look_my_acceleration(acid)
        look_my_ang_velocity(acid)
        rotate_toward(acid, x, y, z)
        turn_to_abs_dir(acid, dir, unit)
        turn_to_rel_dir(acid, dir, unit)
        turn_to_named_dir(acid, dirname)
        turn_to_pos(acid, x, y, z)
        turn_to_obj(acid, objid)
        turn_to_avatar(acid, avname)
        turning_to(acid, opt)

"""

import ActorController as ac


def look_my_region(acid):
    """ Return information about current region (i.e. the 
        region where is the avatar controlled by the actor).

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.       
        On success, returns an 'myregion' perception record containing 
        information about the simulator region where the avatar is currently
        positioned. Perception records are list of strings, 'myregion' record 
        have the following format: 
            ['myregion", rid, rgname]
        where:  rid unique global id of region;
                rgname name or region   
        On success, this action also adds to perception base a list of 
        perception records with more info about avatar's current region:
            ['myregion", rid, rgname]
            ['region", rid]
            ['name", rid , rgname]
            ['handle', rid , handle]: unique rgn id, combination of X,Y coords
            ['world_coord', rid , x, y]: global coords X,Y of region in world grid
            ['access_level', rid , accesslev]
            ['flags', rid, flags]
            ['terr_hght_rng0', rid, heightrange0]
            ['terr_hght_rng1', rid, heightrange1]
            ['terr_hght_rng2', rid, heightrange2]
            ['terr_hght_rng3', rid, heightrange3]
            ['terr_strt_hght0', rid, terrstartheight0]
            ['terr_strt_hght1', rid, terrstartheight0]
            ['terr_strt_hght2', rid, terrstartheight0]
            ['terr_strt_hght3', rid, terrstartheight0]
            ['terr_base0', rid, terrbase0]
            ['terr_base1', rid, terrbase0]
            ['terr_base2', rid, terrbase0]
            ['terr_base3', rid, terrbase0]
            ['terr_detail0', rid, terrdetail0]
            ['terr_detail1', rid, terrdetail0]
            ['terr_detail2', rid, terrdetail0]
            ['terr_detail3', rid, terrdetail0]
            ['water_height', rid, waterheight]           
        All perception records fields are strings.          
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyRegionAction()
    except:
        return None

        
def look_my_position(acid):
    """ Return information about the position of the avatar
        controlled by the actor .

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.      
        On success, returns an 'mypos' perception record containing 
        information about the position of my avatar. Perception
        records are list of strings, 'mypos' record have the following
        format: 
            ['mypos', acid, x, y, z]
        where:  x, y, z are the coordinates of avatar in current region.
        On success, this action also adds the 'mypos' record to the
        perception base.            
        All perception records fields are strings.          
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyPositionAction()
    except:
        return None
        
def look_my_rotation(acid):
    """ Return information about the rotation of the avatar 
        controled by the actor.

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.      
        On success, returns an 'myrot' perception record containing 
        information about the rotation of my avatar. Perception
        records are list of strings, 'myrot' record have the following
        format: 
            ['myrot', acid, roll, pitch, yaw]
        where:  roll, pitch, yaw are Euler radian angles of avatar rotation
        On success, this action also adds the 'myrot' record to the
        perception base.            
        All perception records fields are strings.          
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyRotationAction()
    except:
        return None
        

def look_my_velocity(acid):
    """ Return information about the velocity of the avatar
        controlled by the actor.

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.      
        On success, returns an 'myvel' perception record containing 
        information about the position of my avatar. Perception
        records are list of strings, 'myvel' record have the following
        format: 
            ['myvel', acid, vx, vy, vz]
        where:  vx, vy and vz are values in m/s that represent the velocity 
        of the avatar, respectively, on x,y and z axis.
        On success, this action also adds the 'myvel record to the
        perception base.            
        All perception records fields are strings.          
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyVelocityAction()
    except:
        return None

def look_my_acceleration(acid):
    """ Return information about the acceleration of the avatar
        controlled by the actor.

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.      
        On success, returns an 'myaccel' perception record containing 
        information about the position of my avatar. Perception
        records are list of strings, 'myaccel' record have the following
        format: 
            ['myaccel', acid, ax, ay, az]
        where:  ax, ay and az are values in m/s^2 that represent the 
        acceleration of the avatar, respectively, on x,y and z axis.
        On success, this action also adds the 'myaccel record to the
        perception base.            
        All perception records fields are strings.          
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyAccelerationAction()
    except:
        return None
        
def look_my_ang_velocity(acid):
    """ Return information about the angular velocity of the avatar 
        controled by the actor.

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.      
        On success, returns an 'myangvel' perception record containing 
        information about the rotation of my avatar. Perception
        records are list of strings, 'myangvel' record have the following
        format: 
            ['myangvel', acid, rx, ry, rz]
        where: rx, ry and rz are values in radians per second that represent
        the rate of rotation of avatar, respectively, on axis x, y and z.
        On success, this action also adds the 'myangvel' record to the
        perception base.            
        All perception records fields are strings.          
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyAngularVelocityAction()
    except:
        return None
        

def look_my_height(acid):
    """ Look terrain height in avatar's current position

    Args:
        acid:   str with unique global identifier of actor
        
    Returns:     
        On fail, returns None.       
        On success, returns a perception record with information about 
        height in X,Y coordinates:
            ['my_terrain_height', rid, x, y, height]
        where:  rid is the unique global id of region;
                x,y are the X,Y coordinates of actor's avatar position;
                height is the height in meters at X,Y position.
        All fields from perception records are strings.         
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyHeightAction()
    except:
        return None
 
 
def look_my_wind(acid):
    """ Look wind speed in avatar's current position

    Args:
        acid:   str with unique global identifier of actor
        
    Returns:     
        On fail, returns None.        
        On success, returns a perception record with information about 
        wind speed:
            ['my_wind_speed', rid, x, y, xspeed, yspeed]
        where:  rid is the unique global id of region;
                x,y are the X,Y coordinates of actor's avatar position;
                xspeed is the wind speed in X-axis;
                yspeed is the wind speed in Y-axis.
        All fields from perception records are strings.         
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyWindAction()
    except:
        return None
 
 
def rotate_toward(acid, roll, pitch, yaw):
    """ Rotates the avatar body from 3D Euler rotation angles in radians
        
    Args:
        acid:   str with unique global identifier of actor
        roll:   float with X-axis euler angle in radians
        pitch:  float with Y-axis euler angle in radians
        yaw:    float with X-axis euler angle in radians
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.PosActs.RotateTowardAction(roll,pitch,yaw)
    except:
        return False
 
 
def turn_to_abs_dir(acid, absangle, unit):
    """  Rotates avatar body to direction defined by an absolute angle 
    
    Args:
        acid:       str with unique global identifier of actor
        absangle:   float with absolute angle of new direction
                    absolute east is at 0 dg, north at 90 dg,
                    west at 180 dg and south at 280 dg
        unit:       str, can be 'rad' or 'dg'
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.PosActs.TurnToAbsDirAction(absangle,unit)
    except:
        return False


def turn_to_rel_dir(acid, relangle, unit):
    """  Rotates avatar body by relative angle added to current direction
    
    Args:
        acid:       str with unique global identifier of actor
        relangle:   float with relative angle to be added to current direction
        unit:       str, can be 'rad' or 'dg'
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.PosActs.TurnToRelDirAction(dir,unit)
    except:
        return False


def turn_to_named_dir(acid, dirname):
    """  Rotates avatar body to dirname direction
    
    Args:
        acid:       str with unique global identifier of actor
        dirname:    str, can be 'east','west','north','south','left' or 'right'
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.PosActs.TurnToNamedDirAction(dirname)
    except:
        return False


def turn_to_pos(acid, x, y, z):
    """  Rotates the avatar body toward a target x,y,z position.
    
    Args:
        acid:       str with unique global identifier of actor
        x,y,z:      floats with region X,Y,Z coordinates to turn toward
        unit:       str, can be 'rad' or 'dg'
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.PosActs.TurnToPosAction(x,y,z)
    except:
        return False


def turn_to_obj(acid, objid):
    """  Rotates the avatar body toward the position of objid object
    
    Args:
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to turns toward
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.PosActs.TurnToObjAction(objid)
    except:
        return False


def turn_to_avatar(acid, avname):
    """  Rotates the avatar body toward the position of some avatar
    
    Args:
        acid:   str with unique global identifier of actor
        avname: str with the name of avatar to turns toward
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.PosActs.TurnToAvatarAction(avname)
    except:
        return False


def turning_to(acid, turnact):
    """  Start/stop turning action
    
    Args:
        acid:       str with unique global identifier of actor
        turnact:    str with turning action, can be 'left' to start to
                    turning left, 'right' to start to turning right or
                    'stop' to stop turning action
        
    Returns:     
        On fail, returns False
        On success, True           
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.PosActs.TurningToAction(turnact)
    except:
        return False

