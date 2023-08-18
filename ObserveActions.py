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
#   Module:     ObserveActions
#   Purpose:    Actions to observe objects, avatars and 
#               other virtual world entities
#   Author:     João Carlos Gluz 
#
###############################################################
###############################################################

""" Module ObserveActions - Actions to observe objects, avatars 
        and other virtual world entities
    Functions:
        look_avatar(acid, avid)
        look_avatar_with_name(acid, avname)
        look_obj(acid, objid)
        look_obj_extra_props(acid, objid)
        look_obj_flex_props(acid, objid)
        look_obj_light_props(acid, objid)
        look_obj_sculpt_props(acid, objid)
        look_obj_constr_props(acid, objid)
        look_obj_phys_props(acid, objid)
        look_obj_inventory(acid, objid)
        look_height_at(acid, x, y)
        look_wind_at(acid, x, y)
        look_region(acid, rgname)
        seek_actors(acid)
        seek_avatars(acid)
        seek_obj_children(acid,objid)
        seek_objs_by_radius(acid,rad)
        seek_objs_by_type(acid,rad,typ,subtyp)
        seek_objs_by_name(acid,rad,srchname,srchmode='in',srchcase='nocase')
        seek_objs_by_descr(acid,rad,srchdescr,srchmode='in',srchcase='nocase')
        seek_objs(acid,rad,typ,subtyp,srchtxt='',srchin='name',srchmode='in',srchcase='nocase')
        seek_all_objs(acid)
        seek_regions(acid)
        wait_event(acid,evntpatt,timeout)
        seek_event(acid,evntpatt=None)
        clear_events(acid)

"""

import ActorController as ac

def wait_event(acid,evntpatt,timeout):
    """ Wait for event sent by VR simulator that match the evntpatt pattern. 
        If timeout is different than None, stop waiting after timeout seconds. 
        
    VR events are string lists, where index 0 of list corresponds to field 0 
    of event, and so on. The following types of VR events are handled by Virtual
    Stage:
        
    (Mean) collision event:
        Field 0 (EventType): 'collis'
        Field 1 (Aggressor): the ID of the agent or object that collided with your agent
        Field 2 (Type): the type of collision, can be:  'None', 'Bump', 'LPushObject',
            'SelectedObjectCollide', 'ScriptedObjectCollide', 'PhysicalObjectCollide'
        Field 3 (Magnitude): a value indicating the strength of the collision
        Field 4 (Victim): the ID of the agent that was attacked
        Field 5 (Time): the time the collision occurred in fmt YYYY-MM-ddTHH:MM:SS

    Region crossed event:
        Field 0 (EventType): 'crossrgn'
        Field 1 (NewSimulator): the simulator (region) your agent is now in
        Field 2 (OldSimulator): the simulator (region) your agent just left

    Args:
        acid:       str with unique global identifier of actor.
        evntpatt:   the event pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    event pattern are ignored in the search, string fields
                    defined in event pattern must be equal to corresponding
                    field in the event.
        timeout:    if different than None, defines the maximum time in seconds
                    to wait for the message.

    Returns:     
        On fail, returns None.      
        On success, returns the event as a list of strings.         
    """
    return ac.wait_vrevnt(acid,evntpatt,timeout)


def seek_event(acid,evntpatt=None):
    """ Search for the last event sent by VR simulator that match the evntpatt 
        pattern. Do not wait for an event, if there is no event in reception 
        queue, returns None. 
        
    VR events are string lists, where index 0 of list corresponds to field 0 
    of event, and so on. For a descripion of types and fields of VR events
    see the help of wait_event().
        
    Args:
        acid:       str with unique global identifier of actor.
        evntpatt:   the event pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    event pattern are ignored in the search, pattern strings
                    defined in event pattern must match the corresponding
                    field in the event according to the following rules:
                        - If pattern string starts with '^' then corresponding 
                        field must match the pattern from first character;
                        - If pattern string ends with '$' then corresponding  
                        field must match the pattern until last character;
                        - If pattern string starts with '!' then corresponding
                        field cannot match the pattern;
                        - If pattern string is a list of strings separated by '|'
                        then some of these strings must match corresponding field;
                        - Otherwise the pattern string must be a substring of 
                        the corresponding field.

    Returns:     
        On fail, returns None.      
        On success, returns the event as a list of strings.         
    """
    return ac.get_vrevnt(acid,evntpatt)

def clear_events(acid):
    """ Clears the event reception queue.       
        
    Args:
        acid:       str with unique global identifier of actor.

    Returns:     
        On fail, returns False.     
        On success, clears the event reception queue and returns True.          
    """
    return ac.clear_vrevnts(acid)
    
