import requests, unittest
from bs4 import BeautifulSoup


WORDLIST = "wordlist.txt"
SITE = "http://localhost:5000/"


class TestWebFunctions(unittest.TestCase):

	def testRootPage(self):
		loginPage = requests.get(SITE)
		assert(loginPage.status_code == 200)

# def test_Login(my_app):
#     res = my_app.get("/login")
#     assert res.status_code == 200
#     assert b"<title>Login</title>" in res.data

# def test_spell_check(my_app):
#     res = my_app.get("/spell_check")
#     assert res.status_code == 200
#     assert b"<title>Spell Check</title>" in res.data