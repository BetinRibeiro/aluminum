# -*- coding: utf-8 -*-
import datetime
@auth.requires_login()
def acessar_cobrancas():
    usuario=auth.user
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.sub_venda.projeto == request.args(0, cast=int)).select(orderby=db.sub_venda.data_inicio_cobranca)
    for row in rows:
        sum = db.venda.venda_praso.sum()-db.venda.valor_devolvido.sum()
        row.total_venda_praso = (db(db.venda.sub_venda == row.id).select(sum).first()[sum])
        row.update_record()
        sum = db.venda.quant_fichas.sum()-db.venda.quant_fichas_devolvidas.sum()
        row.total_fichas = (db(db.venda.sub_venda == row.id).select(sum).first()[sum])
        row.update_record()
    return locals()
@auth.requires_login()
def acesso_particao_cobranca():
    quant_cobrancas = db(db.sub_venda.auth_user==auth.user.id).count()
    sub_venda = db.sub_venda(request.args(0, cast=int))
    usuario=auth.user
    #se for ramon redireciona para a proxima cobranca
    if usuario.id==47:
      sub_venda = db.sub_venda(121)
    desbloqueado=True
    if auth.user.id==sub_venda.auth_user:
        desbloqueado=False
    if sub_venda.total_venda_praso<0:
        redirect(URL('acessar_cobrancas',args=sub_venda.projeto))
    sub_venda = db.sub_venda(request.args(0, cast=int))
    rows = db(db.cobrador.sub_venda==sub_venda.id).select(orderby=~db.cobrador.total_recebido)
    for row in rows:
      quantidade = db((db.registro_cobranca.sub_venda==sub_venda.id)&(db.registro_cobranca.tipo=="Recebimento")&(db.registro_cobranca.descricao.contains(row.nome))).count()
      if quantidade>0:
            sum = db.registro_cobranca.valor.sum()
            valor = db((db.registro_cobranca.sub_venda==sub_venda.id)&(db.registro_cobranca.tipo=="Recebimento")&(db.registro_cobranca.descricao.contains(row.nome))).select(sum).first()[sum]
            row.total_recebido=valor
      quantidade = db((db.registro_cobranca.sub_venda==sub_venda.id)&(db.registro_cobranca.tipo=="Caderno")&(db.registro_cobranca.descricao.contains(row.nome))).count()
      if quantidade>0:
            sum = db.registro_cobranca.valor.sum()
            valor = db((db.registro_cobranca.sub_venda==sub_venda.id)&(db.registro_cobranca.tipo=="Caderno")&(db.registro_cobranca.descricao.contains(row.nome))).select(sum).first()[sum]
            row.total_vale_caderno=valor
      row.update_record()
    return locals()

