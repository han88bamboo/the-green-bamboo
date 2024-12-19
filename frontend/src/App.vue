<!-- Root Component File. -->

<template>
  <hr style="margin: 0;">
  <router-view/>
</template>

<style>
/* Styling from App.vue */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

.hover-underline {
    text-decoration: none; /* Ensure no underline by default */
}

.hover-underline:hover {
    text-decoration: underline; /* Add underline on hover */
}

</style>