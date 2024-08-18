from odoo import models


class ProductPartnerReportXlsx(models.AbstractModel):
    _name = 'report.account_product_partner_report.product_invoice_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        items = lines.get_item_to_print()
        format1 = workbook.add_format({'font_size':10,'align':'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 9})
        sheet = workbook.add_worksheet('report')
        f=0
        sheet.write(f, 0, 'Proveedor', format1)
        sheet.write(f, 1, 'Cliente', format1)
        sheet.write(f, 2, 'Fecha_DDMMYY', format1)
        sheet.write(f, 3, 'CodInt_PDV', format1)
        sheet.write(f, 4, 'NombrePDV', format1)
        sheet.write(f, 5, 'Direccion', format1)
        sheet.write(f, 6, 'Provincia', format1)
        sheet.write(f, 7, 'Ciudad', format1)
        sheet.write(f, 8, 'Barrio', format1)
        sheet.write(f, 9, 'CP', format1)
        sheet.write(f, 10, 'EAN', format1)
        sheet.write(f, 11, 'SKU_Int', format1)
        sheet.write(f, 12, 'Descripcion_SKU_Int', format1)
        sheet.write(f, 13, 'VentaBT', format1)
        sheet.write(f, 14, 'PesosBT', format1)
        sheet.write(f, 15, 'TipodePDV', format1)
        sheet.write(f, 16, 'VendedorNombreInt', format1)
        sheet.write(f, 17, 'Referencia', format1)
        sheet.write(f, 18, 'Origen', format1)
        sheet.write(f, 19, 'Documento', format1)

        for it in items:
            f += 1
            sheet.write(f, 0, it['seller'], format2)
            sheet.write(f, 1, it['client'], format2)
            sheet.write(f, 2, str(it['date'])[8:]+str(it['date'])[5:7]+str(it['date'])[:4], format2)
            sheet.write(f, 3, it['client_id'], format2)
            sheet.write(f, 4, '', format2)
            sheet.write(f, 5, it['street'], format2)
            sheet.write(f, 6, '', format2)
            sheet.write(f, 7, it['city'], format2)
            sheet.write(f, 8, it['street2'], format2)
            sheet.write(f, 9, it['zip'], format2)
            sheet.write(f, 9, '', format2)
            sheet.write(f, 10, '', format2)
            sheet.write(f, 11, it['product_id'], format2)
            sheet.write(f, 12, it['product'], format2)
            sheet.write(f, 13, it['quantity'], format2)
            sheet.write(f, 14, it['price_total'], format2)
            sheet.write(f, 15, it['type'], format2)
            sheet.write(f, 16, it['commercial'], format2)
            sheet.write(f, 17, it['reference'], format2)
            sheet.write(f, 18, it['origin'], format2)
            sheet.write(f, 19, it['move_name'], format2)

