<script setup>
import Card from './Card.vue'

const props = defineProps({
  cards: { type: Array, default: () => [] },
  position: { type: String, default: "bottom" },
  hidden: { type: Boolean, default: false }
})

const emit = defineEmits(['card-click'])

const handleClick = (index) => {
  emit('card-click', index)
}
</script>

<template>
  <div
    class="card-container"
    :class="position"
  >
    <Card
      v-for="(card, index) in cards"
      :key="card.id"
      v-bind="card"
      v-if="!hidden"
      hoverable
      @click="handleClick(index)"
    />
    <Card
      v-for="card in cards"
      :key="card.id"
      back
      v-if="hidden"
    />
  </div>
</template>

<style scoped>
.card-container {
  position: fixed;
  left: 0;
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
</style>