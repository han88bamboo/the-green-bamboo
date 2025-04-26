<template>
    <NavBar />

    <!-- Display when search is in progress -->
    <div class="text-info-emphasis fst-italic fw-bold fs-5 pt-5" v-if="!dataLoaded"> 
        <span>Currently searching, please hold on!</span>
        <br><br>
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    
    <!-- Display when searching encounters an error -->
    <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="loadError"> 
        <span>An error occurred while searching, please try refreshing the page!</span>
        <br>
        <button class="btn primary-btn btn-sm" @click="()=>{this.$router.go(0)}">
            <span class="fs-5 fst-italic"> Refresh Page </span>
        </button>
    </div>
    
    <!-- Header -->
    <div class="container pt-3">

        <!-- Display requests after data loaded -->
        <div v-if="dataLoaded && !loadError">

            <div class="row">

                <!-- BACK BUTTON, FORM TITLE, SEARCH TERM -->
                <div class="col-md-8 col-12">

                    <div class="row">
                    
                        <!-- Back Button -->
                        <div class="d-grid col-2">
                            <button class="btn primary-light-dropdown-homepage btn-sm" @click="()=>{this.$router.go(-1)}">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-arrow-left-circle" viewBox="0 0 16 16" v-on:click="previousListing">
                                    <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-4.5-.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"/>
                                </svg>
                            </button>
                        </div>

                        <!-- Form Title -->
                        <div class="d-grid col-10" style="color:black;">
                            <p class="fw-bold fs-3 m-0 text-start">Search Results </p>
                        </div>
                    </div>



                    <!-- Request / Create Listing Link (font size reduced at smaller screen width) -->
                    <div style="margin-top: 50px;" class="row mobile-view-hide">
                        <router-link class="col-12 text-decoration-none" v-if="role == 'producer'" :to="{ path: '/Producer/Producer-Create-Listing/' }">
                            <p class="d-none d-md-block fs-5 fst-italic text-start">Don't see what you're looking for? Create a new listing here!</p>
                            <p class="d-md-none fs-6 fst-italic text-start">Don't see what you're looking for? Create a new listing here!</p>
                        </router-link>
                        <router-link class="col-12 text-decoration-none" v-if="role == 'user'" :to="{ path: '/request/new/' }">
                            <p class="d-none d-md-block fs-5 fst-italic text-start">Don't see what you're looking for? Request a new listing here!</p>
                            <p class="d-md-none fs-6 fst-italic text-start">Don't see what you're looking for? Request a new listing here!</p>
                        </router-link>
                        <router-link class="col-12 text-decoration-none" v-if="role != 'producer' && role != 'user'" :to="{ path: '/login' }">
                            <p class="d-none d-md-block fs-5 fst-italic text-start">Don't see what you're looking for? Login to request a new listing!</p>
                            <p class="d-md-none fs-6 fst-italic text-start">Don't see what you're looking for? Login to request a new listing!</p>
                        </router-link>
                    </div>

                </div>

                <div class="col-md-4 col-12">

                    <div class="row d-flex justify-content-center">



                        <div class="col-8 mobile-view-show mobile-pe-0">
                            <router-link class=" text-decoration-none" v-if="role == 'producer'" :to="{ path: '/Producer/Producer-Create-Listing/' }">
                                <p class="d-none d-md-block fs-5 fst-italic text-start">Don't see what you're looking for? Create a new listing here!</p>
                                <p class="d-md-none fs-6 fst-italic text-start">Don't see what you're looking for? Create a new listing here!</p>
                            </router-link>
                            <router-link class="text-decoration-none" v-if="role == 'user'" :to="{ path: '/request/new/' }">
                                <p class="d-none d-md-block fs-5 fst-italic text-start">Don't see what you're looking for? Request a new listing here!</p>
                                <p class="d-md-none fs-6 fst-italic text-start">Don't see what you're looking for? Request a new listing here!</p>
                            </router-link>
                            <router-link class="text-decoration-none" v-if="role != 'producer' && role != 'user'" :to="{ path: '/login' }">
                                <p class="d-none d-md-block fs-5 fst-italic text-start">Don't see what you're looking for? Login to request a new listing!</p>
                                <p class="d-md-none fs-6 fst-italic text-start">Don't see what you're looking for? Login to request a new listing!</p>
                            </router-link>
                        </div>

                        <!-- Sort Options -->
                        <div class="mobile-col-2 mobile-ps-0 col-xxl-6 col-md-12 col-sm-5 col-12 mb-xxl-0 mb-md-2 mb-sm-0 mb-2 dropdown">
                            <div class="d-grid gap-2">
                                <button class="btn primary-light-dropdown-homepage dropdown-toggle mobile-view-remove-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false" style="white-space: nowrap; overflow:hidden; text-overflow: ellipsis;/* min-width: 200px;*/">
                                    <svg xmlns="http://www.w3.org/2000/svg" style="/*height:25px;width:25px;*/"  fill="currentColor" class="bi bi-sort-down funnel-svg-dimensions" viewBox="0 0 16 16">
                                        <path d="M3.5 2.5a.5.5 0 0 0-1 0v8.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L3.5 11.293zm3.5 1a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/>
                                    </svg>
                                    <span class="mobile-view-hide" style="margin-left: 5px;">Sort: {{ sortSelection.category != '' ? sortSelection.category : 'by Category' }}</span>
                                </button>
                                <ul class="dropdown-menu">
                                    <li><span class="dropdown-item" @click="sortByCategory('')"> Clear Sort </span></li>
                                    <li><hr class="dropdown-divider"></li>
                                    <li v-for="category in sortCategoryList[tabActive]" :key="category">
                                        <span class="dropdown-item" @click="sortByCategory(category)"> {{ category }} </span>
                                    </li>
                                </ul>
                            </div>
                        </div> 
                    
                    </div>

                </div>

            </div>
            

            <!-- navtab to toggle between search results -->
            <nav class="pb-0 mobile-px-0">
                <div class="nav nav-tabs justify-content-center" id="nav-tab" role="tablist">
                    <!-- Listings -->
                    <button class="nav-link active col-lg-3 mobile-col-4 xcol-12 px-1" id="nav-listings-tab" data-bs-toggle="tab" data-bs-target="#nav-listings" type="button" role="tab" aria-controls="nav-listings" aria-selected="true" @click="changeActiveTabStatus('listings')"> 
                        <span class="d-flex align-items-center justify-content-center mb-0">
                            Listings &nbsp;
                            <span v-if="resultListings.length > 0" class="rounded-circle mobile-mx-0 mx-3 d-flex align-items-center justify-content-center"> 
                                <p class="m-0">{{ resultListings.length }}</p>
                            </span>
                            <span v-else class="rounded-circle-no-results mobile-mx-0 mx-3 d-flex align-items-center justify-content-center"> 
                                <p class="m-0">{{ resultListings.length }}</p>
                            </span> 
                        </span>
                    </button>
                </div>
            </nav>

            <!-- Display Listings -->
            <div class="tab-content" id="nav-tabContent">

                <!-- NAVTAB 1: LISTINGS -->
                <div class="tab-pane fade show active" id="nav-listings" role="tabpanel" aria-labelledby="nav-listings-tab" style="color:black;">
                    <p class="fw-bold fst-italic fs-5 m-0 py-2 mobile-view-hide" v-if="resultListings.length > 0">Viewing: {{ resultListings.length }} Listing Search Results</p>
                    <p class="fw-bold fst-italic fs-5 m-0 py-2" v-else>No Listing Results Found!</p>
                    
                    <div class="container text-start">
                        <div class="row" v-for="resultListing in resultListings" :key="resultListing.id">
                            <hr>
                            <!-- Image -->
                            <div class="col-lg-3 col-12 image-container mb-3 producer-profile-no-left-padding-large-screen mobile-col-3 mobile-mx-0 mobile-px-0 mobile-mb-0">
                                <router-link :to="{ path: '/listing/view/' + resultListing.id }">
                                    <img v-if="resultListing['photo']" :src="resultListing['photo']" class="img-border img-fluid object-fit-cover" style="width:256px; height:256px">
                                    <img v-else src="../../Images/Drinks/Placeholder.png" class=" img-border img-fluid object-fit-cover" style="/*width:256px; height:256px*/"> 
                                </router-link>
                                <!--<BookmarkIcon 
                                    v-if="user" 
                                    :user="user" 
                                    :listing="resultListing" 
                                    :overlay="true"
                                    size="30"
                                    @icon-clicked="handleIconClick" />-->
                            </div>

                            <div class="col-lg-8 col-12 ps-3 mobile-col-7 mobile-pe-0 mobile-ps-1 mobile-view-show">
                                <!-- Listing Name + Router Link -->
                                <router-link class="xtext-dark xtext-decoration-none" :to="{ path: '/listing/view/' + resultListing.id }">
                                    <p class="default-text fs-5 mobile-fs-6" style="margin-bottom: 0.3rem;"><b><u>{{ resultListing['listingName'] }}</u></b></p>
                                </router-link>
                                <p class="text-start mb-1 mobile-fs-7"> 
                                    {{ resultListing["bottler"] }} | {{ resultListing["drinkType"] }} | {{ resultListing["typeCategory"] }} | {{ resultListing["abv"] }} ABV | {{ resultListing["originCountry"] }} 
                                </p>
                            </div>

                            <div class="mobile-col-2 mobile-pe-0 mobile-ps-1 mobile-view-show">
                                <div class="d-flex flex-column align-items-center ps-lg-3" >
                                    <p class="fs-3 fw-bold rating-text text-end d-flex align-items-center mobile-fs-5" style="margin-bottom: 0.1rem;">    
                                        {{ getRatings(resultListing) }}
                                    </p>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                    </svg>
                                    
                                </div>
                            </div>

                            <!-- Details -->
                            <div class="row col-lg-9 col-12 mobile-view-hide">

                                <div class="col-lg-8 col-12">
                                    <!-- Listing Name + Router Link -->
                                    <router-link class="text-dark text-decoration-none" :to="{ path: '/listing/view/' + resultListing.id }">
                                        <h4 class="fw-bold my-1">{{ resultListing['listingName'] }}</h4>
                                    </router-link>
                                    <!-- Producer Name + Router Link -->
                                    <router-link class="text-secondary-emphasis text-decoration-none" :to="{ path: '/profile/producer/' + resultListing.producerID }">
                                        <p class="m-0">
                                            <b> Producer: </b>
                                            {{ getProducerName(resultListing['producerID']) }}
                                        </p>
                                        <p class="fw-bold fst-italic m-0" v-if="resultListing['bottler'] != 'OB'">Bottler: {{ resultListing['bottler'] }}</p>
                                    </router-link>
                                    <!-- Country of Origin -->
                                    <p class="m-0">
                                        <b> Origin: </b>
                                        {{ resultListing['originCountry'] }}
                                    </p>
                                    <!-- Added Date -->
                                    <p class="m-0 xmb-3">
                                        <b> Date Added: </b>
                                        {{ formatDate(resultListing['addedDate']) }}
                                    </p>
                                    <!-- Drink Type / Type Category -->
                                    <p class="m-0">
                                        <b> Type: </b>
                                        {{ resultListing['drinkType'] }}
                                    </p>
                                    <p class="m-0" v-if="resultListing['typeCategory']">
                                        <b> Category: </b>
                                        {{ resultListing['typeCategory'] }}</p>
                                    <!-- Rating -->
                                    <p class="m-0">
                                        <b> Rating: </b>
                                        {{ getRatings(resultListing) }}
                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                                            <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                        </svg>
                                    </p>
                                </div>

                                <div class="col-lg-4 col-12 text-xl-end text-start" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                    
                                    
                                    <!-- Buttons -->
                                    <div class="row py-1">
                                        <!-- have tried button -->
                                        <div class="col-5 m-0 p-0">
                                            <div v-if="user" v-html="checkDrinkLists(resultListing).buttons.haveTried" class="d-grid w-100" @click="addToTriedList(resultListing)"></div>
                                        </div>
                                        <!-- want to try button -->
                                        <div class="col-5 m-0 p-0">
                                            <div v-if="user" v-html="checkDrinkLists(resultListing).buttons.wantToTry" class="d-grid w-100" @click="addToWantList(resultListing)"></div>
                                        </div>
                                        <!-- bookmark button -->
                                        <div class="col-2 m-0 text-end">
                                            <BookmarkIcon 
                                                v-if="user" 
                                                :user="user" 
                                                :listing="resultListing" 
                                                :overlay="false"
                                                size="30"
                                                @icon-clicked="handleIconClick" />
                                        </div>
                                    </div>
                                </div>

                                <!-- Description -->
                                <p class="fst-italic scrollable-long">{{ resultListing["officialDesc"] }}</p>

                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <BookmarkModal 
                v-if="user"
                :user="user" 
                :listings="listings" 
                :listingID="bookmarkListingID" />
        </div>
    </div>