@auth.requires_login()
def alterar_dados():
    response.view = 'generic.html' # use a generic view
    sub_venda = db.sub_venda(request.args(0, cast=int))
    if auth.user.id==sub_venda.auth_user:
        redirect(URL('acesso_particao_cobranca',args=sub_venda.id))
    projeto = db.projeto(sub_venda.projeto)
    db.sub_venda.id.readable = False
    db.sub_venda.id.writable = False
    db.sub_venda.projeto.readable = False
    db.sub_venda.projeto.writable = False
    db.sub_venda.data_inicio_cobranca.readable = False
    db.sub_venda.data_inicio_cobranca.writable = False
    db.sub_venda.data_final_cobranca.readable = False
    db.sub_venda.data_final_cobranca.writable = False
    db.sub_venda.primeira_cidade.readable = False
    db.sub_venda.primeira_cidade.writable = False
    db.sub_venda.ultima_cidade.readable = False
    db.sub_venda.ultima_cidade.writable = False
    db.sub_venda.comissao_cobranca.readable = True
    db.sub_venda.comissao_cobranca.writable = True
    db.sub_venda.adiantamento_cobranca.readable = True
    db.sub_venda.adiantamento_cobranca.writable = True
    db.sub_venda.total_vale_saida_cobrador.readable = True
    db.sub_venda.total_vale_saida_cobrador.writable = True
    db.sub_venda.cobranca_finalizada.readable = True
    db.sub_venda.cobranca_finalizada.writable = True
    form = SQLFORM(db.sub_venda, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acesso_particao_cobranca', args=sub_venda.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

@auth.requires_login()
def alterar_particao():
    response.view = 'generic.html' # use a generic view
    sub_venda = db.sub_venda(request.args(0, cast=int))
    projeto = db.projeto(sub_venda.projeto)
    db.sub_venda.id.readable = False
    db.sub_venda.id.writable = False
    db.sub_venda.projeto.readable = False
    db.sub_venda.projeto.writable = False
    db.sub_venda.data_inicio_cobranca.readable = False
    db.sub_venda.data_inicio_cobranca.writable = False
    db.sub_venda.data_final_cobranca.readable = False
    db.sub_venda.data_final_cobranca.writable = False
    db.sub_venda.primeira_cidade.readable = False
    db.sub_venda.primeira_cidade.writable = False
    db.sub_venda.comissao_cobranca.readable = True
    db.sub_venda.comissao_cobranca.writable = True
    db.sub_venda.adiantamento_cobranca.readable = True
    db.sub_venda.adiantamento_cobranca.writable = True
    db.sub_venda.descricao.readable = True
    db.sub_venda.descricao.writable = True
    db.sub_venda.total_vale_saida_cobrador.readable = True
    db.sub_venda.total_vale_saida_cobrador.writable = True
    db.sub_venda.cobranca_iniciada.readable = True
    db.sub_venda.cobranca_iniciada.writable = True
    db.sub_venda.data_final_cobranca.readable = True
    db.sub_venda.data_final_cobranca.writable = True
    db.sub_venda.cobranca_finalizada.readable = True
    db.sub_venda.cobranca_finalizada.writable = True
    form = SQLFORM(db.sub_venda, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acesso_particao_cobranca', args=sub_venda.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

@auth.requires_login()
def lista_registros():
    usuario=auth.user
    sub_venda = db.sub_venda(request.args(0, auth.user))
    tipo = request.args(1, auth.user)
    dataontem=datetime.date(request.now.year, request.now.month, request.now.day)
    if (dataontem.day>2):
        dataontem=datetime.date(dataontem.year, dataontem.month, dataontem.day-2)
    else:dataontem=datetime.date(dataontem.year, dataontem.month-1, 27)
    rows = db((db.registro_cobranca.sub_venda==sub_venda.id)&(db.registro_cobranca.tipo==tipo)).select(orderby=db.registro_cobranca.data_inicio)
    consul=(request.args(2))
    if consul:
        consul= "entrou no if"
        #consulta = request.args(2, auth.user)
        rows = db((db.registro_cobranca.sub_venda==sub_venda.id)&(db.registro_cobranca.tipo==tipo)&(db.registro_cobranca.descricao.contains(request.args(2)))).select(orderby=db.registro_cobranca.data_inicio)
    return locals()

@auth.requires_login()
def inserir_registro():
    response.view = 'generic.html' # use a generic view
    sub_venda = db.sub_venda(request.args(0, auth.user))
    projeto = db.projeto(sub_venda.projeto)
    tipo = request.args(1, auth.user)
    db.registro_cobranca.sub_venda.default = sub_venda.id
    db.registro_cobranca.sub_venda.writable = False
    db.registro_cobranca.projeto.default = sub_venda.projeto
    db.registro_cobranca.projeto.writable = False
    db.registro_cobranca.empresa.default = projeto.empresa
    db.registro_cobranca.empresa.writable = False
    db.registro_cobranca.tipo.default = tipo
#     db.registro_cobranca.tipo.writable = True
    quant_cobradores=db(db.cobrador.sub_venda == sub_venda.id).count()
    if (quant_cobradores>0)and(tipo!="Deposito"):
      db.registro_cobranca.descricao.requires = IS_IN_DB(db(db.cobrador.sub_venda == sub_venda.id), 'cobrador.nome', '%(nome)s')
    else:
      db.registro_cobranca.descricao.default = tipo
    db.registro_cobranca.tipo.writable = False
#     db.registro_cobranca.descricao.default = tipo
    form = SQLFORM(db.registro_cobranca).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('lista_registros', args=[sub_venda.id,tipo]))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)