def look_height_at(acid, x, y):
    """ Look terrain height at x,y position in current region

    Args:
        acid:   str with unique global identifier of actor
        x,y:    float, int or numeric str numbers with X,Y region coordinates
        
    Returns:     
        On fail, returns None.       
        On success, returns a perception record with information about 
        height in X,Y coordinates:
            ['terrain_height_at', rid, x, y, height]
        where:  rid is the unique global id of region;
                x,y are the X,Y region coordinates;
                height is the terrain height in meters at X,Y position.
        All fields from perception records are strings.         
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookHeightAtAction(x,y)
    except:
        return None
        
def look_wind_at(acid,x,y):
    """ Look wind speed in x,y position

    Args:
        acid:   str with unique global identifier of actor
        x,y:    float, int or numeric str numbers with X,Y region coordinates 
        
    Returns:    
        On fail, returns None.       
        On success, returns a perception record with information about 
        wind speed:
            ['wind_speed_at', rid, x, y, xspeed, yspeed]
        where:  rid is the unique global id of region;
                x,y are the X,Y coordinates of region;
                xspeed is the wind speed in X-axis;
                yspeed is the wind speed in Y-axis.
        All fields from perception records are strings.         
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookWindAtAction(x,y)
    except:
        return None
                
def look_region(acid, rgname):
    """ Get information about a simulator region with name rgname.

    Args:
        acid:   str with unique global identifier of actor.
        rgname:  str with name of region to get information.

    Returns:     
        On fail, returns None.        
        On success, returns an 'region' perception record containing information
        about the rgname region. Perception records are lists of strings.        
        The 'region' record contains basic information about regions: 
            ['region', rid, name]
        Where:  rid is the unique global id of region;
                name is the name of regions.                
        On success, this action also adds to perception base a list of 
        perception records with more info about this region:
            ['region', rid, name]
            ['world_coord', rid, x, y]: global coords X,Y of region in world grid
            ['handle', rid, handle]: unique identifier/handler for region, 
                            a combination of X and Y global coords
                        
        All fields from perception records are strings.         
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookRegionAction(rgname)
    except:
        return None
        
def look_avatar(acid, avid):
    """ Get attributes and properties of avatar with avid unique id.

    Args:
        acid:   str with unique global identifier of actor.
        avid:  str with unique global identifier of avatar.

    Returns:     
        On fail, returns None.        
        On success, returns an 'avatar' perception record containing information
        about the avatar identified by avid. Perception records are lists of strings. The 
        'avatar' record contains basic information about the avatar: 
            ['avatar', avid, name, dist, x, y, z]
        where:  name is the name of avatar; 
                dist is the distance from actor;
                x,y,z are X,Y,Z region coordinates of avatar.                
        On success, this action also adds to perception base a list of 
        perception records with remaining info about the avatar:
            ['avatar', avid, name, dist, x, y, z]
            ['name', avid, name]: name (first name + last name) of avatar
            ['first_name', avid, firtname]: first name of avatar
            ['last_name', avid, lastname]: last name of avatar
            ['dist', avid, dist]: distance from actor
            ['pos', avid, x, y, z]: position of avatar in X,Y,Z region coordinates
            ['scale', avid, sx, sy, sz]: scale of avatar in X,Y,Z axis
            ['rot', avid, roll, pitch, yaw]: rotation of avatar in 
                roll,pitch,yaw Euler radian angles
            ['veloc', avid, vx, vy, vz]: speed of avatar in meters/sec 
                n X,Y,Z axis directions
            ['ang_veloc', objid, angvx, angvy, anvz]: angular velocity
                of avatar in X,Y,Z axis in radians/sec
            ['accel', objid, accelx, accely, accelz ]: acceleration of avatar
                in meters2/sec in X,Y,Z axis directions
            ['local_id', avid, localid]: local id of avatar (an integer)           
            ['txtr',avid,txtrid]: global id of default texture of avatar
            ['color',avid,r,g,b,a]: red, green, blue, alpha(transparency)
                components of default color of avatar
            ['glow',avid,glow]: default glow of avatar, from 0.0 to 1.0
            ['nfaces',avid,n]: number of faces that have specific textures
            ['txtr_<faceidx>',avid,txtrid]: texture of face with index
                faceidx (only added if avatar has a texture in faceidx face)
            ['color_faceidx>',avid,r,g,b,a]: color of texture of face with
                index faceidx (only added if avatar has a texture in faceidx face)
            ['glow_<faceidx>',avid,glow]: glow of texture of face with
                index faceidx (only added if avatar has a texture in faceidx face)           
        All fields from perception records are strings.         
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookAvatarByIDAction(avid)
    except:
        return None

        
