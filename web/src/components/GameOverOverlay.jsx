// Blackjack x Buckshot Roulette - Game Over Overlay component

import Controls from './Controls'
import '../styles/table.css'

export default function GameOverOverlay({ game, onPlayAgain, busy }) {
  if (!game) return null

  const winner = game.winner
  const isWin = winner === 'player'

  return (
    <div className='game-over-overlay' style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(5, 5, 7, 0.98)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '20px',
      gap: '24px',
      animation: 'fade-in 1s ease-out forwards'
    }}>
      <h1 className={isWin ? 'win' : 'lose'} style={{
        margin: 0,
        fontSize: 'clamp(2.5rem, 8vw, 5rem)',
        textShadow: '0 0 30px currentColor',
        color: isWin ? 'var(--gold)' : 'var(--blood-bright)'
      }}>
        {isWin ? "The Dealer's last candle goes out." : 'Your last candle goes out.'}
      </h1>

      <div className='final-stats' style={{
        color: 'var(--ash)',
        fontSize: 'clamp(1rem, 2vw, 1.3rem)',
        textAlign: 'center'
      }}>
        <p>Final HP — You: {game.player.hp}  Dealer: {game.dealer.hp}</p>
        <p style={{ marginTop: '8px', color: 'var(--bone)' }}>
          {isWin ? 'You survived the chamber.' : 'The chamber claimed you.'}
        </p>
      </div>

      <Controls
        state='GAME_OVER'
        onPlay={onPlayAgain}
        disabled={busy}
      />
    </div>
  )
}