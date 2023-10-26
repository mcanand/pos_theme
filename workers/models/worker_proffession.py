from odoo import fields, models, api


class ProfessionCategory(models.Model):
    _name = 'profession.category'

    name = fields.Char()
    image = fields.Binary()
    worker_profession_ids = fields.One2many('worker.profession','profession_category_id')


class WorkerProfession(models.Model):
    _name = 'worker.profession'

    name = fields.Char()
    image = fields.Binary()
    profession_category_id = fields.Many2one('profession.category')
