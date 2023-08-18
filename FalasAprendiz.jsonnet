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
#   File:       FalasAprendiz.jsonnet 
#   Purpose:    Exemplo de arquivo JSON/JSONNET que especifica as falas usadas
#               nas conversas/dialogos do ator aprendiz (trainee actor)
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

{
   "abaixando(OMEMBRO)": [
      "OK, abaixando {0}",
      "Abaixando {0}",
      "Já estou abaixando {0}",
      "Estou abaixando {0}",
      "Sim, abaixando {0}",
      "Estou abaixando {0}"
   ],
   "abrindo(OMEMBRO;NAPOSICAO)": [
      "OK, abrindo {0} {1}",
      "Abrindo {0} {1}",
      "Já estou abrindo {0} {1}",
      "Estou abrindo {0} {1}",
      "Sim, abrindo {0} {1}",
      "Estou abrindo {0} {1}"
   ],
   "acheiLugar": [
      "Ok achei o lugar",
      "Sim este é o lugar",
      "Ok, sim esse é o local"
   ],
   "acheiObjeto": [
      "Achei o objeto!",
      "Que bom que encontrei o objeto",
      "Sou bom em achar coisas"
   ],
   "achoQueRecuperei(OSDADOS;NOMEARQ)": [
      "Ok acho que recuperei {0} de {1}",
      "Ok acho que recuperei {0} do arquivo {1}",
      "Acho que relembrei {0} do arquivo {1}",
      "Em princípio recarreguei {0} de {1}",
      "Em princípio recarreguei {0} do arquivo {1}",
      "Devo ter recuperado {0} do arquivo {1}"
   ],
   "achoQueSalvei(OSDADOS;NOMEARQ)": [
      "Ok acho que salvei {0} em {1}",
      "Ok acho que salvei {0} no arquivo {1}",
      "Acho que armazenei {0} no arquivo {1}",
      "Em princípio guardei {0} em {1}",
      "Em princípio guardei {0} no arquivo {1}",
      "Devo ter salvado {0} no arquivo {1}"
   ],
   "agradecimentos": [
      "Muito obrigado!",
      "Quem bom!",
      "Obrigado pela ajuda!",
      "Muito bom saber!",
      "Fico feliz!"
   ],
   "aprendiPergunta": [
      "Sim, aprendi a pergunta",
      "Ok, vou lembrar da pergunta",
      "Registrei a pergunta"
   ],
   "aprendiPerguntaResposta(QUESTAO;RESP)": [
      "Sim, aprendi que a pergunta: {0}, tem resposta: {1}",
      "Ok, vou lembrar que a pergunta: {0}, é respondida com: {1}", 
      "Registrei que a pergunta: {0}, deve ser respondida com: {1}", 
      "Registrei que a pergunta: {0}, tem resposta: {1}", 
      "Aprendi que a pergunta: {0}, tem resposta: {1}", 
      "Vou lembrar que a pergunta: {0}, é respondida com: {1}"
   ],
   "aprendiINovoLugar(X;Y)": [
      "OK, aprendi que um novo lugar fica na posição {0}, {1}", 
      "Aprendi sobre um novo local que fica nas coordenadas {0}, {1}", 
      "Vou lembrar sobre o novo lugar na posição {0}, {1}", 
      "Agora sei sobre um novo local nas coordenadas {0}, {1}",
      "OK, agora conheço um novo lugar na posição {0}, {1}",
      "OK, conheço um novo local na posição {0}, {1}"
   ],
   "aprendiInfoLugar(PROP;VAL)": [
      "OK, aprendi que {0} desse lugar é {1}", 
      "Aprendi que {0} desse local é {1}", 
      "OK, aprendi que {0} desse lugar é {1}", 
      "Vou lembrar que {0} desse local é {1}", 
      "Vou me lembrar que {0} daqui é {1}", 
      "Vou lembrar que {0} daqui é {1}", 
      "Agora sei que {0} desse local é {1}",
      "OK, agora sei que {0} daqui é {1}",
      "Agora sei que {0} desse lugar é {1}"
   ],
   "aprendiInfoObjeto(PROP;VAL)": [
      "OK, aprendi que {0} disso é {1}", 
      "Aprendi que {0} desse objeto é {1}", 
      "OK, aprendi que {0} dessa coisa é {1}", 
      "Vou lembrar que {0} desse objeto é {1}", 
      "Vou me lembrar que {0} disso é {1}", 
      "Vou lembrar que {0} dessa coisa é {1}", 
      "Agora sei que {0} dessa coisa é {1}",
      "OK, agora sei que {0} disso é {1}",
      "Agora sei que {0} desse objeto é {1}"
   ],
   "ateLogo": [
      "OK Tchau!",
      "Bye!",
      "Bye Bye!",
      "Tchau!",
      "Tchauzinho",
      "Tchau, te vejo mais tarde",
      "Até logo",
      "Até mais",
      "Adeus"
   ],
   "atributoLugarEh(PROP;VAL)": [
      "Sei que {0} daqui é {1}", 
      "Sei que {0} desse lugar é {1}", 
      "Aprendi que {0} desse lugar é {1}", 
      "Aprendi que {0} daqui é {1}", 
      "Me disseram que {0} desse local é {1}"
   ],
   "atributoObjetoEh(PROP;VAL)": [
      "Sei que {0} do objeto é {1}", 
      "Sei que {0} disto aqui é {1}", 
      "Aprendi que {0} dessa coisa é {1}", 
      "Aprendi que {0} disto aqui é {1}", 
      "Me disseram que {0} desse objeto é {1}"
   ],
   "atenderDesejo(DESCR)": [
      "Sim, farei {0}",
      "OK vou tentar {0}",
      "Seu desejo de {0} é uma ordem",
      "Tentarei {0}"
   ],
   "chegaDeAprender": [
      "Ok, se quiser ensinar outras coisas é só falar",
      "Tá bom, paramos por agora",
      "Ok, chega de aprender por agora"
   ],
   "chegamosLugar": [
      "Oi! Chegamos ao local", 
      "Olá! Já estamos no lugar",
      "Olha, já chegamos ao lugar"
   ],
   "comecarTourLugaresConhecidos": [
      "OK, vamos começar o tour pelos lugares que conheço",
      "Claro que sim, vamos começar a ver os lugares que conheço",
      "Sim, vamos começar o passeio pelos locais que eu conheço",
      "Certo, começamos o tour pelos lugares que conheço"
   ],
   "confirmaNome": [
      "Sim, esse é meu nome",
      "Sim, você esta certo esse é meu nome",
      "Sim, pode me chamar assim",
      "OK, é assim que me chamo"
   ],
   "conhecoCenas": [
      "Conheço as seguintes cenas",
      "Tenho informações sobre as cenas",
      "Me informaram sobre as seguintes cenas"
   ],
   "conhecoDescricaoLugar(DESCR)": [
      "Sei que esse lugar é {0}",
      "Sei que esse local é {0}",
      "Me disseram que esse lugar é {0}",
      "Me falaram que esse local é {0}"
   ],
   "conhecoDescricaoObjeto(DESCR)": [
      "Sei que esse objeto é {0}",
      "Sei que essa coisa é {0}",
      "Sei que isso é {0}",
      "A descrição disso é {0}",
      "Isso é descrito como {0}"
   ],
   "conhecoEventoLugar(EVENTO)": [
      "Sei que nesse lugar houve {0}",
      "Me disseram que aqui aconteceu {0}",
      "Me falaram que aqui ocorreu {0}",
      "Soube que nesse lugar ocorreu {0}"
   ],
   "conhecoLugaresAqui": [
      "Conheço os seguintes lugares",
      "Tenho informações sobre os locais",
      "Me informaram sobre os seguintes lugares"
   ],
   "conhecoNomeLugar(NOME)": [
      "Conheço esse lugar como {0}", 
      "Sei que o nome daqui é {0}",
      "Sei que o nome desse local é {0}", 
      "Aprendi que esse lugar se chama {0}", 
      "Me disseram que o nome daqui é {0}"
   ],
   "conhecoNomeObjeto(NOME)": [
      "Conheço esse objeto como {0}",
      "Sei que nome dessa coisa é {0}",
      "Sei que nome desse objeto é {0}",
      "Aprendi que isso se chama {0}",
      "Me ensinaram que o nome disso é {0}"
   ],
   "conhecoObjetosAqui": [
      "Conheço os seguintes objetos aqui por perto",
      "Reconheço as seguintes coisas aqui",
      "Me lembro das seguintes coisas por aqui"
   ],
   "conhecoTarefas": [
      "Conheço as seguintes tarefas",
      "Sei fazer as seguintes tarefas",
      "Sei como fazer as seguintes atuações",
      "Me ensinaram as seguintes atuações",
      "Me ensinaram como fazer as seguintes tarefas"
   ],
   "conhecoUsoObjeto(USO)": [
      "Esse objeto serve para {0}",
      "Isso é usado para {0}",
      "Essa coisa é usada para {0}",
      "Isso serve para {0}"
   ],
   "conheco(PROP;COISA;VAL)": [
      "Conheço {0} {1} como {2}", 
      "Sei que {0} {1} é {2}",
      "Aprendi que {0} {1} é {2}", 
      "Me disseram que {0} {1} é {2}"
   ],
   "deitando(NACOISA)": [
      "OK, deitando {0}",
      "Sim, estou me deitando {0}",
      "Estou me deitando {0}",
      "Já estou me deitando {0}",
      "Sim, estou deitando {0}",
      "Ok estou me deitando {0}",
      "Estou deitando {0}"
   ],
   "deitei(NACOISA)": [
      "OK, deitei {0}",
      "Sim, deitei {0}",
      "Já me deitei {0}",
      "Sim, já me deitei {0}",
      "Ok estou deitado {0}",
      "Estou deitado {0}"
   ],
   "desconfirmaNome": [
      "Não, esse não é meu nome",
      "Esse não é meu nome",
      "Não me chamo assim, esse não é meu nome",
      "Não me chamo assim"
   ],
   "digaAtributo": [
      "Você não disse no fim da frase qual propriedade/atributo devo aprender",
      "O que é que você quer que eu aprenda? Diga isso no fim da frase",
      "No fim da frase tem que dizer qual propriedade ou atributo eu devo aprender"
   ],
   "digaQualConversa": [
      "Diga no fim da frase a conversa que você quer informações",
      "Fale no fim da frase a conversa que você quer ajuda",
      "Tem que dizer no fim da frase que conversa ou diálogo você quer ajuda",
      "Diga qual a conversa que que ajuda no fim da frase"
   ],
   "esseObjetoEh(TIPO)": [
      "Isso é {0}",
      "Isto é {0}",
      "Essa coisa é {0}",
      "Esse objeto é {0}"
   ],
   "esseObjetoEh(TIPO;DESCR)": [
      "Isso é {0} e sua descrição é: {1}",
      "Isto é {0} com descrição: {1}",
      "Essa coisa é {0} cuja descrição é: {1}",
      "Esse objeto é {0} com descrição: {2}"
   ],
   "essaPlantaEh(TIPO)": [
      "Essa planta é {0}",
      "Esta árvore é {0}"
   ],
   "essaPlantaEh(TIPO;DESCR)": [
      "Essa planta é {0} descrita como: {1}",
      "Essa planta é {0} cuja descrição é: {1}",
      "Esta árvore é {0} e sua descrição é: {1}"
   ],
   "essaGramaEh(TIPO)": [
      "Isso é uma grama {0}",
      "Esta grama é {0}"
   ],
   "essaGramaEh(TIPO;DESCR)": [
      "Isso é uma grama {0} descrita como: {1}",
      "Isso é uma grama {0} com descrição: {1}",
      "Esta grama é {0} e sua descrição é: {1}"
   ],
   "estouIndo": [
      "Estou indo",
      "Vou indo",
      "Já vou ir",
      "Tô seguindo"
   ],
   "estouIndoParaLa": [
      "Estou indo para lá",
      "Vou indo até lá",
      "Já vou ir para lá",
      "Tô seguindo pra lá"
   ],
   "estouTeOlhando": [
      "Já estou te olhando",
      "Estou te olhando",
      "Estou olhando pra ti"
   ],
   "estouTeleportando": [
      "Estou teleportando agora",
      "Já estou me teleportando até aí",
      "Teleportando até aí"
   ],
   "estouVindo": [
      "Estou vindo",
      "Estou indo",
      "Quase chegando aí",
      "Quase lá",
      "Já vou indo",
      "Já vou até aí"
   ],
   "euSouUm(DESCR)": [
      "Sou um {0}",
      "Eu sou um {0}"
   ],
   "euSouUmTenhoAnos(DESCR;IDADE)": [
      "Eu sou um {0} e tenho {1} anos",
      "Sou um {0} com {1} anos"
   ],
   "euTenhoAnos(IDADE)": [
      "Eu tenho {0} anos",
      "Estou com {0} anos",
      "Tenho {0} anos"
   ],
   "faleNovamente": [
      "Você pode repetir",
      "Pode falar de novo",
      "Fale novamente",
      "Por favor, fale novamente"
   ],
   "faleOutraPergunta": [
      "Me fale mais uma pergunta",
      "Sim, me diga uma outra pergunta",
      "Ok, pode me falar outra pergunta"
   ],
   "falePergunta": [
      "Me fale uma pergunta",
      "Sim, me diga uma pergunta",
      "Ok, pode me falar uma pergunta"
   ],
   "faleSobreLugar": [
      "Ok, me fale o que você sabe sobre esse lugar",
      "Sim, me passe as informações desse local aqui",
      "Claro que sim, pode me falar o que conhece sobre esse lugar"
   ],
   "faleSobreObjeto": [
      "Sim, me fale o que você sabe sobre esse objeto",
      "Sim, me passe as informações sobre isso",
      "Claro que sim, pode me falar o que conhece sobre essa coisa"
   ],
   "ficandoDePe": [
      "OK, estou ficando de pé",
      "Sim, estou ficando de pé",
      "Estou me levantando",
      "Já vou ficar de pé",
      "Quase de pé"
   ],
   "fimListagem(ITEMS)": [
      "Ok encerrou a lista de {0}",
      "Não tenho mais {0} pra listar",
      "Acabei a lista de {0}"
   ],
   "inParaClinica": [
      "Vou ir para a clínica",
      "Tenho que ir para a clínica",
      "Está na hora de ir para a clínica",
      "Devo ir para a clínica"   ],
   "informeResposta": [
      "Qual a resposta",
      "Diga a resposta",
      "Informe a resposta",
      "Mas agora me passe a resposta",
      "Agora informe a resposta",
      "Agora me diga a resposta"
   ],
   "levantando(DACOISA)": [
      "OK, levantando {0}",
      "Sim, estou me levantando {0}",
      "Já estou me levantando {0}",
      "Estou me levantando {0}",
      "Sim, estou levantando {0}",
      "Ok estou me levantando {0}",
      "Estou levantando {0}"
   ],
   "levantando(OMEMBRO;NAPOSICAO)": [
      "OK, levantando {0} {1}",
      "Levantando {0} {1}",
      "Já estou levantando {0} {1}",
      "Estou levantando {0} {1}",
      "Sim, levantando {0} {1}",
      "Estou levantando {0} {1}"
   ],
   "lembroLugarExato": [
      "Ok, conheço o lugar ",
      "Me lembro do local ",
      "Sim conheço o lugar "
   ],
   "lembroLugarExato(NOME)": [
      "Ok, conheço o lugar chamado {0}",
      "Me lembro do local com nome {0}",
      "Sim conheço o lugar {0} "
   ],
   "lembroLugarParecido": [
      "Ok, conheço um lugar parecido ",
      "Me lembro de um local similar ",
      "Sim conheço um lugar que talvez seja esse "
   ],
   "lembroLugarParecido(NOME)": [
      "Ok, conheço um lugar parecido chamado {0}",
      "Me lembro de um local similar: {0}",
      "Sim, conheço um lugar que talvez seja esse: {0} "
   ],
   "meuNomeEh(NOME)": [
      "Meu nome é {0}",
      "O meu nome é {0}",
      "Me chamo {0}",
      "Eu me chamo {0}"
   ],
   "naoAcheiLugar": [
      "Não encontrei o lugar",
      "Desculpa, não achei o lugar",
      "Puxa vida, não sei onde está o local",
      "Ué, não sei que lugar você está falando",
      "Puxa, não consigo achar o lugar",
      "De que lugar você está falando?",
      "Qual o local que você está falando?",
      "Onde está esse local?"
   ],
   "naoAcheiObjeto": [
      "Desculpa, então não era esse objeto",
      "Então não é isso",
      "Pena que não é esse objeto",
      "Não é isso, talvez seja outra coisa"
   ],
   "naoConhecoCenas": [
      "Não conheço nenhuma cena",
      "Não tenho informações sobre nenhuma cena",
      "Olha, não me disseram nada sobre alguma cena"
   ],
   "naoConhecoComEsseNome": [
      "Não conheço nada com esse nome",
      "Não tenho informações sobre algum objeto ou lugar com esse nome",
      "Olha, não sei de nada com esse nome",
      "Não conheço coisa ou local com esse nome",
      "Com esse nome, não conheço nada",
      "Não me lembro de nada com esse nome"
   ],
   "naoConhecoLugaresAqui": [
      "Não conheço nenhum lugar em especial",
      "Não tenho informações sobre nenhum local em particular",
      "Olha, não me disseram nada sobre os lugares que têm aqui"
   ],
   "naoConhecoObjetosAqui": [
      "Não conheço nenhum objeto em especial",
      "Não tenho informações sobre nenhum objeto em particular",
      "Veja, não me disseram nada sobre os objetos por aqui"
   ],
   "naoConhecoTarefas": [
      "Não conheço nenhuma tarefa ou atuação",
      "Não sei fazer nenhuma tarefa",
      "Não sei fazer nenhuma atuação",
      "Não me ensinaram nenhuma atuação",
      "Não me ensinaram nenhuma tarefa"
   ],
   "naoConhecoUsoObjeto": [
      "Não conheço pra que esse objeto é usado",
      "Não sei pra que essa coisa serve",
      "Olha, não me disseram nada sobre pra esse objeto serve",
      "Não tenho informações sobre pra que essa coisa é usada"
   ],
   "naoDisseAtributo": [
      "Você não disse no fim da frase qual propriedade/atributo devo aprender",
      "O que você quer que eu aprenda? Diga isso no fim da frase",
      "No fim da frase diga qual propriedade ou atributo eu devo aprender"
   ],
   "naoEntendiFala": [
      "Não entendi o que você disse",
      "Não comprendi nada do que você falou", 
      "Ué, o que você falou?"
   ],
   "naoEntendiInfoLugar": [
      "Não entendi o que você quer que eu aprenda sobre esse lugar",
      "Não comprendi a informação que você passou sobre aqui",
      "Não entendi o que você está falando sobre esse local"
   ],
   "naoEntendiInfoObjeto": [
      "Não entendi o que você quer que eu aprenda sobre esse objeto",
      "Não comprendi a informação que você passou sobre isso",
      "Não entendi o que você está falando sobre essa coisa"
   ],
   "naoEntendiQueDisseSobre(PROP;COISA)": [
      "Não entendi o que você falou sobre {0} {1}",
      "Não comprendi o que você disse sobre {0} {1}",
      "Não entendi o que você disse sobre {0} {1}"
   ],
   "naoFalouPergunta": [
      "Ué você não falou nenhuma pergunta",
      "Mas você não disse nenhuma pergunta",
      "Qual é a pergunta afinal? Você não me passou a pergunta"
   ],
   "naoFalouResposta": [
      "Humm, mas você não falou qual é a resposta",
      "Mas você não disse a resposta",
      "Qual é a resposta? Você tem que informar a resposta"
   ],
   "naoLembroLugar": [
      "Não me lembro de nenhum lugar como nome parecido com esse",
      "Não sei de um lugar como esse que você falou",
      "Não reconheço nenhum lugar com esse nome ou descrição"
   ],
   "naoLembroLugarChamado(NOME)": [
      "Não me lembro de nenhum lugar com nome ou descrito como {0}",
      "Não lembro de nenhum local chamado ou descrito como {0}",
      "Não sei de um lugar com nome ou descrição de {0}",
      "Não reconheço nenhum lugar com nome ou descrição de {0}"
   ],
   "naoLembroMeuNome": [
       "Isso é estranho, mas não lembro meu nome",
       "Que coisa estranha, mas não lembro meu nome",
       "Não estou conseguindo lembrar meu nome"
   ],
   "naoReconhecoObjeto": [
      "Ué, não sei o que é isso",
      "Puxa, não consigo identificar essa coisa",
      "Não lembro o que é esse objeto",
      "Não reconheço esse objeto"
   ],
   "naoReconhecoLugar": [
      "Não conheço esse lugar",
      "Não lembro nada sobre esse local",
      "Não tenho informações sobre esse local aqui",
      "Não sei nada especial desse lugar"
   ],
   "naoReconhecoNomeLugar": [
      "Não sei o nome desse local", 
      "Não sei o nome daqui",
      "Não sei como esse local se chama", 
      "Não me disseram como esse lugar se chama ", 
      "Não me ensinaram o nome daqui"
   ],
   "naoReconhecoDescricaoLugar": [
      "Não sei a descrição desse local", 
      "Não me disseram a descrição desse lugar ", 
      "Não me falaram a descrição daqui"
   ],
   "naoReconhecoEventoLugar": [
      "Não sei o que ocorreu nesse local", 
      "Não sei o que aconteceu aqui", 
      "Não me disseram o que ocorreu aqui ", 
      "Não me falaram sobre eventos que ocorreram aqui"
   ],
  "naoReconheco(PROP;COISA)": [
      "Não sei {0} {1}", 
      "Não me disseram {0} {1}", 
      "Não me falaram {0} {1}"
   ],
   "naoSei": [
      "Não sei",
      "Hum, não sei",
      "Não sei mesmo",
      "Puxa, não tenho ideia"
   ],
   "naoSeiOndeVoceEsta": [
      "Não sei onde você está",
      "Não te achei",
      "Não te vejo",
      "Não vejo você",
      "Cadê você?",
      "Ué, onde você está",
      "Não estou te vendo"
   ],
   "naoSeiQualAtributo": [
      "Você não disse qual característica que você quer informação",
      "Não sei qual a propriedade que você quer saber informação",
      "Não sei sobre que propriedade você quer informação"
   ],
   "naoVejo(ACOISA)": [
      "Não vejo {0}",
      "Não vi {0}",
      "Não sei onde está {0}",
      "Não consigo ver {0}",
      "Qual {0} que você está falando?",
      "Onde está {0}?",
      "Acho que {0} não está aqui"
   ],
   "naoVejoLugar": [
      "De que lugar você está falando. Onde você está?",
      "Não vejo você, onde está esse lugar?",
      "Não sei onde é esse lugar"
   ],
   "naoVejoObjeto": [
      "Não vejo a coisa que você falou",
      "Não vejo o objeto que você disse",
      "Não vi nada como o que você falou",
      "Não vejo nenhum objeto por aqui",
      "De que coisa você está falando?",
      "Qual o objeto que você está falando?",
      "Não vejo nenhuma coisa aqui perto",
      "Onde está esse objeto que você falou?",
      "Não tem nenhuma coisa por aqui",
      "Não vi nada por aqui",
      "Não vejo objetos nesse lugar"
   ],
   "naoVouSeguirVoce": [
      "OK paro de te seguir",
      "Vou parar de seguir voce",
      "Não vou ficar mais com voce",
      "Não vou te acompanhar mais"
   ],
   "nomeObjetoMundoVirtual(NOME)": [
      "No mundo virtual o nome deste objeto é {0}",
      "Dentro da realidade virtual o nome disso é {0}",
      "O nome de objeto dentro do mundo virtual é {0}"
   ],
   "okAprendi": [
      "OK, aprendi",
      "Vou lembrar",
      "Agora sei"
   ],
  "parandoDeMover(OMEMBRO)": [
      "OK, parando de mover {0}",
      "Parando de mover {0}",
      "Relaxando {0}",
      "Parando {0}",
      "Estou parando {0}"
   ],
   "pararTour": [
      "OK, paramos de fazer o tour",
      "OK, paramos o tour",
      "Sim, paramos o passeio",
      "Certo, finalizamos o passeio"
   ],
   "pararTourProblema": [
      "Vou ter que parar o tour, porque que não consigo chegar no lugar", 
      "Vamos parar com o passeio, porque não estou conseguindo ir para o lugar",
      "Vamos ter que parar com o tour, porque não vou conseguir chegar no lugar"
   ],
   "pareiListagem": [
      "Ok, parei a lista",
      "Tá bom, chega de listar",
      "Ok, parei de listar"
   ],
   "pecaAjuda": [
      "Peça ajuda sobre as conversas que eu entendo com 'ajuda conversas'",
      "Se você dizer 'ajuda conversas' te explico as conversas que entendo",
      "Diga 'ajuda conversas' que te explico as conversas que entendo"
   ],
   "pecaAjudaConversa": [
      "Também ajudo com uma conversa específica, fale 'ajuda conversa' seguido do nome da conversa",
      "Posso ajudar com uma conversa específica, false 'ajuda conversa' e o nome da conversa",
      "Ajudo com conversas específicas também, diga 'ajuda conversa' seguido do nome da conversa"
   ],
   "pedeConfirmacaoObjeto": [
      "OK, é isso?",
      "É essa coisa?",
      "É esse objeto?",
      "Apontei pra coisa certa?"
   ],
   "perfilEstagiario":[
      "Posso aprender facilmente nomes e informações sobre objetos e lugares.\n"+
         "Depois posso responder perguntas e explicar o que aprendi.\n"+
         "E posso mostrar para as pessoas como chegar nos lugares que conheço daqui.",
      "Estou aprendendo nomes e informações sobre objetos e lugares.\n"+
         "Então posso responder perguntas e explicar o que aprendi.\n"+
         "Também posso mostrar para as pessoas como chegar nos locais que conheço."
   ],
   "perguntaInformacaoLugar": [
      "Se quiser saber algo mais sobre o local basta perguntar", 
      "Sei mais coisas sobre esse lugar, é só perguntar",
      "Tenho mais informações sobre este lugar, é só perguntar"
   ],
   "podeIndicarDeNovo": [
      "Você pode indicar de novo",
      "Pode me mostrar de novo",
      "Por favor, mostre novamente",
      "Pode indicar novamente",
      "Pode apontar de novo"
   ],
   "podeRepetir": [
      "Você pode repetir",
      "Pode falar de novo",
      "Por favor, fale novamente"
   ],
   "qualMesmo(ACOISA)": [
      "Qual {0} mesmo?",
      "Que {0} mesmo?",
      "Qual {0} tu queria mesmo?",
      "Você precisa informar {0}"
   ],
   "querEnsinarMaisBatePapos":[
      "Quer ensinar mais um bate-papo?",
      "Quer seguir ensinando perguntas e respostas?",
      "Quer ensinar mais bate-papos?",
      "Quer ensinar mais uma pergunta e resposta?"
   ],
   "querVerMaisBatePapos": [
      "Quer seguir vendo os outros bate-papos que eu entendo?",
      "Conheço outros bate-papos, quer ver eles também?",
      "Não listei todos os bate-papos que conheço, quer ver os demais?"
   ],
   "querVerMaisCenas": [
      "Quer seguir vendo as outras cenas que conheço?",
      "Conheço outras cenas, quer seguir vendo elas?",
      "Não listei todas as cenas que conheço, quer ver as demais?"
   ],
   "querVerMaisConversas": [
      "Quer seguir vendo as outras conversas que eu entendo?",
      "Conheço outras conversas, quer ver elas também?",
      "Não listei todas as conversas que conheço, quer ver as demais?"
   ],
   "querVerMaisLugares": [
      "Quer seguir vendo os outros locais que conheço?",
      "Conheço outros lugares, quer seguir vendo eles?",
      "Não listei todas os lugares que conheço, quer ver os demais?"
   ],
   "querVerMaisObjetos": [
      "Quer seguir vendo os outros objetos que conheço?",
      "Conheço outras coisas, quer seguir vendo elas também?",
      "Não listei todos os objetos que conheço, quer ver os demais?"
   ],
   "querVerMaisTarefas": [
      "Quer seguir vendo as outras tarefas que conheço?",
      "Conheço outras atuações, quer seguir vendo elas?",
      "Não listei todas as tarefas que conheço, quer ver as demais?"
   ],
   "reconhecoSeguintes(COISAS)": [
      "Reconheço seguintes {0}",
      "Reconheço próximos {0}",
      "Entendo seguintes {0}",
      "Compreendo seguintes {0}",
      "Compreendo próximos {0}",
      "Sei seguintes {0}"
   ],
   "respostaNao": [
      "Não foi possível",
      "Opa! não deu",
      "Não deu certo!",
      "Deu problema"
   ],
   "respostaSaudacoes": [
      "Oi, tudo bem?",
      "Oi amigo, estou bem e você?",
      "Olá para você também"
   ],
   "respostaSim": [
      "Ok",
      "Sim",
      "Tá bem",
      "Tudo bem",
      "É isso",
      "Claro que sim",
      "Tá OK",
      "Sem problemas",
      "Sim claro",
      "Tudo tranquilo"
   ],
   "saudacoesIniciais": [
      "Oi!",
      "Olá!",
      "Prazer em te ver",
      "Que bom te ver",
      "Alô!",
      "Bom te ver"
   ],
   "sePrecisarAjuda": [
      "Se precisar de ajuda é só pedir de novo",
      "Mas se quiser ajuda de novo é só pedir",
      "Caso precise de ajuda novamente é só falar"
   ],
   "segueListagem(ITEMS)": [
      "Aí vão mais {0} que entendo",
      "Seguem mais {0} que compreendo",
      "Outras {0} que compreendo",
      "Mais {0} que posso entender"
   ],
   "semPadraoFrase": [
      "Não tenho nenhum padrão de frase pra começar essa conversa",
      "Não conheço nenhum padrão de frase pra começar essa conversa",
      "Não entendo nenhum padrão de conversa para iniciar esse diálogo",
      "Não reconheço nenhum padrão de diálogo inicial para essa conversa"
   ],
   "sentei(NACOISA)": [
      "OK, sentei {0}",
      "Sim, sentei {0}",
      "Já me sentei {0}",
      "Sim, já me sentei {0}",
      "Ok estou sentado {0}",
      "Estou sentado {0}"
   ],
   "sinonAntes": [
      "antes",
      "anteriormente",
      "previamente"
   ],
   "sinonCena": [
      "cena",
      "cenário"
   ],
   "sinonCenas": [
      "cenas",
      "cenários"
   ],
   "sinonConversa": [
      "conversa",
      "diálogo"
   ],
   "sinonConversas": [
      "conversas",
      "diálogos"
   ],   
   "sinonLugar": [
      "lugar",
      "local"
   ],
   "sinonLugares": [
      "lugares",
      "locais"
   ],
   "sinonObjeto": [
      "objeto",
      "coisa"
   ],
   "sinonObjetos": [
      "objetos",
      "coisas"
   ],
   "sinonTarefa": [
      "tarefa",
      "atuação",
      "performance"
   ],
   "sinonTarefas": [
      "tarefas",
      "atuações",
      "performances"
   ],
   "temResposta": [
      "Deve ser respondida com",
      "Tem resposta",
      "É respondida com"
   ],
   "tenhoPadroesFrase": [
      "Tenho os seguintes padrões de frase para iniciar essa conversa",
      "Conheço os seguintes padrões de conversa para começar esse diálogo",
      "Entendo os seguintes padrões de frase pra começar essa conversa"
   ],
   "vamosProximoLugar": [
      "OK, vamos ao próximo local",
      "Sim, vamos ao lugar seguinte",
      "Certo, vamos ao próximo local"
   ],
   "vemComigoPrimeiroLugar": [
      "Venha comigo, estou indo para o primeiro lugar", 
      "Vamos juntos ao primeiro local que conheço",
      "Vou ir ao primeiro lugar que conheço, venha comigo"
   ],
   "vemComigoProximoLugar": [
      "Venha comigo por favor, estou indo ao próximo local", 
      "Vamos juntos ao próximo local que conheço",
      "Venha que já estou indo ao próximo lugar"
   ],
   "venhaComigo": [
      "Venha comigo",
      "Vamos juntos",
      "Vamos agora",
      "Venha agora"
   ],
   "viOutrosObjetosAqui": [
      "Também vi outros objetos aqui",
      "Vi também outras coisas por aqui",
      "Notei também outras coisas aqui"
   ],
   "virando(OMEMBRO;NAPOSICAO)": [
      "OK, virando {0} {1}",
      "Virando {0} {1}",
      "Já estou virando {0} {1}",
      "Estou virando {0} {1}",
      "Sim, virando {0} {1}",
      "Estou virando {0} {1}"
   ],
   "voceEstaDistante": [
      "Você está muito distante",
      "Venha mais perto, você está distante",
      "Você está muito longe",
      "Você está distante demais"
   ],
   "voltarPosicaoInicial": [
      "Vou voltar para minha posição inicial",
      "Vou me teleportar para a posição inicial",
      "Vou ir pra minha posição inicial",
      "Estou voltando para a posição inicial",
      "Voltando pra posição inicial"
   ],
   "vouIrAte(X;Y)": [
      "OK, vou ir até {0},{1}",
      "Vou tentar caminhar até o local {0},{1}",
      "Estou indo para a posição {0},{1}"
   ],
   "vouLembrarPergunta(QUESTAO)": [
      "Sim, aprendi a pergunta: {0}",
      "Ok, vou lembrar a pergunta: {0}",
      "Registrei a pergunta: {0}"
   ],
   "vouLembrarQuePergunta": [
      "Sim, aprendi que a pergunta",
      "Ok, vou lembrar que a pergunta",
      "Registrei que a pergunta"
   ],
   "vouSeguirVoce": [
      "OK estou indo com você",
      "Vou seguir você",
      "Vou ir com você",
      "Vou te seguir sim",
      "Vou com você"
   ],
   "vouTentarComecar(ATIV)": [
      "Ok espero poder começar {0}",
      "Acho que vou começar {0}",
      "Vou tentar começar {0}"
   ],
   "vouTentarParar(ATIV)": [
      "Ok parando {0}",
      "Acho que vou parar {0}",
      "Vou tentar parar {0}"
   ]
}
