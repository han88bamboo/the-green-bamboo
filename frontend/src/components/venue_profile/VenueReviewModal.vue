<template>
  <teleport to="body">
    <!-- Venue Review Modal -->
    <div v-if="user_id != 'defaultUser'" class="modal fade" id="venueReviewModal" tabindex="-1"
      aria-labelledby="venueReviewModalLabel" aria-hidden="true" data-bs-backdrop="static">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">

          <!-- Success Message -->
          <template v-if="successSubmission">
            <div class="modal-body text-success fst-italic fw-bold fs-3 text-center p-5">
              <span v-if="!inEdit">Your review has successfully been submitted!</span>
              <span v-else>Your review has successfully been updated!</span>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="reloadRoute"
                data-bs-dismiss="modal">Close</button>
            </div>
          </template>

          <!-- Error Message -->
          <template v-else-if="errorSubmission">
            <div class="modal-body text-danger fw-bold fs-6 text-center p-4">
              <div v-if="errorMessage">
                <p v-if="!inEdit">An error occurred while attempting to submit, please try again!</p>
                <p v-else>An error occurred while attempting to update, please try again!</p>
                <button class="btn primary-btn btn-sm" @click="reset">
                  <span class="fs-7 fst-italic">Retry here!</span>
                </button>
              </div>
              <div v-if="duplicateEntry">
                <p v-if="!inEdit">You've already submitted a review for this venue!</p>
                <p v-else>There is no review for this venue!</p>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            </div>
          </template>

          <!-- Add/Edit Review Form -->
          <template v-else-if="addingVenueReview">
            <div class="modal-header" style="background-color:#F0B358">
              <h5 class="modal-title" id="venueReviewModalLabel" style="color: black; font-weight:bold;">
                {{ inEdit ? 'Edit Your Review' : 'Add Your Review' }}
              </h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body px-4">
              <div class="row">
                <div class="col-md-4">
                  <p class="text-start mb-2 fw-bold">Photos</p>
                  <input class="form-control" @change="onFilesChange" type="file" id="venueReviewPhotos"
                    accept="image/*" multiple style="display: none;">
                  <!-- <label for="venueReviewPhotos" class="btn btn-outline-dark w-100 mb-2">
                    Click to Upload
                  </label> -->
                  <label for="venueReviewPhotos">
                    <div class="mobile-review-svg-button">
                      <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                        <circle cx="8.5" cy="8.5" r="1.5"></circle>
                        <path d="M20.4 14.5L16 10 4 20"></path>
                        <circle cx="19" cy="19" r="3" fill="black"></circle>
                        <line x1="18" y1="19" x2="20" y2="19" stroke="white" stroke-width="1"></line>
                        <line x1="19" y1="18" x2="19" y2="20" stroke="white" stroke-width="1"></line>
                      </svg>
                    </div>
                  </label>

                  <div class="row" v-if="selectedImagesForReview.length > 0 || reviewImages64.length > 0">
                    <div
                      v-for="(image, index) in (selectedImagesForReview.length > 0 ? selectedImagesForReview : reviewImages64)"
                      :key="index" class="col-6 mb-2">
                      <img :src="image" alt="Review Image" class="img-fluid rounded" />
                    </div>
                  </div>
                  <button v-if="reviewImages64.length > 0 || selectedImagesForReview.length > 0"
                    class="btn btn-sm btn-danger mt-2" @click="clearPhoto">
                    Clear Photos
                  </button>
                </div>

                <div class="col-md-8">
                  <!-- Review Text -->
                  <div class="mb-3">
                    <p class="text-start mb-2 fw-bold">Review<span class="text-danger">*</span></p>
                    <textarea v-model="reviewDesc" class="form-control" id="venueReviewTextarea" rows="6"
                      placeholder="Min 20 characters"></textarea>
                    <p v-if="reviewDescError" class="text-danger text-start mb-0 mt-1">{{ reviewDescError }}</p>
                  </div>

                  <!-- Rating Slider -->
                  <div class="mb-3">
                    <p class="text-start mb-1 fw-bold">My Rating<span class="text-danger">*</span></p>
                    <div class="text-start mb-2">
                      <span style="color:#F0B358;">★</span>
                      <span style="font-weight:bold;">{{ rating }}</span> Stars
                    </div>
                    <div class="row align-items-center">
                      <div class="col-auto pe-0">
                        <label for="customRange" class="form-label fw-bold">1</label>
                      </div>
                      <div class="col">
                        <div class="slider-container" style="position: relative;">
                          <input v-model="rating" type="range" class="form-range" min="1" max="10" step="0.1"
                            id="customRange">
                          <div class="tickmarks">
                            <span v-for="i in 9" :key="i" class="tick" :style="{ left: (i * 10) + '%' }">|</span>
                          </div>
                        </div>
                      </div>
                      <div class="col-auto ps-0">
                        <label for="customRange" class="form-label fw-bold">10</label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- Modal Footer with Action Buttons -->
            <!--
              FIX: Removed inefficient v-for and filter from the template.
              This logic should be handled by a computed property in the script.
              Assuming a computed property 'currentUserReview' will be created.
            -->
            <div class="modal-footer d-flex justify-content-between">
              <button v-if="inEdit" class="btn btn-danger py-1 mobile-fs-7"
                @click="setDeleteID(reviewToEdit)" data-bs-toggle="modal" data-bs-target="#deleteReview">
                Delete Review
              </button>
              <span v-else></span> <!-- Placeholder to keep justify-content-between working -->
              <div>
                <button type="button" class="btn secondary-btn-less-round-inverse me-2"
                  data-bs-dismiss="modal">Close</button>
                <button v-if="!inEdit" type="button" @click="addVenueReview" class="btn secondary-btn-less-round">
                  Submit Review
                </button>
                <button v-else type="button" @click="editVenueReview" class="btn secondary-btn-less-round">
                  Update Review
                </button>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script>
