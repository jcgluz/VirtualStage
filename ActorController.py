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
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
#********************************************************
#
#   Module:     ActorController 
#   Purpose:    Main controller module for VR actors
#   Author:     João Carlos Gluz 
#
#
###############################################################
###############################################################

""" ActorController Module - Controller of VirtualStage Actors

    VirtualStage is a platform for the design and development of 
    intelligent virtual actors, capable of controlling digital 
    characters (or "Non-Player" Characters - NPCs) that operate in 
    Virtual Reality (VR) worlds or environments.
    
    VirtualStage offers a complete interface to program and control these 
    digital characters in Python. Using VirtualStage programming interface
    (its API) it is possible to quickly and easily create VirtualStage 
    "actors" able to play and interpret the most diverse types of digital 
    characters in a VR world. 
    
    In a sense, VirtualStage API creates a true "virtual stage" for 
    "virtual actors". Analogously to real actors, a VirtualStage actor 
    must also follow a script to act on the virtual stage and play a 
    digital character. But, in the case of VirtualStage, the scripts
    that guide the actor's performance are scripts in Python. Using the 
    VirtualStage API a Python program can implement several actors that 
    play different digital characters on the virtual stage, each of 
    these actors being executed by a separate thread.
    
    The VirtualStage API is implemented by an extensive library of Python 
    functions that allow the actor to precisely control the performance of 
    its digital character on the stage or virtual world. This API also makes 
    it possible for actors to perform a wide variety of actions on the 
    virtual stage, interact with other characters or avatars, and observe 
    what objects exist and what situations are occurring on the virtual 
    stage. VirtualStage provides a memory to store and recall information 
    that the actor collected during its performance. VirtualStage also
    implements support for Near Natural Language (NNL) conversations and 
    chats between VirtualStage actors and other avatars or characters.
    
    The ActorController module provides functions to manage and control 
    the operation of actors and its scripts. It also provides functions 
    for non VR inter-actor communication, which allow VirtualStage actors 
    intercommunication that do not depends on VR world simulator.
    
    1)  The operation (performance) of some actor is started by calling the
        function:
            start_actor(first_name, last_name, password, vr_server_url, 
                start_loc=None, init_script=None, extra_args=None)
                
        This function tries to connect with an OpenSimulator VR simulator 
        located in vr_server_url web address, logging in the avatar with name 
        and password defined by first_name, last_name and password args. If 
        the login is successful, this avatar will be the digital character 
        or NPC controlled by the VirtualStage actor in the VR world. 
        
        After a successful login, the start_actor() function begins actor's 
        performance by running the initial script of actor (as defined by 
        init_script argument) in a new Python thread.   
        
        If everything goes well, then start_actor() returns the actor's 
        "acid" to the calling function, which is a string with the actor's 
        unique universal ID (UUID) that must be used when calling other 
        functions of VirtualStage API. However, if some problem occur, this 
        function returns None.
        
        All VirtualStage actors begin their performances by running an initial 
        script, which is implemented by the Python function passed to start_actor() 
        as the init_script argument. This argument is a reference a callable Python 
        function with the following arguments:
            acid: a string with the unique global identifier of new actor.
            acname: the name of new actor.
            extra_args: tuple with additional arguments.
       
        For debugging and testing purposes, the init_script argument can be None.
        In this case, the function and the Python thread were this function is
        running will be the initial script and thread of the actor. This tipically 
        is the Python console and by doing this is possible to call VirtualStage 
        API functions directly from the console.
        
        When the initial script function terminates and return, this only finish the
        corresponding Python thread. To logout the avatar controlled by this actor
        from VR world and end actor's operation in this world is necessary to
        call the function:
            stop_actor(acid)
            
        Additional information about VirtualStage actor can be obtained with 
        functions:
            print_version()
            get_version()
            get_actor_id(acname)
            curr_actor_id()
            get_agctl(acid)
            get_actor_name(acid)
            
    2)  In addition to the initial thread that runs the initial script, a 
        VirtualStage actor can also execute other concurrent scripts in 
        separate threads. To do so, the initial script of the actor can 
        call the following function:        
            start_script(acid, script, scriptargs)
        
        This function will start a new actor script running on a new Python 
        thread and return the unique identifier of the script. The script 
        argument references a callable Python function, which implements the 
        script. This function has the following arguments:
            acid: a string with the unique global identifier of new actor.
            acname: the name of new actor.
            scriptargs: tuple with additional args passed to script function.
            
        To wait for the script identified by scriptid to finish is necessary
        to call the function:
            wait_script_finish(acid, scriptid, timeout=None)
        This function uses join() to wait for corresponding thread to terminates.
        
    3)  The ActorController module also implements the inter-actor (non VR) 
        communication functions:
            wait_comm(acid, srcacids, commpatt, timeout)
            send_comm(acid, dstacids, type, content, slots)
            seek_comms(acid, srcacids, commpatt)
            clear_comms(acid)

        These functions can be used to send and receive communications between 
        actors running in the same instance of VirtualStage. Communications
        are messages exchanged between actors that do not pass trough the VR 
        simulator. They are composed by lists of strings with the format:
            [comtype, acid, content, acname, slots]
        where comtype identifies the type (or code) of the comm. message, 
        acid and acname are, respectivelly, the unique ID and the name of the
        actor that sent this message, content is the text of the comm. message 
        and slots is a list of strings with additional comm. message fields
        (slots can be None).
        
    4)  The DialogController Module implements the Near Natural Language (NNL) 
        dialog system, which supports several forms of conversations and chats 
        between VirtualStage actors and its users (i.e., other avatars and 
        characters).
        
    5)  The remaining functions of the VirtualStage API are implemented by the
        VirtualStage Actions Library, which is a library of Python modules that 
        implement actions that the actor can be perform on VR world.
        
        The VirtualStage Actions Library is composed by the following modules:
    
        - Module AppearanceActions: implement actions to view and/or change avatar's 
            appearance

        - Module CommunicateActions: implement actions to communicate with other 
            avatars

        - Module MemoryActions: implement actions to manage actor's memory
        
        - Module ModifyActions: implement actions to modify objects of VR world

        - Module MoveActions: implement actions to move the avatar on VR
        
        - Module ObserveActions: implement actions to observe VR world/environment

        - Module PerceptActions: implement actions to manage actor's perceptions
    
        - Module PositionActions: implement actions to view and/or change avatar's
            positioning/orientation

        - Module PostureActions: implement actions to view and/or change avatar's 
            posture and gestures

        - Module ResourcesActions: implement actions to view and/or modify resources 
            stored in the avatar's inventory

        - Module SocialActions: implement actions for social interaction with 
            other avatars
            
        - Module SystemActions: execute system actions

"""

