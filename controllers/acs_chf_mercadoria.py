# -*- coding: utf-8 -*-
def carradas():
    projeto = db.projeto(request.args(0, auth.user))
    usuario=auth.user
    usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user.id)
    if (usuario.id!=1)and(usuario_empresa.empresa!=projeto.empresa):
        redirect(URL('default','index'))
    rows = db(db.carrada.projeto==projeto.id).select()
    return locals()

def acessar_carrada():
    carrada = db.carrada(request.args(0, auth.user))
    projeto = db.projeto(carrada.projeto)
    rows = db(db.item_carrada.carrada==carrada.id).select()
    return locals()

def adicionar_carrada():
    response.view = 'generic.html' # use a generic view
    #busca o projeto pelo id passado
    projeto = db.projeto(request.args(0, auth.user))
    if projeto.venda_finalizada:
        session.flash = 'A venda já foi finalizada'
        redirect(URL('carradas', args=projeto.id))
    #insere na coluna projeto o id do projeto atual
    db.carrada.projeto.default = projeto.id
    #bloqueia o espaço de projeto para que o usuario não consiga ver
    db.carrada.projeto.writable = False
    #form é uma variavel que recebe o formulario passado para a view
    form = SQLFORM(db.carrada).process()
    #caso o furmulario seja submetido
    if form.accepted:
        #mensagem que o formulario foi aceito
        response.flash = 'Carrada Inserida'
        #redireciona para o acesso as carradas passando como argumento o id do projeto
        redirect(URL('carradas', args=projeto.id))
    elif form.errors:
        #caso tenha erro no formulario aparecerá mensagem de erro
        response.flash = 'Formulario não aceito'
    return dict(form=form)

@auth.requires_login()
def alterar_dados_carrada():
    
    response.view = 'generic.html' # use a generic view
    carrada = db.carrada(request.args(0, cast=int))
    projeto = db.projeto(carrada.projeto)
    empresa = db.empresa(projeto.empresa)
    if projeto.venda_finalizada:
        session.flash = 'A venda já foi finalizada'
        redirect(URL('carradas', args=projeto.id))
    db.carrada.id.readable = False
    db.carrada.id.writable = False

    db.carrada.projeto.readable = False
    db.carrada.projeto.writable = False
    db.carrada.finalizada.readable = True
    db.carrada.finalizada.writable = True
    deletable=True
    #caso o usuario seja diferênte do chefe ele pode finalizar a carrada
    #ou liberar só o chefe que não pode alterar
    if empresa.auth_user!=auth.user.id:
        db.carrada.finalizada.readable = True
        db.carrada.finalizada.writable = True
        if carrada.finalizada:
            deletable=False
            db.carrada.data_envio.readable = True
            db.carrada.data_envio.writable = False

            db.carrada.descricao.readable = True
            db.carrada.descricao.writable = False
    deletar =True
    if carrada.total_pecas>0:
        deletar =False
        
    form = SQLFORM(db.carrada, request.args(0, cast=int), deletable=deletar)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('carradas', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)

def adicionar_item_carrada():
    response.view = 'generic.html' # use a generic view
    carrada = db.carrada(request.args(0, auth.user))
    projeto = db.projeto(carrada.projeto)
    empresa = db.empresa(projeto.empresa)
    if projeto.venda_finalizada:
        session.flash = 'A venda já foi finalizada'
        redirect(URL('carrada', args=projeto.id))
    db.item_carrada.projeto.default = projeto.id
    
    db.item_carrada.carrada.default = carrada.id
    db.item_carrada.carrada.writable = False

    if projeto.auth_user!=auth.user.id:
        db.item_carrada.custo_unitario.readable = True
        db.item_carrada.custo_unitario.writable = True


    db.item_carrada.projeto.default = carrada.projeto
    db.item_carrada.projeto.writable = False

    db.item_carrada.projeto.readable = False
    db.item_carrada.projeto.writable = False
    if (auth.user.id==10)or(auth.user.id==11):
        db.item_carrada.custo_unitario.readable = True
        db.item_carrada.custo_unitario.writable = True
    if (auth.user.id==1)or(auth.user.id==6):
        db.item_carrada.custo_unitario.readable = True
        db.item_carrada.custo_unitario.writable = True
    form = SQLFORM(db.item_carrada).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acessar_carrada', args=carrada.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    return dict(form=form)

