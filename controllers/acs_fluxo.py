# -*- coding: utf-8 -*-
def index():
    empresa = db.empresa(request.args(0, auth.user))
    lista_projetos_abertos = db((db.projeto.empresa==empresa.id)&(db.projeto.venda_finalizada==False)).select()
    custo_total =0
    preco_total =0
    venda_prazo_total =0
    venda_vista_total =0
    for projeto in lista_projetos_abertos:
      custo_total +=projeto.total_custo_mercadoria
      preco_total +=projeto.total_preco_mercadoria
      venda_prazo_total +=projeto.total_venda_prazo
      venda_vista_total +=projeto.total_venda_vista*2
    lista_cobrancas_andamento = db((db.sub_venda.empresa==empresa.id)&(db.sub_venda.cobranca_finalizada==False)).select()
    valor_total_cobrancas = 0
    valor_recebido_cobrancas =0 
    valor_depositos_cobrancas =0
    for cobranca in lista_cobrancas_andamento:
      valor_total_cobrancas +=cobranca.total_venda_praso
      valor_recebido_cobrancas += cobranca.total_recebido
      valor_depositos_cobrancas += cobranca.total_deposito
    lista_cheques_pendente = db((db.cheque.empresa==empresa.id)&(db.cheque.quitado==False)).select()
    total_contas = 0
    for cheque in lista_cheques_pendente:
      total_contas += cheque.valor
    return locals()
