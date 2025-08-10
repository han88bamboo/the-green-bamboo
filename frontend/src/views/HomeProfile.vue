<template>
    <NavBar />

    <!-- Display when data is still loading -->
    <LoadingWithFunFact v-if="dataLoaded === false" />

    <!-- Main Content -->
    <div class="container pt-5 mobile-pt-3" v-if="dataLoaded == true">
        <div class="row">

            <!-- ------- START Home Information ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Home Information -->
            <div class="col-xl-9 col-12 px-3 px-lg-4">

                <!-- ------- START Home Name / Title ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                <!-- Home Name -->
                <div class="row">
                    <div class="ps-0 pe-0">
                        <h3 class="text-body-secondary mobile-view-hide"> <b> Home Tastings </b> </h3>
                        <h4 class="text-body-secondary mobile-view-show pe-0 ps-0 mb-1"> <b> Home Tastings </b> </h4>
                    </div>
                </div>

                <!-- ------- END Home Name / START Description   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                <!-- Description -->
                <div class="row scrollable">
                    <div class="col-12 pe-lg-0 ps-0">
                        <div class="ps-0 pe-0 ">
                            <p class="text-body-secondary fs m-0 mobile-rating-smaller-text-2">
                                Explore and share tasting experiences from the comfort of home. Join the community of home tasters discovering new flavors and sharing their reviews.
                            </p>
                        </div>
                    </div>
                </div>

                <!-- View Mode: Home Info + Buttons -->
                <div class="row mt-4 mobile-mt-1 text-start">
                    <!-- Home Info -->
                    <div class="col-7 mobile-col-12 mobile-mb-2">
                        <p class="text-body-secondary mobile-rating-smaller-text-2 fs-6 mb-0">
                            <strong>Total Reviews:</strong> {{ homeReviews.length }} | 
                            <strong>Average Rating:</strong> {{ averageRating.toFixed(1) }}/5 |
                            <strong>Community:</strong> Home tasters worldwide
                        </p>
                    </div>

                    <!-- Right Side: Follow Button -->
                    <div class="col-5 mobile-col-12 d-flex justify-content-end mobile-justify-content-start">
                        <div class="d-flex flex-column gap-2 mobile-d-grid mobile-gap-1">
                            <!-- Follow Button -->
                            <button v-if="!homeFollowing"
                                class="btn btn-lg primary-btn-less-round text-nowrap mobile-rating-smaller-text-2"
                                @click="toggleHomeFollow" style="font-weight: bold;">
                                + Follow
                            </button>
                            <button v-else
                                class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2"
                                @click="toggleHomeFollow"
                                style="font-weight: bold; background-color: rgb(249, 115, 106);">
                                Following
                            </button>
                        </div>
                    </div>
                </div>

                <!--------- END Follow Button ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- START Content Buttons (Home Overview / Home Reviews) -->
                <div class="row mt-3 mobile-mt-1" id="menu-section">
                    <div class="col-8 d-flex justify-content-start mobile-col-7 mobile-pe-0">
                        <!-- Toggle Home Overview -->
                        <button v-if="contentMode == 'overview'"
                            class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'overview'"> Home Overview </button>
                        <button v-else
                            class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'overview'"> Home Overview </button>
                        
                        <!-- Toggle Home Reviews -->
                        <button v-if="contentMode == 'reviews'"
                            class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'reviews'">
                            Home Reviews ({{ homeReviews.length }})
                        </button>
                        <button v-else
                            class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'reviews'">
                            Home Reviews ({{ homeReviews.length }})
                        </button>
                    </div>
                </div>
                <!-- End Content Buttons -->
                <hr>

                <!-- Home Overview -->
                <div v-if="contentMode == 'overview'">
                    <!-- Latest Updates Header -->
                    <div class="row">
                        <div class="col-12">
                            <p class="text-start text-body-secondary fs-4 fw-bold m-0 mobile-fs-6">Home Tasting Community</p>
                            <p class="text-start fs-6 mobile-rating-smaller-text-2 fst-italic m-1 pb-2">Discover what fellow enthusiasts are tasting at home!</p>
                        </div>
                    </div>

                    <!-- Recent Activity -->
                    <div v-if="homeReviews.length > 0">
                        <!-- Row 1: Recent Home Reviews -->
                        <div class="row align-items-start mt-3">
                            <div class="col-12 text-start">
                                <p class="text-start text-body-secondary fs-5 fw-bold m-0 mobile-fs-6">Recent Home Reviews</p>
                                
                                <div v-for="review in recentReviews" :key="review.id" class="row mt-3 p-3 border rounded">
                                    <div class="col-2 mobile-col-4">
                                        <img :src="review.listing_image || '/default-bottle.jpg'" 
                                             :alt="review.listing_name" class="img-fluid rounded" />
                                    </div>
                                    <div class="col-10 mobile-col-8">
                                        <h6 class="fw-bold">{{ review.listing_name }}</h6>
                                        <div class="rating mb-2">
                                            <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= review.rating }">★</span>
                                            <span class="ms-2">{{ review.rating }}/5</span>
                                        </div>
                                        <p class="mb-2">{{ review.review_text || 'No review text provided.' }}</p>
                                        <small class="text-muted">
                                            By {{ review.username }} on {{ formatDate(review.date_time) }}
                                        </small>
                                        <div class="mt-2">
                                            <router-link :to="`/listing/${review.listing_id}/${review.listing_name}`" 
                                                       class="btn btn-sm btn-outline-primary">
                                                View Listing
                                            </router-link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- No Reviews State -->
                    <div v-else class="text-center py-5">
                        <i class="fas fa-home fa-3x text-muted mb-3"></i>
                        <h5>No home reviews yet</h5>
                        <p class="text-muted">Be the first to share a home tasting experience!</p>
                        <router-link to="/create-review" class="btn btn-primary">
                            Create First Home Review
                        </router-link>
                    </div>
                </div>

                <!-- Home Reviews -->
                <div v-if="contentMode == 'reviews'">
                    <div class="row">
                        <div class="col-12">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <p class="text-start text-body-secondary fs-4 fw-bold m-0 mobile-fs-6">All Home Reviews ({{ homeReviews.length }})</p>
                                <div class="sort-options" v-if="homeReviews.length > 0">
                                    <select v-model="sortBy" @change="sortReviews" class="form-select">
                                        <option value="newest">Newest First</option>
                                        <option value="oldest">Oldest First</option>
                                        <option value="highest">Highest Rating</option>
                                        <option value="lowest">Lowest Rating</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div v-if="homeReviews.length === 0" class="text-center py-5">
                                <i class="fas fa-home fa-3x text-muted mb-3"></i>
                                <h5>No home reviews yet</h5>
                                <p class="text-muted">Start the home tasting community by creating the first review!</p>
                                <router-link to="/create-review" class="btn btn-primary">
                                    Create First Home Review
                                </router-link>
                            </div>
                            
                            <div v-else>
                                <div v-for="review in sortedReviews" :key="review.id" class="row mt-3 p-3 border rounded">
                                    <div class="col-md-3 mobile-col-12">
                                        <img :src="review.listing_image || '/default-bottle.jpg'" 
                                             :alt="review.listing_name" class="img-fluid rounded review-image" />
                                    </div>
                                    <div class="col-md-9 mobile-col-12">
                                        <div class="d-flex justify-content-between align-items-start mb-2">
                                            <div>
                                                <h5 class="fw-bold">{{ review.listing_name }}</h5>
                                                <div class="rating mb-2">
                                                    <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= review.rating }">★</span>
                                                    <span class="rating-text ms-2">{{ review.rating }}/5</span>
                                                </div>
                                            </div>
                                            <div class="text-end">
                                                <small class="text-muted d-block">{{ formatDate(review.date_time) }}</small>
                                                <small class="text-muted d-block">by {{ review.username }}</small>
                                            </div>
                                        </div>
                                        
                                        <p class="review-text">{{ review.review_text || 'No review text provided.' }}</p>
                                        
                                        <div class="d-flex gap-2 align-items-center">
                                            <router-link :to="`/listing/${review.listing_id}/${review.listing_name}`" 
                                                       class="btn btn-sm btn-outline-primary">
                                                View Listing
                                            </router-link>
                                            <span class="badge bg-secondary">
                                                <i class="fas fa-home me-1"></i>
                                                Home Tasting
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            <!-- ------- END Home Information / START Home Sidebar ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Home Sidebar -->
            <div class="col-xl-3 col-12">
                
                <!-- ------- START Home Statistics ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                <div class="row">
                    <div class="col-12">
                        <div class="border rounded p-3 mb-3">
                            <h5 class="fw-bold mb-3">Home Tasting Stats</h5>
                            
                            <div class="stat-item mb-2">
                                <div class="d-flex justify-content-between">
                                    <span class="text-muted">Total Reviews:</span>
                                    <span class="fw-bold">{{ homeReviews.length }}</span>
                                </div>
                            </div>
                            
                            <div class="stat-item mb-2">
                                <div class="d-flex justify-content-between">
                                    <span class="text-muted">Average Rating:</span>
                                    <span class="fw-bold">{{ averageRating.toFixed(1) }}/5</span>
                                </div>
                            </div>
                            
                            <div class="stat-item mb-2">
                                <div class="d-flex justify-content-between">
                                    <span class="text-muted">Active Reviewers:</span>
                                    <span class="fw-bold">{{ uniqueReviewers }}</span>
                                </div>
                            </div>
                            
                            <hr class="my-3">
                            
                            <div class="d-grid">
                                <router-link to="/create-review" class="btn btn-primary">
                                    <i class="fas fa-plus me-1"></i>
                                    Add Home Review
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ------- START About Home Tastings ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                <div class="row">
                    <div class="col-12">
                        <div class="border rounded p-3">
                            <h5 class="fw-bold mb-3">About Home Tastings</h5>
                            <p class="small text-muted mb-3">
                                Home tastings allow you to explore and review drinks in the comfort of your own space. 
                                Share your experiences with the community and discover what others are enjoying at home.
                            </p>
                            <p class="small text-muted mb-0">
                                <strong>Features:</strong> Rate drinks, write detailed reviews, share photos, and connect with fellow enthusiasts.
                            </p>
                        </div>
                    </div>
                </div>

            </div>

        </div>
    </div>
