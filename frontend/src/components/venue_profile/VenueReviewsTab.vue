<template>
  <div>
    <!-- Header Section -->
    <div class="mb-3">
      <h4 class="text-start text-dark fs-4 fw-bold m-0 mobile-fs-6 mb-2">
        Average Venue Rating: {{ averageRating }}
        <span class="text-warning">★</span>
        ({{ venueReviews.length }} {{ venueReviews.length === 1 ? 'Review' : 'Reviews' }})
      </h4>
    </div>

    <!-- Image Gallery Section -->
    <div class="row text-start ps-3">
      <div class="col">
        <div class="row justify-content-start align-items-start mt-2">
          <!-- Add Review Button -->
          <div 
            v-if="canAddReview" 
            class="mobile-col-3 col-sm-6 col-md-4 col-lg-2 mobile-px-1" 
            data-bs-toggle="modal"
            data-bs-target="#venueReviewModal" 
            role="button"
            tabindex="0"
          >
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              fill="#83A9E8" 
              class="bi bi-plus-lg review-image"
              viewBox="0 0 16 16"
            >
              <path 
                fill-rule="evenodd" 
                d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2" 
              />
            </svg>
          </div>

          <!-- Review Images -->
          <div 
            v-for="(imageData, index) in venueReviewImages"
            :key="`venue-${index}`" 
            class="mobile-col-3 col-sm-8 col-md-6 col-lg-2 mobile-px-1 position-relative"
          >
            <img 
              :src="imageData.photo || defaultPhoto" 
              :alt="`Review image ${index + 1}`"
              class="review-image" 
              loading="lazy" 
            />
            <div class="position-absolute top-0 end-0 m-1">
              <span class="badge bg-primary" style="font-size: 0.6rem;">V</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <hr />

    <!-- Reviews List -->
    <div class="reviews-container">
      <div 
        v-for="review in venueReviews" 
        :key="review.id" 
        class="review-item mb-4"
      >
        <div class="row">
          <!-- Review Content -->
          <div class="col-12 col-lg-9">
            <div class="row">
              <div class="text-start">
                <!-- User Info Row -->
                <div class="row align-items-center mb-2">
                  <!-- Profile Photo -->
                  <div class="col-auto mobile-col-2">
                    <router-link :to="`/profile/user/${review.userID}`">
                      <img 
                        :src="getPhotoFromReview(review) || defaultProfilePhoto" 
                        :alt="`${getUsernameFromReview(review)} profile`"
                        class="profile-image" 
                      />
                    </router-link>
                  </div>

                  <!-- User Details -->
                  <div class="col mobile-rating-smaller-text-2">
                    <div class="user-info">
                      <router-link 
                        :to="`/profile/user/${review.userID}`" 
                        class="text-decoration-none text-dark fw-bold"
                      >
                        @{{ getUsernameFromReview(review) }}
                      </router-link>
                      
                      <span class="ms-2 text-muted">
                        {{ getUserPointsFromReview(review) }}
                      </span>
                      
                      <span :style="{ color: getUserRankColor(review) }" class="ms-1">
                        {{ getUserRankFromReview(review) }}
                      </span>

                      <div class="rating-info mt-1">
                        <span>rated</span>
                        <span class="text-warning mx-1">★</span>
                        <span class="fw-bold">{{ review.rating }}</span>
                        <span>Stars</span>
                      </div>

                      <!-- Moderator Badge -->
                      <span 
                        v-if="checkModFromUserID(review.userID)"
                        class="badge rounded-pill ms-3 mobile-ms-0 mobile mt-1"
                        style="color: black; background-color: #f0b358"
                      >
                        Moderator
                      </span>
                    </div>

                    <!-- Action Buttons -->
                    <div class="action-buttons mt-2" v-if="canEditReview(review) || canMod">
                      <button 
                        v-if="canEditReview(review)"
                        class="btn btn-warning btn-sm me-2 mobile-fs-7" 
                        @click="setUpdateID(review)"
                        data-bs-toggle="modal" 
                        data-bs-target="#venueReviewModal"
                      >
                        Edit
                      </button>
                      
                      <button 
                        v-if="canMod" 
                        class="btn btn-danger btn-sm mobile-fs-7"
                        @click="setDeleteID(review)" 
                        data-bs-toggle="modal"
                        data-bs-target="#deleteReview"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Review Description -->
                <div class="review-text my-3 mobile-rating-smaller-text-2">
                  <p class="mb-0">{{ review.reviewDesc }}</p>
                </div>

                <!-- Voting Section -->
                <div class="d-flex align-items-center text-start mb-2">
                  <!-- Upvote Button -->
                  <button 
                    class="btn btn-link p-0 me-1"
                    @click="voteReview(review, getUpvoteAction(review))"
                    :class="{ 'text-success': hasUserUpvoted(review) }"
                  >
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      width="20" 
                      height="20" 
                      :fill="hasUserUpvoted(review) ? 'currentColor' : 'currentColor'"
                      :class="hasUserUpvoted(review) ? 'bi-caret-up-fill' : 'bi-caret-up'"
                      viewBox="0 0 16 16"
                    >
                      <path 
                        v-if="!hasUserUpvoted(review)"
                        d="M3.204 11h9.592L8 5.519zm-.753-.659 4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659" 
                      />
                      <path 
                        v-else
                        d="m7.247 4.86-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z" 
                      />
                    </svg>
                  </button>

                  <!-- Vote Score -->
                  <span class="mx-2 fw-bold">
                    {{ getVoteScore(review) }}
                  </span>

                  <!-- Downvote Button -->
                  <button 
                    class="btn btn-link p-0 me-3"
                    @click="voteReview(review, getDownvoteAction(review))"
                    :class="{ 'text-danger': hasUserDownvoted(review) }"
                  >
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      width="20" 
                      height="20" 
                      :fill="hasUserDownvoted(review) ? 'currentColor' : 'currentColor'"
                      :class="hasUserDownvoted(review) ? 'bi-caret-down-fill' : 'bi-caret-down'"
                      viewBox="0 0 16 16"
                    >
                      <path 
                        v-if="!hasUserDownvoted(review)"
                        d="M3.204 5h9.592L8 10.481zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659" 
                      />
                      <path 
                        v-else
                        d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z" 
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Review Photo (Desktop) -->
          <div class="col-3 text-end d-none d-lg-block">
            <div 
              class="review-photo-container"
              data-bs-toggle="modal" 
              :data-bs-target="`#reviewImageModal${getUsernameFromReview(review)}`"
              role="button"
              tabindex="0"
            >
              <img 
                :src="review.photos?.[0] || defaultPhoto" 
                :alt="`Review photo by ${getUsernameFromReview(review)}`"
                class="review-image"
                style="width: 125px; height: 125px; object-fit: cover;" 
              />
            </div>
          </div>
        </div>

        <!-- Review Photo (Mobile) -->
        <div class="row d-lg-none mt-2">
          <div class="col-12">
            <div 
              class="review-photo-container"
              data-bs-toggle="modal" 
              :data-bs-target="`#reviewImageModal${getUsernameFromReview(review)}`"
              role="button"
              tabindex="0"
            >
              <img 
                :src="review.photos?.[0] || defaultPhoto" 
                :alt="`Review photo by ${getUsernameFromReview(review)}`"
                class="review-image img-fluid"
                style="max-width: 300px; height: auto;" 
              />
            </div>
          </div>
        </div>

        <!-- Image Modal -->
        <div 
          class="modal fade" 
          :id="`reviewImageModal${getUsernameFromReview(review)}`" 
          tabindex="-1"
          :aria-labelledby="`reviewImageModalLabel${getUsernameFromReview(review)}`"
          aria-hidden="true"
        >
          <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" :id="`reviewImageModalLabel${getUsernameFromReview(review)}`">
                  Review Photo
                </h5>
                <button 
                  type="button" 
                  class="btn-close" 
                  data-bs-dismiss="modal" 
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body p-4">
                <img 
                  :src="review.photos?.[0] || defaultPhoto" 
                  :alt="`Full size review photo by ${getUsernameFromReview(review)}`"
                  class="img-fluid w-100"
                />
              </div>
            </div>
          </div>
        </div>

        <hr class="mt-4 mb-2" />
      </div>
    </div>

    <!-- Load More Button -->
    <div 
      v-if="shouldShowLoadMore" 
      class="d-flex justify-content-center mb-3"
    >
      <button 
        class="btn btn-primary btn-lg" 
        @click="loadMoreReviews"
        :disabled="loadingMore"
      >
        <span v-if="loadingMore" class="spinner-border spinner-border-sm me-2" role="status"></span>
        {{ loadingMore ? 'Loading...' : 'Load More Reviews' }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VenueReviewsTab',
  
  props: {
    venueReviews: {
      type: Array,
      default: () => []
    },
    userId: [String, Number],
    canMod: {
      type: Boolean,
      default: false
    },
    userType: String,
    user_id: [String, Number],
    inEdit: Boolean,
    combinedReviewImages: {
      type: Array,
      default: () => []
    },
    noMoreReviews: Boolean,
    defaultPhoto: String,
    loadingMore: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultVenueProfilePhoto.png?v=1748435337",
    } 
  },

  computed: {
    averageRating() {
      if (!this.venueReviews || this.venueReviews.length === 0) return '-';
      const total = this.venueReviews.reduce((acc, review) => acc + review.rating, 0);
      return (total / this.venueReviews.length).toFixed(1);
    },

    canAddReview() {
      return this.userType === 'user' && 
             this.user_id !== 'defaultUser' && 
             !this.inEdit;
    },

    venueReviewImages() {
      return this.combinedReviewImages
        .filter(img => img.reviewType === 'venue')
        .slice(0, 5);
    },

    shouldShowLoadMore() {
      return this.venueReviews.length > 0 && 
             !this.noMoreReviews;
    }
  },

  methods: {
    canEditReview(review) {
      return review.userID === parseInt(this.user_id);
    },

    hasUserUpvoted(review) {
      return review.userVotes?.upvotes?.includes(parseInt(this.user_id));
    },

    hasUserDownvoted(review) {
      return review.userVotes?.downvotes?.includes(parseInt(this.user_id));
    },

    getUpvoteAction(review) {
      return this.hasUserUpvoted(review) ? 'unupvote' : 'upvote';
    },

    getDownvoteAction(review) {
      return this.hasUserDownvoted(review) ? 'undownvote' : 'downvote';
    },

    getVoteScore(review) {
      const upvotes = review.userVotes?.upvotes?.length || 0;
      const downvotes = review.userVotes?.downvotes?.length || 0;
      return upvotes - downvotes;
    },

    // These methods should be implemented based on your application logic
    getPhotoFromReview(review) {
      // Implementation depends on your data structure
      return review.userPhoto || null;
    },

    getUsernameFromReview(review) {
      // Implementation depends on your data structure
      return review.username || 'Unknown User';
    },

    getUserPointsFromReview(review) {
      // Implementation depends on your data structure
      return review.userPoints || 0;
    },

    getUserRankFromReview(review) {
      // Implementation depends on your data structure
      return review.userRank || '';
    },

    getUserRankColor() {
      // Implementation depends on your ranking system
      return '#6c757d'; // Default Bootstrap secondary color
    },

    checkModFromUserID() {
      // Implementation depends on your moderator checking logic
      return false;
    },

    setUpdateID(review) {
      this.$emit('update-review', review);
    },

    setDeleteID(review) {
      this.$emit('delete-review', review);
    },

    voteReview(review, action) {
      this.$emit('vote-review', { review, action });
    },

    loadMoreReviews() {
      this.$emit('load-more-reviews');
    }
  }
}
</script>

