from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,Warning
from datetime import datetime,date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class WizardReject(models.TransientModel):
    _name = 'abrus.reject.wizard'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    reason = fields.Text(string='Reason')
    reject_ribbon_bool = fields.Boolean("REJECT RIBBON BOOL")
    crm_m2m = fields.Many2one('crm.lead',default=lambda self:self._context.get('active_id',False))

    def process_reject_abrus(self):
        for rec in self:
            rec.crm_m2m.nxt_user_id = [(5, 0, 0)]
            rec.crm_m2m.reject_bool = True
            rec.crm_m2m.reject_reason = rec.reason
            rec.crm_m2m.write({
                'status_approved': 'rejected'
            })
        self.crm_m2m.get_catter()
        # display_msg = 'Rejected -->' + self.reason
        # self.message_post(body=display_msg)



