# demo-handler.py
# Heiher <r@hev.cc>
#

import gi
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gio
gi.require_version('HevSCGI', '1.0')
from gi.repository import HevSCGI

class Handler (GObject.GObject, HevSCGI.Handler):
    def __init__ (self):
        GObject.GObject.__init__ (self)

    def do_get_alias (self):
        return 'HevSCGIHandlerDemo'

    def do_get_name (self):
        return 'HevSCGIHandlerDemo'

    def do_get_version (self):
        return '0.0.1'

    def do_get_pattern (self):
        return '/scgi/python.*';

    def res_os_splice_async_handler (self, res_os, result, task):
        res_os.splice_finish (result)

    def f_read_async_handler (self, f, result, task):
        f_is = f.read_finish (result)

        res = task.get_response ()
        res_os = res.get_output_stream ()
        res_os.splice_async (f_is, Gio.OutputStreamSpliceFlags.NONE, 0,
                None, self.res_os_splice_async_handler, task)

    def write_header_async_handler (self, res, result, task):
        res.write_header_finish (result)

        f = Gio.File.new_for_path ('src/hev_scgi_handler_demo.py')
        f.read_async (0, None, self.f_read_async_handler, task)

    def do_handle (self, task):
        res = task.get_response ()
        res_htb = res.get_header_hash_table ()

        res_htb['Status'] = '200 OK'
        res_htb['Content-Type'] = 'text/plain'
        res.write_header_async(None, self.write_header_async_handler, task)
