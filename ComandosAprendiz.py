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
#   Module:     ComandosAprendiz 
#   Purpose:    Exemplo de modulo que implementa as intencoes por trás 
#               de conversas/dialogos com comandos ao ator aprendiz
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

""" Modulo IntencoesComandosAprendiz - Exemplo de modulo que implementa
        intenções por trás de conversas/dialogos com comandos ao ator 
        aprendiz (trainee actor) """

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


#####################################
# Intention functions to execute
# learned TASKS or generic commands
#####################################

def _doCommand(acid,cmd):
    rval = True
    if cmd=="sentar":
        ac.sit(acid)
    elif cmd=="levantar":
        ac.stand(acid)
    elif cmd=="bater palmas":
        ac.start_play(acid,'std_anim','clap')
        delay=random.choice([0.5,1.0,1.5,2.0,2.5,3.0])
        time.sleep(delay)
        ac.stop_play(acid,'std_anim','clap') 
    elif cmd=="dançar":
        ac.start_play(acid,'std_anim','dance1')
        delay=random.choice([0.5,1.0,1.5,2.0,2.5,3.0])
        time.sleep(delay)
        ac.stop_play(acid,'std_anim','dance1')
    elif cmd=="curvar":
        ac.start_play(acid,'std_anim','bow')
        delay=random.choice([0.5,1.0,1.5,2.0,2.5,3.0])
        time.sleep(delay)
        ac.stop_play(acid,'std_anim','bow')
    elif cmd=="pular":
        ac.jump(acid,'start')
        delay=random.choice([0.5,1.0,1.5,2.0,2.5,3.0])
        time.sleep(delay)
        ac.jump(acid,'stop')
    elif cmd=="agachar":
        ac.crouch(acid,'start')
        delay=random.choice([0.5,1.0,1.5,2.0,2.5,3.0])
        time.sleep(delay)
        ac.crouch(acid,'stop')
    elif cmd=="correr":
        ac.fly(acid, 'stop')
        ac.run(acid, 'start')
    elif cmd=="voar":
        ac.run(acid, 'stop')
        ac.fly(acid, 'start')
    elif cmd=="caminhar":
        ac.run(acid, 'stop')
        ac.fly(acid, 'stop')
    else:
        rval = False
    return rval
        
def ordenaComando(acid,username,userinput,matches):
    resp = dc.gen_speak(acid,'atenderDesejo(DESCR)',matches,'OK')
    rval = _doCommand(acid,matches[0])
    if rval:
        resp= resp + " ... feito"
    else:
        resp= resp + " ... deu algum problema"
    return resp

def facaTarefa(acid,username,userinput,matches):
    knowntasks = ac.remember_all(acid,['known-task'])
    maxsimil = 0.0
    maxsimil_taskid=None
    maxsimil_taskname=None
    for task in knowntasks:
        taskname = ac.remember(acid,['known-task-name',task[1]])
        simil = af.string_similarity(matches[0],taskname[2])
        if simil>maxsimil:
            maxsimil = simil
            maxsimil_taskid=task[1]
            maxsimil_taskname=taskname[2]
    if maxsimil<0.9:
        return "Não conheço tarefa com esse nome de "+matches[0]
    ac.say(acid,"Ok vou fazer a tarefa de "+maxsimil_taskname)
    ac.say(acid,"Começando a executar as ações que aprendi nessa tarefa ...")
    learnedtask = ac.remember_all(acid,['known-task-intent',maxsimil_taskid])
    learnedtask.sort()
    lasttime=0.0
    for intent in learnedtask:
        currtime = float(intent[3])
        ac.print_dbg('intencoes','replay lasttime=',lasttime,' currtime=',currtime)
        if lasttime>0.0:
            sleeptime = currtime - lasttime
            ac.print_dbg('intencoes','replay sleeptime=',sleeptime)
            if sleeptime>0:
                sleeptime = min(sleeptime,300.0)
                time.sleep(sleeptime)
        lasttime = currtime
        # Quando faz um replay da intencao, troca o nome de usuario 
        # para o usuario atual
        resp=dc.replay_intent(acid, username, intent[5], intent[6], intent[7:-1])
        if resp!=None:
            ac.say(acid,resp)
    return "Ok finalizei a tarefa"

#####################################
# Intention functions to execute
# MOVEMENT commands
#####################################

def vaParaPosicao(acid,username,userinput,matches):
    ac.print_dbg('intencoes','vaParaPosicao: ',matches)
    try:
        xpos=float(matches[0])
        ypos=float(matches[1])
    except:
        return " ... desculpa, não entendi, posso apenas ir para lugares definidas por coordenadas numericas X Y"    
    resp = dc.gen_speak(acid,'vouIrAte(X;Y)',[xpos,ypos],"Indo")
    ac.walk_to(acid,xpos,ypos)
    return resp

def vaEmFrente(acid,username,userinput,matches):
    if af.maybe(0.7):
        rval=ac.forward(acid)
    else:
        tim=random.choice([1,2,3])
        rval=ac.forward(acid,tim,'sec')
    if rval:
        resp = dc.gen_speak(acid,'respostaSim')
    else:
        resp = dc.gen_speak(acid,'respostaNao')
    return resp

