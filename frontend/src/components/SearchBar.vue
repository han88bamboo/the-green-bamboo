<template>
    <div>
        <!-- Row 1: Search bar + Scan Bottle (side by side on desktop, search bar only on mobile) -->
        <div class="row">
            <!-- Search bar - full width on mobile, partial width on desktop -->
            <div
                class="col-12 col-md-12 pt-2 d-flex align-items-center justify-content-center"
            >
                <div
                    class="col-8 position-relative search-bar d-flex w-100"
                    style="height: 50px"
                >
                    <div class="w-100 position-relative">
                        <input
                            class="form-control fst-italic "
                            type="text"
                            style="border: none; height: 100%; line-height: 50px; padding: 0 1rem;"
                            placeholder="Search drinks & more!"
                            v-model="searchInput"
                            v-on:input="fetchSuggestion"
                            autocomplete="off"
                        />
                        <div
                            class="autocomplete-container position-absolute w-100"
                            v-if="
                                showSuggestions &&
                                suggestions.length > 0
                            "
                        >
                            <ul class="list-group">
                                <li
                                    class="list-group-item list-group-item-action text-start"
                                    v-for="(
                                        suggestion, index
                                    ) in suggestions"
                                    :key="index"
                                    v-on:click="selectSuggestion(suggestion)"
                                >
                                    {{ suggestion }}
                                </li>
                            </ul>
                        </div>

                        <div class="autocomplete-container position-absolute w-100"
                            v-if="showNoResultsMsg">
                            <ul class="list-group">
                                <li class="list-group-item list-group-item-action text-start">
                                     
                                </li>
                            </ul>
                        </div>
                    </div>
                    <img
                        src="../../Images/Others/search-green.png"
                        style="
                            width: 25px;
                            height: 25px;
                            margin: 0px 10px;
                            align-self: center;
                        "
                        v-on:click="goSearch"
                    />
                </div>
            </div>

            <!-- Scan bottle - beside search on desktop, moves to second row on mobile 
            <div
                class="col-6 col-md-4 d-none d-md-block d-flex justify-content-center"
            >
                <button
                    class="btn d-flex align-items-center fw-bold"
                    style="background-color: #027562; color: white; height: 50px; padding: 0px 15px"
                    v-on:click="imageSearch"
                >
                    <span>Scan bottle</span>
                    <img
                        src="../../Images/Others/camera-white.png"
                        style="width: 30px; height: 30px; margin-left: 10px"
                    />
                </button>
            </div>-->
        </div>

        <!-- Row 2: Surprise Me on desktop, Scan bottle + Surprise Me on mobile -->
        <div class="row mt-3">
            
            <!--<div class="col-6 mobile-view-hide d-flex justify-content-center">
                <button
                    class="btn d-flex align-items-center fw-bold"
                    style="background-color: #027562; color: white"
                    v-on:click="imageSearch"
                >
                    <span>Scan bottle</span>
                    <img
                        src="../../Images/Others/camera-white.png"
                        style="width: 20px; height: 20px; margin-left: 10px"
                        class="fw-bold"
                    />
                </button>
            </div>-->

            <!--Surprise Me button - full row on desktop, half width on mobile -->
            <div class="col-12 align-items-center justify-content-center " v-if="showSurpriseButton">
                <router-link :to="'/explore'">
                    <button
                        class="btn btn-md text-white fw-bold"
                        style="background-color: #83a9e8"
                        aria-label="Surprise Me!"
                    >
                        Surprise Me!
                    </button>
                </router-link>
            </div>
        </div> 
    </div>
</template>
<script>

