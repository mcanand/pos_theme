from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    district_id = fields.Many2one('res.country.state.district',
                                  string="District",
                                  domain="[('state_id','=?', state_id)]")
    location_id = fields.Many2one('res.country.state.district.location',
                                  string="Location",
                                  domain="[('district_id','=?', district_id)]")

    @api.onchange('district_id')
    def onchange_district_id(self):
        if self.district_id:
            self.state_id = self.district_id.state_id.id

    @api.onchange('location_id')
    def onchange_location_id(self):
        if self.location_id:
            self.district_id = self.location_id.district_id.id