def vaParaTras(acid,username,userinput,matches):
    if af.maybe(0.7):
        rval=ac.backward(acid)
    else:
        tim=random.choice([1,2,3])
        rval=ac.backward(acid,tim,'sec')
    if rval:
        resp = dc.gen_speak(acid,'respostaSim')
    else:
        resp = dc.gen_speak(acid,'respostaNao')
    return resp

def vaParaDireita(acid,username,userinput,matches):
    if af.maybe(0.7):
        rval=ac.rightward(acid)
    else:
        tim=random.choice([1,2,3])
        rval=ac.rightward(acid,tim,'sec')
    if rval:
        resp = dc.gen_speak(acid,'respostaSim')
    else:
        resp = dc.gen_speak(acid,'respostaNao')
    return resp

def vaParaEsquerda(acid,username,userinput,matches):
    if af.maybe(0.7):
        rval=ac.leftward(acid)
    else:
        tim=random.choice([1,2,3])
        rval=ac.leftward(acid,tim,'sec')
    if rval:
        resp = dc.gen_speak(acid,'respostaSim')
    else:
        resp = dc.gen_speak(acid,'respostaNao')
    return resp

def pareDeVoar(acid,username,userinput,matches):
    ac.fly(acid, 'stop')
    ac.forward(acid)
    resp = dc.gen_speak(acid,'respostaSim')
    return resp

def comeceVoar(acid,username,userinput,matches):
    ac.fly(acid, 'start')
    ac.run(acid, 'stop')
    resp = dc.gen_speak(acid,'respostaSim')
    return resp

def pareDeCorrer(acid,username,userinput,matches):
    ac.run(acid, 'stop')
    resp = dc.gen_speak(acid,'respostaSim')
    return resp

def comeceCorrer(acid,username,userinput,matches):
    ac.run(acid, 'start')
    resp = dc.gen_speak(acid,'respostaSim')
    return resp

def comeceAndar(acid,username,userinput,matches):
    ac.fly(acid, 'stop')
    ac.run(acid, 'stop')
    resp = dc.gen_speak(acid,'respostaSim')
    return resp

def venhaAqui(acid,username,userinput,matches):
    userinfo=ac.look_avatar_with_name(acid,username)
    if userinfo==None:
        return dc.gen_speak(acid, 'naoSeiOndeVoceEsta')
    dist = float(userinfo[3])
    if dist>20.0:
        return dc.gen_speak(acid, 'voceEstaDistante')
    x = float(userinfo[4])+1.0 if af.maybe(0.5) else float(userinfo[4])-1.0
    y = float(userinfo[5])+1.0 if af.maybe(0.5) else float(userinfo[5])-1.0    
    ac.walk_to(acid,x,y)
    ac.record(acid,['walking-to-avatar',userinfo[1],str(x),str(y)])
    dc.replace_recording_intent(acid,username,userinput,'vaParaPosicao',[str(x),str(y)])       
    return dc.gen_speak(acid, 'estouVindo')

def teleporteAqui(acid,username,userinput,matches):
    userinfo=ac.look_avatar_with_name(acid,username)
    if userinfo==None:
        return dc.gen_speak(acid, 'naoSeiOndeVoceEsta')
    dist = float(userinfo[3])
    if dist>20.0:
        return dc.gen_speak(acid, 'voceEstaDistante')
    xtarget = float(userinfo[4])+1.0 if af.maybe(0.5) else float(userinfo[4])-1.0
    ytarget = float(userinfo[5])+1.0 if af.maybe(0.5) else float(userinfo[5])-1.0    
    ac.tele_to(acid,xtarget,ytarget)  
    ac.fly(acid,'stop')
    ac.forward(acid)
    ac.turn_to_avatar(acid,userinfo[1])
    return dc.gen_speak(acid, 'estouTeleportando')

def sigaMe(acid,username,userinput,matches):
    rval=ac.follow(acid,username)
    if rval:
        ac.record(acid,['following-avatar',username])
        resp= dc.gen_speak(acid, 'vouSeguirVoce')
    else:
        resp= " ... desculpa, não posso seguir você"
    return resp

def meDeixeSozinho(acid,username,userinput,matches):
    followvar = ac.remember(acid,['following-avatar'])
    if followvar!=None:
        ac.stop_follow(acid)
        ac.forget(acid,['following-avatar'])
        resp=dc.gen_speak(acid, 'naoVouSeguirVoce')
    else:
        resp=dc.gen_speak(acid, 'ateLogo')
    return resp

def vaParaLugar(acid,username,userinput,matches):
    placefound = af.find_place_with_name_or_descr(acid,matches[0])
    if  placefound==None:
        return dc.gen_speak(acid,'naoLembroLugarChamado(NOME)',[matches[0]])
    simil,placeid,placename=placefound
    if  simil>0.9:
        ac.say(acid,dc.gen_speak(acid,'lembroLugarExato(NOME)',[placename]))
    else:
        ac.say(acid,dc.gen_speak(acid,'lembroLugarParecido(NOME)',[placename]))    
    place=ac.remember(acid,['known-place',placeid])
    x=float(place[2])
    y=float(place[3])
    ac.walk_to(acid,x,y)
    ac.print_dbg('intencoes','va para lugar x=',x,' y=',y)
    return dc.gen_speak(acid,'estouIndoParaLa')
        
