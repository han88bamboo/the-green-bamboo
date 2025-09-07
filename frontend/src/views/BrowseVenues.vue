<!-- Browse Listings page for drink categories and styles. Shows filtered drinks based on drinkType or typeCategory. -->

<template>
    <NavBar />
    <!-- Display when searching encounters an error -->
    <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="loadError">
        <span>An error occurred while loading venues, please try refreshing the page!</span>
        <br>
        <button class="btn primary-btn btn-sm" @click="() => { this.$router.go(0) }">
            <span class="fs-5 fst-italic"> Refresh Page </span>
        </button>
    </div>

    <!-- Header -->
    <div class="container pt-3">

        <!-- Display listings after data loaded -->
        <div>
            <div class="row mt-2">
                <!-- BACK BUTTON, FORM TITLE, BROWSE TERM -->
                <div class="col-md-4 col-12">
                    <div class="row">
                        <!-- Back Button -->
                        <div class="d-grid col-1">
                            <button class="btn btn-sm" @click="() => { this.$router.go(-1) }">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor"
                                    class="bi bi-arrow-left-circle" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd"
                                        d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-4.5-.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z" />
                                </svg>
                            </button>
                        </div>
                        <!-- Form Title -->
                        <div class="d-grid col-11" style="color:black;">
                            <p class="fw-bold fs-5 m-0 text-start mobile-ms-2">Browse: {{ effectiveBrowseTerm }}</p>
                        </div>

                    </div>

                    <!-- Request / Create Listing Link (font size reduced at smaller screen width) -->
                    <div class="row mt-2 mobile-view-hide">
                        <div class="col-12">
                            <p class="fs-6 fst-italic text-start">
                                Don't see what you're looking for? Search for it above!
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Filters  -->
                <div class="col-md-8 col-12">

                    <div class="row d-flex justify-content-center">

                        <!-- Mobile View: Create/Request Link -->
                        <div class="col-12 mobile-view-show mobile-pe-0 mt-2 mb-3">
                            <router-link class="text-decoration-none" v-if="role == 'producer'"
                                :to="{ path: '/Producer/Producer-Create-Listing/' }">
                                <p class="mobile-rating-smaller-text-2 fst-italic text-center">Don't see what you're
                                    looking for? Create a new listing here!</p>
                            </router-link>
                            <router-link class="text-decoration-none" v-if="role == 'user'"
                                :to="{ path: '/request/new/' }">
                                <p class="mobile-rating-smaller-text-2 fst-italic text-center">Don't see what you're
                                    looking for? Request a new listing here!</p>
                            </router-link>
                            <router-link class="text-decoration-none" v-if="role != 'producer' && role != 'user'"
                                :to="{ path: '/login' }">
                                <p class="mobile-rating-smaller-text-2 fst-italic text-center">Don't see what you're
                                    looking for? Login to request a new listing!</p>
                            </router-link>
                        </div>

                        <!-- Clear All Filters Button -->
                        <div class="col-lg-2 col-md-3 col-6 mb-2">
                            <button class="btn btn-outline-danger w-100" @click="clearAllFilters()" :disabled="!hasActiveFilters()">
                                <span>Clear</span>
                            </button>
                        </div>

                        <!-- Venue Type Filter -->
                        <div class="col-lg-2 col-md-3 col-6 mb-2 dropdown">
                            <button class="btn dropdown-toggle w-100" type="button" data-bs-toggle="dropdown"
                                aria-expanded="false"
                                style="color: whitesmoke; background-color: #83a9e8; border-radius: 10px; font-weight: bold;">
                                <span>{{ browseFilters.venueMainType || 'Type' }}</span>

                            </button>
                            <ul class="dropdown-menu">
                                <li><span class="dropdown-item text-muted" @click="toggleFilter('venueMainType', '')">
                                        <input type="radio" :checked="!browseFilters.venueMainType"
                                            class="form-check-input me-2">
                                        All Types
                                    </span></li>
                                <li>
                                    <hr class="dropdown-divider">
                                </li>
                                <li v-for="venueType in venueTypes.main_type" :key="venueType.id">
                                    <span class="dropdown-item"
                                        :class="{ 'active': browseFilters.venueMainType === venueType.venueMainType }"
                                        @click="toggleFilter('venueMainType', venueType.venueMainType)">
                                        <input type="radio"
                                            :checked="browseFilters.venueMainType === venueType.venueMainType"
                                            class="form-check-input me-2">
                                        {{ venueType.venueMainType }}
                                    </span>
                                </li>
                            </ul>
                        </div>

                        <!-- Venue sub type Filter -->
                        <div class="col-lg-2 col-md-3 col-6 mb-2 dropdown">
                            <button class="btn dropdown-toggle w-100" type="button" data-bs-toggle="dropdown"
                                aria-expanded="false"
                                style="color: whitesmoke; background-color: #83a9e8; border-radius: 10px; font-weight: bold;">
                                <span>{{ browseFilters.venueSubType || 'Sub Type' }}</span>

                            </button>
                            <ul class="dropdown-menu">
                                <li><span class="dropdown-item text-muted" @click="toggleFilter('venueSubType', '')">
                                        <input type="radio" :checked="!browseFilters.venueSubType"
                                            class="form-check-input me-2">
                                        All Sub Types
                                    </span></li>
                                <li>
                                    <hr class="dropdown-divider">
                                </li>
                                <li v-for="venueType in venueTypes.sub_type" :key="venueType.id">
                                    <span class="dropdown-item"
                                        :class="{ 'active': browseFilters.venueSubType === venueType.venueSubType }"
                                        @click="toggleFilter('venueSubType', venueType.venueSubType)">
                                        <input type="radio"
                                            :checked="browseFilters.venueSubType === venueType.venueSubType"
                                            class="form-check-input me-2">
                                        {{ venueType.venueSubType }}
                                    </span>
                                </li>
                            </ul>
                        </div>

                        <!-- Rating Filter -->
                        <div class="col-lg-2 col-md-3 col-6 mb-2 dropdown">
                            <button class="btn btn-filter dropdown-toggle w-100" type="button" data-bs-toggle="dropdown"
                                aria-expanded="false" :aria-label="getFilterAriaLabel()"
                                :class="{ 'filter-active': hasActiveFilters() }">
                                <span>{{ formatRatingRange() || 'Rating' }}</span>
                            </button>

                            <div class="dropdown-menu dropdown-menu-filter">
                                <div class="px-3 py-2">
                                    <!-- Min Rating -->
                                    <div class="mb-3">
                                        <label for="minRating" class="form-label small mb-1">
                                            Min Rating:
                                        </label>
                                        <select id="minRating" v-model="browseFilters.minRating"
                                            @change="handleRatingChange" class="form-select form-select-sm"
                                            :class="{ 'is-invalid': hasRatingConflict() }">
                                            <option value="">Any</option>
                                            <option v-for="rating in minRatingOptions" :key="rating.value"
                                                :value="rating.value">
                                                {{ rating.label }}
                                            </option>
                                        </select>
                                    </div>

                                    <!-- Max Rating -->
                                    <div class="mb-3">
                                        <label for="maxRating" class="form-label small mb-1">
                                            Max Rating:
                                        </label>
                                        <select id="maxRating" v-model="browseFilters.maxRating"
                                            @change="handleRatingChange" class="form-select form-select-sm"
                                            :class="{ 'is-invalid': hasRatingConflict() }">
                                            <option value="">Any</option>
                                            <option v-for="rating in maxRatingOptions" :key="rating.value"
                                                :value="rating.value">
                                                {{ rating.label }}
                                            </option>
                                        </select>
                                    </div>

                                    <!-- Validation Message -->
                                    <div v-if="hasRatingConflict()" class="alert alert-warning alert-sm mb-2">
                                        <small>Min rating cannot exceed max rating</small>
                                    </div>

                                    <!-- Action Buttons -->
                                    <!-- <div class="d-flex gap-2">
                                        <button type="button" class="btn btn-sm btn-outline-secondary flex-fill"
                                            @click="clearRatingFilters">
                                            Clear
                                        </button>
                                        <button type="button" class="btn btn-sm btn-primary flex-fill"
                                            @click="applyRatingFilters" :disabled="hasRatingConflict()">
                                            Apply
                                        </button>
                                    </div> -->
                                </div>
                            </div>
                        </div>

                        <!-- Sort Options -->
                        <div class="col-lg-2 col-md-3 col-6 mb-2 dropdown">
                            <button class="btn dropdown-toggle w-100" type="button" data-bs-toggle="dropdown"
                                aria-expanded="false"
                                style="color: whitesmoke; background-color: #83a9e8; border-radius: 10px; font-weight: bold;"
                                :aria-label="getSortAriaLabel()">

                                <span>{{ getSortDisplayText() }}</span>
                            </button>

                            <ul class="dropdown-menu">
                                <!-- Default Smart Order -->
                                <li>
                                    <span class="dropdown-item position-relative"
                                        :class="{ 'selected-sort': !sortSelection.category }"
                                        @click="sortByCategory('')" style="cursor: pointer;">
                                        Smart Order (Default)
                                        <i v-if="!sortSelection.category"
                                            class="fas fa-check position-absolute end-0 me-3 text-success" style="top: 50%; transform: translateY(-50%);" aria-hidden="true">
                                        </i>
                                    </span>
                                </li>

                                <li>
                                    <hr class="dropdown-divider">
                                </li>

                                <!-- Dynamic Sort Categories -->
                                <li v-for="category in sortCategoryList" :key="category">
                                    <span class="dropdown-item position-relative"
                                        :class="{ 'selected-sort': sortSelection.category === category }"
                                        @click="sortByCategory(category)" style="cursor: pointer;">
                                        {{ category }}
                                        <i v-if="sortSelection.category === category"
                                            class="fas fa-check position-absolute end-0 me-3 text-success" style="top: 50%; transform: translateY(-50%);" aria-hidden="true">
                                        </i>
                                    </span>
                                </li>
                            </ul>
                        </div>

                    </div>

                </div>

                <!-- Results Header -->
                <div class="row mt-3">
                    <div class="col-12" v-if="!venues.loading">
                        <p class="fw-bold fs-6 m-0 py-2 mobile-view-hide"
                            v-if="venues.listing && venues.listing.length > 0">
                            Viewing: {{ venues.listing.length }} {{ effectiveBrowseTerm }} {{ venues.listing.length ===
                                1 ? 'Listing' : 'Listings' }}
                        </p>
                        <p class="fw-bold fs-6 m-0 py-2" v-else-if="!venues.loading">No {{ effectiveBrowseTerm }}
                            Listings Found!</p>
                    </div>
                </div>

                <!-- Display Listings -->
                <div class="text-start">
                    <div class="venue-listing-row mb-3" v-for="resultListing in venues.listing" :key="resultListing.id">
                        <router-link
                            :to="{ path: '/profile/venue/' + resultListing.id + '/' + slugify(resultListing.venueName) }"
                            class="venue-listing-link">

                            <!-- MOBILE VIEW-->
                            <div class="row mobile-view-show">
                                <!-- Image -->
                                <div
                                    class="mobile-col-3 mobile-me-3 image-container mb-3 mobile-px-0 producer-profile-no-left-padding-large-screen">
                                    <ImgLoader :Photo="resultListing.photo || ''" :default-photo="defaultProfilePhoto"
                                        :imgAlt="resultListing.venueName" :loading="imageLoading"
                                        @error="handleImageError" ref="venueImageRef" />
                                </div>

                                <!-- Details -->
                                <div class="col-lg-8 col-12 ps-3 mobile-col-6 mobile-pe-0 mobile-ps-1">
                                    <!-- Listing Name -->
                                    <h6 class="fw-bold mb-1 mobile-fs-6">{{ resultListing.venueName }}</h6>
                                    <p class="text-start mb-1 mobile-fs-7">
                                        <strong>{{ resultListing.originLocation && resultListing.originLocation.trim() !== '' ? resultListing.originLocation : 'N/A' }}</strong>
                                        <span v-if="resultListing.venueMainTypeName"> • {{ resultListing.venueMainTypeName }}</span>
                                        <span v-if="resultListing.venueSubTypeName"> • {{ resultListing.venueSubTypeName }}</span>
                                    </p>
                                    <p class="mt-1 fst-italic scrollable-long mobile-fs-7">
                                        {{ resultListing["venueDesc"]?.length > 60
                                            ? resultListing["venueDesc"].substring(0, 60) + "..."
                                            : resultListing["venueDesc"] || "No description available" }}
                                    </p>
                                </div>

                                <!-- Rating ★ -->
                                <div class="mobile-col-2 mobile-pe-0 mobile-ps-1">
                                    <div class="d-flex flex-column align-items-center ps-lg-3">
                                        <div class="d-flex align-items-center justify-content-center mb-1">
                                            <span class="mobile-fs-7">{{ resultListing.averageRating !== '0' ? resultListing.averageRating : '-'}}</span>
                                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12"
                                                fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16"
                                                style="color: gold;" v-if="resultListing.averageRating !== '0'">
                                                <path
                                                    d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                            </svg>
                                        </div>
                                        <!-- Bookmark Icon -->
                                        <BookmarkIcon v-if="user" :listing="resultListing" :user="user"
                                            @icon-clicked="handleIconClick" />
                                    </div>
                                </div>
                            </div>

                            <!-- DESKTOP VIEW-->
                            <div class="row mobile-view-hide align-items-start">
                                <!-- Image on the left -->
                                <div class="col-auto image-container mobile-px-0">
                                    <ImgLoader :Photo="resultListing.photo || ''" :default-photo="defaultProfilePhoto"
                                        :imgAlt="resultListing.venueName" :loading="imageLoading"
                                        @image-selected="handleImageSelected" @image-reverted="handleImageReverted"
                                        @image-removed="handleImageRemoved" @error="handleImageError"
                                        ref="venueImageRef" />
                                </div>

                                <!-- Details on the right -->
                                <div class="col">
                                    <div class="row">
                                        <div class="col-lg-8 col-12">
                                            <!-- Listing Name -->
                                            <h5 class="fw-bold mb-2">{{ resultListing.venueName }}</h5>

                                            <!-- Producer + Type Info -->
                                            <p class="mb-1">
                                                <strong>Location:</strong> {{ resultListing.originLocation }}
                                            </p>
                                            <p class="mb-1" v-if="resultListing.venueMainTypeName">
                                                <strong>Type:</strong> {{ resultListing.venueMainTypeName }}
                                            </p>
                                            <p class="mb-1" v-if="resultListing.venueSubTypeName">
                                                <strong>Sub Type:</strong> {{ resultListing.venueSubTypeName }}
                                            </p>

                                            <!-- Description -->
                                            <p class="mt-1 fst-italic scrollable-long">
                                                {{ resultListing["venueDesc"]?.length > 200
                                                    ? resultListing["venueDesc"].substring(0, 200) + "..."
                                                    : resultListing["venueDesc"] || "No description available" }}
                                            </p>
                                        </div>

                                        <!-- Rating & Bookmark -->
                                        <div
                                            class="col-lg-4 col-12 d-flex flex-column align-items-end justify-content-start">
                                            <div class="d-flex align-items-center mb-2">
                                                <span class="fs-5 me-2">{{ resultListing.averageRating !== '0' ? resultListing.averageRating : '-' }}</span>
                                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"
                                                    fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16"
                                                    style="color: gold;" v-if="resultListing.averageRating !== '0'">
                                                    <path
                                                        d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                                </svg>
                                            </div>
                                            <!-- Bookmark Icon -->
                                            <BookmarkIcon v-if="user" :listing="resultListing" :user="user"
                                                @icon-clicked="handleIconClick" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </router-link>
                    </div>

                    <!-- Load More Indicator -->
                    <div class="d-flex justify-content-center py-3" v-if="venues.loading">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </div>

                    <!-- End of Results Message -->
                    <div class="text-center text-muted py-3" v-if="!venues.hasNextPage && !venues.loading && venues.listing.length > 0">
                        <p class="mb-0">You've reached the end of the list.</p>
                    </div>
                </div>

            </div>
        </div>

        <BookmarkModal v-if="user" :user="user" :listingID="bookmarkListingID" />
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import BookmarkIcon from '@/components/BookmarkIcon.vue';
import BookmarkModal from '@/components/BookmarkModal.vue';
import ImgLoader from '@/components/elements/ImgLoader.vue';

