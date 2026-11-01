// Blackjack x Buckshot Roulette - DevBar component
// Only rendered in mock mode. Switches states with keys 1-9.

import { useEffect, useState } from 'react'
import { allStates, stateLabels } from './mockStates'
import '../styles/intro.css'

export default function DevBar({ currentState, setState }) {
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === 'd' && (e.ctrlKey || e.metaKey)) {
        setVisible(v => !v)
      }
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [])

  if (!visible) return null

  return (
    <div style={{
      position: 'fixed',
      bottom: 12,
      right: 12,
      zIndex: 9999,
      background: 'var(--bg-1)',
      border: '1px solid var(--gold)',
      borderRadius: 8,
      padding: '8px 12px',
      fontSize: '0.75rem',
      color: 'var(--bone)',
      fontFamily: 'monospace',
      maxWidth: '300px',
      boxShadow: '0 4px 20px rgba(0,0,0,0.5)'
    }}>
      <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap', alignItems: 'center' }}>
        <strong>Mock:</strong>
        {allStates.map((s, i) => (
          <button
            key={i}
            onClick={() => setState(s)}
            style={{
              padding: '2px 8px',
              border: currentState === s ? '1px solid var(--lamp)' : '1px solid var(--gold)',
              background: currentState === s ? 'var(--bg-2)' : 'transparent',
              color: currentState === s ? 'var(--lamp)' : 'var(--bone)',
              borderRadius: 4,
              cursor: 'pointer',
              fontSize: '0.7rem',
              fontFamily: 'monospace',
              transition: 'all 0.1s'
            }}
            title={stateLabels[i]}
          >
            {i + 1}
          </button>
        ))}
        <span style={{ marginLeft: '8px', color: 'var(--ash)' }}>Ctrl+D to toggle</span>
      </div>
    </div>
  )
}