def meLeveLugar(acid,username,userinput,matches):
    placefound = af.find_place_with_name_or_descr(acid,matches[0])
    if  placefound==None:
        return dc.gen_speak(acid,'naoLembroLugarChamado(NOME)',[matches[0]])
    simil,placeid,placename=placefound
    if  simil>0.9:
        ac.say(acid,dc.gen_speak(acid,'lembroLugarExato(NOME)',[placename]))
    else:
        ac.say(acid,dc.gen_speak(acid,'lembroLugarParecido(NOME)',[placename]))
    ac.say(acid,dc.gen_speak(acid,'estouIndoParaLa'))
    place=ac.remember(acid,['known-place',placeid])
    x=float(place[2])
    y=float(place[3])
    ac.walk_to(acid,x,y)
    ac.print_dbg('intencoes','me leve lugar x=',x,' y=',y)
    return dc.gen_speak(acid,'venhaComigo')
        
def vaParaCena(acid,username,userinput,matches):
    scene = af.find_scene_with_name(acid,matches[0])
    if  scene==None:
        return dc.gen_speak(acid,'naoLembroCenaChamada(NOME)',[matches[0]])
    ac.say(acid,dc.gen_speak(acid,'lembroCenaChamada(NOME)',[matches[0]]))
    scenepos=af.compute_scene_central_point(acid,scene[1])
    if scenepos==None:
        return "Não conseguir descobrir onde fica essa cena"
    x,y = scenepos
    ac.say(acid,"O ponto central desta cena fica na posição: "+str(x)+","+str(y))
    ac.walk_to(acid,x,y)
    ac.print_dbg('intencoes','va para lugar x=',x,' y=',y)
    return dc.gen_speak(acid,'estouIndoParaLa')
        
def meLeveCena(acid,username,userinput,matches):
    scene = af.find_scene_with_name(acid,matches[0])
    if  scene==None:
        return dc.gen_speak(acid,'naoLembroCenaChamada(NOME)',[matches[0]])
    ac.say(acid,dc.gen_speak(acid,'lembroCenaChamada(NOME)',[matches[0]]))
    scenepos=af.compute_scene_central_point(acid,scene[1])
    if scenepos==None:
        return "Não conseguir descobrir onde fica essa cena"
    x,y = scenepos
    ac.say(acid,"O ponto central desta cena fica na posição: "+str(x)+","+str(y))
    ac.walk_to(acid,x,y)
    ac.say(acid,dc.gen_speak(acid,'estouIndoParaLa'))
    ac.print_dbg('intencoes','me leve cena x=',x,' y=',y)
    return dc.gen_speak(acid,'venhaComigo')
        
def comecarTourTodosLugares(acid,username,userinput,matches):
    resp = dc.gen_speak(acid,'comecarTourLugaresConhecidos')
    ac.record(acid,['start-known-places-tour'])
    return resp

def visitarProximoLugar(acid,username,userinput,matches):
    resp = dc.gen_speak(acid,'vamosProximoLugar')
    ac.record(acid,['visit-next-place'])
    return resp

def pararTour(acid,username,userinput,matches):
    resp = dc.gen_speak(acid,'pararTour')+".\n"
    resp += dc.gen_speak(acid,'ateLogo')+".\n"
    resp += dc.gen_speak(acid,'voltarPosicaoInicial')
    ac.record(acid,['stop-tour'])
    return resp

def venhaAoConsultorio(acid,username,userinput,matches):
    ac.say(acid,dc.gen_speak(acid, 'estouVindo'))
    ac.say(acid,"Para o consultório")
    time.sleep(15.0)
    ac.walk_to(acid,87.0,84.0)
    time.sleep(2.0)
    ac.walk_to(acid,76.0,84.0)
    time.sleep(5.0)
    ac.walk_to(acid,76.0,87.0)
    time.sleep(3.0)
    return "Olá Dra. Carla, cheguei"


#####################################
# Intention functions to execute
# POSTURE/GESTURE commands
#####################################

def fale(acid,username,userinput,matches):
    return matches[0]

def olheParaMim(acid,username,userinput,matches):
    userinfo=ac.look_avatar_with_name(acid,username)
    if userinfo!=None:
#       ac.print_dbg('intencoes','encontrou: ',userinfo)
        ac.turn_to_avatar(acid,userinfo[1])
        resp = dc.gen_speak(acid,'respostaSim')+". "+dc.gen_speak(acid,'estouTeOlhando')
    else:
        resp = dc.gen_speak(acid,'naoSeiOndeVoceEsta')
    return resp

def deiteNaMesa(acid,username,userinput,matches):
    mesa = ac.seek_objs_by_name(acid,20.0,'deitar-mesa',1,False)
    if (mesa!=None and mesa!=[]):
        ac.sit_on(acid,mesa[0][1])
        resp = dc.gen_speak(acid,'deitei(NACOISA)',['na mesa'])
    else:
        resp = dc.gen_speak(acid,'nãoVejo(ACOISA)',['a mesa'])
    return resp

def deiteNaCama(acid,username,userinput,matches):
    cama = ac.seek_objs_by_name(acid,20.0,'deitar-cama',1,False)
    if (cama!=None and cama!=[]):
        ac.sit_on(acid,cama[0][1])
        resp = dc.gen_speak(acid,'deitei(NACOISA)',['na cama'])
    else:
        resp = dc.gen_speak(acid,'nãoVejo(ACOISA)',['a cama'])
    return resp

