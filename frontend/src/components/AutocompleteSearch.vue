<template>
  <div class="search-container">
    <!-- Search Input -->
    <div class="position-relative">
      <div class="input-group">
        <!-- <span class="input-group-text bg-white border-end-0" @click="focusInput" style="cursor: pointer;"> -->
        <span class="input-group-text bg-white border-end-0" @click="handleManualSearch" style="cursor: pointer;">
          <i class="bi bi-search text-muted" style="color: #027562;"></i>
        </span>
        <input
          ref="searchInput"
          v-model="searchQuery"
          @focus="showResults = true"
          @blur="handleBlur"
          @keydown="handleKeydown"
          class="form-control border-start-0 ps-0"
          type="text"
          placeholder="Go for it!"
          autocomplete="off"
        />
      </div>
    </div>

    <!-- Results Dropdown -->
    <div 
      v-if="showResults && searchQuery.length >= 2" 
      class="dropdown-menu d-block position-absolute w-100 mt-1 shadow-lg border-0" style="max-height: 750px;"
      @mouseenter="isMousedOverResults = true"
      @mouseleave="isMousedOverResults = false"
    >
      <!-- Loading State -->
      <div v-if="isLoading" class="d-flex align-items-center justify-content-center p-4">
        <div class="spinner-border spinner-border-sm text-primary me-2" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <span class="text-muted">Searching...</span>
      </div>

      <!-- Results Content -->
      <div v-else-if="hasResults">
        <!-- Listings Section -->
        <div v-if="results.listings.length > 0">
          <h6 class="dropdown-header d-flex align-items-center py-2 px-3 mb-0">
            <i class="bi bi-cup-hot me-2 text-muted"></i>
            <span class="fw-small text-muted">Listings</span>
          </h6>
          <div
            v-for="(item, index) in results.listings"
            :key="`listing-${item.id}`"
            :class="[
              'dropdown-item search-item py-2 px-3',
              { 'active': selectedIndex === getItemIndex('listings', index) }
            ]"
            @mousedown="selectItem(item, 'listings', $event)"
            @mouseenter="selectedIndex = getItemIndex('listings', index)"
            role="button"
          >
            <div class="d-flex justify-content-between align-items-center w-100">
              <div class="d-flex flex-column">
                <span class="fw-small text-dark item-name">{{ item.listingName }}</span>
                <small class="text-muted producer-name">{{ item.producerName || "Unknown Producer" }}</small>
              </div>
              <small class="text-muted item-detail">{{ item.originCountry || item.drinkType }}</small>
            </div>
          </div>
          <div class="dropdown-divider my-1" v-if="results.venues.length > 0 || results.producers.length > 0 || results.users.length > 0"></div>
        </div>

        <!-- Venues Section -->
        <div v-if="results.venues.length > 0">
          <h6 class="dropdown-header d-flex align-items-center py-2 px-3 mb-0">
            <i class="bi bi-geo-alt me-2 text-muted"></i>
            <span class="fw-small text-muted">Venues</span>
          </h6>
          <div
            v-for="(item, index) in results.venues"
            :key="`venue-${item.id}`"
            :class="[
              'dropdown-item search-item py-2 px-3',
              { 'active': selectedIndex === getItemIndex('venues', index) }
            ]"
            @mousedown="selectItem(item, 'venues', $event)"
            @mouseenter="selectedIndex = getItemIndex('venues', index)"
            role="button"
          >
            <div class="d-flex justify-content-between align-items-center w-100">
              <div class="d-flex flex-column">
                <span class="fw-small text-dark item-name">{{ item.venueName }}</span>
                <small class="text-muted venue-address">{{ item.address || "No address" }}</small>
              </div>
              <small class="text-muted item-detail">{{ item.originLocation || "unknown" }}</small>
            </div>
          </div>
          <div class="dropdown-divider my-1" v-if="results.producers.length > 0 || results.users.length > 0"></div>
        </div>

        <!-- Producers Section -->
        <div v-if="results.producers.length > 0">
          <h6 class="dropdown-header d-flex align-items-center py-2 px-3 mb-0">
            <i class="bi bi-people me-2 text-muted"></i>
            <span class="fw-small text-muted">Producers</span>
          </h6>
          <div
            v-for="(item, index) in results.producers"
            :key="`producer-${item.id}`"
            :class="[
              'dropdown-item search-item py-2 px-3',
              { 'active': selectedIndex === getItemIndex('producers', index) }
            ]"
            @mousedown="selectItem(item, 'producers', $event)"
            @mouseenter="selectedIndex = getItemIndex('producers', index)"
            role="button"
          >
            <div class="d-flex justify-content-between align-items-center w-100">
              <span class="fw-medium text-dark item-name">{{ item.producerName }}</span>
              <small class="text-muted item-detail">{{ item.originCountry || "Not specified" }}</small>
            </div>
          </div>
          <div class="dropdown-divider my-1" v-if="results.users.length > 0"></div>
        </div>

        <!-- Users Section -->
        <div v-if="results.users.length > 0">
          <h6 class="dropdown-header d-flex align-items-center py-2 px-3 mb-0">
            <i class="bi bi-person me-2 text-muted"></i>
            <span class="fw-small text-muted">Users</span>
          </h6>
          <div
            v-for="(item, index) in results.users"
            :key="`user-${item.id}`"
            :class="[
              'dropdown-item search-item py-2 px-3',
              { 'active': selectedIndex === getItemIndex('users', index) }
            ]"
            @mousedown="selectItem(item, 'users', $event)"
            @mouseenter="selectedIndex = getItemIndex('users', index)"
            role="button"
          >
            <div class="d-flex align-items-center w-100">
              <div class="user-avatar me-2">
                <img 
                  v-if="item.photo" 
                  :src="item.photo" 
                  :alt="item.username"
                  class="rounded-circle"
                  style="width: 24px; height: 24px; object-fit: cover;"
                />
                <div 
                  v-else
                  class="rounded-circle bg-secondary d-flex align-items-center justify-content-center"
                  style="width: 24px; height: 24px; font-size: 12px; color: white;"
                >
                  {{ item.username ? item.username.charAt(0).toUpperCase() : '?' }}
                </div>
              </div>
              <div class="d-flex flex-column flex-grow-1">
                <span class="fw-medium text-dark item-name">@{{ item.username }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- No Results -->
      <div v-else-if="!isLoading && searchQuery.length >= 2" class="text-center p-4">
        <div class="mb-2">
          <i class="bi bi-search text-muted" style="font-size: 2rem;"></i>
        </div>
        <div class="fw-medium text-muted">Nothing found</div>
        <small class="text-muted">Try different keywords</small>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, watch, computed } from 'vue'
