<script setup>
import { ref } from 'vue'

function playCard(index) {
  cards.value.splice(index, 1)
}

const suitSymbol = (suit) => {
  switch (suit) {
    case "hearts": return "♥"
    case "spades": return "♠"
    case "diamonds": return "♦"
    case "clubs": return "♣"
  }
}

const cards = ref([{ suit: 'hearts', sign: 'A', value: 14 }, { suit: 'hearts', sign: 'A', value: 14 }, { suit: 'clubs', sign: 'K', value: 2 }, { suit: 'spades', sign: '10', value: 10 }])
</script>

<template>
  <div class="card-container">
    <div 
      v-for="(card, index) in cards" 
      :key="index" 
      class="card" 
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
  bottom: 20px;
  left : 0;
  width: 100%;
  display: flex;
  justify-content: center;
  gap: 12px;
}

.card {
  width: 80px;
  height: 120px;
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

.card:hover {
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