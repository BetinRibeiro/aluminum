# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    usuario=auth.user
    projeto = db.projeto(request.args(0, cast=int))
    tipo= (request.args(1))
    rows = db((db.classe_despesa.projeto == projeto.id) & (db.classe_despesa.tipo == tipo)).select()
    tipodesp=(request.args(1, auth.user))
    return locals()
  
def mudar_classe():
    response.view = 'generic.html' # use a generic view
    classe_despesa = db.classe_despesa(request.args(0, cast=int))
    classe_despesa.projeto=80
    classe_despesa.update_record()
    redirect(URL('index', args=[classe_despesa.projeto,"Despesa_Venda"]))
    return locals()
@auth.requires_login()
def criar_classe_despesa():
    response.view = 'generic.html' # use a generic view
    projeto = db.projeto(request.args(0, auth.user))
    tipodesp=(request.args(1))
    
    db.classe_despesa.projeto.default = projeto.id
    db.classe_despesa.projeto.writable = False
    
    db.classe_despesa.tipo.default  = tipodesp
    
    db.classe_despesa.tipo.writable = False
    usuario = auth.user
    if usuario.id==2544:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('index', args=[projeto.id,tipodesp]))

    form = SQLFORM(db.classe_despesa).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('index', args=[projeto.id,tipodesp]))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return  dict(form=form)
@auth.requires_login()
def alterar_classe_despesa():
    response.view = 'generic.html' # use a generic view
    classe_despesa = db.classe_despesa(request.args(0, cast=int))
    tipodesp=(request.args(1, auth.user))
    projeto = db.projeto(classe_despesa.projeto)
    db.classe_despesa.id.readable = False
    db.classe_despesa.id.writable = False
    
    db.classe_despesa.projeto.readable = False
    db.classe_despesa.projeto.writable = False
    
    db.classe_despesa.tipo.readable = False
    db.classe_despesa.tipo.writable = False

    usuario = auth.user
    if usuario.id==25434:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('index', args=[projeto.id,tipodesp]))

    form = SQLFORM(db.classe_despesa, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('index', args=[projeto.id,tipodesp]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)


@auth.requires_login()
def acesso_despesa():
    classe_despesa = db.classe_despesa(request.args(0, cast=int))
    projeto = db.projeto(classe_despesa.projeto)
    tipodesp=(request.args(1, auth.user))
    rows = db(db.despesa.classe_despesa == request.args(0, cast=int)).select(orderby=db.despesa.data_inicio)
    return locals()

@auth.requires_login()
def criar_desp():
    response.view = 'generic.html' # use a generic view
    classe_despesa = db.classe_despesa(request.args(0, auth.user))
    tipodesp=(request.args(1, auth.user))
    variavel=0
    variavel=request.args(2, auth.user)
    if variavel>=1:
        newdespesa = db(db.despesa.classe_despesa== classe_despesa.id).select().last()
        db.despesa.insert(classe_despesa=classe_despesa.id, data_inicio=request.now , descricao=newdespesa.descricao , valor=newdespesa.valor)
        return redirect(URL('acesso_despesa', args=[classe_despesa.id,tipodesp]))
    
    usuario = auth.user
    if usuario.id==2344:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('acesso_despesa', args=[classe_despesa.id,tipodesp]))

    db.despesa.classe_despesa.default = classe_despesa.id
    db.despesa.classe_despesa.writable = False

    form = SQLFORM(db.despesa).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acesso_despesa', args=[classe_despesa.id,tipodesp]))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)
@auth.requires_login()
def alterar_desp():
    response.view = 'generic.html' # use a generic view
    despesa = db.despesa(request.args(0, cast=int))
    classe_despesa = db.classe_despesa(despesa.classe_despesa)
    tipodesp=(request.args(1, auth.user))
    
    db.despesa.id.readable = False
    db.despesa.id.writable = False
    
    db.despesa.classe_despesa.readable = False
    db.despesa.classe_despesa.writable = False
    
    usuario = auth.user
    if usuario.id==2344:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('acesso_despesa', args=[classe_despesa.id,tipodesp]))
    form = SQLFORM(db.despesa, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acesso_despesa', args=[classe_despesa.id,tipodesp]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
@auth.requires_login()
def relatorio_despesa():
    projeto = db.projeto(request.args(0, cast=int))
    return locals()
@auth.requires_login()
def acessar_despesa_local():
    classe_despesa_local = db.classe_despesa_local(request.args(0, cast=int))
    empresa = db.empresa(classe_despesa_local.empresa)
    rows = db(db.despesa_local.classe_despesa_local == request.args(0, cast=int)).select(orderby=db.despesa_local.data_inicio)
    return locals()
@auth.requires_login()
def criar_classe_despesa_local():
    response.view = 'generic.html' # use a generic view
    empresa = db.empresa(request.args(0, cast=int))
    
    db.classe_despesa_local.empresa.default = empresa.id
    db.classe_despesa_local.empresa.writable = False

    form = SQLFORM(db.classe_despesa_local).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('usuario','fsprojetos', args=[empresa.id]))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return  dict(form=form)

@auth.requires_login()
def alterar_classe_despesa_local():
    response.view = 'generic.html' # use a generic view
    classe_despesa_local = db.classe_despesa_local(request.args(0, cast=int))
    empresa = db.empresa(classe_despesa_local.empresa)
    db.classe_despesa_local.id.readable = False
    db.classe_despesa_local.id.writable = False
    
    db.classe_despesa_local.empresa.readable = False
    db.classe_despesa_local.empresa.writable = False

    form = SQLFORM(db.classe_despesa_local, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('usuario','fsprojetos', args=[empresa.id]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

@auth.requires_login()
def criar_desp_local():
    response.view = 'generic.html' # use a generic view
    classe_despesa_local = db.classe_despesa_local(request.args(0, auth.user))
    
    db.despesa_local.classe_despesa_local.default = classe_despesa_local.id
    db.despesa_local.classe_despesa_local.writable = False

    form = SQLFORM(db.despesa_local).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acessar_despesa_local', args=[classe_despesa_local.id]))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)

@auth.requires_login()
def alterar_desp_local():
    response.view = 'generic.html' # use a generic view
    despesa_local = db.despesa_local(request.args(0, cast=int))
    
    db.despesa_local.id.readable = False
    db.despesa_local.id.writable = False
    
    db.despesa_local.classe_despesa_local.readable = False
    db.despesa_local.classe_despesa_local.writable = False

    form = SQLFORM(db.despesa_local, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acessar_despesa_local', args=[despesa_local.classe_despesa_local]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
