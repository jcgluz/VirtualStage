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
#   Module:     PerguntasAprendiz 
#   Purpose:    Exemplo de modulo que implementa as intencoes das perguntas
#               tratadas nas conversas do ator aprendiz (apprentice actor)
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

""" Modulo IntencoesAprendiz - Exemplo de modulo que implementa as intencoes por
        trás de perguntas direcionadas ao ator aprendiz (trainee actor) """

import random
import clr
import time
import re
import uuid
import math
import ActorController as ac
import DialogController as dc
import AtorAprendiz
import AuxiliaryFunctions as af

###################################
# Intentions functions to answer
# questions about OBJECTS
###################################

def respostaSim_listing_objects(acid,username,userinput,matches):
    ac.print_dbg('intencoes',"listing-objects")
    objlist = dc.get_topic_content(acid)
    ac.print_dbg('intencoes',"objlist=",objlist)
    objetos=dc.gen_speak(acid,'sinonObjetos')
    if objlist:
        resp=dc.gen_speak(acid,'segueListagem(ITEMS)',[objetos],"Segue mais")+":\n"
        resp+=printingObjects(acid,objlist)
        ac.print_dbg('intencoes',"printingObjects= ",resp)
    else:
        resp=dc.gen_speak(acid,'fimListagem(ITEMS)',[objetos],"Sem mais")+":\n"
    return resp
    

def respostaNao_listing_objects(acid,username,userinput,matches):
    return dc.gen_speak(acid,'pareiListagem')+'. '+dc.gen_speak(acid,'sePrecisarAjuda')


def printingObjects(acid,objnamelist):
    resp = ""
    while objnamelist:
        resp += objnamelist.pop(0)+"\n"
        if objnamelist==[]:
            resp+=dc.gen_speak(acid,'fimListagem(ITEMS)',["objetos"],"Acabou")            
        elif len(resp)>500:
            resp+=dc.gen_speak(acid,'querVerMaisObjetos')
            dc.set_next_topic(acid,'listing-objects',objnamelist.copy())
            objnamelist=[]
    return resp
    

def perguntaObjetosConhecidos(acid,username,userinput,matches):
    kobjs = ac.remember_all(acid,['known-obj'])
    if kobjs==None or len(kobjs)==0:
        return dc.gen_speak(acid,'naoConhecoObjetosAqui')
    resp = dc.gen_speak(acid,'conhecoObjetosAqui')+":\n"
    objnamelist=[]
    for kobj in kobjs:
        kobjname = ac.remember(acid,['obj-name',kobj[1]])
        if kobjname!=None:
            objnamelist.append(kobjname[2])
        else:
            vrobj = ac.look_obj(acid,kobj[1])
            if vrobj!=None:
             objnamelist.append(vrobj[2])               
    resp += printingObjects(acid,objnamelist)
    return resp

        
