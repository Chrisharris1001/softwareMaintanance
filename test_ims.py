import unittest
import sqlite3
import os
from db_helper import execute_query, fetch_query

class TestIMS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        create_table_query = "CREATE TABLE IF NOT EXISTS category (cid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)"
        execute_query(create_table_query)

    def setUp(self):
        execute_query("DELETE FROM category")

    def test_unit_execute_insert(self):
        execute_query("INSERT INTO category (name) VALUES (?)", ("Electronics",))
        result = fetch_query("SELECT * FROM category WHERE name='Electronics'")
        self.assertEqual(len(result), 1)

    def test_unit_fetch_empty(self):
        result = fetch_query("SELECT * FROM category WHERE name='NonExistent'")
        self.assertEqual(result, [])

    def test_unit_execute_delete(self):
        execute_query("INSERT INTO category (name) VALUES (?)", ("Toys",))
        execute_query("DELETE FROM category WHERE name=?", ("Toys",))
        result = fetch_query("SELECT * FROM category WHERE name='Toys'")
        self.assertEqual(len(result), 0)


    def test_integration_add_and_fetch_category(self):
        cat_name = "Home Decor"
        execute_query("INSERT INTO category (name) VALUES (?)", (cat_name,))
        rows = fetch_query("SELECT name FROM category")
        names = [row[0] for row in rows]
        self.assertIn(cat_name, names)

    def test_integration_search_logic(self):
        execute_query("INSERT INTO category (name) VALUES (?)", ("Apple",))
        execute_query("INSERT INTO category (name) VALUES (?)", ("Banana",))

        search_txt = "%App%"
        results = fetch_query("SELECT * FROM category WHERE name LIKE ?", (search_txt,))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "Apple")

if __name__ == "__main__":
    unittest.main()