from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    main_seller_id = fields.Many2one(
        'res.partner',
        compute='_compute_main_seller',
        store=True,
        index=True,
        string='Main seller',
    )

    @api.depends('seller_ids','sequence')
    def _compute_main_seller(self):
        company_id = 2 #empresa tienda
        for rec in self:
            if not rec.seller_ids:
                rec.main_seller_id = False
                continue
            filtered_seller_ids = [seller for seller in rec.seller_ids if seller.company_id.id != company_id]
            sellers = sorted(filtered_seller_ids, key=lambda seller: seller.sequence)
            # sellers = rec.seller_ids.sorted()
            if not sellers:
                rec.main_seller_id = False
                continue
            rec.main_seller_id = sellers[0].name.id

            rec.write({'main_seller_id': rec.main_seller_id})
