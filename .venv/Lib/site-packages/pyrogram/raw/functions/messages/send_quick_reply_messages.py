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


class SendQuickReplyMessages(TLObject):  # type: ignore
    """Send a quick reply shortcut ».


    Details:
        - Layer: ``200``
        - ID: ``6C750DE1``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            The peer where to send the shortcut (users only, for now).

        shortcut_id (``int`` ``32-bit``):
            The ID of the quick reply shortcut to send.

        id (List of ``int`` ``32-bit``):
            Specify a subset of messages from the shortcut to send; if empty, defaults to all of them.

        random_id (List of ``int`` ``64-bit``):
            Unique client IDs required to prevent message resending, one for each message we're sending, may be empty (but not recommended).

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: list[str] = ["peer", "shortcut_id", "id", "random_id"]

    ID = 0x6c750de1
    QUALNAME = "functions.messages.SendQuickReplyMessages"

    def __init__(self, *, peer: "raw.base.InputPeer", shortcut_id: int, id: list[int], random_id: list[int]) -> None:
        self.peer = peer  # InputPeer
        self.shortcut_id = shortcut_id  # int
        self.id = id  # Vector<int>
        self.random_id = random_id  # Vector<long>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendQuickReplyMessages":
        # No flags
        
        peer = TLObject.read(b)
        
        shortcut_id = Int.read(b)
        
        id = TLObject.read(b, Int)
        
        random_id = TLObject.read(b, Long)
        
        return SendQuickReplyMessages(peer=peer, shortcut_id=shortcut_id, id=id, random_id=random_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.shortcut_id))
        
        b.write(Vector(self.id, Int))
        
        b.write(Vector(self.random_id, Long))
        
        return b.getvalue()