def look_avatar_with_name(acid, avname):
    """ Search information about avatar with name avname
    
    Args:
        acid:   str with unique global identifier of actor.
        avname: str with name of avatar.

    Returns:     
        On fail, returns None.        
        On success, returns an 'avatar' perception record containing basic
        information about the avatar with name avnameand adds to perception 
        base a list of perception records with remaining info about avatar.        
        See look_avatar() action for a description about types and formats of 
        perception records returned or added to perception base by this action.         
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookAvatarByNameAction(avname)
    except:
        return None

def look_obj(acid, objid):
    """ Look to objid object to get its basic info and additional properties.

    Args:
        acid:   str with unique global identifier of actor.
        objid:  str with unique global identifier of object.

    Returns:    
        On fail, returns None.        
        On success, returns an 'obj' perception record containing information
        about the object identified by objid. Perception records are lists of strings. 
        The 'obj' record contains basic information about the object: 
            ['obj', objid, name, type, subtyp, dist, 
                x, y, z, sx, sy, sz, descr ]
        where:  objid is the unique global identifier of object (an string)
                name is the name of object
                type can be 'prim', 'tree' or 'grass' 
                subtyp is the type of primitive, tree or grass
                dist is the distance of object from actor's avatar
                x,y,z are X,Y,Z region coordinates of obj
                sx,sy,sz are the scale (size) of obj in X,Y,Z axis.               
                descr is the description of object (max 127 chars)
        On success, this action adds the 'obj' record to perception base and also 
        adds to this base a list of perception records with the remaining basic
        and additional properties of this object:
            ['name', objid, name]: name property of object
            ['descr', objid, description]: description of object (max 127 chars)
            ['dist', objid, dist]: distance from actor
            ['type', objid, obj_type]: type of object
            ['subtype', objid, primtype]: subtype of obj, see 'obj' record
            ['local_id', objid, localid]: local id of object (an integer)
            ['parent_id', objid, parentid]: local id of parent obj, is obj is linked
            ['is_flex', objid]: added if obj is flexible
            ['is_light', objid]: added if obj is light
            ['is_sculpt', objid]: added if obj is sculpt
            ['is_flex', objid]: added if obj is flexible
            ['has_children', objid]: added if is linked obj with children
            ['is_linked', objid]: added if obj has children or has parent
            ['has_phys', objid]: added if obj had physical parameters
            ['has_shadows', objid]: added if obj cast shadows
            ['is_temp', objid]: added if obj is temporary
            ['is_phantom', objid]: added if obj is phantom, i.e., cannot collides
            ['pos', objid, x, y , z]: position of obj in X,Y,Z region coordinates
            ['scale', objid, sx, sy, sz]: scale of obj in X,Y,Z axis
            ['rot', objid, roll, pitch, yaw]: rotation of obj in 
                roll,pitch,yaw Euler radian angles
            ['veloc', objid, vx, vy, vz]: speed of object in meters/sec 
                in X,Y,Z axis directions
            ['ang_veloc', objid, angvx, angvy, anvz]: angular velocity
                of object in X,Y,Z axis in radians/sec
            ['accel', objid, accelx, accely, accelz ]: acceleration of object
                in meters2/sec in X,Y,Z axis directions
            ['collis_plane', objid, x, y, z, w]: collision plane of object
            ['hover_text', objid, text]: added if obj hover text is not empty
            ['is_attach', objid]: added if obj is an attachment
            ['txtr',objid,txtrid]: global id of default texture of obj
            ['color',objid,r,g,b,a]: red, green, blue, alpha(transparency)
                components of default color of obj
            ['glow',objid,glow]: default glow of obj, from 0.0 to 1.0
            ['nfaces',objid,n]: number of faces that have specific textures
            ['txtr_<faceidx>',objid,txtrid]: texture of face with index
                faceidx (only added if obj has a texture in faceidx face)
            ['color_faceidx>',objid,r,g,b,a]: color of texture of face with
                index faceidx (only added if obj has a texture in faceidx face)
            ['glow_<faceidx>',objid,glow]: glow of texture of face with
                index faceidx (only added if obj has a texture in faceidx face)           
            ['extra_props', objid, name, descr, creatid, ownerid, creatdate]
            ['creator_id', objid, creatid]: id of object's creator
            ['owner_id', objid, ownerid]: id of object's owner
            ['creat_date', objid, creatdate]: creation date of object
            ['owner_perms', objid, perms]: permissions for object's owner
            ['group_perms', objid, perms]: permissions for group
            ['all_perms', objid, perms]: permissions for every one
            ['base_perms', objid, perms]: base permissions
            ['nextown_perms', objid, perms]: permissions for next owner            
        All fields from perception records are strings.         
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookObjAction(objid)
    except:
        return None
        
