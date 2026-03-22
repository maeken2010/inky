from . import weather, date, cal

PAGES = [weather, date, cal]
PAGE_NAMES = {p.__name__.split('.')[-1]: p for p in PAGES}
