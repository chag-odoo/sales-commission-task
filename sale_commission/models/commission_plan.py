from odoo import api,fields,models,_
from odoo.exceptions import UserError, ValidationError


class CommissionPlan(models.Model):
    _name='commission.plan'
    _description='Commission Plan'

    name = fields.Char(string='Commission Plan',required=True)
    company_id = fields.Many2one('res.company', string='Company Name', required=True, default=lambda self: self.env.company)
    start_date = fields.Date(string='Start Date',default=fields.Date.today())
    end_date = fields.Date(string='End Date')
    target = fields.Integer(string='Target', compute='_compute_total_target')
    stage = fields.Selection([('draft', 'Draft'),('approved', 'Approved'),('done', 'Done'),('cancelled', 'Cancelled')], default='draft')

    product_ids = fields.Many2many('product.product',string='Products')
    sales_team_id = fields.Many2one('crm.team',string='Sales Team',required=True)
    salesperson_id = fields.Many2one('res.users',string='Salespersons')
    active = fields.Boolean(default=True)

    commission_ids = fields.One2many('commission.sale', 'commission_plan_id', string='Commission') 
    target_ids = fields.One2many('commission.target', 'commission_plan_id', string='Targets')


    # @api.depends('sales_team_id','salesperson_id')
    # def _compute_display_name(self):
    #     for record in self:
    #         record.display_name = f"{record.salesperson_id.name}{record.sales_team_id.name}"

    def action_approve(self): 
        for record in self: 
            if record.stage=='cancelled':
                raise ValidationError("Cannot approve cancelled plan.") 
            elif record.stage=='approved':
                raise ValidationError("The plan is already approved.") 
            elif record.stage=='done':
                raise ValidationError("Plan already done") 
        record.stage='approved' 
            
    def action_cancel(self): 
        for record in self: 
            if record.stage=='done': 
                raise ValidationError("Plan is already done so cannot be cancelled.") 
        record.stage='cancelled'
        return True

    @api.depends('target_ids') 
    def _compute_total_target(self): 
        self.target = sum(self.target_ids.mapped('q_target')) 
