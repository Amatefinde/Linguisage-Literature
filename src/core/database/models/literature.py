from datetime import datetime

from sqlalchemy import func, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Literature(Base):
    __abstract__ = True
    cover: Mapped[str]
    title: Mapped[str]
    original_pdf: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
        server_default=func.now(),
    )
    last_opened_at: Mapped[datetime | None]
    last_read_position: Mapped[int | None]


class LiteratureEpub(Literature):
    __tablename__ = "literature_epub"


class LiteraturePDF(Literature):
    __tablename__ = "literature_pdf"
    pages: Mapped["PdfPageImg"] = relationship(back_populates="literature")


class PdfPageImg(Base):
    __tablename__ = "pdf_page_img"
    page_number: Mapped[int] = mapped_column()
    literature_id: Mapped[int] = mapped_column(ForeignKey("literature_pdf.id"))
    literature: Mapped["LiteraturePDF"] = relationship(back_populates="pages")

    CheckConstraint("page_number >= 1", name="check_page_number_constraint")
