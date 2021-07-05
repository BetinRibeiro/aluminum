# -*- coding: utf-8 -*-
#acessa todas as carradas cadastradas
#dentro de cada carrada possui uma lista de produtos que compom o total
#chagamos aqui pela tela de acesso principal
@auth.requires_login()
def acesso_carradas():
    #busca no bando de dados o projeto que estamos trabalhando
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    usuario = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user)
    if usuario.bloqueado==True:
      redirect(URL('acs_mensagem','usuario_bloqueado',args="Usuario Temporariamente Bloqueado!"))
    if usuario.empresa!=projeto.empresa:
      usuario.bloqueado=True
      usuario.nome="Bloqueio (tentou acessar outro projeto, mercadoria.acesso_carradas)"
      usuario.update_record()
      redirect(URL('acs_mensagem','usuario_bloqueado',args="Usuario Temporariamente Bloqueado!"))
    rows = db(db.carrada.projeto == projeto.id).select(orderby=db.carrada.data_envio)
    return locals()

@auth.requires_login()
def acesso_item_carrada():
    carrada = db.carrada(request.args(0, cast=int))
    rows = db(db.item_carrada.carrada == request.args(0, cast=int)).select(orderby=~db.item_carrada.q_pcs)
    return dict(rows=rows, carrada=carrada)

#funções descontinuadas não vi mais a necessidade de deixar essa alteração na mao
# no chefe da equipes, problemas podem acontecer nisso verificar se possui algum problema

#cria carrada
#chegamos aqui pelo acesso as carradas@auth.requires_login()
def conferir():
  redirect(URL('default','index'))
  response.view = 'generic.html' # use a generic view
  item_carrada = db.item_carrada(request.args(0, cast=int))
  a=False
  if 'cfrd' in item_carrada.descricao:
    a=True
    item_carrada.descricao=item_carrada.descricao.replace('cfrd','')
  else:
    item_carrada.descricao=item_carrada.descricao+'cfrd'
  item_carrada.update_record()
  redirect(URL('acesso_item_carrada', args=item_carrada.carrada))
  return locals()
def conferir_retorno():
  redirect(URL('default','index'))
  response.view = 'generic.html' # use a generic view
  item_carrada = db.item_carrada(request.args(0, cast=int))
  a=False
  if 'rtnc' in item_carrada.descricao:
    a=True
    item_carrada.descricao=item_carrada.descricao.replace('rtnc','')
  else:
    item_carrada.descricao=item_carrada.descricao+'rtnc'
  item_carrada.update_record()
  redirect(URL('acesso_item', args=item_carrada.projeto))
  return locals()
@auth.requires_login()
def criar_carrada():
  redirect(URL('default','index'))
  response.view = 'generic.html' # use a generic view
  #busca o projeto pelo id passado
  projeto = db.projeto(request.args(0, auth.user))
  if projeto.venda_finalizada:
      session.flash = 'A venda já foi finalizada'
      redirect(URL('acesso_carradas', args=projeto.id))
  #insere na coluna projeto o id do projeto atual
  db.carrada.projeto.default = projeto.id
  #bloqueia o espaço de projeto para que o usuario não consiga ver
  db.carrada.projeto.writable = False
  #form é uma variavel que recebe o formulario passado para a view
  form = SQLFORM(db.carrada).process()
  #caso o furmulario seja submetido
  if form.accepted:
      #mensagem que o formulario foi aceito
      response.flash = 'Carrada Inserida'
      #redireciona para o acesso as carradas passando como argumento o id do projeto
      redirect(URL('acesso_carradas', args=projeto.id))
  elif form.errors:
      #caso tenha erro no formulario aparecerá mensagem de erro
      response.flash = 'Formulario não aceito'
  return dict(form=form)

