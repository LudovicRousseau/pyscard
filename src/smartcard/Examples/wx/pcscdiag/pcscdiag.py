#! /usr/bin/env python3
"""
Example wxPython application that displays readers and inserted cards ATRs.
This example displays a snapshot of the readers and cards, there is no
automatic refresh of the readers and cards.

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

import smartcard.Exceptions
import smartcard.System
import smartcard.util

# wxPython GUI modules (https://www.wxpython.org/)
try:
    import wx
except ImportError:
    print(
        "You need wxpython (https://www.wxpython.org/) "
        + "to run this sample from the source code!"
    )
    print("press a key to continue")
    import msvcrt

    msvcrt.getch()
    import sys

    sys.exit()


def getATR(reader):
    """Return the ATR of the card inserted into the reader."""
    connection = reader.createConnection()
    atr = ""
    try:
        connection.connect()
        atr = smartcard.util.toHexString(connection.getATR())
        connection.disconnect()
    except smartcard.Exceptions.NoCardException:
        atr = "no card inserted"
    return atr


class pcscdiag(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(600, 400))
        w, h = self.GetClientSize()
        self.tree = wx.TreeCtrl(
            self,
            wx.NewIdRef(),
            wx.DefaultPosition,
            (w, h),
            wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS,
        )
        self.InitTree()
        self.OnExpandAll()

    def InitTree(self):
        self.tree.AddRoot("Readers and ReaderGroups")

        readerNode = self.tree.AppendItem(self.tree.GetRootItem(), "Readers")
        for reader in smartcard.System.readers():
            childReader = self.tree.AppendItem(readerNode, repr(reader))
            childCard = self.tree.AppendItem(childReader, getATR(reader))

        readerGroupNode = self.tree.AppendItem(
            self.tree.GetRootItem(), "Readers Groups"
        )
        for readergroup in smartcard.System.readergroups():
            childReaderGroup = self.tree.AppendItem(readerGroupNode, readergroup)
            readers = smartcard.System.readers(readergroup)
            for reader in readers:
                child = self.tree.AppendItem(childReaderGroup, repr(reader))

    def OnExpandAll(self):
        """expand all nodes"""
        root = self.tree.GetRootItem()
        fn = self.tree.Expand
        self.traverse(root, fn)
        self.tree.Expand(root)

    def traverse(self, traverseroot, function, cookie=0):
        """recursively walk tree control"""
        if self.tree.ItemHasChildren(traverseroot):
            firstchild, cookie = self.tree.GetFirstChild(traverseroot)
            function(firstchild)
            self.traverse(firstchild, function, cookie)

        child = self.tree.GetNextSibling(traverseroot)
        if child:
            function(child)
            self.traverse(child, function, cookie)


if __name__ == "__main__":
    app = wx.App()
    frame = pcscdiag(None, "Smartcard readers and reader groups")
    frame.Show()
    app.MainLoop()
