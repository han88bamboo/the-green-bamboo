<template>
  <div v-if="contentMode === 'recentActivity'">
    <!-- Header Section -->
    <header class="mb-3">
      <h4 class="text-start text-dark fs-4 fw-bold m-0 d-md-block d-none">
        Drinks tasted at this Venue
      </h4>
      <h4 class="text-start text-dark fs-6 fw-bold m-0 d-md-none mb-2">
        Drinks tasted at this Venue
      </h4>
    </header>

    <!-- Review Images Gallery -->
    <section class="mb-4" style="padding-left: 0.75rem">
      <div class="row justify-content-start align-items-start">
        <div
          v-for="(imageData, index) in bottleReviewImages"
          :key="`bottle-${index}`"
          class="col-2 col-sm-2 col-md-2 col-lg-2 px-1 d-md-block d-none"
          @click="openDetailedReviewModal(imageData)"
        >
          <div class="position-relative" style="cursor: pointer">
            <img
              :src="imageData.photo || defaultPhoto"
              :alt="`Review ${index + 1}`"
              class="review-image img-fluid"
              loading="lazy"
            />
            <span class="position-absolute top-0 end-0 m-1 badge bg-success" style="font-size: 0.6rem">
              B
            </span>
          </div>
        </div>
        
        <!-- Mobile view for images -->
        <div
          v-for="(imageData, index) in bottleReviewImages"
          :key="`bottle-mobile-${index}`"
          class="col-3 px-1 d-md-none"
          @click="openDetailedReviewModal(imageData)"
        >
          <div class="position-relative" style="cursor: pointer">
            <img
              :src="imageData.photo || defaultPhoto"
              :alt="`Review ${index + 1}`"
              class="review-image img-fluid"
              loading="lazy"
            />
            <span class="position-absolute top-0 end-0 m-1 badge bg-success" style="font-size: 0.6rem">
              B
            </span>
          </div>
        </div>
      </div>
    </section>

    <hr class="my-4" />

    <!-- Reviews Section -->
    <section v-if="hasBottleReviews">
      <article
        v-for="review in bottleReviews"
        :key="review.id"
        class="mb-4"
      >
        <div class="row">
          <!-- Review Content -->
          <div class="col-12 col-lg-9">
            <!-- User Info Header -->
            <header class="mb-3">
              <div class="row align-items-center">
                <!-- Profile Photo -->
                <div class="col-2 col-lg-1">
                  <router-link :to="`/profile/user/${review.userID}`">
                    <img
                      :src="getPhotoFromReview(review) || defaultProfilePhoto"
                      :alt="`${getUsernameFromReview(review)} profile`"
                      class="profile-image img-fluid rounded-circle"
                    />
                  </router-link>
                </div>

                <!-- User Details -->
                <div class="col-10 ps-2 ps-lg-3">
                  <div class="d-flex flex-column flex-lg-row align-items-start align-items-lg-center">
                    <div class="me-lg-3 mb-1 mb-lg-0">
                      <router-link
                        :to="`/profile/user/${review.userID}`"
                        class="text-decoration-none text-dark fw-bold"
                      >
                        @{{ getUsernameFromReview(review) }}
                      </router-link>
                    </div>
                    
                    <div class="d-flex align-items-center flex-wrap gap-2">
                      <span class="text-muted small">
                        {{ getUserPointsFromReview(review) }}
                      </span>
                      <span
                        class="badge small"
                        :style="{ backgroundColor: getUserRankColor(review) }"
                      >
                        {{ getUserRankFromReview(review) }}
                      </span>
                      <span class="text-muted small">rated</span>
                      <span class="text-warning">★</span>
                      <span class="fw-bold">{{ review.rating }}</span>
                      <span class="text-muted small">Stars</span>
                    </div>
                  </div>

                  <!-- Drink Name -->
                  <div class="mt-2">
                    <span class="text-muted small">for</span>
                    <router-link
                      :to="getBottleRoute(review)"
                      class="text-decoration-none text-dark fw-bold ms-1"
                    >
                      {{ getBottleNameFromReview(review) }}
                    </router-link>
                  </div>
                </div>
              </div>
            </header>

            <!-- Review Content -->
            <div class="mb-3">
              <p class="mb-2">{{ review.reviewDesc }}</p>
              <button
                type="button"
                class="btn btn-link p-0 text-secondary text-decoration-underline"
                @click="openDetailedReviewModal({ reviewType: 'bottle', reviewData: review })"
              >
                Detailed Review &gt;
              </button>
            </div>
          </div>

          <!-- Review Image (Desktop) -->
          <div class="col-3 d-none d-lg-block text-end">
            <img
              :src="review.photo || defaultPhoto"
              :alt="`${getBottleNameFromReview(review)} review`"
              class="review-image img-fluid"
              style="width: 125px; height: 125px; object-fit: cover; cursor: pointer"
              data-bs-toggle="modal"
              :data-bs-target="`#reviewModal${review.id}`"
            />
          </div>
        </div>

        <!-- Review Image (Mobile) -->
        <div class="row d-lg-none mt-3">
          <div class="col-12">
            <img
              :src="review.photo || defaultPhoto"
              :alt="`${getBottleNameFromReview(review)} review`"
              class="review-image img-fluid"
              style="max-width: 200px; cursor: pointer"
              data-bs-toggle="modal"
              :data-bs-target="`#reviewModal${review.id}`"
            />
          </div>
        </div>

        <!-- Image Modal -->
        <div
          class="modal fade"
          :id="`reviewModal${review.id}`"
          tabindex="-1"
          :aria-labelledby="`reviewModalLabel${review.id}`"
          aria-hidden="true"
        >
          <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" :id="`reviewModalLabel${review.id}`">
                  {{ getBottleNameFromReview(review) }} Review
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body p-0">
                <img
                  :src="review.photo || defaultPhoto"
                  :alt="`${getBottleNameFromReview(review)} review`"
                  class="img-fluid w-100"
                />
              </div>
            </div>
          </div>
        </div>

        <hr class="my-4" />
      </article>

      <!-- Load More Button -->
      <div class="text-center mb-4" v-if="!noMoreBottleReviews">
        <button
          type="button"
          class="btn btn-primary btn-lg"
          @click="loadMoreBottleReviews"
          :disabled="loadingMoreReviews"
        >
          <span v-if="loadingMoreReviews" class="spinner-border spinner-border-sm me-2" role="status">
            <span class="visually-hidden">Loading...</span>
          </span>
          Load More Drink Reviews
        </button>
      </div>
    </section>

    <!-- Empty State -->
    <section v-else class="text-center py-5">
      <div class="text-muted">
        <i class="bi bi-cup-straw fs-1 mb-3 d-block"></i>
        <h5>No drink reviews found</h5>
        <p>This venue doesn't have any drink reviews yet.</p>
      </div>
    </section>

    <!-- Delete Review Modal -->
    <div
      class="modal fade"
      id="deleteReviewModal"
      tabindex="-1"
      aria-labelledby="deleteReviewModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Success State -->
          <div v-if="successDelete" class="modal-body text-center py-4">
            <div class="text-success mb-3">
              <i class="bi bi-check-circle fs-1"></i>
            </div>
            <h5 class="text-success mb-3">Review Deleted Successfully!</h5>
            <button
              type="button"
              class="btn btn-success"
              data-bs-dismiss="modal"
              @click="reloadRoute"
            >
              Close
            </button>
          </div>

          <!-- Error State -->
          <div v-else-if="errorDelete" class="modal-body text-center py-4">
            <div class="text-danger mb-3">
              <i class="bi bi-exclamation-circle fs-1"></i>
            </div>
            <h5 class="text-danger mb-3">Failed to Delete Review</h5>
            <p class="text-muted mb-3">{{ errorDelete }}</p>
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
          </div>

          <!-- Confirmation State -->
          <div v-else>
            <div class="modal-header">
              <h5 class="modal-title" id="deleteReviewModalLabel">
                Delete Review
              </h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <p>Are you sure you want to delete this review? This action cannot be undone.</p>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Cancel
              </button>
              <button
                type="button"
                class="btn btn-danger"
                @click="deleteReview"
                :disabled="deletingReview"
              >
                <span v-if="deletingReview" class="spinner-border spinner-border-sm me-2" role="status">
                  <span class="visually-hidden">Loading...</span>
                </span>
                Delete Review
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VenueActivityTab',
  
  data() {
    return {
      // Add your data properties here
      loadingMoreReviews: false,
      deletingReview: false,
      successDelete: false,
      errorDelete: null,
    }
  },

  computed: {
    bottleReviewImages() {
      return this.combinedReviewImages
        ?.filter(img => img.reviewType === 'bottle')
        ?.slice(0, 5) || []
    },

    hasBottleReviews() {
      return this.bottleReviews && this.bottleReviews.length > 0
    }
  },

  methods: {
    getBottleRoute(review) {
      const bottleName = this.getBottleNameFromReview(review)
        .toLowerCase()
        .replace(/\s+/g, '-')
        .replace(/[^a-z0-9-]/g, '')
      
      return `/listing/view/${review.reviewTarget}/${bottleName}`
    },

    async loadMoreBottleReviews() {
      this.loadingMoreReviews = true
      try {
        // Your load more logic here
        await this.loadMoreReviews()
      } catch (error) {
        console.error('Failed to load more reviews:', error)
      } finally {
        this.loadingMoreReviews = false
      }
    },

    async deleteReview() {
      this.deletingReview = true
      this.errorDelete = null
      
      try {
        // Your delete logic here
        await this.performDeleteReview()
        this.successDelete = true
      } catch (error) {
        this.errorDelete = error.message || 'Failed to delete review'
      } finally {
        this.deletingReview = false
      }
    },

    reloadRoute() {
      // Your reload logic here
      this.$router.go(0)
    },

    // Add your other existing methods here:
    // openDetailedReviewModal, getPhotoFromReview, getUsernameFromReview, 
    // getUserPointsFromReview, getUserRankColor, getUserRankFromReview,
    // getBottleNameFromReview, etc.
  }
}
</script>

<style scoped>
.review-image {
  border-radius: 8px;
  object-fit: cover;
  aspect-ratio: 1;
}

.profile-image {
  width: 40px;
  height: 40px;
  object-fit: cover;
}

@media (max-width: 767.98px) {
  .profile-image {
    width: 35px;
    height: 35px;
  }
}

.btn-link:hover {
  text-decoration: underline !important;
}

.modal-dialog-centered {
  min-height: calc(100vh - 1rem);
}
</style>