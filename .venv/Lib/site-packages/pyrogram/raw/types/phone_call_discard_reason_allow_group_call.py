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


class PhoneCallDiscardReasonAllowGroupCall(TLObject):  # type: ignore
    """

    Constructor of :obj:`~pyrogram.raw.base.PhoneCallDiscardReason`.

    Details:
        - Layer: ``200``
        - ID: ``AFE2B839``

    Parameters:
        encrypted_key (``bytes``):
            N/A

    """

    __slots__: list[str] = ["encrypted_key"]

    ID = 0xafe2b839
    QUALNAME = "types.PhoneCallDiscardReasonAllowGroupCall"

    def __init__(self, *, encrypted_key: bytes) -> None:
        self.encrypted_key = encrypted_key  # bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PhoneCallDiscardReasonAllowGroupCall":
        # No flags
        
        encrypted_key = Bytes.read(b)
        
        return PhoneCallDiscardReasonAllowGroupCall(encrypted_key=encrypted_key)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.encrypted_key))
        
        return b.getvalue()
