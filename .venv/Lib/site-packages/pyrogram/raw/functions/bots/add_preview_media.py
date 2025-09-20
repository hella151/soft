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


class AddPreviewMedia(TLObject):  # type: ignore
    """Add a main mini app preview, see here » for more info.


    Details:
        - Layer: ``200``
        - ID: ``17AEB75A``

    Parameters:
        bot (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            The bot that owns the Main Mini App.

        lang_code (``str``):
            ISO 639-1 language code, indicating the localization of the preview to add.

        media (:obj:`InputMedia <pyrogram.raw.base.InputMedia>`):
            The photo/video preview, uploaded using messages.uploadMedia.

    Returns:
        :obj:`BotPreviewMedia <pyrogram.raw.base.BotPreviewMedia>`
    """

    __slots__: list[str] = ["bot", "lang_code", "media"]

    ID = 0x17aeb75a
    QUALNAME = "functions.bots.AddPreviewMedia"

    def __init__(self, *, bot: "raw.base.InputUser", lang_code: str, media: "raw.base.InputMedia") -> None:
        self.bot = bot  # InputUser
        self.lang_code = lang_code  # string
        self.media = media  # InputMedia

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AddPreviewMedia":
        # No flags
        
        bot = TLObject.read(b)
        
        lang_code = String.read(b)
        
        media = TLObject.read(b)
        
        return AddPreviewMedia(bot=bot, lang_code=lang_code, media=media)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.bot.write())
        
        b.write(String(self.lang_code))
        
        b.write(self.media.write())
        
        return b.getvalue()
