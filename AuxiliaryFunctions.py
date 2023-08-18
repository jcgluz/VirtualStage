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
#   Module:     AuxiliaryFunctions
#   Purpose:    Module that implements some auxiliary functions
#               used in VirtualStage 
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

""" Module AuxiliaryFunctions - module that implements some 
        auxiliary functions used by VirtualStage actors
    Functions:
        maybe(threshold)
        optional(threshold,text)
        find_nearest_obj(acid)
        find_obj_with_name(acid,name, radius=20.0)
        find_place(acid,stx,sty)
        find_place_with_name_or_descr(acid,name)
        find_scene(acid,x,y)
        find_scene_with_name(acid,scenename)
        compute_scene_central_point(acid,sceneid)
        find_task_with_name(acid,taskname)
        learn_new_known_place(acid, lang, place_x, place_y)
        print_obj_type(acid, lang, obj)
        print_obj_info(acid, lang, obj)
        print_obj_name(acid,lang,obj)
        print_obj_descr(acid,lang,obj)
        print_obj_use(acid,lang,obj)
        print_obj_attr(acid,lang,attr,obj)
        print_place_info(acid,lang,place)
        print_place_name(acid, lang, place)
        print_place_descr(acid,lang,place)
        print_place_event(acid,lang,place)
        print_place_attr(acid,lang,attr,place)
        print_scene_info(acid,lang,scene)
        print_scene_name(acid, lang, scene)
        print_task_info(acid, lang, task)
        string_similarity(str1, str2)
        set_string_similarity_metric(metric)
        possible_gender_of_name(lang, name)
        translate(lang, termtype, termval, deftrans='')
        importance_to_value(lang, imptxt)
        importance_to_text(lang, impval)
        relangle_to_avatar(acid,avid)
        relangle_to_avatar_with_name(acid,avname)
        reldir_to_avatar(acid,avid)
        reldir_to_avatar_with_name(acid,avname)
        vertpos_to_avatar(acid,avid)
        vertpos_to_avatar_with_name(acid,avname)
        relangle_to_obj(acid,objid)
        reldir_to_obj(acid,objid)
        vertpos_to_obj(acid,objid)
        check_inside_poly(p, poly)
        compute_poly_centroid(vertices)
        compute_convex_poly(points)
"""

import random
import clr
import time
import re
import uuid
import math
import nltk
import unidecode
from nltk.metrics.distance import jaro_winkler_similarity
from nltk.metrics.distance import jaro_similarity
from nltk.metrics.distance import edit_distance
import ActorController as ac
import DialogController as dc


#*******************************************
# PROBABILISTIC DECISION FUNCTIONS
#******************************************

def maybe(threshold):
    if random.random()>threshold:
        return False
    return True


def optional(threshold,text):
    if random.random()>threshold:
        return text
    return ''

    
#*******************************************
# FUNCTIONS TO FIND THINGS IN VR
#******************************************

def _objDistanceField(obj):
    return float(obj[5])
 
 
def find_nearest_obj(acid):
    """ Find the nearest object from the position of avatar 
        controlled by the actor.
        
    Args:
        acid:   str with unique global identifier of actor.
        
    Returns:    
        On fail, returns None.        
        On success, returns the UUID of nearest object. 
    """
    try:
        nearobjs = ac.seek_objs_by_radius(acid,10.0)
        ac.print_dbg('af','nearobjs=',nearobjs)
        nearobjs.sort(key=_objDistanceField)
        return nearobjs[0]
    except:
        return None

def find_obj_with_name(acid, name, radius=20.0):
    """ Find the object with name name.
        
    Args:
        acid:   str with unique global identifier of actor
        name:   str with object name
        radius: float, int or numeric str with search radius in meters.
        
    Returns:    
        On fail, returns None.        
        On success, returns the UUID of object. 
    """
    obj = ac.seek_objs_by_name(acid,radius,name,1,False)
    if obj==None or obj==[]:
        return None
    return obj[0][1]


def _inSamePlace(x,y,place_x,place_y,place_r):
    return math.dist([x,y],[place_x,place_y])<=place_r
    

def find_place(acid,x,y):
    """ Check if it is a known place at given x,y coordinates.
        
    Args:
        acid: str with unique global identifier of actor
        x,y: str float values of x,y coordinates
        
    Returns:    
        On fail, returns None.        
        On success, returns a known place record with following structure:
            ['known-place', id, x, y]
        where:
            id is a str with the unique UUID of the known place;
            x, y are str float values with the X,Y coordinates of central 
                position of place.
    """
    try:
        ac.print_dbg('af','findplace ','x=',x,' y=', y)
        pos_x=float(x)
        pos_y=float(y)
        kplaces = ac.remember_all(acid,['known-place'])
        for place in kplaces:
            place_x=float(place[2])
            place_y=float(place[3])
            radius = ac.remember(acid,['place-radius',place[1]])
            place_r = float(radius[2])
            ac.print_dbg('af','findplace',' checking place',' x=',place_x,' y=',place_y,' r=',place_r)
            if _inSamePlace(pos_x,pos_y,place_x,place_y,place_r):
                ac.print_dbg('af','findplace',' found place')
                return place
        return None
    except:
        return None

def find_place_with_name_or_descr(acid,name):
    """ Find known place with name or description that match name argument.
        
    Args:
        acid:   str with unique global identifier of actor
        name:   str with place name
        
    Returns:    
        On fail, returns None.        
        On success, returns a tuple (simil,id,term) where
            simil is the maximum similarity coeficient found in 
            the search, id is the UUID of the known place with
            maximum similarity and term is the name or description
            of this known place that achieved the maximum similarity
            index.
    """
    maxsimil = 0.0
    maxsimil_placeid=None
    maxsimil_placename=None
    placenames = ac.remember_all(acid,['place-name'])
    for place in placenames:
        simil = string_similarity(name,place[2])
        if simil>maxsimil:
            maxsimil = simil
            maxsimil_placeid=place[1]
            maxsimil_placename=place[2]
    placedescrs = ac.remember_all(acid,['place-descr'])
    for place in placedescrs:
        simil = string_similarity(name,place[2])
        if simil>maxsimil:
            maxsimil = simil
            maxsimil_placeid=place[1]
            maxsimil_placename=place[2]
    if  maxsimil<0.7:
        return None
    return (maxsimil,maxsimil_placeid,maxsimil_placename)
 
