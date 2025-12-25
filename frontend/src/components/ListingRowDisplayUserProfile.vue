<!-- Updated ListingRowDisplayUserProfile.vue to handle both listings and top rated reviews -->

<template>
    <div class="d-flex justify-content-between pt-1 mobile-spacer ">
      <div class="text-start"><h5 class="text-body-secondary fw-bold mobile-fs-6"> {{ displayName }}</h5></div>
      <router-link
        :to="`/profile/user/${userID}/${username}/allreviews`"
        class="text-end text-muted text-decoration-none mobile-rating-smaller-text-2"
        >
          VIEW ALL →
      </router-link>
    </div>
    <hr class="mobile-col-11 mobile-spacer">
    <div class="">
        <!-- Top Rated Reviews Display (when topRatedReviews prop is provided) -->
      <div v-if="topRatedReviews && topRatedReviews.length > 0" class="row g-3 top-rated-row trending-reviews-container align-items-start">
        <div
          v-for="(review, index) in topRatedReviews"
          :key="review.id"
          class="col-6 col-lg-4 top-rated-col"
        >
          <div class="card h-100 review-card border-light">

            <!-- IMAGE TOP -->
            <div class="card-img-top-wrapper">
              <div
                style="position: relative; border-radius: 10px; overflow: hidden; width: 100%;"
              >
                <!-- Notch Overlay for Private Review (only visible to owner) -->
                <div v-if="!review.isPublic && ownProfile" class="item-notch item-notch-private">
                  <div class="notch-content">
                    <span class="notch-icon"><i class="bi bi-eye-slash"></i></span>
                    <span class="notch-text">Private</span>
                  </div>
                </div>

                <router-link
                  :to="{ path: '/listing/view/' + review.reviewTarget + '/' + slugify(review.listingName || 'unknown-listing') }"
                >
                  <img
                    v-if="review.photo && review.photo !== ''"
                    :src="review.photo"
                    alt=""
                    class="card-img-top review-card-img"
                  />
                  <img
                    v-else-if="review.listingPhoto && review.listingPhoto !== ''"
                    :src="review.listingPhoto"
                    alt=""
                    class="card-img-top review-card-img"
                  />
                  <img
                    v-else
                    src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
                    alt=""
                    class="card-img-top review-card-img"
                  />
                </router-link>
              </div>
            </div>

            <!-- BODY -->
            <div class="card-body d-flex flex-column">

              <!-- Title -->
              <router-link
                :to="{ path: '/listing/view/' + review.reviewTarget + '/' + slugify(review.listingName || 'unknown-listing') }"
                class="text-decoration-none"
                style="color: #223957"
              >
                <h6 class="card-title mb-1 fw-bold">
                  {{ review.listingName || 'Unknown Listing' }}
                </h6>
              </router-link>

              <!-- Rating / tasted line (keep your logic) -->
              <p class="text-muted mb-2">
                <template v-if="!isNaN(parseFloat(review.rating))">
                  Rated <span class="fw-bold rating-text ">{{ parseFloat(review.rating).toFixed(1) }}★</span>
                </template>
                <template v-else>
                  Tasted
                </template>
                <span v-if="review.venueName"> at <span class="fw-bold rating-text ">{{ review.venueName }}</span></span>
              </p>

            
              <!-- Review text w/ read more (uses your existing expandedReviews + methods) -->
              <div v-if="review.reviewDesc || review.reviewText" class="mb-2">
                <p v-if="!expandedReviews[index]" class="mb-0 small" style="color:#333; line-height:1.5;">
                  {{ getPreviewText(review) }}
                  <span
                    v-if="shouldShowReadMore(review)"
                    @click="expandReview(index)"
                    class="read-more-link"
                    style="color:#027562; cursor:pointer; font-weight:700; text-decoration:underline;"
                  >
                    (Read More)
                  </span>
                </p>

                <p v-else class="mb-0 small" style="color:#333; line-height:1.5;">
                  {{ getFullReviewText(review) }}
                  <span
                    @click="collapseReview(index)"
                    class="read-less-link"
                    style="color:#027562; cursor:pointer; font-weight:700; text-decoration:underline;"
                  >
                    (Read Less)
                  </span>
                </p>
              </div>

              <!-- TAGS (same data, just inside the body) -->
              <div class="mt-auto pt-2">
                <div class="tags-section mb-2">
                  <span
                    v-for="(tag, tagIndex) in review.flavourTag.slice(0,3)"
                    :key="'flavor-' + tagIndex"
                    class="badge mobile-rating-smaller-text-2 me-2 mb-2"
                    :style="{ backgroundColor: getTagColor(parseInt(tag)) }"
                  >
                    {{ getTagName(parseInt(tag)) }}
                  </span>

                  <span
                    v-for="(tag, tagIndex) in review.observationTag.slice(0,2)"
                    :key="'obs-' + tagIndex"
                    class="badge mobile-rating-smaller-text-2 me-2 mb-2 tag-badge"
                    :style="{ backgroundColor: getActionTagColor(tag), color: 'black' }"
                  >
                    {{ getActionTagDisplayText(tag) }}
                  </span>

                </div>

                
              </div>

            </div>
          </div>
        </div>
      </div>


        <!-- Original Listings Display (when listingArr prop is provided) -->
        <div v-else-if="listingArr && listingArr.length > 0">
            <div v-for="(listing, index) in listingArr" :key="index" class="row mb-3" :style="{ display: 'flex' }">
                <div class="col-3 mobile-col-3 mobile-pe-0" v-if="listing?.id">
                    <div class="Xdrink-photo-container-row Ximage-container-150">
                        <router-link :to="{ path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName) }" class="default-text-no-background">
                            <img v-if="listing.photo !== '' && listing.photo !== null" :src="listing.photo" class="add-drink-photo-background-user-profile centered rounded"> 
                            <img v-else src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" class="add-drink-photo-background-user-profile centered rounded">
                        </router-link>
                    </div>
                </div>
                <div class="col-9 mobile-col-9 mobile-ps-2" v-if="listing?.id">
                    <router-link :to="{ path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName) }" class="default-clickable-text scrollable mt-2 mobile-fs-7" style="text-decoration: none">
                        <p v-if="listing.listingName.length > 63" class="fs-5 mobile-fs-6 mb-1"> 
                            <b>{{ listing.listingName.slice(0,63) + (listing.listingName.length > 63 ? '...' : '') }}</b>
                        </p>
                        <p v-else class="fs-5 mobile-fs-6 mb-1"> 
                            <b>{{ listing.listingName }}</b>
                        </p>    
                    </router-link>
                    <p class="mobile-fs-7 mb-1" style="font-weight:bold; color: #2a6959;">
                        {{ getProducerName(listing)?.length > 40 ? getProducerName(listing).slice(0, 40) + '...' : getProducerName(listing) || 'Unknown Producer' }}
                    </p>
                    <p class="mobile-fs-7 mb-0" style="color: #333">
                        {{ listing.officialDesc?.length > 100 ? listing.officialDesc.slice(0, 100) + "..." : listing.officialDesc }}
                    </p>
                </div>
            </div>
        </div>

        <!-- Empty State -->
        <div v-else class="mb-2 mobile-rating-smaller-text-2">
            No {{ displayName.toLowerCase() }} yet. To explore more drinks in the home page, 
            <router-link to="/" style="color: inherit;">click here</router-link>. 
        </div>
    </div>