def look_obj_extra_props(acid, objid):
    """ Get additional properties about objid object.

    Args:
        acid:   str with unique global identifier of actor.
        objid:  str with unique global identifier of object.

    Returns:     
        On fail, returns None.        
        On success, returns an 'extra_props' perception record containing a
        a resume of the additional properties of objid object. Perception 
        records are lists of strings, the 'props_data' record has the 
        following structure: 
            ['extra_props', objid, name, descr, creatid, ownerid, creatdate]
        where:  name is the name of object (max 63 chars);
                descr is the description of object (max 127 chars);
                creatid is the unique global id of object'a creator;
                ownerid is the unique global id of object'a owner;
                creatdate is the date of creation of object.                
        On success, this action adds 'extra_props' record to perception base and
        also adds list of perception records with remaining additional properties
        of this object:
            ['name', objid, name]: name of object (max 63 chars)
            ['descr', objid, description]: description of object (max 127 chars)
            ['creator_id', objid, creatid]: id of object's creator
            ['owner_id', objid, ownerid]: id of object's owner
            ['creat_date', objid, creatdate]: creation date of object
            ['owner_perms', objid, perms]: permissions for object's owner
            ['group_perms', objid, perms]: permissions for group
            ['all_perms', objid, perms]: permissions for every one
            ['base_perms', objid, perms]: base permissions
            ['nextown_perms', objid, perms]: permissions for next owner            
        All fields from perception records are strings.         
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookObjExtraPropsAction(objid)
    except:
        return None

        
def look_obj_flex_props(acid, objid):
    """ If objid is a flexible object, get its flexible properties.

    Args:
        acid:   str with unique global identifier of actor.
        objid:  str with unique global identifier of object.

    Returns:     
        On fail, returns None.        
        On success, returns an 'flex_props' perception record containing 
        a resume of the flexible properties of objid object. Perception
        records are list of strings, 'flex_obj' record have the following
        format: 
            ['flex_props', objid, softness]
        where:  softness contains an int value, which determines the number 
                of joints a flexible object will have.            
        On success, this action also adds 'flex_props' record to perception base
        and also adds to this base a list of perception records with remaining
        flexible properties of this object:
            ['is_flex', objid]
            ['flex_soft', objid, softness]: number of joints of flex obj
            ['flex_grav', objid, gravity]: the downward pull on the obj
            ['flex_drag', objid, drag]: affects how fast obj snap back into place.
            ['flex_wind', objid, wind]: adjusts how wind will affect flex obj
            ['flex_tension', objid, tension]: makes the flex obj stiff or loose
            ['flex_force', objid,xforce,yforce,zforce]: x,y,z axis directions of 
                pushing or pulling force on flex obj           
        All fields from perception records are strings.         
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookObjFlexPropsAction(objid)
    except:
        return None

        
def look_obj_light_props(acid, objid):
    """ If objid is a light object, get its light properties.

    Args:
        acid:   str with unique global identifier of actor.
        objid:  str with unique global identifier of object.

    Returns:     
        On fail, returns None.        
        On success, returns an 'light_props' perception record containing 
        a resume of light properties of objid object. Perception records
        are list of strings, 'light_props' record have the following
        format: 
            ['light_props', objid, r, g, b, alpha, intensity, radius]
        where:  r, g, b are the red, green, blue components of light color
                alpha is the intensity of light color (in object colors
                is the alpha channel for transparency)
                intensity of color (equiv to alpha)
                radius of the light emitted by obj            
        On success, this action also adds 'light_props' to perception base and
        also adds to this base a list of perception records with remaining 
        light properties of this object:
            ['is_light', objid]
            ['light_color', objid, red, green, blue, alpha]: see 'light_obj'
            ['light_intens', objid, intensity]: intensity of color
            ['light_radius', objid, radius]: radius of the light emitted by obj
            ['light_cutoff', objid, cutoff]: 
            ['light_falloff', objid, falloff]: where light will cease to shine 
            ['lightmap_texture', objid, lighttextrid]: optional, light texture id
            ['lightmap_params', objid, x, y, z]: optional params of light txtr. id            
        All fields from perception records are strings.         
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookObjLightPropsAction(objid)
    except:
        return None

        
def look_obj_sculpt_props(acid, objid):
    """ If objid is a sculpt object, get its sculpt properties.

    Args:
        acid:   str with unique global identifier of actor.
        objid:  str with unique global identifier of object.

    Returns:     
        On fail, returns None.        
        On success, returns an 'sculpt_props' perception record containing 
        a resume of sculpt properties of objid object. Perception records
        are list of strings, 'sculpt_props' record have the following
        format: 
            ['sculpt_obj', objid,sculptype,textrid]
        where:  sculptype can be: 'none', 'sphere', 'torus', 'plane',
                    'cylinder', 'mesh'           
        On success, this action also adds 'sculpt_props' record to perception 
        base and also adds to this base a list of perception records remaining 
        sculpt properties of this object:
            ['is_sculpt', objid]
            ['sculpt_txtr', objid, txtrid]: texture of the sculpt
            ['sculpt_type', objid, sculptype]
            ['sculpt_is_invert', objid]: added if sculpt obj is inverted (i.e. 
                rendered inside out with normals inverted)
            ['sculpt_is_mirror', objid]: added if sculpt obj is mirrored (i.e.
                render an X axis mirror of sculpt)
        All fields from perception records are strings.         
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookObjSculptPropsAction(objid)
    except:
        return None

        
