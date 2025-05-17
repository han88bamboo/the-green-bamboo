<template>
    <NavBar />

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
    <div>

        <!-- Header and selection -->
        <div class="text-center gap-3">
            <h1>Best Of</h1>
            <h2>A round of community favourites, as voted by you!</h2>

            <!-- Button to cast vote -->
            <button
                class="btn primary-btn btn-sm primary-btn-less-round-blue" 
                @click="$router.push('/vote')"
            >
                <span class="fs-5 fst-italic"> Cast your vote! </span>
            </button>

            <!-- Select form control to choose drink type and category -->
            <div class="rounded-3 primary-btn-green">

                <!-- Drink Type -->
                <span>
                    Drink Type:
                </span>
                <select class="form-select" aria-label="Default select example" v-model="selectedDrinkType">
                    <option v-for="type in drinkTypes" :key="type.id" :value="type.drinkType">
                        {{ type.drinkType }}
                    </option>
                </select>

                <!-- Drink Type Category -->
                <div v-if="selectedDrinkType && selectedDrinkType != 'Show All Types'">
                    <span>
                        Drink Type Category:
                    </span>
                    <select class="form-select" aria-label="Default select example" v-model="selectedDrinkTypeCategory">
                        <option v-for="category in selectedDrinkTypeCategory" :key="category" :value="category">
                            {{ category.drinkTypeCategory }}
                        </option>
                    </select>
                </div>
            </div>
        </div>
        
        <!-- Grails -->
        <div>

        </div>

        <!-- Up and coming -->
        <div>

        </div>


        <!-- Goats -->
        <div>
            
        </div>
    </div>

    <FooterBar />

</template>

<script>
import NavBar from "@/components/NavBar.vue";
import FooterBar from "@/components/FooterBar.vue";

export default {
    name: "BestOfView",
    components: {
        NavBar,
        FooterBar
    }, 
    data() {
        return {
            dataLoaded: false,

            // Drink type array 
            drinkTypes: [
                {
                    drinkType: "Show All Types",
                }
            ],

            // Variable to store the selected drink type
            selectedDrinkType: null,

            // Variable to store the selected drink type category
            selectedDrinkTypeCategory: null,

            // Top 5 listings array
            top5Listings: [],
        };
    }, 
    computed: {
        // Set the type category based on the selected drink type
        selectedDrinkTypeCategory() {
            return this.drinkTypes.find(
                (type) => type.drinkType === this.selectedDrinkType
            )?.typeCategory;
        },
    },
    watch: {
        // Watch for changes in the selected drink type category and fetch the top 5 listings
        watch: {
            selectedDrinkTypeCategory(newVal, oldVal) {
                if (newVal !== oldVal && newVal !== null && newVal !== undefined) {
                this.fetchTop5();
                }
            }
        }
    },
    methods: {
        async fetchDrinkTypes() {
            try {
                const response = await this.axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getDrinkTypes`
                );

                // Append the response data to the drinkTypes array
                this.drinkTypes = this.drinkTypes.concat(response.data);

            } catch (error) {
                this.dataLoaded = null;
                console.error("Error fetching drink types:", error);
            }
        },

        async fetchTop5() {
            try {
                const response = await this.axios.get(
                    `${process.env.VUE_APP_API_URL}/editDashboard/getTop5/${this.selectedDrinkType}`
                );

                this.top5Listings = response.data;
                this.dataLoaded = true;

            } catch (error) {
                console.error("Error fetching listings:", error);
                this.dataLoaded = null;
            }
        },
    },
    mounted() {
        this.fetchDrinkTypes();
    },
}
</script>