</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    import BookmarkIcon from '@/components/BookmarkIcon.vue';
    import BookmarkModal from '@/components/BookmarkModal.vue';

    export default {
        name: "SearchView",
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
                searchTerm: this.$route.params.input,
                searchFilter: {
                    drinkType: ''
                },
                drinkTypeList: [],
                producerList: [],
                venueList: [],
                originalResults: [],
                resultListings: [],
                producerListings: [],
                venueListings: [],
                listings: [],

                // reviews
                reviews: [],

                // for sort function
                sortSelection: {
                    category: ''
                },
                sortCategoryList: {
                    listings: [
                        'Alphabetical (A - Z)',
                        'Alphabetical (Z - A)',
                        'Date (Newest - Oldest)',
                        'Date (Oldest - Newest)',
                        'Ratings (Highest - Lowest)',
                        'Ratings (Lowest - Highest)',
                    ],
                    producers: [
                        'Alphabetical (A - Z)',
                        'Alphabetical (Z - A)',
                        'Ratings (Highest - Lowest)',
                        'Ratings (Lowest - Highest)',
                    ],
                    venues: [
                        'Alphabetical (A - Z)',
                        'Alphabetical (Z - A)',
                        'Ratings (Highest - Lowest)',
                        'Ratings (Lowest - Highest)',
                    ]
                },
                sortedListings: [],

                userID: "",
                userType: "",

                // for bookmark
                user: null,
                userBookmarks: [],
                drinkList:  {
                                "haveTried": [""],
                                "wantToTry": [""]
                            },
                haveTried: false,
                wantToTry: false,

                // for bookmark component
                bookmarkListingID: {},

                // for search results display
                tabActive: 'listings',
            }
        },
        computed: {
            effectiveSearchTerm() {
                return this.searchTerm || this.$route.params.tag;
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
            }
            this.loadData();
        },
        methods: {
            async loadData() {
            try {
                const logo = this.$route.query.logo; // Get the logo from URL parameters
                const labels = this.$route.query.labels
                ? this.$route.query.labels.split(",")
                : []; // Get the labels from URL, assuming it's a comma-separated list
                const detectedText = this.$route.query.detectedText
                ? this.$route.query.detectedText.split(",")
                : []; // Get the detected text from URL, assuming it's a comma-separated list

                if (!logo && labels.length === 0 && detectedText.length === 0) {
                console.warn("No logo, labels, or text parameters found in query.");
                return;
                }

                const requestData = {
                logo: logo,
                labels: labels,
                detectedText: detectedText,
                };

                const response = await this.$axios.post(
                `${process.env.VUE_APP_API_URL}/getData/getImageSearchResults`,
                requestData, // Pass the entire request body
                { headers: { "Content-Type": "application/json" } }
                );

                if (response.status === 200 && response.data.length > 0) {
                this.listings = response.data; // Store API results
                this.resultListings = this.listings;
                this.dataLoaded = true;
                } else {
                console.warn("No listings found for the given parameters.");
                this.listings = [];
                this.resultListings = [];
                this.dataLoaded = false;
                }
            } catch (error) {
                console.error("Error fetching listings:", error);
                this.listings = [];
                this.resultListings = [];
                this.dataLoaded = false;
            }},
            
            sortResults() {
                let category = this.sortSelection.category;

                // ------ SORT LISTINGS --------
                if (this.tabActive == 'listings') {
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
                    // [DEFAULT] #4: Date (Oldest - Newest)
                    else if (category == '' || category == 'Date (Oldest - Newest)') {
                        this.resultListings.sort((a, b) => {
                            return new Date(a.addedDate) - new Date(b.addedDate);
                        });
                    }
                    // #5: Ratings (Highest - Lowest)
                    else if (category == 'Ratings (Highest - Lowest)') {
                        this.resultListings.sort((a, b) => {
                            return this.getAllRatings(b) - this.getAllRatings(a);
                        });
                    }
                    // #6: Ratings (Lowest - Highest)
                    else if (category == 'Ratings (Lowest - Highest)') {
                        this.resultListings.sort((a, b) => {
                            return this.getAllRatings(a) - this.getAllRatings(b);
                        });
                    }
                }

                // ------ SORT PRODUCERS ------
                else if (this.tabActive == 'producers') {
                    // #1: [DEFAULT] Alphabetical (A - Z)
                    if (category == '' || category == 'Alphabetical (A - Z)') {
                        this.producerListings.sort((a, b) => {
                            return a.producerName.localeCompare(b.producerName);
                        });
                    }
                    // #2: Alphabetical (Z - A)
                    else if (category == 'Alphabetical (Z - A)') {
                        this.producerListings.sort((a, b) => {
                            return b.producerName.localeCompare(a.producerName);
                        });
                    }
                    // #3: Ratings (Highest - Lowest)
                    else if (category == 'Ratings (Highest - Lowest)') {
                        this.producerListings.sort((a, b) => {
                            return this.getAvgProducerRating(b) - this.getAvgProducerRating(a);
                        });
                    }
                    // #4: Ratings (Lowest - Highest)
                    else if (category == 'Ratings (Lowest - Highest)') {
                        this.producerListings.sort((a, b) => {
                            return this.getAvgProducerRating(a) - this.getAvgProducerRating(b);
                        });
                    }
                }

                // ------ SORT VENUES ------
                else if (this.tabActive == 'venues') {
                    // #1: [DEFAULT] Alphabetical (A - Z)
                    if (category == '' || category == 'Alphabetical (A - Z)') {
                        this.venueListings.sort((a, b) => {
                            return a.venueName.localeCompare(b.venueName);
                        });
                    }
                    // #2: Alphabetical (Z - A)
                    else if (category == 'Alphabetical (Z - A)') {
                        this.venueListings.sort((a, b) => {
                            return b.venueName.localeCompare(a.venueName);
                        });
                    }
                    // #3: Ratings (Highest - Lowest)
                    else if (category == 'Ratings (Highest - Lowest)') {
                        this.venueListings.sort((a, b) => {
                            return this.getAvgVenueRating(b) - this.getAvgVenueRating(a);
                        });
                    }
                    // #4: Ratings (Lowest - Highest)
                    else if (category == 'Ratings (Lowest - Highest)') {
                        this.venueListings.sort((a, b) => {
                            return this.getAvgVenueRating(a) - this.getAvgVenueRating(b);
                        });
                    }
                }
            },

            // Sort Support Function (Category)
            sortByCategory(category) {
                // Check if the selected filter is the same as the current filter
                if (this.sortSelection.category == category) {
                    return;
                }
                else {
                    this.sortSelection.category = category
                    this.sortResults();
                }
            },

            // get ratings for a listing --> return "-" if no ratings
            getRatings(listing) {
                const ratings = this.reviews.filter((rating) => rating["reviewTarget"] == listing['id']);
                // if there are no ratings
                if (ratings.length == 0) return "-";
                // else there are ratings
                const averageRating = ratings.reduce((total, rating) => {
                    return total + parseFloat(rating["rating"]);
                }, 0) / ratings.length;

                return averageRating.toFixed(1);
            },

            // get ratings for a listing --> return 0 if no ratings
            getAllRatings(listing) {
                const ratings = this.reviews.filter((rating) => {
                    return rating["reviewTarget"] == listing['id'];
                });
                // if there are no ratings
                if (ratings.length == 0) {
                    return 0;
                }
                // else there are ratings
                const averageRating = ratings.reduce((total, rating) => {
                    return total + rating["rating"];
                }, 0) / ratings.length;
                // round to 1 decimal place
                const roundedRating = Math.round(averageRating * 10) / 10;
                return roundedRating;
            },

            // get average rating for producer --> return "-" if no ratings
            getAllProducerRating(producer) {
                let allProducerReviews = this.reviews.filter(review => {
                    let review_target = review.reviewTarget;
                    let all_drinks = this.listings.filter(listing => listing.producerID == producer.id);
                    return all_drinks.some(drink => drink.id === review_target);
                });
                // if there are no ratings
                if (allProducerReviews.length == 0) {
                    return "-";
                }
                // else there are ratings
                const averageRating = allProducerReviews.reduce((total, review) => {
                    return total + parseFloat(review.rating);
                }, 0) / allProducerReviews.length;
                // round to 1 decimal place
                return averageRating.toFixed(1);
            },

            // get average rating for producer --> return 0 if no ratings
            getAvgProducerRating(producer) {
                let allProducerReviews = this.reviews.filter(review => {
                    let review_target = review.reviewTarget;
                    let all_drinks = this.listings.filter(listing => listing.producerID == producer.id);
                    return all_drinks.some(drink => drink.id === review_target);
                });
                // if there are no ratings
                if (allProducerReviews.length == 0) {
                    return 0;
                }
                // else there are ratings
                const averageRating = allProducerReviews.reduce((total, review) => {
                    return total + parseFloat(review.rating);
                }, 0) / allProducerReviews.length;
                // round to 1 decimal place
                return averageRating.toFixed(1);
            },

            // get all drinks that a venue has
            getAllVenueDrinks(venue) {
                let allMenuItems = venue["menu"]
                let allSectionMenus = allMenuItems.reduce((acc, menuItem) => {
                    return acc.concat(menuItem.sectionMenu);
                }, []);
                let allListingsIDs = allSectionMenus.reduce((acc, menuItem) => {
                    return acc.concat(menuItem.itemID); 
                }, []);
                let uniqueListingsIDs = [...new Set(allListingsIDs.map(item => item))];
                let allVenueDrinks = this.listings.filter(listing => {
                    let listing_id = listing.id;
                    return uniqueListingsIDs.includes(listing_id);
                });
                return allVenueDrinks
            },

            // get average rating for venue --> return "-" if no ratings
            getAllVenueRating(venue) {
                let allVenueReviews = this.reviews.filter(review => {
                    let review_target = review.reviewTarget;
                    let all_drinks = this.getAllVenueDrinks(venue)
                    return all_drinks.some(drink => drink.id === review_target);
                });
                // if there are no ratings
                if (allVenueReviews.length == 0) {
                    return "-";
                }
                // else there are ratings
                const averageRating = allVenueReviews.reduce((total, review) => {
                    return total + parseFloat(review.rating);
                }, 0) / allVenueReviews.length;
                // round to 1 decimal place
                return averageRating.toFixed(1);
            },

            // get average rating for venue --> return 0 if no ratings
            getAvgVenueRating(venue) {
                let allVenueReviews = this.reviews.filter(review => {
                    let review_target = review.reviewTarget;
                    let all_drinks = this.getAllVenueDrinks(venue)
                    return all_drinks.some(drink => drink.id === review_target);
                });
                // if there are no ratings
                if (allVenueReviews.length == 0) {
                    return 0;
                }
                // else there are ratings
                const averageRating = allVenueReviews.reduce((total, review) => {
                    return total + parseFloat(review.rating);
                }, 0) / allVenueReviews.length;
                // round to 1 decimal place
                return averageRating.toFixed(1);
            },

            // for bookmark component
            handleIconClick(data) {
                this.bookmarkListingID = data
            },

            // format date
            formatDate(dateTimeString) {
                let date = new Date(dateTimeString);

                // splitting the date into year, month, and day
                let day = String(date.getDate()).padStart(2, '0');
                let month = String(date.getMonth() + 1).padStart(2, '0');
                let year = date.getFullYear();

                // formatting the date
                let formattedDate = `${day}/${month}/${year}`;
                return formattedDate;
            },

            checkDrinkLists(listing) {
                const haveTried = this.drinkList.haveTried.includes(listing.listingName);
                const wantToTry = this.drinkList.wantToTry.includes(listing.listingName);

                const haveTriedButton = `
                <button type="button" class="btn custom-drink-list-btn rounded-0 ${haveTried ? 'disabled' : ''}">
                    Have tried
                </button>
                `;

                const wantToTryButton = `
                <button type="button" class="btn custom-drink-list-btn rounded-0 ${wantToTry ? 'disabled' : ''}">
                    Want to try
                </button>
                `;

                return {
                    buttons: {
                        haveTried: haveTriedButton,
                        wantToTry: wantToTryButton,
                    }
                }
            },

            async addToTriedList(resultListing){
                let responseCode = "";
                
                let submitData = {
                            "date": new Date(),
                            "listingID": resultListing.id,
                            "userID": this.userID,
                            
                }
                await this.$axios.put(`${process.env.VUE_APP_API_URL}/addToList/addToTried/`, submitData)
                    .then((response) => {
                        responseCode = response.data.code;
                    })
                    .catch((error) => {
                        console.error(error);
                        responseCode = error.response.data.code;
                    });

                if (responseCode == 200) {
                    console.log("Success")
                } else {
                    console.log("Fail");
                }
                window.location.reload();
            },

            async addToWantList(resultListing){
                let responseCode = "";
                let submitData = {
                            "date": new Date(),
                            "listingID": resultListing.id,
                            "userID": this.userID,
                            
                }
                await this.$axios.put(`${process.env.VUE_APP_API_URL}/addToList/addToWant/`, submitData)
                    .then((response) => {
                        responseCode = response.data.code;
                    })
                    .catch((error) => {
                        console.error(error);
                        responseCode = error.response.data.code;
                    });

                if (responseCode == 210) {
                    console.log("Success")
                } else {
                    console.log("Fail");
                }
                window.location.reload();
            },

            // to change active tab
            changeActiveTabStatus(selectedTab) {
                // change active tab
                this.tabActive = selectedTab;
                // clear sort selection
                this.sortSelection.category = '';
            },

            // get producerName for a listing based on producerID
            getProducerName(producerID) {
                const producer = this.producerList.find((producer) => {
                    return producer["id"] == producerID;
                });
                // ensures that producer is found before accessing "producerName"
                if (producer) {
                    const producerName = producer["producerName"];
                    return producerName;
                }
                else {
                    return null;
                }
            },
        }
    }
</script>