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
#   File:       IntencoesAtendente.jsonnet
#   Purpose:    Exemplo de arquivo JSON/JSONNET que especifica os padrões 
#               de deteccao das intencoes de conversas do ator atendente
#   Author:     João Carlos Gluz - 2020-2023
#
###############################################################
###############################################################

# Word/Phrases synonyms

local sinonObjeto = "<objeto|coisa|peça|utensílio|ente|entidade|primitiva|"+
					"artefato|aparelho|instrumento|dispositivo|"+
					"troço|treco|tralha|trambolho|cacareco|bugiganga>";
local sinonObjetos = "<objetos|coisas|peças|utensílios|entes|entidades|primitivas|"+
					"artefatos|aparelhos|instrumentos|dispositivos|"+
					"troços|trecos|tralhas|trambolhos|cacarecos|bugigangas>";
local sinonLugar = 	"<lugar|local|posição|localidade|área|espaço|ponto|zona|"+
					"parte|localização|sítio>";
local sinonLugares = "<lugares|locais|posições|localidades|áreas|espaços|pontos|zonas|"+
					"partes|localizações|sítios>";
local sinonConversas = "<conversas|discuss.es|di.logos|bate.papos|papos|falas>";
local sinonConversa = "<conversa|discuss.o|di.logo|bate.papo|papo|fala>";
local sinonVemVai = "<va|vá|vai|vem|venha|volte|mova.se|mova|ande|caminhe|siga>";
local sinonIrVir = "<vir|ir|andar|caminhar|seguir|voltar|mover.se>";
local sinonPorFavor = "<agora>?<por|gostaria|agrade.o>?<favor|que|se>?<agora>?";
local sinonPronTrat = "<o|a>?<voc.|tu|senhor|senhora>?<pode|podes|poderia|gostaria>?<de>?";
local sinonMarcar = "<marcar|agendar|definir|reservar|combinar|programar>";
local sinonConsulta = "<consulta|atendimento>";
local sinonQuero = "<quero|preciso|necessito|tenho|desejo|peço>";
local sinonExame = "<exame|checkup|checape|estudo>";
local sinonMedico = "<medico|medica|médico|médica|doutor|doutora|dr|dra>";

# Pattern prefixes

local prefixAprender = sinonPorFavor+sinonPronTrat+
    "<aprenda|saiba|lembre|lembre.se|conhe.a|registre|aprender|saber|lembrar|conhecer|registrar>"+
    "<que>?";
local prefixSalvar = sinonPorFavor+sinonPronTrat+"<salve|armazene|salvar|armazenar>";
local prefixRecuperar = sinonPorFavor+sinonPronTrat+"<recupere|relembre|recuperar|relembrar>";

# Imported Files

local ConversasPerguntas = import 'ConversasPerguntasAprendiz.jsonnet';
local ConversasTreinamento = import 'ConversasTreinamentoAprendiz.jsonnet';

