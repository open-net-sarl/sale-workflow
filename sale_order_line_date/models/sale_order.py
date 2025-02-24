# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    @api.onchange('commitment_date')
    def _onchange_commitment_date(self):
        """Warn if the commitment dates is sooner than the commitment date"""
        result = super(SaleOrder, self)._onchange_commitment_date()
        if not result:
            result = {}
        if not self:
            return result
        self.ensure_one()
        if 'warning' not in result:
            lines = []
            for line in self.order_line:
                lines.append((1, line.id, {'commitment_date':
                                           self.commitment_date}))
            result['value'] = {'order_line': lines}
        return result
