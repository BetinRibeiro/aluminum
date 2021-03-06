# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    data=request.now
    empresa = db.empresa(db.empresa.auth_user==auth.user.id)
    usuario=auth.user
    usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user.id)
    #caso não tenha nem uma empresa o usuario pode estar vinculado a
    #algum projeto ou sub venda pode ser (chefe ou cobrador)
    if (usuario_empresa):
      if usuario_empresa.bloqueado:
      #redireciona para pagina de usuario)
        redirect(URL('acs_empresa','mensagem'))
      if (usuario_empresa.tipo=="Cobrador")|(usuario_empresa.tipo=="Chefe"):
        redirect(URL('default','acesso_inicial_usuario'))
    if not empresa:
      empresa = db.empresa(usuario_empresa.empresa)
      if not empresa:
        #redireciona para pagina de usuario)
        redirect(URL('default','index'))
    consul=(request.args(0))
    if consul:
      n=int(consul)/12
      empresa = db.empresa(n)
    #caso contrario procegue, busca todos os projetos da empresa
    rows = db(db.projeto.empresa==empresa.id).select(orderby=db.projeto.descricao)
    rowsdesp = db(db.classe_despesa_local.empresa==empresa.id).select(orderby=db.classe_despesa_local.descricao)
    rowsuser = db(db.usuario_empresa.empresa==empresa.id).select()
    rowspgmt = db((db.pagamento.empresa==empresa.id)&(db.pagamento.quitado==False)).count()
    if request.args(0, auth.user)=="235":
      rows = db(db.projeto.empresa).select(orderby=db.empresa)
    #2 consultas no banco
    return locals()

@auth.requires_login()
def lista_logins():
    data=request.now
    empresa = db.empresa(request.args(0, auth.user))
    consul=(request.args(0))
    if consul:
        n=int(consul)
        empresa = db.empresa(n)
    usuario=auth.user
    if not empresa:
        usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user.id)
        empresa = db.empresa(usuario_empresa.empresa)
    row = db(db.usuario_empresa.empresa==empresa.id).select(orderby=db.usuario_empresa.id)
    if request.args(0, auth.user)=="235":
        rows = db(db.usuario_empresa.empresa).select(orderby=db.empresa)
    #2 consultas no banco
    return locals()

@auth.requires_login()
def lista_pagmt_sistema():
    data=request.now
    empresa = db.empresa(db.empresa.auth_user==auth.user.id)
    consul=(request.args(0))
    if consul:
        n=int(consul)/12
        empresa = db.empresa(n)
    usuario=auth.user
    limites = (0, 6)
    if auth.user.id==1:
      limites = (0, 6)
    rows = db(db.pagamento.empresa==empresa.id).select(limitby=limites,orderby=~db.pagamento.id)
    if request.args(0, auth.user)=="235":
        rows = db(db.pagamento.empresa).select(orderby=db.empresa)
    #2 consultas no banco
    return locals()
@auth.requires_login()
def lista_projetos():
    data=request.now
    empresa = db.empresa(db.empresa.auth_user==auth.user.id)
    consul=(request.args(0))
    if consul:
        n=int(consul)/12
        empresa = db.empresa(n)
    usuario=auth.user
    usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user.id)
    if usuario_empresa.bloqueado:
      #redireciona para pagina de usuario)
        redirect(URL('acs_empresa','mensagem'))
    if not empresa:
        usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user.id)
        empresa = db.empresa(usuario_empresa.empresa)
    if (usuario.id!=1)and(usuario_empresa.empresa!=empresa.id):
        redirect(URL('default','index'))
    rows = db(db.projeto.empresa==empresa.id).select(orderby=db.projeto.venda_finalizada|~db.projeto.id)
    return locals()
