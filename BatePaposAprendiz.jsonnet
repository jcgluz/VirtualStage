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
#   File:       BatePaposAprendiz.jsonnet 
#   Purpose:    Exemplo de arquivo JSON/JSONNET que especifica os bate-papos
#               pergunta/resposta do ator aprendiz (apprentice actor)
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

[
   {    "hear":     ["<samba>"],
        "talk":     "É uma música brasileira"
   },
   {    "hear":     ["<rock>"],
        "talk":     "Música de origem norte-americana"
   },
   {    "hear":     ["<eu><gosto><de><m.sica>(<.+>+)"],
        "talk":     "Voce gosta de ouvir música {0}"
   },
   {    "hear":     ["<eu><gosto><de><ler>(<.+>+)"],
        "talk":     "Voce gosta de ler {0}"
   },
   {    "hear":     ["<quem><é><que><te><criou>",
                    "<quem><é><teu|seu|tua|sua><pai|m.e|criador|criadora>"],
        "talk":     "Meu criador é {npc-creator}"
   },
   {    "hear":     ["<o>?<que><o|a><voc.|tu|senhor.*><est.*><sentindo|passando|sofrendo>_",
                    "<o>?<que><est.><acontecendo|passando|incomodando><com>?<o|a><senhor.*>_",
                    "<o>?<que><est.><te|lhe>?<incomodando|doendo|acontecendo|passando>_"],
        "talk":     ["Estou com dor nos braços e nas articulações, parece que tenho febre",
                    "Acho que estou com febre, mas o pior é que me doem os braços",
                    "Os braços estão me incomodando, acho que tô com um pouco de febre",
                    "Me doem as articulações dos braços, também me sinto como se tivesse febre"]
   },
   {    "hear":     ["<voc.>?<se|te>?<lembra>?<quando><isso|isto><come.ou|iniciou>_",
                    "<voc.>?<se|te>?<lembra>?<quando><esta|essa><dor><come.ou|iniciou>_",
                    "<voc.>?<se|te>?<lembra>?<quando><vo.e|tu>?<come.ou|iniciou>_",
                    "<voc.>?<se|te>?<lembra>?<quando><isso|isto>?<come.ou|iniciou>_",
                    "<j.>?<faz><quanto>?<tempo>_"],
                    
        "talk":     ["Já faz uns dias",
                    "Tem uns três ou quatro dias",
                    "Desde a semana passada mais ou menos",
                    "Não faz muito, deve ter começado já faz uns dois ou três dias"]
   },
   {    "hear":     ["<o|a>?<voc.|tu|senhor|senhora>?<se|te>?<lembra.*>?<se>?<teve|sofreu><uma>?<les.o|tors.o>_",
                    "<o|a>?<voc.|tu|senhor|senhora>?<se|te>?<lembra.*>?<se>?<praticou|fez><muito>?<esfor.o|trabalho|esporte>_",
                    "<o|a>?<voc.|tu|senhor|senhora>?<se|te>?<lembra.*>?<se>?<carregou|levantou><muito>?<peso>_"],
        
        "talk":     ["No outro fim de semana trabalhei bastante com a obra lá em casa",
                    "Já faz uma semana mais ou menos carreguei bastante peso pra obra que estamos fazendo em casa",
                    "Sim levantei bastante peso faz uns dias, estamos trabalhando lá em casa e eu estava ajudando",
                    "Não me lembro ter me lesionado, mas trabalhei muito e carreguei bastante peso na semana passada"]
   },
   {    "hear":     ["<ok>?<seu|dona>?<.*><n.s>?<vamos>_",
                    "<ok>?<seu|dona>?<.*><acho>_",],
                    
        "talk":     ["Ok doutora, me explica bem que se tiver que fazer isso eu faço sem problemas",
                    "Sim tudo bem, basta me dizer o que fazer",
                    "Claro doutora, se precisar vou fazer o que a senhora disser"]
   },
   {    "hear":     ["<meu><pai><é>(<.+>+)<quem><é><seu|teu><pai>"],
        "talk":     "O seu pai é {0}, mas meu criador é {npc-creator}"
   }
 ]
