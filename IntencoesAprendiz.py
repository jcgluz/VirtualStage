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
#   Module:     IntencoesAprendiz 
#   Purpose:    Exemplo de modulo que implementa as intencoes das
#               conversas/dialogos do ator aprendiz (trainee actor)
#   Author:     João Carlos Gluz 
#
###############################################################
###############################################################

""" Modulo IntencoesAprendiz - Exemplo de modulo que implementa as intencoes
        das conversas/dialogos do ator aprendiz (apprentice actor) """

import random
import clr
import time
import re
import uuid
import math
import ActorController as ac
import DialogController as dc
import AtorAprendiz
from PerguntasAprendiz import *
from ComandosAprendiz import *
from TreinamentoAprendiz import *

###############################
# Intention Functions
###############################

def ultimaFraseTeste(acid,username,userinput,matches):
    return "Testou OK! Testou OK!"
    
def saudacoes(acid,username,userinput,matches):
    return dc.gen_speak(acid,'respostaSaudacoes')
    
def incentivos(acid,username,userinput,matches):
    return dc.gen_speak(acid,'agradecimentos')
    
def obrigado(acid,username,userinput,matches):
    return dc.gen_speak(acid,'respostaSim')
    
def adeus(acid,username,userinput,matches):
    followvar = ac.remember(acid,['following-avatar'])
    resp=""
    if followvar!=None:
        ac.stop_follow(acid)
        ac.forget(acid,['following-avatar'])
        resp+=dc.gen_speak(acid,'naoVouSeguirVoce')+".\n"
    resp=dc.gen_speak(acid,'ateLogo')
    return resp
    
def usuarioInformaNome(acid,username,userinput,matches):
    ac.record(acid,['user-name',matches[0]])
    return "OK, e como você está {0}".format(matches[0])

