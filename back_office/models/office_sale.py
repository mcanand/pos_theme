from odoo import fields, models, api
from datetime import datetime


class OfficeSale(models.Model):
    _name = "office.sale"

    name = fields.Char()
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    session_ids = fields.One2many('office.session', 'sale_id')
    active_session_id = fields.Many2one('office.session', compute="_compute_active_session")
    session_responsible_user_id = fields.Many2one('res.users', compute="_compute_user_id")
    journal_id = fields.Many2one('account.journal', domain=[('type', '=', 'sale')], required=True,
                                 compute="_compute_journal_id", store=True, readonly=False)
    agent_journal_id = fields.Many2one('account.journal', domain=[('type', '=', 'purchase')])
    discount_product_id = fields.Many2one('product.product')
    sale_agent_product_id = fields.Many2one('product.product', domain=[('detailed_type', '=', 'service')])


    @api.depends('company_id')
    def _compute_journal_id(self):
        for order in self:
            order.journal_id = False
            domain = [('company_id', '=', order.company_id.id), ('type', '=', 'sale')]
            journal = self.env['account.journal'].search(domain, limit=1)
            if journal:
                order.journal_id = journal.id

    @api.depends('session_ids', 'active_session_id')
    def _compute_user_id(self):
        for rec in self:
            rec.session_responsible_user_id = False
            if rec.active_session_id:
                rec.session_responsible_user_id = rec.active_session_id.user_id.id

    @api.depends('session_ids')
    def _compute_active_session(self):
        for rec in self:
            sessions = self.env['office.session'].sudo()
            session = sessions.search([('sale_id', '=', rec.id), ('state', '=', 'in_progress')], limit=1)
            rec.active_session_id = session.id if session else False

    def action_open_session_orders(self):
        sessions = self.env['office.session'].sudo()
        active_sessions = sessions.search([('sale_id', '=', self.id), ('state', '=', 'in_progress')])
        if active_sessions:
            if len(active_sessions) > 1:
                return {
                    'name': 'Sessions',
                    'type': 'ir.actions.act_window',
                    'res_model': 'office.session',
                    'view_mode': 'tree,form',
                    "context": {"create": False, },
                    "domain": [('id', 'in', self.session_ids.ids)],
                    'views': [[False, "tree"], [False, "form"]],
                }
            else:
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'office.order',
                    'view_mode': 'form',
                    'target': 'current',
                    'view_id': self.env.ref('back_office.view_office_order_form').id,
                    'views': [(False, 'form')],
                    'context': {'default_session_id': active_sessions.id}
                }
        new_session = sessions.create({'sale_id': self.id,
                                       'start_at': datetime.now(),
                                       'state': 'in_progress'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'office.order',
            'view_mode': 'form',
            'target': 'current',
            'view_id': self.env.ref('back_office.view_office_order_form').id,
            'views': [(False, 'form')],
            'context': {'default_session_id': new_session.id}
        }

    def action_close_session_orders(self):
        sessions = self.env['office.session'].sudo()
        active_sessions = sessions.search([('sale_id', '=', self.id), ('state', '=', 'in_progress')])
        if len(active_sessions) > 1:
            return {
                'name': 'Sessions',
                'type': 'ir.actions.act_window',
                'res_model': 'office.session',
                'view_mode': 'tree,form',
                "context": {"create": False, },
                "domain": [('id', 'in', self.session_ids.ids)],
                'views': [[False, "tree"], [False, "form"]],
            }
        else:
            active_sessions.action_close()

    def action_sessions(self):
        if self.session_ids:
            return {
                'name': 'Sessions',
                'type': 'ir.actions.act_window',
                'res_model': 'office.session',
                'view_mode': 'tree,form',
                "context": {"create": False, },
                "domain": [('id', 'in', self.session_ids.ids)],
                'views': [[False, "tree"], [False, "form"]],
            }

    def action_orders(self):
        order_ids = self.session_ids.mapped('order_ids').ids
        if order_ids:
            return {
                'name': 'Orders',
                'type': 'ir.actions.act_window',
                'res_model': 'office.order',
                'view_mode': 'tree,form',
                "context": {"create": False, },
                "domain": [('id', 'in', order_ids)],
                'views': [[False, "tree"], [False, "form"]],
            }

    def action_settings(self):
        return {
            'name': self.name + " Settings",
            'type': 'ir.actions.act_window',
            'res_model': 'office.sale',
            "context": {"create": False},
            'view_mode': 'form',
            'res_id': self.id
        }

    def action_session(self):
        if self.active_session_id:
            return {
                'name': self.name,
                'type': 'ir.actions.act_window',
                'res_model': 'office.session',
                "context": {"create": False},
                'view_mode': 'form',
                'res_id': self.active_session_id.id
            }