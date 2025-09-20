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


class BotPreparedInlineMessage(TLObject):  # type: ignore
    """Represents a prepared inline message saved by a bot, to be sent to the user via a web app »

    Constructor of :obj:`~pyrogram.raw.base.messages.BotPreparedInlineMessage`.

    Details:
        - Layer: ``200``
        - ID: ``8ECF0511``

    Parameters:
        id (``str``):
            The ID of the saved message, to be passed to the id field of the web_app_send_prepared_message event »

        expire_date (``int`` ``32-bit``):
            Expiration date of the message

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.SavePreparedInlineMessage
    """

    __slots__: list[str] = ["id", "expire_date"]

    ID = 0x8ecf0511
    QUALNAME = "types.messages.BotPreparedInlineMessage"

    def __init__(self, *, id: str, expire_date: int) -> None:
        self.id = id  # string
        self.expire_date = expire_date  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BotPreparedInlineMessage":
        # No flags
        
        id = String.read(b)
        
        expire_date = Int.read(b)
        
        return BotPreparedInlineMessage(id=id, expire_date=expire_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.id))
        
        b.write(Int(self.expire_date))
        
        return b.getvalue()
