from odoo import models, api

class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.model
    def _get_tax_totals_summary(self, base_lines, currency, company, cash_rounding=None):

        res = super()._get_tax_totals_summary(base_lines, currency, company, cash_rounding)

        res['total_discount_currency'] = 44

        return res

