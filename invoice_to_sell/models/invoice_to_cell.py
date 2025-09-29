from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    sale_order_id = fields.Many2one(
        'sale.order',
        string="Related Sale Order",
        help="The Sale Order created from this invoice."
    )

    discount_in_sales = fields.Float(string="Discount In Sales")

    def button_create_sale_order(self):

        for invoice in self:
            if invoice.sale_order_id:
                continue

            if invoice.move_type != 'out_invoice':
                continue

            # Create Sale Order
            sale_order = self.env['sale.order'].create({
                'partner_id': invoice.partner_id.id,
                'origin': invoice.name or invoice.ref or "Invoice",
                'invoice_id': invoice.id,  # link invoice → sale order
            })

            # Add Sale Order Lines from Invoice Lines
            for line in invoice.invoice_line_ids:
                self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'price_unit': line.price_unit,
                    'name': line.name,
                    'discount': line.discount,
                    'tax_id': line.tax_ids,
                })

            # Link back
            invoice.sale_order_id = sale_order.id

        return True
