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
#   Module:     DialogController 
#   Purpose:    Main controller module for VirtualStage Near 
#               Natural Language (NNL) dialog system
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

""" DialogController Module - Controller of VirtualStage Near 
    Natural Language (NNL) dialog system.
    
    The NNL dialog system provides several dialog processors to 
    handle the interactions or conversations between the actor 
    and the users (the other avatars or characters):
    
    a)  NNL main intent processor: this processor is oriented to 
        find user intents. It is formed by a token pattern matcher 
        that tries to identify an intention on the input string, 
        and execute its corresponding intent function, which is 
        a Python function that implements the actor's handling
        of this user intention. 
        
    b)  Hear-talk rules processor: the NNL dialog system also 
        handle "hear and talk" production rules that map token 
        patterns found on input text into output text messages. 
        When no intent is found on the user input and hear-talk 
        rules are configured, then these rules are searched and, 
        if the 'hear' part of some rule match the input text, then 
        the output of this rule (the 'talk' part) is sent to user.
        
    c)  AIML rules interpreter: NNL dialog system can also work 
        with AIML rules to process user input. An AIML interpreter 
        can be configured to work integrated with this system. If the 
        AIML interpreter is configured and and no intention is found 
        on user input neither an hear-talk rule can be applied to 
        this input, then the AIML intepreter will process the input 
        text. Any response provided by it is returned to user.
    
    The NNL dialog system also provides several additional services
    to help handling of dialog interactions:
    
    1)  Discussion topic service: this service can be used by intent 
        functions to keep track of the topic being discussed in dialogs 
        with user. 
        
    2)  Input mode service: this service is used to select particular 
        intentions depending on the current input mode.
        
    3)  Intent recording service: this service can be used to record 
        intent functions executed by the actor during the processing 
        of user inputs.
        
    4)  Standard speeches service: the NNL dialog system provides a 
        service that can be used by intent function to generate standard 
        speeches in some particular language.
        
    5)  Hear-talk manager service: the NNL dialog system provides a 
        service to dynamically manage hear-talk rules.
        
    6)  AIML interface service: the NNL dialog system provides an 
        interface service that allows the actor to get and set the
        values of AIML global bot properties and global predicates.
    
    7)  Configuration and initialization of NNL dialog system:
    
        To start using NNL dialog system, first its processors must be 
        confiugured by functions:
            set_dialog_patterns_file(acid, pattsfile)
            set_dialog_intents_file(acid, intentsfile)
            set_dialog_speeches_file(acid, speechesfile)
            set_dialog_hear_talk_rules_file(acid, prodrulesfile)
            set_dialog_aiml_files(acid, aimlfiles)
        
        Then the dialog system must be initialized calling the function:
            init_dialog_system(acid)
        
    8)  Input processing:
    
        The user input is processed by NNL dialog system by calling 
        the function:
            process_dialog_input(acid, username, userinput)
        where acid arg. is the unique ID of the VirtualStage actor, 
        username arg. is the name of the user that sent the input and 
        userinput arg. is a string with the text entered by the user.
        
        The user is some other avatar in the VR world, thus username 
        is the full name of this avatar in the VR. The userinput text 
        usually is a chat or instant message sent to the actor's avatar 
        by user's avatar.
        
        If some NNL dialog processor was succesful in handling the
        input, then this function returns an string of text that
        can be sent back to user. Otherwise, this function returns 
        None.
    
    List of NNL dialog system functions organized by service:
    
        Dialog system configuration and initialization:
            set_dialog_patterns_file(acid, pattsfile)
            set_dialog_intents_file(acid, intentsfile)
            set_dialog_speeches_file(acid, speechesfile)
            set_dialog_hear_talk_rules_file(acid, prodrulesfile)
            set_dialog_aiml_files(acid, aimlfiles)
            init_dialog_system(acid)
        
        Input processing:
            process_dialog_input(acid,username,userinput)
        
        Discussion topic service: 
            get_topic_name(acid)
            get_topic_content(acid)
            set_topic(acid,name,content=None)
            set_next_topic(acid,name,content=None)
            keep_topic(acid)
        
        Input mode service:
            get_mode(acid)
            set_mode(acid,mode)
            keep_mode(acid)
            
        Intent recording service:
            start_recording_intents(acid)
            restart_recording_intents(acid,index)
            stop_recording_intents(acid)
            is_recording_intents(acid)
            
        Hear-talk rules management service:
            save_hear_talk_rules(acid,prodsfile)
            add_hear_talk_rule(acid,hear,talk)
            
        Standard speeches service:
            gen_speak(acid,speechid,paramlist=[],defaultphrase="")
            get_speaks(acid,speechid)
            
        NNL dialog system information:
            get_last_dlg_proc(acid)
            get_intent_list(acid,searchstr=None)
            get_patterns_intent_list(acid,intention)
            
        AIML interface service:
            aiml_set_bot_prop(acid, name, value)
            aiml_set_pred(acid, name, value)
            aiml_get_bot_prop(acid, name)
            aiml_get_pred(acid, name)

"""

import json
import re
import sys
import threading
import itertools
import importlib
import nltk
import aiml
import random
import time
import ActorController as ac

#*******************************************
# GLOBAL VARIABLES WITH THE CONFIGURATION
# OF DIALOG PROCESSORS AND SERVICES
#*******************************************

#DTLock = threading.Lock()
IntentsPatternsFile = {}
IntentsFunctionsFile = {}
SpeechesFile = {}
ProdRulesFile = {}
AIMLFiles = {}

#*******************************************
# GLOBAL DESCRIPTOR TABLES FOR DIALOG PROCESSORS
#*******************************************

IntentsPatternsTbl = {}
IntentsFunctionsTbl = {}
ProdRulesTbl = {}
AIMLKrnlTbl = {}

#*******************************************
# GLOBAL DESCRIPTOR TABLES FOR DIALOG SERVICES
#*******************************************

SpeechesTbl = {}
LastDlgProc = {}
CurrDiscussTopic = {}
#DlgTopicName = {}
#DlgTopicContent = {}
#NextDlgTopicName = {}
#NextDlgTopicContent = {}
CurrInputMode = {}
# DlgMode = {}
# KeepDlgMode = {}
RecIntents = {}
ReplaceRecIntent = {}

#*******************************************
# AUXILIARY FUNCTIONS USED TO PROCESS AND
# EXECUTE SEARCHES WITH TOKEN PATTERNS 
#*******************************************

######################################################################
#
# _toTokenString(tklist)
# 
# A function that converts a list of tokens produced by some tokenizer 
# to a "token string", which is a string where tokens are marked with 
# angle brackets. The function assumes that each token in the input 
# token list is a string.
# Example:
#   >>> import VRAgentInteractins as inter
#   >>> tklist=['the','quick','brown','fox','jumps','over','the','lazy','dog']
#   >>> inter._toTokenString(tklist)
#   '<the><quick><brown><fox><jumps><over><the><lazy><dog>' 
#
def _toTokenString(tklist):
    tkstr = "".join("<" + wrd + ">" for wrd in tklist)
#   ac.print_dbg('dc','tklist=',tklist)
#   ac.print_dbg('dc','tkstr=',tkstr)
    return tkstr

def _preprocessTokenRegExp(tkregexp):
    # Preprocess the token regular expression
    if tkregexp[0]!='^' and tkregexp[-1]!='$':
        if tkregexp[0]!='_':
            tkregexp = '^'+tkregexp
        else:
            tkregexp = tkregexp[1:]
        if tkregexp[-1]!='_':
            tkregexp = tkregexp+'$'
        else:
            tkregexp = tkregexp[0:-1]
    regexp = re.sub(r"\s", "", tkregexp)
    regexp = re.sub(r"<", "(?:<(?:", regexp)
    regexp = re.sub(r">", ")>)", regexp)
    regexp = re.sub(r"(?<!\\)\.", "[^>]", regexp)
    regexp = re.sub(r"__", "><", regexp)
    
    #ac.print_dbg('dc',"patt tkregexp= ",tkregexp)
    #ac.print_dbg('dc',"patt rawregexp=",regexp)
    return regexp

