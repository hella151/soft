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


class ForwardMessages(TLObject):  # type: ignore
    """Forwards messages by their IDs.


    Details:
        - Layer: ``200``
        - ID: ``BB9FA475``

    Parameters:
        from_peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            Source of messages

        id (List of ``int`` ``32-bit``):
            IDs of messages

        random_id (List of ``int`` ``64-bit``):
            Random ID to prevent resending of messages

        to_peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            Destination peer

        silent (``bool``, *optional*):
            Whether to send messages silently (no notification will be triggered on the destination clients)

        background (``bool``, *optional*):
            Whether to send the message in background

        with_my_score (``bool``, *optional*):
            When forwarding games, whether to include your score in the game

        drop_author (``bool``, *optional*):
            Whether to forward messages without quoting the original author

        drop_media_captions (``bool``, *optional*):
            Whether to strip captions from media

        noforwards (``bool``, *optional*):
            Only for bots, disallows further re-forwarding and saving of the messages, even if the destination chat doesn't have content protection enabled

        allow_paid_floodskip (``bool``, *optional*):
            Bots only: if set, allows sending up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.

        top_msg_id (``int`` ``32-bit``, *optional*):
            Destination forum topic

        schedule_date (``int`` ``32-bit``, *optional*):
            Scheduled message date for scheduled messages

        send_as (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`, *optional*):
            Forward the messages as the specified peer

        quick_reply_shortcut (:obj:`InputQuickReplyShortcut <pyrogram.raw.base.InputQuickReplyShortcut>`, *optional*):
            Add the messages to the specified quick reply shortcut », instead.

        video_timestamp (``int`` ``32-bit``, *optional*):
            N/A

        allow_paid_stars (``int`` ``64-bit``, *optional*):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: list[str] = ["from_peer", "id", "random_id", "to_peer", "silent", "background", "with_my_score", "drop_author", "drop_media_captions", "noforwards", "allow_paid_floodskip", "top_msg_id", "schedule_date", "send_as", "quick_reply_shortcut", "video_timestamp", "allow_paid_stars"]

    ID = 0xbb9fa475
    QUALNAME = "functions.messages.ForwardMessages"

    def __init__(self, *, from_peer: "raw.base.InputPeer", id: list[int], random_id: list[int], to_peer: "raw.base.InputPeer", silent: Optional[bool] = None, background: Optional[bool] = None, with_my_score: Optional[bool] = None, drop_author: Optional[bool] = None, drop_media_captions: Optional[bool] = None, noforwards: Optional[bool] = None, allow_paid_floodskip: Optional[bool] = None, top_msg_id: Optional[int] = None, schedule_date: Optional[int] = None, send_as: "raw.base.InputPeer" = None, quick_reply_shortcut: "raw.base.InputQuickReplyShortcut" = None, video_timestamp: Optional[int] = None, allow_paid_stars: Optional[int] = None) -> None:
        self.from_peer = from_peer  # InputPeer
        self.id = id  # Vector<int>
        self.random_id = random_id  # Vector<long>
        self.to_peer = to_peer  # InputPeer
        self.silent = silent  # flags.5?true
        self.background = background  # flags.6?true
        self.with_my_score = with_my_score  # flags.8?true
        self.drop_author = drop_author  # flags.11?true
        self.drop_media_captions = drop_media_captions  # flags.12?true
        self.noforwards = noforwards  # flags.14?true
        self.allow_paid_floodskip = allow_paid_floodskip  # flags.19?true
        self.top_msg_id = top_msg_id  # flags.9?int
        self.schedule_date = schedule_date  # flags.10?int
        self.send_as = send_as  # flags.13?InputPeer
        self.quick_reply_shortcut = quick_reply_shortcut  # flags.17?InputQuickReplyShortcut
        self.video_timestamp = video_timestamp  # flags.20?int
        self.allow_paid_stars = allow_paid_stars  # flags.21?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ForwardMessages":
        
        flags = Int.read(b)
        
        silent = True if flags & (1 << 5) else False
        background = True if flags & (1 << 6) else False
        with_my_score = True if flags & (1 << 8) else False
        drop_author = True if flags & (1 << 11) else False
        drop_media_captions = True if flags & (1 << 12) else False
        noforwards = True if flags & (1 << 14) else False
        allow_paid_floodskip = True if flags & (1 << 19) else False
        from_peer = TLObject.read(b)
        
        id = TLObject.read(b, Int)
        
        random_id = TLObject.read(b, Long)
        
        to_peer = TLObject.read(b)
        
        top_msg_id = Int.read(b) if flags & (1 << 9) else None
        schedule_date = Int.read(b) if flags & (1 << 10) else None
        send_as = TLObject.read(b) if flags & (1 << 13) else None
        
        quick_reply_shortcut = TLObject.read(b) if flags & (1 << 17) else None
        
        video_timestamp = Int.read(b) if flags & (1 << 20) else None
        allow_paid_stars = Long.read(b) if flags & (1 << 21) else None
        return ForwardMessages(from_peer=from_peer, id=id, random_id=random_id, to_peer=to_peer, silent=silent, background=background, with_my_score=with_my_score, drop_author=drop_author, drop_media_captions=drop_media_captions, noforwards=noforwards, allow_paid_floodskip=allow_paid_floodskip, top_msg_id=top_msg_id, schedule_date=schedule_date, send_as=send_as, quick_reply_shortcut=quick_reply_shortcut, video_timestamp=video_timestamp, allow_paid_stars=allow_paid_stars)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 5) if self.silent else 0
        flags |= (1 << 6) if self.background else 0
        flags |= (1 << 8) if self.with_my_score else 0
        flags |= (1 << 11) if self.drop_author else 0
        flags |= (1 << 12) if self.drop_media_captions else 0
        flags |= (1 << 14) if self.noforwards else 0
        flags |= (1 << 19) if self.allow_paid_floodskip else 0
        flags |= (1 << 9) if self.top_msg_id is not None else 0
        flags |= (1 << 10) if self.schedule_date is not None else 0
        flags |= (1 << 13) if self.send_as is not None else 0
        flags |= (1 << 17) if self.quick_reply_shortcut is not None else 0
        flags |= (1 << 20) if self.video_timestamp is not None else 0
        flags |= (1 << 21) if self.allow_paid_stars is not None else 0
        b.write(Int(flags))
        
        b.write(self.from_peer.write())
        
        b.write(Vector(self.id, Int))
        
        b.write(Vector(self.random_id, Long))
        
        b.write(self.to_peer.write())
        
        if self.top_msg_id is not None:
            b.write(Int(self.top_msg_id))
        
        if self.schedule_date is not None:
            b.write(Int(self.schedule_date))
        
        if self.send_as is not None:
            b.write(self.send_as.write())
        
        if self.quick_reply_shortcut is not None:
            b.write(self.quick_reply_shortcut.write())
        
        if self.video_timestamp is not None:
            b.write(Int(self.video_timestamp))
        
        if self.allow_paid_stars is not None:
            b.write(Long(self.allow_paid_stars))
        
        return b.getvalue()
