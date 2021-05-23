# -*- coding: utf-8 -*-

import datetime
@auth.requires_login()
def index():
    usuario=auth.user
    usuario
    projeto = db.projeto(request.args(0, cast=int))
    rows = db((db.sub_venda.projeto == request.args(0, cast=int)) & (db.sub_venda.total_venda_praso>0)).select(orderby=db.sub_venda.data_inicio_cobranca)
    for row in rows:
        sum = db.venda.venda_praso.sum()-db.venda.valor_devolvido.sum()
        row.total_venda_praso = (db(db.venda.sub_venda == row.id).select(sum).first()[sum])
        row.update_record()
        sum = db.venda.quant_fichas.sum()-db.venda.quant_fichas_devolvidas.sum()
        row.total_fichas = (db(db.venda.sub_venda == row.id).select(sum).first()[sum])
        row.update_record()
    return locals()

@auth.requires_login()
def cobranca_periodo():
    empresa = db.empresa(request.args(2, auth.user))
    mes=request.now
    ano=request.now
    mes=request.args(0, cast=int)
    ano=request.args(1, cast=int)
    primeira_data=datetime.date(ano, mes, 1)
    ultima_data=datetime.date(ano, mes, 1)

    if (mes==12):
        ultima_data=datetime.date(ano+1, 1, 1)
    else:
        ultima_data=datetime.date(ano, mes+1, 1)
    rows = db((db.registro_cobranca.empresa==empresa.id)&(db.registro_cobranca.tipo=='Recebimento')&(db.registro_cobranca.data_inicio>=primeira_data)&(db.registro_cobranca.data_inicio<ultima_data)).select(orderby=db.registro_cobranca.data_inicio)
    return locals()


@auth.requires_login()
def depositos_periodo():
    empresa = db.empresa(request.args(2, auth.user))
    mes=request.now
    ano=request.now
    mes=request.args(0, cast=int)
    ano=request.args(1, cast=int)
    primeira_data=datetime.date(ano, mes, 1)
    ultima_data=datetime.date(ano, mes, 1)

    if (mes==12):
        ultima_data=datetime.date(ano+1, 1, 1)
    else:
        ultima_data=datetime.date(ano, mes+1, 1)
    rows = db((db.registro_cobranca.empresa==empresa.id)&(db.registro_cobranca.tipo=='Deposito')&(db.registro_cobranca.data_inicio>=primeira_data)&(db.registro_cobranca.data_inicio<ultima_data)).select(orderby=db.registro_cobranca.data_inicio)
    return locals()
@auth.requires_login()
def relatorio_cobranca():
    sub_venda = db.sub_venda(request.args(0, cast=int))
    desbloqueado=True
    if auth.user.id==sub_venda.auth_user:
        desbloqueado=False
    if sub_venda.total_venda_praso<0:
        redirect(URL('acessar_cobrancas',args=sub_venda.projeto))
    return locals()
def inserir_empresa():
    rows=db((db.registro_cobranca)).select()
    for row in rows:
        row.empresa=row.sub_venda.projeto.empresa
        #row.update_record()
    redirect(URL('default','index'))
    return locals()

@auth.requires_login()
def definir_cobrador():
    sub_venda = db.sub_venda(request.args(0, auth.user))
    projeto = db.projeto(sub_venda.projeto)
    rows = db(db.usuario_empresa.empresa==projeto.empresa).select()
    return locals()

@auth.requires_login()
def definir_cobrador_confirmar():
    sub_venda = db.sub_venda(request.args(0, auth.user))
    usuario = db.usuario_empresa(request.args(1, auth.user))
    sub_venda.auth_user=usuario.auth_user
    sub_venda.nome_cobrador=usuario.nome
    sub_venda.update_record()
    redirect(URL('definir_cobrador', args=sub_venda.id))
    return locals()


@auth.requires_login()
def saldo_quitacao():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.vendedor.projeto == projeto.id).select(orderby=~db.vendedor.total_vendas)
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

    db.sub_venda.data_inicio_cobranca.readable = True
    db.sub_venda.data_inicio_cobranca.writable = True

    db.sub_venda.nome_cobrador.writable = True

    db.sub_venda.data_final_cobranca.readable = False
    db.sub_venda.data_final_cobranca.writable = False

    db.sub_venda.primeira_cidade.readable = True
    db.sub_venda.primeira_cidade.writable = True

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


    db.sub_venda.descricao.readable = True
    db.sub_venda.descricao.writable = True
    form = SQLFORM(db.sub_venda, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('relatorio_cobranca', args=sub_venda.id))
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
def alterar_comissao_cobranca():
    response.view = 'generic.html' # use a generic view
    vendedor = db.vendedor(request.args(0, cast=int))
    projeto = db.projeto(vendedor.projeto)
    db.vendedor.id.readable = False
    db.vendedor.id.writable = False

    db.vendedor.projeto.readable = False
    db.vendedor.projeto.writable = False

    db.vendedor.nome.readable = True
    db.vendedor.nome.writable = True

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