def _rawTokenMatcher(acid, tkstr, regexp):
    # First replace memory vars enclosed in '%' by their values
    varnames = re.findall("%([a-zA-Z][-a-zA-Z0-9]*)%",regexp)
    for var in varnames:
        val = ac.remember(acid,[var])
        if val!=None and val[1]!=None:
            # Convert memory var value to lowercase, remove leading/trailing spaces, 
            # remove internal extra spaces and enclose each word in '(?:<(' and ')>)'          
            regexp.replace('%'+var+'%',
                str(val[1]).casefold().strip().replace(' ',
                    ')>)(?:<(').replace('(?:<()>)','')+'>')
        else:
            # Cannot find memory var or var has no value, remove var from regexp
            regexp.replace('(?:<(%'+var+'%)>)','')       
    # Token regular expression must already be preprocessed
    # to perform the search
    tkhits = re.findall(regexp, tkstr)
    #ac.print_dbg('dc',"tkhits=",tkhits)
    # Sanity check and postprocessing
    if tkhits==None or tkhits==[]:
        # Pattern not matched with token string 
        return []
    # Pattern matched with token string
    if tkhits[0]==tkstr and not (regexp.startswith("^((") or regexp.startswith("((")):
        # Pattern do not starts with some string capturing group and tkhits[0], the 
        # resulting string from re.findall(), is identical to tkstr. This shows that 
        # there is a matching but no string was captured, thus returns a list with one 
        # empty string to indicate that a match happened but no string was captured
        return ['']
    # Pattern matched with string and have string capturing groups, 
    # so tkhits is the list of token strings captured by the pattern
    # Convert token strings captured to untokened strings
    hits = []
    for tkhit in tkhits:
        if isinstance(tkhit,tuple):
            strlst = []
            for tkhitstr in tkhit:
                if tkhitstr.startswith("<") and tkhitstr.endswith(">"):
                    strlst.append(tkhitstr[1:-1].replace("><"," "))
                else:
                    strlst.append('')
            hits.append(strlst)
        elif tkhit.startswith("<") and tkhit.endswith(">"):
            hits.append(tkhit[1:-1].replace("><"," "))
        else:
            hits.append('')
    return hits


#####################################################################
#
# _tokenMatcher(tkstr,tkregexp)
# Find instances of token regular expression in the token string.
# The token string tkstr is a string where each token is surrounded by
# angle brackets '<' and '>'. 
# The _tokenMatcher() function uses re.findall() method to implement the 
# regexp matching. However the token regular expression tkregexp passed 
# to re.findall() is modified to treat angle brackets as non-capturing 
# parentheses, in addition to matching the token boundaries; and to 
# have ``'.'`` not _tokenMatcher the angle brackets.
# Examples of use:
#   >>> import DialogController as dlg
#   >>> txt = "<a><text><with><eleven><tokens><or><a><slogan><with><no><sense>"
#   >>> dlg._tokenMatcher(txt,"<.*><.*><with>")
#   ['a text with', 'a slogan with']
#   >>> dlg._tokenMatcher(txt,"<a>(<.*>)<with>")
#   ['text', 'slogan']
#   >>> dlg._tokenMatcher(txt,"<t.*>{2,}")
#   ['eleven tokens']
#   >>> dlg._tokenMatcher(txt,"^<.*><.*><with>")
#   ['a text with']
#   >>> dlg._tokenMatcher(txt,"<.*><.*><with><.*><.*>")
#   ['a text with eleven tokens', 'a slogan with no sense']
#   >>> dlg._tokenMatcher(txt,"<.*><.*><with><.*><.*>$")
#   ['a slogan with no sense']
#   >>> dlg._tokenMatcher(txt,"(<t.*>)")
#   ['text', 'tokens']
#   >>> dlg._tokenMatcher(txt,"(<t.*>)<.*>*(<t.*>)<.*>*(<s.*>)")
#   [['text', 'tokens', 'sense']]
#   >>> dlg._tokenMatcher(txt,'<with>(<.*>)<.*>*<with>(<.*>)')
#   [['eleven', 'no']]
# This function is based on findall() method of TokenSearcher class of
# nltk.Text module. However the original findall() method cannot handle 
# multiple group matches, i.e., the following token regexp:
#   '<with>(<.*>)<.*>*<with>(<.*>)'
# which should return [['eleven', 'no']] when applied to txt variable define 
# in the example above, will cause an error in findall() method of nltk's 
# TokenSearcher class.
# The function _tokenMatcher() defined below corrects this error.
#

def _tokenMatcher(acid, tkstr, tkregexp):
    # preprocess the token regular expression
    regexp = _preprocessTokenRegExp(tkregexp)
    
    # perform the search
    hits = _rawTokenMatcher(acid, tkstr, regexp)
    return hits

#*******************************************
# OBJECT REPRESENTATION OF INTENT PATTERNS
#*******************************************

class IntentPatterns:
    """__init__() class constructor"""
    def __init__(self,origintent,intentfun,users,modes,patterns,origpatterns):
        self.origintent = origintent
        self.intentfun = intentfun
        self.users = users
        self.modes = modes
        self.patterns = patterns
        self.origpatterns = origpatterns

#*******************************************
# AUXILIARY FUNCTIONS USED TO LOAD INTENT 
# PATTERNS, HEAR-TALK PROD. RULES AND
# STANDARD SPEECHES
#*******************************************

def _splitIntent(input):
    #Delete text between '(' and ')'
    #if ('(' in input) and (')' in input):
    #    input = input.split('(')[0]+input.split(')')[1]
    intus_mod = input.split('@')
    int_us = intus_mod[0].split(':')
    if len(int_us)>1:
        int_us = [int_us[0], int_us[1].strip('][').split(',')]
    else:
        int_us = [int_us[0], None]
    if len(intus_mod)>1:
        mod = [intus_mod[1].strip('][').split(',')] 
    else:
        mod = [None]
    return int_us + mod


def _asIntentPatterns(jsdict):
    #ac.print_dbg('dc',"jsdict=",jsdict)
    ipatlist=list(jsdict.items())
    intent = ipatlist[0][0]
    splitint = _splitIntent(intent)
    patlist = ipatlist[0][1]
    procpatlist=[]
    for pat in patlist:
        procpatlist.append(_preprocessTokenRegExp(pat))        
    return IntentPatterns(intent,splitint[0],splitint[1],splitint[2],procpatlist,patlist)
    
def _loadPatterns(pattfile):
    try: 
        with open(pattfile, encoding='utf-8') as pf:
            patts = json.load(pf, object_hook=_asIntentPatterns)
    except Exception as error:
        ac.print_dbg('dc','Patterns to intents file read error ',error)
        return None
    return patts

def _loadProdRules(prodsfile):
    try: 
        with open(prodsfile, encoding='utf-8') as pf:
            prods = json.load(pf)
    except Exception as error:
        ac.print_dbg('dc','Prod rules file read error ', error)
        prods = None
    return prods

def _loadSpeeches(speechesfile):
    try: 
        with open(speechesfile, encoding='utf-8') as sf:
            speeches = json.load(sf)
    except Exception as error:
        ac.print_dbg('dc','Speeches file read error ', error)
        speeches = None
    return speeches

#*******************************************
# AUXILIARY FUNCTIONS USED TO FIND AND 
# EXECUTE INTENT FUNCTIONS AND PROCESS
# HEAR-TALK PRODUCTION RULES
#*******************************************
    
    
def _findIntent(acid,username,userinput):
    #DTLock.acquire()
    global IntentsPatternsTbl, IntentsFunctionsTbl   
    dlgpatts = IntentsPatternsTbl[acid]
    tkstrinput = _toTokenString( nltk.word_tokenize(userinput.lower()) )
    for intent in dlgpatts:
        #ac.print_dbg('dc','will check patterns')
        #intfunmod=intpatts.intent.split('@')
        #ac.print_dbg('dc','intfunmod=',intfunmod)
        #intentfun = intfunmod[0]
        if intent.users!=None and not (username in intent.users):
            # The intention is specific for some set of users, but current
            # user does not belong to this set, so continue the search 
            continue       
        #ac.print_dbg('dc','intentfun=',intentfun,' intentmode=',intentmode)
        if intent.modes!=None and not (get_mode(acid) in intent.modes):
            # The intention is specific for some mode or modes, but current
            # dialog mode is not one of these modes, so continue the search 
            continue
        #ac.print_dbg('dc','checking intent: ',intent.intentfun)
        #for patt in intent.patterns:
        for patt, origpatt in zip(intent.patterns, intent.origpatterns):
            #ac.print_dbg('dc','input: "', tkstrinput,'"')
            #ac.print_dbg('dc','origpatt: "',origpatt,'"')
            #ac.print_dbg('dc','patt: "',patt,'"')
            try:
                hits = _rawTokenMatcher(acid,tkstrinput,patt)
            except:
                ac.print_dbg('dc','Error checking intent: ',intent.intentfun,' with input: "', tkstrinput,'"')
                ac.print_dbg('dc','  orig patt: "',origpatt,'"')
                ac.print_dbg('dc','  raw  patt: "',patt,'"')
                continue
            if len(hits)>0:
                matches = hits[0] if isinstance(hits[0],list) else [hits[0]]
                #DTLock.release()
                #ac.print_dbg('dc','matched intent: ',intent.intentfun,' hits: ',matches)
                return (intent.intentfun, matches)    
    #DTLock.release()
    return None

def _execIntentAction(acid,username,userinput,intent,matches):
    #DTLock.acquire()
    global IntentsPatternsTbl, IntentsFunctionsTbl   
    actsmodule = IntentsFunctionsTbl[acid]
    try:
        actFunction = getattr(actsmodule,intent)
        result = actFunction(acid,username,userinput,matches)
    except Exception as error:
        ac.print_dbg('dc','Conversation action error ', error)
        result = None  
    #DTLock.release()
    return result

