<template>
    <NavBar />
        <div class="d-flex align-items-center justify-content-center login-header-banner">
            <img src="@/assets/Best-Of.png" alt="Banner" />
            </div>
        <!-- Display when data is still loading -->
        <div
            class="text-info-emphasis fst-italic fw-bold fs-5 pt-5"
            v-if="dataLoaded == false"
        >
            <span>Loading page, please wait...</span>
            <br /><br />
            <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <!-- Display when data fails to load-->
        <div
            class="text-danger fst-italic fw-bold fs-3 pt-5"
            v-if="dataLoaded == null"
        >
            <span>An error occurred while loading this page, please try again!</span>
            <br />
            <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
            <span class="fs-5 fst-italic"> Return to previous page </span>
            </button>
            <button class="btn primary-btn btn-sm mx-1" @click="this.$router.go(0)">
            <span class="fs-5 fst-italic"> Go to Home page </span>
            </button>
        </div>

        <!-- Main Content -->
        <div v-if="dataLoaded" class="container text-start">
            
            <!-- Header and selection -->
        
                <div class="container">
                    <div class="text-center mt-4">
                        <h2 class="fw-bold mobile-fs-4">Best Of</h2>
                        <p class="mobile-rating-smaller-text-2">A round of community favourites, as voted by you!</p>

                        <!-- Button to cast vote -->
                        <button
                            class="btn primary-btn-less-round-blue btn-lg mb-3 mobile-rating-smaller-text-2" 
                            @click="$router.push('/dashboard/user')"
                        >
                            <span class="fw-bold "> Cast your vote! </span>
                        </button>

                            
                        <!-- Select form control to choose drink type and category -->
                        <!-- Drink Type and Category Row -->
                        <div class="row rounded-3 primary-btn-green py-3 justify-content-between" style="width: 90%; margin: auto;">
                            <!-- Drink Type -->
                            <div class="col-md-6 d-flex flex-column mb-2">
                                <div class="d-flex align-items-center gap-2 mobile-rating-smaller-text-2">
                                    <span>Drink Type:</span>
                                    <select class="form-select mobile-rating-smaller-text-2" aria-label="Default select example" style="width: 70%" v-model="selectedDrinkType">
                                        <option v-for="type in drinkTypes" :key="type.id" :value="type.drinkType">
                                            {{ type.drinkType }}
                                        </option>
                                    </select>
                                </div>
                            </div>
                            <!-- Drink Type Category -->
                            <div
                                class="col-md-6 d-flex flex-column"
                            >
                                <div class="d-flex align-items-center gap-2 w-full mobile-rating-smaller-text-2">
                                    <span>Drink Category:</span>
                                    <select class="form-select mobile-rating-smaller-text-2" aria-label="Default select example" v-model="selectedDrinkTypeCategory" :disabled="selectedDrinkType == 'Show All Types'" style="width: 60%">
                                        <option v-for="category in drinkTypeCategories" :key="category" :value="category">
                                            {{ category }}
                                        </option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                   
                </div>
                <div class="container mx-lg-5 sm-mx-0">
                   
                <!-- Grails -> Change to "DEsperate to Try" -->
                    <div class="mb-3 mb-md-5">
                        <h5 class="ms-3 mb-3 fw-bold mt-4 mobile-fs-6">Desperate to Try</h5>
                        <div v-if="top5Listings.grails?.length > 0" class="row gx-3 px-3">
                            <div
                                v-for="listing in top5Listings['grails']"
                                :key="listing.listingID"
                                class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 d-flex justify-content-center"
                            >
                                <BestOfCard :listing="listing" />
                            </div>
                        </div>
                        <div v-else>
                            <p class="ms-3">No grails found for the selected drink type and category.</p>
                        </div>

                    </div>
                
                <!-- Up and coming -> Change to "Up And Coming" -->
                <div class="mb-3 mb-md-5">
                    <h5 class="ms-3 mb-3 fw-bold mobile-fs-6">Up And Coming</h5>
                        <div v-if="top5Listings.upAndComing?.length > 0" class="row gx-3 px-3">
                            <div
                                v-for="listing in top5Listings['upAndComing']"
                                :key="listing.listingID"
                                class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 d-flex justify-content-center"
                            >
                                <BestOfCard :listing="listing" />
                            </div>
                        </div>
                        <div v-else>
                            <p class="ms-3">No Up And Coming listings found for the selected drink type and category.</p>
                        </div>
                </div>

                <!-- Goats -> Change to Ride or Die -->
                <div class="mb-3 mb-md-5">
                    <h5 class="ms-3 mb-3 fw-bold mobile-fs-6">Ride or Die</h5>
                        <div v-if="top5Listings.goats?.length > 0"  class="row gx-3 px-3">
                            <div
                                v-for="listing in top5Listings['goats']"
                                :key="listing.listingID"
                                class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 d-flex justify-content-center"
                            >
                                <BestOfCard :listing="listing" />
                            </div>
                        </div>
                        <div v-else>
                            <p class="ms-3">No Ride or Dies found for the selected drink type and category.</p>
                        </div>
                </div>
                </div>
        </div>
    

    <FooterBar />