def deiteNoSofa(acid,username,userinput,matches):
    sofa = ac.seek_objs_by_name(acid,20.0,'deitar-sofa',1,False)
    if (sofa!=None and sofa!=[]):
        ac.sit_on(acid,sofa[0][1])
        resp = dc.gen_speak(acid,'deitei(NACOISA)',['no sofá'])
    else:
        resp = dc.gen_speak(acid,'nãoVejo(ACOISA)',['o sofá'])
    return resp

def senteNaMesa(acid,username,userinput,matches):
    mesa = ac.seek_objs_by_name(acid,20.0,'sentar-mesa',1,False)
    if (mesa!=None and mesa!=[]):
        ac.sit_on(acid,mesa[0][1])
        resp = dc.gen_speak(acid,'sentei(NACOISA)',['na mesa'])
    else:
        resp = dc.gen_speak(acid,'nãoVejo(ACOISA)',['a mesa'])
    return resp

def senteNaCadeira(acid,username,userinput,matches):
    cadeira = ac.seek_objs_by_name(acid,20.0,'sentar-cadeira',1,False)
    if (cadeira!=None and cadeira!=[]):
        ac.sit_on(acid,cadeira[0][1])
        resp = dc.gen_speak(acid,'sentei(NACOISA)',['na cadeira'])
    else:
        resp = dc.gen_speak(acid,'nãoVejo(ACOISA)',['a cadeira'])
    return resp

def senteNaCama(acid,username,userinput,matches):
    cama = ac.seek_objs_by_name(acid,20.0,'sentar-cama',1,False)
    if (cama!=None and cama!=[]):
        ac.sit_on(acid,cama[0][1])
        resp = dc.gen_speak(acid,'sentei(NACOISA)',['na cama'])
    else:
        resp = dc.gen_speak(acid,'nãoVejo(ACOISA)',['a cama'])
    return resp

def levanteBracoParaFrente(acid,username,userinput,matches):
    if matches!=None and matches[0]!=None:
        if matches[0]=='esquerdo':
            ac.start_posing(acid,'left-arm','forward')
            resp = dc.gen_speak(acid,'levantando(OMEMBRO;NAPOSICAO)',['o braço esquerdo','pra frente'])
        elif matches[0]=='direito':
            ac.start_posing(acid,'right-arm','forward')
            resp = dc.gen_speak(acid,'levantando(OMEMBRO;NAPOSICAO)',['o braço direito','pra frente'])
        else:
            resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['o braço'])
    else:
        resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['o braço'])
    return resp

def bracosParaFrente(acid,username,userinput,matches):
    ac.start_posing(acid,'left-arm','forward')
    ac.start_posing(acid,'right-arm','forward')
    resp = dc.gen_speak(acid,'levantando(OMEMBRO;NAPOSICAO)',['os braços','pra frente'])
    return resp

def levanteBracoParaCima(acid,username,userinput,matches):
    if matches!=None and matches[0]!=None:
        if matches[0]=='esquerdo':
            ac.start_posing(acid,'left-arm','up')
            resp = dc.gen_speak(acid,'levantando(OMEMBRO;NAPOSICAO)',['o braço esquerdo','pra cima'])
        elif matches[0]=='direito':
            ac.start_posing(acid,'right-arm','up')
            resp = dc.gen_speak(acid,'levantando(OMEMBRO;NAPOSICAO)',['o braço direito','pra cima'])
        else:
            resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['o braço'])
    else:
        resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['o braço'])
    return resp

def bracosParaCima(acid,username,userinput,matches):
    ac.start_posing(acid,'left-arm','up')
    ac.start_posing(acid,'right-arm','up')
    resp = dc.gen_speak(acid,'levantando(OMEMBRO;NAPOSICAO)',['os braços','pra cima'])
    return resp

def levanteBracoParaLado(acid,username,userinput,matches):
    if matches!=None and matches[0]!=None:
        if matches[0]=='esquerdo':
            ac.start_posing(acid,'left-arm','side')
            resp = dc.gen_speak(acid,'levantando(OMEMBRO;NAPOSICAO)',
                            'Levantando o braço esquerdo pro lado',['o braço esquerdo','pro lado'])
        elif matches[0]=='direito':
            ac.start_posing(acid,'right-arm','side')
            resp = dc.gen_speak(acid,'levantando(OMEMBRO;NAPOSICAO)',['o braço direito','pro lado'])
        else:
            resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['o braço'])
    else:
        resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['o braço'])
    return resp

def abraBracos(acid,username,userinput,matches):
    ac.start_posing(acid,'left-arm','side')
    ac.start_posing(acid,'right-arm','side')
    resp = dc.gen_speak(acid,'abrindo(OMEMBRO;NAPOSICAO)',['os braços','pro lado'])
    return resp

def abaixeBraco(acid,username,userinput,matches):
    if matches!=None and matches[0]!=None:
        if matches[0]=='esquerdo':
            ac.start_posing(acid,'left-arm','down')
            resp = dc.gen_speak(acid,'abaixando(OMEMBRO)',['o braço esquerdo'])
        elif matches[0]=='direito':
            ac.start_posing(acid,'right-arm','down')
            resp = dc.gen_speak(acid,'abaixando(OMEMBRO)',['o braço direito'])
        else:
            resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['o braço'])
    else:
        resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['o braço'])
    return resp

