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


class AuthorizationForm(TLObject):  # type: ignore
    """Telegram Passport authorization form

    Constructor of :obj:`~pyrogram.raw.base.account.AuthorizationForm`.

    Details:
        - Layer: ``200``
        - ID: ``AD2E1CD8``

    Parameters:
        required_types (List of :obj:`SecureRequiredType <pyrogram.raw.base.SecureRequiredType>`):
            Required Telegram Passport documents

        values (List of :obj:`SecureValue <pyrogram.raw.base.SecureValue>`):
            Already submitted Telegram Passport documents

        errors (List of :obj:`SecureValueError <pyrogram.raw.base.SecureValueError>`):
            Telegram Passport errors

        users (List of :obj:`User <pyrogram.raw.base.User>`):
            Info about the bot to which the form will be submitted

        privacy_policy_url (``str``, *optional*):
            URL of the service's privacy policy

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetAuthorizationForm
    """

    __slots__: list[str] = ["required_types", "values", "errors", "users", "privacy_policy_url"]

    ID = 0xad2e1cd8
    QUALNAME = "types.account.AuthorizationForm"

    def __init__(self, *, required_types: list["raw.base.SecureRequiredType"], values: list["raw.base.SecureValue"], errors: list["raw.base.SecureValueError"], users: list["raw.base.User"], privacy_policy_url: Optional[str] = None) -> None:
        self.required_types = required_types  # Vector<SecureRequiredType>
        self.values = values  # Vector<SecureValue>
        self.errors = errors  # Vector<SecureValueError>
        self.users = users  # Vector<User>
        self.privacy_policy_url = privacy_policy_url  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AuthorizationForm":
        
        flags = Int.read(b)
        
        required_types = TLObject.read(b)
        
        values = TLObject.read(b)
        
        errors = TLObject.read(b)
        
        users = TLObject.read(b)
        
        privacy_policy_url = String.read(b) if flags & (1 << 0) else None
        return AuthorizationForm(required_types=required_types, values=values, errors=errors, users=users, privacy_policy_url=privacy_policy_url)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.privacy_policy_url is not None else 0
        b.write(Int(flags))
        
        b.write(Vector(self.required_types))
        
        b.write(Vector(self.values))
        
        b.write(Vector(self.errors))
        
        b.write(Vector(self.users))
        
        if self.privacy_policy_url is not None:
            b.write(String(self.privacy_policy_url))
        
        return b.getvalue()
