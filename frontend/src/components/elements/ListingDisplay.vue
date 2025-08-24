<template>
  <div class="listing-row-container">
    <!-- Header -->
    <h5 class="listing-header">
      <strong>{{ displayName }}</strong>
    </h5>

    <!-- Loading State -->
    <div v-if="loading" class="text-center p-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert alert-danger text-center">
      Could not load {{ displayName.toLowerCase() }}.
      <button class="btn btn-sm btn-danger ms-2" @click="$emit('retry')">Retry</button>
    </div>

    <!-- Content or Empty State -->
    <template v-else>
      <div v-if="validListings.length > 0" class="listings-container">
        <!-- Desktop/Tablet Grid View -->
        <div class="d-none d-md-block">
          <div class="row g-3">
            <div 
              v-for="listing in validListings" 
              :key="listing.id"
              class="col-xl-2 col-lg-3 col-md-4 col-sm-6"
            >
              <ListingCard 
                :listing="listing"
                :user="user"
                :truncate-length="DESKTOP_TRUNCATE_LENGTH"
                @icon-clicked="handleIconClick"
              />
            </div>
          </div>
        </div>

        <!-- Mobile Horizontal Scroll View -->
        <div class="d-block d-md-none">
          <div class="mobile-scroll-container">
            <div class="mobile-scroll-wrapper">
              <div 
                v-for="listing in validListings" 
                :key="listing.id"
                class="mobile-scroll-item"
              >
                <ListingCard 
                  :listing="listing"
                  :user="user"
                  :truncate-length="MOBILE_TRUNCATE_LENGTH"
                  :is-mobile="true"
                  @icon-clicked="handleIconClick"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      <EmptyState 
        v-else 
        :display-name="displayName" 
      />
    </template>
  </div>
</template>

<script>
// Child Components
const ListingCard = {
  name: 'ListingCard',
  components: {
    BookmarkIcon: () => import('@/components/BookmarkIcon.vue')
  },
  props: {
    listing: {
      type: Object,
      required: true
    },
    user: {
      type: Object,
      default: () => ({})
    },
    truncateLength: {
      type: Number,
      default: 63
    },
    isMobile: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    listingImageSrc() {
      return this.listing?.photo && this.listing.photo !== '' 
        ? this.listing.photo 
        : this.defaultImageSrc;
    },
    
    truncatedListingName() {
      const name = this.listing?.listingName || '';
      return name.length > this.truncateLength 
        ? `${name.slice(0, this.truncateLength)}...`
        : name;
    },
    
    listingUrl() {
      return `/listing/view/${this.listing.id}/${this.slugify(this.listing.listingName)}`;
    },
    
    showBookmark() {
      return this.user && Object.keys(this.user).length > 0;
    },
    
    cardClasses() {
      return {
        'listing-card': true,
        'listing-card--mobile': this.isMobile
      };
    }
  },
  data() {
    return {
      defaultImageSrc: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739'
    };
  },
  methods: {
    slugify(text) {
      if (!text) return '';
      return text
        .toString()
        .toLowerCase()
        .replace(/\s+/g, '')
        .replace(/[^\w]/g, '');
    },
    
    handleBookmarkClick(data) {
      this.$emit('icon-clicked', data);
    }
  },
  template: `
    <div :class="cardClasses">
      <!-- Image Container -->
      <div class="listing-card__image-container">
        <router-link :to="listingUrl" class="listing-card__image-link">
          <img 
            :src="listingImageSrc"
            :alt="listing.listingName"
            class="listing-card__image"
            loading="lazy"
          />
        </router-link>
        
        <BookmarkIcon 
          v-if="showBookmark"
          :user="user" 
          :listing="listing" 
          :overlay="true"
          size="20"
          class="listing-card__bookmark"
          @icon-clicked="handleBookmarkClick" 
        />
      </div>

      <!-- Listing Name -->
      <router-link 
        :to="listingUrl" 
        class="listing-card__title-link"
      >
        <div class="listing-card__title" :title="listing.listingName">
          {{ truncatedListingName }}
        </div>
      </router-link>
    </div>
  `
};

const EmptyState = {
  name: 'EmptyState',
  props: {
    displayName: {
      type: String,
      required: true
    }
  },
  template: `
    <div class="empty-state">
      <p class="empty-state__text">
        No {{ displayName.toLowerCase() }} yet. To explore more drinks on the home page, 
        <router-link to="/" class="empty-state__link">click here</router-link>.
      </p>
    </div>
  `
};

