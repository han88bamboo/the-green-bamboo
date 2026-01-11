<template>
  <NavBar />
  
  <div class="container px-4 mt-4">
    <div class="container">
      <!-- Header with Search -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="row justify-content-left mb-2">
            <h3 class="text-start fw-bold mobile-fs-4">Assemblies: Your Drink Communities 🍷🥃🍺</h3>
            <h5 class="text-start fw-bold mobile-fs-6">Join conversations about wine, whisky, sake, and more...</h5>
          </div>

          <!-- ONE responsive row for BOTH controls -->
          <div class="row align-items-center g-2">
            <!-- Left: Functional controls -->
            <div class="col-12 col-md d-flex align-items-center justify-content-start gap-2 flex-wrap flex-md-nowrap">
              <div class="input-group search-compact" style="max-width: 400px;">
                <input
                  type="text"
                  class="form-control"
                  placeholder="Search assemblies"
                  v-model="searchTerm"
                  @input="filterAssemblies"
                />
                <button class="btn btn-outline-secondary" type="button">
                  <i class="bi bi-search"></i>
                </button>
              </div>

              <!-- TODO: Create Assembly button (admin only or proposal system) -->
              <button 
                v-if="userID && userID !== 'defaultUser'"
                class="btn primary-btn-less-round-blue fw-bold btn-md"
                @click="createAssembly"
              >
                Create Assembly
              </button>
            </div>

            <!-- Right: Sort options (only when there are assemblies) -->
            <div
              v-if="filteredAssemblies.length > 0"
              class="col-12 col-md d-flex justify-content-center justify-content-md-end mobile-mt-3"
            >
              <div class="btn-group btn-group-md" role="group">
                <button 
                    type="button" 
                    class="btn"
                    :class="sortBy === 'popular' ? 'btn-primary' : 'btn-outline-secondary'"
                    @click="setSortBy('popular')"
                  >
                    Most Popular
                  </button>
                  <button 
                    type="button" 
                    class="btn"
                    :class="sortBy === 'recent' ? 'btn-primary' : 'btn-outline-secondary'"
                    @click="setSortBy('recent')"
                  >
                    Most Recent
                  </button>
                  <button 
                    type="button" 
                    class="btn"
                    :class="sortBy === 'alphabetical' ? 'btn-primary' : 'btn-outline-secondary'"
                    @click="setSortBy('alphabetical')"
                  >
                    Alphabetical
                  </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3 text-muted">Loading assemblies...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <h4 class="alert-heading">Error Loading Assemblies</h4>
        <p>{{ error }}</p>
        <button class="btn btn-outline-danger" @click="loadAssemblies">Try Again</button>
      </div>

      <!-- Assemblies Grid -->
      <div v-else class="row g-4 mb-5">
        <div
          v-for="assembly in paginatedAssemblies"
          :key="assembly.id"
          class="col-12 col-md-6 col-lg-4"
        >
          <div class="card h-100 shadow-sm assembly-card">
            <!-- Assembly Preview Images (Pinterest-style grid from recent posts) -->
            <div class="card-img-top position-relative" style="height: 200px; overflow: hidden;">
              <div class="pin-grid" v-if="assembly.previewPosts && assembly.previewPosts.length > 0">
                <!-- Main image (larger) -->
                <div class="pin-cell pin-main">
                  <img
                    v-if="assembly.previewPosts[0] && assembly.previewPosts[0].photo"
                    :src="assembly.previewPosts[0].photo"
                    class="pin-img"
                    :alt="assembly.previewPosts[0].title || 'Post preview'"
                  />
                  <div v-else class="pin-placeholder bg-light">
                    <i class="bi bi-image text-muted" style="font-size: 2rem;"></i>
                  </div>
                </div>
                
                <!-- Side images -->
                <div class="pin-cell pin-side1">
                  <img
                    v-if="assembly.previewPosts[1] && assembly.previewPosts[1].photo"
                    :src="assembly.previewPosts[1].photo"
                    class="pin-img"
                    :alt="assembly.previewPosts[1].title || 'Post preview'"
                  />
                  <div v-else class="pin-placeholder bg-light"></div>
                </div>
                
                <div class="pin-cell pin-side2">
                  <img
                    v-if="assembly.previewPosts[2] && assembly.previewPosts[2].photo"
                    :src="assembly.previewPosts[2].photo"
                    class="pin-img"
                    :alt="assembly.previewPosts[2].title || 'Post preview'"
                  />
                  <div v-else class="pin-placeholder bg-light"></div>
                </div>
              </div>
              
              <!-- Default placeholder if no preview posts -->
              <div v-else class="d-flex align-items-center justify-content-center h-100 bg-light">
                <i class="bi bi-people text-muted" style="font-size: 3rem;"></i>
              </div>
            </div>

            <!-- Card Body -->
            <div class="card-body d-flex flex-column p-3">
              <!-- Assembly Name and Stats -->
              <div class="d-flex justify-content-between align-items-center mb-2">
                <a href="#" class="text-decoration-underline default-clickable-text" style="color: inherit;" @click.prevent="viewAssembly(assembly)">
                  <h5 class="card-title fw-bold mb-0 flex-grow-1 text-start">{{ assembly.assemblyName }}</h5>
                </a>
                <small class="text-muted ms-2">{{ assembly.totalMembers || 0 }} Member{{ assembly.totalMembers !== 1 ? 's' : '' }}</small>
              </div>

              <!-- Post Count -->
              <div class="mb-2 text-start">
                <small class="text-muted">
                  <i class="bi bi-chat-square-text me-1"></i>
                  {{ assembly.totalPosts || 0 }} Post{{ assembly.totalPosts !== 1 ? 's' : '' }}
                </small>
              </div>

              <!-- Creator Info -->
              <div class="mb-2">
                <div class="d-flex align-items-center justify-content-left ps-0">
                  <img
                    :src="assembly.creatorPhoto || defaultProfilePhoto"
                    alt="Creator"
                    class="rounded-circle me-2"
                    style="width: 24px; height: 24px; object-fit: cover;"
                  />
                  <span>Created by</span>
                  <a href="#" 
                    @click.prevent="goToCreatorProfile(assembly)"
                    class="default-clickable-text"
                    style="color: inherit;">
                    <span class="fw-bold ms-1">{{ assembly.creatorDisplayName || assembly.creatorUsername }}</span>
                  </a>
                </div>
              </div>

              <!-- Assembly Description -->
              <p class="card-text text-muted mb-3 description-text text-start">
                {{ assembly.assemblyDesc || '' }}
              </p>

              <!-- Action Buttons Row -->
              <div class="d-flex justify-content-between align-items-center mb-3 mt-auto">
                <!-- View Button (Left) -->
                <a
                  href="#"
                  class="btn btn-outline-secondary fw-semibold mobile-rating-smaller-text-2"
                  style="background-color: rgb(240, 68, 68); border-color: rgb(240, 68, 68); color: white;"
                  @click.prevent="viewAssembly(assembly)"
                >
                  View
                </a>

                <!-- Share Button (Right) -->
                <div class="d-flex gap-2">
                  <!-- Share Button -->
                  <button
                    class="btn btn-sm btn-outline-secondary d-flex align-items-center gap-1"
                    @click="shareAssembly(assembly)"
                    style="background-color: #f8f9fa; border-color: #dee2e6; color: #212529;"
                  >
                    <i class="bi bi-reply share-icon"></i>
                    <span>Share</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && filteredAssemblies.length === 0" class="text-center py-5">
        <i class="bi bi-search text-muted mb-3" style="font-size: 4rem;"></i>
        <h4 class="text-muted">No assemblies found</h4>
        <p class="text-muted">Try adjusting your search criteria or check back later for new assemblies.</p>
      </div>

      <!-- Show More Button -->
      <div v-if="!loading && hasMore && filteredAssemblies.length > 0" class="text-center mt-4 mb-5">
        <button class="btn btn-warning" @click="loadMore">
          Show More
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import { useToast } from "vue-toastification";

