# -*- coding: utf-8 -*-

@auth.requires_login()
def acesso_equipe():
    projeto = db.projeto(request.args(0, cast=int))
    usuario = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user)
    if usuario.bloqueado==True:
      redirect(URL('acs_mensagem','usuario_bloqueado',args="Usuario Temporariamente Bloqueado!"))
    if usuario.empresa!=projeto.empresa:
      usuario.bloqueado=True
      usuario.nome="Bloqueio (tentou acessar outro projeto, equipe_venda/acesso_equipe)"
      usuario.update_record()
      redirect(URL('acs_mensagem','usuario_bloqueado',args="Usuario Temporariamente Bloqueado!"))
    rows = db(db.vendedor.projeto == projeto.id).select(orderby=~db.vendedor.total_vendas)
    return locals()
@auth.requires_login()
def acesso_venda():
    usuario = auth.user
    vendedor = db.vendedor(request.args(0, cast=int))
    projeto = db.projeto(vendedor.projeto)
    usuario = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user)
    if usuario.bloqueado==True:
      redirect(URL('acs_mensagem','usuario_bloqueado',args="Usuario Temporariamente Bloqueado!"))
    if usuario.empresa!=projeto.empresa:
      usuario.bloqueado=True
      usuario.nome="Bloqueio (tentou acessar outro projeto, equipe_venda/acesso_equipe)"
      usuario.update_record()
      redirect(URL('acs_mensagem','usuario_bloqueado',args="Usuario Temporariamente Bloqueado!"))
    rows_sub = db(db.sub_venda.projeto == vendedor.projeto).select(orderby=db.sub_venda.data_inicio_cobranca)
    rows_vend = db(db.venda.vendedor == request.args(0, cast=int)).select(orderby=db.venda.sub_venda|db.venda.data_venda)
    return locals()
  
##funções de julguei desnecessarias pra o chefe da equipe
#irei descontinuar
@auth.requires_login()
def criar_vendedor():
    response.view = 'generic.html' # use a generic view
    projeto = db.projeto(request.args(0, auth.user))

    db.vendedor.projeto.default = projeto.id
    db.vendedor.projeto.writable = False

    form = SQLFORM(db.vendedor).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acesso_equipe', args=projeto.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)

@auth.requires_login()
def alterar_vendedor():
    response.view = 'generic.html' # use a generic view
    vendedor = db.vendedor(request.args(0, cast=int))
    projeto = db.projeto(vendedor.projeto)
    if 'cfrd' in vendedor.nome:
      redirect(URL('acesso_equipe', args=projeto.id))
    db.vendedor.id.readable = False
    db.vendedor.id.writable = False

    db.vendedor.projeto.readable = False
    db.vendedor.projeto.writable = False
    deletar=True
    if vendedor.total_vendas>0:
        deletar=False
        

    usuario = auth.user
    if usuario.id==2234:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('acesso_equipe', args=projeto.id))
    form = SQLFORM(db.vendedor, request.args(0, cast=int), deletable=deletar)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acesso_equipe', args=projeto.id))
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
    
    db.venda.vendedor.default = vendedor.id
    db.venda.vendedor.writable = False
    
    
    usuario = auth.user
    if usuario.id==243344:
        session.flash = 'Essa informação deve ser mantida pelo chefe de equipe'
        redirect(URL('acesso_venda', args=vendedor.id))
    form = SQLFORM(db.venda).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('acesso_venda', args=vendedor.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return dict(form=form)

@auth.requires_login()
def alterar_venda():
    response.view = 'generic.html' # use a generic view
    venda = db.venda(request.args(0, cast=int))
    vendedor =  db.vendedor(venda.vendedor)
    projeto =  db.projeto(vendedor.projeto)
    descricao =str(venda.descricao_devolucao)
    valor =(venda.venda_praso)
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
        redirect(URL('acesso_venda', args=vendedor.id))
    #CASO NÃO SEJA O CHEFE DE EQUIPE NÃO PODERÁ ALTERAR A OBSERVAÇÃO
    if (usuario.id!=projeto.auth_user) and(usuario.id!=1):
      db.venda.descricao_devolucao.readable = True
      db.venda.descricao_devolucao.writable = False

    form = SQLFORM(db.venda, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        #CASO NÃO SEJA O CHEFE DE EQUIPE IRÁ SALVAR O LOG DE ALTERAÇÃO COM O VALOR ANTERIOR
        if (usuario.id!=1):
          venda = db.venda(request.args(0, cast=int))
          #descricao = str(descricao)+" "+str(auth.user.id)+"-A-"+str(venda.data_venda)+"V"+str(valor)
          #venda.descricao_devolucao=descricao
          #venda.update_record()
        redirect(URL('acesso_venda', args=vendedor.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

@auth.requires_login()
def conferir():
  response.view = 'generic.html' # use a generic view
  vendedor = db.vendedor(request.args(0, cast=int))
  a=False
  if 'cfrd' in vendedor.nome:
    a=True
    vendedor.nome=vendedor.nome.replace('cfrd','')
  else:
    vendedor.nome=vendedor.nome+'cfrd'
  vendedor.update_record()
  redirect(URL('acesso_equipe', args=[vendedor.projeto,a]))
  return locals()
