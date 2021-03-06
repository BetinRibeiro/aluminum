# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    usuario = auth.user
    projeto = db.projeto(request.args(0, cast=int))
    tipo = (request.args(1))
    empresa = db.empresa(projeto.empresa)
    #caso o usuario da empresa for diferênte do usuario logado
    #redireciona pois será um usuario do projeto (chefe) ou 
    #usuario da sub_venda(Cobrador)
    usuario=auth.user
    if (usuario.id==737326) and (tipo=="venda_vista"):
        redirect(URL('acesso_registro_venda_diaposdia', args=[projeto.id,tipo]))
    rows = db((db.registro_venda.projeto == projeto.id) & (db.registro_venda.tipo == tipo)).select(orderby=db.registro_venda.data_inicio)
    return locals()

@auth.requires_login()
def inserir_registro():
    response.view = 'generic.html' # use a generic view
    projeto = db.projeto(request.args(0, auth.user))
    tipo = (request.args(1))

    db.registro_venda.projeto.default = projeto.id
    db.registro_venda.projeto.writable = False

    db.registro_venda.tipo.default = tipo

    if tipo!="Gratificacao":
        usuario = auth.user
        if usuario.id==24324:
            session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
            redirect(URL('index', args=[projeto.id,tipo]))
    
    form = SQLFORM(db.registro_venda).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('index', args=[projeto.id,tipo]))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)

@auth.requires_login()
def alterar_registro():
    response.view = 'generic.html' # use a generic view
    registro_venda = db.registro_venda(request.args(0, cast=int))
    tipo = (request.args(1))
    projeto = db.projeto(registro_venda.projeto)
    if tipo!="Gratificacao":
        usuario = auth.user
        if usuario.id==2434:
            session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
            redirect(URL('index', args=[projeto.id,tipo]))
    
    db.registro_venda.id.readable = False
    db.registro_venda.id.writable = False

    db.registro_venda.projeto.readable = False
    db.registro_venda.projeto.writable = False

    form = SQLFORM(db.registro_venda, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('index', args=[projeto.id,tipo]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
