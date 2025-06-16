<!-- HTML -->
<template>
    <NavBar />

    <!-- main content -->

    <div class="container pt-5">
        <div class="row">

            <!-- spacer -->
            <div class="col-xl-3 col-lg-2 col-md-1"></div>
            
            <!-- main form area -->
            <div class="col-xl-6 col-lg-8 col-md-10">

                <!-- form title -->
                <div class="d-grid gap-2">
                    <p class="fw-bold fs-1"> Add Listing To Menu </p>
                </div>

                <!-- form content -->
                <form>
                    <!-- [input] bottle name -->
                    <div class="form-group mb-3">
                        <p class="text-start mb-1"> Name of Bottle <span class="text-danger">*</span></p>
                        <input list="bottle-listings" v-model="bottleName" class="form-control" id="bottleName" placeholder="Enter bottle name" v-on:change="updateBottleName">
                        <datalist id="bottle-listings">
                            <option v-for="listing in listings" :key="listing.id" :value="listing.listingName">
                                {{listing.listingName}}
                            </option>
                        </datalist>
                        <p v-show="bottleName.length > 0" class="text-start mb-1 text-danger" id="bottleNameError"></p>
                    </div>

                    <!-- [input] item price -->
                    <div class="form-group mb-3">
                        <p class="text-start mb-1"> Item Price <span class="text-danger">*</span></p>
                        <input type="number" v-model="itemPrice" class="form-control" id="itemPrice" placeholder="Enter item price" v-on:change="updateItemPrice">
                        <p v-show="itemPrice.length > 0" class="text-start mb-1 text-danger" id="itemPriceError"></p>
                    </div>

                    <!-- [input] serving type -->
                    <div class="form-group mb-3">
                        <p class="text-start mb-1"> Serving Type <span class="text-danger">*</span></p>
                        <select class="form-select" aria-label="menu sections" v-model="selectedServingType" v-on:change="updateServingType">
                            <option disabled value=""> Select a serving type </option>
                            <option v-for="servingType in servingTypes" v-bind:key="servingType" v-bind:value="servingType"> 
                                {{ servingType.servingType }} 
                            </option>
                        </select>
                        <p v-show="selectedServingType.length > 0" class="text-start mb-1 text-danger" id="servingTypeError"></p>
                    </div>


                    <!-- [input] menu section to add to -->
                    <div class="form-group mb-3">
                        <p class="text-start mb-1"> Menu Section <span class="text-danger">*</span></p>
                        <select class="form-select" aria-label="menu sections" v-model="selectedMenuSection" v-on:change="updateMenuSection">
                            <option disabled value=""> Select a menu section </option>
                            <option v-for="section in filteredMenuSections" v-bind:key="section" v-bind:value="section"> 
                                {{ section }} 
                            </option>
                        </select>
                        <p v-show="selectedMenuSection.length > 0" class="text-start mb-1 text-danger" id="menuSectionError"></p>
                    </div>

                    <!-- show preview of bottle listing -->
                    <div v-if="bottleNameOK" class="card my-5">
                        <div class="card-header mb-0">
                            <h5 class="fw-bold"> Preview of Bottle Listing To Be Added To Menu </h5>
                        </div>
                        <div class="card-body m-2 p-3">
                            <div class="row card-text text-start"> 

                                <!-- image -->
                                <div class="col-4 image-container">
                                    <img v-bind:src="'data:image/png;base64,' + (selectedListing['photo'] || defaultListingPhoto)" style="width: 220px; height: 220px;" class="img-border">
                                    <!-- <img v-bind:src="(selectedListing['photo'] || defaultListingPhoto)" style="width: 220px; height: 220px;" class="img-border"> -->
                                </div>
                                <!-- details -->
                                <div class="col-8 ps-5">
                                    <!-- expression name -->
                                    <div class="row pt-1">
                                        <router-link :to="{ path: '/listing/view/' + selectedListing.id }" class="primary-clickable-text">
                                            <h4> <b> {{ selectedListing["listingName"] }} </b> </h4>
                                        </router-link>
                                    </div>
                                    <!-- producer -->
                                    <div class="row">
                                        <router-link :to="{ path: '/Producers/Profile-Page/' + selectedListing.producerID }" class="primary-clickable-text">
                                            <h5> <b> {{ getProducerName(selectedListing) }} </b> </h5>
                                        </router-link>
                                    </div>
                                    <!-- review -->
                                    <div class="row pt-3">
                                        <router-link :to="{ path: '/listing/view/' + selectedListing.id }" class="default-clickable-text scrollable fst-italic">
                                            <h5> {{ selectedListing["officialDesc"] }}. </h5>
                                        </router-link>
                                    </div>
                                </div>
                                
                            </div>
                        </div>
                    </div>

                    <!-- [button] allow submit -->
                    <div>
                        <button type="submit" class="btn tertiary-btn rounded reverse-clickable-text" v-bind:disabled="!bottleNameOK || !itemPriceOK || !menuSectionOK" v-on:click="addListingToMenu()"> 
                            Add Listing to Menu 
                        </button>
                    </div>
                </form>

            </div>
        </div>
    </div>