@auth.requires_login()
def inserir_projeto():
    response.view = 'generic.html' # use a generic view
    #recebe id da empresa como parametro e busca empresa
    empresa = db.empresa(request.args(0, auth.user))
    #bloqueia visualização empresa e coloca o id da empresa como padrão
    db.projeto.empresa.default = empresa.id
    db.projeto.empresa.writable = False
    db.projeto.comissao_cobranca.writable = False
    #deixa o usuario que esta logado como usuario padrão
    #deixa o id bloqueado para visualização
    db.projeto.adiantamento.writable = False
    db.projeto.descricao_adiantamento.readable = False
    db.projeto.descricao_adiantamento.writable = False
    db.projeto.vale_saida.writable = False
    db.projeto.descricao_vale.readable = False
    db.projeto.descricao_vale.writable = False
    db.projeto.auth_user.default = 28
    db.projeto.auth_user.writable = False
    #deixa o nome padrão e bloqueia para visualização
    db.projeto.nome_chefe.default = auth.user.first_name
    db.projeto.nome_chefe.writable = False
    #cria um sqlforma para ser processado
    form = SQLFORM(db.projeto).process()
    if form.accepted:
        #caso aceito redireciona para tela de acesso inicial
        response.flash = 'Formulario aceito'
        projeto=db.projeto(form.vars.id)
        redirect(URL('lista_projetos', args=empresa.id*12))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    #2 consultas no banco
    return  dict(form=form)

@auth.requires_login()
def cadastrar_login():
    response.view = 'generic.html' # use a generic view
    empresa = db.empresa(request.args(0, cast=int))
    form = SQLFORM(db.auth_user).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('vincular_login', args=[empresa.id,form.vars.id]))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    #2 consultas no banco
    return  dict(form=form)
@auth.requires_login()
def vincular_login():
    response.view = 'generic.html' # use a generic view
    empresa = db.empresa(request.args(0, cast=int))
    usuario = db.auth_user(request.args(1, cast=int))
    db.usuario_empresa.empresa.default = request.args(0, cast=int)
    db.usuario_empresa.auth_user.default = request.args(1, cast=int)
    db.usuario_empresa.tipo.default = "Chefe"
    db.usuario_empresa.nome.default = usuario.first_name
    db.usuario_empresa.telefone.default = "**********"
    db.usuario_empresa.id.readable = False
    db.usuario_empresa.id.readable = False
    form = SQLFORM(db.usuario_empresa).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acs_principal','lista_logins', args=empresa.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    #2 consultas no banco
    return  dict(form=form)
@auth.requires_login()
def cadastrar_empresa():
    response.view = 'generic.html' # use a generic view
    db.empresa.auth_user.default = 1
    form = SQLFORM(db.empresa).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acs_principal','lista_empresas', args=1))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    #2 consultas no banco
    return  dict(form=form)
@auth.requires_login()
def alterar_projeto():
    response.view = 'generic.html' # use a generic view
    #recebe id do projeto e busca projeto no banco
    usuario = auth.user
    projeto = db.projeto(request.args(0, cast=int))
    #caso o projeto não esteja ativo redireciona
    #pois não pode ser alterado
    if projeto.venda_finalizada:
        session.flash = 'A venda já foi finalizada'
        redirect(URL('lista_projetos', args=projeto.empresa*12))
    db.projeto.empresa.readable = False
    db.projeto.empresa.writable = False
    db.projeto.id.readable = False
    db.projeto.id.writable = False

    if projeto.id>125:
      db.projeto.adiantamento.writable = False
      db.projeto.descricao_adiantamento.readable = False
      db.projeto.descricao_adiantamento.writable = False
      db.projeto.vale_saida.writable = False
      db.projeto.descricao_vale.readable = False
      db.projeto.descricao_vale.writable = False
    
    if projeto.id==129:
      db.projeto.descricao_adiantamento.readable = True
      db.projeto.descricao_adiantamento.writable = True
    a=True
    if projeto.total_venda_prazo>0:
        a=False
    if usuario.id==1:
#       db.projeto.descricao_adiantamento.label = "Programador (Descrição Adiantamento)"
      db.projeto.descricao_adiantamento.readable = True
      db.projeto.descricao_adiantamento.writable = True
      db.projeto.data_final.label = "#Programador (Data_final)"
      db.projeto.data_final.readable = True
      db.projeto.data_final.writable = True
      db.projeto.id.readable = True
      db.projeto.id.writable = True
      db.projeto.empresa.label = "#Programador (Empresa)"
      db.projeto.empresa.readable = True
      db.projeto.empresa.writable = True
      a=True
    db.projeto.descricao_adiantamento.label = "Observação Geral"
    db.projeto.descricao_adiantamento.readable = True
    db.projeto.descricao_adiantamento.writable = True
    form = SQLFORM(db.projeto, request.args(0, cast=int), deletable=a)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        if projeto.total_venda_prazo>0:
          redirect(URL('acs_projeto','index', args=projeto.id))
        else:
          redirect(URL('acs_principal','lista_projetos', args=projeto.empresa*12))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return  dict(form=form)

