# -*- coding: utf-8 -*-
from datetime import date
@auth.requires_login()
def acesso_projeto():
    projeto = db.projeto(request.args(0, cast=int))
    total_particao = db(db.sub_venda.projeto==projeto.id).count()
    hj = date.today()
    if total_particao==0:
      futuro = date.fromordinal(hj.toordinal()+60)
      db.sub_venda.insert(projeto=projeto.id,
                         data_inicio_cobranca=futuro,
                         primeira_cidade="Primeira Rota")
    diferenca=projeto.data_final-hj
    if diferenca.days>=0:
      #redirect(URL('acs_mensagem','usuario_bloqueado',args="Usuario bloqueado"))
      projeto.venda_finalizada=False
      projeto.update_record()
    else:
      projeto.venda_finalizada=True
      projeto.update_record()
    empresa = db.empresa(projeto.empresa)
    usuario = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user)
    if usuario.bloqueado==True:
      redirect(URL('acs_mensagem','usuario_bloqueado',args="Usuario Temporariamente Bloqueado!"))
    if usuario.empresa!=empresa.id:
      usuario.bloqueado=True
      usuario.nome="Bloqueio 2714"
      usuario.update_record()
      redirect(URL('acs_mensagem','usuario_bloqueado',args="Usuario bloqueado"))
    
    diferenca=diferenca.days
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
    usuario = auth.user
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