def look_obj_constr_props(acid, objid):
    """ Get construction properties of objid object. This information can be 
        used to construct the visual representation of a primitive object.

    Args:
        acid:   str with unique global identifier of actor.
        objid:  str with unique global identifier of object.

    Returns:    
        On fail, returns None.        
        On success, returns an 'constr_props' perception record containing 
        a resume of construction info about objid object. Perception records 
        are list of strings, 'constr_props' records have the following format: 
            ['constr_data', objid, profshape, holetype, pathcurve]
        where:  profshape can be: 'circle', 'square', 'isotriangle',
                    'equaltriangle', 'righttriangle', 'halfcircle'
                holetype can be: 'same', 'circle', 'square', 'triangle'
                pathcurve can be: 'line', 'circle', 'circle2', 'test', 
                    'flexible'            
        On success, this action adds 'constr_props' record to perception base 
        and also adds to this base a list of perception records remaining
        construction info about this object:
            ['attach_point', objid, attachpoint] added if it is attach point
            ['prof_shape', objid, profshape]: shape of the profile
            ['prof_hole', objid, holetype]: prof. hole type, if profhollow non-zero
            ['prof_begin', objid, profbegin]: where profile cut (if any) begins
            ['prof_end', objid, profend]: where profile cut (if any) ends
            ['prof_hollow', objid, profhollow]: how much of the profile is 
                hollowed out, as a percent of original bounding box. If non-zero 
                creates a hole using the shape defined in profhole
            ['path_curve', objid, pathcurve]: shape of extrusion path                
            ['path_begin', objid, pathbegin]: float construction parameter
            ['path_end', objid, pathend]: float construction parameter
            ['path_begin_scale'], objid, x, y]
            ['path_end_scale', objid, x, y]
            ['path_rad_offset', objid, pathradoffset]: float constr. parameter
            ['path_skew', objid, pathskew]: float construction parameter
            ['path_scale', objid, x, y ]
            ['path_shear', objid, x, y]
            ['path_taper', objid, x, y]
            ['path_twist', objid, pathtwist]: float construction parameter
            ['path_twist_begin', pathtwistbegin]: float construction parameter
            ['path_revols', objid, profrevols]: float construction parameter
            ['material', objid, material]: material can be: 'stone', 'metal',
                'glass', 'wood', 'flesh', 'plastic', 'rubber', 'light'          
        All fields from perception records are strings.         
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookObjConstrPropsAction(objid)
    except:
        return None
        
def look_obj_phys_props(acid, objid):
    """ Get physical properties of objid object, if this object has 
        physical properties.

    Args:
        acid:   str with unique global identifier of actor.
        objid:  str with unique global identifier of object.

    Returns:    
        On fail, returns None.       
        On success, returns 'phys_props' perception record containing a 
        resume of physical properties of objid object. Perception records are 
        lists of strings, 'phys_props' record has the following structure: 
            ['phys_props', objid, dens, frict, grav]
        where:  dens is object density in kg/m3 (1000 for normal density)
                frict is friction coefficient (0.6 default value);
                grav is the gravity multiplier (1.0 for normal gravity).
        On success, this action also adds to perception base a list of 
        perception records with remaining physical properties of this object:
            ['phys_dens', objid, dens]: density in kg/m3 (1000 for normal density)
            ['phys_frict', objid, frict]: friction coefficient
            ['phys_grav', objid, grav]: gravity multiplier
            ['phys_bounce', objid, bounc]: bounciness factor (0.5 default value)
            ['phys_shape', objid, shapetype]: can be: 'prim', 'none' or 
                'convexhull'            
        All fields from perception records are strings.         
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookObjPhysPropsAction(objid)
    except:
        return None
        
        
