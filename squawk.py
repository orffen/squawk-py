#!/usr/bin/env python3
# squawk.py -- generate a valid squawk code for flight simulation

import os
import random
import sys
import urllib.request
import wx


class SquawkGUI(wx.Frame):
    """Creates a GUI for the Squawk! utility"""
    def __init__(self, parent):
        self.squawk_code = generate_squawk()
        self.title = "Squawk!"
        self.style = wx.CAPTION|wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.RESIZE_BORDER \
            |wx.STAY_ON_TOP
        super(SquawkGUI, self).__init__(
            parent, title=self.title, style=self.style)

        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, "squawk.ico")
        else:
            icon_path = "squawk.ico"
        icon = wx.Icon(icon_path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        font_fixed = wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                             wx.FONTWEIGHT_NORMAL)
        font_squawk = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font_squawk.SetPointSize(20)
        font_squawk.SetWeight(wx.FONTWEIGHT_BOLD)
        font_warning = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font_warning.SetPointSize(9)
        font_warning.SetWeight(wx.FONTWEIGHT_BOLD)

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        squawk_box = wx.StaticBoxSizer(wx.HORIZONTAL, panel,
                                       label="Squawk Code")

        self.st_squawk = wx.StaticText(panel, label=str(self.squawk_code),
                                       style=wx.ALIGN_CENTRE|wx.CENTRE)
        self.st_squawk.SetFont(font_squawk)
        squawk_box.Add(self.st_squawk, proportion=1,
                       flag=wx.EXPAND)

        btn_new_squawk = wx.Button(panel, label="Get New")
        btn_new_squawk.Bind(wx.EVT_BUTTON, self.update_squawk)
        squawk_box.Add(btn_new_squawk, flag=wx.ALIGN_CENTRE_VERTICAL|wx.TOP,
                       border=5)

        vbox.Add(squawk_box, flag=wx.ALL|wx.EXPAND, border=10)

        metar_box = wx.StaticBoxSizer(wx.VERTICAL, panel, label="METAR/TAF")

        metar_box_hbox = wx.BoxSizer(wx.HORIZONTAL)

        st_icao = wx.StaticText(panel, label="ICAO:")
        metar_box_hbox.Add(st_icao, flag=wx.ALIGN_CENTRE_VERTICAL)

        self.tc_icao = wx.TextCtrl(panel) #TODO: add size?
        self.tc_icao.Bind(wx.EVT_TEXT, self._uppercase_tc_icao)
        metar_box_hbox.Add(self.tc_icao, proportion=1, flag=wx.LEFT|wx.RIGHT,
                           border=10)

        btn_get_metar = wx.Button(panel, label="Refresh")
        btn_get_metar.Bind(wx.EVT_BUTTON, self.update_metar)
        metar_box_hbox.Add(btn_get_metar, flag=wx.ALIGN_CENTRE_VERTICAL)

        metar_box.Add(metar_box_hbox, flag=wx.EXPAND|wx.BOTTOM, border=5)

        self.tc_metar = wx.TextCtrl(panel,
                                    size=panel.FromDIP(wx.Size(300, 100)),
                                    style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.tc_metar.SetFont(font_fixed)
        metar_box.Add(self.tc_metar, proportion=1, flag=wx.EXPAND)

        vbox.Add(metar_box, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT,
                 border=10)

        st_warning = wx.StaticText(panel,
                                   label="FOR FLIGHT SIMULATION USE ONLY")
        st_warning.SetFont(font_warning)
        st_warning.SetForegroundColour(wx.RED)
        vbox.Add(st_warning, flag=wx.ALIGN_CENTRE_HORIZONTAL|wx.ALL, border=5)

        vbox.SetSizeHints(self)
        panel.SetSizerAndFit(vbox)
        panel.Layout()
        self.CentreOnScreen()


    def update_squawk(self, event):
        self.squawk_code = generate_squawk()
        self.st_squawk.SetLabel(self.squawk_code)
        self.Layout()


    def update_metar(self,event):
        self.tc_metar.SetValue(retrieve_metar(self.tc_icao.GetValue()))
        self.Layout()


    def _uppercase_tc_icao(self, event):
        event.Skip()
        selection = self.tc_icao.GetSelection()
        self.tc_icao.ChangeValue(self.tc_icao.GetValue().upper())
        self.tc_icao.SetSelection(*selection)


def squawk_OK(code: str) -> bool:
    RESERVED_CODES = [
        21, 22, 25, 33, 500, 600, 700, 1200, 5061, 5062, 7001, 7004, 7615,
        list(range(41, 58)), list(range(100, 701)), list(range(1200, 1278)),
        list(range(4400, 4478)), list(range(7501, 7578))
    ]
    code_as_int = int(code)
    if code[-2:] == "00": # all codes ending in 00 are reserved
        return False
    if not (0 < code_as_int <= 7777): # range check
        return False
    if code_as_int in RESERVED_CODES:
        return False
    return True


def generate_squawk() -> str:
    code = "1200"
    while not squawk_OK(code):
        code = str(random.randint(0, 7))
        code += str(random.randint(0, 7))
        code += str(random.randint(0, 7))
        code += str(random.randint(0, 7))
    return code


def retrieve_metar(icao: str) -> str:
    API_URL = "https://aviationweather.gov/api/data/metar?taf=true&ids="
    with urllib.request.urlopen(API_URL + icao) as response:
        if (response.status != 200):
            return "Error retrieving METAR, status code " + response.status
        return response.read().decode("utf-8")


if __name__ == "__main__":
    app = wx.App()
    gui = SquawkGUI(None)
    gui.Show()
    app.MainLoop()
