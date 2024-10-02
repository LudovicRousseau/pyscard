#! /usr/bin/env python3
"""
Simple smart card monitoring application.

__author__ = "https://www.gemalto.com/"

Copyright 2001-2012 gemalto
Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com

This file is part of pyscard.

pyscard is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.

pyscard is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyscard; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import os.path
import sys

from smartcard.wx.SimpleSCardApp import *
from smartcard.wx.SimpleSCardAppEventObserver import SimpleSCardAppEventObserver

ID_TEXT = 10000


def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located.
    From WhereAmI page on py2exe wiki."""

    return hasattr(sys, "frozen")


def module_path():
    """This will get us the program's directory,
    even if we are frozen using py2exe. From WhereAmI page on py2exe wiki."""

    if we_are_frozen():
        return os.path.dirname(sys.executable)

    return os.path.dirname(__file__)


class SamplePanel(wx.Panel, SimpleSCardAppEventObserver):
    """A simple panel that displays activated cards and readers.
    The panel implements the SimpleSCardAppEventObserver, and has
    a chance to react on reader and card activation/deactivation."""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        sizer = wx.FlexGridSizer(0, 3, 0, 0)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(1)

        sizer.Add([20, 20], 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizer.Add([20, 20], 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizer.Add([20, 20], 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizer.Add([20, 20], 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.feedbacktext = wx.StaticText(
            self, ID_TEXT, "", wx.DefaultPosition, wx.DefaultSize, 0
        )
        sizer.Add(self.feedbacktext, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        sizer.Add([20, 20], 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizer.Add([20, 20], 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizer.Add([20, 20], 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizer.Add([20, 20], 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    # callbacks from SimpleSCardAppEventObserver interface
    def OnActivateCard(self, card):
        """Called when a card is activated by double-clicking on the
        card or reader tree control or toolbar.
        In this sample, we just connect to the card on the first activation."""
        SimpleSCardAppEventObserver.OnActivateCard(self, card)
        self.feedbacktext.SetLabel("Activated card: " + repr(card))

    def OnActivateReader(self, reader):
        """Called when a reader is activated by double-clicking on the
        reader tree control or toolbar."""
        SimpleSCardAppEventObserver.OnActivateReader(self, reader)
        self.feedbacktext.SetLabel("Activated reader: " + repr(reader))

    def OnDeactivateCard(self, card):
        """Called when a card is deactivated in the reader tree control
        or toolbar."""
        SimpleSCardAppEventObserver.OnActivateCard(self, card)
        self.feedbacktext.SetLabel("Deactivated card: " + repr(card))

    def OnSelectCard(self, card):
        """Called when a card is selected by clicking on the card or
        reader tree control or toolbar."""
        SimpleSCardAppEventObserver.OnSelectCard(self, card)
        self.feedbacktext.SetLabel("Selected card: " + repr(card))

    def OnSelectReader(self, reader):
        """Called when a reader is selected by clicking on the reader
        tree control or toolbar."""
        SimpleSCardAppEventObserver.OnSelectReader(self, reader)
        self.feedbacktext.SetLabel("Selected reader: " + repr(reader))


def main(argv):
    app = SimpleSCardApp(
        appname="A simple card monitoring tool",
        apppanel=SamplePanel,
        appstyle=TR_SMARTCARD | TR_READER,
        appicon=os.path.join(module_path(), "images", "mysmartcard.ico"),
        size=(800, 600),
    )
    app.MainLoop()


if __name__ == "__main__":
    import sys

    main(sys.argv)
