<!-- Root Component File with Sticky Footer Layout -->

<template>
  <div id="app" class="app-container">
    <hr style="margin: 0;">
    
    <!-- Main content area that will expand to fill space -->
    <main class="main-content">
      <router-view/>
    </main>
    
    <!-- Footer will always be at bottom -->
    <FooterBar />
  </div>
</template>

<script>
import FooterBar from './components/FooterBar.vue'

export default {
  name: 'App',
  components: {
    FooterBar
  }
}
</script>

<style>
/* Global styles for sticky footer */
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

/* Styling from App.vue */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%; /* Add this for full height */
}

/* Sticky footer layout styles */
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  /* This will make the main content area expand to fill available space */
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: rgb(2, 117, 98);
}

.hover-underline {
    text-decoration: none; /* Ensure no underline by default */
}

.hover-underline:hover {
    text-decoration: underline; /* Add underline on hover */
}
</style>