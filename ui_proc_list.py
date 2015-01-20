#
# Copyright (C) 2015 Christopher Hewitt
#
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

from gi.repository import Gdk
from gi.repository import Gtk

from ui_maps_list import MemViewUIMapsList

class MemViewUIProcListWindow(Gtk.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(title='Goldfish (Process List)')
        self.set_size_request(600, 600)
        self.connect('destroy', Gtk.main_quit)

        self.process_treeview_scroller = self.create_process_list()
        self.ptrace_status_label = Gtk.Label('', xalign=1)

        vbox = Gtk.VBox()
        vbox.pack_start(self.process_treeview_scroller, True, True, 0)
        vbox.pack_start(self.ptrace_status_label, False, True, 0)
        self.add(vbox)

        self.show_all()

    def create_menu_bar(self):
        action_group = Gtk.ActionGroup("goldfish_actions")

        self.add_file_menu_actions(action_group)
        self.add_help_menu_actions(action_group)

    def create_process_list(self):
        self.process_liststore = Gtk.ListStore(int, str, str, int, int, int)

        text_left_aligned = Gtk.CellRendererText(xalign=0)
        text_right_aligned = Gtk.CellRendererText(xalign=1)

        process_treeview = Gtk.TreeView(model=self.process_liststore)

        column_pid = Gtk.TreeViewColumn('PID', text_right_aligned, text=0)
        column_pid.set_sort_column_id(0)
        process_treeview.append_column(column_pid)

        column_filename = Gtk.TreeViewColumn('Filename', text_left_aligned, text=1)
        column_filename.set_sort_column_id(1)
        process_treeview.append_column(column_filename)

        column_state = Gtk.TreeViewColumn('State', text_left_aligned, text=2)
        column_state.set_sort_column_id(2)
        process_treeview.append_column(column_state)

        column_ppid = Gtk.TreeViewColumn('Parent PID', text_right_aligned, text=3)
        column_ppid.set_sort_column_id(3)
        process_treeview.append_column(column_ppid)

        column_pgrp = Gtk.TreeViewColumn('Process GID', text_right_aligned, text=4)
        column_pgrp.set_sort_column_id(4)
        process_treeview.append_column(column_pgrp)

        column_session = Gtk.TreeViewColumn('Session ID', text_right_aligned, text=5)
        column_session.set_sort_column_id(5)
        process_treeview.append_column(column_session)

        process_treeview_scroller = Gtk.ScrolledWindow()
        process_treeview_scroller.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        process_treeview_scroller.add(process_treeview)

        return process_treeview_scroller

    def update_process_list(self, processes):
        self.process_liststore.clear()
        for process in processes:
            self.process_liststore.append([process['pid'], process['comm'], process['state'], process['ppid'], process['pgrp'], process['session']])

    def update_ptrace_label(self, msg):
        self.ptrace_status_label.set_text('Process trace restrictions: {msg}'.format(msg=msg))

    def run(self):
        Gtk.main()

if __name__ == '__main__':
    MemViewUIWindow()

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python