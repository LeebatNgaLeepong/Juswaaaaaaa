// Blackjack x Buckshot Roulette - Hand component

import Card from './Card'
import '../styles/table.css'

export default function Hand({ cards, hideSecond = false }) {
  return (
    <div className='hand' role='list' aria-label='Hand of cards'>
      {cards.map((card, i) => {
        const isHidden = hideSecond && i === 1
        return <Card key={i} card={isHidden ? null : card} index={i} />
      })}
    </div>
  )
}