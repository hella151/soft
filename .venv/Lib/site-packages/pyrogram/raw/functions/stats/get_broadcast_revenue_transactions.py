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


class GetBroadcastRevenueTransactions(TLObject):  # type: ignore
    """Fetch channel ad revenue transaction history ».


    Details:
        - Layer: ``200``
        - ID: ``70990B6D``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            Get ad revenue transactions for the specified channel or bot

        offset (``int`` ``32-bit``):
            Offset for pagination

        limit (``int`` ``32-bit``):
            Maximum number of results to return, see pagination

    Returns:
        :obj:`stats.BroadcastRevenueTransactions <pyrogram.raw.base.stats.BroadcastRevenueTransactions>`
    """

    __slots__: list[str] = ["peer", "offset", "limit"]

    ID = 0x70990b6d
    QUALNAME = "functions.stats.GetBroadcastRevenueTransactions"

    def __init__(self, *, peer: "raw.base.InputPeer", offset: int, limit: int) -> None:
        self.peer = peer  # InputPeer
        self.offset = offset  # int
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetBroadcastRevenueTransactions":
        # No flags
        
        peer = TLObject.read(b)
        
        offset = Int.read(b)
        
        limit = Int.read(b)
        
        return GetBroadcastRevenueTransactions(peer=peer, offset=offset, limit=limit)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.offset))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
