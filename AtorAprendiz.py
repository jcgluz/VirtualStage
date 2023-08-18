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
#   Module:     AtorAprendiz 
#   Purpose:    Exemplo de modulo de controle de um ator 
#               aprendiz (trainee actor)
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

""" Modulo AtorAprendiz - Exemplo de modulo de controle de um 
        ator aprendiz (apprentice actor) """

import sys
import time
import math
import clr
import threading
import queue
import re
import os
import random
import ActorController as ac
import DialogController as dc
import AuxiliaryFunctions as af


MIN_WAIT_TIME = 100

def press_enter():
    print('Press enter to continue')
    k=input()


def print_msg(msg):
    if msg!=None:
        ac.print_dbg('aprendiz','Recvd msg: ', msg)



StopAgent=False

def stop():
    global StopAgent
    StopAgent=True
    
def processa_msg_usuario(acid,agname,msg):
    print_msg(msg)
    # press_enter()
    resp=None
    if (msg!=None):
        try:
            resp = dc.process_dialog_input(acid,msg[1],msg[2])
        except Exception as e:
            print('Chat error')
            print(e)
            resp=dc.gen_speak(acid,'naoEntendiFala')+".\n"
            resp+=dc.gen_speak(acid,'faleNovamente')+".\n"
            resp+=dc.gen_speak(acid,'pecaAjuda')+".\n"
            resp+=dc.gen_speak(acid,'pecaAjudaConversa')
    return resp

def placeOrderField(placeord_mem):
    return int(placeord_mem[2])

def samePosition(x1,y1,x2,y2):
    return abs(float(x1)-float(x2))<0.5 and abs(float(y1)-float(y2))<0.5
    
