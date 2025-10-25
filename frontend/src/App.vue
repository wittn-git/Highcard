<script setup>
import { ref, onMounted } from 'vue'
import TableCards from './components/TableCards.vue'
import CardContainer from './components/CardContainer.vue'
import SelectionPopup from './components/SelectionPopup.vue'

// Game state variables
const handCards = ref([])
const oppHandCards = ref([])
const tableCards = ref([])
const oppTableCards = ref([])

// UI state variables
const showCardPopup = ref(true)
const showModelPopup = ref(false)
const showWinnerPopup = ref(false)

// PopUp options
const cardOptions = ref([])
const modelOptions = ref([])
const winner = ref([])

// PopUp selections
const selectedCardCount = ref(null)
const selectedModel = ref(null)

// --- API helpers ---
const API_BASE = 'http://localhost:5000'

async function fetchJson(url) {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`Request failed: ${res.status}`)
  return res.json()
}

async function postJson(url, body) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  if (!res.ok) throw new Error(`Request failed: ${res.status}`)
  return res.json()
}

// Selection handlers
onMounted(async () => {
  cardOptions.value = await fetchJson(`${API_BASE}/options/cards`)
})

async function chooseCardCount(count) {
  selectedCardCount.value = count
  showCardPopup.value = false
  showModelPopup.value = true
  modelOptions.value = await fetchJson(`${API_BASE}/options/models?cards=${count}`)
}

function chooseModel(model) {
  selectedModel.value = model
  showModelPopup.value = false
  initGame()
}

function showWinner(x) {
  showWinnerPopup.value = false
  showCardPopup.value = true
}

// Game logic functions
function initGame() {
  handCards.value = []
  oppHandCards.value = []
  tableCards.value = []
  oppTableCards.value = []
  for (let i=1; i <= selectedCardCount.value; i++){
    handCards.value.push({id: i, suit: 'spades', value: i})
    oppHandCards.value.push({id: i + selectedCardCount.value, suit: 'hearts', value: i})
  }
}

async function playCard(index) {

  // player plays card
  const card = handCards.value[index]
  tableCards.value.push(card)
  handCards.value.splice(index, 1)

  // opponent plays card
  const payloadCard = {
    tableCards: tableCards.value.map(c => c.value),
    oppTableCards: oppTableCards.value.map(c => c.value),
    cardCount: selectedCardCount.value,
    model: selectedModel.value
  }
  const resCard = await postJson(`${API_BASE}/play`, payloadCard)
  const oppCardValue = resCard.card
  const oppIndex = oppHandCards.value.findIndex(c => c.value === oppCardValue)
  oppTableCards.value.push(oppHandCards.value[oppIndex])
  oppHandCards.value.splice(oppIndex, 1)

  // check for winner
  const payloadWinner = {
    tableCards: tableCards.value.map(c => c.value),
    oppTableCards: oppTableCards.value.map(c => c.value),
    cardCount: selectedCardCount.value
  }
  const resWinner = await postJson(`${API_BASE}/winner`, payloadWinner)
  if(resWinner.winner){
    winner.value = [resWinner.winner]
    setTimeout(() => {
      showWinnerPopup.value = true
    }, 2000)
  }
}
</script>

<template>

  <!-- Number of cards selection -->
  <SelectionPopup
    v-if="showCardPopup"
    title="Select Number of Cards"
    :options="cardOptions"
    @select="chooseCardCount"
  />

  <!-- Model selection -->
  <SelectionPopup
    v-if="showModelPopup"
    title="Select Model to Play Against"
    :options="modelOptions"
    @select="chooseModel"
  />

  <!-- Game board -->
  <div v-if="!showCardPopup && !showModelPopup && !showWinnerPopup">
    <CardContainer :cards="oppHandCards" position="top" hidden />
    <TableCards :tableCards="tableCards" :oppTableCards="oppTableCards" />
    <CardContainer :cards="handCards" position="bottom" @card-click="playCard" />
  </div>

  <!-- Winner popup-->
  <SelectionPopup
    v-if="showWinnerPopup"
    title="The winner is..."
    :options="winner"
    @select="showWinner"
  />

</template>