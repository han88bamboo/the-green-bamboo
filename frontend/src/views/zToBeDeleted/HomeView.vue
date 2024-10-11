<!-- Default generated view by Vue CLI, should not be actively used in the final version. -->
<!-- Currently used as Component Testing PLAYGROUND. -->

<template>
  <NavBar />
  <PromptLogin />
  <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modalPromptLogin">
    Launch Login Prompt Modal
  </button>
  <div class="home">
    <img alt="Vue logo" src="../../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>

</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import NavBar from '@/components/NavBar.vue'
import PromptLogin from '@/components/PromptLogin.vue';

export default {
  name: 'HomeView',
  components: {
    HelloWorld,
    NavBar,
    PromptLogin
  },
  mounted() {
    this.$router.push('/Users/Bottle-Listings');
  }
}
</script>
