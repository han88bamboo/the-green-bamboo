<template>
    <div class="row align-items-start mb-4">
        <!-- Image Column -->
        <div class="col-lg-2 col-md-3 col-4 text-center">
            <img :src="newPhotoPreview || venue.photo || defaultProfilePhoto" alt="Venue Profile Photo"
                class="img-fluid rounded" style="width: 150px; height: 150px; object-fit: cover;">
            
            <div v-if="isEditing" class="mt-2">
                <input type="file" ref="photoInput" @change="handlePhotoChange" accept="image/*" class="d-none">
                <button type="button" class="btn btn-sm btn-secondary" @click="$refs.photoInput.click()">
                    Change
                </button>
            </div>
        </div>

        <!-- Details and Actions Column -->
        <div class="col-lg-10 col-md-9 col-8">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <h5 class="text-body-secondary mb-0">{{ venue.originLocation }}</h5>
                    <h1 class="fw-bold">{{ venue.venueName }}</h1>
                    <p class="text-muted">{{ venue.venueType }}</p>
                </div>
                <div class="text-end">
                    <div v-if="isSelfView || isPowerView">
                        <button v-if="!isEditing" type="button" class="btn btn-outline-primary" @click="$emit('toggle-edit')">
                            Edit Profile
                        </button>
                        <button v-else type="button" class="btn btn-success" @click="$emit('save-profile')">
                            Save Profile
                        </button>
                    </div>
                    <div v-else>
                        <p v-if="!venue.claimStatus" class="text-primary text-decoration-underline fst-italic" style="cursor: pointer;" @click="$emit('claim-business')">
                            Claim This Business
                        </p>
                        <p v-else class="text-success fw-bold fst-italic">
                            ✓ Verified Venue
                        </p>
                    </div>
                </div>
            </div>

            <div class="mt-2">
                <p>
                    {{ displayedDescription }}
                    <span v-if="venue.venueDesc && venue.venueDesc.length > 150" @click="toggleDescription" class="text-primary" style="cursor: pointer;">
                        {{ showFullDescription ? '(Read Less)' : '(Read More)' }}
                    </span>
                </p>
            </div>

            <div class="d-flex justify-content-between align-items-end mt-3">
                <div>
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
                        <strong>Instagram:</strong> {{ venue.instagram && venue.instagram.toString().trim() ? venue.instagram : 'n/a' }}
                    </p>
                    <p class="mb-0">
                        <strong>Phone:</strong> {{ venue.phone && venue.phone.toString().trim() ? venue.phone : 'n/a' }}
                    </p>
                </div>
                <div class="d-flex align-items-center gap-2">
                    <button class="btn btn-danger fw-bold" @click="$emit('follow-clicked')">
                        + Follow
                    </button>
                    <button class="btn btn-danger fw-bold" @click="$emit('review-clicked')">
                        Review Venue
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'VenueHeader',
  props: {
    venue: {
      type: Object,
      required: true,
    },
    isSelfView: Boolean,
    isPowerView: Boolean,
    isEditing: Boolean,
  },
  data() {
    return {
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultVenueProfilePhoto.png?v=1748435337",
      showFullDescription: true, // To match the image showing "(Read Less)"
      newPhotoPreview: null,
    };
  },
  methods: {
    handlePhotoChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.newPhotoPreview = URL.createObjectURL(file);
        this.$emit('photo-updated', file);
      }
    },
    toggleDescription() {
      this.showFullDescription = !this.showFullDescription;
    }
  },
  computed: {
    displayedDescription() {
      const desc = this.venue.venueDesc || '';
      if (desc.length > 150 && !this.showFullDescription) {
        return desc.slice(0, 150) + '...';
      }
      return desc;
    }
  }
}
</script>