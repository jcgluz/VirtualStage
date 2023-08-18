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
#   Module:     CommunicateActions 
#   Purpose:    Actions for communication with other avatars 
#               through VR simulator facilities.
#   Author:     João Carlos Gluz - 2020-2022
#
###############################################################
###############################################################

""" Module CommunicateActions - Actions for communication with 
    other avatars through VR simulator facilities.
    
    Functions:
        wait_msg(acid,msgpatt,timeout)
        wait_inst_msg(acid, srcnam, cntntpatt, timeout)
        wait_chat_msg(acid, srcnam, cntntpatt, timeout)
        wait_chat_inst_msg(acid, srcnam, chattyp, cntntpatt, timeout)
        wait_shout_msg(acid, srcnam, cntntpatt, timeout)
        wait_say_msg(acid, srcnam, cntntpatt, timeout)
        wait_whisper_msg(acid, srcnam, cntntpatt, timeout)
        wait_code_msg(acid, srcnam, codetyp, cntntpatt, timeout)
        wait_group_msg(acid, srcnam, cntntpatt, grpid, timeout)
        wait_session_msg(acid, srcnam, cntntpatt, sessid, timeout)
        seek_msg(acid,msgpatt)
        clear_msgs(acid)
        send_chat_msg(acid, chann, chatyp, msgtxt)
        send_inst_msg(acid, avname, msgtxt, sessid=None)
        send_code_msg(acid, code, avname, msgtxt, sessid)
        send_group_msg(acid, grpid, msgtxt)
        say(acid, msgtxt, chann=None)
        shout(acid, msgtxt, chann=None)
        whisper(acid, msgtxt, chann=None)
        show_menu_for_avatar(acid, avid, menu_msg, menu_opts, menu_chann=-98186)
        show_menu_for_avatar_with_name(acid, avname, menu_msg, menu_opts, menu_chann=-98186)
        input_text_from_avatar(acid, avid, text_msg, menu_chann=-98186)
        input_text_from_avatar_with_name(acid, avname, text_msg, menu_chann=-98186)
        wait_menu_selection(acid, timeout=None)
        wait_input_text(acid, timeout=None)
        play_sound(acid, soundid)        
"""


import ActorController as ac


