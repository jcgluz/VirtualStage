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
#   Module:     ModifyActions
#   Purpose:    Actions to modify objects of virtual world
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

""" Module ModifyActions - Actions to modify objects of virtual world
    Functions:
        degrab(acid,objid)
        derezz(acid,objid)
        take(acid,objid,foldname)
        grab(acid,objid)
        touch(acid,objid)
        move(acid, objid, x, y, z)
        paint(acid, objid, txtrid)
        resize(acid, objid, sx, sy, sz)
        rezz(acid, objname, objtyp, subtyp, x, y, z)
        rezz_with_rot(acid, objname, objtyp, subtyp, x, y, z, rotunit, rol, pit, yaw)
        rezz_with_size_rot(acid, objname, objtyp, subtyp, x, y, z, sx, sy, sz,
        rezz_with_size(acid, objname, objtyp, subtyp, x, y, z, sx, sy, sz)
        rotate(acid, objid, rotunit, rol, pit, yaw)
        set_descr(acid, objid, descr)
        set_material(acid, objid, mat)
        set_name(acid, objid, name)
        set_flags(acid, objid, phys, temp, phant, shad)
        import_xml(acid, objfile, x, y, z)
        export_xml(acid, objid, objfile)
    
"""


import ActorController as ac

#region ModificationAcions

def degrab(acid,objid):
    """ Drop or 'de grab' object identified by objid

    Args:
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be dropped
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.DeGrabAction(objid)
    except:
        return False

def derezz(acid,objid):
    """ Delete or 'de-rezz' object identified by objid from virtual world

    Args:
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be de-rezzed
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.DerezObjAction(objid)
    except:
        return False

def take(acid,objid,foldname):
    """ Take an object identified by objid from virtual world and store
        it in inventory in the foldname folder. The object is de-rezzed
        or deleted from virtual world.

    Args:
        acid: str with unique global identifier of actor
        objid: str with unique global identifier of object to be de-rezzed
        foldname: str with name of inventory folder that will receive object
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.TakeObjAction(objid,foldname)
    except:
        return False

def grab(acid,objid):
    """ Grab object identified by objid

    Args:
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be grabbed
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.GrabAction(objid)
    except:
        return False

def touch(acid,objid):
    """ Touch object identified by objid
    
    Args:
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be touched
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.TouchAction(objid)
    except:
        return False

def select(acid,objid):
    """ Select object identified by objid

    Args:
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be selected
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.SelObjAction(objid)
    except:
        return False

def deselect(acid,objid):
    """ Deselect object identified by objid

    Args:
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be deselected
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.DeselObjAction(objid)
    except:
        return False

def click(acid,objid):
    """ Click on object identified by objid

    Args:
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be clicked
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.ClickObjAction(objid)
    except:
        return False

def move(acid, objid, x, y, z):
    """ Move objid object to x,y,z position

    Args:
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be moved
        x,y,z:  float, int or numeric str numbers with X,Y,Z coordinates 
                to move object
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.MoveObjAction(objid,x,y,z)
    except:
        return False

def paint(acid, objid, txtrid):
    """ Paint objid object with texture identified by txtrid
        Set the default texture of object to txtrid
    
    Args:
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be painted
        txtrid: str with unique global identifier of texture
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.PaintObjAction(objid,txtrid)
    except:
        return False

def resize(acid, objid, sx, sy, sz):
    """ Change size of objid object to sx,sy,sz scale

    Args:
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be resized
        sx:     float, int or numeric str with size (or scale) of object 
                in X-axis direction
        sy:     float, int or numeric str with size (or scale) of object 
                in Y-axis direction
        sz:     float, int or numeric str with size (or scale) of object 
                in Z-axis direction
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.ResizeObjAction(objid,sx,sy,sz)
    except:
        return False

def rezz(acid, objname, objtyp, subtyp, x, y, z):
    """ Create or 'rezz' a new object in virtual world
    
    Args: 
        acid: str with unique global identifier of actor
        objname: str with name of new object
        objtyp: type of new obj, can be: 'prim','tree','grass','item'
        subtyp: subtype of object, if type is 'prim', it can be:
                    'box','cylinder','prism','sphere','torus','tube','ring',
                    'sculpt','mesh'
                if type is 'tree', it can be: 
                    'pine1','oak','tropicalbush1','palm1','dogwood',
                    'tropicalbush2','palm2','cypress1','cypress2',
                    'pine2','plumeria','winterpine1','winteraspen',
                    'winterpine2','eucalyptus','fern','eelgrass','seasword',
                    'kelp1','beachgrass1','kelp2'
                if type is 'grass', it can be: 
                    'grass0','grass1','grass2','grass3','grass4','undergrowth1'
                if type is 'item', then subtyp is a str with the path 
                    to an actor's inventory item, which will be copied and 
                    rezzed as a new object in virtual world
        x,y,z: float, int or numeric str numbers with X,Y,Z coordinates to rezz 
            the new object
        
    Returns:     
        On fail, returns None
        On success, returns the unique global identifier of new object
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.RezObjAction(objname,objtyp,subtyp,x,y,z)
    except:
        return None