@auth.requires_login()
def alterar_registro():
    usuario=auth.user
    response.view = 'generic.html' # use a generic view
    registro_cobranca = db.registro_cobranca(request.args(0, cast=int))
    tipo = request.args(1)
    if registro_cobranca.descricao:
      if 'cfrd' in registro_cobranca.descricao:
        redirect(URL('lista_registros', args=[registro_cobranca.sub_venda,tipo]))
    sub_venda = db.sub_venda(registro_cobranca.sub_venda)
    db.registro_cobranca.id.readable = False
    db.registro_cobranca.id.writable = False
    db.registro_cobranca.sub_venda.readable = False
    db.registro_cobranca.sub_venda.writable = False
    db.registro_cobranca.projeto.readable = False
    db.registro_cobranca.projeto.writable = False
    db.registro_cobranca.empresa.writable = False
    db.registro_cobranca.tipo.readable = False
    db.registro_cobranca.tipo.writable = False
    if (registro_cobranca.tipo=="Deposito") and (usuario.id!=sub_venda.auth_user):
        db.registro_cobranca.observacao.readable = True
        db.registro_cobranca.observacao.writable = True
    form = SQLFORM(db.registro_cobranca, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('lista_registros', args=[registro_cobranca.sub_venda,tipo]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

@auth.requires_login()
def saldo_quitacao():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.vendedor.projeto == projeto.id).select(orderby=~db.vendedor.total_vendas)
    return locals()
@auth.requires_login()
def cobranca_individual():
    vendedor = db.vendedor(request.args(0, cast=int))
    projeto = db.projeto(vendedor.projeto)
    sub_venda = db.sub_venda(request.args(1, cast=int))
    rows_cob= db(db.cobranca_venda.vendedor==vendedor.id).select(orderby=db.cobranca_venda.recebido)
    rows_vend = db(db.venda.vendedor == vendedor.id).select(orderby=db.venda.data_venda)
    return locals()
@auth.requires_login()
def inserir_cobranca():
    response.view = 'generic.html' # use a generic view
    sub_venda=db.sub_venda(request.args(0, cast=int))
    vendedor=db.vendedor(request.args(1, cast=int))
    db.cobranca_venda.sub_venda.default = sub_venda.id
    db.cobranca_venda.sub_venda.writable = False
    db.cobranca_venda.vendedor.default = vendedor.id
    db.cobranca_venda.vendedor.writable = False
    form = SQLFORM(db.cobranca_venda).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('cobranca_individual', args=[vendedor.id,sub_venda.id]))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)
