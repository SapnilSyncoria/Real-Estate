from odoo import fields, models, api, exceptions

class EstatePropertyTypes(models.Model):   # Class names should be CamelCase
    _name = "estate.property.type"
    _description = "Real Estate Property Types"
    _order = "sequence desc, type_estate_properties asc"
    _rec_name = "type_estate_properties"


    type_estate_properties = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer(string = 'Sequence', default=0, help="Used to order stages. Higher is better.")
    property_ids = fields.One2many("estate.property", "property_type_ids" )

    @api.constrains('type_estate_properties')
    def _check_unique_name(self):
        for record in self:
            if self.search([('type_estate_properties', '=', record.type_estate_properties), ('id', '!=', record.id)]):
                raise exceptions.ValidationError('Property Type must be unique!')

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_counts= fields.Integer(
        string="Number of Offers",
        compute="_compute_offer_count",
        store=True
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_counts = record.offer_ids.search_count([('property_type_id', '=', record.id)])
    def action_view_offers(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Offers',
            'res_model': 'estate.property.offer',
            'view_mode': 'list,form',
            'domain': [('property_type_id', '=', self.id)],
            'context': {'default_property_type_id': self.id},
        }




