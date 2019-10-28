import pytest
import app

def test_register(my_app):
    res = my_app.get("/register")
    assert res.status_code == 200
    assert b"<title>Register</title>" in res.data