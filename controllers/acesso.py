# -*- coding: utf-8 -*-
@auth.requires_login()
def projetos():
    #empresa = db.empresa(db.empresa.auth_user==auth.user.id)
    empresa = db.empresa(db.empresa)
    rows = db(db.projeto.empresa==11).select(orderby=db.empresa)
    rowsd = db((db.classe_despesa_local.empresa == empresa.id)).select(orderby=~db.classe_despesa_local.descricao)
    return locals()

@auth.requires_login()
def acesso_projeto():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.item_carrada.projeto == request.args(0, cast=int)).select(orderby=~db.item_carrada.carrada)
    return locals()

@auth.requires_login()
def despesa_venda():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.classe_despesa.projeto == request.args(0, cast=int)).select(orderby=~db.classe_despesa.total_classe)
    return locals()

@auth.requires_login()
def mercadoria():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.item_carrada.projeto == request.args(0, cast=int)).select(orderby=db.item_carrada.carrada|~db.item_carrada.q_pcs)
    return locals()


@auth.requires_login()
def relatorio_chefe():
    projeto = db.projeto(request.args(0, cast=int))
    return locals()
@auth.requires_login()
def vendas():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.vendedor.projeto == projeto.id).select(orderby=~db.vendedor.total_vendas)
    rows_fun = db(db.funcionario.projeto == projeto.id).select()
    return locals()

@auth.requires_login()
def ver_particao():
    sub_venda = db.sub_venda(request.args(0, cast=int))
    rows = db(db.venda.sub_venda == sub_venda.id).select(orderby=db.venda.data_venda)
    return locals()


@auth.requires_login()
def ver_data_venda():
    venda = db.venda(request.args(0, cast=int))
    sub_venda = db.sub_venda(venda.sub_venda)
    data_venda=venda.data_venda
    rows = db((db.venda.sub_venda == sub_venda.id) & (db.venda.data_venda==venda.data_venda)).select(orderby=db.venda.vendedor)
    return locals()

@auth.requires_login()
def vendas_dia_dia():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.sub_venda.projeto == projeto.id).select()
    total_venda=0.0
    total_fichas=0
    for row in rows:
        total_venda=0.0
        total_fichas=0
        #sum = db.venda.venda_praso.sum()
        #row.venda_praso=(db(db.venda.sub_venda == row.id).select(sum).first()[sum])
        #row.update_record()
        rowsv = db(db.venda.sub_venda == row.id).select()
        for rowv in rowsv:
            total_venda+=rowv.venda_praso-rowv.valor_devolvido
            total_fichas+=rowv.quant_fichas-rowv.quant_fichas_devolvidas
        row.quant_fichas=total_fichas
        row.venda_praso=total_venda
    return locals()

def api():
    response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers['Access-Control-Max-Age'] = 86400
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    

    response.view = 'generic.json' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables:raise HTTP(403)
    grid = db[tablename](request.args(1, cast=int))
    if not grid:
        grid =db(db.projeto.empresa==11).select(db[tablename].ALL,orderby=~db[tablename].quant_vendedores).as_list()
    return dict(grid=grid)
