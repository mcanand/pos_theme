from odoo import fields, models


class PartnerRating(models.Model):
    _name = 'res.partner.rating'

    comment = fields.Char()
    star_count = fields.Integer()
    partner_id = fields.Many2one('res.partner')
