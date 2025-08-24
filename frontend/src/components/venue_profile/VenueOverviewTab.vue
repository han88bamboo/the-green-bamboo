<template>
    <div>
        <!-- LATEST UPDATES SECTION -->
        <div id="updates-section">
            <h4 class="text-start fs-4 fw-bold">Latest Updates from {{ venueName }}</h4>

            <!-- This is a perfect candidate for its own component: LatestUpdates.vue -->
            <div v-if="updates && updates.length > 0">
                <!-- Display logic for the latest update -->

                <!-- Row 1: Photo + Update Text -->
                <div class="row align-items-start mt-3">

                    <!-- Image (25%) -->
                    <div class="col-2 mobile-col-4 text-start1">
                        <img :src="(updates[0].photo || defaultPhoto)" alt="" class="img-fluid rounded" />
                    </div>

                    <!-- Text (75%) -->
                    <div class="col-10 mobile-col-8 text-start">
                        <p class="mobile-rating-smaller-text-2 mb-0">
                            {{ targetVenue['updates'][0].text }}
                        </p>
                    </div>

                </div>

                <!-- Row 2: Likes + Posted Date + Admin Buttons (Full Width) -->
                <div class="row pt-3">

                    <div class="col-12 d-flex flex-wrap align-items-center justify-content-start gap-3">

                        <!-- Like Heart and Count -->
                        <div class="d-flex align-items-center">
                            <div v-if="Array.isArray(updates[0].likes) && viewerType !== null"
                                @click="likeUpdates(updates[0].id)" style="cursor: pointer;">
                                <svg v-if="updates[0].likes.some(like => ((like.userId == viewerID) && (like.userType === userType)))"
                                    xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="red"
                                    class="bi bi-heart-fill" viewBox="0 0 16 16">
                                    <path d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314" />
                                </svg>
                                <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                    fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                                    <path
                                        d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15" />
                                </svg>
                            </div>
                            <span class="ms-2 mobile-rating-smaller-text-2">{{
                                updates[0].likes.length }}</span>
                        </div>

                        <!-- Posted Date -->
                        <div class="text-body-secondary mobile-rating-smaller-text-2">
                            Posted on: {{ updates[0].date }}
                        </div>

                        <!-- Admin Buttons -->
                        <div v-if="selfView || powerView" class="ms-auto">
                            <button v-if="editUpdateTarget != updates[0].id" type="button"
                                class="btn btn-warning btn-sm me-2" @click="editUpdate(updates[0])">
                                Edit
                            </button>
                            <button v-if="editUpdateTarget != updates[0].id" type="button" class="btn btn-danger btn-sm"
                                @click="deleteUpdate(updates[0])">
                                Delete
                            </button>
                            <button v-if="editUpdateTarget == updates[0].id" type="button"
                                class="btn btn-success btn-sm me-2" @click="saveUpdate(updates[0])"
                                :disabled="!(editUpdateContent[updates[0].id].newText.length > 0)">
                                Save
                            </button>
                            <button v-if="editUpdateTarget == updates[0].id" type="button"
                                class="btn btn-secondary btn-sm" @click="editUpdateTarget = null">
                                Cancel
                            </button>
                        </div>

                    </div>

                </div>

            </div>
            <div v-else>
                <p class="text-start fst-italic text-muted mt-2">{{ venueName }} has not posted any updates!</p>
            </div>

            <!-- Text Box / Options -->
            <div v-if="isOwner" class="w-100">
                <div class="input-group centered">

                    <!-- Text Box -->
                    <input class="search-bar form-control mobile-rating-smaller-text-2 rounded fst-italic"
                        style="border: 2px solid #000000;" type="text" placeholder="Say hi to your patrons!"
                        v-model="newUpdateText">

                    <!-- Photo Upload -->
                    <label for="fileSelectUpdate" class="btn p-0 ms-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor"
                            class="bi bi-camera" viewBox="0 0 16 16">
                            <path
                                d="M15 12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h1.172a3 3 0 0 0 2.12-.879l.83-.828A1 1 0 0 1 6.827 3h2.344a1 1 0 0 1 .707.293l.828.828A3 3 0 0 0 12.828 5H14a1 1 0 0 1 1 1zM2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 0 1 3.172 4z" />
                            <path
                                d="M8 11a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5m0 1a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M3 6.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0" />
                        </svg>
                    </label>
                    <input id="fileSelectUpdate" type="file" @change="FileSelection" ref="fileInput"
                        style="width: 0px; height: 0px; display: none;" accept="image/*">

                    <!-- Submit Button -->
                    <button class="btn send-icon p-0 mx-1" @click="submitUpdate">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor"
                            class="bi bi-send" viewBox="0 0 16 16">
                            <path
                                d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z" />
                        </svg>
                    </button>
                </div>

                <!-- Image Preview Thumbnail -->
                <div v-if="newUpdatePhotoPreview" class="mt-2 position-relative" style="max-width: 150px;">
                    <img :src="newUpdatePhotoPreview" class="img-thumbnail" alt="Image preview">
                    <button @click="removeImagePreview" class="btn btn-sm btn-danger position-absolute top-0 end-0 m-1" style="padding: 0.1rem 0.3rem; line-height: 1;">
                        &times;
                    </button>
                </div>
            </div>
            <!-- End of potential LatestUpdates.vue component -->
        </div>

        <hr class="my-4">

        <!-- View Sorted Listings -->
        <div class="venue-overview-container">
            <!-- Most Popular Section -->
            <ListingDisplay section-key="mostPopular" display-name="Most Popular" :listing-data="overview.mostPopular"
                :loading="overview.mp_loading" :error="overview.mp_error" :user="user"
                @icon-clicked="handleBookmarkClick" @retry="handleRetry('mostPopular')" />

            <!-- Most Discussed Section -->
            <ListingDisplay section-key="mostDiscussed" display-name="Most Discussed"
                :listing-data="overview.mostDiscussed" :loading="overview.md_loading" :error="overview.md_error"
                :user="user" @icon-clicked="handleBookmarkClick" @retry="handleRetry('mostDiscussed')" />

            <!-- Recently Added Section -->
            <ListingDisplay section-key="recentlyAdded" display-name="Recently Added"
                :listing-data="overview.ra_recentlyAdded" :loading="overview.ra_loading" :error="overview.ra_error"
                :user="user" @icon-clicked="handleBookmarkClick" @retry="handleRetry('recentlyAdded')" />

        </div>

    </div>
