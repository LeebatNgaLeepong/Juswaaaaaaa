// Blackjack x Buckshot Roulette - CardRain component
// Tarot cards slowly fall from top to bottom with three depth layers.

import { useMemo, useEffect } from 'react'
import { cardSrc, RANKS, SUITS } from '../assets'
import SafeImage from './SafeImage'
import '../styles/rain.css'

const LAYERS = [
  { name: 'far',  w: [48, 64],   o: [0.12, 0.2],  blur: 2,   dur: [20, 28] },
  { name: 'mid',  w: [72, 96],   o: [0.2, 0.32],  blur: 1,   dur: [13, 19] },
  { name: 'near', w: [110, 150], o: [0.3, 0.45],  blur: 0.5, dur: [9, 13] },
]

const rand = (min, max) => min + Math.random() * (max - min)
const pick = (arr) => arr[Math.floor(Math.random() * arr.length)]

function makeCards(count) {
  return Array.from({ length: count }, (_, i) => {
    const layer = LAYERS[i % LAYERS.length]
    // about 40 percent card backs, the rest random faces
    const card = Math.random() < 0.4 ? null : { rank: pick(RANKS), suit: pick(SUITS) }
    return {
      id: i,
      src: cardSrc(card),
      style: {
        '--x': `${rand(-3, 100)}vw`,
        '--w': `${rand(...layer.w)}px`,
        '--o': rand(...layer.o),
        '--b': `${layer.blur}px`,
        '--dur': `${rand(...layer.dur)}s`,
        '--delay': `-${rand(0, layer.dur[1])}s`,   // negative = already mid-fall at start
        '--r0': `${rand(-35, 35)}deg`,
        '--r1': `${rand(-120, 120)}deg`,
        '--drift': `${rand(-12, 12)}vw`,
      },
    }
  })
}

export default function CardRain({ count = 20 }) {
  const cards = useMemo(() => makeCards(count), [count])

  // Pause animation when tab is hidden
  useEffect(() => {
    const handleVisibilityChange = () => {
      const rainEl = document.querySelector('.rain')
      if (rainEl) {
        rainEl.classList.toggle('paused', document.hidden)
      }
    }
    document.addEventListener('visibilitychange', handleVisibilityChange)
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange)
  }, [])

  return (
    <div className='rain' aria-hidden='true'>
      {cards.map(c => (
        <SafeImage key={c.id} className='rain-card' src={c.src} alt='' style={c.style} />
      ))}
    </div>
  )
}