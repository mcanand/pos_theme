from lxml import etree

from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil import tz
import pytz
from pytz import timezone, UTC
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class CRMLead(models.Model):
    _inherit = 'crm.lead'
    _order = 'create_date desc'

    def _get_bool_dsa_true(self):
        for rec in self:
            # is_bool = False
            token = self.env['ir.config_parameter'].sudo().get_param('crmsuite_custom.is_dsr_abrus')
            if token == 'True' and rec.type == 'opportunity':
                rec.bool_dsa_true = True
            else:
                rec.bool_dsa_true = False
            # rec.is_bool = is_bool

    # token = self.env['ir.config_parameter'].sudo().get_param('url_shortens.bitly_token')
    def dsa_report_abrus(self):
        return self.env.ref('crmsuite_custom.report_dsa_abrus').report_action(self)

    def get_catter(self):

        display_msg = 'Rejected -->' + 'Reason -->' + self.reject_reason
        self.message_post(body=display_msg)

    @api.onchange('user_id')
    def onchange_assigned_to(self):
        if self.user_id:
            # self.user_id = self.assigned_to
            if self.team_id:
                team_members = self.env['crm.team'].sudo().search([('id', '=', self.team_id.id)])
                self.lead_team_ids = [(4, self.user_id.id)]
                for member in team_members.member_ids:
                    self.lead_team_ids = [(4, member.id)]

    def approval_abrus(self):
        for move in self:
            move.current_login = self.env.user
            move.nxt_user_id = [(5, 0, 0)]
            approve_user_same_val = self.env['crm.lead'].search([('nxt_user_id', 'in', move.user_abrus_id.id)])
            if approve_user_same_val:
                move.approval_user_same = True
            else:
                move.approval_user_same = False
            txt = move.level
            x = txt.split()
            y = x[0]
            z = str(int(x[1]) + 1)
            p = (" ".join([y, z]))
            move.level = p
            if move.level in move.stage_id.level_ids.mapped('name'):
                move.nxt_user_id = [(4, user.id) for user in
                                    move.stage_id.level_ids.filtered(lambda x: x.name == move.level).mapped(
                                        'users_ids')]
            else:
                move.nxt_user_id = [(5, 0, 0)]
                move.is_users_approved = True
                # move.write({
                #     'status_approved': 'sales_approved'
                # })
                abrus_stage_ids = self.env['crm.stage'].search([('is_prescreening', '=', True)])
                move.is_send_approval_bool = False
                move.is_aproval_need = False
                move.is_users_approved = False
                if move.pre_screen_bool == True:
                    abrus_stage_app_ids = self.env['crm.stage'].search([('is_approved_stage', '=', True)])
                    move.write({'stage_id': abrus_stage_app_ids.id})
                    move.write({
                        'status_approved': 'screening_approved'
                    })
                if abrus_stage_ids and move.stage_id.is_approved_stage != True:
                    move.write({'stage_id': abrus_stage_ids.id})
                    move.write({
                        'status_approved': 'sales_approved'
                    })

            display_msg = 'Approved'
            self.message_post(body=display_msg)

    def reject_abrus(self):
        # for rec in self:
        #     rec.reject_bool =  True
        # print(self.employee_id.name)
        context = dict(self._context or {})
        return {
            'name': 'Approval Rejection of' + ' ' + self.partner_id.name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'abrus.reject.wizard',
            'target': 'new',
            'context': context,
        }

    def send_approval_abrus(self):
        for rec in self:
            rec.is_send_approval_bool = True
            if rec.stage_id.is_approval_needed == True and rec.stage_id.level_ids:
                level = rec.stage_id.level_ids[0].name
                rec.level = level
                rec.nxt_user_id = [(4, user.id) for user in
                                   rec.stage_id.level_ids.filtered(lambda x: x.name == rec.level).mapped('users_ids')]
                list = []
                for dsmail in rec.nxt_user_id:
                    list.append(dsmail.partner_id.email)
                    delim = ','

                    emails_user = delim.join(list)
                    dsa_group = rec.nxt_user_id
                    # current_employee_id = self.env['res.users'].search([('partner_id', '=', self.env.uid)])
                    current_employee_id = rec.user_abrus_id
                    if not current_employee_id.partner_id.email:
                        raise ValidationError(
                            _("The working email is not found in '%s' employee!") % (current_employee_id.name))
                    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    model_name = self._name
                    model_id = self.id
                    url = base_url + '/web#id=' + str(model_id) + '&model=' + model_name + '&view_type=form'
                    # current_employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
                    id = self.env['ir.attachment']
                    mail_content = _(
                        'Dear <b>%s,</b>'
                        '<br/>'
                        'An DSA request raised by <b>%s</b> has send for approvals by %s.<br/>'
                        '<br/>'
                        '<a href= %s> Click Here </a> to view more details. <br/>'
                        '<br/>'
                        '<br/>'
                        ''
                        '<br/>'
                        '<br/>'
                        ' '
                        '<br/>'
                        'Thank You <br/>'
                        'My Company <br/>'
                    ) % \
                                   (dsmail.name,
                                    self.partner_id.name,
                                    current_employee_id.name,
                                    url)

                    title = _('DSA %s') % (self.partner_id.name)
                    msg_id = self.env['mail.mail'].create({
                        'email_from': current_employee_id.partner_id.email,
                        'email_to': emails_user,
                        'subject': _('DSA %s') % (self.partner_id.name),
                        'body_html': mail_content
                    })
                    if msg_id:
                        msg_id.send()
                    # result = self.env['mail.mail'].create(values).send()

            if rec.is_send_approval_bool == True:
                print("ooo")
        display_msg = 'Send For Approval'
        self.message_post(body=display_msg)

    def _get_boolean_value_dsa(self):
        for rec in self:
            # is_bool = False
            token = self.env['ir.config_parameter'].sudo().get_param('crmsuite_custom.is_dsr_abrus')
            if token == 'True':
                rec.is_bool_abrus_dsa = True
            else:
                rec.is_bool_abrus_dsa = False
            # rec.is_bool = is_bool

    def _get_user_same(self):
        for rec in self:
            if self.env.user in rec.nxt_user_id:
                # if rec.nxt_user_id == rec.user_abrus_id:
                rec.user_bool = True
            else:
                rec.user_bool = False

    def _get_is_aproval_need(self):
        for rec in self:
            if rec.stage_id.is_approval_needed == True:
                rec.is_aproval_need = True
            else:
                rec.is_aproval_need = False

    crm_stage_id = fields.Many2one('crm.stage', string='Stage', ondelete='restrict', track_visibility='onchange',
                                   index=True, copy=False,
                                   domain="['|', ('abrus_team_ids', '=', False), ('abrus_team_ids', '=', team_id)]")

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        print("Stagess", stages)
        team_id = self._context.get('default_team_id')
        if team_id:
            search_domain = [
                '|', ('id', 'in', stages.ids), '|', ('abrus_team_ids', '=', False),
                ('abrus_team_ids', 'in', [team_id])]
        else:
            print("elseee")
            search_domain = ['|', ('id', 'in', stages.ids), ('abrus_team_ids', '=', False)]
        # perform search
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    color = fields.Integer("Color", compute='_get_color')

    def _get_color(self):
        """Compute Color value according to the conditions"""
        for rec in self:
            if rec.is_send_approval_bool == True:
                rec.color = 1
                if rec.is_users_approved == True:
                    rec.color = 0
            else:
                rec.color = 0

    status_approved = fields.Selection([
        ('sales_approved', 'Sales Approved'),
        ('screening_approved', 'Pre-Screening Approved'),
        ('rejected', 'Rejected')

    ])

    def get_pre_scrren(self):
        # if self.stage_id.is_prescreening == True:
        bool_pre = self.stage_id.is_prescreening == True
        if bool_pre:
            self.pre_screen_bool = True
        else:
            self.pre_screen_bool = False

    # def get_stage_app(self):

    approve_stage = fields.Boolean("Approve stage", compute='get_stage_app')
    pre_screen_bool = fields.Boolean('pre-screen bool', compute='get_pre_scrren')
    current_login = fields.Many2one('res.users')
    approval_user_same = fields.Boolean("Approval User Same")
    is_value = fields.Boolean("IS VALUE")
    is_approve_reqted = fields.Boolean(string="Approve requested", default=False)
    is_users_approved = fields.Boolean(string="All users approved")
    reject_reason = fields.Text("Reason")
    reject_bool = fields.Boolean("Reject Bool")
    is_aproval_need = fields.Boolean("Is Approve Found", compute='_get_is_aproval_need')
    user_abrus_id = fields.Many2one('res.users', string="User ID", default=lambda self: self.env.uid)
    level = fields.Char("Level", default=lambda self: self.env['ir.sequence'].next_by_code('increment_your_field'))
    user_bool = fields.Boolean(string="Is User Same", compute='_get_user_same')
    bool_dsa_true = fields.Boolean(string="BOOL", compute='_get_bool_dsa_true')
    is_bool_abrus_dsa = fields.Boolean(string="Boolean", compute='_get_boolean_value_dsa', default=False)
    is_send_approval_bool = fields.Boolean("Send For Approvals")
    nxt_user_id = fields.Many2many('res.users', string='Responsible', track_visibility='always')
    card_type = fields.Many2one('card.type.abrus', string="Product")
    salary = fields.Integer(string="Salary")
    card_variant = fields.Many2one('card.variant.abrus', string="Card Variant")
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', default='single', tracking=True)
    dob_abrus = fields.Date("Date Of Birth")
    uae_vintage = fields.Char(string="UAE Vintage")
    years_1 = fields.Selection([(str(num), str(num)) for num in range(1960, datetime.now().year + 10)], string='Year')
    month_1 = fields.Selection([
        ('jan', 'January'),
        ('feb', 'February'),
        ('march', 'March'),
        ('april', 'April'),
        ('may', 'May'),
        ('june', 'June'),
        ('july', 'July'),
        ('aug', 'August'),
        ('sept', 'September'),
        ('oct', 'October'),
        ('nov', 'November'),
        ('dec', 'December')
    ], string='Month', tracking=True)
    type_of_residence = fields.Many2one('residence.abrus', string="Type Of Residence")
    residence_emirates = fields.Char(string="Residence Emirate")
    fixed_income = fields.Integer(string="Fixed Income")
    existing_total_credit = fields.Char(string="Existing Total Credit Card Limit")
    existing_total_loans_emi = fields.Selection([
        ('no', 'No'),
        ('yes', 'Yes'),
    ], string='Existing Total Loans EMI', default='no', tracking=True)
    dbr_per = fields.Char(string="DBR %")
    olc_last_3_months = fields.Char(string="OLC in Last 3 months?")
    cheque_bounce = fields.Char("Cheque bounce in last 6 months ?")
    applied_pl = fields.Char("Applied PL or CC within last 30 days ?")
    email_id = fields.Char("Email ID Personal")
    mobile = fields.Char("Mobile Number", size=11)
    nationality = fields.Many2one('res.country', string="Nationality")
    emirates_id_num = fields.Char("Emirates ID Number")
    emirates_id_expiry = fields.Date(string="Emirates ID Expiry Date")
    passport_num = fields.Char("Passport Number")
    passport_expiry = fields.Date("Passport Expiry")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    ], string='Gender', default='male', tracking=True)
    office_num = fields.Char("Office Number")
    wrk_email = fields.Char("Work Email")
    salaried = fields.Selection([
        ('salaried', 'Salaried'),
        ('self_employed', 'Self Employed'),

    ], string='Salaried/Self-Employed', default='salaried', tracking=True)
    company_name = fields.Char("Company Full Name")
    comapny_website = fields.Char("Company Website")
    company_address = fields.Char("Company Address")
    # Address Feilds
    street_dsa = fields.Char('Street', readonly=False, store=True)
    street2_dsa = fields.Char('Street2', readonly=False, store=True)
    zip_dsa = fields.Char('Zip', readonly=False, store=True)
    city_dsa = fields.Char('City', readonly=False, store=True)
    state_dsa_id = fields.Many2one(
        "res.country.state", string='State',
        readonly=False, store=True,
        domain="[('country_id', '=?', country_dsa_id)]")
    country_dsa_id = fields.Many2one(
        'res.country', string='Country',
        readonly=False, store=True)

    designation = fields.Char("Designation")
    length_service = fields.Char("Length Of Service")
    year_2 = fields.Selection([(str(num), str(num)) for num in range(1960, datetime.now().year + 10)], string='Year')
    month_2 = fields.Selection([
        ('jan', 'January'),
        ('feb', 'February'),
        ('march', 'March'),
        ('april', 'April'),
        ('may', 'May'),
        ('june', 'June'),
        ('july', 'July'),
        ('aug', 'August'),
        ('sept', 'September'),
        ('oct', 'October'),
        ('nov', 'November'),
        ('dec', 'December')
    ], string='Month', tracking=True)
    Dob = fields.Date("Date Of Joining")
    security_check = fields.Selection([
        ('no', 'No'),
        ('yes', 'Yes'),

    ], string='Security Cheque Availabilty', default='yes', tracking=True)
    company_ac = fields.Char("Company A/C BANK – IBAN NO")
    bank = fields.Char("Bank")
    iban = fields.Char("IBAN")
    home_country = fields.Char("Home Country Address")
    # Address Feilds
    street_home_dsa = fields.Char('Street', readonly=False, store=True)
    street2_dsa_home = fields.Char('Street2', readonly=False, store=True)
    zip_dsa_home = fields.Char('Zip', readonly=False, store=True)
    city_dsa_home = fields.Char('City', readonly=False, store=True)
    state_dsa_home_id = fields.Many2one(
        "res.country.state", string='State',
        readonly=False, store=True,
        domain="[('country_id', '=?', country_dsa_home_id)]")
    country_dsa_home_id = fields.Many2one(
        'res.country', string='Country',
        readonly=False, store=True)
    name_home_country_ref = fields.Char("Name")
    mob_home_country_ref = fields.Char("Mob.No", size=11)
    home_country_ref = fields.Char("Home country Reference Friend /Relative")
    uae_frnd = fields.Char("UAE Reference Friend /Relative")
    name_uae_frnd = fields.Char("Name")
    mob_uae_frnd = fields.Char("Mob.No", size=11)
    uae_home_add = fields.Char("UAE Home Address")
    # Address Feilds
    street_dsa_uae = fields.Char('Street', readonly=False, store=True)
    street2_dsa_uae = fields.Char('Street2', readonly=False, store=True)
    zip_dsa_uae = fields.Char('Zip', readonly=False, store=True)
    city_dsa_uae = fields.Char('City', readonly=False, store=True)
    state_dsa_uae_id = fields.Many2one(
        "res.country.state", string='State',
        readonly=False, store=True,
        domain="[('country_id', '=?', country_dsa_uae_id)]")
    country_dsa_uae_id = fields.Many2one(
        'res.country', string='Country',
        readonly=False, store=True)

    fst_name = fields.Char("First Name")
    lst_name = fields.Char("Last Name")
    relationship = fields.Char("Relationship")
    pass_num = fields.Char("Passport Number")
    date_birth = fields.Date("Date Of Birth")
    credit_limit_1 = fields.Char("Credit Limit")
    fst_name_2 = fields.Char("First Name")
    last_name_2 = fields.Char("Last Name")
    relationship_2 = fields.Char("Relationship")
    pass_2 = fields.Char("Passport Number")
    dob_2 = fields.Date("Date Of Birth")
    credit_lim = fields.Char("Credit Limit")

    def _check_kyc_need(self):
        kyc = self.env['ir.config_parameter'].sudo().get_param('crmsuite_custom.is_kyc_details')
        if kyc:
            return True
        else:
            return False

    is_need_kyc = fields.Boolean(string="Need KYC", default=_check_kyc_need)
    kyc_company_id = fields.Many2one('res.company', string="Company")
    kyc_company_name = fields.Char(string="Company Name")
    kyc_company_office_no = fields.Char(string="Office No.")
    kyc_company_building = fields.Char(string="Building Name")
    kyc_company_street = fields.Char(string="Street")
    kyc_company_emirates = fields.Char(string="Emirates")

    kyc_residency_flat = fields.Char(string="Flat/Villa")
    kyc_residency_building = fields.Char(string="Building Name")
    kyc_residency_street = fields.Char(string="Street")
    kyc_residency_emirates = fields.Char(string="Emirates")
    kyc_company_mobile = fields.Char(string="Mobile")
    kyc_company_email = fields.Char(string="Email")
    kyc_home_country_no = fields.Char(string="Home Country No.")
    kyc_company_po_box = fields.Char(string="PO BOX")
    kyc_mother_name = fields.Char(string="Signatory Mothers Name")
    kyc_source_of_fund = fields.Selection([('existing_business', 'Existing Business'), ('salaried', 'Salaried'),
                                           ('running_business', 'Running Business'),
                                           ('bank_statement', 'Bank Statement')], string='Source Of fund ')
    kyc_qualification = fields.Selection([('graduate', 'Graduate'), ('under_graduate', 'Under Graduate')],
                                         string="Qualification")
    kyc_currency_id = fields.Many2one('res.currency', string="Currency Required")
    kyc_yrly_turn_over = fields.Float(string="Yearly Turn Over")
    kyc_monthly_cash_per = fields.Float(string="Cash")
    kyc_monthly_non_cash_per = fields.Float(string="Non Cash")
    # kyc_business_activity = fields.Text(string="Business Activity")
    kyc_business_activity = fields.Html(string="Business Activity")
    kyc_personal_experience = fields.Html(string="Personal Experience: Since In UAE - ")
    kyc_cust_line_id = fields.One2many('lead.kyc.cust.details', 'opportunity_id', string="Customer Details")
    kyc_suppl_line_id = fields.One2many('lead.kyc.suppl.details', 'opportunity_id', string="Supplier Details")
    kyc_customer_name = fields.Char(string="Name")
    kyc_date = fields.Date(string="Date", default=fields.date.today())
    crm_lead_lead_seq = fields.Char(string="Lead")
    trade_license_no = fields.Char(string="TL No.")
    referred_id = fields.Many2one('lead.referred', string="Referred By")
    lead_requested_amt = fields.Float(string="Requested Amount")
    lead_tenure_amt = fields.Float(string="Tenure")
    partner_mobile = fields.Char(string="Mobile")
    partner_email = fields.Char(string="Email")
    lead_activity_id = fields.Many2one('lead.lead_activity', string="Lead Activity")
    is_approved_stage = fields.Boolean(string="Is Approved Stage", compute="check_approved_stage")
    is_expected_revenue = fields.Boolean(string="Expected Revenue", compute="need_expected_revenue")
    approved_amt = fields.Float(string="Approved Amount")
    interest_rate = fields.Float(string="Interest Rate")
    processing_fee = fields.Float(string="Processing Fee")
    bank_cordinator_id = fields.Many2one('lead.bank.cordinator', string="Bank Cordinator")
    is_need_amt_details = fields.Boolean(string="Show Amount/Fee", related='card_type.is_need_amt_details')
    is_converted_stage = fields.Boolean(string="Converted Stage")
    is_declined_stage = fields.Boolean(string="Declined Stage")
    is_converted_declined_stage = fields.Boolean(string="Converted/Declined Stage")
    is_approved_oppor = fields.Boolean(string="Approved Stage")
    team_lead_ids = fields.Many2many('res.users', string="Lead Teams", compute="get_lead_teams")
    lead_team_ids = fields.Many2many('res.users', 'lead_res_user_rel', 'lead_id', 'user_id', string="Lead Teams")
    lead_comment_ids = fields.One2many('lead.comments.details', 'opportunity_id', string="Comments")
    photo_attach_ids = fields.Many2many('ir.attachment', string="photos", tracking=True)
    document_attach_ids = fields.Many2many('ir.attachment', 'attachment_lead_rel' 'lead_id', 'attachment_id',
                                           string="Documents", tracking=True)
    location_url = fields.Char(string="Location")
    stage_ids = fields.Many2many('crm.stage', 'lead_leag_stage_rel', 'lead_id', 'crm_stages_id',
                                 string="Product Stages", compute="get_crm_stages")
    stage_id = fields.Many2one('crm.stage', string='Stages', index=True, tracking=True, readonly=False,
                               copy=False, ondelete='restrict')

    partner_id = fields.Many2one(
        'res.partner', string='Customer', check_company=True, index=True, tracking=10,
        domain="[('name', '=', False)]",
        help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")

    # lead_street = fields.Char(string="Address")
    # lead_street2 = fields.Char(string="Street2")
    # lead_city = fields.Char(string="City")
    # lead_state_id = fields.Many2one('res.country.state', string="State")
    # lead_country_id = fields.Many2one('res.country', string="Country")

    # @api.depends('team_id', 'type')
    # def _compute_stage_id(self):
    #     for lead in self:
    #         if not lead.stage_ids and lead.card_type:
    #             lead.stage_ids = [(4, st.id) for st in lead.card_type.stage_ids]
    # lead.stage_id = lead._stage_find(domain=[('fold', '=', False)]).id

    def get_crm_stages(self):
        for rec in self:
            if rec.card_type:
                rec.stage_ids = [(4, st.id) for st in rec.card_type.stage_ids]

    def get_lead_teams(self):
        for rec in self:
            if rec.team_id:
                team_members = self.env['crm.team'].sudo().search([('id', '=', rec.team_id.id)])
                rec.team_lead_ids = [(4, team_members.user_id.id)]
                for member in team_members.member_ids:
                    rec.team_lead_ids = [(4, member.id)]
            else:
                rec.team_lead_ids = False

    def need_expected_revenue(self):
        for rec in self:
            expected_revenue = self.env['ir.config_parameter'].sudo().get_param(
                'crmsuite_custom.is_need_expected_revenue')
            rec.is_expected_revenue = True if expected_revenue else False

    def name_get(self):
        result = []
        for rec in self:
            name = rec.card_type.card_type_name if rec.card_type else False
            result.append((rec.id, name))
        return result

    @api.onchange('stage_id')
    def onchange_stage_id(self):
        for rec in self:
            rec.is_converted_stage = True if rec.stage_id.is_converted_stage else False
            rec.is_declined_stage = True if rec.stage_id.is_declined_stage else False
            rec.is_converted_declined_stage = True if rec.stage_id.is_converted_stage or rec.stage_id.is_declined_stage else False
            rec.is_approved_oppor = True if rec.stage_id.is_oppor_approved_stage else False

    @api.model
    def create(self, vals):
        res = super(CRMLead, self).create(vals)
        if res.type == 'lead':
            lead_sequence = self.env['ir.sequence'].next_by_code('crm.lead.lead_seq')
            res.crm_lead_lead_seq = lead_sequence
        if res.team_id:
            team_members = self.env['crm.team'].sudo().search([('id', '=', res.team_id.id)])
            res.lead_team_ids = [(4, team_members.user_id.id)]
            for member in team_members.member_ids:
                res.lead_team_ids = [(4, member.id)]
        return res

    def check_approved_stage(self):
        for rec in self:
            rec.is_approved_stage = True if rec.stage_id.is_approved_stage else False


class LeadKYCCustDetails(models.Model):
    _name = 'lead.kyc.cust.details'

    opportunity_id = fields.Many2one('crm.lead', string="opportunity")
    customer_name = fields.Char(string="Customers")
    company_name = fields.Char(string="Company")
    cust_country_id = fields.Many2one('res.country', string="Country")


class LeadKYCSupplDetails(models.Model):
    _name = 'lead.kyc.suppl.details'

    opportunity_id = fields.Many2one('crm.lead', string="opportunity")
    supplier_name = fields.Char(string="Suppliers")
    company_name = fields.Char(string="Company")
    suppl_country_id = fields.Many2one('res.country', string="Country")


class LeadReferred(models.Model):
    _name = 'lead.referred'

    name = fields.Char(string="Referred")


class LeadActivity(models.Model):
    _name = 'lead.lead_activity'

    name = fields.Char(string="Lead Activity")


class LeadBankCordinator(models.Model):
    _name = 'lead.bank.cordinator'

    name = fields.Char(string="Bank Cordinator")


class CRMTeam(models.Model):
    _inherit = 'crm.team'

    @api.model
    def _action_update_to_pipeline(self, action):
        res = super(CRMTeam, self)._action_update_to_pipeline(action)
        res['domain'] = [('is_converted_declined_stage', '=', False)]
        return res

    @api.model
    def action_converted_pipeline(self):
        action = self.env["ir.actions.actions"]._for_xml_id("crmsuite_custom.crm_converted_lead_action_pipeline")
        return action

    @api.model
    def action_declined_pipeline(self):
        action = self.env["ir.actions.actions"]._for_xml_id("crmsuite_custom.crm_declined_lead_action_pipeline")
        return action


class LeadCommentsData(models.Model):
    _name = 'lead.comments.details'

    opportunity_id = fields.Many2one('crm.lead', string="opportunity")
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    comment_date = fields.Datetime(string='Date', index=True, default=fields.Datetime.now)
    comments = fields.Text(string="Comments")
    check_group = fields.Boolean(compute='_get_group_check')

    def _get_group_check(self):
        for rec in self:
            if rec.env.user.has_group('crmsuite_custom.edit_comments_group'):
                rec.check_group = True
            else:
                rec.check_group = False

    # def write(self, values):
    #     # Check if the user belongs to the specified group
    #     edit_comments_group = self.env.ref('crmsuite_custom.edit_comments_group')
    #     if not edit_comments_group or not self.env.user.has_group('crmsuite_custom.edit_comments_group'):
    #         raise ValidationError("You cannot edit the comments. Please contact the administrator!")
    #
    #     return super(LeadCommentsData, self).write(values)
    #     return super(LeadCommentsData, self).write()

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     result = super(LeadCommentsData, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
    #                                                            submenu=submenu)
    #
    #     # Check if the user belongs to the specified group
    #     edit_comments_group = self.env.ref('crmsuite_custom.edit_comments_group')
    #     if not edit_comments_group or not self.env.user.has_group(edit_comments_group.id):
    #         doc = etree.XML(result['arch'])
    #
    #         # Disable the 'comments' field for users without the group
    #         comments_field = doc.xpath("//field[@name='comments']")
    #         for field in comments_field:
    #             field.set('readonly', '1')
    #
    #         result['arch'] = etree.tostring(doc)
    #
    #     return result

    # def current_user_datetime(self):
    #     user_tz = tz.gettz(self.env.user.tz)
    #     std_tz = tz.gettz('UTC')
    #     userdatetime = fields.datetime.now().replace(tzinfo=std_tz).astimezone(user_tz).replace(tzinfo=None)
    #     print(userdatetime)
    #     self.comments_date = userdatetime