</template>

<script>
import axios from 'axios';
import NavBar from "@/components/NavBar.vue";
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';

export default {
  name: 'HomeProfile',
  components: {
    NavBar,
    LoadingWithFunFact
  },
  data() {
    return {
      contentMode: 'overview',
      homeReviews: [],
      sortBy: 'newest',
      loading: true,
      error: null,
      dataLoaded: false,
      homeFollowing: false
    };
  },
  computed: {
    averageRating() {
      if (this.homeReviews.length === 0) return 0;
      const sum = this.homeReviews.reduce((acc, review) => acc + review.rating, 0);
      return sum / this.homeReviews.length;
    },
    recentReviews() {
      return [...this.homeReviews]
        .sort((a, b) => new Date(b.date_time) - new Date(a.date_time))
        .slice(0, 5);
    },
    sortedReviews() {
      let sorted = [...this.homeReviews];
      
      switch (this.sortBy) {
        case 'newest':
          return sorted.sort((a, b) => new Date(b.date_time) - new Date(a.date_time));
        case 'oldest':
          return sorted.sort((a, b) => new Date(a.date_time) - new Date(b.date_time));
        case 'highest':
          return sorted.sort((a, b) => b.rating - a.rating);
        case 'lowest':
          return sorted.sort((a, b) => a.rating - b.rating);
        default:
          return sorted;
      }
    },
    uniqueReviewers() {
      const reviewers = new Set(this.homeReviews.map(review => review.username));
      return reviewers.size;
    }
  },
  mounted() {
    this.fetchHomeReviews();
  },
  methods: {
    async fetchHomeReviews() {
      try {
        this.loading = true;
        this.dataLoaded = false;
        const response = await axios.get('/api/getHomeReviews');
        this.homeReviews = response.data;
        this.error = null;
        this.dataLoaded = true;
      } catch (error) {
        console.error('Error fetching home reviews:', error);
        this.error = 'Failed to load home reviews';
        this.homeReviews = [];
        this.dataLoaded = true;
      } finally {
        this.loading = false;
      }
    },
    sortReviews() {
      // Computed property will handle the sorting
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    toggleHomeFollow() {
      this.homeFollowing = !this.homeFollowing;
      // Here you could add API call to save follow status
      // For now, just toggle the local state
    }
  }
};
</script>

<style scoped>
/* Match VenueProfile.vue styling patterns */

.rating .star {
  color: #ddd;
  font-size: 1.2rem;
}

.rating .star.filled {
  color: #ffc107;
}

.rating-text {
  color: #6c757d;
  font-weight: 500;
}

.review-text {
  color: #495057;
  line-height: 1.6;
  margin: 1rem 0;
}

.review-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
}