def _applyProdRules(acid,username,userinput):
    global ProdRulesTbl    
    prods = ProdRulesTbl[acid]
    if prods==None:
        return None
    tkstrinput = _toTokenString( nltk.word_tokenize(userinput.lower()) )
    for pr in prods:
        hear_patts = pr['hear']
        if hear_patts==None:
            continue
        for patt in hear_patts:
            ac.print_dbg('dc','matching hear: ',patt,' with: ',tkstrinput)
            hits = _tokenMatcher(acid, tkstrinput, patt)
            if len(hits)==0:
                continue
            matches = hits[0] if isinstance(hits[0],list) else [hits[0]]
            ac.print_dbg('dc','matches: ',matches)
            # Check if it is a list or a string and take a copy of what is to talk
            talks = pr['talk']
            if isinstance(talks,list):
                talk=str(random.choice(talks))
            else:
                talk = str(talks)
            ac.print_dbg('dc','talk0: ',talk)
            # Process memory variables '... {mem-var1} ... {mem-var2} ...'
            try:
                memvarnames = re.findall("\{([a-zA-Z][-a-zA-Z0-9]*)\}",talk)
                ac.print_dbg('dc','memvarnames=', memvarnames)
                for memvarname in memvarnames:
                    if memvarname=='username':
                        talk = talk.replace('{username}',username)
                    else:
                        memvar = ac.remember(acid,[memvarname])
                        ac.print_dbg('dc','memvar=', memvar)
                        if memvar!=None and memvar[1]!=None:
                            talk = talk.replace('{'+memvarname+'}',str(memvar[1]))
            except Exception as error:
                ac.print_dbg('dc','prod rules mem var error ', error)
            ac.print_dbg('dc','talk1: ',talk)
            # Process extracted fields '... {0} ... {1} ...'
            try:
                talk = talk.format(*matches)
            except Exception as error1:
                ac.print_dbg('dc','prod rules extract field error ', error1)
            ac.print_dbg('dc','talk2: ',talk)
            return talk
    return None

#*******************************************
# OBJECT REPRESENTATION OF DISCUSSION TOPICS
#*******************************************

class DiscussTopic:
    """__init__() class constructor"""
    def __init__(self):
        self.topicName = None
        self.topicContent = None
        self.nextTopicName = None
        self.nextTopicContent = None

#*******************************************
# INTERFACE FUNCTIONS TO DISCUSSION TOPIC SERVICE 
#*******************************************

def get_topic_name(acid):
    """ Get the name of the current discussion topic. For more details on
    discussion topics see the help of set_topic() function.
        
    Args:
        acid:   str with unique global identifier of actor.

    Returns:    
        If no topic was set, returns None.
        Otherwise, returns a string with current topic name.         
    """
    #global DlgTopicName, DlgTopicContent, NextDlgTopicName, NextDlgTopicContent
    global CurrDiscussTopic
    return CurrDiscussTopic[acid].topicName
    #return DlgTopicName.get(acid)
    
def get_topic_content(acid):
    """ Get the content of the current discussion topic. The content of the
    discussion topic, if defined, can be any Python literal value. For more 
    details on discussion topics see the help of set_topic() function.
    
    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        If no topic was set or no content was set for current topic, returns None.
        Otherwise, returns the content set for current topic.         
    """
    #global DlgTopicName, DlgTopicContent, NextDlgTopicName, NextDlgTopicContent
    global CurrDiscussTopic
    return CurrDiscussTopic[acid].topicContent
    #return DlgTopicContent.get(acid)
    
def set_topic(acid,name,content=None):
    """ Set the name and (optionally) the content for the current discussion 
    topic. The name of the topic is a string and the content of topic, if 
    defined, can be any Python literal value.
    
    The NNL dialog system provides a service to handle discussion topics 
    that can be used by intent functions to keep track of the topic being 
    discussed in dialogs with user. 
    
    When called inside an intention function, the set_topic() function alters the 
    current topic for the duration of the current processing iteration of dialog 
    processor. After this iteration the current topic usually will be reset or 
    cleared. A discussion topic usually lasts only for one iteraction of 
    dialog processor. After processing the input string and soon before
    returning the response, the dialog processor will reset or clear the
    current discussion topic.
    
    However, if during the processing of the input string by some intention
    function, the next discussion topic is set by calling the set_next_topic() 
    function then after reseting the current topic, this next topic will be 
    transformed in the new current topic. The function keep_topic() can also 
    be used in intention functions to keep de current discussion topic alive 
    in the next iteraction of the dialog processor.         
    
    Args:
        acid:   str with unique global identifier of actor.
        name:   str with topic name
        content: any literal value

    Returns:    
        On fail, returns False.        
        On success, returns True.      
    """
    # global DlgTopicName, DlgTopicContent, NextDlgTopicName, NextDlgTopicContent
    global CurrDiscussTopic
    cdt = CurrDiscussTopic[acid]
    cdt.topicName=name
    cdt.topicContent=content
    cdt.nextTopicName=None
    cdt.nextTopicContent=None    
    # DlgTopicName[acid] = name
    # DlgTopicContent[acid] = content
    # NextDlgTopicName[acid] = None
    # NextDlgTopicContent[acid] = None
    return True

def reset_topic(acid):
    # global DlgTopicName, DlgTopicContent, NextDlgTopicName, NextDlgTopicContent
    global CurrDiscussTopic
    cdt = CurrDiscussTopic[acid]
    cdt.topicName=None
    cdt.topicContent=None
    cdt.nextTopicName=None
    cdt.nextTopicContent=None    
    # DlgTopicName[acid] = None
    # DlgTopicContent[acid] = None
    # NextDlgTopicName[acid] = None
    # NextDlgTopicContent[acid] = None
    return True

def keep_topic(acid):
    """ Keep the current discussion topic alive in the next iteration of 
    dialog processor. When called inside some intention function, will 
    preserve the name and content of current discussion topic for the next 
    iteration of dialog processor. For more details on discussion topics 
    see the help of set_topic() function.
    
    Args:
        acid: str with unique global identifier of actor.

    Returns:     
        On fail, returns False.        
        On success, returns True.      
    """
    # global DlgTopicName, DlgTopicContent, NextDlgTopicName, NextDlgTopicContent
    global CurrDiscussTopic
    cdt = CurrDiscussTopic[acid]
    cdt.nextTopicName=cdt.topicName
    cdt.nextTopicContent=cdt.topicContent     
    # NextDlgTopicName[acid] = DlgTopicName.get(acid)
    # NextDlgTopicContent[acid] = DlgTopicContent.get(acid)
    return True

def pass_topic_forward(acid):
    # global DlgTopicName, DlgTopicContent, NextDlgTopicName, NextDlgTopicContent
    global CurrDiscussTopic
    cdt = CurrDiscussTopic[acid]
    cdt.topicName=cdt.nextTopicName
    cdt.topicContent=cdt.nextTopicContent
    cdt.nextTopicName=None
    cdt.nextTopicContent=None    
    # DlgTopicName[acid] = NextDlgTopicName.get(acid)
    # DlgTopicContent[acid] = NextDlgTopicContent.get(acid)
    # NextDlgTopicName[acid] = None
    # NextDlgTopicContent[acid] = None
    return True

def get_next_topic_name(acid):
    # global DlgTopicName, DlgTopicContent, NextDlgTopicName, NextDlgTopicContent
    global CurrDiscussTopic
    return CurrDiscussTopic[acid].nextTopicName
    # return NextDlgTopicName.get(acid)
    
def set_next_topic(acid,name,content=None):
    """ Set the name and (optionally) the content for the next discussion 
    topic. The name of the topic is a string and the content of topic,
    if defined, can be any Python literal value. Usually a discussion topic 
    lasts only for one iteraction of dialog  processor. However, if during 
    the processing of the user input, the set_next_topic() function is called    
    by some intention function, then after reseting the current topic, this 
    next topic will be transformed in the new current topic. For more details 
    on discussion topics see the help of set_topic() function.
    
    Args:
        acid:   str with unique global identifier of actor.
        name:   str with topic name
        content: any literal value

    Returns:     
        On fail, returns False.        
        On success, returns True.      
    """
    #global DlgTopicName, DlgTopicContent, NextDlgTopicName, NextDlgTopicContent
    global CurrDiscussTopic
    cdt = CurrDiscussTopic[acid]
    cdt.nextTopicName=name
    cdt.nextTopicContent=content    
    # NextDlgTopicName[acid] = name
    # NextDlgTopicContent[acid] = content
    return True

#*******************************************
# OBJECT REPRESENTATION OF INPUT MODES
#*******************************************

class InputMode:
    """__init__() class constructor"""
    def __init__(self):
        self.mode = None
        self.keepMode = None
        
#*******************************************
# INTERFACE FUNCTIONS TO INPUT MODE SERVICE 
#*******************************************

def get_mode(acid):
    """ Get the identifier of the current input mode. Input modes can be 
    used to select particular intentions from the JSON dialog pattern files. 
    An input mode is definde by an identifier (a single word) that can be 
    associated to some intention in the dialog pattern file using an '@' 
    character. See set_mode() function for details.
        
    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        If no input mode was set, returns None.
        Otherwise, returns a string with current input mode identifier.         
    """
    #global DlgMode, KeepDlgMode
    global CurrInputMode
    return CurrInputMode[acid].mode
    #return DlgMode.get(acid)
 
