# -*- coding: utf-8 -*-
# from odoo import http


# class CreditSuprapak(http.Controller):
#     @http.route('/credit_suprapak/credit_suprapak/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/credit_suprapak/credit_suprapak/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('credit_suprapak.listing', {
#             'root': '/credit_suprapak/credit_suprapak',
#             'objects': http.request.env['credit_suprapak.credit_suprapak'].search([]),
#         })

#     @http.route('/credit_suprapak/credit_suprapak/objects/<model("credit_suprapak.credit_suprapak"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('credit_suprapak.object', {
#             'object': obj
#         })
