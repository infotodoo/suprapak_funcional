from odoo import models,api,fields


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    number_code = fields.Integer('Number Code')


    _sql_constraints = [
        ('name_number_code_uniq', 'unique(country_id,number_code)', 'The code of the country must be unique by country !')
    ]

class ResCountry(models.Model):
    _inherit = 'res.country'

    average_days = fields.Char('Average Transit Days')
    region = fields.Char('Region')
    sub_region = fields.Char('Sub-Region')