</template>

<script>
import ListingDisplay from '@/components/elements/ListingDisplay.vue';

export default {
    name: 'VenueOverviewTab',
    components: {
        ListingDisplay,
    },
    props: {
        updates: Array,
        venueName: String,
        isOwner: Boolean,
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
    data() {
        return {
            newUpdateText: '',
            newUpdatePhoto: null,
            newUpdatePhotoPreview: null,
        };
    },
    methods: {
        handleBookmarkClick(data) {
            // Emit to parent component for handling
            this.$emit('bookmark-clicked', data);
        },

        handleRetry(sectionKey) {
            // Emit retry event with section identifier
            this.$emit('retry-section', sectionKey);
        },

        // Helper function to handle file selection for new update photo
        FileSelection(event) {
            const file = event.target.files[0];
            if (!file) {
                return;
            }
            try {
                const reader = new FileReader;
                reader.onload = () => {
                    this.newUpdatePhotoPreview = reader.result;
                    this.newUpdatePhoto = reader.result.split(',')[1];
                };
                reader.readAsDataURL(file);
            }
            catch (error) {
                console.error("Error reading file for preview:", error);
                this.removeImagePreview();
            }
        },

        removeImagePreview() {
            this.newUpdatePhoto = null;
            this.newUpdatePhotoPreview = null;
            this.$refs.fileInput.value = '';
        },

        submitUpdate() {
            this.$emit('submit-update', {
                text: this.newUpdateText,
                photo: this.newUpdatePhoto
            });
            // Clear the fields after submitting
            this.newUpdateText = '';
            this.removeImagePreview();
        }
    }
}
</script>

<style scoped>
.venue-overview-container {
    padding: 1rem 0;
}

.venue-overview-container>*+* {
    margin-top: 2rem;
}

@media (max-width: 768px) {
    .venue-overview-container {
        padding: 0.5rem 0;
    }

    .venue-overview-container>*+* {
        margin-top: 1.5rem;
    }
}
</style>