import os

from fastapi import UploadFile


class TextManager:
    def __init__(self, file: UploadFile):
        self.file = file.file
        self.file_name = file.filename
        self.file_extension = os.path.splitext(file.filename)[1]



