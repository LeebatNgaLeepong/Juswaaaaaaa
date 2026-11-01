// Blackjack x Buckshot Roulette - useActionGuard hook
// Runs one action at a time with a minimum cooldown gap.
// While an action (plus its minimum gap) is running, every other call is ignored.
// This is a throttle (first click runs immediately, extras are dropped), NOT a debounce.

import { useCallback, useRef, useState } from 'react'

/**
 * Runs one action at a time with a minimum gap.
 * @returns {Object} { run, locked }
 *   - run(action, minGapMs): executes action if not locked, waits minGapMs after
 *   - locked: boolean, true while action+cooldown is running (for button styling)
 */
export function useActionGuard() {
  const running = useRef(false)          // read synchronously, blocks instant double-clicks
  const [locked, setLocked] = useState(false)   // only used to grey out buttons

  const run = useCallback(async (action, minGapMs = 500) => {
    if (running.current) return false     // ignored: something is already running
    running.current = true
    setLocked(true)
    const started = performance.now()
    try {
      await action()
    } catch (err) {
      console.error('Action failed:', err)
    }
    const left = minGapMs - (performance.now() - started)
    if (left > 0) await new Promise(resolve => setTimeout(resolve, left))
    running.current = false
    setLocked(false)
    return true
  }, [])

  return { run, locked }
}