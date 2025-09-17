<script setup>
import { ref } from 'vue'
import TableCards from './components/TableCards.vue'
import CardContainer from './components/CardContainer.vue'

const handCards = ref([
  { id: 1, suit: 'hearts', sign: 'A', value: 14 },
  { id: 2, suit: 'hearts', sign: 'A', value: 14 },
  { id: 3, suit: 'clubs', sign: 'K', value: 2 },
  { id: 4, suit: 'spades', sign: '10', value: 10 }
])
const oppHandCards = ref([
  { id: 1, suit: 'clubs', sign: 'B', value: 11 },
  { id: 2, suit: 'diamonds', sign: '8', value: 8 },
  { id: 3, suit: 'clubs', sign: 'K', value: 2 }
])
const tableCards = ref([])
const oppTableCards = ref([])

function playCard(index) {
  const card = handCards.value[index]
  tableCards.value.push(card)
  handCards.value.splice(index, 1)

  const randIndex = Math.floor(Math.random() * oppHandCards.value.length)
  oppTableCards.value.push(oppHandCards.value[randIndex])
  oppHandCards.value.splice(randIndex, 1)
}
</script>

<template>
  <CardContainer :cards="oppHandCards" position="top" hidden />
  <TableCards :tableCards="tableCards" :oppTableCards="oppTableCards" />
  <CardContainer :cards="handCards" position="bottom" @card-click="playCard" />
</template>