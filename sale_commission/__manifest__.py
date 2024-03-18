{
    'name': "Sale Commission",
    'version': '17.0.0.1.0',
    'author': "Chirayu Agrawal",

    'depends': ['base','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/commission_plan_views.xml',
        'views/commission_sale_views.xml',
        'views/commission_target_views.xml',
        'views/commission_plan_report_views.xml',
        'views/commission_menus.xml',
    ],
    'application':True,
    'installable':True
    
}
