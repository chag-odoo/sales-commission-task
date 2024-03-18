from odoo import fields, models, api
from odoo.exceptions import ValidationError

class CommissionPlanReport(models.Model):
    _name = "commission.plan.report"
    _description = "Sales Commission Plan Report"

    commission_plan_id = fields.Many2one('commission.plan', string="Commission Plan")
    target_id = fields.Many2one('commission.target', string="Quarterly Target")
    target_value = fields.Float(compute='_compute_display_value')
    salesperson_id = fields.Many2one('res.users', string="Salesperson", compute='_compute_display_value')
    sales_team_id = fields.Many2one('crm.team', string="Team", compute='_compute_display_value')
    achieved_amount = fields.Float(compute='_compute_achieved_amount')
    com_rate = fields.Float(string="Commission Rate",compute='_compute_commission_rate')

    @api.depends('target_id', 'commission_plan_id')
    def _compute_display_value(self):
        for record in self:
            record.target_value = record.target_id.q_target
            record.salesperson_id = record.commission_plan_id.salesperson_id
            record.sales_team_id = record.commission_plan_id.sales_team_id


    @api.depends("commission_plan_id", "target_id")
    def _compute_achieved_amount(self):
        for record in self:
            orders = self.env['sale.order.line'].search([
                ('salesman_id', '=', record.commission_plan_id.salesperson_id.id),
                ('order_id.date_order', '>=', record.target_id.q_start_date),
                ('order_id.date_order', '<=', record.target_id.q_end_date),
                ('product_id', 'in', record.commission_plan_id.product_ids.ids)
            ])
            record.achieved_amount = sum(order.price_subtotal for order in orders)  

    @api.depends('commission_plan_id','achieved_amount','target_value')
    def _compute_commission_rate(self):
        for record in self:
            expected_com_rate = 0
            if record.commission_plan_id and record.target_value:
                achievement_percent = (record.achieved_amount/record.target_value)*100
                for commission in record.commission_plan_id.commission_ids:
                    if commission.min_achievement <= achievement_percent:
                        expected_com_rate = max(expected_com_rate, commission.commission_rate)
            record.com_rate = expected_com_rate