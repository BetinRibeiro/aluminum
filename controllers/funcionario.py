# -*- coding: utf-8 -*-

@auth.requires_login()
def conferir():
  response.view = 'generic.html' # use a generic view
  funcionario = db.funcionario(request.args(0, cast=int))
  a=False
  if 'cfrd' in funcionario.nome:
    a=True
    funcionario.nome=funcionario.nome.replace('cfrd','')
  else:
    funcionario.nome=funcionario.nome+'cfrd'
  funcionario.update_record()
  redirect(URL('acesso_funcionario', args=[funcionario.projeto,a]))
  return locals()
@auth.requires_login()
def acesso_funcionario():
    usuario=auth.user
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.funcionario.projeto == request.args(0, cast=int)).select(orderby=~db.funcionario.vale_saida)
    return locals()
@auth.requires_login()
def criar_funcionario():
    response.view = 'generic.html' # use a generic view
    projeto = db.projeto(request.args(0, auth.user))

    db.funcionario.projeto.default = projeto.id
    db.funcionario.projeto.writable = False

    form = SQLFORM(db.funcionario).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acesso_funcionario', args=projeto.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)
@auth.requires_login()
def alterar_funcionario():
    response.view = 'generic.html' # use a generic view
    funcionario = db.funcionario(request.args(0, cast=int))
    projeto = db.projeto(funcionario.projeto)
    if 'cfrd' in funcionario.nome:
      redirect(URL('acesso_funcionario', args=projeto.id))
    db.funcionario.id.readable = False
    db.funcionario.id.writable = False
    
    db.funcionario.projeto.readable = False
    db.funcionario.projeto.writable = False

    usuario = auth.user
    
    form = SQLFORM(db.funcionario, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acesso_funcionario', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
@auth.requires_login()
def acesso_vales():
    funcionario = db.funcionario(request.args(0, cast=int))
    rows = db(db.vale_funcionario.funcionario == request.args(0, cast=int)).select(orderby=~db.vale_funcionario.data_vale)
    return locals()

@auth.requires_login()
def inserir_vale():
    response.view = 'generic.html' # use a generic view
    funcionario = db.funcionario(request.args(0, auth.user))

    db.vale_funcionario.funcionario.default = funcionario.id
    db.vale_funcionario.funcionario.writable = False

    usuario = auth.user
    if usuario.id==24:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('acesso_vales', args=funcionario.id))
    form = SQLFORM(db.vale_funcionario).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acesso_vales', args=funcionario.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)

@auth.requires_login()
def alterar_vale():
    response.view = 'generic.html' # use a generic view
    vale_funcionario = db.vale_funcionario(request.args(0, cast=int))
    funcionario = db.funcionario(vale_funcionario.funcionario)
    db.vale_funcionario.id.readable = False
    db.vale_funcionario.id.writable = False

    db.vale_funcionario.funcionario.readable = False
    db.vale_funcionario.funcionario.writable = False

    usuario = auth.user
    if usuario.id==24:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('acesso_vales', args=funcionario.id))
    form = SQLFORM(db.vale_funcionario, request.args(0, cast=int))
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acesso_vales', args=funcionario.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
