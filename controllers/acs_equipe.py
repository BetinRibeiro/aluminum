# -*- coding: utf-8 -*-

def conferir():
  response.view = 'generic.html' # use a generic view
  vendedor = db.vendedor(request.args(0, cast=int))
  a=False
  if ('cfrd' in vendedor.nome) or ('CFRD' in vendedor.nome):
    a=True
    vendedor.nome=vendedor.nome.replace('cfrd','').replace('CFRD','')
  else:
    vendedor.nome=vendedor.nome+'cfrd'
  vendedor.update_record()
  redirect(URL('index', args=vendedor.projeto))
  return locals()

def trocar():
  response.view = 'generic.html' # use a generic view
  venda = db.venda(request.args(0, cast=int))
  #132 partição geral 14 dede
  venda.sub_venda=15478
  venda.update_record()
  redirect(URL('acessar_venda', args=venda.vendedor))
  return locals()
@auth.requires_login()
def index():
    usuario=auth.user
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.vendedor.projeto == request.args(0, cast=int)).select(orderby=~db.vendedor.total_vendas)
    if projeto.empresa==17:
        redirect(URL('vendedores_boletos', args=projeto.id))
    return locals()

@auth.requires_login()
def vendedores_boletos():
    usuario=auth.user
    projeto = db.projeto(request.args(0, cast=int))
    total_boletos = db(db.boleto.projeto==projeto.id).count()
    id=0
    conexao = db.conexao(db.conexao.projeto==projeto.id)
    if not conexao:
        id=db.conexao.update_or_insert((db.conexao.projeto == projeto.id),
                           projeto=projeto.id,
                           chave_acesso='#',
                           total_boletos=0)
        conexao = db.conexao(id)
    rows = db(db.vendedor.projeto == request.args(0, cast=int)).select(orderby=~db.vendedor.total_vendas)
    return locals()

@auth.requires_login()
def atualizar_boletos():
    response.view = 'generic.html' # use a generic view
    conexao = db.conexao(request.args(0, cast=int))
    projeto = db.projeto(conexao.projeto)
    import json
    import urllib, urllib2
    import gluon.contrib.simplejson as sj
    import datetime
    headers = {
        'Content-Type': 'application/json',
        'access_token': conexao.chave_acesso
    }
    req = Request('https://www.asaas.com/api/v3/payments?dateCreated%5Bge%5D='+(conexao.data_inicio).strftime("%Y-%m-%d")+'&dateCreated%5Ble%5D='+(conexao.data_final).strftime("%Y-%m-%d")+'&offset=3&limit=50', headers=headers)
    page = urlopen(req).read()
    total_boletos=json.loads(page).values()[1]
    total_paginas = total_boletos/50
    #total_paginas=2
    a=0
    while a<total_boletos:
        req = Request('https://www.asaas.com/api/v3/payments?dateCreated%5Bge%5D='+(conexao.data_inicio).strftime("%Y-%m-%d")+'&dateCreated%5Ble%5D='+(conexao.data_final).strftime("%Y-%m-%d")+'&offset='+str(a)+'&limit=50', headers=headers)
        page = urlopen(req).read()
        page=json.loads(page)
        for row in page.values()[5]:
          cobrado=True
          if row.get("value")=="OVERDUE":
            cobrado=False
          id=db.boleto.update_or_insert((db.boleto.id_asaas == row.get("id")),
                           id_asaas=row.get("id"),
                           #projeto=projeto.id,
                           #description=row.get("description"),
                           value_total=row.get("value"),
                           status=row.get("status"),
                           due_date=row.get("dueDate"),
                           value_receber=row.get("netValue"))
        a+=50
    
    #redirect(URL('vendedores_boletos', args=projeto.id))
    return dict(page=page,total_boletos=total_boletos,total_paginas=total_paginas,a=a)

@auth.requires_login()
def ver_boletos():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.boleto.projeto==projeto.id).select(orderby=db.boleto.due_date)
    consul=(request.args(1))
    if (consul):
        rows = db((db.boleto.projeto==projeto.id)and(db.boleto.description.contains(consul))).select(orderby=db.boleto.due_date)
    return locals()
  
@auth.requires_login()
def deletar_tudo():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.boleto.projeto==projeto.id).delete()
    redirect(URL('ver_boletos', args=projeto.id))
    return locals()
  
@auth.requires_login()
def alterar_acesso():
    response.view = 'generic.html' # use a generic view
    conexao = db.conexao(request.args(0, cast=int))
    projeto = db.projeto(conexao.projeto)
    db.conexao.id.readable = False
    db.conexao.id.writable = False

    db.conexao.projeto.readable = False
    db.conexao.projeto.writable = False
    deletar=False
    usuario = auth.user
    form = SQLFORM(db.conexao, request.args(0, cast=int), deletable=deletar)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('vendedores_boletos', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
  
@auth.requires_login()
def adicionar_vendedor():
    response.view = 'generic.html' # use a generic view
    projeto = db.projeto(request.args(0, auth.user))

    db.vendedor.projeto.default = projeto.id
    db.vendedor.projeto.writable = False
    
    db.vendedor.comissao_cobranca.readable = False
    db.vendedor.comissao_cobranca.writable = False

    form = SQLFORM(db.vendedor).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('index', args=projeto.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)

@auth.requires_login()
def acessar_venda():
    usuario = auth.user
    vendedor = db.vendedor(request.args(0, cast=int))
    projeto = db.projeto(vendedor.projeto)
    rows_sub = db(db.sub_venda.projeto == vendedor.projeto).select(orderby=~db.sub_venda.data_inicio_cobranca)
    rows_vend = db(db.venda.vendedor == request.args(0, cast=int)).select(orderby=db.venda.sub_venda|db.venda.data_venda)
    return locals()

@auth.requires_login()
def alterar_vendedor():
    response.view = 'generic.html' # use a generic view
    vendedor = db.vendedor(request.args(0, cast=int))
    projeto = db.projeto(vendedor.projeto)
    if 'cfrd' in vendedor.nome:
      redirect(URL('index', args=projeto.id))
    db.vendedor.id.readable = False
    db.vendedor.id.writable = False

    db.vendedor.projeto.readable = False
    db.vendedor.projeto.writable = False
    
    db.vendedor.comissao_cobranca.readable = False
    db.vendedor.comissao_cobranca.writable = False
    
    deletar=True
    if vendedor.total_vendas>0:
        deletar=False
    usuario = auth.user
    if usuario.id==2234:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('index', args=projeto.id))
    form = SQLFORM(db.vendedor, request.args(0, cast=int), deletable=deletar)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('index', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)


