from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'estate.property',      # The target model
        'user_id',       # The Many2one field on estate.property that links to res.users
        string='Properties',
        domain=[('state', '=', 'new')]  # Only show properties that are available (state = 'new')
    )

    real_estate_role = fields.Selection(
        [
            ('user', 'User'),
            ('manager', 'Manager'),
            ('admin', 'Admin'),
        ],
        string="Real Estate Role",
    )

    @api.onchange('real_estate_role')
    def _onchange_real_estate_role(self):
        for user in self:
            # Remove any existing Real Estate groups
            user.groups_id -= self.env.ref('your_module.group_real_estate_user')
            user.groups_id -= self.env.ref('your_module.group_real_estate_manager')
            user.groups_id -= self.env.ref('your_module.group_real_estate_admin')

            # Assign the group based on selection
            if user.real_estate_role == 'user':
                user.groups_id |= self.env.ref('your_module.group_real_estate_user')
            elif user.real_estate_role == 'manager':
                user.groups_id |= self.env.ref('your_module.group_real_estate_manager')
            elif user.real_estate_role == 'admin':
                user.groups_id |= self.env.ref('your_module.group_real_estate_admin')

