# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.fields import datetime,date
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo.tools.misc import formatLang, get_lang


class AbrusDsrConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    is_dsr_abrus = fields.Boolean("Card Details", config_parameter='crmsuite_custom.is_dsr_abrus')
    is_kyc_details = fields.Boolean("KYC Details", config_parameter='crmsuite_custom.is_kyc_details')
    module_ks_dashboard_ninja = fields.Boolean(string="CRM Dashboard")
    is_need_expected_revenue = fields.Boolean("Expected Revenue", config_parameter='crmsuite_custom.is_need_expected_revenue')
    module_crm_pipeline_default_tree = fields.Boolean(string="Pipline Tree View Default")
