<script setup>
import { computed } from 'vue'

const props = defineProps({
  id: { type: Number, required: true },
  sign: { type: String, default: "" },
  suit: { type: String, default: "" },
  back: { type: Boolean, default: false },
  hoverable: { type: Boolean, default: false }
})

const suitSymbol = (suit) => {
  switch (suit) {
    case "hearts": return "♥"
    case "spades": return "♠"
    case "diamonds": return "♦"
    case "clubs": return "♣"
    default: return ""
  }
}

const suitIcon = computed(() => suitSymbol(props.suit))
</script>

<template>
  <div
    class="card"
    :class="['card--' + props.suit, { 'card--back': back, 'card--hoverable': hoverable }]"
  >
    <template v-if="!back">
      <div class="card-sign card-sign--top">{{ sign }}{{ suitIcon }}</div>
      <div class="card-suit">{{ suitIcon }}</div>
      <div class="card-sign card-sign--bottom">{{ sign }}{{ suitIcon }}</div>
    </template>
    <template v-else>
      <div class="card-back-pattern"></div>
    </template>
  </div>
</template>

<style scoped>
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
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card--back {
  background: #FF0000;
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

.card--hoverable:hover {
  transform: translateY(-10px) scale(1.05);
  box-shadow: 0 8px 16px rgba(0,0,0,0.4);
}

.card-sign {
  font-size: 18px;
  font-weight: bold;
}

.card-sign--top {
  align-self: flex-start;
}

.card-sign--bottom {
  align-self: flex-end;
  transform: rotate(180deg);
}

.card-suit {
  font-size: 32px;
  text-align: center;
}

.card--hearts, .card--diamonds {
  color: red;
}

.card--spades, .card--clubs {
  color: black;
}
</style>