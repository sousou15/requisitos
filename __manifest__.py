# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Requisitos",
    "summary": "Módulo para gestionar requisitos",
    "version": "12.0.1.0.0",
    # see https://odoo-community.org/page/development-status
    "category": "Lista",
    "website": "https://github.com/OCA/helpdesk",
    "author": "Youssef, Trey, Odoo Community Association (OCA)",
    # see https://odoo-community.org/page/maintainer-role for a description of the maintainer role and responsibilities
    "maintainers": ["sousou15"],
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": [
        "base",
        "mail",
    ],
    "data": [
        "security/requisitos_security.xml",
        "security/ir.model.access.csv",
        "views/templates.xml",
        "views/requisitos_views.xml",
        "views/requisitos_action_views.xml",
    ],
}
