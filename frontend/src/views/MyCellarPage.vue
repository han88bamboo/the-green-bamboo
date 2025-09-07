<template>
  <NavBar />
  
  <main>
    <!-- Page Header -->
    <section class="page-header py-4">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <h1 class="page-title fw-bold mb-0">My Cellar</h1>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content Grid -->
    <section class="main-content py-4">
      <div class="container">
        <div class="row">
          <!-- Left Column - Collections & Items (8/12 columns) -->
          <div class="col-12 col-lg-8">
            <!-- Tab Navigation -->
            <div class="tabs-container">
              <nav class="tabs-nav p-0">
                <ul class="nav nav-tabs folder-tabs">
                  <!-- All Drinks Tab -->
                  <li class="nav-item">
                    <button 
                      class="nav-link folder-tab"
                      :class="{ active: activeTab === 'all' }"
                      @click="setActiveTab('all')"
                      type="button"
                    >
                      All Drinks in Cellar
                      <span class="item-count" v-if="!loading">{{ totalItemCount }} Items</span>
                      <span class="item-count" v-else>...</span>
                    </button>
                  </li>
                  <!-- Dynamic Collection Tabs -->
                  <li class="nav-item" v-for="collection in collections" :key="collection.id">
                    <button 
                      class="nav-link folder-tab"
                      :class="{ active: activeTab === collection.id }"
                      @click="setActiveTab(collection.id)"
                      type="button"
                      v-if="!collection.isDefault"
                    >
                      {{ collection.collectionName }}
                      <span class="item-count">{{ collection.itemCount }} Items</span>
                    </button>
                  </li>
                  <!-- Add Collection Ghost Tab -->
                  <li class="nav-item">
                    <button 
                      class="nav-link folder-tab ghost-tab"
                      type="button"
                      data-bs-toggle="modal"
                      data-bs-target="#addCollectionModal"
                    >
                      <i class="bi bi-plus-circle me-2"></i>
                      Add new Collection
                    </button>
                  </li>
                </ul>
              </nav>
            </div>

            <!-- Cellar Surface - unified container for filters and items -->
            <section class="cellar-surface">
              <!-- Filters Row -->
              <div class="filters-container">
                <div class="row g-3">
                  <!-- Search Input -->
                  <div class="col-12 col-md-4">
                    <div class="input-group">
                      <span class="input-group-text">
                        <i class="bi bi-search"></i>
                      </span>
                      <input
                        type="text"
                        class="form-control"
                        placeholder="Search by name or producer..."
                        v-model="searchQuery"
                        @input="debouncedSearch"
                      >
                    </div>
                  </div>

                  <!-- Vintage Filter -->
                  <div class="col-6 col-md-2">
                    <select class="form-select" v-model="filters.vintage">
                      <option value="">Any Vintage</option>
                      <option v-for="year in vintageOptions" :key="year" :value="year">
                        {{ year }}
                      </option>
                    </select>
                  </div>

                  <!-- Size Filter -->
                  <div class="col-6 col-md-2">
                    <select class="form-select" v-model="filters.size">
                      <option value="">Any Size</option>
                      <option value="187">187ml</option>
                      <option value="375">375ml</option>
                      <option value="750">750ml</option>
                      <option value="1500">1.5L</option>
                    </select>
                  </div>

                  <!-- Status Filter -->
                  <div class="col-6 col-md-2">
                    <select class="form-select" v-model="filters.status">
                      <option value="">Any Status</option>
                      <option value="In Possession">In Cellar</option>
                      <option value="On Its Way">On Its Way</option>
                      <option value="Wishlisted">Wishlisted</option>
                      <option value="Consumed">Consumed</option>
                    </select>
                  </div>

                  <!-- Drink Now Checkbox -->
                  <div class="col-6 col-md-2">
                    <div class="form-check">
                      <input
                        class="form-check-input"
                        type="checkbox"
                        id="drinkNowFilter"
                        v-model="filters.drinkNow"
                      >
                      <label class="form-check-label" for="drinkNowFilter">
                        Only drink-now
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Items Grid -->
              <div class="items-grid">
              <!-- Loading Skeletons -->
              <div v-if="loading" class="row">
                <div 
                  v-for="n in 9" 
                  :key="'skeleton-' + n"
                  class="col-12 col-md-6 col-lg-4 mb-4"
                >
                  <div class="card cellar-item-skeleton">
                    <div class="skeleton-image"></div>
                    <div class="card-body">
                      <div class="skeleton-line skeleton-title"></div>
                      <div class="skeleton-line skeleton-subtitle"></div>
                      <div class="skeleton-line skeleton-notes"></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Error State -->
              <div v-else-if="error" class="text-center py-5">
                <div class="alert alert-danger" role="alert">
                  <h4 class="alert-heading">Error Loading Cellar</h4>
                  <p>{{ error }}</p>
                  <button class="btn btn-outline-danger" @click="loadCellarData">
                    Try Again
                  </button>
                </div>
              </div>

              <!-- Empty State -->
              <div v-else-if="filteredItems.length === 0" class="empty-state text-center py-5">
                <div class="empty-icon mb-3">
                  🍷
                </div>
                <h3 class="mb-2">No bottles match your filters</h3>
                <p class="text-muted">
                  Try adjusting your search criteria or add some drinks to your cellar.
                </p>
                <button class="btn btn-primary" @click="clearFilters">
                  Clear Filters
                </button>
              </div>

              <!-- Items Cards -->
              <div v-else class="row">
                <div 
                  v-for="group in paginatedItems" 
                  :key="`${group.listingId}_${group.variant || 'no-variant'}`"
                  class="col-12 col-md-6 col-lg-4 mb-4"
                >
                  <div 
                    class="card cellar-item-card h-100"
                    role="button"
                    tabindex="0"
                    data-bs-toggle="modal"
                    data-bs-target="#itemDetailsModal"
                    @click="setSelectedGroup(group)"
                    @keyup.enter="setSelectedGroup(group)"
                  >
                    <!-- Image Area -->
                    <div class="card-img-container">
                      <img 
                        :src="getItemImageUrl(group.representative)"
                        :alt="group.representative.listingName"
                        class="card-img-top"
                        @error="onImageError"
                      >
                      <!-- Bottle Count Badge -->
                      <div class="quantity-badge">
                        {{ group.bottleCount }} bottle{{ group.bottleCount !== 1 ? 's' : '' }}
                      </div>
                    </div>

                    <!-- Info Band -->
                    <div class="card-body">
                      <div class="card-content">
                        <!-- Primary Line -->
                        <h6 class="card-title" :title="group.representative.listingName">
                          {{ group.representative.listingName }}
                          <span v-if="group.representative.variant" class="text-muted ms-1">
                            ({{ group.representative.variant }})
                          </span>
                        </h6>
                        
                        <!-- Secondary Line -->
                        <p class="card-subtitle text-muted mb-2">
                          {{ group.representative.drinkType }}
                          <span v-if="group.representative.typeCategory"> | {{ group.representative.typeCategory }}</span>
                        </p>

                        <!-- Producer -->
                        <p class="card-producer text-muted mb-2" v-if="group.representative.producerName">
                          {{ group.representative.producerName }}
                        </p>

                        <!-- Notes (from representative bottle) -->
                        <p 
                          class="card-notes text-muted small" 
                          v-if="group.representative.noteToSelf"
                          :title="group.representative.noteToSelf"
                        >
                          {{ group.representative.noteToSelf }}
                        </p>

                        <!-- Status Overview -->
                        <div class="status-info mt-2">
                          <div class="status-breakdown">
                            <span 
                              v-for="(count, status) in getGroupStatusBreakdown(group.bottles)"
                              :key="status"
                              class="status-badge badge me-1"
                              :class="getStatusBadgeClass(status)"
                              :title="`${count} bottle${count !== 1 ? 's' : ''} ${status.toLowerCase()}`"
                            >
                              {{ count }}x {{ status }}
                            </span>
                          </div>
                          <div class="drink-dates mt-1" v-if="group.representative.drinkByDate || group.representative.drinkOnwardsDate">
                            <small class="text-muted">
                              <span v-if="group.representative.drinkOnwardsDate">
                                Drink from: {{ formatDate(group.representative.drinkOnwardsDate) }}
                              </span>
                              <span v-if="group.representative.drinkByDate">
                                Drink by: {{ formatDate(group.representative.drinkByDate) }}
                              </span>
                            </small>
                          </div>
                        </div>
                      </div>

                      <!-- Hover Actions (Desktop Only) -->
                      <div class="hover-actions d-none d-lg-flex">
                        <button 
                          class="btn btn-sm btn-outline-primary"
                          @click.stop="consumeGroup(group)"
                          title="Coming soon"
                          disabled
                        >
                          Consume
                        </button>
                        <button 
                          class="btn btn-sm btn-outline-secondary"
                          @click.stop="adjustGroup(group)"
                          title="Coming soon"
                          disabled
                        >
                          Adjust
                        </button>
                        <button 
                          class="btn btn-sm btn-outline-info"
                          @click.stop="moveGroup(group)"
                          title="Coming soon"
                          disabled
                        >
                          Move
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Pagination -->
              <div v-if="totalPages > 1" class="pagination-container mt-4">
                <nav aria-label="Cellar items pagination">
                  <ul class="pagination justify-content-start">
                    <li class="page-item" :class="{ disabled: currentPage === 1 }">
                      <button 
                        class="page-link" 
                        @click="goToPage(currentPage - 1)"
                        :disabled="currentPage === 1"
                      >
                        Previous
                      </button>
                    </li>
                    <li 
                      class="page-item" 
                      :class="{ active: page === currentPage }"
                      v-for="page in visiblePages" 
                      :key="page"
                    >
                      <button class="page-link" @click="goToPage(page)">
                        {{ page }}
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                      <button 
                        class="page-link" 
                        @click="goToPage(currentPage + 1)"
                        :disabled="currentPage === totalPages"
                      >
                        Next
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
            </section>
          </div>

          <!-- Right Column - Add Drink to Cellar (4/12 columns) -->
          <div class="col-12 col-lg-4 mt-4 mt-lg-0">
            <div class="add-drink-to-cellar">
              <div class="card h-100">
                <div class="card-header">
                  <h5 class="card-title mb-0">
                    <i class="bi bi-plus-circle me-2"></i>
                    Add Drink(s) to Cellar
                  </h5>
                </div>
                <div class="card-body">
                  <form @submit.prevent="addDrinkToCellar">
                    <!-- Producer Search -->
                    <div class="form-group mb-3">
                      <label class="form-label text-start">
                        Producer (Optional)
                        <small class="text-muted d-block text-start">Select a producer to filter drink search</small>
                      </label>
                      <input 
                        type="text" 
                        class="form-control"
                        v-model="addDrinkForm.producerSearchQuery"
                        @input="debouncedSearchProducers"
                        placeholder="Search for a producer to filter drinks..."
                      />
                      <ul 
                        class="list-group mt-1"
                        v-if="addDrinkForm.producerSearchResults && addDrinkForm.producerSearchResults.length > 0 && addDrinkForm.producerSearchQuery"
                      >
                        <li 
                          v-for="producer in addDrinkForm.producerSearchResults" 
                          :key="producer.id"
                          class="list-group-item list-group-item-action"
                          @click="selectProducer(producer)"
                        >
                          {{ producer.producerName }}
                          <small class="text-muted">
                            ({{ producer.originCountry }})
                          </small>
                        </li>
                      </ul>
                      <!-- Show selected producer -->
                      <div 
                        v-if="addDrinkForm.selectedProducer && addDrinkForm.selectedProducer.id" 
                        class="mt-2 p-2 bg-light border rounded text-start"
                      >
                        <small class="text-success fw-bold">
                          ✓ Producer Selected: {{ addDrinkForm.selectedProducer.producerName }}
                          <button 
                            type="button" 
                            class="btn btn-sm btn-outline-danger ms-2"
                            @click="clearSelectedProducer"
                          >
                            Clear
                          </button>
                        </small>
                      </div>
                    </div>

                    <!-- Drink Search -->
                    <div class="form-group mb-3">
                      <label class="form-label text-start">
                        Drink Name <span class="text-danger">*</span>
                        <small class="text-muted d-block text-start">Start typing to search for drinks</small>
                        <small 
                          v-if="addDrinkForm.selectedProducer && addDrinkForm.selectedProducer.id" 
                          class="text-info fw-bold d-block text-start"
                        >
                          Filtered by {{ addDrinkForm.selectedProducer.producerName }}
                        </small>
                      </label>
                      <input 
                        type="text" 
                        class="form-control"
                        v-model="addDrinkForm.searchQuery"
                        @input="debouncedSearchDrinks"
                        :placeholder="addDrinkForm.selectedProducer && addDrinkForm.selectedProducer.id ? 
                          'Search drinks from ' + addDrinkForm.selectedProducer.producerName : 
                          'Enter a drink name to search...'"
                        required
                      />
                      <ul 
                        class="list-group mt-1"
                        v-if="addDrinkForm.searchResults && addDrinkForm.searchResults.length > 0 && addDrinkForm.searchQuery"
                      >
                        <li 
                          v-for="listing in addDrinkForm.searchResults" 
                          :key="listing.id"
                          class="list-group-item list-group-item-action"
                          @click="selectDrink(listing)"
                        >
                          {{ listing.listingName }}
                          <small class="text-muted d-block">
                            Producer: {{ listing.producerName }} | 
                            Type: {{ listing.drinkType }} | 
                            ABV: {{ listing.abv ? listing.abv + '%' : 'N/A' }} |
                            Country: {{ listing.originCountry }}
                          </small>
                        </li>
                      </ul>
                      <!-- Show selected drink -->
                      <div 
                        v-if="addDrinkForm.selectedDrink && addDrinkForm.selectedDrink.id" 
                        class="mt-2 p-2 bg-light border rounded text-start"
                      >
                        <small class="text-success fw-bold">
                          ✓ Drink Selected: {{ addDrinkForm.selectedDrink.listingName }}
                        </small>
                      </div>
                    </div>

                    <!-- Drink Preview Section -->
                    <div 
                      v-if="addDrinkForm.selectedDrink && addDrinkForm.selectedDrink.id"
                      class="cellar-item-preview mb-4"
                    >
                      <hr>
                      <p class="text-secondary-emphasis fw-bold fst-italic text-start mb-3">Drink Preview:</p>
                      
                      <!-- Desktop Preview -->
                      <div class="row d-none d-md-flex">
                        <!-- Item Image -->
                        <div class="col-3 text-center">
                          <img 
                            :src="getPreviewImageUrl(addDrinkForm.selectedDrink)"
                            class="preview-image"
                            style="max-width: 80px; max-height: 80px; object-fit: contain;"
                            @error="onImageError"
                          />
                        </div>

                        <!-- Item Information -->
                        <div class="col-9">
                          <!-- Item Name with Vintage -->
                          <div class="row mb-2">
                            <div class="col-12">
                              <h6 class="fw-bold text-start text-decoration-underline mb-0"
                                  style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                                {{ addDrinkForm.selectedDrink.listingName }}
                                <span v-if="addDrinkForm.vintage"> [{{ addDrinkForm.vintage }} Vintage]</span>
                              </h6>
                            </div>
                          </div>

                          <!-- Item Details -->
                          <div class="row mb-2">
                            <div class="col-12">
                              <p class="text-start mb-1 text-muted"
                                 style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                                <span v-if="addDrinkForm.selectedDrink.producerName">
                                  {{ addDrinkForm.selectedDrink.producerName }} |
                                </span>
                                <span v-if="addDrinkForm.selectedDrink.drinkType">
                                  {{ addDrinkForm.selectedDrink.drinkType }} |
                                </span>
                                <span v-if="addDrinkForm.selectedDrink.typeCategory">
                                  {{ addDrinkForm.selectedDrink.typeCategory }} |
                                </span>
                                <span v-if="addDrinkForm.selectedDrink.abv">
                                  {{ addDrinkForm.selectedDrink.abv }}% ABV |
                                </span>
                                <span v-if="addDrinkForm.selectedDrink.originCountry">
                                  {{ addDrinkForm.selectedDrink.originCountry }}
                                </span>
                              </p>

                              <!-- Description -->
                              <p class="text-start fst-italic mb-1 small text-muted"
                                 style="height: 40px; max-height: 40px; overflow-y: auto;">
                                <span v-if="addDrinkForm.selectedDrink.officialDesc">
                                  {{ addDrinkForm.selectedDrink.officialDesc }}
                                </span>
                                <span v-else class="text-muted">
                                  No description available
                                </span>
                              </p>
                            </div>
                          </div>

                          <!-- Cellar Details -->
                          <div class="row">
                            <div class="col-12">
                              <p class="text-start fw-bold text-primary mb-0">
                                <span v-if="addDrinkForm.quantity">
                                  Adding {{ addDrinkForm.quantity }} bottle{{ addDrinkForm.quantity !== 1 ? 's' : '' }}
                                </span>
                                <span v-if="addDrinkForm.status" class="ms-2">
                                  | Status: {{ addDrinkForm.status }}
                                </span>
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- Mobile Preview -->
                      <div class="row d-md-none">
                        <!-- Item Image -->
                        <div class="col-4 text-center">
                          <img 
                            :src="getPreviewImageUrl(addDrinkForm.selectedDrink)"
                            class="preview-image-mobile"
                            style="width: 80px; height: 80px; object-fit: contain;"
                            @error="onImageError"
                          />
                        </div>

                        <!-- Item Information -->
                        <div class="col-8">
                          <!-- Item Name -->
                          <h6 class="fw-bold text-start text-decoration-underline mb-1 small">
                            {{ addDrinkForm.selectedDrink.listingName }}
                            <span v-if="addDrinkForm.vintage"> [{{ addDrinkForm.vintage }}]</span>
                          </h6>

                          <!-- Item Details -->
                          <p class="text-start mb-1 small text-muted">
                            <span v-if="addDrinkForm.selectedDrink.producerName">
                              {{ addDrinkForm.selectedDrink.producerName }}
                            </span>
                            <span v-if="addDrinkForm.selectedDrink.drinkType">
                              | {{ addDrinkForm.selectedDrink.drinkType }}
                            </span>
                            <span v-if="addDrinkForm.selectedDrink.abv">
                              | {{ addDrinkForm.selectedDrink.abv }}% ABV
                            </span>
                          </p>

                          <!-- Cellar Details -->
                          <p class="text-start fw-bold text-primary mb-0 small">
                            Adding {{ addDrinkForm.quantity || 1 }} bottle{{ (addDrinkForm.quantity || 1) !== 1 ? 's' : '' }}
                          </p>
                        </div>
                      </div>
                    </div>

                    <!-- Quantity Section -->
                    <div class="form-group mb-3" v-if="addDrinkForm.selectedDrink && addDrinkForm.selectedDrink.id">
                      <label class="form-label text-start">
                        Quantity to Add<span class="text-danger">*</span>
                      </label>
                      <input 
                        type="number" 
                        class="form-control"
                        v-model="addDrinkForm.quantity"
                        min="1"
                        required
                        placeholder="Number of bottles"
                      />
                    </div>

                    <!-- Group Properties Section -->
                    <div class="form-section mb-4" v-if="addDrinkForm.selectedDrink && addDrinkForm.selectedDrink.id">
                      <hr>
                      <h6 class="section-header text-start mb-3">
                        <i class="bi bi-collection me-2"></i>
                        Group Properties
                        <small class="text-muted d-block fw-normal">Values applied to only Master Item within this group.</small>
                      </h6>

                      <!-- Row 1: Vintage -->
                      <div class="row g-3 mb-3" v-if="addDrinkForm.selectedDrink && ['Wine', 'Sake'].includes(addDrinkForm.selectedDrink.drinkType)">
                        <div class="col-md-12">
                          <label class="form-label text-start">Vintage</label>
                          <input 
                            type="number" 
                            class="form-control"
                            v-model="addDrinkForm.vintage"
                            min="1900" 
                            max="2030"
                            placeholder="e.g., 2020"
                          />
                        </div>
                      </div>

                      <!-- Row 2: Format, Volume -->
                      <div class="row g-3 mb-3">
                        <div class="col-md-6">
                          <label class="form-label text-start">Format</label>
                          <select 
                            class="form-select"
                            v-model="addDrinkForm.format"
                          >
                            <option value="Bottle">Bottle</option>
                            <option value="Can">Can</option>
                            <option value="Sample">Sample</option>
                          </select>
                        </div>
                        <div class="col-md-6">
                          <label class="form-label text-start">Volume</label>
                          <div class="input-group">
                            <input 
                              type="number" 
                              class="form-control"
                              v-model="addDrinkForm.volumeNumber"
                              step="0.1" 
                              min="0"
                              placeholder="750"
                            />
                            <select class="form-select" v-model="addDrinkForm.volumeUnit" style="max-width: 70px;">
                              <option value="ml">ml</option>
                              <option value="oz">oz</option>
                              <option value="l">L</option>
                            </select>
                          </div>
                        </div>
                      </div>

                      <!-- Row 3: Market Value -->
                      <div class="row g-3 mb-3">
                        <div class="col-md-12">
                          <label class="form-label text-start">Current Market Value</label>
                          <div class="input-group">
                            <select class="form-select" v-model="addDrinkForm.currentValueCurrency" style="max-width: 80px;">
                              <option value="USD">USD</option>
                              <option value="EUR">EUR</option>
                              <option value="GBP">GBP</option>
                              <option value="JPY">JPY</option>
                              <option value="CAD">CAD</option>
                              <option value="AUD">AUD</option>
                            </select>
                            <input 
                              type="number" 
                              class="form-control"
                              v-model="addDrinkForm.currentValueEstimation"
                              step="0.01"
                              min="0"
                              placeholder="0.00"
                            />
                          </div>
                        </div>
                      </div>

                      <!-- Row 4: Drinking Window -->
                      <div class="row g-3 mb-3">
                        <div class="col-md-6">
                          <label class="form-label text-start">Drink Onwards Date</label>
                          <div class="input-group">
                            <input 
                              type="date" 
                              class="form-control"
                              v-model="addDrinkForm.drinkOnwardsDate"
                            />
                            <span class="input-group-text">
                              <i class="bi bi-calendar3"></i>
                            </span>
                          </div>
                        </div>
                        <div class="col-md-6">
                          <label class="form-label text-start">Drink By Date</label>
                          <div class="input-group">
                            <input 
                              type="date" 
                              class="form-control"
                              v-model="addDrinkForm.drinkByDate"
                            />
                            <span class="input-group-text">
                              <i class="bi bi-calendar3"></i>
                            </span>
                          </div>
                        </div>
                      </div>

                      <!-- Row 5: Food Pairing -->
                      <div class="row g-3 mb-3">
                        <div class="col-md-12">
                          <label class="form-label text-start">Suggested Food Pairing</label>
                          <div class="input-group">
                            <input 
                              type="text" 
                              class="form-control"
                              v-model="addDrinkForm.suggestedFoodPairing"
                              placeholder="e.g., Grilled salmon, Dark chocolate"
                            />
                            <button class="btn btn-outline-secondary" type="button" disabled title="Coming soon">+</button>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Individual Item Properties Section -->
                    <div class="form-section mb-4" v-if="addDrinkForm.selectedDrink && addDrinkForm.selectedDrink.id">
                      <hr>
                      <h6 class="section-header text-start mb-3">
                        <i class="bi bi-bottle me-2"></i>
                        Individual Item Properties
                        <small class="text-muted d-block fw-normal">
                          Values here are applied to every individual bottle (can be adjusted later in the cellar)
                        </small>
                      </h6>

                      <!-- Row 1: Status, Consumption -->
                      <div class="row g-3 mb-3">
                        <div class="col-md-6">
                          <label class="form-label text-start">Status</label>
                          <select 
                            class="form-select"
                            v-model="addDrinkForm.status"
                          >
                            <option value="In Possession">In Possession</option>
                            <option value="On Its Way">On Its Way</option>
                            <option value="Purchased">Purchased</option>
                            <option value="Held Elsewhere">Held Elsewhere</option>
                            <option value="Wishlisted">Wishlisted</option>
                          </select>
                        </div>
                        <div class="col-md-6">
                          <label class="form-label text-start">Consumption</label>
                          <select 
                            class="form-select"
                            v-model="addDrinkForm.consumption"
                          >
                            <option value="Unopened">Unopened</option>
                            <option value="Opened">Opened</option>
                            <option value="Empty">Empty</option>
                          </select>
                        </div>
                      </div>

                      <!-- Row 2: Storage Location, Sub Location -->
                      <div class="row g-3 mb-3">
                        <div class="col-md-6">
                          <label class="form-label text-start">Storage Location</label>
                          <input 
                            type="text" 
                            class="form-control"
                            v-model="addDrinkForm.currentLocation"
                            placeholder="e.g., Wine fridge, Cellar rack 3"
                          />
                        </div>
                        <div class="col-md-6">
                          <label class="form-label text-start">Sub Location</label>
                          <input 
                            type="text" 
                            class="form-control"
                            v-model="addDrinkForm.subLocation"
                            placeholder="e.g., Minibar, Kitchen cabinet"
                          />
                        </div>
                      </div>

                      <!-- Row 3: Place of Purchase -->
                      <div class="row g-3 mb-3">
                        <div class="col-md-12">
                          <label class="form-label text-start">Place of Purchase</label>
                          <div class="purchase-location-container" style="position: relative;">
                            <!-- Google Maps Autocomplete Input -->
                            <div class="input-group">
                              <GMapAutocomplete 
                                placeholder="e.g., Wine shop, Online store, or enter manually"
                                @place_changed="setPurchasePlaceFromAutocomplete" 
                                @input="onPurchaseLocationInput"
                                @focus="onPurchaseLocationFocus" 
                                @blur="onPurchaseLocationBlur"
                                class="form-control input-with-icon" 
                                ref="purchaseLocationInput" 
                                :value="addDrinkForm.purchaseLocationInputValue"
                                :options="{ types: ['establishment'] }"
                              />
                              <span class="input-group-text" :title="addDrinkForm.selectedPurchasePlace ? 'Location selected via Google Maps' : 'Click input to search locations'">
                                <i class="bi bi-geo-alt" :class="{ 'text-success': addDrinkForm.selectedPurchasePlace }"></i>
                              </span>
                            </div>
                            
                            <!-- Location confirmation display -->
                            <div v-if="addDrinkForm.selectedPurchasePlace && addDrinkForm.selectedPurchaseAddress" 
                                 class="alert alert-success mt-2 mb-0 small">
                              📍 Selected: {{ addDrinkForm.selectedPurchasePlace }}
                              <br>
                              <small class="text-muted">{{ addDrinkForm.selectedPurchaseAddress }}</small>
                              <button 
                                type="button" 
                                class="btn btn-sm btn-outline-danger ms-2"
                                @click="clearSelectedPurchaseLocation"
                              >
                                Clear
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- Row 4: Purchase Date, Delivery Date -->
                      <div class="row g-3 mb-3">
                        <div class="col-md-6">
                          <label class="form-label text-start">Purchase Date</label>
                          <div class="input-group">
                            <input 
                              type="date" 
                              class="form-control"
                              v-model="addDrinkForm.purchaseDate"
                            />
                            <span class="input-group-text">
                              <i class="bi bi-calendar3"></i>
                            </span>
                          </div>
                        </div>
                        <div class="col-md-6">
                          <label class="form-label text-start">Delivery Date</label>
                          <div class="input-group">
                            <input 
                              type="date" 
                              class="form-control"
                              v-model="addDrinkForm.deliveryDate"
                            />
                            <span class="input-group-text">
                              <i class="bi bi-calendar3"></i>
                            </span>
                          </div>
                        </div>
                      </div>

                      <!-- Row 5: Purchase Price -->
                      <div class="row g-3 mb-3">
                        <div class="col-md-12">
                          <label class="form-label text-start">Purchase Price</label>
                          <div class="input-group">
                            <select class="form-select" v-model="addDrinkForm.purchaseCurrency" style="max-width: 80px;">
                              <option value="USD">USD</option>
                              <option value="EUR">EUR</option>
                              <option value="GBP">GBP</option>
                              <option value="JPY">JPY</option>
                              <option value="CAD">CAD</option>
                              <option value="AUD">AUD</option>
                            </select>
                            <input 
                              type="number" 
                              class="form-control"
                              v-model="addDrinkForm.purchasePrice"
                              step="0.01"
                              min="0"
                              placeholder="0.00"
                            />
                          </div>
                        </div>
                      </div>

                      <!-- Row 6: Personal Notes -->
                      <div class="row g-3 mb-3">
                        <div class="col-md-12">
                          <label class="form-label text-start">Personal Notes</label>
                          <textarea 
                            class="form-control"
                            v-model="addDrinkForm.personalNotes"
                            rows="3"
                            placeholder="Add your personal notes about these bottles..."
                          ></textarea>
                        </div>
                      </div>
                    </div>

                    <!-- Collection Selection Section -->
                    <div class="form-section mb-4" v-if="addDrinkForm.selectedDrink && addDrinkForm.selectedDrink.id">
                      <hr>
                      <h6 class="section-header text-start mb-3">
                        <i class="bi bi-collection me-2"></i>
                        Collection Selection
                        <small class="text-muted d-block fw-normal">Choose which collection to add these bottles to.</small>
                      </h6>

                      <!-- Collection Dropdown -->
                      <div class="row g-3 mb-3">
                        <div class="col-md-12">
                          <label class="form-label text-start">Select Collection</label>
                          <select 
                            class="form-select"
                            v-model="addDrinkForm.selectedCollectionId"
                          >
                            <option v-for="collection in collections" :key="collection.id" :value="collection.id">
                              {{ collection.collectionName }}
                            </option>
                          </select>
                          <small class="text-muted">If no collection is selected, bottles will be added to your General Collection.</small>
                        </div>
                      </div>
                    </div>

                    <!-- Submit Button -->
                    <div class="d-grid">
                      <button 
                        type="submit" 
                        class="btn btn-primary"
                        :disabled="!canAddToCellar || addingToCellar"
                      >
                        <span v-if="addingToCellar" class="spinner-border spinner-border-sm me-2"></span>
                        {{ addingToCellar ? 'Adding...' : 'Add to Cellar' }}
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modals -->
    <!-- Item Details Modal -->
    <div 
      class="modal fade" 
      id="itemDetailsModal" 
      tabindex="-1" 
      aria-labelledby="itemDetailsModalLabel" 
      aria-hidden="true"
    >
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <div class="d-flex justify-content-between align-items-center w-100">
              <div>
                <h5 class="modal-title mb-0" id="itemDetailsModalLabel">
                  {{ selectedGroup?.representative?.listingName || 'Item Details' }}
                  <span v-if="selectedGroup?.representative?.variant" class="text-muted">
                    ({{ selectedGroup.representative.variant }})
                  </span>
                </h5>
              </div>
              <div class="d-flex align-items-center gap-3">
                <div class="collection-selector" v-if="selectedGroup?.representative">
                  <select class="form-select form-select-sm collection-status-select" :value="selectedGroup.representative.collectionId" style="min-width: 220px;">
                    <option v-for="collection in collections" :key="collection.id" :value="collection.id">
                      {{ collection.id === selectedGroup.representative.collectionId ? 'Currently In: ' : 'Move To: ' }}{{ collection.collectionName }}
                    </option>
                  </select>
                </div>
                <button 
                  type="button" 
                  class="btn-close" 
                  data-bs-dismiss="modal" 
                  aria-label="Close"
                ></button>
              </div>
            </div>
          </div>
          <div class="modal-body" v-if="selectedGroup">
            <!-- Header Row: Image + Drink Information -->
            <div class="modal-header-content row mb-4">
              <!-- Left Column - Image -->
              <div class="col-md-3">
                <div class="item-image-container">
                  <img 
                    :src="getItemImageUrl(selectedGroup.representative)"
                    :alt="selectedGroup.representative.listingName"
                    class="item-detail-image"
                    @error="onImageError"
                  >
                </div>
              </div>

              <!-- Right Column - Drink Information Summary -->
              <div class="col-md-9">
                <div class="drink-info-summary">
                  <h6 class="section-header mb-3">Summary of Drink Information</h6>
                  
                  <!-- Row 1: Producer | Bottler | Vintage -->
                  <div class="info-row mb-2">
                    <span class="info-text">
                      <strong>Producer:</strong> <span class="text-muted">{{ selectedGroup.representative.producerName || 'N/A' }}</span>
                      <span v-if="selectedGroup.representative.bottlerName || selectedGroup.representative.producerName" class="mx-2">|</span>
                      <strong>Bottler:</strong> <span class="text-muted">{{ selectedGroup.representative.bottlerName || 'Original Bottling' }}</span>
                      <span v-if="selectedGroup.representative.variant" class="mx-2">|</span>
                      <span v-if="selectedGroup.representative.variant">
                        <strong>Vintage:</strong> <span class="text-muted">{{ selectedGroup.representative.variant }}</span>
                      </span>
                    </span>
                  </div>
                  
                  <!-- Row 2: Country / Type / Category / Style -->
                  <div class="info-row mb-2">
                    <span class="info-text text-muted">
                      <template v-if="selectedGroup.representative.originCountry">{{ selectedGroup.representative.originCountry }}</template>
                      <template v-if="selectedGroup.representative.originCountry && selectedGroup.representative.drinkType"> | </template>
                      <template v-if="selectedGroup.representative.drinkType">{{ selectedGroup.representative.drinkType }}</template>
                      <template v-if="selectedGroup.representative.drinkType && selectedGroup.representative.typeCategory"> | </template>
                      <template v-if="selectedGroup.representative.typeCategory">{{ selectedGroup.representative.typeCategory }}</template>
                      <template v-if="selectedGroup.representative.typeCategory && selectedGroup.representative.drinkStyle"> | </template>
                      <template v-if="selectedGroup.representative.drinkStyle">{{ selectedGroup.representative.drinkStyle }}</template>
                    </span>
                  </div>

                  <!-- Row 3: Drinking Window -->
                  <div class="info-row mb-2" v-if="selectedGroup.representative.drinkOnwardsDate || selectedGroup.representative.drinkByDate">
                    <span class="info-text text-muted">
                      <strong>Drinking Window:&nbsp;</strong>
                      <template v-if="selectedGroup.representative.drinkOnwardsDate"><span class="editable-value">{{ formatDate(selectedGroup.representative.drinkOnwardsDate) }}</span></template>
                      <template v-if="selectedGroup.representative.drinkOnwardsDate && selectedGroup.representative.drinkByDate"> – </template>
                      <template v-if="selectedGroup.representative.drinkByDate"><span class="editable-value">{{ formatDate(selectedGroup.representative.drinkByDate) }}</span></template>
                    </span>
                  </div>

                  <!-- Row 4: Market Value -->
                  <div class="info-row mb-2" v-if="selectedGroup.representative.currentValueEstimation">
                    <span class="info-text text-muted">
                      <strong>Market Value:</strong> <span class="editable-value">{{ selectedGroup.representative.currentValueCurrency || 'USD' }} {{ selectedGroup.representative.currentValueEstimation }}</span>
                    </span>
                  </div>

                  <!-- Row 5: Food Pairing -->
                  <div class="info-row mb-3" v-if="selectedGroup.representative.suggestedFoodPairing">
                    <span class="info-text text-muted">
                      <strong>Suggested Pairing:</strong> <span class="editable-value">{{ selectedGroup.representative.suggestedFoodPairing }}</span>
                    </span>
                  </div>

                  <!-- Row 6: Quantity Owned -->
                  <div class="info-row mb-3">
                    <span class="info-text">
                      <strong>Quantity Owned:</strong> <span class="editable-value">{{ selectedGroup.bottleCount }}</span>
                    </span>
                  </div>
                  
                  <!-- Learn More Button -->
                  <div class="learn-more-section">
                    <button 
                      type="button" 
                      class="btn btn-primary btn-md"
                      data-bs-dismiss="modal"
                      @click="goToListingPage(selectedGroup)"
                    >
                      Learn more about this drink
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Drink Details -->
            <div class="drink-details-section mb-4">
              <h6 class="section-header text-start">Drink Details</h6>
              <div class="row g-3 mb-4">
                <div class="col-md-3">
                  <label class="form-label">Vintage</label>
                  <input type="number" class="form-control" :value="selectedGroup.representative.variant" min="1900" max="2030" readonly>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Format</label>
                  <select class="form-select" :value="selectedGroup.representative.drinkFormat">
                    <option value="Bottle">Bottle</option>
                    <option value="Can">Can</option>
                    <option value="Sample">Sample</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Volume</label>
                  <div class="input-group">
                    <input type="number" class="form-control" :value="selectedGroup.representative.volumeNumber" step="0.1" min="0">
                    <select class="form-select volume-unit-select">
                      <option value="ml" selected>ml</option>
                      <option value="oz">oz</option>
                      <option value="l">L</option>
                    </select>
                  </div>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Current Market Value</label>
                  <div class="input-group">
                    <select class="form-select currency-select" :value="selectedGroup.representative.currentValueCurrency">
                      <option value="USD" selected>USD</option>
                      <option value="EUR">EUR</option>
                      <option value="GBP">GBP</option>
                      <option value="JPY">JPY</option>
                      <option value="CAD">CAD</option>
                      <option value="AUD">AUD</option>
                    </select>
                    <input 
                      type="number" 
                      class="form-control" 
                      :value="selectedGroup.representative.currentValueEstimation"
                      step="0.01" 
                      min="0"
                      placeholder="0.00"
                    >
                  </div>
                </div>
              </div>

              <div class="row g-3 mb-4">
                <div class="col-md-4">
                  <label class="form-label">Drink Onwards Date</label>
                  <div class="input-group">
                    <input 
                      type="text" 
                      class="form-control date-input" 
                      :value="formatDateForInput(selectedGroup.representative.drinkOnwardsDate)"
                      placeholder="MM/DD/YYYY"
                    >
                    <span class="input-group-text">
                      <i class="bi bi-calendar3"></i>
                    </span>
                  </div>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Drink By Date</label>
                  <div class="input-group">
                    <input 
                      type="text" 
                      class="form-control date-input" 
                      :value="formatDateForInput(selectedGroup.representative.drinkByDate)"
                      placeholder="MM/DD/YYYY"
                    >
                    <span class="input-group-text">
                      <i class="bi bi-calendar3"></i>
                    </span>
                  </div>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Suggested Food Pairing</label>
                  <div class="input-group">
                    <select class="form-select" :value="selectedGroup.representative.suggestedFoodPairing">
                      <option value="">Select pairing</option>
                      <option 
                        v-if="selectedGroup.representative.suggestedFoodPairing" 
                        :value="selectedGroup.representative.suggestedFoodPairing"
                        selected
                      >
                        {{ selectedGroup.representative.suggestedFoodPairing }}
                      </option>
                    </select>
                    <button class="btn btn-outline-secondary" type="button">+</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Individual Bottles Management -->
            <div class="individual-bottles-section mb-4">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <div class="d-flex align-items-center">
                  <h6 class="section-header mb-0 me-3">Individual Item Management</h6>
                  <span class="bottle-counter">
                    <i class="bi bi-bottle me-1"></i>
                    {{ selectedGroup.bottleCount }} Item{{ selectedGroup.bottleCount !== 1 ? 's' : '' }} of same label and vintage
                  </span>
                </div>
                <button 
                  class="btn btn-sm btn-outline-primary d-flex align-items-center"
                  @click="addNewBottle"
                  title="Add new bottle to this group"
                >
                  <i class="bi bi-plus-circle me-1"></i>
                  Add Bottle
                </button>
              </div>
              <div class="bottles-list">
                <div 
                  v-for="(bottle, index) in selectedGroup.bottles" 
                  :key="bottle.cellarItemId"
                  class="bottle-item p-4 mb-3 border rounded"
                  :class="{ 'bottle-consumed': bottle.status === 'Consumed' }"

                  style="border-color: #0dcaf0 !important;"
                >
                  <!-- Bottle Header -->
                  <div class="row mb-3">
                    <div class="col-12">
                      <h6 class="mb-1 text-start">
                        <strong>Bottle #{{ index + 1 }}</strong>
                        <small class="text-muted ms-2">Variant Group ID: {{ bottle.variantGroupID }} | Quantity Variant ID: {{ bottle.quantityVariantID }}</small>
                      </h6>
                    </div>
                  </div>

                  <!-- Row 1: Status, Consumption, Location, Sub Location, Notes -->
                  <div class="row g-3 mb-3">
                    <div class="col-md-2">
                      <label class="form-label small">Status</label>
                      <select class="form-select form-select-sm" :value="bottle.status">
                        <option value="In Possession">In Possession</option>
                        <option value="On Its Way">On Its Way</option>
                        <option value="Purchased">Purchased</option>
                        <option value="Held Elsewhere">Held Elsewhere</option>
                        <option value="Wishlisted">Wishlisted</option>
                        <option value="Consumed">Consumed</option>
                      </select>
                    </div>
                    <div class="col-md-2">
                      <label class="form-label small">Consumption</label>
                      <select class="form-select form-select-sm" :value="bottle.consumption">
                        <option value="Unopened">Unopened</option>
                        <option value="Opened">Opened</option>
                        <option value="Empty">Empty</option>
                      </select>
                    </div>
                    <div class="col-md-2">
                      <label class="form-label small">Location</label>
                      <input 
                        type="text" 
                        class="form-control form-control-sm" 
                        :value="bottle.currentLocation" 
                        placeholder="Location"
                      >
                    </div>
                    <div class="col-md-2">
                      <label class="form-label small">Sub Location</label>
                      <input 
                        type="text" 
                        class="form-control form-control-sm" 
                        :value="bottle.subLocation" 
                        placeholder="Sub-location"
                      >
                    </div>
                    <div class="col-md-4">
                      <label class="form-label small">Notes</label>
                      <textarea 
                        class="form-control form-control-sm" 
                        rows="2" 
                        :value="bottle.noteToSelf"
                        placeholder="Add notes for this bottle..."
                      ></textarea>
                    </div>
                  </div>

                  <!-- Row 2: Place of Purchase, Purchase Date, Delivery Date, Price of Purchase -->
                  <div class="row g-3 mb-3">
                    <div class="col-md-3">
                      <label class="form-label small">Place of Purchase</label>
                      <div class="input-group input-group-sm">
                        <input 
                          type="text" 
                          class="form-control" 
                          :value="bottle.purchasePlaceName"
                          placeholder="Enter location"
                        >
                        <span class="input-group-text" title="Google Maps integration coming soon">
                          <i class="bi bi-geo-alt"></i>
                        </span>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <label class="form-label small">Date of Purchase</label>
                      <div class="input-group input-group-sm">
                        <input 
                          type="text" 
                          class="form-control date-input" 
                          :value="formatDateForInput(bottle.purchaseDate)"
                          placeholder="MM/DD/YYYY"
                        >
                        <span class="input-group-text">
                          <i class="bi bi-calendar3"></i>
                        </span>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <label class="form-label small">Delivery Date</label>
                      <div class="input-group input-group-sm">
                        <input 
                          type="text" 
                          class="form-control date-input" 
                          :value="formatDateForInput(bottle.deliveryDate)"
                          placeholder="MM/DD/YYYY"
                        >
                        <span class="input-group-text">
                          <i class="bi bi-calendar3"></i>
                        </span>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <label class="form-label small">Price of Purchase</label>
                      <div class="input-group input-group-sm">
                        <select class="form-select currency-select" :value="bottle.purchaseCurrency">
                          <option value="USD" selected>USD</option>
                          <option value="EUR">EUR</option>
                          <option value="GBP">GBP</option>
                          <option value="JPY">JPY</option>
                          <option value="CAD">CAD</option>
                          <option value="AUD">AUD</option>
                        </select>
                        <input 
                          type="number" 
                          class="form-control" 
                          :value="bottle.purchasePrice"
                          step="0.01" 
                          min="0"
                          placeholder="0.00"
                        >
                      </div>
                    </div>
                  </div>

                  <!-- Archive Button Row -->
                  <div class="row">
                    <div class="col-12 text-center">
                      <button 
                        type="button" 
                        class="btn btn-danger btn-sm"
                        @click="archiveBottle(bottle.cellarItemId)"
                        title="Archive this item"
                      >
                        <i class="bi bi-archive me-1"></i>
                        Archive Item
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <div class="d-flex justify-content-between align-items-center w-100">
              <!-- Left side: Group actions -->
              <div class="action-buttons">
                <div class="dropdown">
                  <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                    <i class="bi bi-three-dots"></i> Group Actions
                  </button>
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#" @click="consumeBottle('one')">
                      <i class="bi bi-cup"></i> Consume One Bottle
                    </a></li>
                    <li><a class="dropdown-item" href="#" @click="moveGroup">
                      <i class="bi bi-arrow-left-right"></i> Move Group
                    </a></li>
                    <li><a class="dropdown-item" href="#" @click="duplicateGroup">
                      <i class="bi bi-files"></i> Duplicate Group
                    </a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item text-danger" href="#" @click="deleteGroup">
                      <i class="bi bi-trash"></i> Delete All Bottles
                    </a></li>
                  </ul>
                </div>
              </div>

              <!-- Right side: Close and Save -->
              <div class="close-save-buttons">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-primary" @click="saveGroupChanges">
                  <i class="bi bi-check-lg"></i> Save Changes
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Collection Modal (Stub) -->
    <div 
      class="modal fade" 
      id="addCollectionModal" 
      tabindex="-1" 
      aria-labelledby="addCollectionModalLabel" 
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addCollectionModalLabel">Add New Collection</h5>
            <button 
              type="button" 
              class="btn-close" 
              data-bs-dismiss="modal" 
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="text-center py-4">
              <i class="bi bi-collection" style="font-size: 3rem; color: #6c757d;"></i>
              <h4 class="mt-3">Collection Management - Coming Next</h4>
              <p class="text-muted">
                Create and organize custom collections for your cellar items.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