def set_mode(acid,mode):
    """ Set input mode for the next iteration of dialog processor.
    
    The NNL dialog system provides a service to handle input modes that 
    can be used to select particular intentions from the JSON dialog 
    pattern files. An input mode is defined by an identifier (a single 
    word) that can be associated to some intention in the dialog pattern 
    file using an '@' character.
    
    The patterns corresponding to this intention are compared against the 
    input string only if the current input mode is the same input
    mode associated to the intention by the '@' character. For instance, in 
    the following dialog patterns:
        {"processResponse":  
            ["<the><response|answer><is>(<.+>+)"]},
        {"processResponde@answering-mode":
            ["<is>(<.+>+)", "<it><is>(<.+>+)", "(<.+>+)"]},
    the intention processResponse() will be called if the pattern:
        "<the><response|answer><is>(<.+>+)"
    matches the input string, or if the current input mode is:
        "answering-mode"
    and some of the following patterns match the input string:
        "<is>(<.+>+)", 
        "<it><is>(<.+>+)", 
        "(<.+>+)"
    
    Note that in this example, the patterns used in "answering-mode" mode are
    much more generic than the patterns used when this mode is not required.
    In particular the last pattern, "(<.+>+)", will match and extract any
    sequence of words.
    
    As in the case of discussion topics, an input mode will usually last
    only for one iteraction of NNL dialog processor. After processing the 
    input string and soon before returning the response, the NNL dialog 
    processor will reset or clear the current input mode.
    
    However, if during the processing of the input string by some intention
    function, the set_mode() function is called by some intention function, then
    a new input mode is defined and will be used in the next iteration of
    dialog processor. 
    
    Likewise, if the keep_mode() function is called by some intention function 
    then the current input mode will be preserved to be used in the next 
    iteraction of the dialog processor.  
    
    Args:
        acid:   str with unique global identifier of actor.
        mode:   str with the identifier of input mode, input
                mode identifiers are single words

    Returns:    
        On fail, returns False.        
        On success, returns True.      
    """
    # global DlgMode, KeepDlgMode
    global CurrInputMode
    cim = CurrInputMode[acid]
    cim.mode = mode
    cim.keepMode = True
    # DlgMode[acid] = mode
    # KeepDlgMode[acid] = True
    return True
    
def reset_mode(acid):
    """ Reset input mode for the next iteration of dialog processor
    See set_mode() function for details.   
    Args:
        acid:   str with unique global identifier of actor.
    Returns:     
        On fail, returns False.        
        On success, returns True.      
    """
    # global DlgMode, KeepDlgMode
    global CurrInputMode
    cim = CurrInputMode[acid]
    cim.mode = None
    cim.keepMode = False
    # DlgMode[acid] = None
    # KeepDlgMode[acid] = False
    return True
    
def keep_mode(acid):
    """ Keep current input mode for the next iteration of dialog 
    processor. See set_mode() function for details.   
    Args:
        acid:   str with unique global identifier of actor.
    Returns:     
        On fail, returns False.        
        On success, returns True.      
    """
    # global DlgMode, KeepDlgMode
    global CurrInputMode
    cim = CurrInputMode[acid]
    if cim.mode!=None:
        cim.keepMode = True
    else:
        cim.keepMode = False        
    # if DlgMode.get(acid) != None:
        # KeepDlgMode[acid] = True
    # else:
        # KeepDlgMode[acid] = False
    return True
        
def pass_mode_forward(acid):
    """ Pass current input mode for the next iteration of dialog 
    processor. See set_mode() function for details.   
    Args:
        acid:   str with unique global identifier of actor.
    Returns:     
        On fail, returns False.        
        On success, returns True.      
    """
    # global DlgMode, KeepDlgMode
    global CurrInputMode
    CurrInputMode[acid].keepMode = False        
    # KeepDlgMode[acid] = False
    return True
        
def is_keeping_mode(acid):
    """ Check if is keeping current input mode for the next iteration 
    of dialog processor. See set_mode() function for details.   
    Args:
        acid:   str with unique global identifier of actor.
    Returns:     
        On fail, returns False.        
        On success, returns True.      
    """
    # global DlgMode, KeepDlgMode
    global CurrInputMode
    return CurrInputMode[acid].keepMode       
    # return KeepDlgMode.get(acid)


#*******************************************
# INTERFACE FUNCTIONS TO INTENT RECORDING SERVICE
#*******************************************

def start_recording_intents(acid):
    """ Start recording the intents performed by the actor.
    
    The NNL dialog system provides a service to record intent functions 
    executed by the actor during the processing of user inputs. 
    
    These intents, for short, are recorded as intent records, which are 
    memory records with the following format:
    
    ['recorded-intent',index,time,username,userinput,intentname,matches...]
    
    where:
        index: is the sequential index of the recorded intent, with value 1 
            for the first intent record, and 2, 3, ... for the next records
        time: system time when the intent was recorded
        username: the name of the user that sent the input text
        userinput: the text sent by the user
        intentname: the name of the intent (which is also the name of the 
            function that implements the intent)
        matches: optional list of strings extracted by the token matcher, 
            can be None if no strings were extracted from the input string,
            otherwise is the series of matches: match1, match2, ...
            extracted from the input string
    
    After calling start_recording_intents() each intention executed by the
    actor will be registered as a new 'record-intent' memory record,
    starting with intent index equals to 1    
    
    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns False.        
        On success, returns True.      
    """
    global RecIntents
    ac.forget(acid,['recorded-intent'])
    RecIntents[acid] = 1
    return True
    
def restart_recording_intents(acid,newindex):
    """ Restart the recording of intents performed by the actor.
    
    The NNL dialog system provides a service to record intent functions 
    executed by the actor during the processing of user inputs. These intents, 
    for short, are recorded as intent records, which are memory records where 
    the second field is an sequential index of the recorded intent, with value 
    1 for the first record, 2 for the second, and so on.
    
    The restart_recording_intents() restart the recording of intents,
    but with a new sequential index provided by the newindex argument.

    After calling restart_recording_intents() each intention executed by the
    actor will be registered as a new 'record-intent' memory record,
    starting with intent index equals to newindex
    
    Args:
        acid: str with unique global identifier of actor.
        newindex: the new initial value of sequential index of recorded 
            intents, after the recording is restarted

    Returns:     
        On fail, returns False.        
        On success, returns True.      
    """
    global RecIntents
    RecIntents[acid] = newindex
    return True
    
def stop_recording_intents(acid):
    """ Stop recording the intents performed by the actor. After calling 
    stop_recording_intents() the next intention functions executed by the 
    actor do not will be recorded as 'record-intent' memory records.
    See the help of start_recording_intents() function for details.
    
    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns False.        
        On success, returns True.      
    """
    global RecIntents
    RecIntents[acid] = 0
    return True

def is_recording_intents(acid):
    """ Check if intents are being recorded. In practice, returns 
        the sequential index of the next intent to be recorded.
        If this index is zero, intents are not being recorded.
        If this index is greater than zero, then intents are being
        recorded and the next intent will receive this value for
        its sequential index. See the help of start_recording_intents() 
        function for details.
        
    Args:
        acid: str with unique global identifier of actor.

    Returns:     
        Zero if intents are not being recorded.        
        A non zero value (the sequential index of the next intent 
            to be recorded) if intents are being recorded.      
    """
    global RecIntents    
    if RecIntents.get(acid) != None:
        return RecIntents[acid]
    RecIntents[acid] = 0
    return 0
    
def replay_intent(acid, username, userinput, intentname, matches):
    """ Replay an intent previosly recorded by the actor. See the 
    help of start_recording_intents() function for details.
     
    Args:
        acid:   str with unique global identifier of actor.
        username: the name of the user that sent the input text
        userinput: the text sent by the user
        intentname: the name of the intent (which is also the name of the 
            function that implements the intent)
        matches: optional list of strings extracted by the token matcher, 
            can be None if no strings were extracted from the input string,
            otherwise is the list of matches: [match1, match2, ...]
            extracted from the input string

    Returns:     
        On fail, returns None.      
        On success, returns a string with response provided by the
        intention function.
    """
    resp = _execIntentAction(acid,username,userinput,intentname,matches)
    #resp = _execIntentAction(acid,intent[0],intent[1],intent[2],intent[3:])
    ac.print_dbg('dc','played rec int=',intentname,' with matches=', matches)        
    if is_keeping_mode(acid):
        pass_mode_forward(acid)
    else:
        reset_mode(acid)
    if get_next_topic_name(acid)!=None:
        pass_topic_forward(acid)
    else:
        reset_topic(acid)
    return resp
  
class ReplacementIntent:
    """__init__() class constructor"""
    def __init__(self,username, userinput, intentname, matches):
        self.userName = username
        self.userInput = userinput
        self.intentName = intentname
        self.matchArgs = matches

