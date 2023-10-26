from odoo import fields, models


class Districts(models.Model):
    _name = 'res.country.state.district.location'
    _description = 'location of district'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    district_id = fields.Many2one('res.country.state.district',
                                  string="District",
                                  readonly=True)
