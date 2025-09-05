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
              <nav class="tabs-nav">
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
                          <span v-if="group.representative.typeCategory"> • {{ group.representative.typeCategory }}</span>
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

          <!-- Right Column - Add Drink Placeholder (4/12 columns) -->
          <div class="col-12 col-lg-4 mt-4 mt-lg-0">
            <div class="add-drink-placeholder">
              <div class="placeholder-content text-center p-4">
                <div class="placeholder-icon mb-3">
                  <i class="bi bi-plus-circle" style="font-size: 3rem; color: #6c757d;"></i>
                </div>
                <h4 class="placeholder-title mb-2">Add a Drink to Cellar</h4>
                <p class="placeholder-text text-muted">
                  Coming next - Add drinks to your personal cellar with detailed tracking options.
                </p>
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
            <h5 class="modal-title" id="itemDetailsModalLabel">
              {{ selectedGroup?.representative?.listingName || 'Item Details' }}
              <span v-if="selectedGroup?.representative?.variant" class="text-muted">
                ({{ selectedGroup.representative.variant }})
              </span>
            </h5>
            <button 
              type="button" 
              class="btn-close" 
              data-bs-dismiss="modal" 
              aria-label="Close"
            ></button>
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
                  
                  <!-- Row 1: Producer | Bottler -->
                  <div class="info-row mb-2">
                    <span class="info-text">
                      <strong>Producer:</strong> {{ selectedGroup.representative.producerName || 'N/A' }}
                      <span v-if="selectedGroup.representative.bottlerName || selectedGroup.representative.producerName" class="mx-2">|</span>
                      <strong>Bottler:</strong> {{ selectedGroup.representative.bottlerName || 'Original Bottling' }}
                    </span>
                  </div>
                  
                  <!-- Row 2: Country • Type • Category -->
                  <div class="info-row mb-2">
                    <span class="info-text text-muted">
                      <template v-if="selectedGroup.representative.originCountry">{{ selectedGroup.representative.originCountry }}</template>
                      <template v-if="selectedGroup.representative.originCountry && selectedGroup.representative.drinkType"> • </template>
                      <template v-if="selectedGroup.representative.drinkType">{{ selectedGroup.representative.drinkType }}</template>
                      <template v-if="selectedGroup.representative.drinkType && selectedGroup.representative.typeCategory"> • </template>
                      <template v-if="selectedGroup.representative.typeCategory">{{ selectedGroup.representative.typeCategory }}</template>
                    </span>
                  </div>
                  
                  <!-- Row 3: Group Summary -->
                  <div class="info-row mb-3">
                    <span class="info-text">
                      <strong>You have {{ selectedGroup.bottleCount }} bottle{{ selectedGroup.bottleCount !== 1 ? 's' : '' }}</strong>
                      <span v-if="selectedGroup.representative.variant" class="mx-2">•</span>
                      <span v-if="selectedGroup.representative.variant">
                        <strong>Vintage:</strong> {{ selectedGroup.representative.variant }}
                      </span>
                    </span>
                  </div>

                  <!-- Row 4: Drinking Window -->
                  <div class="info-row mb-2" v-if="selectedGroup.representative.drinkOnwardsDate || selectedGroup.representative.drinkByDate">
                    <span class="info-text text-muted">
                      <template v-if="selectedGroup.representative.drinkOnwardsDate">
                        <strong>Drink from:</strong> {{ formatDate(selectedGroup.representative.drinkOnwardsDate) }}
                      </template>
                      <template v-if="selectedGroup.representative.drinkOnwardsDate && selectedGroup.representative.drinkByDate"> • </template>
                      <template v-if="selectedGroup.representative.drinkByDate">
                        <strong>Drink by:</strong> {{ formatDate(selectedGroup.representative.drinkByDate) }}
                      </template>
                    </span>
                  </div>

                  <!-- Row 5: Collection & Market Value -->
                  <div class="info-row mb-2">
                    <span class="info-text text-muted">
                      <template v-if="selectedGroup.representative.collectionId">
                        <strong>Collection:</strong> {{ collections.find(c => c.id === selectedGroup.representative.collectionId)?.collectionName || 'Default Collection' }}
                      </template>
                      <template v-else>
                        <strong>Collection:</strong> Default Collection
                      </template>
                      <template v-if="selectedGroup.representative.currentValueEstimation"> • </template>
                      <template v-if="selectedGroup.representative.currentValueEstimation">
                        <strong>Market Value:</strong> {{ selectedGroup.representative.currentValueCurrency || 'USD' }} {{ selectedGroup.representative.currentValueEstimation }}
                      </template>
                    </span>
                  </div>

                  <!-- Row 6: Food Pairing -->
                  <div class="info-row mb-3" v-if="selectedGroup.representative.suggestedFoodPairing">
                    <span class="info-text text-muted">
                      <strong>Suggested Pairing:</strong> {{ selectedGroup.representative.suggestedFoodPairing }}
                    </span>
                  </div>
                  
                  <!-- Learn More Button -->
                  <div class="learn-more-section">
                    <button 
                      type="button" 
                      class="btn btn-primary btn-md"
                      data-bs-dismiss="modal"
                      @click="goToListingPage(selectedGroup.representative)"
                    >
                      Learn more about this drink
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Individual Bottles Management -->
            <div class="individual-bottles-section mb-4">
              <h6 class="section-header">Individual Bottles Management</h6>
              <div class="bottles-list">
                <div 
                  v-for="(bottle, index) in selectedGroup.bottles" 
                  :key="bottle.cellarItemId"
                  class="bottle-item p-3 mb-3 border rounded"
                  :class="{ 'bottle-consumed': bottle.status === 'Consumed' }"
                >
                  <div class="row align-items-center">
                    <div class="col-md-2">
                      <strong>Bottle #{{ index + 1 }}</strong>
                      <br>
                      <small class="text-muted">ID: {{ bottle.quantityVariantID }}</small>
                    </div>
                    <div class="col-md-3">
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
                    <div class="col-md-3">
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
                      <button 
                        class="btn btn-sm btn-outline-primary w-100"
                        @click="editIndividualBottle(bottle)"
                        title="Edit this specific bottle"
                      >
                        <i class="bi bi-pencil"></i> Edit
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Shared Properties for Group -->
            <div class="editable-sections">
              <div class="detail-section">
                <!-- Group Details -->
                <h6 class="section-header">Group Details</h6>
                <div class="row g-3 mb-4">
                  <div class="col-md-3">
                    <label class="form-label">Total Bottles</label>
                    <input type="number" class="form-control" :value="selectedGroup.bottleCount" readonly>
                    <small class="text-muted">Each bottle tracked individually above</small>
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
                    <label class="form-label">Vintage</label>
                    <input type="number" class="form-control" :value="selectedGroup.representative.variant" min="1900" max="2030">
                  </div>
                  <div class="col-md-3">
                    <label class="form-label">Volume</label>
                    <div class="input-group">
                      <input type="number" class="form-control" :value="selectedGroup.representative.volumeML" step="0.1" min="0">
                      <select class="form-select volume-unit-select">
                        <option value="ml" selected>ml</option>
                        <option value="oz">oz</option>
                        <option value="l">L</option>
                      </select>
                    </div>
                  </div>
                </div>

                <!-- Drinking Window -->
                <h6 class="section-header">Drinking Window</h6>
                <div class="row g-3 mb-4">
                  <div class="col-md-6">
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
                  <div class="col-md-6">
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
                </div>

                <!-- Procurement Details -->
                <h6 class="section-header">Procurement Details</h6>
                <div class="row g-3 mb-4">
                  <div class="col-md-6">
                    <label class="form-label">Date of Purchase</label>
                    <div class="input-group">
                      <input 
                        type="text" 
                        class="form-control date-input" 
                        :value="formatDateForInput(selectedGroup.representative.purchaseDate)"
                        placeholder="MM/DD/YYYY"
                      >
                      <span class="input-group-text">
                        <i class="bi bi-calendar3"></i>
                      </span>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label">Delivery Date</label>
                    <div class="input-group">
                      <input 
                        type="text" 
                        class="form-control date-input" 
                        :value="formatDateForInput(selectedGroup.representative.deliveryDate)"
                        placeholder="MM/DD/YYYY"
                      >
                      <span class="input-group-text">
                        <i class="bi bi-calendar3"></i>
                      </span>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label">Place of Purchase</label>
                    <div class="input-group">
                      <input 
                        type="text" 
                        class="form-control" 
                        :value="selectedGroup.representative.purchasePlaceName"
                        placeholder="Enter location"
                      >
                      <span class="input-group-text" title="Google Maps integration coming soon">
                        <i class="bi bi-geo-alt"></i>
                      </span>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label">Price of Purchase</label>
                    <div class="input-group">
                      <select class="form-select currency-select" :value="selectedGroup.representative.purchaseCurrency">
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
                        :value="selectedGroup.representative.purchasePrice"
                        step="0.01" 
                        min="0"
                        placeholder="0.00"
                      >
                    </div>
                  </div>
                </div>

                <!-- Default Collection -->
                <h6 class="section-header">Collection</h6>
                <div class="row g-3 mb-4">
                  <div class="col-md-6">
                    <label class="form-label">Collection</label>
                    <select class="form-select" :value="selectedGroup.representative.collectionId">
                      <option value="">Default Collection</option>
                      <option v-for="collection in collections" :key="collection.id" :value="collection.id">
                        {{ collection.collectionName }}
                      </option>
                    </select>
                  </div>
                </div>

                <!-- Additional Information -->
                <h6 class="section-header">Additional Information</h6>
                <div class="row g-3 mb-4">
                  <div class="col-md-6">
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
                  <div class="col-md-6">
                    <label class="form-label">Suggested Food Pairing</label>
                    <div class="input-group">
                      <select class="form-select" :value="selectedGroup.representative.suggestedFoodPairing">
                        <option value="">Select pairing</option>
                      </select>
                      <button class="btn btn-outline-secondary" type="button" title="Add new pairing">
                        <i class="bi bi-plus"></i>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Notes -->
                <h6 class="section-header">Notes</h6>
                <div class="row">
                  <div class="col-12">
                    <textarea 
                      class="form-control" 
                      rows="3" 
                      :value="selectedGroup.representative.noteToSelf"
                      placeholder="Add your notes here..."
                    ></textarea>
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
      searchTimeout: null
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
    
    // Group items by listing + variant for display
    groupedItems() {
      const groups = {}
      
      this.tabItems.forEach(item => {
        // Create unique key for listing + variant combination
        const groupKey = `${item.listingId}_${item.variant || 'no-variant'}`
        
        if (!groups[groupKey]) {
          groups[groupKey] = {
            // Use first item as representative for display
            representative: item,
            // Track all individual bottles in this group
            bottles: [],
            // Count of bottles in this group
            bottleCount: 0,
            // Group identification
            listingId: item.listingId,
            variant: item.variant,
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
        groups = groups.filter(group => group.representative.volumeML == this.filters.size)
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
        
        // Debug: log first item to see what image properties are available
        if (this.allItems.length > 0) {
          console.log('Sample cellar item data:', this.allItems[0]);
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
      if (group.listingId && group.representative.drinkName) {
        // Small delay to allow modal dismiss to complete
        setTimeout(() => {
          const listingName = group.representative.drinkName.replace(/[^a-zA-Z0-9\s-]/g, '').replace(/\s+/g, '-').toLowerCase()
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
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      })
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
.add-drink-placeholder {
  background-color: #fff;
  border: 2px dashed #dee2e6;
  border-radius: 0.5rem;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-content {
  max-width: 300px;
}

.placeholder-title {
  color: #495057;
  margin-bottom: 1rem;
}

.placeholder-text {
  line-height: 1.5;
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
}

.info-row {
  line-height: 1.4;
}

.info-text {
  font-size: 0.95rem;
  color: #212529;
}

.info-text strong {
  font-weight: 600;
  color: #495057;
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
  
  .add-drink-placeholder {
    margin-top: 2rem;
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
}
</style>