def record_intent(acid, username, userinput, intentname, matches=None):
    """ Record an intent executed by the actor. See the help of 
    start_recording_intents() function for details.

     
    Args:
        acid:   str with unique global identifier of actor.
        username: the name of the user that sent the input text
        userinput: the text sent by the user
        intentname: the name of the intent (which is also the name of the 
            function that implements the intent)
        matches: optional list of strings extracted by the token matcher, 
            can be None if no strings were extracted from the input string,
            otherwise is the list of matches: [match1, match2, ...]
            extracted from the input string

    Returns:     
        On fail, returns False.      
        On success, returns True.
    """
    global RecIntents, ReplaceRecIntent
    index = RecIntents[acid]
    if index==0:
        return False
        
    if ReplaceRecIntent.get(acid)!=None:
        rri=ReplaceRecIntent[acid]
        if rri.userName==None or rri.userInput==None or rri.intentName==None:
            return True
        username=rri.userName
        userinput=rri.userInput
        intentname=rri.intentName
        matches=rri.matchArgs
        ReplaceRecIntent[acid] = None
    if matches!=None and type(matches) is list:
        intrec = ['recorded-intent', str(index), str(time.time()), 
                    username, userinput, intentname]+matches
    else:
        intrec = ['recorded-intent',str(index), str(time.time()),
                    username, userinput, intentname, matches]
    ac.record(acid,intrec)
    ac.print_dbg('dc','rec int=',intrec)        
    RecIntents[acid] = index+1
    return True
   
def replace_recording_intent(acid, username, userinput, intentname, matches=None):
    """ Replace the intent to be recorded, by this intent. See the help 
    of start_recording_intents() function for details.

     
    Args:
        acid: str with unique global identifier of actor.
        username: the name of the user that sent the input text
        userinput: the text sent by the user
        intentname: the name of the intent (which is also the name of the 
            function that implements the intent)
        matches: optional list of strings extracted by the token matcher, 
            can be None if no strings were extracted from the input string,
            otherwise is the list of matches: [match1, match2, ...]
            extracted from the input string

    Returns:     
        On fail, returns False.      
        On success, returns True.
    """
    global RecIntents, ReplaceRecIntent
    if RecIntents[acid]==0:
        return False
    ReplaceRecIntent[acid] = ReplacementIntent(username,userinput,intentname,matches)
    return True

def do_not_record_intent(acid):
    """ Do not record current intent. See the help of start_recording_intents() 
    function for details.

     
    Args:
        acid: str with unique global identifier of actor.

    Returns:     
        On fail, returns False.      
        On success, returns True.
    """
    global RecIntents, ReplaceRecIntent
    if RecIntents[acid]==0:
        return False
    ReplaceRecIntent[acid] = ReplacementIntent(None,None,None,None)
    return True
   
   
#*******************************************
# MAIN INTERFACE FUNCTIONS FOR CONFIGURATION
# AND INITIALIZATION OF DIALOG CONTROLLER
#*******************************************

def set_dialog_patterns_file(acid, pattsfile):
    """ The main processor of NNL dialog system is formed by a token pattern 
    matcher that try to identify some intention on the input string, and execute 
    the corresponding Python function that implements the handling of this 
    intention. 
    
    The token pattern matcher is configured by a patterns to intents JSON file 
    (the pattsfile parameter) with a JSON list with the following structure:
    [
        {"intent-1":     [pattern1-for-intent-1, pattern2-for-intent1, ...]},
        {"intent-2":     [pattern1-for-intent-2, pattern2-for-intent2, ...]},
        {"intent-3":     [pattern1-for-intent-3, pattern2-for-intent3, ...]},
            ...
        {"intent-n":     [pattern1-for-intent-n, pattern2-for-intent-n, ...]}
    ]
    
    In this list, each element with index i is an JSON object with structure:
        {"intent-i": [pattern1-for-intent-i, pattern2-for-intenti, ...]}
    that defines an intent detection pattern where:     
        intent-i is the identifier of the intention. Intent identifiers can
            have one of the following formats:
                intent-name
                intent-name:[username1, username2, ...]
                intent-name@dialog-mode
                intent-name:[username1, username2, ...]@dialog-mode
            where:
                intent-name is the name of the Python function which 
                    implements the intention, 
                username1, username2 are names of users, when this list of 
                    users is specified, then the intention can be selected 
                    only if the user that send the input text being processed 
                    is in this list.
                dialog-mode is an identifier that can be used to select 
                    particular intentions from the JSON dialog pattern file. 
                    See set_mode() function for details. 
        pattern1-for-intent-i, pattern2-for-intent-i, ...
            are token patterns, where each token pattern is a
            string of tokens to be matched against the input string. 
            
    To identify some intention on the input string the token pattern matcher
    will go through the list of intent detection patterns from the first to the 
    last element (or, equivalently, from top to bottom of patterns to intents 
    JSON file).

    If some token pattern from a patterns-for-intent-i list matches the input 
    string, then the intent Python function corresponding to intent identifier
    intent-i, is called. 
    
    Only the first intention found on the input string has its corresponding 
    intent function called. The pattern matcher scans the pattern to intent
    JSON file from top to botton for each new input string.
           
    A token pattern is a string formed by tokens enclosed in '<' and '>'.
    Words separated by one or more spaces (or tabs) in the input string
    are matched against the tokens defined in the token pattern.
    The case of characters (if they are uppercase or lowercase) is 
    irrelevant. Additionally, regular expression operators can be used
    with tokens and inside tokens too. In particular, the following regular
    expression operations are supported by token patterns:
        "." - the dot operator will match any character in that position;
        "|" - the OR operator can be use for OR comparisons: a match occurs
            if any word from the words separated by "|" inside the token 
            match the corresponding word in the input string
        "*" - the asterisk operator will match any sequence of zero or more
            repetitions of the character or pattern preceding this operator 
        "+" - the plus operator will match any sequence of one or more
            repetitions of the character or pattern preceding this oper    
        "?" - the optional operator: the matching of the preceding token 
            in the token pattern is optional
        "_" - the substring operator used only on the beginning or the
                ending of the token pattern: 
                - if the token pattern starts with "_", then the subsequent 
                token pattern do not need to match from the beginning of 
                the input string 
                - if the token pattern ends with "_", then the preceding
                token pattern do not need to match until the end of 
                the input string 
    
    Strings can also be extracted from the input string by enclosing tokens 
    in the token pattern in '(' and ')'. Text that matched tokens enclosed in 
    parentheses is extracted and returned by the token matcher. Some examples 
    of token patterns:
    
        "<a><text><with><five><tokens>" - this pattern will match strings 
        similar to:
            "a text with five tokens"
            "A Text   With fIVe tokeNS"
            "A TeXT with   FIVE  TOKEns"
            
        "_<a><text><with><five><tokens>" - this pattern will match strings 
        similar to:
            "a text with five tokens"
            "this is not a   text   with   five tokens"
            "THIS  also is not A Text   With fIVe  tokeNS"
            "I dont care about A TeXT with   FIVE TOKEns"
            
        "<a><text><with><five><tokens>_" - this pattern will match strings 
        similar to:
            "a text with five tokens"
            "A Text   With fIVe tokeNS is what i NEEd"
            "A TeXT with   FIVE TOKEns and another four TOkens"
            
        "_<a><text><with><five><tokens>_" - this pattern will match strings 
        similar to:
            "a text with five tokens"
            "this is not a   text   with   five tokens"
            "A Text   With fIVe tokeNS is what i NEEd"
            "thIS is not A TeXT with   FIVE TOKEns and another  four toKens"
            
        "<a><text|phrase|paragraph|message><with><five><tokens|words|terms>" -
            this pattern will match strings similar to:
            "a text with five tokens"
            "a message with five words"
            "A Paragraph With Five Terms"
            "A phrase with   FIVE words"   
            
        "_<.+><.+><with>_" - this pattern matches with strings that have 
            a sequence of 3 tokens where the last token is "with"
            
        "<a>(<.*>)<with>" - this pattern matches with strings that have 
            a sequence of 2 or more tokens where the first token is "a"  
            and the last is "with". This pattern also extract the text that
            match the tokens in the middle of the sequence. For instance,
            this pattern will match the string:
                "a text with five tokens"
            and extract the string: "text"
            It will also match the string:
                "A Paragraph With Five Terms"
            extracting the string: "Paragraph"
                
        "<.+><.+><with>" - matches with strings that start with a sequence
            of 3 tokens and the last token is "with"
            
        "_<.+><.+><five><.+>" - matches with strings that end with a 
            sequence of 4 tokens, where the third token of this
            sequence is "five"
            
        "(<t.*>)" - matches with strings that have one token which starts with
            character 't'. The matching string is also extracted
            
        "(<a.*>)<.*>*(<t.*>)" - matches with strings formed by a sequence of 2
            or more tokens, where the first token start with character 'a' and
            the last token start with character 't'. This pattern also extract 
            strings corresponding to the first and last token.  For instance,
            this pattern will match the string:
                "a text with five tokens"
            and extract the strings: "a" and "tokens"
            It will also match the string:
                "A Paragraph With Five Terms"
            extracting the strings: "A" and "Terms"
    
    Args:
        acid: str with unique global identifier of actor.
        pattsfile: name of JSON file with dialog patterns to detect intentions
                        
    Returns:     
        On fail, returns False.     
        On success, configure the dialog pattern file used by NNL dialog 
            system and returns True. 
    """   
    global IntentsPatternsFile  
    IntentsPatternsFile[acid] = pattsfile
    return True
    