def pareMoverBraco(acid,username,userinput,matches):
    if matches!=None and matches[0]!=None:
        if matches[0]=='esquerdo':
            ac.stop_posing(acid,'left-arm')
            resp = dc.gen_speak(acid,'parandoDeMover(OMEMBRO)',['o braço esquerdo'])
        elif matches[0]=='direito':
            ac.stop_posing(acid,'right-arm')
            resp = dc.gen_speak(acid,'parandoDeMover(OMEMBRO)',['o braço direito'])
        else:
            resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['o braço'])
    else:
        resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['o braço'])
    return resp

def pareMoverOsBracos(acid,username,userinput,matches):
    ac.stop_posing(acid,'left-arm')
    ac.stop_posing(acid,'right-arm')
    resp = dc.gen_speak(acid,'parandoDeMover(OMEMBRO)',['os bracos'])
    
def levantePernaParaCima(acid,username,userinput,matches):		
    if matches!=None and matches[0]!=None:
        if matches[0]=='esquerda':
            ac.start_posing(acid,'left-leg','lift-up')
            resp = dc.gen_speak(acid,'levantando(OMEMBRO;NAPOSICAO)',['a perna esquerda','pra cima'])
        elif matches[0]=='direita':
            ac.start_posing(acid,'right-leg','lift-up')
            resp = dc.gen_speak(acid,'levantando(OMEMBRO;NAPOSICAO)',['a perna direita','pra cima'])
        else:
            resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['a perna'])
    else:
        resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['a perna'])
    return resp

def levanteUmPoucoPerna(acid,username,userinput,matches):	
    if matches!=None and matches[0]!=None:
        if matches[0]=='esquerda':
            ac.start_posing(acid,'left-leg','half-lift')
            resp = dc.gen_speak(acid,'levantando(OMEMBRO;NAPOSICAO)',['a perna esquerda','um pouco pra cima'])
        elif matches[0]=='direita':
            ac.start_posing(acid,'right-leg','half-lift')
            resp = dc.gen_speak(acid,'levantando(OMEMBRO;NAPOSICAO)',['a perna direita','um pouco pra cima'])
        else:
            resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['a perna'])
    else:
        resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['a perna'])
    return resp

def abaixePerna(acid,username,userinput,matches):	
    if matches!=None and matches[0]!=None:
        if matches[0]=='esquerda':
            ac.start_posing(acid,'left-leg','down')
            resp = dc.gen_speak(acid,'abaixando(OMEMBRO)',['a perna esquerda'])
        elif matches[0]=='direita':
            ac.start_posing(acid,'right-leg','down')
            resp = dc.gen_speak(acid,'abaixando(OMEMBRO)',['a perna direita'])
        else:
            resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['a perna'])
    else:
        resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['a perna'])
    return resp

def dobrePerna(acid,username,userinput,matches):	
    if matches!=None and matches[0]!=None:
        if matches[0]=='esquerda':
            ac.start_posing(acid,'left-leg','bent')
            resp = dc.gen_speak(acid,'dobrando(OMEMBRO)',['a perna esquerda'])
        elif matches[0]=='direita':
            ac.start_posing(acid,'right-leg','bent')
            resp = dc.gen_speak(acid,'dobrando(OMEMBRO)',['a perna direita'])
        else:
            resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['a perna'])
    else:
        resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['a perna'])
    return resp

def pareMoverPerna(acid,username,userinput,matches):		
    if matches!=None and matches[0]!=None:
        if matches[0]=='esquerda':
            ac.stop_posing(acid,'left-leg')
            resp = dc.gen_speak(acid,'parandoDeMover(OMEMBRO)',['a perna esquerda'])
        elif matches[0]=='direita':
            ac.stop_posing(acid,'right-leg')
            resp = dc.gen_speak(acid,'parandoDeMover(OMEMBRO)',['a perna direita'])
        else:
            resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['o braço'])
    else:
        resp = dc.gen_speak(acid,'qualMesmo(ACOISA)',['o braço'])
    return resp

def pareMoverAsPernas(acid,username,userinput,matches):
    ac.stop_posing(acid,'left-leg')
    ac.stop_posing(acid,'right-leg')
    resp = dc.gen_speak(acid,'parandoDeMover(OMEMBRO)',['as pernas'])
    return resp
    
def vireCabecaParaDireita(acid,username,userinput,matches):	
    ac.start_posing(acid,'head','turn-right')
    resp = dc.gen_speak(acid,'virando(OMEMBRO;POSICAO)',['a cabeca', 'para direita'])
    return resp
    
def vireCabecaParaEsquerda(acid,username,userinput,matches):	
    ac.start_posing(acid,'head','turn-left')
    resp = dc.gen_speak(acid,'virando(OMEMBRO;POSICAO)',['a cabeca', 'para esquerda'])
    return resp
    
def vireCabecaParaCima(acid,username,userinput,matches):	
    ac.start_posing(acid,'head','look-up')
    resp = dc.gen_speak(acid,'virando(OMEMBRO;POSICAO)',['a cabeca', 'para cima'])
    return resp
    
