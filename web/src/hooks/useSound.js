// Blackjack x Buckshot Roulette - useSound hook
// Safe sound loading and playing

import { useEffect, useRef, useState } from 'react'

const SOUND_FILES = {
  ambience: 'ambience.ogg',
  flicker: 'flicker.ogg',
  card: 'card.ogg',
  click: 'click.ogg',
  shot_live: 'shot_live.ogg',
  shot_blank: 'shot_blank.ogg',
  win: 'win.ogg',
  lose: 'lose.ogg',
  heartbeat: 'heartbeat.ogg'
}

export default function useSound() {
  const audioRefs = useRef({})
  const [muted, setMuted] = useState(false)
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    const base = import.meta.env.BASE_URL + 'assets/sounds/'
    Object.entries(SOUND_FILES).forEach(([key, file]) => {
      try {
        const audio = new Audio(base + file)
        audio.preload = 'auto'
        audio.volume = key === 'ambience' ? 0.3 : 0.6
        if (key === 'ambience' || key === 'heartbeat') audio.loop = true
        audioRefs.current[key] = audio
      } catch (e) {
        console.warn(`Failed to load sound: ${file}`, e)
        audioRefs.current[key] = null
      }
    })
    setLoaded(true)
  }, [])

  const play = (name) => {
    if (muted) return
    const audio = audioRefs.current[name]
    if (audio) {
      try {
        audio.currentTime = 0
        audio.play().catch(() => {}) // Ignore autoplay errors
      } catch (e) {
        // Silent fail
      }
    }
  }

  const stop = (name) => {
    const audio = audioRefs.current[name]
    if (audio) {
      audio.pause()
      audio.currentTime = 0
    }
  }

  const toggleMute = () => setMuted(m => !m)

  return { play, stop, toggleMute, muted, loaded }
}