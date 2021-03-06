# -*- coding: utf-8 -*-
@auth.requires_login()
def relatorio_chefe():
    projeto = db.projeto(request.args(0, cast=int))
    subvenda = db(db.sub_venda.projeto == projeto.id).select()
    totalvenda=0
    totalfichas=0
    try:
        for a in subvenda:
            totalvenda = db(db.venda.sub_venda == a.id).select(db.venda.venda_praso.sum()).first()[db.venda.venda_praso.sum()]
            totalvenda -= db(db.venda.sub_venda == a.id).select(db.venda.valor_devolvido.sum()).first()[db.venda.valor_devolvido.sum()]
            totalfichas = db(db.venda.sub_venda == a.id).select(db.venda.quant_fichas.sum()).first()[db.venda.quant_fichas.sum()]
            totalfichas -= db(db.venda.sub_venda == a.id).select(db.venda.quant_fichas_devolvidas.sum()).first()[db.venda.quant_fichas_devolvidas.sum()]
            a.quant_fichas=totalfichas
            a.venda_praso=totalvenda
            a.update_record()
            return locals()
    except:
        totalvenda=0
        totalfichas=0
        session.flash = 'Comece a Inserir vendas primeiro'
        #redirect(URL('projeto','acesso_projeto', args=projeto.id))
    return locals()

@auth.requires_login()
def relatorio_chefe_sal():
    projeto = db.projeto(request.args(0, cast=int))
    subvenda = db(db.sub_venda.projeto == projeto.id).select()
    totalvenda=0
    totalfichas=0
    try:
        for a in subvenda:
            totalvenda = db(db.venda.sub_venda == a.id).select(db.venda.venda_praso.sum()).first()[db.venda.venda_praso.sum()]
            totalvenda -= db(db.venda.sub_venda == a.id).select(db.venda.valor_devolvido.sum()).first()[db.venda.valor_devolvido.sum()]
            totalfichas = db(db.venda.sub_venda == a.id).select(db.venda.quant_fichas.sum()).first()[db.venda.quant_fichas.sum()]
            totalfichas -= db(db.venda.sub_venda == a.id).select(db.venda.quant_fichas_devolvidas.sum()).first()[db.venda.quant_fichas_devolvidas.sum()]
            a.quant_fichas=totalfichas
            a.venda_praso=totalvenda
            a.update_record()
            return locals()
    except:
        totalvenda=0
        totalfichas=0
        session.flash = 'Comece a Inserir vendas primeiro'
        #redirect(URL('projeto','acesso_projeto', args=projeto.id))
    return locals()
@auth.requires_login()
def investimento():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db((db.registro_venda.projeto == projeto.id) & (db.registro_venda.tipo == "Saldo_quitacao")).select(orderby=db.registro_venda.data_inicio)
    rowsr = db((db.registro_venda.projeto == projeto.id) & (db.registro_venda.tipo == "Entrada_repasse")).select(orderby=db.registro_venda.data_inicio)
    return locals()


@auth.requires_login()
def prestacao_venda():
    projeto = db.projeto(request.args(0, cast=int))
    return locals()

@auth.requires_login()
def prestacao_venda_sal():
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

    db.projeto.vale_saida.readable = False
    db.projeto.vale_saida.writable = False

    db.projeto.comissao_cobranca.readable = False
    db.projeto.comissao_cobranca.writable = False
    
    db.projeto.empresa.readable = False
    db.projeto.empresa.writable = False

    db.projeto.descricao.readable = False
    db.projeto.descricao.writable = False
    
    db.projeto.total_devolucao_dinheiro.readable = True
    db.projeto.total_devolucao_dinheiro.writable = True

    db.projeto.adiantamento.readable = True
    db.projeto.adiantamento.writable = True

    db.projeto.total_acrescentado_dinheiro.readable = False
    db.projeto.total_acrescentado_dinheiro.writable = False

    db.projeto.descricao_devolucao_dinheiro.readable = True
    db.projeto.descricao_devolucao_dinheiro.writable = True
      
    db.projeto.descricao_adiantamento.readable = True
    db.projeto.descricao_adiantamento.writable = True
    
    db.projeto.venda_finalizada.readable = True
    db.projeto.venda_finalizada.writable = True
    
    if projeto.id>125:
      db.projeto.descricao_devolucao_dinheiro.writable = False
      db.projeto.descricao_devolucao_dinheiro.readable = False
      db.projeto.total_devolucao_dinheiro.writable = False
      db.projeto.total_devolucao_dinheiro.readable = False
      db.projeto.adiantamento.writable = False
      db.projeto.descricao_adiantamento.readable = False
      db.projeto.descricao_adiantamento.writable = False
    form = SQLFORM(db.projeto, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('prestacao_venda', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return  dict(form=form)
  
  
def mapeamanto_administrativo():
    return locals()

  
def deposito_pagamento():
    projeto = db.projeto(request.args(0, cast=int))
    lista_cobrancas = db(db.sub_venda.projeto == projeto.id).select(orderby=db.sub_venda.data_inicio_cobranca)
    lista_pagamentos = db(db.cheque.projeto == projeto.id).select(orderby=db.cheque.data_cheque)
    return locals()
