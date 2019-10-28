import pytest
import app

def my_app():
    test_app = app.create_app()
    test_app.debug = True
    return test_app.test_client()

def test_register():
	var = my_app()
    res = var.get("/register")
    assert res.status_code == 200
    assert b"<title>Register</title>" in res.data

# def test_Login(my_app):
#     res = my_app.get("/login")
#     assert res.status_code == 200
#     assert b"<title>Login</title>" in res.data

# def test_spell_check(my_app):
#     res = my_app.get("/spell_check")
#     assert res.status_code == 200
#     assert b"<title>Spell Check</title>" in res.data