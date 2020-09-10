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
