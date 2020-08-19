# -*- coding: utf-8 -*-
# tente algo como
def index():
    usuario=auth.user
    sub_venda = db.sub_venda(request.args(0, auth.user))
    tipo = request.args(1, auth.user)
    dataontem=datetime.date(request.now.year, request.now.month, request.now.day)
    if (dataontem.day>2):
        dataontem=datetime.date(dataontem.year, dataontem.month, dataontem.day-2)
    else:dataontem=datetime.date(dataontem.year, dataontem.month-1, 27)
    rows = db((db.registro_cobranca.sub_venda==sub_venda.id)&(db.registro_cobranca.tipo==tipo)).select(orderby=db.registro_cobranca.data_inicio)
    consul=(request.args(2))
    if consul:
        consul= "entrou no if"
        #consulta = request.args(2, auth.user)
        rows = db((db.registro_cobranca.sub_venda==sub_venda.id)&(db.registro_cobranca.tipo==tipo)&(db.registro_cobranca.descricao.contains(request.args(2)))).select(orderby=db.registro_cobranca.data_inicio)
    return locals()


@auth.requires_login()
def inserir_registro():
    response.view = 'generic.html' # use a generic view
    sub_venda = db.sub_venda(request.args(0, auth.user))
    projeto = db.projeto(sub_venda.projeto)
    tipo = request.args(1, auth.user)
    db.registro_cobranca.sub_venda.default = sub_venda.id
    db.registro_cobranca.sub_venda.writable = False

    db.registro_cobranca.projeto.default = sub_venda.projeto
    db.registro_cobranca.projeto.writable = False

    db.registro_cobranca.tipo.default = tipo
    db.registro_cobranca.tipo.writable = False

    db.registro_cobranca.descricao.default = tipo

    form = SQLFORM(db.registro_cobranca).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('index', args=[sub_venda.id,tipo]))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)

@auth.requires_login()
def alterar_registro():
    usuario=auth.user
    response.view = 'generic.html' # use a generic view
    registro_cobranca = db.registro_cobranca(request.args(0, cast=int))
    tipo = request.args(1)
    sub_venda = db.sub_venda(registro_cobranca.sub_venda)

    db.registro_cobranca.id.readable = False
    db.registro_cobranca.id.writable = False

    db.registro_cobranca.sub_venda.readable = False
    db.registro_cobranca.sub_venda.writable = False

    db.registro_cobranca.projeto.readable = False
    db.registro_cobranca.projeto.writable = False

    db.registro_cobranca.tipo.readable = False
    db.registro_cobranca.tipo.writable = False
    
    if (registro_cobranca.tipo=="Deposito") and (usuario.id!=sub_venda.auth_user):

        db.registro_cobranca.observacao.readable = True
        db.registro_cobranca.observacao.writable = True
        

    form = SQLFORM(db.registro_cobranca, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('index', args=[registro_cobranca.sub_venda,tipo]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
