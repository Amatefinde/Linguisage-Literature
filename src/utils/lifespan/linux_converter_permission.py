import platform
import subprocess
from loguru import logger


def give_permission():
    os_name = platform.system()
    if os_name == "Linux":
        file_path = "src/utils/fb2_converter/fb2c"
        chmod_command = ["chmod", "a+x", file_path]
        subprocess.run(chmod_command)
        logger.info("linux permission given")
