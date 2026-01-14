<!-- 
  =====================================================================================
  BrowseStoryNewsletters.vue - Browse All Story Newsletters
  =====================================================================================
  Purpose: Display all newsletters in a browsable grid format with search and filtering.
           Similar to BrowseAssemblies.vue structure.
  
  Route: /stories/newsletters
  
  Features:
  - Search bar for filtering newsletters by name
  - Grid of newsletter cards showing cover images
  - Sort by most recent / alphabetical / most subscribers (server-side)
  - Create Newsletter button (for any logged-in user)
  - Pagination with "Load More" button
  
  Backend Endpoints Used:
  - GET /stories/getNewsletters/<offset>?sortBy=X&userID=Y&userType=Z - Get paginated list
  - GET /stories/getNewsletterswSearch/<offset>/<search>?sortBy=X&userID=Y&userType=Z - Search
  
  Related Files:
  - backend/scripts/stories.py - Backend API endpoints
  - frontend/src/router/modules/story.js - Route registration
  - frontend/src/views/BrowseAssemblies.vue - Reference for structure/styling
  - frontend/src/views/SpecificStoryNewsletter.vue - Individual newsletter page
  - frontend/src/views/CreateNewsletter.vue - Create newsletter form
  
  Database Tables:
  - newsletters
  - newsletterPatrons (subscribers)
  - stories
  =====================================================================================
