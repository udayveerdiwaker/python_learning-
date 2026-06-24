import React, { useState } from 'react'
import { Copy, Check, Shield, X, Loader2 } from 'lucide-react'

export default function ApiKeyModal({ isOpen, onClose, onAuthenticate, token }) {
  const [copied, setCopied] = useState(false)
  const [loading, setLoading] = useState(false)
  const [apiKey, setApiKey] = useState(token || '')

  if (!isOpen) return null

  const handleGenerate = async () => {
    setLoading(true)
    setCopied(false)
    try {
      const response = await fetch('/api/auth/token')
      if (response.ok) {
        const data = await response.json()
        setApiKey(data.token)
      } else {
        alert("Failed to generate token from server.")
      }
    } catch (err) {
      console.error(err)
      alert("Error generating token.")
    } finally {
      setLoading(false)
    }
  }

  const handleCopyAndUse = () => {
    navigator.clipboard.writeText(apiKey)
    setCopied(true)
    onAuthenticate(apiKey)
    setTimeout(() => {
      setCopied(false)
      onClose()
    }, 800)
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div 
        className="glass-panel modal-content" 
        style={{ maxWidth: '450px', width: '90%', padding: '2rem', position: 'relative' }}
        onClick={(e) => e.stopPropagation()}
      >
        <button className="modal-close-btn" onClick={onClose} aria-label="Close modal">
          <X size={18} />
        </button>

        <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          <div className="modal-icon-wrapper">
            <Shield size={28} />
          </div>
          <h3 className="section-title" style={{ justifyContent: 'center', margin: '0.75rem 0 0.25rem 0', fontSize: '1.35rem' }}>
            Generate API Key
          </h3>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            Generate a secure API key to authenticate your database session.
          </p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
          <button 
            type="button" 
            onClick={handleGenerate} 
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? (
              <>
                <Loader2 className="spinner" size={16} />
                <span>Generating Secure Key...</span>
              </>
            ) : (
              <span>Generate New Key</span>
            )}
          </button>

          {apiKey && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.5rem', animation: 'fadeInUp 0.3s ease' }}>
              <label style={{ fontSize: '0.75rem', fontWeight: '600', color: 'var(--text-muted)' }}>Your Generated API Key:</label>
              <div className="token-container">
                <input
                  type="text"
                  className="form-input token-input"
                  value={apiKey}
                  readOnly
                  style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(192, 132, 252, 0.3)', color: '#c084fc' }}
                />
              </div>
              
              <button
                type="button"
                className="btn"
                style={{ 
                  background: copied ? 'rgba(16, 185, 129, 0.15)' : 'rgba(255,255,255,0.05)',
                  border: copied ? '1px solid #10b981' : '1px solid var(--glass-border)',
                  color: copied ? '#34d399' : '#fff',
                  fontSize: '0.9rem',
                  marginTop: '0.5rem'
                }}
                onClick={handleCopyAndUse}
                disabled={!apiKey || loading}
              >
                {copied ? (
                  <>
                    <Check size={16} />
                    <span>Copied & Authenticated!</span>
                  </>
                ) : (
                  <>
                    <Copy size={16} />
                    <span>Copy & Use Key</span>
                  </>
                )}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
