<template>
  <NavBar />

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
      <!-- User Profile Header -->
      <UserProfileHeader />

      <div class="row mobile-px-3">
        <div class="col-12 col-md-10 mx-auto px-2">
          <!-- Header Section -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
              <h3 class="mb-1 mobile-fs-5">
                <b>{{ displayUser.displayName || displayUser.username }}'s {{ currentView === 'following' ? 'Following' : 'Followers' }}</b>
              </h3>
              <p class="text-muted mb-0 mobile-rating-smaller-text-2">
                {{ totalUsers }} {{ currentView === 'following' ? 'following' : 'follower' }}{{ totalUsers !== 1 ? 's' : '' }} total
              </p>
            </div>
            <button
              class="mobile-view-hide btn btn-sm primary-btn"
              @click="$router.push(`/profile/user/${displayUserID}/${routeUsername}`)"
            >
              Back to Profile
            </button>
            <button
              class="mobile-view-show btn primary-btn btn-sm fw-bold"
              @click="$router.push(`/profile/user/${displayUserID}/${routeUsername}`)"
            >
              <i class="bi bi-arrow-return-left"></i>
            </button>
          </div>

          <!-- View Toggle -->
          <div class="d-flex justify-content-between mb-3">
            <!-- Following/Followers Toggle -->
            <div class="btn-group" role="group" aria-label="Following/Followers toggle">
              <button 
                type="button" 
                class="btn btn-outline-secondary mobile-rating-smaller-text-2"
                :class="{ active: currentView === 'following' }"
                @click="switchView('following')"
                title="Following"
              >
                Following ({{ followingCount }})
              </button>
              <button 
                type="button" 
                class="btn btn-outline-secondary mobile-rating-smaller-text-2"
                :class="{ active: currentView === 'followers' }"
                @click="switchView('followers')"
                title="Followers"
              >
                Followers ({{ followersCount }})
              </button>
            </div>
            
            <!-- Grid/List View Toggle -->
            <div class="btn-group" role="group" aria-label="View toggle">
              <button 
                type="button" 
                class="btn btn-outline-secondary"
                :class="{ active: viewMode === 'grid' }"
                @click="viewMode = 'grid'"
                title="Grid View"
              >
                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M1 2.5A1.5 1.5 0 0 1 2.5 1h3A1.5 1.5 0 0 1 7 2.5v3A1.5 1.5 0 0 1 5.5 7h-3A1.5 1.5 0 0 1 1 5.5v-3zm8 0A1.5 1.5 0 0 1 10.5 1h3A1.5 1.5 0 0 1 15 2.5v3A1.5 1.5 0 0 1 13.5 7h-3A1.5 1.5 0 0 1 9 5.5v-3zm-8 8A1.5 1.5 0 0 1 2.5 9h3A1.5 1.5 0 0 1 7 10.5v3A1.5 1.5 0 0 1 5.5 15h-3A1.5 1.5 0 0 1 1 13.5v-3zm8 0A1.5 1.5 0 0 1 10.5 9h3a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5h-3A1.5 1.5 0 0 1 9 13.5v-3z"/>
                </svg>
              </button>
              <button 
                type="button" 
                class="btn btn-outline-secondary"
                :class="{ active: viewMode === 'list' }"
                @click="viewMode = 'list'"
                title="List View"
              >
                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5z"/>
                </svg>
              </button>
            </div>
          </div>
          
          
          <!-- Filter and Sort Controls -->
          <div class="d-flex justify-content-between mb-4 gap-2">
            <div class="col-md-4">
              <label class="form-label mobile-rating-smaller-text-2">Search by Name:</label>
              <input 
                v-model="searchFilter" 
                @input="applyFilters" 
                class="form-control" 
                placeholder="Search by name, drinks, or flavours..."
              />
            </div>
            
            <div class="col-md-4">
              <label class="form-label mobile-rating-smaller-text-2">Sort by:</label>
              <select v-model="sortBy" @change="applyFilters" class="form-select">
                <option value="name">Name (A-Z)</option>
                <option value="name-desc">Name (Z-A)</option>
                <option value="join-date">Newest Members</option>
                <option value="join-date-desc">Oldest Members</option>
                <option value="reviews">Most Reviews</option>
                <option value="followers">Most Followers</option>
                <option value="points">Most Points</option>
                <option value="points-desc">Least Points</option>
              </select>
            </div>
            
          </div>

          <div class="offcanvas offcanvas-bottom d-md-none" tabindex="-1" id="sortSheet" style="max-height: 60vh;">
            <div class="offcanvas-header">
              <h6 class="offcanvas-title">Sort by</h6>
              <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
            </div>
            <div class="offcanvas-body">
              <div class="list-group">
                <label v-for="opt in sortOptions" :key="opt.value" class="list-group-item d-flex align-items-center gap-2">
                  <input class="form-check-input me-2" type="radio" name="sort" :value="opt.value" v-model="sortBy">
                  <span>{{ opt.label }}</span>
                </label>
              </div>
            </div>
            <div class="border-top p-3 d-flex justify-content-end bg-white">
              <button class="btn primary-btn" data-bs-dismiss="offcanvas" @click="applyFilters">Apply</button>
            </div>
          </div>

          <!-- Users List (List View) -->
          <div v-if="filteredUsers && filteredUsers.length > 0 && viewMode === 'list'">
            <div v-for="user in paginatedUsers" :key="user.id" class="mb-4">
              <div style="display: flex" class="row mb-2 border rounded p-3 user-card">
                <div class="col-3 mobile-col-3 mobile-pe-0">
                  <img
                    :src="user.photo || defaultUserImage"
                    alt=""
                    class="rounded user-img"
                  />
                </div>
                <div class="col-9 mobile-col-9 mobile-ps-2">
                  <a
                    :href="`/profile/user/${user.id}/${user.username}`"
                    style="text-decoration: none; color: #223957"
                  >
                    <p class="fs-5 mobile-fs-6 mb-1 mobile-mb-0_5 default-clickable-text">
                      <b>{{ user.displayName || user.username }}</b>
                    </p>
                  </a>
                  
                  <!-- Username if different from display name -->
                  <p class="text-muted small mb-2" v-if="user.displayName && user.displayName !== user.username">
                    @{{ user.username }}
                  </p>

                  <!-- User Stats -->
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    
                    <div class="d-flex align-items-center">
                      <p class="mb-2 small fw-bold" style="color: #f0b358;">
                        <i class="fas fa-wine-glass me-1"></i>{{ user.reviewCount || 0 }} reviews
                      </p>
                      <p class="mb-2 small fw-bold" style="color: #f0b358;">
                        <i class="fas fa-users me-1"></i>{{ user.followerCount || 0 }} followers
                      </p>
                    </div>
                  </div>

                  <!-- Points and Rank -->
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <div class="d-flex align-items-center">
                      <p class="text-muted small mb-0 me-3">
                        <i class="fas fa-trophy me-1"></i>{{ user.currentPoints || 0 }} proof points
                      </p>
                      <div v-if="user.proofRank" class="d-flex align-items-center">
                        <span class="badge" :style="{ backgroundColor: user.proofRank[1], color: '#fff' }">
                          {{ user.proofRank[0] }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <!-- Choice Drinks and Flavours -->
                  <div class="mb-2" v-if="user.choiceDrinks && user.choiceDrinks.length > 0">
                    <p class="small text-muted mb-1">Favourite Drinks:</p>
                    <div class="d-flex flex-wrap">
                      <span v-for="drink in user.choiceDrinks.slice(0, 5)" :key="drink" class="badge bg-secondary me-1 mb-1">
                        {{ drink }}
                      </span>
                      <span v-if="user.choiceDrinks.length > 5" class=" text-muted">
                        +{{ user.choiceDrinks.length - 5 }} more
                      </span>
                    </div>
                  </div>

                  <div class="mb-2" v-if="user.choiceFlavours && user.choiceFlavours.length > 0">
                    <p class="small text-muted mb-1">Favorite Flavours:</p>
                    <div class="d-flex flex-wrap">
                      <span v-for="flavour in user.choiceFlavours.slice(0, 5)" :key="flavour" class="badge bg-info me-1 mb-1">
                        {{ flavour }}
                      </span>
                      <span v-if="user.choiceFlavours.length > 5" class="small text-muted">
                        +{{ user.choiceFlavours.length - 5 }} more
                      </span>
                    </div>
                  </div>

                  <!-- Full name if available -->
                  <!-- <div class="mb-2" v-if="user.firstName || user.lastName">
                    <p class="small text-muted mb-0">
                      {{ [user.firstName, user.lastName].filter(Boolean).join(' ') }}
                    </p>
                  </div> -->
                  <p class="text-muted small mb-2">
                      Joined {{ formatDate(user.joinDate) }}
                    </p>
                  <!-- Action buttons -->
                  <div class="d-flex justify-content-between align-items-center">
                    
                    <button 
                      class="btn btn-sm primary-btn"
                      @click="visitProfile(user.id, user.username)"
                    >
                      View Profile
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Users Grid (Grid View) -->
          <div v-if="filteredUsers && filteredUsers.length > 0 && viewMode === 'grid'" class="row">
            <div v-for="user in paginatedUsers" :key="user.id" class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4">
              <div class="card h-100 user-card border-light">
                <!-- Image at top -->
                <div class="card-img-top-wrapper">
                  <img
                    :src="user.photo || defaultUserImage"
                    alt=""
                    class="card-img-top user-card-img"
                  />
                </div>
                
                <div class="card-body d-flex flex-column">
                  <!-- User name -->
                  <a
                    :href="`/profile/user/${user.id}/${user.username}`"
                    class="text-decoration-none"
                    style="color: #223957"
                  >
                    <h6 class="card-title mb-2 default-clickable-text fw-bold">
                      {{ user.displayName || user.username }}
                    </h6>
                  </a>
                  
                  <!-- Username if different -->
                  <p class="text-muted small mb-2" v-if="user.displayName && user.displayName !== user.username">
                    @{{ user.username }}
                  </p>
                  
                  <!-- Stats -->
                  <p class="mb-2 small fw-bold" style="color: #f0b358;">
                    {{ user.reviewCount || 0 }} reviews / {{ user.followerCount || 0 }} followers
                  </p>
                  
                  <!-- Points and Rank -->
                  <div class="mb-2">
                    <p class="mb-1 small text-muted">
                      <i class="fas fa-trophy me-1"></i>{{ user.currentPoints || 0 }} proof points
                    </p>
                    <div v-if="user.proofRank" class="mb-1">
                      <span class="badge " :style="{ backgroundColor: user.proofRank[1], color: '#fff' }">
                        {{ user.proofRank[0] }}
                      </span>
                    </div>
                  </div>

                  <!-- Choice Drinks -->
                  <div class="mb-2" v-if="user.choiceDrinks && user.choiceDrinks.length > 0">
                    <div class="d-flex flex-wrap">
                      <span v-for="drink in user.choiceDrinks.slice(0, 5)" :key="drink" class="badge bg-secondary me-1 mb-1">
                        {{ drink }}
                      </span>
                      <span v-if="user.choiceDrinks.length > 5" class=" text-muted">
                        +{{ user.choiceDrinks.length - 5 }} more
                      </span>
                    </div>
                  </div>
                  
                  
                  <!-- Bottom row: Join date and action -->
                  <div class="d-flex justify-content-between align-items-center mt-auto">
                    <small class="text-muted">
                      {{ formatDateGrid(user.joinDate) }}
                    </small>
                    <button 
                      class="btn btn-sm primary-btn"
                      @click="visitProfile(user.id, user.username)"
                    >
                      View Profile
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty state (standalone, not chained) -->
          <div
            v-if="dataLoaded && (!filteredUsers || filteredUsers.length === 0)"
            class="text-center py-5"
          >
            <h5 class="text-muted">No {{ currentView }} yet.</h5>
            <p class="text-muted">
              {{ displayUser.displayName || displayUser.username }}
              {{ currentView === 'following' ? "isn't following anyone yet" : "doesn't have any followers yet" }}.
            </p>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="d-flex justify-content-center mt-4">
            <nav aria-label="Users pagination">
              <ul class="pagination">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                  <button 
                    class="page-link" 
                    @click="changePage(currentPage - 1)"
                    :disabled="currentPage === 1"
                  >
                    Previous
                  </button>
                </li>
                <li 
                  v-for="page in visiblePages" 
                  :key="page" 
                  class="page-item" 
                  :class="{ active: page === currentPage }"
                >
                  <button class="page-link" @click="changePage(page)">
                    {{ page }}
                  </button>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                  <button 
                    class="page-link" 
                    @click="changePage(currentPage + 1)"
                    :disabled="currentPage === totalPages"
                  >
                    Next
                  </button>
                </li>
              </ul>
            </nav>
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

export default {
  name: "AllFollowingFollowers",
  components: {
    NavBar,
    LoadingWithFunFact,
    UserProfileHeader,
  },
  data() {
    return {
      dataLoaded: false,
      
      // Default images
      defaultUserImage: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
      
      // User data
      displayUserID: null,
      routeUsername: null,
      displayUser: {},
      
      // Users data
      allFollowing: [],
      allFollowers: [],
      filteredUsers: [],
      
      // Current view state
      currentView: 'following', // 'following' or 'followers'
      
      // Pagination
      currentPage: 1,
      usersPerPage: 20,
      totalUsers: 0,
      
      // Filtering and sorting
      searchFilter: '',
      sortBy: 'name',
      
      // View mode
      viewMode: 'grid', // Default to grid view
    };
  },
  computed: {
    sortOptions() {
      return [
        { value: 'name', label: 'Name (A–Z)' },
        { value: 'name-desc', label: 'Name (Z–A)' },
        { value: 'join-date', label: 'Newest Members' },
        { value: 'join-date-desc', label: 'Oldest Members' },
        { value: 'reviews', label: 'Most Reviews' },
        { value: 'followers', label: 'Most Followers' },
        { value: 'points', label: 'Most Points' },
        { value: 'points-desc', label: 'Least Points' },
      ];
    },
    followingCount() {
      return this.allFollowing.length;
    },
    
    followersCount() {
      return this.allFollowers.length;
    },
    
    paginatedUsers() {
      const start = (this.currentPage - 1) * this.usersPerPage;
      const end = start + this.usersPerPage;
      return this.filteredUsers.slice(start, end);
    },
    
    totalPages() {
      return Math.ceil(this.filteredUsers.length / this.usersPerPage);
    },
    
    visiblePages() {
      const pages = [];
      const maxVisible = 5;
      const start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2));
      const end = Math.min(this.totalPages, start + maxVisible - 1);
      
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    }
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
        
        // Load both following and followers data
        await Promise.all([
          this.loadAllFollowing(),
          this.loadAllFollowers()
        ]);
        
        // Set initial filtered users based on current view
        this.switchView(this.currentView);
        
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
    
    async loadAllFollowing() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getAllUserFollowing/${this.displayUserID}`
        );
        
        this.allFollowing = response.data.following || [];
      } catch (error) {
        console.error("Error loading following:", error);
        this.allFollowing = [];
      }
    },
    
    async loadAllFollowers() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getAllUserFollowers/${this.displayUserID}`
        );
        
        this.allFollowers = response.data.followers || [];
      } catch (error) {
        console.error("Error loading followers:", error);
        this.allFollowers = [];
      }
    },
    
    switchView(view) {
      this.currentView = view;
      
      if (view === 'following') {
        this.filteredUsers = [...this.allFollowing];
      } else {
        this.filteredUsers = [...this.allFollowers];
      }
      
      this.totalUsers = this.filteredUsers.length;
      this.currentPage = 1; // Reset to first page
      this.applyFilters();
    },
    
    applyFilters() {
      let filtered;
      
      // Start with the appropriate dataset
      if (this.currentView === 'following') {
        filtered = [...this.allFollowing];
      } else {
        filtered = [...this.allFollowers];
      }
      
      // Apply search filter
      if (this.searchFilter.trim()) {
        const searchTerm = this.searchFilter.toLowerCase();
        filtered = filtered.filter(user => {
          const displayName = (user.displayName || '').toLowerCase();
          const username = (user.username || '').toLowerCase();
          const firstName = (user.firstName || '').toLowerCase();
          const lastName = (user.lastName || '').toLowerCase();
          
          // Search in choice drinks and flavours
          const choiceDrinks = (user.choiceDrinks || []).join(' ').toLowerCase();
          const choiceFlavours = (user.choiceFlavours || []).join(' ').toLowerCase();
          
          return displayName.includes(searchTerm) || 
                 username.includes(searchTerm) ||
                 firstName.includes(searchTerm) ||
                 lastName.includes(searchTerm) ||
                 choiceDrinks.includes(searchTerm) ||
                 choiceFlavours.includes(searchTerm);
        });
      }
      
      // Apply sorting
      filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'name': {
            const nameA = (a.displayName || a.username || '').toLowerCase();
            const nameB = (b.displayName || b.username || '').toLowerCase();
            return nameA.localeCompare(nameB);
          }
          case 'name-desc': {
            const nameDescA = (a.displayName || a.username || '').toLowerCase();
            const nameDescB = (b.displayName || b.username || '').toLowerCase();
            return nameDescB.localeCompare(nameDescA);
          }
          case 'join-date':
            return new Date(b.joinDate) - new Date(a.joinDate);
          case 'join-date-desc':
            return new Date(a.joinDate) - new Date(b.joinDate);
          case 'reviews':
            return (b.reviewCount || 0) - (a.reviewCount || 0);
          case 'followers':
            return (b.followerCount || 0) - (a.followerCount || 0);
          case 'points':
            return (b.currentPoints || 0) - (a.currentPoints || 0);
          case 'points-desc':
            return (a.currentPoints || 0) - (b.currentPoints || 0);
          default:
            return 0;
        }
      });
      
      this.filteredUsers = filtered;
      this.currentPage = 1; // Reset to first page when filters change
    },
    
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        // Scroll to top of users section
        this.$nextTick(() => {
          const usersSection = document.querySelector('.userprofile');
          if (usersSection) {
            usersSection.scrollIntoView({ behavior: 'smooth' });
          }
        });
      }
    },
    
    visitProfile(userId, username) {
      this.$router.push(`/profile/user/${userId}/${username}`);
    },
    
    formatDate(dateString) {
      if (!dateString) return 'Unknown date';
      
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    
    formatDateGrid(dateString) {
      if (!dateString) return 'Unknown';
      
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      }).replace(/\//g, ' / '); // Add spaces around slashes
    }
  }
};
</script>

