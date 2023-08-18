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
#   Module:     IntencoesAtendente
#   Purpose:    Exemplo de modulo que implementa as intencoes das
#               conversas/dialogos do ator atendente simples
#   Author:     João Carlos Gluz - 2020-2022
#
###############################################################
###############################################################

""" Modulo IntencoesAtendente - Exemplo de modulo que implementa as intencoes
        das conversas/dialogos do ator atendente simples """
import random
import clr
import time
import re
import ActorController as ac
import DialogController as dc
import AuxiliaryFunctions as af
import AtorAtendente as aa


###########################
# Funcoes Auxiliares
###########################

def maybe(threshold):
    if random.random()>threshold:
        return False
    return True

def small_delay():
    delay = random.choice( [0.5, 1.0, 1.5, 2.0, 3.0, 4.0])
    time.sleep(delay)

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
    
def podeAtender(acid,username):
    atendendo=ac.remember(acid,['atendendo-usuario'])
    if atendendo==None or atendendo==[]:
        # Livre para atender
        ac.record(acid,['atendendo-usuario',username])
        myname=ac.remember(acid,['character-name'])
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'sou(FULANO)',[myname[1]]))
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'souAtendenteDaqui'))
        return True
        
    if atendendo[1]==username:
        # Segue atendimento do mesmo usuario
        return True
        
    # Esta' atendendo outro usuario
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'aindaEstouAtendendo(FULANO)',
            [prefixPronTrat(acid,atendendo[1])]))
    return False

def prefixPronTrat(acid,nome):
    genero=af.possible_gender_of_name('pt-br',nome)
    if genero=='M':
        return dc.gen_speak(acid,'senhor(NOME)',[nome]) 
    if genero=='F':
        return dc.gen_speak(acid,'senhora(NOME)',[nome])
    return nome

def limpaDadosAtendimento(acid): 
    ac.forget(acid,['atendendo-usuario'])
    ac.forget(acid,['paciente-informado'])
    ac.forget(acid,['medico-informado'])
    ac.forget(acid,['exame-informado'])
    ac.forget(acid,['horario-informado'])
  
###################################
# Mapeamento das Intencoes em Acoes
###################################

def saudacoes(acid,username,userinput,matches):
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'respostaSaudacoes'))
    atendendo=ac.remember(acid,['atendendo-usuario'])
    if atendendo==None or atendendo==[]:
        # Livre para atender
        ac.record(acid,['atendendo-usuario',username])
        myname=ac.remember(acid,['character-name'])
        ac.start_play(acid,'std_anim','salute')
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'sou(FULANO)',[myname[1]]))
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'souAtendenteDaqui'))
        time.sleep(1.5)
        ac.stop_play(acid,'std_anim','salute')
        small_delay()
        return dc.gen_speak(acid,'emQuePossoAtender')
        
    if atendendo[1]==username:
        # Segue atendimento do mesmo usuario
        small_delay()
        return dc.gen_speak(acid,'ok')
        
    # Esta' atendendo outro usuario
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'aindaEstouAtendendo(FULANO)',
            [prefixPronTrat(acid,atendendo[1])]))
    small_delay()
    return dc.gen_speak(acid,'espereUmPouco')


#def unknownUserInput(acid,username,userinput,matches):
#    return saudacoes(acid,username,userinput,matches)
    
def vouAoConsultorio(acid,username,userinput,matches):
    nomeformal = ac.remember(acid,['known-character-formal-name',username])
    small_delay()
    if nomeformal!=None:
        return dc.gen_speak(acid,'ok(COMPL)',nomeformal[2])
    return dc.gen_speak(acid,'ok')

    
def meChameSeHouverPacientes(acid,username,userinput,matches):
    nomeformal = ac.remember(acid,['known-character-formal-name',username])
    small_delay()
    if nomeformal!=None:
        return dc.gen_speak(acid,'ok(COMPL)',nomeformal[2])
    return dc.gen_speak(acid,'ok')

