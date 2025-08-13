<template>
  <NavBar />

  <!-- Display when data is still loading -->
  <LoadingWithFunFact v-if="dataLoaded === false" />

  <!-- Display when data fails to load -->
  <div
    class="text-danger fst-italic fw-bold fs-3 pt-5"
    v-if="dataLoaded == null"
  >
    <span>An error occurred wh  async mounted() {
    // Get route parameters
    this.displayUserID = parseInt(this.$route.params.userID);
    this.routeUsername = this.$route.params.username;
    
    console.log("DEBUG: Route params:", this.$route.params);
    console.log("DEBUG: displayUserID:", this.displayUserID, "type:", typeof this.displayUserID);
    console.log("DEBUG: routeUsername:", this.routeUsername);
    
    await this.loadData();
  }, this page, please try again!</span>
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
      <div class="row">
        <div class="col-12 col-md-10 mx-auto">
          <!-- Header Section -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
              <h2 class="mb-1">
                <b>All Reviews by {{ displayUser.displayName || displayUser.username }}</b>
              </h2>
              <p class="text-muted mb-0">
                {{ totalReviews }} review{{ totalReviews !== 1 ? 's' : '' }} total
              </p>
            </div>
            <button
              class="btn primary-btn"
              @click="$router.push(`/profile/user/${displayUserID}/${routeUsername}`)"
            >
              Back to Profile
            </button>
          </div>

          <!-- Filter and Sort Controls -->
          <div class="row mb-4">
            <div class="col-md-6">
              <label class="form-label">Filter by Rating:</label>
              <select v-model="ratingFilter" @change="applyFilters" class="form-select">
                <option value="">All Ratings</option>
                <option value="9-10">Excellent (9-10)</option>
                <option value="7-8">Good (7-8)</option>
                <option value="5-6">Average (5-6)</option>
                <option value="1-4">Poor (1-4)</option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label">Sort by:</label>
              <select v-model="sortBy" @change="applyFilters" class="form-select">
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
                <option value="highest">Highest Rating</option>
                <option value="lowest">Lowest Rating</option>
              </select>
            </div>
          </div>

          <!-- Reviews List -->
          <div v-if="filteredReviews && filteredReviews.length > 0">
            <div v-for="review in paginatedReviews" :key="review.id" class="mb-4">
              <div style="display: flex" class="row mb-2 border rounded p-3">
                <div class="col-3 mobile-col-3 mobile-pe-0">
                  <img
                    :src="review.photo || defaultDrinkImage"
                    alt=""
                    class="rounded bottle-img"
                  />
                </div>
                <div class="col-9 mobile-col-9 mobile-ps-2">
                  <a
                    :href="'/listing/view/' + review.reviewTarget + '/' + encodeURIComponent(getListingName(review.reviewTarget) || 'unknown-listing')"
                    style="text-decoration: none; color: #223957"
                  >
                    <p class="fs-5 mobile-fs-6 mb-1 mobile-mb-0_5 default-clickable-text">
                      <b>{{ getListingName(review.reviewTarget) }}</b>
                    </p>
                  </a>

                  <!-- Review Date -->
                  <p class="text-muted small mb-2">
                    Reviewed on {{ formatDate(review.createdDate) }}
                  </p>

                  <!-- Flavor Tags -->
                  <div class="mb-2">
                    <span
                      v-for="(tag, index) in review.flavorTag"
                      :key="index"
                      class="mobile-view-hide badge rounded-pill-user-profile me-2 mb-1 mobile-me-0_5 mobile-mb-0_5"
                      :style="{ backgroundColor: getTagColor(tag) }"
                    >
                      {{ getTagName(tag) }}
                    </span>
                    <span
                      v-for="(tag, index) in review.observationTag"
                      :key="index"
                      class="mobile-view-hide badge rounded-pill-user-profile me-2 mb-1 mobile-me-0_5 mobile-mb-0_5"
                      style="background-color: #f0b358; color: black"
                    >
                      {{ tag }}
                    </span>

                    <!-- Mobile view (limited tags) -->
                    <span
                      v-for="(tag, index) in review.flavorTag?.slice(0, 2)"
                      :key="index"
                      class="mobile-view-show badge rounded-pill-user-profile me-2 mb-1 mobile-me-0_5 mobile-mb-0_5"
                      :style="{ backgroundColor: getTagColor(tag) }"
                    >
                      {{ getTagName(tag) }}
                    </span>
                    <span
                      v-for="(tag, index) in review.observationTag.slice(0, 1)"
                      :key="index"
                      class="mobile-view-show badge rounded-pill-user-profile me-2 mb-1 mobile-me-0_5 mobile-mb-0_5"
                      style="background-color: #f0b358; color: black"
                    >
                      {{ tag }}
                    </span>
                  </div>

                  <!-- Review Content -->
                  <div class="mb-2">
                    <p class="mobile-fs-7 mb-1" v-if="review.reviewTitle">
                      <b>{{ review.reviewTitle }}</b>
                    </p>
                    <p class="mobile-fs-7 mb-2" v-if="review.reviewDesc">
                      {{ review.reviewDesc }}
                    </p>
                  </div>

                  <!-- Rating and Location -->
                  <div class="d-flex justify-content-between align-items-center">
                    <p class="fs-4 mobile-fs-5 fw-bold rating-text mobile-mb-1 mb-0">
                      {{ parseFloat(review.rating).toFixed(1) }}★
                    </p>
                    <p class="text-muted small mb-0" v-if="review.location || review.address">
                      {{ getLocationName(review.location) || review.address }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- No Reviews Message -->
          <div v-else-if="dataLoaded" class="text-center py-5">
            <h4 class="text-muted">No reviews found</h4>
            <p class="text-muted">
              {{ displayUser.displayName || displayUser.username }} hasn't written any reviews yet.
            </p>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="d-flex justify-content-center mt-4">
            <nav aria-label="Reviews pagination">
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

          <!-- Load More Button (alternative to pagination) -->
          <div v-if="hasMoreReviews && !showPagination" class="text-center mt-4">
            <button 
              class="btn primary-btn" 
              @click="loadMoreReviews"
              :disabled="loadingMore"
            >
              {{ loadingMore ? 'Loading...' : 'Load More Reviews' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';

export default {
  name: "AllReviews",
  components: {
    NavBar,
    LoadingWithFunFact,
  },
  data() {
    return {
      dataLoaded: false,
      
      // Default images
      defaultDrinkImage: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1748434288",
      
      // User data
      displayUserID: null,
      routeUsername: null,
      displayUser: {},
      
      // Reviews data
      allReviews: [],
      filteredReviews: [],
      listings: {},
      venues: {},
      subTags: [],
      flavourTags: [],
      
      // Pagination
      currentPage: 1,
      reviewsPerPage: 20,
      totalReviews: 0,
      hasMoreReviews: true,
      loadingMore: false,
      showPagination: true,
      
      // Filtering and sorting
      ratingFilter: '',
      sortBy: 'newest',
      
      // Loading states
      loadingReviews: false,
    };
  },
  computed: {
    paginatedReviews() {
      if (this.showPagination) {
        const start = (this.currentPage - 1) * this.reviewsPerPage;
        const end = start + this.reviewsPerPage;
        return this.filteredReviews.slice(start, end);
      }
      return this.filteredReviews;
    },
    
    totalPages() {
      return Math.ceil(this.filteredReviews.length / this.reviewsPerPage);
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
    
    console.log("DEBUG: Route params:", this.$route.params);
    console.log("DEBUG: displayUserID:", this.displayUserID, "type:", typeof this.displayUserID);
    console.log("DEBUG: routeUsername:", this.routeUsername);
    
    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        this.dataLoaded = false;
        
        // Load user profile
        await this.getDisplayUserProfile();
        
        // Load reviews
        await this.loadAllReviews();
        
        // Load supporting data
        await this.loadSupportingData();
        
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
    
    async loadAllReviews() {
      try {
        this.loadingReviews = true;
        console.log(`DEBUG: Making request to /getData/getAllUserReviews/${this.displayUserID}`);
        console.log(`DEBUG: displayUserID type: ${typeof this.displayUserID}, value: ${this.displayUserID}`);
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getAllUserReviews/${this.displayUserID}`
        );
        
        console.log("DEBUG: Response from getAllUserReviews:", response.data);
        console.log("DEBUG: Response status:", response.status);
        console.log("DEBUG: Response headers:", response.headers);
        
        this.allReviews = response.data.reviews || [];
        
        // For testing: show test data info
        if (response.data.message === "Test response") {
          console.log("DEBUG: Received test response successfully!");
          alert(`Test successful! Endpoint called with userID: ${this.displayUserID}`);
        }
        this.totalReviews = response.data.total || this.allReviews.length;
        this.hasMoreReviews = response.data.hasMore || false;
        
        this.applyFilters();
      } catch (error) {
        console.error("Error loading reviews:", error);
        this.allReviews = [];
        this.totalReviews = 0;
      } finally {
        this.loadingReviews = false;
      }
    },
    
    async loadMoreReviews() {
      if (this.loadingMore || !this.hasMoreReviews) return;
      
      try {
        this.loadingMore = true;
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getAllUserReviews/${this.displayUserID}`,
          {
            params: {
              offset: this.allReviews.length,
              limit: this.reviewsPerPage
            }
          }
        );
        
        const newReviews = response.data.reviews || [];
        this.allReviews.push(...newReviews);
        this.hasMoreReviews = response.data.hasMore || false;
        
        this.applyFilters();
      } catch (error) {
        console.error("Error loading more reviews:", error);
      } finally {
        this.loadingMore = false;
      }
    },
    
    async loadSupportingData() {
      try {
        // Load listings for review targets
        const listingIDs = [...new Set(this.allReviews.map(r => r.reviewTarget))];
        if (listingIDs.length > 0) {
          const listingsResponse = await this.$axios.post(
            `${process.env.VUE_APP_API_URL}/getData/getListingsByIDs`,
            { listingIDs }
          );
          
          // Convert array to object for quick lookup
          this.listings = {};
          listingsResponse.data.forEach(listing => {
            this.listings[listing.id] = listing;
          });
        }
        
        // Load venues
        const venueResponse = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getVenues`
        );
        
        // Convert array to object for quick lookup
        this.venues = {};
        venueResponse.data.forEach(venue => {
          this.venues[venue.id] = venue;
        });
        
        // Load flavor tags
        const subTagsResponse = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getSubTags`
        );
        this.subTags = subTagsResponse.data;
        
        const flavourTagsResponse = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getFlavourTags`
        );
        this.flavourTags = flavourTagsResponse.data;
        
      } catch (error) {
        console.error("Error loading supporting data:", error);
      }
    },
    
    applyFilters() {
      let filtered = [...this.allReviews];
      
      // Apply rating filter
      if (this.ratingFilter) {
        const [min, max] = this.ratingFilter.split('-').map(Number);
        filtered = filtered.filter(review => {
          const rating = parseFloat(review.rating);
          return rating >= min && rating <= max;
        });
      }
      
      // Apply sorting
      filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'newest':
            return new Date(b.createdDate) - new Date(a.createdDate);
          case 'oldest':
            return new Date(a.createdDate) - new Date(b.createdDate);
          case 'highest':
            return parseFloat(b.rating) - parseFloat(a.rating);
          case 'lowest':
            return parseFloat(a.rating) - parseFloat(b.rating);
          default:
            return 0;
        }
      });
      
      this.filteredReviews = filtered;
      this.currentPage = 1; // Reset to first page when filters change
    },
    
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        // Scroll to top of reviews section
        this.$nextTick(() => {
          const reviewsSection = document.querySelector('.userprofile');
          if (reviewsSection) {
            reviewsSection.scrollIntoView({ behavior: 'smooth' });
          }
        });
      }
    },
    
    getListingName(listingID) {
      return this.listings[listingID]?.listingName || 'Unknown Listing';
    },
    
    getLocationName(locationID) {
      return this.venues[locationID]?.venueName || '';
    },
    
    getTagName(tag) {
      if (!this.subTags || !this.flavourTags) {
        return tag;
      }
      
      const subTag = this.subTags.find((subTag) => subTag.id === tag);
      if (subTag) {
        const flavourTag = this.flavourTags.find((flavourTag) => flavourTag.id === subTag.familyTagId);
        return flavourTag ? flavourTag.familyTag : subTag.subtag;
      } else {
        const flavourTag = this.flavourTags.find((flavourTag) => flavourTag.id === tag);
        return flavourTag ? flavourTag.familyTag : tag;
      }
    },
    
    getTagColor(tag) {
      if (!this.subTags || !this.flavourTags) {
        return '#6c757d';
      }
      
      const subTag = this.subTags.find((subTag) => subTag.id === tag);
      if (subTag) {
        const flavourTag = this.flavourTags.find((flavourTag) => flavourTag.id === subTag.familyTagId);
        return flavourTag ? flavourTag.hexcode : '#6c757d';
      } else {
        const flavourTag = this.flavourTags.find((flavourTag) => flavourTag.id === tag);
        return flavourTag ? flavourTag.hexcode : '#6c757d';
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return 'Unknown date';
      
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    }
  }
};
</script>

<style scoped>
.bottle-img {
  width: 100%;
  height: 120px;
  object-fit: cover;
}

.rounded-pill-user-profile {
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
}

.rating-text {
  color: #f0b358;
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
  
  .mobile-fs-5 {
    font-size: 1.125rem !important;
  }
  
  .mobile-fs-7 {
    font-size: 0.875rem !important;
  }
  
  .mobile-mb-0_5 {
    margin-bottom: 0.25rem !important;
  }
  
  .mobile-me-0_5 {
    margin-right: 0.25rem !important;
  }
  
  .mobile-mb-0_5 {
    margin-bottom: 0.25rem !important;
  }
  
  .mobile-mb-1 {
    margin-bottom: 0.5rem !important;
  }
  
  .mobile-mt-3 {
    margin-top: 1rem !important;
  }
  
  .mobile-view-hide {
    display: none !important;
  }
  
  .mobile-view-show {
    display: inline !important;
  }
}

@media (min-width: 769px) {
  .mobile-view-hide {
    display: inline !important;
  }
  
  .mobile-view-show {
    display: none !important;
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
</style>