def find_scene(acid,x,y):
    """ Check if it is a known scene at given x,y coordinates.
        
    Args:
        acid: str with unique global identifier of actor
        x,y: str float values of x,y coordinates
        
    Returns:    
        On fail, returns None.        
        On success, returns a known place record with following structure:
            ['known-scene', id]
        where:
            id is a str with the unique UUID of the known scene;
    """
    try:
        ac.print_dbg('af','findscene ','x=',x,' y=', y)
        kscenes = ac.remember_all(acid,['known-scene'])
        pos_x=float(x)
        pos_y=float(y)
        found=False
        for scene in kscenes:
            scenepts = ac.remember_all(acid,['scene-point',scene[1]])
            scenepoly=[]
            for scenept in scenepts:
                scenepoly += [(float(scenept[2]),float(scenept[3]))]
            if check_inside_poly((pos_x,pos_y),scenepoly):
                ac.print_dbg('af','findscene',' found scene')
                return scene
        return None
    except:
        return None

def find_scene_with_name(acid,scenename):
    """ Find the UUID of the scene with name scenename.
        
    Args:
        acid: str with unique global identifier of actor
        scenename: str with the name of scene
        
    Returns:    
        On fail, returns None.        
        On success, returns a known scene record with following structure:
            ['known-scene', id]
        where:
            id is a str with the unique UUID of the known scene;
    """
    try:
        kscenes = ac.remember_all(acid,['known-scene'])
        for scene in kscenes:
            sname = ac.remember(acid,['scene-name',scene[1]])
            if sname!=None and string_similarity(sname[2],scenename)>=0.9:
                return scene
        return None
    except:
        return None

def compute_scene_central_point(acid,sceneid):
    """ Compute the x,y coordinates of the central point of scene with
        sceneid unique id
        
    Args:
        acid: str with unique global identifier of actor
        sceneid: str with the unique id (the UUID) of scene
        
    Returns:    
        On fail, returns None.        
        On success, a pair (x,y) with X,Y coordinate of scene central point.
    """
    try:
        if sceneid==None:
            return None
        scenepts = ac.remember_all(acid,['scene-point',sceneid])
        scenepoly=[]
        for scenept in scenepts:
            scenepoly += [(float(scenept[2]),float(scenept[3]))]
        ac.print_dbg('af','scenepoly=',scenepoly)
        convex_scenepoly = compute_convex_poly(scenepoly)
        ac.print_dbg('af','convec_scenepoly=',convex_scenepoly)
        scenecentroid = compute_poly_centroid(convex_scenepoly)
        ac.print_dbg('af','scenecentroid=',scenecentroid)
        return scenecentroid
    except:
        return None

def find_task_with_name(acid,taskname):
    """ Find the UUID of the task with name taskname.
        
    Args:
        acid: str with unique global identifier of actor
        taskname: str with the name of task
        
    Returns:    
        On fail, returns None.        
        On success, returns a known task record with following structure:
            ['known-task', id]
        where:
            id is a str with the unique UUID of the known scene;
    """
    try:
        ktasks = ac.remember_all(acid,['known-task'])
        for task in ktasks:
            tname = ac.remember(acid,['task-name',task[1]])
            if tname!=None and string_similarity(tname[2],taskname)>=0.9:
                return task
        return None
    except:
        return None



#*******************************************
# FUNCTIONS TO LEARN FACTS ABOUT OBJECTS AND 
# PLACES - FEEDBACK IS IN PORTUGUESE LANGUAGE 
# (TERSE ENGLISH FEEDBACKS IN OTHER LANGS.)
#******************************************

def learn_new_known_place(acid, lang, x, y):
    """ Record a new known place.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        x, y: str float values with the X,Y coordinates of central 
            position of new known place.
        
    Returns:    
        Returns a known-place record with information about the new
        known place. This record has the following structure:
            ['known-place', id, x, y]
        where:
            id is a new random UUID for the known place
            x,y are the X,Y central coordinates of the known place
        The known-place record is also stored in memory. This function
        also stores in memory a place-radius record related to the known 
        place. This record has the following structure:
            ['place-radius', id, r]
        where id is the UUID of the new known place, and r is the radius 
        size in meters of this place from its central position. The default 
        initial radius size for known places is 5.0 meters, but this can be 
        easily changed updating this record.        
    """
    # Is a new place, generate a random unique ID for this new place 
    placeid = str(uuid.uuid4())
    # Get default radius for places, from its central position 
    radius_rec = ac.remember(acid,['default-place-radius'])
    if radius_rec!=None:
        r = radius_rec[1]
    else:
        # Default radius of places not defined, set it as 5 meters
        r = '5.0'
        ac.record(acid,['default-place-radius','5.0'])
    # Register the new place as a known place
    newplace=['known-place',placeid,x,y]
    ac.record(acid,newplace)
    # Register the default place radius as the radius of the place
    ac.record(acid,['place-radius',placeid,r])
    return newplace



#*******************************************
# FUNCTIONS FOR PRINT INFORMATION ABOUT 
# OBJECTS AND PLACES IN PORTUGUESE LANGUAGE 
# (RETURN TERSE ENGLISH PHRASES IN OTHER LANGS.)
#******************************************

def print_obj_type(acid, lang, obj):
    """ Print type of the object in lang language.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        obj: obj record as returned by look_obj(), see look_obj()
            help for details.
        
    Returns:    
        Returns a string with information about the type of the object in
        the language defined by lang. This string can be sent back to user. 
        Currently only accepts pt-br language. For the remaining languages 
        generates a string in English.
    """
    if obj==None:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Cannot see object'
        return dc.gen_speak(acid,'naoVejoObjeto')
    try:
        objtype = obj[3]
        objsubtype = obj[4]
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Is '+objsubtype+' '+objtype      
        if objtype=='prim':
            primtype = translate('pt-br','primtype',objsubtype.casefold(),'desconhecido')
            return dc.gen_speak(acid,'esseObjetoEh(TIPO)',[primtype])
        if objtype=='tree':
            treetype = translate('pt-br','treetype', objsubtype.casefold(), 'desconhecida')
            return dc.gen_speak(acid,'essaPlantaEh(TIPO)',[treetype])
        if objtype=='grass':
            grasstype = translate('pt-br','grasstype', objsubtype.casefold(), 'desconhecida')
            return dc.gen_speak(acid,'essaGramaEh(TIPO)',[grasstype])
        return "Isso é '"+primtype+"'. "
    except:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Do not know this object'
        return dc.gen_speak(acid,'naoReconhecoObjeto')