def mePassePacientes(acid,username,userinput,matches):
    tratform_med = ac.remember(acid,['known-character-formal-name',username])
    small_delay()
    if tratform_med!=None:
        ac.say(acid,dc.gen_speak(acid,'ok(COMPL)',tratform_med[2]))
    else:
        ac.say(acid,dc.gen_speak(acid,'ok'))
    esperando = ac.remember(acid,['consulta'])
    small_delay()            
    if esperando!=None:
        ac.forget(acid,esperando)
        tratform_pac= ac.remember(acid,['known-character-formal-name',esperando[1]])
        if tratform_pac!=None:
            return dc.gen_speak(acid,'podeVirBuscar(COMPL)','o paciente '+tratform_pac[2])
        return dc.gen_speak(acid,'podeVirBuscar(COMPL)','o paciente '+esperando[2])
    return dc.gen_speak(acid,'ninguemEsperandoConsulta')

def agendarConsulta(acid,username,userinput,matches):
    if not podeAtender(acid,username):
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    dc.set_next_topic(acid,'agendando-consulta',None)
    paciente = ac.remember(acid,['paciente-informado'])
    if paciente!=None and paciente!=[]:
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'obrigado(COMPL)',[prefixPronTrat(acid,paciente[1])]))
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'okAgendarConsulta'))
        ac.say(acid,dc.gen_speak(acid,'agoraPreciso(ALGO)',['do nome do médico ou da médica']))
        dc.set_mode(acid,'modo-informa-medico')
        small_delay()
        return dc.gen_speak(acid,'perguntaMedico')
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'okAgendarConsulta'))
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'masPrimeiroPreciso(ALGO)',['o seu nome']))
    dc.set_mode(acid,'modo-informa-nome')
    small_delay()
    return dc.gen_speak(acid,'perguntaNome')


def agendarExame(acid,username,userinput,matches):
    if not podeAtender(acid,username):
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    dc.set_next_topic(acid,'agendando-exame',None)
    paciente = ac.remember(acid,['paciente-informado'])
    if paciente!=None and paciente!=[]:
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'obrigado(COMPL)',[prefixPronTrat(acid,paciente[1])]))
        ac.say(acid,dc.gen_speak(acid,'agoraPreciso(ALGO)',['do nome do exame']))
        dc.set_mode(acid,'modo-informa-exame')
        small_delay()
        return dc.gen_speak(acid,'perguntaExame')
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'okAgendarExame'))
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'masPrimeiroPreciso(ALGO)',['o seu nome']))
    dc.set_mode(acid,'modo-informa-nome')
    small_delay()
    return dc.gen_speak(acid,'perguntaNome') 

def fazerConsulta(acid,username,userinput,matches):
    if not podeAtender(acid,username):
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    dc.set_next_topic(acid,'fazendo-consulta',None)
    paciente = ac.remember(acid,['paciente-informado'])
    if paciente!=None and paciente!=[]:
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'obrigado(COMPL)',[prefixPronTrat(acid,paciente[1])]))
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'okConsultarMedico'))
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'agoraPreciso(ALGO)',['do nome do seu médico ou médica']))
        dc.set_mode(acid,'modo-informa-medico')
        small_delay()
        return dc.gen_speak(acid,'perguntaMedico')
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'okConsultarMedico'))
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'masPrimeiroPreciso(ALGO)',['o seu nome']))
    dc.set_mode(acid,'modo-informa-nome')
    small_delay()
    return dc.gen_speak(acid,'perguntaNome')

def consultarPacienteComMedico(acid,username,userinput,matches):
    if podeAtender(acid,username):
        paciente = matches[0]
        medico = matches[1]
        small_delay()
        agradecimento = dc.gen_speak(acid,'ok') if maybe(0.7) else dc.gen_speak(acid,'obrigado')
        ac.say(acid,agradecimento)
        ac.record(acid,['consulta',username,paciente,medico])
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'falaSim'))
        ac.start_play(acid,'std_anim','type')
        time.sleep(2.5)
        ac.stop_play(acid,'std_anim','type')
        ac.say(acid,dc.gen_speak(acid,'podeSeSentar'))
        limpaDadosAtendimento(acid)
        small_delay()
        return dc.gen_speak(acid,'espereChamarConsulta')
    small_delay()
    return dc.gen_speak(acid,'espereUmPouco')


