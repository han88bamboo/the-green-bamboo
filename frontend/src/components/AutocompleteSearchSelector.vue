<template>
  <div class="search-selector-container">
    <!-- Search Input -->
    <div class="position-relative">
      <div class="input-group">
        <!-- Drinks Icon -->
        <span class="input-group-text bg-white">
          <i class="bi bi-cup-straw text-muted"></i>
        </span>
        <input
          ref="searchInput"
          v-model="searchQuery"
          @focus="showResults = true"
          @blur="handleBlur"
          @keydown="handleKeydown"
          class="form-control"
          type="text"
          :placeholder="placeholder"
          :disabled="disabled"
          autocomplete="off"
          autocorrect="off"
          autocapitalize="off"
          spellcheck="false"
        />
      </div>
    </div>

    <!-- Results Dropdown -->
    <div 
      v-if="showResults && searchQuery.length >= 2" 
      class="dropdown-menu d-block position-absolute w-100 mt-1 shadow-lg border-0 results-dropdown"
      @mouseenter="isMousedOverResults = true"
      @mouseleave="isMousedOverResults = false"
    >
      <!-- Loading State -->
      <div v-if="isLoading" class="d-flex align-items-center justify-content-center p-4">
        <div class="spinner-border spinner-border-sm text-primary me-2" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <span class="text-muted">Searching drinks...</span>
      </div>

      <!-- Results Content -->
      <div v-else-if="results.length > 0" class="results-list" style="max-height: 300px; overflow-y: auto;">
        <div
          v-for="(item, index) in results"
          :key="`listing-${item.id}`"
          :class="[
            'dropdown-item search-item py-2 px-3',
            { 'active': selectedIndex === index }
          ]"
          @mousedown="selectItem(item, $event)"
          @mouseenter="selectedIndex = index"
          role="button"
        >
          <div class="d-flex align-items-center w-100">
            <div style="width: 32px; height: 32px; flex-shrink: 0; margin-right: 12px;">
              <img 
                :src="item.photo || defaultDrinkPhoto" 
                :alt="item.listingName"
                class="rounded"
                style="width: 100%; height: 100%; object-fit: cover;"
              />
            </div>
            <div class="d-flex flex-column" style="flex: 1; min-width: 0;">
              <span class="fw-medium text-dark item-name text-truncate">{{ item.listingName }}</span>
              <small class="text-muted producer-name text-truncate">
                <template v-if="item.producerName">{{ item.producerName }}</template>
                <template v-if="item.producerName && item.drinkType"> · </template>
                <template v-if="item.drinkType && item.drinkType !== 'Other'">{{ item.drinkType }}</template>
                <template v-if="item.abv"> · {{ item.abv }}%</template>
              </small>
            </div>
            <small v-if="item.originCountry" class="text-muted item-detail" style="margin-left: 12px; flex-shrink: 0;">{{ item.originCountry }}</small>
          </div>
        </div>
      </div>

      <!-- No Results -->
      <div v-else-if="!isLoading && searchQuery.length >= 2" class="text-center p-4">
        <div class="mb-2">
          <i class="bi bi-cup-straw text-muted" style="font-size: 2rem;"></i>
        </div>
        <div class="fw-medium text-muted">No drinks found</div>
        <small class="text-muted">Try different keywords</small>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  name: 'AutocompleteSearchSelector',
  props: {
    placeholder: {
      type: String,
      default: 'Search for drinks to link...'
    },
    disabled: {
      type: Boolean,
      default: false
    },
    maxResults: {
      type: Number,
      default: 8
    }
  },
  emits: ['select'],
  setup(props, { emit }) {
    const defaultDrinkPhoto = "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
    
    const searchInput = ref(null)
    const searchQuery = ref('')
    const showResults = ref(false)
    const isLoading = ref(false)
    const selectedIndex = ref(-1)
    const debounceTimer = ref(null)
    const abortController = ref(null)
    const isMousedOverResults = ref(false)
    const results = ref([])

    // API call for drinks only
    const getBottleListings = async (query, signal) => {
      const api_endpoint = `${process.env.VUE_APP_API_URL}/getData/bottle-listings?q=${encodeURIComponent(query)}&limit=${props.maxResults}`
      const response = await fetch(api_endpoint, { signal })

      if (response.status === 404) {
        return []
      }      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      return response.json()
    }

    const performSearch = async (query) => {
      if (query.length < 2) {
        results.value = []
        isLoading.value = false
        return
      }

      // Cancel previous request
      if (abortController.value) {
        abortController.value.abort()
      }

      abortController.value = new AbortController()
      const signal = abortController.value.signal

      isLoading.value = true
      selectedIndex.value = -1

      try {
        const listingsData = await getBottleListings(query, signal)
        results.value = listingsData || []
      } catch (error) {
        if (error.name !== 'AbortError') {
          results.value = []
        }
      } finally {
        isLoading.value = false
      }
    }

    // Debounced search
    const debouncedSearch = (query) => {
      if (debounceTimer.value) {
        clearTimeout(debounceTimer.value)
      }
      
      if (query.length >= 2) {
        debounceTimer.value = setTimeout(() => {
          performSearch(query)
        }, 400)
      } else {
        performSearch(query)
      }
    }

    // Watch for search query changes
    watch(searchQuery, (newQuery) => {
      const trimmedQuery = newQuery.trim()
      
      if (trimmedQuery.length >= 2) {
        debouncedSearch(trimmedQuery)
      } else {
        results.value = []
        isLoading.value = false
        
        if (abortController.value) {
          abortController.value.abort()
        }
        
        if (debounceTimer.value) {
          clearTimeout(debounceTimer.value)
        }
      }
    })

    // Keyboard navigation
    const handleKeydown = (event) => {
      if (!showResults.value || results.value.length === 0) {
        return
      }

      switch (event.key) {
        case 'ArrowDown':
          event.preventDefault()
          selectedIndex.value = selectedIndex.value < results.value.length - 1 
            ? selectedIndex.value + 1 
            : 0
          break
        case 'ArrowUp':
          event.preventDefault()
          selectedIndex.value = selectedIndex.value > 0 
            ? selectedIndex.value - 1 
            : results.value.length - 1
          break
        case 'Enter':
          event.preventDefault()
          if (selectedIndex.value >= 0 && selectedIndex.value < results.value.length) {
            selectItem(results.value[selectedIndex.value])
          }
          break
        case 'Escape':
          event.preventDefault()
          showResults.value = false
          searchInput.value.blur()
          break
      }
    }

    // Handle input blur
    const handleBlur = () => {
      if (!isMousedOverResults.value) {
        showResults.value = false
      }
    }

    // Handle item selection - emit to parent
    const selectItem = (item, event) => {
      if (event) {
        event.preventDefault()
      }
      
      // Emit the selected drink to parent component
      emit('select', item)
      
      // Clear search and close dropdown
      searchQuery.value = ''
      results.value = []
      showResults.value = false
      isMousedOverResults.value = false
      
      if (searchInput.value) {
        searchInput.value.blur()
      }
    }

    // Method to clear and focus
    const focus = () => {
      if (searchInput.value) {
        searchInput.value.focus()
      }
    }

    const clear = () => {
      searchQuery.value = ''
      results.value = []
    }
    
    return {
      searchInput,
      searchQuery,
      showResults,
      isLoading,
      selectedIndex,
      results,
      isMousedOverResults,
      defaultDrinkPhoto,
      handleKeydown,
      handleBlur,
      selectItem,
      focus,
      clear
    }
  }
}
</script>
<style scoped>
.search-selector-container {
  position: relative;
  width: 100%;
}

