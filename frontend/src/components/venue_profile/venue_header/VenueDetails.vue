<!-- VenueDetails.vue -->
<template>
  <div class="col-lg-9 col-12 text-start ps-lg-5 ps-1 mobile-col-7">
    <div class="row">
      <!-- Country Section -->
      <div class="col-7 pe-0 ps-0">
        <!-- Edit Mode -->
        <div v-if="isEditing">
          <label for="editCountryInput">Country of Origin</label>
          <input 
            type="text" 
            class="form-control mb-3" 
            id="editCountryInput"
            aria-describedby="originLocation" 
            v-model="localEditData.country"
            @input="handleInputChange"
            :class="{ 'is-invalid': errors.country }"
          >
          <div v-if="errors.country" class="invalid-feedback">
            {{ errors.country }}
          </div>
        </div>

        <!-- View Mode -->
        <div v-else>
          <template v-if="isLoading">
            <div class="shimmer shimmer-line-h5 mobile-view-hide"></div>
            <div class="shimmer shimmer-line-h6 mobile-view-show mb-1"></div>
          </template>
          <template v-else>
            <h5 class="text-body-secondary mobile-view-hide">
              {{ (venue && venue.originLocation) || 'Unknown' }}
            </h5>
            <h6 class="text-body-secondary mobile-view-show mb-1">
              {{ (venue && venue.originLocation) || 'Unknown' }}
            </h6>
          </template>
        </div>
      </div>

      <!-- Actions Slot (for claim venue, edit profile buttons) -->
      <div class="col-5">
        <slot name="actions">

        </slot>
      </div>

      <!-- <div class="d-flex justify-content-between align-items-end mt-3" style="border: 1px solid red;">
        <slot name="details">

        </slot>
      </div> -->
    </div>

    <!-- Venue Name Section -->
    <div class="row">
      <div class="col-12 pe-0 ps-0">
        <!-- Edit Mode -->
        <div v-if="isEditing">
          <label for="venueNameInput">Venue Name</label>
          <input 
            type="text" 
            class="form-control mb-3" 
            id="venueNameInput"
            aria-describedby="venueName" 
            v-model="localEditData.venueName"
            @input="handleInputChange"
            :class="{ 'is-invalid': errors.venueName }"
            maxlength="100"
          >
          <div v-if="errors.venueName" class="invalid-feedback">
            {{ errors.venueName }}
          </div>
          <div class="form-text">
            {{ localEditData.venueName.length }}/100 characters
          </div>
        </div>

        <!-- View Mode -->
        <div v-else class="ps-0 pe-0">
          <template v-if="isLoading">
            <div class="shimmer shimmer-line-h3 mobile-view-hide"></div>
            <div class="shimmer shimmer-line-h4 mobile-view-show mb-1"></div>
          </template>
          <template v-else>
            <h3 class="text-body-secondary mobile-view-hide">
              <b>{{ (venue && venue.venueName) || 'Venue Name Not Set' }}</b>
            </h3>
            <h4 class="text-body-secondary mobile-view-show pe-0 ps-0 mb-1">
              <b>{{ (venue && venue.venueName) || 'Venue Name Not Set' }}</b>
            </h4>
          </template>
        </div>
      </div>
    </div>

    <!-- Venue Type Section -->
    <div class="row">
      <div class="col-12 pe-lg-0 ps-0">
        <!-- Edit Mode -->
        <div v-if="isEditing">
          <label for="venueTypeInput">Venue Type</label>
          <select 
            class="form-select mb-3" 
            id="venueTypeInput"
            v-model="localEditData.venueType"
            @change="handleInputChange"
            :class="{ 'is-invalid': errors.venueType }"
          >
            <option value="">Select venue type</option>
            <option v-for="type in venueTypes" :key="type.value" :value="type.value">
              {{ type.label }}
            </option>
          </select>
          <div v-if="errors.venueType" class="invalid-feedback">
            {{ errors.venueType }}
          </div>
        </div>

        <!-- View Mode -->
        <div v-else class="ps-0 pe-0">
          <template v-if="isLoading">
            <div class="shimmer shimmer-line-p"></div>
          </template>
          <p v-else class="text-body-secondary fs m-0 mobile-rating-smaller-text-2">
            <i>{{ (venue && venue.venueType) || 'N/A' }}</i>
          </p>
        </div>
      </div>
    </div>

    <!-- Venue Description Section -->
    <div class="row scrollable">
      <div class="col-12 pe-lg-0 ps-0">
        <!-- Edit Mode -->
        <div v-if="isEditing">
          <label for="venueDescInput">Venue Description</label>
          <textarea 
            class="form-control mb-3" 
            id="venueDescInput"
            aria-describedby="venueDesc" 
            v-model="localEditData.venueDesc"
            @input="handleInputChange"
            :class="{ 'is-invalid': errors.venueDesc }"
            rows="4"
            maxlength="500"
            placeholder="Describe your venue, its atmosphere, specialties, and what makes it unique..."
          ></textarea>
          <div v-if="errors.venueDesc" class="invalid-feedback">
            {{ errors.venueDesc }}
          </div>
          <div class="form-text">
            {{ localEditData.venueDesc.length }}/500 characters
          </div>
        </div>

        <!-- View Mode -->
        <div v-else class="ps-0 pe-0">
          <template v-if="isLoading">
            <div class="shimmer shimmer-line-desc w-90"></div>
            <div class="shimmer shimmer-line-desc w-80"></div>
            <div class="shimmer shimmer-line-desc w-70"></div>
          </template>
          <div v-else>
            <div v-if="venue && venue.venueDesc && venue.venueDesc.length > descriptionLimit">
              <!-- <p v-if="!showFullDescription" class="text-body-secondary fs m-0 mobile-rating-smaller-text-2">
                {{ truncatedDescription }}
                <a @click="showFullDescription = true" 
                   class="text-primary fw-bold text-decoration-none"
                   style="cursor: pointer;">
                  (Read More)
                </a>
              </p> -->
              <p class="text-body-secondary fs m-0 mobile-rating-smaller-text-2">
                {{ venue.venueDesc }}
              </p>
            </div>
            <p v-else class="text-body-secondary fs m-0 mobile-rating-smaller-text-2">
              {{ (venue && venue.venueDesc) || 'Claim the business to add your story!' }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- <div class="row">
      <div class="col-12 pe-0 ps-0">
        <slot name="details"></slot>
      </div>
    </div> -->

    <!-- Validation Summary (shown in edit mode if there are errors) -->
    <div v-if="isEditing && hasErrors" class="row mt-2">
      <div class="col-12">
        <div class="alert alert-danger">
          <h6 class="alert-heading">Please fix the following errors:</h6>
          <ul class="mb-0">
            <li v-for="(error, field) in errors" :key="field">{{ error }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VenueDetails',

  props: {
    isLoading: Boolean,
    // Venue object containing all venue information
    venue: {
      type: Object,
      default: () => ({
        venueName: '',
        originLocation: '',
        venueType: '',
        venueDesc: '',
        photo: ''
      })
    },

    // Whether component is in edit mode
    isEditing: {
      type: Boolean,
      default: false
    },

    // Initial edit data (when entering edit mode)
    editData: {
      type: Object,
      default: () => ({})
    },

    // Character limit for description truncation
    descriptionLimit: {
      type: Number,
      default: 150
    },

    // Available venue types
    venueTypes: {
      type: Array,
      default: () => [
        { value: 'restaurant', label: 'Restaurant' },
        { value: 'bar', label: 'Bar' },
        { value: 'cafe', label: 'Cafe' },
        { value: 'pub', label: 'Pub' },
        { value: 'lounge', label: 'Lounge' },
        { value: 'nightclub', label: 'Nightclub' },
        { value: 'brewery', label: 'Brewery' },
        { value: 'winery', label: 'Winery' },
        { value: 'hotel', label: 'Hotel' },
        { value: 'resort', label: 'Resort' },
        { value: 'other', label: 'Other' }
      ]
    },

    // Validation rules
    validationRules: {
      type: Object,
      default: () => ({
        venueName: { required: true, minLength: 2, maxLength: 100 },
        country: { required: true, minLength: 2 },
        venueType: { required: false },
        venueDesc: { required: false, maxLength: 500 }
      })
    }
  },

  data() {
    return {
      // Local copy of edit data to avoid direct prop mutation
      localEditData: {
        country: '',
        venueName: '',
        venueType: '',
        venueDesc: ''
      },

      // Validation errors
      errors: {},

      // Debounce timer for validation
      validationTimer: null,

      // Track previous venue description for watch
      previousVenueDesc: ''
    }
  },

  computed: {
    /**
     * Truncated description for "read more" functionality
     */
    truncatedDescription() {
      if (!this.venue || !this.venue.venueDesc) return ''
      
      return this.venue.venueDesc.length > this.descriptionLimit
        ? this.venue.venueDesc.slice(0, this.descriptionLimit) + '...'
        : this.venue.venueDesc
    },

    /**
     * Check if there are any validation errors
     */
    hasErrors() {
      return Object.keys(this.errors).length > 0
    },

    /**
     * Check if the edit data is valid
     */
    isValid() {
      return !this.hasErrors
    }
  },

  watch: {
    // Watch for changes in edit mode
    isEditing: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.initializeEditData()
        } else {
          this.resetComponent()
        }
      }
    },

    // Watch for changes in edit data prop
    editData: {
      deep: true,
      handler(newVal) {
        if (newVal && Object.keys(newVal).length > 0) {
          this.localEditData = { ...this.localEditData, ...newVal }
        }
      }
    },

    // Watch venue changes to reset description state
    venue: {
      deep: true,
      handler(newVenue) {
        if (newVenue && newVenue.venueDesc !== this.previousVenueDesc) {
          this.showFullDescription = false
          this.previousVenueDesc = newVenue.venueDesc
        }
      }
    }
  },

  methods: {
    /**
     * Initialize edit data when entering edit mode
     */
    initializeEditData() {
      this.localEditData = {
        country: this.editData.country || (this.venue && this.venue.originLocation) || '',
        venueName: this.editData.venueName || (this.venue && this.venue.venueName) || '',
        venueType: this.editData.venueType || (this.venue && this.venue.venueType) || '',
        venueDesc: this.editData.venueDesc || (this.venue && this.venue.venueDesc) || ''
      }
      
      // Clear any existing errors
      this.errors = {}
    },

    /**
     * Handle input changes with debounced validation
     */
    handleInputChange() {
      // Clear existing timer
      if (this.validationTimer) {
        clearTimeout(this.validationTimer)
      }

      // Emit immediate change for parent reactivity
      this.$emit('update:editData', { ...this.localEditData })

      // Debounced validation (300ms delay)
      this.validationTimer = setTimeout(() => {
        this.validateField()
      }, 300)
    },

    /**
     * Validate current field data
     */
    validateField() {
      const newErrors = {}

      // Validate venue name
      if (this.validationRules.venueName?.required && !this.localEditData.venueName.trim()) {
        newErrors.venueName = 'Venue name is required'
      } else if (this.localEditData.venueName.length < (this.validationRules.venueName?.minLength || 2)) {
        newErrors.venueName = `Venue name must be at least ${this.validationRules.venueName?.minLength || 2} characters`
      } else if (this.localEditData.venueName.length > (this.validationRules.venueName?.maxLength || 100)) {
        newErrors.venueName = `Venue name must be less than ${this.validationRules.venueName?.maxLength || 100} characters`
      }

      // Validate country
      if (this.validationRules.country?.required && !this.localEditData.country.trim()) {
        newErrors.country = 'Country is required'
      } else if (this.localEditData.country.length < (this.validationRules.country?.minLength || 2)) {
        newErrors.country = `Country must be at least ${this.validationRules.country?.minLength || 2} characters`
      }

      // Validate venue type
      if (this.validationRules.venueType?.required && !this.localEditData.venueType) {
        newErrors.venueType = 'Please select a venue type'
      }

      // Validate description
      if (this.localEditData.venueDesc.length > (this.validationRules.venueDesc?.maxLength || 500)) {
        newErrors.venueDesc = `Description must be less than ${this.validationRules.venueDesc?.maxLength || 500} characters`
      }

      this.errors = newErrors

      // Emit validation status
      this.$emit('validation-changed', {
        isValid: Object.keys(newErrors).length === 0,
        errors: newErrors,
        data: this.localEditData
      })
    },

    /**
     * Public method to validate all fields (called by parent)
     */
    validate() {
      this.validateField()
      return this.isValid
    },

    /**
     * Public method to get current edit data
     */
    getEditData() {
      return { ...this.localEditData }
    },

    /**
     * Reset component state
     */
    resetComponent() {
      this.showFullDescription = false
      this.errors = {}
      
      if (this.validationTimer) {
        clearTimeout(this.validationTimer)
        this.validationTimer = null
      }
    },

    /**
     * Public method to set edit data (called by parent)
     */
    setEditData(data) {
      this.localEditData = { ...this.localEditData, ...data }
      this.$emit('update:editData', this.localEditData)
    },

    /**
     * Toggle description display
     */
    toggleDescription() {
      this.showFullDescription = !this.showFullDescription
    }
  },

  beforeUnmount() {
    // Clean up timer
    if (this.validationTimer) {
      clearTimeout(this.validationTimer)
    }
  },

  // Expose public methods
  expose: ['validate', 'getEditData', 'setEditData', 'toggleDescription']
}
</script>