def wait_msg(acid,msgpatt,timeout):
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
                        then some of these strings must be a substring of the
                        corresponding field;
                        - Otherwise the pattern string must be a substring of 
                        the corresponding field.
                    
        timeout:    if different than None, defines the maximum time in seconds
                    to wait for the message.

    Returns:
     
        On fail, returns None.      
        On success, returns the message as a list of strings.           
    """

    return ac.wait_vrmsg(acid,msgpatt,timeout)

def wait_inst_msg(acid, srcnam, cntntpatt, timeout):
    """ Wait for instant text message sent by some avatar/agent with name srcname
        and with content that match cntntpatt. If timeout is different 
        than None, stop waiting after timeout seconds. 
        
    VR messages are string lists, where index 0 of list corresponds to field 0 
    of message, and so on. For a descripion of types and fields of VR messages
    see the help of wait_message().
         

    Args:

        acid:       str with unique global identifier of actor.
        srcnam:     if different than None, is a string that defines the name 
                    of avatar/agent that sent the message.
        cntntpatt:  if different than None, is a pattern string that must match
                    the content of the message:
                        - If pattern starts with '^' then content must match 
                        pattern from first character;
                        - If pattern ends with '$' then content must match 
                        pattern until last character;
                        - If pattern starts with '!' then pattern cannot be a 
                        match the content;
                        - If pattern is a list of strings separated by '|' then
                        some of these strings must be a substring of content;
                        - Otherwise, the pattern must be a substring of content.
        timeout:    if different than None, defines the maximum time in seconds
                    to wait for the message.

    Returns:
     
        On fail, returns None.      
        On success, returns the message as a list of strings.           
    """

    return ac.wait_vrmsg(acid,['instmsg',srcnam,cntntpatt],timeout)

def wait_chat_msg(acid, srcnam, cntntpatt, timeout):
    """ Wait for a chat message sent by some avatar/agent with name srcnam
        and with content that match cntntpatt. If timeout is different than 
        None, stop waiting after timeout seconds. 
        
    VR messages are string lists, where index 0 of list corresponds to field 0 
    of message, and so on. For a descripion of types and fields of VR messages
    see the help of wait_message().
         

    Args:

        acid:       str with unique global identifier of actor.
        srcnam:     if different than None, is a string that defines the name 
                    of avatar/agent that sent the message.
        cntntpatt:  if different than None, is a pattern string that must match
                    the content of the message:
                        - If pattern starts with '^' then content must match 
                        pattern from first character;
                        - If pattern ends with '$' then content must match 
                        pattern until last character;
                        - If pattern starts with '!' then pattern cannot be a 
                        substring of content;
                        - If pattern is a list of strings separated by '|' then
                        some of these strings must be a substring of content;
                        - Otherwise, the pattern must be a substring of content.
        timeout:    if different than None, defines the maximum time in seconds
                    to wait for the message.

    Returns:
     
        On fail, returns None.      
        On success, returns the message as a list of strings.           
    """

    return ac.wait_vrmsg(acid,['chatmsg',srcnam,cntntpatt],timeout)

def wait_chat_inst_msg(acid, srcnam, cntntpatt, timeout):
    """ Wait for an instant or chat message sent by some avatar/agent
        with name srcnam and with content that match cntntpatt. 
        If timeout is different than None, stop waiting after timeout seconds. 
        
    VR messages are string lists, where index 0 of list corresponds to field 0 
    of message, and so on. For a descripion of types and fields of VR messages
    see the help of wait_message().
         

    Args:

        acid:       str with unique global identifier of actor.
        srcnam:     if different than None, is a string that defines the name 
                    of avatar/agent that sent the message.
        cntntpatt:  if different than None, is a pattern string that must match
                    the content of the message:
                        - If pattern starts with '^' then content must match 
                        pattern from first character;
                        - If pattern ends with '$' then content must match 
                        pattern until last character;
                        - If pattern starts with '!' then pattern cannot be a 
                        substring of content;
                        - If pattern is a list of strings separated by '|' then
                        some of these strings must be a substring of content;
                        - Otherwise, the pattern must be a substring of content.
        timeout:    if different than None, defines the maximum time in seconds
                    to wait for the message.

    Returns:
     
        On fail, returns None.      
        On success, returns the message as a list of strings.           
    """

    return ac.wait_vrmsg(acid,['instmsg|chatmsg',srcnam,cntntpatt],timeout)

def wait_shout_msg(acid, srcnam, cntntpatt, timeout):
    """ Wait for a chat message of type 'shout', i.e., a message 'shouted' in
        chat channel by some avatar/agent with name srcnam  and with content 
        that match cntntpatt. If timeout is different than None, 
        stop waiting after timeout seconds. 
        
    VR messages are string lists, where index 0 of list corresponds to field 0 
    of message, and so on. For a descripion of types and fields of VR messages
    see the help of wait_message().
         

    Args:

        acid:       str with unique global identifier of actor.
        srcnam:     if different than None, is a string that defines the name 
                    of avatar/agent that sent the message.
        cntntpatt:  if different than None, is a pattern string that must match
                    the content of the message:
                        - If pattern starts with '^' then content must match 
                        pattern from first character;
                        - If pattern ends with '$' then content must match 
                        pattern until last character;
                        - If pattern starts with '!' then pattern cannot be a 
                        substring of content;
                        - If pattern is a list of strings separated by '|' then
                        some of these strings must be a substring of content;
                        - Otherwise, the pattern must be a substring of content.
        timeout:    if different than None, defines the maximum time in seconds
                    to wait for the message.

    Returns:
     
        On fail, returns None.      
        On success, returns the message as a list of strings.           
    """

    return ac.wait_vrmsg(acid,['chatmsg',srcnam,cntntpatt,None,None,None,None,None,'shout'],timeout)

def wait_say_msg(acid, srcnam, cntntpatt, timeout):
    """ Wait for a chat message of type 'say', i.e., a message 'said' in
        chat channel by some avatar/agent with name srcnam  and with content 
        that match cntntpatt. If timeout is different than None, 
        stop waiting after timeout seconds. 
        
    VR messages are string lists, where index 0 of list corresponds to field 0 
    of message, and so on. For a descripion of types and fields of VR messages
    see the help of wait_message().
         

    Args:

        acid:       str with unique global identifier of actor.
        srcnam:     if different than None, is a string that defines the name 
                    of avatar/agent that sent the message.
        cntntpatt:  if different than None, is a pattern string that must match
                    the content of the message:
                        - If pattern starts with '^' then content must match 
                        pattern from first character;
                        - If pattern ends with '$' then content must match 
                        pattern until last character;
                        - If pattern starts with '!' then pattern cannot be a 
                        substring of content;
                        - If pattern is a list of strings separated by '|' then
                        some of these strings must be a substring of content;
                        - Otherwise, the pattern must be a substring of content.
        timeout:    if different than None, defines the maximum time in seconds
                    to wait for the message.

    Returns:
     
        On fail, returns None.      
        On success, returns the message as a list of strings.           
    """

    return ac.wait_vrmsg(acid,['chatmsg',srcnam,cntntpatt,None,None,None,None,None,'say'],timeout)

def wait_whisper_msg(acid, srcnam, cntntpatt, timeout):
    """ Wait for a chat message of type 'whisper', i.e., a message 'whispered' in
        chat channel by some avatar/agent with name srcnam  and with content 
        that match cntntpatt. If timeout is different than None, 
        stop waiting after timeout seconds. 
        
    VR messages are string lists, where index 0 of list corresponds to field 0 
    of message, and so on. For a descripion of types and fields of VR messages
    see the help of wait_message().
         

    Args:

        acid:       str with unique global identifier of actor.
        srcnam:     if different than None, is a string that defines the name 
                    of avatar/agent that sent the message.
        cntntpatt:  if different than None, is a pattern string that must match
                    the content of the message:
                        - If pattern starts with '^' then content must match 
                        pattern from first character;
                        - If pattern ends with '$' then content must match 
                        pattern until last character;
                        - If pattern starts with '!' then pattern cannot be a 
                        substring of content;
                        - If pattern is a list of strings separated by '|' then
                        some of these strings must be a substring of content;
                        - Otherwise, the pattern must be a substring of content.
        timeout:    if different than None, defines the maximum time in seconds
                    to wait for the message.

    Returns:
     
        On fail, returns None.      
        On success, returns the message as a list of strings.           
    """

    return ac.wait_vrmsg(acid,['chatmsg',srcnam,cntntpatt,None,None,None,None,None,'whisper'],timeout)

def wait_code_msg(acid, srcnam, codetyp, cntntpatt, timeout):
    """ Wait for a code instant message sent by some avatar/agent with name srcnam,
        with content that match cntntpatt and code type that match codetyp. 
        If timeout is different than None, stop waiting after timeout seconds. 
        
    VR messages are string lists, where index 0 of list corresponds to field 0 
    of message, and so on. For a descripion of types and fields of VR messages
    see the help of wait_message().
         

    Args:

        acid:       str with unique global identifier of actor.
        srcnam:     if different than None, is a string that defines the name 
                    of avatar/agent that sent the message.
        cntntpatt:  if different than None, is a pattern string that must match
                    the content of the message:
                        - If pattern starts with '^' then content must match 
                        pattern from first character;
                        - If pattern ends with '$' then content must match 
                        pattern until last character;
                        - If pattern starts with '!' then pattern cannot be a 
                        substring of content;
                        - If pattern is a list of strings separated by '|' then
                        some of these strings must be a substring of content;
                        - Otherwise, the pattern must be a substring of content.
        codetyp:    if different than None, defines the code type of message.
        timeout:    if different than None, defines the maximum time in seconds
                    to wait for the message.

    Returns:
     
        On fail, returns None.      
        On success, returns the message as a list of strings.           
    """

    return ac.wait_vrmsg(acid,
                ['codemsg',srcnam,cntntpatt,None,None,None,None,None,codetyp,None,None],timeout)

def wait_group_msg(acid, srcnam, cntntpatt, grpid, timeout):
    """ Wait for a group instant message sent by some avatar/agent with name srcnam,
        with content that match cntntpatt and session id that match sessid. If timeout 
        is different than None, stop waiting after timeout seconds. 
        
    VR messages are string lists, where index 0 of list corresponds to field 0 
    of message, and so on. For a descripion of types and fields of VR messages
    see the help of wait_message().
         

    Args:

        acid:       str with unique global identifier of actor.
        srcnam:     if different than None, is a string that defines the name 
                    of avatar/agent that sent the message.
        cntntpatt:  if different than None, is a pattern string that must match
                    the content of the message:
                        - If pattern starts with '^' then content must match 
                        pattern from first character;
                        - If pattern ends with '$' then content must match 
                        pattern until last character;
                        - If pattern starts with '!' then pattern cannot be a 
                        substring of content;
                        - If pattern is a list of strings separated by '|' then
                        some of these strings must be a substring of content;
                        - Otherwise, the pattern must be a substring of content.
        grpid:      if different than None, defines the group id of message.
        timeout:    if different than None, defines the maximum time in seconds
                    to wait for the message.

    Returns:
     
        On fail, returns None.      
        On success, returns the message as a list of strings.           
    """

    return ac.wait_vrmsg(acid,
                ['codemsg',srcnam,cntntpatt,None,None,None,None,None,None,'roup',grpid],timeout)

def wait_session_msg(acid, srcnam, cntntpatt, sessid, timeout):
    """ Wait for a session instant message sent by some avatar/agent with name srcnam,
        with content that match cntntpatt and session id that match sessid. If timeout 
        is different than None, stop waiting after timeout seconds. 
        
    VR messages are string lists, where index 0 of list corresponds to field 0 
    of message, and so on. For a descripion of types and fields of VR messages
    see the help of wait_message().
         

    Args:

        acid:       str with unique global identifier of actor.
        srcnam:     if different than None, is a string that defines the name 
                    of avatar/agent that sent the message.
        cntntpatt:  if different than None, is a pattern string that must match
                    the content of the message:
                        - If pattern starts with '^' then content must match 
                        pattern from first character;
                        - If pattern ends with '$' then content must match 
                        pattern until last character;
                        - If pattern starts with '!' then pattern cannot be a 
                        substring of content;
                        - If pattern is a list of strings separated by '|' then
                        some of these strings must be a substring of content;
                        - Otherwise, the pattern must be a substring of content.
        sessid:     if different than None, defines the session id of message.
        timeout:    if different than None, defines the maximum time in seconds
                    to wait for the message.

    Returns:
     
        On fail, returns None.      
        On success, returns the message as a list of strings.           
    """

    return ac.wait_vrmsg(acid,
                ['codemsg',srcnam,cntntpatt,None,None,None,None,None,None,'session',sessid],timeout)


def seek_msg(acid,msgpatt=None):
    """ Seek for the last message sent by VR simulator that match the msgpatt
        pattern. Do not wait for a message, if there is no message in reception 
        queue, returns None. 
        
    VR messages are string lists, where index 0 of list corresponds to field 0 
    of message, and so on. For a descripion of types and fields of VR messages
    see the help of wait_message().
        
    Args:

        acid:       str with unique global identifier of actor.
        msgpatt:    the message search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
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
                        then some of these strings must be a substring of the 
                        corresponding field;
                        - Otherwise the pattern string must be a substring of 
                        the corresponding field.

    Returns:
     
        On fail, returns None.      
        On success, returns the message as a list of strings.           
    """
    return ac.get_vrmsg(acid,msgpatt)

def clear_msgs(acid):
    """ Clears the message reception queue.         
        
    Args:

        acid:   str with unique global identifier of actor.

    Returns:
     
        On fail, returns False.     
        On success, clears the message reception queue and returns True.            
    """
    return ac.clear_vrmsgs(acid)



def send_chat_msg(acid, chann, chatyp, msgtxt):
    """ Send a chat message to channel chann. If chann is None, sent to
        default public channel (channel 0). 
        
    Args:

        acid:       str with unique global identifier of actor.
        chatyp:     type of chat message, can be: 'say','shout' or 'whisper'
        chann:      number of channel to sent message, 0 is the default
                    public channel
        msgtxt:     text of message

    Returns:
     
        On fail, returns True.      
        On success, send the chat message and returns true.         
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.CommActs.ChatAction(chann,chatyp,msgtxt)
    except:
        return False