import { useRouter } from 'vue-router'


export default {
  name: 'AutocompleteSearch',
  emits: ['select'],
  setup(props, { emit }) {
    const router = useRouter()
    const listingsReturnCount = 6
    const venuesReturnCount = 3
    const producersReturnCount = 3
    const usersReturnCount = 3
    const searchInput = ref(null)
    const searchQuery = ref('')
    const showResults = ref(false)
    const isLoading = ref(false)
    const selectedIndex = ref(-1)
    const debounceTimer = ref(null)
    const abortController = ref(null)

    const results = reactive({
      listings: [],
      venues: [],
      producers: [],
      users: []
    })

    // Calculate total items for keyboard navigation
    const getTotalItems = () => {
      return results.listings.length + results.venues.length + results.producers.length + results.users.length
    }

    const getItemIndex = (section, index) => {
      let baseIndex = 0
      if (section === 'venues') {
        baseIndex = results.listings.length
      } else if (section === 'producers') {
        baseIndex = results.listings.length + results.venues.length
      } else if (section === 'users') {
        baseIndex = results.listings.length + results.venues.length + results.producers.length
      }
      return baseIndex + index
    }

    const hasResults = computed(() => {
      return results.listings.length > 0 || results.venues.length > 0 || results.producers.length > 0 || results.users.length > 0
    })

    // API calls
    const getBottleListings = async (query, signal) => {
      const api_endpoint = `${process.env.VUE_APP_API_URL}/getData/bottle-listings?q=${encodeURIComponent(query)}&limit=${listingsReturnCount}`
      const response = await fetch(api_endpoint, {
        signal,
      })

      if (response.status === 404) {
        // Expected behavior for no results
        return []
      }      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      return response.json()
    }

    const getVenueListings = async (query, signal) => {
      // Replace with your actual API endpoint get_venue_listings
      const response = await fetch(`${process.env.VUE_APP_API_URL}/getData/venue-listings?q=${encodeURIComponent(query)}&limit=${venuesReturnCount}`, {
        signal
      })
      if (response.status === 404) {
        // Expected behavior for no results
        return []
      }      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      return response.json()
    }

    const getProducerListings = async (query, signal) => {
      // Replace with your actual API endpoint
      const response = await fetch(`${process.env.VUE_APP_API_URL}/getData/producer-listings?q=${encodeURIComponent(query)}&limit=${producersReturnCount}`, {
        signal
      })
      if (response.status === 404) {
        // Expected behavior for no results
        return []
      }      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      return response.json()
    }

    const getUserListings = async (query, signal) => {
      const response = await fetch(`${process.env.VUE_APP_API_URL}/getData/user-listings?q=${encodeURIComponent(query)}&limit=${usersReturnCount}`, {
        signal
      })
      if (response.status === 404) {
        // Expected behavior for no results
        return []
      }      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      return response.json()
    }

    const performSearch = async (query) => {
      // Clear results immediately if query is too short
      if (query.length < 1) {
        results.listings = []
        results.venues = []
        results.producers = []
        results.users = []
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
        // Make all API calls concurrently
        const [listingsData, venuesData, producersData, usersData] = await Promise.all([
          getBottleListings(query, signal).catch(() => []),
          getVenueListings(query, signal).catch(() => []),
          getProducerListings(query, signal).catch(() => []),
          getUserListings(query, signal).catch(() => [])
        ])

        // Update results
        results.listings = listingsData || []
        results.venues = venuesData || []
        results.producers = producersData || []
        results.users = usersData || []

      } catch (error) {
        if (error.name !== 'AbortError') {
          // Only log unexpected errors (not 404s or network issues)
          // console.error('Unexpected search error:', error)
          results.listings = []
          results.venues = []
          results.producers = []
          results.users = []
        }
      } finally {
        isLoading.value = false
      }
    }

    // Debounced search
    const debouncedSearch = (query) => {
      // Clear any existing timer
      if (debounceTimer.value) {
        clearTimeout(debounceTimer.value)
      }
      
      // Only debounce if we have a query, otherwise search immediately
      if (query.length >= 1) {
        debounceTimer.value = setTimeout(() => {
          performSearch(query)
        }, 300)
      } else {
        // Immediately clear results for empty/short queries
        performSearch(query)
      }
    }

    // Watch for search query changes
    watch(searchQuery, (newQuery) => {
      // Trim whitespace for better UX
      const trimmedQuery = newQuery.trim()
      
      if (trimmedQuery.length >= 2) {
        debouncedSearch(trimmedQuery)
      } else {
        // Immediately clear results and stop loading for empty/short queries
        results.listings = []
        results.venues = []
        results.producers = []
        results.users = []
        isLoading.value = false
        
        // Cancel any pending requests
        if (abortController.value) {
          abortController.value.abort()
        }
        
        // Clear any pending debounced search
        if (debounceTimer.value) {
          clearTimeout(debounceTimer.value)
        }
      }
    })

    // Get item by index for keyboard navigation
    const getItemByIndex = (index) => {
      const totalListings = results.listings.length
      const totalVenues = results.venues.length
      const totalProducers = results.producers.length
      
      if (index < totalListings) {
        return { item: results.listings[index], type: 'listings' }
      } else if (index < totalListings + totalVenues) {
        return { item: results.venues[index - totalListings], type: 'venues' }
      } else if (index < totalListings + totalVenues + totalProducers) {
        return { item: results.producers[index - totalListings - totalVenues], type: 'producers' }
      } else {
        return { item: results.users[index - totalListings - totalVenues - totalProducers], type: 'users' }
      }
    }

    // Handle manual search (magnifier click or Enter without dropdown selection)
    const handleManualSearch = () => {
      const query = searchQuery.value.trim()
      if (query.length > 0) {
        // Create a custom search item
        const customItem = {
          name: query,
          // Add any other properties you might need
        }
        
        emit('select', { item: customItem, type: 'Any' })
        showResults.value = false
        searchInput.value.blur()
      }
    }

    // Keyboard navigation
    const handleKeydown = (event) => {
      // if (!showResults.value || getTotalItems() === 0) return
      if (!showResults.value) {
        // Handle Enter when dropdown is not showing
        if (event.key === 'Enter') {
          event.preventDefault()
          handleManualSearch()
        }
        return
      }

      // Handle keyboard navigation when dropdown is showing
      if (getTotalItems() === 0) {
        // No dropdown items, handle Enter for manual search
        if (event.key === 'Enter') {
          event.preventDefault()
          handleManualSearch()
        }
        return
      }

      switch (event.key) {
        case 'ArrowDown':
          event.preventDefault()
          selectedIndex.value = selectedIndex.value < getTotalItems() - 1 
            ? selectedIndex.value + 1 
            : 0
          break
        case 'ArrowUp':
          event.preventDefault()
          selectedIndex.value = selectedIndex.value > 0 
            ? selectedIndex.value - 1 
            : getTotalItems() - 1
          break
        case 'Enter':
          event.preventDefault()
          if (selectedIndex.value >= 0) {
            // Select from dropdown
            const { item, type } = getItemByIndex(selectedIndex.value)
            selectItem(item, type)
          } else {
            // No item selected, perform manual search
            handleManualSearch()
          }
          break
        case 'Escape':
          event.preventDefault()
          showResults.value = false
          searchInput.value.blur()
          break
      }
    }

    const isMousedOverResults = ref(false)

    // Handle input blur
    const handleBlur = () => {
      if (!isMousedOverResults.value) {
        showResults.value = false
      }
    }

    // // Handle item selection - execute as search query
    // const selectItem = (item, type, event) => {
    //   if (event) {
    //     event.preventDefault()
    //   }

    //   emit('select', { item, type })
      
    //   let name = ''
    //   if (type === 'listings') {
    //     name = item.listingName
    //   } else if (type === 'venues') {
    //     name = item.venueName
    //   } else if (type === 'producers') {
    //     name = item.producerName
    //   }
    //   searchQuery.value = name

    //   showResults.value = false
    //   isMousedOverResults.value = false // Reset the flag
    //   searchInput.value.blur()
    // }

    // // Handle item selection - directly go to bottling page

    const selectItem = (item, type, event) => {
      if (event) {
        event.preventDefault()
      }
      
      // Navigate directly based on type with correct URL patterns
      if (type === 'listings') {
        // Use the correct listing view route with slug if available
        const slug = item.listingName ? '/' + item.listingName.toLowerCase().replace(/\s+/g, '') : ''
        router.push(`/listing/view/${item.id}${slug}`)
      } else if (type === 'venues') {
        // Use the correct venue profile route with name slug if available
        const slug = item.venueName ? '/' + item.venueName.toLowerCase().replace(/\s+/g, '') : ''
        router.push(`/profile/venue/${item.id}${slug}`)
      } else if (type === 'producers') {
        // Use the correct producer profile route with name slug if available
        const slug = item.producerName ? '/' + item.producerName.toLowerCase().replace(/\s+/g, '') : ''
        router.push(`/profile/producer/${item.id}${slug}`)
      } else if (type === 'users') {
        // Navigate to user profile
        const slug = item.username ? '/' + item.username.toLowerCase().replace(/\s+/g, '') : ''
        router.push(`/profile/user/${item.id}${slug}`)
      }

      showResults.value = false
      isMousedOverResults.value = false // Reset the flag
      searchInput.value.blur()
    }
    
    return {
      searchInput,
      searchQuery,
      showResults,
      isLoading,
      selectedIndex,
      results,
      hasResults,
      handleKeydown,
      handleBlur,
      selectItem,
      getItemIndex
    }
  }
}
</script>

