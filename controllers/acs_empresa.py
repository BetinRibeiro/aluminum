# -*- coding: utf-8 -*-
@auth.requires_login()
def projecao_simulada():
  usuario_empresa = db.usuario_empresa(db.usuario_empresa.auth_user==auth.user.id)
  if usuario_empresa:
    empresa = db.empresa(usuario_empresa.empresa)
    simulacao = db.simulacao(db.simulacao.empresa==empresa.id)
    if not simulacao:
      db.simulacao.update_or_insert(db.simulacao.empresa == empresa.id,
                                    empresa = empresa.id,
                                    descricao=empresa.nome)
  else:
    redirect(URL('default','index'))
    if (auth.user.id==1)&(request.args(0, cast=int)):
      empresa = db.empresa(request.args(0, cast=int))
      simulacao = db.simulacao(db.simulacao.empresa==empresa.id)
  return dict(simulacao=simulacao)


def alterar_simulacao():
  response.view = 'generic.html' # use a generic view
  simulacao = db.simulacao(request.args(0, cast=int))
  db.simulacao.id.readable = False
  db.simulacao.id.writable = False
  form = SQLFORM(db.simulacao, request.args(0, cast=int))
  if form.process().accepted:
      session.flash = 'Atualizado'
      redirect(URL('projecao_simulada', args=simulacao.empresa))
  elif form.errors:
      response.flash = 'Erros no formulário!'
  return  dict(form=form)


def mensagem():
  response.view = 'generic.html' # use a generic view
  mensagem = "Seu servidor de acesso e armazenamento da empresa não foi pago, entre em contato com seu provedor de serviço, para regularizar o débito. desde já agradecemos a compreenção!"
  return dict(mensagem=mensagem)
