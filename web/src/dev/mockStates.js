// Blackjack x Buckshot Roulette - Mock states for development
// These match the exact format from the server (Migration Plan, Section 5.3)

export const playerTurn = {
  state: 'PLAYER_TURN',
  round_result: null,
  player: {
    name: 'Player',
    hp: 3,
    cards: [
      { rank: 'K', suit: 'spades' },
      { rank: '7', suit: 'hearts' }
    ],
    value: 17,
    is_bust: false,
    is_blackjack: false
  },
  dealer: {
    name: 'Dealer',
    hp: 2,
    cards: [
      { rank: '9', suit: 'clubs' },
      null
    ],
    value: null,
    is_bust: false,
    is_blackjack: false,
    hidden_count: 1
  },
  shotgun: { live: 2, blank: 4 },
  last_shot: { result: null, target: null, damage: 0 },
  winner: null
}

export const playerTurnBlackjack = {
  state: 'PLAYER_TURN',
  round_result: null,
  player: {
    name: 'Player',
    hp: 3,
    cards: [
      { rank: 'A', suit: 'spades' },
      { rank: 'K', suit: 'hearts' }
    ],
    value: 21,
    is_bust: false,
    is_blackjack: true
  },
  dealer: {
    name: 'Dealer',
    hp: 2,
    cards: [
      { rank: '10', suit: 'clubs' },
      null
    ],
    value: null,
    is_bust: false,
    is_blackjack: false,
    hidden_count: 1
  },
  shotgun: { live: 1, blank: 5 },
  last_shot: { result: null, target: null, damage: 0 },
  winner: null
}

export const roundResultDealerWins = {
  state: 'ROUND_RESULT',
  round_result: 'dealer',
  player: {
    name: 'Player',
    hp: 3,
    cards: [
      { rank: 'K', suit: 'spades' },
      { rank: '8', suit: 'hearts' },
      { rank: '5', suit: 'clubs' }
    ],
    value: 23,
    is_bust: true,
    is_blackjack: false
  },
  dealer: {
    name: 'Dealer',
    hp: 2,
    cards: [
      { rank: '10', suit: 'clubs' },
      { rank: '9', suit: 'diamonds' }
    ],
    value: 19,
    is_bust: false,
    is_blackjack: false,
    hidden_count: 0
  },
  shotgun: { live: 2, blank: 4 },
  last_shot: { result: null, target: null, damage: 0 },
  winner: null
}

export const roundResultPlayerWins = {
  state: 'ROUND_RESULT',
  round_result: 'player',
  player: {
    name: 'Player',
    hp: 3,
    cards: [
      { rank: 'K', suit: 'spades' },
      { rank: 'Q', suit: 'hearts' }
    ],
    value: 20,
    is_bust: false,
    is_blackjack: false
  },
  dealer: {
    name: 'Dealer',
    hp: 2,
    cards: [
      { rank: '9', suit: 'clubs' },
      { rank: '8', suit: 'diamonds' }
    ],
    value: 17,
    is_bust: false,
    is_blackjack: false,
    hidden_count: 0
  },
  shotgun: { live: 2, blank: 4 },
  last_shot: { result: null, target: null, damage: 0 },
  winner: null
}

export const push = {
  state: 'ROUND_RESULT',
  round_result: 'push',
  player: {
    name: 'Player',
    hp: 3,
    cards: [
      { rank: 'K', suit: 'spades' },
      { rank: 'Q', suit: 'hearts' }
    ],
    value: 20,
    is_bust: false,
    is_blackjack: false
  },
  dealer: {
    name: 'Dealer',
    hp: 2,
    cards: [
      { rank: '10', suit: 'clubs' },
      { rank: '10', suit: 'diamonds' }
    ],
    value: 20,
    is_bust: false,
    is_blackjack: false,
    hidden_count: 0
  },
  shotgun: { live: 2, blank: 4 },
  last_shot: { result: null, target: null, damage: 0 },
  winner: null
}

