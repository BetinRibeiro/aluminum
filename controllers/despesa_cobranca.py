# -*- coding: utf-8 -*-
@auth.requires_login()
def acessar_despesa():
    sub_venda = db.sub_venda(request.args(0, cast=int))
    rows = db((db.classe_despesa_cobranca.sub_venda == sub_venda.id)).select()
    return locals()
@auth.requires_login()
def criar_class_desp():
    response.view = 'generic.html' # use a generic view
    sub_venda = db.sub_venda(request.args(0, cast=int))
    db.classe_despesa_cobranca.sub_venda.default = sub_venda.id
    db.classe_despesa_cobranca.sub_venda.writable = False
    form = SQLFORM(db.classe_despesa_cobranca).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acessar_despesa', args=[sub_venda.id]))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)
@auth.requires_login()
def alterar_class_desp():
    response.view = 'generic.html' # use a generic view
    classe_despesa_cobranca = db.classe_despesa_cobranca(request.args(0, cast=int))

    sub_venda = db.sub_venda(classe_despesa_cobranca.sub_venda)
    db.classe_despesa_cobranca.id.readable = False
    db.classe_despesa_cobranca.id.writable = False

    db.classe_despesa_cobranca.sub_venda.readable = False
    db.classe_despesa_cobranca.sub_venda.writable = False

    form = SQLFORM(db.classe_despesa_cobranca, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acessar_despesa', args=[sub_venda.id]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

@auth.requires_login()
def acesso_despesa():
    classe_despesa_cobranca = db.classe_despesa_cobranca(request.args(0, cast=int))
    sub_venda = db.sub_venda(classe_despesa_cobranca.sub_venda)
    rows = db(db.despesa_cobranca.classe_despesa_cobranca == classe_despesa_cobranca.id).select(orderby=db.despesa_cobranca.data_inicio)
    return locals()

@auth.requires_login()
def criar_desp():
    response.view = 'generic.html' # use a generic view
    classe_despesa_cobranca = db.classe_despesa_cobranca(request.args(0, auth.user))
    variavel=0
    variavel=request.args(1, auth.user)
    if variavel>=1:
        response.flash = 'Entrou no if'
        newdespesa = db(db.despesa_cobranca.classe_despesa_cobranca == classe_despesa_cobranca.id).select().last()
        db.despesa_cobranca.insert(classe_despesa_cobranca=classe_despesa_cobranca.id, data_inicio=request.now , descricao=newdespesa.descricao , valor=newdespesa.valor)
        return redirect(URL('acesso_despesa', args=[classe_despesa_cobranca.id]))

    db.despesa_cobranca.classe_despesa_cobranca.default = classe_despesa_cobranca.id
    db.despesa_cobranca.classe_despesa_cobranca.writable = False

    form = SQLFORM(db.despesa_cobranca).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acesso_despesa', args=[classe_despesa_cobranca.id]))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)
@auth.requires_login()
def alterar_desp():

    response.view = 'generic.html' # use a generic view
    despesa_cobranca = db.despesa_cobranca(request.args(0, cast=int))
    try:
      classe_despesa_cobranca = db.classe_despesa_cobranca(despesa_cobranca.classe_despesa_cobranca)

      db.despesa_cobranca.id.readable = False
      db.despesa_cobranca.id.writable = False

      db.despesa_cobranca.classe_despesa_cobranca.readable = False
      db.despesa_cobranca.classe_despesa_cobranca.writable = False

      form = SQLFORM(db.despesa_cobranca, request.args(0, cast=int), deletable=True)
      if form.process().accepted:
          session.flash = 'Atualizado'
          redirect(URL('acesso_despesa', args=[classe_despesa_cobranca.id]))
      elif form.errors:
          response.flash = 'Erros no formulário!'
      else:
          if not response.flash:
              response.flash = 'Preencha o formulário!'
    except:
        redirect(URL('acesso_despesa', args=classe_despesa_cobranca.id))
    return dict(form=form)