def fazerExame(acid,username,userinput,matches):
    if not podeAtender(acid,username):
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    dc.set_next_topic(acid,'fazendo-exame',None)
    paciente = ac.remember(acid,['paciente-informado'])
    if paciente!=None and paciente!=[]:
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'obrigado(COMPL)',[prefixPronTrat(acid,paciente[1])]))
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'okFazerExame'))
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'agoraPreciso(ALGO)',['do nome do exame']))
        dc.set_mode(acid,'modo-informa-exame')
        small_delay()
        return dc.gen_speak(acid,'perguntaMedico')
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'okFazerExame'))
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'masPrimeiroPreciso(ALGO)',['o seu nome']))
    dc.set_mode(acid,'modo-informa-nome')
    small_delay()
    return dc.gen_speak(acid,'perguntaNome')
    
def fazerExameDeTipoComPaciente(acid,username,userinput,matches):
    if not podeAtender(acid,username):
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    paciente = matches[0]
    exame = matches[1]
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'ok'))
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'obrigado(COMPL)',[prefixPronTrat(acid,paciente)]))
    ac.record(acid,['exame',username,paciente,exame])
    ac.start_play(acid,'std_anim','type')
    time.sleep(2.5)
    ac.stop_play(acid,'std_anim','type')
    ac.say(acid,dc.gen_speak(acid,'podeSeSentar'))
    limpaDadosAtendimento(acid)
    small_delay()
    return dc.gen_speak(acid,'espereChamarExame')
    
def informaNome(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    if topic=='agendando-consulta':
        return informaNome_agendando_consulta(acid,username,userinput,matches)
    if topic=='fazendo-consulta':
        return informaNome_fazendo_consulta(acid,username,userinput,matches)
    if topic=='agendando-exame':
        return informaNome_agendando_exame(acid,username,userinput,matches)
    if topic=='fazendo-exame':
        return informaNome_fazendo_exame(acid,username,userinput,matches)
    if not podeAtender(acid,username):
        dc.keep_topic(acid)
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    ac.record(acid,['paciente-informado',matches[0]])
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'obrigado(COMPL)',[prefixPronTrat(acid,matches[0])]))
    small_delay()
    return dc.gen_speak(acid,'emQuePossoAtender')


def informaNome_agendando_consulta(acid,username,userinput,matches):
    dc.keep_topic(acid)
    if not podeAtender(acid,username):
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    ac.record(acid,['paciente-informado',matches[0]])
    small_delay()
    agradecimento = dc.gen_speak(acid,'ok') if maybe(0.7) else dc.gen_speak(acid,'obrigado')
    ac.say(acid,agradecimento)
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'agoraPreciso(ALGO)',['do nome do médico ou da médica']))
    dc.set_mode(acid,'modo-informa-medico')
    small_delay()
    return dc.gen_speak(acid,'perguntaMedico')


def informaNome_fazendo_consulta(acid,username,userinput,matches):
    dc.keep_topic(acid)
    if not podeAtender(acid,username):
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    ac.record(acid,['paciente-informado',matches[0]])
    small_delay()
    agradecimento = dc.gen_speak(acid,'ok') if maybe(0.7) else dc.gen_speak(acid,'obrigado')
    ac.say(acid,agradecimento)
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'agoraPreciso(ALGO)',['do nome do médico ou da médica']))
    dc.set_mode(acid,'modo-informa-medico')
    small_delay()
    return dc.gen_speak(acid,'perguntaMedico')


def informaNome_agendando_exame(acid,username,userinput,matches):
    dc.keep_topic(acid)
    if not podeAtender(acid,username):
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    ac.record(acid,['paciente-informado',matches[0]])
    small_delay()
    agradecimento = dc.gen_speak(acid,'ok') if maybe(0.7) else dc.gen_speak(acid,'obrigado')
    ac.say(acid,agradecimento)
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'agoraPreciso(ALGO)',['do nome do exame']))
    dc.set_mode(acid,'modo-informa-exame')
    small_delay()
    return dc.gen_speak(acid,'perguntaExame')


def informaNome_fazendo_exame(acid,username,userinput,matches):
    dc.keep_topic(acid)
    if not podeAtender(acid,username):
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    ac.record(acid,['paciente-informado',matches[0]])
    small_delay()
    agradecimento = dc.gen_speak(acid,'ok') if maybe(0.7) else dc.gen_speak(acid,'obrigado')
    ac.say(acid,agradecimento)
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'agoraPreciso(ALGO)',['do nome do exame']))
    dc.set_mode(acid,'modo-informa-exame')
    small_delay()
    return dc.gen_speak(acid,'perguntaExame')


