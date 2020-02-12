#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""Creates a taskbar icon that indicates if updates are available and provides a context menu to inspect and install them.

   Dependencies:
	* pacman-contrib to check for updates
	* python-wxpython for the icon and the context menu
	* pacman for updating
"""

import wx
import wx.adv
import subprocess
import os

# update period in ms
UPDATE_PERIOD = int (os.getenv('UPDATE_PERIOD', 60 * 60 * 1000))

# terminal has to support `-e` parameter
TERMINAL = os.getenv('TERMINAL', "xterm")

# the cmd to execute when clicking update
UPDATE_CMD = os.getenv('UPDATE_CMD', "sudo pacman -Syu")

# the folder used to search the icons
ICONS_FOLDER = os.getenv('ICONS_FOLDER', "/usr/share/pixmaps/archupdate-indicator")

ARCHUPDATE_INDICATOR_VERSION = "1.0.0"

class Icons:
	def __getPath(x):
		return os.path.join (ICONS_FOLDER, x)

	NO_UPDATES = __getPath("no_updates.png")
	UPDATES_AVAILABLE = __getPath("updates_available.png")
	CHECK_UPDATES_FAILED = __getPath("updates_failed.png")

class TaskBarIcon(wx.adv.TaskBarIcon):
	def __init__(self, frame, timerDelta, terminal, updateCmd):
		self.frame = frame
		wx.adv.TaskBarIcon.__init__(self)

		self.onSetIcon(Icons.NO_UPDATES)

		self.updates = []
		self.checkUpdates()

		self.terminal = terminal
		self.updateCmd = updateCmd

		# add recurring timer
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.onTimerTriggered)
		self.timerDelta = timerDelta
		self.timer.Start(self.timerDelta)

	def CreatePopupMenu(self):
		menu = wx.Menu()

		check = wx.MenuItem(menu, wx.NewId(), "Check now")
		menu.Bind(wx.EVT_MENU, self.onCheck, id=check.GetId())
		menu.Append(check)

		if len (self.updates) > 0:
			update = wx.MenuItem(menu, wx.NewId(), "Install")
			menu.Bind(wx.EVT_MENU, self.onInstall, id=update.GetId())
			menu.Append(update)

		about = wx.MenuItem(menu, wx.NewId(), "About")
		menu.Bind(wx.EVT_MENU, self.onAbout, id=about.GetId())
		menu.Append(about)

		menu.AppendSeparator()

		quit = wx.MenuItem(menu, wx.NewId(), "Quit")
		menu.Bind(wx.EVT_MENU, self.onQuit, id=quit.GetId())
		menu.Append(quit)

		menu.AppendSeparator()

		for u in self.updates:
			menu.Append(wx.MenuItem(menu, wx.ID_ANY, u))

		if len(self.updates) == 0:
			menu.Append(wx.MenuItem(menu, wx.ID_ANY, "No updates"))

		return menu

	def checkUpdates(self):
		print("Checking for updates")

		complProc = subprocess.run(["checkupdates"], capture_output=True, text=True, encoding='utf-8')
		icon = Icons.NO_UPDATES
		# there are updates
		if complProc.returncode == 0:
			self.updates = complProc.stdout.splitlines()
			numUpdates = len(self.updates)
			if numUpdates > 0:
				icon = Icons.UPDATES_AVAILABLE
				print ("Found {} update(s)".format (numUpdates))
			else:
				print ("No updates found")
		# return code 2 = no updates
		elif complProc.returncode == 2:
			self.updates = []
			icon = Icons.NO_UPDATES
			print ("No updates found")
		# treat everything else as error
		else:
			print ("checkupdates returned error code {}".format (complProc.returncode))
			self.updates.append("checkupdates failed")
			self.updates = []
			icon = Icons.CHECK_UPDATES_FAILED

		self.onSetIcon(icon)

	def onTimerTriggered(self,event):
		self.checkUpdates()
		self.timer.Start(self.timerDelta)

	def onSetIcon(self, path):
		icon = wx.Icon(path)

		tooltip = "Invalid icon"
		if path == Icons.NO_UPDATES:
			tooltip = "No updates available"
		elif path == Icons.UPDATES_AVAILABLE:
			tooltip = "{} updates available".format (len(self.updates))
		elif path == Icons.CHECK_UPDATES_FAILED:
			tooltip = "Update check failed"

		self.SetIcon(icon, tooltip)

	def onCheck(self, path):
		self.checkUpdates()

	def onInstall(self,event):
		os.system("{} -e 'bash -c \"{}; read -p \\\"Press enter to close terminal\\\"\"'".format(self.terminal, self.updateCmd))
		self.checkUpdates()

	def onAbout(self,event):
		info = wx.adv.AboutDialogInfo()
		info.SetName("Arch Update Indicator")
		info.SetVersion(ARCHUPDATE_INDICATOR_VERSION)
		info.SetDescription("""Creates a taskbar icon that indicates if updates are available and provides a context menu to inspect and install them.

Artwork used in this project:

"Arch linux, archlinux icon" (from https://www.iconfinder.com/icons/386451/arch_linux_archlinux_icon) by Aha-Soft is licensed under 
Creative Commons (Attribution 3.0 Unported) (https://creativecommons.org/licenses/by/3.0/)

"Green and Red Arch Linux Icons" are a derivative of "Arch linux, archlinux icon" by Aha-Soft, used under Creative Commons (Attribution 3.0 Unported). They are hereby licensed under Creative Commons (Attribution 3.0 Unported) by epsilontheta.""")
		info.SetCopyright("MIT License 2019 epsilontheta <voidptr@outlook.de>")
		info.AddDeveloper("epsilontheta")
		info.SetWebSite("https://github.com/epsilontheta/archupdate-indicator")

		wx.adv.AboutBox(info)

	def onQuit(self, event):
		self.RemoveIcon()
		wx.CallAfter(self.Destroy)
		self.frame.Close()

if __name__ == '__main__':
	app = wx.App()
	frame=wx.Frame(None)
	print("Creating TaskBarIcon with update period of {} min".format (UPDATE_PERIOD/1000/60))
	TaskBarIcon(frame, UPDATE_PERIOD, TERMINAL, UPDATE_CMD)
	app.MainLoop()
