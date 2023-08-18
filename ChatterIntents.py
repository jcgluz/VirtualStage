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
#   Module:     ChatterIntents 
#   Purpose:    Exemple of module that implements intents for
#               ChatterActor conversations
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

""" Modulo ChatterIntents - Exemple of module that implements intents
        for ChatterActor conversations """
import random
import clr
import time
import ActorController as ac
import DialogController as dc
import ChatterActor


###########################
# Auxiliary Functions
###########################

def _objDistanceField(obj):
    return float(obj[5])
    
def printObjInfo(obj):
    try:
        objdescr = "I think this is a "+obj[4]+" "+obj[3]
        if obj[2]!=None:
            objdescr+=" called "+obj[2]
        result= objdescr
    except:
        result= None
    return result
    
def maybe(threshold):
    if random.random()>threshold:
        return False
    return True
    
def findNearestObj(acid):
    try:
        nearobjs = ac.seek_objs_by_radius(acid,10.0)
        print(nearobjs)
        nearobjs.sort(key=_objDistanceField)
        return nearobjs[0]
    except:
        return None

###############################
# Do Command Functions
###############################

def doListCommands(acid):
    return "sit, stand, clap, dance, bow, jump, crouch, run, walk, and fly"
    
def doCommand(acid,cmd):
    rval = True
    if cmd=="sit":
        ac.sit(acid)
    elif cmd=="stand":
        ac.stand(acid)
    elif cmd=="clap":
        ac.start_play(acid,'std_anim','clap')
        delay=random.choice([0.5,1.0,1.5,2.0,2.5,3.0])
        time.sleep(delay)
        ac.stop_play(acid,'std_anim','clap') 
    elif cmd=="dance":
        ac.start_play(acid,'std_anim','dance')
        delay=random.choice([0.5,1.0,1.5,2.0,2.5,3.0])
        time.sleep(delay)
        ac.stop_play(acid,'std_anim','dance')
    elif cmd=="bow":
        ac.start_play(acid,'std_anim','bow')
        delay=random.choice([0.5,1.0,1.5,2.0,2.5,3.0])
        time.sleep(delay)
        ac.stop_play(acid,'std_anim','bow')
    elif cmd=="jump":
        ac.jump(acid,'start')
        delay=random.choice([0.5,1.0,1.5,2.0,2.5,3.0])
        time.sleep(delay)
        ac.jump(acid,'stop')
    elif cmd=="crouch":
        ac.crouch(acid,'start')
        delay=random.choice([0.5,1.0,1.5,2.0,2.5,3.0])
        time.sleep(delay)
        ac.crouch(acid,'stop')
    elif cmd=="run":
        ac.fly(acid, 'stop')
        ac.run(acid, 'start')
    elif cmd=="fly":
        ac.run(acid, 'stop')
        ac.fly(acid, 'start')
    elif cmd=="walk":
        ac.run(acid, 'stop')
        ac.fly(acid, 'stop')
    else:
        rval = False
    return rval
               

###############################
# Intention to Action Functions
###############################

def greetings(acid,username,userinput,matches):
    return dc.gen_speak(acid,'iAmOK')
    
def tellName(acid,username,userinput,matches):
    ac.record(acid,['known-user',matches[0]])
    return dc.gen_speak(acid,'howAreYou(NAME)',[matches[0]])

def askObjInfo(acid,username,userinput,matches):
    resp = random.choice(["Well, let me see ...", "I think ...", "I will check ..."])
    obj = findNearestObj(acid)
    if  obj!=None:
        resp += printObjInfo(obj)
    else:
        resp += dc.gen_speak(acid,'iDontKnowThis')
    return resp
        
def askName(acid,username,userinput,matches):
    namevar = ac.remember(acid,['character-name'])
    if namevar==None:
        return dc.gen_speak(acid,'dontRememberMyName')
    return dc.gen_speak(acid,'hello(USER)myNameIs(NAME)',[username,namevar[1]])


def checkName(acid,username,userinput,matches):
    namevar = ac.remember(acid,['character-name'])
    if namevar==None:
        return dc.gen_speak(acid,'dontRememberMyName')
    if namevar[1]==matches[0]:
        return dc.gen_speak(acid,'thisIsMyName')
    return dc.gen_speak(acid,'thisIsNotMyName')


def askCmdsInfo(acid,username,userinput,matches):
    resp = "I can "
    rval=doListCommands(acid)
    if rval!=None:
        return resp+rval+"for you"
    return resp+"do nothing for you"

def askGenderAge(acid,username,userinput,matches):
    gendervar = ac.remember(acid,['character-gender'])
    agevar = ac.remember(acid,['character-age'])
    if gendervar!=None and agevar!=None:
        return dc.gen_speak(acid,'iAm(GENDER)with(AGE)',[gendervar[1], agevar[1]] )
    if agevar!=None:
        return dc.gen_speak(acid,'iHave(AGE)',[agevar[1]] )
    if gendervar!=None:
        return dc.gen_speak(acid,'iAm(GENDER)',[gendervar[1]] )
    return dc.gen_speak(acid,'iDontKnow')

def askGender(acid,username,userinput,matches):
    gendervar = ac.remember(acid,['character-gender'])
    if gendervar!=None:
        return dc.gen_speak(acid,'iAm(GENDER)',[gendervar[1]] )
    return dc.gen_speak(acid,'iDontKnow')