export default {
    name: "BrowseVenues",
    components: {
        NavBar,
        BookmarkIcon,
        BookmarkModal,
        ImgLoader
    },
    data() {
        return {
            dataLoaded: false,
            loadError: false,
            role: localStorage.getItem('88B_accType'),

            // if theres no image set, we need a fallback image
            defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultVenueProfilePhoto.png?v=1748435337",

            // Filter options
            browseFilters: {
                venueMainType: '',
                venueSubType: '',
                minRating: '',
                maxRating: '',
                sortCategory: ''
            },

            // Filter dropdown lists
            venueTypes: {
                loading: true,
                error: null,
                main_type: [],
                sub_type: []
            },

            // Results
            venues: {
                loading: true,
                error: null,
                listing: [], // list of venues 
                hasNextPage: false, // whether more venues are available
                nextCursor: null, // cursor for next page
                isFirstLoad: true // whether this is the first load
            },

            // Sorting
            sortSelection: {
                category: ''
            },
            sortCategoryList: [
                'Alphabetical (A - Z)',
                'Alphabetical (Z - A)',
                'Date (Newest - Oldest)',
                'Date (Oldest - Newest)',
                'Ratings (Highest - Lowest)',
                'Ratings (Lowest - Highest)',
            ],

            // User data
            userID: "",
            userType: "",
            user: null,
            userBookmarks: [],
            drinkList: {
                "haveTried": [""],
                "wantToTry": [""]
            },

            // for bookmark component
            bookmarkListingID: {},

            minRatingOptions: [
                { value: '1', label: '1.0+' },
                { value: '2', label: '2.0+' },
                { value: '3', label: '3.0+' },
                { value: '4', label: '4.0+' },
                { value: '4.5', label: '4.5+' }
            ],
            maxRatingOptions: [
                { value: '2', label: '≤ 2.0' },
                { value: '3', label: '≤ 3.0' },
                { value: '4', label: '≤ 4.0' },
                { value: '5', label: '≤ 5.0' }
            ]
        }
    },
    computed: {
        effectiveBrowseTerm() {
            // Display the most specific term available
            if (this.browseFilters.venueSubType) {
                return `${this.browseFilters.venueMainType} - ${this.browseFilters.venueSubType}`;
            } else if (this.browseFilters.venueMainType) {
                return this.browseFilters.venueMainType;
            } else {
                return 'Venues';
            }
        }
    },
    mounted() {
        // Load local storage variables
        this.loadUserFromStorage();

        // Run the browse operation
        this.runBrowse();

        // Add scroll listener for infinite scrolling
        window.addEventListener('scroll', this.handleScroll);
    },
    beforeUnmount() {
        // Remove scroll listener to prevent memory leaks
        window.removeEventListener('scroll', this.handleScroll);
    },
    methods: {
        loadUserFromStorage() {
            try {
                this.userID = localStorage.getItem("88B_accID") || null;
                this.userType = localStorage.getItem("88B_accType") || null;
                this.userName = localStorage.getItem("88B_accUsername") || null;

                if (this.userType === 'user') {
                    this.getUserData();
                }
            } catch (error) {
                console.warn('Failed to load user data from storage:', error);
            }
        },

        /**
         * Handle image-related errors
         * @param {string} errorMessage - Error message from component
         */
        handleImageError(errorMessage) {
            console.error('Image error:', errorMessage)

            // Show user-friendly error message
            this.showErrorMessage(errorMessage)
        },

        slugify(text) {
            if (!text) return '';
            return text
                .toString()
                .toLowerCase()
                .replace(/\s+/g, '-')
                .replace(/[^\w-]+/g, '');
        },

        async runBrowse() {
            try {
                // Load filter dropdown options first
                await this.loadVenueTypes();
                // Then load initial listings
                await this.loadVenues();
            }
            catch (error) {
                console.error("Error in runBrowse:", error);
                this.loadError = true;
            }
        },

        // Load main and sub types of venues for filter system 
        async loadVenueTypes() {
            this.venueTypes.loading = true;
            this.venueTypes.error = null;
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/venues/types`, {
                    timeout: 10000,
                    headers: { 'Accept': 'application/json' }
                });
                if (!response.data || typeof response.data !== 'object') {
                    throw new Error('Invalid response format');
                }
                const { main_type = [], sub_type = [] } = response.data;
                if (!Array.isArray(main_type) || !Array.isArray(sub_type)) {
                    throw new Error('Expected arrays for venue types');
                }
                this.venueTypes.main_type = main_type;
                this.venueTypes.sub_type = sub_type;
            } catch (error) {
                console.error('Error loading venue types:', error);
                this.venueTypes.error = error.message || 'Failed to load venue types.';
                this.venueTypes.main_type = [];
                this.venueTypes.sub_type = [];
            } finally {
                this.venueTypes.loading = false;
            }
        },

        // Get user data
        async getUserData() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUser/${this.userID}`);
                this.user = response.data;
                if (this.user) {
                    this.userBookmarks = this.user.drinkLists;
                    let triedDrinks = [];
                    let wantToTryDrinks = [];
                    for (let bookmark of this.userBookmarks) {
                        if (bookmark.listType === 'haveTried') {
                            triedDrinks.push(bookmark.listItems);
                        } else if (bookmark.listType === 'wantToTry') {
                            wantToTryDrinks.push(bookmark.listItems);
                        }
                    }
                    this.drinkList = {
                        haveTried: triedDrinks,
                        wantToTry: wantToTryDrinks
                    };
                }
            }
            catch (error) {
                console.error(error);
            }
        },

        async loadVenues(isLoadMore = false) {
            if (this.venues.loading && isLoadMore) return;

            this.venues.loading = true;
            this.venues.error = null;

            if (!isLoadMore) {
                this.venues.listing = [];
                this.venues.nextCursor = null;
                this.venues.hasNextPage = false;
            }

            try {
                const params = new URLSearchParams();

                if (this.browseFilters.venueMainType) {
                    const mainType = this.venueTypes.main_type.find(t => t.venueMainType === this.browseFilters.venueMainType);
                    if (mainType) {
                        params.append('venueMainType', mainType.id);
                    }
                }
                if (this.browseFilters.venueSubType) {
                    const subType = this.venueTypes.sub_type.find(t => t.venueSubType === this.browseFilters.venueSubType);
                    if (subType) {
                        params.append('venueSubType', subType.id);
                    }
                }
                // Note: Rating and sort filters will be added here once backend is updated.

                if (isLoadMore && this.venues.nextCursor) {
                    params.append('cursor', this.venues.nextCursor);
                }

                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/venues/`, { params });

                if (response.data && response.data.success) {
                    const { venues, pagination } = response.data.data;
                    console.log(venues)
                    if (isLoadMore) {
                        this.venues.listing.push(...venues);
                    } else {
                        this.venues.listing = venues;
                    }
                    this.venues.hasNextPage = pagination.hasNextPage;
                    this.venues.nextCursor = pagination.nextCursor;
                } else {
                    throw new Error(response.data.message || 'Failed to load venues.');
                }
            } catch (error) {
                console.error('Error loading venues:', error);
                this.venues.error = error.message || 'An unknown error occurred.';
                this.loadError = true;
            } finally {
                this.venues.loading = false;
            }
        },

        handleScroll() {
            // Check if we're near the bottom of the page
            const buffer = 300; // pixels from bottom
            const isAtBottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - buffer;

            if (isAtBottom && this.venues.hasNextPage && !this.venues.loading) {
                this.loadVenues(true);
            }
        },

        // Filter functions
        toggleFilter(filterType, value) {
            if (this.browseFilters[filterType] === value) {
                this.browseFilters[filterType] = '';
            } else {
                this.browseFilters[filterType] = value;
            }
            this.applyFilters();
        },

        hasActiveFilters() {
            return this.browseFilters.venueMainType || this.browseFilters.venueSubType ||
                this.browseFilters.minRating || this.browseFilters.maxRating;
        },

        clearAllFilters() {
            this.browseFilters = {
                venueMainType: '',
                venueSubType: '',
                minRating: '',
                maxRating: ''
            };
            this.applyFilters();
        },

        async applyFilters() {
            await this.loadVenues(false);
        },

        formatRatingRange() {
            const { minRating, maxRating } = this.browseFilters;
            if (minRating && maxRating) return `${minRating}-${maxRating}★`;
            if (minRating) return `${minRating}★+`;
            if (maxRating) return `≤${maxRating}★`;
            return '';
        },

        // Sort functions
        sortByCategory(category) {
            this.sortSelection.category = category;
            this.sortResults();
        },

        sortResults() {
            let category = this.sortSelection.category;
            // Note: Sorting is currently client-side. This will be moved to the backend.
            if (category === 'Alphabetical (A - Z)') {
                this.venues.listing.sort((a, b) => a.venueName.localeCompare(b.venueName));
            } else if (category === 'Alphabetical (Z - A)') {
                this.venues.listing.sort((a, b) => b.venueName.localeCompare(a.venueName));
            } else if (category === 'Date (Newest - Oldest)') {
                this.venues.listing.sort((a, b) => new Date(b.addedDate) - new Date(a.addedDate));
            } else if (category === 'Date (Oldest - Newest)') {
                this.venues.listing.sort((a, b) => new Date(a.addedDate) - new Date(b.addedDate));
            } else if (category === 'Ratings (Highest - Lowest)') {
                this.venues.listing.sort((a, b) => {
                    const aRating = a.averageRating === '-' ? 0 : parseFloat(a.averageRating);
                    const bRating = b.averageRating === '-' ? 0 : parseFloat(b.averageRating);
                    return bRating - aRating;
                });
            } else if (category === 'Ratings (Lowest - Highest)') {
                this.venues.listing.sort((a, b) => {
                    const aRating = a.averageRating === '-' ? 0 : parseFloat(a.averageRating);
                    const bRating = b.averageRating === '-' ? 0 : parseFloat(b.averageRating);
                    return aRating - bRating;
                });
            } else {
                // Default: Smart Order (reload from backend)
                this.loadVenues(false);
            }
        },

        handleIconClick(data) {
            this.bookmarkListingID = data;
        },

        formatDate(dateTimeString) {
            let date = new Date(dateTimeString);
            let day = String(date.getDate()).padStart(2, '0');
            let month = String(date.getMonth() + 1).padStart(2, '0');
            let year = date.getFullYear();
            return `${day}/${month}/${year}`;
        },

        hasRatingConflict() {
            if (!this.browseFilters.minRating || !this.browseFilters.maxRating) {
                return false;
            }
            return parseFloat(this.browseFilters.minRating) > parseFloat(this.browseFilters.maxRating);
        },

        getFilterAriaLabel() {
            const range = this.formatRatingRange();
            return range ? `Rating filter: ${range}` : 'Rating filter - no selection';
        },

        handleRatingChange() {
            clearTimeout(this.ratingChangeTimeout);
            this.ratingChangeTimeout = setTimeout(() => {
                if (!this.hasRatingConflict()) {
                    this.applyFilters();
                }
            }, 300);
        },

        applyRatingFilters() {
            if (!this.hasRatingConflict()) {
                this.applyFilters();
                this.$el.querySelector('.dropdown-toggle').click();
            }
        },

        clearRatingFilters() {
            this.browseFilters.minRating = '';
            this.browseFilters.maxRating = '';
            this.applyFilters();
        },

        getSortDisplayText() {
            return this.sortSelection.category || 'Sort';
        },

        getSortAriaLabel() {
            const currentSort = this.getSortDisplayText();
            if (currentSort === 'Sort') {
                return 'Sort options - no selection';
            }
            return `Sort options - currently sorted by ${currentSort}`;
        },
    }
}
</script>

<style scoped>
.scrollable-long {
    max-height: 4em;
    overflow: hidden;
    text-overflow: ellipsis;
}

.funnel-svg-dimensions {
    height: 20px;
    width: 20px;
}

.dropdown-menu-scrollable {
    max-height: 300px;
    overflow-y: auto;
}

.dropdown-item.active {
    background-color: #0d6efd;
    color: white;
}

.dropdown-item:hover {
    background-color: #f8f9fa;
}

.dropdown-item.active:hover {
    background-color: #0b5ed7;
}

.dropdown-header {
    display: flex;
    align-items: center;
    font-weight: 600;
    color: #495057;
}

.mobile-fs-6 {
    font-size: 0.9rem;
}

.mobile-fs-7 {
    font-size: 0.8rem;
}

/* Custom button sizing for filter buttons */
.btn {
    font-size: 0.85rem;
    padding: 0.375rem 0.5rem;
}

.btn-sm {
    font-size: 0.8rem;
    padding: 0.25rem 0.4rem;
}

/* Ensure consistent button heights */
.dropdown-toggle {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Better spacing for mobile */
@media (max-width: 576px) {
    .btn {
        font-size: 0.75rem;
        padding: 0.3rem 0.4rem;
    }

    .col-6.mb-2 {
        padding-left: 0.25rem;
        padding-right: 0.25rem;
    }
}



@media (max-width: 768px) {
    .mobile-view-hide {
        display: none !important;
    }

    .mobile-view-show {
        display: flex !important;
    }

    .mobile-col-2 {
        flex: 0 0 auto;
        width: 16.666667%;
    }

    .mobile-col-3 {
        flex: 0 0 auto;
        width: 25%;
    }

    .mobile-col-6 {
        flex: 0 0 auto;
        width: 50%;
    }

    .mobile-col-8 {
        flex: 0 0 auto;
        width: 66.666667%;
    }
}

.btn-filter {
    color: whitesmoke;
    background-color: #83a9e8;
    border-radius: 10px;
    font-weight: bold;
    border: 2px solid transparent;
}

.btn-filter:hover {
    background-color: #6b94e3;
}

.btn-filter.filter-active {
    background-color: #5a85de;
    border-color: #4a75ce;
}

.dropdown-menu-filter {
    min-width: 280px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.alert-sm {
    padding: 0.375rem 0.75rem;
    font-size: 0.875rem;
}

.form-select:focus {
    border-color: #83a9e8;
    box-shadow: 0 0 0 0.2rem rgba(131, 169, 232, 0.25);
}

.is-invalid {
    border-color: #dc3545;
}

@media (max-width: 576px) {
    .dropdown-menu-filter {
        min-width: 260px;
    }
}

.selected-sort {
    background-color: #e3f2fd !important;
    color: #1976d2 !important;
    font-weight: 600;
}

.selected-sort:hover {
    background-color: #bbdefb !important;
    color: #1976d2 !important;
}

.dropdown-item {
    transition: all 0.2s ease;
}

/* Remove link styling and add hover effects */
.venue-listing-link {
    text-decoration: none !important;
    color: inherit !important;
    display: block;
}

.venue-listing-link:hover,
.venue-listing-link:focus,
.venue-listing-link:active,
.venue-listing-link:visited {
    text-decoration: none !important;
    color: inherit !important;
}

/* Hover effect for the entire listing row */
.venue-listing-row {
    padding: 15px;
    border-radius: 8px;
    transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

.venue-listing-row:hover {
    background-color: #dfdfdf;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

/* Ensure images maintain proper spacing */
.image-container {
    padding-right: 15px;
}

/* Mobile specific adjustments */
@media (max-width: 768px) {
    .venue-listing-row {
        padding: 10px;
    }
    
    .image-container {
        padding-right: 0;
        margin-bottom: 10px;
    }
}
</style>