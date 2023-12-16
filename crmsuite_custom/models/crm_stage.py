from odoo import api, fields, models,_


class ModeOfApprove(models.Model):
    _inherit = 'crm.stage'

    @api.onchange('level_of_approve')
    def onchange_level_approve(self):
        if self.level_of_approve:
            res_ids = []
            for i in range(self.level_of_approve):
                res_ids.append((0, 0, {'name': 'Level' + ' ' + str(i + 1)}))
            self.level_ids = res_ids
            print(self.level_ids)



    # name = fields.Char()
    is_approval_needed = fields.Boolean(string="Is Approval Needed?")
    level_of_approve = fields.Integer(limit=5, string='Level Of Approve')
    # reference_no = fields.Char(string='Reference')
    level_ids = fields.One2many('approve.level', 'approve_id')
    # abrus_team_ids = fields.Many2many('crm.team',string="Sales Team Abrus")
    abrus_team_ids = fields.Many2many('crm.team', string="Sales Teams")
    is_prescreening = fields.Boolean('Is Pre-screening Stage?' )
    is_approved_stage = fields.Boolean("Convert To Sale")
    is_converted_stage = fields.Boolean(string="Converted Stage")
    is_declined_stage = fields.Boolean(string="Declined Stage")
    is_oppor_approved_stage = fields.Boolean(string="Approved Stage")


class LevelApprove(models.Model):
    _name = 'approve.level'

    @api.onchange('group_id')
    def onchange_group_id(self):
        for rec in self:
            grp = self.env['res.groups'].search([('full_name', '=', rec.group_id.full_name)])
            print("grp",grp.full_name)
            print("grp_full",rec.group_id.full_name)
            rec.users_ids = grp.users
            # rec.users_ids = [(4, user.id) for user in  grp.users]

    users_ids = fields.Many2many('res.users', string="Users")

    group_id = fields.Many2one('res.groups', string="Allotted Users",
                    domain=lambda self: [("category_id.name", "=", 'Sales')])
    approve_id = fields.Many2one('crm.stage',string='Approve')
    name = fields.Char(string='Levels')
    # user_ids = fields.Many2many('res.users', string='Allotted Users')
    document_id = fields.Many2one('approve.document')
    bool_document = fields.Boolean(default=False)

class ApproveDocument(models.Model):
    _name = 'approve.document'

    reference_no = fields.Char('Reference No')
    level_ids = fields.One2many('approve.level', 'document_id')