def vireCabecaParaBaixo(acid,username,userinput,matches):	
    ac.start_posing(acid,'head','look-down')
    resp = dc.gen_speak(acid,'virando(OMEMBRO;POSICAO)',['a cabeca', 'para baixo'])
    return resp

def deiteSeChao(acid,username,userinput,matches):
    ac.start_posing(acid,'body','lying')
    resp = dc.gen_speak(acid,'deitando(NACOISA)',['no chão'],"Deitando")
    return resp

def levanteSeChao(acid,username,userinput,matches):
    ac.stop_posing(acid,'body')
    ac.stand(acid)
    resp = dc.gen_speak(acid,'levantando(DACOISA)',['do chão'],"Levantando")
    return resp

def fiqueDePe(acid,username,userinput,matches):
    ac.stop_play(acid,'asset-id','0accf5e0-a113-4301-9c91-5456b99575b7')
    ac.stand(acid)
    resp = dc.gen_speak(acid,'ficandoDePe')
    return resp

def iniciarAnimacaoPadrao(acid,username,userinput,matches):
    if matches!=None and matches[0]!=None:
        resp = dc.gen_speak(acid,'vouTentarComecar(ATIV)',["a animação padrão: "],"Iniciando animação")
        resp += matches[0]
        ac.start_play(acid,'std_anim',matches[0])
    else:
        resp=dc.gen_speak(acid, 'qualMesmo(ACOISA)',["a animação"],"Qual animação?")
    return resp

def iniciarAnimacaoGravada(acid,username,userinput,matches):
    if matches!=None and matches[0]!=None:
        resp = dc.gen_speak(acid,'vouTentarComecar(ATIV)',["a animação: "],"Iniciando animação")
        resp += matches[0]+" que está gravada no meu inventário"
        ac.start_play(acid,'item',matches[0])
    else:
        resp=dc.gen_speak(acid, 'qualMesmo(ACOISA)',["a animação"],"Qual animação?")
    return resp

def pararAnimacaoPadrao(acid,username,userinput,matches):
    if matches!=None and matches[0]!=None:
        resp = dc.gen_speak(acid,'vouTentarParar(ATIV)',["a animação padrão: "],"Parando animação")
        resp += matches[0]
        ac.stop_play(acid,'std_anim',matches[0])
    else:
        resp=dc.gen_speak(acid, 'qualMesmo(ACOISA)',["a animação"],"Qual?")
    return resp

def pararAnimacaoGravada(acid,username,userinput,matches):
    if matches!=None and matches[0]!=None:
        resp = dc.gen_speak(acid,'vouTentarParar(ATIV)',["a animação: "],"Parando animação")
        resp += matches[0]+" que está gravada no meu inventário"
        ac.stop_play(acid,'item',matches[0])
    else:
        resp=dc.gen_speak(acid, 'qualMesmo(ACOISA)',["a animação"],"Qual?")
    return resp


#####################################
# Intention functions to locate
# and manipulate OBJECTS
#####################################


def respostaSim_confirm_obj(acid,username,userinput,matches):
    selobj = dc.get_topic_content(acid)
    dc.set_next_topic(acid,'obj-selected',selobj)
    return dc.gen_speak(acid,'acheiObjeto')

def respostaNao_confirm_obj(acid,username,userinput,matches):
    ac.stop_pointing(acid)
    return dc.gen_speak(acid,'naoAcheiObjeto')

def olheObjeto(acid,username,userinput,matches):
    objinfo = af.find_nearest_obj(acid)
    if objinfo!=None:
        ac.turn_to_obj(acid,objinfo[1])
        resp = af.print_obj_info(acid, 'pt-br', objinfo)
        resp += ". "+dc.gen_speak(acid,'pedeConfirmacaoObjeto')
        dc.set_next_topic(acid,'confirm-obj',objinfo[1])
    else:
        resp = dc.gen_speak(acid, 'naoVejoObjeto') + af.optional(0.5,", pode me mostrar de novo")
    return resp

def aponteObjeto(acid,username,userinput,matches):
    objinfo = af.find_nearest_obj(acid)
    if objinfo!=None:
        ac.print_dbg('intencoes','encontrou: ',objinfo)
        ac.turn_to_obj(acid,objinfo[1])
        ac.point_at_obj(acid,objinfo[1])
        resp = dc.gen_speak(acid,'pedeConfirmacaoObjeto')
        dc.set_next_topic(acid,'confirm-obj',objinfo[1])
    else:
        resp = dc.gen_speak(acid, 'naoVejoObjeto') + af.optional(0.5,", pode me mostrar de novo")
    return resp

def pareDeApontar(acid,username,userinput,matches):
    ac.stop_pointing(acid)
    resp = dc.gen_speak(acid, 'respostaSim')+ af.optional(0.5,", parei de apontar")
    return resp