def send_inst_msg(acid, avname, msgtxt, sessid=None):
    """ Send a text message to VR agent/avatar avname using the Instant 
        Message service. 
        
    Args:

        acid:       str with unique global identifier of actor.
        avname:     name of VR avatar/agent to receive the message
        msgtxt:     text of message
        sessid:     if the message is a session message, contains
                    the identifier of the session

    Returns:
     
        On fail, returns False.     
        On success, send the text message and returns True.         
    """

    try:
        agent = ac.get_agctl(acid)
        if sessid==None:
            result= agent.CommActs.SendInstMsgAction(avname,msgtxt)
        else:
            result= agent.CommActs.SendInstMsgAction(avname,msgtxt,sessid)
    except:
        result= False
    return result
    
def send_code_msg(acid, code, avname, msgtxt, sessid):
    """ Send a code message to VR agent/avatar avname using the Instant 
        Message service. 
        
    Args:

        acid:       str with unique global identifier of actor.
        code:       str with the code of the message
        avname:     name of VR avatar/agent to receive the message
        msgtxt:     text of message
        sessid:     if the message is a session message, contains
                    the identifier of the session

    Returns:
     
        On fail, returns False.     
        On success, send the text message and returns True.         
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.CommActs.SendCodeMsgAction(code,avname,sessid,msgtxt)
    except:
        return False

def send_group_msg(acid, grpid, msgtxt):
    """ Send a text message to the group of VR agents/avatars identified by
        grpid using the Instant Message service. 
        
    Args:

        acid:       str with unique global identifier of actor.
        grpid:      str with identifier of the group of VR avatars/agents
                    that will receive the message
        msgtxt:     text of message

    Returns:
     
        On fail, returns False.     
        On success, send the text message and returns True.         
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.CommActs.SendMsgToGroupAction(grpid,msgtxt)
    except:
        return False