@auth.requires_login()
def alterar_empresa():
    response.view = 'generic.html' # use a generic view
    #recebe id do projeto e busca projeto no banco
    usuario = auth.user
    empresa = db.empresa(request.args(0, cast=int))
    form = SQLFORM(db.empresa, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('lista_empresas', args=empresa.id*12))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return  dict(form=form)
@auth.requires_login()
def inserir_class_desp():
    response.view = 'generic.html' # use a generic view

    empresa = db.empresa(request.args(0, auth.user))

    db.classe_despesa_local.empresa.default = empresa.id
    db.classe_despesa_local.empresa.writable = False

    form = SQLFORM(db.classe_despesa_local).process()
    if form.accepted:
        #caso aceito redireciona para tela de acesso inicial
        response.flash = 'Formulario aceito'
        redirect(URL('index', args=empresa.id*12))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    #2 consultas no banco
    return  dict(form=form)


@auth.requires_login()
def inserir_pagamento():
    response.view = 'generic.html' # use a generic view
    empresa = db.empresa(request.args(0, auth.user))
    db.pagamento.empresa.default = empresa.id
    db.pagamento.empresa.writable = False
    
    #cria um sqlforma para ser processado
    form = SQLFORM(db.pagamento).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('index', args=empresa.id*12))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    #2 consultas no banco
    return  dict(form=form)