def print_obj_info(acid, lang, obj):
    """ Print information about the object, including the type, name,
        description and use of the object (if available) in the
        lang language.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        obj: obj record as returned by look_obj(), see look_obj()
            help for details.
        
    Returns:    
        Returns a string with information about the object in language 
        defined by lang. This string can be sent back to user. 
        Currently only works with pt-br language. For the remaining 
        languages generates a string in English.
    """
    if obj==None:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Cannot see object'
        return dc.gen_speak(acid,'naoVejoObjeto')
    try:
        objtype = obj[3]
        objsubtype = obj[4]
        objname_rec = ac.remember(acid,['obj-name',obj[1]])
        objname = objname_rec[2] if objname_rec!=None else obj[2]
        objdescr_rec = ac.remember(acid,['obj-descr',obj[1]])
        objdescr = objdescr_rec[2] if objdescr_rec!=None else obj[12]
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Is '+objsubtype+' '+objtype+' with name '+objname
        typetxt = print_obj_type(acid,lang,obj)
        nametxt = (dc.gen_speak(acid,'conhecoNomeObjeto(NOME)',[objname]) if objname_rec!=None 
                    else dc.gen_speak(acid,'nomeObjetoMundoVirtual(NOME)',[objname]))   
        descrtxt=(dc.gen_speak(acid,'conhecoDescricaoObjeto(DESCR)',[objdescr]) if objdescr!="" 
                    else "")
        objuse_rec = ac.remember(acid,['obj-use',obj[1]])
        usetxt = (dc.gen_speak(acid,'conhecoUsoObjeto(USO)',[objuse_rec[2]]) if objuse_rec!=None
                    else "")           
        if maybe(0.5):
            return typetxt+".\n"+nametxt+".\n"+descrtxt+".\n"+usetxt+"."
        return typetxt+".\n"+descrtxt+".\n"+nametxt+".\n"+usetxt+". "
    except:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Do not know this object'
        return dc.gen_speak(acid,'naoReconhecoObjeto')

def print_obj_name(acid,lang,obj):
    """ Print the name of the object in lang language.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        obj: obj record as returned by look_obj(), see look_obj()
            help for details.
        
    Returns:    
        Returns a string with information about the name of the object in
        the language defined by lang. This string can be sent back to user. 
        Currently only accepts pt-br language. For the remaining languages 
        generates a string in English.
    """
    if obj==None:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Cannot see object'
        return dc.gen_speak(acid,'naoVejoObjeto')
    try:
        objname_rec = ac.remember(acid,['obj-name',obj[1]])
        objname = objname_rec[2] if objname_rec!=None else obj[2]
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return objname
        if objname_rec!=None:
            return dc.gen_speak(acid,'conhecoNomeObjeto(NOME)',[objname])
        return dc.gen_speak(acid,'nomeObjetoMundoVirtual(NOME)',[objname])    
    except:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Do not know this object'
        return dc.gen_speak(acid,'naoReconhecoObjeto')

def print_obj_descr(acid,lang,obj):
    """ Print description of the object in lang language.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        obj: obj record as returned by look_obj(), see look_obj()
            help for details.
        
    Returns:    
        Returns a string with description about the object in the
        language defined by lang. This string can be sent back to user. 
        Currently only accepts pt-br language. For the remaining languages 
        generates a string in English.
    """
    if obj==None:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Cannot see object'
        return dc.gen_speak(acid,'naoVejoObjeto')
    try:
        objtype = obj[3]
        objsubtype = obj[4]
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Is '+objsubtype+' '+objtype       
        objdescr_rec = ac.remember(acid,['obj-descr',obj[1]])
        objdescr = objdescr_rec[2] if objdescr_rec!=None else obj[12]
        if objdescr=="":
            return print_obj_type(acid,lang,obj)
        if objtype=='prim':
            primtype = translate('pt-br','primtype',objsubtype.casefold(),'desconhecido')
            return dc.gen_speak(acid,'esseObjetoEh(TIPO;DESCR)',[primtype,objdescr])
        if objtype=='tree':
            treetype = translate('pt-br','treetype', objsubtype.casefold(), 'desconhecida')
            return dc.gen_speak(acid,'essaPlantaEh(TIPO;DESCR)',[treetype,objdescr])
        if objtype=='grass':
            grasstype = translate('pt-br','grasstype', objsubtype.casefold(), 'desconhecida')
            return dc.gen_speak(acid,'essaGramaEh(TIPO;DESCR)',[grasstype,objdescr])
        return "Isso é um '"+objdescr
    except:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Do not know this object'
        return dc.gen_speak(acid,'naoReconhecoObjeto')


def print_obj_use(acid,lang,obj):
    """ Print information about the recorded use of the object 
        in lang language.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        obj: obj record as returned by look_obj(), see look_obj()
            help for details.
        
    Returns:    
        Returns a string with information about the use of the object in
        the language defined by lang. This string can be sent back to user. 
        Currently only accepts pt-br language. For the remaining languages 
        generates a string in English.
    """
    if obj==None:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Cannnot see object'
        return dc.gen_speak(acid,'naoVejoObjeto')
    try:
        usetxt=""
        objuse_rec = ac.remember(acid,['obj-use',obj[1]])
        if objuse_rec!=None:
            return dc.gen_speak(acid,'naoConhecoUsoObjeto')
        return dc.gen_speak(acid,'conhecoUsoObjeto(USO)',[objuse_rec[2]])
    except:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Do not know this object'
        return dc.gen_speak(acid,'naoReconhecoObjeto')


def print_obj_attr(acid,lang,attr,obj):
    """ Print information about some recorded attribute (or property) 
        about the object in lang language.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        attr: str with identifier of object's attribute (or property)
        obj: obj record as returned by look_obj(), see look_obj()
            help for details.
        
    Returns:    
        Returns a string with information about some attribute (or property) 
        of the object in language defined by lang. This string can be sent 
        back to user. 
        Currently only accepts pt-br language. For the remaining languages 
        generates a string in English.
    """
    if obj==None:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Cannnot see object'
        return dc.gen_speak(acid,'naoVejoObjeto')
    try:
        if attr==None or attr=="":
            if lang.lower()!='pt' and lang.lower()!='pt-br':
                return 'Property not informed'
            return dc.gen_speak(acid,'naoSeiQualAtributo')
        objattr_rec = ac.remember(acid,['obj-attr',obj[1],attr])
        if objattr_rec==None:
            return dc.gen_speak(acid,'naoConhecoEsseAtributo')
        return dc.gen_speak(acid,'atributoObjetoEh(PROP;VAL)',[objattr_rec[4],objattr_rec[3]])
    except:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Do not know this object'
        return dc.gen_speak(acid,'naoReconhecoObjeto')


def print_place_info(acid,lang,place):
    """ Print information about some known place, including the name
        and description of the place (if available) in the
        lang language.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        place: known-place record, see learn_new_known_place()
            help for details.
        
    Returns:    
        Returns a string with information about the place in language 
        defined by lang. This string can be sent back to user. 
        Currently only works with pt-br language. For the remaining 
        languages generates a string in English.
    """
    if place==None:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Cannot see place'
        return dc.gen_speak(acid,'naoReconhecoLugar')
    try:
        placeid=place[1]
        placename_rec = ac.remember(acid,['place-name',placeid])
        if placename_rec==None:
            if lang.lower()!='pt' and lang.lower()!='pt-br':
                return 'Do not know the name of this place'
            return dc.gen_speak(acid,'naoReconhecoNomeLugar')       
        placename = placename_rec[2]
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Place name is '+placename
        nametxt=dc.gen_speak(acid,'conhecoNomeLugar(NOME)',[placename]) if placename!="" else ""
        placedescr_rec = ac.remember(acid,['place-descr',placeid])
        placedescr = placedescr_rec[2] if placedescr_rec!=None else ""
        descrtxt=dc.gen_speak(acid,'conhecoDescricaoLugar(DESCR)',[placedescr]) if placedescr!="" else ""
        if maybe(0.5) and descrtxt!="":
            return descrtxt+".\n"+nametxt
        return nametxt+".\n"+descrtxt
    except:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Do not know this place'
        return dc.gen_speak(acid,'naoAcheiLugar')
        