import sys
import time
import math
import clr
import clr
#from System import String
#from System.Collections import *
import threading
import queue
import re
import os
clr.AddReference("bin\\VRAgents")
from OpenMetaverse import VRAgentManager
from DialogController import *
from AppearanceActions import *
from CommunicateActions import *
from MemoryActions import *
from ModifyActions import *
from MoveActions import *
from ObserveActions import *
from PerceptActions import *
from PositionActions import *
from PostureActions import *
from ResourcesActions import *
from SocialActions import *
from SystemActions import *


VirtualStage_Version = "0.7.0"

#*******************************************
# DEBUG FUNCTIONS

PrDbgEnabled = False
PrDbgFilter = None

def print_dbg(arg1, *args):
    global PrDbgEnabled, PrDbgFilter
    if not PrDbgEnabled:
        return
    if PrDbgFilter!=None and PrDbgFilter!=arg1:
        return
    print('DBG['+arg1+']: ',end='')
    for arg in args:
        print(arg,end='')
    print('')

def print_list_dbg(arg1, arglist):
    global PrDbgEnabled, PrDbgFilter
    if not PrDbgEnabled:
        return
    if PrDbgFilter!=None and PrDbgFilter!=arg1:
        return
    print('DBG['+arg1+']: ',end='')
    print(arglist)

def enable_print_dbg():
    global PrDbgEnabled, PrDbgFilter
    PrDbgEnabled=True
    
def disable_print_dbg():
    global PrDbgEnabled, PrDbgFilter
    PrDbgEnabled=False
 
def set_print_dbg_filter(typ):
    global PrDbgEnabled, PrDbgFilter
    PrDbgFilter=typ
    
#*******************************************
# WAITER DESCRIPTOR OBJECT

class WaiterDescr:
    """__init__() class constructor"""
    def __init__(self):
        self.enabled = False
        self.pattern = None
        self.sources = None
        self.signalpyev = threading.Event()
        self.signalpyev.clear()
        self.obj = None

#*******************************************
# VR ACTOR DESCRIPTOR OBJECT

class ActorDescriptor:
    """__init__() class constructor"""
    def __init__(self, active, id, name, avfstname, avlstname, simurl, agctl, mainthr, evthr):
        self.lock = threading.Lock()
        self.active = active
        self.id = id
        self.name = name
        self.avfstname = avfstname
        self.avlstname = avlstname
        self.simurl = simurl
        self.agctl = agctl
        self.mainthr = mainthr
        self.evthr = evthr
        self.vrmsgs = []
        self.vrevnts = []
        self.acmsgs = []
        self.waiter_vrmsg = WaiterDescr()
        self.waiter_vrevnt = WaiterDescr()
        self.waiter_agmsg = WaiterDescr()
        self.secthrds = []

#*******************************************
# ACTOR DESCRIPTORS TABLE

ActorsTblLock = threading.Lock()
ActorsTbl = {}

#*******************************************
# EVENT/MESSAGE MATCHING FUNCTIONS
#*******************************************

def _compareEvOrMsgStr(patt,val):
#   print_dbg('ac','_compareEvOrMsgStr("',patt.casefold(),'","',val.casefold(),'")')
    if patt.find("|")>0:
        pattlist = patt.split("|")
        for spatt in pattlist:
            if val.casefold().find(spatt.casefold())>=0:
                return True
        return False
    
    if len(patt)<3:
        if patt.casefold()!=val.casefold(): 
            return False
    elif patt[0]=='^' and patt[-1]=='$':
        if patt[1:-1].casefold()!=val.casefold(): 
            return False
    elif patt[0]=='^':
        if not val.casefold().startswith(patt[1:].casefold()):
            return False
    elif patt[-1]=='$':
        if not val.casefold().endswith(patt[:-1].casefold()):
            return False
    elif patt[0]=='!':
        if val.casefold().find(patt[1:].casefold())>=0:
            return False
    elif val.casefold().find(patt.casefold())<0:
        return False
    return True

def _compareEvOrMsgComp(patt,val):
    if type(patt) is str and type(val) is str:
#   if type(patt) is str:
        if not _compareEvOrMsgStr(patt,val):
#           print_dbg('ac','_compareEvOrMsgStr=False')
            return False
    elif type(patt)!=type(val):
        return False
    elif patt!=val:
        return False
    return True

def _compareEvOrMsgElem(patt,val):
    if type(patt) is tuple and type(val) is tuple:
#   if type(patt) is tuple:
        if len(patt)>len(val):
            return False
        for j in range(len(patt)):
            if not _compareEvOrMsgComp(patt[j],val[j]):
                return False
    elif type(patt) is str and type(val) is str:
#   elif type(patt) is str:
        if not _compareEvOrMsgStr(patt,val):
#           print_dbg('ac','_compareEvOrMsgStr=False')
            return False
    elif type(patt)!=type(val):
        return False
    elif patt!=val:
        return False
    return True

def _matchEvOrMsg(patt,val):
    try:
        if patt==None:
            return True
        if type(patt) is not list and type(val) is not list:
#       if type(patt) is not list:
            return _compareEvOrMsgElem(patt,val)
        if type(patt) is not list or type(val) is not list:
            return False
        if len(patt)>len(val):
            return False
        for i in range(len(patt)):
            if patt[i]!=None:
                if not _compareEvOrMsgElem(patt[i],val[i]):
                    return False
        return True
    except:
        return False



#*******************************************
# FUNCTION TO HANDLE VR MESSAGES WAITERS
#*******************************************

def _handleVRMsgsWaiters(acid,newvrmsgs):
    global ActorsTbl, ActorsTblLock
    # First lock the general lock (VRActorsLock), ensuring mutex
    # access to VR actors descriptors table (VRActors dictionary).
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    if actor==None:
        # Actor stopped, ends handle event thread
        return False
    # Then locks the specific lock of the VR actor (VRActor[acid].lock 
    # or actor.lock), which ensures mutex access to this particular VR 
    # actor descriptor.
    actor.lock.acquire()
    # Now the work with VR actor descriptor can be done. When this 
    # work is finished, then the VR actor descriptor lock is unlocked.
    if  not actor.active:
        # Actor inactive (stopping), release locks and ends handle event thread
        actor.lock.release()
        return False
    # If some VR message is being waited, check if there is a message in VR msgs.
    # buffer retrieved from VR actor controller that _matchEvOrMsg the waiting pattern.
    waiting = actor.waiter_vrmsg.enabled
    patt = actor.waiter_vrmsg.pattern
    actor.lock.release()
    found = False
    if waiting and len(newvrmsgs)>0:
        for i,vrmsg in enumerate(newvrmsgs):
            print_list_dbg('ac-vrmsg',vrmsg)
            if _matchEvOrMsg(patt,vrmsg):
                # VR msg. matched pattern, extract msg. from buffer and 
                # indicates found something
                found = True
#               print_dbg('ac','found OK')
                newvrmsgs.pop(i)
#               print_dbg('ac','pop OK')
                break
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    if actor==None:
        # Actor stopped, ends handle event thread
        return False
    actor.lock.acquire()
    if  not actor.active:
        # Actor inactive (stopping), release locks and ends handle event thread
        actor.lock.release()
        return False
    if waiting and found:
        # VR msg. found, signalize waiting Python event and returns found msg.
        actor.waiter_vrmsg.obj = vrmsg
        actor.waiter_vrmsg.enabled = False
        actor.waiter_vrmsg.signalpyev.set()
#       print_dbg('ac','waiting and found OK')
    # Add any other VR msg. retrieved from VR controller to actor's VR msgs. list
    actor.vrmsgs.extend(newvrmsgs)
    actor.lock.release()
    return True

#*******************************************
# FUNCTION TO HANDLE VR EVENTS WAITERS
#*******************************************

def _handleVREventsWaiters(acid,newvrevnts):
    global ActorsTbl, ActorsTblLock
    # Each time event handler thread sleeps, all locks are released
    # So, after the sleep, the locks must be acquired again
    #ActorsTblLock.acquire()
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    #ActorsTblLock.release()
    if actor==None:
        return False
    actor.lock.acquire()
    if  not actor.active:
        # Actor stopped, release locks and ends handle event thread
        actor.lock.release()
        return False
    # If some VR event is being waited, check if there is a event in VR event
    # buffer retrieved from VR actor controller that _matchEvOrMsg the waiting pattern.
    waiting = actor.waiter_vrevnt.enabled
    patt = actor.waiter_vrevnt.pattern
    actor.lock.release()
    found = False
    if waiting and len(newvrevnts)>0:
        for i,vrevnt in enumerate(newvrevnts):
            print_dbg('ac','info: <rcvd vr evnt ',vrevnt,'>')
            if _matchEvOrMsg(patt,vrevnt):
                # VR ev. matched pattern, extract ev. from buffer and indicates
                # found something
                found = True
                newvrevnts.pop(i)
                break
    #ActorsTblLock.acquire()
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    #ActorsTblLock.release()
    if actor==None:
        # Actor stopped, release locks and ends handle event thread
        return False
    actor.lock.acquire()
    if  not actor.active:
        # Actor inactive (stopping), release locks and ends handle event thread
        actor.lock.release()
        return False
    if waiting and found:
        actor.waiter_vrevnt.obj = vrevnt
        actor.waiter_vrevnt.enabled = False
        actor.waiter_vrevnt.signalpyev.set()
    # Add any other VR ev. retrieved from VR controller to actor's VR evnts. list
    actor.vrevnts.extend(newvrevnts)
    actor.lock.release()
    return True


#*******************************************
# FUNCTION TO HANDLE ACTOR MESSAGES WAITERS
#*******************************************

def _handleActorMsgsWaiters(acid):
    global ActorsTbl, ActorsTblLock
    # Each time event handler thread sleeps, all locks are released
    # So, after the sleep, the locks must be acquired again
    #ActorsTblLock.acquire()
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    #ActorsTblLock.release()
    if actor==None:
        # Actor stopped, ends handle event thread
        return False
    actor.lock.acquire()
    if  not actor.active:
        # Actor stopped, release locks and ends handle event thread
        actor.lock.release()
        return False
    # If some actor message is being waited, check if there is a actor message in
    # the actor message buffer of the actor that _matchEvOrMsg the waiting pattern.
    if actor.waiter_agmsg.enabled:
        msgpatt = actor.waiter_agmsg.pattern
        if actor.waiter_agmsg.sources==None:
            # The waiting pattern does not specify any actor or actors
            # as sources of the message, check the remaining elements
            # of the pattern
            for i,msg in enumerate(actor.acmsgs):
                if _matchEvOrMsg(msgpatt,msg):
                    # Ag. msg. matched the pattern, extract msg. from buffer and  
                    # signalize waiting Python event, returning the msg.
                    actor.waiter_agmsg.obj = msg
                    actor.waiter_agmsg.enabled = False
                    actor.acmsgs.pop(i)
                    actor.waiter_agmsg.signalpyev.set()
                    break
        elif type(actor.waiter_agmsg.sources) is not list:
            # The waiting pattern specify a single actor as the source of message
            srcacid=actor.waiter_agmsg.sources
            for i,msg in enumerate(actor.acmsgs):
                if msg[1]!=srcacid:
                    continue
                if _matchEvOrMsg(msgpatt,msg):
                    # Ag. msg. matched source actor. and pattern, extract msg. from  
                    # buffer and signalize waiting Python event, returning the msg.
                    actor.waiter_agmsg.obj = msg
                    actor.waiter_agmsg.enabled = False
                    actor.acmsgs.pop(i)
                    actor.waiter_agmsg.signalpyev.set()
                    break
        else:
            # The waiting pattern specify a list of actors as the sources of msg.
            srcacids=actor.waiter_agmsg.sources
            for i,msg in enumerate(actor.acmsgs):
                if msg[1] not in srcacids:
                    continue
                if _matchEvOrMsg(msgpatt,msg):
                    # Ag. msg. matched source actor. and pattern, extract msg. from  
                    # buffer and signalize waiting Python event, returning the msg.
                    actor.waiter_agmsg.obj = msg
                    actor.waiter_agmsg.enabled = False
                    actor.acmsgs.pop(i)
                    actor.waiter_agmsg.signalpyev.set()
                    break
    actor.lock.release()
    return True


