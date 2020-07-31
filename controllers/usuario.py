# -*- coding: utf-8 -*-
@auth.requires_login()
def acesso_projeto():
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    if len(db(db.carrada.projeto == projeto.id).select())>0:
        data= db(db.carrada.projeto == projeto.id).select(orderby=db.carrada.data_envio).first().data_envio
    else:
        data= None
    usuario=auth.user
    return locals()

@auth.requires_login()
def acesso_completo():
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    return locals()
def betinho_acesso():
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    return locals()
@auth.requires_login()
def abencoado():
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    data=db(db.carrada.projeto == projeto.id).select(orderby=db.carrada.data_envio).first().data_envio
    return locals()
@auth.requires_login()
def fsprojetos():
    
    empresa = db.empresa(request.args(0, cast=int))
    if empresa.id==8:
        response.flash = T("Alerta de pegamento! pendente à 13 dias")
    if auth.user.id==10:
        empresa = db.empresa(8)
    rows = db(db.projeto.empresa==empresa.id).select(orderby=~db.projeto.descricao)
    rowsd = db((db.classe_despesa_local.empresa == empresa.id)).select(orderby=~db.classe_despesa_local.descricao)
    rowsuser = db(db.usuario_empresa.empresa==empresa.id).select(orderby=db.usuario_empresa.nome)
    return locals()
@auth.requires_login()
def fs():
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    return locals()
@auth.requires_login()
@cache.action()
def fscontador():
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    return locals()
@auth.requires_login()
def chefefs():
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    return locals()
