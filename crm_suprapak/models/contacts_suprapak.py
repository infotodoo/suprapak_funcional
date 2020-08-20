from odoo import models,api,fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    ticket_count = fields.Integer('Number of Tickets', compute = '_compute_tickets')
    ticket_ids = fields.One2many('helpdesk.ticket','opportunity_id','Tickets')

    def _compute_tickets(self):
        for ticket in self:
            count = len(ticket.ticket_ids)
            ticket.ticket_count = count

    def action_view_ticket(self):
        action = self.env.ref('helpdesk.helpdesk_ticket_action_main_tree').read()[0]
        action['context'] = {
            'default_partner_id': self.partner_id.id,
            'default_opportunity_id': self.id
        }
        action['domain'] = [('opportunity_id', '=', self.id)]
        return action


class TicketsCrm(models.Model):
    _inherit = 'helpdesk.ticket'

    opportunity_id = fields.Many2one('crm.lead','Opportunity')