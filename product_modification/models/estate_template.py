from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_property = fields.Boolean(
        string="Is a Property?",
        help="Mark this product as a property-related product.",
        copy=False,
    )

    @api.constrains('is_property', 'type')
    def _check_is_property_service(self):
        for record in self:
            if record.is_property and record.type != 'service':
                raise ValidationError(
                    "You can only mark a product as a Property if its Type is 'Service'."
                )
            if record.is_property:
                existing = self.search([('is_property', '=', True), ('id', '!=', record.id)], limit=1)
                if existing:
                    raise ValidationError(
                        "Only one product can be marked as a Property. "
                        f"Product '{existing.name}' is already marked."
                    )
