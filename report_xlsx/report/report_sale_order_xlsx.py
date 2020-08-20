# Copyright 2017 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleXlsx(models.AbstractModel):
    _name = "report.report_xlsx.sale_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Sale XLSX Report"

    def generate_xlsx_report(self, workbook, data, orders):
        hoja = workbook.add_worksheet("Sale")
        for i, obj in enumerate(orders):
            report_name = obj.name
        #for obj in orders:
            bold = workbook.add_format({"bold": True})
            date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})
            hoja.write(i, 0, obj.name, bold)
            #hoja.write(i, 1, obj.date_order, date_format)
            hoja.write(i, 2, obj.payment_term_id.name, bold)
            hoja.write(i, 3, obj.partner_invoice_id.name, bold)
            hoja.write(i, 4, obj.partner_shipping_id.name, bold)

#SaleXlsx('report.report_xlsx.sale_xlsx','report.report_xlsx.sale_xlsx')
