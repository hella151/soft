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


class StarsAmount(TLObject):  # type: ignore
    """Describes a real (i.e. possibly decimal) amount of Telegram Stars.

    Constructor of :obj:`~pyrogram.raw.base.StarsAmount`.

    Details:
        - Layer: ``200``
        - ID: ``BBB6B4A3``

    Parameters:
        amount (``int`` ``64-bit``):
            The integer amount of Telegram Stars.

        nanos (``int`` ``32-bit``):
            The decimal amount of Telegram Stars, expressed as nanostars (i.e. 1 nanostar is equal to 1/1'000'000'000th of a Telegram Star). This field may also be negative (the allowed range is -999999999 to 999999999).

    """

    __slots__: list[str] = ["amount", "nanos"]

    ID = 0xbbb6b4a3
    QUALNAME = "types.StarsAmount"

    def __init__(self, *, amount: int, nanos: int) -> None:
        self.amount = amount  # long
        self.nanos = nanos  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarsAmount":
        # No flags
        
        amount = Long.read(b)
        
        nanos = Int.read(b)
        
        return StarsAmount(amount=amount, nanos=nanos)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.amount))
        
        b.write(Int(self.nanos))
        
        return b.getvalue()
