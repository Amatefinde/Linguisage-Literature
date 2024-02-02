import os
import zipfile
from lxml import etree
from typing import IO
from PIL import Image


NAMESPACES = {
    "dc": "http://purl.org/dc/elements/1.1/",
    "calibre": "http://calibre.kovidgoyal.net/2009/metadata",
    "opf": "http://www.idpf.org/2007/opf",
    "dcterms": "http://purl.org/dc/terms/",
    "xhtml": "http://www.w3.org/1999/xhtml",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "u": "urn:oasis:names:tc:opendocument:xmlns:container",
}


def __handle_epub2(t):
    try:
        cover_id = t.xpath(
            "//opf:metadata/opf:meta[@name='cover']",
            namespaces=NAMESPACES,
        )[0].get("content")
        cover_href = t.xpath(
            "//opf:manifest/opf:item[@id='" + cover_id + "']",
            namespaces=NAMESPACES,
        )[0].get("href")
        return cover_href
    except IndexError:
        pass


def __handle_epub3(t):
    try:
        cover_href = t.xpath(
            "//opf:manifest/opf:item[@properties='cover-image']",
            namespaces=NAMESPACES,
        )[0].get("href")
        return cover_href
    except IndexError:
        pass


def __handle_other_cases(t, root_file_path, z):
    try:
        cover_page_id = t.xpath("//opf:spine/opf:itemref", namespaces=NAMESPACES)[0].get(
            "idref"
        )
        cover_page_href = t.xpath(
            "//opf:manifest/opf:item[@id='" + cover_page_id + "']",
            namespaces=NAMESPACES,
        )[0].get("href")
        cover_page_path = os.path.join(os.path.dirname(root_file_path), cover_page_href)
        t = etree.fromstring(z.read(cover_page_path.replace("\\", "/")))
        cover_href = t.xpath("//xhtml:img", namespaces=NAMESPACES)[0].get("src")
        return cover_href
    except IndexError:
        pass


def __find_cover_href(lxml_tree, root_file_path, zip_file):
    cover_href = __handle_epub2(lxml_tree)
    if not cover_href:
        cover_href = __handle_epub3(lxml_tree)
    if not cover_href:
        cover_href = __handle_other_cases(lxml_tree, root_file_path, zip_file)
    if not cover_href:
        return None
    return cover_href


def extract_cover_from_epub(
    epub: str | os.PathLike[str] | IO[bytes],
) -> Image.Image | None:
    with zipfile.ZipFile(epub) as zip_file:
        lxml_tree = etree.fromstring(zip_file.read("META-INF/container.xml"))
        root_file_path = lxml_tree.xpath(
            "/u:container/u:rootfiles/u:rootfile", namespaces=NAMESPACES
        )[0].get("full-path")
        lxml_tree = etree.fromstring(zip_file.read(root_file_path))
        cover_href = __find_cover_href(lxml_tree, root_file_path, zip_file)
        cover_path = os.path.join(
            str(os.path.dirname(root_file_path)),
            cover_href,
        ).replace("\\", "/")
        cover_path = zip_file.open(cover_path)
        cover_image = Image.open(cover_path)
        return cover_image


if __name__ == "__main__":
    epubfile = "voina-i-mir.epub"
    cover = extract_cover_from_epub(epubfile)
    cover.show()
