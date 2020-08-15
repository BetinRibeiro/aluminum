# -*- coding: utf-8 -*-
@auth.requires_membership('admin')
def index():
    empresa = db.empresa(db.empresa.auth_user==auth.user.id)
    usuario=auth.user
    if (auth.user.id==6):
        empresa = db.empresa(4)
        #empresa.id
        redirect(URL('usuario','fsprojetos',args=empresa.id))
    #caso seja hiago vai listar todos os projetos da empresa fs
    if (auth.user.id==11)or(auth.user.id==10):
        empresa = db.empresa(8)
        #empresa.id
        redirect(URL('usuario','fsprojetos',args=empresa.id))
    if auth.user.id==10:
        empresa = db.empresa(8)
        redirect(URL('usuario','fsprojetos',args=empresa.id))
    #caso não tenha nem uma empresa o usuario pode estar vinculado a
    #algum projeto ou sub venda pode ser (chefe ou cobrador)
    if not empresa:
        #redireciona para pagina de usuario)
        redirect(URL('acesso_inicial_usuario'))
    #caso contrario procegue, busca todos os projetos da empresa
    rows = db(db.projeto.empresa==empresa.id).select()
    if request.args(0, auth.user)=="235":
        rows = db(db.projeto.empresa).select(orderby=db.empresa)
    #2 consultas no banco
    return locals()
