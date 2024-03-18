from odoo import fields, models

class SalesCommissions(models.Model): 
    _name = 'commission.sale' 
    _description = 'Sales Commissions'

    min_achievement = fields.Float(string='Minimum Achievement') 
    commission_percent = fields.Float(string="Commission Percent") 
    commission_plan_id = fields.Many2one('commission.plan')