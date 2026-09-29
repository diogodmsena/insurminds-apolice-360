import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_sample_policy(filename, title, insurer, policy_num, tomador, lmg, sublimits, deductibles, coverages, exclusions, extra_notes=""):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    # Custom styles
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0F2942"),
        spaceAfter=6
    )
    
    subheader_style = ParagraphStyle(
        'SubHeaderStyle',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1A5F7A"),
        spaceBefore=10,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2C3E50")
    )

    story = []

    # Cabeçalho da Apólice
    story.append(Paragraph(f"<b>{insurer}</b>", header_style))
    story.append(Paragraph(f"<b>CONTRATO DE SEGURO DE RESPONSABILIDADE CIVIL D&O</b>", subheader_style))
    story.append(Paragraph(f"Apólice / Especificação de Coberturas nº <b>{policy_num}</b>", body_style))
    story.append(Spacer(1, 10))

    # Tabela de Dados Gerais
    general_data = [
        [Paragraph("<b>Tomador (Estipulante):</b>", body_style), Paragraph(tomador, body_style)],
        [Paragraph("<b>Segurados:</b>", body_style), Paragraph("Diretores Estatutários, Conselheiros de Administração e Fiscais", body_style)],
        [Paragraph("<b>Período de Vigência:</b>", body_style), Paragraph("01/01/2026 às 24h00 a 01/01/2027 às 24h00", body_style)],
        [Paragraph("<b>Limite Máximo de Garantia (LMG):</b>", body_style), Paragraph(f"<b>{lmg}</b>", body_style)],
        [Paragraph("<b>Data de Retroatividade:</b>", body_style), Paragraph("Ilimitada", body_style)],
        [Paragraph("<b>Âmbito Geográfico e Jurisdição:</b>", body_style), Paragraph("Brasil e Extensões Contratadas", body_style)],
    ]
    t_gen = Table(general_data, colWidths=[2.2*inch, 4.8*inch])
    t_gen.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F4F7F9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D7DE")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_gen)
    story.append(Spacer(1, 12))

    # Coberturas Contratadas
    story.append(Paragraph("<b>1. QUADRO RESUMO DE COBERTURAS</b>", subheader_style))
    cov_rows = [[Paragraph("<b>Cobertura / Extensão</b>", body_style), Paragraph("<b>Limite / Condição</b>", body_style), Paragraph("<b>Cláusula Ref.</b>", body_style)]]
    for c in coverages:
        cov_rows.append([Paragraph(c[0], body_style), Paragraph(c[1], body_style), Paragraph(c[2], body_style)])
    
    t_cov = Table(cov_rows, colWidths=[3.2*inch, 2.4*inch, 1.4*inch])
    t_cov.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_cov)
    story.append(Spacer(1, 12))

    # Franquias / POS
    story.append(Paragraph("<b>2. PARTICIPAÇÃO OBRIGATÓRIA DO SEGURADO (POS / FRANQUIA)</b>", subheader_style))
    pos_rows = [[Paragraph("<b>Tipo de Reclamação</b>", body_style), Paragraph("<b>Valor da Franquia</b>", body_style)]]
    for d in deductibles:
        pos_rows.append([Paragraph(d[0], body_style), Paragraph(d[1], body_style)])
    t_pos = Table(pos_rows, colWidths=[4.2*inch, 2.8*inch])
    t_pos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_pos)
    story.append(Spacer(1, 12))

    # Exclusões
    story.append(Paragraph("<b>3. CLÁUSULAS DE EXCLUSÕES PRINCIPAIS</b>", subheader_style))
    for e in exclusions:
        story.append(Paragraph(f"• <b>{e[0]}:</b> {e[1]} <i>({e[2]})</i>", body_style))
        story.append(Spacer(1, 3))

    if extra_notes:
        story.append(Spacer(1, 10))
        story.append(Paragraph("<b>4. DISPOSIÇÕES ESPECÍFICAS</b>", subheader_style))
        story.append(Paragraph(extra_notes, body_style))

    doc.build(story)
    print(f"Gerado: {filename}")

