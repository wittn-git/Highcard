<script setup>
import { ref } from 'vue'

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

const suitSymbol = (suit) => {
  switch (suit) {
    case "hearts": return "♥"
    case "spades": return "♠"
    case "diamonds": return "♦"
    case "clubs": return "♣"
  }
}

const handCards = ref([{ suit: 'hearts', sign: 'A', value: 14 }, { suit: 'hearts', sign: 'A', value: 14 }, { suit: 'clubs', sign: 'K', value: 2 }, { suit: 'spades', sign: '10', value: 10 }])
const oppHandCards = ref([{ suit: 'clubs', sign: 'B', value: 11 }, { suit: 'diamonds', sign: '8', value: 8 }, { suit: 'clubs', sign: 'K', value: 2 }])
const tableCards = ref([])
const oppTableCards = ref([])

</script>

<template>
  <div class="card-container top">
    <div 
      v-for="(card, index) in oppHandCards" 
      :key="index" 
      class="card back"
    >
      <div class="card-back-pattern"></div>
    </div>
  </div>

  <div class="table">
    <div class="table-cards">
      <div 
        v-if="oppTableCards.length" 
        class="card" 
        :class="oppTableCards[oppTableCards.length - 1].suit"
      >
        <div class="card-sign top">{{ oppTableCards[oppTableCards.length - 1].sign }}{{ suitSymbol(oppTableCards[oppTableCards.length - 1].suit) }}</div>
        <div class="card-suit">{{ suitSymbol(oppTableCards[oppTableCards.length - 1].suit) }}</div>
        <div class="card-sign bottom">{{ oppTableCards[oppTableCards.length - 1].sign }}{{ suitSymbol(oppTableCards[oppTableCards.length - 1].suit) }}</div>
      </div>

      <div 
        v-if="tableCards.length" 
        class="card" 
        :class="tableCards[tableCards.length - 1].suit"
      >
        <div class="card-sign top">{{ tableCards[tableCards.length - 1].sign }}{{ suitSymbol(tableCards[tableCards.length - 1].suit) }}</div>
        <div class="card-suit">{{ suitSymbol(tableCards[tableCards.length - 1].suit) }}</div>
        <div class="card-sign bottom">{{ tableCards[tableCards.length - 1].sign }}{{ suitSymbol(tableCards[tableCards.length - 1].suit) }}</div>
      </div>
    </div>
  </div>

  <div class="card-container bottom">
    <div 
      v-for="(card, index) in handCards" 
      :key="index" 
      class="card hoverable" 
      :class="card.suit"
      @click="playCard(index)"
    >
      <div class="card-sign top">{{ card.sign }}{{ suitSymbol(card.suit) }}</div>
      <div class="card-suit">{{ suitSymbol(card.suit) }}</div>
      <div class="card-sign bottom">{{ card.sign }}{{ suitSymbol(card.suit) }}</div>
    </div>
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

.card {
  width: 100px;
  height: 150px;
  background: white;
  border-radius: 10px;
  border: 2px solid #333;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 8px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.card.back {
  background: #FF0000; /* deep red */
  border: 4px solid white;
  outline: 3px solid #FF0000;
  box-shadow: 0 0 0 2px navy;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: default;
}

.card-back-pattern {
  width: 90%;
  height: 90%;
  border-radius: 12px;
  background-color: #FF3333;
  background-image:
    radial-gradient(circle, white 20%, transparent 22%),
    conic-gradient(from 0deg, white 0 10deg, transparent 10deg 20deg),
    conic-gradient(from 90deg, white 0 10deg, transparent 10deg 20deg),
    conic-gradient(from 180deg, white 0 10deg, transparent 10deg 20deg),
    conic-gradient(from 270deg, white 0 10deg, transparent 10deg 20deg);
  background-size: 80px 80px;
  background-position: center;
}

.hoverable:hover {
  transform: translateY(-10px);
}

.card-sign {
  font-size: 18px;
  font-weight: bold;
}

.card-sign.top {
  align-self: flex-start;
}

.card-sign.bottom {
  align-self: flex-end;
  transform: rotate(180deg);
}

.card-suit {
  font-size: 32px;
  text-align: center;
}

.hearts, .diamonds {
  color: red;
}

.spades, .clubs {
  color: black;
}
</style>