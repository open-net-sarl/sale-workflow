# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    commitment_date = fields.Datetime()

    @api.multi
    def write(self, vals):
        for line in self:
            if not line.commitment_date and line.order_id.commitment_date and\
                    'commitment_date' not in vals:
                vals.update({
                    'commitment_date': line.order_id.commitment_date
                })
        return super(SaleOrderLine, self).write(vals)

    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        if res.order_id.commitment_date and not res.commitment_date:
            res.write({'commitment_date': res.order_id.commitment_date})
        return res

    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        vals = super(SaleOrderLine, self).\
            _prepare_procurement_values(group_id)
        if self.commitment_date:
            vals.update({'date_planned': self.commitment_date})
        return vals