[
	{"saudacoes": 	
		[
        "<oi|olá|ola>",
        "<oi|olá|ola>?<como><voc.|tu>?<vai.*|est.*>_",
        "<oi|olá|ola>?<tudo><tranquilo|bem|certo>_",
        "<oi|olá|ola>?<bom><dia>_",
        "<oi|olá|ola>?<boa><tarde|noite>_"
        ]},
        
	{"incentivos": 	
		[
        "<sim|ok>?<ta|tá|esta|está>?<ótimo|otimo|excelente|certo|perfeito|continue>",
        "<sim|ok>?<ta|tá|esta|está>?<muito|indo|siga><bom|bem|assim>",
        "<sim|ok>?<tá|ta|esta|está>?<certo|bom|bem><é|e><isso|isto><mesmo|aí|ai>",
        "<sim|ok>?<é|e><isso|isto><mesmo|aí|ai>"
        ]},
    
      
	{"vouAoConsultorio:['medica carla']":		
        [
        "<vou|estou><indo>?<ao|para|atender><o|no>?<consultorio>_",
		"<vou|estou><indo>?<atender><na><minha>?<sala>_"
        ]},
                    
	{"meChameSeHouverPacientes:['medica carla']":		
        [
        sinonPorFavor+"<assim>?<se|que|quando><houver><pacientes|pessoas><pode>?<me>?<chamar|chame>_",
        sinonPorFavor+"<pode>?<me>?<chamar|chame><assim>?<se|que|quando><houver><pacientes|pessoas>_"
        ]},
                    
	{"mePassePacientes:['medica carla']":		
        [
        sinonPorFavor+"<agora>?<pode>?<me>?<passar|passe|chamar|mandar|mande><os|as>?<pacientes|pessoas>_",
        sinonPorFavor+"<agora>?<posso>?<receber><os|as>?<pacientes|pessoas>_"
        ]},
                    
	{"agendarConsulta":		
        [
        sinonPorFavor+sinonQuero+"<para|pra>?<que>?"+sinonMarcar+
            "<uma|um>?<hor.rio|hora>?<para|pra|pro>?<o>?"+sinonConsulta+"_",
		sinonPorFavor+"<vim|estou><aqui>?<hoje|agora>?<aqui>?<hoje|agora>?<para|pra>?"+
            sinonMarcar+"<uma|um>?<hor.rio|hora>?<para|pra|pro>?<o>?"+sinonConsulta+"_",
		sinonPorFavor+sinonPronTrat+sinonMarcar+"<uma|um>?<hor.rio|hora>?<para|pra|pro>?<o>?"+
            sinonConsulta+"_"
        ]},
                    
	{"agendarExame":		
        [
        sinonPorFavor+sinonQuero+"<para|pra>?<que>?"+sinonMarcar+
            "<uma|um>?<hor.rio|hora>?<para|pra|pro>?<o>?"+sinonExame+"_",
		sinonPorFavor+"<vim|estou><aqui>?<hoje|agora>?<aqui>?<hoje|agora>?<para|pra>?"+
            sinonMarcar+"<uma|um>?<hor.rio|hora>?<para|pra|pro>?<o>?"+sinonExame+"_",
		sinonPorFavor+sinonPronTrat+sinonMarcar+
            "<uma|um>?<hor.rio|hora>?<para|pra|pro>?<o>?"+sinonExame+"_"
        ]},
                    
	{"consultarPacienteComMedico":	
        [
        sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+sinonQuero+
            "<para|pra>?<que>?<me>?"+"<consultar|atender>_"+
            "<com><a|o>?<dra|doutora|doutor|dr|medic.>(<.*>*)<agora|as|ás>?_",
        sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+sinonQuero+
            "<para|pra>?<que>?<me>?"+"<consultar|atender>_"+
            "<.*>*<dra|doutora|doutor|dr|medic.>(<.*><.*>?)_",
		sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+"<vou><me>?<consultar|atender>"+
            "<com><a|o>?<dra|doutora|doutor|dr|medic.>(<.*>*)<agora|as|ás>?_",
		sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+"<vou><me>?<consultar|atender>"+
            "<.*>*<dra|doutora|doutor|dr|medic.>(<.*><.*>?)_",
		sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+
            "<vim|estou><aqui>?<hoje|agora>?<aqui>?<hoje|agora>?<para|pra>?"+
            "<me>?<a|o>?<consultar|consulta|atender|atendimento>_"+
            "<com><a|o>?<dra|doutora|doutor|dr|medic.>(<.*>*)<agora|as|ás>?_",
		sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+
            "<vim|estou><aqui>?<hoje|agora>?<aqui>?<hoje|agora>?<para|pra>?"+
            "<me>?<a|o>?<fazer>?<consultar|consulta|atender|atendimento>_"+
            "<.*>*<dra|doutora|doutor|dr|medic.>(<.*><.*>?)_",
		sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+
            "<ja|já>?<tenho><uma|um>?"+sinonConsulta+"<marcad.|agendad.>"+
            "<com><a|o>?<dra|doutora|doutor|dr|medic.>(<.*>*)<agora|as|ás>?_",
		sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+
            "<ja|já>?<tenho><uma|um>?"+sinonConsulta+"<marcad.|agendad.>"+
            "<.*>*<dra|doutora|doutor|dr|medic.>(<.*><.*>?)_",
		sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+
            "<ja|já>?<tenho><uma|um>?<hor.rio|hora>?"+
            "<marcado|reservado|agendado|combinado>?<para|pra|pro>?<a|o>?"+sinonConsulta+
            "<com><a|o>?<dra|doutora|doutor|dr|medic.>(<.*>*)<agora|as|ás>?_",
		sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+
            "<ja|já>?<tenho><uma|um>?<hor.rio|hora>?"+
            "<marcado|reservado|agendado|combinado>?<para|pra|pro>?<a|o>?"+sinonConsulta+
            "<.*>*<dra|doutora|doutor|dr|medic.>(<.*><.*>?)_"
        ]},
                    
	{"fazerConsulta":	
        [
        sinonPorFavor+sinonQuero+"<para|pra>?<que>?<me>?"+"<consultar|atender>_",
		sinonPorFavor+"<vou><me>?<consultar|atender>_",
		sinonPorFavor+"<vim|estou><aqui>?<hoje|agora>?<aqui>?<hoje|agora>?<para|pra>?"+
            "<me>?<a|o>?<fazer>?<consultar|consulta|atender|atendimento>_",
		sinonPorFavor+"<ja|já>?<tenho><uma|um>?"+sinonConsulta+"_",
		sinonPorFavor+"<ja|já>?<tenho><uma|um>?<hor.rio|hora>?"+
            "<marcado|reservado|agendado|combinado>?<para|pra|pro>?<o>?"+sinonConsulta+"_"
        ]},
                    
	{"fazerExameDeTipoComPaciente":	
        [
        sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+sinonQuero+"<para|pra>?<que>?"+
            "<fazer|realizar|proceder><com>?<o>?"+sinonExame+"<de>?(<.*>+)<agora>?<as|ás>?_",
		sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+"<vou>"+
            "<fazer|realizar|proceder><com>?<o>?"+sinonExame+"<de>?(<.*>+)<agora>?<as|ás>?_",
		sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+
            "<vim|estou><aqui>?<hoje|agora>?<aqui>?<hoje|agora>?<para|pra>?"+
            "<fazer|realizar|proceder><com>?<o>?"+sinonExame+"<de>?(<.*>+)<agora>?<as|ás>?_",
		sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+
            "<ja|já>?<tenho><uma|um>?"+sinonExame+"<de>?(<.*>+)<agora>?<as|ás>?_",
		sinonPorFavor+"<eu>?<sou|me><chamo>?(<.*>+)<e>?"+
            "<ja|já>?<tenho><uma|um>?<hor.rio|hora>?"+
            "<marcado|reservado|agendado|combinado>?<para|pra|pro>?<o>?"+
            sinonExame+"<de>?(<.*>+)<agora>?<as|ás>?_"
        ]},
                    
	{"fazerExame":	
        [
        sinonPorFavor+sinonQuero+"<para|pra>?<que>?"+
            "<fazer|realizar|proceder><com>?<o>?"+sinonExame+"_",
		sinonPorFavor+"<vou>"+
            "<fazer|realizar|proceder><com>?<o>?"+sinonExame+"_",
		sinonPorFavor+"<vim|estou><aqui>?<hoje|agora>?<aqui>?<hoje|agora>?<para|pra>?"+
            "<fazer|realizar|proceder><com>?<o>?"+sinonExame+"_",
		sinonPorFavor+"<ja|já>?<tenho><uma|um>?"+sinonExame+"_",
		sinonPorFavor+"<ja|já>?<tenho><uma|um>?<hor.rio|hora>?"+
            "<marcado|reservado|agendado|combinado>?<para|pra|pro>?<o>?"+sinonExame+"_"
        ]},
                    
	{"informaNome": 	
		[
        "<ok|sim>?<oi|olá|ola>?<o>?<meu><nome><completo>?<é|e>(<.*>+)", 
        "<ok|sim>?<oi|olá|ola>?<pode><me><chamar><de>?(<.*>+)", 
        "<ok|sim>?<oi|olá|ola>?<eu>?<me><chamo|chamam><o|a|de>?(<.*>+)",
        "<ok|sim>?<oi|olá|ola>?<eu>?<sou><o|a>?(<.*>+)"
        ]},
 
    {"informaNome@modo-informa-nome":	
        [
        "(<.*>*)"
        ]},
 
	{"informaMedico": 	
		[
        "<ok|sim>?<oi|olá|ola>?<e|é>?<o|a>?"+sinonMedico+"<é|e|se>?<chama>?(<.*>+)", 
        "<ok|sim>?<oi|olá|ola>?<o>?<nome><do|da>"+sinonMedico+"<é|e>?(<.*>+)"
        ]},
 
    {"informaMedico@modo-informa-medico":	
        [
        "(<.*>*)"
        ]},
 
	{"informaTipoExame": 	
		[
        "<ok|sim>?<oi|olá|ola>?<e|é>?<um|o>?"+sinonExame+"<de>?(<.*>+)", 
        "<ok|sim>?<oi|olá|ola>?<o>?<nome><do|da>"+sinonExame+"<é|e>?(<.*>+)"
        ]},
 
    {"informaExame@modo-informa-exame":	
        [
        "(<.*>*)"
        ]},
 
	{"informaHorario": 	
		[
        "<ok|sim>?<oi|olá|ola>?<quero|fico>?<com>?<o|a>?<hor.rio|hora><das>?(<.*>+)", 
        "<ok|sim>?<oi|olá|ola>?<pra|para>?<mim>?<tá|ta|esta|está>?"+
            "<bom|ok|otimo|ótimo>?<o|a>?<hor.rio|hora><das>?(<.*>+)"
        ]},
        
    {"informaHorario@modo-escolhe-horario":	
        [
        "(<.*>*)"
        ]},
 
    {"qualquerResposta@modo-segue-atendimento":	
        [
        "(<.*>*)"
        ]},
 
	{"confirma":	
		[
        "<sim>",
        "<ok>",
        "<concordo>",
        "<tudo><bem>",
        "<tá><bem>",
        "<confirmo>",
        "<com><certeza>",
		"<tudo><certo>",
        "<está><bem>",
        "<sem><dúvida>",
        "<está>?<certo>",
        "<positivo>",
		"<isso><sim>",
        "<de><acordo>",
        "<mas><sim>"
        ]},

	{"recusa":		
		[
        "<não|nao>",
        "<não|nao><pode>",
        "<não|nao><da|dá>",
        "<neca>",
        "<nego>",
        "<recuso>",
		"<recusado>",
        "<me><oponho>",
        "<nunca>",
        "<nenhum>",
        "<negado>",
        "<negativo>"
        ]},

	{"olheParaMim":	
		[
        sinonPorFavor+"<se>?<dirija|volte|olhe><para|pra><mim>_",
        sinonPorFavor+"<me><olhe|veja>",
        sinonPorFavor+sinonPronTrat+"<se>?<dirijir|voltar|olhar><para|pra><mim>_",
        sinonPorFavor+sinonPronTrat+"<me><olhar|ver>"
        ]},

	{"ajudaConversas":	
		[
        "_<diga|fale|explique><quais|que>"+sinonConversas+
            "<voc.>?<conhe.e>?",
		"_<diga|fale|explique><quais|que>"+sinonConversas+
            "<voc.>?<conhe.e>?<sobre>?(<.+>+)",
		"_<ajuda|informac..s|info><sobre>?"+sinonConversas,
		"_<ajuda|informac..s|info><sobre>?"+sinonConversas+
            "<sobre>?(<.+>+)"
		]},
		
	{"ajudaSobreConversa":	
		[
        sinonPorFavor+sinonPronTrat+"<me>?<diga|fale|explique|dizer|falar|explicar>?"+
            "<quais|que><frases|ora..es|senten.as|palavras><o|a>?<voc.|tu|senhor|senhora>"+
            "<conhe.e.*|sabe.*|reconhe.e.*|aprendeu|entende>?<sobre>?<a|o>?"+
            sinonConversa+"(<.+>+)",
        sinonPorFavor+sinonPronTrat+"<ajuda|informac..s|info|ajudar|informar><sobre>?"+
            sinonConversa+"(<.+>+)"
		]},		

	{"adeus":		
		[
        "<bye><bye>",
        "<tchau>",
        "<até><mais>",
        "<até><logo>",
        "<adeus>"
        ]},

	{"logOut":		
		[
        "<fa.a><log><out>",
        "<fa.a><logout>",
        "<saia|deixe><deste|desta|este|esta|do|da><mundo|vr|rv><agora>?"
        ]},

    {"setPrDebType":
        [
        "<set><prdeb><type>(<.*>*)"
        ]},

    {"enablePrDeb":
        [
        "<enable><prdeb>_"
        ]},

    {"disablePrDeb":
        [
        "<disable><prdeb>_"
        ]},
        
#    {"unknownUserInput":	
#        [
#        "(<.*>*)"
#        ]}

]