</template>

<script>
import NavBar from '@/components/NavBar.vue'
// import { useToast } from "vue-toastification";

export default {
  name: 'myCellar',
  components: {
    NavBar
  },
  props: {
    ownerType: {
      type: String,
      required: true,
      validator: value => ['user', 'producer', 'venue'].includes(value)
    },
    id: {
      type: String,
      required: true
    },
    username: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      // Data loading states
      loading: true,
      error: null,
      
      // Tabs and collections
      activeTab: 'all',
      collections: [],
      
      // Items and filtering
      allItems: [],
      searchQuery: '',
      filters: {
        vintage: '',
        size: '',
        status: '',
        drinkNow: false
      },
      
      // Pagination
      currentPage: 1,
      itemsPerPage: 24,
      
      // Modal states
      selectedGroup: null,
      
      // Dashboard data
      dashboardData: null,
      
      // Search debouncing
      searchTimeout: null,

      // Add drink to cellar form
      addDrinkForm: {
        // Producer search
        producerSearchQuery: '',
        producerSearchResults: [],
        selectedProducer: {},
        producerDebounceTimer: null,
        
        // Drink search
        searchQuery: '',
        searchResults: [],
        selectedDrink: {},
        drinkDebounceTimer: null,
        
        // Group properties (applied to all items in the drink group)
        vintage: null,
        format: 'Bottle',
        volumeNumber: 750,
        volumeUnit: 'ml',
        currentValueEstimation: null,
        currentValueCurrency: 'USD',
        drinkOnwardsDate: null,
        drinkByDate: null,
        suggestedFoodPairing: '',
        
        // Individual item properties (applied to each bottle)
        quantity: 1,
        status: 'In Possession',
        consumption: 'Unopened',
        currentLocation: 'At Home',
        subLocation: '',
        purchasePlaceName: '',
        
        // Purchase location with Google Maps integration
        purchaseLocationInputValue: '', // Input field value for Google Maps autocomplete
        selectedPurchasePlace: '', // Name from Google Maps (for purchasePlaceName)
        selectedPurchaseAddress: '', // Address from Google Maps (for purchaseAddress)
        selectedPurchaseVenueId: null, // Optional venue ID if applicable
        
        purchaseDate: null,
        deliveryDate: null,
        purchasePrice: null,
        purchaseCurrency: 'USD',
        personalNotes: '',
        
        // Collection selection
        selectedCollectionId: null
      },
      
      // Add to cellar state
      addingToCellar: false,
      
      // Debug tracking
      lastCanAddToCellarState: null
    }
  },
  computed: {
    // Total item count for the active tab
    totalItemCount() {
      if (this.activeTab === 'all') {
        return this.allItems.length
      }
      const collection = this.collections.find(c => c.id === this.activeTab)
      return collection ? collection.itemCount : 0
    },
    
    // Get items for active tab/collection
    tabItems() {
      if (this.activeTab === 'all') {
        return this.allItems
      }
      return this.allItems.filter(item => item.collectionId === this.activeTab)
    },
    
    // Group items by listing + variant + format + volume for display
    groupedItems() {
      const groups = {}
      
      this.tabItems.forEach(item => {
        // Use variantGroupID for grouping - items with the same variantGroupID belong together
        const groupKey = item.variantGroupID || `standalone_${item.cellarItemId}`
        
        // Debug logging for grouping
        if (this.activeTab === 'all' && this.tabItems.length < 20) { // Only log when not too many items
          console.log(`TZHFrontendLog: Grouping item ${item.cellarItemId} with variantGroupID: ${item.variantGroupID}`);
          console.log(`TZHFrontendLog:   - Using groupKey: ${groupKey}`);
        }
        
        if (!groups[groupKey]) {
          groups[groupKey] = {
            // Use first item as representative for display
            representative: item,
            // Track all individual bottles in this group
            bottles: [],
            // Count of bottles in this group
            bottleCount: 0,
            // Group identification
            variantGroupID: item.variantGroupID,
            listingId: item.listingId,
            variant: item.variant,
            drinkFormat: item.drinkFormat,
            volumeNumber: item.volumeNumber,
            volumeUnit: item.volumeUnit,
            listingName: item.listingName
          }
        }
        
        groups[groupKey].bottles.push(item)
        groups[groupKey].bottleCount = groups[groupKey].bottles.length
      })
      
      return Object.values(groups)
    },
    
    // Apply search and filters to grouped items
    filteredItems() {
      let groups = this.groupedItems
      
      // Search filter - search within the representative item
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase()
        groups = groups.filter(group => 
          group.representative.listingName.toLowerCase().includes(query) ||
          (group.representative.producerName && group.representative.producerName.toLowerCase().includes(query))
        )
      }
      
      // Vintage filter
      if (this.filters.vintage) {
        groups = groups.filter(group => group.representative.variant == this.filters.vintage)
      }
      
      // Size filter
      if (this.filters.size) {
        groups = groups.filter(group => group.representative.volumeNumber == this.filters.size)
      }
      
      // Status filter - check if any bottle in the group matches
      if (this.filters.status) {
        groups = groups.filter(group => 
          group.bottles.some(bottle => bottle.status === this.filters.status)
        )
      }
      
      // Drink now filter - check if any bottle in the group is ready to drink
      if (this.filters.drinkNow) {
        const today = new Date()
        groups = groups.filter(group => {
          return group.bottles.some(bottle => {
            if (!bottle.drinkOnwardsDate && !bottle.drinkByDate) return false
            
            const drinkFrom = bottle.drinkOnwardsDate ? new Date(bottle.drinkOnwardsDate) : null
            const drinkBy = bottle.drinkByDate ? new Date(bottle.drinkByDate) : null
            
            const afterDrinkFrom = !drinkFrom || today >= drinkFrom
            const beforeDrinkBy = !drinkBy || today <= drinkBy
            
            return afterDrinkFrom && beforeDrinkBy
          })
        })
      }
      
      return groups
    },
    
    // Pagination calculations
    totalPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage)
    },
    
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredItems.slice(start, end)
    },
    
    visiblePages() {
      const pages = []
      const maxVisible = 5
      let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2))
      let end = Math.min(this.totalPages, start + maxVisible - 1)
      
      if (end - start + 1 < maxVisible) {
        start = Math.max(1, end - maxVisible + 1)
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    },
    
    // Vintage options for filter dropdown
    vintageOptions() {
      const vintages = new Set()
      this.allItems.forEach(item => {
        if (item.variant) {
          vintages.add(item.variant)
        }
      })
      return Array.from(vintages).sort((a, b) => b - a)
    },

    // Form validation for add to cellar
    canAddToCellar() {
      const hasSelectedDrink = this.addDrinkForm.selectedDrink && this.addDrinkForm.selectedDrink.id;
      const hasValidQuantity = this.addDrinkForm.quantity > 0;
      return hasSelectedDrink && hasValidQuantity;
    }
  },
  watch: {
    // Watch route params for changes
    '$route'(to, from) {
      if (to.params.ownerType !== from.params.ownerType || 
          to.params.id !== from.params.id) {
        this.loadCellarData()
      }
    },
    
    // Reset pagination when filters change
    'filters': {
      handler() {
        this.currentPage = 1
      },
      deep: true
    },
    
    searchQuery() {
      this.currentPage = 1
    },
    
    // Watch canAddToCellar for debug logging
    canAddToCellar(newValue, oldValue) {
      if (newValue !== oldValue) {
        const hasSelectedDrink = this.addDrinkForm.selectedDrink && this.addDrinkForm.selectedDrink.id;
        const hasValidQuantity = this.addDrinkForm.quantity > 0;
        
        console.log('TZHFrontendLog: canAddToCellar validation state changed:');
        console.log('TZHFrontendLog:   hasSelectedDrink:', hasSelectedDrink);
        console.log('TZHFrontendLog:   selectedDrink.id:', this.addDrinkForm.selectedDrink?.id);
        console.log('TZHFrontendLog:   hasValidQuantity:', hasValidQuantity);
        console.log('TZHFrontendLog:   quantity:', this.addDrinkForm.quantity);
        console.log('TZHFrontendLog:   canAddToCellar result:', newValue);
        
        this.lastCanAddToCellarState = newValue;
      }
    }
  },
  async mounted() {
    await this.loadCellarData()
  },
  beforeUnmount() {
    // Cancel any pending search timeout
    if (this.searchTimeout) {
      clearTimeout(this.searchTimeout)
    }
    
    // Cancel any pending add drink form timers
    if (this.addDrinkForm.producerDebounceTimer) {
      clearTimeout(this.addDrinkForm.producerDebounceTimer)
    }
    
    if (this.addDrinkForm.drinkDebounceTimer) {
      clearTimeout(this.addDrinkForm.drinkDebounceTimer)
    }
  },
  methods: {
    // Data loading
    async loadCellarData() {
      this.loading = true
      this.error = null
      
      try {
        // Load dashboard and items data in parallel
        const [dashboardResponse, itemsResponse] = await Promise.all([
          this.fetchCellarDashboard(),
          this.fetchCellarItems()
        ])
        
        this.dashboardData = dashboardResponse.data || dashboardResponse
        this.allItems = itemsResponse.data?.items || itemsResponse.items || []
        this.collections = itemsResponse.data?.collections || itemsResponse.collections || []
        
        // Set default collection for add drink form if not already set
        if (this.collections.length > 0 && !this.addDrinkForm.selectedCollectionId) {
          const defaultCollection = this.collections.find(c => c.isDefault)
          if (defaultCollection) {
            this.addDrinkForm.selectedCollectionId = defaultCollection.id
          } else {
            // If no default collection found, use the first one
            this.addDrinkForm.selectedCollectionId = this.collections[0].id
          }
        }
        
        // Debug: log first item to see what properties are available
        if (this.allItems.length > 0) {
          console.log('Sample cellar item data:', this.allItems[0]);
          console.log('Available fields in first item:', Object.keys(this.allItems[0]));
          console.log('drinkStyle field:', this.allItems[0].drinkStyle);
          console.log('typeCategory field:', this.allItems[0].typeCategory);
          console.log('drinkType field:', this.allItems[0].drinkType);
          console.log('variantGroupID field:', this.allItems[0].variantGroupID);
        }
        
      } catch (error) {
        console.error('Error loading cellar data:', error)
        this.error = error.message || 'Failed to load cellar data'
      } finally {
        this.loading = false
      }
    },
    
    async fetchCellarDashboard() {
      // Use full URL for development since proxy doesn't handle /getData
      const baseUrl = process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '';
      const response = await this.$axios.get(`${baseUrl}/getData/getCellarDashboard/${this.ownerType}/${this.id}`)
      return response.data
    },
    
    async fetchCellarItems() {
      // Use full URL for development since proxy doesn't handle /getData
      const baseUrl = process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '';
      const params = new URLSearchParams()
      if (this.activeTab !== 'all') {
        params.append('collectionId', this.activeTab)
      }
      
      const response = await this.$axios.get(`${baseUrl}/getData/getCellarData/${this.ownerType}/${this.id}?${params}`)
      return response.data
    },
    
    // Tab management
    setActiveTab(tabId) {
      this.activeTab = tabId
      this.currentPage = 1
      // TODO: Fetch filtered data if needed
    },
    
    // Filter management
    debouncedSearch() {
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout)
      }
      this.searchTimeout = setTimeout(() => {
        // Search is handled by computed property
        // This debouncing prevents excessive filtering during typing
      }, 300)
    },
    
    clearFilters() {
      this.searchQuery = ''
      this.filters = {
        vintage: '',
        size: '',
        status: '',
        drinkNow: false
      }
      this.currentPage = 1
    },
    
    // Pagination
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        // Scroll to top of items grid
        this.$nextTick(() => {
          document.querySelector('.items-grid')?.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
          })
        })
      }
    },
    
    
    // Modal management  
    setSelectedGroup(group) {
      this.selectedGroup = group
    },

    // Get status breakdown for a group
    getGroupStatusBreakdown(items) {
      const breakdown = {}
      items.forEach(item => {
        const status = item.consumption || 'Unopened'
        breakdown[status] = (breakdown[status] || 0) + 1
      })
      return breakdown
    },

    // Navigate to listing page
    goToListingPage(group) {
      if (group.listingId && group.representative.listingName) {
        // Small delay to allow modal dismiss to complete
        setTimeout(() => {
          const listingName = group.representative.listingName.replace(/[^a-zA-Z0-9\s-]/g, '').replace(/\s+/g, '-').toLowerCase()
          this.$router.push(`/listing/view/${group.listingId}/${listingName}`)
        }, 150)
      }
    },

    // Group actions
    consumeBottle(type = 'one') {
      console.log('Consume bottle from group:', this.selectedGroup, 'type:', type)
      // TODO: Implement consume functionality for individual bottles
    },

    moveGroup() {
      console.log('Move group:', this.selectedGroup)
      // TODO: Implement move functionality for entire group
    },

    duplicateGroup() {
      console.log('Duplicate group:', this.selectedGroup)
      // TODO: Implement duplicate functionality for entire group
    },

    deleteGroup() {
      console.log('Delete group:', this.selectedGroup)
      // TODO: Implement delete functionality for entire group
    },

    saveGroupChanges() {
      console.log('Save group changes:', this.selectedGroup)
      // TODO: Implement save functionality for group updates
    },

    // Individual bottle management
    editIndividualBottle(bottle) {
      console.log('Edit individual bottle:', bottle)
      // TODO: Implement individual bottle editing
    },

    addNewBottle() {
      if (!this.selectedGroup) return
      
      console.log('Adding new bottle to group:', this.selectedGroup)
      
      // Create a new bottle object with default values
      const newBottle = {
        // Generate a temporary ID (in real implementation, this would come from backend)
        cellarItemId: `temp_${Date.now()}`,
        quantityVariantID: `temp_variant_${Date.now()}`,
        variantGroupID: this.selectedGroup.variantGroupID, // Inherit the group's variantGroupID
        listingId: this.selectedGroup.listingId,
        variant: this.selectedGroup.variant,
        
        // Default status values
        status: 'In Possession',
        consumption: 'Unopened',
        currentLocation: 'At Home',
        subLocation: '',
        noteToSelf: '',
        
        // Copy shared properties from representative bottle
        drinkFormat: this.selectedGroup.representative.drinkFormat,
        volumeNumber: this.selectedGroup.representative.volumeNumber,
        
        // Default procurement details
        purchaseDate: null,
        deliveryDate: null,
        purchasePlaceName: '',
        purchasePrice: null,
        purchaseCurrency: 'USD'
      }
      
      // Add to the group's bottles array
      this.selectedGroup.bottles.push(newBottle)
      
      // Update bottle count
      this.selectedGroup.bottleCount = this.selectedGroup.bottles.length
      
      // TODO: In real implementation, this would make an API call to create the bottle in the backend
    },

    updateBottleStatus(bottle, newStatus) {
      console.log('Update bottle status:', bottle, 'to:', newStatus)
      // TODO: Update individual bottle status
    },

    updateBottleConsumption(bottle, newConsumption) {
      console.log('Update bottle consumption:', bottle, 'to:', newConsumption)
      // TODO: Update individual bottle consumption status
    },

    updateBottleLocation(bottle, newLocation) {
      console.log('Update bottle location:', bottle, 'to:', newLocation)
      // TODO: Update individual bottle location
    },    // Utility methods
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      
      // Get day with ordinal suffix
      const day = date.getDate()
      const ordinalSuffix = this.getOrdinalSuffix(day)
      
      // Get month name and year
      const month = date.toLocaleDateString('en-US', { month: 'short' })
      const year = date.getFullYear()
      
      return `${day}${ordinalSuffix} ${month} ${year}`
    },
    
    getOrdinalSuffix(day) {
      if (day >= 11 && day <= 13) {
        return 'th'
      }
      switch (day % 10) {
        case 1: return 'st'
        case 2: return 'nd'
        case 3: return 'rd'
        default: return 'th'
      }
    },
    
    formatDateForInput(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      if (isNaN(date.getTime())) return ''
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit' 
      })
    },
    
    getStatusBadgeClass(status) {
      const statusClasses = {
        'In Possession': 'bg-success',
        'On Its Way': 'bg-info',
        'Wishlisted': 'bg-warning',
        'Consumed': 'bg-secondary',
        'Held Elsewhere': 'bg-primary'
      }
      return statusClasses[status] || 'bg-secondary'
    },
    
    onImageError(event) {
      event.target.src = 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739'
    },
    
    // Get the proper image URL for a cellar item or group
    getItemImageUrl(itemOrGroup) {
      const baseUrl = process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '';
      
      // For grouped items, use the representative item's photo
      const item = itemOrGroup.representative || itemOrGroup;
      
      // Try different possible photo properties from the API response
      const photoPath = item.drinkPhoto || item.photo || item.listingPhoto;
      
      if (photoPath) {
        // If it's already a full URL, use it as-is
        if (photoPath.startsWith('http')) {
          return photoPath;
        }
        // Otherwise, prepend the backend base URL
        return `${baseUrl}${photoPath.startsWith('/') ? '' : '/'}${photoPath}`;
      }
      
      // Fallback to default image
      return 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739';
    },

    // Get preview image URL for selected drink in add form
    getPreviewImageUrl(drink) {
      const baseUrl = process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '';
      
      // Try different possible photo properties from the API response
      const photoPath = drink.photo || drink.drinkPhoto || drink.listingPhoto;
      
      if (photoPath) {
        // If it's already a full URL, use it as-is
        if (photoPath.startsWith('http')) {
          return photoPath;
        }
        // Otherwise, prepend the backend base URL
        return `${baseUrl}${photoPath.startsWith('/') ? '' : '/'}${photoPath}`;
      }
      
      // Fallback to default image
      return 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739';
    },

    // Add to cellar functionality
    // Debounced producer search
    debouncedSearchProducers() {
      // Clear previous timeout
      if (this.addDrinkForm.producerDebounceTimer) {
        clearTimeout(this.addDrinkForm.producerDebounceTimer);
      }

      // Set new timeout
      this.addDrinkForm.producerDebounceTimer = setTimeout(() => {
        this.searchProducers();
      }, 300);
    },

    // Search producers API call
    async searchProducers() {
      if (!this.addDrinkForm.producerSearchQuery || this.addDrinkForm.producerSearchQuery.trim().length < 2) {
        this.addDrinkForm.producerSearchResults = [];
        return;
      }

      try {
        const baseUrl = process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '';
        const response = await this.$axios.get(`${baseUrl}/getData/getProducerNamesDynamicSearch/${this.addDrinkForm.producerSearchQuery}`);

        if (response.status === 200) {
          this.addDrinkForm.producerSearchResults = response.data.slice(0, 10); // Limit to 10 results
        }
      } catch (error) {
        console.error('Error searching producers:', error);
        this.addDrinkForm.producerSearchResults = [];
      }
    },

    // Select producer
    selectProducer(producer) {
      console.log('TZHFrontendLog: selectProducer called with producer:', JSON.stringify(producer, null, 2));
      this.addDrinkForm.selectedProducer = producer;
      this.addDrinkForm.producerSearchQuery = producer.producerName;
      this.addDrinkForm.producerSearchResults = [];
      
      // Reset drink search when producer changes
      console.log('TZHFrontendLog: Resetting drink search due to producer change');
      this.addDrinkForm.searchQuery = '';
      this.addDrinkForm.searchResults = [];
      this.addDrinkForm.selectedDrink = {};
      console.log('TZHFrontendLog: Updated selectedProducer:', JSON.stringify(this.addDrinkForm.selectedProducer, null, 2));
    },

    // Clear selected producer
    clearSelectedProducer() {
      this.addDrinkForm.selectedProducer = {};
      this.addDrinkForm.producerSearchQuery = '';
      this.addDrinkForm.producerSearchResults = [];
      
      // Reset drink search
      this.addDrinkForm.searchQuery = '';
      this.addDrinkForm.searchResults = [];
      this.addDrinkForm.selectedDrink = {};
    },

    // Debounced drink search
    debouncedSearchDrinks() {
      // Clear previous timeout
      if (this.addDrinkForm.drinkDebounceTimer) {
        clearTimeout(this.addDrinkForm.drinkDebounceTimer);
      }

      // Set new timeout
      this.addDrinkForm.drinkDebounceTimer = setTimeout(() => {
        this.searchDrinks();
      }, 300);
    },

    // Search drinks API call
    async searchDrinks() {
      console.log('TZHFrontendLog: searchDrinks called with query:', this.addDrinkForm.searchQuery);
      console.log('TZHFrontendLog: Selected producer for filtering:', JSON.stringify(this.addDrinkForm.selectedProducer, null, 2));
      
      if (!this.addDrinkForm.searchQuery || this.addDrinkForm.searchQuery.trim().length < 2) {
        console.log('TZHFrontendLog: Search query too short, clearing results');
        this.addDrinkForm.searchResults = [];
        return;
      }

      try {
        const baseUrl = process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '';
        let response;
        let searchUrl;
        
        // If a producer is selected, search only within that producer's listings
        if (this.addDrinkForm.selectedProducer && this.addDrinkForm.selectedProducer.id) {
          searchUrl = `${baseUrl}/getData/getListingNamesByProducer/${this.addDrinkForm.searchQuery}/${this.addDrinkForm.selectedProducer.id}`;
          console.log('TZHFrontendLog: Searching drinks by producer with URL:', searchUrl);
          response = await this.$axios.get(searchUrl);
        } else {
          // Otherwise, search all listings
          searchUrl = `${baseUrl}/getData/getListingNamesDynamicSearch/${this.addDrinkForm.searchQuery}`;
          console.log('TZHFrontendLog: Searching all drinks with URL:', searchUrl);
          response = await this.$axios.get(searchUrl);
        }

        console.log('TZHFrontendLog: Drink search response status:', response.status);
        console.log('TZHFrontendLog: Drink search response data length:', response.data ? response.data.length : 'no data');
        
        if (response.status === 200) {
          this.addDrinkForm.searchResults = response.data.slice(0, 10); // Limit to 10 results
          console.log('TZHFrontendLog: Updated search results:', JSON.stringify(this.addDrinkForm.searchResults, null, 2));
        }
      } catch (error) {
        console.error('TZHFrontendLog: Error searching drinks:', error);
        this.addDrinkForm.searchResults = [];
      }
    },

    // Select drink
    selectDrink(listing) {
      console.log('TZHFrontendLog: selectDrink called with listing:', JSON.stringify(listing, null, 2));
      this.addDrinkForm.selectedDrink = listing;
      this.addDrinkForm.searchQuery = listing.listingName;
      this.addDrinkForm.searchResults = [];
      console.log('TZHFrontendLog: Updated addDrinkForm.selectedDrink:', JSON.stringify(this.addDrinkForm.selectedDrink, null, 2));
      console.log('TZHFrontendLog: canAddToCellar after selection:', this.canAddToCellar);
    },

    // ============ Purchase Location Google Maps Methods ============
    
    // Handle place selection from Google Maps autocomplete for purchase location
    setPurchasePlaceFromAutocomplete(place) {
      console.log('TZHFrontendLog: setPurchasePlaceFromAutocomplete called with place:', place);
      
      if (place && place.geometry) {
        this.addDrinkForm.selectedPurchasePlace = place.name || place.formatted_address;
        this.addDrinkForm.selectedPurchaseAddress = place.formatted_address;
        this.addDrinkForm.purchaseLocationInputValue = this.addDrinkForm.selectedPurchasePlace;
        
        // Set purchasePlaceName for backend compatibility
        this.addDrinkForm.purchasePlaceName = this.addDrinkForm.selectedPurchasePlace;
        
        // Check if this is a known venue (optional - for future use)
        this.addDrinkForm.selectedPurchaseVenueId = this.checkVenueIfExists(place);
        
        console.log('TZHFrontendLog: Purchase location selected:', {
          place: this.addDrinkForm.selectedPurchasePlace,
          address: this.addDrinkForm.selectedPurchaseAddress,
          venueId: this.addDrinkForm.selectedPurchaseVenueId
        });
      }
    },

    // Handle input changes for purchase location
    onPurchaseLocationInput(event) {
      // Handle both string values and event objects
      const inputValue = typeof event === 'string' ? event : event.target.value;
      this.addDrinkForm.purchaseLocationInputValue = inputValue;
      
      // If user is typing manually (not from autocomplete), clear the selection
      if (inputValue !== this.addDrinkForm.selectedPurchasePlace) {
        this.addDrinkForm.selectedPurchasePlace = '';
        this.addDrinkForm.selectedPurchaseAddress = '';
        this.addDrinkForm.selectedPurchaseVenueId = null;
        
        // Set manual entry as purchasePlaceName (only if inputValue is not empty)
        this.addDrinkForm.purchasePlaceName = inputValue ? inputValue.trim() : '';
      }
    },

    // Handle focus on purchase location input
    onPurchaseLocationFocus() {
      // Could be used for future enhancements like showing recent places
      console.log('TZHFrontendLog: Purchase location input focused');
    },

    // Handle blur on purchase location input
    onPurchaseLocationBlur() {
      // Ensure manual entry is captured
      if (this.addDrinkForm.purchaseLocationInputValue && !this.addDrinkForm.selectedPurchasePlace) {
        this.addDrinkForm.purchasePlaceName = this.addDrinkForm.purchaseLocationInputValue.trim();
        console.log('TZHFrontendLog: Manual purchase location entry captured:', this.addDrinkForm.purchasePlaceName);
      }
    },

    // Clear selected purchase location
    clearSelectedPurchaseLocation() {
      this.addDrinkForm.selectedPurchasePlace = '';
      this.addDrinkForm.selectedPurchaseAddress = '';
      this.addDrinkForm.selectedPurchaseVenueId = null;
      this.addDrinkForm.purchaseLocationInputValue = '';
      this.addDrinkForm.purchasePlaceName = '';
      
      console.log('TZHFrontendLog: Purchase location cleared');
    },

    // Check if place exists as a venue (optional functionality)
    checkVenueIfExists(_place) {
      // This would check against a venues database in the future
      // Parameter _place would be used to lookup venue by place.place_id or place.name
      // For now, return null since venue ID is optional
      console.log('TZHFrontendLog: checkVenueIfExists called with place:', _place?.name || 'unknown');
      return null;
    },

    // ============ End Purchase Location Methods ============

    // Add drink to cellar
    async addDrinkToCellar() {
      console.log('TZHFrontendLog: ===========================================');
      console.log('TZHFrontendLog: Starting addDrinkToCellar process');
      console.log('TZHFrontendLog: Form validation check - canAddToCellar:', this.canAddToCellar);
      console.log('TZHFrontendLog: Selected drink:', JSON.stringify(this.addDrinkForm.selectedDrink, null, 2));
      console.log('TZHFrontendLog: Current form state:', JSON.stringify(this.addDrinkForm, null, 2));
      
      if (!this.canAddToCellar) {
        console.log('TZHFrontendLog: Form validation failed - cannot add to cellar');
        return;
      }

      this.addingToCellar = true;
      console.log('TZHFrontendLog: Set addingToCellar flag to true');

      try {
        console.log('TZHFrontendLog: Starting data preparation...');
        
        // Log each form field before processing
        console.log('TZHFrontendLog: Raw form fields:');
        console.log('TZHFrontendLog:   - selectedDrink.id:', this.addDrinkForm.selectedDrink.id);
        console.log('TZHFrontendLog:   - ownerType:', this.ownerType);
        console.log('TZHFrontendLog:   - ownerId:', this.id);
        console.log('TZHFrontendLog:   - quantity:', this.addDrinkForm.quantity);
        console.log('TZHFrontendLog:   - format:', this.addDrinkForm.format);
        console.log('TZHFrontendLog:   - volumeNumber:', this.addDrinkForm.volumeNumber);
        console.log('TZHFrontendLog:   - volumeUnit:', this.addDrinkForm.volumeUnit);
        console.log('TZHFrontendLog:   - vintage:', this.addDrinkForm.vintage);
        console.log('TZHFrontendLog:   - currentValueEstimation:', this.addDrinkForm.currentValueEstimation);
        console.log('TZHFrontendLog:   - currentValueCurrency:', this.addDrinkForm.currentValueCurrency);
        console.log('TZHFrontendLog:   - drinkOnwardsDate:', this.addDrinkForm.drinkOnwardsDate);
        console.log('TZHFrontendLog:   - drinkByDate:', this.addDrinkForm.drinkByDate);
        console.log('TZHFrontendLog:   - suggestedFoodPairing:', this.addDrinkForm.suggestedFoodPairing);
        console.log('TZHFrontendLog:   - status:', this.addDrinkForm.status);
        console.log('TZHFrontendLog:   - consumption:', this.addDrinkForm.consumption);
        console.log('TZHFrontendLog:   - currentLocation:', this.addDrinkForm.currentLocation);
        console.log('TZHFrontendLog:   - subLocation:', this.addDrinkForm.subLocation);
        console.log('TZHFrontendLog:   - purchasePlaceName:', this.addDrinkForm.purchasePlaceName);
        console.log('TZHFrontendLog:   - selectedPurchasePlace:', this.addDrinkForm.selectedPurchasePlace);
        console.log('TZHFrontendLog:   - selectedPurchaseAddress:', this.addDrinkForm.selectedPurchaseAddress);
        console.log('TZHFrontendLog:   - selectedPurchaseVenueId:', this.addDrinkForm.selectedPurchaseVenueId);
        console.log('TZHFrontendLog:   - purchaseLocationInputValue:', this.addDrinkForm.purchaseLocationInputValue);
        console.log('TZHFrontendLog:   - purchaseDate:', this.addDrinkForm.purchaseDate);
        console.log('TZHFrontendLog:   - deliveryDate:', this.addDrinkForm.deliveryDate);
        console.log('TZHFrontendLog:   - purchasePrice:', this.addDrinkForm.purchasePrice);
        console.log('TZHFrontendLog:   - purchaseCurrency:', this.addDrinkForm.purchaseCurrency);
        console.log('TZHFrontendLog:   - personalNotes:', this.addDrinkForm.personalNotes);
        console.log('TZHFrontendLog:   - selectedCollectionId:', this.addDrinkForm.selectedCollectionId);

        // Prepare cellar item data according to backend API specification
        const cellarData = {
          // Required fields
          listingId: this.addDrinkForm.selectedDrink.id,
          ownerType: this.ownerType,
          ownerId: parseInt(this.id),
          quantity: parseInt(this.addDrinkForm.quantity),
          
          // Group properties (master record) - only sent if they have values
          ...(this.addDrinkForm.format && { format: this.addDrinkForm.format }),
          ...(this.addDrinkForm.volumeNumber && { volumeNumber: parseFloat(this.addDrinkForm.volumeNumber) }),
          ...(this.addDrinkForm.volumeUnit && { volumeUnit: this.addDrinkForm.volumeUnit }),
          ...(this.addDrinkForm.currentValueEstimation && { currentValueEstimation: parseFloat(this.addDrinkForm.currentValueEstimation) }),
          ...(this.addDrinkForm.currentValueCurrency && { currentValueCurrency: this.addDrinkForm.currentValueCurrency }),
          ...(this.addDrinkForm.drinkOnwardsDate && { drinkOnwardsDate: this.addDrinkForm.drinkOnwardsDate }),
          ...(this.addDrinkForm.drinkByDate && { drinkByDate: this.addDrinkForm.drinkByDate }),
          ...(this.addDrinkForm.suggestedFoodPairing && this.addDrinkForm.suggestedFoodPairing.trim() && { suggestedFoodPairing: this.addDrinkForm.suggestedFoodPairing.trim() }),
          ...(this.addDrinkForm.vintage && { variant: parseInt(this.addDrinkForm.vintage) }),
          
          // Individual properties (applied to each bottle)
          ...(this.addDrinkForm.status && { status: this.addDrinkForm.status }),
          ...(this.addDrinkForm.consumption && { consumption: this.addDrinkForm.consumption }),
          ...(this.addDrinkForm.currentLocation && this.addDrinkForm.currentLocation.trim() && { currentLocation: this.addDrinkForm.currentLocation.trim() }),
          ...(this.addDrinkForm.subLocation && this.addDrinkForm.subLocation.trim() && { subLocation: this.addDrinkForm.subLocation.trim() }),
          
          // Purchase location data (Google Maps integration)
          ...(this.addDrinkForm.purchasePlaceName && this.addDrinkForm.purchasePlaceName.trim() && { purchasePlaceName: this.addDrinkForm.purchasePlaceName.trim() }),
          ...(this.addDrinkForm.selectedPurchaseAddress && this.addDrinkForm.selectedPurchaseAddress.trim() && { purchaseAddress: this.addDrinkForm.selectedPurchaseAddress.trim() }),
          ...(this.addDrinkForm.selectedPurchaseVenueId && { purchaseVenueId: parseInt(this.addDrinkForm.selectedPurchaseVenueId) }),
          
          ...(this.addDrinkForm.purchaseDate && { purchaseDate: this.addDrinkForm.purchaseDate }),
          ...(this.addDrinkForm.deliveryDate && { deliveryDate: this.addDrinkForm.deliveryDate }),
          ...(this.addDrinkForm.purchasePrice && { purchasePrice: parseFloat(this.addDrinkForm.purchasePrice) }),
          ...(this.addDrinkForm.purchaseCurrency && { purchaseCurrency: this.addDrinkForm.purchaseCurrency }),
          ...(this.addDrinkForm.personalNotes && this.addDrinkForm.personalNotes.trim() && { personalNotes: this.addDrinkForm.personalNotes.trim() }),
          
          // Collection selection (optional, will use default if not provided)
          ...(this.addDrinkForm.selectedCollectionId && { collectionId: parseInt(this.addDrinkForm.selectedCollectionId) })
        };

        console.log('TZHFrontendLog: Prepared cellar data payload:', JSON.stringify(cellarData, null, 2));
        console.log('TZHFrontendLog: Payload size:', JSON.stringify(cellarData).length, 'characters');
        console.log('TZHFrontendLog: Number of fields in payload:', Object.keys(cellarData).length);

        // Call the actual API endpoint
        const baseUrl = process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '';
        const fullUrl = `${baseUrl}/editCellar/addToCellar`;
        console.log('TZHFrontendLog: Making API call to:', fullUrl);
        console.log('TZHFrontendLog: Request headers will include axios defaults');
        
        const response = await this.$axios.post(fullUrl, cellarData);

        console.log('TZHFrontendLog: API call completed');
        console.log('TZHFrontendLog: Response status:', response.status);
        console.log('TZHFrontendLog: Response headers:', JSON.stringify(response.headers, null, 2));
        console.log('TZHFrontendLog: Response data:', JSON.stringify(response.data, null, 2));

        if (response.status === 201 && response.data.code === 201) {
          console.log('TZHFrontendLog: Success response received');
          console.log('TZHFrontendLog: Master ID created:', response.data.data.masterId);
          console.log('TZHFrontendLog: Bottle IDs created:', response.data.data.bottleIds);
          console.log('TZHFrontendLog: Collection ID used:', response.data.data.collectionId);
          console.log('TZHFrontendLog: Number of bottles added:', response.data.data.quantity);
          
          // Success! Reset form and reload data
          console.log('TZHFrontendLog: Resetting form...');
          this.resetAddDrinkForm();
          
          // Reload cellar data to show the new item
          console.log('TZHFrontendLog: Reloading cellar data...');
          await this.loadCellarData();
          console.log('TZHFrontendLog: Cellar data reloaded successfully');
          
          // Show success message
          console.log('TZHFrontendLog: Process completed successfully!', response.data);
          
          // Optional: You can add a toast notification here
          // this.$toast.success(`Successfully added ${response.data.data.quantity} bottle(s) to cellar!`);
          
        } else {
          console.log('TZHFrontendLog: Unexpected response status or code');
          console.log('TZHFrontendLog: Expected status 201 and code 201, got status:', response.status, 'code:', response.data.code);
          throw new Error(response.data.message || 'Failed to add to cellar');
        }

      } catch (error) {
        console.log('TZHFrontendLog: Error occurred during process');
        console.error('TZHFrontendLog: Error object:', error);
        console.error('TZHFrontendLog: Error message:', error.message);
        
        if (error.response) {
          console.error('TZHFrontendLog: Error response status:', error.response.status);
          console.error('TZHFrontendLog: Error response headers:', JSON.stringify(error.response.headers, null, 2));
          console.error('TZHFrontendLog: Error response data:', JSON.stringify(error.response.data, null, 2));
        }
        
        // Show user-friendly error message
        let errorMessage = 'Failed to add drink to cellar';
        if (error.response && error.response.data && error.response.data.message) {
          errorMessage = error.response.data.message;
        } else if (error.message) {
          errorMessage = error.message;
        }
        
        console.error('TZHFrontendLog: Final error message:', errorMessage);
        
        // Optional: You can add a toast notification here
        // this.$toast.error(errorMessage);
        
      } finally {
        console.log('TZHFrontendLog: Setting addingToCellar flag to false');
        this.addingToCellar = false;
        console.log('TZHFrontendLog: Frontend process completed');
        console.log('TZHFrontendLog: ===========================================');
      }
    },

    // Reset add drink form
    resetAddDrinkForm() {
      this.addDrinkForm = {
        // Producer search
        producerSearchQuery: '',
        producerSearchResults: [],
        selectedProducer: {},
        producerDebounceTimer: null,
        
        // Drink search
        searchQuery: '',
        searchResults: [],
        selectedDrink: {},
        drinkDebounceTimer: null,
        
        // Group properties (applied to all items in the drink group)
        vintage: null,
        format: 'Bottle',
        volumeNumber: 750,
        volumeUnit: 'ml',
        currentValueEstimation: null,
        currentValueCurrency: 'USD',
        drinkOnwardsDate: null,
        drinkByDate: null,
        suggestedFoodPairing: '',
        
        // Individual item properties (applied to each bottle)
        quantity: 1,
        status: 'In Possession',
        consumption: 'Unopened',
        currentLocation: 'At Home',
        subLocation: '',
        purchasePlaceName: '',
        
        // Purchase location with Google Maps integration
        purchaseLocationInputValue: '', // Input field value for Google Maps autocomplete
        selectedPurchasePlace: '', // Name from Google Maps (for purchasePlaceName)
        selectedPurchaseAddress: '', // Address from Google Maps (for purchaseAddress)
        selectedPurchaseVenueId: null, // Optional venue ID if applicable
        
        purchaseDate: null,
        deliveryDate: null,
        purchasePrice: null,
        purchaseCurrency: 'USD',
        personalNotes: '',
        
        // Collection selection
        selectedCollectionId: null
      };
      
      // Set default collection if collections are available
      if (this.collections.length > 0) {
        const defaultCollection = this.collections.find(c => c.isDefault)
        if (defaultCollection) {
          this.addDrinkForm.selectedCollectionId = defaultCollection.id
        } else {
          // If no default collection found, use the first one
          this.addDrinkForm.selectedCollectionId = this.collections[0].id
        }
      }
    }
  }
}
</script>

