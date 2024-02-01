from os.path import join

from src.utils.fb2_converter import convert
import platform
from src.core import settings

if __name__ == "__main__":

    fb = join(settings.base_dir, r"src\utils\voina-i-mir.fb2")
    epub = join(settings.base_dir, r"sandbox")
    convert(fb, epub)
