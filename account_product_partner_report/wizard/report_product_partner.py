from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPartnerReport(models.TransientModel):
    _name = "product.partner.report"
    _description = "Product Partner Report"


    def get_domain_sellers(self):
        ids = [template.main_seller_id.id for template in  self.env['product.template'].search([('main_seller_id', '!=', False)]) ]
        return [('id', 'in', list(set(ids)))]
    
    seller_ids = fields.Many2many(comodel_name="res.partner", string="Sellers")
    main_seller_ids = fields.Many2many(comodel_name="res.partner", string="Main sellers", domain=get_domain_sellers, relation='product_main_seller_report_client_rel')
    date_start = fields.Date('Date start')
    date_end = fields.Date('Date end')
    show_rectifying = fields.Boolean('Show invoice rectifying', default=False)
    client_ids = fields.Many2many(comodel_name='res.partner', string='Clients', relation='product_partner_report_client_rel')
    company_ids = fields.Many2many(comodel_name='res.company', string='Companies', default=lambda self: [(6, 0, [self.env.company.id])] )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        return res

    def _print_report(self, report_type):
        self.ensure_one()
        if not (
                self.date_start
                or self.date_end
        ):
            raise ValidationError(
                _(
                    "You must set dates."
                )
            )

        if report_type == "xlsx":
            report_name = "account_product_partner_report." "action_report_product_partner_invoice_xls"
        else:
            report_name = "account_product_partner_report." "action_report_product_partner_invoice"
        return self.env.ref(
            report_name
        ).report_action(self)

    def get_item_to_print(self):
        self.ensure_one()

        type = ['out_invoice']
        if self.show_rectifying:
            type = ['out_invoice', 'out_refund']

        query_arg = (self.date_end, self.date_start, type)

        query = """
                    SELECT
                        rps.name as seller,  aml.date, rp.display_name as client, rp.id as client_id, rp.street, 
                        pt.name as product,  aml.quantity, pp.id product_id, am.ref as reference,
                        rp.city, rp.zip, cp.name as commercial, rp.street2, aml.company_id, rc.name as company,
                        (SELECT pc.name FROM res_partner_category pc 
                        JOIN res_partner_res_partner_category_rel pcr ON pcr.category_id = pc.id
                        WHERE pcr.partner_id = aml.partner_id LIMIT 1) as type, 
                        CASE WHEN am.type = 'out_refund' THEN -1 * aml.price_total ELSE aml.price_total END as price_total, 
                        am.type as type_invoice, am.invoice_origin origin, am.name as move_name 
                    FROM
                        account_move_line AS aml
                    JOIN account_move AS am ON am.id = aml.move_id
                    JOIN product_product AS pp ON pp.id = aml.product_id
                    JOIN product_template AS pt ON pt.id = pp.product_tmpl_id
                    JOIN res_company as rc ON rc.id = aml.company_id
                    LEFT JOIN res_partner AS rps ON rps.id = pt.main_seller_id
                    LEFT JOIN res_partner AS rp ON rp.id = am.partner_id
                    LEFT JOIN res_users AS us ON us.id = rp.user_id
                    LEFT JOIN res_partner AS cp ON cp.id = us.partner_id
                    
                    WHERE
                        (aml.parent_state = 'posted')
                    AND (aml.date IS NULL OR aml.date<=%s)
                    AND (aml.date IS NULL OR aml.date>=%s)
                    AND (am.type = any(%s))
                """

        if self.seller_ids:
            query += " AND (pt.main_seller_id IN (%s))"
            query_arg += (self.seller_ids.id,)

        if self.client_ids:
            query += " AND (rp.id IN %s)"
            query_arg += (tuple(self.client_ids.ids), )


        if self.company_ids:
            query += " AND (aml.company_id IN %s)"
            query_arg += (tuple(self.company_ids.ids), )

        if self.main_seller_ids:
            query += " AND (pt.main_seller_id IN (%s))"
            query_arg += (self.main_seller_ids.id,)

    
        query += " ORDER BY aml.date"

        self._cr.execute(query, query_arg)
        results = []
        for data in self._cr.dictfetchall():
            results.append(data)

        return results

    # def print_report_xls(self):
    #     report = ProductPartnerReportXlsx()
    #     report.generate_xlsx_report()

    def button_export_pdf(self):
        self.ensure_one()
        report_type = "qweb-pdf"
        return self._export(report_type)

    def button_export_xlsx(self):
        self.ensure_one()
        report_type = "xlsx"
        return self._export(report_type)

    def _export(self, report_type):
        """Default export is PDF."""
        return self._print_report(report_type)
