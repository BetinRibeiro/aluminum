# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.vendedor.projeto == request.args(0, cast=int)).select(orderby=~db.vendedor.total_vendas)
    return locals()

@auth.requires_login()
def projetos():
    usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==request.args(0, cast=int))
    empresa = db.empresa(usuario_empresa.empresa)
    rows = db(db.projeto.auth_user == usuario_empresa.auth_user).select(orderby=~db.projeto.descricao)
    rows_cobrancas = db(db.sub_venda.auth_user == usuario_empresa.auth_user).select(orderby=~db.sub_venda.primeira_cidade)
    return locals()

@auth.requires_login()
def adicionar_vendedor():
    response.view = 'generic.html' # use a generic view
    projeto = db.projeto(request.args(0, auth.user))

    db.vendedor.projeto.default = projeto.id
    db.vendedor.projeto.writable = False
    
    db.vendedor.comissao_cobranca.readable = False
    db.vendedor.comissao_cobranca.writable = False

    form = SQLFORM(db.vendedor).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('index', args=projeto.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)

@auth.requires_login()
def acessar_venda():
    usuario = auth.user
    vendedor = db.vendedor(request.args(0, cast=int))
    projeto = db.projeto(vendedor.projeto)
    rows_sub = db(db.sub_venda.projeto == vendedor.projeto).select(orderby=~db.sub_venda.data_inicio_cobranca)
    rows_vend = db(db.venda.vendedor == request.args(0, cast=int)).select(orderby=db.venda.sub_venda|db.venda.data_venda)
    return locals()

def alterar_vendedor():
    response.view = 'generic.html' # use a generic view
    vendedor = db.vendedor(request.args(0, cast=int))
    projeto = db.projeto(vendedor.projeto)
    db.vendedor.id.readable = False
    db.vendedor.id.writable = False

    db.vendedor.projeto.readable = False
    db.vendedor.projeto.writable = False
    
    db.vendedor.comissao_cobranca.readable = False
    db.vendedor.comissao_cobranca.writable = False
    
    deletar=True
    if vendedor.total_vendas>0:
        deletar=False
    usuario = auth.user
    if usuario.id==2234:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('index', args=projeto.id))
    form = SQLFORM(db.vendedor, request.args(0, cast=int), deletable=deletar)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('index', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)


@auth.requires_login()
def inserir_venda():
    response.view = 'generic.html' # use a generic view
    vendedor = db.vendedor(request.args(0, auth.user))
    sub_venda = db.sub_venda(request.args(1, auth.user))
    
    db.venda.sub_venda.default = sub_venda.id
    db.venda.sub_venda.writable = False
    db.venda.sub_venda.readable = False
    
    db.venda.quant_fichas_devolvidas.writable = False
    db.venda.quant_fichas_devolvidas.readable = False
    
    db.venda.valor_devolvido.writable = False
    db.venda.valor_devolvido.readable = False
    
    db.venda.vendedor.default = vendedor.id
    db.venda.vendedor.writable = False
    
    
    usuario = auth.user
    if usuario.id==243344:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('acessar_venda', args=vendedor.id))
    form = SQLFORM(db.venda).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acessar_venda', args=vendedor.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)

@auth.requires_login()
def alterar_venda():
    response.view = 'generic.html' # use a generic view
    venda = db.venda(request.args(0, cast=int))
    vendedor = db.vendedor(venda.vendedor)
    db.venda.id.readable = False
    db.venda.id.writable = False
        
    db.venda.sub_venda.default = venda.sub_venda
    db.venda.sub_venda.writable = False
    db.venda.sub_venda.readable = False

    db.venda.vendedor.readable = False
    db.venda.vendedor.writable = False
    
    usuario = auth.user
    if usuario.id==2324:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('acessar_venda', args=vendedor.id))

    form = SQLFORM(db.venda, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acessar_venda', args=vendedor.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