export default {
    name: "SearchBar",
    props: {
        // You can define any props if needed
        showSurpriseButton: {
            type: Boolean,
            default: true, // Default to true if not provided
        },
    },
    data() {
        return {
            searchInput: "",
            suggestions: [],
            showSuggestions: false,
            isFetching: false,
            showNoResultsMsg: false, // Flag to show no results message
        };
    },
    // computed: {
    //     filteredSuggestions() {
    //         if (this.searchInput.trim() === "") return [];

    //         const searchTerm = this.searchInput.toLowerCase();

    //         // First prioritize items that start with the search term
    //         const startsWithMatches = this.suggestions.filter((item) =>
    //             item.toLowerCase().startsWith(searchTerm)
    //         );

    //         // Then add items where any word starts with the search term
    //         const wordStartsWithMatches = this.suggestions.filter((item) => {
    //             const words = item.toLowerCase().split(" ");
    //             return (
    //                 words.some((word) => word.startsWith(searchTerm)) &&
    //                 !item.toLowerCase().startsWith(searchTerm)
    //             ); // exclude already matched items
    //         });

    //         // Finally add substring matches not covered by above rules
    //         const substringMatches = this.suggestions.filter(
    //             (item) =>
    //                 item.toLowerCase().includes(searchTerm) &&
    //                 !item.toLowerCase().startsWith(searchTerm) &&
    //                 !item
    //                     .toLowerCase()
    //                     .split(" ")
    //                     .some((word) => word.startsWith(searchTerm))
    //         );

    //         // Combine all matches with priority order and limit to 7
    //         return [
    //             ...startsWithMatches,
    //             ...wordStartsWithMatches,
    //             ...substringMatches,
    //         ].slice(0, 7);
    //     },
    // },
    mounted() {
        // Close suggestions when clicking outside
        document.addEventListener("click", this.handleClickOutside);
        // Add keyboard navigation
        document.addEventListener("keydown", this.handleKeyDown);
    },
    beforeUnmount() {
        document.removeEventListener("click", this.handleClickOutside);
        document.removeEventListener("keydown", this.handleKeyDown);
    },
    methods: {
        // Fetch all listings from backend
        async fetchSuggestion() {
            try {

                if (this.searchInput.trim() === "") {
                    this.suggestions = [];
                    this.showSuggestions = false;
                    return;
                }

                this.isFetching = true;
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getListingsNames/${this.searchInput}`
                );
                this.suggestions = response.data;
                this.showSuggestions = true;
                this.showNoResultsMsg = false; // Hide no results message if suggestions are found
            } catch (error) {
                console.error("Error fetching listings:", error);
                if (error.response && error.response.status === 404) {
                    this.showNoResultsMsg = true; // Show no results message
                } 
                this.suggestions = [];
            } finally {
                this.isFetching = false;
            }
        },
        // Select a suggestion
        selectSuggestion(suggestion) {
            this.searchInput = suggestion;
            this.showSuggestions = false;
            this.goSearch();
        },

        // Close suggestions when clicking outside
        handleClickOutside(e) {
            if (!this.$el.contains(e.target)) {
                this.showSuggestions = false;
            }
        },
        // For search feature
        goSearch() {
            if (this.searchInput != "") {
                // Remove any '/' from search input
                this.searchInput = this.searchInput.replace(/\//g, "");

                // If already on search page, refresh the page with new search input
                if (this.$route.path.split("/")[1] == "search") {
                    window.location.href = "/search/" + this.searchInput;
                } else {
                    // Re-route to search page
                    this.$router.push({ path: "/search/" + this.searchInput });
                }
                this.showSuggestions = false;
            }
        },
        // Route to image search page
        imageSearch() {
            // If already on image search page, refresh the page
            if (this.$route.path.split("/")[1] == "imageSearch") {
                window.location.href = "/imageSearch";
            } else {
                // Re-route to image search page
                this.$router.push({ path: "/imageSearch" });
            }
        },
    },
};
</script>

<style scoped>
.autocomplete-container {
    max-height: 300px;
    overflow-y: auto;
    z-index: 1000;
    top: 100%;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.list-group-item:hover {
    background-color: #f8f9fa;
    cursor: pointer;
}
.list-group-item.active {
    background-color: #83a9e8; /* standardised the colour */
    border-color: #dee2e6;
    color: white; /* standardised the colour */
}
input.form-control {
    border: none; /* Match the outer border color */
    box-shadow: none !important; /* Remove the inner shadow */
    outline: none; /* Remove the focus outline */
}
</style>
