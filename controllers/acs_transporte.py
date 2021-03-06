# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    empresa = db.empresa(request.args(0, auth.user))
    rows = db(db.transporte.empresa==empresa.id).select()
    return locals()

@auth.requires_login()
def acesso_transporte(): 
    transporte = db.transporte(request.args(0, auth.user))
    rows = db(db.km.transporte==transporte.id).select()
    return locals()

@auth.requires_login()
def cadastrar_transporte(): 
    response.view = 'generic.html'
    empresa = db.empresa(request.args(0, auth.user))
    db.transporte.empresa.default = empresa.id
    db.transporte.empresa.writable = False
    form = SQLFORM(db.transporte).process()
    if form.accepted:
        #caso aceito redireciona para tela de acesso inicial
        response.flash = 'Formulario aceito'
        redirect(URL('index', args=empresa.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    #2 consultas no banco
    return  dict(form=form)

@auth.requires_login()
def alterar_transporte(): 
    response.view = 'generic.html' # use a generic view
    transporte = db.transporte(request.args(0, cast=int))
    empresa = db.empresa(transporte.empresa)
    db.transporte.id.readable = False
    db.transporte.id.writable = False
    db.transporte.empresa.readable = False
    db.transporte.empresa.writable = False
    form = SQLFORM(db.transporte, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('index', args=empresa.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

@auth.requires_login()
def inserir_km(): 
    response.view = 'generic.html'
    transporte = db.transporte(request.args(0, auth.user))
    db.km.transporte.default = transporte.id
    db.km.transporte.writable = False
    form = SQLFORM(db.km).process()
    if form.accepted:
        #caso aceito redireciona para tela de acesso inicial
        response.flash = 'Formulario aceito'
        redirect(URL('acesso_transporte', args=transporte.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    #2 consultas no banco
    return  dict(form=form)

@auth.requires_login()
def alterar_km(): 
    response.view = 'generic.html' # use a generic view
    km = db.km(request.args(0, cast=int))
    transporte = db.transporte(km.transporte)
    db.km.id.readable = False
    db.km.id.writable = False
    db.km.transporte.readable = False
    db.km.transporte.writable = False
    form = SQLFORM(db.km, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acesso_transporte', args=transporte.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