-->
<template>
  <NavBar />
  
  <div class="container px-4 py-5">
    <!-- Page Header -->
    <div class="row mb-4">
      <div class="col-12 text-center">
        <h1 class="fw-bold mb-2">
          <i class="bi bi-envelope-paper-fill text-primary me-2"></i>
          Story Newsletters
        </h1>
        <p class="text-muted">Subscribe to newsletters and get stories delivered to your inbox</p>
      </div>
    </div>

    <!-- Search and Actions Bar -->
    <div class="row mb-4">
      <div class="col-md-6 mx-auto">
        <div class="input-group">
          <span class="input-group-text bg-white">
            <i class="bi bi-search"></i>
          </span>
          <input 
            type="text" 
            class="form-control" 
            placeholder="Search newsletters..."
            v-model="searchQuery"
            @input="handleSearch"
          />
          <button 
            v-if="searchQuery" 
            class="btn btn-outline-secondary" 
            @click="clearSearch"
          >
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Actions Row -->
    <div class="row mb-4">
      <div class="col-12 d-flex justify-content-between align-items-center flex-wrap gap-2">
        <!-- Sort Options -->
        <div class="sort-options d-flex align-items-center gap-2">
          <span class="text-muted small">Sort by:</span>
          <button 
            class="btn btn-sm"
            :class="sortBy === 'recent' ? 'btn-dark' : 'btn-outline-secondary'"
            @click="sortBy = 'recent'; loadNewsletters()"
          >
            <i class="bi bi-clock-history me-1"></i> Recent
          </button>
          <button 
            class="btn btn-sm"
            :class="sortBy === 'alphabetical' ? 'btn-dark' : 'btn-outline-secondary'"
            @click="sortBy = 'alphabetical'; loadNewsletters()"
          >
            <i class="bi bi-sort-alpha-down me-1"></i> A-Z
          </button>
          <button 
            class="btn btn-sm"
            :class="sortBy === 'subscribers' ? 'btn-dark' : 'btn-outline-secondary'"
            @click="sortBy = 'subscribers'; loadNewsletters()"
          >
            <i class="bi bi-people me-1"></i> Subscribers
          </button>
        </div>

        <!-- Create Newsletter Button -->
        <router-link 
          v-if="userID !== 'defaultUser'"
          to="/stories/newsletters/create" 
          class="btn btn-primary fw-bold"
        >
          <i class="bi bi-plus-circle me-1"></i> Create Newsletter
        </router-link>
        <router-link 
          v-else
          to="/login" 
          class="btn btn-outline-primary fw-bold"
        >
          <i class="bi bi-box-arrow-in-right me-1"></i> Login to Create
        </router-link>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading newsletters...</p>
    </div>

    <!-- Newsletters Grid -->
    <div v-else>
      <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        <!-- Newsletter Card -->
        <!-- TODO: Implement newsletter cards with cover image, title, description, subscriber count -->
        <div 
          v-for="newsletter in newsletters" 
          :key="newsletter.id"
          class="col"
        >
          <div 
            class="card h-100 newsletter-card shadow-sm"
            @click="goToNewsletter(newsletter)"
          >
            <!-- Newsletter Cover Image -->
            <div class="newsletter-cover" :style="getCoverStyle(newsletter)">
              <div class="cover-overlay d-flex align-items-end p-3">
                <!-- Newsletter Title on Image -->
                <div class="text-white">
                  <h5 class="fw-bold mb-0">{{ newsletter.newsletterName }}</h5>
                </div>
              </div>
            </div>
            
            <div class="card-body">
              <!-- Description -->
              <p class="text-start card-text small text-muted mb-2">
                {{ truncateText(newsletter.newsletterDesc, 120) || 'No description' }}
              </p>
              
              <!-- Creator Info -->
              <div class="d-flex align-items-center mb-2">
                <img 
                  :src="newsletter.creatorPhoto || defaultProfilePhoto" 
                  alt="Creator"
                  class="rounded-circle me-2"
                  style="width: 24px; height: 24px; object-fit: cover;"
                />
                <small class="text-muted">
                  By {{ newsletter.creatorUsername || 'Unknown' }}
                </small>
              </div>
              
              <!-- Stats -->
              <div class="d-flex gap-3 small text-muted">
                <span>
                  <i class="bi bi-people-fill me-1"></i>
                  {{ newsletter.subscriberCount || 0 }} subscribers
                </span>
                <span>
                  <i class="bi bi-journal-richtext me-1"></i>
                  {{ newsletter.storyCount || 0 }} stories
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="newsletters.length === 0 && !loading" class="text-center py-5">
        <i class="bi bi-envelope-paper text-muted" style="font-size: 4rem;"></i>
        <h4 class="text-muted mt-3">
          {{ searchQuery ? 'No newsletters match your search' : 'No newsletters yet' }}
        </h4>
        <p class="text-muted">
          {{ searchQuery ? 'Try a different search term' : 'Be the first to create a newsletter!' }}
        </p>
        <router-link 
          v-if="userID !== 'defaultUser' && !searchQuery"
          to="/stories/newsletters/create" 
          class="btn btn-primary mt-2 fw-bold"
        >
          <i class="bi bi-plus-circle me-1"></i> Create Newsletter
        </router-link>
      </div>

      <!-- Load More Button -->
      <div v-if="hasMore && newsletters.length > 0" class="text-center mt-5 mb-4">
        <button 
          class="btn btn-outline-primary btn-lg px-5" 
          @click="loadMore"
          :disabled="loadingMore"
        >
          <span v-if="loadingMore">
            <span class="spinner-border spinner-border-sm me-2"></span>
            Loading...
          </span>
          <span v-else>Load More Newsletters</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";

