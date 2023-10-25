from odoo import fields, models, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    freight_charge = fields.Float()

    def _get_fields_for_draft_order(self):
        res_fields = super(PosOrder, self)._get_fields_for_draft_order()
        res_fields.extend(['freight_charge'])
        return res_fields

    def _export_for_ui(self, order):
        res = super(PosOrder, self)._export_for_ui(order)
        res['freight_charge'] = order.waiter_id.id if order.waiter_id else ''
        return res

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['freight_charge'] = ui_order.get('freight_charge')
        return order_fields
