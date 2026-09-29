import os
import shutil
import cv2
import numpy as np

def create_demo_video(output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    width, height = 1280, 720
    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Cenas de apresentação do vídeo (problema, arquitetura, funcionamento, resultados)
    scenes = [
        {
            "tag": "INSTITUTO DE INTELIGÊNCIA ARTIFICIAL APLICADA (I2A2)",
            "title": "InsurMinds Apólice 360",
            "subtitle": "Plataforma Inteligente para Análise e Comparação de Apólices D&O com IA",
            "bullets": [
                "Projeto Final de Conclusão de Curso - Módulo Avançado",
                "Equipe InsurMinds - Setembro de 2026"
            ],
            "duration_sec": 4,
            "theme": (11, 15, 25) # Dark BGR
        },
        {
            "tag": "PARTE 1: O PROBLEMA ABORDADO",
            "title": "Complexidade e Vulnerabilidade em Apólices D&O",
            "subtitle": "Riscos ocultos em contratos jurídicos corporativos de 100+ páginas",
            "bullets": [
                "Processo manual que demanda mais de 20 horas de especialistas",
                "Assimetrias em Limites Máximos de Garantia (LMG) e Franquias (POS)",
                "Cláusulas perigosas de Penhora Online e Investigação CVM desprotegidas"
            ],
            "duration_sec": 4,
            "theme": (15, 20, 35)
        },
        {
            "tag": "PARTE 2: A ARQUITETURA DA SOLUÇÃO",
            "title": "Ecossistema Multiagente Especializado em IA",
            "subtitle": "Separação estrita de responsabilidades com validação regulatória",
            "bullets": [
                "1. Ingestion & OCR Agent: Extração digital e OCR com preservação de páginas",
                "2. Extraction Agent: Mapeamento semântico D&O via LLM e Pydantic",
                "3. Validation Agent: Auditoria de limites e compliance com Circular SUSEP 553",
                "4. Comparison Agent: Matriz de gaps, assimetrias e scorecards (0-100)",
                "5. Q&A Consultant Agent: Assistente conversacional com citação de cláusulas"
            ],
            "duration_sec": 5,
            "theme": (20, 25, 45)
        },
        {
            "tag": "PARTE 3: O FUNCIONAMENTO DA APLICAÇÃO",
            "title": "Demonstração do MVP em Execução",
            "subtitle": "Interface Web Moderna integrada ao Backend FastAPI",
            "bullets": [
                "Dashboard gerencial com custódia de apólices e indicadores financeiros",
                "Raio-X da Apólice: detalhamento de LMG, sublimites, coberturas e exclusões",
                "Comparador 360: seleção de apólices e geração de matriz de divergências",
                "Chat Consultivo: respostas instantâneas apontando artigos e páginas"
            ],
            "duration_sec": 5,
            "theme": (25, 30, 50)
        },
        {
            "tag": "PARTE 4: PRINCIPAIS RESULTADOS OBTIDOS",
            "title": "Resultados e Impacto de Negócio",
            "subtitle": "Ganhos mensuráveis na tomada de decisão de executivos e corretoras",
            "bullets": [
                "Redução de 95% no tempo de análise comparativa de apólices corporativas",
                "Detecção preventiva de lacunas (gaps) patrimoniais de diretores e conselheiros",
                "Motor resiliente com suporte a Gemini, OpenAI e fallback offline seguro",
                "Código aberto sob licença MIT e documentação técnica exemplar"
            ],
            "duration_sec": 4,
            "theme": (10, 35, 20)
        },
        {
            "tag": "ENTREGA OFICIAL • I2A2",
            "title": "InsurMinds Apólice 360",
            "subtitle": "Conclusão da Demonstração do Projeto Final",
            "bullets": [
                "Relatório Técnico: InsurMinds_Relatorio_Tecnico.pdf",
                "Pitch Deck: InsurMinds_Projeto_Final.pptx",
                "Repositório GitHub Público & Pasta Projeto_Final_Artefatos/"
            ],
            "duration_sec": 4,
            "theme": (11, 15, 25)
        }
    ]

    for scene in scenes:
        frames_count = int(scene["duration_sec"] * fps)
        bg_color = scene["theme"]

        # Base frame
        frame = np.full((height, width, 3), bg_color, dtype=np.uint8)

        # Header tag
        cv2.putText(frame, scene["tag"], (80, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (212, 182, 6), 2, cv2.LINE_AA)

        # Title
        cv2.putText(frame, scene["title"], (80, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 3, cv2.LINE_AA)

        # Subtitle
        cv2.putText(frame, scene["subtitle"], (80, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (233, 165, 14), 2, cv2.LINE_AA)

        # Separator line
        cv2.line(frame, (80, 220), (width - 80, 220), (80, 80, 80), 2)

        # Bullets
        y_pos = 280
        for b in scene["bullets"]:
            cv2.circle(frame, (95, y_pos - 8), 6, (129, 185, 16), -1)
            cv2.putText(frame, b, (120, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (230, 230, 230), 2, cv2.LINE_AA)
            y_pos += 65

        # Footer badge
        cv2.putText(frame, "InsurMinds Apólice 360 • I2A2 Projeto Final", (80, height - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1, cv2.LINE_AA)

        # Write frames
        for _ in range(frames_count):
            out.write(frame)

    out.release()
    print(f"Vídeo de demonstração gerado com sucesso em: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_artifacts = os.path.join(base_dir, "Projeto_Final_Artefatos", "InsurMinds_Projeto_Final.mp4")
    target_root = os.path.join(base_dir, "InsurMinds_Projeto_Final.mp4")
    create_demo_video(target_artifacts)
    shutil.copyfile(target_artifacts, target_root)
