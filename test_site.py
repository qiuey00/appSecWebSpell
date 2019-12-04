import pytest
import app
import os
from bs4 import BeautifulSoup
import requests, unittest

class Tests(unittest.TestCase):

    def test_home(self):
        home = requests.get("http://localhost:5000/")
        assert(home.status_code == 200)

    def test_login(self):
        loginPage = requests.get("http://localhost:5000/login")
        assert(loginPage.status_code == 200)

    def test_spellCheck(self):
        spellCheckPage = requests.get("http://localhost:5000/spell_check")
        assert(spellCheckPage.status_code == 200)

    def test_registerPage(self):
        registerPage = requests.get("http://localhost:5000/register")
        assert(registerPage.status_code == 200)