def alterar_item_carrada():
    response.view = 'generic.html' # use a generic view
    item_carrada = db.item_carrada(request.args(0, cast=int))
    carrada = db.carrada(item_carrada.carrada)
    projeto = db.projeto(carrada.projeto)
    if projeto.venda_finalizada:
        session.flash = 'A venda já foi finalizada'
        redirect(URL('carradas', args=projeto.id))
    db.item_carrada.id.readable = False
    db.item_carrada.id.writable = False
    
    db.item_carrada.projeto.default = projeto.id

    db.item_carrada.carrada.readable = False
    db.item_carrada.carrada.writable = False

    db.item_carrada.projeto.readable = False
    db.item_carrada.projeto.writable = False
    empresa = db.empresa(projeto.empresa)
    #caso o usuario da empresa for diferênte do usuario logado
    #redireciona pois será um usuario do projeto (chefe) ou
    #usuario da sub_venda(Cobrador)
    if projeto.auth_user!=auth.user.id:
        db.item_carrada.custo_unitario.readable = True
        db.item_carrada.custo_unitario.writable = True
    if auth.user.id==6:
        db.item_carrada.projeto.default = carrada.projeto
        db.item_carrada.projeto.writable = False
    if (auth.user.id==10)or(auth.user.id==11):
        db.item_carrada.custo_unitario.readable = True
        db.item_carrada.custo_unitario.writable = True
    if (auth.user.id==1)or(auth.user.id==6):
        db.item_carrada.custo_unitario.readable = True
        db.item_carrada.custo_unitario.writable = True
    form = SQLFORM(db.item_carrada, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acessar_carrada', args=carrada.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)


def retorno():
    projeto = db.projeto(request.args(0, cast=int))
    rowscarrada = db(db.carrada.projeto == request.args(0, cast=int)).select(orderby=db.carrada.data_envio)
    rows = db(db.item_carrada.projeto==projeto.id).select(orderby=db.item_carrada.descricao)
    return locals()

def alterar_descricao():
    response.view = 'generic.html' # use a generic view
    item_carrada = db.item_carrada(request.args(0, cast=int))
    carrada = db.carrada(item_carrada.carrada)
    projeto = db.projeto(carrada.projeto)
    if projeto.venda_finalizada:
        session.flash = 'A venda já foi finalizada'
        redirect(URL('carradas', args=projeto.id))
    db.item_carrada.id.readable = False
    db.item_carrada.id.writable = False
    
    db.item_carrada.projeto.default = projeto.id

    db.item_carrada.carrada.readable = False
    db.item_carrada.carrada.writable = False

    db.item_carrada.projeto.readable = False
    db.item_carrada.projeto.writable = False
    

    db.item_carrada.q_pcs.readable = False
    db.item_carrada.q_pcs.writable = False

    db.item_carrada.preco_unitario.readable = True
    db.item_carrada.preco_unitario.writable = False
    empresa = db.empresa(projeto.empresa)
    
    form = SQLFORM(db.item_carrada, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('retorno', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)


def alterar_retorno():
    response.view = 'generic.html' # use a generic view
    item_carrada = db.item_carrada(request.args(0, cast=int))
    carrada = db.carrada(item_carrada.carrada)
    projeto = db.projeto(carrada.projeto)
    if projeto.venda_finalizada:
        session.flash = 'A venda já foi finalizada'
        redirect(URL('carradas', args=projeto.id))
    db.item_carrada.id.readable = False
    db.item_carrada.id.writable = False
    
    db.item_carrada.projeto.default = projeto.id

    db.item_carrada.carrada.readable = False
    db.item_carrada.carrada.writable = False

    db.item_carrada.projeto.readable = False
    db.item_carrada.projeto.writable = False
    

    db.item_carrada.q_pcs.readable = False
    db.item_carrada.q_pcs.writable = False

    db.item_carrada.descricao.readable = True
    db.item_carrada.descricao.writable = False

    db.item_carrada.preco_unitario.readable = True
    db.item_carrada.preco_unitario.writable = False

    db.item_carrada.quant_pcs_grt.readable = True
    db.item_carrada.quant_pcs_grt.writable = True

    db.item_carrada.quant_pcs_rtr.readable = True
    db.item_carrada.quant_pcs_rtr.writable = True

    db.item_carrada.quant_pcs_rfg.readable = True
    db.item_carrada.quant_pcs_rfg.writable = True
    empresa = db.empresa(projeto.empresa)
    
    form = SQLFORM(db.item_carrada, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('retorno', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)
