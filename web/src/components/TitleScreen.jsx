// Blackjack x Buckshot Roulette - Title Screen component (one-screen)

import { useState } from 'react'
import { useMediaQuery } from 'react-responsive'
import Atmosphere from './Atmosphere'
import Card from './Card'
import CardRain from './CardRain'
import Controls from './Controls'
import '../styles/intro.css'
import '../styles/table.css'

export default function TitleScreen({ onPlay, onRules, onMute, muted }) {
  const [showRules, setShowRules] = useState(false)
  const isSmallScreen = useMediaQuery({ maxWidth: 700 })
  const rainCount = isSmallScreen ? 12 : 22

  return (
    <div className='title-screen' style={{
      position: 'relative',
      height: '100dvh',
      display: 'grid',
      gridTemplateRows: '1fr auto',
      gap: 'var(--gap)',
      padding: 'var(--gap) clamp(8px, 2vw, 24px)',
      boxSizing: 'border-box',
      overflow: 'hidden'
    }}>
      <Atmosphere />

      {/* Card Rain - between Atmosphere and title-block */}
      <CardRain count={rainCount} />

      <div className='title-block' style={{
        position: 'relative',
        zIndex: 10,
        textAlign: 'center',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        gap: 'var(--gap)'
      }}>
        {/* Card fan */}
        <div className='title-fan visible'>
          <Card card={{ rank: 'Q', suit: 'clubs' }} />
          <Card card={{ rank: 'K', suit: 'spades' }} />
          <Card card={{ rank: '10', suit: 'diamonds' }} />
        </div>

        {/* Title */}
        <h1 className='title-1'>BLACKJACK</h1>
        <h1 className='title-2 visible'>x BUCKSHOT ROULETTE</h1>

        {/* Buttons */}
        <Controls
          state='TITLE'
          onPlay={onPlay}
          onMute={onMute}
          muted={muted}
          locked={false}
        />
      </div>

      {/* Rules Modal */}
      {showRules && (
        <div className='modal-overlay' onClick={() => setShowRules(false)} role='dialog' aria-modal='true' aria-labelledby='rules-title' style={{ zIndex: 50 }}>
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