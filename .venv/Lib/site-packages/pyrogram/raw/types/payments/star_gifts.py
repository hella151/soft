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


class StarGifts(TLObject):  # type: ignore
    """Available gifts ».

    Constructor of :obj:`~pyrogram.raw.base.payments.StarGifts`.

    Details:
        - Layer: ``200``
        - ID: ``901689EA``

    Parameters:
        hash (``int`` ``32-bit``):
            Hash used for caching, for more info click here

        gifts (List of :obj:`StarGift <pyrogram.raw.base.StarGift>`):
            List of available gifts.

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            payments.GetStarGifts
    """

    __slots__: list[str] = ["hash", "gifts"]

    ID = 0x901689ea
    QUALNAME = "types.payments.StarGifts"

    def __init__(self, *, hash: int, gifts: list["raw.base.StarGift"]) -> None:
        self.hash = hash  # int
        self.gifts = gifts  # Vector<StarGift>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarGifts":
        # No flags
        
        hash = Int.read(b)
        
        gifts = TLObject.read(b)
        
        return StarGifts(hash=hash, gifts=gifts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.hash))
        
        b.write(Vector(self.gifts))
        
        return b.getvalue()
