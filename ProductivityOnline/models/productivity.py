from odoo import models, fields, api 
from datetime import date

class Productivity(models.Model):
    _inherit = ['mail.thread']
    _name = 'x_productivity'
    _description = 'Productivity Record'

    # Fields definition
    date = fields.Date(string='Date', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    total_productivity = fields.Float(string='Total Productivity', required=True, default=0)
    uom = fields.Selection([
        ('gr', 'gr'),
        ('kg', 'kg'),
    ], string='UOM', tracking=True)

    total_productivity_in_kg = fields.Float(
        string='Total Productivity (kg)',
        compute='_compute_total_productivity_in_kg',
        store=True,
    )
    job_position_id = fields.Char(related='employee_id.job_id.name', string='Job Position')

    @api.depends('total_productivity', 'uom')
    def _compute_total_productivity_in_kg(self):
        for record in self:
            record.total_productivity_in_kg = record.total_productivity / 1000 if record.uom == 'gr' else record.total_productivity

    def create(self, vals_list):
        records = super().create(vals_list)
        records._update_employee_aggregates()
        return records

    def write(self, vals):
        res = super().write(vals)
        self._update_employee_aggregates()
        return res

    def unlink(self):
        employees = self.mapped('employee_id')
        res = super().unlink()
        employees._compute_productivity_aggregates()
        return res

    def _update_employee_aggregates(self):
        employees = self.mapped('employee_id')
        for emp in employees:
            emp._compute_productivity_aggregates()



class Employee(models.Model):
    _inherit = 'hr.employee'

    productivity_ids = fields.One2many('x_productivity', 'employee_id', string='Productivity Records')

    productivity_today = fields.Float(
        string='Productivity Today (kg)',
        compute='_compute_productivity_aggregates',
        store=True
    )
    productivity_this_month = fields.Float(
        string='Productivity This Month (kg)',
        compute='_compute_productivity_aggregates',
        store=True
    )

    @api.depends('productivity_ids', 'productivity_ids.total_productivity_in_kg', 'productivity_ids.date')
    def _compute_productivity_aggregates(self):
        today = date.today()
        for emp in self:
            records = emp.productivity_ids
            emp.productivity_today = sum(r.total_productivity_in_kg for r in records if r.date == today)
            emp.productivity_this_month = sum(
                r.total_productivity_in_kg for r in records
                if r.date and r.date.month == today.month and r.date.year == today.year
            )