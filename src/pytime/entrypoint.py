import sys
from pytime.config import DEBUG
from pytime.gui.app import App


if not DEBUG:
    sys.tracebacklimit = 0


def run():
    app = App()
    app.mainloop()
