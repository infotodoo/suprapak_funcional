# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    sheet_id = fields.Many2one('data.sheet', 'Sheet')
