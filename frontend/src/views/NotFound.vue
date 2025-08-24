<template>
  <div>
    <h1>404 - Not Found</h1>
    <p>The page you are looking for does not exist.</p>
    <button @click="goHome">Go to Home Page</button>
  </div>
</template>

<script>
export default {
  name: "NotFound",
  methods: {
    goHome() {
      this.$router.push('/');
    }
  }
};
</script>