from odoo import fields, models, api


class ResPartners(models.Model):
    _inherit = 'res.partner'

    worker_profession_id = fields.Many2one('worker.profession', string="Profession")
    is_user = fields.Boolean(compute="_compute_is_user", store=True)
    sub_user_type = fields.Selection([('worker', 'Worker'), ('user', 'User')], default='user')
    avg_rating = fields.Float(compute="_compute_avg_rating", store=True)
    partner_rating_ids = fields.One2many('res.partner.rating', 'partner_id')

    @api.depends('user_ids', 'user_id')
    def _compute_is_user(self):
        for rec in self:
            rec.is_user = True if rec.user_ids else False

    @api.depends('partner_rating_ids')
    def _compute_avg_rating(self):
        for rec in self:
            if len(rec.partner_rating_ids) > 0:
                rec.avg_rating = sum(rec.partner_rating_ids.mapped('star_count')) / len(rec.partner_rating_ids)
            else:
                rec.avg_rating = 0
