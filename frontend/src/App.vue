<script setup>
import { ref } from 'vue'
import Card from './components/Card.vue'

function playCard(index) {
  console.log('Playing card at index:', index)
  console.log('Current handCards:', handCards.value)
  let card = handCards.value[index]
  tableCards.value.push(card)
  handCards.value.splice(index, 1)

  let randIndex = Math.floor(Math.random() * oppHandCards.value.length)
  oppTableCards.value.push(oppHandCards.value[randIndex])
  oppHandCards.value.splice(randIndex, 1)
}

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

</script>

<template>
  <div class="card-container top">
    <Card v-for="(card, index) in oppHandCards" :key="index" back />
  </div>

  <div class="table">
    <div class="table-cards">
      <Card
        v-if="oppTableCards.length"
        v-bind="oppTableCards[oppTableCards.length - 1]"
      />
      <Card
        v-if="tableCards.length"
        v-bind="tableCards[tableCards.length - 1]"
      />
    </div>
  </div>

  <div class="card-container bottom">
    <Card
      v-for="(card, index) in handCards"
      :key="index"
      v-bind="card"
      hoverable="true"
      @click="playCard(index)"
    />
  </div>
</template>

<style scoped>

.card-container {
  position: fixed;
  left : 0;
  width: 100%;
  display: flex;
  justify-content: center;
  gap: 12px;
}

.bottom {
  bottom: 20px;
}

.top {
  top: 20px;
}

.table-cards {
  position: absolute;
  top: 40%;
  left: 50%;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transform: translate(-50%, -50%);
  align-items: center;
}

.table {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgb(0, 102, 0);
  z-index: -1;
}

</style>