@ -0,0 +1,119 @@

<template>
  <NavBar />

  <!-- User Profile Header and Navigation (always visible) -->
  <div v-if="displayUserID && routeUsername" class="userprofile mt-5 mobile-mt-3">
    <div class="container text-start">
      <UserProfileHeader />
    </div>
    
    <!-- User Profile Navigation -->
    <div class="container text-start">
      <UserProfileNavbar :userID="displayUserID" :username="routeUsername" />
    </div>
  </div>

  <!-- Display when data is still loading -->
  <LoadingWithFunFact v-if="dataLoaded === false" />

  <!-- Display when data fails to load -->
  <div
    class="text-danger fst-italic fw-bold fs-3 pt-5"
    v-if="dataLoaded == null"
  >
    <span>An error occurred while loading this page, please try again!</span>
    <br />
    <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
      <span class="fs-5 fst-italic"> Return to previous page </span>
    </button>
    <router-link :to="'/'" class="mx-1">
      <button class="btn primary-btn btn-sm">
        <span class="fs-5 fst-italic"> Home </span>
      </button>
    </router-link>
  </div>

  <!-- Main Content -->
  <div
    v-if="dataLoaded"
    class="userprofile mt-5 mobile-mt-3"
  >
    <div class="container text-start">
      <div class="row mobile-px-3">
        <div class="col-12 col-md-10 mx-auto px-2">
          <!-- Placeholder Content -->
          <div class="text-center py-5">
            <h3 class="mb-3">{{ displayUser.displayName || displayUser.username }}'s Badges</h3>
            <p class="text-muted">Badges content coming soon...</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';
import UserProfileHeader from '@/components/UserProfileHeader.vue';
import UserProfileNavbar from '@/components/UserProfileNavbar.vue';

export default {
  name: "UserBadges",
  components: {
    NavBar,
    LoadingWithFunFact,
    UserProfileHeader,
    UserProfileNavbar,
  },
  data() {
    return {
      dataLoaded: false,
      
      // User data
      displayUserID: null,
      routeUsername: null,
      displayUser: {},
    };
  },
  async mounted() {
    // Get route parameters
    this.displayUserID = parseInt(this.$route.params.userID);
    this.routeUsername = this.$route.params.username;
    
    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        this.dataLoaded = false;
        
        // Load user profile
        await this.getDisplayUserProfile();
        
        this.dataLoaded = true;
      } catch (error) {
        console.error("Error loading data:", error);
        this.dataLoaded = null;
      }
    },
    
    async getDisplayUserProfile() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUser/${this.displayUserID}`
        );
        this.displayUser = response.data;
      } catch (error) {
        console.error("Error loading user profile:", error);
        throw error;
      }
    },
  }
};
</script>

<style scoped>
/* Add any custom styles here */
</style>