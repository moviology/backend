# Write units tests for the API

import unittest
import requests
import json

#class ApiTests(unittest.TestCase):
   
      # def test_get(self):
      #    response = requests.get('http://localhost:5000/api/v1.0/movies')
      #    self.assertEqual(response.status_code, 200)
      #    self.assertEqual(response.headers['content-type'], 'application/json')

      # def test_post(self):
      #    response = requests.post('http://localhost:5000/api/v1.0/movies', data = json.dumps({'title': 'test'}))
      #    self.assertEqual(response.status_code, 201)
      #    self.assertEqual(response.headers['content-type'], 'application/json')

      # def test_put(self):
      #    response = requests.put('http://localhost:5000/api/v1.0/movies/1', data = json.dumps({'title': 'test'}))
      #    self.assertEqual(response.status_code, 200)
      #    self.assertEqual(response.headers['content-type'], 'application/json')

      # def test_delete(self):
      #    response = requests.delete('http://localhost:5000/api/v1.0/movies/1')
      #    self.assertEqual(response.status_code, 204)

# if __name__ == '__main__':
#    unittest.main()




# Write functional tests for the API

# class FunctionalTests(unittest.TestCase):
   # Call the API to get the list of movies
   # Check that the response is a list
   # Check that the list is not empty
   # Check that the list contains the movie "The Matrix"
   # def test_get(self):
   #    response = requests.get('http://localhost:5000/api/v1.0/movies')
   #    self.assertEqual(response.status_code, 200)
   #    self.assertEqual(response.headers['content-type'], 'application/json')
   #    self.assertIsInstance(response.json(), list)
   #    self.assertGreater(len(response.json()), 0)
   #    self.assertIn('The Matrix', response.json())

   # Call the API to add a movie
   # Check that the response is a dictionary
   # Check that the dictionary contains the movie "test"
   # def test_post(self):
   #    response = requests.post('http://localhost:5000/api/v1.0/movies', data = json.dumps({'title': 'test'}))
   #    self.assertEqual(response.status_code, 201)
   #    self.assertEqual(response.headers['content-type'], 'application/json')
   #    self.assertIsInstance(response.json(), dict)
   #    self.assertIn('test', response.json().values())

   # Call the API to update a movie
   # Check that the response is a dictionary
   # Check that the dictionary contains the movie "test"
   # def test_put(self):
   #    response = requests.put('http://localhost:5000/api/v1.0/movies/1', data = json.dumps({'title': 'test'}))
   #    self.assertEqual(response.status_code, 200)
   #    self.assertEqual(response.headers['content-type'], 'application/json')
   #    self.assertIsInstance(response.json(), dict)
   #    self.assertIn('test', response.json().values())

   # Call the API to delete a movie
   # Check that the response is a dictionary
   # Check that the dictionary contains the movie "test"
#    def test_delete(self):
#       response = requests.delete('http://localhost:5000/api/v1.0/movies/1')
#       self.assertEqual(response.status_code, 204)

# if __name__ == '__main__':
#    unittest.main()

# Path: Tests\FunctionalTests.py
# Compare this snippet from api\__init__.py:@
# import threading
# from core.pubnub_listener import pubnub, MySubscribeCallback
# from core.config import config
# from main import app
#
# my_channel = config.get("CHANNEL")

# if __name__ == "__main__":

#      moviology_thread = threading.Thread()
#      moviology_thread.start()
#      pubnub.add_listener(MySubscribeCallback())
#      pubnub.subscribe().channels(my_channel).execute()
#      app.run(port=5000)

# Write functional tests for the API


# Test the login page
class LoginTests(unittest.TestCase):
      def test_login(self):
         response = requests.post('http://localhost:5000/auth/login', data = json.dumps({'username': 'admin', 'password': 'admin'}))
         self.assertEqual(response.status_code, 200)
         self.assertEqual(response.headers['content-type'], 'application/json')
         self.assertIsInstance(response.json(), dict)
         self.assertIn('admin', response.json().values())


# Test the register page
class RegisterTests(unittest.TestCase):
      def test_register(self):
         response = requests.post('http://localhost:5000/register', data = json.dumps({'username': 'admin', 'password': 'admin'}))
         self.assertEqual(response.status_code, 200)
         self.assertEqual(response.headers['content-type'], 'application/json')
         self.assertIsInstance(response.json(), dict)
         self.assertIn('admin', response.json().values())


# Test the logout page
class LogoutTests(unittest.TestCase):
      def test_logout(self):
         response = requests.post('http://localhost:5000/logout', data = json.dumps({'username': 'admin', 'password': 'admin'}))
         self.assertEqual(response.status_code, 200)
         self.assertEqual(response.headers['content-type'], 'application/json')
         self.assertIsInstance(response.json(), dict)
         self.assertIn('admin', response.json().values())


# Test the home page

