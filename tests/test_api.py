# Write units tests for the API

import pytest
import requests
import json



## Testing the auth.py file
# test the login endpoint
def test_login():
      url = "http://localhost:5000/auth/login"
      payload = json.dumps({
            "email": "silvester@weebhood.com",
            "password": "silvester"
      })
      headers = {
            'Content-Type': 'application/json'
      }
      response = requests.request("POST", url, headers=headers, data=payload)
      assert response.status_code == 200

# test the register endpoint
def test_register():
      url = "http://localhost:5000/auth/register"
      payload = json.dumps({
            "name": "Kevin Silvester",
            "email": "KevinSilvester@weebhood.com",
            "password": "silvester"
      })
      headers = {
            'Content-Type': 'application/json'
      }
      response = requests.request("POST", url, headers=headers, data=payload)
      assert response.status_code == 200

# test the logout endpoint
def test_logout():
      url = "http://localhost:5000/auth/logout"
      payload = json.dumps({
      })
      headers = {
            'Content-Type': 'application/json'
      }
      response = requests.request("POST", url, headers=headers, data=payload)
      assert response.status_code == 200

# test the refresh endpoint

def test_refresh():
      url = "http://localhost:5000/auth/refresh"
      payload = json.dumps({
      })
      headers = {
            'Content-Type': 'application/json'
      }
      response = requests.request("POST", url, headers=headers, data=payload)
      assert response.status_code == 200



## Testing the review.py file
# Test the review.py file

# test the profile endpoint
def test_profile():
      url = "http://localhost:5000/review/profile"
      payload = json.dumps({
      })
      headers = {
            'Content-Type': 'application/json'
      }
      response = requests.request("POST", url, headers=headers, data=payload)
      assert response.status_code == 200

# test the view_biodata/<review_id> endpoint
def test_view_biodata():
      url = "http://localhost:5000/review/view_biodata/5f8d7b1e6e8f7b2c2c1d7f9c"
      payload = json.dumps({
      })
      headers = {
            'Content-Type': 'application/json'
      }
      response = requests.request("GET", url, headers=headers, data=payload)
      assert response.status_code == 200

# test the book endpoint
def test_book():
      url = "http://localhost:5000/review/book"
      payload = json.dumps({
            "movie_title": "Test Movie",
            "movie_description": "Test Movie Description",
            "movie_genres": "Test Movie Genres",
            "movie_url": "Test Movie URL",
            "review_date": "Test Review Date"
      })
      headers = {
            'Content-Type': 'application/json'
      }
      response = requests.request("POST", url, headers=headers, data=payload)
      assert response.status_code == 200