.results-dropdown {
  border-radius: 8px;
  padding: 0.25rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1050;
}

.results-list {
  scrollbar-width: thin;
  scrollbar-color: #dee2e6 transparent;
}

.results-list::-webkit-scrollbar {
  width: 6px;
}

.results-list::-webkit-scrollbar-track {
  background: transparent;
}

.results-list::-webkit-scrollbar-thumb {
  background-color: #dee2e6;
  border-radius: 3px;
}

.search-item {
  transition: all 0.15s ease;
  border: none;
  background: white;
  min-height: 44px;
  display: flex;
  align-items: center;
  cursor: pointer;
  margin: 0;
  border-radius: 6px;
}

.search-item:hover {
  background-color: #f8f9fa;
}

.search-item.active {
  background-color: #027562;
  color: white;
}

.search-item.active .text-muted,
.search-item.active .producer-name,
.search-item.active .item-detail {
  color: rgba(255, 255, 255, 0.8) !important;
}

.search-item.active .item-name {
  color: white !important;
}

.item-name {
  font-size: 0.9rem;
  font-weight: 500;
  color: #212529;
  line-height: 1.2;
  display: block;
  margin: 0;
  padding: 0;
}

.producer-name {
  font-size: 0.75rem;
  color: #6c757d;
  line-height: 1.2;
  margin-top: 2px;
  display: block;
  margin-left: 0;
  padding: 0;
}

.item-detail {
  font-size: 0.75rem;
  color: #6c757d;
  font-weight: 400;
  white-space: nowrap;
}

.input-group-text {
  border-color: #dee2e6;
  background-color: white;
}

.form-control {
  border-color: #dee2e6;
}

.form-control:focus {
  border-color: #027562;
  box-shadow: 0 0 0 0.2rem rgba(2, 117, 98, 0.15);
}

.form-control::placeholder {
  color: #adb5bd;
  font-weight: 400;
}

.form-control:disabled {
  background-color: #f8f9fa;
}

/* Mobile responsiveness */
@media (max-width: 576px) {
  .results-dropdown {
    max-height: 250px !important;
  }
  
  .search-item {
    padding: 0.5rem 0.75rem !important;
  }
  
  .item-name {
    font-size: 0.85rem;
  }
}
</style>