def askAge(acid,username,userinput,matches):
    agevar = ac.remember(acid,['character-age'])
    if agevar!=None:
        return dc.gen_speak(acid,'iHave(AGE)',[agevar[1]] )
    return dc.gen_speak(acid,'iDontKnow')

def askMyInfo(acid,username,userinput,matches):
    resp = random.choice(["I consider myself an intelligent", "I think I am a smart", 
                "I believe I am an intelligent"])
    return resp + random.choice(["VR bot", "artificial actor", "NPC"])

def orderCmd(acid,username,userinput,matches):
    resp = random.choice(["OK","OK I will try to {0}".format(matches[0]), 
                "Your desire to {0} is an order".format(matches[0]), 
                "Trying to {0}".format(matches[0])])
    rval = doCommand(acid,matches[0])
    if rval:
        return resp + " ... done"
    return resp + " ... found some problem"

def lookToObj(acid,username,userinput,matches):
    obj = findNearestObj(acid)
    if obj!=None:
        resp = printObjInfo(obj)
        resp += random.choice([". OK?",". Is this thing?",". This is it?",". It is ok?"])
        dc.set_next_topic(acid,'looking-obj',obj)
    else:
        resp = random.choice(["Can't find this thing","I don't see the object"])
    return resp

def yesReply(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    topcont=dc.get_topic_content(acid)
    if topic=="goto-place" and topcont!=None: 
        resp= random.choice(["OK, I am going to "+str(topcont[0])+","+str(topcont[1]),
                    "Yes, I will walk to "+str(topcont[0])+","+str(topcont[1])])
        ac.walk_to(acid,topcont[0],topcont[1])
    elif topic=="looking-obj": 
        resp= random.choice(["Sure I would found it","This is it","I found it"])
    else:
        resp= random.choice(["May be", "Well...", "Huh", "Why?"])
    return resp
    
def noReply(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    if topic=="goto-place": 
        resp= random.choice(["OK, I don't will go there","OK, I will stay here"])
    elif topic=="looking-obj": 
        resp= random.choice(["Sorry, I don't see it","I don't see this thing",
                "Maybe this thing is not here"])
    else:
        resp= random.choice(["What?", "Why?", "Huh", "May be"])
    return resp
    
def gotoPlace(acid,username,userinput,matches):
    print(matches)
    try:
        xpos=float(matches[0])
        ypos=float(matches[1])
    except:
        return " ... sorry, I can't go there, I can only go to locations defined by X Y numerical coordinates"   
    resp = dc.gen_speak(acid,'mustGoTo(X,Y)',[matches[0], matches[1]] )
    dc.set_next_topic(acid,'goto-place',[xpos,ypos])
    return resp

def goForward(acid,username,userinput,matches):
    if maybe(0.7):
        rval=ac.forward(acid)
    else:
        tim=random.choice([0.5,1.0,1.5])
        rval=ac.forward(acid,tim,'sec')
    if rval:
        resp = random.choice( ["OK", "Yes"])
    else:
        resp = random.choice(["Oops","Oh","Ouch","huh"])
    return resp

def goBack(acid,username,userinput,matches):
    if maybe(0.7):
        rval=ac.backward(acid)
    else:
        tim=random.choice([0.5,1.0,1.5])
        rval=ac.backward(acid,tim,'sec')
    if rval:
        resp = random.choice( ["OK", "Yes"])
    else:
        resp = random.choice(["Oops","Oh","Ouch","huh"])
    return resp

def cameHere(acid,username,userinput,matches):
    userav=ac.look_avatar_with_name(acid,username)
    if userav==None:
        return random.choice(["Oops where are you?","I don't see you"])
    dist = float(userav[3])
    if dist>20.0:
        return random.choice(["You're too far away","Come closer",
                            "you are too far"])
    x = float(userav[4])+1.0 if maybe(0.5) else float(userav[4])-1.0
    y = float(userav[5])+1.0 if maybe(0.5) else float(userav[5])-1.0    
    ac.walk_to(acid,x,y)
    ac.print_dbg('ca','cameHere X=',str(x),' Y=',str(y))
    return random.choice(["I'm coming","I am going","Almost there"])

def followMe(acid,username,userinput,matches):
    rval=ac.follow(acid,username)
    if rval:
        ac.record(acid,['following-avatar',username])
        return random.choice(["OK", "I will follow you", "Going with you"])
    return " ... sorry, cannot follow you"

def leaveAlone(acid,username,userinput,matches):
    followvar = ac.remember(acid,['following-avatar'])
    if followvar!=None:
        ac.stop_follow(acid)
        ac.forget(acid,['following-avatar'])
        resp=random.choice(["OK", "I will stop following you", "I will not follow you"])
    else:
        resp=random.choice(["OK", "Bye", "I will let you alone","See you later", "Good bye"])
    return resp

def goodBye(acid,username,userinput,matches):
    followvar = ac.remember(acid,['following-avatar'])
    if followvar!=None:
        ac.stop_follow(acid)
        ac.forget(acid,['following-avatar'])
        resp=random.choice(["OK", "I will stop following you", "I will not follow you"])
    else:
        resp=random.choice(["OK", "Bye", "I will let you alone","See you later", 
                        "Good bye", "Bye!", "Bye bye", "Adieu"])
    return resp
    
def logOut(acid,username,userinput,matches):
    ChatterActor.stop()
    resp=random.choice(["OK, I will log out", "Bye, I will leave this world"])
    return resp

