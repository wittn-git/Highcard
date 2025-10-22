<script setup>
    defineProps({
        title: String,
        options: Array
    })

    defineEmits(['select'])
</script>

<template>
  <div class="popup">
    <h2>{{ title }}</h2>
    <div class="buttons">
      <button
        v-for="option in options"
        :key="option"
        @click="$emit('select', option)"
      >
        {{ option }}
      </button>
    </div>
  </div>
</template>

<style scoped>
    .popup {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: grey;
        border-radius: 1rem;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
        padding: 2rem;
        text-align: center;
        z-index: 100;
    }

    .buttons {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1rem;
        margin-top: 1rem;
    }

    button {
        padding: 0.6rem 1.2rem;
        border: none;
        border-radius: 0.5rem;
        background: darkgrey;
        color: white;
        cursor: pointer;
        font-size: 1rem;
    }

    button:hover {
        background: #2980b9;
    }

</style>