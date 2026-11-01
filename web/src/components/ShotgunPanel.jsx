// Blackjack x Buckshot Roulette - Shotgun Panel component

import '../styles/table.css'

export default function ShotgunPanel({ live = 0, blank = 0, lastShot = null }) {
  return (
    <div className='shotgun-panel' aria-label='Shotgun shells'>
      <div className='shell-row'>
        <span className='shell-label'>Live:</span>
        {Array.from({ length: live }, (_, i) => (
          <div key={i} className='shell-icon live' aria-hidden='true' />
        ))}
        {Array.from({ length: 6 - live - blank }, (_, i) => (
          <div key={i} className='shell-icon empty' aria-hidden='true' style={{ opacity: 0.2, borderColor: 'var(--gold)' }} />
        ))}
      </div>
      <div className='shell-row'>
        <span className='shell-label'>Blank:</span>
        {Array.from({ length: blank }, (_, i) => (
          <div key={i} className='shell-icon blank' aria-hidden='true' />
        ))}
        {Array.from({ length: 6 - live - blank }, (_, i) => (
          <div key={i} className='shell-icon empty' aria-hidden='true' style={{ opacity: 0.2, borderColor: 'var(--gold)' }} />
        ))}
      </div>
      {lastShot && lastShot.result !== null && (
        <div className={`shot-result ${lastShot.result ? 'live' : 'blank'}`} role='status'>
          {lastShot.result ? (
            <>
              BANG. <strong>{lastShot.target}</strong> takes <strong>{lastShot.damage}</strong>.
            </>
          ) : (
            <>
              Click. Blank. <strong>{lastShot.target}</strong> survives.
            </>
          )}
        </div>
      )}
    </div>
  )
}