def print_place_name(acid, lang, place):
    """ Print information about the name of a known place in the
        lang language.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        place: known-place record, see learn_new_known_place()
            help for details.
        
    Returns:    
        Returns a string with information about the name of place in
        language defined by lang. This string can be sent back to user. 
        Currently only works with pt-br language. For the remaining 
        languages generates a string in English.
    """
    if place==None:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Cannnot see place'
        return dc.gen_speak(acid,'naoReconhecoLugar')
    try:
        placeid=place[1]
        placename_rec = ac.remember(acid,['place-name',placeid])
        if placename_rec==None:
            if lang.lower()!='pt' and lang.lower()!='pt-br':
                return 'Do not know the name of this place'
            return dc.gen_speak(acid,'naoReconhecoNomeLugar')       
        placename = placename_rec[2]
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Place name is '+placename
        return  dc.gen_speak(acid,'conhecoNomeLugar(NOME)',[placename])    
    except:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Do not know this place'
        return dc.gen_speak(acid,'naoAcheiLugar')


def print_place_descr(acid,lang,place):
    """ Print description about the known place in the
        lang language.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        place: known-place record, see learn_new_known_place()
            help for details.
        
    Returns:    
        Returns a string with description about the place in language
        defined by lang. This string can be sent back to user. 
        Currently only works with pt-br language. For the remaining 
        languages generates a string in English.
    """
    if place==None:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Cannnot see place'
        return dc.gen_speak(acid,'naoReconhecoLugar')
    try:
        placeid=place[1]
        placedescr_rec = ac.remember(acid,['place-descr',placeid])
        if placedescr_rec==None:
            if lang.lower()!='pt' and lang.lower()!='pt-br':
                return 'Do not know the name of this place'
            return dc.gen_speak(acid,'naoReconhecoDescricaoLugar')         
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Place description is '+placedescr_rec[2]
        return dc.gen_speak(acid,'conhecoDescricaoLugar(DESCR)',[placedescr_rec[2]])
    except:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Do not know this place'
        return dc.gen_speak(acid,'naoAcheiLugar')
        

def print_place_event(acid,lang,place):
    """ Print information about some event that occured in
        the known place in the lang language.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        place: known-place record, see learn_new_known_place()
            help for details.
        
    Returns:    
        Returns a string with information about some event that ocurred
        in the place in language defined by lang. This string can be 
        sent back to user. 
        Currently only works with pt-br language. For the remaining 
        languages generates a string in English.
    """
    if place==None:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Cannnot see place'
        return dc.gen_speak(acid,'naoReconhecoLugar')
    try:
        placeid=place[1]
        placeev_rec = ac.remember(acid,['place-event',placeid])
        if placeev_rec==None:
            if lang.lower()!='pt' and lang.lower()!='pt-br':
                return 'Do not know events on this place'
            return dc.gen_speak(acid,'naoReconhecoEventoLugar')        
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Here happened '+placeev_rec[2]
        return dc.gen_speak(acid,'conhecoEventoLugar(EVENTO)',[placeev_rec[2]])
    except:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Do not know this place'
        return dc.gen_speak(acid,'naoAcheiLugar')


def print_place_attr(acid,lang,attr,place):
    """ Print information about some recorded attribute (or property) 
        about the known place in lang language.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        attr: str with identifier of object's attribute (or property)
        obj: obj record as returned by look_obj(), see look_obj()
            help for details.
        
    Returns:    
        Returns a string with information about some attribute (or property) 
        of the place in language defined by lang. This string can be sent 
        back to user. 
        Currently only accepts pt-br language. For the remaining languages 
        generates a string in English.
    """
    if place==None:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Cannnot see place'
        return dc.gen_speak(acid,'naoReconhecoLugar')
    try:
        placeid=place[1]
        if attr==None or attr=="":
            if lang.lower()!='pt' and lang.lower()!='pt-br':
                return 'Property not informed'
            return dc.gen_speak(acid,'naoSeiQualAtributo')
        placeattr_rec = ac.remember(acid,['place-attr',placeid,attr])
        if placeattr_rec==None:
            return dc.gen_speak(acid,'naoConhecoEsseAtributo')
        return dc.gen_speak(acid,'atributoLugarEh(PROP;VAL)',[placeattr_rec[4],placeattr_rec[3]])
    except:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Do not know this place'
        return dc.gen_speak(acid,'naoAcheiLugar')


def print_scene_info(acid,lang,scene):
    """ Print information about some known scene in the
        lang language.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        scene: known-scene record with following structure:
                ['known-scene', id]
            where:
                id is a str with the unique UUID of the known scene;
        
    Returns:    
        Returns a string with information about the scene in language 
        defined by lang. This string can be sent back to user. 
        Currently only works with pt-br language. For the remaining 
        languages generates a string in English.
    """
    if scene==None:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'I do not known any scene here'
        return "Não conheco nenhuma cena aqui"
    try:
        sceneid=scene[1]
        scenename_rec = ac.remember(acid,['scene-name',sceneid])
        if scenename_rec==None:
            if lang.lower()!='pt' and lang.lower()!='pt-br':
                return 'Do not know the name of this scene'
            return "Não conheço o nome da cena aqui"       
        scenename = scenename_rec[2]
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Scene name is '+scenename
        nametxt="O nome da cena aqui é "+scenename
        sceneinfo_rec = ac.remember(acid,['scene-info',sceneid])
        if sceneinfo_rec==None:
            return nametxt
        return nametxt+".\n"+"A cena aqui é "+sceneinfo_rec[2]
    except:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'I do not known any scene here'
        return "Não conheco nenhuma cena aqui" 
        

def print_scene_name(acid, lang, scene):
    """ Print information about the name of a known scene in the
        lang language.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        scene: known-scene record with following structure:
                ['known-scene', id]
            where:
                id is a str with the unique UUID of the known scene;
        
    Returns:    
        Returns a string with the scene of place in language defined 
        by lang. This string can be sent back to user. 
        Currently only works with pt-br language. For the remaining 
        languages generates a string in English.
    """
    if scene==None:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'I do not known any scene here'
        return "Não conheco nenhuma cena aqui"
    try:
        sceneid=scene[1]
        scenename_rec = ac.remember(acid,['scene-name',sceneid])
        if scenename_rec==None:
            if lang.lower()!='pt' and lang.lower()!='pt-br':
                return 'Do not know the name of this scene'
            return "Não conheço o nome da cena aqui"       
        scenename = scenename_rec[2]
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Scene name is '+scenename
        return "O nome da cena aqui é "+scenename
    except:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'I do not known any scene here'
        return "Não conheco nenhuma cena aqui" 


