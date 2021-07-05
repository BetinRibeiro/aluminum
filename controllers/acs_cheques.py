# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    empresa = db.empresa(request.args(2, auth.user))
    mes=request.now
    ano=request.now
    mes=request.args(0, cast=int)
    ano=request.args(1, cast=int)
    primeira_data=datetime.date(ano, mes, 1)
    ultima_data=datetime.date(ano, mes, 1)

    if (mes==12):
        ultima_data=datetime.date(ano+1, 1, 1)
    else:
        ultima_data=datetime.date(ano, mes+1, 1)
    rows = db((db.cheque.empresa==empresa.id)&(db.cheque.data_cheque>=primeira_data)&(db.cheque.data_cheque<ultima_data)).select(orderby=db.cheque.data_cheque)
    total_cheques_pendentes = db((db.cheque.empresa==empresa.id)&(db.cheque.data_cheque<primeira_data)&(db.cheque.quitado==False)).count()
    return locals()

@auth.requires_login()
def cadastrar_cheque():
    response.view = 'generic.html'
    data=request.now
    empresa = db.empresa(request.args(0, auth.user))
    db.cheque.empresa.default = empresa.id
    db.cheque.empresa.writable = False
    form = SQLFORM(db.cheque).process()
    if form.accepted:
        #caso aceito redireciona para tela de acesso inicial
        response.flash = 'Formulario aceito'
        redirect(URL('index', args=[data.month,data.year,empresa.id]))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    #2 consultas no banco
    return  dict(form=form)

@auth.requires_login()
def alterar():
    response.view = 'generic.html' # use a generic view
    cheque = db.cheque(request.args(0, cast=int))
    empresa = db.empresa(cheque.empresa)
    data=cheque.data_cheque
    db.cheque.id.readable = False
    db.cheque.id.writable = False

    form = SQLFORM(db.cheque, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('index', args=[data.month,data.year,empresa.id]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
