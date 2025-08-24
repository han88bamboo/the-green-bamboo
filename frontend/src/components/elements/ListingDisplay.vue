<template>
  <!-- Section Title -->
  <h5 class="text-muted text-start pt-1 mb-3">
    <strong>{{ title }}</strong>
  </h5>

  <!-- Desktop View -->
  <div class="container-fluid pe-lg-0 ps-0 d-none d-md-block">
    <div v-if="hasListings" class="d-flex flex-wrap justify-content-start" style="gap: 1rem;">
      <div 
        v-for="(listing, index) in validListings" 
        :key="`desktop-${listing.id}-${index}`"
        class="flex-shrink-0"
        :style="{ width: columnWidth, minWidth: '150px' }"
      >
        <DrinkCard 
          :listing="listing" 
          :user="user"
          :column-width="columnWidth"
          :desktop-truncate-length="DESKTOP_TRUNCATE_LENGTH"
          :mobile-truncate-length="MOBILE_TRUNCATE_LENGTH"
          @bookmark-clicked="handleIconClick" 
        />
      </div>
    </div>
    
    <EmptyState v-else :title="title" />
  </div>

  <!-- Mobile View -->
  <div class="container-fluid pe-0 ps-0 d-block d-lg-none">
    <div v-if="hasListings" class="mobile-scroll-container">
      <div class="d-flex overflow-auto pb-3" style="gap: 1rem;">
        <div 
          v-for="(listing, index) in validListings" 
          :key="`mobile-${listing.id}-${index}`"
          class="flex-shrink-0"
          style="width: 150px;"
        >
          <DrinkCard 
            :listing="listing" 
            :user="user" 
            :is-mobile="true"
            :column-width="columnWidth"
            :desktop-truncate-length="DESKTOP_TRUNCATE_LENGTH"
            :mobile-truncate-length="MOBILE_TRUNCATE_LENGTH"
            @bookmark-clicked="handleIconClick" 
          />
        </div>
      </div>
    </div>
    
    <EmptyState v-else :title="title" />
  </div>
</template>

<script>
import DrinkCard from './DrinkCard.vue'
import EmptyState from './EmptyState.vue'

export default {
  name: 'ListingDisplay', // Using your original component name
  components: {
    DrinkCard,
    EmptyState
  },
  
  props: {
    title: {
      type: String,
      required: true
    },
    listings: {
      type: Array,
      default: () => []
    },
    user: {
      type: Object,
      default: () => ({})
    },
    columnWidth: {
      type: String,
      default: '195px'
    }
  },

  data() {
    return {
      DESKTOP_TRUNCATE_LENGTH: 63,
      MOBILE_TRUNCATE_LENGTH: 25
    }
  },

  computed: {
    validListings() {
      return this.listings.filter(listing => listing?.id)
    },
    
    hasListings() {
      return this.validListings.length > 0
    },
    
    isUserLoggedIn() {
      return this.user && Object.keys(this.user).length > 0
    }
  },

  methods: {
    handleIconClick(data) {
      this.$emit('icon-clicked', data)
    },
    
    slugify(text) {
      return text
        .toString()
        .toLowerCase()
        .replace(/\s+/g, '')
        .replace(/[^\w]/g, '') // Using your original regex pattern
    }
  }
}
</script>

<style scoped>
.mobile-scroll-container {
  padding: 0 1rem;
}

.mobile-scroll-container::-webkit-scrollbar {
  height: 6px;
}

.mobile-scroll-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.mobile-scroll-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.mobile-scroll-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>