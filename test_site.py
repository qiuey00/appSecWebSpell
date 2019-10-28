import pytest
import app
import os


@pytest.fixture
def my_app():
    test_app = app.create_app()
    # test_app.debug = True
    return test_app.test_client()

def test_Register(my_app):
    res = my_app.get("/register")
    assert res.status_code == 200
    assert b"<title>Register</title>" in res.data

def test_Login(my_app):
    res = my_app.get("/login")
    assert res.status_code == 200
    assert b"<title>Login</title>" in res.data

def test_spell_check(my_app):
    res = my_app.get("/spell_check")
    assert res.status_code == 200
    assert b"<title>Spell Check</title>" in res.data

def test_register(my_app):
    res = my_app.get("/register")
    assert res.status_code == 200
    soup = BeautifulSoup(res.data, 'html.parser')
    csrf_token = soup.find('form').contents[1].attrs['value']
    res = my_app.post('/register',
                      data=dict(userName='asdf', password='asdf', auth2fa='asdf',
                                csrf_token=csrf_token),
                      follow_redirects=True)
    soup = BeautifulSoup(res.data, 'html.parser')
    response = soup.find(id='success')
    assert (str(response.contents[0]) == 'success')