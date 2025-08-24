<template>
    <NavBar />

    <!-- Main Content -->
    <div class="container pt-5 mobile-pt-3">

        <!-- Display when data is still loading -->
        <LoadingWithFunFact v-if="dataLoaded === false" />

        <!-- Display when data fails to load -->
        <div class="text-danger fst-italic fw-bold fs-3" v-if="dataLoaded == null">
            <span>An error occurred while loading this page, please try again!</span>
            <br>
            <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
                <span class="fs-5 fst-italic"> Return to previous page </span>
            </button>
            <router-link :to="'/'" class="mx-1">
                <button class="btn primary-btn btn-sm">
                    <span class="fs-5 fst-italic"> Go to Home page </span>
                </button>
            </router-link>
        </div>

        <div class="row" v-if="dataLoaded == true">

            <!-- ------- START Home Information ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Home Information -->
            <div class="col-xl-9 col-12 px-3 px-lg-4">

                <!-- ------- START Header ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Header -->
                <div class="row">

                    <!-- ------- START Image ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Image -->
                    <div class="col-lg-3 col-12 mb-lg-0 mb-3 image-container text-start mobile-col-5">
                        <div>
                            <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Tasted_at_home.png?v=1754842378" alt="Home Tastings"
                                class="producer-bottle-listing-page-image">
                        </div>
                    </div>

                    <!-- ------- END Image / START Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Details -->
                    <div class="col-lg-9 col-12 text-start ps-lg-5 ps-1 mobile-col-7">
                        <div class="row">

                            <!-- Country -->
                            <div class="col-7 pe-0 ps-0">
                                <h5 class="text-body-secondary mobile-view-hide">Home Tasting Community</h5>
                                <h6 class="text-body-secondary mobile-view-show mb-1">Home Tasting Community</h6>
                            </div>

                            <!-- No claim/edit section for Home Profile -->
                            <div class="col-5 mobile-view-hide">
                                <!-- This space intentionally left blank to match VenueProfile layout -->
                            </div>

                        </div>

                        <!-- ------- START Home Name ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                        <!-- Home Name -->
                        <div class="row">
                            <div class="ps-0 pe-0">
                                <h3 class="text-body-secondary mobile-view-hide"> <b>Tasted at Home</b> </h3>
                                <h4 class="text-body-secondary mobile-view-show pe-0 ps-0 mb-1"> <b>Tasted at Home</b> </h4>
                            </div>
                        </div>

                        <!-- ------- END Home Name / START Home Type   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                        <!-- Home Type -->
                        <div class="row">
                            <div class="col-12 pe-lg-0 ps-0">
                                <div class="ps-0 pe-0">
                                    <p class="text-body-secondary fs m-0 mobile-rating-smaller-text-2">
                                        <i>Virtual Tasting Location</i>
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- ------- END Home Name / START Description   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                        <!-- Description -->
                        <div class="row scrollable">
                            <div class="col-12 pe-lg-0 ps-0">
                                <div class="ps-0 pe-0 ">
                                    <p class="text-body-secondary fs m-0 mobile-rating-smaller-text-2">
                                        Explore and share tasting experiences from the comfort of home. Join the community of home tasters discovering new flavours together! 
                                    </p>
                                </div>
                            </div>
                        </div>

                    </div>
                    <!-- ------- END Description ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                </div>

                <!-- View Mode: Home Info + Buttons -->
                <div class="row mt-4 mobile-mt-1 text-start">
                    <!-- Home Info -->
                    <div class="col-7 mobile-col-12 mobile-mb-2">
                        <p class="text-body-secondary mobile-rating-smaller-text-2 fs-6 mb-0">
                            <strong>{{ homeReviews.length }}</strong> reviews • 
                            <strong>{{ averageRating.toFixed(1) }}</strong>/5 average rating • 
                            <strong>{{ uniqueReviewers }}</strong> reviewers
                        </p>
                    </div>

                    <!-- Right Side: Follow Button -->
                    <div class="col-5 d-flex flex-column flex-lg-row justify-content-start justify-content-lg-end align-items-start align-items-lg-center gap-2">
                        <div class="d-flex gap-2">
                            <!-- Follow Button -->
                            <button v-if="!homeFollowing"
                                class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2"
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
                <!-- ------- END Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                <!-- ------- END Header  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- START Content Buttons (Home Overview / Home Reviews) -->
                <div class="row mt-3 mobile-mt-1" id="menu-section">
                    <div class="col-8 d-flex justify-content-start mobile-col-7 mobile-pe-0">
                        <!-- Toggle Home Overview -->
                        <button v-if="contentMode == 'overview'"
                            class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'overview'"> Home Tastings Overview </button>
                        <button v-else
                            class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'overview'"> Home Tastings Overview </button>
                        
                        <!-- Toggle Home Reviews -->
                        <button v-if="contentMode == 'reviews'"
                            class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'reviews'">
                            Home Reviews
                        </button>
                        <button v-else
                            class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'reviews'">
                            Home Reviews
                        </button>
                    </div>
                </div>
                <!-- End Content Buttons -->
                <hr>

                <!-- Home Overview -->
                <div v-if="contentMode == 'overview'">

                    <!-- ------- START Latest Updates Header + Latest Update Information ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Latest Updates Header -->
                    <div class="row">
                        <div class="col-12">
                            <p class="text-start text-body-secondary fs-4 fw-bold m-0 mobile-fs-6">Latest Updates from Tasted at Home</p>
                            <p class="text-start fs-6 mobile-rating-smaller-text-2 fst-italic m-1 pb-2">Community updates and featured home tastings will appear here!</p>
                        </div>
                    </div>

                    <!-- Latest Update Information -->
                    <div v-if="homeReviews.length > 0">

                        <!-- Row 1: Recent Home Reviews Preview -->
                        <div class="row align-items-start mt-3">
                            <div class="col-12 text-start">
                                <h5 class="text-body-secondary fw-bold mb-3">Recent Home Tastings</h5>
                                <div v-for="review in recentReviews.slice(0, 3)" :key="review.id" class="mb-3 p-3 border rounded">
                                    <div class="d-flex justify-content-between align-items-start">
                                        <div>
                                            <h6 class="fw-bold mb-1">{{ review.listing_name }}</h6>
                                            <div class="rating mb-2">
                                                <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= review.rating }">★</span>
                                                <span class="rating-text ms-2">{{ review.rating }}/5</span>
                                            </div>
                                            <p class="review-text">{{ review.review_text?.substring(0, 150) }}{{ review.review_text?.length > 150 ? '...' : '' }}</p>
                                            <small class="text-muted">by {{ review.username }} • {{ formatDate(review.date_time) }}</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                </div>

                <!-- ------- END Home Overview ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                <!-- Home Reviews -->
                <div v-if="contentMode == 'reviews'">

                    <!-- Reviews Header with Sort -->
                    <div class="row mb-3">
                        <div class="col-8">
                            <h4 class="text-body-secondary fw-bold">Home Tasting Reviews</h4>
                        </div>
                        <div class="col-4 text-end">
                            <select v-model="sortBy" @change="sortReviews" class="form-select sort-options">
                                <option value="newest">Newest First</option>
                                <option value="oldest">Oldest First</option>
                                <option value="highest">Highest Rated</option>
                                <option value="lowest">Lowest Rated</option>
                            </select>
                        </div>
                    </div>

                    <!-- Reviews List -->
                    <div v-if="sortedReviews.length > 0">
                        <div v-for="review in sortedReviews" :key="review.id" class="row mb-4 pb-3 border-bottom">
                            <div class="col-12">
                                <div class="d-flex justify-content-between align-items-start mb-2">
                                    <div>
                                        <h5 class="fw-bold mb-1">{{ review.listing_name }}</h5>
                                        <div class="rating mb-2">
                                            <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= review.rating }">★</span>
                                            <span class="rating-text ms-2">{{ review.rating }}/5</span>
                                        </div>
                                    </div>
                                    <small class="text-muted">{{ formatDate(review.date_time) }}</small>
                                </div>
                                <p class="review-text">{{ review.review_text }}</p>
                                <div class="d-flex justify-content-between align-items-center">
                                    <small class="text-muted">Reviewed by {{ review.username }}</small>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- No Reviews Message -->
                    <div v-else class="text-center py-5">
                        <h5 class="text-muted">No home tasting reviews yet</h5>
                        <p class="text-muted">Be the first to share your home tasting experience!</p>
                    </div>

                </div>

                <!-- ------- END Home reviews ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            </div>

            <!-- ------- END Home Information / START Home Sidebar ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Home Sidebar -->
            <div class="col-xl-3 col-12">

                <!-- ------- START Q & A ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                <!-- NOTE: Q&A section is intentionally removed for Home Profile -->

                <!-- ------- END Q & A / START Map View ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                <!-- NOTE: Map/Location section is intentionally removed for Home Profile -->

                <!-- ------- START Opening Hours ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                <!-- NOTE: Opening Hours section is intentionally removed for Home Profile -->

                <!-- ------- END Opening Hours / START About Section ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- About Home Tastings -->
                <div class="col-xl-12 col-lg-3 col-md-6 col-12">
                    <div class="primary-square text-start p-3 mb-4">
                        <h5 class="fw-bold text-body-secondary mb-3">About Home Tastings</h5>
                        <div class="stat-item mb-2">
                            <strong>Total Reviews:</strong> {{ homeReviews.length }}
                        </div>
                        <div class="stat-item mb-2">
                            <strong>Average Rating:</strong> {{ averageRating.toFixed(1) }}/5
                        </div>
                        <div class="stat-item mb-2">
                            <strong>Unique Reviewers:</strong> {{ uniqueReviewers }}
                        </div>
                        <div class="stat-item">
                            <strong>Community:</strong> Home Tasters
                        </div>
                    </div>
                </div>

                <!-- ------- END About Section ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            </div>

            <!-- ------- END Home Sidebar ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

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
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/getData/getHomeReviews`);
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

.producer-bottle-listing-page-image {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.square {
  border: 1px solid #dee2e6;
}

.primary-square-green-outline {
  border-color: #28a745;
}

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

.primary-btn {
  background-color: #007bff;
  color: white;
  border: 1px solid #007bff;
  border-radius: 4px;
  padding: 8px 16px;
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
  
  .mobile-col-5 {
    flex: 0 0 41.666667%;
    max-width: 41.666667%;
  }
  
  .mobile-col-4 {
    flex: 0 0 33.333333%;
    max-width: 33.333333%;
  }
  
  .mobile-col-3 {
    flex: 0 0 25%;
    max-width: 25%;
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

