# -*- coding: utf-8 -*-
# tente algo como
def quebrei(): 
    return locals()

def processo_154(): 
    projeto = db.projeto(80)
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
def motivos(): 
    return locals()

def principios(): 
    return locals()
def foco():
    return locals()
def meme_abencoado():
    sub_venda = db.sub_venda(db.sub_venda.id==81)
    projeto = db.projeto(sub_venda.projeto)
    rows = db(db.venda.sub_venda == sub_venda.id).select(orderby=db.venda.data_venda)
    return locals()

def meme_relatorio():
    
    projeto = db.projeto(59)
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
