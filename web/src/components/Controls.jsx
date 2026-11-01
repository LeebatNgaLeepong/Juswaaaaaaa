// Blackjack x Buckshot Roulette - Controls component

import '../styles/intro.css'
import '../styles/table.css'

export default function Controls({
  state,
  roundResult,
  onHit,
  onStand,
  onTrigger,
  onNext,
  onPlay,
  onMute,
  onHome,
  muted,
  locked = false
}) {
  const buttons = []

  // Determine what actions are allowed in current state
  const canHit = state === 'PLAYER_TURN'
  const canStand = state === 'PLAYER_TURN'
  const canTrigger = state === 'ROUND_RESULT' && roundResult !== 'push'
  const canNext = (state === 'ROUND_RESULT' && roundResult === 'push') || state === 'TRIGGER_PULL'
  const canPlay = state === 'GAME_OVER' || state === 'TITLE'

  // Wrapper to blur after click (prevents Space/Enter from re-triggering)
  const makeClick = (handler) => (e) => {
    e.currentTarget.blur()
    handler(e)
  }

  if (canHit) {
    buttons.push(
      <button key='hit' type='button' className={`btn ${locked ? 'cooling' : ''}`} onClick={makeClick(onHit)} disabled={locked} style={{ '--cd': 'var(--cd-hit)' }}>Hit</button>,
      <button key='stand' type='button' className={`btn ${locked ? 'cooling' : ''}`} onClick={makeClick(onStand)} disabled={locked} style={{ '--cd': 'var(--cd-stand)' }}>Stand</button>
    )
  } else if (canTrigger) {
    buttons.push(
      <button key='trigger' type='button' className={`btn btn--danger ${locked ? 'cooling' : ''}`} onClick={makeClick(onTrigger)} disabled={locked} style={{ '--cd': 'var(--cd-trigger)' }}>Pull Trigger</button>
    )
  } else if (canNext) {
    buttons.push(
      <button key='next' type='button' className={`btn ${locked ? 'cooling' : ''}`} onClick={makeClick(onNext)} disabled={locked} style={{ '--cd': 'var(--cd-next)' }}>Next Round</button>
    )
  } else if (canPlay) {
    if (state === 'GAME_OVER') {
      buttons.push(
        <button key='play' type='button' className={`btn ${locked ? 'cooling' : ''}`} onClick={makeClick(onPlay)}>Play Again</button>,
        <button key='home' type='button' className={`btn ${locked ? 'cooling' : ''}`} onClick={makeClick(onHome)}>Home</button>
      )
    } else {
      buttons.push(
        <button key='play' type='button' className={`btn ${locked ? 'cooling' : ''}`} onClick={makeClick(onPlay)} disabled={locked}>Play</button>,
        <button key='rules' type='button' className={`btn ${locked ? 'cooling' : ''}`} onClick={makeClick(() => {})} disabled={locked}>How to Play</button>,
        <button key='mute' type='button' className={`btn ${locked ? 'cooling' : ''}`} onClick={makeClick(onMute)} disabled={locked}>{muted ? 'Unmute' : 'Mute'}</button>
      )
    }
  }

  return (
    <div className='controls' style={{ display: 'flex', gap: 'var(--gap)', justifyContent: 'center', flexWrap: 'wrap' }}>
      {buttons}
    </div>
  )
}