from odoo import models, fields, api, _

class CrmLead(models.Model):
    _inherit = 'crm.lead'


    def send_msg_crm(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Whatsapp Message'),
                'res_model': 'whatsapp.message.wizard.crm',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_user_id': self.id},
                }