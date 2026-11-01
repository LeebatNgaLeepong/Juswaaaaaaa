// Blackjack x Buckshot Roulette - useGame hook
// Handles game state, API calls, animations, and sound triggers

import { useEffect, useRef, useState } from 'react'
import { allStates } from '../dev/mockStates'
import useSound from './useSound'
import { useActionGuard } from './useActionGuard'

const API_BASE = '/api'

export default function useGame() {
  const [game, setGame] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)
  const [flash, setFlash] = useState(false)
  const [shake, setShake] = useState(false)
  const [revealDealer, setRevealDealer] = useState(false)
  const [showGameOver, setShowGameOver] = useState(false)
  const [screenState, setScreenState] = useState('INTRO') // INTRO, TITLE, PLAYING
  const [introSeen, setIntroSeen] = useState(false)

  const sound = useSound()
  const prevStateRef = useRef(null)
  const dealerRevealTimer = useRef(null)

  // Action guard for spam prevention
  const { run, locked } = useActionGuard()

  // Check for mock mode
  const isMock = new URLSearchParams(window.location.search).get('mock') === '1'
  const isCardGallery = new URLSearchParams(window.location.search).get('cards') === '1'

  // Load intro seen flag
  useEffect(() => {
    try {
      const seen = sessionStorage.getItem('introSeen')
      if (seen) setIntroSeen(true)
    } catch (e) {
      // Ignore
    }
  }, [])

  // Fetch game state from API
  const fetchState = async () => {
    if (isMock) return
    try {
      const res = await fetch(`${API_BASE}/state`)
      if (!res.ok) throw new Error(`Server error: ${res.status}`)
      const data = await res.json()
      setGame(data)
    } catch (e) {
      setError('Cannot reach the game server. Is uvicorn running?')
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchState()
    const interval = setInterval(fetchState, 1000) // Poll for changes
    return () => clearInterval(interval)
  }, [])

  // Handle state changes and trigger animations/sounds
  useEffect(() => {
    if (!game) return

    // Dealer reveal delay (PLAYER_TURN -> ROUND_RESULT after stand)
    if (prevStateRef.current === 'PLAYER_TURN' && game.state === 'ROUND_RESULT') {
      setRevealDealer(true)
      sound.play('card')
      dealerRevealTimer.current = setTimeout(() => {
        setRevealDealer(false)
      }, 800)
    }

    // Trigger pull animations
    if (prevStateRef.current === 'ROUND_RESULT' && game.state === 'TRIGGER_PULL') {
      const shot = game.last_shot
      if (shot && shot.result !== null) {
        setFlash(shot.result)
        setShake(shot.result)
        sound.play(shot.result ? 'shot_live' : 'shot_blank')
        // Lamp dip
        setTimeout(() => {}, 100) // Placeholder for lamp dip
      }
    }

    // Game over
    if (game.state === 'GAME_OVER' && !showGameOver) {
      setShowGameOver(true)
      sound.play(game.winner === 'player' ? 'win' : 'lose')
      // Slow darken then overlay
      setTimeout(() => {
        // Overlay is shown via showGameOver
      }, 1500)
    }

    prevStateRef.current = game.state
  }, [game])

  // Cleanup timers
  useEffect(() => {
    return () => {
      if (dealerRevealTimer.current) clearTimeout(dealerRevealTimer.current)
    }
  }, [])

  // Handlers - wrapped with action guard
  const apiCall = async (endpoint, method = 'POST') => {
    if (isMock) return // Mock mode handled separately
    if (!game) return
    try {
      const v = game.version
      const res = await fetch(`${API_BASE}${endpoint}?v=${v}`, { method })
      if (res.status === 409) {
        // Stale request - server returned current state
        const data = await res.json()
        setGame(data)
        return data
      }
      if (!res.ok) throw new Error(`API error: ${res.status}`)
      const data = await res.json()
      setGame(data)
      return data
    } catch (e) {
      setError(e.message)
      console.error(e)
    }
  }

  const onPlay = () => run(async () => {
    sound.play('click')
    if (isMock) {
      setGame(allStates[0])
    } else {
      await apiCall('/match/new')
    }
    setScreenState('PLAYING')
  }, 500)

  const onHit = () => run(async () => {
    if (isMock) {
      // Simple mock: just advance to next mock state
      const idx = allStates.findIndex(s => s === game)
      if (idx >= 0 && idx < allStates.length - 1) {
        sound.play('card')
        setGame(allStates[idx + 1])
      }
    } else {
      sound.play('card')
      await apiCall('/hit')
    }
  }, 450)

  const onStand = () => run(async () => {
    if (isMock) {
      const idx = allStates.findIndex(s => s === game)
      if (idx >= 0 && idx < allStates.length - 1) {
        sound.play('card')
        setGame(allStates[idx + 1])
      }
    } else {
      sound.play('card')
      await apiCall('/stand')
      // Dealer reveal delay is inside the lock
      await new Promise(resolve => setTimeout(resolve, 800))
    }
  }, 900)

  const onTrigger = () => run(async () => {
    sound.play('click')
    if (isMock) {
      const idx = allStates.findIndex(s => s === game)
      if (idx >= 0 && idx < allStates.length - 1) {
        setGame(allStates[idx + 1])
      }
    } else {
      await apiCall('/trigger')
    }
    // Flash, shake, sound handled in useEffect on state change
  }, 1200)

  const onNext = () => run(async () => {
    sound.play('click')
    if (isMock) {
      const idx = allStates.findIndex(s => s === game)
      if (idx >= 0 && idx < allStates.length - 1) {
        setGame(allStates[idx + 1])
      }
    } else {
      await apiCall('/next')
    }
  }, 600)

  const onIntroDone = () => {
    setScreenState('TITLE')
    try { sessionStorage.setItem('introSeen', '1') } catch (e) {}
  }

  const onSkipIntro = () => {
    if (dealerRevealTimer.current) clearTimeout(dealerRevealTimer.current)
    onIntroDone()
  }

  // Initial load for mock mode
  useEffect(() => {
    if (isMock && !game) {
      setGame(allStates[0])
      setLoading(false)
    }
  }, [isMock])

  // Dev check for page height
  useEffect(() => {
    if (!import.meta.env.DEV) return
    const check = () => {
      const el = document.documentElement
      if (el.scrollHeight > window.innerHeight + 1) {
        console.warn('Page taller than screen:', el.scrollHeight, 'vs', window.innerHeight)
      }
    }
    window.addEventListener('resize', check)
    const interval = setInterval(check, 2000)
    return () => {
      window.removeEventListener('resize', check)
      clearInterval(interval)
    }
  }, [])

  return {
    game,
    loading,
    error,
    message,
    busy,
    flash,
    shake,
    revealDealer,
    showGameOver,
    screenState,
    introSeen,
    sound,
    locked,
    setMessage,
    onPlay,
    onHit,
    onStand,
    onTrigger,
    onNext,
    onIntroDone,
    onSkipIntro,
    setScreenState,
    isMock,
    isCardGallery
  }
}