</template>

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>
// import { all } from 'axios';
    import NavBar from '@/components/NavBar.vue';


    export default {
        components: {
            NavBar
        },
        data() {
            return {
                // data from database
                listings: [],
                venues: [],
                servingTypes: [],

                // define user type here (defined on mounted() function)
                userID: "",
                userType: "",
                correctVenue: false,
                specified_venue: {},

                // v-model form data
                itemPrice: "",
                bottleName: "",
                menuSection: "",

                // selected form data
                selectedBottle: "",
                selectedMenuSection: "",
                selectedServingType: "",

                // filtered data
                filteredListings: [],
                selectedListing: {},
                filteredMenuSections: [],

                // menu order
                menuOrder: null,

                // convert inputs
                servingTypeId: "",

                // allow submit form
                bottleNameOK: false,
                itemPriceOK: false,
                menuSectionOK: false,
                servingTypeOK: false,

                // default listing photo
                defaultListingPhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",
            };
        },
        async mounted() {
            let userID = localStorage.getItem('88B_accID')
            if (userID != null) {
                this.userID = userID
            }
            let userType = localStorage.getItem('88B_accType')
            if (userType != null) {
                this.userType = userType
            }

            await this.loadData();
        },
        methods: {
            // load data from database
            async loadData() {
                // Get the query string parameters (listing ID) from the URL
                this.venue_id = this.$route.params.id;
                if (this.userID != this.venue_id && this.userType != 'venue') {
                    // redirect to page
                    this.$router.push('/');
                }
                else {
                    this.correctVenue = true
                }
                // listings
                // _id, listingName, producerID, bottler, originCountry, drinkType, typeCategory, age, abv, reviewLink, officialDesc, sourceLink, photo
                    try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListings`);
                        this.listings = response.data;
                    } 
                    catch (error) {
                        console.error(error);
                    }
                // venues
                // _id, venueName, venueDesc, originCountry, address, openingHours
                    try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenues`);
                        this.venues = response.data;
                        this.specified_venue = this.venues.find(venue => venue["id"] == this.venue_id); // find specified venue
                        this.getMenuSections();
                    } 
                    catch (error) {
                        console.error(error);
                    }
                // producers
                // _id, producerName, producerDesc, originCountry, statusOB, mainDrinks
                try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducers`);
                        this.producers = response.data;
                    } 
                    catch (error) {
                        console.error(error);
                    }
                // serving types
                // _id, servingType
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getServingTypes`);
                    this.servingTypes = response.data;
                }
                catch (error) {
                    console.error(error);
                }
            },

            updateBottleName() {
                // get error message element
                let bottleNameError = document.getElementById("bottleNameError")
                // find listing based on bottle name
                let listing = this.listings.find(listing => listing.listingName === this.bottleName)
                if (listing) {
                    this.selectedListing = listing
                    this.selectedBottle = listing.id
                    this.bottleNameOK = true;
                    bottleNameError.innerHTML = ""
                }
                else {
                    this.selectedListing = null
                    this.selectedBottle = ""
                    this.bottleNameOK = false;
                    bottleNameError.innerHTML = "Please enter a valid bottle listing name"
                }
            },

            updateItemPrice() {
                // get error message element
                let itemPriceError = document.getElementById("itemPriceError")
                if (this.itemPrice < 0) {
                    this.itemPriceOK = false;
                    itemPriceError.innerHTML = "Please enter a price"
                }
                else {
                    this.itemPriceOK = true;
                    itemPriceError.innerHTML = ""
                }
            },

            updateServingType() {
                // get id of servingType 
                this.servingTypeId = this.selectedServingType.id
                // get error message element
                let servingTypeError = document.getElementById("servingTypeError")
                if (this.selectedServingType != "") {
                    this.servingTypeOK = true;
                    servingTypeError.innerHTML = ""
                }
                else {
                    this.servingTypeOK = false;
                    servingTypeError.innerHTML = "Please select a serving type"
                }
            },

            getMenuSections() {
                let allVenueMenus = this.specified_venue.menu
                for (let i = 0; i < allVenueMenus.length; i++) {
                    let menuSection = allVenueMenus[i].sectionName
                    this.filteredMenuSections.push(menuSection)
                }
            },

            updateMenuSection() {
                if (this.selectedMenuSection != "") {
                    // get error message element
                    let menuSectionError = document.getElementById("menuSectionError")

                    // get all menu items in the selected menu section
                    let existingMenuItems = this.specified_venue.menu.find(menuItem => menuItem.sectionName == this.selectedMenuSection).listingsID

                    // get length of menu section & derive order of new item (menu length since order starts from 0)
                    let menuSectionLength = existingMenuItems.length
                    this.menuOrder = menuSectionLength

                    // if there are items in the menu
                    if (existingMenuItems.some(item => item === this.selectedBottle)) {
                        // The selected bottle is already in this menu section
                        this.menuSectionOK = false;
                        menuSectionError.innerHTML = "This bottle is already in this menu section";
                    } 
                    else {
                        // The selected bottle is not in this menu section
                        this.menuSectionOK = true;
                        menuSectionError.innerHTML = "";
                    }
                }
            },

            // get producerName for a listing based on listing
            getProducerName(listing) {
                const producer = this.producers.find((producer) => {
                    return producer["id"] == listing["producerID"];
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

            async addListingToMenu() {
                try {
                    const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/addListingToMenu`, 
                        {
                            venueID: this.userID,
                            menuOrder: this.menuOrder,
                            listingID: this.selectedBottle,
                            itemPrice: this.itemPrice,
                            servingType: this.servingTypeId,
                            sectionName: this.selectedMenuSection
                        },
                        {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    console.log(response.data);
                } 
                catch (error) {
                    console.error(error);
                }

                // force page to reload
                window.location.reload();
            }
        }
    }

</script>