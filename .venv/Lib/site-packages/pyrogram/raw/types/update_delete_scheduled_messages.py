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


class UpdateDeleteScheduledMessages(TLObject):  # type: ignore
    """Some scheduled messages were deleted (or sent) from the schedule queue of a chat

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``200``
        - ID: ``F2A71983``

    Parameters:
        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            Peer

        messages (List of ``int`` ``32-bit``):
            Deleted scheduled messages

        sent_messages (List of ``int`` ``32-bit``, *optional*):
            If set, this update indicates that some scheduled messages were sent (not simply deleted from the schedule queue).  In this case, the messages field will contain the scheduled message IDs for the sent messages (initially returned in updateNewScheduledMessage), and sent_messages will contain the real message IDs for the sent messages.

    """

    __slots__: list[str] = ["peer", "messages", "sent_messages"]

    ID = 0xf2a71983
    QUALNAME = "types.UpdateDeleteScheduledMessages"

    def __init__(self, *, peer: "raw.base.Peer", messages: list[int], sent_messages: Optional[list[int]] = None) -> None:
        self.peer = peer  # Peer
        self.messages = messages  # Vector<int>
        self.sent_messages = sent_messages  # flags.0?Vector<int>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateDeleteScheduledMessages":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b)
        
        messages = TLObject.read(b, Int)
        
        sent_messages = TLObject.read(b, Int) if flags & (1 << 0) else []
        
        return UpdateDeleteScheduledMessages(peer=peer, messages=messages, sent_messages=sent_messages)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.sent_messages else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Vector(self.messages, Int))
        
        if self.sent_messages is not None:
            b.write(Vector(self.sent_messages, Int))
        
        return b.getvalue()
