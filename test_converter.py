from os.path import join

from src.utils.fb2_converter import convert
from src.core import settings

fb = join(settings.base_dir, r"src/utils/voina-i-mir.fb2")
epub = join(settings.base_dir, r"sandbox")
convert(fb, epub)
