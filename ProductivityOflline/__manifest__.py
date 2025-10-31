{
    'name': 'Productivity',
    'author': 'Gili',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'description': """
        This module purpose for test in Indev, thankyou
    """,
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/prod_rec.xml',
        'views/menu.xml',
    ],
    'application': True,
    'installable': True,
}