def alterar_usuario_empresa():
    response.view = 'generic.html' # use a generic view
    #recebe id do projeto e busca projeto no banco
    usuario = auth.user
    usuario_empresa = db.usuario_empresa(request.args(0, cast=int))
    db.usuario_empresa.id.readable = False
    db.usuario_empresa.auth_user.writable = False
    db.usuario_empresa.empresa.readable = True
    db.usuario_empresa.empresa.writable = False
    if usuario_empresa.nome=="Bloqueio 2714":
      db.usuario_empresa.nome.writable = False
      db.usuario_empresa.bloqueado.writable = False
    if usuario.id==1:
      db.usuario_empresa.empresa.label = "#(Programador) Empresa"
      db.usuario_empresa.nome.label = "#(Programador) Nome"
      db.usuario_empresa.auth_user.label = "#(Programador) Usuario"
      db.usuario_empresa.bloqueado.label = "#(Programador) Bloqueado"
      db.usuario_empresa.empresa.writable = True
      db.usuario_empresa.nome.writable = True
      db.usuario_empresa.auth_user.writable = True
      db.usuario_empresa.bloqueado.writable = True
    form = SQLFORM(db.usuario_empresa, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
      session.flash = 'Projeto atualizado'
      redirect(URL('alterar_usuario', args=usuario_empresa.auth_user))
    elif form.errors:
      response.flash = 'Erros no formulário!'
    return  dict(form=form)
def alterar_usuario():
    response.view = 'generic.html' # use a generic view
    #recebe id do projeto e busca projeto no banco
    usuario = db.auth_user(request.args(0, cast=int))
    usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==usuario.id)
    db.auth_user.id.readable = False
    form = SQLFORM(db.auth_user, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
      session.flash = 'Projeto atualizado'
      redirect(URL('lista_logins', args=usuario_empresa.empresa))
    elif form.errors:
      response.flash = 'Erros no formulário!'
    return  dict(form=form)
@auth.requires_login()
def alterar_pagamento():
    response.view = 'generic.html' # use a generic view
    pagamento = db.pagamento(request.args(0, cast=int))
    empresa = db.empresa(pagamento.empresa)

    form = SQLFORM(db.pagamento, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('index', args=empresa.id*12))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return  dict(form=form)

def lista_empresas():
    rows = db(db.empresa).select(orderby=db.empresa.nome)
    return locals()


@auth.requires_membership('admin')
def bloqueio_verificacao():
    projeto = db.projeto(request.args(0, cast=int))
    return locals()
  
  
def pagina_pagamento():
    pagamento = db.pagamento(request.args(0, cast=int))
    empresa = db.empresa(pagamento.empresa)
    return locals()

  
def lista_cobrancas():
    todas_cobrancas = db(db.sub_venda.empresa==None).select()
    for cobranca in todas_cobrancas:
      projeto = db.projeto(db.sub_venda.projeto==cobranca.projeto)
      cobranca.empresa=projeto.empresa
      cobranca.update_record()
    try:
      usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user.id)
      consul=(request.args(0))
      if consul:
        empresa = db.empresa(request.args(0, auth.user))
      paginacao = 15
      if len(request.args) == 0:
          empresa = db.empresa(db.empresa.id==usuario_empresa.empresa)
          pagina = 1
      elif len(request.args) == 1:
          pagina = 1
      else:
          try:
              pagina = int(request.args[1])
          except ValueError:
              redirect(URL('erro', vars={
                    'msg':'Numero da página inválido'
                    }))
      if pagina <= 0:
          pagina = 1
      total = db((db.sub_venda.empresa==empresa)&(db.sub_venda.cobranca_iniciada==True)).count()
      paginas = total/paginacao
      if total%paginacao:
          paginas+=1
      if total==0:
          paginas=1 
      if pagina > paginas:
          redirect(URL(args=[empresa.id,paginas]))
      limites = (paginacao*(pagina-1), (paginacao*pagina))
      registros = db((db.sub_venda.empresa==empresa)&(db.sub_venda.cobranca_iniciada==True)).select(
        limitby=limites,orderby=~db.sub_venda.data_inicio_cobranca|~db.sub_venda.projeto)
      consul=(request.args(2))
      if (consul):
          registros = db((db.sub_venda.empresa==empresa)&(db.sub_venda.primeira_cidade.contains(consul))).select(limitby=(0,paginacao))
    except:
      redirect(URL('index', args=empresa.id*12))
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, consul=consul, empresa=empresa)
  
  
def alterar_cobranca():
    response.view = 'generic.html' # use a generic view
    sub_venda = db.sub_venda(request.args(0, cast=int))
    projeto = db.projeto(sub_venda.projeto)
    db.sub_venda.cobranca_finalizada.writable = True
    db.sub_venda.data_final_cobranca.writable = False
    db.sub_venda.data_final_cobranca.readable = False
    form = SQLFORM(db.sub_venda, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
      session.flash = 'Projeto atualizado'
      redirect(URL('lista_cobrancas', args=projeto.empresa))
    elif form.errors:
      response.flash = 'Erros no formulário!'
    return  dict(form=form)

  
def alteracao_projeto():
    response.view = 'generic.html' # use a generic view
    #recebe id do projeto e busca projeto no banco
    usuario = auth.user
    projeto = db.projeto(request.args(0, cast=int))
    #caso o projeto não esteja ativo redireciona
    #pois não pode ser alterado
    if projeto.venda_finalizada:
        session.flash = 'A venda já foi finalizada'
        redirect(URL('lista_projetos', args=projeto.empresa*12))

    db.projeto.adiantamento.writable = False
    db.projeto.adiantamento.readable = False
    db.projeto.adiantamento.writable = False
    db.projeto.adiantamento.readable = False
    db.projeto.descricao_adiantamento.readable = False
    db.projeto.descricao_adiantamento.writable = False
    db.projeto.vale_saida.writable = False
    db.projeto.descricao_vale.readable = False
    db.projeto.descricao_vale.writable = False
    db.projeto.total_venda_prazo.readable = True
    a=True
    if projeto.total_venda_prazo>0:
        a=False
    if usuario.id==1:
      db.projeto.data_final.label = "#Data_final Bloqueia projeto (Programador)"
      db.projeto.data_final.readable = True
      db.projeto.data_final.writable = True
      db.projeto.id.label = "#ID (Programador)"
      db.projeto.id.readable = True
      db.projeto.id.writable = True
      db.projeto.empresa.label = "#Empresa (Programador)"
      db.projeto.empresa.readable = True
      db.projeto.empresa.writable = True
    db.projeto.venda_finalizada.readable = True
    db.projeto.venda_finalizada.writable = True
    form = SQLFORM(db.projeto, request.args(0, cast=int), deletable=a)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        if projeto.total_venda_prazo>0:
          redirect(URL('acs_projeto','index', args=projeto.id))
        else:
          redirect(URL('acs_principal','lista_projetos', args=projeto.empresa*12))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return  dict(form=form)

  
def recibo_pagamento():
    pagamento = db.pagamento(request.args(0, cast=int))
    empresa = db.empresa(pagamento.empresa)
    return locals()
