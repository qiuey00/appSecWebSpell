import pytest
import app

def test_register(my_app):
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