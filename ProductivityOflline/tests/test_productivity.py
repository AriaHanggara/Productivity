from odoo.tests.common import TransactionCase

class TestProductivity(TransactionCase):
    def setUp(self):
        super(TestProductivity, self).setUp()
        # Set up initial data for tests
        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
            'job_id': self.env['hr.job'].create({'name': 'Test Job'}).id,
        })
        self.productivity_record = self.env['x_productivity'].create({
            'employee_id': self.employee.id,
            'date': '2025-10-31',
            'total_productivity': 8,
            'uom': 'gr',
        })

    def test_productivity_creation(self):
        record = self.env['x_productivity'].search([('employee_id', '=', self.employee.id)])
        self.assertEqual(len(record), 1)
        self.assertEqual(record.total_productivity, 8)
        self.assertEqual(record.uom, 'gr')

    def test_productivity_conversion_kg(self):
        record = self.productivity_record
        self.assertEqual(record.total_productivity_in_kg, 0.008)

    def test_employee_productivity_aggregates(self):
        self.employee._compute_productivity_aggregates()
        self.assertEqual(self.employee.productivity_today, 0.008)
        self.assertEqual(self.employee.productivity_this_month, 0.008)

    def test_update_productivity(self):
        self.productivity_record.write({
            'total_productivity': 100,
            'uom': 'kg',
        })
        self.assertEqual(self.productivity_record.total_productivity_in_kg, 100)
    
