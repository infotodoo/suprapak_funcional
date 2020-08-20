from odoo import models, api, fields


class SaleSuprapak(models.Model):
    _inherit = 'sale.order'

    production_id = fields.Many2one('mrp.production', 'Production', compute='_compute_production_id')
    type_sale = fields.Selection([('nu', 'NU'), ('re', 'RE'), ('rc', 'RC'), ('r1', 'R1')], 'Tipo de pedido',
                                 compute='_compute_type_sale')
    bool_client = fields.Boolean('Customer does not Satisfated?')
    order_production_id = fields.Many2one('mrp.production', 'Production Order')

    def split(self):
        return list(self)

    def cod_vendor(self):
        cod_vendor = ''
        employee_obj = self.env['hr.employee'].search([('name','=',self.user_id.name)])
        if employee_obj :
            cod_vendor = employee_obj.identification_id
        else:
            cod_vendor = ''
        return cod_vendor

    def programing_meters(self):
        programming_meter = 0
        kronos_id = self.env['data.sheet'].search([('name', '=', self.sheet_id.name)])
        if kronos_id.uom_id.name == 'Unidades':
            if len(kronos_id.print_color_ids) > 6:
                programming = int(int(kronos_id.quantity) / kronos_id.uds_m)
                meter = int(programming/100)+1
                programming_meter = (meter * 100) + 200
            else:
                programming = int(int(kronos_id.quantity) / kronos_id.uds_m)
                meter = int(programming / 100) + 1
                programming_meter = (meter * 100) + 100
        else:
            programming_meter = 0
        return programming_meter

    def _compute_production_id(self):
        for record in self:
            mrp = record.env['mrp.production'].search([('origin', '=', record.name)], limit=1)
            record.production_id = mrp if mrp else False
            print(mrp)
    def _compute_type_sale(self):
        for record in self:
            if record.bool_client:
                record.type_sale = 'r1'
            elif self._compute_before_production():
                record.type_sale = 're'
            elif record.sheet_id and record.sheet_id.version > 1:
                record.type_sale = 'rc'
            else:
                record.type_sale = 'nu'

    def _compute_before_production(self):
        before_production = []
        for record in self:
            for lines in record.order_line:
                domain = [('product_id', '=', lines.product_id.id), ('date_planned_start', '<', record.date_order)]
                mrp_ids = record.env['mrp.production'].sudo().search(domain, order='date_planned_start', limit=1)
                for production in mrp_ids:
                    before_production.append(production.name)
        return before_production

    def _compute_before_type_sale(self):
        before_order = ''
        for record in self:
            for lines in record.order_line:
                domain = [('product_id', '=', lines.product_id.id), ('date_planned_start', '<', record.date_order)]
                mrp_ids = record.env['mrp.production'].sudo().search(domain, order='date_planned_start', limit=1)
                if mrp_ids:
                    for production in mrp_ids:
                        domain = [('name', '=', production.origin)]
                        sale_obj = record.env['sale.order'].search(domain)
                        if sale_obj:
                            before_order = sale_obj.type_sale
                        else:
                            before_order = ''
                return before_order


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    date_order = fields.Datetime('Date Order', related='order_id.date_order', store=False)

