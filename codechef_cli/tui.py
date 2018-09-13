from picotui.context import Context
from picotui.screen import Screen
from picotui.defs import C_BLACK, C_WHITE, KEY_ESC, KEY_DOWN, KEY_UP
from picotui.widgets import (
    WMultiEntry,
    WButton,
    WListBox,
    Dialog,
    ACTION_OK)
import click

import shutil

from codechef_cli import util


class TextArea(WMultiEntry):
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


def draw_contest_page(contest):
    if not contest.problem_codes:
        print('No problems. Contest may not be started yet.')
        return
    with Context():
        def set_text_body(prob):
            # chunks, chunk_size = len(body), text.w
            # wrapped = [body[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
            # lines = []
            # for line in wrapped:
                # lines += line.split('<br />')
            lines = util.html_to_terminal(prob.body).split('\n')
            lines = [click.style(prob.problem_name, bg='black',
                                 fg='blue', bold=True), ''] + lines
            text.set(lines)

        def listbox_changed(w_a):
            prob = contest[w_a.choice]
            set_text_body(prob)
            text.goto_line(0)
            text.redraw()

        Screen.attr_color(C_WHITE, C_BLACK)
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
