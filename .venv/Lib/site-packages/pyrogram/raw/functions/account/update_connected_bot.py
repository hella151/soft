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


class UpdateConnectedBot(TLObject):  # type: ignore
    """Connect a business bot » to the current account, or to change the current connection settings.


    Details:
        - Layer: ``200``
        - ID: ``43D8521D``

    Parameters:
        bot (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            The bot to connect or disconnect

        recipients (:obj:`InputBusinessBotRecipients <pyrogram.raw.base.InputBusinessBotRecipients>`):
            Configuration for the business connection

        can_reply (``bool``, *optional*):
            Whether the bot can reply to messages it receives from us, on behalf of us using the business connection.

        deleted (``bool``, *optional*):
            Whether to fully disconnect the bot from the current account.

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: list[str] = ["bot", "recipients", "can_reply", "deleted"]

    ID = 0x43d8521d
    QUALNAME = "functions.account.UpdateConnectedBot"

    def __init__(self, *, bot: "raw.base.InputUser", recipients: "raw.base.InputBusinessBotRecipients", can_reply: Optional[bool] = None, deleted: Optional[bool] = None) -> None:
        self.bot = bot  # InputUser
        self.recipients = recipients  # InputBusinessBotRecipients
        self.can_reply = can_reply  # flags.0?true
        self.deleted = deleted  # flags.1?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateConnectedBot":
        
        flags = Int.read(b)
        
        can_reply = True if flags & (1 << 0) else False
        deleted = True if flags & (1 << 1) else False
        bot = TLObject.read(b)
        
        recipients = TLObject.read(b)
        
        return UpdateConnectedBot(bot=bot, recipients=recipients, can_reply=can_reply, deleted=deleted)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.can_reply else 0
        flags |= (1 << 1) if self.deleted else 0
        b.write(Int(flags))
        
        b.write(self.bot.write())
        
        b.write(self.recipients.write())
        
        return b.getvalue()
