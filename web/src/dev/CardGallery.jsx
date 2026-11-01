// Blackjack x Buckshot Roulette - Card Gallery (dev check)
// Shows all 52 cards plus the back when URL has ?cards=1

import { useEffect, useState } from 'react'
import Card from '../components/Card'
import { RANKS, SUITS, cardSrc, preloadCards } from '../assets'
import '../styles/table.css'

export default function CardGallery() {
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    preloadCards()
    setLoaded(true)
  }, [])

  if (!loaded) return <div style={{ color: 'var(--bone)', padding: '20px' }}>Loading...</div>

  return (
    <div style={{
      padding: '20px',
      background: 'var(--bg-0)',
      color: 'var(--bone)',
      minHeight: '100vh',
      fontFamily: 'IM Fell English, Georgia, serif'
    }}>
      <h1 style={{ fontFamily: 'Cinzel, Georgia, serif', color: 'var(--gold)' }}>Card Gallery</h1>
      <p>Check all 52 cards and the back load correctly. Broken images show the CSS fallback.</p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))', gap: '16px', marginTop: '20px' }}>
        {/* Card back */}
        <Card card={null} />

        {/* All 52 cards */}
        {SUITS.map(suit =>
          RANKS.map(rank => (
            <Card key={`${rank}_${suit}`} card={{ rank, suit }} />
          ))
        )}
      </div>
    </div>
  )
}