# -*- coding: utf-8 -*-
def index():
    return locals()
#gera arquivo para criação de toda empresa e projetos
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def captura_empresa():
    
    a1 = SQLFORM.smartgrid(db.empresa)
    #a2 = SQLFORM.grid(db.empresa,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #a3 = SQLFORM.grid(db.projeto,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #a4 = SQLFORM.grid(db.carrada,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #a5 = SQLFORM.grid(db.item_carrada,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    
    #a6 = SQLFORM.grid(db.funcionario,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #a7 = SQLFORM.grid(db.vale_funcionario,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #a8 = SQLFORM.grid(db.vendedor,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #a9 = SQLFORM.grid(db.sub_venda,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #b1 = SQLFORM.grid(db.venda,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #b2 = SQLFORM.grid(db.cobranca_venda,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #b3 = SQLFORM.grid(db.classe_despesa,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #b4 = SQLFORM.grid(db.despesa,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    
    #b5 = SQLFORM.grid(db.classe_despesa_cobranca,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #b6 = SQLFORM.grid(db.despesa_cobranca,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #b7 = SQLFORM.grid(db.registro_venda,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #b8 = SQLFORM.grid(db.registro_cobranca,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #b9 = SQLFORM.grid(db.classe_despesa_local,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    #c1 = SQLFORM.grid(db.despesa_local,paginate=40,searchable=False,create=False,deletable=False,editable=False)
    return locals()
@auth.requires_login()
def acesso_inicial_usuario():
    #busca usuario da empresa, para verificar de qual empresa o login é
    usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user.id)
    liberar = auth.user.id
    #define empresa como nula
    empresa =None
    #caso o uruario esteja vinculado a alguma empresa
    if usuario_empresa:
        #busca a empresa que o funcionario esta vinculado
        empresa = db.empresa(usuario_empresa.empresa)
    else:
        #caso contrario retorna ao index (pagina inicial)
        session.flash = 'Procure o administrador'
        redirect(('https://api.whatsapp.com/send?phone=5588981126816'))
        #busca todos os projetos do usuario
    rows = db(db.projeto.auth_user==auth.user.id).select()
    rowscob = db(db.sub_venda.auth_user==auth.user.id).select()
    #3 consultas no banco
    return locals()
#o acesso inicial requer estar logado
@auth.requires_login()
def acesso_inicial():
    #busca empresa que tenha o usuario iguela ao logado
    empresa = db.empresa(db.empresa.auth_user==auth.user.id)
    usuario=auth.user
    if (auth.user.id==44) or (auth.user.id==45) or (auth.user.id==46):
        redirect(URL('acs_chefe','index'))
    if (auth.user.id==6):
        empresa = db.empresa(4)
        #empresa.id
        redirect(URL('usuario','fsprojetos',args=empresa.id))
    #caso seja hiago vai listar todos os projetos da empresa fs
    if (auth.user.id==11)or(auth.user.id==10):
        empresa = db.empresa(8)
        #empresa.id
        redirect(URL('usuario','fsprojetos',args=empresa.id))
    if auth.user.id==10:
        empresa = db.empresa(8)
        redirect(URL('usuario','fsprojetos',args=empresa.id))
    #caso não tenha nem uma empresa o usuario pode estar vinculado a
    #algum projeto ou sub venda pode ser (chefe ou cobrador)
    if not empresa:
        #redireciona para pagina de usuario)
        redirect(URL('acesso_inicial_usuario'))
    #caso contrario procegue, busca todos os projetos da empresa
    rows = db(db.projeto.empresa==empresa.id).select()
    if request.args(0, auth.user)=="235":
        rows = db(db.projeto.empresa).select(orderby=db.empresa)
    #2 consultas no banco
    return locals()
@auth.requires_login()
def criar_projeto():
    response.view = 'generic.html' # use a generic view
    #recebe id da empresa como parametro e busca empresa
    empresa = db.empresa(request.args(0, auth.user))
    #bloqueia visualização empresa e coloca o id da empresa como padrão
    db.projeto.empresa.default = empresa.id
    db.projeto.empresa.writable = False
    #deixa o usuario que esta logado como usuario padrão
    #deixa o id bloqueado para visualização
    if (auth.user.id!=empresa.auth_user)or(auth.user.id!=11)or(auth.user.id!=1):
        db.projeto.auth_user.default = auth.user.id
        db.projeto.auth_user.writable = False
    #deixa o nome padrão e bloqueia para visualização
    db.projeto.nome_chefe.default = auth.user.first_name
    db.projeto.nome_chefe.writable = False
    #cria um sqlforma para ser processado
    form = SQLFORM(db.projeto).process()
    if form.accepted:
        #caso aceito redireciona para tela de acesso inicial
        response.flash = 'Formulario aceito'
        projeto=db.projeto(form.vars.id)
        redirect(URL('acesso_inicial'))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    #2 consultas no banco
    return  dict(form=form)

# para alterar precisa estar logado
@auth.requires_login()
def alterar_projeto():
    response.view = 'generic.html' # use a generic view
    #recebe id do projeto e busca projeto no banco
    usuario = auth.user
    projeto = db.projeto(request.args(0, cast=int))
    #caso o projeto não esteja ativo redireciona
    #pois não pode ser alterado
    if projeto.venda_finalizada:
        session.flash = 'A venda já foi finalizada'
        redirect(URL('projeto','acesso_projeto', args=projeto.id))
    
        
    #bloqueia id para visualização e alteração
    db.projeto.id.readable = False
    db.projeto.id.writable = False
    #bloqueia empresa para alteração
    db.projeto.empresa.readable = True
    db.projeto.empresa.writable = False
    a=True
    #caso a venda a prazo seja maior que zero não deleta
    #medida de segurança
    if projeto.total_venda_prazo>0:
        a=False
    
    if auth.user.id==1:
        db.projeto.empresa.readable = True
        db.projeto.empresa.writable = True
        a=True
    #buzca um sqlforma para ser alterado
    form = SQLFORM(db.projeto, request.args(0, cast=int), deletable=a)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('acesso_inicial'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    
    #2 consultas no banco
    return  dict(form=form)
# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=True, editable=True)
    return dict(grid=grid)
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def gridsimples():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], create=False, deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
