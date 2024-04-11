from odoo.tests import TransactionCase
from odoo.fields import Date


class TestRequirements(TransactionCase):

    def setUp(self):
        super().setUp()
        self.requirements_obj = self.env['requirements']

    def test_set_progress(self):
        record = self.requirements_obj.create({
            'state': 'new',
            'name': 'nombre'})
        record.set_progress()
        self.assertEqual(record.state, 'progress')

    def test_set_done(self):
        record = self.requirements_obj.create({
            'state': 'new',
            'name': 'nombre'})
        record.set_done()
        self.assertEqual(record.state, 'done')

    def test_compute_dedicated_time(self):
        record = self.requirements_obj.create({
                    'name': 'nombre'
                    })
        self.env['requirements.action'].create({
            'dedicated_time': 10,
            'requirements_id': record.id})
        self.env['requirements.action'].create({
            'dedicated_time': 20,
            'requirements_id': record.id})
        record._compute_dedicated_time()

        self.assertEqual(
            record.dedicated_time, 30)

    def test_set_dedicated_time(self):
        record = self.requirements_obj.create({
            'name': 'nombre',
            'dedicated_time': 20
        })
        record._set_dedicated_time()
        self.assertEqual(record.dedicated_time, 20)

        computed_time = sum(record.action_ids.mapped('dedicated_time'))
        self.assertEqual(record.dedicated_time, computed_time, "El tiempo dedicado no se actualizó correctamente")

        self.assertTrue(record.action_ids, "No se han creado acciones relacionadas")
        self.assertEqual(record.action_ids.date, Date.today())

    def test_search_dedicated_time(self):
        record1 = self.requirements_obj.create({
            'name': 'requisito1',
            'dedicated_time': 10
        })
        record2 = self.requirements_obj.create({
            'name': 'requisito2',
            'dedicated_time': 20
        })
        record3 = self.requirements_obj.create({
            'name': 'requisito3',
            'dedicated_time': 30
        })

        search_domain = record1._search_dedicated_time('=', 20)
        self.assertEqual(search_domain, [('id', 'in', [record2.id])], "La búsqueda con '=' y el valor 20 no devolvió los resultados esperados")

        search_domain = record1._search_dedicated_time('>', 20)
        self.assertEqual(search_domain, [('id', 'in', [record3.id])], "La búsqueda con '>' y el valor 20 no devolvió los resultados esperados")

        search_domain = record1._search_dedicated_time('<', 20)
        self.assertEqual(search_domain, [('id', 'in', [record1.id])], "La búsqueda con '<' y el valor 20 no devolvió los resultados esperados")

    def test_check_create_requirement(self):
        # Conjunto de requisitos
        requirements_records = self.env['requirements'].search([])
        # Longitud (cantidad de requisitos totales)
        self.assertEqual(len(requirements_records), 0)
        # Crear un nuevo requisito
        requirement1 = self.requirements_obj.create({
            'name': 'Nuevo Requisito',
            'dedicated_time': 10,
            'related_actions': [
                (0, 0, {
                    'name': 'Acción 1',
                }),]
        })

        requirements_records = self.env['requirements'].search([])
        self.assertEqual(len(requirements_records), 1)

        self.assertEqual(len(requirement1.related_actions), 1, "No hay acciones")
        self.assertEqual(requirement1.related_actions.name, 'Acción 1', "Nombre acción no adecuado")

        requirement1.write({
            'related_actions': [(0, 0, {
                'name': 'Otra Acción',
            })],
        })
        self.assertEqual(len(requirement1.related_actions), 2, "Nº de acciones no adecuado")

    def test_compute_assigned(self):
        record = self.requirements_obj.create({
            'name': 'nombre'
        })
        # Si no tiene usuario el estado no debe ser assigned
        self.assertNotEqual(record.state, 'assigned')
        # Estado inicial deber ser new
        self.assertEqual(record.state, 'new')

        # Si tiene usuario asignado el estado debe ser assigned
        new_user = {
            'id': 1,  # Simulamos un ID para el usuario
            'name': 'Nuevo Usuario de Prueba',
        }

        record.user_id = new_user['id']
        self.assertEqual(record.state, 'assigned')

    def test__compute_is_done(self):
        record = self.requirements_obj.create({
            'name': 'nombre',
            'state': 'new'
        })

        self.assertFalse(record.is_done, "is_done debería ser False para un estado diferente de 'done'")

        record.state = 'done'

        self.assertTrue(record.is_done, "is_done debería ser True para el estado 'done'")

