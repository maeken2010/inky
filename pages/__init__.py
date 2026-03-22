from . import weather

PAGES = [weather]
PAGE_NAMES = {p.__name__.split('.')[-1]: p for p in PAGES}
