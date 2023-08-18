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
#   Module:     AtorAtendente
#   Purpose:    Exemplo de modulo de controle de um ator 
#               atendente muito simples
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

""" Modulo AtorAtendente - Exemplo de modulo de controle de um 
        ator atendente """

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


def press_enter():
    print('Pressione enter para continuer')
    k=input()


agstop_flag=False

def stop():
    global agstop_flag
    agstop_flag=True
    
def small_delay():
    delay = random.choice( [0.0, 0.5, 1.0, 1.5, 2.0])
    if delay>0.0:
        time.sleep(delay)

def script_principal_atendente(acid,acname,x,y):
    ac.enable_print_dbg()
    ac.print_dbg('atendente','inicializando sistema de dialogo')
    # Informacoes do personagem digital (NPC) controlado pelo ator
    # (podem ser usadas nos dialogos de linguagem natural) 
    ac.record(acid,['actor-creator','João Gluz'])
    ac.record(acid,['actor-name',acname])
    ac.record(acid,['actor-role','atendente'])
    ac.record(acid,['actor-location','Porto Alegre'])
    ac.record(acid,['actor-age','1'])
    ac.record(acid,['actor-gender','R'])
    ac.record(acid,['character-name','Marcos'])
    ac.record(acid,['character-type','atendente'])
    ac.record(acid,['character-nickname','Marcos'])
    ac.record(acid,['character-formal-name','Sr. Marcos'])
    ac.record(acid,['character-gender','M'])
    ac.record(acid,['known-character-name','medica carla'])
    ac.record(acid,['known-character-type','medica carla','medico'])
    ac.record(acid,['known-character-nickname','medica carla','Carla'])
    ac.record(acid,['known-character-formal-name','medica carla','Dra. Carla'])
    ac.record(acid,['known-character-gender','medica carla','F'])
    ac.record(acid,['known-character-name','enfermeiro roberto'])
    ac.record(acid,['known-character-type','enfermeiro roberto','enfermeiro'])
    ac.record(acid,['known-character-nickname','enfermeiro roberto','Roberto'])
    ac.record(acid,['known-character-formal-name','enfermeiro roberto','Enf. Roberto'])
    ac.record(acid,['known-character-gender','enfermeiro roberto','M'])
    ac.record(acid,['known-character-name','paciente jair'])
    ac.record(acid,['known-character-type','paciente jair','paciente'])
    ac.record(acid,['known-character-nickname','paciente jair','seu Jair'])
    ac.record(acid,['known-character-formal-name','paciente jair','seu Jair'])
    ac.record(acid,['known-character-gender','paciente jair','M'])
    ac.record(acid,['known-character-name','paciente sueli'])
    ac.record(acid,['known-character-type','paciente sueli','paciente'])
    ac.record(acid,['known-character-nickname','paciente sueli','dona Sueli'])
    ac.record(acid,['known-character-formal-name','paciente sueli','dona Sueli'])
    ac.record(acid,['known-character-gender','paciente sueli','F'])
    
    dc.set_dialog_patterns_file(acid,'IntencoesAtendente.json')
    dc.set_dialog_intents_file(acid,'IntencoesAtendente')
    dc.set_dialog_speeches_file(acid,'FalasAtendente.json')
    dc.set_dialog_hear_talk_rules_file(acid,'BatePaposAtendente.json')
    dc.init_dialog_system(acid)
    
    time.sleep(1.0)
    ac.print_dbg('atendente','teleportando para posicao inicial (',x,', ',y,')')
    ac.tele_to(acid,x,y)
#    print('Caminhando para posicao de atendimento (',166.0,', ',123.0,')')
#    press_enter()
#    time.sleep(1.0)
#    ac.walk_to(acid,166.0,123.0)
#    time.sleep(12.0)
    time.sleep(5.0)
    ac.print_dbg('atendente','procurando pela cadeira')
    small_delay();
    ac.say(acid,dc.gen_speak(acid,'cadeMinhaCadeira'))
    cadeira = af.find_obj_with_name(acid,'sentar-recepcao-1')
    if cadeira!=None:
        ac.print_dbg('atendente','sentando na cadeira')
        ac.sit_on(acid,cadeira)
    else:
        ac.say(acid,"Ue', aonde colocaram a minha cadeira??")
        time.sleep(2.0)
        ac.say(acid,"Vou ter que atender de pe'!")
    ac.print_dbg('atendente','iniciando atendimento')
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'bomDiaTodos'))
    while(not agstop_flag):
        # Wait for some chat message for at most 2 seconds
        msg = ac.wait_chat_inst_msg(acid,'!'+acname,None,2)
        if (msg==None):
            continue
        ac.print_dbg('atendente','chat msg: ', msg[2],' from: ',msg[1])
        try:
            resp = dc.process_dialog_input(acid,msg[1],msg[2])
        except Exception as e:
            ac.print_dbg('atendente','chat error',e)
            resp=None
        if resp==None:
            resp = dc.gen_speak(acid,'NaoEntendi')
            time.sleep(2.0)
        ac.print_dbg('atendente','resp:',resp)
        if msg[0]=='chatmsg':
            ac.say(acid,resp)
        else:
            ac.send_inst_msg(acid,msg[1],resp)
    ac.stop_actor(acid)

def start():
    # Inicia o novo ator que controlará o avatar: atendente marcos
    # O script principal do ator é definido pela função: script_principal_atendente
    acid=ac.start_actor("atendente","marcos","user","http://127.0.0.1:9800",
                    None, script_principal_atendente,(90.0,73.0))
    return acid
        