def script_tour_lugares_conhecidos(acid,acname):
    global StopAgent
    # First, discover what places are known
    kplaces = ac.remember_all(acid,['known-place'])
    if kplaces==None or len(kplaces)==0:
         return dc.gen_speak(acid,'naoConhecoLugaresAqui')
    # Then, if there is places with visit order already defined
    placesorder = ac.remember_all(acid,['place-order'])
    if placesorder!=None:
        # Sort the list of ordered places found by visit order
        placesorder.sort(key=placeOrderField)
    # Create a list of ids of places to visit, starting from ordered places
    placestovisit=[]
    for place in placesorder:
        placestovisit.append(place[1])
    # And then adding the remaining known places to the end of ordered list 
    # (note that remaining places are added in no particular order)
    for place in kplaces:
            if not place[1] in placestovisit:
                placestovisit.append(place[1])
    # Start the tour by known places
    ac.print_dbg('aprendiz','placestovisit=',placestovisit)
    visitorder=0
    StopTour=False
    tour_state='starting'
    while not StopTour and not StopAgent:
        if tour_state=='starting':
            # Starting the tour
            txtmsg = dc.gen_speak(acid,'vemComigoPrimeiroLugar')
            ac.say(acid,txtmsg)
            placeid=placestovisit[visitorder]
            place=ac.remember(acid,['known-place',placeid])
            mypos = ac.look_my_position(acid)
            # Register current position
            walk_last_x = mypos[2]
            walk_last_y = mypos[3]
            # Register as last position the position of first place to visit
            walk_end_x = place[2]
            walk_end_y = place[3]
            ac.stop_follow(acid)
            time.sleep(1.5)
            # Start walking to first place
            ac.walk_to(acid,float(walk_end_x),float(walk_end_y))
            tour_state='walking'
            continue

        if tour_state=='walking':
            # Walking to next known place
            ac.print_dbg('aprendiz','walking')
            # Wait for some chat message for at most 3 seconds 
            msg = ac.wait_chat_msg(acid,'!'+acname,None,3)
            resp = processa_msg_usuario(acid,acname,msg)
            if resp!=None:
                ac.say(acid,resp)
            mypos = ac.look_my_position(acid)
            # Check if user wants to stop the tour
            stoptour_mem = ac.extract_memory(acid,['stop-tour'])
            if stoptour_mem!=None:
                # User wants to stop tour
                StopTour=True
            elif samePosition(mypos[2],mypos[3],walk_end_x,walk_end_y):
                # Continuing the tour and arrived to destination
                txtmsg = dc.gen_speak(acid,'chegamosLugar')
                ac.say(acid,txtmsg)
                placeid = placestovisit[visitorder]
                place = ac.remember(acid,['known-place',placeid])
                # Set the place as the topic of conversation
                dc.set_topic(acid,'place-selected',place)
                txtmsg=af.print_place_name(acid,'pt-br',place)
                ac.say(acid,txtmsg)
                # Inform user we arrived at next place
                txtmsg = dc.gen_speak(acid,'perguntaInformacaoLugar')
                # Indicates will start visiting the place
                tour_state = 'visiting'
            elif samePosition(walk_last_x,walk_last_y,mypos[2],mypos[3]):
                # Actor's avatar do not moved from last check, probably is stuck
                # by some obstacle, stop the tour
                ac.say(acid,txtmsg)
                StopTour = True
            else:
                # Continuing the tour and still walking to next place
                # Only update current position
                walk_last_x=mypos[2]
                walk_last_y=mypos[3]
            continue
            
        if tour_state=='visiting':
            # Visiting the known place
            # Wait for some chat message for at most 1 second
            msg = ac.wait_chat_msg(acid,'!'+acname,None,1)
            resp = processa_msg_usuario(acid,acname,msg)
            if resp!=None:
                #ac.print_dbg('aprendiz',"will say: ",resp)
                ac.say(acid,resp)
            stoptour_mem = ac.extract_memory(acid,['stop-tour'])
            visitnext_mem = ac.extract_memory(acid,['visit-next-place'])
            if stoptour_mem!=None:
                StopTour=True
            elif visitnext_mem!=None:
                txtmsg = dc.gen_speak(acid,'vemComigoProximoLugar')
                ac.say(acid,txtmsg)
                visitorder += 1
                if visitorder>=len(placestovisit):
                    visitorder=0
                placeid=placestovisit[visitorder]
                place=ac.remember(acid,['known-place',placeid])
                mypos = ac.look_my_position(acid)
                walk_last_x = mypos[2]
                walk_last_y = mypos[3]
                walk_end_x = place[2]
                walk_end_y = place[3]
                ac.stop_follow(acid)
                time.sleep(1.5)
                ac.walk_to(acid,float(walk_end_x),float(walk_end_y))
                tour_state='walking'
            continue
        
        StopTour=True
   

