// Blackjack x Buckshot Roulette - Table component (main game screen)

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
  busy
}) {
  if (!game) return null

  const { player, dealer, shotgun, state, round_result, last_shot } = game

  // Determine who was shot for the message
  const shotTarget = last_shot?.target
  const shotResult = last_shot?.result
  const shotDamage = last_shot?.damage

  return (
    <div className={`table-container ${flash ? 'flash' : ''} ${shake ? 'shake' : ''}`} style={{
      position: 'relative',
      minHeight: '100vh',
      width: '100%',
      display: 'flex',
      flexDirection: 'column',
    }}>
      <Atmosphere />

      {/* Dealer area */}
      <div className='dealer-area' style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '20px',
        gap: '8px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', width: '100%', justifyContent: 'center' }}>
          <HpCandles hp={dealer.hp} max={3} label='Dealer' />
        </div>
        <Hand cards={dealer.hand?.cards || []} hideSecond={revealDealer ? false : (state === 'PLAYER_TURN')} />
        {state !== 'PLAYER_TURN' && dealer.hand?.value !== null && (
          <div style={{ color: 'var(--ash)', fontSize: '0.9rem' }}>Value: {dealer.hand.value}</div>
        )}
        {state === 'PLAYER_TURN' && (
          <div style={{ color: 'var(--ash)', fontSize: '0.9rem' }}>Value: ??</div>
        )}
      </div>

      {/* Middle area: message + shotgun */}
      <div className='middle-area' style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        gap: '20px',
        padding: '0 20px'
      }}>
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

      {/* Player area */}
      <div className='player-area' style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '20px',
        gap: '16px'
      }}>
        <Hand cards={player.hand?.cards || []} />
        {player.hand?.value !== undefined && (
          <div style={{ color: 'var(--ash)', fontSize: '0.9rem' }}>Value: {player.hand.value}</div>
        )}
        <HpCandles hp={player.hp} max={3} label='Player' />
        <Controls
          state={state}
          roundResult={round_result}
          onHit={onHit}
          onStand={onStand}
          onTrigger={onTrigger}
          onNext={onNext}
          disabled={busy}
        />
      </div>

      {/* Flash overlay */}
      {flash && <div className='flash-overlay' style={{
        position: 'fixed',
        inset: 0,
        background: 'rgba(209, 32, 47, 0.4)',
        pointerEvents: 'none',
        zIndex: 50,
        animation: 'flash-fade 300ms ease-out forwards'
      }} />}

      {/* Shake is handled via CSS on container */}
    </div>
  )
}