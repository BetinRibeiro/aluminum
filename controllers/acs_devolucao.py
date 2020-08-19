# -*- coding: utf-8 -*-
def index():
    sub_venda = db.sub_venda(request.args(0, cast=int))
    rows = db((db.devolucao.sub_venda == sub_venda.id)).select()
    return locals()

def criar_devolucao():
    response.view = 'generic.html' # use a generic view
    sub_venda = db.sub_venda(request.args(0, auth.user))

    db.devolucao.sub_venda.default = sub_venda.id
    db.devolucao.sub_venda.writable = False
    
    db.devolucao.data_recolhimento.writable = False
    
    db.devolucao.custo_aproveitamento.writable = False

    form = SQLFORM(db.devolucao).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('index', args=[sub_venda.id]))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return  dict(form=form)

def alterar_dados_devolucao():
    response.view = 'generic.html' # use a generic view
    devolucao = db.devolucao(request.args(0, cast=int))
    sub_venda = db.sub_venda(devolucao.sub_venda)
    
    db.devolucao.id.readable = False
    db.devolucao.id.writable = False
    db.devolucao.data_recolhimento.writable = False
    db.devolucao.data_recolhimento.readable = False
    db.devolucao.sub_venda.readable = False
    db.devolucao.sub_venda.writable = False
    
    form = SQLFORM(db.devolucao, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('index', args=[sub_venda.id]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)
    
def acessar_devolucao():
    devolucao = db.devolucao(request.args(0, cast=int))
    rows = db((db.item_devolucao.devolucao == devolucao.id)).select()
    return locals()


def adicionar_item_devolucao():
    response.view = 'generic.html' # use a generic view
    devolucao = db.devolucao(request.args(0, auth.user))
    sub_venda = db.sub_venda(devolucao.sub_venda)

    db.item_devolucao.devolucao.default = devolucao.id
    db.item_devolucao.devolucao.writable = False
    db.item_devolucao.quant_recolhida.writable = False
    db.item_devolucao.quant_novas.writable = False

    form = SQLFORM(db.item_devolucao).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acessar_devolucao', args=devolucao.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    return dict(form=form)

def confirmar_recolhimento():
    devolucao = db.devolucao(request.args(0, cast=int))
    sub_venda = db.sub_venda(devolucao.sub_venda)
    if devolucao.recolhido:
        devolucao.recolhido=False
    else:
        devolucao.recolhido=True
    devolucao.update_record()
    redirect(URL('acessar_devolucao', args=[devolucao.id]))
    
    return locals



def alterar_item_devolucao_rec():
    response.view = 'generic.html' # use a generic view
    item_devolucao = db.item_devolucao(request.args(0, cast=int))
    devolucao = db.devolucao(item_devolucao.devolucao)
    
    db.item_devolucao.id.readable = False
    db.item_devolucao.id.writable = False
    
    
    db.item_devolucao.quant_ditada.writable = False
    db.item_devolucao.custo.writable = False
    db.item_devolucao.preco.writable = False
    db.item_devolucao.custo.readable = True
    db.item_devolucao.preco.readable = True
    db.item_devolucao.descricao.writable = False
    db.item_devolucao.descricao.readable = True
    
    db.item_devolucao.devolucao.readable = False
    db.item_devolucao.devolucao.writable = False
    
    form = SQLFORM(db.item_devolucao, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acessar_devolucao', args=[devolucao.id]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)


def alterar_item_devolucao():
    response.view = 'generic.html' # use a generic view
    item_devolucao = db.item_devolucao(request.args(0, cast=int))
    devolucao = db.devolucao(item_devolucao.devolucao)
    
    db.item_devolucao.id.readable = False
    db.item_devolucao.id.writable = False
    
    db.item_devolucao.devolucao.readable = False
    db.item_devolucao.devolucao.writable = False
    
    form = SQLFORM(db.item_devolucao, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acessar_devolucao', args=[devolucao.id]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)
