// Blackjack x Buckshot Roulette - Main App component

import { useEffect } from 'react'
import Intro from './components/Intro'
import TitleScreen from './components/TitleScreen'
import Table from './components/Table'
import GameOverOverlay from './components/GameOverOverlay'
import CardGallery from './dev/CardGallery'
import DevBar from './dev/DevBar'
import { preloadCards } from './assets'
import useGame from './hooks/useGame'
import './styles/theme.css'
import './styles/atmosphere.css'
import './styles/intro.css'
import './styles/table.css'

function App() {
  const {
    game,
    loading,
    error,
    flash,
    shake,
    revealDealer,
    showGameOver,
    screenState,
    introSeen,
    sound,
    locked,
    onPlay,
    onHit,
    onStand,
    onTrigger,
    onNext,
    onHome,
    onIntroDone,
    onSkipIntro,
    setScreenState,
    isMock,
    isCardGallery
  } = useGame()

  // Preload cards on mount
  useEffect(() => {
    preloadCards()
  }, [])

  // Handle keyboard shortcuts - goes through the same guarded functions as mouse
  useEffect(() => {
    const handleKey = (e) => {
      if (screenState !== 'PLAYING' || error) return
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return
      if (e.repeat) return  // holding a key does nothing

      const key = e.key.toLowerCase()

      // Check what actions are valid in current state
      const canHit = game?.state === 'PLAYER_TURN'
      const canStand = game?.state === 'PLAYER_TURN'
      const canAdvance = (game?.state === 'ROUND_RESULT' && game.round_result !== 'push') ||
                         game?.state === 'TRIGGER_PULL' ||
                         (game?.state === 'ROUND_RESULT' && game.round_result === 'push')

      if (key === 'h' && canHit) { e.preventDefault(); onHit() }
      else if (key === 's' && canStand) { e.preventDefault(); onStand() }
      else if ((key === ' ' || key === 'enter') && canAdvance) {
        e.preventDefault()  // stops the focused button from also clicking
        if (game?.state === 'ROUND_RESULT' && game.round_result !== 'push') onTrigger()
        else if (game?.state === 'TRIGGER_PULL') onNext()
        else if (game?.state === 'ROUND_RESULT' && game.round_result === 'push') onNext()
        else if (game?.state === 'GAME_OVER') onPlay()
      } else if (key === 'm' || key === 'M') {
        sound.toggleMute()
      }
    }

    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [screenState, game, error, onHit, onStand, onTrigger, onNext, onPlay, sound])

  // Show card gallery
  if (isCardGallery) {
    return <CardGallery />
  }

  // Loading / error state
  if (loading) {
    return (
      <div style={{
        height: '100dvh',
        background: 'var(--bg-0)',
        display: 'grid',
        placeItems: 'center',
        color: 'var(--bone)',
        fontFamily: 'IM Fell English, Georgia, serif'
      }}>
        <div style={{ textAlign: 'center' }}>
          <h1 style={{ fontFamily: 'Cinzel, Georgia, serif', color: 'var(--gold)' }}>BLACKJACK x BUCKSHOT ROULETTE</h1>
          <p style={{ marginTop: '16px', color: 'var(--ash)' }}>Loading...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div style={{
        height: '100dvh',
        background: 'var(--bg-0)',
        display: 'grid',
        placeItems: 'center',
        color: 'var(--bone)',
        fontFamily: 'IM Fell English, Georgia, serif',
        padding: '20px',
        textAlign: 'center'
      }}>
        <h1 style={{ fontFamily: 'Cinzel, Georgia, serif', color: 'var(--blood-bright)' }}>Connection Error</h1>
        <p style={{ marginTop: '16px', color: 'var(--ash)' }}>{error}</p>
        <button className='btn' onClick={() => window.location.reload()} style={{ marginTop: '20px' }}>
          Retry
        </button>
      </div>
    )
  }

  return (
    <div style={{ position: 'relative', height: '100dvh', width: '100%' }}>
      {/* Screen routing */}
      {screenState === 'INTRO' && (
        <Intro
          onDone={onIntroDone}
          playSound={sound.play}
          onSkip={onSkipIntro}
        />
      )}

      {screenState === 'TITLE' && (
        <TitleScreen
          onPlay={onPlay}
          onRules={() => {}}
          onMute={sound.toggleMute}
          muted={sound.muted}
        />
      )}

      {screenState === 'PLAYING' && (
        <>
          <Table
            game={game}
            revealDealer={revealDealer}
            flash={flash}
            shake={shake}
            onHit={onHit}
            onStand={onStand}
            onTrigger={onTrigger}
            onNext={onNext}
            onHome={onHome}
            busy={false}
            locked={locked}
          />

          {showGameOver && (
            <GameOverOverlay
              game={game}
              onPlayAgain={onPlay}
              busy={false}
            />
          )}
        </>
      )}

      {/* Dev tools (mock mode only) */}
      {isMock && <DevBar currentState={game} setState={setScreenState} />}
    </div>
  )
}

export default App