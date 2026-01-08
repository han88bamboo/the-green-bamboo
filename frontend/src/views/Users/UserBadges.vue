

<template>
  <NavBar />

  <!-- User Profile Header and Navigation (always visible) -->
  <div v-if="displayUserID && routeUsername" class="userprofile mt-5 mobile-mt-3">
    <div class="container text-start">
      <UserProfileHeader 
        :displayUserData="displayUser"
        :loggedInUserData="loggedInUser"
        :isOwnProfile="ownProfile"
      />
    </div>
    
    <br>
    
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
        <div class="col-12 col-lg-10 mx-auto mb-4 px-2">
          <!-- badges tab -->
                
                <div v-if="!userBadges || userBadges.length === 0" class="container  py-4">
                  <div class="text-muted text-center">
                    <i class="bi bi-trophy" style="font-size: 3rem;"></i>
                    <h5 class="mt-3">No Badges Unlocked Yet.</h5>
                    <p><router-link to="/badges-and-points" style="color: inherit; text-decoration: underline;">
                      Click here to find out how badges are earned on Drink-X.
                    </router-link></p>
                  </div>
                </div>
                
                <div v-else class="container">
                  <div class="row">
                    <!-- Display 4 badges per row -->
                    <div class="col-6 col-sm-4 col-md-3 mb-4" v-for="badge in userBadges" :key="badge.id">
                      <div class="badge-card text-center">
                        <!-- Badge image -->
                        <img 
                          :src="badge.badgePhoto || defaultProfilePhoto"
                          alt=""
                          class="rounded-circle-white-bg  badge-img mb-2"
                          style="width: 100px; height: 100px;"
                        />
                        
                        <!-- Badge name -->
                        <p class="badge-name mb-1 text-center">
                          <strong>{{ badge.badgeName }} <span style="white-space: nowrap;">(Lvl {{ badge.currentLevel }})</span></strong>
                        </p>
                        
                        <!-- Date acquired -->
                        <p class="badge-date text-muted small mb-2">{{ new Date(badge.dateEarned).toLocaleDateString() }}</p>
                        
                        <!-- Progress bar -->
                        <div v-if="badge.nextLevelRequirement" class="progress mb-1" style="height: 8px;">
                          <div 
                            class="progress-bar"
                            style="background-color: #3498db;" 
                            role="progressbar"
                            :style="{
                              width: badge.currentProgress >= badge.nextLevelRequirement 
                                ? '0%' 
                                : (badge.currentProgress / badge.nextLevelRequirement * 100) + '%'
                            }"
                            :aria-valuenow="badge.currentProgress"
                            aria-valuemin="0"
                            :aria-valuemax="badge.nextLevelRequirement"
                          ></div>
                        </div>
                        
                        <!-- Progress text -->
                        <p class="progress-text small mb-0" v-if="badge.nextLevelRequirement">
                          <span v-if="badge.currentProgress < badge.nextLevelRequirement">
                            <span v-if="badge.badgeType === 'Action'">
                              {{ badge.nextLevelRequirement - badge.currentProgress }} More Actions To<br>Reach The Next Level!
                            </span>
                            <span v-else>
                              {{ badge.nextLevelRequirement - badge.currentProgress }} More Reviews To<br>Reach The Next Level!
                            </span>
                          </span>
                          <span v-else>
                            Ready to Level Up!
                          </span>
                        </p>

                        <p class="progress-text small mb-0" v-else>Maximum level reached!</p>
                      </div>
                    </div>
                  </div>
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
      userID: null,
      displayUserID: null,
      routeUsername: null,
      displayUser: {},
      loggedInUser: null,
      ownProfile: false,
      userBadges: [],
      userBadgesLoaded: false,
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
    };
  },
  async mounted() {
    // Get route parameters
    this.displayUserID = parseInt(this.$route.params.userID);
    this.routeUsername = this.$route.params.username;
    
    // Get logged-in user ID from localStorage
    const accID = localStorage.getItem("88B_accID");
    if (accID !== null) {
      this.userID = accID;
    }
    
    // Check if viewing own profile
    this.ownProfile = (this.displayUserID == this.userID);
    
    // Get logged-in user data from localStorage (stored by UserProfileRefactor)
    const storedUser = localStorage.getItem("88B_loggedInUser");
    if (storedUser) {
      this.loggedInUser = JSON.parse(storedUser);
    }
    
    await this.loadData();
  },

  methods: {
    // Badges
    async getBadges() {
      // for Badges
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getBadges`
        );
        // const response = await this.$axios.get(`http://127.0.0.1:5000/getData/getBadges`);
        this.badges = response.data;
        this.badgesDataLoaded = true;
      } catch (error) {
        console.error(error);
        if (error.status === 404) {
          this.badgesDataLoaded = true;
        } else {
          this.badgesDataLoaded = false;
        }
      }
    },

    async getUserBadges() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUserBadges/${this.displayUserID}`
        );
        this.userBadges = response.data;
        this.userBadgesLoaded = true;
      } catch (error) {
        console.error("Error fetching user badges:", error);
        console.warn("getUserBadges failed for userID:", this.displayUserID, error);
        this.userBadgesLoaded = false;
      }
    },

    async loadData() {
      try {
        this.dataLoaded = false;
        
        // Load user profile
        await this.getDisplayUserProfile();

        // Ensure badges are loaded before rendering
        await Promise.all([
          this.getBadges(),
          this.getUserBadges()
        ]);
        
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