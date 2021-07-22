# -*- coding: utf-8 -*-
from datetime import date
@auth.requires_login()
#esse tipo de cache considera as variaveis diferêntes
@cache.action(time_expire=300, cache_model=cache.ram, quick='SVP')
def acesso_projeto():
  #busca o projeto que quer acessar
    projeto = db.projeto(request.args(0, cast=int))
    #busca quantidade de partições que tem
    total_particao = db(db.sub_venda.projeto==projeto.id).count()
    #data de hoje que pode ser usada em dois if's
    hj = date.today()
    #verifica se não possui partições
    if total_particao==0:
      futuro = date.fromordinal(hj.toordinal()+75)
      db.sub_venda.insert(projeto=projeto.id,empresa=projeto.empresa,
                         data_inicio_cobranca=futuro,
                         primeira_cidade="PRIMEIRA ROTA COBRANÇA")
    #verifica se o projeto possui data final
    if projeto.data_final:
      diferenca=projeto.data_final-hj
      #se a data final tiver maior que a data de hoje
      #o projeto é bloqueado automaticamente
      if diferenca.days>=0:
        projeto.venda_finalizada=False
        projeto.update_record()
      else:
        projeto.venda_finalizada=True
        projeto.update_record()
    else:
      projeto.data_final=date.fromordinal(hj.toordinal()+60)
    usuario = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user)
    if usuario.bloqueado==True:
      redirect(URL('acs_mensagem','usuario_bloqueado',args="Usuario Temporariamente Bloqueado!"))
    if usuario.empresa!=projeto.empresa:
      usuario.bloqueado=True
      usuario.nome="Bloqueio (tentou acessar outro projeto, usuario.acesso_principal)"
      usuario.update_record()
      redirect(URL('acs_mensagem','usuario_bloqueado',args="Usuario bloqueado"))
    return locals()

  
  #as funções abaixo foram descontinuadas
  #estão bloqueada desde o dia 21 jun de 2021
  #caso tenha algum problema iremos corrigir
  #caso contrario seram deletadas no periodo dos proximos 
  #90 dias, verifique e delete
@auth.requires_login()
def acesso_completo():
    redirect(URL('default','index'))
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    return locals()
def betinho_acesso():
    redirect(URL('default','index'))
    redirect(URL('default','index'))
    empresa = db.empresa(projeto.empresa)
    return locals()
@auth.requires_login()
def abencoado():
    redirect(URL('default','index'))
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    if empresa.id!=4:
      redirect(URL('default','index'))
    data=db(db.carrada.projeto == projeto.id).select(orderby=db.carrada.data_envio).first().data_envio
    return locals()
@auth.requires_login()
def fsprojetos():
    redirect(URL('default','index'))
    empresa = db.empresa(request.args(0, cast=int))
    if auth.user.id==10:
        empresa = db.empresa(8)
    else:
      redirect(URL('default','index'))
    rows = db(db.projeto.empresa==empresa.id).select(orderby=~db.projeto.descricao)
    rowsd = db((db.classe_despesa_local.empresa == empresa.id)).select(orderby=~db.classe_despesa_local.descricao)
    rowsuser = db(db.usuario_empresa.empresa==empresa.id).select(orderby=db.usuario_empresa.nome)
    return locals()
@auth.requires_login()
def fs():
    redirect(URL('default','index'))
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    return locals()
@auth.requires_login()
@cache.action()
def fscontador():
    redirect(URL('default','index'))
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    return locals()
@auth.requires_login()
def chefefs():
    redirect(URL('default','index'))
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    return locals()
