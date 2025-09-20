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


class InputInvoiceStarGift(TLObject):  # type: ignore
    """Used to buy a Telegram Star Gift, see here » for more info.

    Constructor of :obj:`~pyrogram.raw.base.InputInvoice`.

    Details:
        - Layer: ``200``
        - ID: ``E8625E92``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        gift_id (``int`` ``64-bit``):
            Identifier of the gift, from starGift.id

        hide_name (``bool``, *optional*):
            If set, your name will be hidden if the destination user decides to display the gift on their profile (they will still see that you sent the gift)

        include_upgrade (``bool``, *optional*):
            N/A

        message (:obj:`TextWithEntities <pyrogram.raw.base.TextWithEntities>`, *optional*):
            Optional message, attached with the gift. The maximum length for this field is specified in the stargifts_message_length_max client configuration value ».

    """

    __slots__: list[str] = ["peer", "gift_id", "hide_name", "include_upgrade", "message"]

    ID = 0xe8625e92
    QUALNAME = "types.InputInvoiceStarGift"

    def __init__(self, *, peer: "raw.base.InputPeer", gift_id: int, hide_name: Optional[bool] = None, include_upgrade: Optional[bool] = None, message: "raw.base.TextWithEntities" = None) -> None:
        self.peer = peer  # InputPeer
        self.gift_id = gift_id  # long
        self.hide_name = hide_name  # flags.0?true
        self.include_upgrade = include_upgrade  # flags.2?true
        self.message = message  # flags.1?TextWithEntities

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputInvoiceStarGift":
        
        flags = Int.read(b)
        
        hide_name = True if flags & (1 << 0) else False
        include_upgrade = True if flags & (1 << 2) else False
        peer = TLObject.read(b)
        
        gift_id = Long.read(b)
        
        message = TLObject.read(b) if flags & (1 << 1) else None
        
        return InputInvoiceStarGift(peer=peer, gift_id=gift_id, hide_name=hide_name, include_upgrade=include_upgrade, message=message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.hide_name else 0
        flags |= (1 << 2) if self.include_upgrade else 0
        flags |= (1 << 1) if self.message is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Long(self.gift_id))
        
        if self.message is not None:
            b.write(self.message.write())
        
        return b.getvalue()
