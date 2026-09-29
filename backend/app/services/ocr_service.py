import os
import fitz  # PyMuPDF
from typing import Dict, Any, List
import logging
from PIL import Image

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        self.tesseract_available = False
        try:
            import pytesseract
            self.pytesseract = pytesseract
            self.tesseract_available = True
        except ImportError:
            self.pytesseract = None

    def extract_document(self, file_path: str) -> Dict[str, Any]:
        """
        Extrai texto e metadados de arquivos PDF ou de imagens.
        Suporta PDF nativo com alta fidelidade de paginação e fallback OCR.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext in [".pdf"]:
            return self._extract_pdf(file_path)
        elif file_ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"]:
            return self._extract_image(file_path)
        else:
            raise ValueError(f"Formato não suportado: {file_ext}")

    def _extract_pdf(self, file_path: str) -> Dict[str, Any]:
        doc = fitz.open(file_path)
        pages_content: List[Dict[str, Any]] = []
        full_text_list = []
        total_pages = len(doc)
        has_scanned_pages = False

        for page_idx in range(total_pages):
            page = doc[page_idx]
            page_text = page.get_text("text").strip()
            
            # Se a página contiver menos de 30 caracteres mas contiver imagens, tenta OCR se disponível
            if len(page_text) < 30 and len(page.get_images()) > 0 and self.tesseract_available:
                try:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    ocr_text = self.pytesseract.image_to_string(img, lang="por")
                    if len(ocr_text.strip()) > len(page_text):
                        page_text = ocr_text.strip()
                        has_scanned_pages = True
                except Exception as e:
                    logger.warning(f"Erro no OCR da página {page_idx + 1}: {e}")

            pages_content.append({
                "page_number": page_idx + 1,
                "text": page_text,
                "char_count": len(page_text)
            })
            full_text_list.append(f"--- PÁGINA {page_idx + 1} ---\n{page_text}")

        meta = doc.metadata or {}
        full_text = "\n\n".join(full_text_list)
        doc.close()

        return {
            "file_name": os.path.basename(file_path),
            "file_path": file_path,
            "total_pages": total_pages,
            "metadata": meta,
            "has_scanned_pages": has_scanned_pages,
            "full_text": full_text,
            "pages": pages_content
        }

    def _extract_image(self, file_path: str) -> Dict[str, Any]:
        text = ""
        if self.tesseract_available:
            try:
                img = Image.open(file_path)
                text = self.pytesseract.image_to_string(img, lang="por")
            except Exception as e:
                logger.warning(f"Erro no OCR da imagem {file_path}: {e}")
                text = f"[OCR indisponível para imagem: {os.path.basename(file_path)}]"
        else:
            text = f"[Tesseract não configurado para imagem: {os.path.basename(file_path)}]"

        return {
            "file_name": os.path.basename(file_path),
            "file_path": file_path,
            "total_pages": 1,
            "metadata": {"format": "image"},
            "has_scanned_pages": True,
            "full_text": f"--- IMAGEM ---\n{text}",
            "pages": [{"page_number": 1, "text": text, "char_count": len(text)}]
        }
