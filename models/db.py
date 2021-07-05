# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
from urllib2 import Request, urlopen

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig()

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'), fake_migrate_all=False,
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
# -*- coding: utf-8 -*-
#essa classe vai ser utilizada para identificar um grupo especifico de projetos
db.define_table('empresa',
                Field('auth_user','reference auth_user', label='Usuario'),
                Field('nome', 'string', label='Nome',requires = IS_UPPER()),
                Field('descricao', 'text', label='Descrição',requires = IS_UPPER()),
                Field('nome_cobranca', 'string', label='Nome Cobrança'),
                Field('cpf_cobranca', 'string', label='CPF Cobrança'),
                Field('quant_usuarios', 'integer', writable=True, readable=True , notnull=True, default=4),
                Field('data_bloqueio', 'date', writable=True, readable=False, default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('valor', 'double', writable=True, readable=False, label='Valor', default=0, notnull=True),
                Field('bloqueada', 'boolean', label='Bloquear', writable=True, readable=True, default=False),
                format='%(nome)s')

db.define_table('produto',
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('nome', 'string', label='Nome',requires = IS_UPPER()),
                Field('bloqueado', 'boolean', label='Bloquear', writable=True, readable=True, default=True),
                format='%(nome)s')

db.define_table('funcionario_empresa',
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('nome', 'string', label='Nome',requires = IS_UPPER()),
                Field('debito', 'double',label="Débito", notnull=True, default=0),
                Field('observacao', 'text', label='Observação',requires = IS_UPPER()),
                Field('bloqueado', 'boolean', label='Bloquear', writable=True, readable=True, default=False),
                format='%(nome)s')
db.define_table('registro_funcionario_empresa',
                Field('funcionario_empresa','reference funcionario_empresa', writable=False, readable=False, label='Funcionario'),
                Field('tipo', 'string', label='Tipo',requires = IS_UPPER()),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                Field('valor', 'double',label="Débito", notnull=True, default=0),
                format='%(descricao)s')
#essa classe vai servir para alocara chefe de equipe e cobradores que são usuarios da empresa em outros projetos
db.define_table('usuario_empresa',
                Field('auth_user','reference auth_user', writable=False, readable=False, label='Usuario'),
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('tipo', 'string', label='Tipo'),
                Field('nome', 'string', label='Nome',requires = IS_UPPER()),
                Field('telefone', 'string', label='Telefone',requires = IS_UPPER()),
                Field('bloqueado', 'boolean', label='Bloquear', writable=True, readable=True, default=False),
                format='%(nome)s')
#projetos que são as informações da venda
db.define_table('projeto',
                Field('empresa','reference empresa', label='Empresa'),
                Field('data_inicial', 'date', writable=True, readable=True, default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('data_final', 'date', writable=False, readable=False, default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                Field('adiantamento', 'double',label="Adiantamento Venda", notnull=True, default=0),
                Field('descricao_adiantamento', 'text', label='Descrição do Adiantamento',requires = IS_UPPER()),
                Field('auth_user','reference auth_user', label='Chefe', writable=False, readable=False),
                Field('nome_chefe', 'string', writable=False, readable=False, label='Nome_chefe',requires = IS_UPPER()),
                Field('vale_saida', 'double', writable=True, readable=False, label='Vale Saida', default=0, notnull=True),
                Field('descricao_vale', 'text', label='Descrição do Vale do Chefe',requires = IS_UPPER()),
                Field('comissao_vista', 'double', writable=True, readable=False, label='Comissao Vista (chefe)', default=6, notnull=True),
                Field('comissao_praso', 'double', writable=True, readable=False, label='Comissao Prazo (chefe)', default=3, notnull=True),
                Field('comissao_cobranca', 'double', writable=True, readable=False, label='Comissao Cobrança', default=5, notnull=True),

                 #informações Mercadoria e retorno
                Field('total_pecas_mercadoria', 'integer', writable=False, readable=False , notnull=True, default=0),
                Field('total_preco_mercadoria', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_custo_mercadoria', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_pecas_gratificacao', 'integer', writable=False, readable=False , notnull=True, default=0),
                Field('total_preco_gratificacao', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_custo_gratificacao', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_pecas_refugo', 'integer', writable=False, readable=False , notnull=True, default=0),
                Field('total_preco_refugo', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_custo_refugo', 'double', writable=False, readable=False , notnull=True, default=0),

                Field('total_pecas_retorno', 'integer', writable=False, readable=False , notnull=True, default=0),
                Field('total_preco_retorno', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_custo_retorno', 'double', writable=False, readable=False , notnull=True, default=0),


                Field('total_venda_vista', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('quant_dias_venda_vista', 'integer', writable=False, readable=False , notnull=True, default=0),

                Field('quant_fichas_venda', 'integer', writable=False, readable=False , notnull=True, default=0),
                Field('total_entradas_venda', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_venda_prazo', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_comissao_venda', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_vales_vendedor', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_caderno_vendedor', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('quant_vendedores', 'integer', writable=False, readable=False , notnull=True, default=0),
                Field('total_saldo_vendedor', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_debito_vendedor', 'double', writable=False, readable=False , notnull=True, default=0),

                Field('total_salario_funcionario', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_vale_funcionario', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_caderno_funcionario', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('quant_funcionario', 'integer', writable=False, readable=False , notnull=True, default=0),
                Field('total_saldo_funcionario', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_debito_funcionario', 'double', writable=False, readable=False , notnull=True, default=0),

                Field('total_despesa_local', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_despesa_venda', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_despesa_cobranca', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_gratificacao', 'double', writable=False, readable=False , notnull=True, default=0),

                Field('total_caderno_chefe', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_saldo_chefe', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_debito_chefe', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_acrescentado_dinheiro', 'double',label="Dinheiro Acrescentado", writable=False, readable=False , notnull=True, default=0),
                Field('total_devolucao_dinheiro', 'double',label="Dinheiro Devolvido", writable=False, readable=False , notnull=True, default=0),
                Field('descricao_devolucao_dinheiro', 'text', label='Descrição Dinh. Devolvido', writable=False, readable=False,requires = IS_UPPER()),
                Field('total_adiantamento_cobranca', 'double',label="Adiantamento Cobrança Devolvido", writable=False, readable=False , notnull=True, default=0),
                Field('total_vale_cobrador', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_vale_caderno_cobrador', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_cobrado', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_despesa_cobranca', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_deposito_cobranca', 'double', writable=False, readable=False , notnull=True, default=0),

                Field('total_saldo_cobradores', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_debito_cobradores', 'double', writable=False, readable=False , notnull=True, default=0),

                Field('total_custo_devolucao_nova', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_custo_devolucao_aproveitamento', 'double', writable=False, readable=False , notnull=True, default=0),

                Field('total_saldo_quitacao_chefe', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_saldo_quitacao_vendedores', 'double', writable=False, readable=False , notnull=True, default=0),
                Field('total_debito_quitacao_vendedores', 'double', writable=False, readable=False , notnull=True, default=0),

                Field('dias_cobrando', 'integer', writable=False, readable=False , notnull=True, default=0),
                Field('venda_finalizada', 'boolean', writable=False, readable=False, default=False),
                Field('bloqueio_chefe', 'boolean', writable=True, readable=False, default=False),
                format='%(descricao)s')
db.projeto.empresa.readable = False
db.projeto.empresa.writable = False
db.projeto.id.readable = False
db.projeto.id.writable = False

db.define_table('carrada',
                Field('projeto','reference projeto', label='Equipe'),
                Field('data_envio', 'date', label="Data", default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                Field('total_pecas', 'integer', label='Quant. Peças', writable=False, readable=True , notnull=True, default=0),
                Field('total_preco', 'double', label='Total Preço', writable=False, readable=True , notnull=True, default=0),
                Field('total_custo', 'double', label='Total Custo', writable=False, readable=False , notnull=True, default=0),
                Field('finalizada', 'boolean', writable=False, readable=False, default=False),
                format='%(descricao)s')
db.define_table('item_carrada',
                Field('projeto','reference projeto', label='Equipe'),
                Field('carrada','reference carrada', label='Carrada'),
                Field('q_pcs', 'integer', label='Quant Peças', notnull=True, default=0),
                Field('descricao', 'string',label='Descrição', notnull=True,requires = IS_UPPER()),
                Field('preco_unitario', 'double',label='Preço Unit', notnull=True, default=0),
                Field('custo_unitario', 'double', writable=False, readable=False,label='Custo Unit', notnull=True, default=0),
                Field('quant_pcs_grt', 'integer',label='Peças Gratificação', writable=False, readable=False, default=0, notnull=True),
                Field('quant_pcs_rtr', 'integer',label='Peças Retorno', writable=False, readable=False, default=0, notnull=True),
                Field('quant_pcs_rfg', 'integer',label='Peças Estragadas', writable=False, readable=False, default=0, notnull=True)
                )
db.define_table('funcionario',
                Field('projeto','reference projeto', label='Equipe', writable=False, readable=False),
                Field('nome', 'string', label='Nome',requires = IS_UPPER()),
                Field('funcao', 'string', label='Função',requires = IS_UPPER()),
                Field('salario', 'double', label='Salario',  notnull=True, default=1500),
                Field('vale_saida', 'double', label='Vale da saida', notnull=True, default=0),
                Field('descricao_vale', 'text', label='Descrição do vale',requires = IS_UPPER()),
                Field('total_vale_caderno', 'double', label='Vale do Caderno', writable=False, readable=False, default=0, notnull=True),
                format='%(nome)s')
db.define_table('vale_funcionario',
                Field('funcionario','reference funcionario', label='Funcionario'),
                Field('data_vale', 'date', label="Data", default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('valor', 'double', label='Valor',  notnull=True, default=0),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER())
                )
db.define_table('vendedor',
                Field('empresa','reference empresa',writable=False, readable=False, label='Empresa'),
                Field('funcionario_empresa','reference funcionario_empresa',writable=False, readable=False, label='Funcionario Empresa'),
                Field('projeto','reference projeto', label='Equipe', writable=True, readable=True),
                Field('nome', 'string', label='Nome',requires = IS_UPPER()),
                Field('vale_saida', 'double',label='Vale da Saida', notnull=True, default=0),
                Field('comissao_venda', 'double',label='% Comissão', notnull=True, default=8),
                Field('descricao', 'text', label='Descrição do vale',requires = IS_UPPER()),
                Field('total_vale_caderno', 'double',label='Vale Caderno', writable=False, readable=False , notnull=True, default=0),
                Field('total_vendas', 'double', label='Venda a Prazo',writable=False, readable=False , notnull=True, default=0),
                Field('total_entradas', 'double', label='Entrada Venda',writable=False, readable=False , notnull=True, default=0),
                Field('total_fichas', 'integer', label='Quant Fichas',writable=False, readable=False , notnull=True, default=0),
                Field('comissao_cobranca', 'double',label='% Comissão Cobrança', notnull=True, default=10),
                Field('total_recebido', 'double',label='TotalRecebido', writable=False, readable=False , notnull=True, default=0),
                Field('total_devolvido', 'double', label='Total Devolução',writable=False, readable=False , notnull=True, default=0),
                Field('total_prego', 'double', label='Total de Prego',writable=False, readable=False , notnull=True, default=0),
                Field('total_fichas_retorno', 'integer', label='Quant Fichas',writable=False, readable=False , notnull=True, default=0),
                Field('total_descontado', 'double', label='Desconto de Quitação', writable=False, readable=False, notnull=True, default=0),
                format='%(nome)s')

db.define_table('funcionario_vendedor',
                Field('empresa','reference empresa', label='Empresa'),
                Field('vendedor','reference vendedor', label='Vendedor'),
                Field('funcionario_empresa','reference funcionario_empresa', label='Funcionario Empresa'),
                format='%(nome)s')

db.define_table('sub_venda',
                Field('projeto','reference projeto', label='Projeto', writable=False, readable=False),
                Field('empresa','reference empresa', label='Empresa', writable=False, readable=False),
                Field('auth_user','reference auth_user', label='Cobrador', writable=False, readable=False),
                Field('nome_cobrador', 'string', label='Nome Cobrador',requires = IS_UPPER()),
                Field('data_inicio_cobranca', 'date', label="Data Cobrança",notnull=True, default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('data_final_cobranca', 'date', label="Data Final Cobrança", writable=False, readable=False,notnull=True, default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('primeira_cidade', 'string', label='Descrição',requires = IS_UPPER()),
                Field('ultima_cidade', 'string', label='Ultima Cidade', writable=False, readable=False,requires = IS_UPPER()),
                Field('venda_finalizada', 'boolean', writable=False, readable=False, default=False),
                Field('total_fichas', 'integer', label='Quant Fichas', writable=False, readable=False, notnull=True, default=0),
                Field('total_venda_praso', 'double', writable=False, readable=False, notnull=True, default=0),
                Field('total_entradas', 'double', writable=False, readable=False, notnull=True, default=0),

                Field('adiantamento_cobranca', 'double',label='Adiantamento', writable=False, readable=False, notnull=True, default=0),
                Field('comissao_cobranca', 'double',label='% Comissão Cobrança', writable=False, readable=False, notnull=True, default=5),
                Field('total_vale_saida_cobrador', 'double',label='Vale Saida', writable=False, readable=False, notnull=True, default=0),
                Field('descricao', 'text', label='Descrição do vale', writable=False, readable=False,requires = IS_UPPER()),

                Field('total_vale_caderno_cobrador', 'double', writable=False, readable=False, notnull=True, default=0),

                Field('total_recebido', 'double', writable=False, readable=False, notnull=True, default=0),
                Field('total_despesa', 'double', writable=False, readable=False, notnull=True, default=0),
                Field('total_deposito', 'double', writable=False, readable=False, notnull=True, default=0),
                Field('total_caderno_cobrador', 'double', writable=False, readable=False, notnull=True, default=0),
                Field('total_saldo_cobrador', 'double', writable=False, readable=False, notnull=True, default=0),
                Field('total_custo_devolucao_nova', 'double', writable=False, readable=False, notnull=True, default=0),
                Field('total_custo_devolucao_aproveitamento', 'double', writable=False, readable=False, notnull=True, default=0),
                Field('cobranca_iniciada', 'boolean', writable=False, readable=False, default=False),
                Field('cobranca_finalizada', 'boolean', writable=False, readable=False, default=False),
                format='%(primeira_cidade)s')
db.define_table('cobrador',
                Field('sub_venda','reference sub_venda', label='sub_venda', writable=True, readable=True),
                Field('nome', 'string', label='Nome',requires = IS_UPPER()),
                Field('tipo', 'string', label='Tipo Cobrador',default="Chefe"),
                Field('vale_saida', 'double',label='Vale da Saida', notnull=True, default=0),
                Field('comissao_venda', 'double',label='% Comissão', notnull=True, default=8),
                Field('tipo_comissao', 'string', label='Tipo Comiss',default="Geral"),
                Field('descricao', 'text', label='Descrição do vale',requires = IS_UPPER()),
                Field('total_vale_caderno', 'double',label='Vale Caderno', writable=False, readable=False , notnull=True, default=0),
                Field('total_recebido', 'double',label='Vale Caderno', writable=False, readable=False , notnull=True, default=0),
                Field('total_fichas_retorno', 'integer', label='Quant Fichas',writable=False, readable=False , notnull=True, default=0),
                format='%(nome)s')
db.define_table('venda',
                Field('sub_venda','reference sub_venda', label='Sub-Venda', writable=True, readable=True),
                Field('vendedor','reference vendedor', label='Vendedor', writable=True, readable=True),
                Field('data_venda', 'date', label="Data Venda", default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('vale_caderno', 'double', label='Vale Caderno', notnull=True, default=0),
                Field('quant_fichas', 'integer', label='Quant Fichas', notnull=True, default=0),
                Field('venda_praso', 'double', label='Venda Prazo', notnull=True, default=0),
                Field('entradas_venda', 'double', label='Entrada', notnull=True, default=0),
                Field('venda_vista', 'double', writable=False, readable=False, label='Venda à Vista', notnull=True, default=0),
                Field('quant_fichas_devolvidas', 'integer', label='Quant Fichas Devolvidas', notnull=True, default=0),
                Field('valor_devolvido', 'double', label='Valor Devolvido', notnull=True, default=0),
                Field('descricao_devolucao', label='Descrição do Caderno',requires = IS_UPPER()),
				)
db.define_table('cobranca_venda',
                Field('sub_venda','reference sub_venda', label='Sub-Venda', writable=True, readable=True),
                Field('vendedor','reference vendedor', label='Vendedor', writable=True, readable=True),
                Field('recebido', 'double', notnull=True, default=0),
                Field('devolvido', 'double', notnull=True, default=0),
                Field('prego', 'double', notnull=True, default=0),
                Field('quant_fichas_devolvidas', 'integer', notnull=True, default=0),
				)

db.define_table('classe_despesa',
                Field('projeto','reference projeto', label='Equipe'),
                Field('tipo', 'string', label='Tipo',requires = IS_UPPER()),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                Field('total_classe', 'double', label='Total', writable=False, readable=True , notnull=True, default=0),
                auth.signature,
                format='%(descricao)s')

db.define_table('despesa',
                Field('projeto','reference projeto', label='Equipe', writable=False, readable=False),
                Field('classe_despesa','reference classe_despesa', label='Classe', writable=False, readable=False),
                Field('tipo', 'string', label='Tipo',requires = IS_UPPER(), writable=False, readable=True),
                Field('data_inicio', 'date', label="Data", default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('descricao', 'string',label='Descrição', default="DESPESA", notnull=True,requires = IS_UPPER()),
                Field('valor', 'double',label='Valor', notnull=True, default=0),
                )

db.define_table('classe_despesa_cobranca',
                Field('sub_venda','reference sub_venda', label='Cobrança'),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                Field('total_despesa', 'double', label='Total', writable=False, readable=True , notnull=True, default=0),
                Field('bloqueado', 'boolean', label='Bloquear', writable=True, readable=True, default=False),
                format='%(descricao)s')
db.define_table('despesa_cobranca',
                Field('sub_venda','reference sub_venda', label='Cobrança', writable=False, readable=False),
                Field('classe_despesa_cobranca','reference classe_despesa_cobranca', label='Classe Despesa', writable=True, readable=True),
                Field('data_inicio', 'date', label="Data", default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('descricao', 'string',label='Descrição', default="DESPESA", notnull=True,requires = IS_UPPER()),
                Field('valor', 'double',label='Valor', notnull=True, default=0),
                )

db.define_table('registro_venda',
                Field('projeto','reference projeto', label='Equipe'),
                Field('tipo', 'string', label='tipo',requires = IS_UPPER(), writable=False, readable=True , notnull=True),
                Field('data_inicio', 'date', label="Data", default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('descricao', 'string',label='Descrição', default="#", notnull=True,requires = IS_UPPER()),
                Field('valor', 'double',label='Valor', notnull=True, default=0),
                )
db.define_table('registro_cobranca',
                Field('sub_venda','reference sub_venda', label='Cobrança'),
                Field('empresa','reference empresa', writable=False, readable=False, label='empresa'),
                Field('projeto','reference projeto'),
                Field('tipo', 'string', label='tipo',requires = IS_UPPER(), writable=False, readable=True , notnull=True),
                Field('data_inicio', 'date', label="Data", default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('descricao', 'string',label='Descrição', default="#", notnull=True,requires = IS_UPPER()),
                Field('valor', 'double',label='Valor', notnull=True, default=0),
                Field('observacao', 'string',label='Observacao', writable=False, readable=False, default="#", notnull=True,requires = IS_UPPER()),
                Field('bloqueado', 'boolean', writable=False, readable=False, default=False),
                )
db.define_table('classe_despesa_local',
                Field('empresa','reference empresa', label='Empresa'),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                Field('total_classe', 'double', label='Total', writable=False, readable=True , notnull=True, default=0),
                auth.signature,
                format='%(descricao)s')

db.define_table('despesa_local',
                Field('classe_despesa_local','reference classe_despesa_local', label='Classe', writable=True, readable=True),
                Field('data_inicio', 'date', label="Data Inicio", default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('descricao', 'string',label='Descrição', default="DESPESA", notnull=True,requires = IS_UPPER()),
                Field('valor', 'double',label='Valor', notnull=True, default=0),
                )
