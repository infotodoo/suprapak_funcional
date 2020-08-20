# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TypeOfFailure(models.Model):
    _name = 'type.of.failure'
    _description = 'model for the types of failures'

    name = fields.Char("Name")
    maintenance_equipment_id = fields.Many2one('maintenance.equipment', string="Equipment")

class ResponsableTechnic(models.Model):
    _name = 'responsable.technic'
    _description = 'model contains the responsable Technic'

    name = fields.Char("Name",required=True)

    email = fields.Char('Email',required=True)

    document = fields.Char('Document',required=True)


class MaintenanceReques(models.Model):
    _inherit = 'maintenance.request'

    failure_id = fields.Many2one('type.of.failure',string="Type of failure")
    
    responsable_technic_id = fields.Many2one('responsable.technic','Technic')
