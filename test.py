from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        '''This runs before every test'''
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_start(self):
        '''Test the landing page for different aspects of the HTML to be shown and that session is functioning'''
        with self.client:
            res = self.client.get('/')
            self.assertIn('board',session)

    def test_vaild_word(self):
        '''With sample board,check that word can be used'''
        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["D", "R", "A", "G", "T"], 
                                    ["G", "B", "E", "S", "N"], 
                                    ["O", "A", "M", "U", "K"], 
                                    ["F", "S", "T", "O", "B"], 
                                    ["C", "I", "H", "Z", "T"]]
        res = self.client.get('/check-word?word=drag')
        self.assertEqual(res.json['result'], 'ok')

    def test_invalid_word(self):
        '''Test if word is on the board'''
        self.client.get('/')
        res = self.client.get('/check-word?word=abracadabra')
        self.assertEqual(res.json['result'], 'not-on-board')

    def test_not_word(self):
        '''Test if gibberish is in dictionary'''
        self.client.get('/')
        res = self.client.get('/check-word?word=hfuoewncoiwnia')
        self.assertEqual(res.json['result'], 'not-word')