def print_task_info(acid, lang, task):
    """ Print information about the a known task in the
        lang language.
        
    Args:
        acid: str with unique global identifier of actor
        lang: str with language identifier (currently accept pt-br)
        scene: known-task record with following structure:
                ['known-task', id]
            where:
                id is a str with the unique UUID of the known task;
        
    Returns:    
        Returns a string with information about task in language defined 
        by lang. This string can be sent back to user. 
        Currently only works with pt-br language. For the remaining 
        languages generates a string in English.
    """
    try:
        taskid=task[1]
        taskname_rec = ac.remember(acid,['task-name',taskid])
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'Yes I can do the '+taskname_rec[2]+' task'
        return "Sim posso fazer a tarefa de "+taskname_rec[2]
    except:
        if lang.lower()!='pt' and lang.lower()!='pt-br':
            return 'I do not known this task'
        return "Não conheco essa tarefa" 



#*******************************************
# NATURAL LANGUAGE FUNCTIONS
#*******************************************

SimilarityMetric = 'jaro-winkler'

def string_similarity(str1, str2):
    global SimilarityMetric
    if SimilarityMetric=='jaro-winkler':
        return jaro_winkler_similarity(str1,str2)
    if SimilarityMetric=='jaro':
        return jaro_similarity(str1,str2)
    return edit_distance(str1,str2)
        
def set_string_similarity_metric(metric):
    SimilarityMetric = metric
    

#*******************************************
# NATURAL LANGUAGE FUNCTIONS FOR
# PORTUGUESE LANGUAGE
#*******************************************

PtBrFemNames = []
PtBrMascNames = []

def possible_gender_of_name(lang, name):
    global PtBrFemNames, PtBrMascNames    
    if lang.lower()!='pt' and lang.lower()!='pt-br':
        return 'U'       
    if len(PtBrFemNames)==0:
        with open("nomes-femininos-brasil.txt", "r") as f:
            for line in f:
                PtBrFemNames.extend(line.strip())                    
    if len(PtBrMascNames)==0:
        with open("nomes-masculinos-brasil.txt", "r") as f:
            for line in f:
                PtBrMascNames.extend(line.strip()) 
    first_name_normal = unidecode.unidecode(name.lower().split()[0])       
    if first_name_normal in PtBrFemNames:
        if first_name_normal in PtBrMascNames:
            return 'B'
        return 'F'
    if first_name_normal in PtBrMascNames:
        return 'M'
    return 'U'

_ptBrTranslatePrimType = { 
    "box": "uma caixa",
    "cylinder": "um cilindro",
    "prism": "um prisma",
    "sphere": "uma esfera",
    "torus": "um torus",
    "tube": "um tubo",
    "ring": "um anel",
    "sculpt": "um objeto de tipo sculpt",
    "mesh": "um objeto de tipo malha",
    "unknown": "um objeto de tipo desconhecido"
}

_ptBrTranslateTreeType = {
    "pine1": "uma variedade de pinheiro",
    "oak": "um carvalho",
    "tropicalbush1": "uma variedade de arbusto tropical",
    "palm1": "um variedade de palmeira",
    "dogwood": "da variedade dogwood",
    "tropicalbush2": "outra variedade de arbusto tropical",
    "palm2": "outra variedade de palmeira",
    "cypress1": "uma variedade de cipreste",
    "cypress2": "outra variedade de cipreste",
    "pine2": "outra variedade de pinheiro",
    "plumeria": "uma plumeria",
    "winterpine1": "uma variedade de pinheiro de inverno",
    "winteraspen": "um álamo",
    "winterpine2": "outra variedade de pinheiro de inverno",
    "eucalyptus": "um eucalipto",
    "fern": "uma samambaia",
    "eelgrass": "um capim",
    "seasword": "outra variedade de alga",
    "kelp1": "um tipo de alga marinha",
    "beachgrass1": "um tipo de arbusto da praia",
    "kelp2": "outro tipo de alga marinha"
}


_ptBrTranslateGrassType = {
    "grass0": "básica",
    "grass1": "da variedade um",
    "grass2": "da variedade dois",
    "grass3": "da variedade três",
    "grass4": "da variedade quatro",
    "undergrowth1": "de baixo crescimento"
}


_ptBrTranslateOrdNumber = {
    "zer": "0",         "primeir": "1",     "segund": "2",      "terceir": "3",
    "quart": "4",       "quint": "5",       "sext": "6",        "sétim": "7",
    "setim": "7",       "oitav": "8",       "non": "9",         "décim": "10",
    "decim": "10",      "vigésim": "20",    "vigesim": "20",    "trigésim": "30",
    "trigesim": "30",   "quadrigésim":"40", "quadrigesim":"40", "quadragésim": "40",
    "quadragesim":"40", "quincagésim":"50", "quincagesim":"50", "sexagésim": "50",
    "sexagesim": "60",  "septagésim": "70", "septagesim": "70", "octagésim": "80",
    "octagesim": "80" , "nonagésim": "90",  "nonagesim": "90", "centésim": "100",
    "centésim": "100",  "milésim": "1000",  "milesim": "1000"
}

_ptBrNumbersDict = {
        'zero': 0,      'um': 1,        'dois': 2,      'três':3,'tres':3, 'quatro': 4,
        'cinco': 5,     'seis': 6,      'sete': 7,      'oito': 8,      'nove': 9,
        'dez': 10,      'onze': 11,     'doze': 12,     'treze': 13,    'catorze': 14,
        'quinze': 15,   'dezesseis':16, 'dezessete':17, 'dezoito': 18,  'dezenove': 19,
        'vinte': 20,    'trinta': 30,   'quarenta': 40, 'cinquenta': 50,'sessenta': 60,
        'setenta': 70,  'oitenta': 80,  'noventa': 90,  'cem': 100,     'cento': 100,
        'duzentos': 200,    'trezentos': 300,   'quatrocentos': 400,    'quinhentos': 500,
        'seiscentos': 600,  'setecentos': 700,  'oitocentos': 800,      'novecentos': 900,
        'mil': 1000,        'milhão': 1000000,  'milhao': 1000000,      'milhões': 1000000,
        'milhoes': 1000000, 'bilhão': 1000000000,'bilhao': 1000000000,  'bilhões': 1000000000, 
        'bilhoes': 1000000000
    }



