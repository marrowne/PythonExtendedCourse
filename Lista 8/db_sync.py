import sqlite3, time

"""
THE STRUCTURE OF TABLE IN DB

CREATE TABLE contacts
       (id          INTEGER PRIMARY KEY AUTOINCREMENT   NOT NULL,
       surname      TEXT                                NOT NULL,
       name         TEXT                                NOT NULL,
       last_viewed  TEXT,
       phone        TEXT,
       email        TEXT);
"""
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.db = self.conn.cursor()

    def add_person(self, surname, name, phone=None, email=None, contact_id=None):
        """
        Add person to table contacts.
        surname, name - remained
        phone, email, contact_id - are not
        :return:
        """
        if contact_id is None:
            self.db.execute('''INSERT INTO contacts
                          (surname, name, last_viewed, phone, email)
                          VALUES (?, ?, 'Nie wyświetlano', ?, ?)''', (surname, name, phone, email))
        else:
            self.db.execute('''INSERT INTO contacts
                          (id, surname, name, last_viewed, phone, email)
                          VALUES (?, ?, ?, 'Nie wyświetlano', ?, ?)''', (contact_id, surname, name, phone, email))
        self.conn.commit()

    def show_contacts(self):
        """
        :return: list of rows in table contacts
        """
        return self.db.execute('SELECT * FROM contacts').fetchall()

    def search_in_db(self, name):
        """
        :param name: name or surname
        :return: list of matching rows
        """
        if name != '':
            surnames = self.db.execute('SELECT * FROM contacts WHERE surname=?', (name,)).fetchall()
            names = self.db.execute('SELECT * FROM contacts WHERE name=?', (name,)).fetchall()
        else:
            return self.show_contacts()

        return surnames + names

    def viewed_timestamp(self, contact_id):
        """
        Adds current date and time to last_viewed in contacts table.
        Date format: '30-02-15 14:18'
        :param contact_id
        """
        time.strftime('%d-%m-%y %H:%M')
        self.db.execute("UPDATE contacts SET last_viewed = ? WHERE id = ?",
                        (time.strftime('%d-%m-%y %H:%M'), contact_id))
        self.conn.commit()

    def fetch_person(self, contact_id):
        """
        :param contact_id
        :return: row with this ID
        """
        return self.db.execute('SELECT * FROM contacts WHERE id=?', (contact_id,)).fetchone()

    def drop_person(self, contact_id):
        """
        Deletes person from table.
        :param contact_id
        """
        self.db.execute('DELETE FROM contacts WHERE id=?', (contact_id,))
        self.conn.commit()

    def edit_person(self, contact_id, surname, name, phone=None, email=None):
        """
        Updates data for a person.
        conctact_id, surname, name - remained
        phone, email - are not
        """
        self.db.execute('UPDATE contacts SET surname=?, name=?, phone=?, email=? WHERE id=?',
                        (surname, name, phone, email, contact_id))
        self.conn.commit()