def set_dialog_intents_file(acid, intentsfile):
    """ The main processor of NNL dialog system is formed by a token pattern 
    matcher that try to identify some intention on the input string, and execute 
    the corresponding Python function that implements the handling of this 
    intention.
    
    Intent functions are Python functions that implement the handling of intentions 
    defined in the patterns to intents file. The intentsfile parameter is the name of 
    the Python module that contains all intent functions defined in the pattern 
    to intents JSON file.
    
    Intent functions defined in intentsfile module must have the same name of 
    the intention and must use the following template:
        intent_name(acid,username,userinput,matches)
    where intent_name is the name of the intention as defined in the patterns to
    intents file (without the quotes), and with the following arguments:
        acid:       str with unique global identifier of actor.
        username:   name of the user as received by process_dialog_input() function
        userinput:  string with last user input as received by process_dialog_input() 
                    function
        matches:    list of tokens extracted by the token matcher, can be None or the
                    empty list [] if no tokens were extracted from the input string
    
    Intent functions return a string to be sent back to the user.
    
    Args:
        acid: str with unique global identifier of actor.
        intentsfile: name of Python module with functions that implement dialog 
            intentions
                        
    Returns:
     
        On fail, returns False.     
        On success, configure the intents file to be used by the NNL dialog 
            system and returns True.            
    """   
    global IntentsFunctionsFile  
    IntentsFunctionsFile[acid] = intentsfile
    return True
    

def set_dialog_hear_talk_rules_file(acid, rulesfile):
    """ In addition to the main processor of the NNL dialog system, 
    which is oriented to find user intents, the NNL dialog system can 
    also handle simple "hear and talk" rules that map token patterns 
    found in input text directly into output text messages. If no intent 
    is found on the user input and the hear-talk rule processing is 
    configured then the NNL processor will search hear-talk rules for a 
    rule that match the input string and return the output of this rule
    (the 'talk' part of the rule) as the output message.
    
    This hear-talk rule processing is configured by the hear-talk JSON 
    file defined by rulesfile parameter. This file stores a JSON list
    of hear-talk rules with the following structure:
    [
        {
        "hear":    [token-patterns-for-rule-1],
        "talk":    <output-for-rule-1>
        },
        {
        "hear":    [token-patterns-for-rule-2],
        "talk":    <output-for-rule-2>,
        },
        ...
        {
        "hear":    [token-patterns-for-rule-n],
        "talk":    <output-for-rule-n>
        }
    ]
    where: 
        <output-for-rule-i> can be an output string or a list of output strings.
    
    Each hear-talk rule has a "hear" and a "talk" side. The "hear" side of 
    the rule define a list of token patterns to be matched against the input 
    string. The format of these token patterns is the same used in the pattern 
    to intents file (see the help of set_dialog_patterns_file() function for 
    details).
    
    The hear-talk pattern matcher scans the hear-talk JSON file from top to 
    botton for each new input string. If some of the token patterns from the 
    "hear" part of some hear-talk rule match the input string, then the output 
    for this rule defined in the "talk" side of the rule is processed and sent 
    back to the user.
    
    The output of hear-talk rules can be composed by an output string or by 
    a list of output strings. If it is a list, then some string of this list 
    is randomically chosen as the output string to be sent to user.
    
    Output strings can contain some additional fields, enclosed by '{' and
    '}' character, which are replaced with corresponding values before 
    sending the output back to user.
    
    Fields {0}, {1}, {2}, ... are replaced by tokens extracted from the input 
    string by the token pattern (see set_dialog_patterns_file() function help 
    for details on how to extract tokens from input).
    
    Fields {memory-var-1}, {memory-var-2}, ... where memory-var-i are strings
    with the name of memory variables, are replaced by the values of these
    variables. A memory variable is stored in a memory record with two fields: 
    the first field is a string with the name of the variable and the second 
    field is a string with the value of the variable. 
     
    Args:
        acid: str with unique global identifier of actor.
        rulesfile: name of JSON file containing hear-talk rules
                        
    Returns:
        On fail, returns False.     
        On success, configure hear-talk rules file used by the NNL dialog 
            system and returns True.            
    """   
    global ProdRulesFile  
    ProdRulesFile[acid] = rulesfile
    return True
    
 
def set_dialog_aiml_files(acid, aimlfiles):
    """ The NNL dialog processor can also be configured to use AIML
    rules to process user input. An additional AIML interpreter can 
    be configured to work with NNL dialog system. 
    
    If the aimlfiles argument is provided then the dialog system will 
    try to initialize the AIML kernel interpreter with these files. 
    If the AIML initialization is OK and no intention is found on user 
    input neither an hear-talk rule can be applied to this input, then 
    the AIML intepreter will process the input string. Any response 
    provided by AIML interpreter is then returned to the user.
    
    Functions aiml_set_bot_prop() and aiml_get_bot_prop() can be used to
    manage global bot properties (constants) accessed by AIML rules with
    AIML tags like:
        <bot name="master"/>
        <bot name="name"/>
        <bot name="birthday"/>
        <bot name="birthplace"/>
        <bot name="gender"/>
    
    Functions aiml_set_pred() and aiml_get_pred() can be used to read and
    modify global predicates (variables) used by AIML rules with
    AIML tags like:
        <set name="name"/>
        <get name="name"/>
        <set name="age"/>
        <get name="age"/>
    
    See the help of these functions for more details.
                    
    Args:
        acid:  str with unique global identifier of actor.
        aimlfiles:  the AIML file (or list of AIML files) to be loaded 
            by AIML interpreter
                        
    Returns:
     
        On fail, returns False.     
        On success, configure AIML files used by the NNL dialog system 
            and returns True.            
    """    
    global AIMLFiles  
    AIMLFiles[acid] = aimlfiles
    return True


def set_dialog_speeches_file(acid, speechesfile):
    """ The NNL dialog system provides a service that can be used by 
    intent functions to generate standard speeches or locutions. The 
    set_dialog_speeches_file() function configures this service, 
    informing through the speechesfile parameter, which JSON file 
    contains the set of standard speeches or locutions to be used by
    the service. 
    
    Each speech has an unique identifier associated to to a list of 
    strings of text. These strings define the standard phrases or 
    utterances to be said in respect to the speech id. The JSON file 
    that defines the speeches have the following structure:
    {
        "speech-id-1":  ["string-1-of-speech-id-1",
                        "string-2-of-speech-id-1",
                            ...
                        ],
        "speech-id-2":  ["string-1-of-speech-id-1",
                        "string-2-of-speech-id-1",
                            ...
                        ],
                            
            ...
            
        "speech-id-n":  ["string-1-of-speech-id-1",
                        "string-2-of-speech-id-1",
                            ...
                        ],
    }
    
    The function: 
        gen_speak(acid,speechid,paramlist=[],defaultphrase="")
    can be used in intent functions to generate standard speeches. When called, 
    this function will try to find the list of strings/phrases associated to 
    speechid and return a random selected string/phrase from this list (if 
    nothing is found, this function returns defaultphrase argument).
    Parametric phrases, with parameters {0}, {1}, ... are possible. If they 
    are used the paramlist argument contains the list of values to replace 
    parameters {0}, {1}, ...
    
    The function: 
        get_speaks(acid,speechid) 
    will return the list of strings or phrases associated to a speechid.
    
    Args:
        acid: str with unique global identifier of actor.
        speechesfile: name of JSON file containing speeches that can be 
            used in intention functions
                        
    Returns:
     
        On fail, returns False.     
        On success, configure the speeches file used by the NNL dialog 
            system and returns True.            
    """    
    global SpeechesFile  
    SpeechesFile[acid] = speechesfile
    return True
    
    
def init_dialog_system(acid):
    """ Initialize the VirtualStage Near Natural Language (NNL) dialog system. 
    
    The NNL dialog system main processor is formed by a token pattern matcher 
    that try to identify some intention on the input string, and execute the 
    intent function corresponding to this intention.
    
    The token pattern matcher is configured by a patterns to intents JSON 
    file and must be previously defined by:
        set_dialog_patterns_file() 
    function (see the help of set_dialog_patterns_file() function for details 
    about the format of this JSON file).
    
    Intent functions are Python functions that implement the intentions 
    defined in the patterns to intents file. The name of the Python module 
    that contains all intent functions used in pattern to intents file must 
    be previously defined by:
        set_dialog_intents_file() 
    function (see the help of set_dialog_intents_file() function for details 
    about intent functions syntax and semantics).
    
    Besides the intent oriented dialog processing, the NNL dialog processor can
    handle simple hear-talk rules, that map some token pattern into an output text 
    message. To use hear-talk rules is necessary to define the JSON file that 
    contain these rules calling the:
        set_dialog_hear_talk_rules_file() 
    function before calling init_dialog_system(), otherwise the NNL dialog system 
    will not process any hear-talk rule (see the help of set_dialog_hear_talk_rules_file() 
    function for details about hear-talk rules).
    
    An additional AIML interpreter can also be configured to work with dialog system
    calling:
        set_dialog_aiml_files()
    function before calling init_dialog_system(), otherwise the NNL dialog system 
    will not process any AIML rule (see the help of set_dialog_aiml_files() 
    function for details about AIML processing).
                    
    An optional set of standard speeches or locutions, specified by a JSON file, 
    can also be passed to the NNL standard speeches service calling:
        set_dialog_speeches_file() 
    function. Each speech has an unique speechid identifier associated to a list 
    of strings. The function:
        gen_speak(acid,speechid,paramlist=[],defaultphrase="")
    handles speechid identifier and can be used by intent functions to generate 
    standard speeches if the speeches JSON file was defined (see the help of 
    set_dialog_speeches_file() function for details).
    
    Args:
        acid: str with unique global identifier of actor.
                        
    Returns:    
        On fail, returns False.     
        On success, initialize and start the NNL dialog system and returns True.            
    """    
    global IntentsPatternsFile, IntentsFunctionsFile, ProdRulesFile, SpeechesFile
    global IntentsPatternsTbl, IntentsFunctionsTbl, DlgProdsRulesTbl 
    global SpeechesTbl, AIMLFiles, AIMLKrnlTbl 
    global CurrDiscussTopic, CurrInputMode