def respostaSim(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    ac.print_dbg('intencoes',"yes answer topic=",topic)
    if topic=="confirm-obj":
        return respostaSim_confirm_obj(acid,username,userinput,matches)
    if topic=="helping-intents":
        return respostaSim_helping_intents(acid,username,userinput,matches)          
    if topic=="helping-prod-rules":
        return respostaSim_helping_prod_rules(acid,username,userinput,matches)
    if topic=="listing-objects":
       return respostaSim_listing_objects(acid,username,userinput,matches)
    if topic=="listing-places":
       return respostaSim_listing_places(acid,username,userinput,matches)
    if topic=="listing-scenes":
       return respostaSim_listing_scenes(acid,username,userinput,matches)
    if topic=="listing-tasks":
       return respostaSim_listing_tasks(acid,username,userinput,matches)
    if topic=="continue-learning-question-answer":
       return respostaSim_continue_learning_question_answer(acid,username,userinput,matches)
    return dc.gen_speak(acid,'respostaSim')
    
def respostaNao(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    if topic=="confirm-obj": 
        return respostaNao_confirm_obj(acid,username,userinput,matches)
    if topic=="helping-intents":
        return respostaNao_helping_intents(acid,username,userinput,matches)
    if topic=="helping-prod-rules":
        return respostaNao_helping_prod_rules(acid,username,userinput,matches)
    if topic=="listing-objects":
        return respostaNao_listing_objects(acid,username,userinput,matches)
    if topic=="listing-places":
        return respostaNao_listing_places(acid,username,userinput,matches)
    if topic=="listing-scenes":
        return respostaNao_listing_scenes(acid,username,userinput,matches)
    if topic=="listing-tasks":
        return respostaNao_listing_tasks(acid,username,userinput,matches)
    if topic=="continue-learning-question-answer":
        return respostaNao_continue_learning_question_answer(acid,username,userinput,matches)
    return random.choice(["Tá bom", "Pode ser", "Que seja"])
      
def salveMemorias(acid,username,userinput,matches):
    if matches!=None and matches[0]!=None:
        memorias = random.choice(["minhas memórias ","meu estado mental ","meus ensinamentos "])
        resp = dc.gen_speak(acid, 'achoQueSalvei(OSDADOS;NOMEARQ)',[memorias,matches[0]],"Salvei memórias")
        ac.save_memories(acid,matches[0])
    else:
        resp=dc.gen_speak(acid,'qualMesmo(ACOISA)',["o nome do arquivo"],"Qual?")
    return resp

def recupereMemorias(acid,username,userinput,matches):
    if matches!=None and matches[0]!=None:
        memorias = random.choice(["minhas memórias ","meu estado mental ","meus ensinamentos "])
        resp = dc.gen_speak(acid, 'achoQueRecuperei(OSDADOS;NOMEARQ)',[memorias,matches[0]],"Recuperei memórias")
        ac.restore_memories(acid,matches[0])
    else:
        resp=dc.gen_speak(acid,'qualMesmo(ACOISA)',["o nome do arquivo"],"Qual?")
    return resp

def salveBatePapos(acid,username,userinput,matches):
    if matches!=None and matches[0]!=None:
        resp = dc.gen_speak(acid, 'achoQueSalvei(OSDADOS;NOMEARQ)',["meus bate-papos",matches[0]],"Salvei bate-papos")
        dc.save_hear_talk_rules(acid,matches[0])
    else:
        resp=dc.gen_speak(acid,'qualMesmo(ACOISA)',["o nome do arquivo"],"Qual?")
    return resp
    
def recupereBatePapos(acid,username,userinput,matches):
    if matches!=None and matches[0]!=None:
        resp = dc.gen_speak(acid, 'achoQueRecuperei(OSDADOS;NOMEARQ)',["meus bate-papos",matches[0]],"Recuperei bate-papos")
        dc.restore_prod_rules(acid,matches[0])
    else:
        resp=dc.gen_speak(acid,'qualMesmo(ACOISA)',["o nome do arquivo"],"Qual?")
    return resp


def ajudaSobreComandos(acid,username,userinput,matches):
    resp = "Eu posso "+"sentar, levantar, bater palmas, dançar, curvar," + \
            " pular, agachar, correr, caminhar ou voar para você"
    return resp


def tokenPatternToWordsPattern(tokpatt):
    patt = tokpatt.replace('..*','_*')
    patt = tokpatt.replace('.*','*')
    patt = patt.replace('.+','_*')
    patt = patt.replace('.','_')
    patt = '... '+patt[1:] if patt[0]=='_' else patt
    patt = patt[:-1]+' ...' if patt[-1]=='_' else patt
    patt = re.sub(r'<([^>]+?)>\?',r'[\1]',patt)
    patt = patt.replace('><',' ')
    patt = patt.replace('>',' ')
    patt = patt.replace('<',' ')
    patt = patt.replace('|','/')
    return patt


def respostaSim_helping_prod_rules(acid,username,userinput,matches):
    ac.print_dbg('intencoes',"helping-prod-rules topic")
    prodrules = dc.get_topic_content(acid)
    ac.print_dbg('intencoes',"intentlist=",prodrules)
    if prodrules:
        resp=dc.gen_speak(acid,'segueListagem(ITEMS)',["bate-papos"],"Segue mais")+":\n"
        resp+=printingProdRules(acid,prodrules)
        ac.print_dbg('intencoes',"printingProdRules= ",resp)
    else:
        resp=dc.gen_speak(acid,'fimListagem(ITEMS)',["bate-papos"],"Sem mais")+":\n"
    return resp
    

def respostaNao_helping_prod_rules(acid,username,userinput,matches):
    return dc.gen_speak(acid,'pareiListagem')+'. '+dc.gen_speak(acid,'sePrecisarAjuda')
    

def printingProdRules(acid,prodrules):
    resp = ""
    while prodrules:
        prodrule = prodrules.pop(0)
        ac.print_dbg('funaux','prodrule=',prodrule)
        patts = prodrule['hear']
        outp = prodrule['talk']
        if patts==None or len(patts)==0:
            continue
        resp+="Padrões de pergunta:\n"
        for patt in patts:
            resp+="    "+tokenPatternToWordsPattern(patt)+"\n"
        resp+="Resposta:\n"
        resp+="   "+outp+"\n"
        # VR chat messages are limited to 1023 chars, using a low limit to avoid problems
        if prodrules==[]:
            resp+=dc.gen_speak(acid,'fimListagem(ITEMS)',["bate-papos"],"Acabou")            
        elif len(resp)>500:
            resp+=dc.gen_speak(acid,'querVerMaisBatePapos')
            dc.set_next_topic(acid,'helping-prod-rules',prodrules.copy())
            prodrules=[]
    return resp
    

def ajudaBatePapos(acid,username,userinput,matches):
    resp = dc.gen_speak(acid,'saudacoesIniciais')+".\n"
    batepapos = random.choice(["bate-papos","chats"])
    resp+=dc.gen_speak(acid,'reconhecoSeguintes(COISAS)',[batepapos],"Reconheço chats")+":\n"
    prodrules = dc.get_prod_rules(acid)
    resp+=printingProdRules(acid,prodrules)
    return resp

    
def respostaSim_helping_intents(acid,username,userinput,matches):
    ac.print_dbg('intencoes',"helping-intents topic")
    intentlist = dc.get_topic_content(acid)
    ac.print_dbg('intencoes',"intentlist=",intentlist)
    conversas=random.choice(["conversas","diálogos"])
    if intentlist:
        resp=dc.gen_speak(acid,'segueListagem(ITEMS)',[conversas],"Segue mais")+":\n"
        resp+=printingIntents(acid,intentlist)
        ac.print_dbg('intencoes',"printingIntents= ",resp)
    else:
        resp=dc.gen_speak(acid,'fimListagem(ITEMS)',[conversas], "Sem mais") 
    return resp
    

def respostaNao_helping_intents(acid,username,userinput,matches):
    return dc.gen_speak(acid,'pareiListagem')+'. '+dc.gen_speak(acid,'sePrecisarAjuda')
    

def printingIntents(acid,intentlist):
    resp = ""
    while intentlist:
        intent = intentlist.pop(0)
        intfunmod=intent.split('@')
        intentname = intfunmod[0]
        intentmode = intfunmod[1] if len(intfunmod)>1 else None
        intentphrase=re.findall('[a-zA-Z][^A-Z]*',intentname)
        resp+=" ".join(intentphrase).casefold()
        if intentmode!=None:
            resp+=" @ "+intentmode.casefold().replace('-', ' ')
        resp+="\n"
        ac.print_dbg('funaux',"processed intent: ", intent)
        # VR chat messages are limited to 1023 chars, using a low limit to avoid problems
        if intentlist==[]:
            resp+=dc.gen_speak(acid,'fimListagem(ITEMS)',["conversas"],"Acabou")            
        elif len(resp)>500:
            resp+=dc.gen_speak(acid,'querVerMaisConversas')
            dc.set_next_topic(acid,'helping-intents',intentlist.copy())
            intentlist=[]
    return resp

    
def ajudaConversas(acid,username,userinput,matches):
    ac.print_dbg('intencoes',"matches=",matches)
    if matches==None or matches==[]:
        intentlist = dc.get_intent_list(acid)
    else:
        intentlist = dc.get_intent_list(acid,matches[0])
    resp = dc.gen_speak(acid,'saudacoesIniciais')+".\n"
    conversas = random.choice(["diálogos","conversas"])
    resp+=printingIntents(acid,intentlist)
    return resp
    
def ajudaSobreConversa(acid,username,userinput,matches):
    if len(matches)<1:
        return dc.gen_speak(acid,'digaQualConversa')
    intentwords = matches[0].casefold().split(' ')
    intent = intentwords[0]
    if len(intentwords)>1:
        for i in range(1,len(intentwords)):
            intent += intentwords[i].casefold().capitalize()
    patts = dc.get_patterns_intent_list(acid,intent)
    if patts==None or len(patts)==0:
        return dc.gen_speak(acid,'semPadraoFrase')
    resp= dc.gen_speak(acid,'tenhoPadroesFrase')+":\n"
    for patt in patts:
        resp+=tokenPatternToWordsPattern(patt)+"\n"
    return resp
    
def logOut(acid,username,userinput,matches):
    AtorAprendiz.stop()
    resp=random.choice(["OK, vou fazer logout e sair deste mundo", "Tchau, vou fazer logout"])
    return resp

def enablePrDeb(acid,username,userinput,matches):
    ac.enable_print_dbg()
    return "OK, enabled DEBUG printing"

def disablePrDeb(acid,username,userinput,matches):
    ac.disable_print_dbg()
    return "OK, disabled DEBUG printing"

def setPrDebType(acid,username,userinput,matches):
    ac.set_print_dbg_filter(matches[0])
    return "OK, set DEBUG print type to: "+matches[0]

