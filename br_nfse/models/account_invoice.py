# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    ambiente_nfse = fields.Selection(
        string="Ambiente NFe", related="company_id.tipo_ambiente_nfse",
        readonly=True)

    def _return_pdf_invoice(self, doc):
        if self.fiscal_document_id.code == '001':  # Paulistana
            return 'br_nfse.report_br_nfse_danfe'
        elif self.fiscal_document_id.code == '002':  # Ginfes
            return 'br_nfse.report_br_nfse_danfe_ginfes'
        elif self.fiscal_document_id.code == '008':  # Simpliss
            return 'br_nfse.report_br_nfse_danfe_simpliss'
        elif self.fiscal_document_id.code == '010':
            return 'br_nfse.report_br_nfse_danfe_imperial'  # Imperial
        elif self.fiscal_document_id.code == '009':  # Susesu
            return {
                "type": "ir.actions.act_url",
                "url": doc.url_danfe,
                "target": "_blank",
            }
        return super(AccountInvoice, self)._return_pdf_invoice(doc)

    def _prepare_edoc_vals(self, inv):
        res = super(AccountInvoice, self)._prepare_edoc_vals(inv)

        res['ambiente_nfse'] = 'homologacao' \
            if inv.company_id.tipo_ambiente_nfse == '2' else 'producao'

        if self.invoice_model == '001':
            res['data_emissao'] = self.date_invoice
            res['data_fatura'] = self.date_invoice

        return res

    def _prepare_edoc_item_vals(self, line):
        res = super(AccountInvoice, self)._prepare_edoc_item_vals(line)
        res['codigo_servico_paulistana'] = \
            line.service_type_id.codigo_servico_paulistana
        res['codigo_tributacao_municipio'] = \
            line.service_type_id.codigo_tributacao_municipio
        return res