# Initialize token pattern matcher, which is the main processor of NNL
    # Load patterns to intents JSON file
    try: 
        patterns = _loadPatterns(IntentsPatternsFile[acid])
    except Exception as error:
        ac.print_dbg('dc','Dialog patterns file error ', error)
        return False
    if patterns==None:
        ac.print_dbg('dc','Cannot load dialog patterns file')
        return False
    ac.print_dbg('dc','Dialog patterns loaded')
    # Load intents function Python module
    try:
        intentsmod = importlib.import_module(IntentsFunctionsFile[acid])
    except Exception as error:
        ac.print_dbg('dc','Dialog actions file error ', error)
        return False
    if patterns==None:
        ac.print_dbg('dc','Cannot load dialog actions file')
        return False
    ac.print_dbg('dc','Dialog actions module loaded')
    if patterns==None or intentsmod==None:
        return False 
    #DTLock.acquire()
    IntentsPatternsTbl[acid] = patterns
    IntentsFunctionsTbl[acid] = intentsmod
    #DTLock.release()

    # Initialize standard speeches generator, if it is configured
    if SpeechesFile.get(acid)!=None:
        # Load JSON file with standard speeches
        speeches=_loadSpeeches(SpeechesFile.get(acid))
        if speeches!=None:
            SpeechesTbl[acid] = speeches
            ac.print_dbg('dc','Speeches file loaded')
        else:
            ac.print_dbg('dc','Cannot load speeches file')

    # Initialize hear-talk production rules processor, if it is configured
    if ProdRulesFile.get(acid)!=None:
        # Load JSON file with hear-talk production rules
        prods=_loadProdRules(ProdRulesFile.get(acid))
        if prods!=None:
            ProdRulesTbl[acid] = prods
            ac.print_dbg('dc','Dialog production rules file loaded')
        else:
            ac.print_dbg('dc','Cannot load dialog production rules file')
        
    # Initialize AIML processor, if it is configured
    if AIMLFiles.get(acid)!=None:
        ac.print_dbg('dc','Loading AIML files')
        # Initialize AIML kernel
        aimlk = aiml.Kernel()
        # Load AIML files
        aimlk.bootstrap(learnFiles=AIMLFiles.get(acid))
    else:
        aimlk=None
    AIMLKrnlTbl[acid]=aimlk
    
    # Initialize discussion topic, dialog mode and intent
    # recording services processing
    CurrDiscussTopic[acid] = DiscussTopic()
    CurrInputMode[acid] = InputMode() 
    RecIntents[acid] = 0
    ReplaceRecIntent[acid] = None

    return True


#*******************************************
# MAIN INTERFACE FUNCTIONS FOR PROCESSING
# USER INPUT BY DIALOG SYSTEM
#*******************************************

def process_dialog_input(acid,username,userinput):
    """ Process user input with dialog processors configured in NNL dialog
    system.
    
    First, runs the main processor of NNL dialog system on the user input 
    text trying to identify some intention (i.e. match some intent pattern on
    the user input). If some intent is found, then calls the function that 
    implements the intention and returns the response provided by the function 
    to the caller. 
    
    If no intention is found and hear-talk rules processing is configured, 
    then check if some hear-talk rule can be applied to user input. If this is 
    so, then return the text produced by the rule to the caller.
    
    Finally, if no intention was found in user input, neither some hear-talk 
    rule could be applied to this input, then if the AIML interpreter is 
    configured, runs this interpreter on the user input and returns the 
    response provided by this interpreter to the caller. 
    
    Otherwise return None.
        
    Args:
        acid:           str with unique global identifier of actor.
        username:       name of the user that sent the input text
        userinput:      string with last input to be processed by dialog system
                        
    Returns:     
        On fail, returns None.      
        On success, returns a string with response provided by some intention or 
            by the AIML interpreter. The function get_last_dlg_proc(acid)
            will return what processor ('NNL', 'AIML' or None) whas used to
            process last input.
    """

    global IntentsPatternsTbl, IntentsFunctionsTbl, AIMLKrnlTbl, LastDlgProc
    #global RecIntents
    LastDlgProc[acid]=None
    # First check if user input match some intent pattern
    intent = _findIntent(acid,username,userinput)
    ac.print_dbg('dc','_findIntent=',intent)
    if intent!=None:
        # Found intent pattern, execute corresponding intent function
        was_recording_intents = is_recording_intents(acid)
        resp = _execIntentAction(acid,username,userinput,intent[0],intent[1])
        if was_recording_intents>0 and is_recording_intents(acid)>0:
            # Was recording intentions before and after the execution
            # of the intention, thus record this intention
            # (this avoids recording the intentions that start and stop
            # intention recording) 
            record_intent(acid,username,userinput,intent[0],intent[1])
            # index = was_recording_intents
            # if intent[1] != None and type(intent[1]) is list:
                # intrec = ['recorded-intent', str(index), str(time.time()), 
                            # username, userinput, intent[0]]+intent[1]
            # else:
                # intrec = ['recorded-intent',str(index), str(time.time()),
                            # username, userinput, intent[0], intent[1]]
            # ac.record(acid,intrec)
            # ac.print_dbg('dc','rec int=',intrec)        
            # RecIntents[acid] = index+1
        # Register that last input was processed by the main intent processor
        LastDlgProc[acid]='NNL-MIP'
        ac.print_dbg('dc','NNL-MIP resp=',resp)        
    else:
        # No intention was found in user input, now check if some
        # hear-talk production rule can be applied to this input
        resp = _applyProdRules(acid,username,userinput)
        if resp!=None:
            # Register that last input was processed by some hear-talk prod. rule
            LastDlgProc[acid]='NNL-HTP'
            ac.print_dbg('dc','NNL-HTP resp=',resp)
        else:
            # No intention was found in user input, neither some hear-talk 
            # production could be applied to this input, finally check if 
            # AIML processor is configured and can handle user input
            aimlk = AIMLKrnlTbl[acid]
            if aimlk!=None:
                resp = aimlk.respond(userinput,acid)
                # Register that last input was processed by AIML
                LastDlgProc[acid]='NNL-AIML'
                ac.print_dbg('dc','NNL-AIML resp=',resp)
            else:
                ac.print_dbg('dc','NO intent or rule found and AIML not running')
                # No NNL processor could handle the input, return None
                resp = None
    
    # Maintenance work on discussion topic and dialog mode services
    if is_keeping_mode(acid):
        pass_mode_forward(acid)
    else:
        reset_mode(acid)
    ac.print_dbg('dc','handled mode')
    if get_next_topic_name(acid)!=None:
        pass_topic_forward(acid)
    else:
        reset_topic(acid)
    ac.print_dbg('dc','handled topic')
    return resp
        
#*******************************************
# INTERFACE FUNCTIONS TO HEAR-TALK 
# RULES MANAGEMENT SERVICE
#*******************************************

def save_hear_talk_rules(acid,prodsfile):
    """ The NNL dialog system provides a service to dynamically manage 
    hear-talk rules. The function save_hear_talk_rules() saves
    the hear-talk rules currently in use by NNL processor directly 
    to a JSON file.
    
     Args:       
        acid:       str with unique global identifier of actor.
        prodsfile:  str with the name of JSON file where hear-talk
                    rules will be written.
                        
    Returns:     
        On fail, returns False.      
        On success, returns True
    """
    try:
        prods=ProdRulesTbl[acid]
        if prods!=None:
            with open(prodsfile, 'w') as fp:
                json.dump(prods, fp)
            return True
    except Exception as error:
        ac.print_dbg('dc','Dialog prod rules file save error ', error)
    return False
 
