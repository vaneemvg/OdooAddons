# python

# odoo
from odoo import models, fields, api

class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    main_seller_id = fields.Many2one('res.partner', string='Main seller', readonly=True)


    @api.model
    def _select(self):
        select = super()._select()
        select += ', main_seller.id as main_seller_id'
        return select
    
    @api.model
    def _from(self):
        frm = super()._from()
        frm += 'LEFT JOIN res_partner main_seller ON main_seller.id = template.main_seller_id'
        return frm
    
    @api.model
    def _group_by(self):
        group_by = super()._group_by()
        group_by += ', main_seller.id'
        return group_by