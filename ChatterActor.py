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
#   Module:     ChatterActor 
#   Purpose:    Exemple chatter actor for VirtualStage
#   Author:     João Carlos Gluz 
#
###############################################################
###############################################################

""" Module ChatterActor - Example Chatter Actor """

import ActorController as ac
import DialogController as dc

stop_chatter_actor=False

def main_script(acid,actorname,x,y):
    global stop_chatter_actor
    ac.enable_print_dbg()
    # Some memories to remember about me 
    ac.record(acid,['character-name','Chatter VRBot'])
    ac.record(acid,['character-age','1'])
    ac.record(acid,['character-gender','robot'])
    # Initialization of dialog manager    
    dc.set_dialog_patterns_file(acid,'ChatterPatterns.json')
    dc.set_dialog_intents_file(acid,'ChatterIntents')
    dc.set_dialog_speeches_file(acid,'ChatterSpeeches.json')
    dc.set_dialog_hear_talk_rules_file(acid,'ChatterChats.json')
    dc.set_dialog_aiml_files(acid,['aiml\\standard-bot\\std-*.aiml'])
    dc.init_dialog_system(acid)
    # Teleporting to initial position x and y
    ac.tele_to(acid,x,y)
    # Saying hello to everyone
    ac.say(acid,'Hello everyone, everything good?')
    # Main interaction loop
    while (not stop_chatter_actor):
        msg = ac.wait_chat_msg(acid,'!'+actorname,None,5) # Wait chat msg not sent by me
        if (msg==None): 
            continue # No message received, return to loop
        resp=None
        try: # Process input by dialog system            
            resp = ac.process_dialog_input(acid,msg[1],msg[2])
        except Exception as e:
            print('Chat error: ',e)
        if resp!=None:
            ac.say(acid,resp) # Something to say, according to dialog system 
    ac.stop_actor(acid)

def stop():
    global stop_chatter_actor
    stop_chatter_actor=True
    
def start():
    return ac.start_actor("Chatter","Actor","actor","http://127.0.0.1:9000", [],
                main_script,(128.0,128.0))
        

