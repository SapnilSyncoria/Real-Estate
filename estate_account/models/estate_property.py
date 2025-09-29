from odoo import models, fields, api
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    invoice_id = fields.Many2one(
        'account.move',
        string="Created Invoice",
    )
    def action_mark_sold(self):

        res = super().action_mark_sold()

        # Find the product template marked as property
        property_template = self.env['product.template'].search([('is_property', '=', True)], limit=1)
        if property_template:
            property_product = property_template.product_variant_id  # get the variant

        for property in self:
            if property.buyer and property_template:
                # Create the invoice
                move_obj = self.env['account.move'].create({
                    'move_type': 'out_invoice',  # Customer invoice
                    'partner_id': property.buyer.id,
                    'invoice_line_ids': [
                        (0, 0, {
                            'product_id': property_product.id,  # product variant
                            'quantity': 1,
                            'price_unit': property.selling_price,  # 6% commission
                        })
                    ],
                    'property_id': property.id,
                })
                #print('move_ob-------', move_obj)
                property.write({
                    'invoice_created': True,
                    'invoice_id': move_obj.id,
                })
        return res