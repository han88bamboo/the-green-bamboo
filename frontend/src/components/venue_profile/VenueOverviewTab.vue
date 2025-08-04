<template>
    <div>
        <!-- LATEST UPDATES SECTION -->
        <div id="updates-section">
            <h4 class="text-start fs-4 fw-bold">Latest Updates from {{ venueName }}</h4>
            
            <!-- This is a perfect candidate for its own component: LatestUpdates.vue -->
            <div v-if="updates && updates.length > 0">
                <!-- Display logic for the latest update -->
                <p>Latest update content goes here...</p>
            </div>
            <div v-else>
                <p class="text-start fst-italic text-muted mt-2">{{ venueName }} has not posted any updates!</p>
            </div>

            <!-- Add Update Form (for self view) -->
            <div v-if="isSelfView" class="mt-4">
                <h5>Post a New Update</h5>
                <!-- Simplified form for posting an update -->
                <textarea class="form-control" placeholder="Say hi to your patrons!"></textarea>
                <button class="btn btn-primary mt-2">Post</button>
            </div>
            <!-- End of potential LatestUpdates.vue component -->
        </div>

        <hr class="my-4">

        <!-- View Sorted Listings -->
        <div class="venue-overview-container">
            <!-- Most Popular Section -->
            <ListingDisplay
                section-key="mostPopular"
                display-name="Most Popular"
                :listing-data="overview.mostPopular"
                :loading="overview.mp_loading"
                :error="overview.mp_error"
                :user="user"
                @icon-clicked="handleBookmarkClick"
                @retry="handleRetry('mostPopular')"
            />

            <!-- Most Discussed Section -->
            <ListingDisplay
                section-key="mostDiscussed"
                display-name="Most Discussed"
                :listing-data="overview.mostDiscussed"
                :loading="overview.md_loading"
                :error="overview.md_error"
                :user="user"
                @icon-clicked="handleBookmarkClick"
                @retry="handleRetry('mostDiscussed')"
            />

            <!-- Recently Added Section -->
            <ListingDisplay
                section-key="recentlyAdded"
                display-name="Recently Added"
                :listing-data="overview.ra_recentlyAdded"
                :loading="overview.ra_loading"
                :error="overview.ra_error"
                :user="user"
                @icon-clicked="handleBookmarkClick"
                @retry="handleRetry('recentlyAdded')"
            />

        </div>

    </div>
</template>

<script>
import ListingDisplay from '../elements/ListingDisplay.vue';

export default {
    name: 'VenueOverviewTab',
    components: {
        ListingDisplay,
    },
    props: {
        updates: Array,
        venueName: String,
        isSelfView: Boolean,
        overview: {
            type: Object,
            required: true,
            validator(value) {
                // Validate the structure of overview object
                const requiredKeys = [
                    'mp_loading', 'mp_error', 'mostPopular',
                    'md_loading', 'md_error', 'mostDiscussed', 
                    'ra_loading', 'ra_error', 'ra_recentlyAdded'
                ];
                return requiredKeys.every(key => key in value);
            }
        },
        userInfo: Object, // Passed for potential interactions
    },
    methods: {
        handleBookmarkClick(data) {
            // Emit to parent component for handling
            this.$emit('bookmark-clicked', data);
        },

        handleRetry(sectionKey) {
            // Emit retry event with section identifier
            this.$emit('retry-section', sectionKey);
        }
    }
}
</script>

<style scoped>
.venue-overview-container {
  padding: 1rem 0;
}

.venue-overview-container > * + * {
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .venue-overview-container {
    padding: 0.5rem 0;
  }
  
  .venue-overview-container > * + * {
    margin-top: 1.5rem;
  }
}
</style>