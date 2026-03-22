from . import weather, clock

PAGES = [weather, clock]
PAGE_NAMES = {p.__name__.split('.')[-1]: p for p in PAGES}
