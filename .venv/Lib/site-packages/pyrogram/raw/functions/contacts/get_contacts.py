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


class GetContacts(TLObject):  # type: ignore
    """Returns the current user's contact list.


    Details:
        - Layer: ``200``
        - ID: ``5DD69E12``

    Parameters:
        hash (``int`` ``64-bit``):
            Hash used for caching, for more info click here.Note that the hash is computed using the usual algorithm, passing to the algorithm first the previously returned contacts.contacts.saved_count field, then max 100000 sorted user IDs from the contact list, including the ID of the currently logged in user if it is saved as a contact. Example: tdlib implementation.

    Returns:
        :obj:`contacts.Contacts <pyrogram.raw.base.contacts.Contacts>`
    """

    __slots__: list[str] = ["hash"]

    ID = 0x5dd69e12
    QUALNAME = "functions.contacts.GetContacts"

    def __init__(self, *, hash: int) -> None:
        self.hash = hash  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetContacts":
        # No flags
        
        hash = Long.read(b)
        
        return GetContacts(hash=hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.hash))
        
        return b.getvalue()
