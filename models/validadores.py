# -*- coding: utf-8 -*-

db.usuario_empresa.tipo.requires = IS_IN_SET(['Chefe','Cobrador','Administrador','Proprietário'])


db.cobrador.tipo.requires = IS_IN_SET(['Chefe','Ajudante'])
db.cobrador.tipo_comissao.requires = IS_IN_SET(['Geral','Especifica'])
