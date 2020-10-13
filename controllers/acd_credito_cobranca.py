# -*- coding: utf-8 -*-
def index():
    projeto = db.projeto(request.args(0, cast=int))
    
    rows = db((db.boleto_atrasado.projeto == request.args(0, cast=int))&(db.boleto_atrasado.status == 'OVERDUE')).select(orderby=db.boleto_atrasado.due_date)
    #grid = SQLFORM.smartgrid(db.boleto)
    return dict(rows=rows)
