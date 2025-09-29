from odoo import api, fields, models, exceptions
from odoo.exceptions import UserError
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):   # Class names should be CamelCase
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "id desc"
    _rec_name = "property_id"


    price = fields.Float(string="Price")

    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")],string="State",copy=False)

    partner_id = fields.Many2one("res.partner",string="Customer",required=True)
    validity = fields.Integer(string="Validity (days)", default = 7)

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date.date() + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days

    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline",
                                store=True)
    def status_accepted(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda o: o.status == "accepted"):
                raise exceptions.UserError("An offer for this property has already been accepted.")
            else:
                record.status = "accepted"
                if record.property_id:
                    record.property_id.selling_price = record.price
                    record.property_id.buyer = record.partner_id

    def status_refused(self):
        for record in self:
            record.status = "refused"

    @api.constrains("price")
    def _offer_price_con(self):
        for record in self:
            if record.price <= 0:  # Example: must be 9 characters
                raise exceptions.ValidationError("Give a good deal, please!")

    @api.constrains("status")
    def _check_offer_price(self):
        for offer in self:
            if offer.status == "accepted" and offer.price <= offer.property_id.expected_price * 0.9:
                raise exceptions.ValidationError("Cannot accept this offer: price is less than 90% of expected property price.")

    property_id = fields.Many2one("estate.property",string="Property",required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type",
                                       related="property_id.property_type_id", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'property_id' in vals:
                property_rec = self.env['estate.property'].browse(vals['property_id'])
                existing_offers = property_rec.offer_ids.mapped('price')
                if existing_offers and vals['price'] < max(existing_offers):
                    raise UserError(
                        f"You cannot create an offer lower than an existing offer for property {property_rec.name}."
                    )
        return super(EstatePropertyOffer, self).create(vals_list)