def look_obj_inventory(acid, objid):
    """ Retrieve inventory of items stored inside object objid.

    Args:
        acid:   str with unique global identifier of actor.
        objid:  str with unique global identifier of object.

    Returns:     
        On fail, returns None.        
        On success, returns an list of inventory perception records containing 
        information about items/folders stored inside objid object. Inventory
        perception records are lists of strings. Two kinds of inventory
        records are retrieved by this action, 'objfolder' records containing 
        information about folders: 
            ['objfolder', id, objid, name, objid]
        or 'objitem' records containing information about items: 
            ['objitem', id, objid, name, descr, invtyp, assetyp]
        where:  id is the unique global id of folder/item;
                objid is the unique global identifier of object                
                name is the name of folder/item;
                descr is the description of item;
                invtyp is the inventory type of item.
                assetyp is the asset type of item.                
        On success, this action also adds the 'objfolder' and/or 'objitem'
        retrieved records to the perception base.           
        All perception records fields are strings.          
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookObjInventoryAction(objid)
    except:
        return None
 
 
def seek_avatars(acid):
    """ Search (look) for avatars in virtual world.

    Args:
        acid: str with unique global identifier of actor.

    Returns:     
        On fail, returns None.        
        On success, returns a list of 'avatar' perception records for each 
        avatar found in virtual world.
        On success, this action also adds to perception base a list of 
        perception records, for each avatar found.        
        See look_avatar() action for a description about types and formats of 
        perception records returned or added to perception base by this action.         
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookForAvatarsAction()
    except:
        return None
        
