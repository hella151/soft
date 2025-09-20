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


class GlobalPrivacySettings(TLObject):  # type: ignore
    """Global privacy settings

    Constructor of :obj:`~pyrogram.raw.base.GlobalPrivacySettings`.

    Details:
        - Layer: ``200``
        - ID: ``C9D8DF1C``

    Parameters:
        archive_and_mute_new_noncontact_peers (``bool``, *optional*):
            Whether to archive and mute new chats from non-contacts

        keep_archived_unmuted (``bool``, *optional*):
            Whether unmuted chats will be kept in the Archive chat list when they get a new message.

        keep_archived_folders (``bool``, *optional*):
            Whether unmuted chats that are always included or pinned in a folder, will be kept in the Archive chat list when they get a new message. Ignored if keep_archived_unmuted is set.

        hide_read_marks (``bool``, *optional*):
            If this flag is set, the inputPrivacyKeyStatusTimestamp key will also apply to the ability to use messages.getOutboxReadDate on messages sent to us. Meaning, users that cannot see our exact last online date due to the current value of the inputPrivacyKeyStatusTimestamp key will receive a 403 USER_PRIVACY_RESTRICTED error when invoking messages.getOutboxReadDate to fetch the exact read date of a message they sent to us. The userFull.read_dates_private flag will be set for users that have this flag enabled.

        new_noncontact_peers_require_premium (``bool``, *optional*):
            If set, only users that have a premium account, are in our contact list, or already have a private chat with us can write to us; a 403 PRIVACY_PREMIUM_REQUIRED error will be emitted otherwise.  The userFull.contact_require_premium flag will be set for users that have this flag enabled.  To check whether we can write to a user with this flag enabled, if we haven't yet cached all the required information (for example we don't have the userFull or history of all users while displaying the chat list in the sharing UI) the users.getIsPremiumRequiredToContact method may be invoked, passing the list of users currently visible in the UI, returning a list of booleans that directly specify whether we can or cannot write to each user. This option may be enabled by both non-Premium and Premium users only if the new_noncontact_peers_require_premium_without_ownpremium client configuration flag » is equal to true, otherwise it may be enabled only by Premium users and non-Premium users will receive a PREMIUM_ACCOUNT_REQUIRED error when trying to enable this flag.

        noncontact_peers_paid_stars (``int`` ``64-bit``, *optional*):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetGlobalPrivacySettings
            account.SetGlobalPrivacySettings
    """

    __slots__: list[str] = ["archive_and_mute_new_noncontact_peers", "keep_archived_unmuted", "keep_archived_folders", "hide_read_marks", "new_noncontact_peers_require_premium", "noncontact_peers_paid_stars"]

    ID = 0xc9d8df1c
    QUALNAME = "types.GlobalPrivacySettings"

    def __init__(self, *, archive_and_mute_new_noncontact_peers: Optional[bool] = None, keep_archived_unmuted: Optional[bool] = None, keep_archived_folders: Optional[bool] = None, hide_read_marks: Optional[bool] = None, new_noncontact_peers_require_premium: Optional[bool] = None, noncontact_peers_paid_stars: Optional[int] = None) -> None:
        self.archive_and_mute_new_noncontact_peers = archive_and_mute_new_noncontact_peers  # flags.0?true
        self.keep_archived_unmuted = keep_archived_unmuted  # flags.1?true
        self.keep_archived_folders = keep_archived_folders  # flags.2?true
        self.hide_read_marks = hide_read_marks  # flags.3?true
        self.new_noncontact_peers_require_premium = new_noncontact_peers_require_premium  # flags.4?true
        self.noncontact_peers_paid_stars = noncontact_peers_paid_stars  # flags.5?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GlobalPrivacySettings":
        
        flags = Int.read(b)
        
        archive_and_mute_new_noncontact_peers = True if flags & (1 << 0) else False
        keep_archived_unmuted = True if flags & (1 << 1) else False
        keep_archived_folders = True if flags & (1 << 2) else False
        hide_read_marks = True if flags & (1 << 3) else False
        new_noncontact_peers_require_premium = True if flags & (1 << 4) else False
        noncontact_peers_paid_stars = Long.read(b) if flags & (1 << 5) else None
        return GlobalPrivacySettings(archive_and_mute_new_noncontact_peers=archive_and_mute_new_noncontact_peers, keep_archived_unmuted=keep_archived_unmuted, keep_archived_folders=keep_archived_folders, hide_read_marks=hide_read_marks, new_noncontact_peers_require_premium=new_noncontact_peers_require_premium, noncontact_peers_paid_stars=noncontact_peers_paid_stars)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.archive_and_mute_new_noncontact_peers else 0
        flags |= (1 << 1) if self.keep_archived_unmuted else 0
        flags |= (1 << 2) if self.keep_archived_folders else 0
        flags |= (1 << 3) if self.hide_read_marks else 0
        flags |= (1 << 4) if self.new_noncontact_peers_require_premium else 0
        flags |= (1 << 5) if self.noncontact_peers_paid_stars is not None else 0
        b.write(Int(flags))
        
        if self.noncontact_peers_paid_stars is not None:
            b.write(Long(self.noncontact_peers_paid_stars))
        
        return b.getvalue()
