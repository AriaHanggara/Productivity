from odoo import api, fields, models
from datetime import date

class Productivity(models.Model):
    _name = 'x_productivity'
    _description = 'Daily Employee Productivity'
    _order = 'date desc'

    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    total_productivity = fields.Float(string='Total Productivity', required=True, default=0.0)
    uom = fields.Selection([('gr', 'Gram'), ('kg', 'Kilogram')], string='Unit of Measure', required=True, default='kg')
    job_position_id = fields.Char(related='employee_id.job_id.name', string='Job Position')
    total_kg = fields.Float(string='Total (kg)', compute='_compute_total_kg', store=True)

    @api.depends('total_productivity', 'uom')
    def _compute_total_kg(self):
        for record in self:
            record.total_kg = record.total_productivity / 1000 if record.uom == 'gr' else record.total_productivity

    # ---- Synchronization with employee aggregates ----
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._update_employee_productivity()
        return records

    def write(self, vals):
        res = super().write(vals)
        self._update_employee_productivity()
        return res

    def unlink(self):
        employees = self.mapped('employee_id')
        res = super().unlink()
        employees._compute_productivity_today()
        employees._compute_productivity_this_month()
        return res

    def _update_employee_productivity(self):
        employees = self.mapped('employee_id')
        employees._compute_productivity_today()
        employees._compute_productivity_this_month()