def script_principal(acid,acname,initial_x,initial_y):
    global StopAgent, ActorID
    ac.enable_print_dbg()
    ac.print_dbg('aprendiz','Inicializando controlador de dialogos')
    # Informacoes do personagem digital controlado pelo ator
    # (podem ser usadas nos dialogos de linguagem natural) 
    ac.record(acid,['actor-creator','João Gluz'])
    ac.record(acid,['actor-name',acname])
    ac.record(acid,['actor-location','Porto Alegre'])
    ac.record(acid,['actor-age','1'])
    ac.record(acid,['actor-gender','R'])
    ac.record(acid,['character-name','Estagiário'])
    ac.record(acid,['character-type','aprendiz'])
    ac.record(acid,['character-nickname','Novato'])
    ac.record(acid,['character-formal-name','Estagiário'])
    ac.record(acid,['character-gender','M'])
    ac.record(acid,['default-place-radius','5.0'])
     
    dc.set_dialog_patterns_file(acid,'IntencoesAprendiz.json')
    dc.set_dialog_intents_file(acid,'IntencoesAprendiz')
    dc.set_dialog_speeches_file(acid,'FalasAprendiz.json')
    dc.set_dialog_hear_talk_rules_file(acid,'BatePaposAprendiz.json')
    dc.set_dialog_aiml_files(acid,['aiml\\cybora-bot\\cybora-*.aiml'])
    dc.init_dialog_system(acid)
    
    # Informacoes repassadas ao kernel de processamento AIML da Cybora
    # através de propriedades globais (aka 'bot predicates')
    dc.aiml_set_bot_prop(acid, 'master', 'Paulo Gonçalves')
    dc.aiml_set_bot_prop(acid, 'name', acname)
    dc.aiml_set_bot_prop(acid, 'sexo', 'robô feminino')
    dc.aiml_set_bot_prop(acid, 'sexo2', 'robô feminino')
    dc.aiml_set_bot_prop(acid, 'sexoposto', 'robô')
    # ac.tele_to(acid,80.0,18.0)
    # time.sleep(6.0)   
    # ac.say(acid,dc.gen_speak(acid,'irParaClinica'))
    # ac.walk_to(acid,80.0,44.0)
    # time.sleep(10.0)
    # ac.walk_to(acid,107.0,49.0)
    # time.sleep(10.0)
    # ac.walk_to(acid,107.0,73.0)
    # time.sleep(10.0)
    # ac.walk_to(acid,89.0,73.0)
    # time.sleep(6.0)
    # ac.turn_to_avatar(acid,'atendente marcos')
    # ac.say(acid,'Olá!')
    # time.sleep(4.0)
    # ac.say(acid,'Bom dia!')
    # time.sleep(15.0)
    # ac.say(acid,'Tenho uma consulta marcada daqui a pouco, as 10h com a dra. Carla')
    # time.sleep(20.0)
    # cadeira = ac.seek_objs_by_name(acid,10.0,'sentar-recepcao-2',1,False)
    # if (cadeira!=None and cadeira!=[]):
        # ac.say(acid,'Que bom tem uma cadeira livre, vou me sentar')
        # ac.sit_on(acid,cadeira[0][1])
    # else:
        # ac.say(acid,"Não tem nenhuma cadeira, vou ficar de pé mesmo")
    waiting_points = ac.seek_objs_by_name(acid,20.0,'virtualstage-waiting-point')
    ac.print_dbg('aprendiz','waiting_points=',waiting_points)
    walking_to_point = False
    min_waiting_time = MIN_WAIT_TIME
    walktopt_end_x = None
    walktopt_end_y = None
    walktopt_last_x = None
    walktopt_last_y = None
                    
    walking_to_avatar = False
    walktoav_last_x = None
    walktoav_last_y = None
    walktoav_avid = None
    walktoav_end_x = None
    walktoav_end_y = None
    
    following_avatar = False
    
    while not StopAgent:
        # Wait for some chat message for at most 2 seconds
        msg = ac.wait_chat_msg(acid,'!'+acname,None,2)
        if msg!=None:
            # Is interacting with user at this point, postpone decision to
            # go to other waiting point 
            min_waiting_time = MIN_WAIT_TIME
            resp = processa_msg_usuario(acid,acname,msg)
            if resp!=None:
                #ac.print_dbg('aprendiz',"will say: ",resp)
                # Send the response produced by Dialog Controller to the user
                ac.say(acid,resp)
            
        if walking_to_point:
            # Is walking to some waiting point
            mypos = ac.look_my_position(acid)
            if samePosition(mypos[2],mypos[3],walktopt_end_x,walktopt_end_y):
                # Reached the waiting point position
                walking_to_point = False
                min_waiting_time=MIN_WAIT_TIME
            elif samePosition(walktopt_last_x,walktopt_last_y,mypos[2],mypos[3]):
                # Is not walking for more than 2 seconds, and not reached the final
                # position, teleport to the waiting point position 
                ac.tele_to(acid,float(walktopt_end_x),float(walktopt_end_y))
            else:
                walktopt_last_x=mypos[2]
                walktopt_last_y=mypos[3]

        if walking_to_avatar:
            # Is walking to the position of some avatar
            mypos = ac.look_my_position(acid)
            if samePosition(mypos[2],mypos[3],walktoav_end_x,walktoav_end_y):
                # Reached the avatar position, turn and look to the avatar
                ac.turn_to_avatar(acid,walktoav_avid)
                walking_to_avatar = False
            elif samePosition(walktoav_last_x,walktoav_last_y,mypos[2],mypos[3]):
                # Is not walking for more than 2 seconds, and not reached the final
                # position, only stop considering that is going to some position 
                walking_to_avatar = False
            else:
                walktoav_last_x=mypos[2]
                walktoav_last_y=mypos[3]
                
        starttour_mem = ac.extract_memory(acid,['start-known-places-tour'])
        if starttour_mem!=None:
            # User asked for a tour of known places
            script_tour_lugares_conhecidos(acid,acname)
            ac.say(acid,dc.gen_speak(acid,'voltarPosicaoInicial'))
            ac.tele_to(acid,initial_x,initial_y)
            continue
            
        walktoav_mem = ac.extract_memory(acid,['walking-to-avatar'])
        if walktoav_mem!=None:
            # User asked for actor's avatar to go to his or her position
            mypos = ac.look_my_position(acid)
            walktoav_last_x = mypos[2]
            walktoav_last_y = mypos[3]
            walktoav_avid = walktoav_mem[1]
            walktoav_end_x = walktoav_mem[2]
            walktoav_end_y = walktoav_mem[3]
            walking_to_avatar=True
            continue
            
        followav_mem = ac.remember(acid,['following-avatar'])
        following_avatar =  followav_mem!=None
            
        if following_avatar or walking_to_avatar or walking_to_point:
            # If is following an avatar, or already is walking to some avatar
            # position or some waiting point, do not start to walk to a new
            # waiting point
            continue
            
        if waiting_points!=None and len(waiting_points)>0:
            # There is a list of waiting points
            min_waiting_time-=1
            #ac.print_dbg('aprendiz','min_waiting_time=',min_waiting_time)
            if min_waiting_time<=0 and af.maybe(0.1):
                #ac.print_dbg('aprendiz','will move to other waiting point')
                # After waiting for a minimum period of time in some waiting point,
                # will randomly decide to go to another point with 30% of chance
                mypos = ac.look_my_position(acid)
                next_point = random.choice(waiting_points)
                # It is possible to have randomly selected the same position that
                # the actor's avatar already is
                if not samePosition(mypos[2],mypos[3],next_point[6],next_point[7]):
                    # It is not the same position, actor's avatar will have to walk
                    # to the new waiting point
                    min_waiting_time=MIN_WAIT_TIME
                    walktopt_end_x = next_point[6]
                    walktopt_end_y = next_point[7]
                    walktopt_last_x = mypos[2]
                    walktopt_last_y = mypos[3]
                    walking_to_point = True
                    ac.walk_to(acid,float(walktopt_end_x),float(walktopt_end_y))
                    
    ac.stop_actor(acid)

def start(fstname=None,lstname=None,passw=None,x=None,y=None,simurl=None):
    global StopAgent, ActorFirstName, ActorLastName, ActorID
    # Nome default do ator, caso não tenha sido passado como parâmetro
    if fstname==None:
#        fstname="Ator"
#        lstname="Aprendiz"
#        passw="aprendiz"
        fstname="paciente"
        lstname="jair"
        passw="user"
    # Endereço web default do simulador OpenSim
    if simurl==None:
#        simurl="http://192.168.0.223:9200"
#        simurl="http://localhost:9800"
        simurl="http://localhost:9000"
    # Posição inicial default do avatar controlado pelo ator
    if x==None:
        x=128.0
        y=128.0
    # Registra essas informações em variáveis globais
    StopAgent=False
    ActorFirstName=fstname
    ActorLastName=lstname
    ActorName=fstname+" "+lstname
    # Inicia o novo ator, a função Python que implementa o script principal
    # desse ator se chama script_principal()
    acid=ac.start_actor(fstname,lstname,passw,simurl,None,script_principal,(x,y))
    ActorID = acid
    return acid
        

