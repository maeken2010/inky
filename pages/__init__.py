from . import weather, date, cal, photo

PAGES = [weather, date, cal, photo]
PAGE_NAMES = {p.__name__.split('.')[-1]: p for p in PAGES}