# YE (not so) GOOD OLD CHAT-GPT CODE ;)
#    (with some Gluz corrections...)
# Two errors were corrected: 
# - the CHAT-GPT code does not consider the "e" conective used in 
#   numbers like: "cento e trinta e quatro", to correct this
#   I added the "elif word!='e'" clause 
# - the words scanning loop was initially testing "if value>100", but
#   this converted "mil quinhentos" to 500000 (that is "quinhentos mil"),
#   to correct this I changed the test to  "if value>1000".
# The CHAT-GPT code also only works with accentuated words for numbers, 
# like "três" or "milhão". For generality sake I added equivalent non 
# accentuated words like "tres", "milhao", ...
# (also change lower() to casefold())
# Besides these problems it is a good initial code example ...

def _translatePortugueseToNumber(phrase):
    # Define a dictionary with Portuguese words for numbers and their numerical values
    words = phrase.casefold().split()
    total = 0
    curr_number = 0
    for word in words:
        if word in _ptBrNumbersDict:
            value = _ptBrNumbersDict[word]
            if value >= 1000:
                if curr_number == 0:
                    curr_number = value
                else:
                    curr_number *= value
                    total += curr_number
                    curr_number = 0
            else:
                curr_number += value
        elif word!='e':
            return None
    return total + curr_number


def translate(lang, termtype, termval, deftrans=''):
    translation = deftrans
    if lang.lower()!='pt' and lang.lower()!='pt-br':
        if termtype=='natnumber':
            if termval.isnumeric():
                translation=termval
        return translation      
    if termtype=='primtype':
        translation = str(_ptBrTranslatePrimType.get(termval) or deftrans)
    elif termtype=='treetype':
        translation = str(_ptBrTranslateTreeType.get(termval) or deftrans)
    elif termtype=='grasstype':
        translation = str(_ptBrTranslateGrassType.get(termval) or deftrans)
    elif termtype=='natnumber':
        if termval.isnumeric():
            translation=termval
        else:
            translation = _ptBrTranslateOrdNumber.get(termval[:-1])
            if translation==None:
                #translation = str(PtBrTranslateCardNumber.get(termval) or deftrans)
                translation = str(_translatePortugueseToNumber(termval) or deftrans)
    return translation


_ptBrImportanceToValue = {
    "mais alta":5, "muito alta":5, "mais alto":5, "muito alto":5, "maior":5, "enorme":5,
    "alta":4, "alto":4, "grande":4,
    "medio":3, "médio":3, "média":3, "media":3, "razoável":3, "razoavel":3,
    "mediana":3, "mediano":3, "intermediária": 3, "intermediaria": 3, "intermediário": 3,
    "intermediario":3,
    "baixo":2, "baixa":2, "pouco":2, "pouca":2, "algum":2, "alguma":2,
    "muito baixa":1, "muito baixo":1, "muito pouco":1,  "muito pouca":1, "quase sem":1,
    "sem":0, "nenhum":0, "nenhuma":0, "não é":0, "nao é":0, "não e":0, "nao e":0,
    "não tem":0, "nao tem":0
}

_ptBrImportanceToText = {
    "mais alta": 5,     "muito alta": 5,    "maior": 5,     "enorme": 5,
    "alta": 4,          "grande": 4,    
    "média": 3,         "razoável": 3,      "mediana": 3,   "intermediária": 3,
    "baixa": 2,         "pouca": 2,         "alguma": 2,
    "muito baixa": 1,   "muito pouca": 1,   "quase sem": 1,
    "sem": 0,           "nenhuma": 0
}


def importance_to_value(lang, imptxt):
    if lang.lower()!='pt' and lang.lower()!='pt-br':
        return 0
    imp = " ".join(imptxt.casefold().split())
    maxsimil = 0.0
    maxsimil_val=3
    for imp,val in _ptBrImportanceToValue.items():
        simil = string_similarity(imp,imp)
        if simil>maxsimil:
            maxsimil = simil
            maxsimil_val = val
    if maxsimil<0.7:
        return None
    return str(maxsimil_val)

    
def importance_to_text(lang, impval):
    if lang.lower()!='pt' and lang.lower()!='pt-br':
        return 'unknown'
    imptxts=[]
    for imp,val in _ptBrImportanceToText.items():
        if impval==val:
            imptxts.append(imp)
    if len(imptxts)==0:
        return 'desconhecida'
    return random.choice(imptxts)

#*******************************************
# 3D AND 2D GRAPHICAL FUNCTIONS
#*******************************************

def _bearingAngle(x0,y0,x1,y1):
    dx = x1-x0
    dy = y1-y0
    d = math.sqrt(dx**2 + dy**2)
    t = math.acos(dx/d)*(180/math.pi)
    if d!=0.0:
        if dy>=0:
            return t
        return 360 - t
    return 0.0
        
def _bearing(x0,y0,x1,y1):
    dx = x1-x0
    dy = y1-y0
    d = math.sqrt(dx**2 + dy**2)
    if d!=0.0:
        b = math.acos(dx/d)
        return b
#        if dy>=0:
#            return b
#        else:
#            return 2*math.pi - b
    return 0.0

def _relAngle(yaw, x0, y0, x1, y1):
    b = _bearingAngle(x0,y0,x1,y1)
    print("bearingangle=",b)
    t = yaw-b
    if t>=0: 
        return t
    return 360+t
 
def _relAngleToAvatar(acid,avid):
    myrot = ac.look_my_rotation(acid)
    myyaw = float(myrot[4])*(180/math.pi)
    if myyaw<0.0:
        myyaw = myyaw+360
    mypos = ac.look_my_position(acid)
    myx = float(mypos[2])
    myy = float(mypos[3])   
    avinf = ac.look_avatar(acid,avid)
    if avinf==None:
        return 0.0
    avx = float(avinf[4])
    avy = float(avinf[5])
    r = _relAngle(myyaw,myx,myy,avx,avy)
    print("my yaw=",myyaw," x=",myx," y=",myy)
    print("av x=",avx," y=",avy)
    print("relangle=",r)
    return r
 
def relangle_to_avatar(acid,avid):
    """ Discover the relative angle (the bearing) from the avatar 
        controlled by the actor to other avatar with avid unique id.
        
    Args:
        acid:   str with unique global identifier of actor.
        avid:   str with unique global identifier of other avatar.
        
    Returns:    
        On fail, returns None.       
        On success, returns a float with the relative angle (in degrees) 
        from  actor's avatar to other avatar identified by avid.     
    """
    myrot = ac.look_my_rotation(acid)
    myyaw = float(myrot[4])*(180/math.pi)
    if myyaw<0.0:
        myyaw = myyaw+360
    mypos = ac.look_my_position(acid)
    myx = float(mypos[2])
    myy = float(mypos[3])   
    avinf = ac.look_avatar(acid,avid)
    if avinf==None:
        return 0.0
    avx = float(avinf[4])
    avy = float(avinf[5])
    r = _relAngle(myyaw,myx,myy,avx,avy)
    print("my yaw=",myyaw," x=",myx," y=",myy)
    print("av x=",avx," y=",avy)
    print("relangle=",r)
    return r
    
