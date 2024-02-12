from unittest import TestCase
from app import app
from flask import session, jsonify
from boggle import Boggle


class FlaskTests(TestCase):

    def test_display_boggle(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('<h1>Boggle Game</h1>', html)
    
    def test_session_count(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['count'] = 2

            res = client.get('/')

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['count'], 3)
    
    def test_word_validation_not_on_board(self):
        with app.test_client() as client:
            with client.session_transaction() as cl_session:
                cl_session['board'] = [["D", "O", "L", "L", "X"],
                ["D", "O", "L", "L", "X"],
                ["D", "O", "L", "L", "X"],
                ["D", "O", "L", "L", "X"],
                ["D", "O", "L", "L", "X"] ]
        
        res = client.get('/check-word/cat')    
        self.assertEqual(res.json['result'], 'not-on-board')
    
    def test_word_validation_ok(self):
        with app.test_client() as client:
            with client.session_transaction() as cl_session:
                cl_session['board'] = [["D", "O", "L", "L", "X"],
                ["D", "O", "L", "L", "X"],
                ["D", "O", "L", "L", "X"],
                ["D", "O", "L", "L", "X"],
                ["D", "O", "L", "L", "X"] ]
        
        res = client.get('/check-word/doll')    
        self.assertEqual(res.json['result'], 'ok')
    
    def test_word_validation_not_word(self):
        with app.test_client() as client:
            with client.session_transaction() as cl_session:
                cl_session['board'] = [["D", "O", "L", "L", "X"],
                ["D", "O", "L", "L", "X"],
                ["D", "O", "L", "L", "X"],
                ["D", "O", "L", "L", "X"],
                ["D", "O", "L", "L", "X"] ]
        
        res = client.get('/check-word/asdss')    
        self.assertEqual(res.json['result'], 'not-word')