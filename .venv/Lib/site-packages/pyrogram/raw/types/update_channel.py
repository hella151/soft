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


class UpdateChannel(TLObject):  # type: ignore
    """Channel/supergroup (channel and/or channelFull) information was updated.


	 | title 

	 | megagroup 

	 | color 

	 | photo 

	 | username 

	 | usernames 

	 | has_geo 

	 | noforwards 

	 | emoji_status 

	 | has_link 

	 | slow_mode_enabled 

	 | scam 

	 | fake 

	 | gigagroup 

	 | forum 

	 | level 

	 | restricted 

	 | restriction_reason 

	 | join_to_send 

	 | join_request 

	 | is_verified 

	 | default_banned_rights 

	 | signature_profiles 




    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``200``
        - ID: ``635B4C09``

    Parameters:
        channel_id (``int`` ``64-bit``):
            Channel ID

    """

    __slots__: list[str] = ["channel_id"]

    ID = 0x635b4c09
    QUALNAME = "types.UpdateChannel"

    def __init__(self, *, channel_id: int) -> None:
        self.channel_id = channel_id  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateChannel":
        # No flags
        
        channel_id = Long.read(b)
        
        return UpdateChannel(channel_id=channel_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.channel_id))
        
        return b.getvalue()
