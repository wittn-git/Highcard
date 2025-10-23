<script setup>
import { ref, onMounted } from 'vue'
import TableCards from './components/TableCards.vue'
import CardContainer from './components/CardContainer.vue'
import SelectionPopup from './components/SelectionPopup.vue'

const handCards = ref([])
const oppHandCards = ref([])
const tableCards = ref([])
const oppTableCards = ref([])

const showCardPopup = ref(true)
const showModelPopup = ref(false)
const showWinnerPopup = ref(false)
const cardOptions = ref([])
const modelOptions = ref([])
const winner = ref([])
const selectedCardCount = ref(null)
const selectedModel = ref(null)

onMounted(async () => {
  const res = await fetch('http://localhost:5000/options/cards')
  cardOptions.value = await res.json()
})

async function chooseCardCount(count) {
  selectedCardCount.value = count
  showCardPopup.value = false
  showModelPopup.value = true
  const res = await fetch(`http://localhost:5000/options/models?cards=${count}`)
  modelOptions.value = await res.json()
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
  const card = handCards.value[index]
  tableCards.value.push(card)
  handCards.value.splice(index, 1)
  const payload_card = {
    tableCards: tableCards.value.map(c => c.value),
    oppTableCards: oppTableCards.value.map(c => c.value),
    cardCount: selectedCardCount.value,
    model: selectedModel.value
  }
  const res_card = await fetch('http://localhost:5000/play', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload_card)
  })
  const res_card_json = await res_card.json()
  let oppCard = res_card_json["card"]
  let oppIndex = oppHandCards.value.findIndex(card => card.value === oppCard)
  if(oppIndex == -1){
    console.error("Opponent card not found in hand")
    return
  }
  oppTableCards.value.push(oppHandCards.value[oppIndex])
  oppHandCards.value.splice(oppIndex, 1)

  const payload_winner = {
    tableCards: tableCards.value.map(c => c.value),
    oppTableCards: oppTableCards.value.map(c => c.value),
    cardCount: selectedCardCount.value
  }
  const res_winner = await fetch('http://localhost:5000/winner', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload_winner)
  })
  const res_winner_json = await res_winner.json()
  console.log(res_winner_json)
  if(res_winner_json["winner"]){
    setTimeout(() => {
      () => {}
    }, 3000)
    winner.value = [res_winner_json["winner"]]
    showWinnerPopup.value = true
  }
}
</script>

<template>

  <!-- Number of cards -->
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
    <CardContainer :cards="oppHandCards" position="top"  /> <!-- hidden-->
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