<style scoped>
.user-img {
  width: 100%;
  object-fit: cover;
}

.user-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.user-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.default-clickable-text:hover {
  text-decoration: underline !important;
}

.border {
  border-color: #e9ecef !important;
}

.border:hover {
  border-color: #dee2e6 !important;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.2s ease;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .mobile-col-3 {
    flex: 0 0 25%;
    max-width: 25%;
  }
  
  .mobile-col-9 {
    flex: 0 0 75%;
    max-width: 75%;
  }
  
  .mobile-pe-0 {
    padding-right: 0 !important;
  }
  
  .mobile-ps-2 {
    padding-left: 0.5rem !important;
  }
  
  .mobile-fs-6 {
    font-size: 1rem !important;
  }
  
  .mobile-mb-0_5 {
    margin-bottom: 0.25rem !important;
  }
  
  .mobile-mt-3 {
    margin-top: 1rem !important;
  }
}

.pagination .page-link {
  color: #223957;
  border-color: #dee2e6;
}

.pagination .page-item.active .page-link {
  background-color: #f0b358;
  border-color: #f0b358;
  color: #000;
}

.pagination .page-link:hover {
  color: #f0b358;
  background-color: #f8f9fa;
}

/* Grid view styles */
.card-img-top-wrapper {
  height: 150px;
  overflow: hidden;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-card-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
}

.card-body {
  padding: 1rem;
}

.card-title {
  font-size: 1rem;
  line-height: 1.3;
}

/* View toggle buttons */
.btn-group .btn.active {
  background-color: #f0b358;
  border-color: #f0b358;
  color: #000;
}

.btn-outline-secondary {
  color: #223957;
  border-color: #223957;
}

.btn-outline-secondary:hover {
  background-color: #f0b358;
  border-color: #f0b358;
  color: #000;
}

/* Badge styling */
.badge {
  padding: 0.25em 0.5em;
}

/* Choice drinks and flavours */
.badge.bg-secondary {
  background-color: #6c757d !important;
}

.badge.bg-info {
  background-color: #0dcaf0 !important;
}
</style>