</template>

<script>
import { parseActionTag, getTagDisplayText, getTagColor } from '@/utils/tagUtils';

export default {
  name: "ListingRowDisplayUserProfile",
  props: {
    displayName: String,
    listingArr: {
      type: Array,
      default: () => []
    },
    topRatedReviews: {
      type: Array,
      default: () => []
    },
    columnWidth: {
      type: String,
      default: '195px'
    },
    producers: {
      type: Array,
      default: () => []
    },
    // Add these props for tag handling
    subTags: {
      type: Array,
      default: () => []
    },
    flavourTags: {
      type: Array,
      default: () => []
    },
    // User identity so profile links work correctly
    userID: {
      type: [String, Number],
      default: null
    },
    username: {
      type: String,
      default: ''
    },
    // Add ownProfile prop for privacy handling
    ownProfile: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      expandedReviews: {} // Track which reviews are expanded
    };
  },
  methods: {
    
    slugify(text) {
      if (!text) return ""
      return text
        .toString()
        .toLowerCase()
        .normalize('NFD') // Decompose accented characters
        .replace(/[\u0300-\u036f]/g, '') // Remove diacritical marks
        .replace(/\s+/g, '-')                 // Replace spaces with hyphens
        .replace(/[^\w]/g, '') // Remove non-word characters
    },
    
    // Original method for listings
    getProducerName(listing) {
      if (!this.producers || !listing.producerID) {
        return null;
      }
      const producer = this.producers.find(
        (producer) => producer.id === listing.producerID
      );
      return producer ? producer.producerName : null;
    },

    // New methods for top rated reviews
    getPreviewText(review) {
      const fullText = this.getFullReviewText(review);
      const maxLength = 120;
      
      if (fullText.length <= maxLength) {
        return fullText;
      }
      
      const truncated = fullText.substring(0, maxLength);
      const lastSpace = truncated.lastIndexOf(' ');
      
      return truncated.substring(0, lastSpace) + '...';
    },

    getFullReviewText(review) {
      let reviewText = '';
      
      if (review.reviewDesc) {
        reviewText += review.reviewDesc;
      }
      
      if (review.aroma && review.aroma.trim()) {
        if (reviewText) reviewText += ' ';
        reviewText += `Aroma: ${review.aroma}`;
      }
      
      if (review.taste && review.taste.trim()) {
        if (reviewText) reviewText += ' ';
        reviewText += `Taste: ${review.taste}`;
      }
      
      if (review.finish && review.finish.trim()) {
        if (reviewText) reviewText += ' ';
        reviewText += `Finish: ${review.finish}`;
      }
      
      return reviewText || 'No review text available';
    },

    shouldShowReadMore(review) {
      const fullText = this.getFullReviewText(review);
      return fullText.length > 120;
    },

    expandReview(index) {
      this.expandedReviews[index] = true;
      this.$forceUpdate();
    },

    collapseReview(index) {
      this.expandedReviews[index] = false;
      this.$forceUpdate();
    },

    // Tag-related methods (updated to match working reference)
    getTagName(tag) {
      if (!this.subTags || !this.flavourTags || !tag) {
        return "";
      }

      const subTag = this.subTags.find((subTag) => subTag.id === tag);
      if (subTag) {
        const familyTag = this.flavourTags.find(
          (family) => subTag.familyTagId === family.id
        );
        if (familyTag) {
          const hexcode = familyTag.hexcode;
          const subtagInfo = subTag.subTag;
          const tagInfo = subtagInfo + hexcode;
          const tagParts = tagInfo.split("#");
          return tagParts[0];
        }
      } else {
        return "<deleted tag>";
      }
    },

    getTagColor(tag) {
      if (!this.subTags || !this.flavourTags) {
        return "#f0f0f0";
      }
      const subTag = this.subTags.find((subTag) => subTag.id === tag);
      if (subTag) {
        const familyTag = this.flavourTags.find(
          (family) => subTag.familyTagId === family.id
        );
        if (familyTag) {
          const hexcode = familyTag.hexcode;
          const subtagInfo = subTag.subTag;
          const tagInfo = subtagInfo + hexcode;
          const tagParts = tagInfo.split("#");
          return "#" + tagParts[1];
        }
      } else {
        return "#030303";
      }
    },

    // Helper method to determine text color based on background color
    getTextColor(backgroundColor) {
      if (!backgroundColor) return '#000';
      
      // Remove # if present
      const hex = backgroundColor.replace('#', '');
      
      // Convert to RGB
      const r = parseInt(hex.substr(0, 2), 16);
      const g = parseInt(hex.substr(2, 2), 16);
      const b = parseInt(hex.substr(4, 2), 16);
      
      // Calculate luminance
      const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
      
      // Return white text for dark backgrounds, black for light backgrounds
      return luminance > 0.5 ? '#000' : '#fff';
    },

    // Action Tag Utility Methods
    parseActionTag(tag) {
      return parseActionTag(tag);
    },

    getActionTagDisplayText(tag) {
      return getTagDisplayText(tag);
    },

    getActionTagColor(tag) {
      return getTagColor(tag);
    }
  }
};
</script>


