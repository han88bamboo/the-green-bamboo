<template>
  <div>
    <h1>Browsing: {{ $route.params.browseDrinkType }}</h1>
    <p>This is a placeholder page. Implementation is pending.</p>
  </div>
</template>

<script setup>
const route = useRoute();
console.log('Category:', route.params.browseDrinkType);
</script>
