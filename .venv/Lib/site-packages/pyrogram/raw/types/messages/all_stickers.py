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


class AllStickers(TLObject):  # type: ignore
    """Info about all installed stickers

    Constructor of :obj:`~pyrogram.raw.base.messages.AllStickers`.

    Details:
        - Layer: ``200``
        - ID: ``CDBBCEBB``

    Parameters:
        hash (``int`` ``64-bit``):
            Hash used for caching, for more info click here

        sets (List of :obj:`StickerSet <pyrogram.raw.base.StickerSet>`):
            All stickersets

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetAllStickers
            messages.GetMaskStickers
            messages.GetEmojiStickers
    """

    __slots__: list[str] = ["hash", "sets"]

    ID = 0xcdbbcebb
    QUALNAME = "types.messages.AllStickers"

    def __init__(self, *, hash: int, sets: list["raw.base.StickerSet"]) -> None:
        self.hash = hash  # long
        self.sets = sets  # Vector<StickerSet>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AllStickers":
        # No flags
        
        hash = Long.read(b)
        
        sets = TLObject.read(b)
        
        return AllStickers(hash=hash, sets=sets)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.hash))
        
        b.write(Vector(self.sets))
        
        return b.getvalue()
