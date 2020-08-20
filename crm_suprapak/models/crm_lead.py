# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    planned_revenue = fields.Monetary(compute='_compute_planned_revenue')
    currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.company.currency_id)
    computed_revenue = fields.Monetary('Expected Revenue', currency_field='currency_id')
    # date_currency = fields.Date('Date conversion', help="Date of conversion", default=fields.Date.today())

    api.depends('expected_revenue', 'currency_id')
    def _compute_planned_revenue(self):
        for record in self:
            planned_revenue = record.computed_revenue
            if record.currency_id and record.currency_id != record.company_currency:
                currency_id = record.currency_id
                planned_revenue = currency_id._convert(record.computed_revenue, record.company_currency, record.company_id, record.date_deadline or fields.Date.today())
            record.planned_revenue = planned_revenue
