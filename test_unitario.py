from unittest.mock import patch
from flask import Flask
from app import app, get_songs_response
import unittest

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_songs_response(self):
        artist_name = 'Led Zeppelin'

        with patch('app.retrieve_songs_from_genius_api') as mock_get_songs:
            mock_get_songs.return_value = ['Stairway to Heaven', 'Black Dog', 'Kashmir']


            print('Realizando requisição GET... CACHE=FALSE')
            response = self.app.get(f'/popular_songs/{artist_name}?cache=false')
            if not response:
                print('Requisição sucedida CACHE=FALSE')

            print('Realizando requisição GET... CACHE=TRUE')
            response = self.app.get(f'/popular_songs/{artist_name}?cache=true')
            if not response:
                print('Requisição sucedida CACHE=TRUE')

            

            print('Verificando resposta da requisição...')
            # Verifica se a resposta foi 200 OK
            self.assertEqual(response.status_code, 200)

            # Verifica se a resposta contém a lista de músicas retornadas
            expected_response = ['Stairway to Heaven', 'Black Dog', 'Kashmir']
            self.assertEqual(response.json, expected_response)

            # Verifica se a função get_songs_from_genius foi chamada corretamente
            mock_get_songs.assert_called_once_with(artist_name)

if __name__ == '__main__':
    unittest.main()
