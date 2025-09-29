from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    #discount_from_invoice = fields.Float(string="Discount In Sales")
    discount_amount = fields.Float(
        string="Discount Amount",
        compute="_compute_discount_amount"
    )

    @api.depends('discount','price_unit', 'product_uom_qty')
    def _compute_discount_amount(self):
        for line in self:
            discount = line.price_unit * line.product_uom_qty * (line.discount / 100)
            # Apply currency rounding if available, otherwise just round(2)
            if line.currency_id:
                line.discount_amount = line.currency_id.round(discount)
            else:
                line.discount_amount = round(discount, 2)


