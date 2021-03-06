# -*- coding: utf-8 -*-

def atualizar_projetos():
  rows = db.projeto().select()
  for row in rows:
    row.mercadiria_conferida=False
    row.retorno_conferido=False
    row.particionamento_conferida=False
    row.vales_conferido=False
    row.funcionario_caderno_conferido=False
    row.venda_prazo_conferida=False
    row.venda_vista_conferida=False
    row.despesa_venda_conferida=False
    row.despesa_local_conferida=False
    row.caderno_chefe_conferido=False
    row.percas_gratificacao_conferido=False
    row.pagamento_quitacao_conferido=False
    row.entrada_repasse_conferido=False
    row.cobranca_conferida=False

    row.update_or_insert()

  return locals()

  
@auth.requires_login()
def prestacao_individual():
  projeto = db.projeto(request.args(0, cast=int))
  rows = db(db.vendedor.projeto == request.args(0, cast=int)).select(orderby=~db.vendedor.total_vendas)
  return locals()
@auth.requires_login()
def acesso_projeto():
#     redirect(URL('default','index'))
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    if len(db(db.carrada.projeto == projeto.id).select())>0:
        data= db(db.carrada.projeto == projeto.id).select(orderby=db.carrada.data_envio).first().data_envio
    else:
        data= None
    #caso o usuario da empresa for diferênte do usuario logado
    #redireciona pois será um usuario do projeto (chefe) ou 
    #usuario da sub_venda(Cobrador)
    usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user.id)
    if usuario_empresa:
      if (usuario_empresa.tipo=="Cobrador"):
        redirect(URL('default','index'))
      elif((usuario_empresa.tipo=="Chefe")):
        if projeto.auth_user!=auth.user.id:
          redirect(URL('default','index'))
    usuario=auth.user
    #if (usuario.id==1):
        #redirect(URL('usuario','betinho_acesso',args=projeto.id))
    if (usuario.id==6)or(usuario.id==1686734):
        redirect(URL('usuario','abencoado',args=projeto.id))
    if (usuario.id==105435)or(usuario.id==1456789):
        redirect(URL('usuario','fscontador',args=projeto.id))
        #flavio é o ligin 11
    if (usuario.id==156745631)or(usuario.id==1123456):
        redirect(URL('usuario','fscontador',args=projeto.id))
    if (usuario.id==1):
        projeto.auth_user=None
    if projeto.auth_user==auth.user.id:
        redirect(URL('usuario','acesso_projeto',args=projeto.id))
    return locals()
@auth.requires_login()
def prestacao_venda():
    projeto = db.projeto(request.args(0, cast=int))
    return locals()

@auth.requires_login()
def alterar_ent_said():
    response.view = 'generic.html' # use a generic view
    projeto = db.projeto(request.args(0, cast=int))

    db.projeto.id.readable = False
    db.projeto.id.writable = False

    db.projeto.descricao_adiantamento.readable = False
    db.projeto.descricao_adiantamento.writable = False

    db.projeto.descricao_vale.readable = False
    db.projeto.descricao_vale.writable = False

    db.projeto.empresa.readable = False
    db.projeto.empresa.writable = False

    db.projeto.descricao.readable = False
    db.projeto.descricao.writable = False

    db.projeto.adiantamento.readable = True
    db.projeto.adiantamento.writable = True

    db.projeto.total_acrescentado_dinheiro.readable = False
    db.projeto.total_acrescentado_dinheiro.writable = False

    db.projeto.total_devolucao_dinheiro.readable = True
    db.projeto.total_devolucao_dinheiro.writable = True
    
    db.projeto.venda_finalizada.readable = True
    db.projeto.venda_finalizada.writable = True

    form = SQLFORM(db.projeto, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('projeto','prestacao_venda', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return  dict(form=form)

@auth.requires_login()
def investimento():
    projeto = db.projeto(request.args(0, cast=int))
    return locals()

# @auth.requires_login()
# def prestacao_individual():
#     projeto = db.projeto(request.args(0, cast=int))
#     rows_vendedor = db(db.vendedor.projeto == projeto.id).select(orderby=~db.vendedor.total_vendas)
#     rows_sub = db(db.sub_venda.projeto == projeto.id).select(orderby=db.sub_venda.data_inicio_cobranca)
#     rows_vendas = db(db.venda).select(orderby=db.venda.vendedor)
#     return locals()
