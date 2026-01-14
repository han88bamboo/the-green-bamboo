<template>
  <div class="profile-navbar-container">
    <nav class="profile-navbar">
      <router-link
        :to="`/profile/user/${userID}/${username}`"
        class="profile-nav-link"
        :class="{ active: isProfileActive }"
      >
        Profile
      </router-link>
     
      <router-link
        :to="`/profile/user/${userID}/${username}/allreviews`"
        class="profile-nav-link"
        exact
      >
        Reviews
      </router-link>
      <router-link
        v-if="ownProfile"
        :to="`/profile/user/${userID}/${username}/activity`"
        class="profile-nav-link"
        exact
      >
        Activity
      </router-link>

      <router-link
        :to="cellarRoute"
        class="profile-nav-link"
        exact
      >
        Cellar
      </router-link>

      <router-link
        :to="`/profile/user/${userID}/${username}/stories`"
        class="profile-nav-link"
        exact
      >
        Stories
      </router-link>
     
        <router-link
        :to="`/profile/user/${userID}/${username}/lists`"
        class="profile-nav-link"
        exact
      >
        Lists
      </router-link>

      <router-link
        v-if="ownProfile"
        :to="`/dashboard/user/${userID}`" 
        class="profile-nav-link"
        exact
      >
        Drink Stats
      </router-link>

      <router-link
        :to="`/profile/user/${userID}/${username}/badges`" 
        class="profile-nav-link"
        exact
      >
        Badges
      </router-link>
       <router-link
        :to="`/profile/user/${userID}/${username}/allfollowingfollowers`"
        class="profile-nav-link"
        exact
      >
        Friends
      </router-link>

    </nav>
  </div>
</template>

<script>
export default {
  name: "UserProfileNavbar",
  props: {
    userID: {
      type: [String, Number],
      required: true
    },
    username: {
      type: String,
      required: true
    }
  },
  computed: {
    ownProfile() {
      // Determine ownership by comparing the displayed userID with the logged-in account ID
      const accID = localStorage.getItem('88B_accID');
      return String(this.userID) === String(accID);
    },
    isProfileActive() {
      // Match profileUser route exactly, excluding stories, allreviews and allfollowingfollowers
      const path = this.$route.path;
      const basePath = `/profile/user/${this.userID}/${this.username}`;
      return path === basePath || 
             (path.startsWith(basePath) && 
              !path.includes('/cellar-preview') &&
              !path.includes('/stories') &&
              !path.includes('/allreviews') && 
              !path.includes('/activity') && 
              !path.includes('/lists') && 
              !path.includes('/badges') && 
              !path.includes('/allfollowingfollowers'));
    },
    cellarRoute() {
    return this.ownProfile
      ? `/my-cellar/user/${this.userID}/${this.username}`
      : `/profile/user/${this.userID}/${this.username}/cellar-preview`
    }
  }
};
</script>

<style scoped>
.profile-navbar-container {
  width: 100%;
  background-color: #83a9e8;
}

.profile-navbar {
  display: flex;
  flex-wrap: nowrap;          /* never wrap to a second line */
  white-space: nowrap;        /* keep text in one line */
  overflow-x: auto;           /* enable horizontal scrolling */
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch; /* smooth iOS scrolling */
  justify-content: center;
  padding: 0.1rem 0.5rem;
  margin: 0 auto;
  gap: 0;
}

.profile-navbar::-webkit-scrollbar {
  display: none;              /* Chrome/Safari */
}

.profile-nav-link {
  padding: 0.5rem 0.7rem;
  color: white;
  text-decoration: none;
  transition: all 0.2s;
  border-bottom: 2px solid transparent;
  font-weight:bold;
}

.profile-nav-link:hover:not(.active):not(.router-link-active) {
  border-bottom-color: rgba(91, 66, 66, 0.5);
}

.profile-nav-link.active,
.profile-nav-link.router-link-active {
  color: #000;
  border-bottom-color: #000;
  background-color: transparent;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .profile-nav-link {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
  
  .profile-navbar {
    justify-content: flex-start;
  }
}
</style>
