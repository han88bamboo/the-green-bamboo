<!-- Browse Listings page for drink categories and styles. Shows filtered drinks based on drinkType or typeCategory. -->

<template>
    <NavBar />

    <!-- Display when search is in progress -->
    <div class="text-info-emphasis fst-italic fw-bold fs-5 pt-5" v-if="!dataLoaded"> 
        <span>Currently loading drinks, please hold on!</span>
        <br><br>
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    
    <!-- Display when searching encounters an error -->
    <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="loadError"> 
        <span>An error occurred while loading drinks, please try refreshing the page!</span>
        <br>
        <button class="btn primary-btn btn-sm" @click="()=>{this.$router.go(0)}">
            <span class="fs-5 fst-italic"> Refresh Page </span>
        </button>
    </div>
    
    <!-- Header -->
    <div class="container pt-3">

        <!-- Display listings after data loaded -->
        <div v-if="dataLoaded && !loadError">

            <div class="row mt-2">

                <!-- BACK BUTTON, FORM TITLE, BROWSE TERM -->
                <div class="col-md-8 col-12">

                    <div class="row">
                    
                        <!-- Back Button -->
                        <!-- Back Button -->
                        <div class="d-grid col-1">
                            <button class="btn btn-sm" @click="()=>{this.$router.go(-1)}">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-arrow-left-circle" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-4.5-.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"/>
                                </svg>
                            </button>
                        </div>                        <!-- Form Title -->
                        <div class="d-grid col-11" style="color:black;">
                            <p class="fw-bold fs-5 m-0 text-start mobile-ms-2">Browse: {{ effectiveBrowseTerm }}</p>
                        </div>

                    </div>

                    <!-- Request / Create Listing Link (font size reduced at smaller screen width) -->
                    <div class="row mt-2 mobile-view-hide">
                        <router-link class="col-12 text-decoration-none" v-if="role == 'producer'" :to="{ path: '/Producer/Producer-Create-Listing/' }">
                            <p class="fs-6 fst-italic text-start">Don't see what you're looking for? Create a new listing here!</p>
                        </router-link>
                        <router-link class="col-12 text-decoration-none" v-if="role == 'user'" :to="{ path: '/request/new/' }">
                            <p class="fs-6 fst-italic text-start">Don't see what you're looking for? Request a new listing here!</p>
                        </router-link>
                        <router-link class="col-12 text-decoration-none" v-if="role != 'producer' && role != 'user'" :to="{ path: '/login' }">
                            <p class="fs-6 fst-italic text-start">Don't see what you're looking for? Login to request a new listing!</p>
                        </router-link>
                    </div>

                </div>

                <div class="col-md-4 col-12">

                    <div class="row d-flex justify-content-center">

                        <div class="col-8 mobile-view-show mobile-pe-0 mt-2">
                            <router-link class="text-decoration-none" v-if="role == 'producer'" :to="{ path: '/Producer/Producer-Create-Listing/' }">
                                <p class="mobile-rating-smaller-text-2 fst-italic text-start">Don't see what you're looking for? Create a new listing here!</p>
                            </router-link>
                            <router-link class="text-decoration-none" v-if="role == 'user'" :to="{ path: '/request/new/' }">
                                <p class="mobile-rating-smaller-text-2 fst-italic text-start">Don't see what you're looking for? Request a new listing here!</p>
                            </router-link>
                            <router-link class="text-decoration-none" v-if="role != 'producer' && role != 'user'" :to="{ path: '/login' }">
                                <p class="mobile-rating-smaller-text-2 fst-italic text-start">Don't see what you're looking for? Login to request a new listing!</p>
                            </router-link>
                        </div>

                        <!-- Filter Options -->
                        <div class="mt-2 mobile-col-2 mobile-pe-0 col-xxl-3 col-md-6 col-sm-5 col-12 mb-xxl-0 mb-md-2 mb-sm-0 mb-2 dropdown">
                            <div class="d-grid gap-1">
                                <button class="btn primary-light-dropdown-homepage btn-lg dropdown-toggle mobile-view-remove-toggle d-flex align-items-center fw-bold" type="button" data-bs-toggle="dropdown" aria-expanded="false" style="white-space: nowrap; overflow:hidden; text-overflow: ellipsis;">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-funnel funnel-svg-dimensions" viewBox="0 0 16 16">
                                        <path d="M1.5 1.5A.5.5 0 0 1 2 1h12a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.128.334L10 8.692V13.5a.5.5 0 0 1-.342.474l-3 1A.5.5 0 0 1 6 14.5V8.692L1.628 3.834A.5.5 0 0 1 1.5 3.5zm1 .5v1.308l4.372 4.858A.5.5 0 0 1 7 8.5v5.306l2-.666V8.5a.5.5 0 0 1 .128-.334L13.5 3.308V2z"/>
                                    </svg>
                                    <span class="mobile-view-hide" style="margin-left: 5px;">{{ getFilterDisplayText() }}</span>
                                </button>
                                <ul class="dropdown-menu">
                                    <li><span class="dropdown-item" @click="clearAllFilters()">Clear All Filters</span></li>
                                    <li><hr class="dropdown-divider"></li>
                                    
                                    <!-- Drink Type Filter -->
                                    <li><h6 class="dropdown-header">Drink Type</h6></li>
                                    <li v-for="drinkType in drinkTypeList" :key="drinkType.id">
                                        <span class="dropdown-item" @click="filterByDrinkType(drinkType['drinkType'])">{{ drinkType['drinkType'] }}</span>
                                    </li>
                                    <li><hr class="dropdown-divider"></li>
                                    
                                    <!-- Type Category Filter -->
                                    <li><h6 class="dropdown-header">Category</h6></li>
                                    <li v-for="category in typeCategoryList" :key="category.id">
                                        <span class="dropdown-item" @click="filterByTypeCategory(category['typeCategory'])">{{ category['typeCategory'] }}</span>
                                    </li>
                                    <li><hr class="dropdown-divider"></li>
                                    
                                    <!-- Country Filter -->
                                    <li><h6 class="dropdown-header">Country</h6></li>
                                    <li v-for="country in countryList" :key="country.id">
                                        <span class="dropdown-item" @click="filterByCountry(country['originCountry'])">{{ country['originCountry'] }}</span>
                                    </li>
                                </ul>
                            </div>
                        </div>

                        <!-- Sort Options -->
                        <div class="mt-2 mobile-col-2 mobile-ps-0 col-xxl-3 col-md-6 col-sm-5 col-12 mb-xxl-0 mb-md-2 mb-sm-0 mb-2 dropdown">
                            <div class="d-grid gap-2">
                                <button class="btn primary-light-dropdown-homepage dropdown-toggle mobile-view-remove-toggle d-flex align-items-center fw-bold" type="button" data-bs-toggle="dropdown" aria-expanded="false" style="white-space: nowrap; overflow:hidden; text-overflow: ellipsis;">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-sort-down funnel-svg-dimensions" viewBox="0 0 16 16">
                                        <path d="M3.5 2.5a.5.5 0 0 0-1 0v8.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L3.5 11.293zm3.5 1a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/>
                                    </svg>
                                    <span class="mobile-view-hide" style="margin-left: 5px;">Sort: {{ sortSelection.category != '' ? sortSelection.category : 'Smart Order' }}</span>
                                </button>
                                <ul class="dropdown-menu">
                                    <li><span class="dropdown-item" @click="sortByCategory('')">Smart Order (Default)</span></li>
                                    <li><hr class="dropdown-divider"></li>
                                    <li v-for="category in sortCategoryList" :key="category">
                                        <span class="dropdown-item" @click="sortByCategory(category)">{{ category }}</span>
                                    </li>
                                </ul>
                            </div>
                        </div> 
                    
                    </div>

                </div>

            </div>
            
            <!-- Results Header -->
            <div class="row mt-3">
                <div class="col-12">
                    <p class="fw-bold fs-6 m-0 py-2 mobile-view-hide" v-if="resultListings.length > 0">
                        Viewing: {{ resultListings.length }} {{ effectiveBrowseTerm }} {{ resultListings.length === 1 ? 'Listing' : 'Listings' }}
                    </p>
                    <p class="fw-bold fs-6 m-0 py-2" v-else>No {{ effectiveBrowseTerm }} Listings Found!</p>
                </div>
            </div>

            <!-- Display Listings -->
            <div class="container text-start">
                <div class="row" v-for="resultListing in resultListings" :key="resultListing.id">
                    
                    <!-- MOBILE VIEW-->
                    <!-- Image -->
                    <div class="mobile-col-3 mobile-me-3 image-container mb-3 mobile-px-0 producer-profile-no-left-padding-large-screen mobile-view-show">
                        <router-link :to="{ path: '/listing/view/' + resultListing.id + '/' + slugify(resultListing.listingName) }">
                            <img :src="resultListing.photo || 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739'" 
                                 class="img-fluid rounded" 
                                 :alt="resultListing.listingName"
                                 style="width: 100%; height: 120px; object-fit: cover;">
                        </router-link>
                    </div>
                    <div class="col-lg-8 col-12 ps-3 mobile-col-6 mobile-pe-0 mobile-ps-1 mobile-view-show">
                    <!-- Listing Name + Router Link -->
                        <router-link class="xtext-dark xtext-decoration-none" :to="{ path: '/listing/view/' + resultListing.id + '/' + slugify(resultListing.listingName) }">
                            <h6 class="fw-bold mb-1 mobile-fs-6">{{ resultListing.listingName }}</h6>
                        </router-link>
                        <p class="text-start mb-1 mobile-fs-7"> 
                            <strong>{{ resultListing.producerName }}</strong>
                            <span v-if="resultListing.drinkType"> • {{ resultListing.drinkType }}</span>
                            <span v-if="resultListing.typeCategory"> • {{ resultListing.typeCategory }}</span>
                        </p>
                        <p class="mt-1 fst-italic scrollable-long mobile-fs-7">
                            {{ resultListing["officialDesc"]?.length > 60 
                                ? resultListing["officialDesc"].substring(0, 60) + "..." 
                                : resultListing["officialDesc"] || "No description available" }}
                        </p>
                    </div>
                    <!-- Rating ★ -->
                    <div class="mobile-col-2 mobile-pe-0 mobile-ps-1 mobile-view-show">
                        <div class="d-flex flex-column align-items-center ps-lg-3">
                            <div class="d-flex align-items-center justify-content-center mb-1">
                                <span class="mobile-fs-7">{{ resultListing.averageRating !== '-' ? resultListing.averageRating : '-' }}</span>
                                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16" style="color: gold;" v-if="resultListing.averageRating !== '-'">
                                    <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                </svg>
                            </div>
                            <!-- Bookmark Icon -->
                            <BookmarkIcon 
                                v-if="user"
                                :listing="resultListing"
                                :user="user"
                                @icon-clicked="handleIconClick" />
                        </div>
                    </div>
                    
                    <!-- DESKTOP VIEW-->
                    <!-- Image  -->
                    <div class="d-flex justify-content-end col-3 image-container mb-3 mobile-px-0 mobile-view-hide">
                        <router-link :to="{ path: '/listing/view/' + resultListing.id + '/' + slugify(resultListing.listingName) }">
                            <img :src="resultListing.photo || 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739'" 
                                 class="img-fluid rounded" 
                                 :alt="resultListing.listingName"
                                 style="width: 200px; height: 200px; object-fit: cover;">
                        </router-link>
                    </div>

                    <!-- Details -->
                    <div class="row col-9 mobile-view-hide">
                        <div class="col-lg-6 col-12">
                            <!-- Listing Name + Router Link -->
                            <router-link class="text-dark text-decoration-none" :to="{ path: '/listing/view/' + resultListing.id + '/' + slugify(resultListing.listingName) }">
                                <h5 class="fw-bold mb-2">{{ resultListing.listingName }}</h5>
                            </router-link>
                            <!-- Producer + Type Info -->
                            <p class="mb-1">
                                <strong>Producer:</strong> {{ resultListing.producerName }}
                            </p>
                            <p class="mb-1" v-if="resultListing.drinkType">
                                <strong>Type:</strong> {{ resultListing.drinkType }}
                            </p>
                            <p class="mb-1" v-if="resultListing.typeCategory">
                                <strong>Category:</strong> {{ resultListing.typeCategory }}
                            </p>
                            <p class="mb-1" v-if="resultListing.originCountry">
                                <strong>Country:</strong> {{ resultListing.originCountry }}
                            </p>
                        </div>

                        <div class="d-flex justify-content-end col-lg-5 col-12" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                            <!-- Rating & Bookmark -->
                            <div class="d-flex flex-column align-items-end">
                                <div class="d-flex align-items-center mb-2">
                                    <span class="fs-5 me-2">{{ resultListing.averageRating !== '-' ? resultListing.averageRating : '-' }}</span>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16" style="color: gold;" v-if="resultListing.averageRating !== '-'">
                                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                    </svg>
                                </div>
                                <!-- Bookmark Icon -->
                                <BookmarkIcon 
                                    v-if="user"
                                    :listing="resultListing"
                                    :user="user"
                                    @icon-clicked="handleIconClick" />
                            </div>
                        </div>
                        <!-- Description -->
                        <p class="mt-1 fst-italic scrollable-long">
                            {{ resultListing["officialDesc"]?.length > 200 
                                ? resultListing["officialDesc"].substring(0, 200) + "..." 
                                : resultListing["officialDesc"] || "No description available" }}
                        </p>
                    </div>
                    <hr>
                </div>

                <!-- Load More Listing Result Button -->
                <div class="d-flex justify-content-center mb-3" v-if="resultListings.length > 0 && !noMoreListings">
                    <button class="btn primary-btn btn-lg" @click="loadMoreListings()">Load More Listings</button>
                </div>
            </div>

            <BookmarkModal 
                v-if="user"
                :user="user" 
                :listingID="bookmarkListingID" />
        </div>
    </div>
