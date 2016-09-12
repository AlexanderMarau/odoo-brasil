# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.onchange('tax_icms_id')
    def _simples_nacional_onchange_tax_icms_id(self):
        if self.tax_icms_id:
            self.icms_percent_credit = self.tax_icms_id.percent_credit
