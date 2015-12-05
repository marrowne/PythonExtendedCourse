import unittest
import time
from db_sync import *


class TestDbOperations(unittest.TestCase):
    def setUp(self):
        self.database = Database()

        self.first_name = 'Maria'
        self.surname = 'Kowalska'
        self.phone = '111111111111'
        self.email = 'mail@example.com'

    def test_addition(self):
        """Testing basic addition to database"""
        self.database.add_person(self.surname, self.first_name)
        (db_id, db_surname, db_first_name, db_last_viewed, _, _) = \
            self.database.db.execute('SELECT * FROM contacts WHERE id = '
                                     '(SELECT MAX(id) FROM contacts)') \
                .fetchall().pop()
        self.assertEqual(db_first_name, self.first_name)
        self.assertEqual(db_surname, self.surname)
        self.assertEqual(db_last_viewed, 'Nie wyświetlano')
        self.database.db.execute('DELETE FROM contacts WHERE id=?', (db_id,))
        self.database.conn.commit()

    def test_add_with_params_timestamp_and_del(self):
        """Add, timestamp and delete"""
        # addition
        self.database.add_person(self.surname, self.first_name,
                                 self.phone, self.email)
        (ID, db_surname, db_first_name, db_last_viewed, db_phone, db_email) = \
            self.database.db.execute('SELECT * FROM contacts WHERE id = '
                                     '(SELECT MAX(id) FROM contacts)') \
                .fetchall().pop()
        self.assertEqual(db_first_name, self.first_name, 'Incorrect first name')
        self.assertEqual(db_surname, self.surname, 'Incorrect surname')
        self.assertEqual(db_last_viewed, 'Nie wyświetlano', 'Incorrect init date')
        self.assertEqual(db_phone, self.phone, 'Incorrect phone')
        self.assertEqual(db_email, self.email, 'Incorrect email')

        # timestamping
        current_time = time.strftime('%d-%m-%y %H:%M')
        self.database.viewed_timestamp(ID)

        timestamp = self.database.db.execute('SELECT * FROM contacts '
                                             'WHERE id = (SELECT MAX(id) FROM contacts)') \
            .fetchall().pop()[3]

        # if timestamps don't equals check them once again
        # because maybe the time difference is 1 minute
        if timestamp != current_time:
            current_time = time.strftime('%d-%m-%y %H:%M')
            self.database.viewed_timestamp(ID)
            timestamp = self.database.db.execute('SELECT * FROM contacts '
                                                 'WHERE id = (SELECT MAX(id) '
                                                 'FROM contacts)').fetchall().pop()[3]
            self.assertEqual(current_time, timestamp, 'Time is incorrect')

        # removal
        self.database.drop_person(ID)
        last_row_phone = self.database.db.execute('SELECT * FROM contacts '
                                                  'WHERE id = (SELECT MAX(id) FROM contacts)') \
            .fetchall().pop()[4]
        self.assertNotEqual(self.phone, last_row_phone)

    def test_print_from_db(self):
        """Test fetch all from database"""
        result = self.database.show_contacts()
        self.assertEqual(type(result), type([]), 'Incorrect type')
        correct_result = self.database.db.execute('SELECT * FROM contacts') \
            .fetchall()

        for row in result:
            (ID, db_surname, db_first_name, db_last_viewed,
             db_phone, db_email) = correct_result.pop(0)
            self.assertEqual(row[0], ID)
            self.assertEqual(row[1], db_surname)
            self.assertEqual(row[2], db_first_name)
            self.assertEqual(row[3], db_last_viewed)
            self.assertEqual(row[4], db_phone)
            self.assertEqual(row[5], db_email)

    def test_incorrect_search(self):
        """Test search with incorrect type"""
        result = self.database.search_in_db(1)
        self.assertEqual(type(result), type([]))


if __name__ == '__main__':
    unittest.main()
