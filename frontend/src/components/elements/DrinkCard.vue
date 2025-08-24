
<template>
  <div class="card h-100 border-0 shadow-sm drink-card" :style="cardStyle">
    <!-- Image Container -->
    <div class="position-relative card-img-container">
      <router-link 
        :to="drinkUrl" 
        class="text-decoration-none d-block"
      >
        <img 
          :src="drinkImage" 
          :alt="listing.name"
          class="card-img-top drink-image rounded"
          :class="{ 'mobile-image': isMobile }"
        >
      </router-link>
      
      <!-- Bookmark Icon Overlay -->
      <BookmarkIcon 
        v-if="showBookmark"
        :user="user" 
        :listing="listing" 
        :overlay="true"
        size="20" 
        class="bookmark-overlay"
        @icon-clicked="$emit('bookmark-clicked', $event)"
      />
    </div>

    <!-- Card Body -->
    <div class="card-body p-2 d-flex flex-column">
      <router-link 
        :to="drinkUrl" 
        class="text-decoration-none text-dark flex-grow-1 d-flex align-items-center"
      >
        <h6 
          class="card-title mb-0 text-center lh-sm"
          :class="{ 'small': isMobile }"
          :title="listing.name"
        >
          {{ displayName }}
        </h6>
      </router-link>
    </div>
  </div>
</template>

<script>
import BookmarkIcon from '@/components/BookmarkIcon.vue'

export default {
  name: 'DrinkCard',
  components: {
    BookmarkIcon
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
    isMobile: {
      type: Boolean,
      default: false
    },
    columnWidth: {
      type: String,
      default: '195px'
    },
    desktopTruncateLength: {
      type: Number,
      default: 63
    },
    mobileTruncateLength: {
      type: Number,
      default: 25
    }
  },

  computed: {
    drinkUrl() {
      return {
        path: `/listing/view/${this.listing.id}/${this.slugify(this.listing.name || this.listing.listingName)}`
      }
    },
    
    drinkImage() {
      return this.listing.photo && this.listing.photo !== '' 
        ? this.listing.photo 
        : 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739'
    },
    
    displayName() {
      const name = this.listing.name || this.listing.listingName || ''
      const maxLength = this.isMobile ? this.mobileTruncateLength : this.desktopTruncateLength
      return name.length > maxLength 
        ? name.slice(0, maxLength) + '...' 
        : name
    },
    
    showBookmark() {
      return this.user && Object.keys(this.user).length > 0
    },

    cardStyle() {
      return {
        width: this.isMobile ? '150px' : this.columnWidth
      }
    }
  },

  methods: {
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
.drink-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.drink-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}

.card-img-container {
  aspect-ratio: 1;
  overflow: hidden;
  background: #f8f9fa;
}

.drink-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.2s ease;
}

.mobile-image {
  aspect-ratio: 1;
  max-height: 150px;
}

.drink-card:hover .drink-image {
  transform: scale(1.05);
}

.bookmark-overlay {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  padding: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-weight: 500;
  color: #495057;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.3;
  max-height: 3.9em;
}

@media (max-width: 991.98px) {
  .card-title {
    font-size: 0.85rem;
    -webkit-line-clamp: 2;
    max-height: 2.6em;
  }
}
</style>