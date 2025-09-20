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


class SavePreparedInlineMessage(TLObject):  # type: ignore
    """Save a prepared inline message, to be shared by the user of the mini app using a web_app_send_prepared_message event


    Details:
        - Layer: ``200``
        - ID: ``F21F7F2F``

    Parameters:
        result (:obj:`InputBotInlineResult <pyrogram.raw.base.InputBotInlineResult>`):
            The message

        user_id (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            The user to whom the web_app_send_prepared_message event event will be sent

        peer_types (List of :obj:`InlineQueryPeerType <pyrogram.raw.base.InlineQueryPeerType>`, *optional*):
            Types of chats where this message can be sent

    Returns:
        :obj:`messages.BotPreparedInlineMessage <pyrogram.raw.base.messages.BotPreparedInlineMessage>`
    """

    __slots__: list[str] = ["result", "user_id", "peer_types"]

    ID = 0xf21f7f2f
    QUALNAME = "functions.messages.SavePreparedInlineMessage"

    def __init__(self, *, result: "raw.base.InputBotInlineResult", user_id: "raw.base.InputUser", peer_types: Optional[list["raw.base.InlineQueryPeerType"]] = None) -> None:
        self.result = result  # InputBotInlineResult
        self.user_id = user_id  # InputUser
        self.peer_types = peer_types  # flags.0?Vector<InlineQueryPeerType>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SavePreparedInlineMessage":
        
        flags = Int.read(b)
        
        result = TLObject.read(b)
        
        user_id = TLObject.read(b)
        
        peer_types = TLObject.read(b) if flags & (1 << 0) else []
        
        return SavePreparedInlineMessage(result=result, user_id=user_id, peer_types=peer_types)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.peer_types else 0
        b.write(Int(flags))
        
        b.write(self.result.write())
        
        b.write(self.user_id.write())
        
        if self.peer_types is not None:
            b.write(Vector(self.peer_types))
        
        return b.getvalue()
