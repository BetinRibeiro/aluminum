# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    try:
        data=request.now
        usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user.id)
        empresa = db.empresa(db.empresa.id==usuario_empresa.empresa)
        usuario=auth.user
        rows = db(db.projeto.auth_user==auth.user.id).select(orderby=db.projeto.descricao)
    except:
        redirect(URL('default','index'))
    return locals()

@auth.requires_login()
def inserir_projeto():
    response.view = 'generic.html' # use a generic view
    #recebe id da empresa como parametro e busca empresa
    empresa = db.empresa(request.args(0, auth.user))
    #bloqueia visualização empresa e coloca o id da empresa como padrão
    db.projeto.empresa.default = empresa.id
    db.projeto.empresa.writable = False
    db.projeto.comissao_cobranca.writable = False
    db.projeto.comissao_vista.writable = False
    db.projeto.comissao_praso.writable = False
    
    db.projeto.adiantamento.writable = False
    db.projeto.descricao_adiantamento.writable = False
    db.projeto.vale_saida.writable = False
    db.projeto.descricao_vale.writable = False
    #deixa o usuario que esta logado como usuario padrão
    #deixa o id bloqueado para visualização
    
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
        redirect(URL('index', args=empresa.id*12))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    #2 consultas no banco
    return  dict(form=form)

@auth.requires_login()
def acesso_projeto():
    projeto = db.projeto(request.args(0, auth.user))
    empresa = db.empresa(projeto.empresa)
    usuario=auth.user
    usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user.id)
    rows = db(db.sub_venda.projeto==projeto).select()
    if len(rows)<=0:
         db.sub_venda.insert( projeto=projeto.id, primeira_cidade="Rota Inicial")
    if (usuario.id!=1)and(usuario_empresa.empresa!=projeto.empresa):
        redirect(URL('default','index'))
    return locals()
