// Blackjack x Buckshot Roulette - Atmosphere component
// Renders four fixed, click-through layers behind the UI and above the background.

import '../styles/atmosphere.css'

export default function Atmosphere() {
  return (
    <div className='atmos' aria-hidden='true'>
      <div className='fog fog-a' />
      <div className='fog fog-b' />
      <div className='lamp' />
      <div className='grain' />
      <div className='vignette' />
    </div>
  )
}