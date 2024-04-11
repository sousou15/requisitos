from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class RequirementsAction(models.Model):
    _name = 'requirements.action'
    _description = 'Requirements Action'

    name = fields.Char()
    date = fields.Date()
    dedicated_time = fields.Float(
        string='Time',
    )
    requirements_id = fields.Many2one(
        comodel_name='requirements')


class Requirements(models.Model):
    _name = "requirements"
    _description = "Requirements"
    name = fields.Char(
        string="Name",
        required=True)
    description = fields.Text(string="Description")

    date = fields.Date(string="Date", track_visibility='onchange')
    date_due = fields.Date(string="Date Due")

    def _default_user_id(self):
        return self.env.user

    state = fields.Selection(
        [('new', 'New'),
         ('assigned', 'Assigned'),
         ('progress', 'On progress'),
         ('done', 'Done')],
        string='State',
        default='new'
    )

    # def set_assigned(self):
    #     self.ensure_one()
    #     self.write({
    #         'assigned': True,
    #         'state': 'assigned',
    #         'user_id': self.env.user.id
    #     })

    def set_progress(self):
        self.ensure_one()
        self.state = 'progress'

    def set_done(self):
        self.ensure_one()
        self.state = 'done'

    assigned = fields.Boolean(
        string="Assigned",
        compute='_compute_assigned',
        store=True)

    new_requirement_name = fields.Char(
        string='New tag',
    )
    action_ids = fields.One2many(
        comodel_name='requirements.action',
        inverse_name='requirements_id',
        string='Actions'
    )
    related_actions = fields.Many2many(
        comodel_name='requirements.action',
        relation='requirements_action_rel',  # Nombre de la tabla de relación
        column1='requirements_id',  # Campo que referencia al modelo actual (requirements)
        column2='action_id',  # Campo que referencia al modelo relacionado (Action)
        string='Related Actions'
    )

    dedicated_time = fields.Float(
        string="Time",
        compute="_compute_dedicated_time",
        inverse="_set_dedicated_time",
        search="_search_dedicated_time")

    @api.depends('action_ids.dedicated_time')
    def _compute_dedicated_time(self):
        for record in self:
            record.dedicated_time = sum(
                record.action_ids.mapped('dedicated_time')
            )

    def _search_dedicated_time(self, operator, value):
        action_ids = self.env['requirements.action'].search(
            [('dedicated_time', operator, value)]
            )
        return [('id', 'in', action_ids.mapped('requirements_id').ids)]

    def _set_dedicated_time(self):
        for record in self:
            computed_time = sum(record.action_ids.mapped('dedicated_time'))
            if self.dedicated_time != computed_time:
                values = {
                    'name': "Auto time",
                    'date': fields.Date.today(),
                    'requirements_id': record.id,
                    'dedicated_time': self.dedicated_time - computed_time
                }
                self.update({'action_ids': [(0, 0, values)]})

    requirements_id = fields.Many2one(
        comodel_name='requirements')

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assigned to',
        default=False)

    # def create_new_requirement(self):
    #     new_requirement = self.env['requirements'].create({
    #         'name': self.new_requirement_name,
    #         'date': fields.Date.today(),
    #     })
    #     # return new_requirement
    #     # self.write({
    #     #     'related_actions': [(4, new_requirement.id, 0)]
    #     # })
    # # def create_new_requirement_action(self):

    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            if record.user_id:
                record.assigned = True
                record.state = 'assigned'
            else:
                record.assigned = False
                record.state = 'new'

    is_done = fields.Boolean(
        string="Is Done",
        compute='_compute_is_done',
        store=True)

    @api.depends('state')
    def _compute_is_done(self):
        for record in self:
            record.is_done = record.state == 'done'
