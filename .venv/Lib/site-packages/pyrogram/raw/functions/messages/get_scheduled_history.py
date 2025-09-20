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


class GetScheduledHistory(TLObject):  # type: ignore
    """Get scheduled messages


    Details:
        - Layer: ``200``
        - ID: ``F516760B``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            Peer

        hash (``int`` ``64-bit``):
            Hash used for caching, for more info click here. To generate the hash, populate the ids array with the id, date and edit_date (in this order) of the previously returned messages (in order, i.e. ids = [id1, date1, edit_date1, id2, date2, edit_date2, ...]).

    Returns:
        :obj:`messages.Messages <pyrogram.raw.base.messages.Messages>`
    """

    __slots__: list[str] = ["peer", "hash"]

    ID = 0xf516760b
    QUALNAME = "functions.messages.GetScheduledHistory"

    def __init__(self, *, peer: "raw.base.InputPeer", hash: int) -> None:
        self.peer = peer  # InputPeer
        self.hash = hash  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetScheduledHistory":
        # No flags
        
        peer = TLObject.read(b)
        
        hash = Long.read(b)
        
        return GetScheduledHistory(peer=peer, hash=hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Long(self.hash))
        
        return b.getvalue()
