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


class TogglePaidReactionPrivacy(TLObject):  # type: ignore
    """Changes the privacy of already sent paid reactions on a specific message.


    Details:
        - Layer: ``200``
        - ID: ``435885B5``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            The channel

        msg_id (``int`` ``32-bit``):
            The ID of the message to which we sent the paid reactions

        private (:obj:`PaidReactionPrivacy <pyrogram.raw.base.PaidReactionPrivacy>`):
            If true, makes the current anonymous in the top sender leaderboard for this message; otherwise, does the opposite.

    Returns:
        ``bool``
    """

    __slots__: list[str] = ["peer", "msg_id", "private"]

    ID = 0x435885b5
    QUALNAME = "functions.messages.TogglePaidReactionPrivacy"

    def __init__(self, *, peer: "raw.base.InputPeer", msg_id: int, private: "raw.base.PaidReactionPrivacy") -> None:
        self.peer = peer  # InputPeer
        self.msg_id = msg_id  # int
        self.private = private  # PaidReactionPrivacy

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TogglePaidReactionPrivacy":
        # No flags
        
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        private = TLObject.read(b)
        
        return TogglePaidReactionPrivacy(peer=peer, msg_id=msg_id, private=private)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        b.write(self.private.write())
        
        return b.getvalue()