.sort-options {
  min-width: 200px;
}

.stat-item {
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}

.stat-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

/* Button styles matching VenueProfile */
.active-toggle-button {
  background-color: #007bff;
  color: white;
  border: 1px solid #007bff;
}

.inactive-toggle-button {
  background-color: white;
  color: #007bff;
  border: 1px solid #007bff;
}

.primary-btn-less-round {
  background-color: #007bff;
  color: white;
  border: 1px solid #007bff;
  border-radius: 4px;
  padding: 8px 16px;
}

.primary-btn-less-round-blue {
  background-color: #f9736a;
  color: white;
  border: 1px solid #f9736a;
  border-radius: 4px;
  padding: 8px 16px;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .mobile-view-hide {
    display: none;
  }
  
  .mobile-view-show {
    display: block;
  }
  
  .mobile-col-12 {
    flex: 0 0 100%;
    max-width: 100%;
  }
  
  .mobile-col-8 {
    flex: 0 0 66.666667%;
    max-width: 66.666667%;
  }
  
  .mobile-col-7 {
    flex: 0 0 58.333333%;
    max-width: 58.333333%;
  }
  
  .mobile-col-4 {
    flex: 0 0 33.333333%;
    max-width: 33.333333%;
  }
  
  .mobile-col-2 {
    flex: 0 0 16.666667%;
    max-width: 16.666667%;
  }
  
  .mobile-pt-3 {
    padding-top: 1rem;
  }
  
  .mobile-mt-1 {
    margin-top: 0.25rem;
  }
  
  .mobile-mb-2 {
    margin-bottom: 0.5rem;
  }
  
  .mobile-pe-0 {
    padding-right: 0;
  }
  
  .mobile-ps-1 {
    padding-left: 0.25rem;
  }
  
  .mobile-pe-1 {
    padding-right: 0.25rem;
  }
  
  .mobile-justify-content-start {
    justify-content: flex-start;
  }
  
  .mobile-d-grid {
    display: grid;
  }
  
  .mobile-gap-1 {
    gap: 0.25rem;
  }
  
  .mobile-rating-smaller-text-2 {
    font-size: 0.875rem;
  }
  
  .mobile-fs-6 {
    font-size: 1.25rem;
  }
  
  .mobile-toggle-button-producer-profile {
    font-size: 0.875rem;
    padding: 0.375rem 0.75rem;
  }
  
  .review-image {
    height: 150px;
    margin-bottom: 1rem;
  }
}

/* Hide mobile classes on desktop */
@media (min-width: 769px) {
  .mobile-view-show {
    display: none;
  }
  
  .mobile-view-hide {
    display: block;
  }
}
</style>
