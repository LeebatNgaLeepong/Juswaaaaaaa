// Blackjack x Buckshot Roulette - SafeImage component
// An <img> that shows a fallback when the file is missing.
// This lets you add assets later without crashing anything.

import { useState } from 'react'

export default function SafeImage({ src, alt, fallback = null, ...props }) {
  const [failed, setFailed] = useState(false)
  if (failed) return fallback
  return <img src={src} alt={alt} onError={() => setFailed(true)} draggable={false} {...props} />
}