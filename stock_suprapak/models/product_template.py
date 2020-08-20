# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit  = 'product.template'

    def _get_default_weight_gross_uom(self):
        return self._get_weight_uom_name_from_ir_config_parameter()

    @api.depends('product_variant_ids', 'product_variant_ids.weight_gross')
    def _compute_weight_gross(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.weight_gross = template.product_variant_ids.weight_gross
        for template in (self - unique_variants):
            template.weight_gross = 0.0
    
    def _set_weight_gross(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.weight_gross = template.weight_gross

    def _compute_weight_gross_uom_name(self):
        for template in self:
            template.weight_gross_uom_name = self._get_weight_uom_name_from_ir_config_parameter()

    x_currency_id = fields.Many2one('res.currency', 'Currency')
    customer_reference = fields.Char('Customer Reference')
    date_version = fields.Date('Date Version')
    class_print = fields.Char('Class of Print')
    presentation = fields.Char('Presentation')
    type_selle = fields.Char('Type of Sealed')
    tipo_producto = fields.Selection([('terminado','Producto terminado'),('materia','Materia Prima')],'Tipo de Producto')
    weight = fields.Float(string='Net Weight')
    weight_gross = fields.Float(string='Gross Weight', compute='_compute_weight_gross', digits='Stock Weight', inverse='_set_weight_gross', store=True)
    weight_gross_uom_name = fields.Char(string='Weight unit of measure label', compute='_compute_weight_gross_uom_name', readonly=True, default=_get_default_weight_gross_uom)

class ProductProduct(models.Model):
    _inherit  = 'product.product'

    x_currency_id = fields.Many2one('res.currency', 'Currency')
    customer_reference = fields.Char('Customer Reference')
    date_version = fields.Date('Date Version')
    class_print = fields.Char('Class of Print')
    presentation = fields.Char('Presentation')
    type_selle = fields.Char('Type of Sealed')
    tipo_producto = fields.Selection([('terminado','Producto terminado'),('materia','Materia Prima')],'Tipo de Producto')
    weight = fields.Float(string='Net Weight')
    weight_gross = fields.Float(string='Gross Weight', digits='Stock Weight')