def rezz_with_rot(acid, objname, objtyp, subtyp, x, y, z, unit, rol, pit, yaw):
    """ Create or 'rezz' a new object in virtual world and rotates it 
    
    Args: 
        acid: str with unique global identifier of actor
        objname: str with name of new object
        objtyp: see rezz_obj() action
        subtyp: see rezz_obj() action
        x,y,z: floats with X,Y,Z coordinates to rezz the new object
        unit: angle rot units, can be 'dg' for degrees or 'rad' for radians
        rol: float, int or numeric str with new X-axis euler angle of obj 
            in radians/degrees
        pit: float, int or numeric str with new Y-axis euler angle of obj 
            in radians/degrees
        yaw: float, int or numeric str with new Z-axis euler angle of obj 
            in radians/degrees
        
    Returns:     
        On fail, returns None
        On success, returns the unique global identifier of new object
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.RezObjRotAction(objname,objtyp,subtyp,x,y,z,
                                        unit,rol,pit,yaw)
    except:
        return None

def rezz_with_size_rot(acid, objname, objtyp, subtyp, x, y, z, sx, sy, sz,
                     unit, rol, pit, yaw):
    """ Create or 'rezz' a new object in virtual world and resizes & rotates it 
    
    Args: 
        acid:   str with unique global identifier of actor
        objname: str with name of new object
        objtyp: see rezz_obj() action
        subtyp: see rezz_obj() action
        x,y,z:  float, int or numeric str with X,Y,Z coordinates to rezz 
                the new object
        sx:     float, int or numeric str with size (or scale) of new obj 
                in X-axis direction
        sy:     float, int or numeric str with size (or scale) of new obj 
                in Y-axis direction
        sz:     float, int or numeric str with size (or scale) of new obj 
                in Z-axis direction
        unit:   angle rot units, can be 'dg' for degrees or 'rad' for radians
        rol:    float, int or numeric str with new X-axis euler angle of new 
                obj in radians/degrees
        pit:    float, int or numeric str with new Y-axis euler angle of new 
                obj in radians/degrees
        yaw:    float, int or numeric str with new Z-axis euler angle of new 
                obj in radians/degrees
        
    Returns:     
        On fail, returns None
        On success, returns the unique global identifier of new object
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.RezObjSizeRotAction(objname,objtyp,subtyp,x,y,z,
                                        sx,sy,sz,unit,rol,pit,yaw)
    except:
        return None

def rezz_with_size(acid, objname, objtyp, subtyp, x, y, z, sx, sy, sz):
    """ Create or 'rezz' a new object in virtual world and resizes it 
    
    Args: 
        acid:       str with unique global identifier of actor
        objname:    str with name of new object
        objtyp:     see rezz_obj() action
        subtyp:     see rezz_obj() action
        x,y,z:      float, int or numeric str with X,Y,Z coordinates to rezz 
                    the new object
        sx:         float, int or numeric str with size (or scale) of new obj 
                    in X-axis direction
        sy:         float, int or numeric str with size (or scale) of new obj 
                    in Y-axis direction
        sz:         float, int or numeric str with size (or scale) of new obj 
                    in Z-axis direction
        
    Returns:     
        On fail, returns None
        On success, returns the unique global identifier of new object
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.RezObjSizeAction(objname,objtyp,subtyp,x,y,z,sx,sy,sz)
    except:
        return None

def rotate(acid, objid, unit, rol, pit, yaw):
    """ Rotate an object in virtual world
    
    Args: 
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be resized
        unit:   angle rot units, can be 'dg' for degrees or 'rad' for radians
        rol:    float, int or numeric str with new X-axis euler angle of obj 
                in radians/degrees
        pit:    float, int or numeric str with new Y-axis euler angle of obj 
                in radians/degrees
        yaw:    float, int or numeric str with new Z-axis euler angle of obj 
                in radians/degrees
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.RotateObjAction(objid,unit,rol,pit,yaw)
    except:
        return False

def set_descr(acid, objid, descr):
    """ Set description property of object
    
    Args: 
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be resized
        descr:  str with objects's new description (a text with at most 127 chars)
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.SetDescrAction(objid,descr)
    except:
        return False

def set_material(acid, objid, mat):
    """ Set material property of object
    
    Args: 
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be resized
        mat:    str with new material of obj, can be: 'flesh','glass','light',
                    'metal','plastic','rubber','stone','wood'
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.SetMaterialAction(objid,mat)
    except:
        return False

def set_name(acid, objid, name):
    """ Set name property of object
    
    Args: 
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be resized
        name:  str with objects's new name (a text with at most 63 chars)
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.SetNameAction(objid,name)
    except:
        return False

def set_flags(acid, objid, phys, temp, phant, shad):
    """ Set additional boolean control flags of object
    
    Args: 
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to be resized
        phys:   boolean, if true allows obj to be affected by simulator physics
        temp:   boolean, if true makes obj temporary, it will disappear 1 minute 
                after its initial rezz time
        phant:  boolean, if true makes obj a ghost that other objs or avatars 
                can pass through
        shad:   boolean, if true enable obj to cast shadows
        
    Returns:     
        On fail, returns False
        On success, True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.SetFlagsAction(objid,phys,temp,phant,shad)
    except:
        return False

def import_xml(acid, objfile, x, y, z):
    """ Import a new object from a previously exported XML file and rezz it
        in the virtual world 
    
    Args: 
        acid:       str with unique global identifier of actor
        objfile:    str with name of previously exported XML file
        x,y,z:      float, int or numeric str numbers with X,Y,Z coordinates to rezz 
                    the new object
        
    Returns:     
        On fail, returns False
        On success, returns True
            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.ImportObjectAction(objfile,x,y,z)
    except:
        return False

def export_xml(acid, objid, objfile):
    """ Export a virtual world object to a XML file
    
    Args: 
        acid:       str with unique global identifier of actor
        objfile:    str with name of XML file that will store the object
        
    Returns:     
        On fail, returns False
        On success, returns True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.ModActs.ExportObjectAction(objid,objfile)
    except:
        return False