def seek_obj_children(acid,objid):
    """ Search (look) for children objects linked to objid object.

    Args:
        acid:   str with unique global identifier of actor.
        objid:  str with unique global identifier of target object

    Returns:    
        On fail, returns None.       
        On success, returns a list of 'obj' perception records for each 
        children object.
        On success, this action also adds to perception base a list of 
        perception records, for each children object.        
        See look_obj() action for a description about types and formats of 
        perception records returned or added to perception base by this action.         
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookForObjChildrenAction(objid)
    except:
        return None
        
def seek_all_objs(acid):
    """ Search (look) for all objects in region. Use with care!! Can be
        very time consuming.

    Args
        acid:       str with unique global identifier of actor.

    Returns:     
        On fail, returns None.        
        On success, returns a list of 'obj' perception records for each object
        in the region.
        On success, this action also adds to perception base a list of 
        perception records, for each object that match search criteria.        
        See look_obj() action for a description about types and formats of 
        perception records returned or added to perception base by this action.         
    """
    try:
        agent = ac.get_agctl(acid)
        resp= agent.ObsActs.LookForObjsAction()
    except Exception as error:
        ac.print_dbg('obsacts','seek_all_objs() error ',error)
        resp= None
    return resp

def seek_objs_by_radius(acid,rad):
    """ Search (look) for objects in a circle with radius rad around actor 
        (negative radius will search all region).

    Args:
        acid:       str with unique global identifier of actor.
        rad:        float, int or numeric str with search radius in meters,
                    if rad has a negative value will search all region.
        
    Returns:     
        On fail, returns None.       
        On success, returns a list of 'obj' perception records for each object
        that match search criteria.
        On success, this action also adds to perception base a list of 
        perception records, for each object that match search criteria.        
        See look_obj() action for a description about types and formats of 
        perception records returned or added to perception base by this action.         
    """
    try:
        agent = ac.get_agctl(acid)
        resp= agent.ObsActs.LookForObjsByRadiusAction(rad)
    except Exception as error:
        ac.print_dbg('obsacts','seek_objs_by_radius() error ',error)
        resp= None
    return resp

_objTypeToNumber = { 
    'prim':  '1',
    'tree':  '2',
    'grass': '3'
}

_primTypeToNumber = { 
    'unknown':  0,
    'box':      1,
    'cylinder': 2,
    'prism':    3,
    'sphere':   4,
    'torus':    5,
    'tube':     6,
    'ring':     7,
    'sculpt':   8,
    'mesh':     9
}

_treeTypeToNumber = {
    'pine1':        0,
    'oak':          1,
    'tropicalbush1':2,
    'palm1':        3,
    'dogwood':      4,
    'tropicalbush2':5,
    'palm2':        6,
    'cypress1':     7,
    'cypress2':     8,
    'pine2':        9,
    'plumeria':     10,
    'winterpine1':  11,
    'winteraspen':  12,
    'winterpine2':  13,
    'eucalyptus':   14,
    'fern':         15,
    'eelgrass':     16,
    'seasword':     17,
    'kelp1':        18,
    'beachgrass1':  19,
    'kelp2':        20
}

_grassTypeToNumber = {
    'grass0':       0,
    'grass1':       1,
    'grass2':       2,
    'grass3':       3,
    'grass4':       4,
    'undergrowth1': 5
}

def seek_objs_by_type(acid,rad,typ,subtyp):
    """ Search (look) for objects with particular type and subtype in a circle with 
        radius rad around actor (negative radius will search all region).

    Args:
        acid:       str with unique global identifier of actor.
        rad:        float, int or numeric str with search radius in meters,
                    if rad has a negative value will search all region.
        typ:        str with type of object, it can be:
                        'prim' - primitive object
                        'tree' - tree object
                        'grass' - grass object
        subtyp:     str with subtype of object, the value of subtyp depends on the 
                    value of typ, as follows:
                        If type is 'prim' (primitive object), subtyp can be:
                            'unknown',  'box',  'cylinder', 'prism',    'sphere',   
                            'torus',    'tube', 'ring',     'sculpt',   'mesh'
                        If the type is 'tree' (tree object), subtyp can be:
                            'pine1',        'pine2',        'oak',          'palm1',    
                            'palm2',        'dogwood',      'cypress1',     'cypress2', 
                            'plumeria',     'fern',         'eelgrass',     'seasword',
                            'kelp1',        'kelp2',        'beachgrass1',  'tropicalbush2',
                            'eucalyptus',   'winterpine1',  'winterpine2',  'tropicalbush1',  
                            'winteraspen'
                        If the type is 'grass' (grass object), subtyp can be:
                            'grass0',   'grass1',   'grass2',   'grass3',   'grass4',   
                            'undergrowth1'

    Returns:     
        On fail, returns None.        
        On success, returns a list of 'obj' perception records for each object
        that match search criteria.
        On success, this action also adds to perception base a list of 
        perception records, for each object that match search criteria.        
        See look_obj() action for a description about types and formats of 
        perception records returned or added to perception base by this action.         
    """
    try:
        agent = ac.get_agctl(acid)
        ntyp = _objTypeToNumber[typ]
        if ntyp==0:
            nsubtyp = _primTypeToNumber[subtyp]
        elif ntyp==1:
            nsubtyp = _treeTypeToNumber[subtyp]
        else:
            nsubtyp = _grassTypeToNumber[subtyp]            
        resp= agent.ObsActs.LookForObjsByTypeAction(rad,ntyp,nsubtyp)
    except Exception as error:
        ac.print_dbg('obsacts','seek_objs_by_type() error ',error)
        resp= None
    return resp

_srchModeToNumber = {
    'in':       1,
    'start':    2,
    'end':      3,
    'eq':       4,
    'diff':     5,
    'notin':    6,
    'notstart': 7,
    'notend':   8
}

def seek_objs_by_name(acid,rad,srchname,srchmode='in',srchcase='nocase'):
    """ Search (look) for objects with particular name in a circle with 
        radius rad around actor (negative radius will search all region).

    Args:
        acid:       str with unique global identifier of actor.
        rad:        float, int or numeric str with search radius in meters, 
                    if rad has a negative value will search all region.
        srchname:   str with name to be searched
        srchmode:   str that defines the mode of the search:
                        'in' - for substring search in property text
                        'start' - search if text starts with srchstr
                        'end' - search if text ends with srchstr
                        'eq' - check if srchstr and text are equal
                        'diff' - check if srchstr and text are different
                        'notin' - search if substring is not in text 
                        'notstart' - search if text not starts with srchstr
                        'notend' - search if text not ends with srchstr
        srchcase:   str that defines if the search will be case sensitive or not:
                        'nocase' - the search will be case insensitive
                        'case' - the search will be case sensitive

    Returns:     
        On fail, returns None.
        
        On success, returns a list of 'obj' perception records for each object
        that match search criteria.
        On success, this action also adds to perception base a list of 
        perception records, for each object that match search criteria.
        
        See look_obj() action for a description about types and formats of 
        perception records returned or added to perception base by this action.         
    """
    try:
        agent = ac.get_agctl(acid)
        nsrchmode = _srchModeToNumber[srchmode]
        bsrchcase = (srchcase=='case')
        resp= agent.ObsActs.LookForObjsByNameAction(rad,srchname,nsrchmode,bsrchcase)
    except Exception as error:
        ac.print_dbg('obsacts','seek_objs_by_name() error, srchmode=',srchmode,' srchcase=', srchcase)
        ac.print_dbg('obsacts',error)
        resp= None
    return resp

def seek_objs_by_descr(acid,rad,srchdescr,srchmode='in',srchcase='nocase'):
    """ Search (look) for objects with particular description in a circle 
        with radius rad around actor (negative radius will search all region).

    Args:
        acid:       str with unique global identifier of actor.
        rad:        float, int or numeric str with search radius in meters,
                    if rad has a negative value will search all region.
        srchdescr:  str with description to be searched
        srchmode:   str that defines the mode of the search:
                        'in' - for substring search in property text
                        'start' - search if text starts with srchstr
                        'end' - search if text ends with srchstr
                        'eq' - check if srchstr and text are equal
                        'diff' - check if srchstr and text are different
                        'notin' - search if substring is not in text 
                        'notstart' - search if text not starts with srchstr
                        'notend' - search if text not ends with srchstr
        srchcase:   str that defines if the search will be case sensitive or not:
                        'nocase' - the search will be case insensitive
                        'case' - the search will be case sensitive

    Returns:     
        On fail, returns None.
        
        On success, returns a list of 'obj' perception records for each object
        that match search criteria.
        On success, this action also adds to perception base a list of 
        perception records, for each object that match search criteria.
        
        See look_obj() action for a description about types and formats of 
        perception records returned or added to perception base by this action.         
    """
    try:
        agent = ac.get_agctl(acid)
        nsrchmode = _srchModeToNumber[srchmode]
        bsrchcase = (srchcase=='case')
        resp= agent.ObsActs.LookForObjsByDescrAction(rad,srchdescr,nsrchmode,bsrchcase)
    except Exception as error:
        ac.print_dbg('obsacts','seek_objs_by_descr() error ',error)
        resp= None
    return resp


def seek_objs(acid,rad,typ,subtyp,srchtxt='',srchin='name',srchmode='in',srchcase='nocase'):
    """ Search (look) for objects with particular type and subtype in a circle with 
        radius rad around actor (negative radius will search all region).
        Optionally, can search for objects with particular name or description.

    Args:
        acid:       str with unique global identifier of actor.
        rad:        float, int or numeric str with search radius in meters, 
                    if rad has a negative value will search all region.
        typ:        str with type of object, it can be:
                        'prim' - primitive object
                        'tree' - tree object
                        'grass' - grass object
        subtyp:     str with subtype of object, the value of subtyp depends on the 
                    value of typ, as follows:
                        If type is 'prim' (primitive object), subtyp can be:
                            'unknown',  'box',  'cylinder', 'prism',    'sphere',   
                            'torus',    'tube', 'ring',     'sculpt',   'mesh'
                        If the type is 'tree' (tree object), subtyp can be:
                            'pine1',        'pine2',        'oak',          'palm1',    
                            'palm2',        'dogwood',      'cypress1',     'cypress2', 
                            'plumeria',     'fern',         'eelgrass',     'seasword',
                            'kelp1',        'kelp2',        'beachgrass1',  'tropicalbush2',
                            'eucalyptus',   'winterpine1',  'winterpine2',  'tropicalbush1',  
                            'winteraspen'
                        If the type is 'grass' (grass object), subtyp can be:
                            'grass0',   'grass1',   'grass2',   'grass3',   'grass4',   
                            'undergrowth1'
        srchtxt:    optional str arg, if not None, it specifies the text 
                    to be used in the search.
        srchin:     optional str arg, must be set if srchtxt is specified. 
                    It defines where srchtxt must be searched: 
                        'name' - 1 search in the name of object 
                        'descr' - 2 search in the description of object
        srchmode:   optional str or numeric str arg, must be set if srchtxt 
                    is specified. It defines the mode of the search:
                        'in' - for substring search in property text
                        'start' - search if text starts with srchstr
                        'end' - search if text ends with srchstr
                        'eq' - check if srchstr and text are equal
                        'diff' - check if srchstr and text are different
                        'notin' - search if substring is not in text 
                        'notstart' - search if text not starts with srchstr
                        'notend' - search if text not ends with srchstr
        srchcase:   optional str that defines if the search will be case 
                    sensitive or not, must be set if srchtxt is specified:
                        'nocase' - the search will be case insensitive
                        'case' - the search will be case sensitive

    Returns:     
        On fail, returns None.        
        On success, returns a list of 'obj' perception records for each object
        that match search criteria.
        On success, this action also adds to perception base a list of 
        perception records, for each object that match search criteria.        
        See look_obj() action for a description about types and formats of 
        perception records returned or added to perception base by this action.         
    """
    try:
        agent = ac.get_agctl(acid)
        ntyp = _objTypeToNumber[typ]
        if ntyp==0:
            nsubtyp = _primTypeToNumber[subtyp]
        elif ntyp==1:
            nsubtyp = _treeTypeToNumber[subtyp]
        else:
            nsubtyp = _grassTypeToNumber[subtyp]
        if srchin=='descr':
            nsrchin=2
        else:
            nsrchin=1
        nsrchmode = _srchModeToNumber[srchmode]
        bsrchcase = (srchcase=='case')
        resp= agent.ObsActs.LookForObjsAction(rad,ntyp,nsubtyp,srchtxt,nsrchin,nsrchmode,bsrchcase)
    except Exception as error:
        ac.print_dbg('obsacts','seek_objs() error ',error)
        resp= None
    return resp
    
def seek_regions(acid):
    """ Search (look) for regions in virtual world.

    Args:
        acid:       str with unique global identifier of actor.

    Returns:     
        On fail, returns None.        
        On success, returns a list of 'region' perception records for each 
        region found in virtual world.
        On success, this action also adds to perception base a list of 
        perception records, for each region found.        
        See look_region() action for a description about types and formats of 
        perception records returned or added to perception base by this action.         
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.ObsActs.LookForRegionsAction()
    except:
        return None


