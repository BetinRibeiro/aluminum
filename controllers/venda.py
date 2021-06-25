# -*- coding: utf-8 -*-
@auth.requires_login()
def acesso_particao():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.sub_venda.projeto == projeto.id).select(orderby=db.sub_venda.data_inicio_cobranca)
    total_venda=0.0
    total_fichas=0
    for row in rows:
        total_venda=0.0
        total_fichas=0
        rowsv = db(db.venda.sub_venda == row.id).select()
        for rowv in rowsv:
            total_venda+=rowv.venda_praso-rowv.valor_devolvido
            total_fichas+=rowv.quant_fichas-rowv.quant_fichas_devolvidas
        row.quant_fichas=total_fichas
        row.venda_praso=total_venda
        row.update_record()
    return locals()

@auth.requires_login()
def ver_particao():
    sub_venda = db.sub_venda(request.args(0, cast=int))
    projeto = db.projeto(sub_venda.projeto)
    rows = db(db.venda.sub_venda == sub_venda.id).select(orderby=db.venda.data_venda)
    return locals()
  
##funções descontinuadas dia 21 jun 2021
#verificar os proximos 90 dias
#deleta-las
@auth.requires_login()
def criar_particao():
    redirect(URL('default','index'))
    response.view = 'generic.html' # use a generic view
    projeto = db.projeto(request.args(0, auth.user))

    db.sub_venda.projeto.default = projeto.id
    db.sub_venda.projeto.writable = False

    form = SQLFORM(db.sub_venda).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acesso_particao', args=projeto.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)
@auth.requires_login()
def alterar_particao():
    redirect(URL('default','index'))
    response.view = 'generic.html' # use a generic view
    sub_venda = db.sub_venda(request.args(0, cast=int))
    projeto = db.projeto(sub_venda.projeto)
    db.sub_venda.id.readable = False
    db.sub_venda.id.writable = False

    db.sub_venda.projeto.readable = False
    db.sub_venda.projeto.writable = False
    db.sub_venda.cobranca_iniciada.label = 'Venda Finalizada'
    db.sub_venda.cobranca_iniciada.readable = True
    db.sub_venda.cobranca_iniciada.writable = True
    deletar =True
    if sub_venda.total_venda_praso>0:
        deletar =False
    form = SQLFORM(db.sub_venda, request.args(0, cast=int), deletable=deletar)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acesso_particao', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
