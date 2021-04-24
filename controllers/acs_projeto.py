# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    projeto = db.projeto(request.args(0, auth.user))
    empresa = db.empresa(projeto.empresa)
    usuario=auth.user
    usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user.id)
    if (usuario.id!=1)and(usuario_empresa.empresa!=projeto.empresa):
        redirect(URL('default','index'))
    if (projeto.empresa==4561):
        redirect(URL('acs_projeto_boletos','index'))
    return locals()

@auth.requires_login()
def definir_chefe():
    projeto = db.projeto(request.args(0, auth.user))
    rows = db(db.usuario_empresa.empresa==projeto.empresa).select()
    if (projeto.empresa==17):
        redirect(URL('acs_equipe','vendedores', args=projeto.id))
    return locals()

@auth.requires_login()
def definir_chefe_confirmar():
    projeto = db.projeto(request.args(0, auth.user))
    usuario = db.usuario_empresa(request.args(1, auth.user))
    projeto.auth_user=usuario.auth_user
    projeto.update_record()
    redirect(URL('definir_chefe', args=projeto.id))
    return locals()

@auth.requires_login()
def particoes():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.sub_venda.projeto == projeto.id).select()
    total_venda=0.0
    total_fichas=0
    for row in rows:
        total_venda=0.0
        total_fichas=0
        #sum = db.venda.venda_praso.sum()
        #row.venda_praso=(db(db.venda.sub_venda == row.id).select(sum).first()[sum])
        #row.update_record()
        rowsv = db(db.venda.sub_venda == row.id).select()
        for rowv in rowsv:
            total_venda+=rowv.venda_praso-rowv.valor_devolvido
            total_fichas+=rowv.quant_fichas-rowv.quant_fichas_devolvidas
        row.total_fichas=total_fichas
        row.total_venda_praso=total_venda
        row.update_record()
    return locals()

@auth.requires_login()
def adicionar_rota_cobranca():
    response.view = 'generic.html' # use a generic view
    projeto = db.projeto(request.args(0, cast=int))
    empresa = db.empresa(projeto.empresa)
    if projeto.venda_finalizada:
        session.flash = 'A venda já foi finalizada'
        redirect(URL('particoes', args=projeto.id))

    db.sub_venda.auth_user.default = 28
    db.sub_venda.projeto.default = projeto.id
    db.sub_venda.projeto.writable = False

    db.sub_venda.data_final_cobranca.readable = False
    db.sub_venda.data_final_cobranca.writable = False

    db.sub_venda.ultima_cidade.readable = False
    db.sub_venda.ultima_cidade.writable = False

    form = SQLFORM(db.sub_venda).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('particoes', args=projeto.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    return dict(form=form)

@auth.requires_login()
def alterar_dados_rota():
    response.view = 'generic.html' # use a generic view
    sub_venda = db.sub_venda(request.args(0, cast=int))
    projeto = db.projeto(sub_venda.projeto)
    
    if not sub_venda.auth_user:
        sub_venda.auth_user=28
        sub_venda.update_record()
    db.sub_venda.id.readable = False
    db.sub_venda.id.writable = False

    db.sub_venda.projeto.readable = False
    db.sub_venda.projeto.writable = False
    
    db.sub_venda.cobranca_iniciada.label = 'Venda Finalizada'
    db.sub_venda.cobranca_iniciada.readable = True
    db.sub_venda.cobranca_iniciada.writable = True

    db.sub_venda.data_final_cobranca.readable = False
    db.sub_venda.data_final_cobranca.writable = False

    db.sub_venda.ultima_cidade.readable = False
    db.sub_venda.ultima_cidade.writable = False
    deletar =True
    if sub_venda.total_venda_praso>0:
        deletar =False

    form = SQLFORM(db.sub_venda, request.args(0, cast=int), deletable=deletar)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('particoes', args=projeto.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)


@auth.requires_login()
def acesso_vendas_particao():
    sub_venda = db.sub_venda(request.args(0, cast=int))
    rows = db(db.venda.sub_venda == sub_venda.id).select(orderby=db.venda.data_venda)
    rowsdesp = db(db.despesa.projeto==sub_venda.projeto).select(orderby=db.despesa.data_inicio)
    projeto = db.projeto(sub_venda.projeto)
    #for row in rowsdesp:
      #classe_despesa = db.classe_despesa(db.classe_despesa.id==row.classe_despesa)
      #row.projeto=classe_despesa.projeto
      #row.update_record()
    return locals()

@auth.requires_login()
def prestacao_vendedor():
    projeto = db.projeto(request.args(0, cast=int))
    rows = db(db.vendedor.projeto == projeto.id).select(orderby=db.vendedor.nome)
    rowsf = db(db.funcionario.projeto == projeto.id).select(orderby=db.funcionario.nome)
    return locals()
