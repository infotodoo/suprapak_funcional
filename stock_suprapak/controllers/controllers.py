# -*- coding: utf-8 -*-
# from odoo import http


# class SuprapakStock(http.Controller):
#     @http.route('/stock_suprapak/stock_suprapak/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_suprapak/stock_suprapak/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_suprapak.listing', {
#             'root': '/stock_suprapak/stock_suprapak',
#             'objects': http.request.env['stock_suprapak.stock_suprapak'].search([]),
#         })

#     @http.route('/stock_suprapak/stock_suprapak/objects/<model("stock_suprapak.stock_suprapak"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_suprapak.object', {
#             'object': obj
#         })
