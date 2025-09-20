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


class InputStickeredMediaDocument(TLObject):  # type: ignore
    """A document with stickers attached

    Constructor of :obj:`~pyrogram.raw.base.InputStickeredMedia`.

    Details:
        - Layer: ``200``
        - ID: ``438865B``

    Parameters:
        id (:obj:`InputDocument <pyrogram.raw.base.InputDocument>`):
            The document

    """

    __slots__: list[str] = ["id"]

    ID = 0x438865b
    QUALNAME = "types.InputStickeredMediaDocument"

    def __init__(self, *, id: "raw.base.InputDocument") -> None:
        self.id = id  # InputDocument

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputStickeredMediaDocument":
        # No flags
        
        id = TLObject.read(b)
        
        return InputStickeredMediaDocument(id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.id.write())
        
        return b.getvalue()
