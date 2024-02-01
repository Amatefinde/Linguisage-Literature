from src.utils.fb2_converter import convert
import platform

if __name__ == "__main__":

    fb = r"C:\Users\AMDisPOWER\PycharmProjects\Linguisage-Literature\src\utils\voina-i-mir.fb2"
    epub = r"C:\Users\AMDisPOWER\PycharmProjects\Linguisage-Literature\sandbox"
    convert(fb, epub)
