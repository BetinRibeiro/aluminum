# -*- coding: utf-8 -*-
def index():
#     response.view = 'generic.html' # use a generic view
    empresa = db.empresa(request.args(0, cast=int))
#     lista = db(db.vendedor.id>0).select()
#     for row in lista:
#       projeto= db.projeto(db.projeto.id==row.projeto)
#       row.empresa=projeto.empresa
#       row.update_record()
#     rows = db(db.funcionario_empresa.empresa==empresa.id).select(orderby=db.funcionario_empresa.bloqueado)
    paginacao = 15
    if len(request.args) == 1:
        pagina = 1
    else:
        try:
            pagina = int(request.args[1])
        except ValueError:
            redirect(URL('erro', vars={
                  'msg':'Numero da página inválido'
                  }))
    if pagina <= 0:
        pagina = 1
    total = db(db.funcionario_empresa.empresa==empresa.id).count()
    paginas = total/paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    rows = db(db.funcionario_empresa.empresa==empresa.id).select(
      limitby=limites,orderby=db.funcionario_empresa.bloqueado|db.funcionario_empresa.nome
      )
    return  locals()
  
def cadastrar():
    response.view = 'generic.html' # use a generic view
    empresa = db.empresa(request.args(0, cast=int))

    db.funcionario_empresa.empresa.default = empresa.id
    db.funcionario_empresa.empresa.writable = False

    form = SQLFORM(db.funcionario_empresa).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('index', args=empresa.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)

def listar_projetos_vendedor():
    funcionario_empresa = db.funcionario_empresa(request.args(0, cast=int))
#     rows = db(db.vendedor.funcionario_empresa==funcionario_empresa.id).select(orderby=~db.vendedor.id)
    paginacao = 3
    if len(request.args) == 1:
        pagina = 1
    else:
        try:
            pagina = int(request.args[1])
        except ValueError:
            redirect(URL('erro', vars={
                  'msg':'Numero da página inválido'
                  }))
    if pagina <= 0:
        pagina = 1
    total = db(db.vendedor.funcionario_empresa==funcionario_empresa.id).count()
    paginas = total/paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    rows = db(db.vendedor.funcionario_empresa==funcionario_empresa.id).select(
      limitby=limites,orderby=db.vendedor.projeto
      )
    return  locals()
def alterar():
#     try:
    response.view = 'generic.html' # use a generic view
    request.function='Alterar Funcionario'
    funcionario_empresa= db.funcionario_empresa(request.args(0, cast=int))
    if auth.user.id==1:
        db.funcionario_empresa.empresa.label="(Empresa) # Programador"
        db.funcionario_empresa.empresa.writable=True
        db.funcionario_empresa.empresa.readable=True
    form = SQLFORM(db.funcionario_empresa, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Dados atualizado'
        redirect(URL('index', args=funcionario_empresa.empresa))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)
  
  
def vincular_vendedor():
    response.view = 'generic.html' # use a generic view
    funcionario_empresa = db.funcionario_empresa(request.args(0, cast=int))

    db.funcionario_vendedor.empresa.default = funcionario_empresa.empresa
    db.funcionario_vendedor.empresa.writable = False

    db.funcionario_vendedor.funcionario_empresa.default = funcionario_empresa.id
    db.funcionario_vendedor.funcionario_empresa.writable = False

    db.funcionario_vendedor.vendedor.requires = IS_IN_DB(db((db.vendedor.empresa == funcionario_empresa.empresa)&(db.vendedor.funcionario_empresa == None)), 'vendedor.id', '%(nome)s')
    db.funcionario_vendedor.vendedor.writable=True
    form = SQLFORM(db.funcionario_vendedor).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('index', args=funcionario_empresa.empresa))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)
def alterar_estatus():
    funcionario_empresa = db.funcionario_empresa(request.args(0, cast=int))
    if funcionario_empresa.bloqueado==True:
      funcionario_empresa.bloqueado=False
    else:
      funcionario_empresa.bloqueado=True
    funcionario_empresa.update_record()
    return redirect(URL('index', args=funcionario_empresa.empresa))