<style scoped>
.search-container {
  position: relative;
  width: 100%;
}

.dropdown-menu {
  border-radius: 8px;
  padding: 0.2rem 0.25rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.dropdown-header {
  font-size: 0.800rem;
  font-weight: 600;
  color: #6c757d;
  background-color: transparent;
  border-bottom: none;
  text-transform: none;
  letter-spacing: normal;
}

.search-item {
  transition: all 0.15s ease;
  border: none;
  background: white;
  min-height: 40px;
  display: flex;
  align-items: center;
  cursor: pointer;
  margin: 0;
  border-radius: 4px;
}

.search-item:hover {
  background-color: #f8f9fa;
}

.search-item.active {
  background-color: #027562;
  color: white;
}

.search-item.active .producer-name, 
.search-item.active .venue-address,
.search-item.active .user-display-name {
  color: rgba(255, 255, 255, 0.8) !important;
}


.search-item.active .text-muted,
.search-item.active .item-detail {
  color: rgba(255, 255, 255, 0.8) !important;
}

.search-item.active .item-name {
  color: white !important;
}

.item-name {
  margin-left: 1rem;
  font-size: 0.90rem;
  font-weight: 500;
  color: #212529;
}

.item-detail {
  font-size: 0.80rem;
  color: #6c757d;
  font-weight: 400;
}

.dropdown-divider {
  margin: 0.3rem 0.6rem;
  border-top: 1px solid #e9ecef;
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
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.form-control::placeholder {
  color: #adb5bd;
  font-weight: 400;
}

/* input.form-control {
    border: none; 
    box-shadow: none !important; 
    outline: none; 
} */

/* Mobile-first responsive adjustments */
@media (max-width: 576px) {
  .search-container {
    max-width: 100%;
  }
  
  .dropdown-menu {
    max-height: 300px !important;
    margin: 0.25rem;
    left: 0 !important;
    right: 0 !important;
    max-width: calc(100vw - 0.5rem);
  }
  
  .search-item {
    padding: 0.5rem 1rem !important;
    min-height: 48px;
  }
  
  .item-name {
    font-size: 1rem;
  }
  
  .item-detail {
    font-size: 0.9rem;
  }
}

/* Tablet adjustments */
@media (min-width: 577px) and (max-width: 768px) {
  .search-container {
    max-width: 90%;
  }
}

/* Ensure proper touch targets for mobile */
@media (max-width: 768px) {
  .search-item {
    min-height: 44px;
  }
}

.producer-name {
  font-size: 0.75rem;
  margin-left: 1rem;
  margin-top: 2px;
  display: block;
  color: #6c757d;
}

.venue-address{
  font-size: 0.75rem;
  margin-left: 1rem;
  margin-top: 2px;
  display: block;
  color: #6c757d;
}

.user-display-name {
  font-size: 0.75rem;
  margin-top: 2px;
  display: block;
  color: #6c757d;
}

.user-avatar {
  flex-shrink: 0;
}

</style>