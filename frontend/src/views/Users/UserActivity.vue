@ -0,0 +1,118 @@
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
    class="userprofile mt-4"
  >
    <div class="container text-start">
        <div class="col-11 mx-auto">
          <!-- Placeholder Content -->
            <!-- My Recent ACtivity -->
                <div>
                    <div class="square-inline">
                        <p class="fw-bold text-start my-2">Your Recent Activity</p>
                    </div>
                    <div class="feed-body pb-2">
                        <!-- Loading State -->
                        <div v-if="loadingRecentUserActivity" class="text-center pb-2">
                            <div class="spinner-border spinner-border-sm text-dark me-2" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <span class="text-muted">Loading recent activity...</span>
                        </div>

                        <!-- Error State -->
                        <div v-else-if="errorRecentUserActivity" class="text-center pb-1">
                            <div class="text-danger">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                {{ errorRecentUserActivity }}
                            </div>
                        </div>

                        <!-- Empty State -->
                        <div v-else-if="!recentUserActivity || recentUserActivity.length === 0" class="pb-1">
                            No recent activity.
                        </div>

                        <!-- Activity List -->
                        <div v-else class="overflow-auto" style="max-height: 100%;">
                            <div v-for="activity in recentUserActivity" :key="activity.id || activity.date" class="pb-2">
                                <!-- Your Activity -->
                                <div v-if="activity.type === 'review'">
                                    You rated <b><router-link :to="listingUrl(activity)" class="primary-clickable-text" style="color: rgb(2, 117, 98)"><u>{{ activity.listingName }}</u></router-link> <span style="color: rgb(2, 117, 98)">{{ activity.rating }} stars</span></b> {{ getTimeDifference(activity.date) }}
                                </div>
                                <div v-else-if="activity.type === 'list_add'">
                                    You added <b><router-link :to="listingUrl(activity)" class="primary-clickable-text" style="color: rgb(2, 117, 98)"><u>{{ activity.listingName }}</u></router-link></b> to your list: <b><router-link :to="listUrl(activity)" class="primary-clickable-text"><u><span style="color: rgb(2, 117, 98);">{{ activity.listName }}</span></u></router-link></b><br />{{ getTimeDifference(activity.date) }}
                                </div>
                                <div v-if="activity.type === 'follow'">
                                    You started following
                                    <router-link :to="profileUrl(activity)" class="reverse-clickable-text" style="color: rgb(2, 117, 98)">
                                      @<b>{{ activity.username }}</b>
                                    </router-link>
                                    {{ getTimeDifference(activity.date) }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <div class="square-inline">
                        <p class="fw-bold text-start mt-3">Recent Activity on Your Reviews</p>
                    </div>
                    <div class="feed-body  pb-2">
                        <!-- Loading State -->
                        <div v-if="loadingRecentReviewsActivity" class="text-center pb-1">
                            <div class="spinner-border spinner-border-sm text-dark me-2" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <span class="text-muted fst-italic">Loading recent activity...</span>
                        </div>

                        <!-- Error State -->
                        <div v-else-if="errorRecentReviewsActivity" class="text-center pb-1">
                            <div class="text-danger">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                {{ errorRecentReviewsActivity }}
                            </div>
                        </div>

                        <!-- Empty State -->
                        <div v-else-if="!recentReviewsActivity || recentReviewsActivity.length === 0" class="pb-1">
                            No recent activity.
                        </div>

                        <!-- Activity List -->
                        <div v-else class="overflow-auto" style="max-height: 100%;">
                            <div v-for="activity in recentReviewsActivity" :key="activity.id || activity.date" class="pb-2">
                                <!-- Activity on Your Reviews -->
                                <div v-if="activity.type === 'upvote' || activity.type === 'downvote'">
                                    <router-link :to="profileUrl(activity)" class="primary-clickable-text" style="color: rgb(2, 117, 98)">@<b>{{ activity.username }}</b></router-link> <span :style="{ color: activity.type === 'upvote' ? '#90ee90' : 'black' }">{{ activity.type }}d</span> your review of <router-link :to="listingUrl(activity, activity.reviewTarget)" class="clickable-text" style="color: rgb(2, 117, 98)"><u>{{ activity.listingName }}</u></router-link> {{ getTimeDifference(activity.date) }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <div class="square-inline pb-2">
                        <p class="fw-bold text-start">Recent Activity from Your Followers</p>
                    </div>
                    <div class="feed-body pb-5">
                        <!-- Loading State -->
                        <div v-if="loadingRecentFollowersActivity" class="text-center pb-1">
                            <div class="spinner-border spinner-border-sm text-dark me-2" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <span class="text-muted">Loading recent activity...</span>
                        </div>

                        <!-- Error State -->
                        <div v-else-if="errorRecentFollowersActivity" class="text-center pb-1">
                            <div class="text-danger">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                {{ errorRecentFollowersActivity }}
                            </div>
                        </div>

                        <!-- Empty State -->
                        <div v-else-if="!recentFollowersActivity || recentFollowersActivity.length === 0" class="pb-1">
                            No recent activity.
                        </div>

                        <!-- Activity List -->
                        <div v-else class="overflow-auto" style="max-height: 100%;">
                            <div v-for="activity in recentFollowersActivity" :key="activity.id || activity.date" class="pb-2">
                                <!-- Follower Activity -->
                                <div v-if="activity.type === 'follow'">
                                    <router-link :to="profileUrl(activity)" class="primary-clickable-text" style="color: rgb(2, 117, 98)">@<b>{{ activity.username }}</b></router-link> started following you {{ getTimeDifference(activity.date) }}
                                </div>
                                <div v-else-if="activity.type === 'tag'">
                                    <router-link :to="profileUrl(activity)" class="primary-clickable-text" style="color: rgb(2, 117, 98)">@<b>{{ activity.username }}</b></router-link> tagged you in a review of <router-link :to="listingUrl(activity)" class="primary-clickable-text" style="color: rgb(2, 117, 98)"><u>{{ activity.listingName }}</u></router-link> {{ getTimeDifference(activity.date) }}
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
  name: "UserActivity",
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

      // Recent Activity information
      recentUserActivity: [],
      recentReviewsActivity: [],
      recentFollowersActivity: [],
      loadingRecentUserActivity: false,
      loadingRecentReviewsActivity: false,
      loadingRecentFollowersActivity: false,
      errorRecentUserActivity: null,
      errorRecentReviewsActivity: null,
      errorRecentFollowersActivity: null,
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

        // Load recent activity sections
        await Promise.all([
          this.getRecentUserActivity(),
          this.getRecentReviewsActivity(),
          this.getRecentFollowersActivity()
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
  
      async getRecentUserActivity() {
      this.loadingRecentUserActivity = true;
      this.errorRecentUserActivity = null;
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getRecentUserActivity/${this.displayUserID}`
        );
        this.recentUserActivity = response.data;
      } catch (error) {
        console.error("Error fetching recent user activity:", error);
        this.errorRecentUserActivity = "Failed to load recent user activity.";
      } finally {
        this.loadingRecentUserActivity = false;
      }
    },

    async getRecentReviewsActivity() {
      this.loadingRecentReviewsActivity = true;
      this.errorRecentReviewsActivity = null;
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getRecentReviewsActivity/${this.displayUserID}`
        );
        this.recentReviewsActivity = response.data;
      } catch (error) {
        console.error("Error fetching recent reviews activity:", error);
        this.errorRecentReviewsActivity = "Failed to load recent reviews activity.";
      } finally {
        this.loadingRecentReviewsActivity = false;
      }
    },

    async getRecentFollowersActivity() {
      this.loadingRecentFollowersActivity = true;
      this.errorRecentFollowersActivity = null;
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getRecentFollowersActivity/${this.displayUserID}`
        );
        this.recentFollowersActivity = response.data;
      } catch (error) {
        console.error("Error fetching recent followers activity:", error);
        this.errorRecentFollowersActivity = "Failed to load recent followers activity.";
      } finally {
        this.loadingRecentFollowersActivity = false;
      }
    },

    // Helper methods (copied from UserProfileRefactor)
    slugify(text) {
      if (!text) return '';
      return text
        .toString()
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/\s+/g, '-')
        .replace(/[^\w]/g, '');
    },

    getTimeDifference(date) { 
        const now = new Date();
        const target = new Date(date);
        const diffMs = now - target;
        if (isNaN(target.getTime())) return '';
        if (diffMs < 0) return 'in the future';
        const intervals = [
            { unit: 'year', ms: 365.25 * 24 * 60 * 60 * 1000 },
            { unit: 'month', ms: 30.44 * 24 * 60 * 60 * 1000 },
            { unit: 'day', ms: 24 * 60 * 60 * 1000 },
            { unit: 'hour', ms: 60 * 60 * 1000 },
            { unit: 'minute', ms: 60 * 1000 },
            { unit: 'second', ms: 1000 }
        ];
        for (const { unit, ms } of intervals) {
            const value = Math.floor(diffMs / ms);
            if (value > 0) return `${value} ${unit}${value === 1 ? '' : 's'} ago`;
        }
        return 'just now';
    },

    listingUrl(activity, idOverride = null) {
        const id = idOverride || activity.listingID || activity.reviewTarget || activity.listingID;
        return `/listing/view/${id}/${this.slugify(activity.listingName)}`;
    },

    listUrl(activity) {
        return `/profile/user/${this.displayUserID}/${this.slugify(activity.listName)}`;
    },

    profileUrl(activity) {
        return `/profile/user/${activity.userID || activity.followingUserID}/${this.slugify(activity.username)}`;
    },

  }
};
</script>

<style scoped>
/* Add any custom styles here */
</style>