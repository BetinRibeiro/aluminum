# -*- coding: utf-8 -*-
# tente algo como
@auth.requires_login()
def acesso_equipe():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.vendedor.projeto == projeto.id).select(orderby=~db.vendedor.total_vendas)
    return locals()

@auth.requires_login()
def criar_vendedor():
    response.view = 'generic.html' # use a generic view
    projeto = db.projeto(request.args(0, auth.user))

    db.vendedor.projeto.default = projeto.id
    db.vendedor.projeto.writable = False

    form = SQLFORM(db.vendedor).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acesso_equipe', args=projeto.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)

@auth.requires_login()
def alterar_vendedor():
    response.view = 'generic.html' # use a generic view
    vendedor = db.vendedor(request.args(0, cast=int))
    projeto = db.projeto(vendedor.projeto)
    db.vendedor.id.readable = False
    db.vendedor.id.writable = False

    db.vendedor.projeto.readable = False
    db.vendedor.projeto.writable = False
    deletar=True
    if vendedor.total_vendas>0:
        deletar=False
        

    form = SQLFORM(db.vendedor, request.args(0, cast=int), deletable=deletar)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acesso_equipe', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

@auth.requires_login()
def acesso_venda():
    vendedor = db.vendedor(request.args(0, cast=int))
    projeto = db.projeto(vendedor.projeto)
    rows_sub = db(db.sub_venda.projeto == vendedor.projeto).select(orderby=~db.sub_venda.data_inicio_cobranca)
    rows_vend = db(db.venda.vendedor == request.args(0, cast=int)).select(orderby=db.venda.data_venda)
    return locals()
@auth.requires_login()
def inserir_venda():
    response.view = 'generic.html' # use a generic view
    vendedor = db.vendedor(request.args(0, auth.user))
    sub_venda = db.sub_venda(request.args(1, auth.user))
    
    db.venda.sub_venda.default = sub_venda.id
    db.venda.sub_venda.writable = False
    db.venda.sub_venda.readable = False
    
    db.venda.vendedor.default = vendedor.id
    db.venda.vendedor.writable = False

    form = SQLFORM(db.venda).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acesso_venda', args=vendedor.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
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

    form = SQLFORM(db.venda, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acesso_venda', args=vendedor.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)