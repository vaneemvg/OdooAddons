from odoo import models, api, fields


class WhatsappSendMessageCrm(models.TransientModel):

    _name = 'whatsapp.message.wizard.crm'

    user_id = fields.Many2one('crm.lead', string="Recipient")
    phone = fields.Char(related='user_id.phone', required=True)
    message = fields.Text(string="message", required=True)

    def send_message_crm(self):
        if self.message and self.phone:
            message_string = ''
            message = self.message.split(' ')
            for msg in message:
                message_string = message_string + msg + '%20'
            message_string = message_string[:(len(message_string) - 3)]
            self.user_id.message_post(body='Mensaje whatsapp: '+message_string)
            return {
                'type': 'ir.actions.act_url',
                'url': "https://api.whatsapp.com/send?phone="+self.user_id.phone+"&text=" + message_string,
                'target': 'new',
                'res_id': self.id,
            }