def informaMedico(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    if topic=='agendando-consulta':
        return informaMedico_agendando_consulta(acid,username,userinput,matches)
    if topic=='fazendo-consulta':
        return informaMedico_fazendo_consulta(acid,username,userinput,matches)
    if not podeAtender(acid,username):
        dc.keep_topic(acid)
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    ac.record(acid,['medico-informado',matches[0]])
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'ok(COMPL)',[matches[0]+" é seu médico"]))
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'masAgora'))
    small_delay()
    resp = dc.gen_speak(acid,'emQuePossoAtender')
    return resp


def informaMedico_agendando_consulta(acid,username,userinput,matches):
    dc.keep_topic(acid)
    if not podeAtender(acid,username):
        dc.keep_topic(acid)
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    ac.record(acid,['medico-informado',matches[0]])
    small_delay()
    agradecimento = dc.gen_speak(acid,'ok') if maybe(0.7) else dc.gen_speak(acid,'obrigado')
    ac.say(acid,agradecimento)
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'porFimPreciso(ALGO)',['do horário e dia da consulta']))
    dc.set_mode(acid,'modo-escolhe-horario')
    small_delay()
    return dc.gen_speak(acid,'escolheHoraDiaAgendamento')


def informaMedico_fazendo_consulta(acid,username,userinput,matches):
    if not podeAtender(acid,username):
        dc.keep_topic(acid)
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    ac.record(acid,['medico-informado',matches[0]])
    small_delay()
    agradecimento = dc.gen_speak(acid,'ok') if maybe(0.7) else dc.gen_speak(acid,'obrigado')
    ac.say(acid,agradecimento)
    paciente = ac.remember(acid,['paciente-informado'])
    medico = ac.remember(acid,['medico-informado'])
    ac.record(acid,['consulta',username,paciente[1],medico[1]])
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'falaSim'))
    ac.start_play(acid,'std_anim','type')
    time.sleep(2.5)
    ac.stop_play(acid,'std_anim','type')
    ac.say(acid,dc.gen_speak(acid,'podeSeSentar'))
    limpaDadosAtendimento(acid)
    small_delay()
    return dc.gen_speak(acid,'espereChamarConsulta')


def informaTipoExame(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    if topic=='agendando-exame':
        return informaTipoExame_agendando_exame(acid,username,userinput,matches)
    if topic=='fazendo-exame':
        return informaTipoExame_fazendo_exame(acid,username,userinput,matches)
    if not podeAtender(acid,username):
        dc.keep_topic(acid)
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    ac.record(acid,['exame-informado',matches[0]])
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'ok(COMPL)',["vai fazer o exame de "+matches[0]]))
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'masAgora'))
    small_delay()
    return dc.gen_speak(acid,'emQuePossoAtender')


def informaTipoExame_agendando_exame(acid,username,userinput,matches):
    dc.keep_topic(acid)
    if not podeAtender(acid,username):
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    ac.record(acid,['exame-informado',matches[0]])
    small_delay()
    agradecimento = dc.gen_speak(acid,'ok') if maybe(0.7) else dc.gen_speak(acid,'obrigado')
    ac.say(acid,agradecimento)
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'porFimPreciso(ALGO)',['do horário e dia do exame']))
    dc.set_mode(acid,'modo-escolhe-horario')
    small_delay()
    return dc.gen_speak(acid,'escolheHoraDiaAgendamento')
    
def informaTipoExame_fazendo_exame(acid,username,userinput,matches):
    if not podeAtender(acid,username):
        dc.keep_topic(acid)
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    ac.record(acid,['exame-informado',matches[0]])
    small_delay()
    agradecimento = dc.gen_speak(acid,'ok') if maybe(0.7) else dc.gen_speak(acid,'obrigado')
    ac.say(acid,agradecimento)
    paciente = ac.remember(acid,['paciente-informado'])
    exame = ac.remember(acid,['exame-informado'])
    ac.record(acid,['exame',paciente[1],exame[1]])
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'falaSim'))
    ac.start_play(acid,'std_anim','type')
    time.sleep(2.5)
    ac.stop_play(acid,'std_anim','type')
    ac.say(acid,dc.gen_speak(acid,'podeSeSentar'))
    limpaDadosAtendimento(acid)
    small_delay()
    return dc.gen_speak(acid,'espereChamarExame')