def restore_prod_rules(acid,prodsfile):
    """ The NNL dialog system provides a service to dynamically
    manage hear-talk rules. The restore_prod_rules() function, 
    restores hear-talk rules stored in JSON file.
    
     Args:        
        acid:       str with unique global identifier of actor.
        prodsfile:  str with the name of JSON file where hear-talk
                    rules are stored.
                        
    Returns:     
        On fail, returns False.      
        On success, returns True
    """
    global ProdRulesTbl
    result = False
    try:
        prods=_loadProdRules(prodsfile)
        if prods!=None:
            ProdRulesTbl[acid] = prods
            result = True
            ac.print_dbg('dc','Dialog production rules file loaded')
        else:
            ac.print_dbg('dc','Cannot load dialog production rules from file')
    except Exception as error:
        ac.print_dbg('dc','Dialog prod rules file restore error ', error)
    return result
 
def add_hear_talk_rule(acid,hear,talk):
    """ The NNL dialog system provides a service dynamically manage 
    hear-talk rules. This function adds a new hear-talk rule 
    to NNL processor.
    
     Args:        
        acid:   str with unique global identifier of actor.
        hear:   list of str with hear side patterns (see init_dialog() function).
        talk:   str with talk side output string (see init_dialog() function).
                        
    Returns:     
        On fail, returns False.      
        On success, returns True
    """
    global ProdRulesTbl
    prods = ProdRulesTbl.get(acid)
    if prods==None:
        ProdRulesTbl[acid]=[{'hear':hear, 'talk':talk}.copy()]
    else:
        prods.append({'hear':hear, 'talk':talk}.copy())
    return True


#*******************************************
# INTERFACE FUNCTIONS TO STANDARD SPEECHES 
# GENERATION SERVICE
#*******************************************

def gen_speak(acid, speechid, paramlist=[], defaultphrase = ""):
    """ The NNL dialog system provides a service that can be used by 
    intent function to generate standard speeches. The function gen_speak()
    can be used by some intent function to generate a particular standard
    speech. This will try to find the list of strings/phrases associated to
    speech identified by speechid and return a random selected string/phrase 
    from this list (if nothing is found, this function returns defaultphrase).
    Parametric phrases, with parameters {0}, {1}, ... are possible. If they 
    are used the paramlist argument contains the list of values to replace 
    parameters {0}, {1}, ...
        
    Args:
        acid:           str with unique global identifier of actor.
        speechid:       str with unique identification of the speech.
        defaultphrase:  optional param, str with default phrase to be
                        returned in case of error
        paramlist:      optional param, list of values to replace the
                        parameters {0}, {1}, ... in parametric phrases
                      
    Returns:     
        On fail, returns defaultphrase.      
        On success, returns a random selected string from list of strings 
        (or phrases) associated to speech identified by speechid.
    """
    global SpeechesTbl
    speeches=SpeechesTbl[acid]
    if speeches==None:
        return defaultphrase
    phrases=speeches.get(speechid)
    if phrases==None:
        return defaultphrase
    phrase = random.choice(phrases)
    try:
        if len(paramlist)>0:
            phrase = phrase.format(*paramlist)
    except Exception as error1:
        ac.print_dbg('dc','speak phrase param processing error ', error1)           
    return phrase

def get_speaks(acid,speechid):
    """ This function will return the list of strings or phrases associated 
    to a speechid. See the help of gen_speak() for details.  
        
    Args:
        acid:           str with unique global identifier of actor.
        speechid:       str with unique identification of the speech.                      
                      
    Returns:     
        On fail, returns None.      
        On success, returns the list of strings (or phrases) associated
        to speech identified by speechid.
    """
    global SpeechesTbl
    speeches=SpeechesTbl[acid]
    if speeches==None:
        return None
    return speeches.get(speechid)
    
#*******************************************
# INFORMATION FUNCTIONS ABOUT DIALOG SYSTEM
#*******************************************

def get_last_dlg_proc(acid):
    """ Returns what processor whas used to process last input.
    
     Args:        
        acid: str with unique global identifier of actor.
                        
    Returns:     
        On fail, returns None.      
        On success, returns a string indicating what processor whas used to
        process last input. NNL can use the following processors:
            NNL-MIP: main intent processor
            NNL-HTP: hear-talk rules processor
            NNL-AIML: AIML interpreter
    """
    return LastDlgProc.get(acid)
    
def get_prod_rules(acid):
    """ Returns the list of hear-talk rules configured in NNL dialog 
    processor.
    
    Args:
        acid: str with unique global identifier of actor.                      
                      
    Returns:     
        On fail, returns None.      
        On success, returns the entire list of hear-talk rules.
    """
    global ProdRulesTbl
    prodrules = ProdRulesTbl[acid]
    result=[]
    for prodrule in prodrules:
       result.append(prodrule)
    return result

def get_intent_list(acid,searchstr=None):
    """ Returns the list of intentions configured in NNL dialog processor.
    
    Args:
        acid: str with unique global identifier of actor.
        searchstr: str with an optional search string for intentions.                      
                      
    Returns:     
        On fail, returns None.      
        On success, if searchstr is None, returns the entire list of
            of intentions, otherwise, return the list of intentions
            with names that start with searchstr parameter.
    """
    global IntentsPatternsTbl, IntentsFunctionsTbl, AIMLKrnlTbl
    result=[]
    dlgpatts = IntentsPatternsTbl[acid]
    if searchstr==None or searchstr=='':
        for intpatts in dlgpatts:
            result.append(intpatts.intent)
    else:
        for intpatts in dlgpatts:
            if intpatts.intent.casefold().startswith(searchstr.casefold()):
                result.append(intpatts.intent)        
    return result

def get_patterns_intent_list(acid,intent):
    """ Returns the list of patterns for some intent in NNL dialog 
    processor.
    
     Args:
        acid: str with unique global identifier of actor.
        intent: str the name of intention.                        
                      
    Returns:     
        On fail, returns None.      
        On success, returns the list of patterns for intention intent.
    """
    global IntentsPatternsTbl, IntentsFunctionsTbl, AIMLKrnlTbl    
    ac.print_dbg('dc','get patterns for intention=',intent)
    result=[]
    dlgpatts = IntentsPatternsTbl[acid]
    for intpatts in dlgpatts:
        if intpatts.intent==intent:
            for origpatt in intpatts.origpatterns:
                result.append(origpatt)
    return result

#*******************************************
# INTERFACE FUNCTIONS FOR AIML PROCESSOR
# SERVICES
#*******************************************

def aiml_set_bot_prop(acid, name, value):
    """ Set a global bot property for AIML processor.
    
    A global bot property set by this function is a constant, which can
    be posteriously accessed by AIML rules with <bot name=.../> tags.
    
    For instante, if the bot property "name" is set to "Alice Clone" with:
        aiml_set_bot_prop(acid,"name","Alice Clone")
    then the AIML tag:
        <bot name="name"/>
    will return "Alice Clone" when used in an AIML rule.
        <bot name="birthplace"/>
        <bot name="gender"/>
        
     Args:
        acid:   str with unique global identifier of actor.
        name:   str with the name of bot property. 
        value:  str with the value of bot property
                      
    Returns:     
        On fail, returns False.      
        On success, returns True.
    """
    aimlk = AIMLKrnlTbl.get(acid)
    if aimlk!=None: 
        ac.print_dbg('dc','name=',name,' value=',value,' acid=',acid)
        aimlk.setBotPredicate(name,value)
        return True
    return False

def aiml_set_pred(acid, name, value):
    """ Set a global predicate for AIML processor.
    
    A global predicate set by this function is a variable, which can
    be posteriously accessed by AIML rules with <get name=.../> tags.
    
    For instante, if the predicate "age" is set to "10 years" with:
        aiml_set_prep(acid,"age","10 years")
    then the AIML tag:
        <get name="name"/>
    will return "10 years" when used in an AIML rule.

    Args:
        acid:   str with unique global identifier of actor.
        name:   str with the name of predicate. 
        value:  str with the value of predicate
                      
    Returns:    
        On fail, returns False.      
        On success, returns True.
    """
    aimlk = AIMLKrnlTbl.get(acid)
    if aimlk!=None:
        aimlk.setPredicate(name,value,acid)
        return True
    return False

def aiml_get_bot_prop(acid, name):
    """ Get the value of a global bot property set in AIML processor.
    
     Args:
        acid:   str with unique global identifier of actor.
        name:   str with the name of bot property. 
                      
    Returns:     
        On fail, returns None.      
        On success, returns the value of bot property.
    """
    aimlk = AIMLKrnlTbl.get(acid)
    if aimlk!=None:
        return aimlk.getBotPredicate(name)
    return None   

def aiml_get_pred(acid, name):
    """ Get the value of a global predicate set in AIML processor.
    
    Global predicates are variables that can be modified by AIML rules 
    with <set name=...>...</set> tags or read by these rules with 
    <get name=.../> tag.
    
    For instante, if the predicate "friend" is set to "Elisa Clone" by a
    tag like:
        <set name="friend">Elisa Clone</set> 
    in some AIML rule, then this predicate can be read in Python code 
    calling the function:
        aiml_get_prep(acid,"friend")
    In this case this function will return "Elisa Clone".
    
    Args:
        acid:   str with unique global identifier of actor.
        name:   str with the name of predicate. 
                      
    Returns:     
        On fail, returns None.      
        On success, returns the value of predicate.
    """
    aimlk = AIMLKrnlTbl.get(acid)
    if aimlk!=None:
        return aimlk.getPredicate(name,acid)
    return None


