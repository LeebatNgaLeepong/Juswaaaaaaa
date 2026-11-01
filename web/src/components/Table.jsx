// Blackjack x Buckshot Roulette - Table component (one-screen layout)

import Hand from './Hand'
import HpCandles from './HpCandles'
import ShotgunPanel from './ShotgunPanel'
import MessageBar from './MessageBar'
import Controls from './Controls'
import Atmosphere from './Atmosphere'
import '../styles/table.css'

export default function Table({
  game,
  revealDealer,
  flash,
  shake,
  onHit,
  onStand,
  onTrigger,
  onNext,
  busy,
  locked
}) {
  if (!game) return null

  const { player, dealer, shotgun, state, round_result, last_shot } = game

  // Add 'many' class when 5+ cards
  const dealerCards = dealer.hand?.cards || []
  const playerCards = player.hand?.cards || []
  const dealerMany = dealerCards.length >= 5
  const playerMany = playerCards.length >= 5

  // Determine who was shot for the message
  const shotTarget = last_shot?.target
  const shotResult = last_shot?.result
  const shotDamage = last_shot?.damage

  return (
    <div className={`table-screen ${flash ? 'flash' : ''} ${shake ? 'shake' : ''}`} style={{ position: 'relative' }}>
      <Atmosphere />

      {/* Dealer silhouette - absolute positioned behind */}
      {state !== 'PLAYER_TURN' && (
        <div className='dealer-silhouette' aria-hidden='true'>
          <div className='eyes'>
            <div className='eye' />
            <div className='eye' />
          </div>
        </div>
      )}

      {/* Dealer zone */}
      <div className='zone' style={{ order: 1 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', width: '100%', justifyContent: 'center', flexWrap: 'wrap' }}>
          <HpCandles hp={dealer.hp} max={3} label='Dealer' />
        </div>
        <Hand cards={dealerCards} hideSecond={revealDealer ? false : (state === 'PLAYER_TURN')} className={dealerMany ? 'many' : ''} />
        {state !== 'PLAYER_TURN' && dealer.hand?.value !== null && (
          <div style={{ color: 'var(--ash)', fontSize: 'clamp(0.7rem, 1.8vh, 0.9rem)' }}>Value: {dealer.hand.value}</div>
        )}
        {state === 'PLAYER_TURN' && (
          <div style={{ color: 'var(--ash)', fontSize: 'clamp(0.7rem, 1.8vh, 0.9rem)' }}>Value: ??</div>
        )}
      </div>

      {/* Middle area: message + shotgun */}
      <div className='middle' style={{ order: 2 }}>
        <MessageBar
          message=''
          state={state}
          roundResult={round_result}
          playerHand={player.hand}
          dealerHand={dealer.hand}
        />

        <ShotgunPanel
          live={shotgun.live}
          blank={shotgun.blank}
          lastShot={last_shot}
        />
      </div>

      {/* Player zone */}
      <div className='zone' style={{ order: 3 }}>
        <Hand cards={playerCards} className={playerMany ? 'many' : ''} />
        {player.hand?.value !== undefined && (
          <div style={{ color: 'var(--ash)', fontSize: 'clamp(0.7rem, 1.8vh, 0.9rem)' }}>Value: {player.hand.value}</div>
        )}
        <HpCandles hp={player.hp} max={3} label='Player' />
      </div>

      {/* Controls - always at bottom */}
      <div className='controls' style={{ order: 4 }}>
        <Controls
          state={state}
          roundResult={round_result}
          onHit={onHit}
          onStand={onStand}
          onTrigger={onTrigger}
          onNext={onNext}
          locked={locked}
        />
      </div>
    </div>
  )
}