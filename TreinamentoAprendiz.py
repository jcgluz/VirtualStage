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
#   Purpose:    Exemplo de modulo que implementa as intencoes de 
#               por trás de conversas/dialogos para treinamento e
#               aprendizagem do ator aprendiz (trainee actor)
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

""" Modulo IntencoesTreinamentoAprendiz - Exemplo de modulo que implementa as intencoes de
        treinamento das conversas do ator aprendiz (apprentice actor) """

import random
import clr
import time
import re
import uuid
import math
import nltk
import ActorController as ac
import DialogController as dc
import AtorAprendiz
import AuxiliaryFunctions as af

#####################################
# Intention functions for
# learning QUESTION-ANSWERS
#####################################

def entreModoAprenderPerguntaResposta(acid,username,userinput,matches):
    dc.set_mode(acid,'modo-aprender-pergunta')
    resp=dc.gen_speak(acid,'falePergunta') 
    return resp


def entreComPergunta(acid,username,userinput,matches):
    if len(matches)==0:
        resp=dc.gen_speak(acid,'naoFalouPergunta')
    else:
        dc.set_next_topic(acid,'learning-question',matches[0])
        dc.set_mode(acid,'modo-aprender-resposta')
        resp=dc.gen_speak(acid,'vouLembrarPergunta(QUESTAO)',[matches[0]],"Aprendi pergunta")+"\n"    
        resp+=dc.gen_speak(acid,'informeResposta')+":"
    return resp


def wordsToTokenString(wrds):
    tklst = nltk.word_tokenize(wrds)
    return "".join("<" + wrd + ">" for wrd in tklst)


def wordsPatternToTokenPattern(wrdpatt):
    patt = wordsToTokenString(wrdpatt)
    patt = re.sub(r'<\[><([^>]+?)><\]>',r'<\1>?',patt)
    patt = patt.replace('<_><*>','<.+>')
    patt = patt.replace('_','&%')
    patt = patt.replace('<...>','_')
    patt = patt.replace('&%','.')
    patt = patt.replace('><*></','.*|')
    patt = patt.replace('><*><','.*><')
    patt = patt.replace('/','|')
    patt = patt.replace('<(>','(')
    patt = patt.replace('<)>',')')
    patt = patt.replace('<+>','+')
    return patt


def respostaSim_continue_learning_question_answer(acid,username,userinput,matches):
    ac.print_dbg('intencoes',"continue-learning-question-answer")
    dc.set_mode(acid,'modo-aprender-pergunta')
    return dc.gen_speak(acid,'faleOutraPergunta')+":" 
    
def respostaNao_continue_learning_question_answer(acid,username,userinput,matches):
    return dc.gen_speak(acid,'chegaDeAprender')
      
