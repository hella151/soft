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


class InputPeerChannel(TLObject):  # type: ignore
    """Defines a channel for further interaction.


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




    Constructor of :obj:`~pyrogram.raw.base.InputPeer`.

    Details:
        - Layer: ``200``
        - ID: ``27BCBBFC``

    Parameters:
        channel_id (``int`` ``64-bit``):
            Channel identifier

        access_hash (``int`` ``64-bit``):
            access_hash value from the channel constructor

    """

    __slots__: list[str] = ["channel_id", "access_hash"]

    ID = 0x27bcbbfc
    QUALNAME = "types.InputPeerChannel"

    def __init__(self, *, channel_id: int, access_hash: int) -> None:
        self.channel_id = channel_id  # long
        self.access_hash = access_hash  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPeerChannel":
        # No flags
        
        channel_id = Long.read(b)
        
        access_hash = Long.read(b)
        
        return InputPeerChannel(channel_id=channel_id, access_hash=access_hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.channel_id))
        
        b.write(Long(self.access_hash))
        
        return b.getvalue()
