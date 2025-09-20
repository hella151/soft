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


class InputBusinessAwayMessage(TLObject):  # type: ignore
    """Describes a Telegram Business away message, automatically sent to users writing to us when we're offline, during closing hours, while we're on vacation, or in some other custom time period when we cannot immediately answer to the user.

    Constructor of :obj:`~pyrogram.raw.base.InputBusinessAwayMessage`.

    Details:
        - Layer: ``200``
        - ID: ``832175E0``

    Parameters:
        shortcut_id (``int`` ``32-bit``):
            ID of a quick reply shorcut, containing the away messages to send, see here » for more info.

        schedule (:obj:`BusinessAwayMessageSchedule <pyrogram.raw.base.BusinessAwayMessageSchedule>`):
            Specifies when should the away messages be sent.

        recipients (:obj:`InputBusinessRecipients <pyrogram.raw.base.InputBusinessRecipients>`):
            Allowed recipients for the away messages.

        offline_only (``bool``, *optional*):
            If set, the messages will not be sent if the account was online in the last 10 minutes.

    """

    __slots__: list[str] = ["shortcut_id", "schedule", "recipients", "offline_only"]

    ID = 0x832175e0
    QUALNAME = "types.InputBusinessAwayMessage"

    def __init__(self, *, shortcut_id: int, schedule: "raw.base.BusinessAwayMessageSchedule", recipients: "raw.base.InputBusinessRecipients", offline_only: Optional[bool] = None) -> None:
        self.shortcut_id = shortcut_id  # int
        self.schedule = schedule  # BusinessAwayMessageSchedule
        self.recipients = recipients  # InputBusinessRecipients
        self.offline_only = offline_only  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputBusinessAwayMessage":
        
        flags = Int.read(b)
        
        offline_only = True if flags & (1 << 0) else False
        shortcut_id = Int.read(b)
        
        schedule = TLObject.read(b)
        
        recipients = TLObject.read(b)
        
        return InputBusinessAwayMessage(shortcut_id=shortcut_id, schedule=schedule, recipients=recipients, offline_only=offline_only)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.offline_only else 0
        b.write(Int(flags))
        
        b.write(Int(self.shortcut_id))
        
        b.write(self.schedule.write())
        
        b.write(self.recipients.write())
        
        return b.getvalue()
