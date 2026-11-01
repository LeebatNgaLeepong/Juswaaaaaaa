// Blackjack x Buckshot Roulette - HP Candles component

import '../styles/table.css'

export default function HpCandles({ hp, max = 3, label }) {
  return (
    <div className='candles' aria-label={`${label} HP ${hp} of ${max}`}>
      {Array.from({ length: max }, (_, i) => (
        <div key={i} className={`candle ${i < hp ? 'lit' : 'out'}`}>
          <div className='flame' />
          <div className='wax' />
        </div>
      ))}
    </div>
  )
}