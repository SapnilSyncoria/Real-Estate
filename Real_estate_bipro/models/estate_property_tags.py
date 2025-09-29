from odoo import fields, models, api, exceptions
from odoo.exceptions import ValidationError


class EstatePropertyTag(models.Model):   # Class names should be CamelCase
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"
    _order = "tag_estate_properties asc"
    _rec_name = "tag_estate_properties"


    tag_estate_properties = fields.Char(string="Property Tag", required=True)
    _sql_constraints = [
        ('unique_tag_name', 'unique(tag_estate_properties)', 'Tag should be unique.')
    ]
    color = fields.Integer(string="Color")
    # @api.constrains("tag_estate_properties")
    # def _unique_tag(self):
    #     for record in self:
    #         if record.tag_estate_properties.not unique:  # Example: must be 9 characters
    #             raise exceptions.ValidationError("Tag should be unique.")