export default {
  name: "BrowseAssemblies",
  components: {
    NavBar,
  },
  data() {
    return {
      // Assemblies data
      assemblies: [],
      filteredAssemblies: [],
      
      // UI State
      loading: true,
      error: null,
      searchTerm: '',
      sortBy: 'popular',
      currentPage: 1,
      itemsPerPage: 12,
      hasMore: true, // Track if more assemblies available
      searchTimeout: null, // For debouncing search
      
      // User State
      userID: "defaultUser",
      userType: null,
      username: null,
      
      // Default images
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
    };
  },
  computed: {
    paginatedAssemblies() {
      // Return all filtered assemblies - pagination is handled by backend
      return this.filteredAssemblies;
    },
  },
  mounted() {
    // Get user info from localStorage
    const accID = localStorage.getItem("88B_accID");
    if (accID !== null) {
      this.userID = accID;
    }
    // If no accID, userID remains "defaultUser"
    
    this.userType = localStorage.getItem("88B_accType");
    this.username = localStorage.getItem("88B_accUsername");
    
    // Load assemblies
    this.loadAssemblies();
  },
  methods: {
    async loadAssemblies() {
      this.loading = true;
      this.error = null;
      
      try {
        let response;
        const offset = (this.currentPage - 1) * this.itemsPerPage;
        
        if (this.searchTerm.trim()) {
          // Use search endpoint
          response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/assembly/getAssemblywSearch/${offset}/${encodeURIComponent(this.searchTerm.trim())}`
          );
        } else {
          // Use regular get endpoint
          response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/assembly/getAssemblies/${offset}`
          );
        }
        
        if (response.data.code === 200) {
          const newAssemblies = response.data.data;
          
          if (this.currentPage === 1) {
            this.assemblies = newAssemblies;
          } else {
            // Append for "load more"
            this.assemblies = [...this.assemblies, ...newAssemblies];
          }
          
          // Check if there are more to load
          this.hasMore = newAssemblies.length === this.itemsPerPage;
          
          this.filteredAssemblies = [...this.assemblies];
          this.applySorting();
        } else {
          this.error = response.data.message || 'Failed to load assemblies.';
        }
      } catch (error) {
        console.error('Error loading assemblies:', error);
        this.error = 'Failed to load assemblies. Please try again later.';
      } finally {
        this.loading = false;
      }
    },

    viewAssembly(assembly) {
      const normalizedName = this.normalizeForUrl(assembly.assemblyName);
      this.$router.push({
        name: 'specificAssembly',
        params: {
          assemblyId: assembly.id,
          assemblyName: normalizedName
        }
      });
    },

    goToCreatorProfile(assembly) {
      // Navigate to creator profile based on createdByType
      if (assembly.createdByType === 'user') {
        this.$router.push(`/profile/user/${assembly.createdByID}/${assembly.creatorUsername}`);
      } else if (assembly.createdByType === 'venue') {
        this.$router.push(`/profile/venue/${assembly.createdByID}/${assembly.creatorUsername}`);
      } else if (assembly.createdByType === 'producer') {
        this.$router.push(`/profile/producer/${assembly.createdByID}/${assembly.creatorUsername}`);
      }
    },

    createAssembly() {
      // Navigate to the Create Assembly page
      this.$router.push('/assemblies/create');
    },

    // Debounced search - triggers API call after user stops typing
    filterAssemblies() {
      // Clear existing timeout
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout);
      }
      
      // Debounce the search - wait 300ms after user stops typing
      this.searchTimeout = setTimeout(() => {
        this.currentPage = 1;
        this.loadAssemblies();
      }, 300);
    },

    // Apply client-side sorting to already-fetched data
    applySorting() {
      let sorted = [...this.filteredAssemblies];
      
      sorted.sort((a, b) => {
        switch (this.sortBy) {
          case 'popular':
            return (b.totalMembers || 0) - (a.totalMembers || 0);
          case 'alphabetical':
            return a.assemblyName.localeCompare(b.assemblyName);
          case 'recent':
          default:
            return new Date(b.dateCreated) - new Date(a.dateCreated);
        }
      });
      
      this.filteredAssemblies = sorted;
    },

    setSortBy(sortBy) {
      this.sortBy = sortBy;
      this.applySorting();
    },

    loadMore() {
      this.currentPage++;
      this.loadAssemblies();
    },

    shareAssembly(assembly) {
      const normalizedName = this.normalizeForUrl(assembly.assemblyName);
      const shareUrl = `${window.location.origin}/assemblies/${assembly.id}/${normalizedName}`;
      
      navigator.clipboard.writeText(shareUrl).then(() => {
        const toast = useToast();
        toast.success('Assembly link copied to clipboard!');
      }).catch((err) => {
        console.error('Failed to copy text: ', err);
        const toast = useToast();
        toast.error('Failed to copy link.');
      });
    },

    normalizeForUrl(text) {
      return text
        // Remove emojis
        .replace(/[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F1E0}-\u{1F1FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]|[\u{1F900}-\u{1F9FF}]|[\u{1F018}-\u{1F270}]/gu, '')
        .trim()
        .replace(/\s+/g, ' ')
        .replace(/\s/g, '-')
        .replace(/[^\w-]/g, '')
        .replace(/-+/g, '-')
        .replace(/^-|-$/g, '')
        .toLowerCase();
    },

    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },
  },
};
</script>

<style scoped>
.assembly-card {
  transition: transform 0.2s ease-in-out;
}

.assembly-card:hover {
  transform: translateY(-2px) scale(1.01);
}

.pin-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 4px;
  height: 100%;
  width: 100%;
}

.pin-cell {
  overflow: hidden;
  border-radius: 4px;
}

.pin-main {
  grid-column: 1;
  grid-row: 1 / 3;
}

.pin-side1 {
  grid-column: 2;
  grid-row: 1;
}

.pin-side2 {
  grid-column: 2;
  grid-row: 2;
}

.pin-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pin-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  color: #6c757d;
}

.description-text {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
  max-height: 2.8em;
}

/* Let the search NOT take full width on mobile */
.search-compact {
  flex: 0 1 70%;
  max-width: 70%;
}

.search-compact .form-control {
  min-width: 0;
}

@media (min-width: 768px) {
  .search-compact {
    flex: 0 0 400px;
    max-width: 400px;
  }
}
</style>