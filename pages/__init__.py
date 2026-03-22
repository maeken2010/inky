from . import weather, clock, date, cal

PAGES = [weather, clock, date, cal]
PAGE_NAMES = {p.__name__.split('.')[-1]: p for p in PAGES}
