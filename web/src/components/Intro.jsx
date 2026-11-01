// Blackjack x Buckshot Roulette - Intro sequence component

import { useEffect, useRef, useState } from 'react'
import Atmosphere from '../components/Atmosphere'
import Card from '../components/Card'
import { cardSrc } from '../assets'
import '../styles/intro.css'

const STEPS = [
  { at: 1500, name: 'lamp' },
  { at: 2800, name: 'dealer' },
  { at: 4000, name: 'title1' },
  { at: 4800, name: 'title2' },
  { at: 5800, name: 'tagline' },
  { at: 6800, name: 'cards' },
  { at: 7000, name: 'menu' },
]

export default function Intro({ onDone, playSound, onSkip }) {
  const [phase, setPhase] = useState('gate')      // gate -> playing
  const [shown, setShown] = useState([])          // which steps are visible
  const timers = useRef([])

  const start = () => {
    setPhase('playing')
    playSound('ambience')
    STEPS.forEach(s => {
      timers.current.push(setTimeout(() => setShown(prev => [...prev, s.name]), s.at))
    })
    timers.current.push(setTimeout(onDone, 7200))
  }

  const skip = () => {
    timers.current.forEach(clearTimeout)
    onDone()
  }

  useEffect(() => () => timers.current.forEach(clearTimeout), [])

  // Any key or click skips once playing
  useEffect(() => {
    if (phase !== 'playing') return
    const handleKey = () => skip()
    window.addEventListener('keydown', handleKey)
    window.addEventListener('click', handleKey)
    return () => {
      window.removeEventListener('keydown', handleKey)
      window.removeEventListener('click', handleKey)
    }
  }, [phase])

  const isVisible = (name) => shown.includes(name)

  return (
    <div className={`intro-screen ${phase}`}>
      <Atmosphere />

      {/* Gate screen */}
      <div className={`gate-screen ${phase === 'playing' ? 'hidden' : ''}`} onClick={start}>
        <div className='gate-prompt'>Click to enter</div>
      </div>

      {/* Intro layers */}
      <div className='intro-layers' style={{ position: 'fixed', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', pointerEvents: 'none', zIndex: 2 }}>
        {/* Lamp flicker */}
        <div className={`lamp-on layer ${isVisible('lamp') ? 'visible' : ''}`} style={{ width: '100%', height: '100%' }} />

        {/* Dealer silhouette */}
        <div className={`layer dealer-silhouette ${isVisible('dealer') ? 'visible' : ''}`} style={{ position: 'absolute', bottom: 0, left: '50%', transform: 'translateX(-50%)', width: 200, height: 300, opacity: 0.6, background: 'radial-gradient(ellipse at 50% 20%, var(--blood-bright) 0%, transparent 60%), radial-gradient(ellipse at 50% 85%, var(--bg-0) 0%, transparent 50%)' }}>
          <div className='eyes' style={{ position: 'absolute', top: '25%', left: '50%', transform: 'translateX(-50%)', display: 'flex', gap: '30px' }}>
            <div className='eye' style={{ width: 12, height: 12, background: 'var(--blood-bright)', borderRadius: '50%', boxShadow: '0 0 8px var(--blood-bright), 0 0 16px var(--blood-bright)', animation: 'eye-glow 3s ease-in-out infinite' }} />
            <div className='eye' style={{ width: 12, height: 12, background: 'var(--blood-bright)', borderRadius: '50%', boxShadow: '0 0 8px var(--blood-bright), 0 0 16px var(--blood-bright)', animation: 'eye-glow 3s ease-in-out infinite 0.5s' }} />
          </div>
        </div>

        {/* Title line 1 */}
        <h1 className={`title-1 layer ${isVisible('title1') ? 'visible' : ''}`}>BLACKJACK</h1>

        {/* Title line 2 */}
        <h1 className={`title-2 layer ${isVisible('title2') ? 'visible' : ''}`}>x BUCKSHOT ROULETTE</h1>

        {/* Tagline */}
        <p className={`tagline layer ${isVisible('tagline') ? 'visible' : ''}`}>Twenty-one, or the chamber.</p>

        {/* Card fan */}
        <div className={`title-fan layer ${isVisible('cards') ? 'visible' : ''}`}>
          <Card card={{ rank: 'Q', suit: 'clubs' }} />
          <Card card={{ rank: 'K', suit: 'spades' }} />
          <Card card={{ rank: '10', suit: 'diamonds' }} />
        </div>
      </div>

      <style jsx>{`
        @keyframes eye-glow {
          0%, 100% { opacity: 0.6; transform: scale(1); }
          50% { opacity: 1; transform: scale(1.2); }
        }
      `}</style>
    </div>
  )
}