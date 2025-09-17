<script setup>
import Card from './Card.vue'

const props = defineProps({
  tableCards: { type: Array, default: () => [] },
  oppTableCards: { type: Array, default: () => [] }
})
</script>

<template>
    <div class="table">
        <div class="table-cards">
            <Card
                v-if="oppTableCards.length"
                v-bind="oppTableCards[oppTableCards.length - 1]"
                :key="'opp-' + oppTableCards[oppTableCards.length - 1].id"
                :style="{ transform: 'translateY(-20px) rotate(-5deg)' }"
            />
            
            <Card
                v-if="tableCards.length"
                v-bind="tableCards[tableCards.length - 1]"
                :key="'player-' + tableCards[tableCards.length - 1].id"
                :style="{ transform: 'translateY(20px) rotate(5deg)' }"
            />
        </div>
    </div>
</template>

<style scoped>
.table-cards {
  position: absolute;
  top: 50%;
  left: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transform: translate(-50%, -50%);
  gap: 12px;
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