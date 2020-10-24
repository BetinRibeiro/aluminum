# -*- coding: utf-8 -*-
@auth.requires_membership('admin')
def index():
    data=request.now
    empresa = db.empresa(db.empresa.auth_user==auth.user.id)
    usuario=auth.user
    usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user.id)
    #caso não tenha nem uma empresa o usuario pode estar vinculado a
    #algum projeto ou sub venda pode ser (chefe ou cobrador)
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
    rowspgmt = db(db.pagamento.empresa==empresa.id).select()
    if request.args(0, auth.user)=="235":
        rows = db(db.projeto.empresa).select(orderby=db.empresa)
    #2 consultas no banco
    return locals()

@auth.requires_login()
def lista_logins():
    data=request.now
    empresa = db.empresa(db.empresa.auth_user==auth.user.id)
    consul=(request.args(0))
    if consul:
        n=int(consul)/12
        empresa = db.empresa(n)
    usuario=auth.user
    row = db(db.usuario_empresa.empresa==empresa.id).select()
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
    rows = db(db.pagamento.empresa==empresa.id).select()
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
    if (usuario.id!=1)and(usuario_empresa.empresa!=empresa.id):
        redirect(URL('default','index'))
    rows = db(db.projeto.empresa==empresa.id).select(orderby=db.projeto.descricao)
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
    #bloqueia id para visualização e alteração
    db.projeto.id.readable = False
    db.projeto.id.writable = False
    #bloqueia empresa para alteração
    db.projeto.empresa.readable = True
    db.projeto.empresa.writable = False
    a=True
    if projeto.total_venda_prazo>0:
        a=False
    if auth.user.id==1:
        db.projeto.empresa.readable = True
        db.projeto.empresa.writable = True
        a=True
    form = SQLFORM(db.projeto, request.args(0, cast=int), deletable=a)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('index', args=projeto.empresa*12))
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
