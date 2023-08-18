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
#   File:       IntencoesAprendiz.jsonnet 
#   Purpose:    Exemplo de arquivo JSON/JSONNET que especifica os padrões 
#               de deteccao das intencoes de conversas do ator aprendiz
#   Author:     João Carlos Gluz
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
local sinonTarefa = "<tarefa|atua..o|performance>";

# Pattern prefixes

local prefixAprender = sinonPorFavor+sinonPronTrat+
    "<aprenda|saiba|lembre|lembre.se|conhe.a|registre|aprender|saber|lembrar|conhecer|registrar>"+
    "<que>?";
local prefixSalvar = sinonPorFavor+sinonPronTrat+"<salve|armazene|salvar|armazenar>";
local prefixRecuperar = sinonPorFavor+sinonPronTrat+"<recupere|relembre|recuperar|relembrar>";


[
	{"saudacoes": 	
		[
        "<olá|ola>_",
        "<oi>_",
        "<como><voc.|tu><vai.*|est.*>_",
        "<tudo><tranquilo|bem|certo>_",
        "<bom><dia>_",
        "<boa><tarde|noite>_"
        ]},
	{"incentivos": 	
		[
        "<ótimo>_",
        "<muito><bom>_",
        "<excelente>_",
        "<tá><certo><é><isso><mesmo>_",
        "<perfeito>_"
        ]},
	{"adeus":		
		[
        "<bye><bye>",
        "<tchau>",
        "<até><mais>",
        "<até><logo>",
        "<adeus>"
        ]},
	{"usuarioInformaNome": 	
		[
        "<o>?<meu><nome><é>(<.*>*)", 
        "<pode><me><chamar><de>(<.*>*)", 
        "<me><chamam><de>(<.*>*)", 
        "<eu><me><chamo>(<.*>*)"
        ]},
	{"respostaSim":	
		[
        "<sim>",
        "<ok>",
        "<concordo>",
        "<tudo><bem|certo>",
        "<tá|ta><bem|certo>",
        "<confirmo>",
        "<com><certeza>",
		"<está|esta><bem>",
        "<sem><d.vida>",
        "<está|esta>?<certo>",
        "<positivo>",
		"<isso><sim>",
        "<de><acordo>",
        "<mas><sim>",
        "<claro><que><sim>"
        ]},
	{"respostaNao":		
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
	{"obrigado":		
		[
        "<muit>?<obrigado><a>?<voc.>?",
        "<atenciosamente>",
        "<agradecido>",
        "<grato>",
        "<beleza>",
        "<jóia>",
		"<não|nao><ha|há><de><que>",
        "<por><nada>",
        "<disponha>"
        ]},               
	{"ajudaSobreComandos":	
		[
        sinonPorFavor+"<ajuda|informac..s|info><sobre>?<comandos|ordens>",
		sinonPorFavor+"<que><comandos|ordems><o|a>?<voc.|tu|senhor|senhora>?<sabe><fazer>",
        sinonPorFavor+"<que><comandos|ordems><o|a>?<voc.|tu|senhor|senhora>?<obedece|faz>"
        ]},
	{"ajudaBatePapos":	
		[
        "_<diga|fale|explique><quais|que><bate|chats|bate.papos><papos>?<voc.|tu>?<conhec.*>_?",
		"_<ajuda|informac..s|info><sobre>?<bate|chats|bate.papos><papos>?_"
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
            "<conhe.e.*|sabe.*|reconhe.e.*|aprendeu|entende>?<sobre>?<a|o>?"+sinonConversa+"(<.+>+)",
        sinonPorFavor+sinonPronTrat+"<ajuda|informac..s|info|ajudar|informar><sobre>?"+
            sinonConversa+"(<.+>+)"
		]},		
	{"logOut":		
		[
        "<fa.a><log><out>",
        "<fa.a><logout>",
        "<saia|deixe><deste|desta|este|esta|do|da><mundo|vr|rv><agora>?",
        "<vá|va|volte><para|pra><casa>"
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
]
+   (import 'PerguntasAprendiz.jsonnet-inc')
+   (import 'ComandosAprendiz.jsonnet-inc') 
+   (import 'TreinamentoAprendiz.jsonnet-inc')
+
[	
    {"salveMemorias":	
		[
        prefixSalvar +
			"<seu|teu>?<estado><mental><em>(<.+>)",
		prefixSalvar +
			"<suas|tuas>?<mem.rias|lembranças|cren.as><em>(<.+>)",
		prefixSalvar +
			"<suas|tuas>?<recorda..es|ensinamentos><em>(<.+>)",
		prefixSalvar +
			"<seu|teu>?<estado><mental><no><arquivo>(<.+>)",
		prefixSalvar +
			"<suas|tuas>?<mem.rias|lembran.as|crenças><no><arquivo>(<.+>)",
		prefixSalvar +
			"<suas|tuas>?<recorda..es|ensinamentos><no><arquivo>(<.+>)"
		]},
	{"recupereMemorias":	
		[
        prefixRecuperar +
			"<seu|teu>?<estado><mental><de>(<.+>)",
		prefixRecuperar +
			"<suas|tuas>?<mem.rias|lembran.as|crenças><de>(<.+>)",
		prefixRecuperar +
			"<suas|tuas>?<recorda..es|ensinamentos><de>(<.+>)",
		prefixRecuperar +
			"<seu|teu>?<estado><mental><do><arquivo>(<.+>)",
		prefixRecuperar +
			"<suas|tuas>?<mem.rias|lembran.as|crenças><do><arquivo>(<.+>)",
		prefixRecuperar +
			"<suas|tuas>?<recorda..es|ensinamentos><do><arquivo>(<.+>)"
		]},
	{"salveBatePapos":	
		[
        prefixSalvar +
			"<seus|teus>?<di.logos|bate><simples|papos>?<em|no><arquivo>?(<.+>)",
        prefixSalvar +
			"<seus|teus>?<bate.papos><em|no><arquivo>?(<.+>)",
		prefixSalvar +
			"<suas|tuas>?<conversas|entrevistas|perguntas|questões><simples|respostas>?<em|no><arquivo>?(<.+>)"
		]},
	{"recupereBatePapos":	
		[
        prefixRecuperar +
			"<seus|teus>?<di.logos|bate><simples|papos>?<de|do><arquivo>?(<.+>)",
        prefixRecuperar +
			"<seus|teus>?<bate.papos><de|do><arquivo>?(<.+>)",
		prefixRecuperar +
			"<suas|tuas>?<conversas|entrevistas|perguntas|questões><simples|respostas>?<de|do><arquivo>?(<.+>)"
		]},
	{"ultimaFraseTeste": 	
		[
        "<última|ultima><frase><de><teste>", 
        "<último|ultima><fala><de><teste>", 
        "<último|ultima><mensagem><de><teste>", 
        "<testando><testando>?<fala|frase|mensagem><final>", 
        "<testando><testando>?<última|ultima><fala|frase|mensagem>"
        ]},

]
