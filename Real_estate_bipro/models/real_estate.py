from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
from datetime import date, timedelta


class EstateProperty(models.Model):   # Class names should be CamelCase
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"


    name = fields.Char(string="Name", required=True)
    postcode = fields.Char(string="Postcode")
    bedrooms = fields.Integer(string="Bedrooms", default=2)

    living_area = fields.Integer(string="Living Area")

    expected_price = fields.Float(string="Expected Price", required=True)

    selling_price = fields.Float(string="Selling Price", compute="_compute_selling_price", readonly=True, copy=False)
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: date.today() + timedelta(days=90)  # ~3 months
    )

    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")

    garden_area = fields.Integer(string="Garden Area")

    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)

    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )

    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="State", compute="_compute_state",
        required=True,
        copy=False,
        default="new", store =True
    )
    #many to one
    property_type_id = fields.Many2one(comodel_name="estate.property.type",string="Property Type",required=True )

    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True,
                              default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer')

    # many to many
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    # one to many
    offer_ids = fields.One2many("estate.property.offer","property_id",string="Offers")

    #computational tings
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total")

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Char(compute="_compute_best_price", string="Best Offer", store=True)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
## for button
    status = fields.Selection(
        [
            ("new", "New"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new"
    )


    def sold(self):
        for record in self:
            if record.status == "canceled":
                raise exceptions.UserError("It is already cancelled")
            else:
                record.status = "sold"

    def canceled(self):
        for record in self:
            if record.status == "sold":
                raise exceptions.UserError("It is already sold")
            else:
                record.status = "canceled"

    @api.constrains("expected_price")
    def _expected_price_con(self):
        for record in self:
            if record.expected_price <= 0:  # Example: must be 9 characters
                raise exceptions.ValidationError("Sky should be your limit, man!")

    @api.depends('offer_ids.status', 'offer_ids.price', 'expected_price')
    def _compute_selling_price(self):
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offer:
                offer = accepted_offer[0]
                if offer.price < record.expected_price * 0.9:
                    record.selling_price = 0.0
                else:
                    record.selling_price = offer.price
            else:
                record.selling_price = 0.0

    @api.depends('offer_ids.status', 'status')
    def _compute_state(self):
        for record in self:
            accepted_offers = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            any_offers = record.offer_ids

            # Priority: accepted offer > received offer > new
            if accepted_offers:
                record.state = 'offer_accepted'
            elif any_offers:
                record.state = 'offer_received'
            else:
                record.state = 'new'

            # Then handle final states based on actual property status
            if record.status == 'sold' and accepted_offers:
                record.state = 'sold'
            elif record.status == 'canceled':
                record.state = 'cancelled'

    can_be_sold = fields.Boolean(
        string="Can be Sold",
        compute="_compute_can_be_sold",
        store=True
    )

    @api.depends('offer_ids.status', 'status')
    def _compute_can_be_sold(self):
        for record in self:
            # Sold button visible only if property not sold/canceled and at least one offer accepted
            record.can_be_sold = record.status not in ['sold', 'canceled'] and bool(
                record.offer_ids.filtered(lambda o: o.status == 'accepted')
            )

    # Button: Mark as Sold
    def action_mark_sold(self):
        for record in self:
            if not record.can_be_sold:
                raise UserError("You cannot mark this property as Sold unless an offer has been accepted!")
            record.status = 'sold'

    # Optional: Cancel button
    def action_cancel(self):
        for record in self:
            if record.status in ['sold', 'canceled']:
                raise UserError("This property is already Sold or Cancelled!")
            record.status = 'canceled'

    property_type_ids = fields.Many2one("estate.property.type", string="Property Type IDs")

    @api.ondelete(at_uninstall=False)
    def _cascade_delete_if_new_or_cancelled(self):
        for record in self:
            if record.status not in ['new', 'canceled']:
                raise UserError(
                    "You cannot delete a property unless it is New or Cancelled."
                )
            # Delete dependent offers
            if record.offer_ids:
                record.offer_ids.unlink()

    invoice_created = fields.Boolean(
        string="Invoice Created",
        default=False,
        copy=False
    )


    show_mark_sold_button = fields.Boolean(compute="_compute_show_mark_sold_button")

    def _compute_show_mark_sold_button(self):
        for record in self:
            record.show_mark_sold_button = self.env.user.has_group("base.group_system")
