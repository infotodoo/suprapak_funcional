# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessDenied


class ResSector(models.Model):
    _name = 'res.sector'
    _description = 'Sector of Customer'

    name = fields.Char('Sector')
    code = fields.Char('code')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sector_id = fields.Many2one('res.sector','Sector')
    sectors_ids = fields.Many2many('res.sector','partner_sector_rel','res_sector_id','sector_id','Subsector')
    bool_postobon = fields.Boolean(default = False)
    bool_avon = fields.Boolean(default=False)
    ref_1 = fields.Char('Customer Code')

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if self.city_id:
            partners = len(self.search([('city_id', '=', self.city_id.id)]))
            self.ref_1 = self.city_id.zipcode + str(partners)
            #self.zip = self.ref

    lead_time = fields.Integer('Deal Lead Time')
    tolerance_minimal = fields.Integer('% Minimal Tolerance')
    tolerance_maximun = fields.Integer('% Maximun Tolerance')
    tolerance_minimal_day = fields.Integer('Minimal Tolerance Day')
    tolerance_maximun_day = fields.Integer('Maximun Tolerance Day')
    day_billing = fields.Integer('Days Billing Cut')
    region_id = fields.Many2one('region.region','Region')
    subregion_id = fields.Many2one('subregion.region','Subregion')
    company_class_id = fields.Many2one('class.company','Company Class')
    main_product_id = fields.Many2one('main.product','Main Product')

class RegionRegion(models.Model):
    _name = 'region.region'
    _description = 'Region Region'

    code = fields.Char('Code')
    name = fields.Char('Region')


class SubregionRegion(models.Model):
    _name = 'subregion.region'
    _description = 'Subregion Region'

    code = fields.Char('Code')
    name = fields.Char('Subregion')

class ClassCompany(models.Model):
    _name = 'class.company'
    _description = 'Class Company'

    code = fields.Char('Code')
    name = fields.Char('Subregion')

class MainProduct(models.Model):
    _name = 'main.product'
    _description = 'Main Product'

    code = fields.Char('Code')
    name = fields.Char('Subregion')


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    bill_type = fields.Selection([('saving', 'Saving'),('current','Current')],'Bill Type') 