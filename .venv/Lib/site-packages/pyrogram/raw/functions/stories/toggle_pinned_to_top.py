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


class TogglePinnedToTop(TLObject):  # type: ignore
    """Pin some stories to the top of the profile, see here » for more info.


    Details:
        - Layer: ``200``
        - ID: ``B297E9B``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            Peer where to pin stories.

        id (List of ``int`` ``32-bit``):
            IDs of the stories to pin (max stories_pinned_to_top_count_max).

    Returns:
        ``bool``
    """

    __slots__: list[str] = ["peer", "id"]

    ID = 0xb297e9b
    QUALNAME = "functions.stories.TogglePinnedToTop"

    def __init__(self, *, peer: "raw.base.InputPeer", id: list[int]) -> None:
        self.peer = peer  # InputPeer
        self.id = id  # Vector<int>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TogglePinnedToTop":
        # No flags
        
        peer = TLObject.read(b)
        
        id = TLObject.read(b, Int)
        
        return TogglePinnedToTop(peer=peer, id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Vector(self.id, Int))
        
        return b.getvalue()