export const triggerLive = {
  state: 'TRIGGER_PULL',
  round_result: 'dealer',
  player: {
    name: 'Player',
    hp: 1,
    cards: [
      { rank: 'K', suit: 'spades' },
      { rank: '8', suit: 'hearts' },
      { rank: '5', suit: 'clubs' }
    ],
    value: 23,
    is_bust: true,
    is_blackjack: false
  },
  dealer: {
    name: 'Dealer',
    hp: 2,
    cards: [
      { rank: '10', suit: 'clubs' },
      { rank: '9', suit: 'diamonds' }
    ],
    value: 19,
    is_bust: false,
    is_blackjack: false,
    hidden_count: 0
  },
  shotgun: { live: 1, blank: 4 },
  last_shot: { result: true, target: 'Player', damage: 2 },
  winner: null
}

export const triggerBlank = {
  state: 'TRIGGER_PULL',
  round_result: 'dealer',
  player: {
    name: 'Player',
    hp: 3,
    cards: [
      { rank: 'K', suit: 'spades' },
      { rank: '8', suit: 'hearts' },
      { rank: '5', suit: 'clubs' }
    ],
    value: 23,
    is_bust: true,
    is_blackjack: false
  },
  dealer: {
    name: 'Dealer',
    hp: 2,
    cards: [
      { rank: '10', suit: 'clubs' },
      { rank: '9', suit: 'diamonds' }
    ],
    value: 19,
    is_bust: false,
    is_blackjack: false,
    hidden_count: 0
  },
  shotgun: { live: 1, blank: 4 },
  last_shot: { result: false, target: 'Player', damage: 0 },
  winner: null
}

export const gameOverPlayerWins = {
  state: 'GAME_OVER',
  round_result: 'player',
  player: {
    name: 'Player',
    hp: 1,
    cards: [
      { rank: 'A', suit: 'spades' },
      { rank: 'K', suit: 'hearts' }
    ],
    value: 21,
    is_bust: false,
    is_blackjack: true
  },
  dealer: {
    name: 'Dealer',
    hp: 0,
    cards: [
      { rank: '9', suit: 'clubs' },
      { rank: '8', suit: 'diamonds' }
    ],
    value: 17,
    is_bust: false,
    is_blackjack: false,
    hidden_count: 0
  },
  shotgun: { live: 0, blank: 0 },
  last_shot: { result: true, target: 'Dealer', damage: 1 },
  winner: 'player'
}

export const gameOverDealerWins = {
  state: 'GAME_OVER',
  round_result: 'dealer',
  player: {
    name: 'Player',
    hp: 0,
    cards: [
      { rank: 'K', suit: 'spades' },
      { rank: '8', suit: 'hearts' },
      { rank: '5', suit: 'clubs' }
    ],
    value: 23,
    is_bust: true,
    is_blackjack: false
  },
  dealer: {
    name: 'Dealer',
    hp: 1,
    cards: [
      { rank: '10', suit: 'clubs' },
      { rank: '9', suit: 'diamonds' }
    ],
    value: 19,
    is_bust: false,
    is_blackjack: false,
    hidden_count: 0
  },
  shotgun: { live: 0, blank: 0 },
  last_shot: { result: true, target: 'Player', damage: 2 },
  winner: 'dealer'
}

// All states in order for DevBar (keys 1-9)
export const allStates = [
  playerTurn,
  playerTurnBlackjack,
  roundResultDealerWins,
  roundResultPlayerWins,
  push,
  triggerLive,
  triggerBlank,
  gameOverPlayerWins,
  gameOverDealerWins
]

export const stateLabels = [
  'PLAYER_TURN',
  'PLAYER_TURN (Blackjack)',
  'ROUND_RESULT (Dealer wins)',
  'ROUND_RESULT (Player wins)',
  'ROUND_RESULT (Push)',
  'TRIGGER_PULL (Live)',
  'TRIGGER_PULL (Blank)',
  'GAME_OVER (Player wins)',
  'GAME_OVER (Dealer wins)'
]