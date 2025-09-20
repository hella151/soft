from .reply import reply_handler
from .delete_links import delete_links_handler
from .inline import inline_handler
# Все хендлеры в одном месте
all_handlers = reply_handler + delete_links_handler + inline_handler

__all__ = ['reply_handler', 'delete_links_handler', 'inline_handler', 'all_handlers']