export default {
  name: "ListingDisplay",
  components: {
    ListingCard,
    EmptyState
  },
  props: {
    displayName: {
      type: String,
      required: true
    },
    listingData: {
      type: Array,
      default: () => []
    },
    user: {
      type: Object,
      default: () => ({})
    },
    listing: {
      type: Object,
      default: () => ({})
    },
    columnWidth: {
      type: String,
      default: '195px'
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: [Object, String, Boolean],
      default: null
    }
  },
  data() {
    return {
      DESKTOP_TRUNCATE_LENGTH: 63,
      MOBILE_TRUNCATE_LENGTH: 25
    };
  },
  computed: {
    validListings() {
      return this.listingData?.filter(listing => listing?.id) || [];
    }
  },
  methods: {
    handleIconClick(data) {
      this.$emit('icon-clicked', data);
    }
  }
};
</script>

<style scoped>
/* Container Styles */
.listing-row-container {
  width: 100%;
  padding: 0;
}

.listing-header {
  color: var(--bs-body-color);
  text-align: left;
  padding-top: 0.25rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.listings-container {
  width: 100%;
}

/* Listing Card Styles */
.listing-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  transition: transform 0.2s ease;
}

.listing-card:hover {
  transform: translateY(-2px);
}

.listing-card__image-container {
  position: relative;
  width: 150px;
  height: 150px;
  margin-bottom: 0.5rem;
  border-radius: 0.375rem;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.listing-card__image-link {
  display: block;
  width: 100%;
  height: 100%;
  text-decoration: none;
}

.listing-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0.375rem;
  transition: transform 0.2s ease;
}

.listing-card__image:hover {
  transform: scale(1.05);
}

.listing-card__bookmark {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  z-index: 10;
}

.listing-card__title-link {
  text-decoration: none;
  color: inherit;
  display: block;
  width: 100%;
  margin-top: 0.5rem;
}

.listing-card__title-link:hover {
  color: var(--bs-primary);
}

.listing-card__title {
  text-align: center;
  max-height: 75px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  line-height: 1.4;
  font-size: 0.9rem;
  padding: 0 0.25rem;
}

/* Mobile Specific Styles */
.listing-card--mobile .listing-card__title {
  font-size: 0.8rem;
  -webkit-line-clamp: 2;
  max-height: 50px;
}

/* Mobile Scroll Container */
.mobile-scroll-container {
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  -ms-overflow-style: none;
  padding-bottom: 0.5rem;
}

.mobile-scroll-container::-webkit-scrollbar {
  display: none;
}

.mobile-scroll-wrapper {
  display: flex;
  gap: 1rem;
  padding: 0 1rem;
  min-width: max-content;
}

.mobile-scroll-item {
  flex: 0 0 auto;
  width: 150px;
}

/* Empty State */
.empty-state {
  margin: 1rem 0;
  text-align: left;
}

.empty-state__text {
  margin: 0;
  color: var(--bs-body-color);
}

.empty-state__link {
  color: inherit;
  text-decoration: none;
}

.empty-state__link:hover {
  color: var(--bs-primary);
  text-decoration: underline;
}

/* Responsive Adjustments */
@media (max-width: 576px) {
  .listing-header {
    font-size: 1.1rem;
    margin-bottom: 0.75rem;
  }
  
  .mobile-scroll-wrapper {
    padding: 0 0.5rem;
    gap: 0.75rem;
  }
  
  .mobile-scroll-item {
    width: 130px;
  }
  
  .listing-card__image-container {
    width: 130px;
    height: 130px;
  }
}

@media (min-width: 1400px) {
  .listing-card__image-container {
    width: 160px;
    height: 160px;
  }
}

/* Performance Optimizations */
.listing-card__image {
  will-change: transform;
}

.mobile-scroll-container {
  will-change: scroll-position;
  contain: layout style paint;
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  .listing-card,
  .listing-card__image {
    transition: none;
  }
  
  .listing-card:hover {
    transform: none;
  }
  
  .listing-card__image:hover {
    transform: none;
  }
}

/* Focus States */
.listing-card__image-link:focus,
.listing-card__title-link:focus {
  outline: 2px solid var(--bs-primary);
  outline-offset: 2px;
  border-radius: 0.25rem;
}
</style>