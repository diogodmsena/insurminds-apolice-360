# Roteiro Oficial do Vídeo de Apresentação (Pitch & Demonstração)
## InsurMinds Apólice 360 - Plataforma Inteligente para Análise e Comparação de Apólices D&O
**Duração Total Máxima:** 4 minutos e 45 segundos  
**Arquivo Gerado:** `InsurMinds_Projeto_Final.mp4`  
**Conformidade:** Requisitos da Página 22 do Edital I2A2  

---

### Minutagem e Divisão de Blocos

#### Bloco 1: Abertura e O Problema Abordado (0:00 – 1:00)
- **Visual em Tela:** Apresentação da marca InsurMinds e exibição de apólices reais densas (40 a 80 páginas).
- **Locução:**
  > *"Olá a todos e bem-vindos à apresentação do projeto InsurMinds Apólice 360, desenvolvido para o Projeto Final do Instituto de Inteligência Artificial Aplicada (I2A2). No mundo corporativo moderno, apólices de seguro D&O (Directors and Officers) são essenciais para resguardar o patrimônio pessoal de administradores e conselheiros. Contudo, essas apólices são redigidas em linguagem jurídica intrincada, com centenas de cláusulas de exclusão, sublimites e franquias complexas. Comparar duas ou três cotações exige horas intermináveis de trabalho manual de corretores sêniores e advogados, gerando vulnerabilidades a lacunas de cobertura (gaps) que só são descobertas no momento do sinistro. Para solucionar essa dor crítica, criamos o InsurMinds Apólice 360."*

#### Bloco 2: A Arquitetura da Solução (1:00 – 2:00)
- **Visual em Tela:** Diagrama arquitetural dos 5 agentes em camadas e stack tecnológica (FastAPI, PyMuPDF, Pydantic, LLM Gemini/OpenAI, SQLite, React).
- **Locução:**
  > *"Seguindo as melhores práticas do I2A2, adotamos uma arquitetura de múltiplos agentes especializados com clara separação de responsabilidades. O IngestionAgent faz a leitura e OCR de arquivos PDF ou escaneados; o ExtractionAgent atua como perito atuário, extraindo LMG, sublimites, franquias POS e exclusões via esquemas Pydantic; o ValidationAgent audita a conformidade regulatória segundo a Circular SUSEP 553; o ComparisonAgent cruza as apólices gerando matriz de gaps e scorecards de proteção de 0 a 100; e o QnAAgent responde perguntas de negócio com citação de cláusulas. Tudo apoiado por um motor híbrido com fallback offline resiliente."*

#### Bloco 3: O Funcionamento da Aplicação (2:00 – 3:30)
- **Visual em Tela:** Demonstração da interface web React conectada ao backend FastAPI.
- **Ações:**
  1. *Dashboard e Ingestão:* Exibição das apólices cadastradas (Porto Seguro, Chubb e Tokio Marine). Demonstração do upload drag-and-drop e abertura do modal "Raio-X da Apólice" com detalhes de LMG e franquias.
  2. *Comparador 360:* Seleção das apólices e acionamento do botão "Comparar". Exibição da Matriz de Gaps, Radar de Proteção e Veredito Executivo com recomendações estratégicas para o Conselho de Administração.
  3. *Chat Consultivo Q&A:* Digitação de perguntas como 'Qual apólice protege melhor contra penhora online?' e exibição da resposta fundamentada citando as cláusulas contratuais.
- **Locução:**
  > *"Aqui na aplicação vemos o dashboard executivo. Com apenas um clique, o usuário visualiza o Raio-X completo da apólice, auditado pela IA. Ao selecionar apólices concorrentes e acionar o comparador, o sistema cruza todas as cláusulas em segundos, identificando diferenciais cruciais — como sublimites de penhora online e investigações da CVM. Na aba de consultoria, o executivo pode fazer qualquer pergunta em linguagem natural e receber respostas fundamentadas com indicação expressa da página e do artigo da apólice."*

#### Bloco 4: Principais Resultados Obtidos e Conclusão (3:30 – 4:45)
- **Visual em Tela:** Gráficos de eficiência, tabela comparativa de redução de tempo e encerramento.
- **Locução:**
  > *"Como principais resultados, alcançamos: (1) Redução de mais de 95% no tempo de análise contratual, passando de 20 horas de estudo manual para menos de 60 segundos; (2) Detecção preventiva de riscos patrimoniais ocultos; e (3) Uma arquitetura robusta, 100% testada e de código aberto sob licença MIT. O InsurMinds Apólice 360 comprova o imenso potencial da Inteligência Artificial Generativa para transformar a governança e a segurança jurídica corporativa. Muito obrigado!"*