def entreComResposta(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    question = dc.get_topic_content(acid)
    if topic!='learning-question' or question==None:
        antes=dc.gen_speak(acid,'sinonAntes')
        resp=dc.gen_speak(acid,'naoFalouPergunta')+" "+antes
        return resp
    if len(matches)==0:
        resp=dc.gen_speak(acid,'naoFalouResposta')
        return resp
    patt = wordsPatternToTokenPattern(question)
    ac.print_dbg('dlgctl','question=',question,' patt=',patt,' answer=',matches[0])
    dc.add_hear_talk_rule(acid,[patt],matches[0])
    resp=dc.gen_speak(acid,'aprendiPerguntaResposta(QUESTAO;RESP)',[question,matches[0]],"Aprendi bate-papo")+"\n"
    resp+=dc.gen_speak(acid,'querEnsinarMaisBatePapos')
    dc.set_next_topic(acid,'continue-learning-question-answer')
    return resp


def aprendaPergunta(acid,username,userinput,matches):
    if len(matches)==0:
        resp=dc.gen_speak(acid,'naoFalouPergunta')
    else:
        dc.set_next_topic(acid,'learning-question',matches[0])
        resp=dc.gen_speak(acid,'vouLembrarPergunta(QUESTAO)',[matches[0]],"Aprendi pergunta")+"\n"    
        resp+=dc.gen_speak(acid,'informeResposta')+":"
    return resp


def aprendaResposta(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    question = dc.get_topic_content(acid)
    if topic!='learning-question' or question==None:
        return dc.gen_speak(acid,'naoFalouPergunta')+" "+dc.gen_speak(acid,'sinonAntes')
    if len(matches)==0:
        return dc.gen_speak(acid,'naoFalouResposta')
    patt = wordsPatternToTokenPattern(question)
    ac.print_dbg('dlgctl','question=',question,' patt=',patt,' answer=',matches[0])
    dc.add_hear_talk_rule(acid,[patt],matches[0])
    resp=dc.gen_speak(acid,'aprendiPerguntaResposta(QUESTAO;RESP)',[question,matches[0]],"Aprendi bate-papo")+"\n"    
    return resp

            
#####################################
# Intention functions for learning 
# information about OBJECTS
#####################################

def _getObjID(acid):
    topic = dc.get_topic_name(acid)
    objid = dc.get_topic_content(acid)
    if topic!='obj-selected' or objid==None:
        return None
    # If object is still not known, register it as a known object
    kobj = ac.remember(acid,['known-obj',objid])
    if kobj==None or len(kobj)==0:
        ac.record(acid,['known-obj',objid])
    return objid
        
def entreModoAprenderInfoObjeto(acid,username,userinput,matches):
    objid = _getObjID(acid)
    if objid==None:
        return dc.gen_speak(acid,'naoVejoObjeto')+"\n"+dc.gen_speak(acid,'podeIndicarDeNovo') 
    dc.keep_topic(acid)
    dc.set_mode(acid,'modo-aprender-info-obj')
    return dc.gen_speak(acid,'faleSobreObjeto') 


def aprendaAtributoObjeto(acid,username,userinput,matches):
    objid = _getObjID(acid)
    if objid==None:
        return dc.gen_speak(acid,'naoVejoObjeto')+"\n"+dc.gen_speak(acid,'podeIndicarDeNovo') 
    ac.forget(acid,['obj-attr',objid,matches[1]])
    ac.record(acid,['obj-attr',objid,matches[1],matches[2],matches[0]+" "+matches[1]])
    dc.keep_topic(acid)
    dc.keep_mode(acid)
    return dc.gen_speak(acid,'aprendiInfoObjeto(PROP;VAL)',[matches[0]+" "+matches[1],matches[2]])


def aprendaNomeObjeto(acid,username,userinput,matches):
    objid = _getObjID(acid)
    if objid==None:
        return dc.gen_speak(acid,'naoVejoObjeto')+"\n"+dc.gen_speak(acid,'podeIndicarDeNovo') 
    # Register new  (or update) information about known object
    ac.forget(acid,['obj-name',objid])
    ac.record(acid,['obj-name',objid,matches[0],"o nome"])
    dc.keep_topic(acid)
    dc.keep_mode(acid)
    return dc.gen_speak(acid,'aprendiInfoObjeto(PROP;VAL)',["o nome",matches[0]])



def aprendaDescricaoObjeto(acid,username,userinput,matches):
    objid = _getObjID(acid)
    if objid==None:
        return dc.gen_speak(acid,'naoVejoObjeto')+"\n"+dc.gen_speak(acid,'podeIndicarDeNovo') 
    # Register new  (or update) information about known object
    ac.forget(acid,['obj-descr',objid])
    ac.record(acid,['obj-descr',objid,matches[0],"a descrição"])
    dc.keep_topic(acid)
    dc.keep_mode(acid)
    return dc.gen_speak(acid,'aprendiInfoObjeto(PROP;VAL)',["a descrição",matches[0]])


def aprendaUsoObjeto(acid,username,userinput,matches):
    objid = _getObjID(acid)
    if objid==None:
        return dc.gen_speak(acid,'naoVejoObjeto')+"\n"+dc.gen_speak(acid,'podeIndicarDeNovo') 
    # Register new  (or update) information about known object
    ac.forget(acid,['obj-use',objid])
    o_uso = random.choice(["o uso","a utilidade","a serventia"])
    ac.record(acid,['obj-use',objid,matches[0],o_uso])
    dc.keep_topic(acid)
    dc.keep_mode(acid)
    return dc.gen_speak(acid,'aprendiInfoObjeto(PROP;VAL)',[o_uso,matches[0]])


def aprendaImportanciaObjeto(acid,username,userinput,matches,forget):
    objid = _getObjID(acid)
    if objid==None:
        return dc.gen_speak(acid,'naoVejoObjeto')+"\n"+dc.gen_speak(acid,'podeIndicarDeNovo') 
    dc.keep_topic(acid)
    dc.keep_mode(acid)
    a_importancia = random.choice(['o grau de importância','o grau de relevância']) 
    val = af.importance_to_value('pt-br',matches[0])
    if val==None:
        desse_obj=random.choice(["desse objeto", "dessa coisa", "disso"])
        return dc.gen_speak(acid,'naoEntendiQueDisseSobre(PROP;COISA)',[a_importancia,desse_obj])
    # Clear previous memories and add new (or update) information about known object
    ac.forget(acid,['obj-importance',objid])
    ac.record(acid,['obj-importance',objid,val,a_importancia])
    return dc.gen_speak(acid,'aprendiInfoObjeto(PROP;VAL)',
                [a_importancia+" (em uma escala de 0 a 5)",val])



#####################################
# Intention functions for learning 
# information about PLACES
#####################################


def _getPlaceID(acid,username):
    topic = dc.get_topic_name(acid)
    place = dc.get_topic_content(acid)
    if topic=='place-selected':
        # The place was already a conversation topic, only get its ID
        dc.keep_topic(acid)
        return place[1]
    # No place previously selected, get the position of user avatar
    avrec = ac.look_avatar_with_name(acid,username)
    if avrec==None or avrec[4]==None or avrec[5]==None:
        # Cannot found the user's avatar or its position
        return None
    # Check if the user's avatar already is in a known place
    place=af.find_place(acid,avrec[4],avrec[5])
    if place!=None:
        # The place is already known, get its ID and set
        # it as the place-selected topic
        dc.set_next_topic(acid,'place-selected', place)
        return place[1]
    # The place is unknown, register it as a new known place with X and 
    # Y coordinates of user's avatar as place's central coordinates
    place=af.learn_new_known_place(acid,'pt-br',avrec[4],avrec[5])
    # Inform the user that learned about a new known place
    ac.say(acid,dc.gen_speak(acid,'aprendiNovoLugar(X;Y)',[place[2],place[3]]))
    # Get its ID and set it as the place-selected topic
    dc.set_next_topic(acid,'place-selected', place)       
    return place[1]


def entreModoAprenderInfoLugar(acid,username,userinput,matches):
    placeid = _getPlaceID(acid,username)
    if placeid==None:
        return dc.gen_speak(acid,'naoAcheiLugar')
    dc.keep_topic(acid)
    dc.set_mode(acid,'modo-aprender-info-lugar')
    resp=dc.gen_speak(acid,'faleSobreLugar') 
    return resp

def aprendaNomeLugar(acid,username,userinput,matches):
    placeid = _getPlaceID(acid,username)
    if placeid==None:
        return dc.gen_speak(acid,'naoAcheiLugar')
    dc.keep_topic(acid)
    dc.keep_mode(acid)
    # Clear previous memories and add new information record to memory
    ac.forget(acid,['place-name',placeid])
    ac.record(acid,['place-name',placeid,matches[0],'o nome'])
    return dc.gen_speak(acid,'aprendiInfoLugar(PROP;VAL)',['o nome',matches[0]])
    

def aprendaDescricaoLugar(acid,username,userinput,matches):
    placeid = _getPlaceID(acid,username)
    if placeid==None:
        return dc.gen_speak(acid,'naoAcheiLugar')
    dc.keep_topic(acid)
    dc.keep_mode(acid)
    # Clear previous memories and add new information record to memory
    ac.forget(acid,['place-descr',placeid])
    ac.record(acid,['place-descr',placeid,matches[0],'a descrição'])
    return dc.gen_speak(acid,'aprendiInfoLugar(PROP;VAL)',['a descrição',matches[0]])


def aprendaTamanhoLugar(acid,username,userinput,matches):
    placeid = _getPlaceID(acid,username)
    if placeid==None:
        return dc.gen_speak(acid,'naoAcheiLugar')
    dc.keep_topic(acid)
    dc.keep_mode(acid)
    # Clear previous memories and add new information record to memory
    ac.forget(acid,['place-radius',placeid])
    o_raio = random.choice(["o raio desde a posição central","o tamanho desde o centro"])    
    ac.record(acid,['place-radius',placeid,matches[0],o_raio])
    return dc.gen_speak(acid,'aprendiInfoLugar(PROP;VAL)',[o_raio,matches[0]])


def aprendaImportanciaLugar(acid,username,userinput,matches):
    placeid = _getPlaceID(acid,username)
    if placeid==None:
        return dc.gen_speak(acid,'naoAcheiLugar')
    dc.keep_topic(acid)
    dc.keep_mode(acid)
    a_importancia = random.choice(['o grau de importância','o grau de relevância']) 
    val = af.importance_to_value('pt-br',matches[0])
    if val==None:
        desse_lugar=random.choice(["desse lugar", "desse local", "daqui"])
        return dc.gen_speak(acid,'naoEntendiQueDisseSobre(PROP;COISA)',[a_importancia,desse_lugar])
    # Clear previous memories and add new (or update) information about known place
    ac.forget(acid,['place-importance',placeid])
    ac.record(acid,['place-importance',placeid,val,a_importancia])
    return dc.gen_speak(acid,'aprendiInfoLugar(PROP;VAL)',
                [a_importancia+" (em uma escala de 0 a 5)",val])


def aprendaEventoLugar(acid,username,userinput,matches):
    placeid = _getPlaceID(acid,username)
    if placeid==None:
        return dc.gen_speak(acid,'naoAcheiLugar')
    dc.keep_topic(acid)
    dc.keep_mode(acid)
    # Clear previous memories and add new information record to memory
    ac.forget(acid,['place-event',placeid])
    um_evento = random.choice(["um evento","um acontecimento","uma ocorrência"])    
    ac.record(acid,['place-event',placeid,matches[0],um_evento])
    return dc.gen_speak(acid,'aprendiInfoLugar(PROP;VAL)',[um_evento,matches[0]])


def aprendaOrdemPreferenciaLugar(acid,username,userinput,matches):
    placeid = _getPlaceID(acid,username)
    if placeid==None:
        return dc.gen_speak(acid,'naoAcheiLugar')
    dc.keep_topic(acid)
    dc.keep_mode(acid)
    # Clear previous memories and add new information record to memory
    ac.forget(acid,['place-order',placeid])
    a_ordem = random.choice(["a ordem de preferência","a ordem de interesse"])    
    val = af.translate('pt-br','natnumber',matches[0],'')
    ac.record(acid,['place-order',placeid,val,a_ordem])
    return dc.gen_speak(acid,'aprendiInfoLugar(PROP;VAL)',[a_ordem,val])


def aprendaAtributoLugar(acid,username,userinput,matches):
    if (matches[0]!='a' and matches[0]!='o'):
        return dc.gen_speak(acid,'naoEntendiInfoLugar')
    placeid = _getPlaceID(acid,username)
    if placeid==None:
        return dc.gen_speak(acid,'naoAcheiLugar')
    dc.keep_topic(acid)
    dc.keep_mode(acid)
    # Clear previous memories and add new information record to memory
    ac.forget(acid,['place-attr',placeid,matches[1]])
    ac.record(acid,['place-attr',placeid,matches[1],matches[2],matches[0]+" "+matches[1]])
    return dc.gen_speak(acid,'aprendiInfoLugar(PROP;VAL)',[matches[0]+" "+matches[1],matches[2]])


#####################################
# Intention functions for learning 
# TASKS or PERFORMANCES
#####################################

def comeceAprenderTarefaComNome(acid,username,userinput,matches):
    dc.start_recording_intents(acid)
    # Assume it is a new task, generate a random unique ID for this new scene 
    taskid = str(uuid.uuid4())
    ac.record(acid,['recording-task',taskid])
    ac.record(acid,['recording-task-name',taskid,matches[0]])
    return "OK estou pronto para aprender a tarefa de "+matches[0]

    
def comeceAprenderTarefa(acid,username,userinput,matches):
    dc.start_recording_intents(acid)
    # Assume it is a new task, generate a random unique ID for this new scene 
    taskid = str(uuid.uuid4())
    ac.record(acid,['recording-task',taskid])
    ac.say(acid,"OK estou pronto para aprender uma nova tarefa")
    return "Por favor, não esqueça de me dizer o nome dessa tarefa"
 
 
def pareAprenderTarefa(acid,username,userinput,matches):
    dc.stop_recording_intents(acid)
    task=ac.remember(acid,['recording-task-name'])
    taskintents = ac.remember_all(acid,['recorded-intent'])
    ac.forget(acid,['recording-task'])
    ac.forget(acid,['recording-task-name'])
    ac.forget(acid,['recorded-intent'])
    if task==None or len(task)==0:
        ac.say(acid,"OK parei de aprender a tarefa")     
        return "Mas como você ainda não me disse o nome da tarefa, não vou lembrar mais dela"
    if taskintents==None or len(taskintents)==0:
        ac.say(acid,"OK parei de aprender a tarefa")    
        return "Mas como você não me ensinou nenhuma ação, não vou lembrar mais dela"
    ac.record(acid,['known-task',task[1]])
    ac.record(acid,['known-task-name',task[1],task[2]])
    for intent in taskintents:
        ac.record(acid,['known-task-intent',task[1]]+intent[1:-1])
    return "OK aprendi e devo lembrar de como fazer a tarefa de "+task[2]

def aprendaNomeTarefa(acid,username,userinput,matches):
    task = ac.remember(acid,['recording-task'])
    if task==None or len(task)<2:
        return "Não estou registrando nenhuma tarefa"
    ac.record(acid,['recording-task-name',task[1],matches[0]])
    return "OK vou lembrar que o nome desta tarefa é"+matches[0]
    
#####################################
# Intention functions for learning 
# information about SCENES
#####################################

def comeceAprenderAreaCenaComNome(acid,username,userinput,matches):
    # Assume it is a new scene, generate a random unique ID for this new scene 
    sceneid = str(uuid.uuid4())
    ac.forget(acid,['learning-scene'])
    ac.forget(acid,['learning-scene-name'])
    ac.forget(acid,['learned-scene-point'])
    ac.record(acid,['learning-scene',sceneid])
    ac.record(acid,['learning-scene-name',sceneid,matches[0]])
    return "OK me mostre como é a area da cena "+matches[0]

def comeceAprenderAreaCena(acid,username,userinput,matches):
    # Assume it is a new scene, generate a random unique ID for this new scene 
    sceneid = str(uuid.uuid4())
    ac.forget(acid,['learning-scene'])
    ac.forget(acid,['learning-scene-name'])
    ac.forget(acid,['learned-scene-point'])
    ac.record(acid,['learning-scene-area',sceneid])
    return "OK me mostre como é a area desta cena"

    
def aprendaPontoBordaCena(acid,username,userinput,matches):
    scenenam = ac.remember(acid,['learning-scene-name'])
    sceneinf = ac.remember(acid,['learning-scene'])
    if sceneinf==None or len(sceneinf)<2:
        return "Não estou registrando informações ou área de nenhuma cena"
    avrec = ac.look_avatar_with_name(acid,username)
    if avrec==None or len(avrec)<6 or avrec[4]==None or avrec[5]==None:
        # Cannot found the user's avatar or its position
        return (dc.gen_speak(acid,'naoSeiOndeVoceEsta')+"\n"+
            "Não vou conseguir registrar esse ponto no limite da cena")
    ac.record(acid,['learned-scene-point',sceneinf[1],avrec[4],avrec[5]])
    sname = scenenam[2] if scenenam!=None else ''        
    return ("OK devo lembrar que o ponto onde você está, com coordenadas x="+
        avrec[4]+" e y="+avrec[5]+", também está na borda da cena "+sname)

def pareAprenderAreaCena(acid,username,userinput,matches):
    scenenam = ac.remember(acid,['learning-scene-name'])
    scenepts = ac.remember_all(acid,['learned-scene-point'])
    if scenenam==None or len(scenenam)<2:
        ac.say(acid,"OK parei de registrar como é a área da cena")     
        return ("Mas como você ainda não me disse o nome da cena,"+
            "não vou lembrar mais dela")
    if scenepts==None or len(scenepts)==0:
        ac.say(acid,"OK parei de registrar como é a área da cena")     
        return ("Mas como você ainda não me mostrou nenhum ponto que delimita a área da cena,"+
            "não vou lembrar mais dela")
    ac.record(acid,['known-scene',scenenam[1]])
    ac.record(acid,['scene-name',scenenam[1],scenenam[2]])    
    for pt in scenepts:
        ac.record(acid,['scene-point',scenenam[1],pt[2],pt[3]])
    return "OK aprendi qual a área da cena "+scenenam[2]

def aprendaNomeCena(acid,username,userinput,matches):
    sceneinf = ac.remember(acid,['learning-scene-area'])
    if sceneinf==None or len(sceneinf)<2:
        return "Não estou registrando informações ou área de nenhuma cena"
    ac.record(acid,['learning-scene-name',sceneinf[1],matches[0]])
    return "OK vou lembrar que o nome desta cena é"+matches[0]
    

   