@auth.requires_login()
def inserir_venda():
    response.view = 'generic.html' # use a generic view
    vendedor = db.vendedor(request.args(0, auth.user))
    sub_venda = db.sub_venda(request.args(1, auth.user))
    
    db.venda.sub_venda.default = sub_venda.id
    db.venda.sub_venda.writable = False
    db.venda.sub_venda.readable = False
    
    db.venda.quant_fichas_devolvidas.writable = False
    db.venda.quant_fichas_devolvidas.readable = False
    
    db.venda.valor_devolvido.writable = False
    db.venda.valor_devolvido.readable = False
    
    db.venda.vendedor.default = vendedor.id
    db.venda.vendedor.writable = False
    
    
    usuario = auth.user
    if usuario.id==243344:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('acessar_venda', args=vendedor.id))
    form = SQLFORM(db.venda).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acessar_venda', args=vendedor.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)

@auth.requires_login()
def vincular_vendedor():
    response.view = 'generic.html' # use a generic view
    vendedor = db.vendedor(request.args(0, cast=int))
    projeto = db.projeto(vendedor.projeto)
    db.vendedor.id.readable = False
    db.vendedor.id.writable = False

    db.vendedor.projeto.readable = False
    db.vendedor.projeto.writable = False
    

    db.vendedor.nome.readable = False
    db.vendedor.nome.writable = False
    
    db.vendedor.comissao_cobranca.readable = False
    db.vendedor.comissao_cobranca.writable = False
    
    db.vendedor.vale_saida.readable = False
    db.vendedor.vale_saida.writable = False
    
    db.vendedor.descricao.readable = False
    db.vendedor.descricao.writable = False
    
    db.vendedor.comissao_venda.readable = False
    db.vendedor.comissao_venda.writable = False
    
    db.vendedor.funcionario_empresa.readable = True
    db.vendedor.funcionario_empresa.writable = True
    db.vendedor.funcionario_empresa.writable = True
    db.vendedor.funcionario_empresa.requires = IS_IN_DB(db((db.funcionario_empresa.empresa == projeto.empresa)&(db.funcionario_empresa.bloqueado == False)), 'funcionario_empresa.id', '%(nome)s')
    
    deletar=True
    if vendedor.total_vendas>0:
        deletar=False
    usuario = auth.user
    if usuario.id==2234:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('index', args=projeto.id))
    form = SQLFORM(db.vendedor, request.args(0, cast=int), deletable=deletar)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('index', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)


@auth.requires_login()
def alterar_venda():
    response.view = 'generic.html' # use a generic view
    venda = db.venda(request.args(0, cast=int))
    vendedor = db.vendedor(venda.vendedor)
    db.venda.id.readable = False
    db.venda.id.writable = False
        
    db.venda.sub_venda.default = venda.sub_venda
    db.venda.sub_venda.writable = False
    db.venda.sub_venda.readable = False

    db.venda.vendedor.readable = False
    db.venda.vendedor.writable = False
    
    usuario = auth.user
    if usuario.id==2324:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('acessar_venda', args=vendedor.id))

    form = SQLFORM(db.venda, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acessar_venda', args=vendedor.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

  
def relacao_individual():
  projeto = db.projeto(request.args(0, cast=int))
  rows = db(db.vendedor.projeto == request.args(0, cast=int)).select(orderby=~db.vendedor.total_vendas)
  return locals()

def alterar_comissoes_vendedor():
  response.view = 'generic.html' # use a generic view
  vendedor = db.vendedor(request.args(0, cast=int))
  projeto = db.projeto(vendedor.projeto)
  db.vendedor.id.readable = False
  db.vendedor.id.writable = False
  db.vendedor.nome.writable = False
  db.vendedor.nome.readable = True
  db.vendedor.vale_saida.readable = False
  db.vendedor.vale_saida.writable = False
  db.vendedor.descricao.writable = False
  db.vendedor.descricao.readable = False
  db.vendedor.comissao_venda.writable = False
  db.vendedor.comissao_cobranca.readable = True
  db.vendedor.comissao_cobranca.writable = True
  db.vendedor.total_descontado.readable = True
  db.vendedor.total_descontado.writable = True

  db.vendedor.total_prego.readable = True
  db.vendedor.projeto.readable = True
  db.vendedor.projeto.writable = False
  deletar=True
  if vendedor.total_vendas>0:
      deletar=False
  usuario = auth.user
  if usuario.id==2234:
      session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
      redirect(URL('index', args=projeto.id))
  form = SQLFORM(db.vendedor, request.args(0, cast=int), deletable=deletar)
  if form.process().accepted:
      session.flash = 'Atualizado'
      redirect(URL('relacao_individual', args=projeto.id))
  elif form.errors:
      response.flash = 'Erros no formulário!'
  else:
      if not response.flash:
          response.flash = 'Preencha o formulário!'
  return dict(form=form)