<style scoped>
/* Page Layout */
.page-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.page-title {
  color: #212529;
  font-size: 2rem;
}

/* Tabs */
.tabs-container {
  position: relative;
  z-index: 10;
  margin-bottom: 0;
}

.folder-tabs {
  border: none;
  display: flex;
  gap: 0.25rem;
  align-items: flex-end;
  padding-left: 1rem;
  margin-bottom: 0;
}

.folder-tabs .nav-item {
  flex: none;
}

.folder-tab {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-bottom: none;
  border-radius: 12px 12px 0 0;
  color: #6c757d;
  font-weight: 500;
  padding: 0.75rem 1rem;
  transition: all 0.15s ease-in-out;
  position: relative;
  margin-bottom: 0;
  height: 3rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.folder-tab:hover {
  background-color: #e9ecef;
  color: #495057;
  border-color: #adb5bd;
}

.folder-tab.active {
  background-color: #fff;
  color: #212529;
  border-color: #dee2e6;
  z-index: 2;
  position: relative;
}

.folder-tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 1px;
  background-color: #fff;
  z-index: 3;
}

.ghost-tab {
  border: 1px dashed #dee2e6 !important;
  background-color: #f8f9fa !important;
  color: #6c757d !important;
  opacity: 0.7;
}

.ghost-tab:hover {
  border-color: #adb5bd !important;
  background-color: #e9ecef !important;
  color: #495057 !important;
  opacity: 0.85;
}

