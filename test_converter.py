from os.path import join

from src.utils.fb2_converter import convert
from src.core import settings

fb = "src/utils/voina-i-mir.fb2"
epub = "sandbox"
convert(fb, epub)
