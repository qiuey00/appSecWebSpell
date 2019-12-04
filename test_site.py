import pytest
import app
import os
from bs4 import BeautifulSoup


@pytest.fixture
def my_app():
    test_app = create_app()
    return test_app.test_client()

def test_Register(my_app):
    res = my_app.get("/register")
    assert res.status_code == 200
    assert b"<title>Register</title>" in res.data

def test_Login(my_app):
    res = my_app.get("/login")
    assert res.status_code == 200
    assert b"<title>Login</title>" in res.data

def test_Spell_Check(my_app):
    res = my_app.get("/spell_check")
    assert res.status_code == 200
    assert b"<title>Spell Check</title>" in res.data

def test_register_working(my_app):
    res = my_app.get("/register")
    assert res.status_code == 200
    data = BeautifulSoup(res.data, 'html.parser')
    csrf_token = data.find('form').contents[1].attrs['value']
    res = my_app.post('/register', data=dict(uname='asdf', pword='asdf', fa2='1234567890', csrf_token=csrf_token))
    data = BeautifulSoup(res.data, 'html.parser')
    response = data.find(id='success')
    assert (str(response.contents[0]) == 'success')