.ghost-tab .bi-plus-circle {
  font-size: 0.875rem;
}

.item-count {
  font-size: 0.75rem;
  opacity: 0.8;
  margin-left: 0.5rem;
}

/* Cellar Surface - unified container */
.cellar-surface {
  background-color: #fff;
  border: 1px solid #dee2e6;
  border-radius: 0 0.5rem 0.5rem 0.5rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  position: relative;
  z-index: 1;
  margin-top: -1px;
}

/* Filters */
.filters-container {
  padding: 1rem;
  border-bottom: 1px solid #f8f9fa;
}

/* Items Grid */
.items-grid {
  min-height: 400px;
  padding: 0 1rem 1rem 1rem;
}

/* Item Cards */
.cellar-item-card {
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  transition: all 0.2s ease-in-out;
  cursor: pointer;
  overflow: hidden;
}

.cellar-item-card:hover {
  border-color: #0d6efd;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.cellar-item-card:focus {
  outline: 2px solid #0d6efd;
  outline-offset: 2px;
}

.card-img-container {
  position: relative;
  height: 200px;
  overflow: hidden;
  background-color: #f8f9fa;
}

.card-img-top {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.2s ease-in-out;
}

.cellar-item-card:hover .card-img-top {
  transform: scale(1.05);
}