def say(acid, msgtxt, chann=None):
    """ Send a say chat message to channel chann. If chann is None, sent to
        default public channel (channel 0). 
        
    Args:

        acid:       str with unique global identifier of actor.
        msgtxt:     text of message
        channel:    number of channel to sent message, 0 is the default
                    public channel

    Returns:
     
        On fail, returns True.      
        On success, send the say message and returns true.          
    """

    try:
        agent = ac.get_agctl(acid)
        if chann==None:
            result= agent.CommActs.SayAction(0,msgtxt)
        else:
            result= agent.CommActs.SayAction(chann,msgtxt)
    except:
        result= False
    return result
    
def shout(acid, msgtxt, chann=None):
    """ Send a shout chat message to channel chann. If chann is None, sent to
        default public channel (channel 0). 
        
    Args:

        acid:       str with unique global identifier of actor.
        msgtxt:     text of message
        channel:    number of channel to sent message, 0 is the default
                    public channel

    Returns:
     
        On fail, returns True.      
        On success, send the shout message and returns true.            
    """

    try:
        agent = ac.get_agctl(acid)
        if chann==None:
            result= agent.CommActs.ShoutAction(0,msgtxt)
        else:
            result= agent.CommActs.ShoutAction(chann,msgtxt)
    except:
        result= False
    return result
    