def informaHorario(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    if topic=='agendando-consulta':
        return informaHorario_agendando_consulta(acid,username,userinput,matches)
    if topic=='agendando-exame':
        return informaHorario_agendando_exame(acid,username,userinput,matches)
    if not podeAtender(acid,username):
        dc.keep_topic(acid)
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    small_delay()
    agradecimento = dc.gen_speak(acid,'ok') if maybe(0.7) else dc.gen_speak(acid,'obrigado')
    ac.say(acid,agradecimento)
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'masAgora'))
    small_delay()
    return dc.gen_speak(acid,'emQuePossoAtender')

    
def informaHorario_agendando_consulta(acid,username,userinput,matches):
    if not podeAtender(acid,username):
        dc.keep_topic(acid)
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    ac.record(acid,['horario-informado',matches[0]])
    small_delay()
    agradecimento = dc.gen_speak(acid,'ok') if maybe(0.7) else dc.gen_speak(acid,'obrigado')
    ac.say(acid,agradecimento)
    paciente = ac.remember(acid,['paciente-informado'])
    horario = ac.remember(acid,['horario-informado'])
    medico = ac.remember(acid,['medico-informado'])
    ac.record(acid,['agendamento-consulta',username,paciente[1],medico[1],horario[1]])
    ac.print_dbg('atendente','agendamento-consulta(',paciente[1],medico[1],horario[1],')')
    ac.forget(acid,['medico-informado'])
    ac.forget(acid,['horario-informado'])
    ac.start_play(acid,'std_anim','type')
    time.sleep(2.5)
    ac.stop_play(acid,'std_anim','type')
    ac.say(acid,dc.gen_speak(acid,'consultaMarcada(QUAL;QUANDO)',[medico[1],horario[1]]))
    ac.record(acid,['atendendo-paciente',paciente[1]])
    ac.set_next_topic(acid,'segue-atendimento')
    small_delay()
    return dc.gen_speak(acid,'precisaAlgoMais')

    
def informaHorario_agendando_exame(acid,username,userinput,matches):
    if not podeAtender(acid,username):
        dc.keep_topic(acid)
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    ac.record(acid,['horario-informado',matches[0]])
    small_delay()
    agradecimento = dc.gen_speak(acid,'ok') if maybe(0.7) else dc.gen_speak(acid,'obrigado')
    ac.say(acid,agradecimento)
    paciente = ac.remember(acid,['paciente-informado'])
    horario = ac.remember(acid,['horario-informado'])
    exame = ac.remember(acid,['exame-informado'])
    ac.record(acid,['agendamento-exame',username,paciente[1],exame[1],horario[1]])
    ac.print_dbg('atendente','agendamento-exame(',paciente[1],exame[1],horario[1],')')
    ac.forget(acid,['exame-informado'])
    ac.forget(acid,['horario-informado'])
    ac.start_play(acid,'std_anim','type')
    time.sleep(2.5)
    ac.stop_play(acid,'std_anim','type')
    ac.say(acid,dc.gen_speak(acid,'exameMarcado(QUAL;QUANDO)',[exame[1],horario[1]]))
    ac.record(acid,['atendendo-paciente',paciente[1]])
    ac.set_next_topic(acid,'segue-atendimento',str(time.time()))
    dc.set_mode(acid,'modo-segue-atendimento')
    small_delay()
    return dc.gen_speak(acid,'precisaAlgoMais')

    
def qualquerResposta(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    if topic=='segue-atendimento':
        if not podeAtender(acid,username):
            if (time.time() - float(dc.get_topic_content(acid)))>15.0:
# Usuario antigo nao respondeu por ao menos 15 segundos se quer seguir atendimento
# Passa para o novo atendimento
                limpaDadosAtendimento(acid)
                ac.record(acid,['atendendo-usuario',username])
                myname=ac.remember(acid,['character-name'])
                small_delay()
                ac.say(acid,dc.gen_speak(acid,'sou(FULANO)',[myname[1]]))
                small_delay()
                ac.say(acid,dc.gen_speak(acid,'souAtendenteDaqui'))
                small_delay()
                return dc.gen_speak(acid,'emQuePossoAtender')
            dc.keep_topic(acid)
            dc.keep_mode(acid)
            small_delay()
            return dc.gen_speak(acid,'espereUmPouco')
    dc.keep_topic(acid)
    dc.keep_mode(acid)
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'naoEntendi'))
    return dc.gen_speak(acid,'respondaSimOuNao')



