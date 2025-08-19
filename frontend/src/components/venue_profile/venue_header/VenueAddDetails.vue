<template>
  <!-- Additional business details and action buttons -->
  <div class="row mt-3 align-items-center">
    <!-- Left Column: Text Info -->
    <!-- Display Mode: display additional information such as Year, Website, Reservations -->
    <div class="col-lg-8 col-md-7">
      <div v-if="!isEditing" style="text-align: left;">
        <p class="mb-1">
          <strong>Year Opened:</strong>
          {{ venue.yearOpened && venue.yearOpened.toString().trim() ? venue.yearOpened : 'n/a' }}
          |
          <strong>Open for Reservations:</strong> {{ venue.reservations ? 'Yes' : 'No' }}
        </p>
        <p class="mb-1">
          <strong>Website:</strong>
          <a :href="venue.website" target="_blank">
            {{ venue.website && venue.website.toString().trim() ? venue.website : 'n/a' }}
          </a>
          |
          <strong>Instagram:</strong> 
          <template v-if="formatSocialHandle(venue.instagram, 'instagram')">
            <a :href="venue.instagram" target="_blank">
              {{ formatSocialHandle(venue.instagram, 'instagram') }}
            </a>
          </template>
          <template v-else>
            n/a
          </template>
          | 
          <strong>Facebook:</strong>
          <template v-if="formatSocialHandle(venue.facebook, 'facebook')">
            <a :href="venue.facebook" target="_blank">
              {{ formatSocialHandle(venue.facebook, 'facebook') }}
            </a>
          </template>
          <template v-else>
            n/a
          </template>
          | 
          <strong>tiktok:</strong>
          <template v-if="formatSocialHandle(venue.tiktok, 'tiktok')">
            <a :href="venue.tiktok" target="_blank">
              {{ formatSocialHandle(venue.tiktok, 'tiktok') }}
            </a>
          </template>
          <template v-else>
            n/a
          </template>
        </p>
        <p class="mb-0">
          <strong>Phone:</strong> 
          {{ venue.phone && venue.phone.toString().trim() ? venue.phone : 'n/a' }}
          | 
          <strong>WhatsApp:</strong>
          <a 
            v-if="venue.whatsappNumber && venue.whatsappNumber.toString().trim()" 
            :href="`https://wa.me/${venue.whatsappNumber.replace(/[^0-9]/g, '')}`" 
            target="_blank"
          >
            {{ venue.whatsappNumber }}
          </a>
          <span v-else>n/a</span>
        </p>
      </div>

      <!-- Edit Mode: Inputs for Year, Website, Reservations -->
      <div v-else class="row mb-3">
        <div class="col-6">
          <label for="yearOpenedInput">Year Opened</label>
          <input type="number" class="form-control mb-3" id="yearOpenedInput" v-model="localEditData.yearOpened" @input="handleInputChange" />
        </div>
        <div class="col-6">
          <label for="websiteInput">Website</label>
          <input type="url" class="form-control mb-3" id="websiteInput" v-model="localEditData.website" @input="handleInputChange" />
        </div>
        <div class="col-6">
          <label for="instagramInput">Instagram</label>
          <input type="url" class="form-control mb-3" id="instagramInput" v-model="localEditData.instagram"
            placeholder="https://www.instagram.com/yourhandle" @input="handleInputChange" />
        </div>
        <div class="col-6">
          <label for="facebookInput">Facebook</label>
          <input type="url" class="form-control mb-3" id="facebookInput" v-model="localEditData.facebook"
            placeholder="https://www.facebook.com/yourpage" @input="handleInputChange" />
        </div>
        <div class="col-6">
          <label for="tiktokInput">TikTok</label>
          <input type="url" class="form-control mb-3" id="tiktokInput" v-model="localEditData.tiktok"
            placeholder="https://www.tiktok.com/@yourhandle" @input="handleInputChange" />
        </div>
        <div class="col-6">
          <label for="emailInput">Email</label>
          <input type="email" class="form-control mb-3" id="emailInput" v-model="localEditData.email" @input="handleInputChange" />
        </div>
        <div class="col-6">
          <label for="phoneNumberInput">Phone No.</label>
          <input type="tel" class="form-control mb-3" id="phoneNumberInput" v-model="localEditData.phoneNumber" @input="handleInputChange" />
        </div>
        <div class="col-6">
          <label for="whatsappNumberInput">WhatsApp</label>
          <input type="tel" class="form-control mb-3" id="whatsappNumberInput" v-model="localEditData.whatsappNumber" @input="handleInputChange" />
        </div>
        <div class="col-12 d-flex align-items-center">
          <label class="me-3 mb-0">Open for Reservations:</label>
          <input type="checkbox" id="openForReservationsCheckbox" v-model="localEditData.openForReservations" :true-value="true"
            :false-value="false" @change="handleInputChange" />
          <label for="openForReservationsCheckbox" class="ms-2">
            {{ localEditData.openForReservations === true ? 'Yes' : 'No' }}
          </label>
        </div>
      </div>

    </div>

    <!-- Right Column: Buttons -->
    <div class="col-lg-4 col-md-5">
      <div class="d-flex align-items-center justify-content-md-end justify-content-center gap-2 mt-3 mt-md-0">
        <button class="btn fw-bold action-btn" @click="$emit('follow-clicked')" :disabled="isEditing || isOwner">
          {{ isFollowing ? '- Unfollow' : '+ Follow' }}
        </button>
        <button class="btn fw-bold action-btn" data-bs-toggle="modal" data-bs-target="#venueReviewModal" :disabled="isEditing || isOwner">
          Review Venue
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VenueAddDetails',
  emits: ["follow-clicked", 'review-clicked', 'update:editData'], // declare emits
  props: {
    loading: Boolean,

    isOwner: {
      type: Boolean,
      default: false
    },

    isAdmin: {
      type: Boolean,
      default: false
    },

    // Whether component is in edit mode
    isEditing: {
      type: Boolean,
      default: false
    },

    isFollowing: Boolean,
    // Venue object containing all venue information
    venue: {
      type: Object,
      default: () => ({
        id: null, // Ensure venue ID is available for checks
        updates: [],
        venueName: '',
        claimStatus: false,
        originLocation: '',
        venueType: '',
        venueDesc: '',
        photo: '',
        address: '',
        loc: {
          long: 0,
          lat: 0,
        },
        yearOpened: '',
        website: '',
        reservations: '',
        instagram: '',
        phone: ''
      })
    },
  },

  data() {
    return {
      localEditData: {
        yearOpened: null,
        website: '',
        instagram: '',
        facebook: '',
        tiktok: '',
        email: '',
        phoneNumber: '',
        whatsappNumber: '',
        openForReservations: false
      }
    }
  },

  watch: {
    isEditing: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.initializeEditData();
        }
      }
    },
  },

  methods: {
    initializeEditData() {
      this.localEditData.yearOpened = this.venue.yearOpened || null;
      this.localEditData.website = this.venue.website || '';
      this.localEditData.instagram = this.venue.instagram || '';
      this.localEditData.facebook = this.venue.facebook || '';
      this.localEditData.tiktok = this.venue.tiktok || '';
      this.localEditData.email = this.venue.email || '';
      this.localEditData.phoneNumber = this.venue.phone || '';
      this.localEditData.whatsappNumber = this.venue.whatsappNumber || '';
      this.localEditData.openForReservations = this.venue.reservations || false;
    },
    getEditData() {
      return this.localEditData;
    },
    handleInputChange() {
      this.$emit('update:editData', this.localEditData);
    },
    formatSocialHandle(url, platform) {
        if (!url) return null;
        
        const patterns = {
            instagram: {
                regex: /instagram\.com\/([^/?]+)/,
                format: (handle) => `@${handle}`
            },
            facebook: {
                regex: /facebook\.com\/([^/?]+)/,
                format: (handle) => handle
            },
            tiktok: {
                regex: /tiktok\.com\/@([^/?]+)/,
                format: (handle) => `@${handle}`
            }
        };

        const config = patterns[platform.toLowerCase()];
        if (!config) return null;
        
        const match = url.match(config.regex);
        return match ? config.format(match[1]) : null;
    }
  },
  expose: ['getEditData']
}
</script>

<style scoped>
.action-btn {
  color: #fff;
  background-color: #ff3e31;
  border-radius: 10px;
}

.action-btn:hover {
  background-color: #c22a1f;
}
</style>