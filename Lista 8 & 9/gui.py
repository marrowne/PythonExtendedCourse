from db_sync import *
from os.path import abspath, dirname, join
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

WHERE_AM_I = abspath(dirname(__file__))


def to_main_table(gtk_liststore, rows):
    """
    Change result list from database to a list for GTK liststore.
    :param gtk_liststore: GTK liststore object
    :param rows: list of tuples
        where every element of tuple is a cell in a row
    """
    row_list = []
    gtk_liststore.clear()
    while rows:
        (id, surname, name, last_viewed, _, _) = rows.pop()
        row_list.append([surname, name, last_viewed, id])
    while row_list:
        gtk_liststore.append(row_list.pop())


class Gui(Gtk.Window):
    """
    Contacts app - GTK
    """
    def __init__(self):
        self.db = Database()
        self.builder = Gtk.Builder()
        self.glade_file = join(WHERE_AM_I, 'style.glade')
        self.builder.add_from_file(self.glade_file)

        self.window = self.builder.get_object('main_window')
        self.treeview = self.builder.get_object('tree_view')
        self.liststore = self.builder.get_object('liststore')
        self.window2 = self.builder.get_object('show_contact')

        self.builder.connect_signals(self)
        self.window.show()

    def search_changed(self, searchentry):
        """
        When text in search button will be changed.
         Executes query to database and then displays the result.
        """
        result = self.db.search_in_db(searchentry.get_text())
        row_list = []
        self.liststore.clear()
        while result:
            (id, surname, name, last_viewed, _, _) = result.pop()
            row_list.append([surname, name, last_viewed, id])

        while row_list:
            self.liststore.append(row_list.pop())

    def add_person(self, new_window):
        """
        Add button signal handler
        """
        self.edit = -1
        self.builder.get_object('surname_entry').set_text('')
        self.builder.get_object('name_entry').set_text('')
        self.builder.get_object('phone_entry').set_text('')
        self.builder.get_object('email_entry').set_text('')
        new_window.show()

    def edit_window(self, treeview, path, view_column):
        """
        On click a row new window is displayed
        """
        treeselection = treeview.get_selection()
        (model, _) = treeselection.get_selected()
        tree_iter = model.get_iter(path)
        contact_id = model.get_value(tree_iter, 3)
        self.edit = contact_id
        (_, surname, name, _, phone, email) = self.db.fetch_person(contact_id)

        self.window2.show()
        self.builder.get_object('surname_entry').set_text(surname)
        self.builder.get_object('name_entry').set_text(name)
        self.builder.get_object('phone_entry').set_text(str(phone or ''))
        self.builder.get_object('email_entry').set_text(str(email or ''))
        self.db.viewed_timestamp(contact_id)
        to_main_table(self.liststore, self.db.show_contacts())

    def delete_person(self, button):
        """
        Delete button signal handler
        """
        treeselection = self.treeview.get_selection()
        (model, tree_iter) = treeselection.get_selected()
        if tree_iter:
            contact_id = model.get_value(tree_iter, 3)
            self.db.drop_person(contact_id)

        to_main_table(self.liststore, self.db.show_contacts())

    def submit(self, widget):
        """
        Save button signal handler
        """
        if self.edit == -1:
            surname = self.builder.get_object('surname_entry').get_text()
            name = self.builder.get_object('name_entry').get_text()
            phone = self.builder.get_object('phone_entry').get_text()
            email = self.builder.get_object('email_entry').get_text()
            if phone == '':
                phone = None
            if email == '':
                email = None
            self.db.add_person(surname, name, phone, email)
        else:
            surname = self.builder.get_object('surname_entry').get_text()
            name = self.builder.get_object('name_entry').get_text()
            phone = self.builder.get_object('phone_entry').get_text()
            email = self.builder.get_object('email_entry').get_text()
            if phone == '':
                phone = None
            if email == '':
                email = None
            self.db.edit_person(self.edit, surname, name, phone, email)

        to_main_table(self.liststore, self.db.show_contacts())
        self.window2.hide()

    def hide_widget(self, widget):
        """
        Close show/edit window signal handler
        """
        widget.hide()

    def main_quit(self, widget):
        """
        Close window signal handler
        """
        Gtk.main_quit()
