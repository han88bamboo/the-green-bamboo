<template>
  <div>
    <h1>Browsing: {{ $route.params.browseDrinkType }} / {{ $route.params.browseTypeCategory }}</h1>
    <p>This is a placeholder page for sub-categories. Implementation is pending.</p>
  </div>
</template>

<script setup>
const route = useRoute();
console.log('Category:', route.params.browseDrinkType);
console.log('Sub-category:', route.params.browseTypeCategory);
</script>
