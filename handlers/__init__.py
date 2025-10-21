from .reply import reply_handler
from .inline import inline_handler
# Все хендлеры в одном месте
all_handlers = reply_handler + inline_handler

__all__ = ['reply_handler', 'inline_handler', 'all_handlers']