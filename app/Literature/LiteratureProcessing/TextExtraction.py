import asyncio
import json

import aiohttp
import cv2
import pdfplumber
import io
import numpy as np
from typing import TypedDict, List
import time
import requests
from aiohttp import ClientTimeout

from config import static_path as static_path_default
from app.Literature.DAO import LiteratureDAO
from os import path


async def call_to_ocr(np_image, url='http://192.168.31.23:8007/parse_image'):
    start_time_ocr = time.time()
    _, img_encoded = cv2.imencode(".jpg", np_image)
    data = aiohttp.FormData()
    file = img_encoded.tobytes()
    data.add_field("file", file, filename="image.jpg")
    timeout = ClientTimeout(total=60 * 60 * 3)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, data=data) as response:
            if response.status == 200:
                print("Time for ocr:", time.time() - start_time_ocr)
                return await response.json()
            else:
                raise AssertionError("OCR сервер не доступен в данный момент")


class WordSchema(TypedDict):
    text: str
    start: int
    end: int
    top: int
    bottom: int


class PageSchema(TypedDict):
    pageWidth: int
    pageHeight: int
    words: List[WordSchema]


font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 3

SCALE = 3


async def parse_pfd(
        pdf_bytesio: io.BytesIO | str,
        literature_number: str | int,
        static_path: str = path.join(static_path_default, "literature_pages"),
        use_ocr=False
) -> List[PageSchema]:


    parsed_pages = []
    literature_number = str(literature_number)
    with pdfplumber.open(pdf_bytesio) as pdf:
        for page in pdf.pages:

            print(f"Pages: {page.page_number}")
            parsed_page = {
                "pageWidth": int(page.bbox[2]) * SCALE,
                "pageHeight": int(page.bbox[3]) * SCALE,
                "words": [],
            }
            image = page.to_image(width=parsed_page["pageWidth"], antialias=True)

            cv2_image = np.array(image.original)
            cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGB2BGR)

            if use_ocr:
                parsed_page["words"] = await call_to_ocr(cv2_image)

            else:
                for element in page.extract_words():
                    parsed_page["words"].append({
                        "text": element["text"],
                        "start": int(element["x0"]) * SCALE,
                        "end": int(element["x1"]) * SCALE,
                        "top": int(element["top"]) * SCALE,
                        "bottom": int(element["bottom"]) * SCALE,
                    })

            # for word in parsed_page["words"]:
            #     cv2_image = cv2.rectangle(cv2_image, (word["start"], word["top"]), (word["end"], word["bottom"]), (255, 0, 0), 2)
            #     cv2_image = cv2.putText(cv2_image, word["text"], (word["start"], word["bottom"]), font, fontScale, (0, 0, 200), 5, cv2.LINE_AA)
            # cv2_image = cv2.resize(cv2_image, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_LINEAR)
            fullpath = path.join(static_path, literature_number) + "_" + str(page.page_number) + ".jpeg"
            image.save(fullpath, quantize=False, format="JPEG", bits=16 )
            parsed_pages.append(parsed_page)

            response_db = await LiteratureDAO.add_page_for_literature(
                word_data=parsed_page,
                literature_number=literature_number,
                number_page=page.page_number,
                image_path="static\\literature_pages\\" + literature_number + "_" + str(page.page_number) + ".jpeg"
            )
            if response_db != 200:
                print("При добавлении информации в бд о странице произошла ошибка")

        return parsed_pages


if __name__ == "__main__":
    start_time = time.time()
    async def main():
        with open(r"E:\all\studying\Linguisage-Content\app\static\literature_original\16.pdf", "rb") as file:
            book_bytes = io.BytesIO(file.read())
        pages = await parse_pfd(book_bytes, 83, "")
        print(pages)


    asyncio.run(main())

    print(time.time() - start_time)
