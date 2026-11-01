// Blackjack x Buckshot Roulette - Card component (image version)

import SafeImage from './SafeImage'
import { cardSrc, SUIT_SYMBOL } from '../assets'
import '../styles/table.css'

export default function Card({ card, index = 0 }) {
  const label = card ? `${card.rank} of ${card.suit}` : 'Face-down card'
  const red = card && (card.suit === 'hearts' || card.suit === 'diamonds')

  // Drawn fallback, used only if the PNG is missing
  const fallback = (
    <div className={`card-fallback ${card ? (red ? 'red' : 'black') : 'back'}`}>
      {card && <span>{card.rank}{SUIT_SYMBOL[card.suit]}</span>}
    </div>
  )

  return (
    <div className='card' style={{ animationDelay: `${index * 140}ms` }}>
      {/* key makes the flip-in replay when a hidden card is revealed */}
      <SafeImage
        key={card ? 'front' : 'back'}
        className={card ? 'card-img flip-in' : 'card-img'}
        src={cardSrc(card)}
        alt={label}
        fallback={fallback}
      />
    </div>
  )
}