def relangle_to_avatar_with_name(acid,avname):
    """ Discover the relative angle (the bearing) from the avatar 
        controlled by the actor to other avatar with avname name.
        
    Args:
        acid:   str with unique global identifier of actor.
        avname: str with name of other avatar.
        
    Returns:    
        On fail, returns None.        
        On success, returns a float with the relative angle (in degrees) 
        from actor's avatar to other avatar identified by avid. 
    """
    avinf = ac.look_avatar_with_name(acid,avname)
    if avinf==None:
        return 0.0
    return relangle_to_avatar(acid,avinf[1])

def reldir_to_avatar(acid,avid):
    """ Discover the relative direction from the avatar controlled
        by the actor to other avatar with avid unique id.
        
    Args:
        acid:   str with unique global identifier of actor.
        avid:   str with unique global identifier of other avatar.

    Returns:     
        On fail, returns None.       
        On success, returns the relative direction from  actor's avatar 
        to the other avatar identified by avid. Relative directions can
        be: 'straight-behind', 'straight-ahead', 'straight-at-left', 
        'straight-at-right', 'ahead-at-right', 'behind-at-right', 
        'behind-at-left' or 'ahead-at-left'.                 
        The following diagram show directions relative from avatar's 
        position:
                            straight
                            ahead  
                                |
                ahead           |       ahead 
                at left         |       at right
                                |
        straight  --------------+-------------- straight
        at left                 |               at right
                                |
                behind          |       behind 
                at left         |       at right
                            straight
                            behind
    """
    r = relangle_to_avatar(acid,avid)
    if 165.0 <= r <= 195.0:
        reldir = 'straight-behind'
    elif r<=15.0 or r>=345.0:
        reldir = 'straight-ahead'
    elif 255.0 <= r <= 285.0:
        reldir = 'straight-at-left'  
    elif 75.0 <= r <= 105.0:
        reldir = 'straight-at-right'
    elif 15.0 < r < 75.0:
        return 'ahead-at-right'  
    elif 105.0 < r < 165.0:
        reldir = 'behind-at-right'  
    elif 195.0 < r < 255.0:
        reldir = 'behind-at-left'  
    else:
        reldir = 'ahead-at-left'
    return reldir
    
def reldir_to_avatar_with_name(acid,avname):
    """ Discover the relative direction from the avatar controlled
        by the actor to other avatar with avname name. See the 
        help of reldir_to_avatar() for more details on relative
        directions.

    Args:
        acid:   str with unique global identifier of actor.
        avname: str with name of other avatar.

    Returns:
     
        On fail, returns None.        
        On success, returns the relative direction from  actor's avatar to 
        the other avatar with name avname. Relative directions can
        be: 'straight-behind', 'straight-ahead', 'straight-at-left', 
        'straight-at-right', 'ahead-at-right', 'behind-at-right', 
        'behind-at-left' or 'ahead-at-left'. 
    """
    avinf = ac.look_avatar_with_name(acid,avname)
    if avinf==None:
        return None
    return reldir_to_avatar(acid,avinf[1])
    
def vertpos_to_avatar(acid,avid):
    """ Discover the vertical position from the avatar controlled
        by the actor to other avatar with avid unique id.

    Args:
        acid:   str with unique global identifier of actor.
        avid:   str with unique global identifier of other avatar.

    Returns:    
        On fail, returns None.        
        On success, returns the vertical position from  actor's avatar 
        to the other avatar identified by avid. Vertical positions can 
        be: 'above', 'below', 'same-level', or 'unknown' if the other
        avatar is not found.
    """
    mypos = ac.look_my_position(acid)
    myz = float(mypos[4])
    avinf = ac.look_avatar(acid,avid)
    if avinf==None:
        return 'unknown'
    avz = float(avinf[6])
    print("my z=",myz)
    print("av z=",avz)
    if myz>(avz+0.5):
        vpos='above'
    elif myz<(avz-0.5):
        vpos='below'
    else:
        vpos='same-level'
    return vpos

def vertpos_to_avatar_with_name(acid,avname):
    """ Discover the vertical position from the avatar controlled
        by the actor to other avatar with name avname.

    Args:
        acid:   str with unique global identifier of actor.
        avname: str with name of other avatar.

    Returns:     
        On fail, returns None.
        On success, returns the vertical position from  actor's avatar 
        to the other avatar with name avname. Vertical positions can 
        be: 'above', 'below', 'same-level', or 'unknown' if the other
        avatar is not found.
    """ 
    avinf = ac.look_avatar_with_name(acid,avname)
    if avinf==None:
        return None
    return vertpos_to_avatar(acid,avinf[1])
     
def relangle_to_obj(acid,objid):
    """ Discover the relative angle (the bearing) from the avatar 
        controlled by the actor to object with objid unique id.

    Args:
        acid:   str with unique global identifier of actor.
        avid:   str with unique global identifier of object.

    Returns:     
        On fail, returns None.        
        On success, returns a float number with the relative angle (in 
        degrees) from actor's avatar to the object identified by objid.
    """
    myrot = ac.look_my_rotation(acid)
    myyaw = float(myrot[4])*(180/math.pi)
    if myyaw<0.0:
        myyaw = myyaw+360
    mypos = ac.look_my_position(acid)
    myx = float(mypos[2])
    myy = float(mypos[3])   
    objinf = ac.look_obj(acid,objid)
    if objinf==None:
        return 0.0
    objx = float(objinf[6])
    objy = float(objinf[7])
    r = _relAngle(myyaw,myx,myy,objx,objy)
    print("my yaw=",myyaw," x=",myx," y=",myy)
    print("obj x=",objx," y=",objy)
    print("relangle=",r)
    return r
    
def reldir_to_obj(acid,objid):
    """ Discover the relative direction from the avatar controlled
        by the actor to object with objid unique id.

    Args:
        acid:   str with unique global identifier of actor.
        objid:  str with unique global identifier of object.

    Returns:     
        On fail, returns None.        
        On success, returns the relative direction from  actor's avatar 
        to the object identified by objid. Relative directions can be: 
        'straight-behind', 'straight-ahead', 'straight-at-left', 
        'straight-at-right', 'ahead-at-right', 'behind-at-right', 
        'behind-at-left' or 'ahead-at-left'. The following diagram 
        show directions relative from avatar's position:
                            straight
                            ahead  
                                |
                ahead           |       ahead 
                at left         |       at right
                                |
        straight  --------------+-------------- straight
        at left                 |               at right
                                |
                behind          |       behind 
                at left         |       at right
                            straight
                            behind
    """
    r = relangle_to_obj(acid,objid)
    if 165.0 <= r <= 195.0:
        reldir = 'straight-behind'
    elif r<=15.0 or r>=345.0:
        reldir = 'straight-ahead'
    elif 255.0 <= r <= 285.0:
        reldir = 'straight-at-left'  
    elif 75.0 <= r <= 105.0:
        reldir = 'straight-at-right'
    elif 15.0 < r < 75.0:
        reldir = 'ahead-at-right'  
    elif 105.0 < r < 165.0:
        reldir = 'behind-at-right'  
    elif 195.0 < r < 255.0:
        reldir = 'behind-at-left'  
    else:
        reldir = 'ahead-at-left'
    return reldir

