#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class CheckHistoryImportPeer(TLObject):  # type: ignore
    """Check whether chat history exported from another chat app can be imported into a specific Telegram chat, click here for more info ».


    Details:
        - Layer: ``200``
        - ID: ``5DC60F03``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            The chat where we want to import history ».

    Returns:
        :obj:`messages.CheckedHistoryImportPeer <pyrogram.raw.base.messages.CheckedHistoryImportPeer>`
    """

    __slots__: list[str] = ["peer"]

    ID = 0x5dc60f03
    QUALNAME = "functions.messages.CheckHistoryImportPeer"

    def __init__(self, *, peer: "raw.base.InputPeer") -> None:
        self.peer = peer  # InputPeer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CheckHistoryImportPeer":
        # No flags
        
        peer = TLObject.read(b)
        
        return CheckHistoryImportPeer(peer=peer)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        return b.getvalue()
