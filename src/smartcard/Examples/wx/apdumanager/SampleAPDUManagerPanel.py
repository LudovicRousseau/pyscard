#! /usr/bin/env python3
"""
Simple panel that defines a dialog to send APDUs to a card.

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
import wx

from smartcard.util import toBytes, toHexString
from smartcard.wx.APDUHexValidator import APDUHexValidator
from smartcard.wx.SimpleSCardAppEventObserver import SimpleSCardAppEventObserver

[
    ID_TEXT_COMMAND,
    ID_TEXTCTRL_COMMAND,
    ID_TEXT_RESPONSE,
    ID_TEXTCTRL_RESPONSE,
    ID_TEXT_SW,
    ID_TEXT_SW1,
    ID_TEXTCTRL_SW1,
    ID_TEXT_SW2,
    ID_TEXTCTRL_SW2,
    ID_CARDSTATE,
    ID_TRANSMIT,
] = [wx.NewId() for x in range(11)]


class SampleAPDUManagerPanel(wx.Panel, SimpleSCardAppEventObserver):
    """A simple panel that displays activated cards and readers and can
    send APDU to a connected card."""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        SimpleSCardAppEventObserver.__init__(self)
        self.layoutControls()

        self.Bind(wx.EVT_BUTTON, self.OnTransmit, self.transmitbutton)

    # callbacks from SimpleSCardAppEventObserver interface
    def OnActivateCard(self, card):
        """Called when a card is activated by double-clicking
        on the card or reader tree control or toolbar.
        In this sample, we just connect to the card on the first activation."""
        SimpleSCardAppEventObserver.OnActivateCard(self, card)
        self.feedbacktext.SetLabel("Activated card: " + repr(card))
        self.transmitbutton.Enable()

    def OnActivateReader(self, reader):
        """Called when a reader is activated by double-clicking
        on the reader tree control or toolbar."""
        SimpleSCardAppEventObserver.OnActivateReader(self, reader)
        self.feedbacktext.SetLabel("Activated reader: " + repr(reader))
        self.transmitbutton.Disable()

    def OnDeactivateCard(self, card):
        """Called when a card is deactivated in the reader
        tree control or toolbar."""
        SimpleSCardAppEventObserver.OnActivateCard(self, card)
        self.feedbacktext.SetLabel("Deactivated card: " + repr(card))
        self.transmitbutton.Disable()

    def OnDeselectCard(self, card):
        """Called when a card is selected by clicking on the
        card or reader tree control or toolbar."""
        SimpleSCardAppEventObserver.OnSelectCard(self, card)
        self.feedbacktext.SetLabel("Deselected card: " + repr(card))
        self.transmitbutton.Disable()

    def OnSelectCard(self, card):
        """Called when a card is selected by clicking on the
        card or reader tree control or toolbar."""
        SimpleSCardAppEventObserver.OnSelectCard(self, card)
        self.feedbacktext.SetLabel("Selected card: " + repr(card))
        if hasattr(self.selectedcard, "connection"):
            self.transmitbutton.Enable()

    def OnSelectReader(self, reader):
        """Called when a reader is selected by clicking on the
        reader tree control or toolbar."""
        SimpleSCardAppEventObserver.OnSelectReader(self, reader)
        self.feedbacktext.SetLabel("Selected reader: " + repr(reader))
        self.transmitbutton.Disable()

    # callbacks
    def OnTransmit(self, event):
        if hasattr(self.selectedcard, "connection"):
            apdu = self.commandtextctrl.GetValue()
            data, sw1, sw2 = self.selectedcard.connection.transmit(toBytes(apdu))
            self.SW1textctrl.SetValue("%x" % sw1)
            self.SW2textctrl.SetValue("%x" % sw2)
            self.responsetextctrl.SetValue(toHexString(data + [sw1, sw2]))
        event.Skip()

    def layoutControls(self):

        # create controls
        statictextCommand = wx.StaticText(
            self, ID_TEXT_COMMAND, "Command", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.commandtextctrl = wx.TextCtrl(
            self,
            ID_TEXTCTRL_COMMAND,
            "",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_MULTILINE,
            validator=APDUHexValidator(),
        )
        statictextResponse = wx.StaticText(
            self, ID_TEXT_RESPONSE, "Response", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.responsetextctrl = wx.TextCtrl(
            self,
            ID_TEXTCTRL_RESPONSE,
            "",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_MULTILINE | wx.TE_READONLY,
        )
        statictextStatusWords = wx.StaticText(
            self, ID_TEXT_SW, "Status Words", wx.DefaultPosition, wx.DefaultSize, 0
        )
        statictextSW1 = wx.StaticText(
            self, ID_TEXT_SW1, "SW1", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.SW1textctrl = wx.TextCtrl(
            self,
            ID_TEXTCTRL_SW1,
            "",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_READONLY,
        )
        statictextSW2 = wx.StaticText(
            self, ID_TEXT_SW2, "SW2", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.SW2textctrl = wx.TextCtrl(
            self,
            ID_TEXTCTRL_SW2,
            "",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_READONLY,
        )
        self.feedbacktext = wx.StaticText(
            self, ID_CARDSTATE, "", wx.DefaultPosition, wx.DefaultSize, 0
        )

        # layout controls
        boxsizerCommand = wx.BoxSizer(wx.HORIZONTAL)
        boxsizerCommand.Add(statictextCommand, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        boxsizerCommand.Add(self.commandtextctrl, 5, wx.EXPAND | wx.ALL, 5)

        boxsizerResponse = wx.BoxSizer(wx.HORIZONTAL)
        boxsizerResponse.Add(statictextResponse, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        boxsizerResponse.Add(self.responsetextctrl, 5, wx.EXPAND | wx.ALL, 5)

        boxsizerSW = wx.BoxSizer(wx.HORIZONTAL)
        boxsizerSW.Add(statictextSW1, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        boxsizerSW.Add(self.SW1textctrl, 0, wx.EXPAND | wx.ALL, 5)
        boxsizerSW.Add(statictextSW2, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        boxsizerSW.Add(self.SW2textctrl, 0, wx.EXPAND | wx.ALL, 5)

        item11 = wx.BoxSizer(wx.HORIZONTAL)
        item11.Add(statictextStatusWords, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        item11.Add(boxsizerSW, 0, wx.EXPAND | wx.ALL, 5)

        boxsizerResponseAndSW = wx.BoxSizer(wx.VERTICAL)
        boxsizerResponseAndSW.Add(boxsizerResponse, 0, wx.EXPAND | wx.ALL, 5)
        boxsizerResponseAndSW.Add(item11, 0, wx.EXPAND | wx.ALL, 5)

        staticboxAPDU = wx.StaticBox(self, -1, "APDU")
        boxsizerAPDU = wx.StaticBoxSizer(staticboxAPDU, wx.VERTICAL)
        boxsizerAPDU.Add(boxsizerCommand, 1, wx.EXPAND | wx.ALL, 5)
        boxsizerAPDU.Add(boxsizerResponseAndSW, 4, wx.EXPAND | wx.ALL, 5)

        staticboxEvents = wx.StaticBox(self, -1, "Card/Reader Events")
        boxsizerEvents = wx.StaticBoxSizer(staticboxEvents, wx.HORIZONTAL)
        boxsizerEvents.Add(self.feedbacktext, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        sizerboxTransmitButton = wx.BoxSizer(wx.HORIZONTAL)
        sizerboxTransmitButton.Add([20, 20], 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.transmitbutton = wx.Button(
            self, ID_TRANSMIT, "Transmit", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.transmitbutton.Disable()
        sizerboxTransmitButton.Add(self.transmitbutton, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizerboxTransmitButton.Add([20, 20], 0, wx.ALIGN_CENTER | wx.ALL, 5)

        sizerPanel = wx.BoxSizer(wx.VERTICAL)
        sizerPanel.Add(boxsizerAPDU, 3, wx.EXPAND | wx.ALL, 5)
        sizerPanel.Add(boxsizerEvents, 1, wx.EXPAND | wx.ALL, 5)
        sizerPanel.Add(sizerboxTransmitButton, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizerPanel)
        self.SetAutoLayout(True)
        sizerPanel.Fit(self)