</template>

<script>
import NavBar from "@/components/NavBar.vue";
import FooterBar from "@/components/FooterBar.vue";
import BestOfCard from "@/components/BestOfCard.vue";

export default {
    name: "BestOfView",
    components: {
        NavBar,
        FooterBar,
        BestOfCard,
    }, 
    data() {
        return {
            dataLoaded: false,

            // Drink type array 
            drinkTypes: [
                {
                    drinkType: "Show All Types",
                    typeCategory: ['--'],
                }
            ],

            // Drink type category array
            drinkTypeCategories: ['--'],

            // Variable to store the selected drink type
            selectedDrinkType: "Show All Types",

            // Variable to store the selected drink type category
            selectedDrinkTypeCategory: "--",

            // Top 5 listings array
            top5Listings: [],
        };
    }, 
    watch: {
        selectedDrinkType(newVal) {
            // Find the selected drink type object
            const selectedType = this.drinkTypes.find(type => type.drinkType === newVal);

            // Update categories based on the selected drink type
            this.drinkTypeCategories = selectedType ? selectedType.typeCategory : [];

            // Set selectedDrinkTypeCategory to the first category (if available)
            if (this.drinkTypeCategories.length) {
            this.selectedDrinkTypeCategory = this.drinkTypeCategories[0];
            } else {
            this.selectedDrinkTypeCategory = '';
            }
        },
        selectedDrinkTypeCategory(newVal, oldVal) {
            if (newVal !== oldVal && newVal !== null && newVal !== undefined) {
                this.fetchTop5();
            }
        }
    },
    methods: {
        async fetchDrinkTypes() {
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getDrinkTypes`
                );

                // Append the response data to the drinkTypes array
                this.drinkTypes = this.drinkTypes.concat(response.data);
                this.dataLoaded = true;

            } catch (error) {
                this.dataLoaded = null;
                console.error("Error fetching drink types:", error);
            }
        },

        updateDrinkTypeCategory() {
            const categories = this.drinkTypeCategories;
            if (categories.length) {
            this.selectedDrinkTypeCategory = categories[0];
            } else {
            this.selectedDrinkTypeCategory = '';
            }
        },

        async fetchTop5() {
            try {

                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/editDashboard/getTop5?type=${this.selectedDrinkType}&typeCat=${this.selectedDrinkTypeCategory}`
                );

                this.top5Listings = response.data.data;
                this.dataLoaded = true;

            } catch (error) {
                console.error("Error fetching listings:", error);
                this.dataLoaded = null;
            }
        },
    },
    mounted() {
        this.fetchDrinkTypes();
        this.fetchTop5();
    },
}
</script>

<style scoped>
.login-header-banner {
  position: relative;
  width: 100%;
  padding-top: calc(3 / 6 * 100%); /* 2:6 aspect ratio = 33.33% */
  overflow: hidden;
}

.login-header-banner img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}


@media (min-width: 991px) {
  .login-header-banner {
    padding-top: calc(2/ 9 * 100%); /* 2:6 aspect ratio = 33.33% */
  }
}
</style>