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


class Reactions(TLObject):  # type: ignore
    """List of message reactions

    Constructor of :obj:`~pyrogram.raw.base.messages.Reactions`.

    Details:
        - Layer: ``200``
        - ID: ``EAFDF716``

    Parameters:
        hash (``int`` ``64-bit``):
            Hash used for caching, for more info click here

        reactions (List of :obj:`Reaction <pyrogram.raw.base.Reaction>`):
            Reactions

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetTopReactions
            messages.GetRecentReactions
            messages.GetDefaultTagReactions
    """

    __slots__: list[str] = ["hash", "reactions"]

    ID = 0xeafdf716
    QUALNAME = "types.messages.Reactions"

    def __init__(self, *, hash: int, reactions: list["raw.base.Reaction"]) -> None:
        self.hash = hash  # long
        self.reactions = reactions  # Vector<Reaction>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Reactions":
        # No flags
        
        hash = Long.read(b)
        
        reactions = TLObject.read(b)
        
        return Reactions(hash=hash, reactions=reactions)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.hash))
        
        b.write(Vector(self.reactions))
        
        return b.getvalue()
