from odoo import api, fields, models
from datetime import date

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    productivity_today = fields.Float(
        string='Productivity Today (kg)',
        compute='_compute_productivity_today',
        store=True
    )
    productivity_this_month = fields.Float(
        string='Productivity This Month (kg)',
        compute='_compute_productivity_this_month',
        store=True
    )

    @api.depends('x_productivity_ids.total_kg', 'x_productivity_ids.date')
    def _compute_productivity_today(self):
        today = date.today()
        for emp in self:
            total = sum(
                emp.x_productivity_ids.filtered(lambda r: r.date == today).mapped('total_kg')
            )
            emp.productivity_today = total

    @api.depends('x_productivity_ids.total_kg', 'x_productivity_ids.date')
    def _compute_productivity_this_month(self):
        today = date.today()
        for emp in self:
            total = sum(
                emp.x_productivity_ids.filtered(
                    lambda r: r.date and r.date.month == today.month and r.date.year == today.year
                ).mapped('total_kg')
            )
            emp.productivity_this_month = total

    x_productivity_ids = fields.One2many('x_productivity', 'employee_id', string='Productivity Records')