<style scoped>
.read-more-link:hover,
.read-less-link:hover {
  text-decoration: underline;
}

.review-card-img{
  width: 100%;
  height: 180px;       /* tweak */
  object-fit: cover;
  display: block;
}

/* Grid view styles */
.review-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.review-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.review-content {
  line-height: 1.4;
}

.reviews-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.5rem;
}

/* Mobile: single column */
@media (max-width: 768px) {
  .reviews-grid {
    grid-template-columns: 1fr;
  }

  .review-card-img{
  width: 100%;
  height: 150px;       /* tweak */
  object-fit: cover;
  display: block;
}
}

/* Ensure normal Bootstrap wrapping + no horizontal scroll */
.top-rated-row {
  flex-wrap: wrap !important;
  overflow-x: visible !important;
}



/* ✅ Mobile: horizontal scroller, cards keep a readable size */
@media (max-width: 767.98px) {
  .top-rated-row {
    flex-wrap: nowrap !important;   /* override Bootstrap row wrap */
    overflow-x: auto;
    overflow-y: hidden;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 0.5rem;
  }
}

.tags-section {
  display: flex;
  flex-wrap: wrap;
  max-width: 100%;
}

.tag-badge {
  max-width: 100%;            /* never exceed card width */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;        /* keep it on one line */
}

/* Scrollbar styling for trending reviews */
/* Default (desktop / tablet) */
.trending-reviews-container {
  margin: 0;
}

/* Mobile only */
@media (max-width: 767.98px) {
  .trending-reviews-container {
    margin: 0 12px;
  }
}


.trending-reviews-container::-webkit-scrollbar {
    height: 8px;
}

.trending-reviews-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}

.trending-reviews-container::-webkit-scrollbar-thumb {
    background: #f0b358;
    border-radius: 4px;
}

.trending-reviews-container::-webkit-scrollbar-thumb:hover {
    background: #025a4a;
}


</style>