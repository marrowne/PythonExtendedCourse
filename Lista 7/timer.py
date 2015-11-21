"""
Zaprogramuj graficzny minutnik, tj. program odliczający wstecz zadany przez
użytkownika czas i sygnalizujący koniec odliczania. Aby program był bardziej
użyteczny, np. w kuchni, dodaj możliwość ustalania czasu odliczania poprzez
wskazanie z menu pozycji typu gotowanie ryżu czy gotowanie jajek na miękko.
Zadanie proszę wykonać za pomocą biblioteki Gtk i Cairo.
"""

import cairo
from os.path import abspath, dirname, join
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from time import *
import pygame

WHERE_AM_I = abspath(dirname(__file__))

def toTime(time):
    """
    :param time: seconds as float
    :return: string (hh:)mm:ss
    """
    string = ''
    hours = round(time) // 3600
    minutes = round(time) // 60 % 60
    seconds = round(time) % 60

    if hours > 0:
        if hours < 10:
            string += '0'
        string += str(hours) + ':'

    if minutes < 10:
        string += '0'
    string += str(minutes) + ':'

    if seconds < 10:
        string += '0'
    string += str(seconds)

    return string

class Cv(object):
    SPEED = 200
    TEXT_SIZE_MAX = 20

class Timer(Gtk.Window):

    def __init__(self):
        super(Timer, self).__init__()

        self.builder = Gtk.Builder()
        self.glade_file = join(WHERE_AM_I, 'style.glade')
        self.builder.add_from_file(self.glade_file)

        self.window = self.builder.get_object('main_window')
        self.drawing_area = self.builder.get_object('drawing_area')

        self.initialised = True
        self.time = 0
        self.start_time = time()
        self.alarm_played = True

        self.liststore = Gtk.ListStore(int, str)
        self.liststore.append([0, "Gotowe programy"])
        self.liststore.append([1, "Gotowanie ryżu"])
        self.liststore.append([2, "Gotowane jajek na miękko"])
        self.liststore.append([3, "Gotowane jajek na półmiękko"])
        self.liststore.append([4, "Gotowane jajek na twardo"])
        self.cooking_times = {
            "Gotowanie ryżu": 15*60,
            "Gotowane jajek na miękko": 3*60,
            "Gotowane jajek na półmiękko": 4*60,
            "Gotowane jajek na twardo": 5*60
        }

        self.combobox = self.builder.get_object('combo_box')
        self.combobox.set_model(self.liststore)
        self.cell = Gtk.CellRendererText()
        self.combobox.pack_start(self.cell, True)
        self.combobox.add_attribute(self.cell, 'text', 1)
        self.combobox.set_active(0)

        GLib.timeout_add(Cv.SPEED, self.onGtkTimer)
        self.builder.connect_signals(self)
        self.window.show()

    def onGtkTimer(self):
        if not self.initialised:
            return False
        self.drawing_area.queue_draw()
        return True

    def onStartClicked(self, widget):
        """
        Take values from Gtk spinbuttons and start countdown
        """
        self.start_time = time()
        self.time = \
            self.builder.get_object('seconds_spinbutton').get_value_as_int()\
                + 60 *\
            self.builder.get_object('minutes_spinbutton').get_value_as_int()\
                + 3600 *\
            self.builder.get_object('hours_spinbutton').get_value_as_int()

        if self.time > 0:
            self.alarm_played = False

    def onComboboxChanged(self, widget, data=None):
        index = widget.get_active()
        model = widget.get_model()
        item = model[index][1]
        if index != 0:
            self.builder.get_object('seconds_spinbutton')\
                 .set_value(self.cooking_times[item] % 60)
            self.builder.get_object('minutes_spinbutton')\
                 .set_value(self.cooking_times[item] // 60 % 60)
            self.builder.get_object('hours_spinbutton')\
                 .set_value(self.cooking_times[item] // 3600)

    def on_draw(self, wid, cr):
        """
        Draws remaining time and plays alarm at the end
        """
        w = wid.get_allocated_width()
        h = wid.get_allocated_height()

        cr.set_source_rgb(0.5, 0, 0)
        cr.paint()

        cr.select_font_face("Helvetica", cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_BOLD)

        cr.set_font_size(120)
        cr.set_source_rgb(1, 1, 1)

        remaining_time = self.time - time() + self.start_time
        if remaining_time <= 0:
            remaining_time = 0
            if not self.alarm_played:
                file = 'alarm.mp3'
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(file)
                pygame.mixer.music.play()
                self.alarm_played = True
        time_str = toTime(remaining_time)

        (x, y, width, height, dx, dy) = cr.text_extents(time_str)

        cr.move_to(w/2 - width/2, h/2)
        cr.text_path(time_str)
        cr.clip()
        cr.paint()

    def mainQuit(self, widget):
        """
        Close window
        """
        Gtk.main_quit()

def main():
    app = Timer()
    Gtk.main()


if __name__ == "__main__":
    main()