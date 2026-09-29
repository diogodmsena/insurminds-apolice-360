import os
from typing import Dict, Any
from backend.app.agents.base import BaseAgent
from backend.app.services.ocr_service import OCRService

class IngestionAgent(BaseAgent):
    """
    Agente responsável por:
    1. Recebimento e validação de tipo de documento (PDF, Imagens).
    2. Execução da extração digital ou OCR via OCRService.
    3. Segmentação inicial e contagem de páginas.
    """
    def __init__(self, ocr_service: OCRService = None):
        super().__init__("IngestionAgent")
        self.ocr_service = ocr_service or OCRService()

    def run(self, file_path: str) -> Dict[str, Any]:
        self.logger.info(f"Iniciando ingestão do documento: {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não localizado: {file_path}")

        extracted = self.ocr_service.extract_document(file_path)
        
        # Análise básica de qualidade do texto extraído
        total_chars = sum(p["char_count"] for p in extracted["pages"])
        has_adequate_text = total_chars > 100

        self.logger.info(f"Ingestão concluída. Páginas: {extracted['total_pages']}, Caracteres: {total_chars}")
        return {
            "file_name": extracted["file_name"],
            "file_path": extracted["file_path"],
            "total_pages": extracted["total_pages"],
            "has_scanned_pages": extracted["has_scanned_pages"],
            "full_text": extracted["full_text"],
            "pages": extracted["pages"],
            "metadata": extracted["metadata"],
            "has_adequate_text": has_adequate_text,
            "status": "sucesso"
        }
