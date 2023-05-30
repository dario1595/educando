from django.test import TestCase, Client
from rest_framework import status

class MisCursosViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Aquí puedes configurar los datos necesarios para tus pruebas, como usuarios, tokens, etc.

    def test_mis_cursos_view_with_valid_token(self):
        # Obtén un token válido para la prueba
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZF91c3VhcmlvIjoxMywiZW1haWwiOiJEYXJpb0BnbWFpbC5jb20iLCJub21icmUiOiJEYXJpbyIsImV4cCI6MTY4NTQ4NzU3NH0.RZKr0-n40K1TQsd4iECZmCFZhz7fd-of-b8DWhJ5xZA"

        # Realiza una solicitud GET a la vista con el token válido
        response = self.client.get('mis_cursos/', HTTP_AUTHORIZATION=f'Bearer {token}')

        # Verifica que la respuesta tenga un código de estado 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Realiza las comprobaciones adicionales según tus expectativas

    def test_mis_cursos_view_with_invalid_token(self):
        # Obtén un token inválido para la prueba
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZF91c3VhcmlvIjoxMywiZW1haWwiOiJEYXJpb0BnbWFpbC5jb20iLCJub21icmUiOiJEYXJpbyIsImV4cCI6MTY4NTQ4NzU3NH0.RZKr0-n40K1TQsd4iECZmCFZhz7fd-of-b8DWhJ5xZA"

        # Realiza una solicitud GET a la vista con el token inválido
        response = self.client.get('mis_cursos/', HTTP_AUTHORIZATION=f'Bearer {token}')

        # Verifica que la respuesta tenga un código de estado 401 (No autorizado)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Realiza las comprobaciones adicionales según tus expectativas

