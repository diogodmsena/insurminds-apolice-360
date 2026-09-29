import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_pitch_deck(output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5) # 16:9 Widescreen

    # Paleta Corporativa Insurtech
    C_BG_DARK = RGBColor(11, 15, 25)
    C_CARD_BG = RGBColor(22, 32, 50)
    C_BLUE = RGBColor(14, 165, 233)
    C_CYAN = RGBColor(6, 182, 212)
    C_WHITE = RGBColor(248, 250, 252)
    C_MUTED = RGBColor(148, 163, 184)
    C_EMERALD = RGBColor(16, 185, 129)
    C_ACCENT_BG = RGBColor(15, 23, 42)

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide, color):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category="INSURMINDS APÓLICE 360 • I2A2"):
        # Header category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_CYAN

        # Header title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE

    # ==========================================
    # SLIDE 1: CAPA
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_BG_DARK)

    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.8))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "INSTITUTO DE INTELIGÊNCIA ARTIFICIAL APLICADA (I2A2)"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = C_CYAN
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "InsurMinds Apólice 360"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Plataforma Inteligente para Análise, Extração e Comparação de Apólices D&O com IA Generativa"
    p2.font.size = Pt(18)
    p2.font.color.rgb = C_BLUE
    p2.space_after = Pt(30)

    p3 = tf1.add_paragraph()
    p3.text = "Projeto Final de Conclusão de Curso • Módulo Avançado em IA Generativa • Setembro/2026"
    p3.font.size = Pt(13)
    p3.font.color.rgb = C_MUTED

    # ==========================================
    # SLIDE 2: O PROBLEMA
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, C_BG_DARK)
    add_header(s2, "O Desafio Crítico no Mercado de Seguros D&O", "Contexto & Problema")

    cards_data_s2 = [
        ("Documentos Extensos e Jurídicos", "Contratos com 40 a 100 páginas de texto hermético, onde detalhes em cláusulas de exclusão definem o patrimônio do executivo.", C_BLUE),
        ("Processo Manual e Lento", "Comparar 2 ou 3 apólices exige até 20 horas de especialistas sêniores, gerando gargalos para corretoras e risco moral.", C_CYAN),
        ("Gaps de Proteção Ocultos", "Assimetrias críticas em franquias (POS), penhora online e investigações prévias CVM/CADE passam despercebidas até o sinistro.", C_EMERALD)
    ]
    for i, (head, desc, color) in enumerate(cards_data_s2):
        left = Inches(0.8 + i * 3.9)
        top = Inches(2.2)
        shape = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.6), Inches(4.2))
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_CARD_BG
        shape.line.color.rgb = color
        shape.line.width = Pt(1.5)

        tb = s2.shapes.add_textbox(left + Inches(0.2), top + Inches(0.3), Inches(3.2), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(18)
        p_h.font.bold = True
        p_h.font.color.rgb = color
        p_h.space_after = Pt(12)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = C_WHITE

    # ==========================================
    # SLIDE 3: A SOLUÇÃO INSURMINDS
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, C_BG_DARK)
    add_header(s3, "A Solução: InsurMinds Apólice 360", "Proposta de Valor")

    shape_center = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.6))
    shape_center.fill.solid()
    shape_center.fill.fore_color.rgb = C_CARD_BG
    shape_center.line.color.rgb = C_CYAN

    tb_s3 = s3.shapes.add_textbox(Inches(1.2), Inches(2.3), Inches(11.0), Inches(4.0))
    tf_s3 = tb_s3.text_frame
    tf_s3.word_wrap = True

    p_sol_1 = tf_s3.paragraphs[0]
    p_sol_1.text = "Automação Completa do Ciclo de Análise Securitária com IA"
    p_sol_1.font.size = Pt(22)
    p_sol_1.font.bold = True
    p_sol_1.font.color.rgb = C_CYAN
    p_sol_1.space_after = Pt(14)

    bullet_points = [
        "1. Ingestão Híbrida Inteligente: Processa arquivos PDF digitais e escaneados com OCR e rastreamento de paginação.",
        "2. Extração Semântica Especializada: Mapeia LMG, sublimites, POS/franquias, coberturas e exclusões em segundos.",
        "3. Auditoria Regulatória SUSEP: Validação algorítmica de consistência baseada na Circular SUSEP 553/2017.",
        "4. Comparador Multidimensional: Matriz de divergências lado a lado, radar de score e detecção imediata de gaps.",
        "5. Consultor Securitário RAG: Chat com IA respondendo dúvidas complexas com citação exata de cláusulas e páginas."
    ]
    for bp in bullet_points:
        p_b = tf_s3.add_paragraph()
        p_b.text = bp
        p_b.font.size = Pt(14)
        p_b.font.color.rgb = C_WHITE
        p_b.space_after = Pt(8)

    # ==========================================
    # SLIDE 4: ARQUITETURA MULTIAGENTE
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, C_BG_DARK)
    add_header(s4, "Arquitetura Multiagente de Alta Coesão", "Engenharia de IA")

    agents_data = [
        ("Ingestion Agent", "Recebe documentos, executa parsing PyMuPDF e aciona OCR Tesseract em imagens.", C_BLUE),
        ("Extraction Agent", "Aplica LLM para estruturar entidades D&O em esquemas Pydantic tipados.", C_CYAN),
        ("Validation Agent", "Audita limites vs sublimites, datas e gera score de confiança da extração.", C_EMERALD),
        ("Comparison Agent", "Cruza contratos, computa scores de proteção e formula veredito executivo.", RGBColor(139, 92, 246)),
        ("Q&A Consultant", "Responde a perguntas e litígios citando cláusulas e jurisprudência securitária.", RGBColor(244, 63, 94))
    ]

    for i, (name, role, color) in enumerate(agents_data):
        top_pos = Inches(1.8 + i * 1.0)
        shape_ag = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.7), Inches(0.85))
        shape_ag.fill.solid()
        shape_ag.fill.fore_color.rgb = C_CARD_BG
        shape_ag.line.color.rgb = color
        shape_ag.line.width = Pt(1)

        tb_ag = s4.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.12), Inches(11.3), Inches(0.6))
        tf_ag = tb_ag.text_frame
        p_ag = tf_ag.paragraphs[0]
        p_ag.text = f"{name}: "
        p_ag.font.size = Pt(14)
        p_ag.font.bold = True
        p_ag.font.color.rgb = color

        run_desc = p_ag.add_run()
        run_desc.text = role
        run_desc.font.size = Pt(13)
        run_desc.font.bold = False
        run_desc.font.color.rgb = C_WHITE

    # ==========================================
    # SLIDE 5: RESULTADOS E CASO REAL
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, C_BG_DARK)
    add_header(s5, "Demonstração Prática: Confronto de Apólices Reais", "Resultados do MVP")

    res_cards = [
        ("Porto Seguro D&O", "LMG: R$ 10.000.000,00\n• Foco em litígios cíveis/trabalhistas\n• Sublimite Penhora: R$ 2,5M\n• Franquia PF: R$ 0,00 (Isento)\n• Score de Proteção: 74/100", C_BLUE),
        ("Chubb Corporate Plus", "LMG: R$ 25.000.000,00\n• Extensão CVM/CADE (R$ 7,5M)\n• Penhora Online: R$ 6,25M\n• Gestão de Crise de Imagem\n• Score de Proteção: 86/100", C_CYAN),
        ("Tokio Marine Elite", "LMG: R$ 50.000.000,00\n• Cobertura Mundial com SEC\n• Penhora Online até 100% LMG\n• Práticas Trabalhistas (EPL)\n• Score de Proteção: 96/100", C_EMERALD)
    ]
    for i, (title, text, color) in enumerate(res_cards):
        left = Inches(0.8 + i * 3.9)
        top = Inches(2.0)
        shape = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.6), Inches(4.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_CARD_BG
        shape.line.color.rgb = color
        shape.line.width = Pt(1.5)

        tb = s5.shapes.add_textbox(left + Inches(0.2), top + Inches(0.3), Inches(3.2), Inches(3.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = title
        p_h.font.size = Pt(17)
        p_h.font.bold = True
        p_h.font.color.rgb = color
        p_h.space_after = Pt(10)

        for line in text.split("\n"):
            p_l = tf.add_paragraph()
            p_l.text = line
            p_l.font.size = Pt(12.5)
            p_l.font.color.rgb = C_WHITE
            p_l.space_after = Pt(4)

    # ==========================================
    # SLIDE 6: DIFERENCIAIS E MODELO DE NEGÓCIOS
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, C_BG_DARK)
    add_header(s6, "Diferenciais Competitivos & Mercado Alvo", "Viabilidade & Negócios")

    shape_mkt = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.5))
    shape_mkt.fill.solid()
    shape_mkt.fill.fore_color.rgb = C_CARD_BG
    shape_mkt.line.color.rgb = C_BLUE

    tb_mkt = s6.shapes.add_textbox(Inches(1.2), Inches(2.3), Inches(11.0), Inches(3.8))
    tf_mkt = tb_mkt.text_frame
    tf_mkt.word_wrap = True

    p_m1 = tf_mkt.paragraphs[0]
    p_m1.text = "Inovação Tecnológica com Impacto Direto de Negócio"
    p_m1.font.size = Pt(20)
    p_m1.font.bold = True
    p_m1.font.color.rgb = C_CYAN
    p_m1.space_after = Pt(14)

    points_mkt = [
        "• Redução de 95% no Tempo de Análise: De 20 horas de estudo manual para menos de 60 segundos de processamento.",
        "• Motor Resiliente com Fallback Offline: Nunca falha, garantindo disponibilidade mesmo sob restrições de chaves de API.",
        "• Público Alvo Imediato: Corretoras de Grandes Riscos Corporativos, Departamentos Jurídicos de Empresas S.A. e Fundos de PE/VC.",
        "• Modelo de Receita (SaaS B2B): Assinatura recorrente mensal com créditos de análise por apólice e relatórios em PDF.",
        "• Conformidade SUSEP: Totalmente alinhado às diretrizes regulatórias e termos padrão do mercado securitário brasileiro."
    ]
    for pt in points_mkt:
        p_pt = tf_mkt.add_paragraph()
        p_pt.text = pt
        p_pt.font.size = Pt(13.5)
        p_pt.font.color.rgb = C_WHITE
        p_pt.space_after = Pt(8)

    # ==========================================
    # SLIDE 7: CONCLUSÃO E AGRADECIMENTOS
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, C_BG_DARK)

    tbox_end = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(3.5))
    tf_end = tbox_end.text_frame
    tf_end.word_wrap = True

    pe1 = tf_end.paragraphs[0]
    pe1.text = "InsurMinds Apólice 360"
    pe1.font.size = Pt(40)
    pe1.font.bold = True
    pe1.font.color.rgb = C_CYAN
    pe1.space_after = Pt(12)

    pe2 = tf_end.add_paragraph()
    pe2.text = "A IA Generativa transformando a inteligência e a segurança jurídica nas decisões de gestão corporativa."
    pe2.font.size = Pt(18)
    pe2.font.color.rgb = C_WHITE
    pe2.space_after = Pt(24)

    pe3 = tf_end.add_paragraph()
    pe3.text = "Obrigado! • Projeto Final do Instituto de Inteligência Artificial Aplicada (I2A2)"
    pe3.font.size = Pt(14)
    pe3.font.color.rgb = C_MUTED

    prs.save(output_path)
    print(f"Pitch Deck gerado com sucesso em: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_artifacts = os.path.join(base_dir, "Projeto_Final_Artefatos", "InsurMinds_Projeto_Final.pptx")
    target_root = os.path.join(base_dir, "InsurMinds_Projeto_Final.pptx")
    create_pitch_deck(target_artifacts)
    shutil.copyfile(target_artifacts, target_root)
