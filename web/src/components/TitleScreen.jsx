// Blackjack x Buckshot Roulette - Title Screen component

import { useState } from 'react'
import Atmosphere from './Atmosphere'
import Card from './Card'
import Controls from './Controls'
import '../styles/intro.css'

export default function TitleScreen({ onPlay, onRules, onMute, muted }) {
  const [showRules, setShowRules] = useState(false)

  return (
    <div className='title-screen' style={{ position: 'relative', minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <Atmosphere />

      <div style={{ position: 'relative', zIndex: 10, textAlign: 'center', padding: '20px' }}>
        {/* Card fan */}
        <div className='title-fan visible'>
          <Card card={{ rank: 'Q', suit: 'clubs' }} />
          <Card card={{ rank: 'K', suit: 'spades' }} />
          <Card card={{ rank: '10', suit: 'diamonds' }} />
        </div>

        {/* Title */}
        <h1 className='title-1' style={{ marginTop: '16px' }}>BLACKJACK</h1>
        <h1 className='title-2 visible' style={{ marginTop: '4px' }}>x BUCKSHOT ROULETTE</h1>

        {/* Buttons */}
        <div style={{ marginTop: '40px', display: 'flex', flexDirection: 'column', gap: '12px', alignItems: 'center' }}>
          <Controls
            state='TITLE'
            onPlay={onPlay}
            onMute={onMute}
            muted={muted}
            disabled={false}
          />
          <button
            className='btn'
            onClick={() => setShowRules(true)}
            style={{ width: '200px' }}
          >
            How to Play
          </button>
        </div>
      </div>

      {/* Rules Modal */}
      {showRules && (
        <div className='modal-overlay' onClick={() => setShowRules(false)} role='dialog' aria-modal='true' aria-labelledby='rules-title'>
          <div className='modal' onClick={e => e.stopPropagation()}>
            <h2 id='rules-title'>How to Play</h2>
            <p>
              Win the round at blackjack. The loser pulls the trigger.
              Live shells hurt. Bust and a live shell takes two.
              Lose all three candles and you are done.
            </p>
            <div className='btn-row'>
              <button className='btn' onClick={() => setShowRules(false)}>Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}