#*******************************************
# THREAD WHICH HANDLES ALL EVENTS FOR THE 
# ACTOR. THAT INCLUDES: VR EVENTS, VR MSGS 
# AND OTHER'S ACTORS COMM MSGS
#*******************************************

def _handleAllEventsThread(acid,acname,agctl):
    global ActorsTbl, ActorsTblLock
    #ActorsTblLock.acquire()
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    #ActorsTblLock.release()
    if actor==None:
        # Actor stopped, ends handle event thread
        return

    #*******************************************************
    # MESSAGES/EVENTS PROCESSING LOOP

    while True:
        # Retrieve last messages and events from VR actor controller
        newvrmsgs = agctl.CommActs.LookForMsgs()
        newvrevnts = agctl.ObsActs.LookForEvents()
        # Handle VR messages waiters
        if not _handleVRMsgsWaiters(acid,newvrmsgs):
            return
        # Sleep a little, to let other threads run.
        time.sleep(0.1)
        # Handle VR events waiters 
        if not _handleVREventsWaiters(acid,newvrevnts):
            return
        # Sleep a little, to let other threads run.
        time.sleep(0.1)
        # Handle actor messages waiters 
        if not _handleActorMsgsWaiters(acid):
            return
        # Sleep a little, to let other threads run.
        time.sleep(0.1)


#*******************************************
# WAIT/GET/CLEAR VR MSGS FUNCTIONS
#*******************************************
# Notes: 
#
# * Send VR Msgs functions are implemented
#   by C# AgentController
#
# * VR Msgs are stored in string lists, where
#   index 0 of list corresponds to field 0 of
#   msg, and so on.
#
# * General fields:
#
#   Field 0 (Typ): type of msg='text'|'chat'|'code'
#   Field 1 (FrmNam): name of source actor/avatar
#   Field 2 (Cont): message content
#   Field 3 (FrmId): ID of source actor/avatar
#   Field 4 (TimStmp): time of recvd msg in fmt YYYY-MM-ddTHH:MM:SS
#   Fields 5,6,7 (PosX,PosY,PosZ): X,Y,Z coords of source actor/avatar
#
# * Fields specific for 'chat' msgs:
#
#   Field 8 (ChatTyp): type of chat msg = 'whisper'|'normal'|'shout'
#   Field 9 (AudLev): audible level of chat msg = 'not'|'barely'|'fully'
#   Field 10 (SrcTyp): source type of chat msg = 'system'|'actor'|'object'
#
# * Fields specific for 'code' msgs:
#
#   Field 8 (CodeTyp): type of code msg
#   Field 9 (GrpSes): indicates if is 'group' or 'session' code msg
#   Field 10 (GrpSesId): group ID, for 'group' code msg or 
#                        session ID, for 'session' code msg
#
#*******************************************

