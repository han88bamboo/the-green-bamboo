<!-- NOT ACTIVELY USED (CHECK BEFORE DELETION) -->

<script>
export default {
    name: "FetchData",
    data() {
        return {
            // data from database
            countries: [],
            listings: [],
            producers: [],
            reviews: [],
            users: [],
            venues: [],
            drinkCategories: [],
            tags: ["For My Worst Enemy!", "Good for Gifts", "Beginner Friendly", "Is This Water?", "Overhyped!", "Broke the Bank", "Holy Grails"], // Tags to filter listings
            selectedTag: null, // Current selected tag for filtering
            filteredListings: [], // Listings filtered by tag
        };
    },
    methods: {
        // load data from database
        async loadData() {
            // Countries
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getCountries`);
                this.countries = response.data;
            } catch (error) {
                console.error(error);
            }
            // Listings
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListings`);
                this.listings = response.data;
                // originally, make filteredListings the entire collection of listings
                this.filteredListings = this.listings;
            } catch (error) {
                console.error(error);
            }
            // Producers
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducers`);
                this.producers = response.data;
            } catch (error) {
                console.error(error);
            }
            // Reviews
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getReviews`);
                this.reviews = response.data;
            } catch (error) {
                console.error(error);
            }
            // Users
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUsers`);
                this.users = response.data;
            } catch (error) {
                console.error(error);
            }
            // Venues
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenues`);
                this.venues = response.data;
            } catch (error) {
                console.error(error);
            }
            // Drink Categories
            // try {
            //     const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getDrinkCategories`); // Outdated? Please check.
            //     this.drinkCategories = response.data;
            // } catch (error) {
            //     console.error(error);
            // }
            // Observation Tags
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getObservationTags`);
                this.drinkCategories = response.data;
            } catch (error) {
                console.error(error);
            }
        },

        filterByTag(tag) {
            this.selectedTag = tag;

            // Ensure listings is defined and is an array before filtering
            if (Array.isArray(this.listings)) {
                if (tag) {
                    this.filteredListings = this.listings.filter((listing) =>
                        listing.tags && listing.tags.includes(tag)
                    );
                } else {
                    this.filteredListings = this.listings; // Show all listings if no tag is selected
                }
            } else {
                console.error('Listings is not available or not an array');
                this.filteredListings = []; // Ensure filteredListings is an empty array in this case
            }
        },
    },
    computed: {
        hasFilteredListings() {
            return this.filteredListings.length > 0;
        },
    },
    created() {
        this.loadData();
    },
};
</script>