import React, { useState, useEffect } from 'react';
import { 
  Shield, Scale, MessageSquare, Cpu, FolderArchive, UploadCloud, 
  CheckCircle2, AlertCircle, Sparkles, ArrowRight, FileText, 
  ExternalLink, Trash2, Eye, RefreshCw, BarChart3, HelpCircle,
  Award, TrendingUp, Check, Layers, PlayCircle, Download
} from 'lucide-react';
import PolicyModal from './components/PolicyModal';

const API_BASE = "http://localhost:8000";

export default function App() {
  const [activeTab, setActiveTab] = useState('policies');
  const [policies, setPolicies] = useState([]);
  const [selectedPolicyIds, setSelectedPolicyIds] = useState([]);
  const [comparisonResult, setComparisonResult] = useState(null);
  const [activeModalPolicy, setActiveModalPolicy] = useState(null);
  
  // Loading & Notifications
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [comparing, setComparing] = useState(false);
  const [notification, setNotification] = useState(null);

  // Chat state
  const [chatMessages, setChatMessages] = useState([
    {
      role: 'assistant',
      content: 'Olá! Sou o **Consultor Securitário Especialista em D&O** da plataforma InsurMinds Apólice 360. Como posso apoiar sua diretoria na análise de coberturas, franquias ou comparação entre apólices?'
    }
  ]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);

  // Filtro de matriz comparativa
  const [matrixFilter, setMatrixFilter] = useState('all'); // 'all', 'gaps', 'basic', 'additional'

  const notify = (msg, type = 'success') => {
    setNotification({ msg, type });
    setTimeout(() => setNotification(null), 4500);
  };

  // Carregar apólices
  const fetchPolicies = async () => {
    try {
      setLoading(true);
      const res = await fetch(`${API_BASE}/api/policies`);
      if (res.ok) {
        const data = await res.json();
        setPolicies(data);
        if (data.length >= 2 && selectedPolicyIds.length === 0) {
          setSelectedPolicyIds([data[0].id, data[1].id]);
        }
      }
    } catch (err) {
      console.error("Erro ao buscar apólices:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  // Upload de arquivo
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setUploading(true);
    try {
      const res = await fetch(`${API_BASE}/api/policies/upload`, {
        method: "POST",
        body: formData
      });
      if (res.ok) {
        const newPolicy = await res.json();
        notify(`Apólice "${newPolicy.insurer_name}" extraída com sucesso!`);
        fetchPolicies();
      } else {
        const errData = await res.json();
        notify(errData.detail || "Erro no processamento da apólice", "error");
      }
    } catch (err) {
      notify("Falha de conexão com a API", "error");
    } finally {
      setUploading(false);
      e.target.value = null;
    }
  };

  // Auto seed das 3 apólices demo
  const handleSeedSamples = async () => {
    setUploading(true);
    try {
      const res = await fetch(`${API_BASE}/api/policies/seed-samples`, { method: "POST" });
      if (res.ok) {
        notify("3 Apólices modelo carregadas e processadas com sucesso!");
        fetchPolicies();
      }
    } catch (err) {
      notify("Erro ao carregar apólices modelo", "error");
    } finally {
      setUploading(false);
    }
  };

  // Excluir apólice
  const handleDeletePolicy = async (policyId, e) => {
    e.stopPropagation();
    if (!window.confirm("Deseja realmente remover esta apólice?")) return;
    try {
      const res = await fetch(`${API_BASE}/api/policies/${policyId}`, { method: "DELETE" });
      if (res.ok) {
        notify("Apólice removida");
        setSelectedPolicyIds(prev => prev.filter(id => id !== policyId));
        fetchPolicies();
      }
    } catch (err) {
      notify("Erro ao excluir", "error");
    }
  };

  // Toggle de seleção para comparador
  const toggleSelectPolicy = (id) => {
    setSelectedPolicyIds(prev => 
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  // Executar Comparação
  const handleCompare = async () => {
    if (selectedPolicyIds.length < 2) {
      notify("Selecione pelo menos 2 apólices para comparar", "warning");
      return;
    }

    setComparing(true);
    try {
      const res = await fetch(`${API_BASE}/api/compare`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ policy_ids: selectedPolicyIds })
      });
      if (res.ok) {
        const result = await res.json();
        setComparisonResult(result);
        notify("Análise comparativa gerada pelos Agentes de IA!");
      } else {
        const err = await res.json();
        notify(err.detail || "Falha na comparação", "error");
      }
    } catch (err) {
      notify("Erro na chamada da API de comparação", "error");
    } finally {
      setComparing(false);
    }
  };

  // Enviar mensagem no Chat
  const handleSendMessage = async (customPrompt = null) => {
    const textToSend = customPrompt || chatInput;
    if (!textToSend.trim() || chatLoading) return;

    const userMsg = { role: 'user', content: textToSend };
    setChatMessages(prev => [...prev, userMsg]);
    if (!customPrompt) setChatInput('');
    setChatLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: textToSend,
          policy_ids: selectedPolicyIds.length > 0 ? selectedPolicyIds : undefined
        })
      });
      if (res.ok) {
        const data = await res.json();
        setChatMessages(prev => [...prev, { role: 'assistant', content: data.answer }]);
      } else {
        setChatMessages(prev => [...prev, { role: 'assistant', content: 'Desculpe, ocorreu uma falha ao consultar as apólices. Tente novamente.' }]);
      }
    } catch (err) {
      setChatMessages(prev => [...prev, { role: 'assistant', content: 'Erro de comunicação com o servidor de IA.' }]);
    } finally {
      setChatLoading(false);
    }
  };

  // Filtragem da matriz
  const filteredMatrix = comparisonResult?.coverage_matrix.filter(row => {
    if (matrixFilter === 'gaps') return row.is_gap;
    if (matrixFilter === 'basic') return row.category === 'Básica';
    if (matrixFilter === 'additional') return row.category === 'Adicional';
    return true;
  }) || [];

  return (
    <div className="app-container">
      {/* Toast Notification */}
      {notification && (
        <div style={{
          position: 'fixed', bottom: '24px', right: '24px', zIndex: 9999,
          background: notification.type === 'error' ? 'var(--accent-rose)' : 'linear-gradient(135deg, #0284c7, #2563eb)',
          color: '#fff', padding: '12px 20px', borderRadius: '12px',
          boxShadow: 'var(--shadow-lg)', fontWeight: '600', fontSize: '14px',
          display: 'flex', alignItems: 'center', gap: '8px'
        }} className="animate-fade-in">
          {notification.type === 'error' ? <AlertCircle size={18} /> : <CheckCircle2 size={18} />}
          {notification.msg}
        </div>
      )}

      {/* Header */}
      <header className="header-glass">
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{
            background: 'linear-gradient(135deg, #0284c7, #38bdf8)',
            padding: '10px', borderRadius: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 0 20px rgba(56, 189, 248, 0.4)'
          }}>
            <Shield size={28} color="#ffffff" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <h1 style={{ fontSize: '20px', fontWeight: '800', letterSpacing: '-0.5px', color: '#fff' }}>
                InsurMinds <span style={{ color: 'var(--accent-cyan)' }}>Apólice 360</span>
              </h1>
              <span className="badge badge-cyan">I2A2 Final Project</span>
            </div>
            <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
              Plataforma Inteligente para Análise, Extração e Comparação de Apólices D&O com IA Generativa
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            display: 'flex', alignItems: 'center', gap: '6px',
            background: 'rgba(16, 185, 129, 0.1)', padding: '6px 14px',
            borderRadius: '999px', border: '1px solid rgba(16, 185, 129, 0.3)'
          }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10b981', display: 'inline-block' }}></span>
            <span style={{ fontSize: '12px', fontWeight: '600', color: '#34d399' }}>API Ativa (FastAPI)</span>
          </div>

          <button 
            className="btn-secondary"
            onClick={fetchPolicies}
            title="Atualizar lista"
          >
            <RefreshCw size={16} />
          </button>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '24px', overflowX: 'auto', paddingBottom: '4px' }}>
        <button 
          className={`nav-tab-btn ${activeTab === 'policies' ? 'active' : ''}`}
          onClick={() => setActiveTab('policies')}
        >
          <Layers size={18} /> Apólices & Ingestão ({policies.length})
        </button>

        <button 
          className={`nav-tab-btn ${activeTab === 'compare' ? 'active' : ''}`}
          onClick={() => {
            setActiveTab('compare');
            if (!comparisonResult && selectedPolicyIds.length >= 2) {
              handleCompare();
            }
          }}
        >
          <Scale size={18} /> Comparador 360º & Matriz de Gaps
        </button>

        <button 
          className={`nav-tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          <MessageSquare size={18} /> Consultor Especialista (Q&A)
        </button>

        <button 
          className={`nav-tab-btn ${activeTab === 'architecture' ? 'active' : ''}`}
          onClick={() => setActiveTab('architecture')}
        >
          <Cpu size={18} /> Arquitetura Multiagente
        </button>

        <button 
          className={`nav-tab-btn ${activeTab === 'artifacts' ? 'active' : ''}`}
          onClick={() => setActiveTab('artifacts')}
        >
          <FolderArchive size={18} /> Entregáveis I2A2 (PDF/PPTX/MP4)
        </button>
      </div>

      {/* TAB 1: POLICIES & INGESTION */}
      {activeTab === 'policies' && (
        <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Top Metrics Row */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px' }}>
            <div className="metric-card">
              <span style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Apólices Sob Custódia</span>
              <span style={{ fontSize: '28px', fontWeight: '800', color: 'var(--text-main)' }}>{policies.length}</span>
              <span style={{ fontSize: '12px', color: 'var(--accent-cyan)' }}>Indexadas para análise comparativa</span>
            </div>

            <div className="metric-card">
              <span style={{ fontSize: '13px', color: 'var(--text-muted)' }}>LMG Total Protegido</span>
              <span style={{ fontSize: '28px', fontWeight: '800', color: '#38bdf8' }}>
                R$ {(policies.reduce((acc, p) => acc + p.lmg_amount, 0) / 1_000_000).toFixed(1)}M
              </span>
              <span style={{ fontSize: '12px', color: 'var(--text-dim)' }}>Volume agregado de indenização</span>
            </div>

            <div className="metric-card">
              <span style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Confiança Média da IA</span>
              <span style={{ fontSize: '28px', fontWeight: '800', color: '#10b981' }}>
                {policies.length > 0 
                  ? `${((policies.reduce((acc, p) => acc + p.extraction_confidence_score, 0) / policies.length) * 100).toFixed(0)}%` 
                  : '0%'}
              </span>
              <span style={{ fontSize: '12px', color: '#34d399' }}>Auditoria regulatória SUSEP 100% OK</span>
            </div>

            <div className="metric-card">
              <span style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Apólices Selecionadas</span>
              <span style={{ fontSize: '28px', fontWeight: '800', color: '#f59e0b' }}>{selectedPolicyIds.length}</span>
              <span style={{ fontSize: '12px', color: 'var(--text-dim)' }}>Prontas para cruzar no Comparador</span>
            </div>
          </div>

          {/* Action Bar (Upload + Seed) */}
          <div style={{
            background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-lg)',
            padding: '24px', display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '16px'
          }}>
            <div>
              <h3 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-main)' }}>Ingestão de Novos Documentos</h3>
              <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Carregue contratos em PDF ou imagens para extração automática via OCR e IA Generativa.</p>
            </div>

            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <label className="btn-primary" style={{ cursor: uploading ? 'wait' : 'pointer' }}>
                <UploadCloud size={18} />
                {uploading ? 'Processando Documento...' : 'Fazer Upload de Apólice'}
                <input 
                  type="file" 
                  accept=".pdf,image/*" 
                  onChange={handleFileUpload} 
                  disabled={uploading} 
                  style={{ display: 'none' }} 
                />
              </label>

              <button 
                className="btn-secondary" 
                onClick={handleSeedSamples}
                disabled={uploading}
                title="Carrega apólices da Porto Seguro, Chubb e Tokio Marine"
              >
                <Sparkles size={18} color="#06b6d4" />
                Carregar 3 Apólices Demo (I2A2)
              </button>
            </div>
          </div>

          {/* Policies Grid */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h3 style={{ fontSize: '18px', fontWeight: '700', color: 'var(--text-main)' }}>
                Apólices Processadas ({policies.length})
              </h3>
              {selectedPolicyIds.length >= 2 && (
                <button 
                  className="btn-primary"
                  onClick={() => {
                    setActiveTab('compare');
                    handleCompare();
                  }}
                  style={{ padding: '8px 16px', fontSize: '13px' }}
                >
                  <Scale size={16} /> Comparar as {selectedPolicyIds.length} Selecionadas
                </button>
              )}
            </div>

            {policies.length === 0 ? (
              <div style={{
                background: 'var(--bg-card)', border: '2px dashed var(--border-subtle)', borderRadius: 'var(--radius-lg)',
                padding: '48px 24px', textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px'
              }}>
                <FileText size={48} color="var(--text-dim)" />
                <p style={{ fontSize: '16px', fontWeight: '600', color: 'var(--text-muted)' }}>
                  Nenhuma apólice cadastrada ainda.
                </p>
                <p style={{ fontSize: '13px', color: 'var(--text-dim)', maxWidth: '400px' }}>
                  Clique no botão abaixo para carregar instantaneamente as 3 apólices D&O de demonstração do mercado segurador brasileiro.
                </p>
                <button className="btn-primary" onClick={handleSeedSamples}>
                  <Sparkles size={18} /> Carregar Apólices de Demonstração
                </button>
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '20px' }}>
                {policies.map(p => {
                  const isSelected = selectedPolicyIds.includes(p.id);
                  return (
                    <div 
                      key={p.id}
                      style={{
                        background: 'var(--bg-card)',
                        border: isSelected ? '2px solid var(--accent-cyan)' : '1px solid var(--border-subtle)',
                        borderRadius: 'var(--radius-md)',
                        padding: '20px',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '14px',
                        boxShadow: isSelected ? 'var(--shadow-glow)' : 'var(--shadow-sm)',
                        transition: 'all 0.2s ease',
                        cursor: 'pointer'
                      }}
                      onClick={() => toggleSelectPolicy(p.id)}
                    >
                      {/* Card Top */}
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                        <div>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <input 
                              type="checkbox" 
                              checked={isSelected} 
                              onChange={() => {}} 
                              style={{ width: '16px', height: '16px', cursor: 'pointer' }}
                            />
                            <h4 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-main)' }}>
                              {p.insurer_name}
                            </h4>
                          </div>
                          <span style={{ fontSize: '12px', color: 'var(--text-muted)', marginLeft: '24px', display: 'block' }}>
                            Nº {p.policy_number}
                          </span>
                        </div>
                        <span className="badge badge-success">{p.validation_status}</span>
                      </div>

                      {/* Card Info Details */}
                      <div style={{ background: 'var(--bg-main)', padding: '12px', borderRadius: '8px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px' }}>
                          <span style={{ color: 'var(--text-muted)' }}>Tomador:</span>
                          <span style={{ fontWeight: '600', color: 'var(--text-main)' }}>{p.policyholder}</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px' }}>
                          <span style={{ color: 'var(--text-muted)' }}>LMG Principal:</span>
                          <span style={{ fontWeight: '700', color: '#38bdf8' }}>
                            R$ {p.lmg_amount.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                          </span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px' }}>
                          <span style={{ color: 'var(--text-muted)' }}>Vigência:</span>
                          <span style={{ color: 'var(--text-main)' }}>{p.start_date} a {p.end_date}</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px' }}>
                          <span style={{ color: 'var(--text-muted)' }}>Retroatividade:</span>
                          <span style={{ color: '#10b981', fontWeight: '600' }}>{p.retroactive_date}</span>
                        </div>
                      </div>

                      {/* Features mini pill row */}
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                        <span className="badge badge-cyan">{p.basic_coverages.length + p.additional_coverages.length} Coberturas</span>
                        <span className="badge badge-warning">{p.key_exclusions.length} Exclusões</span>
                        <span className="badge badge-success">Confiança {(p.extraction_confidence_score * 100).toFixed(0)}%</span>
                      </div>

                      {/* Card Footer Actions */}
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '10px', borderTop: '1px solid var(--border-subtle)' }}>
                        <button 
                          className="btn-secondary" 
                          style={{ padding: '6px 12px', fontSize: '12px' }}
                          onClick={(e) => {
                            e.stopPropagation();
                            setActiveModalPolicy(p);
                          }}
                        >
                          <Eye size={14} /> Raio-X da Apólice
                        </button>

                        <button 
                          style={{ background: 'transparent', border: 'none', color: 'var(--accent-rose)', cursor: 'pointer', padding: '6px' }}
                          onClick={(e) => handleDeletePolicy(p.id, e)}
                          title="Excluir apólice"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 2: COMPARATOR 360 & GAPS */}
      {activeTab === 'compare' && (
        <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Controls Bar */}
          <div style={{
            background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-lg)',
            padding: '20px 24px', display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '16px'
          }}>
            <div>
              <h3 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-main)' }}>
                Comparador Multidimensional D&O
              </h3>
              <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
                Selecione as apólices que deseja confrontar e execute a análise com IA para mapear lacunas e assimetrias de proteção.
              </p>
            </div>

            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <button 
                className="btn-primary" 
                onClick={handleCompare} 
                disabled={comparing || selectedPolicyIds.length < 2}
              >
                <Scale size={18} />
                {comparing ? 'Executando Análise Comparativa...' : `Comparar (${selectedPolicyIds.length} selecionadas)`}
              </button>
            </div>
          </div>

          {/* Quick Selection Checkbox Row */}
          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            {policies.map(p => {
              const isChecked = selectedPolicyIds.includes(p.id);
              return (
                <div 
                  key={p.id}
                  onClick={() => toggleSelectPolicy(p.id)}
                  style={{
                    background: isChecked ? 'rgba(6, 182, 212, 0.15)' : 'var(--bg-subtle)',
                    border: isChecked ? '1px solid var(--accent-cyan)' : '1px solid var(--border-subtle)',
                    padding: '8px 16px', borderRadius: '20px', cursor: 'pointer',
                    display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px',
                    fontWeight: isChecked ? '600' : '500', color: isChecked ? '#fff' : 'var(--text-muted)'
                  }}
                >
                  <input type="checkbox" checked={isChecked} onChange={() => {}} />
                  {p.insurer_name} (R$ {(p.lmg_amount / 1_000_000).toFixed(0)}M)
                </div>
              );
            })}
          </div>

          {comparisonResult && (
            <>
              {/* Executive Verdict Card */}
              <div style={{
                background: 'linear-gradient(135deg, rgba(37, 99, 235, 0.2), rgba(6, 182, 212, 0.15))',
                border: '1px solid rgba(56, 189, 248, 0.4)', borderRadius: 'var(--radius-lg)',
                padding: '24px', boxShadow: 'var(--shadow-glow)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                  <Award size={24} color="#38bdf8" />
                  <h3 style={{ fontSize: '18px', fontWeight: '800', color: '#fff' }}>
                    Parecer Executivo & Veredito Técnico da IA
                  </h3>
                </div>
                <p style={{ fontSize: '15px', color: 'var(--text-main)', lineHeight: '1.7', marginBottom: '16px' }}>
                  {comparisonResult.executive_verdict}
                </p>

                <h4 style={{ fontSize: '14px', fontWeight: '700', color: 'var(--accent-cyan)', marginBottom: '8px' }}>
                  Recomendações Estratégicas para a Tomada de Decisão:
                </h4>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '10px' }}>
                  {comparisonResult.strategic_recommendations.map((rec, idx) => (
                    <div key={idx} style={{
                      background: 'rgba(15, 23, 42, 0.6)', border: '1px solid rgba(255, 255, 255, 0.08)',
                      borderRadius: '8px', padding: '12px', display: 'flex', alignItems: 'flex-start', gap: '10px'
                    }}>
                      <CheckCircle2 size={16} color="#10b981" style={{ flexShrink: 0, marginTop: '2px' }} />
                      <span style={{ fontSize: '13px', color: 'var(--text-main)' }}>{rec}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Scorecards Grid */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
                {Object.values(comparisonResult.scorecards).map(sc => (
                  <div key={sc.policy_id} className="metric-card" style={{ padding: '24px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                      <h4 style={{ fontSize: '17px', fontWeight: '700', color: 'var(--text-main)' }}>{sc.insurer_name}</h4>
                      <div style={{
                        background: 'linear-gradient(135deg, #0284c7, #2563eb)', color: '#fff',
                        padding: '6px 12px', borderRadius: '12px', fontWeight: '800', fontSize: '15px'
                      }}>
                        {sc.protection_score}/100
                      </div>
                    </div>

                    {/* Progress bars */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', margin: '14px 0' }}>
                      <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: 'var(--text-muted)', marginBottom: '4px' }}>
                          <span>Solidez Financeira (LMG)</span>
                          <span style={{ fontWeight: '600', color: '#38bdf8' }}>{sc.financial_adequacy_score}%</span>
                        </div>
                        <div style={{ width: '100%', height: '6px', background: 'var(--bg-main)', borderRadius: '3px', overflow: 'hidden' }}>
                          <div style={{ width: `${sc.financial_adequacy_score}%`, height: '100%', background: '#38bdf8' }}></div>
                        </div>
                      </div>

                      <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: 'var(--text-muted)', marginBottom: '4px' }}>
                          <span>Amplitude de Coberturas</span>
                          <span style={{ fontWeight: '600', color: '#10b981' }}>{sc.coverage_breadth_score}%</span>
                        </div>
                        <div style={{ width: '100%', height: '6px', background: 'var(--bg-main)', borderRadius: '3px', overflow: 'hidden' }}>
                          <div style={{ width: `${sc.coverage_breadth_score}%`, height: '100%', background: '#10b981' }}></div>
                        </div>
                      </div>

                      <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: 'var(--text-muted)', marginBottom: '4px' }}>
                          <span>Acessibilidade a Sinistros (POS)</span>
                          <span style={{ fontWeight: '600', color: '#f59e0b' }}>{sc.claims_accessibility_score}%</span>
                        </div>
                        <div style={{ width: '100%', height: '6px', background: 'var(--bg-main)', borderRadius: '3px', overflow: 'hidden' }}>
                          <div style={{ width: `${sc.claims_accessibility_score}%`, height: '100%', background: '#f59e0b' }}></div>
                        </div>
                      </div>
                    </div>

                    {/* Pros and Cons */}
                    <div style={{ marginTop: '8px' }}>
                      <span style={{ fontSize: '12px', fontWeight: '700', color: '#34d399', textTransform: 'uppercase' }}>Pontos Fortes:</span>
                      <ul style={{ paddingLeft: '16px', fontSize: '12px', color: 'var(--text-main)', marginTop: '4px' }}>
                        {sc.pros.map((p, i) => <li key={i} style={{ marginBottom: '2px' }}>{p}</li>)}
                      </ul>
                      {sc.cons.length > 0 && (
                        <>
                          <span style={{ fontSize: '12px', fontWeight: '700', color: '#fb7185', textTransform: 'uppercase', display: 'block', marginTop: '8px' }}>Atenção / Limitações:</span>
                          <ul style={{ paddingLeft: '16px', fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
                            {sc.cons.map((c, i) => <li key={i} style={{ marginBottom: '2px' }}>{c}</li>)}
                          </ul>
                        </>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {/* Coverage Matrix Table */}
              <div style={{
                background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-lg)',
                padding: '24px', overflowX: 'auto'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
                  <div>
                    <h3 style={{ fontSize: '17px', fontWeight: '700', color: 'var(--text-main)' }}>
                      Matriz Comparativa de Coberturas & Gap Analysis
                    </h3>
                    <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
                      Mapeamento cláusula a cláusula evidenciando diferenciais competitivos e vazios de proteção.
                    </p>
                  </div>

                  {/* Filter buttons */}
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <button 
                      className={`btn-secondary ${matrixFilter === 'all' ? 'active' : ''}`}
                      style={{ padding: '6px 12px', fontSize: '12px' }}
                      onClick={() => setMatrixFilter('all')}
                    >
                      Todas ({comparisonResult.coverage_matrix.length})
                    </button>
                    <button 
                      className={`btn-secondary ${matrixFilter === 'gaps' ? 'active' : ''}`}
                      style={{ padding: '6px 12px', fontSize: '12px', color: '#f59e0b' }}
                      onClick={() => setMatrixFilter('gaps')}
                    >
                      Apenas Gaps ({comparisonResult.coverage_matrix.filter(r => r.is_gap).length})
                    </button>
                    <button 
                      className={`btn-secondary ${matrixFilter === 'basic' ? 'active' : ''}`}
                      style={{ padding: '6px 12px', fontSize: '12px' }}
                      onClick={() => setMatrixFilter('basic')}
                    >
                      Básicas
                    </button>
                    <button 
                      className={`btn-secondary ${matrixFilter === 'additional' ? 'active' : ''}`}
                      style={{ padding: '6px 12px', fontSize: '12px' }}
                      onClick={() => setMatrixFilter('additional')}
                    >
                      Adicionais
                    </button>
                  </div>
                </div>

                <table className="custom-table">
                  <thead>
                    <tr>
                      <th style={{ minWidth: '220px' }}>Cobertura</th>
                      <th style={{ width: '120px' }}>Categoria</th>
                      {comparisonResult.policies_meta.map(m => (
                        <th key={m.id} style={{ minWidth: '180px' }}>{m.insurer_name}</th>
                      ))}
                      <th style={{ minWidth: '160px' }}>Diagnóstico</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredMatrix.map((row, idx) => (
                      <tr key={idx} style={{ background: row.is_gap ? 'rgba(245, 158, 11, 0.04)' : 'transparent' }}>
                        <td style={{ fontWeight: '600', color: 'var(--text-main)' }}>{row.coverage_name}</td>
                        <td>
                          <span className={`badge ${row.category === 'Básica' ? 'badge-cyan' : 'badge-success'}`}>
                            {row.category}
                          </span>
                        </td>
                        {comparisonResult.policies_meta.map(m => {
                          const val = row.policy_values[m.id] || "Não Informado";
                          const isMissing = val.includes("Não Contemplado") || val.includes("Excluído");
                          return (
                            <td key={m.id}>
                              <span style={{
                                color: isMissing ? '#fb7185' : '#34d399',
                                fontWeight: isMissing ? '400' : '600',
                                fontSize: '13px'
                              }}>
                                {isMissing ? '✕ Não Coberto' : `✓ ${val}`}
                              </span>
                            </td>
                          );
                        })}
                        <td>
                          {row.is_gap ? (
                            <span className="badge badge-warning">Gap Detectado</span>
                          ) : (
                            <span className="badge badge-success">Uniforme</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}
        </div>
      )}

      {/* TAB 3: CONSULTANT CHAT (Q&A) */}
      {activeTab === 'chat' && (
        <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div style={{
            background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-lg)',
            padding: '20px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center'
          }}>
            <div>
              <h3 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-main)' }}>
                Consultor de Inteligência Securitária D&O
              </h3>
              <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
                Tire dúvidas técnicas, analise riscos de litígios e solicite pareceres com citação das cláusulas contratuais.
              </p>
            </div>
            <span className="badge badge-cyan">{policies.length} Apólices Ativas no Contexto</span>
          </div>

          {/* Quick Prompts */}
          <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '4px' }}>
            {[
              "Qual apólice cobre custos de defesa criminal?",
              "Qual é a franquia para ações na CVM ou valores mobiliários?",
              "Como funciona a cobertura de penhora online para os executivos?",
              "Quais são as exclusões de dolo ou atos ilícitos em cada contrato?",
              "Qual das apólices tem o melhor custo-benefício para a diretoria?"
            ].map((prompt, idx) => (
              <button 
                key={idx}
                className="btn-secondary"
                style={{ fontSize: '12px', padding: '6px 12px', whiteSpace: 'nowrap' }}
                onClick={() => handleSendMessage(prompt)}
              >
                <HelpCircle size={14} color="#06b6d4" /> {prompt}
              </button>
            ))}
          </div>

          {/* Chat Messages Log */}
          <div style={{
            background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-lg)',
            padding: '24px', minHeight: '420px', maxHeight: '550px', overflowY: 'auto',
            display: 'flex', flexDirection: 'column', gap: '16px'
          }}>
            {chatMessages.map((msg, idx) => (
              <div 
                key={idx}
                style={{
                  alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                  maxWidth: '80%',
                  background: msg.role === 'user' ? 'linear-gradient(135deg, #0284c7, #2563eb)' : 'var(--bg-subtle)',
                  color: '#fff',
                  padding: '14px 18px',
                  borderRadius: '16px',
                  borderBottomRightRadius: msg.role === 'user' ? '4px' : '16px',
                  borderBottomLeftRadius: msg.role === 'assistant' ? '4px' : '16px',
                  boxShadow: var_shadow(msg.role),
                  fontSize: '14px',
                  lineHeight: '1.6'
                }}
              >
                <div style={{ fontSize: '11px', opacity: 0.7, marginBottom: '4px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                  {msg.role === 'user' ? 'Sua Consulta' : 'InsurMinds Securitário IA'}
                </div>
                <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
              </div>
            ))}
            {chatLoading && (
              <div style={{ alignSelf: 'flex-start', background: 'var(--bg-subtle)', padding: '12px 18px', borderRadius: '16px', color: 'var(--text-muted)', fontSize: '13px' }}>
                Consultando apólices e regulamentação SUSEP...
              </div>
            )}
          </div>

          {/* Chat Input Bar */}
          <div style={{ display: 'flex', gap: '12px' }}>
            <input 
              type="text" 
              placeholder="Digite sua dúvida sobre as apólices D&O (ex: Existe franquia para bloqueio de bens?)..."
              value={chatInput}
              onChange={e => setChatInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSendMessage()}
              style={{
                flex: 1, background: 'var(--bg-card)', border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)', padding: '14px 18px', color: '#fff',
                fontSize: '14px', outline: 'none'
              }}
            />
            <button 
              className="btn-primary" 
              onClick={() => handleSendMessage()}
              disabled={chatLoading}
              style={{ padding: '0 24px' }}
            >
              Enviar Pergunta
            </button>
          </div>
        </div>
      )}

      {/* TAB 4: MULTIAGENT ARCHITECTURE */}
      {activeTab === 'architecture' && (
        <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div style={{
            background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-lg)',
            padding: '24px'
          }}>
            <h3 style={{ fontSize: '18px', fontWeight: '800', color: 'var(--text-main)', marginBottom: '8px' }}>
              Arquitetura Sistêmica do InsurMinds Apólice 360
            </h3>
            <p style={{ fontSize: '14px', color: 'var(--text-muted)', lineHeight: '1.6', marginBottom: '20px' }}>
              A plataforma foi estruturada seguindo rigorosamente os preceitos de modularidade e separação de responsabilidades 
              recomendados pelo <b>Instituto de Inteligência Artificial Aplicada (I2A2)</b>, integrando 5 agentes de IA autônomos.
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
              <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-subtle)', borderRadius: '12px', padding: '18px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                  <div style={{ background: 'rgba(56, 189, 248, 0.1)', padding: '8px', borderRadius: '8px' }}>
                    <UploadCloud size={20} color="#38bdf8" />
                  </div>
                  <h4 style={{ fontSize: '15px', fontWeight: '700', color: 'var(--text-main)' }}>1. Ingestion & OCR Agent</h4>
                </div>
                <p style={{ fontSize: '13px', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                  Recepciona PDFs e imagens. Executa PyMuPDF para parsing estrutural nativo ou OCR (Tesseract / Vision) em documentos escaneados com preservação de paginação.
                </p>
              </div>

              <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-subtle)', borderRadius: '12px', padding: '18px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                  <div style={{ background: 'rgba(16, 185, 129, 0.1)', padding: '8px', borderRadius: '8px' }}>
                    <Cpu size={20} color="#10b981" />
                  </div>
                  <h4 style={{ fontSize: '15px', fontWeight: '700', color: 'var(--text-main)' }}>2. Extraction Agent</h4>
                </div>
                <p style={{ fontSize: '13px', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                  Especialista de domínio D&O. Mapeia LMG, Sublimites, Franquias (POS), Coberturas Básicas, Extensões e Exclusões Críticas com validação de esquema Pydantic.
                </p>
              </div>

              <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-subtle)', borderRadius: '12px', padding: '18px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                  <div style={{ background: 'rgba(245, 158, 11, 0.1)', padding: '8px', borderRadius: '8px' }}>
                    <Shield size={20} color="#f59e0b" />
                  </div>
                  <h4 style={{ fontSize: '15px', fontWeight: '700', color: 'var(--text-main)' }}>3. Validation Agent</h4>
                </div>
                <p style={{ fontSize: '13px', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                  Audita conformidade securitária (Circular SUSEP 553/2017). Valida coerência de datas, consistência de sublimites e calcula o índice de confiança.
                </p>
              </div>

              <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-subtle)', borderRadius: '12px', padding: '18px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                  <div style={{ background: 'rgba(139, 92, 246, 0.1)', padding: '8px', borderRadius: '8px' }}>
                    <Scale size={20} color="#8b5cf6" />
                  </div>
                  <h4 style={{ fontSize: '15px', fontWeight: '700', color: 'var(--text-main)' }}>4. Comparison Agent</h4>
                </div>
                <p style={{ fontSize: '13px', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                  Confronta 2 ou mais apólices, computa scorecards de proteção, detecta assimetrias contratuais, lacunas (gaps) e formula veredito executivo estratégico.
                </p>
              </div>

              <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-subtle)', borderRadius: '12px', padding: '18px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                  <div style={{ background: 'rgba(244, 63, 94, 0.1)', padding: '8px', borderRadius: '8px' }}>
                    <MessageSquare size={20} color="#f43f5e" />
                  </div>
                  <h4 style={{ fontSize: '15px', fontWeight: '700', color: 'var(--text-main)' }}>5. Q&A Consultant Agent</h4>
                </div>
                <p style={{ fontSize: '13px', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                  Assistente conversacional que responde a questionamentos pontuais com citação precisa de cláusulas, páginas e amparo regulatório.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 5: DELIVERABLES (PDF/PPTX/MP4) */}
      {activeTab === 'artifacts' && (
        <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div style={{
            background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-lg)',
            padding: '24px'
          }}>
            <h3 style={{ fontSize: '18px', fontWeight: '800', color: 'var(--text-main)', marginBottom: '8px' }}>
              Central de Entregáveis Oficiais (I2A2)
            </h3>
            <p style={{ fontSize: '14px', color: 'var(--text-muted)', marginBottom: '24px' }}>
              Todos os artefatos formais exigidos na especificação do projeto depositados na pasta padronizada <code>Projeto_Final_Artefatos/</code>.
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
              {/* Deliverable 1: Relatório Técnico */}
              <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-subtle)', borderRadius: '12px', padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                    <FileText size={24} color="#38bdf8" />
                    <h4 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-main)' }}>Relatório Técnico (PDF)</h4>
                  </div>
                  <p style={{ fontSize: '13px', color: 'var(--text-muted)', lineHeight: '1.5', marginBottom: '14px' }}>
                    Documento formal abrangendo arquitetura da solução, tecnologias, agentes, fluxo de processamento, justificativas arquiteturais, limitações e roadmap.
                  </p>
                  <span style={{ fontSize: '12px', color: 'var(--accent-cyan)', fontFamily: 'monospace' }}>
                    InsurMinds_Relatorio_Tecnico.pdf
                  </span>
                </div>
                <div style={{ marginTop: '16px' }}>
                  <a href={`${API_BASE}/artefatos/InsurMinds_Relatorio_Tecnico.pdf`} target="_blank" rel="noreferrer" className="btn-secondary" style={{ width: '100%', justifyContent: 'center' }}>
                    <Download size={16} /> Baixar Relatório Técnico
                  </a>
                </div>
              </div>

              {/* Deliverable 2: Pitch Deck PPTX */}
              <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-subtle)', borderRadius: '12px', padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                    <BarChart3 size={24} color="#f59e0b" />
                    <h4 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-main)' }}>Pitch Deck Executivo (PPTX)</h4>
                  </div>
                  <p style={{ fontSize: '13px', color: 'var(--text-muted)', lineHeight: '1.5', marginBottom: '14px' }}>
                    Apresentação corporativa formatada conforme as diretrizes do Sebrae para pitch decks, cobrindo problema, solução, mercado D&O e diferenciais de IA.
                  </p>
                  <span style={{ fontSize: '12px', color: '#f59e0b', fontFamily: 'monospace' }}>
                    InsurMinds_Projeto_Final.pptx
                  </span>
                </div>
                <div style={{ marginTop: '16px' }}>
                  <a href={`${API_BASE}/artefatos/InsurMinds_Projeto_Final.pptx`} target="_blank" rel="noreferrer" className="btn-secondary" style={{ width: '100%', justifyContent: 'center' }}>
                    <Download size={16} /> Baixar Apresentação PPTX
                  </a>
                </div>
              </div>

              {/* Deliverable 3: Vídeo Demonstrativo */}
              <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-subtle)', borderRadius: '12px', padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                    <PlayCircle size={24} color="#10b981" />
                    <h4 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-main)' }}>Vídeo de Demonstração (MP4)</h4>
                  </div>
                  <p style={{ fontSize: '13px', color: 'var(--text-muted)', lineHeight: '1.5', marginBottom: '14px' }}>
                    Demonstração audiovisual com duração máxima de 5 minutos, apresentando o problema, arquitetura, execução da plataforma e principais resultados.
                  </p>
                  <span style={{ fontSize: '12px', color: '#10b981', fontFamily: 'monospace' }}>
                    InsurMinds_Projeto_Final.mp4
                  </span>
                </div>
                <div style={{ marginTop: '16px' }}>
                  <a href={`${API_BASE}/artefatos/InsurMinds_Projeto_Final.mp4`} target="_blank" rel="noreferrer" className="btn-secondary" style={{ width: '100%', justifyContent: 'center' }}>
                    <PlayCircle size={16} /> Acessar Arquivo de Vídeo
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Policy Modal */}
      {activeModalPolicy && (
        <PolicyModal 
          policy={activeModalPolicy} 
          onClose={() => setActiveModalPolicy(null)} 
        />
      )}
    </div>
  );
}

function var_shadow(role) {
  return role === 'user' ? '0 4px 12px rgba(2, 132, 199, 0.3)' : '0 2px 8px rgba(0, 0, 0, 0.3)';
}
