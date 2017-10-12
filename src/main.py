# main.py
# Heiher <r@hev.cc>
#

import gi
from gi.repository import GLib
gi.require_version('HevSCGI', '1.0')
from gi.repository import HevSCGI
from hev_scgi_handler_demo import Handler

def main ():
    loop = GLib.MainLoop ()
    server = HevSCGI.Server ()

    handler = Handler ()
    server.add_handler (handler)

    server.load_extern_handlers ()
    server.load_default_handler ()

    server.start ()
    loop.run ()
    server.stop ()

if __name__ == '__main__':
    main ()