@auth.requires_login()
def alterar_carrada():
  redirect(URL('default','index'))
  response.view = 'generic.html' # use a generic view
  usuario=auth.user
  usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user)
  carrada = db.carrada(request.args(0, cast=int))
  projeto = db.projeto(carrada.projeto)
  empresa = db.empresa(projeto.empresa)
  if projeto.venda_finalizada:
    session.flash = 'A venda já foi finalizada'
    redirect(URL('acesso_carradas', args=projeto.id))
  db.carrada.id.readable = False
  db.carrada.id.writable = False

  db.carrada.finalizada.readable = True
  db.carrada.finalizada.writable = True
  db.carrada.projeto.readable = False
  db.carrada.projeto.writable = False
  deletable=True
  if carrada.total_pecas>0:
    deletar =False
  if (carrada.finalizada):
    db.carrada.finalizada.readable = False
    db.carrada.finalizada.writable = False
    db.carrada.descricao.readable = True
    db.carrada.descricao.writable = False
    db.carrada.data_envio.readable = True
    db.carrada.data_envio.writable = False
  if (usuario_empresa.tipo=="Proprietário")|(usuario_empresa.tipo=="Administrador"):
    db.carrada.finalizada.readable = True
    db.carrada.finalizada.writable = True
  form = SQLFORM(db.carrada, request.args(0, cast=int), deletable=deletar)
  if form.process().accepted:
      session.flash = 'Atualizado'
      redirect(URL('acesso_carradas', args=projeto.id))
  elif form.errors:
      response.flash = 'Erros no formulário!'
  return dict(form=form)

def verifica():
  redirect(URL('default','index'))
  carrada = db.carrada(request.args(0, cast=int))
  if carrada.finalizada:
    carrada.finalizada=False
  else:
    carrada.finalizada=True
  carrada.update_record()

  return redirect(URL('acesso_carradas', args=carrada.projeto))


@auth.requires_login()
def gerar_mercadorias():
  redirect(URL('default','index'))
  carrada = db.carrada(request.args(0, cast=int))
  projeto = db.projeto(projeto.carrada==carrada.id)
  lista=['JG PANELA TAMPA DE VIDRO','MANTIMENTO','JG DE PANELÃO','PANELA PRESSÃO 10L','PANELA PRESSÃO 7L','PANELA PRESSÃO 4.5L','FRIGIDEIRAS 3 PC']
  for nome in lista:
      db.item_carrada.insert(equipe=projeto.id,carrada=carrada.id,descricao=nome)
  return redirect(URL('acesso_item_carrada', args=request.args(0, auth.user)))

@auth.requires_login()
def criar_item_carrada():
  redirect(URL('default','index'))
  response.view = 'generic.html' # use a generic view
  carrada = db.carrada(request.args(0, auth.user))
  projeto = db.projeto(carrada.projeto)
  empresa = db.empresa(projeto.empresa)
  if projeto.venda_finalizada:
      session.flash = 'A venda já foi finalizada'
      redirect(URL('projeto','acesso_projeto', args=projeto.id))
  db.item_carrada.projeto.default = projeto.id

  db.item_carrada.carrada.default = carrada.id
  db.item_carrada.carrada.writable = False

  if projeto.auth_user!=auth.user.id:
      db.item_carrada.custo_unitario.readable = True
      db.item_carrada.custo_unitario.writable = True


  db.item_carrada.projeto.default = carrada.projeto
  db.item_carrada.projeto.writable = False

  db.item_carrada.projeto.readable = False
  db.item_carrada.projeto.writable = False
  if (auth.user.id==10)or(auth.user.id==11):
      db.item_carrada.custo_unitario.readable = True
      db.item_carrada.custo_unitario.writable = True
  if (auth.user.id==1)or(auth.user.id==6):
      db.item_carrada.custo_unitario.readable = True
      db.item_carrada.custo_unitario.writable = True
  form = SQLFORM(db.item_carrada).process()
  if form.accepted:
      response.flash = 'Formulario aceito'
      redirect(URL('acesso_item_carrada', args=carrada.id))
  elif form.errors:
      response.flash = 'Formulario não aceito'
  return dict(form=form)

