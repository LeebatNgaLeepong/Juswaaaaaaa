// Blackjack x Buckshot Roulette - Message Bar component

import '../styles/table.css'

export default function MessageBar({ message, state, roundResult, playerHand, dealerHand }) {
  let displayMessage = message
  let className = 'message-bar'

  if (state === 'PLAYER_TURN') {
    displayMessage = 'Your move. Hit or stand?'
  } else if (state === 'ROUND_RESULT') {
    if (roundResult === 'player') {
      displayMessage = 'You win the hand. The Dealer must face the chamber.'
    } else if (roundResult === 'dealer') {
      displayMessage = 'The house wins. You face the chamber.'
    } else if (roundResult === 'push') {
      displayMessage = 'A draw. The chamber stays quiet.'
    }
  } else if (state === 'TRIGGER_PULL') {
    // Message is passed from parent
  }

  // Add BUST/BLACKJACK indicators
  const bustPlayer = playerHand?.is_bust
  const bjPlayer = playerHand?.is_blackjack
  const bustDealer = dealerHand?.is_bust
  const bjDealer = dealerHand?.is_blackjack

  return (
    <div className={className} role='status' aria-live='polite'>
      <span>{displayMessage}</span>
      {(bustPlayer || bustDealer) && <span className='bust'> BUST</span>}
      {(bjPlayer || bjDealer) && <span className='blackjack'> BLACKJACK</span>}
    </div>
  )
}