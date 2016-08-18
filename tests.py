from unittest import TestCase
from io import BytesIO
from model import Closet, Gender, ICategory, Size, Color, Dress, Top, Pant, connect_to_db, db, sample_data
from server import app


#-----------------------------------------------------------------------------#


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Things to do before every test, to provide same environment for every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("Create New Closet", result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Things to do before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

        #connect to test database
        connect_to_db(app, "postgresql:///testdb")

        #create tables
        db.create_all()

        #add the sample data
        sample_data()

    def tearDown(self):
        """Done at the end of every test to clear the data"""

        db.session.close()
        db.drop_all()

    def test_create_closet_get(self):
        """Tests the Create Closet Page"""

        result = self.client.get("/createcloset")
        self.assertIn("CLOSET NAME:", result.data)

    def test_create_closet_post(self):
        """Tests the create closet page, once closet added"""

        result = self.client.post("/createcloset", data={"closet-name": "Travel", "notes": "travel closet"}, follow_redirects=True)
        self.assertIn("Noora's Closets", result.data)

    def test_add_item(self):
        """Tests the Upload Form Page"""

        result = self.client.get("/addItem")
        self.assertIn("Add Item To A Closet", result.data)

    def test_uploads(self):
        """Tests the Upload Form Page"""

        result = self.client.post("/uploads", data={"file": (BytesIO(b'my file contents'), "/static/images/littleblackdress.jpg"), "color": 1, "closet": 1, "size": 1, "category": 1, "notes": "new", "item-type": "dress"}, follow_redirects=True, content_type='multipart/form-data')
        self.assertIn("Travel", result.data)

    def test_closets(self):
        """Tests all closets page"""

        result = self.client.get("/closets")
        self.assertIn("Random", result.data)

    def view_closet(self):
        """Tests the individual view of a closet"""

        result = self.client.get("/viewcloset/2")
        self.assertIn("Travel", result.data)

#-----------------------------------------------------------------------------#


if __name__ == "__main__":
    import unittest

    unittest.main()