@auth.requires_login()
def alterar_item_carrada():
  redirect(URL('default','index'))
  response.view = 'generic.html' # use a generic view
  item_carrada = db.item_carrada(request.args(0, cast=int))
  carrada = db.carrada(item_carrada.carrada)
  if 'cfrd' in item_carrada.descricao:
      redirect(URL('acesso_item_carrada', args=carrada.id))
  projeto = db.projeto(carrada.projeto)
  if projeto.venda_finalizada:
      session.flash = 'A venda já foi finalizada'
      redirect(URL('projeto','acesso_projeto', args=projeto.id))
  db.item_carrada.id.readable = False
  db.item_carrada.id.writable = False

  db.item_carrada.projeto.default = projeto.id

  db.item_carrada.carrada.readable = False
  db.item_carrada.carrada.writable = False

  db.item_carrada.projeto.readable = False
  db.item_carrada.projeto.writable = False
  empresa = db.empresa(projeto.empresa)
  #caso o usuario da empresa for diferênte do usuario logado
  #redireciona pois será um usuario do projeto (chefe) ou
  #usuario da sub_venda(Cobrador)
  if projeto.auth_user!=auth.user.id:
      db.item_carrada.custo_unitario.readable = True
      db.item_carrada.custo_unitario.writable = True
  if auth.user.id==6:
      db.item_carrada.projeto.default = carrada.projeto
      db.item_carrada.projeto.writable = False
  if (auth.user.id==10)or(auth.user.id==11):
      db.item_carrada.custo_unitario.readable = True
      db.item_carrada.custo_unitario.writable = True
  if (auth.user.id==1)or(auth.user.id==6):
      db.item_carrada.custo_unitario.readable = True
      db.item_carrada.custo_unitario.writable = True
  form = SQLFORM(db.item_carrada, request.args(0, cast=int), deletable=True)
  if form.process().accepted:
      session.flash = 'Atualizado'
      redirect(URL('acesso_item_carrada', args=carrada.id))
  elif form.errors:
      response.flash = 'Erros no formulário!'
  return dict(form=form)

@auth.requires_login()
def acesso_item():
  redirect(URL('default','index'))
  usuario=auth.user
  projeto = db.projeto(request.args(0, cast=int))
  rowscarrada = db(db.carrada.projeto == request.args(0, cast=int)).select(orderby=db.carrada.data_envio)
  rows = db(db.item_carrada.projeto==projeto.id).select(orderby=db.item_carrada.id)
  return locals()

@auth.requires_login()
def alterar_item_carrada_gratificacao():
  redirect(URL('default','index'))
  response.view = 'generic.html' # use a generic view
  item_carrada = db.item_carrada(request.args(0, cast=int))
  carrada = db.carrada(item_carrada.carrada)
  projeto = db.projeto(carrada.projeto)
  if projeto.venda_finalizada:
      session.flash = 'A venda já foi finalizada'
      redirect(URL('projeto','acesso_projeto', args=projeto.id))
  db.item_carrada.id.readable = False
  db.item_carrada.id.writable = False
  db.item_carrada.projeto.default = projeto.id

  db.item_carrada.carrada.readable = False
  db.item_carrada.carrada.writable = False

  db.item_carrada.projeto.readable = False
  db.item_carrada.projeto.writable = False

  db.item_carrada.q_pcs.readable = False
  db.item_carrada.q_pcs.writable = False

  db.item_carrada.descricao.readable = True
  db.item_carrada.descricao.writable = False

  db.item_carrada.preco_unitario.readable = True
  db.item_carrada.preco_unitario.writable = False

  db.item_carrada.custo_unitario.readable = False
  db.item_carrada.custo_unitario.writable = False

  db.item_carrada.quant_pcs_grt.readable = True
  db.item_carrada.quant_pcs_grt.writable = True

  form = SQLFORM(db.item_carrada, request.args(0, cast=int), deletable=False)
  if form.process().accepted:
      session.flash = 'Atualizado'
      redirect(URL('acesso_item', args=carrada.projeto))
  elif form.errors:
      response.flash = 'Erros no formulário!'
  return dict(form=form)