def perguntaInformacaoObjeto(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    selobjid = dc.get_topic_content(acid)
    if topic=='obj-selected' and selobjid!=None:
        vrobjinfo = ac.look_obj(acid,selobjid)
        dc.keep_topic(acid)
    else:
        vrobjinfo = af.find_nearest_obj(acid)
        if  vrobjinfo!=None:
            dc.set_next_topic(acid,'obj-selected',vrobjinfo[1])
    ac.print_dbg('intents','vrobjinfo=',vrobjinfo)
    return af.print_obj_info(acid, 'pt-br', vrobjinfo)

        
def perguntaNomeObjeto(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    selobjid = dc.get_topic_content(acid)
    if topic=='obj-selected':
        obj = ac.look_obj(acid,selobjid)
        if  obj!=None:
            dc.keep_topic(acid)
    else:
        obj = af.find_nearest_obj(acid)
        if  obj!=None:
            dc.set_next_topic(acid,'obj-selected',obj[1])
    return af.print_obj_name(acid,'pt-br',obj)

        
def perguntaDescricaoObjeto(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    selobjid = dc.get_topic_content(acid)
    if topic=='obj-selected' and selobjid!=None:
        obj = ac.look_obj(acid,selobjid)
        if  obj!=None:
            dc.keep_topic(acid)
    else:
        obj = af.find_nearest_obj(acid)
        if  obj!=None:
            dc.set_next_topic(acid,'obj-selected',obj[1])
    return af.print_obj_descr(acid,'pt-br',obj)

        
def perguntaUsoObjeto(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    selobjid = dc.get_topic_content(acid)
    if topic=='obj-selected' and selobjid!=None:
        obj = ac.look_obj(acid,selobjid)
        if  obj!=None:
            dc.keep_topic(acid)
    else:
        obj = af.find_nearest_obj(acid)
        if  obj!=None:
            dc.set_next_topic(acid,'obj-selected',obj[1])
    return af.print_obj_use(acid,'pt-br',obj)


def perguntaImportanciaObjeto(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    selobjid = dc.get_topic_content(acid)
    if topic=='obj-selected' and selobjid!=None:
        obj = ac.look_obj(acid,selobjid)
        if  obj!=None:
            dc.keep_topic(acid)
    else:
        obj = af.find_nearest_obj(acid)
        if  obj!=None:
            dc.set_next_topic(acid,'obj-selected',obj[1])
    imprec = ac.remember(acid,['obj-importance'])
    a_importancia = random.choice(['o grau de importância','o grau de relevância']) 
    desse_obj=random.choice(["desse objeto", "dessa coisa", "disso"])
    if imprec==None:
        return dc.gen_speak(acid,'naoReconheco(PROP;COISA)',[a_importancia,desse_obj])
    impval = af.importance_to_text('pt-br',imprec[2])
    return dc.gen_speak(acid,'conheco(PROP;COISA;VAL)',[a_importancia,desse_obj,impval])

def perguntaAtributoObjeto(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    selobjid = dc.get_topic_content(acid)
    if topic=='obj-selected' and selobjid!=None:
        obj = ac.look_obj(acid,selobjid)
        if  obj!=None:
            dc.keep_topic(acid)
    else:
        obj = af.find_nearest_obj(acid)
        if  obj!=None:
            dc.set_next_topic(acid,'obj-selected',obj[1])
    return af.print_obj_attr(acid,'pt-br',matches[0],obj)

        
def perguntaQueObjetosConheceAqui(acid,username,userinput,matches):
    radius_mem = ac.remember(acid,['default-place-radius'])
    if radius_mem==None:
        # Default radius of some place, from its central position is 5 meters
        default_r = 5.0
        ac.record(acid,['default-place-radius','5.0'])
    else:
        default_r = float(radius_mem[1])
    nearobjs = ac.seek_objs_by_radius(acid,default_r)
    if nearobjs==None or len(nearobjs)==0:
        resp = dc.gen_speak(acid,'naoVejoObjeto')
    else:
        knownobjs = []
        unknownobjs = []
        for obj in nearobjs:
            objname = ac.remember(acid,['obj-name',obj[1]])
            if objname!=None:
                knownobjs.append(objname[2])
            else:
                nametxt = ''
                if len(obj[2])>2:
                    nametxt = obj[2]+", "
                objtype = obj[3]
                objsubtype = obj[4]
                if objtype=='prim':
                    nametxt += af.translate('pt-br','primtype',objsubtype.casefold(),'objeto desconhecido')+". "
                elif objtype=='tree':
                    nametxt += af.translate('pt-br','treetype', objsubtype.casefold(), 'planta desconhecida')+". "
                else:
                    nametxt += 'uma grama '+af.translate('pt-br','primtype',objsubtype.casefold(),'grama desconhecida')+". "               
                unknownobjs.append(nametxt)
        resp = dc.gen_speak(acid,'conhecoObjetosAqui')+":\n"
        for name in knownobjs:
            resp+=name+"\n"
        resp += dc.gen_speak(acid,'viOutrosObjetosAquia')+":\n"
        for name in unknownobjs:
            resp+=name+"\n"
    return resp       
 

###################################
# Intentions functions to answer
# questions about PLACES
###################################

def respostaSim_listing_places(acid,username,userinput,matches):
    ac.print_dbg('intencoes',"listing-places")
    placelist = dc.get_topic_content(acid)
    ac.print_dbg('intencoes',"placelist=",placelist)
    lugares=dc.gen_speak(acid,'sinonLugares')
    if placelist:
        resp=dc.gen_speak(acid,'segueListagem(ITEMS)',[lugares],"Segue mais")+":\n"
        resp+=printingPlaces(acid,placelist)
        ac.print_dbg('intencoes',"printingPlaces= ",resp)
    else:
        resp=dc.gen_speak(acid,'fimListagem(ITEMS)',[lugares],"Sem mais")+":\n"
    return resp
 
 
def respostaNao_listing_places(acid,username,userinput,matches):
    return dc.gen_speak(acid,'pareiListagem')+'. '+dc.gen_speak(acid,'sePrecisarAjuda')


def printingPlaces(acid,placenamelist):
    resp = ""
    while placenamelist:
        resp += placenamelist.pop(0)+"\n"
        if placenamelist==[]:
            resp+=dc.gen_speak(acid,'fimListagem(ITEMS)',["lugares"],"Acabou")            
        elif len(resp)>500:
            resp+=dc.gen_speak(acid,'querVerMaisLugares')
            dc.set_next_topic(acid,'listing-places',placenamelist.copy())
            placenamelist=[]
    return resp
    

def perguntaLugaresConhecidos(acid,username,userinput,matches):
    kplaces = ac.remember_all(acid,['known-place'])
    if kplaces==None or len(kplaces)==0:
        return dc.gen_speak(acid,'naoConhecoLugaresAqui')
    resp = dc.gen_speak(acid,'conhecoLugaresAqui')+":\n"
    placenamelist=[]
    for place in kplaces:
        placename = ac.remember(acid,['place-name',place[1]])
        if placename!=None:
            placenamelist.append(placename[2])
    resp+=printingPlaces(acid,placenamelist)
    return resp

        
def perguntaInformacaoLugar(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    place = dc.get_topic_content(acid)
    if topic=='place-selected' and place!=None:
        dc.keep_topic(acid)
    else:
        userinfo=ac.look_avatar_with_name(acid,username)
        if userinfo==None:
            return dc.gen_speak(acid,'naoSeiOndeVoceEsta')
        dist = float(userinfo[3])
        if dist>20.0:
            return dc.gen_speak(acid,'voceEstaDistante')+".\n"+dc.gen_speak(acid,'naoVejoLugar')
        place = af.find_place(acid,userinfo[4],userinfo[5])
        if  place!=None:
            dc.set_next_topic(acid,'place-selected',place)
    return af.print_place_info(acid,'pt-br',place)

def perguntaNomeLugar(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    place = dc.get_topic_content(acid)
    if topic=='place-selected' and place!=None:
        ac.print_dbg('intencoes','perguntaNomeLugar ','place=',place)
        dc.keep_topic(acid)
    else:
        userinfo=ac.look_avatar_with_name(acid,username)
        if userinfo==None:
            return dc.gen_speak(acid,'naoSeiOndeVoceEsta')
        dist = float(userinfo[3])
        if dist>20.0:
            return dc.gen_speak(acid,'voceEstaDistante')+".\n"+dc.gen_speak(acid,'naoVejoLugar')
        place = af.find_place(acid,userinfo[4],userinfo[5])
        if  place!=None:
            dc.set_next_topic(acid,'place-selected',place)
    return af.print_place_name(acid,'pt-br',place)

def perguntaDescricaoLugar(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    place = dc.get_topic_content(acid)
    if topic=='place-selected' and place!=None:
        dc.keep_topic(acid)
    else:
        userinfo=ac.look_avatar_with_name(acid,username)
        if userinfo==None:
            return dc.gen_speak(acid,'naoSeiOndeVoceEsta')
        dist = float(userinfo[3])
        if dist>20.0:
            return dc.gen_speak(acid,'voceEstaDistante')+".\n"+dc.gen_speak(acid,'naoVejoLugar')
        place = af.find_place(acid,userinfo[4],userinfo[5])
        if  place!=None:
            dc.set_next_topic(acid,'place-selected',place)
    return af.print_place_descr(acid,'pt-br',place)

def perguntaEventoLugar(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    place = dc.get_topic_content(acid)
    if topic=='place-selected' and place!=None:
        dc.keep_topic(acid)
    else:
        userinfo=ac.look_avatar_with_name(acid,username)
        if userinfo==None:
            return dc.gen_speak(acid,'naoSeiOndeVoceEsta')
        dist = float(userinfo[3])
        if dist>20.0:
            return dc.gen_speak(acid,'voceEstaDistante')+".\n"+dc.gen_speak(acid,'naoVejoLugar')
        place = af.find_place(acid,userinfo[4],userinfo[5])
        if  place!=None:
            dc.set_next_topic(acid,'place-selected',place)
    return af.print_place_event(acid,'pt-br',place)


def perguntaImportanciaLugar(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    place = dc.get_topic_content(acid)
    if topic=='place-selected' and place!=None:
        dc.keep_topic(acid)
    else:
        userinfo=ac.look_avatar_with_name(acid,username)
        if userinfo==None:
            return dc.gen_speak(acid,'naoSeiOndeVoceEsta')
        dist = float(userinfo[3])
        if dist>20.0:
            return dc.gen_speak(acid,'voceEstaDistante')+".\n"+dc.gen_speak(acid,'naoVejoLugar')
        place = af.find_place(acid,userinfo[4],userinfo[5])
        if  place!=None:
            dc.set_next_topic(acid,'place-selected',place)
    imprec = ac.remember(acid,['place-importance'])
    a_importancia = random.choice(['o grau de importância','o grau de relevância']) 
    desse_lugar=random.choice(["desse lugar", "desse local", "daqui"])
    if imprec==None:
        return dc.gen_speak(acid,'naoReconheco(PROP;COISA)',[a_importancia,desse_lugar])
    impval = af.importance_to_text('pt-br',imprec[2])
    return dc.gen_speak(acid,'conheco(PROP;COISA;VAL)',[a_importancia,desse_lugar,impval])


def perguntaAtributoLugar(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    place = dc.get_topic_content(acid)
    if topic=='place-selected' and place!=None:
        dc.keep_topic(acid)
    else:
        userinfo=ac.look_avatar_with_name(acid,username)
        if userinfo==None:
            return dc.gen_speak(acid,'naoSeiOndeVoceEsta')
        dist = float(userinfo[3])
        if dist>20.0:
            return dc.gen_speak(acid,'voceEstaDistante')+".\n"+dc.gen_speak(acid,'naoVejoLugar')
        place = af.find_place(acid,userinfo[4],userinfo[5])
        if  place!=None:
            dc.set_next_topic(acid,'place-selected',place)
    return af.print_place_attr(acid,'pt-br',matches[0],place)

        

###################################
# Intentions functions to answer
# questions about NAMES of places
# or objects
###################################

def perguntaInformacaoSobreNome(acid,username,userinput,matches):
    objnames = ac.remember_all(acid,['obj-name'])
    if objnames!=None and len(objnames)>0:
        maxsimil = 0.0
        maxsimil_obj=None
        for obj in objnames:
            simil = af.string_similarity(matches[0],obj[2])
            if simil>maxsimil:
                maxsimil = simil
                maxsimil_obj=obj
        if  maxsimil>=0.9:
            obj = ac.look_obj(acid,maxsimil_obj[1])
            ac.print_dbg('perguntas aprendiz','vr obj=',obj)
            return af.print_obj_descr(acid,'pt-br',obj)
            
    placenames = ac.remember_all(acid,['place-name'])
    if placenames==None or len(placenames)==0:
        return dc.gen_speak(acid,'naoConhecoComEsseNome')
        
    maxsimil = 0.0
    maxsimil_place=None
    for place in placenames:
        simil = af.string_similarity(matches[0],place[2])
        if simil>maxsimil:
            maxsimil = simil
            maxsimil_place=place
    if  maxsimil<0.9:
        return dc.gen_speak(acid,'naoConhecoComEsseNome')
    place = ac.remember(acid,['known-place'])
    if  place==None:
        return dc.gen_speak(acid,'naoConhecoComEsseNome')
    return af.print_place_descr(acid,'pt-br',place)

 
###################################
# Intentions functions to answer
# questions about avatar's CHARACTER
###################################

def perguntaMeuNome(acid,username,userinput,matches):
    myname_mem = ac.remember(acid,['character-name'])
    if myname_mem!=None:
        myname=myname_mem[1]
    else:
        myname = ac.get_actor_name(acid)
    if myname==None:
        return dc.gen_speak(acid,'naoLembroMeuNome')
    uname_mem = ac.remember(acid,['user-name'])
    if uname_mem!=None:
        uname = uname_mem[1]
    else:
        uname = username
    resp = dc.gen_speak(acid,'saudacoesIniciais')+af.optional(0.5," "+uname)+".\n" + \
            dc.gen_speak(acid,'meuNomeEh(NOME)',[myname])
    return resp

def perguntaConfirmaMeuNome(acid,username,userinput,matches):
    myname_mem = ac.remember(acid,['character-name'])
    if myname_mem!=None:
        myname=myname_mem[1]
    else:
        myname = ac.get_actor_name(acid)
    if myname!=None and myname==matches[0]:
        resp= dc.gen_speak(acid,'confirmaNome')
    else: 
        resp= dc.gen_speak(acid,'desconfirmaNome')
    return resp


def perguntaMeuSexoIdade(acid,username,userinput,matches):
    sex_mem = ac.remember(acid,['character-sex'])
    age_mem = ac.remember(acid,['character-age'])
    if sex_mem!=None and age_mem!=None:
        resp= dc.gen_speak(acid,'euSouUmTenhoAnos(DESCR;IDADE)',[sex_mem[1],age_mem[1]],"Sou VR Bot" )
    elif age_mem!=None:
        resp= dc.gen_speak(acid,'euTenhoAnos(IDADE)',[age_mem[1]],"Sem idade" )
    elif sex_mem!=None:
        resp= dc.gen_speak(acid,'euSouUm(DESCR)',[sex_mem[1]],"Sou VR Bot" )
    else:
        resp= dc.gen_speak(acid,'naoSei')
    return resp

def perguntaMinhasInformacoes(acid,username,userinput,matches):
    estagiario = random.choice(["estágiário","estágiario aprendiz",
            "estágiário ainda aprendendo","estágiário novato"])
    resp = dc.gen_speak(acid,'euSouUm',[estagiario],"Sou estágiario" )+".\n"
    resp += dc.gen_speak(acid,'perfilEstagiario')
    return resp

###################################
# Intentions functions to answer
# questions about SCENES
###################################

def respostaSim_listing_scenes(acid,username,userinput,matches):
    ac.print_dbg('intencoes',"listing-places")
    scenelist = dc.get_topic_content(acid)
    ac.print_dbg('intencoes',"scenelist=",scenelist)
    cenas=dc.gen_speak(acid,'sinonCenas')
    if scenelist:
        resp=dc.gen_speak(acid,'segueListagem(ITEMS)',[cenas])+":\n"
        resp+=printingScenes(acid,scenelist)
        ac.print_dbg('intencoes',"printingScenes= ",resp)
    else:
        resp=dc.gen_speak(acid,'fimListagem(ITEMS)',[cenas])+":\n"
    return resp
 
 
def respostaNao_listing_scenes(acid,username,userinput,matches):
    return dc.gen_speak(acid,'pareiListagem')+'. '+dc.gen_speak(acid,'sePrecisarAjuda')


def printingScenes(acid,scenenamelist):
    resp = ""
    while scenenamelist:
        resp += scenenamelist.pop(0)+"\n"
        if scenenamelist==[]:
            resp+=dc.gen_speak(acid,'fimListagem(ITEMS)',["cenas"])            
        elif len(resp)>500:
            resp+=dc.gen_speak(acid,'querVerMaisCenas')
            dc.set_next_topic(acid,'listing-scenes',scenenamelist.copy())
            scenenamelist=[]
    return resp
    

def perguntaCenasConhecidas(acid,username,userinput,matches):
    kscenes = ac.remember_all(acid,['known-scene'])
    if kscenes==None or len(kscenes)==0:
        return dc.gen_speak(acid,'naoConhecoCenas')
    resp = dc.gen_speak(acid,'conhecoCenas')+":\n"
    scenenamelist=[]
    for scene in kscenes:
        scenename = ac.remember(acid,['scene-name',scene[1]])
        if scenename!=None:
            scenenamelist.append(scenename[2])
    resp+=printingScenes(acid,scenenamelist)
    return resp

        
def perguntaInformacaoCena(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    scene = dc.get_topic_content(acid)
    if topic=='scene-selected' and scene!=None:
        dc.keep_topic(acid)
    else:
        userinfo=ac.look_avatar_with_name(acid,username)
        if userinfo==None:
            return dc.gen_speak(acid,'naoSeiOndeVoceEsta')
        dist = float(userinfo[3])
        if dist>20.0:
            return dc.gen_speak(acid,'voceEstaDistante')+".\n"+dc.gen_speak(acid,'naoVejoLugar')
        scene = af.find_scene(acid,userinfo[4],userinfo[5])
        if  scene!=None:
            dc.set_next_topic(acid,'scene-selected',scene)
    return af.print_scene_info(acid,'pt-br',scene)

def perguntaNomeCena(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    scene = dc.get_topic_content(acid)
    if topic=='scene-selected' and scene!=None:
        ac.print_dbg('intencoes','perguntaNomeCena ','scene=',scene)
        dc.keep_topic(acid)
    else:
        userinfo=ac.look_avatar_with_name(acid,username)
        if userinfo==None:
            return dc.gen_speak(acid,'naoSeiOndeVoceEsta')
        dist = float(userinfo[3])
        if dist>20.0:
            return dc.gen_speak(acid,'voceEstaDistante')+".\n"+dc.gen_speak(acid,'naoVejoLugar')
        scene = af.find_scene(acid,userinfo[4],userinfo[5])
        if  scene!=None:
            dc.set_next_topic(acid,'scene-selected',scene)
    return af.print_scene_name(acid,'pt-br',scene)

def perguntaConfirmaNomeCena(acid,username,userinput,matches):
    userinfo=ac.look_avatar_with_name(acid,username)
    if userinfo==None:
       return dc.gen_speak(acid,'naoSeiOndeVoceEsta')
    dist = float(userinfo[3])
    if dist>20.0:
        return dc.gen_speak(acid,'voceEstaDistante')+".\n"+dc.gen_speak(acid,'naoVejoLugar')
    scene = af.find_scene(acid,userinfo[4],userinfo[5])
    if  scene==None:
        return "Não há nenhuma cena aqui"
    scenename = ac.remember(acid,['scene-name',scene[1]])
    if scenename==None:
        return "Não sei o nome da cena aqui"
    if af.string_similarity(scenename[2],matches[0])<0.9:
        return "Acho que não é a mesma cena que você falou, a cena aqui se chama "+scenename[2]
    return "Sim, esse é o nome da cena aqui"


###################################
# Intentions functions to answer
# questions about TASKS
###################################

def respostaSim_listing_tasks(acid,username,userinput,matches):
    ac.print_dbg('intencoes',"listing-places")
    tasklist = dc.get_topic_content(acid)
    ac.print_dbg('intencoes',"tasklist=",tasklist)
    cenas=dc.gen_speak(acid,'sinonTarefas')
    if tasklist:
        resp=dc.gen_speak(acid,'segueListagem(ITEMS)',[cenas])+":\n"
        resp+=printingScenes(acid,tasklist)
        ac.print_dbg('intencoes',"printingTasks= ",resp)
    else:
        resp=dc.gen_speak(acid,'fimListagem(ITEMS)',[cenas])+":\n"
    return resp
 
 
def respostaNao_listing_tasks(acid,username,userinput,matches):
    return dc.gen_speak(acid,'pareiListagem')+'. '+dc.gen_speak(acid,'sePrecisarAjuda')


def printingTasks(acid,tasknamelist):
    resp = ""
    while tasknamelist:
        resp += tasknamelist.pop(0)+"\n"
        if tasknamelist==[]:
            resp+=dc.gen_speak(acid,'fimListagem(ITEMS)',["tarefas"])            
        elif len(resp)>500:
            resp+=dc.gen_speak(acid,'querVerMaisTarefas')
            dc.set_next_topic(acid,'listing-tasks',tasknamelist.copy())
            tasknamelist=[]
    return resp
    

def perguntaTarefasConhecidas(acid,username,userinput,matches):
    ktasks = ac.remember_all(acid,['known-task'])
    if ktasks==None or len(ktasks)==0:
        return dc.gen_speak(acid,'naoConhecoTarefas')
    resp = dc.gen_speak(acid,'conhecoTarefas')+":\n"
    tasknamelist=[]
    for task in ktasks:
        taskname = ac.remember(acid,['known-task-name',task[1]])
        if taskname!=None:
            tasknamelist.append(taskname[2])
    resp+=printingTasks(acid,tasknamelist)
    return resp

        
def perguntaInformacaoTarefaComNome(acid,username,userinput,matches):
    task = af.find_task_with_name(acid,matches[0])
    if task==None:
        return "Não sei como fazer essa tarefa"
    return af.print_task_info(acid,'pt-br',task)


