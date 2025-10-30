{
    'name': 'Productivity',
    'author': 'Gili',
    'version': '1.0',
    'category': 'Human Resources',
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/prod_rec.xml',
        'views/menu.xml',
        # 'views/productivity_form_view.xml',
        # 'views/productivity_list_view.xml',
        # 'views/productivity_pivot_view.xml',
    ],
    'application': True,
    'installable': True,
}