def whisper(acid, msgtxt, chann=None):
    """ Send a whisper chat message to channel chann. If chann is None, sent to
        default public channel (channel 0). 
        
    Args:

        acid:       str with unique global identifier of actor.
        msgtxt:     text of message
        channel:    number of channel to sent message, 0 is the default
                    public channel

    Returns:
     
        On fail, returns True.      
        On success, send the whisper message and returns true.          
    """

    try:
        agent = ac.get_agctl(acid)
        if chann==None:
            result= agent.CommActs.WhisperAction(0,msgtxt)
        else:
            result= agent.CommActs.WhisperAction(chann,msgtxt)
    except:
        result= False
    return result

def show_menu_for_avatar(acid, avid, menu_msg, menu_opts, menu_chann=-98186):
    """ Create and show an user menu for the avatar with id avid. 
        The menu will be presented as a blue rectangle, with 
        menu_msg text displayed at the top of rectangle, followed 
        below by option buttons, one for each option in menu_opt 
        list. Ignore and OK buttons are also displayed in the menu.
    
        User menus are OpenSimulator dialog boxes created by LSL 
        scripts running on prim objects located in the virtual world.
        The option buttons are displayed in the same order of these
        dialog boxes, thus options 0, 1, 2, ... in menu_opt list
        will be displayed as buttons in the following order on the
        dialog box:
            9    10    11
            6    7     8  
            3    4     5
            0    1	   2

        To work, this function needs that a prim object be rezzed on
        the virtual world near do the actor's avatar and that the 
        MenuController script must be installed and running in it. 
 
        The file "MenuController.lsl" located in the menu-controller
        subdirectory of VisualStage implements this script.        
        The prim object that runs this script can be an invisible 
        attachment of the actor's avatar, so it will always be close 
        to the avatar. 
        
        The following example shows how to create the menu and wait
        for the selection:
        
        ...
        import ActorController as ac
        ...
        # Create a menu to select the direction: north or south
        ac.show_menu_for_avatar(acid,other_avatar,"Direction?",["North","South"])
        # Wait 60 seconds for the response of other avatar
        selection = ac.wait_menu_selection(acid,60)       

        The default chat channel used to interact with MenuController 
        script has the number -98186. Is a random number that probably
        will work fine and not cause interference with other scripts 
        running in the virtual world. However, if other VirtualStage 
        actors  are in the same virtual world and also use menus to 
        communicate with users, then the MenuController scripts running 
        on attached objects of these actor's will need to have different 
        chat channel numbers. Modify the MenuController script that is 
        loaded in the attached object changing the MenuChannel variable
        to some appropriate new chat number, and call show_menu_to_avatar() 
        with the last parameter, menu_chann, with this new chat number.
        
    Args:
        acid: str with unique global identifier of actor;
        avid: str with unique identifier of avatar that will see the menu.
        menu_msg: str with menu message to be displayed above menu options.
        menu_opts: list of str with menu options.

    Returns:     
        On fail, returns False. 
        On success, True.
        
    """
    try:
        agent = ac.get_agctl(acid)
        menu_msg="@"+acid+"|"+avid+"|"+menu_msg
        for opt in menu_opts:
            menu_msg += "|"+opt
        print("menu_msg=",menu_msg)
        return agent.CommActs.SayAction(menu_chann,menu_msg)
    except:
        return False


