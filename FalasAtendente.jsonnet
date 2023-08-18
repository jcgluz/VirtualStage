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
#   File:       FalasAtendente.jsonnet 
#   Purpose:    Exemplo de arquivo JSON/JSONNET que especifica as falas usadas
#               nas conversas/dialogos do ator atendent
#   Author:     João Carlos Gluz 
#
###############################################################
###############################################################

{  
   "aindaEstouAtendendo": [
      "Ainda estou atendendo",
      "Estou atendendo outra pessoa",
      "Ainda estou atendendo outra pessoa",
      "Estou em atendimento",
      "Ainda estou em atendimento",
      "Outra pessoa está sendo atendida",
      "Outro atendimento está ocorrendo",
      "Estou fazendo outro atendimento"
   ],
   "aindaEstouAtendendo(FULANO)": [
      "Ainda estou atendendo {0}",
      "Estou atendendo {0}",
      "Estou em atendimento de {0}",
      "Estou fazendo o atendimento de {0}"
   ],
   "agoraPreciso(ALGO)": [
      "Agora preciso {0}",
      "Por favor, agora eu preciso {0}",
      "Porém, agora necessito {0}",
      "Mas agora eu preciso {0}",
      "Agora eu preciso {0}",
      "Agora o que eu preciso é {0}",
      "Mas agora eu quero {0}",
      "Agora eu quero {0}",
      "Agora o que eu quero é {0}" 
   ],
   "bomDiaTodos": [
      "Olá, bom dia para todos",
      "Oi bom dia a todos",
      "Bom dia a todos",
      "Bom dia para todos",
      "Olá pessoal, bom dia",
      "Oi pessoal, um bom dia",
      "Um bom dia para todos nós"
   ],
   "cadeMinhaCadeira": [
      "Cadê a minha cadeira?",
      "Onde está minha cadeira?",
      "Deixe ver onde está minha cadeira?",
      "Onde deixaram a minha cadeira?",
      "Tenho que achar minha cadeira",
      "Vamos ver onde está minha cadeira"
   ],
   "consultaMarcada(QUAL;QUANDO)": [
      "Ok sua consulta com {0} foi marcada para {1}",
      "Sim, sua consulta com {0} está marcada para {1}",
      "OK, o horário da consulta com {0} está agendado para {1}",
      "Sim, a consulta com {0} ficou para {1}",
      "Certo, a consulta com {0} ficou agendada para {1}"
   ],
   "duvidaNao": [
      "Não?",
      "O que não?",
      "Não porque?",
      "Como não?"
   ],
   "duvidaSim": [
      "Ok?",
      "Sim?",
      "Certo?",
      "É isso?"
   ],
   "emQuePossoAtender": [
      "Em que posso atender?",
      "O que você precisa?",
      "Em que posso ajudar?",
      "Por favor, em que posso atender?",
      "Por favor, no que posso ajudar?",
      "Por favor, o que você precisa?",
      "Você precisa marcar algum exame ou consulta?",
      "Você tem alguma consulta ou exame marcado?",
      "Em que posso te atender?",
      "Em que posso te ajudar?",
      "No que posso atender você?",
      "Em que posso lhe servir?"
   ],
   "emQueMaisPossoAtender": [
      "Em que mais posso atender?",
      "Em que mais posso ajudar?",
      "O que mais você precisa?",
      "Você precisa de mais alguma coisa? ",
      "Você precisa de algo mais? ",
      "Por favor, em que mais posso te atender?",
      "Por favor, em que mais posso te ajudar?",
      "Por favor, o que mais você precisa?",
      "Você precisa marcar mais algum exame ou consulta?",
      "Em que mais posso te atender?",
      "Em que mais posso te ajudar?",
      "No que mais posso atender você?"
   ],
   "espereUmPouco": [
      "Espere um pouco",
      "Por favor espere",
      "Espere por favor",
      "Você precisa esperar",
      "Você precisa esperar um pouco",
      "Por favor, espere sua vez",
      "Por favor, espere um pouco"
   ],
   "exameMarcado(QUAL;QUANDO)": [
      "Ok seu exame de {0} foi marcado para {1}",
      "Sim, seu exame de {0} foi marcado para {1}",
      "OK, o horário do exame {0} está agendado para {1}",
      "Sim, o exame de {0} ficou para {1}",
      "Certo, seu exame de {0} ficou agendado para {1}"
   ],
   "escolheHoraDiaAgendamento": [
      "Que horário e dia você escolhe agendar?",
      "Qual a hora e dia do agendamento que você escolhe?",
      "Que hora e dia você escolhe marcar?",
      "Qual o horário e dia que quer escolher?"
   ],
   "falaNao": [
      "Não",
      "Não deu",
      "Não foi possível",
      "Não houve como",
      "Não dá"
   ],
   "falaSim": [
      "Ok",
      "Sim",
      "Certo",
      "Tá bem",
      "Tudo bem",
      "É isso",
      "Claro que sim",
      "Tá OK",
      "Sem problemas",
      "Sim claro",
      "Tudo tranquilo"
   ],
   "informacoesUPA": [
      "Aqui é a UPA REVITEX",
      "Essa é a UPA REVITEX",
      "Estamos na UPA REVITEX",
      "Aqui é a recepção da UPA REVITEX",
      "Você está na UPA REVITEX"
   ],
   "masAgora": [
      "Mas agora",
      "Todavia agora",
      "Contudo agora",
      "No entanto agora",
      "Porém no momento",
      "Mas no momento",
      "Porém agora",
      "Contudo no momento" 
   ],
   "masPrimeiroPreciso(ALGO)": [
      "Mas, primeiro preciso {0}",
      "Por favor, primeiro preciso {0}",
      "Eu primeiro preciso {0}",
      "Porém, primeiro necessito {0}",
      "Porém, eu primeiro preciso {0}",
      "Antes de mais nada, eu preciso {0}",
      "Em primeiro lugar, eu preciso {0}",
      "Porém, eu primeiro quero {0}",
      "Antes de mais nada, eu quero {0}",
      "Em primeiro lugar, eu quero {0}",
      "Mas a primeira coisa que eu preciso é {0}" 
   ],
   "naoEntendi": [
      "Não entendi?", 
      "Não comprendi?", 
      "O que você exatamente?",
      "Não te entendi",
      "Hum?",
      "O que mesmo?",     
    ],
   "ninguemEsperandoConsulta": [
      "Não tem ninguém esperando", 
      "Ninguém está esperando consulta", 
      "Ninguém está esperando pela consulta", 
      "Ninguém esperando pela consulta", 
      "Não tem pacientes em espera",
      "Não tem pacientes esperando",
      "Não tem nenhum paciente esperando",
      "Todos pacientes já foram atendidos por agora",     
    ],
   "obrigado": [
      "Obrigado",
      "Muito obrigado",
      "Grato",
      "Beleza"  
   ],
   "obrigado(COMPL)": [
      "Muito obrigado {0}",
      "Obrigado {0}",
      "Ok obrigado {0}",
      "Sim obrigado {0}"  
   ],
   "ok": [
      "OK",
      "Sim",
      "Certo"
   ],
   "ok(COMPL)": [
      "OK, {0}",
      "Sim, {0}",
      "Certo, {0}",
      "Tá OK, {0}",
      "Tá bom, {0}"
   ],
   "okAgendarConsulta": [
      "OK, vamos agendar sua consulta",
      "Sim, vamos agendar sua consulta",
      "OK, vamos marcar a consulta",
      "Claro que sim, agora vamos marcar o atendimento",
      "Sim, então vamos agendar o atendimento",
      "OK, vamos fazer o agendamento da consulta",
      "Sim e agora vamos fazer o agendamento do atendimento",
      "OK, tranquilo agora marcamos sua consulta",
      "Sim já marcamos sua consulta"
   ],
   "okAgendarExame": [
      "OK, vamos agendar seu exame",
      "Sim, vamos agendar seu exame",
      "OK, vamos marcar o exame",
      "Claro que sim, agora vamos marcar o exame",
      "Sim, então vamos agendar o exame",
      "OK, vamos fazer o agendamento do exame",
      "Sim e agora vamos fazer o agendamento do exame",
      "OK, tranquilo agora marcamos seu exame",
      "Sim já marcamos seu exame"
   ],
   "okConsultarMedico": [
      "OK, vamos proceder para sua consulta",
      "Sim, você vai se consultar",
      "OK, vamos passar para a sua consulta",
      "Claro que sim, você vai ser atendido",
      "Sim, então vamos ver seu atendimento",
      "OK, vamos ver sua consulta",
      "Sim e agora vamos proceder para o seu atendimento",
      "OK, tranquilo agora vamos para sua consulta",
      "Sim você irá se consultar"
   ],
   "okFazerExame": [
      "OK, vamos proceder para seu exame",
      "Sim, você vai fazer o seu exame",
      "OK, você vai fazer seu exame",
      "Claro que sim, você vai fazer o exame",
      "Sim, você irá fazer o exame",
      "OK, você irá fazer o exame",
      "Sim e agora vamos proceder para o seu exame",
      "OK, tranquilo agora vamos ver seu exame",
      "Sim vamos ver seu exame"
   ],
   "perguntaDiaAgendamento": [
      "Que dia você quer agendar?",
      "Qual o dia do agendamento?",
      "Que dia quer marcar?",
      "Qual o dia que quer marcar?"
   ],
   "perguntaHorarioAgendamento": [
      "Que horário você quer agendar?",
      "Qual a hora do agendamento?",
      "Que hora quer marcar?",
      "Qual o horário que quer marcar?"
   ],
   "perguntaNome": [
      "Qual é o seu nome completo?",
      "Qual o teu nome completo?",
      "Como é seu nome completo?",
      "Por favor me informe o seu nome completo?",
      "Por favor me diga o seu nome completo?",
      "Por favor me fale o seu nome completo?",
      "Me informe o seu nome completo?",
      "Me diga o seu nome completo?",
      "Me fale o seu nome completo?",
      "Por favor me passe o seu nome completo?",
      "Me passe todo o seu nome?",
      "Me informe todo o seu nome?",
      "Diga o seu nome completo?",
      "Informe todo o seu nome?",
      "Passe o seu nome completo?",
      "Fale o seu nome completo?"
   ],
   "perguntaMedico": [
      "Por favor me fale ou repita qual o médico ou médica da sua consulta?",
      "Qual o médico ou médica que quer se consultar?",
      "Por favor me diga a médica ou médico da consulta?",
      "Por favor me diga a médica ou médico do atendimento?",
      "Por favor me diga o nome do doutor ou doutora da sua consulta?",
      "Por favor me diga o nome do doutor ou doutora do seu atendimento?",
      "Por favor me fale qual a médica ou médico da consulta?",
      "Por favor qual a médica ou médico do atendimento?",
      "Por favor me fale o nome do doutor ou doutora da sua consulta?",
      "Por favor qual o nome do doutor ou doutora do seu atendimento?",
      "Diga qual a médica ou médico da consulta?",
      "Me diga a médica ou médico do atendimento?",
      "Me diga qual o nome do doutor ou doutora da sua consulta?",
      "Me diga o nome do doutor ou doutora do seu atendimento?",
      "Me fale a médica ou médico da consulta?",
      "Fale a médica ou médico do atendimento?",
      "Me fale o nome do doutor ou doutora da sua consulta?",
      "Fale o nome do doutor ou doutora do seu atendimento?"
   ],
   "podeSeguir(COMPL)": [
      "Pode seguir {0}",
      "OK pode seguir {0}",
      "Sim pode seguir {0}",
      "Por favor siga {0}",
      "Siga {0}",
      "Adiante {0}" 
   ],
   "podeSeSentar": [
      "Pode se sentar que você será chamado",
      "Sente se por favor, que você será chamado",
      "Por favor, se sente que será chamado",
      "Por favor, se sente que vão lhe chamar",
      "Sente-se que você será chamado",
      "Sente-se e espere que será chamado",
      "Pode se sentar e esperar que será chamado",
      "Você será chamado, pode se sentar e aguardar",
      "Pode se sentar e aguardar que irão te chamar",
      "Favor se sente, que vão lhe chamar" 
   ],
   "porFimPreciso(ALGO)": [
      "Por fim também preciso {0}",
      "Por último, eu quero {0}",
      "Por fim, necessito {0}",
      "Agora no fim, eu preciso {0}",
      "Por fim eu quero {0}",
      "Por último também quero {0}",
      "Por fim, preciso {0}",
      "Agora no fim, eu quero {0}",
      "Por fim eu preciso {0}",
      "Por último também preciso {0}" 
   ],
   "precisaAlgoMais": [
      "Se precisar de algo mais é só falar",
      "Precisa de algo?",
      "Mais algum atendimento ou agendamento?",
      "Mais alguma coisa?",
      "Algo mais?" 
   ],
   "respondaSimOuNao": [
      "Responda sim ou não",
      "É sim ou não?",
      "Sim ou não?",
      "Por favor, responda sim ou não",
      "Por favor é sim ou não?"
   ],
   "respostaSaudacoes": [
      "Ok tudo bem",
      "Ok tudo tranquilo",
      "Sim tudo bem",
      "Sim tudo tranquilo",
      "Oi pra você também",
      "Olá para você também"
   ],
   "saudacoesFinais": [
      "Até mais",
      "Tchau e tenha um bom dia",
      "Obrigado e tenha um bom dia",
      "Até logo",
      "Tchau e até logo",
      "Tchau e até mais",
      "Tenha um bom dia e até a próxima",
      "Até a próxima"
   ],
   "saudacoesIniciais": [
      "Oi bom dia",
      "Olá bom dia",
      "Bom dia pra voce",
      "Olá",
      "Olá, seja bem vindo",
      "Oi, seja bem vindo"
   ],
   "senhor": [
      "Senhor",
      "Seu",
      "Sr."
   ],
   "senhor(NOME)": [
      "Senhor {0}",
      "Seu {0}",
      "Sr. {0}"
   ],
   "senhora": [
      "Senhora",
      "Dona",
      "Sra."
   ],
   "senhora(NOME)": [
      "Senhora {0}",
      "Dona {0}",
      "Sra. {0}"
   ],
   "sePrecisarAjuda": [
      "Se precisar de ajuda é só pedir de novo",
      "Mas se quiser ajuda de novo é só pedir",
      "Caso precise de ajuda novamente é só falar"
   ],
   "souAtendenteDaqui": [
      "Sou o atendente daqui",
      "Sou o atendente dessa UPA",
      "Faço o atendimento inicial aqui na UPA",
      "Faço a recepção aqui na UPA",
      "Faço a recepção aqui",
      "Atendo as pessoas que chegam aqui na UPA"
   ],
   "sou(FULANO)": [
      "Sou {0}",
      "Me chamo {0}",
      "Meu nome é {0}",
      "Me chamam {0}",
      "O meu nome é {0}",
      "Eu sou {0}"
   ],
   
}
