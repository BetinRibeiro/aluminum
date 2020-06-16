# -*- coding: utf-8 -*-
@auth.requires_login()
def projetos():
    #empresa = db.empresa(db.empresa.auth_user==auth.user.id)
    empresa = db.empresa(db.empresa.id==8)
    rows = db(db.projeto.empresa==empresa.id).select(orderby=db.empresa)
    rowsd = db((db.classe_despesa_local.empresa == empresa.id)).select(orderby=~db.classe_despesa_local.descricao)
    return locals()

@auth.requires_login()
def acesso_projeto():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.item_carrada.projeto == request.args(0, cast=int)).select(orderby=~db.item_carrada.carrada)
    return locals()


@auth.requires_login()
def mercadoria():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.item_carrada.projeto == request.args(0, cast=int)).select(orderby=db.item_carrada.carrada|~db.item_carrada.q_pcs)
    return locals()