def wait_vrmsg(acid,msgpatt,timeout):
    """ Wait for message sent by VR simulator from other avatars/agents,
        that match the msgpatt search pattern. If timeout is different 
        than None, stop waiting after timeout seconds. 
        
    VR messages are string lists, where index 0 of list corresponds to field 0 
    of message, and so on. The following types of VR events are handled by Virtual
    Stage:
    
    'instmsg' messages from other avatars/agents sent by Instant Message service:

        Field 0 (MsgType): 'instmsg'
        Field 1 (FromAvatarName): name of source agent/avatar
        Field 2 (Content): message content
        Field 3 (FromAvatarId): ID of source agent/avatar
        Field 4 (TimeStamp): time of recvd msg in fmt YYYY-MM-ddTHH:MM:SS
        Fields 5,6,7 (PosX,PosY,PosZ): X,Y,Z coords of source agent/avatar

    'chatmsg' messages from other avatars/agents sent by chat channel:
    
        Field 0 (MsgType): 'chatmsg'
        Field 1 (FromAvatarName): name of source agent/avatar
        Field 2 (Content): message content
        Field 3 (FromAvatarId): ID of source agent/avatar
        Field 4 (TimeStamp): time of recvd msg in fmt YYYY-MM-ddTHH:MM:SS
        Fields 5,6,7 (PosX,PosY,PosZ): X,Y,Z coords of source agent/avatar
        Field 8 (ChatType): type of chat msg = 'whisper'|'normal'|'shout'
        Field 9 (AudioLevel): audible level of chat msg = 'not'|'barely'|'fully'
        Field 10 (SrcType): source type of chat msg = 'system'|'actor'|'object'

    'codemsg' messages from other avatars/agents also sent by Instant Message service:
    
        Field 0 (MsgType): 'codemsg'
        Field 1 (FromAvatarName): name of source agent/avatar
        Field 2 (Content): message content
        Field 3 (FromAvatarId): ID of source agent/avatar
        Field 4 (TimeStamp): time of recvd msg in fmt YYYY-MM-ddTHH:MM:SS
        Fields 5,6,7 (PosX,PosY,PosZ): X,Y,Z coords of source agent/avatar
        Field 8 (CodeTyp): type of code msg
        Field 9 (GroupSession): indicates if is 'group' or 'session' code msg
        Field 10 (GrpSesId): group ID, for 'group' code msg or 
                            session ID, for 'session' code msg   

    Args:
        acid:       str with unique global identifier of actor.
        msgpatt:    the message search pattern: a list of fields, each field 
                    containing a pattern string or the None value. None fields in 
                    message pattern are ignored in the search, pattern strings
                    defined in message pattern must match the corresponding
                    field in the message according to the following rules:
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
                    
        timeout:    if different than None, defines the maximum time in seconds
                    to wait for the message.

    Returns:     
        On fail, returns None.      
        On success, returns the message as a list of strings.           
    """

    global ActorsTbl, ActorsTblLock
    # Check if parameters are ok
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    if actor==None:
        return None
    # Acquire lock
    actor.lock.acquire()
    if actor.waiter_vrmsg.enabled or not actor.active:
        # Already waiting for VR message (or actor is inactive)
        actor.lock.release()
        return None
    # Configure VR message detection mechanism implemented by event handler 
    # thread with VR message pattern
    actor.waiter_vrmsg.pattern=msgpatt
    actor.waiter_vrmsg.signalpyev.clear()
    actor.waiter_vrmsg.enabled=True
    actor.lock.release()
    # Release locks and waits for event handler thread to find the VR message
    found = actor.waiter_vrmsg.signalpyev.wait(timeout)
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    if actor==None:
        return None
    actor.lock.acquire()
    if not actor.active:
        actor.lock.release()
        return None
    if found:
        # The VR Message found by detection mechanism, is stored in obj field
        msg = actor.waiter_vrmsg.obj
    else:
        # Timeout ocurred, no VR message was found
        msg = None
    actor.waiter_vrmsg.signalpyev.clear()
    actor.waiter_vrmsg.enabled=False
    actor.waiter_vrmsg.obj = None
    actor.lock.release()
    # Return what was found
    return msg

def get_vrmsg(acid,msgpatt=None):
    """ Get the last message sent by VR simulator that match the msgpatt search 
        pattern. Do not wait for a message, if there is no message in reception 
        queue, returns None. 
        
    VR messages are string lists, where index 0 of list corresponds to field 0 
    of message, and so on. For a descripion of types and fields of VR messages
    see the help of wait_message().
        
    Args:
        acid:       str with unique global identifier of actor.
        msgpatt:    the message search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    message pattern are ignored in the search, string fields
                    defined in message pattern must be equal to corresponding
                    field in the VR message.

    Returns:     
        On fail, returns None.      
        On success, returns the message as a list of strings.           
    """

    global ActorsTbl, ActorsTblLock
    #ActorsTblLock.acquire()
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    #ActorsTblLock.release()
    if actor==None:
        return None
    actor.lock.acquire()
    if  not actor.active:
        actor.lock.release()
        return None;
    result = None
    for i,msg in enumerate(actor.vrmsgs):
        if _matchEvOrMsg(msgpatt,msg):
            result = msg
            actor.vrmsgs.pop(i)
            break
    actor.lock.release()
    return result

def clear_vrmsgs(acid):
    """ Clears the message reception queue.         
        
    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns False.     
        On success, clears the message reception queue and returns True.            
    """

    global ActorsTbl, ActorsTblLock
    #ActorsTblLock.acquire()
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    #ActorsTblLock.release()
    if actor==None:
        return False
    actor.lock.acquire()
    if  actor.active:
        actor.vrmsgs.clear()
    actor.lock.release()
    return True


#*******************************************
# WAIT/GET/CLEAR VR EVENTS FUNCTIONS
#*******************************************

def wait_vrevnt(acid,evntpatt,timeout):
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

    global ActorsTbl, ActorsTblLock
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    if actor==None:
        return None
    actor.lock.acquire()
    if actor.waiter_vrevnt.enabled or not actor.active:
        # Already waiting for VR event (or actor is inactive)
        actor.lock.release()
        return None
    # Configure VR message detection mechanism implemented by event handler 
    # thread with VR message pattern
    actor.waiter_vrevnt.pattern=evntpatt
    actor.waiter_vrevnt.signalpyev.clear()
    actor.waiter_vrevnt.enabled=True
    actor.lock.release()
    # Release lock and wait for event handler thread to find the VR event
    found =  actor.waiter_vrevnt.signalpyev.wait(timeout)
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    if actor==None:
        return None
    actor.lock.acquire()
    if not actor.active:
        actor.lock.release()
        return None
    if found:
        # VR event found by detection mechanism is stored in obj field
        evnt = actor.waiter_vrevnt.obj
    else:
        # Timeout ocurred, no VR event was found
        evnt = None
    actor.waiter_vrevnt.signalpyev.clear()
    actor.waiter_vrevnt.enabled=False
    actor.waiter_vrevnt.obj = None
    actor.lock.release()
    # Return what was found
    return evnt


def get_vrevnt(acid,evntpatt=None):
    """ Get the last event sent by VR simulator that match the evntpatt search 
        pattern. Do not wait for an event, if there is no event in reception 
        queue, returns None. 
        
    VR events are string lists, where index 0 of list corresponds to field 0 
    of event, and so on. For a descripion of types and fields of VR events
    see the help of wait_event().
        
    Args:
        acid:       str with unique global identifier of actor.
        evntpatt:   the event pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    event pattern are ignored in the search, string fields
                    defined in event pattern must be equal to corresponding
                    field in the event.

    Returns:     
        On fail, returns None.      
        On success, returns the event as a list of strings.         
    """
    global ActorsTbl, ActorsTblLock
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    if actor==None:
        return None
    actor.lock.acquire()
    if  not actor.active:
        actor.lock.release()
        return None;
    result = None
    for i,evnt in enumerate(actor.vrevnts):
        if _matchEvOrMsg(evntpatt,evnt):
            result = evnt
            actor.vrevnts.pop(i)
            break
    actor.lock.release()
    return result

