<!-- HTML -->
<template>
    <NavBar />

     <!-- [if] no search input -->
    <div>
        <!-- header -->

        <!-- end of header -->

        <!-- main content -->
        <div class="container pt-3">
            <div class="row">
                <!-- your drinks shelf & brands you follow -->
                
                <!-- discover, following & filter by drink type -->
                <div class="col-9">
                    <div class="container">
                        <!-- buttons -->
                        
                        
                        <!-- listings -->
                        <div class="row">
                            <!-- v-loop for each listing -->
                            <div class="container text-start">
                                <div class="p-3">
                                    
                                    <div class="row">
                                        <!-- image -->
                                        <div class="col-4 image-container">
                                            <img src="../../../Images/Sample/beer.png" style="width: 300px; height: 300px;" class="img-border">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-bookmark overlay-icon" viewBox="0 0 16 16">
                                                <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1z"/>
                                            </svg>
                                        </div>
                                        <!-- details -->
                                        <div class="col-8 ps-5">
                                            <!-- review -->
                                            <div class="row">
                                                <a class="default-clickable-text fst-italic scrollable">
                                                    <h5> "{{ getReviews(editable) }}". </h5>
                                                </a>
                                            </div>
                                            <!-- rating -->
                                            <div class="row pt-5"> 
                                                <div class="col-6">
                                                    <h1 class="rating-text">
                                                        {{ getRatings(editable) }}
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                                                            <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                        </svg>
                                                    </h1>
                                                </div>
                                                <div class="col-6">
                                                    <router-link :to="{ path: '/listing/edit/' + this.ID }">
                                                        <a class="btn secondary-btn btn-md">Edit</a>
                                                    </router-link>
                                                        
                                                    
                                                </div>
                                                
                                            </div>
                                            <!-- expression name -->
                                            <div class="row pt-2">
                                                <a class="primary-clickable-text">
                                                    <h4> <b> {{ this.tempExpressionName }} </b> </h4>
                                                </a>
                                            </div>
                                            <!-- producer -->
                                            <div class="row">
                                                <h5> {{ this.tempProducer }} </h5> 
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                        </div> <!-- end of listings -->
                    </div> <!-- end of container -->
                </div> <!-- end of discover, following & filter by drink type -->
            </div> <!-- end of row -->
        </div>
    </div>
    

    

</template>



