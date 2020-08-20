from odoo import fields, models, api
import xlsxwriter
import io
import base64
from datetime import datetime, timedelta

class OtifReportWizard(models.TransientModel):
    _name = 'otif.report.wizard'
    _description = "Otif report wizard"

    name = fields.Char('File Name',  readonly=True)
    data = fields.Binary('File',  readonly=True,  attachment=False)
    state = fields.Selection([('choose',  'choose'),  ('get',  'get')],  default='choose')
    start_datetime = fields.Datetime('Start Datetime')
    end_datetime = fields.Datetime('End Datetime')
    attachment_id = fields.Many2one('ir.attachment',  'Attachment')
    data_attachment = fields.Binary(related='attachment_id.datas')

    def operation_dates(self,  date1,  date2,  operator):
        date1 = self.date_date(date1)
        date2 = self.date_date(date2)
        if operator == '+':
            result = date1 + date2
        if operator == '-':
            result = date1 - date2
        if operator == '/':
            result = date1 / date2
        return result

    def date_date(self,  date):
        try:
            date = date.date()
        except:
            date = date
        return date

    def generate_file(self):
        this = self[0]

        # Elimina reportes anteriormente creados
        self.env['ir.attachment'].search([('res_model', '=', 'otif.report.wizard')]).unlink()

        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output,  {'in_memory': True})
        worksheet = workbook.add_worksheet()

        #Formats
        title = workbook.add_format({'align':'center',  'bold':True})
        datetime = workbook.add_format({'num_format': 'd-m-yy hh:mm:ss', 'align':'center'})
        subtitle = workbook.add_format({'bold': True, 'align':'center'})
        general = workbook.add_format({'align':'center'})
        general_datetime = workbook.add_format({'align':'center', 'num_format': 'd-m-yy hh:mm:ss'})

        #merge cells
        #worksheet.merge_range('')

        #Size Column
        worksheet.set_column('AB:AB',  20)
        worksheet.set_column('AH:AH',  20)
        worksheet.set_column('AC:AC',  40)
        worksheet.set_column('AI:AI',  40)
        worksheet.set_column('A:N',  20)
        worksheet.set_column('O:AA',  40)
        worksheet.set_column('AD:AE',  20)
        worksheet.set_column('AF:AG', 40)

        # Write some test data.
        worksheet.write(0,  0,  'Reporte Otif')
        worksheet.write(1,  0,  'Inicio', subtitle)
        worksheet.write_datetime(1,  1,  self.start_datetime or '', datetime)
        worksheet.write(2,  0,  'Fin', subtitle)
        worksheet.write(2,  1,  self.end_datetime or '', datetime)

        # codigo,  mes,  Orden,  Cliente,
        worksheet.write(4,  0,  'Codigo del Pais', subtitle)
        worksheet.write(4,  1,  'Mes Facturación', subtitle)
        worksheet.write(4,  2,  'Año', subtitle)
        worksheet.write(4,  3,  'Cliente', subtitle)
        worksheet.write(4,  4,  'Orden', subtitle)
        worksheet.write(4,  5,  'Ficha', subtitle)
        worksheet.write(4,  6,  'Pedido', subtitle)
        worksheet.write(4,  7,  'Codigo Cliente', subtitle)
        worksheet.write(4,  8,  'Referencia', subtitle)
        worksheet.write(4,  9,  'Material', subtitle)
        worksheet.write(4,  10,  'Tipo Pedido', subtitle)
        worksheet.write(4,  11,  'Presentación Material', subtitle)
        worksheet.write(4,  12,  'Descripción', subtitle)
        worksheet.write(4,  13,  'Cantidad Solicitada', subtitle)
        worksheet.write(4,  14,  'Unidad Empaque (Rollos/Unds)', subtitle)
        worksheet.write(4,  15,  'Fecha Requerida Cliente', subtitle)
        worksheet.write(4,  16,  'Fecha Llegada O.C a SPK', subtitle)
        worksheet.write(4,  17,  'Lead Time Solicitado por Cliente', subtitle)
        worksheet.write(4,  18,  'FSP(Fecha Solicitada a PDN)', subtitle)
        worksheet.write(4,  19,  'FED(Fecha Estimada de Despacho)', subtitle)
        worksheet.write(4,  20,  '(ETA) Fecha estimada de llegada a cliente', subtitle)
        worksheet.write(4,  21,  'Ingreso pedidos a Programacion', subtitle)
        worksheet.write(4,  22,  'FOP(Fecha Ofrecida por PDN)', subtitle)
        worksheet.write(4,  23,  'FRE(Fecha Real Entrega PDN', subtitle)
        worksheet.write(4,  24,  'Cantidad entregada', subtitle)
        worksheet.write(4,  25,  'Diferencia en Cumplimiento (Dias)', subtitle)
        worksheet.write(4,  26,  '% Cumplimiento de PDN en Cantidad', subtitle)
        worksheet.write(4,  27,  'Dias en proceso PDN', subtitle)
        worksheet.write(4,  28,  'No factura exportacion', subtitle)
        worksheet.write(4,  29,  'Operador', subtitle)
        worksheet.write(4,  30,  'No de guia', subtitle)
        worksheet.write(4,  31,  'Fecha Real Despacho', subtitle)
        worksheet.write(4,  32,  'Fecha Real Entrega en Cliente', subtitle)
        worksheet.write(4,  33,  'Tiempo de transito', subtitle)
        worksheet.write(4,  34,  'Cumplimiento Cantidades', subtitle)


        # Variables
        domain = [('date_order', '>=', self.start_datetime), ('date_order', '<=', self.end_datetime)]
        orders = self.env['sale.order'].search(domain)
        # print values
        for i,  order in enumerate(orders):

            if self.start_datetime <= order.date_order or order.date_order >= self.end_datetime:
                pass

            worksheet.write(i + 5,  0,  order.partner_id.state_id.number_code or '', general)
            month = order.date_order
            if order.date_order:
                month = month.strftime('%B').capitalize()
            worksheet.write(i + 5,  1,  month if orders else '', general)
            worksheet.write(i + 5,  2,  order.date_order.year or '', general)
            worksheet.write(i + 5,  3,  order.partner_id.name or '', general)
            worksheet.write(i + 5,  4,  order.name or '', general)
            worksheet.write(i + 5,  5,  order.sheet_id.name or '', general)

            #pedido
            production = self.env['mrp.production'].search([('origin', '=', order.name)],  limit=1)
            worksheet.write(i + 5,  6,  production.name if production else '',  general)

            worksheet.write(i + 5,  7,  order.sheet_id.product_code or '', general)
            worksheet.write(i + 5,  8,  order.sheet_id.produce or '', general)
            worksheet.write(i + 5,  9,  order.sheet_id.presentation_id.name or '', general)
            worksheet.write(i + 5,  10,  order.type_sale or '', general)
            worksheet.write(i + 5,  11,  order.sheet_id.presentation_id.name or '', general)
            worksheet.write(i + 5,  12,  order.sheet_id.produce or '', general)
            worksheet.write(i + 5,  13,  order.sheet_id.quantity or 0.00, general)
            worksheet.write(i + 5,  14,  order.sheet_id.uom_id.name or '', general)
            worksheet.write(i + 5,  15,  order.commitment_date or '', general_datetime)
            worksheet.write(i + 5,  16,  order.date_order or '', general_datetime)

            lead = 0
            if order.date_order and order.effective_date:
                lead = self.operation_dates(order.date_order,  order.effective_date,  '-')

            worksheet.write(i + 5,  17,  lead,  general)
            worksheet.write(i + 5,  18,  production.date_planned_finished if production else '', general_datetime)

            picking = self.env['stock.picking'].search([('origin', '=', order.name)],  limit=1)
            worksheet.write(i + 5,  19,  picking.scheduled_date if picking else '',  general_datetime)
            #worksheet.write(i + 5,  20,  obj.scheduled_date or '', general_datetime)eta
            worksheet.write(i + 5,  23,  picking.date_done if picking else '', general_datetime)
            done = 0
            if picking:
                for move in picking.move_line_ids_without_package:
                    done += move.qty_done
            worksheet.write(i + 5,  24,  done,  general)
            worksheet.write(i + 5,  21,  production.date_planned_start if production else '',  general_datetime)
            worksheet.write(i + 5,  22,  production.date_planned_finished if production else '',  general_datetime)
            compliance = 0
            #if order.date_order and order.effective_date:
             #   compliance = self.operation_dates(order.date_order,  order.effective_date,  '-')
            #worksheet.write(i + 5,  25,   if  else '',  general) diferencia en cumplimiento (dias)
            compliance = 0
            if order and picking:
                for sale in order.order_line:
                        if done == 0:
                            compliance = 0
                        else:
                            compliance += (sale.product_uom_qty/done)
            worksheet.write(i + 5,  26,   compliance,  general)
            #worksheet.write(i + 5,  27,  production.date_planned_finished if production else '',  general_datetime)Dias en proceso PDN
            invoice = self.env['account.move'].search([('invoice_origin',  '=',  'order.name')],  limit=1)
            worksheet.write(i + 5,  28,  invoice.name if invoice else '',  general)
            #worksheet.write(i + 5,  29,  invoice.name if invoice else '',  general)operador
            #worksheet.write(i + 5,  30,  invoice.name if invoice else '',  general)no guia
            worksheet.write(i + 5,  31,  picking.date_done if picking else '',  general_datetime)
            # worksheet.write(i + 5,  32,  invoice.name if invoice else '',  general)Fecha Real Entrega en Cliente
            # worksheet.write(i + 5,  33,  invoice.name if invoice else '',  general)Tiempo de transito
            worksheet.write(i + 5,  34,  compliance ,  general)




        # Close the workbook before streaming the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Create attachement
        dic = {
            'name': 'Report.xlsx',
            'type': 'binary',
            'res_model': 'otif.report.wizard',
            'db_datas': base64.encodestring(output.read()),
        }
        attachment_id = self.env['ir.attachment'].create(dic)

        # return values
        out = base64.encodestring(output.read())
        name = 'Report.xlsx'
        this.write({'state': 'get',  'data': out,  'name': name,  'attachment_id': attachment_id.id})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'otif.report.wizard',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False,  'form')],
            'target': 'new',
        }