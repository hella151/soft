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


class CheckUsername(TLObject):  # type: ignore
    """Check if a username is free and can be assigned to a channel/supergroup


    Details:
        - Layer: ``200``
        - ID: ``10E6BD2C``

    Parameters:
        channel (:obj:`InputChannel <pyrogram.raw.base.InputChannel>`):
            The channel/supergroup that will assigned the specified username

        username (``str``):
            The username to check

    Returns:
        ``bool``
    """

    __slots__: list[str] = ["channel", "username"]

    ID = 0x10e6bd2c
    QUALNAME = "functions.channels.CheckUsername"

    def __init__(self, *, channel: "raw.base.InputChannel", username: str) -> None:
        self.channel = channel  # InputChannel
        self.username = username  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CheckUsername":
        # No flags
        
        channel = TLObject.read(b)
        
        username = String.read(b)
        
        return CheckUsername(channel=channel, username=username)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(String(self.username))
        
        return b.getvalue()