<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>
    import NavBar from '@/components/NavBar.vue';

    export default {
        components: {
            NavBar
        },
        data() {
            return {
                // data from database
                countries: [],
                listings: [],
                producers: [],
                reviews: [],
                users: [],
                venues: [],
                // search
                search: false,
                searchInput: '',
                searchTerm: '',
                searchResults: [],
                filteredListings: [],
                editable: [],
                drinkCategories:[],
                ID: '',
                updateStatus: false,
                tempExpressionName: '',
                tempProducerID: '',
                tempProducer: '',
                tempCountry: '',
                tempDrinkType: '',
                tempDrinkCategory:"" ,
                tempTypeCategoryList: null,
                tempAge: '',
                tempABV: '',
                tempReviewLink: '',
                tempSourceLink: '',
                tempDescription: '',
                tempBottler: '',
                drinkTypeInfo: null,
                chooseCategory: false,
                independentStatus:false
                


                
            };
        },
        mounted() {
            this.loadData();
            
            
        },
        methods: {
            // load data from database
            async loadData() {
                // Countries
                try {
                    const response = await this.$axios.get('http://127.0.0.1:5000/getData/getCountries');
                    this.countries = response.data;
                } 
                catch (error) {
                    console.error(error);
                }
                // Listings
                try {
                    const response = await this.$axios.get('http://127.0.0.1:5000/getData/getListings');
                    this.listings = response.data;
                    // originally, make filteredListings the entire collection of listings
                    this.filteredListings = this.listings;
                    this.editable = this.listings[0];
                    this.ID = this.editable["_id"]["$oid"];
                    this.tempExpressionName = this.editable["listingName"];
                    this.tempProducerID = this.editable["producerID"];
                    this.tempBottler = this.editable["bottler"];
                    this.tempCountry = this.editable["originCountry"];
                    this.tempDrinkType = this.editable["drinkType"];
                    this.tempDrinkCategory = this.editable["typeCategory"];
                    this.tempAge = this.editable["age"];
                    this.tempABV = this.editable["abv"];
                    this.tempReviewLink = this.editable["reviewLink"];
                    this.tempDescription = this.editable["officialDesc"];
                    this.tempSourceLink = this.editable["sourceLink"];
                    this.photo = this.editable["photo"];
                } 
                catch (error) {
                    console.error(error);
                }
                // Producers
                try {
                    const response = await this.$axios.get('http://127.0.0.1:5000/getData/getProducers');
                    this.producers = response.data;

                    for (let producer of this.producers) {
                    if (JSON.stringify(producer._id) == JSON.stringify(this.tempProducerID)) {
                        this.tempProducer = producer.producerName;
                        
                    }
                    }
                    
                } 
                catch (error) {
                    console.error(error);
                }
                // Reviews
                try {
                    const response = await this.$axios.get('http://127.0.0.1:5000/getData/getReviews');
                    this.reviews = response.data;
                }
                catch (error) {
                    console.error(error);
                }
                // Users
                try {
                    const response = await this.$axios.get('http://127.0.0.1:5000/getData/getUsers');
                    this.users = response.data;
                } 
                catch (error) {
                    console.error(error);
                }
                // Venues
                try {
                    const response = await this.$axios.get('http://127.0.0.1:5000/getData/getVenues');
                    this.venues = response.data;
                } 
                catch (error) {
                    console.error(error);
                }
                // Drink Categories
                try {
                    const response = await this.$axios.get('http://127.0.0.1:5000/getData/getDrinkTypes');
                    this.drinkCategories = response.data;
                } 
                catch (error) {
                    console.error(error);
                }
            },

            updateListing() {
                this.updateStatus = true;
            },

            saveListing() {
                this.updateStatus = false;
                
                
            },
            getDrinkCategoryList() {
                for (let category of this.drinkCategories) {
                if (category.drinkType == this.tempDrinkType) {
                    this.drinkTypeInfo = category;
                    this.tempTypeCategoryList = category.typeCategory;
                    }
                }

            },
            independentBottler(event) {
                this.independentStatus = event.target.checked;
                // Declare producerNamePlaceholder outside of the loop
                let bottlerNamePlaceholder = "";

                if (this.independentStatus == true) {
                    // May need to work on this 
                    this.tempBottler = bottlerNamePlaceholder;
                    bottlerNamePlaceholder=this.tempBottler;

                } else {
                    // bottlerNamePlaceholder=this.tempBottler;
                    this.tempBottler = 'OB'
                    
                }
            },

            

            // for search button
            searchListings() {

                // flag to check if there are search inputs
                this.search = true;

                const searchInput = this.searchInput.toLowerCase();
                this.searchTerm = this.searchInput;

                // if there is something searched
                const searchResults = this.listings.filter((listing) => {
                    const expressionName = listing["Expression Name"].toLowerCase();
                    const producer = listing["Producer"].toLowerCase();
                    return expressionName.includes(searchInput) || producer.includes(searchInput);
                });

                // if nothing found
                if (searchResults.length == 0) {
                    this.errorFound = true;
                    this.errorMessage = 'No results found, please try again.';
                } 
                else {
                    this.errorFound = false;
                    this.errorMessage = '';
                    this.filteredListings = searchResults;
                }

                // if there is nothing searched
                if (this.searchInput == '') {
                    this.resetListings();
                }
            },

            // for resetting listings (show full listings)
            resetListings() {
                this.filteredListings = this.listings;
                this.search = false;
                this.searchInput = '';
            },

            // get reviews for a listing
            getReviews(listing) {
                // list of all reviews of the particular drink
                const reviews = this.reviews.filter((review) => {
                    return review["reviewTarget"] == listing["listingName"];
                });
                // choose random review from the list
                const randomReview = reviews[Math.floor(Math.random() * reviews.length)];
                // check if a review is found before accessing "Review Desc"
                const reviewDesc = randomReview ? randomReview["reviewDesc"] : null;
                return reviewDesc;
            },

            // get ratings for a listing
            getRatings(listing) {
                const ratings = this.reviews.filter((rating) => {
                    return rating["reviewTarget"] == listing["listingName"];
                });
                // if there are no ratings
                if (ratings.length == 0) {
                    return "-";
                }
                // else there are ratings
                const averageRating = ratings.reduce((total, rating) => {
                    return total + rating["rating"];
                }, 0) / ratings.length;
                // Format the averageRating to 1 decimal place
                const formattedRating = parseFloat(averageRating.toFixed(1));
                return formattedRating;
            }
        },
    };
</script>