@auth.requires_login()
def alterar_item_carrada_retorno():
  redirect(URL('default','index'))
  response.view = 'generic.html' # use a generic view
  item_carrada = db.item_carrada(request.args(0, cast=int))
  carrada = db.carrada(item_carrada.carrada)
  projeto = db.projeto(carrada.projeto)
  if projeto.venda_finalizada:
      session.flash = 'A venda já foi finalizada'
      redirect(URL('projeto','acesso_projeto', args=projeto.id))
  db.item_carrada.id.readable = False
  db.item_carrada.id.writable = False

  db.item_carrada.carrada.readable = False
  db.item_carrada.carrada.writable = False

  db.item_carrada.projeto.readable = False
  db.item_carrada.projeto.writable = False

  db.item_carrada.q_pcs.readable = False
  db.item_carrada.q_pcs.writable = False
  db.item_carrada.projeto.default = projeto.id

  db.item_carrada.descricao.readable = True
  db.item_carrada.descricao.writable = False

  db.item_carrada.preco_unitario.readable = True
  db.item_carrada.preco_unitario.writable = False

  db.item_carrada.custo_unitario.readable = False
  db.item_carrada.custo_unitario.writable = False

  db.item_carrada.quant_pcs_rtr.readable = True
  db.item_carrada.quant_pcs_rtr.writable = True

  form = SQLFORM(db.item_carrada, request.args(0, cast=int), deletable=False)
  if form.process().accepted:
      session.flash = 'Atualizado'
      redirect(URL('acesso_item', args=carrada.projeto))
  elif form.errors:
      response.flash = 'Erros no formulário!'
  return dict(form=form)

@auth.requires_login()
def alterar_item_carrada_refugo():
  redirect(URL('default','index'))
  response.view = 'generic.html' # use a generic view
  item_carrada = db.item_carrada(request.args(0, cast=int))
  carrada = db.carrada(item_carrada.carrada)
  projeto = db.projeto(carrada.projeto)
  if projeto.venda_finalizada:
      session.flash = 'A venda já foi finalizada'
      redirect(URL('projeto','acesso_projeto', args=projeto.id))
  db.item_carrada.id.readable = False
  db.item_carrada.id.writable = False

  db.item_carrada.carrada.readable = False
  db.item_carrada.carrada.writable = False

  db.item_carrada.projeto.readable = False
  db.item_carrada.projeto.writable = False

  db.item_carrada.q_pcs.readable = False
  db.item_carrada.q_pcs.writable = False

  db.item_carrada.descricao.readable = True
  db.item_carrada.descricao.writable = False

  db.item_carrada.preco_unitario.readable = True
  db.item_carrada.preco_unitario.writable = False

  db.item_carrada.custo_unitario.readable = False
  db.item_carrada.custo_unitario.writable = False

  db.item_carrada.quant_pcs_rfg.readable = True
  db.item_carrada.quant_pcs_rfg.writable = True

  form = SQLFORM(db.item_carrada, request.args(0, cast=int), deletable=False)
  if form.process().accepted:
      session.flash = 'Atualizado'
      redirect(URL('acesso_item', args=carrada.projeto))
  elif form.errors:
      response.flash = 'Erros no formulário!'
  return dict(form=form)


@auth.requires_login()
def alterar_descricao():
  redirect(URL('default','index'))
  response.view = 'generic.html' # use a generic view
  item_carrada = db.item_carrada(request.args(0, cast=int))
  carrada = db.carrada(item_carrada.carrada)
  projeto = db.projeto(carrada.projeto)
  if projeto.venda_finalizada:
      session.flash = 'A venda já foi finalizada'
      redirect(URL('projeto','acesso_projeto', args=projeto.id))
  db.item_carrada.id.readable = False
  db.item_carrada.id.writable = False

  db.item_carrada.carrada.readable = False
  db.item_carrada.carrada.writable = False

  db.item_carrada.projeto.readable = False
  db.item_carrada.projeto.writable = False

  db.item_carrada.q_pcs.readable = False
  db.item_carrada.q_pcs.writable = False

  db.item_carrada.preco_unitario.readable = True
  db.item_carrada.preco_unitario.writable = False

  db.item_carrada.custo_unitario.readable = False
  db.item_carrada.custo_unitario.writable = False

  form = SQLFORM(db.item_carrada, request.args(0, cast=int), deletable=False)
  if form.process().accepted:
      session.flash = 'Atualizado'
      redirect(URL('acesso_item', args=carrada.projeto))
  elif form.errors:
      response.flash = 'Erros no formulário!'
  return dict(form=form)

@auth.requires_login()
def relatorio_item_carrada():
  redirect(URL('default','index'))
  projeto = db.projeto(request.args(0, cast=int))
  return locals()