@auth.requires_login()
def alterar_cobranca():
    response.view = 'generic.html' # use a generic view
    cobranca_venda = db.cobranca_venda(request.args(0, cast=int))
    vendedor = db.vendedor(cobranca_venda.vendedor)
    db.cobranca_venda.id.readable = False
    db.cobranca_venda.id.writable = False
    db.cobranca_venda.sub_venda.readable = False
    db.cobranca_venda.sub_venda.writable = False
    db.cobranca_venda.vendedor.readable = False
    db.cobranca_venda.vendedor.writable = False

    form = SQLFORM(db.cobranca_venda, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('cobranca_individual', args=[vendedor.id,cobranca_venda.sub_venda]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
@auth.requires_login()
def alocar_valores():
    sub_venda = db.sub_venda(request.args(0, cast=int))
    projeto = db.projeto(sub_venda.projeto)
    rows = db(db.vendedor.projeto == projeto.id).select(orderby=~db.vendedor.total_vendas)
    rowscob = db(db.venda.sub_venda == sub_venda.id).select(orderby=~db.venda.vendedor)
    rowsrec = db(db.cobranca_venda.sub_venda == sub_venda.id).select(orderby=~db.cobranca_venda.vendedor)
    return locals()

@auth.requires_login()
def alterar_comissao():
    response.view = 'generic.html' # use a generic view
    vendedor = db.vendedor(request.args(0, cast=int))
    projeto = db.projeto(vendedor.projeto)
    db.vendedor.id.readable = False
    db.vendedor.id.writable = False
    db.vendedor.projeto.readable = False
    db.vendedor.projeto.writable = False
    db.vendedor.nome.readable = True
    db.vendedor.nome.writable = False
    db.vendedor.vale_saida.readable = False
    db.vendedor.vale_saida.writable = False
    db.vendedor.comissao_venda.readable = False
    db.vendedor.comissao_venda.writable = False
    db.vendedor.descricao.readable = False
    db.vendedor.descricao.writable = False
    form = SQLFORM(db.vendedor, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('saldo_quitacao', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

@auth.requires_login()
def relatorio_cobranca():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.sub_venda.projeto == projeto.id).select()
    return locals()

@auth.requires_login()
def acesso_cobrador():
    sub_venda = db.sub_venda(request.args(0, cast=int))
    return locals()
@auth.requires_login()
def dados_cobrador():
    sub_venda = db.sub_venda(request.args(0, cast=int))
    projeto = db.projeto(sub_venda.projeto)
    rows = db(db.usuario_empresa.empresa==projeto.empresa).select()
    return locals()
@auth.requires_login()
def alterar_dados_cobrador():
    response.view = 'generic.html' # use a generic view
    sub_venda = db.sub_venda(request.args(0, cast=int))
    db.sub_venda.nome_cobrador.readable = True
    db.sub_venda.nome_cobrador.writable = True
    if request.args(1, cast=int)!=0:
        cobrador = db.auth_user(request.args(1, cast=int))
        sub_venda.auth_user = cobrador.id
        sub_venda.nome_cobrador = cobrador.first_name
        sub_venda.update_record()
        db.sub_venda.nome_cobrador.readable = True
        db.sub_venda.nome_cobrador.writable = False
        db.sub_venda.auth_user.readable = True
        db.sub_venda.auth_user.writable = False
    if sub_venda.cobranca_finalizada:
        session.flash = 'A Cobrança já foi finalizada'
        redirect(URL('acesso_particao_cobranca', args=sub_venda.id))
    db.sub_venda.id.readable = False
    db.sub_venda.id.writable = False
    db.sub_venda.primeira_cidade.readable = False
    db.sub_venda.primeira_cidade.writable = False
    db.sub_venda.projeto.readable = False
    db.sub_venda.projeto.writable = False
    db.sub_venda.ultima_cidade.readable = False
    db.sub_venda.ultima_cidade.writable = False
    db.sub_venda.data_inicio_cobranca.readable = False
    db.sub_venda.data_inicio_cobranca.writable = False
    db.sub_venda.data_final_cobranca.readable = False
    db.sub_venda.data_final_cobranca.writable = False
    db.sub_venda.adiantamento_cobranca.readable = True
    db.sub_venda.adiantamento_cobranca.writable = True
    db.sub_venda.comissao_cobranca.readable = True
    db.sub_venda.comissao_cobranca.writable = True
    db.sub_venda.total_vale_saida_cobrador.readable = True
    db.sub_venda.total_vale_saida_cobrador.writable = True
    form = SQLFORM(db.sub_venda, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Partição atualizado'
        redirect(URL('dados_cobrador', args=sub_venda.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
def conferir():
  response.view = 'generic.html' # use a generic view
  registro_cobranca = db.registro_cobranca(request.args(0, cast=int))
  a=False
  if 'cfrd' in registro_cobranca.descricao:
    a=True
    registro_cobranca.descricao=registro_cobranca.descricao.replace('cfrd','')
  else:
    registro_cobranca.descricao=registro_cobranca.descricao+'cfrd'
  registro_cobranca.update_record()
  redirect(URL('lista_registros', args=[registro_cobranca.sub_venda,registro_cobranca.tipo]))
  return locals()
