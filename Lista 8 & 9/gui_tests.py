import unittest
import sqlite3
from gui import *


class TestGui(unittest.TestCase):
    def setUp(self):
        self.gui = Gui()
        self.conn = sqlite3.connect('./database.db')
        self.db = self.conn.cursor()

        # sample person
        self.first_name = 'Maria'
        self.surname = 'Kowalska'

    def test_person_addition(self):
        """GTK test addition"""
        self.gui.add_person(self.gui.window2)
        self.gui.builder.get_object('surname_entry').set_text(self.surname)
        self.gui.builder.get_object('name_entry').set_text(self.first_name)
        self.gui.submit(None)
        self.gui.hide_widget(self.gui.window2)
        (ID, db_surname, db_first_name, db_last_viewed, _, _) = \
            self.db.execute('SELECT * FROM contacts WHERE '
                            'id = (SELECT MAX(id) FROM contacts)') \
                .fetchall().pop()
        self.assertEqual(db_first_name, self.first_name)
        self.assertEqual(db_surname, self.surname)
        self.assertEqual(db_last_viewed, 'Nie wyświetlano')
        self.db.execute('DELETE FROM contacts WHERE id=?', (ID,))
        self.conn.commit()

    def test_searching(self):
        """GTK test searchbox"""
        searchentry = self.gui.builder.get_object('search_entry')
        searchentry.set_text('A')
        self.gui.search_changed(searchentry)
        treeiter = self.gui.liststore.get_iter_first()
        result = []
        while treeiter != None:
            result.append(self.gui.liststore[treeiter][:])
            if self.gui.liststore.iter_has_child(treeiter):
                childiter = self.gui.liststore.iter_children(treeiter)
            treeiter = self.gui.liststore.iter_next(treeiter)

        db_res = self.db.execute("SELECT * FROM contacts WHERE surname LIKE ? OR name LIKE ?",
                                 ('A%', 'A%')).fetchall()

        for row in result:
            (db_id, db_surname, db_first_name, db_last_viewed, _, _) = db_res.pop(0)
            self.assertEqual(row[3], db_id)
            self.assertEqual(row[0], db_surname)
            self.assertEqual(row[1], db_first_name)
            self.assertEqual(row[2], db_last_viewed)


if __name__ == '__main__':
    unittest.main()
