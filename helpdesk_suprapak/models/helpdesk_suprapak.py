from odoo import models, fields, api

class Helpdesk(models.Model):
    _inherit = 'helpdesk.ticket'


    filter = fields.Char(compute ='_compute_filter')
    complaint = fields.Selection([('product','Complaint By Product'),('service','Complaint By Service')],'Coplaint Type')
    service_id = fields.Many2one('service','PQRS by Service')
    pqrs = fields.Selection([('print','Print'),('paste','Paste'),('technic','Technic'),('cut','Cut'),('rewind','Rewind')],'PQRS by Product')
    print_id = fields.Many2one('print','Print')
    paste_id = fields.Many2one('paste','Paste')
    technic_id = fields.Many2one('technic','Technic')
    cut_id = fields.Many2one('cut','Cut')
    rewind_id = fields.Many2one('rewind','Rewind')



    def _compute_filter(self):
        if self.team_id:
            self.filter = self.team_id.name
        else:
            self.filter = None



class Print(models.Model):
    _name = 'print'
    _description = 'PSRS by Print'

    name = fields.Char('Caused by Print')
    code = fields.Char('code')


class Paste(models.Model):
    _name = 'paste'
    _description = 'PSRS by Paste'

    name = fields.Char('Caused by Paste')
    code = fields.Char('code')


class Technic(models.Model):
    _name = 'technic'
    _description = 'PSRS by Technic'

    name = fields.Char('Caused by Technic')
    code = fields.Char('code')


class Rewind(models.Model):
    _name = 'rewind'
    _description = 'PSRS by Rewind'

    name = fields.Char('Caused by Rewind')
    code = fields.Char('code')


class Cut(models.Model):
    _name = 'cut'
    _description = 'PSRS by Cut'

    name = fields.Char('Caused by Cut')
    code = fields.Char('code')


class Service(models.Model):
    _name = 'service'
    _description = 'Complaint By Service'

    name = fields.Char('Complaint By Service')
    code = fields.Char('code')


class HelpdeskTicketType(models.Model):
    _inherit = 'helpdesk.ticket.type'

    team_id = fields.Many2one('helpdesk.team', 'Helpdesk Team')
