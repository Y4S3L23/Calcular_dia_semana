from django.test import TestCase
from django.urls import reverse


class CalcularDiaTests(TestCase):
    def test_get_muestra_formulario(self):
        response = self.client.get(reverse('fecha:calcular_dia'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Calcular día de la semana')

    def test_fecha_conocida_miércoles(self):
        response = self.client.post(
            reverse('fecha:calcular_dia'),
            {'fecha': '2026-09-23'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'miércoles')
        self.assertContains(response, '23 de septiembre de 2026')

    def test_lunes(self):
        response = self.client.post(
            reverse('fecha:calcular_dia'),
            {'fecha': '2026-09-21'},
        )
        self.assertContains(response, 'lunes')

    def test_domingo(self):
        response = self.client.post(
            reverse('fecha:calcular_dia'),
            {'fecha': '2026-09-20'},
        )
        self.assertContains(response, 'domingo')

    def test_enero_se_come_de_ano_anterior(self):
        response = self.client.post(
            reverse('fecha:calcular_dia'),
            {'fecha': '2026-01-01'},
        )
        self.assertContains(response, 'jueves')

    def test_fecha_bisiesto_29_febrero(self):
        response = self.client.post(
            reverse('fecha:calcular_dia'),
            {'fecha': '2024-02-29'},
        )
        self.assertContains(response, 'jueves')

    def test_29_febrero_no_bisiesto_es_invalida(self):
        response = self.client.post(
            reverse('fecha:calcular_dia'),
            {'fecha': '2026-02-29'},
        )
        self.assertContains(response, 'La fecha ingresada no es válida.')

    def test_dia_fuera_de_rango_es_invalida(self):
        response = self.client.post(
            reverse('fecha:calcular_dia'),
            {'fecha': '2026-04-31'},
        )
        self.assertContains(response, 'La fecha ingresada no es válida.')

    def test_dias_eliminados_de_1582_son_invalidos(self):
        for dia in range(5, 15):
            response = self.client.post(
                reverse('fecha:calcular_dia'),
                {'fecha': f'1582-10-{dia:02d}'},
            )
            self.assertContains(response, 'La fecha ingresada no es válida.')

    def test_dia_4_de_octubre_1582_es_valido(self):
        response = self.client.post(
            reverse('fecha:calcular_dia'),
            {'fecha': '1582-10-04'},
        )
        self.assertContains(response, '4 de octubre de 1582')

    def test_dia_15_de_octubre_1582_es_valido(self):
        response = self.client.post(
            reverse('fecha:calcular_dia'),
            {'fecha': '1582-10-15'},
        )
        self.assertContains(response, 'viernes')

    def test_fecha_vacia_muestra_error(self):
        response = self.client.post(
            reverse('fecha:calcular_dia'),
            {'fecha': ''},
        )
        self.assertContains(response, 'Debes ingresar una fecha.')

    def test_fecha_invalida_muestra_error(self):
        response = self.client.post(
            reverse('fecha:calcular_dia'),
            {'fecha': 'no-es-fecha'},
        )
        self.assertContains(response, 'La fecha ingresada no es válida.')