def clear_vrevnts(acid):
    """ Clears the event reception queue.       
        
    Args:
        acid: str with unique global identifier of actor.

    Returns:     
        On fail, returns False.     
        On success, clears the event reception queue and returns True.          
    """

    global ActorsTbl, ActorsTblLock
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    if actor==None:
        return False
    actor.lock.acquire()
    if  actor.active:
        actor.vrevnts.clear()
    actor.lock.release()
    return True


#*******************************************
# SEND/WAIT/SEEK/CLEAR ACTOR COMMS FUNCTIONS
#*******************************************

def send_comm(acid,dstacids,comtype,content,slots):
    """ Send a communication to other actors running in the same
        instance of VirtualStage. 
        
    Communications are messages that can be exchanged between VirtualStage 
    actors but do not pass trough the VR simulator. These communications 
    are formed by lists with the following format:
        [comtype, acid, content, acname, slots]
    where:
        comtype is a string, which defines the type of the communication;
        acid is a string with the unique identifier of source actor that 
            sent the communication
        content is the text of the communication
        acname is a string with the name of source actor that sent the 
            communications
        slots is a list of additional fields, can be None of the empty
            list []

    Args:
        acid:       str with unique global identifier of actor.
        dstacids:   list of strings with unique global identifiers of actor that
                    will receive the communication.
        comtype     str that defines the type of the communication;
        content     str with the text of the communication
        slots       list of strings with an additional list of slots

    Returns:     
        On fail, returns False.     
        On success, returns True.           
    """

    global ActorsTbl, ActorsTblLock
    with ActorsTblLock:
        if not acid in ActorsTbl:
            return False
        acname=ActorsTbl[acid].name
        dstags = []
        if type(dstacids) is not list:
            dstag = ActorsTbl.get(dstacids) 
            dstags.append(dstag)
        else:
            for dstacid in dstacids:
                dstag = ActorsTbl.get(dstacid) 
                dstags.append(dstag)
    acmsg=[comtype,acid,content,acname,slots]
    sent = False
    for dstag in dstags:
        if dstag!=None:
            dstag.lock.acquire()
            if dstag.active:
                dstag.acmsgs.append(acmsg)
                sent = True
            dstag.lock.release()
    return sent


def wait_comm(acid,srcacids,commpatt,timeout):
    """ Wait for communication sent by other actors that match the commpatt 
        search pattern.  These other actor must be running in the same
        instance of VirtualStage. If timeout is different than None, stop 
        waiting after timeout seconds. 
        
    Communications are messages that can be exchanged between VirtualStage 
    actors but do not pass trough the VR simulator. These communications 
    are formed by lists with the following format:
        [comtype, acid, content, acname, slots]
    where:
        comtype is a string, which defines the type of the communication;
        acid is a string with the unique identifier of source actor that 
            sent the communication
        content is the text of the communication
        acname is a string with the name of source actor that sent the 
            communications
        slots is a list of additional fields, can be None of the empty
            list []

    Args:
        acid:       str with unique global identifier of actor.
        srcacids:   list with unique global identifiers of actors that could have
                    sent the communication, 
                    if srcacids is None accept communications from any actors.
        commpatt:   the communication search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    communication pattern are ignored in the search, string fields
                    defined in communication pattern must be equal to corresponding
                    field in the communication, 
                    if commpatt is None accept communication with any content. 
        timeout:    if different than None, defines the maximum time in seconds
                    to wait for the communication.

    Returns:    
        On fail, returns None.      
        On success, returns the communication as a list of strings.         
    """
    global ActorsTbl, ActorsTblLock
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    if actor==None:
        return None
    actor.lock.acquire()
    if actor.waiter_agmsg.enabled or not actor.active:
        # Already waiting for message from other actor (or is inactive)
        actor.lock.release()
        return None
    # Configure actor message detection mechanism implemented by event handler 
    # thread with actor message pattern
    actor.waiter_agmsg.pattern=commpatt
    actor.waiter_agmsg.sources=srcacids
    actor.waiter_agmsg.signalpyev.clear()
    actor.waiter_agmsg.enabled=True
    actor.lock.release()
    # Release lock and wait for event handler thread to find the actor message
    found = actor.waiter_agmsg.signalpyev.wait(timeout)
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    if actor==None:
        return None
    actor.lock.acquire()
    if not actor.active:
        actor.lock.release()
        return None
    if found:
        # Message is stored in obj field by detection mechanism
        acmsg = actor.waiter_agmsg.obj
    else:
        # Timeout ocurred
        acmsg = None
    actor.waiter_agmsg.signalpyev.clear()
    actor.waiter_agmsg.enabled=False
    actor.waiter_agmsg.obj = None
    actor.lock.release()
    # Return what was found
    return acmsg

def seek_comms(acid,srcacids,commpatt):
    """ Seek for the list of last communications received by this actor
        from some actor in srcacids list and that match the commpatt search 
        pattern. Do not wait for communications, if there is no 
        communications in communication reception queue, returns None. 
        
    Communications are messages that can be exchanged between VirtualStage 
    actors but do not pass trough the VR simulator. See the help of
    wait_communication for a description of the format of communictions.
        
    Args:
        acid:       str with unique global identifier of actor.
        srcacids:   list with unique global identifiers of actors that could have
                    sent the communication, 
                    if srcacids is None accept communications from any actors.
        commpatt:   the communication search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    communication pattern are ignored in the search, string fields
                    defined in communication pattern must be equal to corresponding
                    field in the communication, 
                    if commpatt is None accept communication with any content. 

    Returns:     
        On fail, returns None.      
        On success, returns the event as a list of strings.         
    """

    global ActorsTbl, ActorsTblLock
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    if actor==None:
        return None
    actor.lock.acquire()
    if  not actor.active:
        actor.lock.release()
        return None;
    results = []
    if srcacids==None:
        for i,msg in enumerate(actor.acmsgs):
            if _matchEvOrMsg(commpatt,msg):
                results.append(msg)
                actor.acmsgs.pop(i)
    elif type(srcacids) is not list:
        for i,msg in enumerate(actor.acmsgs):
            if msg[1]!=srcacids:
                continue
            if _matchEvOrMsg(commpatt,msg):
                results.append(msg)
                actor.acmsgs.pop(i)
    else:
        for i,msg in enumerate(actor.acmsgs):
            if msg[1] not in srcacids:
                continue
            if _matchEvOrMsg(commpatt,msg):
                results.append(msg)
                actor.acmsgs.pop(i)
    actor.lock.release()
    return results