def generate_all_samples():
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "samples")
    
    # 1. Apólice Alpha (Porto Seguro D&O Standard)
    create_sample_policy(
        filename=os.path.join(base_dir, "apolice_alpha_dno_standard.pdf"),
        title="Apólice D&O Standard Essencial",
        insurer="Porto Seguro Seguros S.A.",
        policy_num="DO-2026-BR-001092",
        tomador="Vanguarda Alimentos & Bebidas S.A.",
        lmg="R$ 10.000.000,00 (Dez Milhões de Reais)",
        sublimits=[
            ("Penhora Online", "R$ 2.500.000,00"),
            ("Gestão de Crise", "R$ 1.000.000,00")
        ],
        deductibles=[
            ("Reclamações contra Segurados Pessoas Físicas", "Isento (R$ 0,00)"),
            ("Reclamações Corporativas envolvendo o Tomador", "R$ 100.000,00")
        ],
        coverages=[
            ("Custos de Defesa Judicial e Arbitral", "Até 100% do LMG (R$ 10M)", "Cláusula 3.1"),
            ("Indenizações e Reparações Cíveis Decorrentes de Acordo", "Até 100% do LMG (R$ 10M)", "Cláusula 3.2"),
            ("Penhora Online e Bloqueio de Ativos Pessoais", "Sublimite R$ 2.500.000,00", "Extensão 4.1"),
            ("Gestão de Imagem e Relações Públicas", "Sublimite R$ 1.000.000,00", "Extensão 4.2"),
            ("Responsabilidade Tributária e Trabalhista Solidária", "Até 100% do LMG", "Extensão 4.3")
        ],
        exclusions=[
            ("Atos Dolosos e Condutas Fraudulentas", "Exclusão aplicável unicamente após sentença judicial condenatória transitada em julgado.", "Cláusula 7.1"),
            ("Vantagem Pessoal Ilegítima", "Reclamações oriundas de remuneração ou ganho pecuniário auferido sem base contratual ou legal.", "Cláusula 7.2"),
            ("Danos Físicos e Corporais Diretos", "Danos causados a terceiros cobertos tipicamente por apólices de Responsabilidade Civil Geral.", "Cláusula 7.3")
        ],
        extra_notes="Prazo complementar de reclamação de 36 meses concedido sem custo adicional em caso de não renovação."
    )

    # 2. Apólice Beta (Chubb D&O Corporate Plus)
    create_sample_policy(
        filename=os.path.join(base_dir, "apolice_beta_dno_corporate.pdf"),
        title="Apólice D&O Corporate Plus",
        insurer="Chubb Seguros Brasil S.A.",
        policy_num="CHUBB-DNO-2026-8841",
        tomador="Vanguarda Alimentos & Bebidas S.A.",
        lmg="R$ 25.000.000,00 (Vinte e Cinco Milhões de Reais)",
        sublimits=[
            ("Investigações Oficiais CVM/CADE", "R$ 7.500.000,00"),
            ("Penhora Online e Bloqueio Bancário", "R$ 6.250.000,00"),
            ("Gestão de Crise Corporativa", "R$ 2.000.000,00"),
            ("Despesas de Extradição e Fiança", "R$ 1.000.000,00")
        ],
        deductibles=[
            ("Segurados Pessoas Físicas (Brasil)", "Isento (R$ 0,00)"),
            ("Reclamações de Valores Mobiliários (CVM / Ações Coletivas)", "R$ 250.000,00"),
            ("Ações Fora do Território Nacional", "US$ 50.000,00")
        ],
        coverages=[
            ("Custos de Defesa Cível, Trabalhista e Criminal", "Até 100% do LMG (R$ 25M)", "Cláusula 3.1"),
            ("Custos de Resposta a Investigações Oficiais CVM / CADE", "Sublimite R$ 7.500.000,00", "Extensão 5.1"),
            ("Penhora Online e Bloqueio de Ativos Pessoais", "Sublimite R$ 6.250.000,00", "Extensão 5.2"),
            ("Gestão de Crise e Preservação de Reputação", "Sublimite R$ 2.000.000,00", "Extensão 5.3"),
            ("Despesas de Extradição, Fiança e Desacato Involuntário", "Sublimite R$ 1.000.000,00", "Extensão 5.4"),
            ("Responsabilidade por Danos Ambientais (Custos de Defesa)", "Sublimite R$ 5.000.000,00", "Extensão 5.5")
        ],
        exclusions=[
            ("Atos Dolosos ou Má-fé Comprovada", "Válido apenas quando confirmado por julgamento definitivo final sem possibilidade de recurso.", "Cláusula 8.1"),
            ("Benefício Econômico Ilícito", "Retenção indevida de fundos corporativos ou propina.", "Cláusula 8.2"),
            ("Poluição Gradual Contínua", "Danos ecológicos acumulados ao longo do tempo (coberto apenas incidente súbito).", "Cláusula 8.3")
        ],
        extra_notes="Extensão automática de cobertura para novos administradores nomeados ao longo do exercício fiscal."
    )

    # 3. Apólice Gamma (Tokio Marine D&O Global Premium)
    create_sample_policy(
        filename=os.path.join(base_dir, "apolice_gamma_dno_premium.pdf"),
        title="Apólice D&O Global Elite",
        insurer="Tokio Marine Seguradora S.A.",
        policy_num="TM-CORP-DNO-99214",
        tomador="Vanguarda Alimentos & Bebidas S.A.",
        lmg="R$ 50.000.000,00 (Cinquenta Milhões de Reais)",
        sublimits=[
            ("Investigações Oficiais CVM/CADE/SEC", "R$ 15.000.000,00"),
            ("Penhora Online e Depósitos de Garantia", "Até 100% do LMG"),
            ("Práticas Trabalhistas Indevidas (EPL)", "R$ 10.000.000,00"),
            ("Poluição Súbita e Acidental", "R$ 10.000.000,00")
        ],
        deductibles=[
            ("Segurados Pessoas Físicas", "Isento (R$ 0,00)"),
            ("Reclamações Globais / SEC / NYSE", "US$ 100.000,00")
        ],
        coverages=[
            ("Custos de Defesa Plenos (Sem Dedução de Honorários)", "Até 100% do LMG (R$ 50M)", "Cláusula 3.1"),
            ("Investigações Formais e Pré-Processuais (CVM, CADE, SEC)", "Sublimite R$ 15.000.000,00", "Extensão 5.1"),
            ("Penhora Online e Indisponibilidade de Bens", "Até 100% do LMG", "Extensão 5.2"),
            ("Práticas Trabalhistas Indevidas (Assédio / Discriminação)", "Sublimite R$ 10.000.000,00", "Extensão 5.3"),
            ("Gestão de Crise de Alta Repercussão", "Sublimite R$ 5.000.000,00", "Extensão 5.4"),
            ("Responsabilidade Ambiental e Custos de Remediação Emergencial", "Sublimite R$ 10.000.000,00", "Extensão 5.5")
        ],
        exclusions=[
            ("Dolo Reconhecido em Sentença Definitiva", "Não há direito a repetição de custos pagos antes da sentença transitada.", "Cláusula 9.1"),
            ("Ganhos Pessoais Ilegais", "Exclusão de enriquecimento sem causa comprovado.", "Cláusula 9.2")
        ],
        extra_notes="Âmbito de cobertura mundial com jurisdição válida no Brasil, União Europeia e Estados Unidos da América."
    )

if __name__ == "__main__":
    generate_all_samples()
