import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_technical_report(output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0B2545"),
        spaceAfter=6,
        alignment=1 # Center
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#134074"),
        spaceAfter=15,
        alignment=1
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0B2545"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading3'],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#134074"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1D2D44"),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=3
    )

    story = []

    # Capa / Cabeçalho Institucional
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>INSTITUTO DE INTELIGÊNCIA ARTIFICIAL APLICADA – I2A2</b>", subtitle_style))
    story.append(Paragraph("<b>RELATÓRIO TÉCNICO DE CONCLUSÃO DE PROJETO FINAL</b>", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>InsurMinds Apólice 360</b>", title_style))
    story.append(Paragraph("Plataforma Inteligente para Análise, Extração e Comparação de Apólices D&O com IA Generativa", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0B2545"), spaceAfter=15))

    # Identificação do Projeto
    ident_data = [
        [Paragraph("<b>Projeto:</b>", body_style), Paragraph("InsurMinds Apólice 360 - Plataforma D&O", body_style)],
        [Paragraph("<b>Domínio de Aplicação:</b>", body_style), Paragraph("Seguros de Responsabilidade Civil de Administradores (D&O)", body_style)],
        [Paragraph("<b>Tecnologias Nucleares:</b>", body_style), Paragraph("Python 3.11, FastAPI, Pydantic, PyMuPDF, IA Generativa (Gemini/OpenAI), React", body_style)],
        [Paragraph("<b>Licença de Software:</b>", body_style), Paragraph("MIT License (Código Aberto)", body_style)],
        [Paragraph("<b>Data de Conclusão:</b>", body_style), Paragraph("Setembro de 2026", body_style)]
    ]
    t_id = Table(ident_data, colWidths=[1.8*inch, 5.0*inch])
    t_id.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0F4F8")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_id)
    story.append(Spacer(1, 15))

    # 1. INTRODUÇÃO E OBJETIVO
    story.append(Paragraph("<b>1. Introdução e Contextualização do Problema</b>", h1_style))
    story.append(Paragraph(
        "Apólices de seguro D&O (Directors & Officers) representam instrumentos contratuais altamente complexos, "
        "com dezenas de páginas redigidas em jargão jurídico rigoroso. Avaliar e comparar propostas concorrentes "
        "demanda tradicionalmente incontáveis horas de especialistas e corretores sêniores, aumentando a vulnerabilidade "
        "de empresas a vazios de cobertura (gaps) patrimoniais em momentos de litígio, investigações regulatórias (CVM/CADE) "
        "ou penhoras judiciais online. O projeto <b>InsurMinds Apólice 360</b> automatiza e qualifica essa análise por meio "
        "de uma arquitetura de múltiplos agentes de Inteligência Artificial Generativa.",
        body_style
    ))

    # 2. ARQUITETURA DA SOLUÇÃO
    story.append(Paragraph("<b>2. Arquitetura da Solução</b>", h1_style))
    story.append(Paragraph(
        "A solução adota uma arquitetura em camadas orientada a serviços (SOA) e desacoplada, separando a recepção documental, "
        "o pipeline multiagente, a camada de persistência e a interface interativa do usuário:",
        body_style
    ))
    story.append(Paragraph("• <b>Camada de Ingestão e OCR:</b> Validação de formato (PDF, TIFF, imagens), extração digital de blocos textuais e OCR para documentos digitalizados.", bullet_style))
    story.append(Paragraph("• <b>Camada de Agentes Especialistas:</b> Orquestração de 5 agentes com responsabilidades únicas e autocontidas.", bullet_style))
    story.append(Paragraph("• <b>Camada de Persistência:</b> Banco relacional SQLite com serialização JSON e esquemas Pydantic rigorosamente tipados.", bullet_style))
    story.append(Paragraph("• <b>Camada de Exposição (API):</b> FastAPI assíncrono com validação OpenAPI e documentação Swagger automática.", bullet_style))
    story.append(Paragraph("• <b>Camada de Apresentação:</b> Aplicação web moderna em React com design corporativo Dark Fintech e dashboards em tempo real.", bullet_style))

    # 3. TECNOLOGIAS UTILIZADAS
    story.append(Paragraph("<b>3. Tecnologias Utilizadas e Justificativa</b>", h1_style))
    tech_data = [
        [Paragraph("<b>Componente</b>", body_style), Paragraph("<b>Tecnologia</b>", body_style), Paragraph("<b>Motivação Técnica</b>", body_style)],
        [Paragraph("Linguagem Principal", body_style), Paragraph("Python 3.11", body_style), Paragraph("Padrão da indústria para pipelines de dados e IA Generativa.", body_style)],
        [Paragraph("Framework de API", body_style), Paragraph("FastAPI + Uvicorn", body_style), Paragraph("Alta performance assíncrona, tipagem Pydantic nativa.", body_style)],
        [Paragraph("Motor de IA Generativa", body_style), Paragraph("Google Gemini / OpenAI / Motor Especialista", body_style), Paragraph("Compreensão semântica profunda de minutas jurídicas com fallback offline.", body_style)],
        [Paragraph("Extração de Documentos", body_style), Paragraph("PyMuPDF (fitz) + Tesseract", body_style), Paragraph("Extração veloz preservando metadados de páginas e coordenadas.", body_style)],
        [Paragraph("Persistência", body_style), Paragraph("SQLite3 + SQLAlchemy Schema", body_style), Paragraph("Armazenamento estruturado leve, confiável e autocontido.", body_style)],
        [Paragraph("Frontend UI", body_style), Paragraph("React + Vite + Design Tokens", body_style), Paragraph("Interface rica, responsiva, com experiência WOW para o usuário.", body_style)]
    ]
    t_tech = Table(tech_data, colWidths=[1.5*inch, 2.0*inch, 3.3*inch])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # 4. DESCRIÇÃO DOS AGENTES DESENVOLVIDOS
    story.append(Paragraph("<b>4. Descrição dos Agentes Especializados</b>", h1_style))
    story.append(Paragraph(
        "Seguindo a recomendação expressa do edital do I2A2 (pág. 24), a inteligência do sistema foi particionada em agentes funcionais:",
        body_style
    ))
    story.append(Paragraph("1. <b>IngestionAgent:</b> Realiza triagem dos arquivos submetidos, analisa a integridade do arquivo, executa PyMuPDF para parsing estrutural nativo e aciona OCR quando detecta páginas escaneadas.", bullet_style))
    story.append(Paragraph("2. <b>ExtractionAgent:</b> Atua como perito em regulação securitária. Mapeia dados vitais: Tomador, LMG (Limite Máximo de Garantia), Sublimites, Franquias (POS), Coberturas Básicas e Adicionais, Exclusões e Cláusula de Retroatividade.", bullet_style))
    story.append(Paragraph("3. <b>ValidationAgent:</b> Executa a checagem de conformidade com as regras da Circular SUSEP 553/2017. Verifica se nenhum sublimite extrapola o LMG, confere cronologia de vigência e atribui o Índice de Confiança (0 a 100%).", bullet_style))
    story.append(Paragraph("4. <b>ComparisonAgent:</b> Cruza 2 ou mais apólices estruturadas, gerando matriz de coberturas lado a lado, mapa de assimetrias, gaps de proteção, scorecards de proteção global e parecer executivo para a diretoria.", bullet_style))
    story.append(Paragraph("5. <b>QnAAgent:</b> Consultor interativo RAG que responde a questionamentos em linguagem natural, citando expressamente as cláusulas e páginas contratuais correspondentes.", bullet_style))

    # 5. FLUXO COMPLETO DE PROCESSAMENTO
    story.append(Paragraph("<b>5. Fluxo Completo de Processamento Ponta a Ponta</b>", h1_style))
    story.append(Paragraph(
        "O ciclo de processamento ocorre em 6 etapas coordenadas: (1) <i>Upload</i> do PDF ou imagem na interface web; "
        "(2) <i>Ingestão</i> com normalização textual e preservação de paginação; (3) <i>Extração Semântica</i> via IA com validação de esquema JSON; "
        "(4) <i>Auditoria e Persistência</i> no SQLite; (5) <i>Análise Comparativa</i> sob demanda com geração de matriz de divergências; e "
        "(6) <i>Exibição Interativa</i> com gráficos, scorecards e chat consultivo com citação de fontes.",
        body_style
    ))

    # 6. JUSTIFICATIVA DAS DECISÕES ARQUITETURAIS
    story.append(Paragraph("<b>6. Justificativa das Decisões Arquiteturais</b>", h1_style))
    story.append(Paragraph(
        "• <b>Mecanismo Híbrido com Fallback Resiliente:</b> A plataforma foi concebida para operar tanto conectada a provedores de LLM "
        "de ponta (Google Gemini, OpenAI) quanto em modo totalmente offline via Motor Especialista Heurístico. Essa decisão garante que o projeto "
        "possa ser avaliado pela banca sem riscos de falha por indisponibilidade de rede ou chave de API externa.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Validação Estrita via Pydantic:</b> O tráfego de dados entre agentes é 100% tipado, eliminando alucinações na formatação de valores "
        "financeiros e garantindo que limites monetários sejam validados antes da gravação em banco.",
        body_style
    ))

    # 7. LIMITAÇÕES CONHECIDAS E EVOLUÇÃO FUTURA
    story.append(Paragraph("<b>7. Limitações Conhecidas e Possibilidades de Evolução</b>", h1_style))
    story.append(Paragraph(
        "<b>Limitações Atuais:</b> Foco especializado em contratos D&O (não estendido a RC Geral ou Transportes); sensibilidade a PDFs "
        "com caligrafia manuscrita de baixa resolução em documentos antigos não padronizados.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Evolução Futura:</b> (a) Integração direta com o sistema de registro eletrônico de apólices da SUSEP e APIs de corretores; "
        "(b) Agente de precificação atuarial preditiva comparando sinistralidade setorial; (c) Emissão automatizada de cartas de recusa ou endossos de contratação.",
        body_style
    ))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=10))
    story.append(Paragraph("<i>InsurMinds Apólice 360 • Instituto de Inteligência Artificial Aplicada (I2A2) • 2026</i>", subtitle_style))

    doc.build(story)
    print(f"Relatório Técnico gerado com sucesso em: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_artifacts = os.path.join(base_dir, "Projeto_Final_Artefatos", "InsurMinds_Relatorio_Tecnico.pdf")
    target_root = os.path.join(base_dir, "InsurMinds_Relatorio_Tecnico.pdf")
    generate_technical_report(target_artifacts)
    shutil.copyfile(target_artifacts, target_root)