.quantity-badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.card-body {
  position: relative;
  padding: 1rem;
  border-top: 1px solid #dee2e6;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 0.5rem;
  line-height: 1.2;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-subtitle {
  font-size: 0.875rem;
  line-height: 1.2;
}

.card-producer {
  font-size: 0.875rem;
  font-weight: 500;
  color: #6c757d;
}

.card-notes {
  font-size: 0.8rem;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.status-info {
  border-top: 1px solid #f8f9fa;
  padding-top: 0.5rem;
}

.status-badge {
  font-size: 0.75rem;
}

.drink-dates {
  font-size: 0.75rem;
  line-height: 1.2;
}

/* Hover Actions */
.hover-actions {
  position: absolute;
  bottom: 1rem;
  left: 1rem;
  right: 1rem;
  background-color: rgba(255, 255, 255, 0.95);
  padding: 0.5rem;
  border-radius: 0.375rem;
  gap: 0.5rem;
  opacity: 0;
  transform: translateY(1rem);
  transition: all 0.2s ease-in-out;
}

.cellar-item-card:hover .hover-actions {
  opacity: 1;
  transform: translateY(0);
}

/* Loading Skeletons */
.cellar-item-skeleton {
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  overflow: hidden;
}

.skeleton-image {
  height: 200px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

.skeleton-line {
  height: 1rem;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 0.25rem;
  margin-bottom: 0.5rem;
}

.skeleton-title {
  width: 80%;
}

.skeleton-subtitle {
  width: 60%;
}

.skeleton-notes {
  width: 90%;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Empty State */
.empty-state .empty-icon {
  font-size: 4rem;
  opacity: 0.5;
}

/* Right Column Placeholder */
.add-drink-to-cellar .card {
  border: 1px solid #dee2e6;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.add-drink-to-cellar .card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.add-drink-to-cellar .form-label {
  font-weight: 500;
  color: #495057;
  margin-bottom: 0.5rem;
  text-align: left !important;
  display: block;
  width: 100%;
}

.add-drink-to-cellar .form-label small {
  text-align: left !important;
  display: block;
  width: 100%;
}

.add-drink-to-cellar .form-group {
  position: relative;
  text-align: left !important;
}

.add-drink-to-cellar .form-control,
.add-drink-to-cellar .form-select {
  border: 1px solid #ced4da;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.add-drink-to-cellar .form-control:focus,
.add-drink-to-cellar .form-select:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.add-drink-to-cellar .list-group {
  max-height: 200px;
  overflow-y: auto;
  position: absolute;
  z-index: 1000;
  width: 100%;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.add-drink-to-cellar .list-group-item {
  cursor: pointer;
  padding: 0.75rem;
  border-color: #dee2e6;
}

.add-drink-to-cellar .list-group-item:hover {
  background-color: #f8f9fa;
}

.add-drink-to-cellar .list-group-item:first-child {
  border-top-left-radius: 0.375rem;
  border-top-right-radius: 0.375rem;
}

.add-drink-to-cellar .list-group-item:last-child {
  border-bottom-left-radius: 0.375rem;
  border-bottom-right-radius: 0.375rem;
}

.add-drink-to-cellar .btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
  font-weight: 500;
}

.add-drink-to-cellar .btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

.add-drink-to-cellar .btn-primary:disabled {
  background-color: #6c757d;
  border-color: #6c757d;
  opacity: 0.65;
}

.add-drink-to-cellar .spinner-border-sm {
  width: 0.875rem;
  height: 0.875rem;
}

/* Form group spacing */
.add-drink-to-cellar .form-group {
  position: relative;
  text-align: left !important;
}

/* Drink Preview Section */
.add-drink-to-cellar .cellar-item-preview {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 1rem 0;
}

.add-drink-to-cellar .cellar-item-preview hr {
  margin: 0 0 1rem 0;
  border-color: #dee2e6;
}

.add-drink-to-cellar .preview-image,
.add-drink-to-cellar .preview-image-mobile {
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  background-color: #fff;
  padding: 0.5rem;
}

.add-drink-to-cellar .cellar-item-preview h6 {
  color: #212529;
  font-size: 1rem;
  line-height: 1.2;
}

.add-drink-to-cellar .cellar-item-preview .text-muted {
  color: #6c757d !important;
  font-size: 0.875rem;
  line-height: 1.3;
}

.add-drink-to-cellar .cellar-item-preview .text-primary {
  color: #0d6efd !important;
  font-size: 0.875rem;
}

/* Success message styling */
.add-drink-to-cellar .bg-light {
  background-color: #e7f3ff !important;
  border-color: #86b7fe !important;
  text-align: left !important;
}

.add-drink-to-cellar .text-success {
  color: #198754 !important;
  text-align: left !important;
}

/* Input group styling */
.add-drink-to-cellar .input-group .form-select {
  border-right: none;
}

.add-drink-to-cellar .input-group .form-control {
  border-left: none;
}

.add-drink-to-cellar .input-group .form-select:focus {
  border-right: none;
  box-shadow: none;
}

.add-drink-to-cellar .input-group .form-control:focus {
  border-left: none;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.add-drink-to-cellar .input-group:focus-within .form-select {
  border-color: #86b7fe;
}

.add-drink-to-cellar .input-group:focus-within .form-control {
  border-color: #86b7fe;
}

/* Pagination */
.pagination-container {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

/* Modal Styles */
.modal-xl {
  max-width: 1200px;
}

.modal-header-content {
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 1.5rem;
  margin-bottom: 1.5rem !important;
}

.item-image-container {
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-detail-image {
  max-width: 100%;
  max-height: 300px;
  object-fit: contain;
  border-radius: 0.375rem;
}

.drink-info-summary {
  height: 100%;
  display: flex;
  flex-direction: column;
  text-align: left;
}

.info-row {
  line-height: 1.4;
  text-align: left;
}

.info-text {
  font-size: 0.95rem;
  color: #212529;
}

.info-text strong {
  font-weight: 600;
  color: #495057;
}

.editable-value {
  color: #1c6bb0 !important;
  cursor: pointer;
  transition: color 0.2s ease;
}

.editable-value:hover {
  color: #495057 !important;
}

.learn-more-section {
  margin-top: auto;
  padding-top: 0.5rem;
}

.info-item {
  margin-bottom: 0.75rem;
}

.info-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #6c757d;
  margin-bottom: 0.25rem;
  display: block;
}

.info-value {
  font-size: 1rem;
  color: #212529;
  margin: 0;
  font-weight: 500;
}

.editable-sections {
  background-color: #fafbfc;
  border-radius: 0.5rem;
  padding: 1.5rem;
}

.detail-section {
  background-color: #fff;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.detail-section:last-child {
  margin-bottom: 0 !important;
}

.section-header {
  color: #495057;
  font-weight: 600;
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #e9ecef;
  font-size: 1.1rem;
}

.currency-select {
  max-width: 80px;
  flex: 0 0 80px;
}

.volume-unit-select {
  max-width: 70px;
  flex: 0 0 70px;
}

.date-input {
  cursor: pointer;
}

.date-input:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.input-group-text {
  cursor: pointer;
}

.form-label {
  font-weight: 500;
  color: #495057;
  margin-bottom: 0.5rem;
}

.form-control[readonly] {
  background-color: #f8f9fa;
  border-color: #e9ecef;
  color: #6c757d;
}

/* Modal responsive adjustments */
@media (max-width: 768px) {
  .modal-xl {
    max-width: 95%;
    margin: 0.5rem auto;
  }
  
  .modal-header-content {
    flex-direction: column;
  }
  
  .item-image-container {
    min-height: 200px;
    padding: 0.75rem;
    margin-bottom: 1rem;
  }
  
  .item-detail-image {
    max-height: 250px;
  }
  
  .drink-info-summary {
    margin-top: 1rem;
  }
  
  .editable-sections {
    padding: 1rem;
  }
  
  .detail-section {
    padding: 1rem;
  }
  
  .currency-select {
    max-width: 70px;
    flex: 0 0 70px;
  }
  
  .volume-unit-select {
    max-width: 60px;
    flex: 0 0 60px;
  }
}

/* Responsive Design */
@media (max-width: 992px) {
  .hover-actions {
    display: none !important;
  }
  
  .add-drink-to-cellar {
    margin-top: 2rem;
  }
  
  .add-drink-to-cellar .card-body {
    padding: 1rem;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 1.5rem;
  }
  
  .filters-container .row > div {
    margin-bottom: 0.5rem;
  }
  
  .folder-tabs {
    padding-left: 0.5rem;
    gap: 0.125rem;
    flex-wrap: wrap;
  }
  
  .folder-tab {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
    height: 2.5rem;
    border-radius: 8px 8px 0 0;
  }
  
  .item-count {
    display: block;
    font-size: 0.7rem;
    margin-left: 0;
    margin-top: 0.125rem;
  }
  
  .ghost-tab .bi-plus-circle {
    font-size: 0.75rem;
  }
  
  .cellar-surface {
    border-radius: 0 0.375rem 0.375rem 0.375rem;
  }
  
  .add-drink-to-cellar .form-label {
    font-size: 0.875rem;
  }
  
  .add-drink-to-cellar .form-control,
  .add-drink-to-cellar .form-select {
    font-size: 0.875rem;
  }
}

/* Collection Selector in Modal Header */
.collection-selector {
  text-align: right;
}

.collection-selector .form-label {
  display: block;
  margin-bottom: 2px;
  font-size: 0.75rem;
  font-weight: 500;
}

.collection-selector .form-select {
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.collection-selector .form-select:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.collection-status-select {
  font-weight: 500;
}

.collection-status-select option {
  padding: 8px 12px;
  font-weight: 500;
}

/* Note: Individual option color styling is limited in browsers, 
   but this provides the text prefixes as requested */

/* Bottle Counter Controls */
.bottle-counter-controls {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-left: auto;
}

.bottle-count {
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 500;
  color: #495057;
}

.bottle-count i {
  font-size: 16px;
  color: #6c757d;
}

.btn-add-bottle {
  font-size: 14px;
  padding: 4px 12px;
  border-radius: 20px;
  background-color: #28a745;
  border-color: #28a745;
  transition: all 0.3s ease;
}

.btn-add-bottle:hover {
  background-color: #218838;
  border-color: #1e7e34;
  transform: translateY(-1px);
}

.btn-add-bottle i {
  margin-right: 5px;
  font-size: 12px;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 1.5rem;
  }
  
  .filters-container .row > div {
    margin-bottom: 0.5rem;
  }
  
  .folder-tabs {
    padding-left: 0.5rem;
    gap: 0.125rem;
    flex-wrap: wrap;
  }
  
  .folder-tab {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
    height: 2.5rem;
    border-radius: 8px 8px 0 0;
  }
  
  .item-count {
    display: block;
    font-size: 0.7rem;
    margin-left: 0;
    margin-top: 0.125rem;
  }
  
  .ghost-tab .bi-plus-circle {
    font-size: 0.75rem;
  }
  
  .cellar-surface {
    border-radius: 0 0.375rem 0.375rem 0.375rem;
  }
}

@media (max-width: 576px) {
  .card-img-container {
    height: 150px;
  }
  
  .card-body {
    padding: 0.75rem;
  }
  
  .card-title {
    font-size: 0.9rem;
  }
  
  .pagination-container {
    justify-content: center;
  }
  
  .folder-tabs {
    padding-left: 0.25rem;
  }
  
  .folder-tab {
    padding: 0.4rem 0.6rem;
    font-size: 0.8rem;
    height: 2.25rem;
    border-radius: 6px 6px 0 0;
  }
  
  .filters-container {
    padding: 0.75rem;
  }
  
  .items-grid {
    padding: 0 0.75rem 0.75rem 0.75rem;
  }
  
  .add-drink-to-cellar .card-header {
    padding: 0.75rem;
  }
  
  .add-drink-to-cellar .card-body {
    padding: 0.75rem;
  }
  
  .add-drink-to-cellar .form-label {
    font-size: 0.8rem;
    margin-bottom: 0.375rem;
  }
  
  .add-drink-to-cellar .form-control,
  .add-drink-to-cellar .form-select,
  .add-drink-to-cellar textarea {
    font-size: 0.8rem;
    padding: 0.375rem 0.5rem;
  }
  
  .add-drink-to-cellar .btn {
    font-size: 0.875rem;
    padding: 0.5rem 1rem;
  }
  
  .add-drink-to-cellar .list-group-item {
    padding: 0.5rem;
    font-size: 0.8rem;
  }
  
  .add-drink-to-cellar .cellar-item-preview {
    padding: 0.75rem;
    margin: 0.75rem 0;
  }
  
  .add-drink-to-cellar .cellar-item-preview h6 {
    font-size: 0.875rem;
  }
  
  .add-drink-to-cellar .cellar-item-preview .text-muted {
    font-size: 0.75rem;
  }
  
  .add-drink-to-cellar .cellar-item-preview .text-primary {
    font-size: 0.75rem;
  }
}

/* Form Section Styling */
.form-section {
  border: 1px solid #e9ecef;
  border-radius: 0.375rem;
  padding: 1.5rem;
  background-color: #fafbfc;
  margin-bottom: 1rem;
}

.form-section .section-header {
  color: #495057;
  font-weight: 600;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.form-section .section-header i {
  color: #6c757d;
}

.form-section .section-header small {
  color: #6c757d;
  font-size: 0.75rem;
  line-height: 1.2;
}

/* Text alignment overrides */
.form-section .form-label.text-start,
.form-section .section-header {
  text-align: left !important;
}

/* Responsive adjustments for form sections */
@media (max-width: 768px) {
  .form-section {
    padding: 1rem;
  }
  
  .form-section .section-header {
    font-size: 1rem;
  }
}

/* Google Maps Purchase Location Styles */
.purchase-location-container {
  position: relative;
}

.purchase-location-container .input-with-icon {
  border-right: none;
}

.purchase-location-container .input-group-text .bi-geo-alt.text-success {
  color: #198754 !important;
}

.purchase-location-container .alert {
  font-size: 0.875rem;
  padding: 0.5rem 0.75rem;
  margin-bottom: 0;
}

.purchase-location-container .alert .btn-sm {
  padding: 0.125rem 0.25rem;
  font-size: 0.75rem;
}

/* Global Google Maps autocomplete dropdown styling */
:global(.pac-container) {
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 0.375rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  font-family: inherit;
  z-index: 1051 !important; /* Above Bootstrap modals */
}

:global(.pac-item) {
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}

:global(.pac-item:hover) {
  background-color: #f8f9fa;
}

:global(.pac-item:last-child) {
  border-bottom: none;
}

:global(.pac-item-query) {
  font-weight: 600;
  color: #212529;
}

:global(.pac-matched) {
  font-weight: 700;
  color: #0d6efd;
}
</style>
