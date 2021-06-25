# -*- coding: utf-8 -*-

db.define_table('simulacao',
                Field('empresa','reference empresa', label='empresa', writable=False, readable=False),
                Field('descricao', 'string', label='Nome Empresa', writable=False, readable=False, default=""),
                Field('venda', 'double', label='Valor da Venda', notnull=True, default=0),
                Field('perc_margem', 'double', label='%-Margem Mercadoria', notnull=True, default=0),
                Field('perc_retorno', 'double', label='%-Retorno', notnull=True, default=0),
                Field('perc_avista', 'double', label='%-À vista', notnull=True, default=0),
                Field('perc_desp_local', 'double', label='%-Desp Local', notnull=True, default=0),
                Field('perc_funcionarios', 'double', label='%-Desp Funcionario', notnull=True, default=0),
                Field('perc_desp_venda', 'double', label='%-Desp Venda', notnull=True, default=0),
                Field('perc_desp_cobranca', 'double', label='%-Desp Cobrança', notnull=True, default=0),
                Field('perc_cobrado', 'double', label='%-Cobrança', notnull=True, default=0),
                Field('perc_devolucao', 'double', label='%-Devolução', notnull=True, default=0),
                Field('perc_comiss_vendedor', 'double', label='%-Comiss Vendedor', notnull=True, default=0),
                Field('perc_comiss_chefe', 'double', label='%-Comiss Chefe', notnull=True, default=0),
                Field('perc_comiss_cobrador', 'double', label='%-Comiss Cobrador', notnull=True, default=0),
                Field('perc_devolucao', 'double', label='%-Devolução', notnull=True, default=0),
                format='%(descricao)s')



db.define_table('cotacao',
                Field('empresa','reference empresa', label='empresa', writable=False, readable=False),
                Field('data_cotacao', 'date', label="Data Cotaçao", default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('fornecedor', 'string', label='Fornecedor', writable=True, readable=True, default="",requires = IS_UPPER()),
                Field('produto', 'string', label='Produto', writable=True, readable=True, default="",requires = IS_UPPER()),
                Field('tipo', 'string', label='Tipo de Compra', writable=True, readable=True, default="A Prazo"),
                Field('custo', 'double', label='Valor Compra', notnull=True, default=0),
                Field('preco', 'double', label='Valor Venda', notnull=True, default=0),
                format='%(produto)s')

db.cotacao.tipo.requires = IS_IN_SET(['À Vista','A Prazo'])
