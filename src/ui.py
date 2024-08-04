import os
import sys
import wx

from utils import *


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

        font_fixed = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                             wx.FONTWEIGHT_NORMAL)
        font_squawk = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font_squawk.SetPointSize(20)
        font_squawk.SetWeight(wx.FONTWEIGHT_BOLD)
        font_warning = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font_warning.SetPointSize(9)
        font_warning.SetWeight(wx.FONTWEIGHT_BOLD)

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL) # main container

        hbox1 = wx.BoxSizer(wx.HORIZONTAL) # for squawk box and TOD box

        # squawk box -----------------------------------------------------------
        squawk_box = wx.StaticBoxSizer(wx.VERTICAL, panel,
                                       label="Squawk Code")

        self.st_squawk = wx.StaticText(panel, label=str(self.squawk_code))
        self.st_squawk.SetFont(font_squawk)
        squawk_box.Add(self.st_squawk,
                       flag=wx.ALIGN_CENTRE_HORIZONTAL|wx.ALL, border=10)

        btn_new_squawk = wx.Button(panel, label="Get New")
        btn_new_squawk.Bind(wx.EVT_BUTTON, self.update_squawk)
        squawk_box.Add(btn_new_squawk, proportion=1, flag=wx.EXPAND)

        hbox1.Add(squawk_box, flag=wx.EXPAND)
        # end squawk box -------------------------------------------------------

        # TOD box --------------------------------------------------------------
        tod_box = wx.StaticBoxSizer(wx.HORIZONTAL, panel,
                                    label="TOD Calculator")

        # TOD box > rate -------------------------------------------------------
        tod_rate_box = wx.BoxSizer(wx.VERTICAL)

        st_ground_speed = wx.StaticText(panel, label="Ground Speed")
        tod_rate_box.Add(st_ground_speed, flag=wx.ALIGN_CENTRE_HORIZONTAL)

        self.tc_ground_speed = wx.TextCtrl(panel, style=wx.TE_CENTRE)
        self.tc_ground_speed.Bind(wx.EVT_TEXT, self.update_tod_rate)
        tod_rate_box.Add(self.tc_ground_speed,
                          flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, border=5)

        self.st_descent_rate = wx.StaticText(panel, label="Descent Rate")
        tod_rate_box.Add(self.st_descent_rate, flag=wx.ALIGN_CENTRE_HORIZONTAL)

        self.st_fpm = wx.StaticText(panel, style=wx.ALIGN_CENTRE_HORIZONTAL| \
                                    wx.ST_NO_AUTORESIZE)
        self.st_fpm.SetFont(self.st_fpm.GetFont().Bold())
        tod_rate_box.Add(self.st_fpm, flag=wx.EXPAND)

        tod_box.Add(tod_rate_box, flag=wx.EXPAND)
        # end TOD box > rate ---------------------------------------------------

        # TOD box > distance ---------------------------------------------------
        tod_distance_box = wx.BoxSizer(wx.VERTICAL)

        st_current_altitude = wx.StaticText(panel, label="Current Altitude")
        tod_distance_box.Add(st_current_altitude,
                             flag=wx.ALIGN_CENTRE_HORIZONTAL)

        self.tc_current_altitude = wx.TextCtrl(panel, style=wx.TE_CENTRE)
        self.tc_current_altitude.Bind(wx.EVT_TEXT, self.update_tod_distance)
        tod_distance_box.Add(self.tc_current_altitude,
                          flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, border=5)

        st_target_altitude = wx.StaticText(panel, label="Target Altitude")
        tod_distance_box.Add(st_target_altitude,
                             flag=wx.ALIGN_CENTRE_HORIZONTAL)

        self.tc_target_altitude = wx.TextCtrl(panel, style=wx.TE_CENTRE)
        self.tc_target_altitude.Bind(wx.EVT_TEXT, self.update_tod_distance)
        tod_distance_box.Add(self.tc_target_altitude,
                          flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, border=5)

        st_distance_required = wx.StaticText(panel, label="Distance Required")
        tod_distance_box.Add(st_distance_required,
                             flag=wx.ALIGN_CENTRE_HORIZONTAL)

        self.st_distance = wx.StaticText(panel,
                                         style=wx.ALIGN_CENTRE_HORIZONTAL| \
                                            wx.ST_NO_AUTORESIZE)
        self.st_distance.SetFont(self.st_distance.GetFont().Bold())
        tod_distance_box.Add(self.st_distance, flag=wx.EXPAND)

        tod_box.Add(tod_distance_box, flag=wx.EXPAND)
        # end TOD box > distance -----------------------------------------------

        hbox1.Add(tod_box, flag=wx.EXPAND|wx.LEFT, border=10)
        # end TOD box ----------------------------------------------------------

        vbox.Add(hbox1, flag=wx.EXPAND|wx.ALL, border=10)

        # metar box ------------------------------------------------------------
        metar_box = wx.StaticBoxSizer(wx.VERTICAL, panel, label="METAR/TAF")

        metar_box_hbox = wx.BoxSizer(wx.HORIZONTAL)

        st_icao = wx.StaticText(panel, label="ICAO:")
        metar_box_hbox.Add(st_icao, flag=wx.ALIGN_CENTRE_VERTICAL)

        self.tc_icao = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.tc_icao.Bind(wx.EVT_TEXT, self._uppercase_tc_icao)
        self.tc_icao.Bind(wx.EVT_TEXT_ENTER, self.update_metar)
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
        # end metar box --------------------------------------------------------

        # warning text
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


    def update_tod_distance(self, event):
        event.Skip()
        focus = wx.Window.FindFocus()
        selection = focus.GetSelection()
        try:
            current_alt = int(self.tc_current_altitude.GetValue())
            target_alt = int(self.tc_target_altitude.GetValue())
        except:
            current_alt = 0
            target_alt = 0
        distance = tod_calc_distance(current_alt, target_alt)
        if distance > 0:
            self.st_distance.SetLabel(f"{distance:.1f} nm")
        else:
            self.st_distance.SetLabel('')
        focus.SetSelection(*selection)
        self.Layout()


    def update_tod_rate(self, event):
        event.Skip()
        selection = self.tc_ground_speed.GetSelection()
        try:
            ground_speed = int(self.tc_ground_speed.GetValue())
        except:
            ground_speed = 0
        if ground_speed > 0:
            self.st_fpm.SetLabel(str(tod_calc_rate(ground_speed)) + " fpm")
        else:
            self.st_fpm.SetLabel('')
        self.tc_ground_speed.SetSelection(*selection)
        self.Layout()


    def update_metar(self,event):
        self.tc_metar.SetValue(retrieve_metar(self.tc_icao.GetValue()))
        self.Layout()


    def _uppercase_tc_icao(self, event):
        event.Skip()
        selection = self.tc_icao.GetSelection()
        self.tc_icao.ChangeValue(self.tc_icao.GetValue().upper())
        self.tc_icao.SetSelection(*selection)
