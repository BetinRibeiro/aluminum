# -*- coding: utf-8 -*-
@auth.requires_login()
def acesso_registro_venda():
    projeto = db.projeto(request.args(0, cast=int))
    tipo = (request.args(1))
    empresa = db.empresa(projeto.empresa)
    #caso o usuario da empresa for diferênte do usuario logado
    #redireciona pois será um usuario do projeto (chefe) ou 
    #usuario da sub_venda(Cobrador)
    usuario=auth.user
    if (usuario.id==6) and (tipo=="venda_vista"):
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

    form = SQLFORM(db.registro_venda).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acesso_registro_venda', args=[projeto.id,tipo]))
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
    
    db.registro_venda.id.readable = False
    db.registro_venda.id.writable = False

    db.registro_venda.projeto.readable = False
    db.registro_venda.projeto.writable = False

    form = SQLFORM(db.registro_venda, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acesso_registro_venda', args=[projeto.id,tipo]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

@auth.requires_login()
def acesso_registro_venda_diaposdia():
    projeto = db.projeto(request.args(0, cast=int))
    tipo = (request.args(1))
    subvenda = db(db.sub_venda.projeto==projeto.id).select()
    classe_despesa =  db(db.classe_despesa.projeto==projeto.id).select()
    listdesp = db(db.despesa.id == 789456).select()
    rowsv = db(db.venda.id == 789456).select()
    for f in classe_despesa:
        listdesp += db(db.despesa.classe_despesa == f.id).select()
    for l in subvenda:
        rowsv += db(db.venda.sub_venda == l.id).select()
    #rowsv = db(db.venda.sub_venda == subvenda.id or db.venda.sub_venda == subvenda[0].id).select()
    rows = db((db.registro_venda.tipo == "venda_vista") & (db.registro_venda.projeto==projeto.id)).select(orderby=db.registro_venda.data_inicio)
    return locals()