<style scoped>
.review-image {
  width: 100%;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}

.review-image:hover {
  transform: scale(1.05);
}

.profile-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.review-item {
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 1rem;
}

.review-item:last-child {
  border-bottom: none;
}

.user-info {
  line-height: 1.4;
}

.rating-info {
  font-size: 0.9rem;
}

.review-text p {
  color: #495057;
  line-height: 1.5;
}

.review-photo-container {
  cursor: pointer;
  transition: opacity 0.2s;
}

.review-photo-container:hover {
  opacity: 0.8;
}

.action-buttons .btn {
  font-size: 0.875rem;
}

/* Mobile specific styles */
@media (max-width: 576px) {
  .mobile-fs-6 {
    font-size: 1.1rem !important;
  }
  
  .mobile-fs-7 {
    font-size: 0.75rem !important;
  }
  
  .mobile-rating-smaller-text-2 {
    font-size: 0.85rem;
  }
  
  .mobile-col-2 {
    flex: 0 0 auto;
    width: 16.66666667%;
  }
  
  .mobile-col-3 {
    flex: 0 0 auto;
    width: 25%;
  }
  
  .mobile-px-1 {
    padding-left: 0.25rem !important;
    padding-right: 0.25rem !important;
  }
  
  .mobile-ps-4 {
    padding-left: 1.5rem !important;
  }
  
  .mobile-ms-0 {
    margin-left: 0 !important;
  }
  
  .mobile-mt-1 {
    margin-top: 0.25rem !important;
  }
}
</style>