import axios from 'axios';

export default {
  name: 'VenueReviewModal',
  props: {
    user_id: {
      type: [String, Number],
      required: true,
    },
    venueId: {
      type: [String, Number],
      required: true,
    },
    reviewToEdit: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      addingVenueReview: true,
      successSubmission: false,
      errorSubmission: false,
      errorMessage: '',
      duplicateEntry: false,

      reviewDesc: '',
      reviewDescError: '',
      rating: 5,

      selectedImagesForReview: [],
      reviewImages64: [],
    };
  },
  computed: {
    inEdit() {
      return !!this.reviewToEdit;
    },
  },
  methods: {
    reloadRoute() {
      this.$router.go();
    },
    reset() {
      this.errorSubmission = false;
      this.errorMessage = '';
      this.duplicateEntry = false;
      this.addingVenueReview = true;
    },
    onFilesChange(event) {
      const files = event.target.files;
      if (!files.length) return;

      this.selectedImagesForReview = [];

      for (let i = 0; i < files.length; i++) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.selectedImagesForReview.push(e.target.result);
        };
        reader.readAsDataURL(files[i]);
      }
    },
    clearPhoto() {
      this.selectedImagesForReview = [];
      this.reviewImages64 = [];
      const input = document.getElementById('venueReviewPhotos');
      if (input) {
        input.value = '';
      }
    },
    validateReview() {
      this.reviewDescError = '';
      if (this.reviewDesc.length < 20) {
        this.reviewDescError = 'Review must be at least 20 characters long.';
        return false;
      }
      return true;
    },
    async addVenueReview() {
      if (!this.validateReview()) {
        return;
      }

      const payload = {
        venueID: this.venueId,
        userID: this.user_id,
        rating: this.rating,
        reviewDesc: this.reviewDesc,
        createdDate: new Date().toISOString(),
        photos: this.selectedImagesForReview,
      };

      try {
        const response = await axios.post('http://localhost:5021/create-review/createVenueReview', payload);
        if (response.data.code === 201) {
          this.addingVenueReview = false;
          this.successSubmission = true;
        } else {
          this.errorMessage = response.data.message || 'An unknown error occurred.';
          if (response.data.code === 400) {
            this.duplicateEntry = true;
          }
          this.errorSubmission = true;
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.message || error.message || 'An error occurred while submitting your review.';
        this.errorSubmission = true;
      }
    },
    async editVenueReview() {
      if (!this.validateReview() || !this.reviewToEdit) {
        return;
      }

      const payload = {
        userID: this.user_id,
        venueID: this.venueId,
        rating: this.rating,
        reviewDesc: this.reviewDesc,
        createdDate: new Date(this.reviewToEdit.createdDate).toISOString(),
        photos: this.selectedImagesForReview.length > 0 ? this.selectedImagesForReview : this.reviewImages64,
      };

      try {
        const response = await axios.put(`http://localhost:5022/edit-review/updateVenueReview/${this.reviewToEdit.id}`, payload);
        if (response.data.code === 200) {
          this.addingVenueReview = false;
          this.successSubmission = true;
        } else {
          this.errorMessage = response.data.message || 'An unknown error occurred.';
          this.errorSubmission = true;
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.message || error.message || 'An error occurred while updating your review.';
        this.errorSubmission = true;
      }
    },
    async deleteVenueReview(reviewId) {
      try {
        const response = await axios.delete(`http://localhost:5023/delete-review/deleteVenueReview/${reviewId}`);
        if (response.data.code === 200) {
          this.reloadRoute();
        } else {
          this.errorMessage = response.data.message || 'An unknown error occurred.';
          this.errorSubmission = true;
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.message || error.message || 'An error occurred while deleting your review.';
        this.errorSubmission = true;
      }
    },
    setDeleteID(review) {
      if (review) {
        this.deleteVenueReview(review.id);
      }
    },
    populateFormForEdit(newReview) {
      console.log('Populating form with review data:', newReview);
      if (newReview && Object.keys(newReview).length > 0) {
        this.reviewDesc = newReview.reviewDesc || '';
        this.rating = newReview.rating || 5;
        this.reviewImages64 = newReview.photos || [];
      } else {
        this.reviewDesc = '';
        this.rating = 5;
        this.reviewImages64 = [];
      }
      this.selectedImagesForReview = [];
    }
  },
  watch: {
    reviewToEdit(newVal) {
      this.populateFormForEdit(newVal);
    },
  },
};
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.review-preview-photo {
  width: 100%;
  height: auto;
  object-fit: cover;
  border-radius: 0.25rem;
}

.slider-container {
  position: relative;
  width: 100%;
}

.tickmarks {
  position: absolute;
  top: 10px;
  /* Adjust to center with the range thumb */
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 0 10px;
  /* Align with range input padding */
  box-sizing: border-box;
  pointer-events: none;
  /* Makes sure you can still interact with the slider */
}

.tick {
  position: absolute;
  color: #ced4da;
  font-size: 12px;
}
</style>
