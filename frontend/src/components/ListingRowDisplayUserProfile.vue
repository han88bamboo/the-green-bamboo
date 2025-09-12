<!-- Updated ListingRowDisplayUserProfile.vue to handle both listings and top rated reviews -->

<template>
    <h5 class="text-body-secondary text-start pt-1"> 
        <b> {{ displayName }} </b> 
    </h5>
    <div class="">
        <!-- Top Rated Reviews Display (when topRatedReviews prop is provided) -->
        <div v-if="topRatedReviews && topRatedReviews.length > 0">
            <div v-for="(review, index) in topRatedReviews" :key="review.id" class="review-card mb-4 p-3 mobile-rating-smaller-text-2" style="border: 1px solid #e0e0e0; border-radius: 8px; background: #fff;">
                
                <!-- Rating and Listing Name (centered, full width) -->
                <div class="review-header text-center mb-3" style="margin-right: 140px;">
                    <div class="rating-text mb-2" style="word-wrap: break-word; overflow-wrap: break-word;">
                        <span style="color: #333; font-size: 1.1em;">Rated ⭐</span>
                        <span class="fw-bold" style="color: #333; font-size: 1.1em;">{{ parseFloat(review.rating).toFixed(1) }}</span>
                        <span style="color: #333; font-size: 1.1em;"> Stars</span>
                        <span v-if="review.venueName" style="color: #333; font-size: 1.1em; font-weight: 600;"> at {{ review.venueName }}</span>
                    </div>
                    
                    <!-- Listing Name (prominent, below rating) -->
                    <div class="listing-name">
                        <router-link 
                            :to="{ path: '/listing/view/' + review.reviewTarget + '/' + slugify(review.listingName || 'unknown-listing') }" 
                            class="text-decoration-none"
                        >
                            <h6 class="fw-bold mb-0" style="color: #2a6959;">
                                {{ review.listingName || 'Unknown Listing' }}
                            </h6>
                        </router-link>
                    </div>
                </div>

                <!-- Content Area with Image and Review Text -->
                <div class="content-area position-relative mb-3">
                    <!-- Image positioned on the right -->
                    <div class="image-container" style="float: right; margin-left: 15px; margin-bottom: 10px; margin-top: -60px;">
                        <router-link :to="{ path: '/listing/view/' + review.reviewTarget + '/' + slugify(review.listingName || 'unknown-listing') }">
                            <img 
                                v-if="review.photo && review.photo !== ''" 
                                :src="review.photo" 
                                class="review-image rounded"
                                style="width: 120px; height: 120px; object-fit: cover; display: block;"
                            />
                            <img 
                                v-else-if="review.listingPhoto && review.listingPhoto !== ''"
                                :src="review.listingPhoto" 
                                class="review-image rounded"
                                style="width: 120px; height: 120px; object-fit: cover; display: block;"
                            />
                            <img 
                                v-else 
                                src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" 
                                class="review-image rounded"
                                style="width: 120px; height: 120px; object-fit: cover; display: block;"
                            />
                        </router-link>
                    </div>

                    <!-- Review Content that wraps around the image -->
                    <div class="review-content" style="text-align: justify;">
                        <p v-if="!expandedReviews[index]" class="mb-2" style="color: #333; line-height: 1.6; font-size: 0.95em;">
                            {{ getPreviewText(review) }}
                            <span v-if="shouldShowReadMore(review)" @click="expandReview(index)" class="read-more-link" style="color: #027562; cursor: pointer; font-weight: bold; text-decoration: underline;">
                                (Read More)
                            </span>
                        </p>
                        <p v-else class="mb-2" style="color: #333; line-height: 1.6; font-size: 0.95em;">
                            {{ getFullReviewText(review) }}
                            <span @click="collapseReview(index)" class="read-less-link" style="color: #027562; cursor: pointer; font-weight: bold; text-decoration: underline;">
                                (Read Less)
                            </span>
                        </p>
                    </div>
                    
                    <!-- Clear float to ensure proper layout -->
                    <div style="clear: both;"></div>
                </div>

                <!-- Tags Section -->
                <div class="tags-section mb-3 pt-2">
                    <!-- Flavor Tags -->
                    <span 
                        v-for="(tag, tagIndex) in review.flavourTag" 
                        :key="'flavor-' + tagIndex"
                        class="badge rounded-pill me-2 mb-2"
                        :style="{ backgroundColor: getTagColor(parseInt(tag)) }"
                    >
                        {{ getTagName(parseInt(tag)) }}
                    </span>
                    
                    <!-- Observation Tags -->
                    <span 
                        v-for="(tag, tagIndex) in review.observationTag" 
                        :key="'obs-' + tagIndex"
                        class="badge rounded-pill me-2 mb-2"
                        style="background-color: #f0b358; color: #000;"
                    >
                        {{ tag }}
                    </span>
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
      const maxLength = 300;
      
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
      return fullText.length > 300;
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
    }
  }
};
</script>

<style scoped>
.read-more-link:hover,
.read-less-link:hover {
  text-decoration: underline;
}

.review-content {
  line-height: 1.4;
}
</style>