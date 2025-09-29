from odoo import models, fields, api, exceptions
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_id = fields.Many2one(
        'account.move',
        string="Related Invoice",
        help="The Invoice from which this Sale Order was created."
    )

    discount_percent = fields.Float(
        string="Discount Percent",
        readonly=False,
    )

    @api.constrains('discount_percent')
    def _inbetween_zero_to_hundred(self):
        for record in self:
            if self.discount_percent< 0 or self.discount_percent>100:
                raise exceptions.ValidationError('Ohh! How percent can be larger than 100 or less than 0?')


    total_discount = fields.Monetary(
        string="Total Discount",
        currency_field="currency_id",
    )

    total_discount_2 = fields.Monetary(
        string="Total Discount",
        compute="_compute_total_discount",
        currency_field="currency_id",
    )
    total_amount = fields.Monetary(
        string="Total Amount",
        compute="_compute_total_amount",
        currency_field="currency_id",
    )

    def _compute_total_amount(self):
        for order in self:
            lines = order.order_line.filtered(lambda l: not l.display_type)
            total = sum(
                (l.price_unit or 0.0) * (l.product_uom_qty or 0.0)
                for l in lines
            )
            order.total_amount = order.currency_id.round(total)

    @api.depends(
        'order_line',                  # add/remove lines
        'order_line.display_type',     # skip sections/notes
        'order_line.price_unit',
        'order_line.product_uom_qty',
        'order_line.discount',
    )
    def _compute_total_discount(self):
        for order in self:
            lines = order.order_line.filtered(lambda l: not l.display_type)
            total = sum(
                (l.price_unit or 0.0) * (l.product_uom_qty or 0.0) * (l.discount or 0.0) / 100.0
                for l in lines
            )
            order.total_discount_2 = order.currency_id.round(total)

    def discount_distribution_button(self):
        for order in self:
            lines = order.order_line.filtered(lambda l: not l.display_type)
            n = len(lines)

            discount_new = order.discount_percent /n
            for line in lines:
                discount_percent_amount = (discount_new * 100) / (line.price_unit * line.product_uom_qty)
                if discount_percent_amount < 0 or discount_percent_amount > 100:
                    raise exceptions.ValidationError('Ohh! How percent can be larger than 100 or less than 0?')
                else:
                    line.write({'discount': discount_percent_amount})

        return True
