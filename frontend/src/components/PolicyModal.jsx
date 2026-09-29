import React from 'react';
import { X, Shield, FileText, AlertTriangle, CheckCircle, DollarSign, Calendar, Globe, Award } from 'lucide-react';

export default function PolicyModal({ policy, onClose }) {
  if (!policy) return null;

  return (
    <div className="modal-overlay animate-fade-in" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div style={{ padding: '20px 24px', borderBottom: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ background: 'rgba(6, 182, 212, 0.1)', padding: '10px', borderRadius: '12px', border: '1px solid rgba(6, 182, 212, 0.3)' }}>
              <Shield size={24} color="#06b6d4" />
            </div>
            <div>
              <h2 style={{ fontSize: '18px', fontWeight: '700', color: 'var(--text-main)' }}>{policy.insurer_name}</h2>
              <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Apólice nº {policy.policy_number} • {policy.policyholder}</p>
            </div>
          </div>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', padding: '6px' }}>
            <X size={20} />
          </button>
        </div>

        {/* Body */}
        <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Executive Summary */}
          <div style={{ background: 'var(--bg-subtle)', padding: '16px', borderRadius: '12px', borderLeft: '4px solid var(--accent-cyan)' }}>
            <h4 style={{ fontSize: '14px', fontWeight: '600', color: 'var(--accent-cyan)', marginBottom: '6px' }}>Síntese Técnica Executiva</h4>
            <p style={{ fontSize: '14px', color: 'var(--text-main)', lineHeight: '1.6' }}>{policy.executive_summary}</p>
          </div>

          {/* Quick Metrics Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px' }}>
            <div style={{ background: 'var(--bg-main)', padding: '14px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
              <span style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <DollarSign size={14} color="#38bdf8" /> LMG Global
              </span>
              <p style={{ fontSize: '18px', fontWeight: '700', color: '#38bdf8', marginTop: '4px' }}>
                R$ {policy.lmg_amount.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
              </p>
            </div>

            <div style={{ background: 'var(--bg-main)', padding: '14px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
              <span style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Calendar size={14} color="#10b981" /> Vigência
              </span>
              <p style={{ fontSize: '14px', fontWeight: '600', color: 'var(--text-main)', marginTop: '4px' }}>
                {policy.start_date} a {policy.end_date}
              </p>
            </div>

            <div style={{ background: 'var(--bg-main)', padding: '14px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
              <span style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Globe size={14} color="#8b5cf6" /> Âmbito e Retroatividade
              </span>
              <p style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-main)', marginTop: '4px' }}>
                {policy.territorial_scope} | Retro: {policy.retroactive_date}
              </p>
            </div>

            <div style={{ background: 'var(--bg-main)', padding: '14px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
              <span style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Award size={14} color="#f59e0b" /> Confiança Extração IA
              </span>
              <p style={{ fontSize: '16px', fontWeight: '700', color: '#10b981', marginTop: '4px' }}>
                {(policy.extraction_confidence_score * 100).toFixed(0)}% ({policy.validation_status})
              </p>
            </div>
          </div>

          {/* Sublimites */}
          {policy.sublimits && policy.sublimits.length > 0 && (
            <div>
              <h3 style={{ fontSize: '15px', fontWeight: '700', marginBottom: '10px', color: 'var(--text-main)' }}>Sublimites Específicos de Garantia</h3>
              <table className="custom-table" style={{ borderRadius: '8px', overflow: 'hidden' }}>
                <thead>
                  <tr>
                    <th>Sublimite</th>
                    <th>Valor</th>
                    <th>Condição</th>
                  </tr>
                </thead>
                <tbody>
                  {policy.sublimits.map((s, idx) => (
                    <tr key={idx}>
                      <td style={{ fontWeight: '500' }}>{s.name}</td>
                      <td style={{ color: 'var(--accent-sky)', fontWeight: '600' }}>R$ {s.amount.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</td>
                      <td style={{ color: 'var(--text-muted)' }}>{s.details || '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Franquias / POS */}
          {policy.deductibles_pos && policy.deductibles_pos.length > 0 && (
            <div>
              <h3 style={{ fontSize: '15px', fontWeight: '700', marginBottom: '10px', color: 'var(--text-main)' }}>Participação Obrigatória do Segurado (POS / Franquias)</h3>
              <table className="custom-table" style={{ borderRadius: '8px', overflow: 'hidden' }}>
                <thead>
                  <tr>
                    <th>Categoria</th>
                    <th>Valor</th>
                    <th>Aplicação</th>
                  </tr>
                </thead>
                <tbody>
                  {policy.deductibles_pos.map((d, idx) => (
                    <tr key={idx}>
                      <td style={{ fontWeight: '500' }}>{d.category}</td>
                      <td style={{ color: d.amount === 0 ? '#10b981' : '#f59e0b', fontWeight: '700' }}>
                        {d.amount === 0 ? 'Isento (R$ 0,00)' : `R$ ${d.amount.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
                      </td>
                      <td style={{ color: 'var(--text-muted)' }}>{d.description || '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Coberturas Básicas e Adicionais */}
          <div>
            <h3 style={{ fontSize: '15px', fontWeight: '700', marginBottom: '10px', color: 'var(--text-main)' }}>Coberturas Detalhadas</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '12px' }}>
              {policy.basic_coverages.concat(policy.additional_coverages).map((c, idx) => (
                <div key={idx} style={{ background: 'var(--bg-main)', border: '1px solid var(--border-subtle)', borderRadius: '8px', padding: '12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                    <span style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-main)' }}>{c.title}</span>
                    <span className="badge badge-success">{c.status}</span>
                  </div>
                  <p style={{ fontSize: '12px', color: 'var(--text-muted)', lineHeight: '1.4' }}>{c.description}</p>
                  {c.clause_reference && (
                    <span style={{ fontSize: '11px', color: 'var(--accent-cyan)', marginTop: '6px', display: 'inline-block' }}>
                      Ref: {c.clause_reference} {c.page_number ? `(Pág. ${c.page_number})` : ''}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Exclusões */}
          <div>
            <h3 style={{ fontSize: '15px', fontWeight: '700', marginBottom: '10px', color: 'var(--text-main)' }}>Exclusões Relevantes Analisadas</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {policy.key_exclusions.map((e, idx) => (
                <div key={idx} style={{ background: 'rgba(244, 63, 94, 0.05)', border: '1px solid rgba(244, 63, 94, 0.2)', borderRadius: '8px', padding: '12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                    <span style={{ fontSize: '13px', fontWeight: '600', color: '#fb7185' }}>{e.title}</span>
                    <span className="badge badge-danger">{e.severity}</span>
                  </div>
                  <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{e.description}</p>
                  {e.clause_reference && (
                    <span style={{ fontSize: '11px', color: 'var(--text-dim)', marginTop: '4px', display: 'inline-block' }}>
                      Cláusula: {e.clause_reference}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Notas de Validação */}
          <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-subtle)', borderRadius: '8px', padding: '12px' }}>
            <h4 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '6px' }}>Auditoria Regulatória SUSEP</h4>
            <ul style={{ paddingLeft: '18px', fontSize: '12px', color: 'var(--text-dim)' }}>
              {policy.validation_notes.map((n, idx) => (
                <li key={idx} style={{ marginBottom: '4px' }}>{n}</li>
              ))}
            </ul>
          </div>
        </div>

        {/* Footer */}
        <div style={{ padding: '16px 24px', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'flex-end' }}>
          <button className="btn-secondary" onClick={onClose}>Fechar</button>
        </div>
      </div>
    </div>
  );
}
