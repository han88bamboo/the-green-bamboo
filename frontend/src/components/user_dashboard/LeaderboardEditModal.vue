<!-- src/components/dashboard/LeaderboardEditModal.vue -->
<template>
    <div class="popup-overlay" @click.self="$emit('close')">
        <div class="popup-content">
            <button class="close-btn" @click="$emit('close')">×</button>

            <h5 class="fw-bold mb-1">Select Your {{ renamedCategory }} {{ categoryEmoji }}</h5>
            <p class="text-muted mb-4 subtitle">{{ categorySubtitle }}</p>

            <!-- Search Bar -->
            <div class="search-container mb-4">
                <div class="position-relative">
                    <input 
                        class="form-control search-input" 
                        type="text" 
                        placeholder="Search for a drink"
                        v-model="searchInput" 
                        @input="fetchSuggestions" 
                        @keydown="handleKeyDown"
                        autocomplete="off" 
                        ref="searchInput"
                    />
                    <span class="search-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-search" viewBox="0 0 16 16">
                            <path
                                d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                        </svg>
                    </span>

                    <!-- Autocomplete Suggestions -->
                    <div v-if="showSuggestions && suggestions.length > 0"
                        class="autocomplete-container position-absolute w-100">
                        <ul class="list-group">
                            <li v-for="(suggestion, index) in suggestions" 
                                :key="index"
                                class="list-group-item list-group-item-action text-start"
                                :class="{ 'highlighted': index === highlightedIndex }"
                                @click="selectSuggestion(suggestion)"
                                @mouseenter="highlightedIndex = index">
                                {{ suggestion.listingName }}
                            </li>
                        </ul>
                    </div>
                    <div v-if="showNoResultsMsg" class="autocomplete-container position-absolute w-100">
                        <ul class="list-group">
                            <li class="list-group-item list-group-item-action text-start">
                                No results found. Try a different search.
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Selected Drinks -->
            <div v-if="selectedDrinks.length > 0" class="selected-drinks-container">
                <div v-for="(drink, index) in selectedDrinks" :key="drink.id" class="selected-drink">
                    
                    <!-- Drink Row with Remove Button -->
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <div class="d-flex align-items-center flex-grow-1">
                            <div class="wine-image me-3">
                                <img :src="drink.image || drink.photo || defaultDrinkImage" alt="Drink bottle"
                                    style="height: 60px; width: 40px; object-fit: contain;" />
                            </div>
                            <div class="wine-details text-start">
                                <div class="wine-name">{{ drink.listingName || drink.name }}</div>
                                <div class="wine-producer text-muted">
                                    {{ drink.bottler || "Unknown Producer" }}
                                    {{ drink.originCountry ? "• " + drink.originCountry : "" }}
                                </div>
                            </div>
                        </div>
                        
                        <!-- Remove Button on the Right -->
                        <div class="ms-3">
                            <span class="remove-drink-btn" @click="removeDrink(index)" style="cursor: pointer;">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="red"
                                    class="bi bi-x-circle" viewBox="0 0 16 16">
                                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" />
                                    <path
                                        d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z" />
                                </svg>
                            </span>
                        </div>
                    </div>
                    
                    <!-- Divider (shown for all items except the last one) -->
                    <hr v-if="index < selectedDrinks.length - 1" class="my-0" style="border-color: #dee2e6;">
                </div>
            </div>

            <!-- Confirm Button :disabled="selectedDrinks.length === 0" -->
            <button @click="handleConfirm" class="confirm-btn">
                Confirm Selection
            </button>
        </div>
    </div>
</template>

<script>
import { useToast } from "vue-toastification";

// user add listing upper limit 
const CATEGORY_LIMITS = {
    'Grail': 1,
    'Up & Coming': 3, 
    'GOATs': 3,
}

