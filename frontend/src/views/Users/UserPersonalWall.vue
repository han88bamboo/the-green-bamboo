<template>
  <NavBar />

  <!-- User Profile Header and Navigation (always visible) -->
  <div v-if="displayUserID && routeUsername" class="userprofile mt-5 mobile-mt-3">
    <div class="container text-start">
      <UserProfileHeader />
    </div>

    <br>
    
    <!-- User Profile Navigation -->
    <div class="container text-start">
      <UserProfileNavbar :userID="displayUserID" :username="routeUsername" />
    </div>
  </div>

  <!-- Loading -->
  <LoadingWithFunFact v-if="dataLoaded === false" />

  <!-- Error -->
  <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="dataLoaded == null">
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
  <div v-if="dataLoaded" class="userprofile mt-5 mobile-mt-3">
    <div class="container text-start">
      <div class="row mobile-px-3">
        <div class="col-12 col-md-10 mx-auto mobile-px-3">

          <!-- Page Header -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h4 class="fw-bold mb-0">Personal Wall</h4>
          </div>

          <!-- Write Post Section (only for profile owner) -->
          <div v-if="ownProfile" class="mb-4">
            <div 
              class="d-flex align-items-center gap-3 p-3"
              style="
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: #ffffff;
              "
            >
              <img 
                :src="displayUser.photo || defaultProfilePhoto" 
                alt="Profile" 
                class="rounded-circle"
                style="width: 40px; height: 40px; object-fit: cover;"
              />
              <input 
                type="text" 
                class="form-control"
                placeholder="What's on your mind?"
                style="border-radius: 20px; background-color: #f0f2f5;"
                disabled
              />
              <button 
                class="btn fw-bold primary-btn-less-round-blue"
                style="white-space: nowrap;"
                disabled
              >
                + Write Post
              </button>
            </div>
          </div>

          <!-- Wall Content Placeholder -->
          <div 
            class="text-center py-5"
            style="
              border: 1px solid #e0e0e0;
              border-radius: 8px;
              background-color: #ffffff;
            "
          >
            <i class="bi bi-chat-square-text" style="font-size: 4rem; color: #6c757d;"></i>
            <h5 class="mt-3 text-muted">Personal Wall content coming soon...</h5>
            <p class="text-muted">
              Stay tuned! You'll be able to share updates and connect with friends here.
            </p>
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
  name: "UserPersonalWall",
  components: { 
    NavBar, 
    LoadingWithFunFact, 
    UserProfileHeader, 
    UserProfileNavbar 
  },
  data() {
    return {
      dataLoaded: false,

      // Default images
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",

      // User data
      displayUserID: null,
      routeUsername: null,
      displayUser: {},
      
      // Current user data
      userID: null,
      ownProfile: false,
    };
  },
  async mounted() {
    // Get current user info from localStorage
    const accID = localStorage.getItem("88B_accID");
    if (accID !== null) {
      this.userID = accID;
    }

    // Get route parameters
    this.displayUserID = parseInt(this.$route.params.userID);
    this.routeUsername = this.$route.params.username;

    // Check if viewing own profile
    if (this.displayUserID === parseInt(this.userID)) {
      this.ownProfile = true;
    }

    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        this.dataLoaded = false;

        await this.getDisplayUserProfile();

        this.dataLoaded = true;
      } catch (error) {
        console.error("Error loading data:", error);
        this.dataLoaded = null;
      }
    },

    async getDisplayUserProfile() {
      const response = await this.$axios.get(
        `${process.env.VUE_APP_API_URL}/getData/getUser/${this.displayUserID}`
      );
      this.displayUser = response.data;
    },
  }
};
</script>

<style scoped>
/* Mobile responsiveness */
@media (max-width: 768px) {
  .mobile-mt-3 {
    margin-top: 1rem !important;
  }
  
  .mobile-px-3 {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
  }
}

/* Write post input styling */
.form-control:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}
</style>
