from odoo import fields,models

class SalesTargets(models.Model): 
    _name = 'commission.target' 
    _description = 'Sales Targets'
    
    period = fields.Char(string='Quarter') 
    q_start_date = fields.Date(string='Start Date') 
    q_end_date = fields.Date(string='End Date') 
    q_target = fields.Integer(string='Amount')
     
    commission_plan_id = fields.Many2one('commission.plan')