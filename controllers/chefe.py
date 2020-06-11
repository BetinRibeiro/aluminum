# -*- coding: utf-8 -*-

@auth.requires_login()
def acesso_chefe():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.usuario_empresa.empresa==projeto.empresa).select()
    return locals()

@auth.requires_login()
def acesso_inicial_usuario():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.usuario_empresa.empresa==projeto.empresa).select()
    return locals()

@auth.requires_login()
def alterar_dados_chefe():
    response.view = 'generic.html' # use a generic view
    projeto = db.projeto(request.args(0, cast=int))
    db.projeto.nome_chefe.readable = True
    db.projeto.nome_chefe.writable = True
    if request.args(1, cast=int)!=0:
        chefe = db.auth_user(request.args(1, cast=int))
        projeto.auth_user = chefe.id
        projeto.nome_chefe = chefe.first_name
        projeto.update_record()
        db.projeto.nome_chefe.readable = True
        db.projeto.nome_chefe.writable = False
        db.projeto.auth_user.readable = True
        db.projeto.auth_user.writable = False
    if projeto.venda_finalizada:
        session.flash = 'A venda já foi finalizada'
        redirect(URL('projeto','acesso_projeto', args=projeto.id))

    db.projeto.id.readable = False
    db.projeto.id.writable = False

    db.projeto.empresa.readable = True
    db.projeto.empresa.writable = False

    db.projeto.vale_saida.readable = True
    db.projeto.vale_saida.writable = True

    db.projeto.comissao_vista.readable = True
    db.projeto.comissao_vista.writable = True

    db.projeto.comissao_praso.readable = True
    db.projeto.comissao_praso.writable = True
    
    db.projeto.comissao_cobranca.readable = True
    db.projeto.comissao_cobranca.writable = True

    form = SQLFORM(db.projeto, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('acesso_chefe', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
        
    return dict(form=form)

@auth.requires_login()
def relatorio():
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
def relatoriomeme():
    projeto = db.projeto(request.args(0, cast=int))
    subvenda = db(db.sub_venda.projeto == projeto.id).select()
    for a in subvenda:
        totalvenda = db(db.venda.sub_venda == a.id).select(db.venda.venda_praso.sum()).first()[db.venda.venda_praso.sum()]
        totalvenda -= db(db.venda.sub_venda == a.id).select(db.venda.valor_devolvido.sum()).first()[db.venda.valor_devolvido.sum()]
        totalfichas = db(db.venda.sub_venda == a.id).select(db.venda.quant_fichas.sum()).first()[db.venda.quant_fichas.sum()]
        totalfichas -= db(db.venda.sub_venda == a.id).select(db.venda.quant_fichas_devolvidas.sum()).first()[db.venda.quant_fichas_devolvidas.sum()]
        a.quant_fichas=totalfichas
        a.venda_praso=totalvenda
        a.update_record()
    return locals()
