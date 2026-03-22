from . import weather, clock, date

PAGES = [weather, clock, date]
PAGE_NAMES = {p.__name__.split('.')[-1]: p for p in PAGES}
