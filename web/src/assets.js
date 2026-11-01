// Blackjack x Buckshot Roulette - Asset paths and preloading

const BASE = import.meta.env.BASE_URL

export const RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
export const SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
export const SUIT_SYMBOL = { hearts: '♥', diamonds: '♦', clubs: '♣', spades: '♠' }

// card is {rank, suit} or null (hidden card)
export function cardSrc(card) {
  if (!card) return `${BASE}assets/cards/back.png`
  return `${BASE}assets/cards/${card.rank}_${card.suit}.png`
}

// Load every card once at startup so cards never pop in late
export function preloadCards() {
  for (const suit of SUITS) {
    for (const rank of RANKS) {
      const img = new Image()
      img.src = cardSrc({ rank, suit })
    }
  }
  new Image().src = cardSrc(null)
}