def confirma(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    if topic=='segue-atendimento': 
        return confirma_segue_atendimento(acid,username,userinput,matches)
    small_delay()
    return dc.gen_speak(acid,'duvidaSim')   

def confirma_segue_atendimento(acid,username,userinput,matches):
    small_delay()
    if podeAtender(acid,username):
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'falaSim'))
        return dc.gen_speak(acid,'emQueMaisPossoAtender')
    # Um outro usuario comecou a conversar
    if (time.time() - float(dc.get_topic_content(acid)))<15.0:
        # Porem ainda esta' esperando pela resposta do usuario antigo
        dc.keep_topic(acid)
        small_delay()
        return dc.gen_speak(acid,'espereUmPouco')
    # Usuario antigo nao respondeu por ao menos 15 segundos se quer 
    # seguir com o atendimento, entao passa para o novo atendimento
    limpaDadosAtendimento(acid)
    ac.record(acid,['atendendo-usuario',username])
    myname=ac.remember(acid,['character-name'])
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'sou(FULANO)',[myname[1]]))
    small_delay()
    ac.say(acid,dc.gen_speak(acid,'souAtendenteDaqui'))
    small_delay()
    return dc.gen_speak(acid,'emQuePossoAtender')

def recusa(acid,username,userinput,matches):
    topic = dc.get_topic_name(acid)
    small_delay()
    if topic=='segue-atendimento': 
        if not podeAtender(acid,username):
            if (time.time() - float(dc.get_topic_content(acid)))>15.0:
# Usuario antigo nao respondeu por ao menos 15 segundos se quer seguir atendimento
# Passa para o novo atendimento
                limpaDadosAtendimento(acid)
                ac.record(acid,['atendendo-usuario',username])
                myname=ac.remember(acid,['character-name'])
                small_delay()
                ac.say(acid,dc.gen_speak(acid,'sou(FULANO)',[myname[1]]))
                small_delay()
                ac.say(acid,dc.gen_speak(acid,'souAtendenteDaqui'))
                small_delay()
                return dc.gen_speak(acid,'emQuePossoAtender')
        limpaDadosAtendimento(acid)
        small_delay()
        ac.say(acid,dc.gen_speak(acid,'falaSim'))
        resp= dc.gen_speak(acid,'saudacoesFinais')
    else:
        resp= dc.gen_speak(acid,'naoEntendi')    
    small_delay()
    return resp


def ajudaConversas(acid,username,userinput,matches):
    ac.print_dbg('intencoes',"matches=",matches)
    if matches==None or matches==[]:
        intentlist = dc.get_intent_list(acid)
    else:
# matches[0] deve ter a CONVERSA que se quer ajuda
        intentlist = dc.get_intent_list(acid,matches[0])
    resp = dc.gen_speak(acid,'saudacoesIniciais')+".\n"
    conversas = random.choice(["diálogos","conversas"])
    resp+=printingIntents(acid,intentlist)
    return resp
    
def ajudaBatePapos(acid,username,userinput,matches):
    resp = dc.gen_speak(acid,'saudacoesIniciais')+".\n"
    batepapos = random.choice(["bate-papos","chats"])
    resp+=dc.gen_speak(acid,'reconhecoSeguintes(COISAS)',[batepapos],"Reconheço chats")+":\n"
    prodrules = dc.get_prod_rules(acid)
    resp+=printingProdRules(acid,prodrules)
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
    
def adeus(acid,username,userinput,matches):
    resp=dc.gen_speak(acid,'ateLogo')
    return resp
    
def logOut(acid,username,userinput,matches):
    aa.stop()
    resp=random.choice(["OK, vou fazer logout e sair deste mundo", "Tchau, vou fazer logout"])
    return resp
