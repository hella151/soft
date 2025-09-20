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


class GetBroadcastRevenueWithdrawalUrl(TLObject):  # type: ignore
    """Withdraw funds from a channel's ad revenue balance ».


    Details:
        - Layer: ``200``
        - ID: ``9DF4FAAD``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            Get ad revenue withdrawal URL for the specified channel or bot

        password (:obj:`InputCheckPasswordSRP <pyrogram.raw.base.InputCheckPasswordSRP>`):
            2FA password, see here » for more info.

    Returns:
        :obj:`stats.BroadcastRevenueWithdrawalUrl <pyrogram.raw.base.stats.BroadcastRevenueWithdrawalUrl>`
    """

    __slots__: list[str] = ["peer", "password"]

    ID = 0x9df4faad
    QUALNAME = "functions.stats.GetBroadcastRevenueWithdrawalUrl"

    def __init__(self, *, peer: "raw.base.InputPeer", password: "raw.base.InputCheckPasswordSRP") -> None:
        self.peer = peer  # InputPeer
        self.password = password  # InputCheckPasswordSRP

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetBroadcastRevenueWithdrawalUrl":
        # No flags
        
        peer = TLObject.read(b)
        
        password = TLObject.read(b)
        
        return GetBroadcastRevenueWithdrawalUrl(peer=peer, password=password)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.password.write())
        
        return b.getvalue()