<style scoped>
/* Form validation styles */
.is-invalid {
  border-color: #dc3545;
}

.invalid-feedback {
  display: block;
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.form-text {
  color: #6c757d;
  font-size: 0.875rem;
}

/* Read more/less link styling */
.text-primary {
  color: #0d6efd !important;
}

.text-primary:hover {
  color: #0b5ed7 !important;
  text-decoration: underline !important;
}

/* Character counter styling */
.form-text {
  text-align: right;
  margin-top: -0.5rem;
  margin-bottom: 1rem;
}

/* Mobile responsive adjustments */
@media (max-width: 768px) {
  .mobile-view-hide {
    display: none !important;
  }
  
  .mobile-view-show {
    display: block !important;
  }
  
  .mobile-rating-smaller-text-2 {
    font-size: 0.875rem;
  }
  
  .form-control, .form-select {
    font-size: 16px; /* Prevents zoom on iOS */
  }
}

/* Scrollable description area */
.scrollable {
  max-height: none; /* Remove any height constraints */
}

/* Alert styling */
.alert {
  border-radius: 0.375rem;
  padding: 1rem;
}

.alert-heading {
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.alert ul {
  padding-left: 1.5rem;
}

/* Animation for validation errors */
.invalid-feedback {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Focus states for better accessibility */
.form-control:focus,
.form-select:focus {
  border-color: #86b7fe;
  outline: 0;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

/* Custom styling for required fields */
label[for]:after {
  content: " *";
  color: #dc3545;
  font-weight: bold;
}

/* Remove asterisk for optional fields */
label[for="venueTypeInput"]:after,
label[for="venueDescInput"]:after {
  content: none;
}

/* Shimmer loading effect */
@keyframes placeholderShimmer {
  0% {
    background-position: -468px 0;
  }
  100% {
    background-position: 468px 0;
  }
}

.shimmer {
  animation: placeholderShimmer 1.2s linear infinite forwards;
  background: #f6f7f8;
  background-image: linear-gradient(to right, #f6f7f8 0%, #edeef1 20%, #f6f7f8 40%, #f6f7f8 100%);
  background-repeat: no-repeat;
  background-size: 800px 100%;
  border-radius: 4px;
  display: inline-block;
  position: relative;
  height: 1em;
  width: 100%;
}

.shimmer-line-h5 {
  height: 1.25rem;
  width: 40%;
  margin-bottom: 0.5rem;
}

.shimmer-line-h6 {
  height: 1rem;
  width: 40%;
  margin-bottom: 0.25rem;
}

.shimmer-line-h3 {
  height: 2rem;
  width: 70%;
  margin-bottom: 0.5rem;
}

.shimmer-line-h4 {
  height: 1.75rem;
  width: 70%;
  margin-bottom: 0.5rem;
}

.shimmer-line-p {
  height: 1rem;
  width: 30%;
  margin-bottom: 1rem;
}

.shimmer-line-desc {
  height: 1rem;
  margin-bottom: 0.5rem;
}

.shimmer-line-desc.w-90 { width: 90%; }
.shimmer-line-desc.w-80 { width: 80%; }
.shimmer-line-desc.w-70 { width: 70%; }
</style>