def show_menu_for_avatar_with_name(acid, avname, menu_msg, menu_opts, menu_chann=-98186):
    """ Create an show an user menu for the avatar with name avname. 
        See the help of show_menu_for_avatar() for details.

    Args:
        acid: str with unique global identifier of actor;
        avname: str with name of avatar that will see the menu.
        menu_msg: str with menu message to be displayed above menu options.
        menu_opts: list of str with menu options.

    Returns:     
        On fail, returns False. 
        On success, True.
        
    """
    try:
        agent = ac.get_agctl(acid)
        avinf = ac.look_avatar_with_name(acid,avname)
        if avinf==None:
            return None
        return show_menu_for_avatar(acid,avinf[1],menu_msg,menu_opts,menu_chann)
    except:
        return False


def input_text_from_avatar(acid, avid, text_msg, menu_chann=-98186):
    """ Create and show a text input box for the avatar with id avid. 
        The input will be presented as a blue rectangle, with 
        text_msg text displayed at the top of rectangle. It contains 
        a text box for input, any text that is entered in this box
        will be returned to actor's avatar.
    
        To work, this function needs that a prim object be rezzed on
        the virtual world near do the actor's avatar and that the 
        MenuController script must be installed and running in it. 
 
        The file "MenuController.lsl" located in the menu-controller
        subdirectory of VisualStage implements this script.        
        The prim object that runs this script can be an invisible 
        attachment of the actor's avatar, so it will always be close 
        to the avatar. 
        
        The following example shows how to create an input box and wait
        for the user input:
        
        ...
        import ActorController as ac
        ...
        # Create an input box to enter the name of the user
        ac.input_text_from_avatar(acid,other_avatar,"Enter the name:")
        # Wait 60 seconds for the response of other avatar
        selection = ac.wait_input_text(acid,60)       

        The default chat channel used to interact with MenuController 
        script has the number -98186. Is a random number that probably
        will work fine and not cause interference with other scripts 
        running in the virtual world. However, if other VirtualStage 
        actors  are in the same virtual world and also use menus to 
        communicate with users, then the MenuController scripts running 
        on attached objects of these actor's will need to have different 
        chat channel numbers. Modify the MenuController script that is 
        loaded in the attached object changing the MenuChannel variable
        to some appropriate new chat number, and call show_menu_to_avatar() 
        with the last parameter, menu_chann, with this new chat number.
        
    Args:
        acid: str with unique global identifier of actor;
        avid: str with unique identifier of avatar that will see the menu.
        text_msg: str with text message to be displayed on input box.

    Returns:     
        On fail, returns False. 
        On success, True.
        
    """
    try:
        agent = ac.get_agctl(acid)
        input_msg="&"+acid+"|"+avid+"|"+text_msg
        print("input_msg=",input_msg)
        return agent.CommActs.SayAction(menu_chann,input_msg)
    except:
        return False