export default {
    name: 'LeaderboardEditModal',
    props: {
        category: { type: String, required: true },
        initialSelection: { type: Array, default: () => [] } // To pre-populate if editing
    },
    emits: ['close', 'confirm'],
    data() {
        return {
            searchInput: '',
            suggestions: [],
            showSuggestions: false,
            showNoResultsMsg: false,
            selectedDrinks: [], // This will hold the full drink objects
            defaultDrinkImage: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739',
            debounceTimer: null,
            highlightedIndex: -1, // Track which suggestion is highlighted
        };
    },
    computed: {
        renamedCategory() {
            if (this.category === 'Grail') return 'Desperate To Try';
            if (this.category === 'GOATs') return 'Essentials';
            return this.category;
        },
        categoryEmoji() {
            const emojis = { 'Grail': '👑', 'Up & Coming': '🍷', 'GOATs': '🙌' };
            return emojis[this.category] || '';
        },
        categorySubtitle() {
            const subtitles = {
                'Grail': 'We’re talking bucket list!',
                'Up & Coming': 'Give those underrated folks a shout!',
                'GOATs': 'What’s on pour for you right now'
            };
            return subtitles[this.category] || '';
        }
    },
    methods: {
        handleKeyDown(event) {
            if (!this.showSuggestions || this.suggestions.length === 0) {
                return;
            }

            switch (event.key) {
                case 'ArrowDown':
                    event.preventDefault();
                    this.highlightedIndex = Math.min(this.highlightedIndex + 1, this.suggestions.length - 1);
                    this.scrollToHighlighted();
                    break;
                case 'ArrowUp':
                    event.preventDefault();
                    this.highlightedIndex = Math.max(this.highlightedIndex - 1, 0);
                    this.scrollToHighlighted();
                    break;
                case 'Enter':
                    event.preventDefault();
                    if (this.highlightedIndex >= 0 && this.highlightedIndex < this.suggestions.length) {
                        this.selectSuggestion(this.suggestions[this.highlightedIndex]);
                    }
                    break;
                case 'Escape':
                    event.preventDefault();
                    this.showSuggestions = false;
                    this.highlightedIndex = -1;
                    break;
            }
        },
        scrollToHighlighted() {
            // Scroll the highlighted item into view
            this.$nextTick(() => {
                const container = this.$el.querySelector('.autocomplete-container ul');
                const highlightedItem = container?.children[this.highlightedIndex];
                if (highlightedItem) {
                    highlightedItem.scrollIntoView({ block: 'nearest' });
                }
            });
        },
        async addSelectedDrink() {
            const drinkToAdd = this.searchInput.trim();

            if (drinkToAdd) {
                // First, try to find the exact suggestion
                const exactSuggestion = this.suggestions.find(
                    suggestion => suggestion.listingName.toLowerCase() === drinkToAdd.toLowerCase()
                );

                if (exactSuggestion) {
                    // Use the selectSuggestion method to ensure consistent handling
                    await this.selectSuggestion(exactSuggestion);
                } else {
                    // If no exact match, show an error or provide feedback
                    const toast = useToast();
                    toast.error("Please select a valid drink from the suggestions");
                }
            }
        },
        fetchSuggestions() {
            clearTimeout(this.debounceTimer);
            this.showSuggestions = false;
            this.showNoResultsMsg = false;
            this.highlightedIndex = -1; // Reset highlighted index

            if (this.searchInput.length < 2) {
                this.suggestions = [];
                return;
            }

            this.debounceTimer = setTimeout(async () => {
                try {
                    const sanitizedInput = encodeURIComponent(
                        this.searchInput //.trim().replace(/[^a-zA-Z0-9\s\-']+/g, '')
                    );
                    const api_endpoint = `${process.env.VUE_APP_API_URL}/getData/bottle-listings?q=${encodeURIComponent(sanitizedInput)}&limit=${10}`
                    const response = await fetch(api_endpoint)
                    const data = await response.json();
                    this.suggestions = data;

                    if (this.suggestions.length > 0) {
                        this.showSuggestions = true;
                        this.highlightedIndex = 0; // Auto-highlight first item
                    } else {
                        this.showNoResultsMsg = true;
                    }
                } catch (error) {
                    console.error("Error fetching drink suggestions:", error);
                    this.showNoResultsMsg = true;
                }
            }, 300); // 300ms debounce
        },
        selectSuggestion(suggestion) {
            const limit = CATEGORY_LIMITS[this.category];
            if (this.selectedDrinks.length >= limit) {
                const toast = useToast();
                const drinkNoun = limit === 1 ? 'drink' : 'drinks';
                toast.error(`You can only select up to ${limit} ${drinkNoun} for this category.`);
                return; 
            }

            // alert(limit);
            // Avoid adding duplicates
            if (!this.selectedDrinks.some(d => d.id === suggestion.id)) {
                this.selectedDrinks.push(suggestion);
            }
            this.searchInput = '';
            this.suggestions = [];
            this.showSuggestions = false;
            this.highlightedIndex = -1;
            
            // Return focus to the search input
            this.$nextTick(() => {
                this.$refs.searchInput.focus();
            });
        },
        removeDrink(index) {
            this.selectedDrinks.splice(index, 1);
        },
        handleConfirm() {
            // Emit the selected drink IDs or full objects to the parent
            this.$emit('confirm', { category: this.category, drinks: this.selectedDrinks });
        }
    },
    created() {
        // If you pass in an initial selection, populate it
        this.selectedDrinks = [...this.initialSelection];
    }
};
</script>

<style scoped>
.popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1050;
}

.popup-content {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
    position: relative;
    text-align: center;
    max-height: 80vh;
    display: flex;
    flex-direction: column;
}

.close-btn {
    position: absolute;
    top: 10px;
    right: 15px;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
}

.search-container .search-icon {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: #aaa;
}

.autocomplete-container {
    z-index: 1051;
    /* Must be higher than the overlay */
    max-height: 200px;
    overflow-y: auto;
}

.list-group-item.highlighted {
    background-color: #f8f9fa;
    border-color: #007bff;
}

.selected-drinks-container {
    flex-grow: 1;
    overflow-y: auto;
    margin-bottom: 1rem;
}

.confirm-btn {
    background-color: #F4B754;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 25px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s;
}

.confirm-btn:hover {
    background-color: #e0a84a;
}

.confirm-btn:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}
</style>