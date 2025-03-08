<template>
    <div>
        <!-- Row 1: Search bar + Scan Bottle (side by side on desktop, search bar only on mobile) -->
        <div class="row">
            <!-- Search bar - full width on mobile, partial width on desktop -->
            <div
                class="col-12 col-md-8 d-flex align-items-center justify-content-center"
            >
                <div
                    class="col-8 position-relative search-bar d-flex w-100"
                    style="height: 50px"
                >
                    <div class="w-100 position-relative">
                        <input
                            class="form-control fst-italic"
                            type="text"
                            placeholder="What are you drinking today?"
                            v-model="searchInput"
                            v-on:keyup.enter="goSearch"
                            v-on:input="getSuggestions"
                            autocomplete="off"
                        />
                        <div
                            class="autocomplete-container position-absolute w-100"
                            v-if="
                                showSuggestions &&
                                filteredSuggestions.length > 0
                            "
                        >
                            <ul class="list-group">
                                <li
                                    class="list-group-item list-group-item-action text-start"
                                    v-for="(
                                        suggestion, index
                                    ) in filteredSuggestions"
                                    :key="index"
                                    v-on:click="selectSuggestion(suggestion)"
                                    :class="{ active: selectedIndex === index }"
                                    v-on:mouseover="selectedIndex = index"
                                >
                                    {{ suggestion }}
                                </li>
                            </ul>
                        </div>
                    </div>
                    <img
                        src="../../Images/Others/search-green.png"
                        style="
                            width: 30px;
                            height: 30px;
                            margin: 0px 10px;
                            align-self: center;
                        "
                        v-on:click="goSearch"
                    />
                </div>
            </div>

            <!-- Scan bottle - beside search on desktop, moves to second row on mobile -->
            <div
                class="col-6 col-md-4 d-none d-md-block d-flex justify-content-center"
            >
                <button
                    class="btn primary-btn-less-round-green d-flex align-items-center"
                    style="height: 50px; padding: 0px 15px"
                    v-on:click="imageSearch"
                >
                    <span>Scan bottle</span>
                    <img
                        src="../../Images/Others/camera-white.png"
                        style="width: 30px; height: 30px; margin-left: 10px"
                    />
                </button>
            </div>
        </div>

        <!-- Row 2: Surprise Me on desktop, Scan bottle + Surprise Me on mobile -->
        <div class="row mt-3">
            <!-- Scan bottle button - Only visible on mobile in this row -->
            <div class="col-6 d-md-none d-flex justify-content-center">
                <button
                    class="btn primary-btn-less-round-green d-flex align-items-center"
                    style="height: 50px; padding: 0px 15px"
                    v-on:click="imageSearch"
                >
                    <span>Scan bottle</span>
                    <img
                        src="../../Images/Others/camera-white.png"
                        style="width: 30px; height: 30px; margin-left: 10px"
                    />
                </button>
            </div>

            <!-- Surprise Me button - full row on desktop, half width on mobile -->
            <div class="col-6 col-md-12 d-flex justify-content-center">
                <router-link :to="'/'">
                    <button
                        class="btn btn-lg text-white"
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
import axios from "axios";

export default {
    name: "SearchBar",
    data() {
        return {
            searchInput: "",
            suggestions: [],
            showSuggestions: false,
            selectedIndex: -1,
            isFetching: false,
        };
    },
    computed: {
        filteredSuggestions() {
            if (this.searchInput.trim() === "") return [];

            const searchTerm = this.searchInput.toLowerCase();

            // First prioritize items that start with the search term
            const startsWithMatches = this.suggestions.filter((item) =>
                item.toLowerCase().startsWith(searchTerm)
            );

            // Then add items where any word starts with the search term
            const wordStartsWithMatches = this.suggestions.filter((item) => {
                const words = item.toLowerCase().split(" ");
                return (
                    words.some((word) => word.startsWith(searchTerm)) &&
                    !item.toLowerCase().startsWith(searchTerm)
                ); // exclude already matched items
            });

            // Finally add substring matches not covered by above rules
            const substringMatches = this.suggestions.filter(
                (item) =>
                    item.toLowerCase().includes(searchTerm) &&
                    !item.toLowerCase().startsWith(searchTerm) &&
                    !item
                        .toLowerCase()
                        .split(" ")
                        .some((word) => word.startsWith(searchTerm))
            );

            // Combine all matches with priority order and limit to 7
            return [
                ...startsWithMatches,
                ...wordStartsWithMatches,
                ...substringMatches,
            ].slice(0, 7);
        },
    },
    mounted() {
        this.fetchAllListings();
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
        async fetchAllListings() {
            try {
                this.isFetching = true;
                const response = await axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getListingsName`
                );
                this.suggestions = response.data;
            } catch (error) {
                console.error("Error fetching listings:", error);
                this.suggestions = [];
            } finally {
                this.isFetching = false;
            }
        },
        // Get suggestions based on current input
        getSuggestions() {
            if (this.searchInput.trim().length > 0) {
                this.showSuggestions = true;
            } else {
                this.showSuggestions = false;
            }
        },
        // Select a suggestion
        selectSuggestion(suggestion) {
            this.searchInput = suggestion;
            this.showSuggestions = false;
            this.goSearch();
        },
        // Handle keyboard navigation
        handleKeyDown(e) {
            if (!this.showSuggestions) return;

            const suggestions = this.filteredSuggestions;
            // Down arrow
            if (e.key === "ArrowDown") {
                e.preventDefault();
                this.selectedIndex = Math.min(
                    this.selectedIndex + 1,
                    suggestions.length - 1
                );
            }
            // Up arrow
            else if (e.key === "ArrowUp") {
                e.preventDefault();
                this.selectedIndex = Math.max(this.selectedIndex - 1, 0);
            }
            // Enter key
            else if (e.key === "Enter" && this.selectedIndex >= 0) {
                e.preventDefault();
                this.selectSuggestion(suggestions[this.selectedIndex]);
            }
            // Escape key
            else if (e.key === "Escape") {
                this.showSuggestions = false;
            }
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