def input_text_from_avatar_with_name(acid, avname, text_msg, menu_chann=-98186):
    """ Create an show a text input box for the avatar with name avname. 
        See the help of input_text_from_avatar() for details.

    Args:
        acid: str with unique global identifier of actor;
        avname: str with name of avatar that will see the menu.        
        text_msg: str with text message to be displayed on input box.

    Returns:     
        On fail, returns False. 
        On success, True.
        
    """
    try:
        agent = ac.get_agctl(acid)
        avinf = ac.look_avatar_with_name(acid,avname)
        if avinf==None:
            return None
        return input_text_from_avatar(acid,avinf[1],text_msg,menu_chann)
    except:
        return False


def wait_menu_selection(acid, timeout=None):
    """ Wait for the user to select some menu option and return this
        selection to the caller. If timeout is None, then it wait 
        indefinitely for the response, otherwise timeout defines the 
        max time, in seconds, to wait for the response.
        
        When the user select some option from the user menu, then a
        codemsg is sent to the avatar controlled by the actor. For 
        instance, if the user selected selected "South" then the 
        received codemsg will look like:
        
            ["codemsg", "MenuController", "South", <UUID>, <time>, 
                <X>, <Y>, <Z>, "message_from_object", ...]

        where: "codemsg" field identifies the type of message, 
            "MenuController" field identifies the script/object that 
                sent the message, 
            "South" field contains the content of the message, in this 
                case, contains the option that was selected, 
            <UUID> field contains the id of actor's avatar, 
            <time> is the time when menu was selected, 
            <X>, <Y> and <Z> is the position of the object/script that 
                sent the message and 
            "message_from_object" is the subtype of message, indicating
                it was a codemsg sent by a prim object.      

    Args:
        acid: str with unique global identifier of actor;
        timeout: max time in seconds to wait for the response, if None
            will wait indefinitely.

    Returns:     
        On fail, returns None. 
        On success, returns a string with the selection of the user.
        
    """
    try:
        selmsg=ac.wait_code_msg(acid,'MenuController','message_from_object',None,timeout)
        if selmsg!=None:
            return selmsg[2]
        return None
    except:
        return None

def wait_input_text(acid, timeout=None):
    """ Wait for the user to input some text on the input box and 
        returns this text to the caller. If timeout is None, then it 
        wait indefinitely for the response, otherwise timeout defines 
        the max time, in seconds, to wait for the response. See
        the help of wait_menu_selection() for details.

    Args:
        acid: str with unique global identifier of actor;
        timeout: max time in seconds to wait for the response, if None
            will wait indefinitely.

    Returns:     
        On fail, returns None. 
        On success, returns a string with the selection of the user.
        
    """
    return wait_menu_selection(acid,timeout)



def play_sound(acid, soundid):
    """ Attempt to play a sound.

    Args:

        acid:       str with unique global identifier of actor;
        soundid:    str with unique identifier of asset containing the sound.

    Returns:
     
        On fail, returns False. 
        On success, True.
        
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.PlaySoundAction(soundid)
    except:
        return False

