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
    isProfileActive() {
      // Match profileUser route exactly, excluding allreviews and allfollowingfollowers
      const path = this.$route.path;
      const basePath = `/profile/user/${this.userID}/${this.username}`;
      return path === basePath || 
             (path.startsWith(basePath) && 
              !path.includes('/allreviews') && 
              !path.includes('/allfollowingfollowers'));
    }
  }
};
</script>

<style scoped>
.profile-navbar-container {
  width: 100%;
  background-color: #6ba3d3;
  margin-bottom: 1.5rem;
}

.profile-navbar {
  display: flex;
  justify-content: flex-start;
  padding: 0.4rem 0.7rem;
  margin: 0 auto;
  gap: 0;
}

.profile-nav-link {
  padding: 0.1rem 0.7rem;
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
  border-bottom: 3px solid transparent;
}

.profile-nav-link:hover:not(.active):not(.router-link-active) {
  border-bottom-color: rgba(255, 255, 255, 0.5);
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
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }
}
</style>
