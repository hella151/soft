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


class StarsGiveawayOption(TLObject):  # type: ignore
    """Contains info about a Telegram Star giveaway option.

    Constructor of :obj:`~pyrogram.raw.base.StarsGiveawayOption`.

    Details:
        - Layer: ``200``
        - ID: ``94CE852A``

    Parameters:
        stars (``int`` ``64-bit``):
            The number of Telegram Stars that will be distributed among winners

        yearly_boosts (``int`` ``32-bit``):
            Number of times the chat will be boosted for one year if the inputStorePaymentStarsGiveaway.boost_peer flag is populated

        currency (``str``):
            Three-letter ISO 4217 currency code

        amount (``int`` ``64-bit``):
            Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).

        winners (List of :obj:`StarsGiveawayWinnersOption <pyrogram.raw.base.StarsGiveawayWinnersOption>`):
            Allowed options for the number of giveaway winners.

        extended (``bool``, *optional*):
            If set, this option must only be shown in the full list of giveaway options (i.e. they must be added to the list only when the user clicks on the expand button).

        default (``bool``, *optional*):
            If set, this option must be pre-selected by default in the option list.

        store_product (``str``, *optional*):
            Identifier of the store product associated with the option, official apps only.

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            payments.GetStarsGiveawayOptions
    """

    __slots__: list[str] = ["stars", "yearly_boosts", "currency", "amount", "winners", "extended", "default", "store_product"]

    ID = 0x94ce852a
    QUALNAME = "types.StarsGiveawayOption"

    def __init__(self, *, stars: int, yearly_boosts: int, currency: str, amount: int, winners: list["raw.base.StarsGiveawayWinnersOption"], extended: Optional[bool] = None, default: Optional[bool] = None, store_product: Optional[str] = None) -> None:
        self.stars = stars  # long
        self.yearly_boosts = yearly_boosts  # int
        self.currency = currency  # string
        self.amount = amount  # long
        self.winners = winners  # Vector<StarsGiveawayWinnersOption>
        self.extended = extended  # flags.0?true
        self.default = default  # flags.1?true
        self.store_product = store_product  # flags.2?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarsGiveawayOption":
        
        flags = Int.read(b)
        
        extended = True if flags & (1 << 0) else False
        default = True if flags & (1 << 1) else False
        stars = Long.read(b)
        
        yearly_boosts = Int.read(b)
        
        store_product = String.read(b) if flags & (1 << 2) else None
        currency = String.read(b)
        
        amount = Long.read(b)
        
        winners = TLObject.read(b)
        
        return StarsGiveawayOption(stars=stars, yearly_boosts=yearly_boosts, currency=currency, amount=amount, winners=winners, extended=extended, default=default, store_product=store_product)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.extended else 0
        flags |= (1 << 1) if self.default else 0
        flags |= (1 << 2) if self.store_product is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.stars))
        
        b.write(Int(self.yearly_boosts))
        
        if self.store_product is not None:
            b.write(String(self.store_product))
        
        b.write(String(self.currency))
        
        b.write(Long(self.amount))
        
        b.write(Vector(self.winners))
        
        return b.getvalue()