def pegueCoisa(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    obj = dc.get_topic_content(acid)
    if topic!='obj-selected' or obj==None:
        obj = af.find_nearest_obj(acid)
    if  obj==None:
        return dc.gen_speak(acid,'naoVejoObjeto')
    if ac.take(acid,obj,'/Objects/'):
        ac.record(acid,['last-taken-obj',obj])
        return 'OK peguei o objeto'
    return 'Não pude pegar o objeto'

def pegueCoisaComNome(acid,username,userinput,matches):
    obj = af.find_obj_with_name(acid,matches[0])
    if  obj==None:
        return dc.gen_speak(acid,'naoVejoObjeto')
    if ac.take(acid,obj,'/Objects/'):
        ac.record(acid,['last-taken-obj',obj])
        return 'OK peguei o objeto'
    return 'Não pude pegar o objeto'

def largueCoisa(acid,username,userinput,matches):
    myobj = ac.remember(acid,['last-taken-obj'])
    if myobj==None or myobj==[]:
        return 'Não peguei nenhum objeto recentemente'
    myobj=myobj[1]
    ac.look_obj(acid,myobj)
    myobjname=ac.perceive(acid,['name',myobj])
    if myobjname==None or myobjname==[]:
        return 'Não lembro qual é o objeto que peguei por último'
    myobjname=myobjname[2]
    if ac.look_my_item(acid, '/Objects/'+myobjname)==None:
        return 'Não achei o objeto que peguei por último'
    userinfo=ac.look_avatar_with_name(acid,username)
    if userinfo!=None:
        time.sleep(2.0)
        ac.say(acid,'OK vou largar o objeto perto de você')
        x=float(userinfo[4])
        y=float(userinfo[5])
        z=float(userinfo[6])
    else:
        time.sleep(2.0)
        ac.say(acid,dc.gen_speak(acid, 'naoSeiOndeVoceEsta'))
        ac.say(acid,'Mas vou largar o objeto perto de min')
        mypos=ac.look_my_position(acid)
        x=float(mypos[2])
        y=float(mypos[3])
        z=float(mypos[4])
    x = x + 1.0 if af.maybe(0.5) else x - 1.0
    y = y + 1.0 if af.maybe(0.5) else y - 1.0
    ac.rezz(acid, myobjname, 'item', '/Objects/'+myobjname, x, y, z)
    time.sleep(2.0)
    return 'Largando meu objeto '+myobjname

def largueCoisaComNome(acid,username,userinput,matches):
    myobjname=matches[0]
    if ac.look_my_item(acid, '/Objects/'+myobjname)==None:
        return 'Não tenho um objeto com esse nome'
    userinfo=ac.look_avatar_with_name(acid,username)
    if userinfo!=None:
        time.sleep(2.0)
        ac.say(acid,'OK vou largar o objeto perto de você')
        x=float(userinfo[4])
        y=float(userinfo[5])
        z=float(userinfo[6])
    else:
        time.sleep(2.0)
        ac.say(acid,dc.gen_speak(acid, 'naoSeiOndeVoceEsta'))
        ac.say(acid,'Mas vou largar o objeto perto de min')
        mypos=ac.look_my_position(acid)
        x=float(mypos[2])
        y=float(mypos[3])
        z=float(mypos[4])
    x = x + 1.0 if af.maybe(0.5) else x - 1.0
    y = y + 1.0 if af.maybe(0.5) else y - 1.0
    ac.rezz(acid, myobjname, 'item', '/Objects/'+myobjname, x, y, z)
    time.sleep(2.0)
    return 'Largando meu objeto '+myobjname
    
def largueCoisaComNomeNaPosicao(acid,username,userinput,matches):
    myobjname=matches[0]
    if ac.look_my_item(acid, '/Objects/'+myobjname)==None:
        return 'Não tenho um objeto com esse nome'
    x=float(matches[1])
    y=float(matches[2])
    h=ac.look_height_at(acid, x, y)
    z=float(h[4])
    ac.say(acid,'OK vou largar o objeto na posição '+str(x)+', '+str(y)+', '+str(z))
    ac.rezz(acid, myobjname, 'item', '/Objects/'+myobjname, x, y, z)
    time.sleep(2.0)
    return 'Largando meu objeto '+myobjname

def largueCoisaNaPosicao(acid,username,userinput,matches):
    myobj = ac.remember(acid,['last-taken-obj'])
    if myobj==None or myobj==[]:
        return 'Não peguei nenhum objeto recentemente'
    myobj=myobj[1]
    ac.look_obj(acid,myobj)
    myobjname=ac.perceive(acid,['name',myobj])
    if myobjname==None or myobjname==[]:
        return 'Não lembro qual é o objeto que peguei por último'
    myobjname=myobjname[2]
    if ac.look_my_item(acid, '/Objects/'+myobjname)==None:
        return 'Não achei o objeto que peguei por último'
    x=float(matches[1])
    y=float(matches[2])
    h=ac.look_height_at(acid, x, y)
    z=float(h[4])
    ac.say(acid,'OK vou largar o objeto na posição '+str(x)+', '+str(y)+', '+str(z))
    ac.rezz(acid, myobjname, 'item', '/Objects/'+myobjname, x, y, z)
    time.sleep(2.0)
    return 'Largando meu objeto '+myobjname

def largueCoisaEmCima(acid,username,userinput,matches):
    myobj = ac.remember(acid,['last-taken-obj'])
    if myobj==None or myobj==[]:
        return 'Não peguei nenhum objeto recentemente'
    myobj=myobj[1]
    ac.look_obj(acid,myobj)
    myobjname=ac.perceive(acid,['name',myobj])
    if myobjname==None or myobjname==[]:
        return 'Não lembro qual é o objeto que peguei por último'
    myobjname=myobjname[2]
    if ac.look_my_item(acid, '/Objects/'+myobjname)==None:
        return 'Não achei o objeto que peguei por último'
    otherobj = af.find_obj_with_name(acid,matches[0])
    if  otherobj==None:
        return "Não vejo a coisa onde largar o objeto"
    otherobj=ac.look_obj(acid,otherobj)
    if  otherobj==None:
        return "Não sei onde está a coisa onde largar o objeto"
    x=float(otherobj[6])
    y=float(otherobj[7])
    z=float(otherobj[8])
    ac.say(acid,'OK vou largar o objeto na posição '+str(x)+', '+str(y)+', '+str(z))
    ac.rezz(acid, myobjname, 'item', '/Objects/'+myobjname, x, y, z)
    time.sleep(2.0)
    return 'Largando meu objeto '+myobjname

def largueCoisaComNomeEmCima(acid,username,userinput,matches):
    myobjname=matches[0]
    if ac.look_my_item(acid, '/Objects/'+myobjname)==None:
        return 'Não tenho um objeto com esse nome'
    otherobj = af.find_obj_with_name(acid,matches[0])
    if  otherobj==None:
        return "Não vejo a coisa onde largar o objeto"
    otherobj=ac.look_obj(acid,otherobj)
    if  otherobj==None:
        return "Não sei onde está a coisa onde largar o objeto"
    x=float(otherobj[6])
    y=float(otherobj[7])
    z=float(otherobj[8])
    ac.say(acid,'OK vou largar o objeto na posição '+str(x)+', '+str(y)+', '+str(z))
    ac.rezz(acid, myobjname, 'item', '/Objects/'+myobjname, x, y, z)
    time.sleep(2.0)
    return 'Largando meu objeto '+myobjname

objtypesdict = [
    ['prim', ['box'],       
                ['caixa','arca','baú','caixão','caixao','caixeta','caixote','cubo','dado',
                'dadinho', 'cubinho', 'caixinha', 'cubão']],
    ['prim', ['cylinder'], 
                ['cilindro', 'rolo', 'rolinho', 'cilindrinho', 'cilindrão','rolão']],
    ['prim', ['prism'], 
                ['prisma', 'piramide', 'pirâmide']],
    ['prim', ['sphere'], 
                ['esfera', 'bola', 'globo', 'bolinha', 'bolão', 'globinho', 'globão']],
    ['prim', ['torus'], 
                ['torus', 'rosquinha', 'rosca', 'toro', 'toróide', 'toroide', 'roscão']],
    ['prim', ['tube'], 
                ['tubo', 'cano', 'canudo', 'duto', 'ducto', 'mangueira', 'tubinho',
                'tubão', 'caninho', 'canão', 'canudinho', 'canudão']],
    ['prim', ['ring'], 
                ['anel', 'aro', 'argola', 'aliança', 'alianca', 'elo', 'anelzinho',
                'arinho', 'argolinha', 'aliancinha', 'elinho', 'argolão']],
    ['tree', ['pine1', 'pine2'], 
                ['pinheiro', 'araucária', 'araucaria', 'pinheirinho']],
    ['tree', ['oak'], 
                ['carvalho']],
    ['tree', ['tropicalbush1', 'tropicalbusc2'], 
                ['arbusto','arbusto tropical']],
    ['tree', ['palm1', 'palm2'], 
                ['palmeira', 'palma', 'bananeira']],
    ['tree', ['dogwood'], 
                ['dogwood', 'ipê', 'corniso']],
    ['tree', ['cypress1','cypress2'], 
                ['cipreste']],
    ['tree', ['plumeria'], 
                ['plumeria']],
    ['tree', ['winterpine1','winterpine2'], 
                ['pinheiro de inverno']],
    ['tree', ['winteraspen'], 
                ['álamo', 'alamo']],
    ['tree', ['eucalyptus'], 
                ['eucalipto']],
    ['tree', ['fern'], 
                ['samambaia']],
    ['tree', ['eelgrass'], 
                ['alga marinha', 'eelgrass']],
    ['tree', ['seasword'], 
                ['espada do mar','seasword']],
    ['tree', ['kelp'], 
                ['alga', 'sargaco', 'sargaço', 'kelp']],
    ['tree', ['beachgrass1'], 
                ['beachgrass','capim da praia','capim de praia','mato de praia','mato da praia']],
    ['grass', ['grass1','grass2', 'grass3', 'grass4', 'undergrowth1'], 
                ['grama', 'relva']]
]

def crieCoisaNaPosicao(acid,username,userinput,matches):
    x=float(matches[1])
    y=float(matches[2])
    h=ac.look_height_at(acid, x, y)
    z=float(h[4])
    tipobj = matches[0].lower()
    objtype = None
    subtype = None
    for ot in objtypesdict:
        if tipobj in ot[2]:
            objtype = ot[0]
            subtype = random.choice(ot[1])
            break
    if objtype==None or subtype==None:
        return "Não entendi o que você quer que eu crie?"
    ac.say(acid,'OK vou criar um '+matches[0]+' na posição '+str(x)+', '+str(y)+', '+str(z))
    ac.rezz(acid, matches[0], objtype, subtype, x, y, z)
    time.sleep(2.0)
    return 'Criando objeto '


