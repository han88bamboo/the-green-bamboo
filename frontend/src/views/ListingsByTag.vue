<template>
    <div>
        <searchView />
    </div>  
</template>

<script>
import searchView from './SearchView.vue';
import axios from 'axios';

export default {
    components: {
        searchView,
    },
  data() {
    return {
      tag: ""
    };
  },
  mounted() {
    this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      const tag = this.$route.query.tag; 
      if (!tag) return;
      
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingsByObservationTag/${tag}`);
        this.tags = response.data;
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    }
  }
};
</script>