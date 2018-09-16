from picotui.context import Context
from picotui.screen import Screen
from picotui.defs import *
from picotui.widgets import (
    WMultiEntry,
    WButton,
    WListBox,
    Dialog,
    EditorExt,
    EditableWidget,
    ACTION_OK)
import click

import shutil
import threading

from codechef_cli import util


class TextArea(EditorExt, EditableWidget):
    def __init__(self, w, h, lines):
        EditorExt.__init__(self, width=w, height=h)
        self.h = h
        self.w = w
        self.focus = False
        self.set_lines(lines)

    def get(self):
        return self.content

    def set(self, lines):
        self.set_lines(lines)

    def handle_key(self, key):
        if key in (KEY_ESC,):
            return key
        if key == b'j':
            super().handle_cursor_keys(KEY_DOWN)
            return True
        if key == b'k':
            super().handle_cursor_keys(KEY_UP)
            return True
        if super().handle_cursor_keys(key):
            return True

    def show_line(self, l, i):
        self.attr_color(C_WHITE, C_GRAY)
        super().show_line(l, i)
        self.attr_reset()


def draw_contest_page(contest):
    if not contest.problem_codes:
        print('No problems. Contest may not be started yet.')
        return
    with Context():
        def set_text_body(prob):
            lines = util.html_to_terminal(prob.body).split('\n')
            lines = [click.style(prob.problem_name, bg='black',
                                 fg='blue', bold=True), ''] + lines
            text.set(lines)

        def listbox_changed(w_a):
            # TODO(vn-ki): refractor this
            def write_prob_to_screen():
                prob = contest[w_a.choice]
                if len(text.content) > 1:
                    return
                set_text_body(prob)
                text.goto_line(0)
                text.redraw()
            if not contest.is_problem_fetched(w_a.choice):
                t = threading.Thread(target=write_prob_to_screen)
                t.start()
                text.set(['Loading...'])
                text.goto_line(0)
                text.redraw()
            else:
                write_prob_to_screen()
                prob = contest[w_a.choice]
                set_text_body(prob)
                text.goto_line(0)
                text.redraw()

        Screen.attr_color(C_WHITE, C_GRAY)
        Screen.cls()
        Screen.attr_reset()
        wid, hei = shutil.get_terminal_size()
        d = Dialog(0, 0, wid, hei)

        # Can add a raw string to dialog, will be converted to WLabel
        d.add(0, 0, "ProblemList:")
        w = WListBox(15, hei-4, contest.problem_codes)
        w.tag = "list"
        d.add(3, 2, w)

        text_x, text_y = 30, 2
        text = TextArea(wid-text_x-5, hei-text_y-2,
                        ['CONTEST_CODE: ' + contest.contest_code, 'NAME: '+contest.name])
        set_text_body(contest[0])
        d.add(text_x, text_y, text)
        w.on("changed", listbox_changed)
        b = WButton(8, "Exit")
        d.add(3, hei-2, b)
        b.finish_dialog = ACTION_OK

        res = d.loop()
