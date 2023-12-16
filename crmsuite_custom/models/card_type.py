from odoo import models, fields, api, _


class Card(models.Model):
    _name = 'card.type.abrus'
    # _description = 'HR Employee Family'
    _rec_name = "card_type_name"

    card_type_name = fields.Char(string="Card Type")
    is_need_amt_details = fields.Boolean(string="Show Amount/Fee")
    stage_ids = fields.Many2many('crm.stage', string="Stages")

class CardVarient(models.Model):
    _name = 'card.variant.abrus'
    _rec_name = "card_variant_name"

    card_variant_name = fields.Char(string="Card variant name")


class Recidence(models.Model):
    _name = 'residence.abrus'
    _rec_name = "residence_ab"

    residence_ab = fields.Char(string="Type of Residence")