export default {
  name: "BrowseStoryNewsletters",
  components: {
    NavBar,
  },
  data() {
    return {
      // User Info
      userID: "defaultUser",
      userType: null,
      
      // Newsletters
      newsletters: [],
      loading: true,
      loadingMore: false,
      hasMore: false,
      currentOffset: 0,
      
      // Search & Sort
      searchQuery: "",
      searchTimeout: null,
      sortBy: "recent",
      
      // Default images
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
      defaultCoverImage: "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800",
    };
  },

  async mounted() {
    // Get user info
    const accID = localStorage.getItem("88B_accID");
    if (accID) {
      this.userID = accID;
    }
    
    const accType = localStorage.getItem("88B_accType");
    if (accType) {
      this.userType = accType;
    }

    await this.loadNewsletters();
  },

  methods: {
    async loadNewsletters() {
      this.loading = true;
      this.currentOffset = 0;
      
      try {
        // Build query params for sorting and isSubscribed check
        const params = new URLSearchParams();
        params.append('sortBy', this.sortBy);
        if (this.userID !== 'defaultUser' && this.userType) {
          params.append('userID', this.userID);
          params.append('userType', this.userType);
        }
        
        let url;
        if (this.searchQuery.trim()) {
          url = `${process.env.VUE_APP_API_URL}/stories/getNewsletterswSearch/${this.currentOffset}/${encodeURIComponent(this.searchQuery.trim())}?${params.toString()}`;
        } else {
          url = `${process.env.VUE_APP_API_URL}/stories/getNewsletters/${this.currentOffset}?${params.toString()}`;
        }
        
        const response = await this.$axios.get(url);
        
        if (response.data.code === 200) {
          this.newsletters = response.data.data || [];
          // Check if there might be more (if we got a full page)
          this.hasMore = this.newsletters.length === 12;
        } else {
          console.error("Error loading newsletters:", response.data.message);
          this.newsletters = [];
          this.hasMore = false;
        }
      } catch (error) {
        console.error("Error loading newsletters:", error);
        this.newsletters = [];
        this.hasMore = false;
      } finally {
        this.loading = false;
      }
    },

    async loadMore() {
      this.loadingMore = true;
      this.currentOffset += 12;
      
      try {
        // Build query params
        const params = new URLSearchParams();
        params.append('sortBy', this.sortBy);
        if (this.userID !== 'defaultUser' && this.userType) {
          params.append('userID', this.userID);
          params.append('userType', this.userType);
        }
        
        let url;
        if (this.searchQuery.trim()) {
          url = `${process.env.VUE_APP_API_URL}/stories/getNewsletterswSearch/${this.currentOffset}/${encodeURIComponent(this.searchQuery.trim())}?${params.toString()}`;
        } else {
          url = `${process.env.VUE_APP_API_URL}/stories/getNewsletters/${this.currentOffset}?${params.toString()}`;
        }
        
        const response = await this.$axios.get(url);
        
        if (response.data.code === 200) {
          const newNewsletters = response.data.data || [];
          this.newsletters.push(...newNewsletters);
          this.hasMore = newNewsletters.length === 12;
        }
      } catch (error) {
        console.error("Error loading more newsletters:", error);
        this.currentOffset -= 12; // Reset offset on error
      } finally {
        this.loadingMore = false;
      }
    },

    handleSearch() {
      // Debounce search
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout);
      }
      this.searchTimeout = setTimeout(() => {
        this.loadNewsletters();
      }, 300);
    },

    clearSearch() {
      this.searchQuery = "";
      this.loadNewsletters();
    },

    goToNewsletter(newsletter) {
      const slug = this.slugify(newsletter.newsletterName);
      this.$router.push(`/stories/newsletters/${newsletter.id}/${slug}`);
    },

    getCoverStyle(newsletter) {
      // Use newsletterDisplayPhoto first, fall back to newsletterBanner, then default
      const imageUrl = newsletter.newsletterDisplayPhoto || newsletter.newsletterBanner || this.defaultCoverImage;
      return {
        backgroundImage: `url(${imageUrl})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        height: '150px',
      };
    },

    truncateText(text, maxLength) {
      if (!text) return '';
      if (text.length <= maxLength) return text;
      return text.substring(0, maxLength).trim() + '...';
    },

    slugify(text) {
      if (!text) return '';
      return text
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .trim();
    },
  },
};
</script>

<style scoped>
/* Newsletter Card Styles */
.newsletter-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border-radius: 12px;
  overflow: hidden;
}

.newsletter-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
}

.newsletter-cover {
  position: relative;
}

.cover-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  top: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0) 50%);
}

/* Input Group Styles */
.input-group .form-control:focus {
  border-color: #dee2e6;
  box-shadow: none;
}

.input-group-text {
  border-right: none;
}

.input-group .form-control {
  border-left: none;
}
</style>