def clear_comms(acid):
    """ Clears the communications reception queue.      
        
    Args:
        acid: str with unique global identifier of actor.

    Returns:     
        On fail, returns False.     
        On success, clears the communications reception queue and 
        returns True.           
    """
    global ActorsTbl, ActorsTblLock
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    if actor==None:
        return False
    actor.lock.acquire()
    if  actor.active:
        actor.acmsgs.clear()
    actor.lock.release()
    return True



#*******************************************
# START/WAIT ACTOR SCRIPTS FUNCTIONS
#*******************************************

def start_script(acid,script,scriptargs):
    """ Start a new actor script running on a new Python thread. 
        
    Args:
        acid: str with unique global identifier of actor.
        script: callable Python function which implements the script.
        scriptargs: tuple with additional args to be passed to script function.
        
        The script argument is a callable Python which will be called with 
        the following arguments:
            acid: a string with the unique global identifier of new actor.
            acname: the name of new actor.
            scriptargs: additional arguments. 

    Returns:    
        On fail, returns None.      
        On success, starts the script as a new thread and returns the
        identifier of the script.           
    """

    global ActorsTbl, ActorsTblLock
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    if actor==None:
        return -1
    actor.lock.acquire()
    if not actor.active:
        actor.lock.release()
        return -1
    scriptid = len(actor.secthrds)
    acname = get_actor_name(acid)
    secthr = threading.Thread(target=script,
                          name=acname+' sec script thread ' + str(scriptid),
                          args=(acid,acname,scriptargs))
    actor.secthrds.append(secthr)
    actor.lock.release()
    secthr.start()
    return scriptid



def wait_script_finish(acid,scriptid,timeout=None):
    """ Wait the script to finish, uses join() to wait for the corresponding
        thread to terminates. 
        
    Args:
        acid: str with unique global identifier of actor.
        scriptid: identifier of the script.
        timeout: if different than None, defines the maximum time in seconds
                 to wait for the script to finish.

    Returns:     
        On fail, returns False.     
        On success, returns True.           
    """

    global ActorsTbl, ActorsTblLock
    with ActorsTblLock:
        actor = ActorsTbl.get(acid)
    if actor==None:
        return False
    actor.lock.acquire()
    if not actor.active:
        actor.lock.release()
        return False
    if scriptid<0 or scriptid>=len(actor.secthrds):
        actor.lock.release()
        return False
    scriptthr = actor.secthrds[scriptid]
    actor.lock.release()
    scriptthr.join(timeout)
    if (scriptthr.is_alive()):
        return False
    return True
    
#*******************************************
# ACTOR AND VIRTUAL STAGE INFORMATION FUNCTIONS
#*******************************************

def print_version():
    """ Print current version of VirtualStage on console. 
    """
    global VirtualStage_Version
    print("VirtualStage version: ",VirtualStage_Version)
    
def get_version():
    """ Get the current version of VirtualStage. 
    Returns:     
        A string with the current version of VirtualStage.          
    """
    global VirtualStage_Version
    return VirtualStage_Version
    
def get_actor_id(acname):
    """ Get the unique global identifier of the actor with name acname. 
        
    Args:
        acname:     str with name of actor, names of actors are formed 
                    by the first and last name of VR avatar/agent controlled
                    by the actor.

    Returns:     
        On fail, returns None.      
        On success, returns a string with the id of the actor.          
    """

    global ActorsTbl, ActorsTblLock
    with ActorsTblLock:
        for acid,actor in ActorsTbl.items():
            if actor.active and actor.name==acname:
                return acid
    return None


def curr_actor_id():
    """ Returns the unique global identifier of the actor running 
        the current script. 
        
    Returns:     
        On fail, returns None.      
        On success, returns a string with the id of the actor.          
    """

    global ActorsTbl, ActorsTblLock
    thrid = threading.get_ident()
    with ActorsTblLock:
        for actor in ActorsTbl:
            if actor.mainthr.ident==thrid or actor.evthr.ident==thrid:
                acid = actor.acid
                return acid
            for scriptthr in actor.secthrds:
                if scriptthr.ident==thrid:
                    acid = actor.acid
                    return acid
    return None
    
def get_agctl(acid):
    """ Get the C# module that controls the VR agent/avatar.        

    Args:
        acid:   str with unique global identifier of actor.

    Returns:    
        On fail, returns None.      
        On success, returns the C# module that controls the VR agent/avatar.            
    """

    global ActorsTbl, ActorsTblLock
    #ActorsTblLock.acquire()
    with ActorsTblLock:
        if acid in ActorsTbl.keys():
            agctl = ActorsTbl[acid].agctl
        else:
            agctl=None
    #ActorsTblLock.release()
    return agctl
    
def get_actor_name(acid):
    """ Get the name of the actor with acid identifier, names of actors are formed 
        by the first and last name of VR avatar/agent controlled by the actor.      

    Args:
        acid:   str with unique global identifier of actor.

    Returns:    
        On fail, returns None.      
        On success, returns the name of the actor.          
    """
    with ActorsTblLock:
        if acid in ActorsTbl.keys():
            acname = ActorsTbl[acid].name
        else:
            acname=None
    return acname