def vertpos_to_obj(acid,objid):
    """ Discover the vertical position from the avatar controlled
        by the actor to other object with pbjid unique id.

    Args:
        acid:   str with unique global identifier of actor.
        objid:  str with unique global identifier of object.

    Returns:     
        On fail, returns None.        
        On success, returns the vertical position from  actor's avatar to 
        the object identified by objid. Vertical positions can be: 'above', 
        'below' or 'same-level'.         
    """
    mypos = ac.look_my_position(acid)
    myz = float(mypos[4])
    objinf = ac.look_obj(acid,objid)
    if objinf==None:
        return None
    objz = float(objinf[8])
    print("my z=",myz)
    print("obj z=",objz)
    if myz>(objz+0.5):
        vpos='above'
    elif myz<(objz-0.5):
        vpos='below'
    else:
        vpos='same-level'
    return vpos

def _isOnLine(l, p):
    x,y = p
    p1,p2 = l
    x1,y1=p1
    x2,y2=p2
    # Check whether p is on the line or not
    if (x <= max(x1, x2) and x <= min(x1, x2)
        and (y <= max(y1, y2) and y <= min(y1, y2))):
        return True
    return False

# Get direction of three ordered points p1,p2,p3, returns:
#   0 : Collinear direction
#   1 : Clockwise direction
#   2 : Counterclockwise or anti-clockwise direction
# def _direction(a, b, c):
def _direction(p1, p2, p3):
    val =  (p2[1]-p1[1]) * (p3[0]-p2[0]) - (p2[0]-p1[0]) * (p3[1]-p2[1])
    return 0 if val==0 else (2 if val<0 else 1)

# Get orientation of three ordered points p1,p2,p3, returns:
#   0  : Collinear points
#   >0 : Clockwise points
#   <0 : Counterclockwise points
def _orientation(p1, p2, p3):   
    return (p2[1]-p1[1]) * (p3[0]-p2[0]) - (p2[0]-p1[0]) * (p3[1]-p2[1])


def _isIntersect(l1, l2):
    l1p1,l1p2 = l1
    l2p1,l2p2 = l2
    # Four direction for two lines and points of other line
    dir1 = _direction(l1p1, l1p2, l2p1)
    dir2 = _direction(l1p1, l1p2, l2p2)
    dir3 = _direction(l2p1, l2p2, l1p1)
    dir4 = _direction(l2p1, l2p2, l1p2)
    if dir1 != dir2 and dir3 != dir4:
        return True # When intersecting
    if dir1 == 0 and _isOnLine(l1, l2p1):
        return True # When p2 of line2 are on the line1
    if dir2 == 0 and _isOnLine(l1, l2p2):
        return True # When p1 of line2 are on the line1
    if dir3 == 0 and _isOnLine(l2, l1p1):
        return True # When p2 of line1 are on the line2
    if dir4 == 0 and _isOnLine(l2, l1p2):
        return True # When p1 of line1 are on the line2
    return False

def _leftMost(points):
    mini = 0
    for i in range(1,len(points)):
        if points[i][0] < points[mini][0]:
            mini = i
        elif points[i][0] == points[mini][0]:
            if points[i][1] > points[mini][1]:
                mini = i
    return mini

def check_inside_poly(p, poly):
    """ Check if 2D point p is inside of polygon poly.
        Points at the boundary line of the polygon are
        not considered inside.

    Args:
        p: tuple (x,y) with X,Y coordinates of point p.
        poly:  list of 2D points that define the polygon, each point is
            a tuple (x,y) with X,Y coordinates of the point.

    Returns:     
        Returns True, if p is inside polygon poly.        
        Returns False, otherwise.         
    """
    n = len(poly)
    # When polygon has less than 3 edge, it is not polygon
    if n < 3:
        return False
    x,y = p
    # Create a point at infinity, y is same as point p
    exline = (p, (99999, y))
    count = 0
    i = 0
    while True:
        # Forming a line from two consecutive points of poly
        side = (poly[i], poly[(i + 1) % n])
        sidep1,sidep2 = side
        if _isIntersect(side, exline):
            # If side is intersects ex
            if (_direction(sidep1, p, sidep2) == 0):
                return False
            count += 1      
        i = (i + 1) % n;
        if i == 0:
            break
    # When count is odd
    return bool(count & 1)
    
def compute_poly_centroid(vertices):
    """ Compute the centroid (or geometric center) of the convex hull defined 
        by vertices list of 2D points. This functions only works if vertices
        is a polygon with a convex hull,i.e. is a convex polygon.

    Args:
        vertices:  list of 2D points that define the convex hull, each point 
            is a tuple (x,y) with X,Y coordinates of the point.

    Returns:     
        On fail, returns None.        
        On success, returns a tuple (x,y) with X,Y coordinates of the centroid.               
    """
    x, y = 0, 0
    n = len(vertices)
    signed_area = 0
    for i in range(len(vertices)):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i + 1) % n]
        # shoelace formula
        area = (x0 * y1) - (x1 * y0)
        signed_area += area
        x += (x0 + x1) * area
        y += (y0 + y1) * area
    signed_area *= 0.5
    x /= 6 * signed_area
    y /= 6 * signed_area
    return x, y

def compute_convex_poly(points):
    """ Computes the convex polygon (a convex hull) for the finite set of 
        2D planar points defined by points argument.

    Args:
        points: the convex hull (or polygon) will be calculated over this set 
            of 2D points, each  point is a tuple (x,y) with X,Y coordinates of 
            the point.

    Returns:     
        Returns a list of 2D points that define the convex polygon, each point 
            is a tuple (x,y) with X,Y coordinates of the point.               
    """
    # get leftmost point
    start = points[0]
    min_x = start[0]
    for p in points[1:]:
        if p[0] < min_x:
            min_x = p[0]
            start = p
    point = start
    hull_points = [start]
    far_point = None
    while far_point is not start:
        # get the first point (initial max) to use to compare with others
        p1 = points[1] if point is points[0] else points[0]
        far_point = p1
        for p2 in points:
            # ensure we aren't comparing to self or pivot point
            if p2 is point or p2 is p1:
                continue
            direction = _orientation(point, far_point, p2)
            if direction > 0:
                far_point = p2
        hull_points.append(far_point)
        point = far_point
    return hull_points

