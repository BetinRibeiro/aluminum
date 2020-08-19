# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    despesa = db.classe_despesa_local(request.args(0, auth.user))
    empresa = db.empresa(despesa.empresa)
    rows = db(db.despesa_local.classe_despesa_local==despesa.id).select(orderby=db.despesa_local.data_inicio)
    return locals()

@auth.requires_login()
def alterar_nome_classe():
    response.view = 'generic.html' # use a generic view
    classe_despesa_local = db.classe_despesa_local(request.args(0, cast=int))
    empresa = db.empresa(classe_despesa_local.empresa)
    db.classe_despesa_local.id.readable = False
    db.classe_despesa_local.id.writable = False
    #bloqueia empresa para alteração
    db.classe_despesa_local.empresa.readable = True
    db.classe_despesa_local.empresa.writable = False

    form = SQLFORM(db.classe_despesa_local, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('acs_principal', 'index', args=empresa.id*12))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return  dict(form=form)


@auth.requires_login()
def inserir_despesa():
    response.view = 'generic.html' # use a generic view

    classe_despesa_local = db.classe_despesa_local(request.args(0, auth.user))

    db.despesa_local.classe_despesa_local.default = classe_despesa_local.id
    db.despesa_local.classe_despesa_local.writable = False

    form = SQLFORM(db.despesa_local).process()
    if form.accepted:
        #caso aceito redireciona para tela de acesso inicial
        response.flash = 'Formulario aceito'
        redirect(URL('index', args=classe_despesa_local.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    #2 consultas no banco
    return  dict(form=form)


@auth.requires_login()
def alterar_despesa_local():
    response.view = 'generic.html' # use a generic view
    despesa_local = db.despesa_local(request.args(0, cast=int))
    classe = db.classe_despesa_local(despesa_local.classe_despesa_local)
    db.despesa_local.id.readable = False
    db.despesa_local.id.writable = False
    db.despesa_local.classe_despesa_local.readable = False
    db.despesa_local.classe_despesa_local.writable = False

    form = SQLFORM(db.despesa_local, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('index', args=classe.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return  dict(form=form)
