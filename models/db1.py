# -*- coding: utf-8 -*-
db.define_table('cheque',
                Field('empresa','reference empresa', label='empresa'),
                Field('data_cheque', 'date', label="Data",notnull=True, default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('banco', 'string', label='Banco/AG',requires = IS_UPPER()),
                Field('conta', 'string', label='Conta/Nº',requires = IS_UPPER()),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                Field('valor', 'double', writable=True, readable=True , notnull=True, default=0),
                Field('observacao', 'text', label='Observação',requires = IS_UPPER()),
                Field('quitado', 'boolean', writable=True, readable=True, default=False),
                format='%(banco)s')

db.define_table('pagamento',
                Field('empresa','reference empresa', label='empresa'),
                Field('data_vencimento', 'date', label="Data Vencimento",notnull=True, default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                Field('valor', 'double', writable=True, readable=True , notnull=True, default=0),
                Field('link', 'string', label='Link Recebimento',requires = IS_UPPER()),
                Field('observacao', 'text', label='Observação', writable=True, readable=True,requires = IS_UPPER()),
                Field('quitado', 'boolean', writable=True, readable=True, default=False),
                format='%(descricao)s')

db.define_table('transporte',
                Field('empresa','reference empresa', label='empresa'),
                Field('km', 'integer', writable=True, readable=True , notnull=True, default=0),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                Field('placa', 'string', label='Placa',requires = IS_UPPER()),
                Field('ativo', 'boolean', writable=True, readable=True, default=True),
                format='%(descricao)s')

db.define_table('km',
                Field('transporte','reference transporte', label='transporte'),
                Field('data_registro', 'date', label="Data Registro",notnull=True, default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('km', 'integer', writable=True, readable=True , notnull=True, default=0),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                format='%(descricao)s')


db.define_table('devolucao',
                Field('sub_venda','reference sub_venda', label='Particao'),
                Field('data_registro', 'date', label="Data Registro",notnull=True, default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('data_recolhimento', 'date', label="Data Recolhimento",notnull=True, default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                Field('custo_pecas_novas', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('q_pecas', 'integer', writable=False, readable=False , notnull=True, default=0),
                Field('custo_aproveitamento', 'double', writable=True, readable=True , notnull=True, default=0),
                Field('observacao', 'text', label='Observação', writable=True, readable=True,requires = IS_UPPER()),
                Field('recolhido', 'boolean', writable=True, readable=True, default=False),
                format='%(descricao)s')

db.define_table('item_devolucao',
                Field('devolucao','reference devolucao', label='Devolucao'),
                Field('custo', 'double', writable=True, readable=False , notnull=True, default=0),
                Field('preco', 'double', writable=True, readable=False , notnull=True, default=0),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                Field('quant_ditada', 'integer', label='Quant Ditada', writable=True, readable=True , notnull=True, default=0),
                Field('quant_recolhida', 'integer', label='Quant Recolhida', writable=True, readable=True , notnull=True, default=0),
                Field('quant_novas', 'integer', label='Quant Pças Novas', writable=True, readable=True , notnull=True, default=0),
                format='%(descricao)s')