</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    import BookmarkIcon from '@/components/BookmarkIcon.vue';
    import BookmarkModal from '@/components/BookmarkModal.vue';

    export default {
        name: "BrowseListings",
        components: {
            NavBar,
            BookmarkIcon, 
            BookmarkModal
        },
        data() {
            return {
                dataLoaded: false,
                loadError: false,
                role: localStorage.getItem('88B_accType'),
                
                // Browse parameters from route
                browseDrinkType: this.$route.params.browseDrinkType, // Main drink type (e.g., 'Whisky')
                browseTypeCategory: this.$route.params.browseTypeCategory, // Optional subcategory (e.g., 'Single Malt')
                
                // Filter options
                browseFilters: {
                    drinkType: '',
                    typeCategory: '',
                    originCountry: '',
                    minRating: '',
                    maxRating: ''
                },
                
                // Filter dropdown lists
                drinkTypeList: [],
                typeCategoryList: [],
                countryList: [],
                
                // Results
                resultListings: [],
                
                // Pagination
                noMoreListings: false,
                offsetListings: 0,
                recordsPerLoad: 30,

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
            }
        },
        computed: {
            effectiveBrowseTerm() {
                // Display the most specific term available
                if (this.browseTypeCategory) {
                    return `${this.browseDrinkType} - ${this.browseTypeCategory}`;
                } else if (this.browseDrinkType) {
                    return this.browseDrinkType;
                } else {
                    return 'Drinks';
                }
            }
        },
        mounted() {
            // Load local storage variables
            const accID = localStorage.getItem("88B_accID");
            if(accID !== null){
                this.userID = localStorage.getItem('88B_accID')
            }
            let userType = localStorage.getItem('88B_accType')
            if(userType !=null){
                this.userType = userType

                // Retrieve user data if type user is logged in
                if (userType === 'user') {
                    this.getUserData();
                }
            }
            let userName = localStorage.getItem("88B_accUsername");
            if (userName !== null) {
                this.userName = userName;
            }

            // Initialize browse filters based on route parameters
            this.initializeBrowseFilters();

            // Run the browse operation
            this.runBrowse();
        },
        methods: {
            slugify(text) {
                return text
                    .toString()
                    .toLowerCase()
                    .replace(/\s+/g, '')
                    .replace(/[^\w]/g, '');
            },

            initializeBrowseFilters() {
                // Set initial filters based on route parameters
                if (this.browseDrinkType) {
                    this.browseFilters.drinkType = this.browseDrinkType;
                }
                if (this.browseTypeCategory) {
                    this.browseFilters.typeCategory = this.browseTypeCategory;
                }
            },

            async runBrowse() {
                try {
                    // Load filter dropdown options
                    await Promise.all([
                        this.loadDrinkTypes(),
                        this.loadTypeCategories(),
                        this.loadCountries()
                    ]);

                    // Load initial listings
                    await this.browseListings();

                    this.dataLoaded = true;
                }
                catch (error) {
                    console.error(error);
                    this.loadError = true;
                }
            },

            // Load dropdown options
            async loadDrinkTypes() {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getDrinkTypes`);
                    this.drinkTypeList = response.data;
                } catch (error) {
                    console.error('Error loading drink types:', error);
                }
            },

            async loadTypeCategories() {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getTypeCategories`);
                    this.typeCategoryList = response.data;
                } catch (error) {
                    console.error('Error loading type categories:', error);
                }
            },

            async loadCountries() {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getCountries`);
                    this.countryList = response.data;
                } catch (error) {
                    console.error('Error loading countries:', error);
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

                        // Extract tried and want to try drinks from user's drink lists
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

            // Browse listings using filters
            async browseListings(isLoadMore = false) {
                try {
                    // Build query parameters
                    const params = new URLSearchParams();
                    
                    if (this.browseFilters.drinkType) {
                        params.append('drinkType', this.browseFilters.drinkType);
                    }
                    if (this.browseFilters.typeCategory) {
                        params.append('typeCategory', this.browseFilters.typeCategory);
                    }
                    if (this.browseFilters.originCountry) {
                        params.append('originCountry', this.browseFilters.originCountry);
                    }
                    if (this.browseFilters.minRating) {
                        params.append('minRating', this.browseFilters.minRating);
                    }
                    if (this.browseFilters.maxRating) {
                        params.append('maxRating', this.browseFilters.maxRating);
                    }
                    
                    params.append('offset', this.offsetListings.toString());
                    params.append('limit', this.recordsPerLoad.toString());

                    const response = await this.$axios.get(
                        `${process.env.VUE_APP_API_URL}/getData/getListingsByFilters?${params.toString()}`
                    );
                    
                    if (isLoadMore) {
                        // Append new results for load more
                        this.resultListings = this.resultListings.concat(response.data);
                    } else {
                        // Replace results for new filter/sort
                        this.resultListings = response.data;
                        this.offsetListings = 0;
                    }

                    // Update pagination state
                    this.offsetListings += response.data.length;
                    
                    // Check if no more listings
                    if (response.data.length < this.recordsPerLoad) {
                        this.noMoreListings = true;
                    } else {
                        this.noMoreListings = false;
                    }

                } 
                catch (error) {
                    console.error('Error browsing listings:', error);
                    this.loadError = true;
                }
            },

            // Load more listings (lazy loading)
            async loadMoreListings() {
                await this.browseListings(true);
            },

            // Filter functions
            filterByDrinkType(drinkType) {
                this.browseFilters.drinkType = drinkType;
                this.applyFilters();
            },

            filterByTypeCategory(typeCategory) {
                this.browseFilters.typeCategory = typeCategory;
                this.applyFilters();
            },

            filterByCountry(country) {
                this.browseFilters.originCountry = country;
                this.applyFilters();
            },

            clearAllFilters() {
                this.browseFilters = {
                    drinkType: '',
                    typeCategory: '',
                    originCountry: '',
                    minRating: '',
                    maxRating: ''
                };
                // Restore initial filter from route if it exists
                this.initializeBrowseFilters();
                this.applyFilters();
            },

            async applyFilters() {
                // Reset pagination
                this.offsetListings = 0;
                this.noMoreListings = false;
                
                // Reload listings with new filters
                await this.browseListings(false);
            },

            // Filter display text for button
            getFilterDisplayText() {
                const activeFilters = [];
                if (this.browseFilters.drinkType) activeFilters.push(this.browseFilters.drinkType);
                if (this.browseFilters.typeCategory) activeFilters.push(this.browseFilters.typeCategory);
                if (this.browseFilters.originCountry) activeFilters.push(this.browseFilters.originCountry);
                
                if (activeFilters.length === 0) return 'Filter';
                if (activeFilters.length === 1) return `Filter: ${activeFilters[0]}`;
                return `Filter: ${activeFilters.length} active`;
            },

            // Sort functions
            sortByCategory(category) {
                this.sortSelection.category = category;
                this.sortResults();
            },

            sortResults() {
                let category = this.sortSelection.category;

                // #1: Alphabetical (A - Z)
                if (category == 'Alphabetical (A - Z)') {
                    this.resultListings.sort((a, b) => {
                        return a.listingName.localeCompare(b.listingName);
                    });
                }
                // #2: Alphabetical (Z - A)
                else if (category == 'Alphabetical (Z - A)') {
                    this.resultListings.sort((a, b) => {
                        return b.listingName.localeCompare(a.listingName);
                    });
                }
                // #3: Date (Newest - Oldest)
                else if (category == 'Date (Newest - Oldest)') {
                    this.resultListings.sort((a, b) => {
                        return new Date(b.addedDate) - new Date(a.addedDate);
                    });
                }
                // #4: Date (Oldest - Newest)
                else if (category == 'Date (Oldest - Newest)') {
                    this.resultListings.sort((a, b) => {
                        return new Date(a.addedDate) - new Date(b.addedDate);
                    });
                }
                // #5: Ratings (Highest - Lowest)
                else if (category == 'Ratings (Highest - Lowest)') {
                    this.resultListings.sort((a, b) => {
                        const aRating = a.averageRating === '-' ? 0 : parseFloat(a.averageRating);
                        const bRating = b.averageRating === '-' ? 0 : parseFloat(b.averageRating);
                        return bRating - aRating;
                    });
                }
                // #6: Ratings (Lowest - Highest)
                else if (category == 'Ratings (Lowest - Highest)') {
                    this.resultListings.sort((a, b) => {
                        const aRating = a.averageRating === '-' ? 0 : parseFloat(a.averageRating);
                        const bRating = b.averageRating === '-' ? 0 : parseFloat(b.averageRating);
                        return aRating - bRating;
                    });
                }
                // Default: Smart Order (as returned by backend)
                else {
                    // Reset to original backend order by reloading
                    this.applyFilters();
                }
            },

            // Bookmark functionality
            handleIconClick(data) {
                this.bookmarkListingID = data;
            },

            // Format date
            formatDate(dateTimeString) {
                let date = new Date(dateTimeString);
                let day = String(date.getDate()).padStart(2, '0');
                let month = String(date.getMonth() + 1).padStart(2, '0');
                let year = date.getFullYear();
                let formattedDate = `${day}/${month}/${year}`;
                return formattedDate;
            },
        }
    }
</script>

<style scoped>
.image-container img {
    transition: transform 0.2s ease-in-out;
}

.image-container img:hover {
    transform: scale(1.05);
}

.scrollable-long {
    max-height: 4em;
    overflow: hidden;
    text-overflow: ellipsis;
}

.funnel-svg-dimensions {
    height: 20px;
    width: 20px;
}

.mobile-fs-6 {
    font-size: 0.9rem;
}

.mobile-fs-7 {
    font-size: 0.8rem;
}

@media (max-width: 768px) {
    .mobile-view-hide {
        display: none !important;
    }
    
    .mobile-view-show {
        display: block !important;
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
</style>
