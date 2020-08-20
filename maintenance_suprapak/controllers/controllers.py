# -*- coding: utf-8 -*-
# from odoo import http


# class MaintenanceSuprapak(http.Controller):
#     @http.route('/maintenance_suprapak/maintenance_suprapak/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/maintenance_suprapak/maintenance_suprapak/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('maintenance_suprapak.listing', {
#             'root': '/maintenance_suprapak/maintenance_suprapak',
#             'objects': http.request.env['maintenance_suprapak.maintenance_suprapak'].search([]),
#         })

#     @http.route('/maintenance_suprapak/maintenance_suprapak/objects/<model("maintenance_suprapak.maintenance_suprapak"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('maintenance_suprapak.object', {
#             'object': obj
#         })