#*******************************************
# START/STOP ACTORS FUNCTIONS
#*******************************************

def stop_actor(acid):
    """ Stop the execution of this actor: log out the VR avatar/agent 
        controlled by this actor from VR simulator, disconnect
        the actor from VR simulator and stop main script of actor.      

    Args:
        acid:   str with unique global identifier of actor.

    Returns:    
        On fail, returns False.     
        On success, returns True.           
    """
    global ActorsTbl, ActorsTblLock
    with ActorsTblLock:
        if not acid in ActorsTbl:
            print_dbg('ac','stop_actor() failed - actor:'+acid+' is not on VR actors list')
            return True
        actor = ActorsTbl[acid]
    actor.lock.acquire()
    if not actor.active:
        actor.lock.release()
        print_dbg('ac','stop_actor() failed - actor:'+acid+' is not active')
        return True
    for scriptthr in actor.secthrds:
        if scriptthr.is_alive():
            actor.lock.release()
            print_dbg('ac','stop_actor() failed - actor:'+acid+' has running sec scripts')
            return False
    print_dbg('ac','stop_actor() - will request event thread to stop')
    actor.active = False
    evthr = actor.evthr
    actor.lock.release()
    evthr.join();
    actor.lock.acquire()
    print_dbg('ac','stop_actor() - event thread stopped')
    with ActorsTblLock:
        ActorsTbl.pop(acid,None)
    # avp = Avatars.AvatarPortal()
    # avpi = avp.Instance
    vrmng = VRAgentManager().Instance
    #avpi = vrmng.Instance  
    #avpi = AvatarPortal().Instance 
    print_dbg('ac','stop_actor() - will logout actor: '+acid+' from VR')
    vrmng.vragent_logout(acid)
    print_dbg('ac','stop_actor() - exited VR')
    return True

def start_actor(first_name, last_name, password, vr_server_url, 
                start_loc=None, init_script=None, extra_args=None):
    """ Start a new actor: first connect the actor with the OpenSim VR simulator 
        and tries to log in the VR avatar controlled by this actor into the 
        simulator, then starts main script of actor in a new thread. If successful 
        this functions returns a string with the unique universal ID (UUID) of
        the new actor (is the same UUID of VR avatar, which is returned by the 
        login process). 
        
    Args:
        first_name: first name of VR avatar controlled by the new actor
        last_name: last name of VR avatar controlled by the new actor
        password: login password of VR avatar controlled by the new actor
        vr_server_url: the URL (web address) of OpenSim VR simulator
        
        start_loc: optional arg, if different than None, defines the starting 
            location of avatar/NPC using format:
                [region_name, x_pos, y_pos, z_pos]
            
        init_script: callable Python function which implements the initial 
            script of actor.
            
        extra_args: optional tuple with additional args to be passed to 
            init_script function.
            
        The init_script argument can be None, in this case the current 
        thread (tipically the Python console) will be the main thread of actor.
        Otherwise, init_script must be a reference to a callable Python function 
        that will be called with the following arguments:
            acid: a string with the unique global identifier of new actor.
            acname: the name of new actor.
            extra_args: tuple with additional arguments.
            
        In OpenSim VR Simulators, VR avatars are identified by a first and a 
        last name (first_name and last_name arguments). 
        
        The name of the new actor in VirtualStage will be a full name formed 
        by the concatenation of first and last names, with a blank space in 
        middle: 
            acname = first_name+' '+last_name.
                
    Returns:     
        On fail, returns None.      
        On success, returns a string with unique global ID (an UUID) of new 
        actor. This UUID is the same UUID of VR avatar returned by the login
        process.
            
    """
    global ActorsTbl, ActorsTblLock
    vrmng = VRAgentManager().Instance
    acname=first_name+' '+last_name
    print_dbg('ac','start_actor() - will login actor in VR with avatar name: '+acname)
#    if start_location==None:
#        acid = vrmng.vragent_login([first_name,last_name,password,server_url])
#    else:
#        acid = vrmng.vragent_login([first_name,last_name,password,start_location,server_url])
    if start_loc==None:
        start_loc=[]
    acid = vrmng.vragent_login([first_name,last_name,password,vr_server_url]+start_loc)
    if acid==None:
        print_dbg('ac','start_actor() - login returned None')
        return None
    print_dbg('ac','start_actor() - login returned actor id:'+acid)
    agctl = vrmng.get_vragent_controller(acid)
    if agctl==None:
        print_dbg('ac','start_actor() - cannot get avatar controller')
        return None
    agctl.SysActs.SetLogLevelAction('none')
    with ActorsTblLock:
        if acid in ActorsTbl:
            print_dbg('ac','start_actor() - actor already in VR actors list')
            return None
    print_dbg('ac','start_actor() - will register actor in VR actors list')
    if extra_args!=None:
        scriptargs=(acid,acname)+extra_args
    else:
        scriptargs=(acid,acname)      
    evthrname = acname + ' events handler thread'
    mainthrname = acname + ' initial script thread'
    evthr = threading.Thread(target=_handleAllEventsThread, name=evthrname,
                          args=(acid,acname,agctl))
    if init_script!=None:
        mainthr = threading.Thread(target=init_script, name=mainthrname, args=scriptargs)
    else:
        mainthr = threading.get_ident()
    with ActorsTblLock:
        ActorsTbl[acid] = ActorDescriptor(True,acid,acname,first_name,last_name,vr_server_url,
                            agctl,mainthr,evthr)
    print_dbg('ac','start_actor() - registered actor id: '+acid+' in VR actors list')
    print_dbg('ac','start_actor() - will start event thread')
    evthr.start()
    print_dbg('ac','start_actor() - event thread started')
    if init_script!=None:
        print_dbg('ac','start_actor() - will start main script thread')
        mainthr.start()
        print_dbg('ac','start_actor() - main script thread started')
    else:
        print_dbg('ac','start_actor() - using current thread as main script thread')
    return acid


