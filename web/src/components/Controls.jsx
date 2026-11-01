// Blackjack x Buckshot Roulette - Controls component

import '../styles/intro.css'

export default function Controls({
  state,
  roundResult,
  onHit,
  onStand,
  onTrigger,
  onNext,
  onPlay,
  onMute,
  muted,
  disabled = false
}) {
  const buttons = []

  if (state === 'PLAYER_TURN') {
    buttons.push(
      <button key='hit' className='btn' onClick={onHit} disabled={disabled}>Hit</button>,
      <button key='stand' className='btn' onClick={onStand} disabled={disabled}>Stand</button>
    )
  } else if (state === 'ROUND_RESULT') {
    if (roundResult === 'push') {
      buttons.push(
        <button key='next' className='btn' onClick={onNext} disabled={disabled}>Next Round</button>
      )
    } else {
      buttons.push(
        <button key='trigger' className='btn btn--danger' onClick={onTrigger} disabled={disabled}>Pull Trigger</button>
      )
    }
  } else if (state === 'TRIGGER_PULL') {
    buttons.push(
      <button key='next' className='btn' onClick={onNext} disabled={disabled}>Next Round</button>
    )
  } else if (state === 'GAME_OVER') {
    buttons.push(
      <button key='play' className='btn' onClick={onPlay} disabled={disabled}>Play Again</button>
    )
  } else if (state === 'TITLE') {
    buttons.push(
      <button key='play' className='btn' onClick={onPlay} disabled={disabled}>Play</button>,
      <button key='rules' className='btn' onClick={() => {}} disabled={disabled}>How to Play</button>,
      <button key='mute' className='btn' onClick={onMute} disabled={disabled}>{muted ? 'Unmute' : 'Mute'}</button>
    )
  }

  return (
    <div className='controls' style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
      {buttons}
    </div>
  )
}