# -*- coding: utf-8 -*-
def usuario_bloqueado():
  response.view = 'generic.html' # use a generic view
  return dict(message=request.args(0, cast=str).replace("_"," "))
