import wx

from ui import SquawkGUI


if __name__ == "__main__":
    app = wx.App()
    gui = SquawkGUI(None)
    gui.Show()
    app.MainLoop()
