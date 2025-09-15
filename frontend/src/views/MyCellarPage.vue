<template>
  <NavBar />
  
  <main>
    <!-- Page Header 
    <section class="page-header py-4">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <h1 class="page-title fw-bold mb-0">My Cellar</h1>
          </div>
        </div>
      </div>
    </section>-->

    <!-- Main Content Grid -->
    <section class="main-content py-4">
      <div class="container-fluid">
        <div class="row">
          <!-- Left Column - Collections & Items (responsive width) -->
          <div :class="'col-12 ' + (rightSidebarExpanded ? 'col-lg-8' : 'col-lg-12')">
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
                      My Cellar (All Drinks)
                      <span class="item-count" v-if="!loading && activeTab === 'all'">{{ totalItemCount }} Items</span>
                      <span class="item-count" v-else-if="loading && activeTab === 'all'">...</span>
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
                      <span class="item-count" v-if="!loading">{{ getCollectionItemCount(collection.id) }} Items</span>
                      <span class="item-count" v-else>...</span>
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
                      New Collection
                    </button>
                  </li>
                  <!-- Cellar History Tab -->
                  <li class="nav-item ms-auto">
                    <button 
                      class="nav-link folder-tab"
                      :class="{ active: activeTab === 'history' }"
                      @click="setActiveTab('history')"
                      type="button"
                    >
                      <i class="bi bi-clock-history me-2"></i>
                      <span class="mobile-view-hide">History</span>
                    </button>
                  </li>
                  <!-- Cellar Dashboard Tab -->
                  <li class="nav-item">
                    <button 
                      class="nav-link folder-tab"
                      :class="{ active: activeTab === 'dashboard' }"
                      @click="setActiveTab('dashboard')"
                      type="button"
                    >
                      <i class="bi bi-bar-chart me-2"></i>
                      <span class="mobile-view-hide">Dashboard</span>
                    </button>
                  </li>
                </ul>
              </nav>
            </div>

            <!-- Cellar Surface - unified container for filters and items -->
            <section class="cellar-surface">
              <!-- History Tab Content -->
              <div v-if="activeTab === 'history'" class="history-tab-content">
                <div class="cellar-change-log">
                  <div class="card h-100">
                    <div class="card-header">
                      <h5 class="card-title mb-0">
                        <i class="bi bi-clock-history me-2"></i>
                        Cellar History
                      </h5>
                    </div>
                    <div class="card-body">
                      <!-- Loading State -->
                      <div v-if="loadingChangelog" class="changelog-entries">
                        <div class="changelog-entry mb-3 p-3 border rounded">
                          <div class="change-description mb-2">
                            <div class="d-flex justify-content-between align-items-center">
                              <span class="text-start">
                                <div class="spinner-border spinner-border-sm me-2"></div>
                                Loading your cellar history...
                              </span>
                              <span class="badge bg-secondary ms-2">Loading</span>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <!-- Error State -->
                      <div v-else-if="changelogError" class="changelog-entries">
                        <div class="changelog-entry mb-3 p-3 border rounded border-danger">
                          <div class="change-description mb-2">
                            <div class="d-flex justify-content-between align-items-center">
                              <span class="text-start text-danger">
                                <i class="bi bi-exclamation-triangle me-2"></i>
                                {{ changelogError }}
                              </span>
                              <span class="badge bg-danger ms-2">Error</span>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <!-- Empty State -->
                      <div v-else-if="safeChangelog.length === 0" class="changelog-entries">
                        <div class="changelog-entry mb-3 p-3 border rounded">
                          <div class="change-description mb-2">
                            <div class="d-flex justify-content-between align-items-center">
                              <span class="text-start text-muted">
                                <i class="bi bi-journal-x me-2"></i>
                                No recent changes to your cellar
                              </span>
                              <span class="badge bg-light text-muted ms-2">Empty</span>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <!-- Changelog Entries -->
                      <div v-else-if="safeChangelog.length > 0" class="changelog-entries">
                        <div 
                          v-for="entry in safeChangelog" 
                          :key="entry.id || `entry-${Date.now()}-${Math.random()}`"
                          class="changelog-entry mb-3 p-3 border rounded"
                        >
                          <!-- Human-readable change description -->
                          <div class="change-description mb-2">
                            <div class="d-flex justify-content-between align-items-center">
                              <span class="text-start" v-html="formatChangelogEntry(entry)"></span>
                              <span class="badge ms-2" :class="getChangeTypeBadgeClass(entry?.changeType)">
                                {{ formatChangeType(entry?.changeType) }}
                              </span>
                            </div>
                          </div>
                        </div>
                        
                        <!-- Load More Button -->
                        <div v-if="hasMoreChangelog" class="text-center mt-3">
                          <button 
                            class="btn btn-outline-secondary btn-sm"
                            @click="loadMoreChangelog"
                            :disabled="loadingMoreChangelog"
                          >
                            <span v-if="loadingMoreChangelog" class="spinner-border spinner-border-sm me-1"></span>
                            {{ loadingMoreChangelog ? 'Loading...' : 'Load More' }}
                          </button>
                        </div>
                      </div>
                      
                      <!-- Fallback Empty State -->
                      <div v-else class="changelog-entries">
                        <div class="changelog-entry mb-3 p-3 border rounded">
                          <div class="change-description mb-2">
                            <div class="d-flex justify-content-between align-items-center">
                              <span class="text-start text-muted">
                                <i class="bi bi-journal-x me-2"></i>
                                No recent changes to your cellar
                              </span>
                              <span class="badge bg-light text-muted ms-2">Empty</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Dashboard Tab Content -->
              <div v-else-if="activeTab === 'dashboard'" class="dashboard-tab-content">
                <div class="cellar-dashboard">
                  <div class="card h-100">
                    <div class="card-header">
                      <h5 class="card-title mb-0">
                        <i class="bi bi-bar-chart me-2"></i>
                        Cellar Dashboard
                      </h5>
                    </div>
                    <div class="card-body">
                      <!-- Dashboard Content -->
                      <div class="dashboard-content">
                        <!-- Loading State -->
                        <div v-if="loadingDashboard" class="text-center py-4">
                          <div class="spinner-border spinner-border-sm me-2"></div>
                          Loading dashboard data...
                        </div>
                        
                        <!-- Error State -->
                        <div v-else-if="dashboardError" class="alert alert-danger">
                          <h5>Unable to Load Dashboard</h5>
                          <p>{{ dashboardError }}</p>
                          <button class="btn btn-outline-danger" @click="fetchCellarDashboard">
                            <i class="bi bi-arrow-clockwise me-1"></i>
                            Try Again
                          </button>
                        </div>
                        
                        <!-- Dashboard Content -->
                        <div v-else-if="dashboardData && dashboardData.summary" class="row">
                          <!-- Summary Cards -->
                          <div class="col-12 mb-4">
                            <div class="row">
                              <div class="col-6 col-md-4 mb-3">
                                <div class="card text-center">
                                  <div class="card-body">
                                    <h5 class="card-title">{{ dashboardData.summary.totalItems || 0 }}</h5>
                                    <p class="card-text text-muted">Total Items</p>
                                  </div>
                                </div>
                              </div>
                              <div class="col-6 col-md-4 mb-3">
                                <div class="card text-center">
                                  <div class="card-body">
                                    <h5 class="card-title">${{ (dashboardData.summary.totalPurchaseCost || 0).toLocaleString() }}</h5>
                                    <p class="card-text text-muted">Total Purchase Cost</p>
                                  </div>
                                </div>
                              </div>
                              <div class="col-6 col-md-4 mb-3">
                                <div class="card text-center">
                                  <div class="card-body">
                                    <h5 class="card-title">${{ (dashboardData.summary.totalCurrentValue || 0).toLocaleString() }}</h5>
                                    <p class="card-text text-muted">Current Value</p>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                          
                          <!-- Top Insights -->
                          <div class="col-12">
                            <div class="row">
                              <!-- Top Drink Types -->
                              <div class="col-md-4 col-lg-3 mb-4">
                                <div class="card">
                                  <div class="card-header">
                                    <h6 class="mb-0">Top Drink Types</h6>
                                  </div>
                                  <div class="card-body">
                                    <div v-for="(data, drinkType) in getTopBreakdowns(dashboardData.breakdowns?.byDrinkType, 5)" :key="drinkType" class="d-flex justify-content-between align-items-center mb-2">
                                      <span>{{ drinkType }}</span>
                                      <span class="badge bg-primary">{{ data.count }}</span>
                                    </div>
                                    <div v-if="!dashboardData.breakdowns?.byDrinkType || Object.keys(dashboardData.breakdowns.byDrinkType).length === 0" class="text-muted small">
                                      No drink types data available
                                    </div>
                                  </div>
                                </div>
                              </div>
                              
                              <!-- Top Categories -->
                              <div class="col-md-4 col-lg-3 mb-4">
                                <div class="card">
                                  <div class="card-header">
                                    <h6 class="mb-0">Top Categories</h6>
                                  </div>
                                  <div class="card-body">
                                    <div v-for="(data, category) in getTopBreakdowns(dashboardData.breakdowns?.byCategory, 5)" :key="category" class="d-flex justify-content-between align-items-center mb-2">
                                      <span>{{ category }}</span>
                                      <span class="badge bg-success">{{ data.count }}</span>
                                    </div>
                                    <div v-if="!dashboardData.breakdowns?.byCategory || Object.keys(dashboardData.breakdowns.byCategory).length === 0" class="text-muted small">
                                      No categories data available
                                    </div>
                                  </div>
                                </div>
                              </div>
                              
                              <!-- Top Countries -->
                              <div class="col-md-4 col-lg-3 mb-4">
                                <div class="card">
                                  <div class="card-header">
                                    <h6 class="mb-0">Top Countries</h6>
                                  </div>
                                  <div class="card-body">
                                    <div v-for="(data, country) in getTopBreakdowns(dashboardData.breakdowns?.byCountry, 5)" :key="country" class="d-flex justify-content-between align-items-center mb-2">
                                      <span>{{ country }}</span>
                                      <span class="badge bg-info">{{ data.count }}</span>
                                    </div>
                                    <div v-if="!dashboardData.breakdowns?.byCountry || Object.keys(dashboardData.breakdowns.byCountry).length === 0" class="text-muted small">
                                      No countries data available
                                    </div>
                                  </div>
                                </div>
                              </div>
                              
                              <!-- Top Producers -->
                              <div class="col-md-4 col-lg-3 mb-4">
                                <div class="card">
                                  <div class="card-header">
                                    <h6 class="mb-0">Top Producers</h6>
                                  </div>
                                  <div class="card-body">
                                    <div v-for="(data, producer) in getTopBreakdowns(dashboardData.breakdowns?.byProducer, 5)" :key="producer" class="d-flex justify-content-between align-items-center mb-2">
                                      <span class="text-truncate" :title="producer">{{ producer }}</span>
                                      <span class="badge bg-warning text-dark">{{ data.count }}</span>
                                    </div>
                                    <div v-if="!dashboardData.breakdowns?.byProducer || Object.keys(dashboardData.breakdowns.byProducer).length === 0" class="text-muted small">
                                      No producers data available
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                            
                            <!-- Second Row - Purchase Locations and Status Breakdowns -->
                            <div class="row">
                              <!-- Top Purchase Locations -->
                              <div class="col-md-6 col-lg-4 mb-4">
                                <div class="card">
                                  <div class="card-header">
                                    <h6 class="mb-0">Top Purchase Locations</h6>
                                  </div>
                                  <div class="card-body">
                                    <div v-for="(data, location) in getFilteredPurchaseLocations(dashboardData.breakdowns?.byPurchaseAddress, 5)" :key="location" class="d-flex justify-content-between align-items-center mb-2">
                                      <span class="text-truncate" :title="location">{{ location }}</span>
                                      <span class="badge bg-secondary">{{ data.count }}</span>
                                    </div>
                                    <div v-if="!dashboardData.breakdowns?.byPurchaseAddress || getFilteredPurchaseLocationsCount(dashboardData.breakdowns.byPurchaseAddress) === 0" class="text-muted small">
                                      No purchase locations data available
                                    </div>
                                  </div>
                                </div>
                              </div>
                              
                              <!-- Items by Status -->
                              <div class="col-md-6 col-lg-4 mb-4">
                                <div class="card">
                                  <div class="card-header">
                                    <h6 class="mb-0">Items by Status</h6>
                                  </div>
                                  <div class="card-body">
                                    <div v-for="(data, status) in getTopBreakdowns(dashboardData.breakdowns?.byStatus, 10)" :key="status" class="d-flex justify-content-between align-items-center mb-2">
                                      <span>{{ status }}</span>
                                      <span class="badge" :class="getDashboardStatusBadgeClass(status)">{{ data.count }}</span>
                                    </div>
                                    <div v-if="!dashboardData.breakdowns?.byStatus || Object.keys(dashboardData.breakdowns.byStatus).length === 0" class="text-muted small">
                                      No status data available
                                    </div>
                                  </div>
                                </div>
                              </div>
                              
                              <!-- Items by Consumption -->
                              <div class="col-md-6 col-lg-4 mb-4">
                                <div class="card">
                                  <div class="card-header">
                                    <h6 class="mb-0">Items by Consumption</h6>
                                  </div>
                                  <div class="card-body">
                                    <div v-for="(data, consumption) in getTopBreakdowns(dashboardData.breakdowns?.byConsumption, 10)" :key="consumption" class="d-flex justify-content-between align-items-center mb-2">
                                      <span>{{ consumption }}</span>
                                      <span class="badge bg-dark">{{ data.count }}</span>
                                    </div>
                                    <div v-if="!dashboardData.breakdowns?.byConsumption || Object.keys(dashboardData.breakdowns.byConsumption).length === 0" class="text-muted small">
                                      No consumption data available
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        
                        <!-- Placeholder for no data -->
                        <div v-else class="row">
                          <div class="col-12">
                            <p class="text-muted text-center py-4">
                              <i class="bi bi-info-circle me-2"></i>
                              No dashboard data available. Add some items to your cellar first!
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Collection/Items Tab Content -->
              <div v-else>
              <!-- Mobile Filters Toggle Button (only shown on mobile) -->
              <div class="mobile-filters-toggle d-block d-sm-none mb-3 mt-2">
                <button 
                  class="btn btn-outline-secondary btn-sm w-100" 
                  type="button"
                  @click="toggleMobileFilters"
                >
                  <i class="bi" :class="mobileFiltersCollapsed ? 'bi-funnel' : 'bi-funnel-fill'"></i>
                  {{ mobileFiltersCollapsed ? 'Show Filters' : 'Hide Filters' }}
                  <i class="bi ms-2" :class="mobileFiltersCollapsed ? 'bi-chevron-down' : 'bi-chevron-up'"></i>
                </button>
              </div>
              
              <!-- Filters Row -->
              <div class="filters-container" :class="{ 'mobile-collapsed': mobileFiltersCollapsed }">
                <div class="row g-3">
                  <!-- Public/Private Toggle (only show for non-"all" tabs) -->
                  <div v-if="activeTab !== 'all' && activeTab !== 'history' && activeTab !== 'dashboard'" class="col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_8">
                    <div class="d-flex align-items-center h-100">
                      <div class="form-check form-switch">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          id="publicToggle"
                          v-model="currentCollectionIsPublic"
                          @change="toggleCollectionPublicStatus"
                        >
                        <label class="form-check-label text-start small" for="publicToggle">
                          {{ currentCollectionIsPublic ? 'Public' : 'Private' }}
                        </label>
                      </div>
                    </div>
                  </div>

                  <!-- Drink Type Filter -->
                  <div :class="activeTab !== 'all' && activeTab !== 'history' ? 'col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_8' : 'col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_7'">
                    <select class="form-select" v-model="filters.drinkType">
                      <option value="">Any Type</option>
                      <option v-for="drinkType in drinkTypeOptions" :key="drinkType" :value="drinkType">
                        {{ drinkType }}
                      </option>
                    </select>
                  </div>

                  <!-- Type Category Filter -->
                  <div :class="activeTab !== 'all' && activeTab !== 'history' ? 'col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_8' : 'col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_7'">
                    <select class="form-select" v-model="filters.typeCategory" :disabled="!filters.drinkType">
                      <option value="">Any Category</option>
                      <option v-for="category in typeCategoryOptions" :key="category" :value="category">
                        {{ category }}
                      </option>
                    </select>
                  </div>

                  <!-- Country Filter -->
                  <div :class="activeTab !== 'all' && activeTab !== 'history' ? 'col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_8' : 'col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_7'">
                    <select class="form-select" v-model="filters.country">
                      <option value="">Any Country</option>
                      <option v-for="country in countryOptions" :key="country" :value="country">
                        {{ country }}
                      </option>
                    </select>
                  </div>

                  <!-- Vintage Filter -->
                  <div :class="activeTab !== 'all' && activeTab !== 'history' ? 'col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_8' : 'col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_7'">
                    <select class="form-select" v-model="filters.vintage">
                      <option value="">Any Vintage</option>
                      <option v-for="year in vintageOptions" :key="year" :value="year">
                        {{ year }}
                      </option>
                    </select>
                  </div>

                  <!-- Average Rating Filter -->
                  <div :class="activeTab !== 'all' && activeTab !== 'history' ? 'col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_8' : 'col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_7'">
                    <select class="form-select" v-model="filters.averageRating">
                      <option value="">Any Rating</option>
                      <option value="9">9+ Stars</option>
                      <option value="8">8+ Stars</option>
                      <option value="7">7+ Stars</option>
                      <option value="6">6+ Stars</option>
                      <option value="5">5+ Stars</option>
                    </select>
                  </div>

                  <!-- Status Filter -->
                  <div :class="activeTab !== 'all' && activeTab !== 'history' ? 'col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_8' : 'col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_7'">
                    <select class="form-select" v-model="filters.status">
                      <option value="">Any Status</option>
                      <option value="In Possession">In Cellar</option>
                      <option value="On Its Way">On Its Way</option>
                      <option value="Wishlisted">Wishlisted</option>
                      <option value="Consumed">Consumed</option>
                    </select>
                  </div>

                  <!-- Drink Now Checkbox -->
                  <div :class="activeTab !== 'all' && activeTab !== 'history' ? 'col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_8' : 'col-6 col-sm-4 col-md-2 col-lg-2 col-xl-1_7'">
                    <div class="form-check">
                      <input
                        class="form-check-input"
                        type="checkbox"
                        id="drinkNowFilter"
                        v-model="filters.drinkNow"
                      >
                      <label 
                        class="form-check-label text-start" 
                        for="drinkNowFilter"
                        style="font-size:0.8em;"
                        title="Show only bottles drinkable now (no drinking window specified, or current date is within the drinking window)"
                      >
                        Only show drink-now
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Search and View Toggle Row -->
              <div class="d-flex justify-content-between align-items-center mb-3 mx-3">
                <!-- Search Input -->
                <div class="flex-grow-1 me-3">
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

                <!-- View Toggle -->
                <!-- Mobile: Compact layout -->
                <div class="d-md-none">
                  <div class="btn-group" role="group" aria-label="View toggle">
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      :class="{ active: viewMode === 'grid' }"
                      @click="viewMode = 'grid'"
                      title="Grid View"
                    >
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                        <path d="M1 2.5A1.5 1.5 0 0 1 2.5 1h3A1.5 1.5 0 0 1 7 2.5v3A1.5 1.5 0 0 1 5.5 7h-3A1.5 1.5 0 0 1 1 5.5v-3zm8 0A1.5 1.5 0 0 1 10.5 1h3A1.5 1.5 0 0 1 15 2.5v3A1.5 1.5 0 0 1 13.5 7h-3A1.5 1.5 0 0 1 9 5.5v-3zm-8 8A1.5 1.5 0 0 1 2.5 9h3A1.5 1.5 0 0 1 7 10.5v3A1.5 1.5 0 0 1 5.5 15h-3A1.5 1.5 0 0 1 1 13.5v-3zm8 0A1.5 1.5 0 0 1 10.5 9h3a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5h-3A1.5 1.5 0 0 1 9 13.5v-3z"/>
                      </svg>
                    </button>
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      :class="{ active: viewMode === 'list' }"
                      @click="viewMode = 'list'"
                      title="List View"
                    >
                      <i class="bi bi-list-task"></i>
                    </button>
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      :class="{ active: viewMode === 'compact' }"
                      @click="viewMode = 'compact'"
                      title="Compact List View"
                    >
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                        <path fill-rule="evenodd" d="M2 2.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5zm0 3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5zm0 3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5zm0 3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5zm0 3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5z"/>
                      </svg>
                    </button>
                  </div>
                </div>
                
                <!-- Desktop: Right-aligned compact layout -->
                <div class="d-none d-md-flex">
                  <div class="btn-group" role="group" aria-label="View toggle">
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      :class="{ active: viewMode === 'grid' }"
                      @click="viewMode = 'grid'"
                      title="Grid View"
                    >
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                        <path d="M1 2.5A1.5 1.5 0 0 1 2.5 1h3A1.5 1.5 0 0 1 7 2.5v3A1.5 1.5 0 0 1 5.5 7h-3A1.5 1.5 0 0 1 1 5.5v-3zm8 0A1.5 1.5 0 0 1 10.5 1h3A1.5 1.5 0 0 1 15 2.5v3A1.5 1.5 0 0 1 13.5 7h-3A1.5 1.5 0 0 1 9 5.5v-3zm-8 8A1.5 1.5 0 0 1 2.5 9h3A1.5 1.5 0 0 1 7 10.5v3A1.5 1.5 0 0 1 5.5 15h-3A1.5 1.5 0 0 1 1 13.5v-3zm8 0A1.5 1.5 0 0 1 10.5 9h3a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5h-3A1.5 1.5 0 0 1 9 13.5v-3z"/>
                      </svg>
                    </button>
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      :class="{ active: viewMode === 'list' }"
                      @click="viewMode = 'list'"
                      title="List View"
                    >
                      <i class="bi bi-list-task"></i>
                    </button>
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      :class="{ active: viewMode === 'compact' }"
                      @click="viewMode = 'compact'"
                      title="Compact List View"
                    >
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                        <path fill-rule="evenodd" d="M2 2.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5zm0 3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5zm0 3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5zm0 3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5zm0 3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5z"/>
                      </svg>
                    </button>
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
                  <h4 class="alert-heading">Unable to Load Your Cellar</h4>
                  <p>{{ error }}</p>
                  <div class="mt-3">
                    <button class="btn btn-outline-danger me-2" @click="loadCellarData">
                      <i class="bi bi-arrow-clockwise me-1"></i>
                      Try Again
                    </button>
                    <button class="btn btn-outline-secondary" @click="clearFilters">
                      <i class="bi bi-funnel me-1"></i>
                      Clear Filters
                    </button>
                  </div>
                </div>
              </div>

              <!-- Empty State -->
              <div v-else-if="filteredItems.length === 0" class="empty-state text-center py-5">
                <div class="empty-icon mb-3">
                  🍷🍹🥃🍶🍺🍾🍸
                </div>
                <!-- Different messages for empty cellar vs filtered results -->
                <template v-if="allItems.length === 0">
                  <h3 class="mb-2">Your personal cellar is empty</h3>
                  <p class="text-muted mb-4 px-4">
                    Track your collection, manage inventory, record tasting notes, set drinking windows, and organize bottles into custom collections. Perfect for wine cellars, whiskey cabinets, sake collections, and more!
                  </p>
                  <button class="btn btn-primary" @click="toggleRightSidebar">
                    <i class="bi bi-plus-circle me-2"></i>
                    Add Your First Drink
                  </button>
                </template>
                <template v-else>
                  <h3 class="mb-2">No bottles match your filters</h3>
                  <p class="text-muted mb-4">
                    Try adjusting your search criteria to find what you're looking for.
                  </p>
                  <button class="btn btn-primary" @click="clearFilters">
                    <i class="bi bi-funnel me-2"></i>
                    Clear Filters
                  </button>
                </template>
              </div>

              <!-- Items Cards (Grid View) -->
              <div v-if="viewMode === 'grid'" class="row">
                <div 
                  v-for="group in paginatedItems" 
                  :key="`${group.listingId}_${group.variant || 'no-variant'}`"
                  :class="[
                    'col-12 mb-4',
                    rightSidebarExpanded ? 'col-md-6 col-lg-4' : 'col-md-4 col-lg-custom-5'
                  ]"
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
                    <div class="card-img-container" style="width:100%;">
                      <img 
                        :src="getItemImageUrl(group.representative)"
                        :alt="group.representative.listingName"
                        class="card-img-top"
                        @error="onImageError"
                      >
                      <!-- Combined Quantity and Volume Badge -->
                      <div class="quantity-volume-badge">
                        {{ group.bottleCount }} {{ getContainerType(group.representative.drinkFormat, group.bottleCount) }}{{ getVolumeText(group.representative) }}
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
                          <span v-if="group.representative.producerName">{{ group.representative.producerName }} | </span>{{ group.representative.drinkType }}<span v-if="group.representative.typeCategory"> | {{ group.representative.typeCategory }}</span>
                          <span> | 
                            <span style="color: #f0b358; font-weight: bold;" v-if="group.representative.averageRating">
                              {{ group.representative.averageRating }}&nbsp;★
                            </span>
                            <span style="color: #f0b358; font-weight: normal;" v-else>
                              -&nbsp;★
                            </span>
                          </span>
                        </p>

                        <!-- Status Overview -->
                        <div class="status-info mt-2">
                          <div class="status-breakdown">
                            <span 
                              v-for="(count, status) in getGroupStatusBreakdown(group.bottles)"
                              :key="status"
                              class="status-badge badge me-1 mb-2"
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
                          
                          <!-- Notes (from representative bottle) -->
                          <div 
                            class="card-notes text-muted small mt-1 border rounded p-2 position-relative d-inline-block" 
                            v-if="group.representative.noteToSelf"
                            :title="group.representative.noteToSelf"
                          >
                            <!-- Note icon -->
                            <svg class="position-absolute" style="top: 0px; right: 3px; width: 12px; height: 12px; opacity: 0.8;" viewBox="0 0 16 16" fill="#dc3545">
                              <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2z"/>
                            </svg>
                            {{ group.representative.noteToSelf }}
                          </div>
                        </div>
                      </div>

                      <!-- Hover Actions (Desktop Only) -->
                      <div class="hover-actions d-none d-lg-flex justify-content-center">
                        <button 
                          class="btn btn-sm btn-outline-primary"
                          @click.stop="consumeGroup(group)"
                          
                          disabled
                        >
                          Edit / Learn More
                        </button>

                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Items Cards (List View) -->
              <div v-else-if="viewMode === 'list'">
                <div 
                  v-for="group in paginatedItems" 
                  :key="`${group.listingId}_${group.variant || 'no-variant'}_list`"
                  class="mb-3"
                >
                  <div 
                    class="card cellar-item-list-card"
                    role="button"
                    tabindex="0"
                    data-bs-toggle="modal"
                    data-bs-target="#itemDetailsModal"
                    @click="setSelectedGroup(group)"
                    @keyup.enter="setSelectedGroup(group)"
                  >
                    <div class="row g-0">
                      <!-- Image Column (Left) -->
                      <div class="col-4 col-md-3 col-lg-2">
                        <div class="list-img-container">
                          <img 
                            :src="getItemImageUrl(group.representative)"
                            :alt="group.representative.listingName"
                            class="list-img"
                            @error="onImageError"
                          >
                        </div>
                      </div>

                      <!-- Content Column (Right) -->
                      <div class="col-8 col-md-9 col-lg-10">
                        <div class="card-body py-3">
                          <div class="row">
                            <!-- Main Info -->
                            <div class="col-12 col-lg-8">
                              <!-- Primary Line -->
                              <h6 class="card-title mb-1" :title="group.representative.listingName">
                                {{ group.representative.listingName }}
                                <span v-if="group.representative.variant" class="text-muted ms-1">
                                  ({{ group.representative.variant }})
                                </span>
                              </h6>
                              
                              <!-- Secondary Line -->
                              <p class="text-muted mb-1 small">
                                <span v-if="group.representative.producerName">{{ group.representative.producerName }} | </span>{{ group.representative.drinkType }}<span v-if="group.representative.typeCategory"> | {{ group.representative.typeCategory }}</span>
                                <span> | 
                                  <span style="color: #f0b358; font-weight: bold;" v-if="group.representative.averageRating">
                                    {{ group.representative.averageRating }} ★
                                  </span>
                                  <span style="color: #6c757d; font-weight: normal;" v-else>
                                    - ★
                                  </span>
                                </span>
                              </p>

                              <!-- Notes (truncated) -->
                              <div 
                                class="text-muted small mb-2 border rounded p-2 position-relative d-inline-block mobile-view-hide" 
                                v-if="group.representative.noteToSelf"
                                :title="group.representative.noteToSelf"
                              >
                                <!-- Note icon -->
                                <svg class="position-absolute" style="top: 0px; right: 3px; width: 12px; height: 12px; opacity: 0.8;" viewBox="0 0 16 16" fill="#dc3545">
                                  <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2z"/>
                                </svg>
                                {{ truncateText(group.representative.noteToSelf, 100) }}
                              </div>
                            </div>

                            <!-- Side Info -->
                            <div class="col-12 col-lg-4">
                              <!-- Combined Quantity and Volume Badge -->
                              <div class="mb-2">
                                <span class="quantity-volume-badge-inline">
                                  {{ group.bottleCount }} {{ getContainerType(group.representative.drinkFormat, group.bottleCount) }}{{ getVolumeText(group.representative) }}
                                </span>
                                <span 
                                  v-for="(count, status) in getGroupStatusBreakdown(group.bottles)"
                                  :key="status"
                                  class="status-badge badge me-1 small"
                                  :class="getStatusBadgeClass(status)"
                                  :title="`${count} bottle${count !== 1 ? 's' : ''} ${status.toLowerCase()}`"
                                >
                                  {{ count }}x {{ status }}
                                </span>
                              </div>


                              <!-- Drink Dates -->
                              <div class="drink-dates" v-if="group.representative.drinkByDate || group.representative.drinkOnwardsDate">
                                <small class="text-muted">
                                  <div v-if="group.representative.drinkOnwardsDate">
                                    <strong>Drink from:</strong> {{ formatDate(group.representative.drinkOnwardsDate) }}
                                  </div>
                                  <div v-if="group.representative.drinkByDate">
                                    <strong>Drink by:</strong> {{ formatDate(group.representative.drinkByDate) }}
                                  </div>
                                </small>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Items Cards (Compact List View - No Photos) -->
              <div v-else-if="viewMode === 'compact'">
                <div 
                  v-for="group in paginatedItems" 
                  :key="`${group.listingId}_${group.variant || 'no-variant'}_compact`"
                  class="mb-2"
                >
                  <div 
                    class="card cellar-item-compact-card"
                    role="button"
                    tabindex="0"
                    data-bs-toggle="modal"
                    data-bs-target="#itemDetailsModal"
                    @click="setSelectedGroup(group)"
                    @keyup.enter="setSelectedGroup(group)"
                  >
                    <div class="card-body py-2 px-3">
                      <div class="row align-items-center">
                        <!-- Main Info -->
                        <div class="col-12 col-lg-4">
                          <!-- Primary Line -->
                          <h6 class="card-title mb-1 small" :title="group.representative.listingName">
                            {{ group.representative.listingName }}
                            <span v-if="group.representative.variant" class="text-muted ms-1">
                              ({{ group.representative.variant }})
                            </span>
                          </h6>
                          
                          <!-- Secondary Line -->
                          <p class="text-muted mb-0 small">
                            <span v-if="group.representative.producerName">{{ group.representative.producerName }}</span>
                            <span v-if="group.representative.drinkType"> | {{ group.representative.drinkType }}</span>
                            <span v-if="group.representative.typeCategory"> | {{ group.representative.typeCategory }}</span>
                            <span> | 
                              <span style="color: #f0b358; font-weight: bold;" v-if="group.representative.averageRating">
                                {{ group.representative.averageRating }} ★
                              </span>
                              <span style="color: #6c757d; font-weight: normal;" v-else>
                                - ★
                              </span>
                            </span>
                          </p>
                        </div>

                        <!-- Quantity & Status Info -->
                        <div class="col-12 col-lg-4">
                          <!-- Combined Badges in One Row -->
                          <div class="d-flex flex-wrap align-items-center gap-1 justify-content-center">
                            <!-- Combined Quantity and Volume Badge -->
                            <span class="quantity-volume-badge-inline small">
                              {{ group.bottleCount }} {{ getContainerType(group.representative.drinkFormat, group.bottleCount) }}{{ getVolumeText(group.representative) }}
                            </span>

                            <!-- Status Breakdown -->
                            <span 
                              v-for="(count, status) in getGroupStatusBreakdown(group.bottles)"
                              :key="status"
                              class="status-badge badge small"
                              :class="getStatusBadgeClass(status)"
                              :title="`${count} bottle${count !== 1 ? 's' : ''} ${status.toLowerCase()}`"
                            >
                              {{ count }}x {{ status }}
                            </span>
                          </div>
                        </div>

                        <!-- Drink Dates -->
                        <div class="col-12 col-lg-2">
                          <div class="drink-dates" v-if="group.representative.drinkByDate || group.representative.drinkOnwardsDate">
                            <small class="text-muted">
                              <div v-if="group.representative.drinkOnwardsDate">
                                <strong>From:</strong> {{ formatDate(group.representative.drinkOnwardsDate) }}
                              </div>
                              <div v-if="group.representative.drinkByDate">
                                <strong>By:</strong> {{ formatDate(group.representative.drinkByDate) }}
                              </div>
                            </small>
                          </div>
                        </div>

                        <!-- Notes (Desktop - inline) -->
                        <div class="col-lg-2 d-none d-lg-block" v-if="group.representative.noteToSelf">
                          <p 
                            class="card-notes text-muted small border rounded p-1 mb-0 position-relative d-inline-block" 
                            :title="group.representative.noteToSelf"
                          >
                            <!-- Note icon -->
                            <svg class="position-absolute" style="top: 0px; right: 3px; width: 12px; height: 12px; opacity: 0.8;" viewBox="0 0 16 16" fill="#dc3545">
                              <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2z"/>
                            </svg>
                            {{ truncateText(group.representative.noteToSelf, 80) }}
                          </p>
                        </div>
                      </div>
                      
                      <!-- Notes (Mobile - separate row) -->
                      <div class="row d-lg-none mobile-view-hide" v-if="group.representative.noteToSelf">
                        <div class="col-12">
                          <p 
                            class="card-notes text-muted small mt-2 border rounded p-2 mb-0 position-relative d-inline-block" 
                            :title="group.representative.noteToSelf"
                          >
                            <!-- Note icon -->
                            <svg class="position-absolute" style="top: 0px; right: 3px; width: 12px; height: 12px; opacity: 0.8;" viewBox="0 0 16 16" fill="#dc3545">
                              <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A .5.5 0 0 1 2 15.5V2z"/>
                            </svg>
                            {{ truncateText(group.representative.noteToSelf, 150) }}
                          </p>
                        </div>
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
            </div> <!-- End collection/items tab content (v-else) -->
            </section>
          </div>

          <!-- Right Column - Add Drink to Cellar (4/12 columns) - Desktop Only -->
          <div 
            class="col-12 col-lg-4 mt-4 mt-lg-0 right-sidebar-column d-none d-lg-block" 
            :class="{ 'expanded': rightSidebarExpanded }"
          >
            <div class="right-sidebar-content">
            <div class="add-drink-to-cellar">
              <div class="card h-100" style="overflow: visible;" >
                <div class="card-header" style="width:100%;">
                  <h5 class="card-title mb-0">
                    <i class="bi bi-plus-circle me-2"></i>
                    Add Drink(s) to Cellar
                  </h5>
                </div>
                <div class="card-body" style="width:100%;">
                  <form @submit.prevent="addDrinkToCellar">
                    <!-- Producer Search -->
                    <div class="form-group mb-3">
                      <label class="form-label text-start">
                        Producer (Optional)
                        <small class="text-muted d-block text-start">Filter drink search by producer name</small>
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
                        <small class="text-muted d-block text-start">Search by drink name. If you can't find your drink on Drink-X, <router-link to="/request/new" class="text-decoration-none"> submit a new drink to the database!</router-link></small>
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
                        @focus="onDrinkSearchFocus"
                        :placeholder="addDrinkForm.selectedProducer && addDrinkForm.selectedProducer.id ? 
                          'Search drinks from ' + addDrinkForm.selectedProducer.producerName : 
                          'Enter a drink name to search...'"
                        required
                      />
                      
                      <!-- Loading spinner for drink search -->
                      <div 
                        v-if="addDrinkForm.isSearchingDrinks" 
                        class="d-flex align-items-center justify-content-center p-3 mt-1"
                      >
                        <div class="spinner-border spinner-border-sm text-primary me-2" role="status">
                          <span class="visually-hidden">Loading...</span>
                        </div>
                        <span class="text-muted">Searching drinks...</span>
                      </div>
                      
                      <ul 
                        class="list-group mt-1"
                        v-if="addDrinkForm.searchResults && addDrinkForm.searchResults.length > 0"
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

                    <!-- Simplified Form Fields -->
                    <div v-if="addDrinkForm.selectedDrink && addDrinkForm.selectedDrink.id">
                      <!-- Quantity Section -->
                      <div class="form-group mb-3">
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

                      <!-- Simplified form - only essential fields -->
                      <div v-if="!showExpandedForm" class="simplified-form">
                        <!-- Place of Purchase -->
                        <div class="form-group mb-3">
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
                                class="form-control" 
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

                        <!-- Purchase Price -->
                        <div class="form-group mb-3">
                          <label class="form-label text-start">Purchase Price</label>
                          <div class="input-group">
                            <select class="form-select" v-model="addDrinkForm.purchaseCurrency" style="max-width: 80px;">
                              <option value="USD">USD</option>
                              <option value="AUD">AUD</option>
                              <option value="CAD">CAD</option>
                              <option value="CHF">CHF</option>
                              <option value="CNY">CNY</option>
                              <option value="EUR">EUR</option>
                              <option value="GBP">GBP</option>
                              <option value="HKD">HKD</option>
                              <option value="IDR">IDR</option>
                              <option value="INR">INR</option>
                              <option value="JPY">JPY</option>
                              <option value="KRW">KRW</option>
                              <option value="MXN">MXN</option>
                              <option value="MYR">MYR</option>
                              <option value="NZD">NZD</option>
                              <option value="SGD">SGD</option>
                              <option value="THB">THB</option>
                              <option value="TWD">TWD</option>
                              <option value="VND">VND</option>
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

                        <!-- Personal Notes -->
                        <div class="form-group mb-3">
                          <label class="form-label text-start">Personal Notes</label>
                          <textarea 
                            class="form-control"
                            v-model="addDrinkForm.personalNotes"
                            @focus="onPersonalNotesFocus"
                            @blur="onPersonalNotesBlur"
                            rows="2"
                            placeholder="Add your personal notes about these bottles..."
                          ></textarea>
                        </div>

                        <!-- Collection Selection -->
                        <div class="form-group mb-3">
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

                        <!-- Show More Fields Button -->
                        <div class="form-group mb-3">
                          <button 
                            type="button" 
                            class="btn btn-outline-secondary w-100"
                            @click="toggleFormExpansion"
                          >
                            <i class="bi bi-chevron-down me-2"></i>
                            Show More Fields
                          </button>
                        </div>
                      </div>

                      <!-- Expanded form - all fields -->
                      <div v-else class="expanded-form">
                        <!-- Show Less Fields Button -->
                        <div class="form-group mb-3">
                          <button 
                            type="button" 
                            class="btn btn-outline-secondary w-100"
                            @click="toggleFormExpansion"
                          >
                            <i class="bi bi-chevron-up me-2"></i>
                            Show Less Fields
                          </button>
                        </div>

                        <!-- Group Properties Section -->
                        <div class="form-section mb-4">
                          <hr>
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
                                <option value="Carton / Pouch">Carton / Pouch</option>
                                <option value="Keg">Keg</option>
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
                                  <option value="AUD">AUD</option>
                                  <option value="CAD">CAD</option>
                                  <option value="CHF">CHF</option>
                                  <option value="CNY">CNY</option>
                                  <option value="EUR">EUR</option>
                                  <option value="GBP">GBP</option>
                                  <option value="HKD">HKD</option>
                                  <option value="IDR">IDR</option>
                                  <option value="INR">INR</option>
                                  <option value="JPY">JPY</option>
                                  <option value="KRW">KRW</option>
                                  <option value="MXN">MXN</option>
                                  <option value="MYR">MYR</option>
                                  <option value="NZD">NZD</option>
                                  <option value="SGD">SGD</option>
                                  <option value="THB">THB</option>
                                  <option value="TWD">TWD</option>
                                  <option value="VND">VND</option>
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
                                  ref="drinkOnwardsDateInput"
                                />
                                <span 
                                  class="input-group-text date-picker-trigger"
                                  @click="$refs.drinkOnwardsDateInput.showPicker()"
                                  role="button"
                                  title="Open calendar"
                                >
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
                                  ref="drinkByDateInput"
                                />
                                <span 
                                  class="input-group-text date-picker-trigger"
                                  @click="$refs.drinkByDateInput.showPicker()"
                                  role="button"
                                  title="Open calendar"
                                >
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
                                  @focus="onFoodPairingFocus"
                                  @blur="onFoodPairingBlur"
                                  placeholder="e.g., Grilled salmon, Dark chocolate"
                                />
                                <button class="btn btn-outline-secondary" type="button" disabled title="Coming soon">+</button>
                              </div>
                            </div>
                          </div>
                        </div>

                        <!-- Individual Item Properties Section -->
                        <div class="form-section mb-4">
                          <hr>
                          <!-- Row 1: Status, Consumption -->
                          <div class="row g-3 mb-3">
                            <div class="col-md-6">
                              <label class="form-label text-start">Status</label>
                              <select 
                                class="form-select"
                                v-model="addDrinkForm.status"
                              >
                                <option value="Purchased">Purchased</option>
                                <option value="In Possession">In Possession</option>
                                <option value="On Its Way">On Its Way</option>
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
                                @focus="onCurrentLocationFocus"
                                @blur="onCurrentLocationBlur"
                                placeholder="e.g., Wine fridge, Cellar rack 3"
                              />
                            </div>
                            <div class="col-md-6">
                              <label class="form-label text-start">Sub Location</label>
                              <input 
                                type="text" 
                                class="form-control"
                                v-model="addDrinkForm.subLocation"
                                @focus="onSubLocationFocus"
                                @blur="onSubLocationBlur"
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
                                    class="form-control" 
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
                                  ref="purchaseDateInput"
                                />
                                <span 
                                  class="input-group-text date-picker-trigger"
                                  @click="$refs.purchaseDateInput.showPicker()"
                                  role="button"
                                  title="Open calendar"
                                >
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
                                  ref="deliveryDateInput"
                                />
                                <span 
                                  class="input-group-text date-picker-trigger"
                                  @click="$refs.deliveryDateInput.showPicker()"
                                  role="button"
                                  title="Open calendar"
                                >
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
                                  <option value="AUD">AUD</option>
                                  <option value="CAD">CAD</option>
                                  <option value="CHF">CHF</option>
                                  <option value="CNY">CNY</option>
                                  <option value="EUR">EUR</option>
                                  <option value="GBP">GBP</option>
                                  <option value="HKD">HKD</option>
                                  <option value="IDR">IDR</option>
                                  <option value="INR">INR</option>
                                  <option value="JPY">JPY</option>
                                  <option value="KRW">KRW</option>
                                  <option value="MXN">MXN</option>
                                  <option value="MYR">MYR</option>
                                  <option value="NZD">NZD</option>
                                  <option value="SGD">SGD</option>
                                  <option value="THB">THB</option>
                                  <option value="TWD">TWD</option>
                                  <option value="VND">VND</option>
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
                                @focus="onPersonalNotesFocus"
                                @blur="onPersonalNotesBlur"
                                rows="3"
                                placeholder="Add your personal notes about these bottles..."
                              ></textarea>
                            </div>
                          </div>
                        </div>

                        <!-- Collection Selection Section -->
                        <div class="form-section mb-4">
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

            <!-- Cellar Change Log Section -->
            <div class="cellar-change-log mt-4" :class="{ 'search-results-open': isSearchResultsOpen }" >
              <div class="card h-100">
                <div class="card-header" style="width:100%;">
                  <h5 class="card-title mb-0">
                    <i class="bi bi-clock-history me-2"></i>
                    Cellar History
                  </h5>
                </div>
                <div class="card-body">
                  <!-- Loading State -->
                  <div v-if="loadingChangelog" class="text-center py-4">
                    <div class="spinner-border spinner-border-sm me-2"></div>
                    Loading changelog...
                  </div>
                  
                  <!-- Error State -->
                  <div v-else-if="changelogError" class="alert alert-danger small">
                    {{ changelogError }}
                  </div>
                  
                  <!-- Empty State -->
                  <div v-else-if="safeChangelog.length === 0" class="text-center py-4 text-muted">
                    <i class="bi bi-journal-x fs-1 mb-2 d-block"></i>
                    <p class="small mb-0">No recent changes to your cellar</p>
                  </div>
                  
                  <!-- Changelog Entries -->
                  <div v-else-if="safeChangelog.length > 0" class="changelog-entries" style="max-height: 400px;">
                    <div 
                      v-for="entry in safeChangelog" 
                      :key="entry.id || `entry-${Date.now()}-${Math.random()}`"
                      class="changelog-entry mb-3 p-3 border rounded"
                    >
                      <!-- Human-readable change description -->
                      <div class="change-description mb-2">
                        <div class="d-flex justify-content-between align-items-center">
                          <span class="text-start" v-html="formatChangelogEntry(entry)"></span>
                          <span class="badge ms-2" :class="getChangeTypeBadgeClass(entry?.changeType)">
                            {{ formatChangeType(entry?.changeType) }}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Load More Button -->
                    <div v-if="hasMoreChangelog" class="text-center mt-3">
                      <button 
                        class="btn btn-outline-secondary btn-sm"
                        @click="loadMoreChangelog"
                        :disabled="loadingMoreChangelog"
                      >
                        <span v-if="loadingMoreChangelog" class="spinner-border spinner-border-sm me-1"></span>
                        {{ loadingMoreChangelog ? 'Loading...' : 'Load More' }}
                      </button>
                    </div>
                  </div>
                  
                  <!-- Fallback Empty State -->
                  <div v-else class="text-center py-4 text-muted">
                    <i class="bi bi-journal-x fs-1 mb-2 d-block"></i>
                    <p class="small mb-0">No recent changes to your cellar</p>
                  </div>
                </div>
              </div>
            </div>
            </div> <!-- End right-sidebar-content -->
          </div>
        </div>
        
        <!-- Collapsible Tab Button -->
        <div class="right-sidebar-tab" @click="toggleRightSidebar">
          <div class="tab-content">
            <i :class="isMobile ? 'bi-chevron-left' : (rightSidebarExpanded ? 'bi-chevron-right' : 'bi-chevron-left')"></i>
            <span class="tab-text">{{ isMobile ? 'Add Drinks' : (rightSidebarExpanded ? 'Close' : 'Add Drinks') }}</span>
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
                <h5 class="modal-title mb-0 mobile-view-hide" id="itemDetailsModalLabel">
                  Item Details and Management
                </h5>
              </div>
              <div class="d-flex align-items-center gap-3">
                <div class="collection-selector" v-if="selectedGroup?.representative">
                  <select 
                    class="form-select form-select-sm collection-status-select" 
                    :value="modalEditing.selectedCollectionId || selectedGroup.representative.collectionId" 
                    @change="onCollectionChange($event.target.value)"
                    style="min-width: 220px;"
                  >
                    <option v-for="collection in collections" :key="collection.id" :value="collection.id">
                      {{ collection.id === (modalEditing.selectedCollectionId || selectedGroup.representative.collectionId) ? 'Currently In: ' : 'Move To: ' }}{{ collection.collectionName }}
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
                  <h6 class="section-header mb-3">
                    {{ selectedGroup?.representative?.listingName || 'Item Details' }}, {{ selectedGroup.representative.producerName || 'N/A' }}
                    <span v-if="selectedGroup?.representative?.variant" class="text-muted">
                      ({{ selectedGroup.representative.variant }})
                    </span>
                  </h6>
                  
                  <!-- Row 1: Bottler | Vintage | Country | Type | Category | Style -->
                  <div class="info-row mb-2">
                    <span class="info-text">
                      <strong>Bottler:</strong> <span class="text-muted">{{ selectedGroup.representative.bottlerName || 'Original Bottling' }}</span>
                      <span v-if="selectedGroup.representative.variant" class="mx-2">|</span>
                      <span v-if="selectedGroup.representative.variant">
                        <strong>Vintage:</strong> <span class="text-muted">{{ selectedGroup.representative.variant }}</span>
                      </span>
                      <template v-if="(selectedGroup.representative.variant || selectedGroup.representative.bottlerName || selectedGroup.representative.producerName) && selectedGroup.representative.originCountry"><span class="mx-2">|</span></template>
                      <template v-if="selectedGroup.representative.originCountry"><span class="text-muted">{{ selectedGroup.representative.originCountry }}</span></template>
                      <template v-if="selectedGroup.representative.originCountry && selectedGroup.representative.drinkType"><span class="mx-2">|</span></template>
                      <template v-if="selectedGroup.representative.drinkType"><span class="text-muted">{{ selectedGroup.representative.drinkType }}</span></template>
                      <template v-if="selectedGroup.representative.drinkType && selectedGroup.representative.typeCategory"><span class="mx-2">|</span></template>
                      <template v-if="selectedGroup.representative.typeCategory"><span class="text-muted">{{ selectedGroup.representative.typeCategory }}</span></template>
                      <template v-if="selectedGroup.representative.typeCategory && selectedGroup.representative.drinkStyle"><span class="mx-2">|</span></template>
                      <template v-if="selectedGroup.representative.drinkStyle"><span class="text-muted">{{ selectedGroup.representative.drinkStyle }}</span></template>
                    </span>
                  </div>

                  <!-- Row 2: Drinking Window -->
                  <div class="info-row mb-2" v-if="selectedGroup.representative.drinkOnwardsDate || selectedGroup.representative.drinkByDate">
                    <span class="info-text text-muted">
                      <strong>Drinking Window:&nbsp;</strong>
                      <template v-if="selectedGroup.representative.drinkOnwardsDate"><span class="editable-value">{{ formatDate(selectedGroup.representative.drinkOnwardsDate) }}</span></template>
                      <template v-if="selectedGroup.representative.drinkOnwardsDate && selectedGroup.representative.drinkByDate"> – </template>
                      <template v-if="selectedGroup.representative.drinkByDate"><span class="editable-value">{{ formatDate(selectedGroup.representative.drinkByDate) }}</span></template>
                    </span>
                  </div>

                  <!-- Row 3: Market Value -->
                  <div class="info-row mb-2" v-if="selectedGroup.representative.currentValueEstimation">
                    <span class="info-text text-muted">
                      <strong>Market Value:</strong> <span class="editable-value">{{ selectedGroup.representative.currentValueCurrency || 'USD' }} {{ selectedGroup.representative.currentValueEstimation }}</span>
                    </span>
                  </div>

                  <!-- Row 4: Average Purchase Price -->
                  <div class="info-row mb-2">
                    <span class="info-text text-muted">
                      <strong>Average Purchase Price:</strong> 
                      <span class="editable-value" v-if="getAveragePurchasePrice(selectedGroup).success">
                        {{ getAveragePurchasePrice(selectedGroup).currency }} {{ getAveragePurchasePrice(selectedGroup).amount }}
                      </span>
                      <span class="text-muted" v-else-if="getAveragePurchasePrice(selectedGroup).error">
                        {{ getAveragePurchasePrice(selectedGroup).error }}
                      </span>
                      <span class="text-muted" v-else>
                        No purchase prices available
                      </span>
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
                      Learn more / Review this drink!
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Drink Details -->
            <div class="drink-details-section mb-4">
              <h6 class="section-header text-start">Drink Details</h6>
              <div class="row g-3 mb-4">
                <div class="col-md-3" v-if="getMasterFieldValue('variant')">
                  <label class="form-label">Vintage</label>
                  <input 
                    type="number" 
                    class="form-control" 
                    :value="getMasterFieldValue('variant')" 
                    @input="onMasterFieldChange('variant', $event.target.value)"
                    min="1900" 
                    max="2030" 
                    readonly
                  >
                </div>
                <div :class="getMasterFieldValue('variant') ? 'col-md-3' : 'col-md-4'">
                  <label class="form-label">Format</label>
                  <select 
                    class="form-select" 
                    :value="getMasterFieldValue('drinkFormat')"
                    @change="onMasterFieldChange('drinkFormat', $event.target.value)"
                  >
                    <option value="Bottle">Bottle</option>
                    <option value="Can">Can</option>
                    <option value="Sample">Sample</option>
                    <option value="Carton / Pouch">Carton / Pouch</option>
                    <option value="Keg">Keg</option>
                  </select>
                </div>
                <div :class="getMasterFieldValue('variant') ? 'col-md-3' : 'col-md-4'">
                  <label class="form-label">Volume</label>
                  <div class="input-group">
                    <input 
                      type="number" 
                      class="form-control" 
                      :value="getMasterFieldValue('volumeNumber')" 
                      @input="onMasterFieldChange('volumeNumber', $event.target.value)"
                      step="0.1" 
                      min="0"
                    >
                    <select 
                      class="form-select volume-unit-select"
                      :value="getMasterFieldValue('volumeUnit')"
                      @change="onMasterFieldChange('volumeUnit', $event.target.value)"
                    >
                      <option value="ml" selected>ml</option>
                      <option value="oz">oz</option>
                      <option value="l">L</option>
                    </select>
                  </div>
                </div>
                <div :class="getMasterFieldValue('variant') ? 'col-md-3' : 'col-md-4'">
                  <label class="form-label">Current Market Value</label>
                  <div class="input-group">
                    <select 
                      class="form-select currency-select" 
                      :value="getMasterFieldValue('currentValueCurrency')"
                      @change="onMasterFieldChange('currentValueCurrency', $event.target.value)"
                    >
                      <option value="USD" selected>USD</option>
                      <option value="AUD">AUD</option>
                      <option value="CAD">CAD</option>
                      <option value="CHF">CHF</option>
                      <option value="CNY">CNY</option>
                      <option value="EUR">EUR</option>
                      <option value="GBP">GBP</option>
                      <option value="HKD">HKD</option>
                      <option value="IDR">IDR</option>
                      <option value="INR">INR</option>
                      <option value="JPY">JPY</option>
                      <option value="KRW">KRW</option>
                      <option value="MXN">MXN</option>
                      <option value="MYR">MYR</option>
                      <option value="NZD">NZD</option>
                      <option value="SGD">SGD</option>
                      <option value="THB">THB</option>
                      <option value="TWD">TWD</option>
                      <option value="VND">VND</option>
                    </select>
                    <input 
                      type="number" 
                      class="form-control" 
                      :value="getMasterFieldValue('currentValueEstimation')"
                      @input="onMasterFieldChange('currentValueEstimation', $event.target.value)"
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
                      type="date" 
                      class="form-control" 
                      :value="getMasterFieldValue('drinkOnwardsDate')"
                      @change="onMasterFieldChange('drinkOnwardsDate', $event.target.value)"
                      ref="modalDrinkOnwardsDateInput"
                    >
                    <span 
                      class="input-group-text date-picker-trigger"
                      @click="$refs.modalDrinkOnwardsDateInput.showPicker()"
                      role="button"
                      title="Open calendar"
                    >
                      <i class="bi bi-calendar3"></i>
                    </span>
                  </div>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Drink By Date</label>
                  <div class="input-group">
                    <input 
                      type="date" 
                      class="form-control" 
                      :value="getMasterFieldValue('drinkByDate')"
                      @change="onMasterFieldChange('drinkByDate', $event.target.value)"
                      ref="modalDrinkByDateInput"
                    >
                    <span 
                      class="input-group-text date-picker-trigger"
                      @click="$refs.modalDrinkByDateInput.showPicker()"
                      role="button"
                      title="Open calendar"
                    >
                      <i class="bi bi-calendar3"></i>
                    </span>
                  </div>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Suggested Food Pairing</label>
                  <div class="input-group">
                    <input 
                      type="text"
                      class="form-control"
                      :value="getMasterFieldValue('suggestedFoodPairing')"
                      @input="onMasterFieldChange('suggestedFoodPairing', $event.target.value)"
                      @focus="onFoodPairingFocus"
                      @blur="onFoodPairingBlur"
                      placeholder="Enter food pairing suggestion"
                    >
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
                  v-for="(bottle, index) in getVisibleBottles(selectedGroup.bottles)" 
                  :key="bottle.cellarItemId"
                  class="bottle-item p-4 mb-3 border rounded"
                  :class="{ 'bottle-consumed': bottle.status === 'Consumed' }"
                  :data-bottle-id="bottle.cellarItemId"
                  style="border-color: #0dcaf0 !important;"
                >
                  <!-- Bottle Header -->
                  <div class="row mb-3">
                    <div class="col-12">
                      <h6 class="mb-1 text-start">
                        <strong>Bottle #{{ index + 1 }}</strong>
                        <small class="text-muted ms-2">Variant Group ID: {{ bottle.variantGroupID }} | Quantity Variant ID: {{ bottle.quantityVariantID }}</small>
                        <span v-if="isNewBottle(bottle.cellarItemId)" class="badge bg-success ms-2">New</span>
                      </h6>
                    </div>
                  </div>

                  <!-- Row 1: Status, Consumption, Location, Sub Location, Notes -->
                  <div class="row g-3 mb-3">
                    <div class="col-md-2">
                      <label class="form-label small">Status</label>
                      <select 
                        class="form-select form-select-sm" 
                        :value="getBottleFieldValue(bottle.cellarItemId, 'status')"
                        @change="onBottleFieldChange(bottle.cellarItemId, 'status', $event.target.value)"
                      >
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
                      <select 
                        class="form-select form-select-sm" 
                        :value="getBottleFieldValue(bottle.cellarItemId, 'consumption')"
                        @change="onBottleFieldChange(bottle.cellarItemId, 'consumption', $event.target.value)"
                      >
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
                        :value="getBottleFieldValue(bottle.cellarItemId, 'currentLocation')" 
                        @input="onBottleFieldChange(bottle.cellarItemId, 'currentLocation', $event.target.value)"
                        @focus="onCurrentLocationFocus"
                        @blur="onCurrentLocationBlur"
                        placeholder="Location"
                      >
                    </div>
                    <div class="col-md-2">
                      <label class="form-label small">Sub Location</label>
                      <input 
                        type="text" 
                        class="form-control form-control-sm" 
                        :value="getBottleFieldValue(bottle.cellarItemId, 'subLocation')" 
                        @input="onBottleFieldChange(bottle.cellarItemId, 'subLocation', $event.target.value)"
                        @focus="onSubLocationFocus"
                        @blur="onSubLocationBlur"
                        placeholder="Sub-location"
                      >
                    </div>
                    <div class="col-md-4">
                      <label class="form-label small">Notes</label>
                      <textarea 
                        class="form-control form-control-sm" 
                        rows="2" 
                        :value="getBottleFieldValue(bottle.cellarItemId, 'noteToSelf')"
                        @input="onBottleFieldChange(bottle.cellarItemId, 'noteToSelf', $event.target.value)"
                        @focus="onPersonalNotesFocus"
                        @blur="onPersonalNotesBlur"
                        placeholder="Add notes for this bottle..."
                      ></textarea>
                    </div>
                  </div>

                  <!-- Row 2: Place of Purchase, Purchase Date, Delivery Date, Price of Purchase -->
                  <div class="row g-3 mb-3">
                    <div class="col-md-3">
                      <label class="form-label small">Place of Purchase</label>
                      <div class="purchase-location-container" style="position: relative;">
                        <div class="input-group input-group-sm">
                          <GMapAutocomplete 
                            placeholder="e.g., Wine shop, Online store, or enter manually"
                            @place_changed="setModalPurchasePlaceFromAutocomplete" 
                            @input="onModalPurchaseLocationInput"
                            @focus="onModalPurchaseLocationFocus" 
                            @blur="onModalPurchaseLocationBlur"
                            class="form-control" 
                            :ref="`modalPurchaseLocationInput_${bottle.cellarItemId}`"
                            :value="getModalPurchaseLocationInputValue(bottle.cellarItemId)"
                            :options="{ types: ['establishment'] }"
                          />
                          <span class="input-group-text" :title="getModalSelectedPurchasePlace(bottle.cellarItemId) ? 'Location selected via Google Maps' : 'Click input to search locations'">
                            <i class="bi bi-geo-alt" :class="{ 'text-success': getModalSelectedPurchasePlace(bottle.cellarItemId) }"></i>
                          </span>
                        </div>
                        
                        <!-- Location confirmation display -->
                        <div v-if="getModalSelectedPurchasePlace(bottle.cellarItemId) && getModalSelectedPurchaseAddress(bottle.cellarItemId)" 
                             class="alert alert-success mt-1 mb-0 small p-2">
                          📍 Selected: {{ getModalSelectedPurchasePlace(bottle.cellarItemId) }}
                          <br>
                          <small class="text-muted">{{ getModalSelectedPurchaseAddress(bottle.cellarItemId) }}</small>
                          <button 
                            type="button" 
                            class="btn btn-sm btn-outline-danger ms-2"
                            @click="clearModalSelectedPurchaseLocation(bottle.cellarItemId)"
                            style="font-size: 0.7rem; padding: 0.125rem 0.25rem;"
                          >
                            Clear
                          </button>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <label class="form-label small">Date of Purchase</label>
                      <div class="input-group input-group-sm">
                        <input 
                          type="date" 
                          class="form-control" 
                          :value="getBottleFieldValue(bottle.cellarItemId, 'purchaseDate')"
                          @change="onBottleFieldChange(bottle.cellarItemId, 'purchaseDate', $event.target.value)"
                          :ref="`bottlePurchaseDate${index}`"
                        >
                        <span 
                          class="input-group-text date-picker-trigger"
                          @click="$refs[`bottlePurchaseDate${index}`][0].showPicker()"
                          role="button"
                          title="Open calendar"
                        >
                          <i class="bi bi-calendar3"></i>
                        </span>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <label class="form-label small">Delivery Date</label>
                      <div class="input-group input-group-sm">
                        <input 
                          type="date" 
                          class="form-control" 
                          :value="getBottleFieldValue(bottle.cellarItemId, 'deliveryDate')"
                          @change="onBottleFieldChange(bottle.cellarItemId, 'deliveryDate', $event.target.value)"
                          :ref="`bottleDeliveryDate${index}`"
                        >
                        <span 
                          class="input-group-text date-picker-trigger"
                          @click="$refs[`bottleDeliveryDate${index}`][0].showPicker()"
                          role="button"
                          title="Open calendar"
                        >
                          <i class="bi bi-calendar3"></i>
                        </span>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <label class="form-label small">Price of Purchase</label>
                      <div class="input-group input-group-sm">
                        <select 
                          class="form-select currency-select" 
                          :value="getBottleFieldValue(bottle.cellarItemId, 'purchaseCurrency')"
                          @change="onBottleFieldChange(bottle.cellarItemId, 'purchaseCurrency', $event.target.value)"
                        >
                          <option value="USD" selected>USD</option>
                          <option value="AUD">AUD</option>
                          <option value="CAD">CAD</option>
                          <option value="CHF">CHF</option>
                          <option value="CNY">CNY</option>
                          <option value="EUR">EUR</option>
                          <option value="GBP">GBP</option>
                          <option value="HKD">HKD</option>
                          <option value="IDR">IDR</option>
                          <option value="INR">INR</option>
                          <option value="JPY">JPY</option>
                          <option value="KRW">KRW</option>
                          <option value="MXN">MXN</option>
                          <option value="MYR">MYR</option>
                          <option value="NZD">NZD</option>
                          <option value="SGD">SGD</option>
                          <option value="THB">THB</option>
                          <option value="TWD">TWD</option>
                          <option value="VND">VND</option>
                        </select>
                        <input 
                          type="number" 
                          class="form-control" 
                          :value="getBottleFieldValue(bottle.cellarItemId, 'purchasePrice')"
                          @input="onBottleFieldChange(bottle.cellarItemId, 'purchasePrice', $event.target.value)"
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
                  <button 
                    class="btn btn-sm btn-outline-secondary dropdown-toggle" 
                    type="button" 
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                    id="groupActionsDropdown"
                    data-bs-auto-close="true"
                    @click="toggleGroupActionsDropdown"
                  >
                    <i class="bi bi-three-dots"></i> Group Actions
                  </button>
                  <ul class="dropdown-menu" aria-labelledby="groupActionsDropdown">
                    <li><a class="dropdown-item" href="#" @click.prevent="markAllBottlesInPossession()">
                      <i class="bi bi-house-check"></i> All In Possession
                    </a></li>
                    <li><a class="dropdown-item" href="#" @click.prevent="consumeBottle()">
                      <i class="bi bi-cup-straw"></i> All Consumed
                    </a></li>
                    <li><a class="dropdown-item" href="#" @click.prevent="markAllBottlesEmpty()">
                      <i class="bi bi-droplet"></i> All Empty
                    </a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item text-danger" href="#" @click.prevent="archiveGroup">
                      <i class="bi bi-archive"></i> Archive All
                    </a></li>
                  </ul>
                </div>
              </div>

              <!-- Right side: Close and Save -->
              <div class="close-save-buttons">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-primary" @click="saveModalChanges" :disabled="!modalEditing.hasChanges">
                  <i class="bi bi-check-lg"></i> Save Changes
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Collection Modal -->
    <div 
      class="modal fade" 
      id="addCollectionModal" 
      tabindex="-1" 
      aria-labelledby="addCollectionModalLabel" 
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header text-start">
            <h5 class="modal-title" id="addCollectionModalLabel">Add New Collection</h5>
            <button 
              type="button" 
              class="btn-close" 
              data-bs-dismiss="modal" 
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body text-start">
            <form @submit.prevent="createNewCollection">
              <div class="mb-3">
                <label for="newCollectionName" class="form-label">Collection Name <span class="text-danger">*</span></label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="newCollectionName"
                  v-model="newCollectionForm.collectionName"
                  :class="{ 'is-invalid': newCollectionForm.errors.collectionName }"
                  placeholder="Enter collection name..."
                  maxlength="255"
                  required
                >
                <div v-if="newCollectionForm.errors.collectionName" class="invalid-feedback">
                  {{ newCollectionForm.errors.collectionName }}
                </div>
                <div class="form-text">
                  Create a custom collection to organize your bottles (e.g., "Special Occasions", "Daily Drinkers", "Vintage Collection")
                </div>
              </div>

              <div class="mb-3">
                <div class="form-check">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    id="newCollectionIsPublic"
                    v-model="newCollectionForm.isPublic"
                  >
                  <label class="form-check-label" for="newCollectionIsPublic">
                    Make this collection public
                  </label>
                  <div class="form-text">
                    Public collections can be viewed by other users (feature coming soon)
                  </div>
                </div>
              </div>

              <!-- <div class="mb-3">
                <div class="form-check">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    id="newCollectionIsDefault"
                    v-model="newCollectionForm.isDefault"
                  >
                  <label class="form-check-label" for="newCollectionIsDefault">
                    Set as default collection
                  </label>
                  <div class="form-text">
                    New bottles will be added to the default collection when no specific collection is selected
                  </div>
                </div>
              </div> -->

              <div v-if="newCollectionForm.error" class="alert alert-danger" role="alert">
                {{ newCollectionForm.error }}
              </div>

              <div v-if="newCollectionForm.success" class="alert alert-success" role="alert">
                {{ newCollectionForm.success }}
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button 
              type="button" 
              class="btn btn-primary" 
              @click="createNewCollection"
              :disabled="newCollectionForm.loading || !newCollectionForm.collectionName.trim()"
            >
              <span v-if="newCollectionForm.loading" class="spinner-border spinner-border-sm me-2"></span>
              {{ newCollectionForm.loading ? 'Creating...' : 'Create Collection' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Food Pairing Suggestions Dropdown -->
    <div 
      id="foodPairingDropdown"
      v-if="showFoodPairingSuggestions && (foodPairingSuggestions.length > 0 || loadingFoodPairings)"
      class="food-pairing-dropdown"
      style="position: absolute; background: white; border: 1px solid #dee2e6; border-radius: 0.375rem; box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); max-height: 200px; overflow-y: auto; z-index: 1050;"
    >
      <!-- Loading state -->
      <div v-if="loadingFoodPairings" class="p-3 text-center text-muted">
        <div class="spinner-border spinner-border-sm me-2"></div>
        Loading suggestions...
      </div>
      
      <!-- No suggestions -->
      <div v-else-if="foodPairingSuggestions.length === 0" class="p-3 text-center text-muted">
        No previous food pairings found
      </div>
      
      <!-- Suggestions list -->
      <div v-else>
        <div 
          v-for="(suggestion, index) in foodPairingSuggestions" 
          :key="index"
          class="food-pairing-suggestion-item p-2 cursor-pointer"
          style="border-bottom: 1px solid #f1f3f4; cursor: pointer;"
          @click="selectFoodPairingSuggestion(suggestion)"
          @mouseenter="$event.target.style.backgroundColor = '#f8f9fa'"
          @mouseleave="$event.target.style.backgroundColor = 'white'"
        >
          {{ suggestion }}
        </div>
      </div>
    </div>

    <!-- Current Location Suggestions Dropdown -->
    <div 
      id="currentLocationDropdown"
      v-if="showCurrentLocationSuggestions && (currentLocationSuggestions.length > 0 || loadingCurrentLocations)"
      class="current-location-dropdown"
      style="position: absolute; background: white; border: 1px solid #dee2e6; border-radius: 0.375rem; box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); max-height: 200px; overflow-y: auto; z-index: 1050;"
    >
      <!-- Loading state -->
      <div v-if="loadingCurrentLocations" class="p-3 text-center text-muted">
        <div class="spinner-border spinner-border-sm me-2"></div>
        Loading suggestions...
      </div>
      
      <!-- No suggestions -->
      <div v-else-if="currentLocationSuggestions.length === 0" class="p-3 text-center text-muted">
        No previous storage locations found
      </div>
      
      <!-- Suggestions list -->
      <div v-else>
        <div 
          v-for="(suggestion, index) in currentLocationSuggestions" 
          :key="index"
          class="current-location-suggestion-item p-2 cursor-pointer"
          style="border-bottom: 1px solid #f1f3f4; cursor: pointer;"
          @click="selectCurrentLocationSuggestion(suggestion)"
          @mouseenter="$event.target.style.backgroundColor = '#f8f9fa'"
          @mouseleave="$event.target.style.backgroundColor = 'white'"
        >
          {{ suggestion }}
        </div>
      </div>
    </div>

    <!-- Sub Location Suggestions Dropdown -->
    <div 
      id="subLocationDropdown"
      v-if="showSubLocationSuggestions && (subLocationSuggestions.length > 0 || loadingSubLocations)"
      class="sub-location-dropdown"
      style="position: absolute; background: white; border: 1px solid #dee2e6; border-radius: 0.375rem; box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); max-height: 200px; overflow-y: auto; z-index: 1050;"
    >
      <!-- Loading state -->
      <div v-if="loadingSubLocations" class="p-3 text-center text-muted">
        <div class="spinner-border spinner-border-sm me-2"></div>
        Loading suggestions...
      </div>
      
      <!-- No suggestions -->
      <div v-else-if="subLocationSuggestions.length === 0" class="p-3 text-center text-muted">
        No previous sub locations found
      </div>
      
      <!-- Suggestions list -->
      <div v-else>

        <div 
          v-for="(suggestion, index) in subLocationSuggestions" 
          :key="index"
          class="sub-location-suggestion-item p-2 cursor-pointer"
          style="border-bottom: 1px solid #f1f3f4; cursor: pointer;"
          @click="selectSubLocationSuggestion(suggestion)"
          @mouseenter="$event.target.style.backgroundColor = '#f8f9fa'"
          @mouseleave="$event.target.style.backgroundColor = 'white'"
        >
          {{ suggestion }}
        </div>
      </div>
    </div>

    <!-- Personal Notes Suggestions Dropdown -->
    <div 
      id="personalNotesDropdown"
      v-if="showPersonalNotesSuggestions && (personalNotesSuggestions.length > 0 || loadingPersonalNotes)"
      class="personal-notes-dropdown"
      style="position: absolute; background: white; border: 1px solid #dee2e6; border-radius: 0.375rem; box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); max-height: 200px; overflow-y: auto; z-index: 1050;"
    >
      <!-- Loading state -->
      <div v-if="loadingPersonalNotes" class="p-3 text-center text-muted">
        <div class="spinner-border spinner-border-sm me-2"></div>
        Loading suggestions...
      </div>
      
      <!-- No suggestions -->
      <div v-else-if="personalNotesSuggestions.length === 0" class="p-3 text-center text-muted">
        No previous personal notes found
      </div>
      
      <!-- Suggestions list -->
      <div v-else>
        <div class="p-2 border-bottom bg-light">
          <small class="text-muted fw-bold">Your Previous Personal Notes</small>
        </div>
        <div 
          v-for="(suggestion, index) in personalNotesSuggestions" 
          :key="index"
          class="personal-notes-suggestion-item p-2 cursor-pointer"
          style="border-bottom: 1px solid #f1f3f4; cursor: pointer;"
          @click="selectPersonalNotesSuggestion(suggestion)"
          @mouseenter="$event.target.style.backgroundColor = '#f8f9fa'"
          @mouseleave="$event.target.style.backgroundColor = 'white'"
        >
          {{ suggestion }}
        </div>
      </div>
    </div>
  </main>

  <!-- Mobile Add Drinks Modal -->
  <div 
    class="modal fade" 
    id="mobileAddDrinksModal" 
    tabindex="-1" 
    aria-labelledby="mobileAddDrinksModalLabel" 
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header" style="background: linear-gradient(135deg, rgb(0, 123, 255), rgb(0, 86, 179)); color:white;" >
          <h5 class="modal-title" id="mobileAddDrinksModalLabel">
            <i class="bi bi-plus-circle me-2"></i>
            Add Drink(s) to Cellar
          </h5>
          <button 
            type="button" 
            class="btn-close" 
            data-bs-dismiss="modal" 
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <!-- This contains the exact same content as the right sidebar -->
          <div class="add-drink-to-cellar-mobile">
            <form @submit.prevent="addDrinkToCellar">
              <!-- Producer Search -->
              <div class="form-group mb-3 text-start">
                <label class="form-label text-start">
                  Producer (Optional)
                  <small class="text-muted d-block text-start">Filter drink search by producer name</small>
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
              <div class="form-group mb-3 text-start">
                <label class="form-label text-start">
                  Drink Name <span class="text-danger">*</span>
                  <small class="text-muted d-block text-start">Search by drink name. If you can't find your drink on Drink-X, 
                    <router-link to="/request/new" class="text-decoration-none">
                      submit a new drink to the database!
                    </router-link></small>                   
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
                  @focus="onDrinkSearchFocus"
                  :placeholder="addDrinkForm.selectedProducer && addDrinkForm.selectedProducer.id ? 
                    'Search drinks from ' + addDrinkForm.selectedProducer.producerName : 
                    'Enter a drink name to search...'"
                  required
                />
                
                <!-- Loading spinner for drink search -->
                <div 
                  v-if="addDrinkForm.isSearchingDrinks" 
                  class="d-flex align-items-center justify-content-center p-3 mt-1"
                >
                  <div class="spinner-border spinner-border-sm text-primary me-2" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <span class="text-muted">Searching drinks...</span>
                </div>
                
                <ul 
                  class="list-group mt-1"
                  v-if="addDrinkForm.searchResults && addDrinkForm.searchResults.length > 0"
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
                
                <!-- Mobile Preview -->
                <div class="row">
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

              <!-- Mobile Simplified Form Fields -->
              <div v-if="addDrinkForm.selectedDrink && addDrinkForm.selectedDrink.id">
                <!-- Simplified form - only essential fields -->
                <div v-if="!showExpandedForm" class="simplified-form">
                  <!-- Place of Purchase -->
                  <div class="form-group mb-3">
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
                          class="form-control" 
                          ref="mobilePurchaseLocationInput" 
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

                  <!-- Purchase Price -->
                  <div class="form-group mb-3">
                    <label class="form-label text-start">Purchase Price</label>
                    <div class="input-group">
                      <select class="form-select" v-model="addDrinkForm.purchaseCurrency" style="max-width: 80px;">
                        <option value="USD">USD</option>
                        <option value="AUD">AUD</option>
                        <option value="CAD">CAD</option>
                        <option value="CHF">CHF</option>
                        <option value="CNY">CNY</option>
                        <option value="EUR">EUR</option>
                        <option value="GBP">GBP</option>
                        <option value="HKD">HKD</option>
                        <option value="IDR">IDR</option>
                        <option value="INR">INR</option>
                        <option value="JPY">JPY</option>
                        <option value="KRW">KRW</option>
                        <option value="MXN">MXN</option>
                        <option value="MYR">MYR</option>
                        <option value="NZD">NZD</option>
                        <option value="SGD">SGD</option>
                        <option value="THB">THB</option>
                        <option value="TWD">TWD</option>
                        <option value="VND">VND</option>
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

                  <!-- Personal Notes -->
                  <div class="form-group mb-3">
                    <label class="form-label text-start">Personal Notes</label>
                    <textarea 
                      class="form-control"
                      v-model="addDrinkForm.personalNotes"
                      @focus="onPersonalNotesFocus"
                      @blur="onPersonalNotesBlur"
                      rows="2"
                      placeholder="Add your personal notes about these bottles..."
                    ></textarea>
                  </div>

                  <!-- Collection Selection -->
                  <div class="form-group mb-3">
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

                  <!-- Show More Fields Button -->
                  <div class="form-group mb-3">
                    <button 
                      type="button" 
                      class="btn btn-outline-secondary w-100"
                      @click="toggleFormExpansion"
                    >
                      <i class="bi bi-chevron-down me-2"></i>
                      Show More Fields
                    </button>
                  </div>
                </div>

                <!-- Expanded form - all fields -->
                <div v-else class="expanded-form">
                  <!-- Show Less Fields Button -->
                  <div class="form-group mb-3">
                    <button 
                      type="button" 
                      class="btn btn-outline-secondary w-100"
                      @click="toggleFormExpansion"
                    >
                      <i class="bi bi-chevron-up me-2"></i>
                      Show Less Fields
                    </button>
                  </div>

                  <!-- Group Properties Section -->
                  <div class="form-section mb-4">
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
                          <option value="Carton / Pouch">Carton / Pouch</option>
                          <option value="Keg">Keg</option>
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
                            <option value="AUD">AUD</option>
                            <option value="CAD">CAD</option>
                            <option value="CHF">CHF</option>
                            <option value="CNY">CNY</option>
                            <option value="EUR">EUR</option>
                            <option value="GBP">GBP</option>
                            <option value="HKD">HKD</option>
                            <option value="IDR">IDR</option>
                            <option value="INR">INR</option>
                            <option value="JPY">JPY</option>
                            <option value="KRW">KRW</option>
                            <option value="MXN">MXN</option>
                            <option value="MYR">MYR</option>
                            <option value="NZD">NZD</option>
                            <option value="SGD">SGD</option>
                            <option value="THB">THB</option>
                            <option value="TWD">TWD</option>
                            <option value="VND">VND</option>
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
                            ref="mobiledrinkOnwardsDateInput"
                          />
                          <span 
                            class="input-group-text date-picker-trigger"
                            @click="$refs.mobiledrinkOnwardsDateInput.showPicker()"
                            role="button"
                            title="Open calendar"
                          >
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
                            ref="mobiledrinkByDateInput"
                          />
                          <span 
                            class="input-group-text date-picker-trigger"
                            @click="$refs.mobiledrinkByDateInput.showPicker()"
                            role="button"
                            title="Open calendar"
                          >
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
                            @focus="onFoodPairingFocus"
                            @blur="onFoodPairingBlur"
                            placeholder="e.g., Grilled salmon, Dark chocolate"
                          />
                          <button class="btn btn-outline-secondary" type="button" disabled title="Coming soon">+</button>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Individual Item Properties Section -->
                  <div class="form-section mb-4">
                    <hr>
                    <h6 class="section-header text-start mb-3">
                      <i class="bi bi-bottle me-2"></i>
                      Individual Items
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
                          <option value="Purchased">Purchased</option>
                          <option value="In Possession">In Possession</option>
                          <option value="On Its Way">On Its Way</option>
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
                          @focus="onCurrentLocationFocus"
                          @blur="onCurrentLocationBlur"
                          placeholder="e.g., Wine fridge, Cellar rack 3"
                        />
                      </div>
                      <div class="col-md-6">
                        <label class="form-label text-start">Sub Location</label>
                        <input 
                          type="text" 
                          class="form-control"
                          v-model="addDrinkForm.subLocation"
                          @focus="onSubLocationFocus"
                          @blur="onSubLocationBlur"
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
                              class="form-control" 
                              ref="mobilePurchaseLocationInput" 
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
                            ref="mobilePurchaseDateInput"
                          />
                          <span 
                            class="input-group-text date-picker-trigger"
                            @click="$refs.mobilePurchaseDateInput.showPicker()"
                            role="button"
                            title="Open calendar"
                          >
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
                            ref="mobileDeliveryDateInput"
                          />
                          <span 
                            class="input-group-text date-picker-trigger"
                            @click="$refs.mobileDeliveryDateInput.showPicker()"
                            role="button"
                            title="Open calendar"
                          >
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
                            <option value="AUD">AUD</option>
                            <option value="CAD">CAD</option>
                            <option value="CHF">CHF</option>
                            <option value="CNY">CNY</option>
                            <option value="EUR">EUR</option>
                            <option value="GBP">GBP</option>
                            <option value="HKD">HKD</option>
                            <option value="IDR">IDR</option>
                            <option value="INR">INR</option>
                            <option value="JPY">JPY</option>
                            <option value="KRW">KRW</option>
                            <option value="MXN">MXN</option>
                            <option value="MYR">MYR</option>
                            <option value="NZD">NZD</option>
                            <option value="SGD">SGD</option>
                            <option value="THB">THB</option>
                            <option value="TWD">TWD</option>
                            <option value="VND">VND</option>
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
                          @focus="onPersonalNotesFocus"
                          @blur="onPersonalNotesBlur"
                          rows="3"
                          placeholder="Add your personal notes about these bottles..."
                        ></textarea>
                      </div>
                    </div>
                  </div>

                  <!-- Collection Selection Section -->
                  <div class="form-section mb-4">
                    <!-- <hr>
                    <h6 class="section-header text-start mb-3">
                      <i class="bi bi-collection me-2"></i>
                      Collection Selection
                      <small class="text-muted d-block fw-normal">Choose which collection to add these bottles to.</small>
                    </h6> -->

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

</template>

<script>
import axios from 'axios'
import NavBar from '@/components/NavBar.vue'
import { Modal, Dropdown } from 'bootstrap'
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
      
      // Responsive state
      isMobile: false,
      
      // Tabs and collections
      activeTab: 'all',
      collections: [],
      currentCollectionIsPublic: false,
      
      // Mobile UI states
      mobileFiltersCollapsed: true, // Start collapsed on mobile
      
      // Items and filtering
      allItems: [],
      searchQuery: '',
      filters: {
        vintage: '',
        drinkType: '',
        typeCategory: '',
        country: '',
        averageRating: '',
        status: '',
        drinkNow: false
      },
      
      // Pagination
      currentPage: 1,
      itemsPerPage: 24,
      
      // Modal states
      selectedGroup: null,
      
      // New Collection form
      newCollectionForm: {
        collectionName: '',
        isPublic: true,
        isDefault: false,
        loading: false,
        error: null,
        success: null,
        errors: {
          collectionName: null
        }
      },
      
      // Dashboard data
      dashboardData: null,
      loadingDashboard: false,
      dashboardError: null,
      
      // Search debouncing
      searchTimeout: null,

      // View mode for grid/list toggle
      viewMode: 'grid',

      // Right sidebar state
      rightSidebarExpanded: false,

      // Modal editing states
      modalEditing: {
        hasChanges: false,
        masterData: {}, // Stores original master record data for comparison
        bottleChanges: {}, // Stores changes for individual bottles { bottleId: { field: newValue } }
        archivedBottles: new Set(), // Track bottles marked for archiving
        newBottles: [], // Track new bottles added to the group
        collectionChange: null, // Track collection changes
        pendingCollectionId: null, // Track collection dropdown selection
      },

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
        isSearchingDrinks: false,
        
        // Group properties (applied to all items in the drink group)
        vintage: null,
        format: 'Bottle', // Default fallback, will be updated when drink is selected
        volumeNumber: 700, // Default fallback, will be updated when drink is selected
        volumeUnit: 'ml', // Default fallback, will be updated when drink is selected
        currentValueEstimation: null,
        currentValueCurrency: 'USD',
        drinkOnwardsDate: null,
        drinkByDate: null,
        suggestedFoodPairing: '',
        
        // Individual item properties (applied to each bottle)
        quantity: 1,
        status: 'Purchased',
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
      
      // Form expansion state
      showExpandedForm: false,
      
      // Modal purchase location tracking
      currentModalPurchaseBottleId: null,
      
      // Food pairing suggestions
      foodPairingSuggestions: [],
      loadingFoodPairings: false,
      showFoodPairingSuggestions: false,
      activeFoodPairingInput: null,
      
      // Current location suggestions
      currentLocationSuggestions: [],
      loadingCurrentLocations: false,
      showCurrentLocationSuggestions: false,
      activeCurrentLocationInput: null,
      
      // Sub location suggestions
      subLocationSuggestions: [],
      loadingSubLocations: false,
      showSubLocationSuggestions: false,
      activeSubLocationInput: null,
      
      // Personal notes suggestions
      personalNotesSuggestions: [],
      loadingPersonalNotes: false,
      showPersonalNotesSuggestions: false,
      activePersonalNotesInput: null,
      
      // Cellar changelog
      changelog: [],
      loadingChangelog: false,
      changelogError: null,
      loadingMoreChangelog: false,
      hasMoreChangelog: true,
      changelogLimit: 10,
      changelogOffset: 0,
      
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
      
      // Drink type filter
      if (this.filters.drinkType) {
        groups = groups.filter(group => group.representative.drinkType === this.filters.drinkType)
      }
      
      // Type category filter (only active when drink type is selected)
      if (this.filters.typeCategory && this.filters.drinkType) {
        groups = groups.filter(group => group.representative.typeCategory === this.filters.typeCategory)
      }
      
      // Country filter
      if (this.filters.country) {
        groups = groups.filter(group => group.representative.originCountry === this.filters.country)
      }
      
      // Average rating filter
      if (this.filters.averageRating) {
        const minRating = parseFloat(this.filters.averageRating)
        groups = groups.filter(group => {
          const rating = group.representative.averageRating || 0
          return rating >= minRating
        })
      }
      
      // Size filter (commented out)
      // if (this.filters.size) {
      //   groups = groups.filter(group => group.representative.volumeNumber == this.filters.size)
      // }
      
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
            // If no drinking window is specified, consider it drinkable now
            if (!bottle.drinkOnwardsDate && !bottle.drinkByDate) return true
            
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

    // Drink type options for filter dropdown
    drinkTypeOptions() {
      const drinkTypes = new Set()
      this.allItems.forEach(item => {
        if (item.drinkType) {
          drinkTypes.add(item.drinkType)
        }
      })
      return Array.from(drinkTypes).sort()
    },

    // Type category options for filter dropdown (only shows categories for selected drink type)
    typeCategoryOptions() {
      if (!this.filters.drinkType) {
        return []
      }
      
      const categories = new Set()
      this.allItems.forEach(item => {
        if (item.drinkType === this.filters.drinkType && item.typeCategory) {
          categories.add(item.typeCategory)
        }
      })
      return Array.from(categories).sort()
    },

    // Country options for filter dropdown
    countryOptions() {
      const countries = new Set()
      this.allItems.forEach(item => {
        if (item.originCountry) {
          countries.add(item.originCountry)
        }
      })
      return Array.from(countries).sort()
    },

    // Form validation for add to cellar
    canAddToCellar() {
      const hasSelectedDrink = this.addDrinkForm.selectedDrink && this.addDrinkForm.selectedDrink.id;
      const hasValidQuantity = this.addDrinkForm.quantity > 0;
      return hasSelectedDrink && hasValidQuantity;
    },

    // Conditional defaults based on drinkType
    defaultFormat() {
      if (!this.addDrinkForm.selectedDrink || !this.addDrinkForm.selectedDrink.drinkType) {
        return 'Bottle'; // Fallback default
      }
      
      const drinkType = this.addDrinkForm.selectedDrink.drinkType.toLowerCase();
      
      if (drinkType === 'beer') {
        return 'Can';
      }
      // For Wine, Sake, and any other drinkType
      return 'Bottle';
    },

    defaultVolumeNumber() {
      if (!this.addDrinkForm.selectedDrink || !this.addDrinkForm.selectedDrink.drinkType) {
        return 700; // Fallback default for any other drinkType
      }
      
      const drinkType = this.addDrinkForm.selectedDrink.drinkType.toLowerCase();
      
      if (drinkType === 'beer') {
        return 355;
      } else if (drinkType === 'wine') {
        return 750;
      } else if (drinkType === 'sake') {
        return 720;
      }
      // Any other drinkType
      return 700;
    },

    defaultVolumeUnit() {
      // All drink types use 'ml' as default
      return 'ml';
    },

    // Safe changelog array to prevent null reference errors
    safeChangelog() {
      return Array.isArray(this.changelog) ? this.changelog : [];
    },

    // Check if search results dropdown is open
    isSearchResultsOpen() {
      return this.addDrinkForm.searchResults && 
             this.addDrinkForm.searchResults.length > 0 && 
             this.addDrinkForm.searchQuery;
    }
  },
  created() {
    // Ensure data properties are properly initialized
    if (!Array.isArray(this.changelog)) {
      this.changelog = [];
    }
    
    // Defensive initialization of other critical properties
    if (!this.ownerType || !this.id) {
      console.warn('Component created without required props:', {
        ownerType: this.ownerType,
        id: this.id,
        username: this.username
      });
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
    },

    // Watch for changes to selectedDrink to apply conditional defaults
    'addDrinkForm.selectedDrink': {
      handler(newDrink, oldDrink) {
        // Only apply defaults if we actually have a new drink with a drinkType
        if (newDrink && newDrink.id && newDrink.drinkType && 
            (!oldDrink || oldDrink.id !== newDrink.id)) {
          console.log('TZHFrontendLog: selectedDrink changed, applying conditional defaults for drinkType:', newDrink.drinkType);
          this.applyDrinkTypeDefaults();
        }
      },
      deep: true
    },

    // Watch for changes to drink type filter to clear type category
    'filters.drinkType'(newType, oldType) {
      if (newType !== oldType) {
        this.filters.typeCategory = ''
      }
    }
  },
  async mounted() {
    try {
      // Check if user is authenticated and authorized to view this cellar
      const currentUserId = localStorage.getItem("88B_accID");
      const currentUserType = localStorage.getItem("88B_accType");
      const currentUsername = localStorage.getItem("88B_accUsername");
      
      // If not logged in, redirect to login
      if (!currentUserId || !currentUserType) {
        this.$router.push('/login');
        return;
      }
      
      // Check if the current user is trying to access their own cellar
      const isOwnCellar = (
        currentUserType === this.ownerType &&
        currentUserId === this.id &&
        currentUsername === this.username
      );
      
      // If not their own cellar, redirect to their own cellar or show error
      if (!isOwnCellar) {
        // Redirect to their own cellar based on their account type
        const ownCellarPath = `/my-cellar/${currentUserType}/${currentUserId}/${currentUsername}`;
        this.$router.push(ownCellarPath);
        return;
      }
      
      // Set initial responsive state
      this.isMobile = window.innerWidth < 992;
      this.rightSidebarExpanded = false;
      
      // Add resize listener for responsive behavior
      this.handleResize = () => {
        this.isMobile = window.innerWidth < 992;
      };
      window.addEventListener('resize', this.handleResize);
      
      // Ensure component is fully initialized
      await this.$nextTick();
      
      // Validate required props
      if (!this.ownerType || !this.id) {
        console.error('Missing required props:', { ownerType: this.ownerType, id: this.id });
        return;
      }
      
      await this.loadCellarData();
      
      // Initialize collection public status toggle
      if (this.activeTab !== 'all' && this.activeTab !== 'history') {
        const collection = this.collections.find(c => c.id === this.activeTab)
        if (collection) {
          this.currentCollectionIsPublic = collection.isPublic || false
        }
      }
      
      // Load changelog after cellar data is loaded, with additional safety
      try {
        await this.loadChangelogData();
      } catch (changelogError) {
        console.error('Error loading changelog specifically:', changelogError);
        // Don't fail the entire component if changelog fails
        this.changelog = [];
        this.changelogError = 'Failed to load changelog';
      }
    } catch (error) {
      console.error('Error in mounted hook:', error);
    }
    
    // Add event listener for modal close to reset form
    const addCollectionModal = document.getElementById('addCollectionModal');
    if (addCollectionModal) {
      addCollectionModal.addEventListener('hidden.bs.modal', () => {
        this.resetNewCollectionForm();
      });
    }
  },
  beforeUnmount() {
    // Remove resize listener
    if (this.handleResize) {
      window.removeEventListener('resize', this.handleResize);
    }
    
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

    // Clean up modal event listeners
    const addCollectionModal = document.getElementById('addCollectionModal');
    if (addCollectionModal) {
      addCollectionModal.removeEventListener('hidden.bs.modal', this.resetNewCollectionForm);
    }
    
    // Hide food pairing suggestions
    this.showFoodPairingSuggestions = false
    this.activeFoodPairingInput = null
    
    // Hide current location suggestions
    this.showCurrentLocationSuggestions = false
    this.activeCurrentLocationInput = null
    
    // Hide sub location suggestions
    this.showSubLocationSuggestions = false
    this.activeSubLocationInput = null
    
    // Hide personal notes suggestions
    this.showPersonalNotesSuggestions = false
    this.activePersonalNotesInput = null
  },
  methods: {
    
    slugify(text) {
      return text
        .toString()
        .toLowerCase()
        .normalize('NFD') // Decompose accented characters
        .replace(/[\u0300-\u036f]/g, '') // Remove diacritical marks
        .replace(/\s+/g, '-')                 // Replace spaces with hyphens
        .replace(/[^\w]/g, ''); // Remove non-word characters
    },
    
    // Utility method to get the correct API base URL
    getApiBaseUrl() {
      return process.env.VUE_APP_API_URL || (process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '');
    },

    // Right sidebar toggle
    toggleRightSidebar() {
      if (this.isMobile) {
        // On mobile, open the modal instead of toggling sidebar
        const modal = new Modal(document.getElementById('mobileAddDrinksModal'));
        modal.show();
      } else {
        // On desktop, toggle the sidebar as before
        this.rightSidebarExpanded = !this.rightSidebarExpanded;
      }
    },

    // Mobile filters toggle
    toggleMobileFilters() {
      this.mobileFiltersCollapsed = !this.mobileFiltersCollapsed;
    },

    // Data loading
    async loadCellarData() {
      this.loading = true
      this.error = null
      
      try {
        // Load only items and collections data
        const itemsResponse = await this.fetchCellarItems()
        
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
          console.log('volumeNumber field:', this.allItems[0].volumeNumber, 'type:', typeof this.allItems[0].volumeNumber);
          console.log('volumeUnit field:', this.allItems[0].volumeUnit);
        }
        
      } catch (error) {
        console.error('Error loading cellar data:', error)
        
        // Handle 404 errors as empty cellar instead of showing error
        if (error.response && error.response.status === 404) {
          console.log('Received 404, treating as empty cellar')
          this.allItems = []
          this.collections = []
          this.dashboardData = {}
          this.error = null // Clear any previous errors
        } else {
          // Only show error for non-404 errors
          let errorMessage = 'Failed to load cellar data'
          
          if (error.response) {
            if (error.response.status === 403) {
              errorMessage = 'You do not have permission to view this cellar'
            } else if (error.response.status === 500) {
              errorMessage = 'Server error occurred while loading cellar data'
            } else if (error.response.data && error.response.data.message) {
              errorMessage = error.response.data.message
            }
          } else if (error.message) {
            errorMessage = error.message
          }
          
          this.error = errorMessage
        }
      } finally {
        this.loading = false
      }
    },
    
    async fetchCellarDashboard() {
      this.loadingDashboard = true;
      this.dashboardError = null;
      
      try {
        const baseUrl = this.getApiBaseUrl();
        const url = `${baseUrl}/getData/getCellarDashboard/${this.ownerType}/${this.id}`;
        
        const response = await axios.get(url);
        
        // Store the nested data object which contains summary, breakdowns, etc.
        this.dashboardData = response.data.data;
        return response.data.data;
      } catch (error) {
        console.error('Error fetching cellar dashboard:', error);
        this.dashboardError = error.response?.data?.message || 'Failed to load dashboard data';
        throw error;
      } finally {
        this.loadingDashboard = false;
      }
    },
    
    async fetchCellarItems() {
      // Use environment variable for API URL
      const baseUrl = process.env.VUE_APP_API_URL || (process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '');
      const params = new URLSearchParams()
      if (this.activeTab !== 'all') {
        params.append('collectionId', this.activeTab)
      }
      
      // Include consumed items so they don't disappear after status changes
      params.append('includeConsumed', 'true')
      
      const response = await this.$axios.get(`${baseUrl}/getData/getCellarData/${this.ownerType}/${this.id}?${params}`)
      return response.data
    },
    
    // Tab management
    setActiveTab(tabId) {
      this.activeTab = tabId
      this.currentPage = 1
      
      // Load dashboard data when dashboard tab is selected
      if (tabId === 'dashboard') {
        this.fetchCellarDashboard().catch(error => {
          console.error('Dashboard loading failed:', error);
        });
      }
      
      // Update the current collection's public status when switching tabs
      if (tabId !== 'all' && tabId !== 'history' && tabId !== 'dashboard') {
        const collection = this.collections.find(c => c.id === tabId)
        if (collection) {
          this.currentCollectionIsPublic = collection.isPublic || false
        }
      }
      // TODO: Fetch filtered data if needed
    },

    // Collection public status toggle
    async toggleCollectionPublicStatus() {
      if (this.activeTab === 'all' || this.activeTab === 'history' || this.activeTab === 'dashboard') {
        return // No action for these tabs
      }

      try {
        const baseUrl = this.getApiBaseUrl();
        // TODO: Replace with actual backend endpoint when ready
        await axios.put(`${baseUrl}/editCellar/collections/public-status/${this.activeTab}/`, {
          isPublic: this.currentCollectionIsPublic
        })

        // Update the collection in local state
        const collection = this.collections.find(c => c.id === this.activeTab)
        if (collection) {
          collection.isPublic = this.currentCollectionIsPublic
        }

        console.log('Collection public status updated:', this.currentCollectionIsPublic)
      } catch (error) {
        console.error('Error updating collection public status:', error)
        // Revert the toggle on error
        this.currentCollectionIsPublic = !this.currentCollectionIsPublic
        // TODO: Show error toast notification
      }
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
        drinkType: '',
        typeCategory: '',
        country: '',
        averageRating: '',
        status: '',
        drinkNow: false
      }
      this.currentPage = 1
    },
    
    // Food pairing suggestions
    async loadFoodPairingSuggestions() {
      if (this.loadingFoodPairings || this.foodPairingSuggestions.length > 0) {
        return // Already loaded or loading
      }
      
      this.loadingFoodPairings = true
      
      try {
        const baseUrl = this.getApiBaseUrl()
        const response = await this.$axios.get(`${baseUrl}/getData/getFoodPairings/${this.ownerType}/${this.id}`)
        
        if (response.data && response.data.data && response.data.data.foodPairings) {
          this.foodPairingSuggestions = response.data.data.foodPairings
          console.log('Loaded food pairing suggestions:', this.foodPairingSuggestions.length)
        }
      } catch (error) {
        console.error('Error loading food pairing suggestions:', error)
        // Don't show error to user, just fail silently
      } finally {
        this.loadingFoodPairings = false
      }
    },
    
    onFoodPairingFocus(event) {
      // Load suggestions when user clicks into any food pairing field
      this.loadFoodPairingSuggestions()
      
      // Set the active input and show suggestions
      this.activeFoodPairingInput = event.target
      this.showFoodPairingSuggestions = true
      
      // Position the dropdown below the input
      this.$nextTick(() => {
        this.positionFoodPairingDropdown(event.target)
      })
    },
    
    onFoodPairingBlur() {
      // Hide suggestions when user clicks away (with small delay to allow clicking suggestions)
      setTimeout(() => {
        this.showFoodPairingSuggestions = false
        this.activeFoodPairingInput = null
      }, 200)
    },
    
    selectFoodPairingSuggestion(suggestion) {
      if (this.activeFoodPairingInput) {
        // Determine which form field to update based on the input element
        if (this.activeFoodPairingInput.closest('.modal')) {
          // Modal form - trigger master field change
          this.onMasterFieldChange('suggestedFoodPairing', suggestion)
        } else {
          // Add drink form
          this.addDrinkForm.suggestedFoodPairing = suggestion
        }
      }
      
      this.showFoodPairingSuggestions = false
      this.activeFoodPairingInput = null
    },
    
    positionFoodPairingDropdown(inputElement) {
      const dropdown = document.getElementById('foodPairingDropdown')
      if (!dropdown || !inputElement) return
      
      const inputRect = inputElement.getBoundingClientRect()
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop
      
      dropdown.style.position = 'absolute'
      dropdown.style.top = (inputRect.bottom + scrollTop + 5) + 'px'
      dropdown.style.left = inputRect.left + 'px'
      dropdown.style.width = inputRect.width + 'px'
      dropdown.style.zIndex = '1050'
    },
    
    // Current location suggestions
    async loadCurrentLocationSuggestions() {
      if (this.loadingCurrentLocations || this.currentLocationSuggestions.length > 0) {
        return // Already loaded or loading
      }
      
      this.loadingCurrentLocations = true
      
      try {
        const baseUrl = this.getApiBaseUrl()
        const response = await this.$axios.get(`${baseUrl}/getData/getCurrentLocations/${this.ownerType}/${this.id}`)
        
        if (response.data && response.data.data && response.data.data.currentLocations) {
          this.currentLocationSuggestions = response.data.data.currentLocations
          console.log('Loaded current location suggestions:', this.currentLocationSuggestions.length)
        }
      } catch (error) {
        console.error('Error loading current location suggestions:', error)
        // Don't show error to user, just fail silently
      } finally {
        this.loadingCurrentLocations = false
      }
    },
    
    onCurrentLocationFocus(event) {
      // Load suggestions when user clicks into any current location field
      this.loadCurrentLocationSuggestions()
      
      // Set the active input and show suggestions
      this.activeCurrentLocationInput = event.target
      this.showCurrentLocationSuggestions = true
      
      // Position the dropdown below the input
      this.$nextTick(() => {
        this.positionCurrentLocationDropdown(event.target)
      })
    },
    
    onCurrentLocationBlur() {
      // Hide suggestions when user clicks away (with small delay to allow clicking suggestions)
      setTimeout(() => {
        this.showCurrentLocationSuggestions = false
        this.activeCurrentLocationInput = null
      }, 200)
    },
    
    selectCurrentLocationSuggestion(suggestion) {
      if (this.activeCurrentLocationInput) {
        // Determine which form field to update based on the input element
        if (this.activeCurrentLocationInput.closest('.modal')) {
          // Modal form - find the specific bottle or determine if it's master field
          const bottleContainer = this.activeCurrentLocationInput.closest('.bottle-item')
          if (bottleContainer) {
            // Individual bottle field
            const cellarItemId = bottleContainer.dataset.bottleId
            this.onBottleFieldChange(parseInt(cellarItemId), 'currentLocation', suggestion)
          } else {
            // Master field (if applicable)
            this.onMasterFieldChange('currentLocation', suggestion)
          }
        } else {
          // Add drink form
          this.addDrinkForm.currentLocation = suggestion
        }
      }
      
      this.showCurrentLocationSuggestions = false
      this.activeCurrentLocationInput = null
    },
    
    positionCurrentLocationDropdown(inputElement) {
      const dropdown = document.getElementById('currentLocationDropdown')
      if (!dropdown || !inputElement) return
      
      const inputRect = inputElement.getBoundingClientRect()
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop
      
      dropdown.style.position = 'absolute'
      dropdown.style.top = (inputRect.bottom + scrollTop + 5) + 'px'
      dropdown.style.left = inputRect.left + 'px'
      dropdown.style.width = inputRect.width + 'px'
      dropdown.style.zIndex = '1050'
    },
    
    // Sub location suggestions
    async loadSubLocationSuggestions() {
      if (this.loadingSubLocations || this.subLocationSuggestions.length > 0) {
        return // Already loaded or loading
      }
      
      this.loadingSubLocations = true
      
      try {
        const baseUrl = this.getApiBaseUrl()
        const response = await this.$axios.get(`${baseUrl}/getData/getSubLocations/${this.ownerType}/${this.id}`)
        
        if (response.data && response.data.data && response.data.data.subLocations) {
          this.subLocationSuggestions = response.data.data.subLocations
          console.log('Loaded sub location suggestions:', this.subLocationSuggestions.length)
        }
      } catch (error) {
        console.error('Error loading sub location suggestions:', error)
        // Don't show error to user, just fail silently
      } finally {
        this.loadingSubLocations = false
      }
    },
    
    onSubLocationFocus(event) {
      // Load suggestions when user clicks into any sub location field
      this.loadSubLocationSuggestions()
      
      // Set the active input and show suggestions
      this.activeSubLocationInput = event.target
      this.showSubLocationSuggestions = true
      
      // Position the dropdown below the input
      this.$nextTick(() => {
        this.positionSubLocationDropdown(event.target)
      })
    },
    
    onSubLocationBlur() {
      // Hide suggestions when user clicks away (with small delay to allow clicking suggestions)
      setTimeout(() => {
        this.showSubLocationSuggestions = false
        this.activeSubLocationInput = null
      }, 200)
    },
    
    selectSubLocationSuggestion(suggestion) {
      if (this.activeSubLocationInput) {
        // Determine which form field to update based on the input element
        if (this.activeSubLocationInput.closest('.modal')) {
          // Modal form - find the specific bottle or determine if it's master field
          const bottleContainer = this.activeSubLocationInput.closest('.bottle-item')
          if (bottleContainer) {
            // Individual bottle field
            const cellarItemId = bottleContainer.dataset.bottleId
            this.onBottleFieldChange(parseInt(cellarItemId), 'subLocation', suggestion)
          } else {
            // Master field (if applicable)
            this.onMasterFieldChange('subLocation', suggestion)
          }
        } else {
          // Add drink form
          this.addDrinkForm.subLocation = suggestion
        }
      }
      
      this.showSubLocationSuggestions = false
      this.activeSubLocationInput = null
    },
    
    positionSubLocationDropdown(inputElement) {
      const dropdown = document.getElementById('subLocationDropdown')
      if (!dropdown || !inputElement) return
      
      const inputRect = inputElement.getBoundingClientRect()
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop
      
      dropdown.style.position = 'absolute'
      dropdown.style.top = (inputRect.bottom + scrollTop + 5) + 'px'
      dropdown.style.left = inputRect.left + 'px'
      dropdown.style.width = inputRect.width + 'px'
      dropdown.style.zIndex = '1050'
    },
    
    // Personal notes suggestions
    async loadPersonalNotesSuggestions() {
      if (this.loadingPersonalNotes || this.personalNotesSuggestions.length > 0) {
        return // Already loaded or loading
      }
      
      this.loadingPersonalNotes = true
      
      try {
        const baseUrl = this.getApiBaseUrl()
        const response = await this.$axios.get(`${baseUrl}/getData/getNoteToSelf/${this.ownerType}/${this.id}`)
        
        if (response.data && response.data.data && response.data.data.noteToSelf) {
          this.personalNotesSuggestions = response.data.data.noteToSelf
          console.log('Loaded personal notes suggestions:', this.personalNotesSuggestions.length)
        }
      } catch (error) {
        console.error('Error loading personal notes suggestions:', error)
        // Don't show error to user, just fail silently
      } finally {
        this.loadingPersonalNotes = false
      }
    },
    
    onPersonalNotesFocus(event) {
      // Load suggestions when user clicks into any personal notes field
      this.loadPersonalNotesSuggestions()
      
      // Set the active input and show suggestions
      this.activePersonalNotesInput = event.target
      this.showPersonalNotesSuggestions = true
      
      // Position the dropdown below the input
      this.$nextTick(() => {
        this.positionPersonalNotesDropdown(event.target)
      })
    },
    
    onPersonalNotesBlur() {
      // Hide suggestions when user clicks away (with small delay to allow clicking suggestions)
      setTimeout(() => {
        this.showPersonalNotesSuggestions = false
        this.activePersonalNotesInput = null
      }, 200)
    },
    
    selectPersonalNotesSuggestion(suggestion) {
      if (this.activePersonalNotesInput) {
        // Determine which form field to update based on the input element
        if (this.activePersonalNotesInput.closest('.modal')) {
          // Modal form - find the specific bottle or determine if it's master field
          const bottleContainer = this.activePersonalNotesInput.closest('.bottle-item')
          if (bottleContainer) {
            // Individual bottle field
            const cellarItemId = bottleContainer.dataset.bottleId
            this.onBottleFieldChange(parseInt(cellarItemId), 'noteToSelf', suggestion)
          } else {
            // Master field (if applicable)
            this.onMasterFieldChange('noteToSelf', suggestion)
          }
        } else {
          // Add drink form
          this.addDrinkForm.personalNotes = suggestion
        }
      }
      
      this.showPersonalNotesSuggestions = false
      this.activePersonalNotesInput = null
    },
    
    positionPersonalNotesDropdown(inputElement) {
      const dropdown = document.getElementById('personalNotesDropdown')
      if (!dropdown || !inputElement) return
      
      const inputRect = inputElement.getBoundingClientRect()
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop
      
      dropdown.style.position = 'absolute'
      dropdown.style.top = (inputRect.bottom + scrollTop + 5) + 'px'
      dropdown.style.left = inputRect.left + 'px'
      dropdown.style.width = inputRect.width + 'px'
      dropdown.style.zIndex = '1050'
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
      console.log('TZHFrontendLog: setSelectedGroup - received group:', group);
      console.log('TZHFrontendLog: setSelectedGroup - group.variantGroupID:', group.variantGroupID);
      console.log('TZHFrontendLog: setSelectedGroup - group.representative:', group.representative);
      console.log('TZHFrontendLog: setSelectedGroup - group.bottles:', group.bottles);
      
      this.selectedGroup = group;
      this.modalEditing = {
        hasChanges: false,
        masterData: {},
        bottleChanges: {},
        archivedBottles: [],
        newBottles: [],
        originalCollectionId: group.representative?.collectionId || group.collectionId,
        selectedCollectionId: group.representative?.collectionId || group.collectionId
      };
    },

    // Collection change handler
    onCollectionChange(newCollectionId) {
      this.modalEditing.selectedCollectionId = newCollectionId;
      this.modalEditing.hasChanges = true;
    },

    // Reset modal editing state
    resetModalState() {
      this.modalEditing = {
        hasChanges: false,
        masterData: {},
        bottleChanges: {},
        archivedBottles: [],
        newBottles: [],
        originalCollectionId: null,
        selectedCollectionId: null
      };
      
      // Clear current bottle ID reference
      this.currentModalPurchaseBottleId = null;
    },

    // Master record field change handlers
    onMasterFieldChange(field, value) {
      this.modalEditing.masterData[field] = value;
      this.modalEditing.hasChanges = true;
    },

    // Individual bottle field change handlers
    onBottleFieldChange(cellarItemId, field, value) {
      if (!this.modalEditing.bottleChanges[cellarItemId]) {
        this.modalEditing.bottleChanges[cellarItemId] = {};
      }
      this.modalEditing.bottleChanges[cellarItemId][field] = value;
      this.modalEditing.hasChanges = true;
    },

    // Get current value for bottle field (with change tracking)
    getBottleFieldValue(cellarItemId, field) {
      let value;
      if (this.modalEditing.bottleChanges[cellarItemId] && 
          Object.prototype.hasOwnProperty.call(this.modalEditing.bottleChanges[cellarItemId], field)) {
        value = this.modalEditing.bottleChanges[cellarItemId][field];
      } else {
        const bottle = this.selectedGroup.bottles.find(b => b.cellarItemId === cellarItemId);
        value = bottle ? bottle[field] : '';
      }
      
      // Format dates for HTML date inputs (YYYY-MM-DD format)
      if ((field.includes('Date') || field === 'purchaseDate' || field === 'deliveryDate') && value) {
        return this.formatDateForInput(value);
      }
      
      return value;
    },

    // Get current value for master field (with change tracking)
    getMasterFieldValue(field) {
      let value;
      if (Object.prototype.hasOwnProperty.call(this.modalEditing.masterData, field)) {
        value = this.modalEditing.masterData[field];
      } else {
        const masterBottle = this.selectedGroup.bottles.find(b => b.quantityVariantID === 1);
        value = masterBottle ? masterBottle[field] : '';
      }
      
      // Format dates for HTML date inputs (YYYY-MM-DD format)
      if ((field.includes('Date') || field === 'drinkOnwardsDate' || field === 'drinkByDate') && value) {
        return this.formatDateForInput(value);
      }
      
      return value;
    },

    // Format date for HTML date input (YYYY-MM-DD)
    formatDateForInput(dateValue) {
      if (!dateValue) return '';
      
      try {
        const date = new Date(dateValue);
        if (isNaN(date.getTime())) return '';
        
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        
        return `${year}-${month}-${day}`;
      } catch (error) {
        console.warn('Error formatting date for input:', dateValue, error);
        return '';
      }
    },

    // Check if bottle is new
    isNewBottle(cellarItemId) {
      return this.modalEditing.newBottles.some(nb => nb.tempId === cellarItemId);
    },

    // Filter visible bottles (exclude archived ones)
    getVisibleBottles(bottles) {
      return bottles.filter(bottle => 
        !this.modalEditing.archivedBottles.includes(bottle.cellarItemId)
      );
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

    // Convert currency to USD using fallback rates
    convertToUSD(amount, fromCurrency) {
      if (!amount || !fromCurrency) return null;
      
      // Fallback exchange rates to USD (approximate rates)
      const fallbackRates = {
        'USD': 1.0,
        'EUR': 1.10,
        'GBP': 1.25,
        'JPY': 0.0067,
        'CAD': 0.74,
        'AUD': 0.66,
        'SGD': 0.74,
        'CHF': 1.12,
        'CNY': 0.14,
        'HKD': 0.13,
        'SEK': 0.096,
        'NOK': 0.092,
        'DKK': 0.15
      };

      const rate = fallbackRates[fromCurrency.toUpperCase()];
      if (rate === undefined) {
        console.warn(`Unsupported currency: ${fromCurrency}`);
        return null;
      }

      return parseFloat(amount) * rate;
    },

    // Calculate average purchase price for a group
    getAveragePurchasePrice(group) {
      if (!group || !group.bottles) {
        return { error: 'No group data available' };
      }

      const bottlesWithPrices = [];
      let hasNonUSDCurrency = false;
      let conversionError = false;

      // Collect all bottles with purchase prices
      for (const bottle of group.bottles) {
        const price = this.getBottleFieldValue ? 
          this.getBottleFieldValue(bottle.cellarItemId, 'purchasePrice') : 
          bottle.purchasePrice;
        const currency = this.getBottleFieldValue ? 
          this.getBottleFieldValue(bottle.cellarItemId, 'purchaseCurrency') : 
          bottle.purchaseCurrency;

        if (price && !isNaN(parseFloat(price)) && parseFloat(price) > 0) {
          const priceFloat = parseFloat(price);
          const currencyCode = currency || 'USD';

          if (currencyCode !== 'USD') {
            hasNonUSDCurrency = true;
            const usdAmount = this.convertToUSD(priceFloat, currencyCode);
            if (usdAmount === null) {
              conversionError = true;
              continue;
            }
            bottlesWithPrices.push(usdAmount);
          } else {
            bottlesWithPrices.push(priceFloat);
          }
        }
      }

      // Handle cases
      if (bottlesWithPrices.length === 0) {
        return { error: 'No purchase prices available' };
      }

      if (conversionError) {
        return { error: 'Currency conversion error' };
      }

      // Calculate average
      const sum = bottlesWithPrices.reduce((acc, price) => acc + price, 0);
      const average = sum / bottlesWithPrices.length;

      return {
        success: true,
        amount: average.toFixed(2),
        currency: hasNonUSDCurrency ? ' USD (equivalent)' : ' USD'
      };
    },

    // Get item count for a specific collection
    getCollectionItemCount(collectionId) {
      if (!this.allItems || !collectionId) {
        return 0;
      }
      return this.allItems.filter(item => item.collectionId === collectionId).length;
    },

    // Navigate to listing page
    goToListingPage(group) {
      if (group.listingId && group.representative.listingName) {
        // Small delay to allow modal dismiss to complete
        setTimeout(() => {
          const listingName = this.slugify(group.representative.listingName)
          this.$router.push(`/listing/view/${group.listingId}/${listingName}`)
        }, 150)
      }
    },

    // Group actions
    consumeBottle() {
      if (!this.selectedGroup || !this.selectedGroup.bottles) {
        console.error('No group selected or no bottles in group');
        return;
      }

      const bottleCount = this.selectedGroup.bottles.length;
      const confirmMessage = `Are you sure you want to mark all ${bottleCount} bottle${bottleCount !== 1 ? 's' : ''} as consumed? This action will change their status to "Consumed".`;
      
      if (confirm(confirmMessage)) {
        // Mark all bottles in the group as consumed
        this.selectedGroup.bottles.forEach(bottle => {
          this.onBottleFieldChange(bottle.cellarItemId, 'status', 'Consumed');
        });
        
        console.log(`Marked ${bottleCount} bottles as consumed in group:`, this.selectedGroup);
      }
    },

    markAllBottlesInPossession() {
      if (!this.selectedGroup || !this.selectedGroup.bottles) {
        console.error('No group selected or no bottles in group');
        return;
      }

      const bottleCount = this.selectedGroup.bottles.length;
      const confirmMessage = `Are you sure you want to mark all ${bottleCount} bottle${bottleCount !== 1 ? 's' : ''} as "In Possession"? This action will change their status to "In Possession".`;
      
      if (confirm(confirmMessage)) {
        // Mark all bottles in the group as in possession
        this.selectedGroup.bottles.forEach(bottle => {
          this.onBottleFieldChange(bottle.cellarItemId, 'status', 'In Possession');
        });
        
        console.log(`Marked ${bottleCount} bottles as in possession in group:`, this.selectedGroup);
      }
    },

    markAllBottlesEmpty() {
      if (!this.selectedGroup || !this.selectedGroup.bottles) {
        console.error('No group selected or no bottles in group');
        return;
      }

      const bottleCount = this.selectedGroup.bottles.length;
      const confirmMessage = `Are you sure you want to mark all ${bottleCount} bottle${bottleCount !== 1 ? 's' : ''} as empty? This action will change their consumption status to "Empty".`;
      
      if (confirm(confirmMessage)) {
        // Mark all bottles in the group as empty
        this.selectedGroup.bottles.forEach(bottle => {
          this.onBottleFieldChange(bottle.cellarItemId, 'consumption', 'Empty');
        });
        
        console.log(`Marked ${bottleCount} bottles as empty in group:`, this.selectedGroup);
      }
    },

    archiveGroup() {
      if (!this.selectedGroup || !this.selectedGroup.bottles) {
        console.error('No group selected or no bottles in group');
        return;
      }

      const bottleCount = this.selectedGroup.bottles.length;
      const confirmMessage = `Are you sure you want to archive all ${bottleCount} bottle${bottleCount !== 1 ? 's' : ''} in this group? This action cannot be undone.`;
      
      if (confirm(confirmMessage)) {
        // Archive all bottles in the group
        this.selectedGroup.bottles.forEach(bottle => {
          if (!this.modalEditing.archivedBottles.includes(bottle.cellarItemId)) {
            this.modalEditing.archivedBottles.push(bottle.cellarItemId);
          }
        });
        
        this.modalEditing.hasChanges = true;
        console.log(`Archived ${bottleCount} bottles from group:`, this.selectedGroup);
      }
    },

    saveGroupChanges() {
      console.log('Save group changes:', this.selectedGroup)
      // TODO: Implement save functionality for group updates
    },

    // Toggle group actions dropdown manually if needed
    toggleGroupActionsDropdown() {
      const dropdownElement = document.getElementById('groupActionsDropdown');
      if (dropdownElement) {
        const bootstrapDropdown = new Dropdown(dropdownElement);
        bootstrapDropdown.toggle();
      }
    },

    // Individual bottle management
    editIndividualBottle(bottle) {
      console.log('Edit individual bottle:', bottle)
      // TODO: Implement individual bottle editing
    },

    addNewBottle() {
      if (!this.selectedGroup) return;
      
      console.log('TZHFrontendLog: addNewBottle - selectedGroup:', this.selectedGroup);
      console.log('TZHFrontendLog: addNewBottle - selectedGroup.variantGroupID:', this.selectedGroup.variantGroupID);
      console.log('TZHFrontendLog: addNewBottle - selectedGroup.representative.variantGroupID:', this.selectedGroup.representative?.variantGroupID);
      console.log('TZHFrontendLog: addNewBottle - selectedGroup.bottles[0].variantGroupID:', this.selectedGroup.bottles[0]?.variantGroupID);
      
      const tempId = `temp_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      const maxQuantityVariantID = Math.max(...this.selectedGroup.bottles.map(b => b.quantityVariantID));
      
      const newBottle = {
        cellarItemId: tempId,
        variantGroupID: this.selectedGroup.variantGroupID || this.selectedGroup.bottles[0]?.variantGroupID,
        quantityVariantID: maxQuantityVariantID + 1,
        status: 'In Possession',
        consumption: 'Unopened',
        currentLocation: '',
        subLocation: '',
        noteToSelf: '',
        purchasePlaceName: '',
        purchaseDate: '',
        deliveryDate: '',
        purchaseCurrency: 'USD',
        purchasePrice: ''
      };

      this.selectedGroup.bottles.push(newBottle);
      this.modalEditing.newBottles.push({ tempId, bottle: newBottle });
      this.modalEditing.hasChanges = true;
    },

    // Archive bottle functionality
    archiveBottle(cellarItemId) {
      if (confirm('Are you sure you want to archive this bottle? This action cannot be undone.')) {
        this.modalEditing.archivedBottles.push(cellarItemId);
        this.modalEditing.hasChanges = true;
      }
    },

    // Save all changes to backend
    async saveModalChanges() {
      try {
        this.loading = true;
        
        // Filter out empty/null values from bottle changes
        const cleanedBottleChanges = {};
        Object.keys(this.modalEditing.bottleChanges).forEach(bottleId => {
          const originalFields = this.modalEditing.bottleChanges[bottleId];
          const cleanedFields = {};
          
          Object.keys(originalFields).forEach(fieldName => {
            const fieldValue = originalFields[fieldName];
            // Only include non-empty values
            if (fieldValue !== null && fieldValue !== undefined && fieldValue !== '') {
              cleanedFields[fieldName] = fieldValue;
            }
          });
          
          // Only include bottles that have actual changes
          if (Object.keys(cleanedFields).length > 0) {
            cleanedBottleChanges[bottleId] = cleanedFields;
          }
        });
        
        console.log('TZHFrontendLog: Original bottle changes:', JSON.stringify(this.modalEditing.bottleChanges, null, 2));
        console.log('TZHFrontendLog: Cleaned bottle changes:', JSON.stringify(cleanedBottleChanges, null, 2));
        
        const payload = {
          variantGroupID: this.selectedGroup.variantGroupID,
          changes: {
            collectionChange: {
              from: this.modalEditing.originalCollectionId,
              to: this.modalEditing.selectedCollectionId
            },
            masterData: this.modalEditing.masterData,
            bottleChanges: cleanedBottleChanges,
            archivedBottles: this.modalEditing.archivedBottles,
            newBottles: this.modalEditing.newBottles.map(nb => nb.bottle)
          }
        };
        
        console.log('TZHFrontendLog: Full payload being sent to backend:', JSON.stringify(payload, null, 2));

        const baseUrl = this.getApiBaseUrl();
        const fullUrl = `${baseUrl}/editCellar/editCellar`;
        console.log('TZHFrontendLog: Making API call to:', fullUrl);
        
        const response = await axios.post(fullUrl, payload);
        
        console.log('TZHFrontendLog: API response received');
        console.log('TZHFrontendLog: Response status:', response.status);
        console.log('TZHFrontendLog: Response data:', JSON.stringify(response.data, null, 2));
        console.log('SaveModalChanges response:', response);
        
        if (response.data.success) {
          // Simulate clicking the close button to ensure proper cleanup
          const closeButton = document.querySelector('#itemDetailsModal .btn-close');
          if (closeButton) {
            closeButton.click();
          }
          
          // Reset state and reload data
          this.selectedGroup = null;
          this.resetModalState();
          
          // Reload cellar data to reflect changes
          await this.loadCellarData();
          
          // Show success message
          alert('Changes saved successfully!');
        } else {
          console.log('Success check failed - response.data:', response.data);
          alert('Error saving changes: ' + (response.data.message || 'Unknown error'));
        }
      } catch (error) {
        console.error('TZHFrontendLog: ========== ERROR SAVING CHANGES ==========');
        console.error('TZHFrontendLog: Error object:', error);
        console.error('TZHFrontendLog: Error message:', error.message);
        console.error('TZHFrontendLog: Error response:', error.response);
        
        if (error.response) {
          console.error('TZHFrontendLog: Response status:', error.response.status);
          console.error('TZHFrontendLog: Response data:', JSON.stringify(error.response.data, null, 2));
          console.error('TZHFrontendLog: Response headers:', error.response.headers);
        }
        
        console.error('TZHFrontendLog: Request config:', error.config);
        console.error('TZHFrontendLog: ================================================');
        console.error('Error saving changes:', error);
        
        let errorMessage = 'Error saving changes. Please try again.';
        if (error.response && error.response.data && error.response.data.message) {
          errorMessage = `Error: ${error.response.data.message}`;
        } else if (error.message) {
          errorMessage = `Error: ${error.message}`;
        }
        
        alert(errorMessage);
      } finally {
        this.loading = false;
      }
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

    truncateText(text, maxLength) {
      if (!text) return ''
      if (text.length <= maxLength) return text
      return text.substring(0, maxLength).trim() + '...'
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

    getContainerType(format, count) {
      if (!format) {
        // Default to bottle if no format is specified
        return count === 1 ? 'bottle' : 'bottles'
      }

      const formatLower = format.toLowerCase()
      
      if (formatLower === 'can') {
        return count === 1 ? 'can' : 'cans'
      } else if (formatLower === 'sample') {
        return count === 1 ? 'sample bottle' : 'sample bottles'
      } else {
        // Default to bottle for 'bottle' format or any other format
        return count === 1 ? 'bottle' : 'bottles'
      }
    },

    getVolumeText(representative) {
      if (representative.volumeNumber && representative.volumeUnit) {
        // Debug: log the original value and type
        console.log('Volume debugging - Original volumeNumber:', representative.volumeNumber, 'type:', typeof representative.volumeNumber)
        
        // Format volume number to remove unnecessary decimal places
        const formattedVolume = this.formatVolumeNumber(representative.volumeNumber)
        console.log('Volume debugging - Formatted volumeNumber:', formattedVolume)
        
        return `/${formattedVolume}${representative.volumeUnit}`
      }
      return ''
    },

    formatVolumeNumber(volumeNumber) {
      // Convert to number if it's a string
      const num = parseFloat(volumeNumber)
      
      // If it's a whole number, return as integer
      if (num % 1 === 0) {
        return num.toString()
      }
      
      // Otherwise, return with minimal decimal places
      return num.toString()
    },
    
    onImageError(event) {
      event.target.src = 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739'
    },
    
    // Get the proper image URL for a cellar item or group
    getItemImageUrl(itemOrGroup) {
      const baseUrl = this.getApiBaseUrl();
      
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
      const baseUrl = this.getApiBaseUrl();
      
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
        const baseUrl = this.getApiBaseUrl();
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

    // Handle focus on drink search input
    onDrinkSearchFocus() {
      // If a producer is selected, trigger search immediately on focus
      if (this.addDrinkForm.selectedProducer && this.addDrinkForm.selectedProducer.id) {
        console.log('TZHFrontendLog: Producer selected, triggering search on focus');
        // Don't use debounced search since we want immediate results
        this.searchDrinks();
      }
      // If no producer is selected, do nothing - rely on @input event for typing
    },

    // Search drinks API call
    async searchDrinks() {
      console.log('TZHFrontendLog: searchDrinks called with query:', this.addDrinkForm.searchQuery);
      console.log('TZHFrontendLog: Selected producer for filtering:', JSON.stringify(this.addDrinkForm.selectedProducer, null, 2));
      
      // Allow empty search if producer is selected (to show all drinks from producer)
      const hasProducerSelected = this.addDrinkForm.selectedProducer && this.addDrinkForm.selectedProducer.id;
      const queryLength = this.addDrinkForm.searchQuery ? this.addDrinkForm.searchQuery.trim().length : 0;
      
      if (!hasProducerSelected && queryLength < 2) {
        console.log('TZHFrontendLog: Search query too short and no producer selected, clearing results');
        this.addDrinkForm.searchResults = [];
        this.addDrinkForm.isSearchingDrinks = false;
        return;
      }

      // Set loading state
      this.addDrinkForm.isSearchingDrinks = true;

      try {
        const baseUrl = this.getApiBaseUrl();
        let response;
        let searchUrl;
        
        // Ensure we have a search term for the URL (use placeholder for empty search)
        const searchTerm = this.addDrinkForm.searchQuery ? this.addDrinkForm.searchQuery.trim() : '';
        // Use a placeholder character for empty searches to avoid malformed URLs
        const urlSafeSearchTerm = searchTerm || '_EMPTY_SEARCH_';
        
        // If a producer is selected, search only within that producer's listings
        if (this.addDrinkForm.selectedProducer && this.addDrinkForm.selectedProducer.id) {
          // Use encodeURIComponent to handle special characters
          searchUrl = `${baseUrl}/getData/getListingNamesByProducer/${encodeURIComponent(urlSafeSearchTerm)}/${this.addDrinkForm.selectedProducer.id}`;
          console.log('TZHFrontendLog: Searching drinks by producer with URL:', searchUrl);
          response = await this.$axios.get(searchUrl);
        } else {
          // Otherwise, search all listings
          searchUrl = `${baseUrl}/getData/getListingNamesDynamicSearch/${encodeURIComponent(urlSafeSearchTerm)}`;
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
      } finally {
        // Clear loading state
        this.addDrinkForm.isSearchingDrinks = false;
      }
    },

    // Select drink
    selectDrink(listing) {
      console.log('TZHFrontendLog: selectDrink called with listing:', JSON.stringify(listing, null, 2));
      this.addDrinkForm.selectedDrink = listing;
      this.addDrinkForm.searchQuery = listing.listingName;
      this.addDrinkForm.searchResults = [];
      this.addDrinkForm.isSearchingDrinks = false;
      
      // Apply conditional defaults based on drinkType
      this.applyDrinkTypeDefaults();
      
      console.log('TZHFrontendLog: Updated addDrinkForm.selectedDrink:', JSON.stringify(this.addDrinkForm.selectedDrink, null, 2));
      console.log('TZHFrontendLog: Applied conditional defaults - format:', this.addDrinkForm.format, 'volume:', this.addDrinkForm.volumeNumber, this.addDrinkForm.volumeUnit);
      console.log('TZHFrontendLog: canAddToCellar after selection:', this.canAddToCellar);
    },

    // Apply conditional defaults based on selected drink's drinkType
    applyDrinkTypeDefaults() {
      // Update form defaults based on computed properties
      this.addDrinkForm.format = this.defaultFormat;
      this.addDrinkForm.volumeNumber = this.defaultVolumeNumber;
      this.addDrinkForm.volumeUnit = this.defaultVolumeUnit;
      
      console.log('TZHFrontendLog: Applied drinkType defaults:', {
        drinkType: this.addDrinkForm.selectedDrink?.drinkType,
        format: this.addDrinkForm.format,
        volumeNumber: this.addDrinkForm.volumeNumber,
        volumeUnit: this.addDrinkForm.volumeUnit
      });
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
      
      // Add custom class to Google Maps dropdown when it appears
      // Use multiple attempts with longer delays for modal contexts
      this.$nextTick(() => {
        const attemptToStylePacContainer = (attempt = 1, maxAttempts = 10) => {
          setTimeout(() => {
            const pacContainer = document.querySelector('.pac-container');
            if (pacContainer) {
              pacContainer.classList.add('add-drink-pac-container');
              pacContainer.setAttribute('data-input-source', 'purchase-location');
              console.log('TZHFrontendLog: Successfully styled pac-container on attempt', attempt);
            } else if (attempt < maxAttempts) {
              console.log('TZHFrontendLog: pac-container not found, retrying attempt', attempt + 1);
              attemptToStylePacContainer(attempt + 1, maxAttempts);
            } else {
              console.log('TZHFrontendLog: pac-container not found after', maxAttempts, 'attempts');
            }
          }, attempt === 1 ? 100 : 200); // First attempt after 100ms, subsequent attempts after 200ms
        };
        
        attemptToStylePacContainer();
      });
    },

    // Handle blur on purchase location input
    onPurchaseLocationBlur() {
      // Remove custom class when input loses focus
      const pacContainer = document.querySelector('.pac-container');
      if (pacContainer) {
        pacContainer.classList.remove('add-drink-pac-container');
        pacContainer.removeAttribute('data-input-source');
      }
      
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

    // ============ Modal Purchase Location Google Maps Methods ============
    
    // Handle place selection from Google Maps autocomplete for modal
    setModalPurchasePlaceFromAutocomplete(place) {
      console.log('TZHFrontendLog: ========================================');
      console.log('TZHFrontendLog: setModalPurchasePlaceFromAutocomplete called');
      console.log('TZHFrontendLog: place object:', place);
      
      // Find which bottle this is for by checking which input is focused
      let bottleId = this.currentModalPurchaseBottleId;
      
      // If we don't have a bottle ID, try to find it from the currently focused element
      if (!bottleId) {
        const activeElement = document.activeElement;
        if (activeElement) {
          bottleId = this.findBottleIdFromRef(activeElement);
          console.log('TZHFrontendLog: Found bottle ID from active element:', bottleId);
        }
      }
      
      if (!bottleId) {
        console.error('TZHFrontendLog: Could not determine bottle ID for purchase location');
        console.log('TZHFrontendLog: currentModalPurchaseBottleId:', this.currentModalPurchaseBottleId);
        console.log('TZHFrontendLog: document.activeElement:', document.activeElement);
        return;
      }
      
      console.log('TZHFrontendLog: Working with bottle ID:', bottleId);
      
      if (place && place.geometry) {
        const selectedPlace = place.name || place.formatted_address;
        const selectedAddress = place.formatted_address;
        
        console.log('TZHFrontendLog: Processing place selection for bottle:', bottleId);
        console.log('TZHFrontendLog: selectedPlace:', selectedPlace);
        console.log('TZHFrontendLog: selectedAddress:', selectedAddress);
        
        // Store Google Maps data in bottle changes using backend-compatible field names
        console.log('TZHFrontendLog: Before storing - current bottleChanges:', JSON.stringify(this.modalEditing.bottleChanges[bottleId], null, 2));
        
        this.onBottleFieldChange(bottleId, 'purchasePlaceName', selectedPlace);
        this.onBottleFieldChange(bottleId, 'purchaseAddress', selectedAddress);
        this.onBottleFieldChange(bottleId, 'purchaseVenueId', this.checkVenueIfExists(place));
        
        console.log('TZHFrontendLog: After storing - bottleChanges:', JSON.stringify(this.modalEditing.bottleChanges[bottleId], null, 2));
        console.log('TZHFrontendLog: Check getModalSelectedPurchasePlace:', this.getModalSelectedPurchasePlace(bottleId));
        console.log('TZHFrontendLog: Check getModalSelectedPurchaseAddress:', this.getModalSelectedPurchaseAddress(bottleId));
        
        console.log('TZHFrontendLog: Modal purchase location selected:', {
          bottleId: bottleId,
          place: selectedPlace,
          address: selectedAddress
        });
        
        // Force Vue to update the reactive properties
        this.$forceUpdate();
        console.log('TZHFrontendLog: Force update called');
      } else {
        console.log('TZHFrontendLog: Place object missing geometry or invalid:', place);
      }
      console.log('TZHFrontendLog: ========================================');
    },

    // Handle input changes for modal purchase location
    onModalPurchaseLocationInput(event) {
      const bottleId = this.currentModalPurchaseBottleId;
      if (!bottleId) return;
      
      // Handle both string values and event objects
      const inputValue = typeof event === 'string' ? event : event.target.value;
      
      // Get current Google Maps selection for this bottle
      const currentSelected = this.getBottleFieldValue(bottleId, 'purchasePlaceName') || '';
      
      // If user is typing manually (not from autocomplete), clear the selection
      if (inputValue !== currentSelected) {
        this.onBottleFieldChange(bottleId, 'purchasePlaceName', '');
        this.onBottleFieldChange(bottleId, 'purchaseAddress', '');
        this.onBottleFieldChange(bottleId, 'purchaseVenueId', null);
      }
      
      // Update the bottle field with manual entry
      this.onBottleFieldChange(bottleId, 'purchasePlaceName', inputValue ? inputValue.trim() : '');
    },

    // Handle focus on modal purchase location input
    onModalPurchaseLocationFocus(event) {
      // Store which bottle's input is focused
      const inputElement = event.target;
      const bottleId = this.findBottleIdFromRef(inputElement);
      this.currentModalPurchaseBottleId = bottleId;
      
      console.log('TZHFrontendLog: Modal purchase location input focused for bottle:', bottleId);
      console.log('TZHFrontendLog: Input element:', inputElement);
      console.log('TZHFrontendLog: Found bottle container:', inputElement.closest('[data-bottle-id]'));
      
      // Add custom class to Google Maps dropdown when it appears (modal context)
      this.$nextTick(() => {
        const attemptToStylePacContainer = (attempt = 1, maxAttempts = 10) => {
          setTimeout(() => {
            const pacContainer = document.querySelector('.pac-container');
            if (pacContainer) {
              pacContainer.classList.add('add-drink-pac-container');
              pacContainer.setAttribute('data-input-source', 'modal-purchase-location');
              console.log('TZHFrontendLog: Successfully styled modal pac-container on attempt', attempt);
            } else if (attempt < maxAttempts) {
              console.log('TZHFrontendLog: Modal pac-container not found, retrying attempt', attempt + 1);
              attemptToStylePacContainer(attempt + 1, maxAttempts);
            } else {
              console.log('TZHFrontendLog: Modal pac-container not found after', maxAttempts, 'attempts');
            }
          }, attempt === 1 ? 150 : 250); // Longer delays for modal context
        };
        
        attemptToStylePacContainer();
      });
    },

    // Handle blur on modal purchase location input
    onModalPurchaseLocationBlur() {
      // Remove custom class when input loses focus
      const pacContainer = document.querySelector('.pac-container');
      if (pacContainer) {
        pacContainer.classList.remove('add-drink-pac-container');
        pacContainer.removeAttribute('data-input-source');
      }
      
      // Delay clearing the bottle ID to allow place_changed event to fire
      setTimeout(() => {
        this.currentModalPurchaseBottleId = null;
        console.log('TZHFrontendLog: Cleared currentModalPurchaseBottleId after delay');
      }, 200);
    },

    // Clear selected purchase location for modal
    clearModalSelectedPurchaseLocation(bottleId) {
      this.onBottleFieldChange(bottleId, 'purchasePlaceName', '');
      this.onBottleFieldChange(bottleId, 'purchaseAddress', '');
      this.onBottleFieldChange(bottleId, 'purchaseVenueId', null);
      
      console.log('TZHFrontendLog: Modal purchase location cleared for bottle:', bottleId);
    },

    // Helper methods for modal purchase location
    getModalPurchaseLocationInputValue(bottleId) {
      return this.getBottleFieldValue(bottleId, 'purchasePlaceName') || '';
    },

    getModalSelectedPurchasePlace(bottleId) {
      return this.getBottleFieldValue(bottleId, 'purchasePlaceName') || '';
    },

    getModalSelectedPurchaseAddress(bottleId) {
      return this.getBottleFieldValue(bottleId, 'purchaseAddress') || '';
    },

    // Helper to find bottle ID from input element reference
    findBottleIdFromRef(inputElement) {
      console.log('TZHFrontendLog: findBottleIdFromRef called with element:', inputElement);
      
      // Look for the data-bottle-id attribute on the parent bottle container
      const bottleContainer = inputElement.closest('[data-bottle-id]');
      if (bottleContainer) {
        const bottleId = bottleContainer.getAttribute('data-bottle-id');
        console.log('TZHFrontendLog: Found bottle ID from container:', bottleId);
        return bottleId;
      }
      
      // Fallback: Look through the refs to find which bottle this input belongs to
      for (const [refName, refElement] of Object.entries(this.$refs)) {
        if (refName.startsWith('modalPurchaseLocationInput_')) {
          // Handle case where ref is an array
          if (Array.isArray(refElement)) {
            if (refElement.includes(inputElement)) {
              const bottleId = refName.replace('modalPurchaseLocationInput_', '');
              console.log('TZHFrontendLog: Found bottle ID from refs array:', bottleId);
              return bottleId;
            }
          } else if (refElement === inputElement) {
            const bottleId = refName.replace('modalPurchaseLocationInput_', '');
            console.log('TZHFrontendLog: Found bottle ID from refs:', bottleId);
            return bottleId;
          }
        }
      }
      
      console.log('TZHFrontendLog: Could not find bottle ID for element');
      return null;
    },

    // ============ End Modal Purchase Location Methods ============

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
        const baseUrl = this.getApiBaseUrl();
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
        isSearchingDrinks: false,
        
        // Group properties (applied to all items in the drink group)
        vintage: null,
        format: 'Bottle', // Default fallback, will be updated when drink is selected
        volumeNumber: 700, // Default fallback, will be updated when drink is selected
        volumeUnit: 'ml', // Default fallback, will be updated when drink is selected
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
        }
      }
      
      // Reset form expansion state to simplified view
      this.showExpandedForm = false;
    },

    // Toggle form expansion/simplification
    toggleFormExpansion() {
      this.showExpandedForm = !this.showExpandedForm;
    },

    // Collection Management Methods
    async createNewCollection() {
      try {
        // Reset form state
        this.newCollectionForm.loading = true;
        this.newCollectionForm.error = null;
        this.newCollectionForm.success = null;
        this.newCollectionForm.errors.collectionName = null;

        // Validate collection name
        const collectionName = this.newCollectionForm.collectionName.trim();
        if (!collectionName) {
          this.newCollectionForm.errors.collectionName = 'Collection name is required';
          this.newCollectionForm.loading = false;
          return;
        }

        if (collectionName.length > 255) {
          this.newCollectionForm.errors.collectionName = 'Collection name must be 255 characters or less';
          this.newCollectionForm.loading = false;
          return;
        }

        // Check for duplicate names (client-side check)
        const existingCollection = this.collections.find(c => 
          c.collectionName.toLowerCase() === collectionName.toLowerCase()
        );
        if (existingCollection) {
          this.newCollectionForm.errors.collectionName = 'A collection with this name already exists';
          this.newCollectionForm.loading = false;
          return;
        }

        // Prepare request data
        const payload = {
          ownerType: this.ownerType,
          ownerId: parseInt(this.id),
          collectionName: collectionName,
          isPublic: this.newCollectionForm.isPublic
          // Note: isDefault is not included since this functionality is disabled in UI
        };

        console.log('Creating new collection with payload:', payload);

        // Make API call
        const baseUrl = this.getApiBaseUrl();
        const fullUrl = `${baseUrl}/editCellar/createCollection`;
        const response = await axios.post(fullUrl, payload);

        if (response.data.success) {
          // Show success message
          this.newCollectionForm.success = response.data.message;

          // Add the new collection to the local collections list
          const newCollection = response.data.data;
          this.collections.push(newCollection);

          // If this is the new default collection, update other collections
          if (newCollection.isDefault) {
            this.collections.forEach(collection => {
              if (collection.id !== newCollection.id) {
                collection.isDefault = false;
              }
            });
          }

          // Reset form after a short delay
          setTimeout(() => {
            this.resetNewCollectionForm();
            // Close the modal
            const closeButton = document.querySelector('#addCollectionModal .btn-close');
            if (closeButton) {
              closeButton.click();
            }
          }, 1500);

          console.log('Collection created successfully:', newCollection);
        } else {
          this.newCollectionForm.error = response.data.message || 'Failed to create collection';
        }

      } catch (error) {
        console.error('Error creating collection:', error);
        
        if (error.response && error.response.data) {
          this.newCollectionForm.error = error.response.data.message || 'Failed to create collection';
        } else {
          this.newCollectionForm.error = 'Network error. Please try again.';
        }
      } finally {
        this.newCollectionForm.loading = false;
      }
    },

    resetNewCollectionForm() {
      this.newCollectionForm = {
        collectionName: '',
        isPublic: true,
        isDefault: false,
        loading: false,
        error: null,
        success: null,
        errors: {
          collectionName: null
        }
      };
    },

    // Cellar changelog methods
    async loadChangelogData() {
      if (this.loadingChangelog) return; // Prevent multiple simultaneous requests
      
      this.loadingChangelog = true;
      this.changelogError = null;
      
      try {
        // Check if we have the required data to make the request
        if (!this.ownerType || !this.id) {
          throw new Error('Missing owner information');
        }
        
        const baseUrl = this.getApiBaseUrl();
        const response = await this.$axios.get(
          `${baseUrl}/getData/getCellarItemsChangelog/${this.ownerType}/${this.id}?limit=${this.changelogLimit}`
        );
        
        if (response.data.code === 200) {
          this.changelog = Array.isArray(response.data.data.changelog) ? response.data.data.changelog : [];
          this.hasMoreChangelog = this.changelog.length >= this.changelogLimit;
          this.changelogOffset = this.changelog.length;
        } else {
          throw new Error(response.data.message || 'Failed to load changelog');
        }
      } catch (error) {
        console.error('Error loading changelog:', error);
        this.changelogError = error.message || 'Failed to load changelog data';
        this.changelog = []; // Reset to empty array on error
      } finally {
        this.loadingChangelog = false;
      }
    },

    async loadMoreChangelog() {
      if (this.loadingMoreChangelog || !this.hasMoreChangelog) return;
      
      this.loadingMoreChangelog = true;
      
      try {
        const baseUrl = this.getApiBaseUrl();
        // Note: You would need to modify the backend endpoint to support offset/pagination
        // For now, we'll just increase the limit
        const newLimit = this.changelogOffset + this.changelogLimit;
        const response = await this.$axios.get(
          `${baseUrl}/getData/getCellarItemsChangelog/${this.ownerType}/${this.id}?limit=${newLimit}`
        );
        
        if (response.data.code === 200) {
          const newChangelog = response.data.data.changelog || [];
          this.changelog = newChangelog;
          this.hasMoreChangelog = newChangelog.length >= newLimit;
          this.changelogOffset = newChangelog.length;
        }
      } catch (error) {
        console.error('Error loading more changelog:', error);
      } finally {
        this.loadingMoreChangelog = false;
      }
    },

    formatChangelogEntry(entry) {
      if (!entry) return 'Unknown change';
      
      const date = this.formatChangelogDate(entry.changeDate);
      const drinkName = entry.listingName || 'Unknown Drink';
      const producerName = entry.producerName ? ` by ${entry.producerName}` : '';
      
      switch (entry.changeType) {
        case 'CREATED': {
          const quantity = entry.quantityDelta || 1;
          return `<strong>${date}:</strong> Added ${quantity} bottle${quantity !== 1 ? 's' : ''} of ${drinkName}${producerName}`;
        }
          
        case 'QUANTITY_UPDATED': {
          if (entry.quantityDelta) {
            const change = entry.quantityDelta > 0 ? `Added ${entry.quantityDelta}` : `Removed ${Math.abs(entry.quantityDelta)}`;
            return `<strong>${date}:</strong> ${change} bottle${Math.abs(entry.quantityDelta) !== 1 ? 's' : ''} of ${drinkName}${producerName}`;
          }
          return `<strong>${date}:</strong> Updated quantity of ${drinkName}${producerName}`;
        }
          
        case 'STATUS_CHANGED': {
          // Check for status transition in the aggregated format first
          if (entry.transitions && entry.transitions.status) {
            const statusTransition = entry.transitions.status;
            const quantity = entry.entryCount || 1;
            const bottleText = quantity === 1 ? 'bottle' : 'bottles';
            
            if (statusTransition.includes('→ Consumed')) {
              return `<strong>${date}:</strong> Consumed ${quantity} ${bottleText} of ${drinkName}${producerName}`;
            }
            return `<strong>${date}:</strong> Changed status of ${quantity} ${bottleText} of ${drinkName}${producerName}: ${statusTransition}`;
          }
          
          // Fallback to newValue for detailed format
          const newStatus = entry.newValue || 'Unknown';
          if (newStatus === 'Consumed') {
            return `<strong>${date}:</strong> Consumed ${drinkName}${producerName}`;
          }
          return `<strong>${date}:</strong> Changed status of ${drinkName}${producerName} to ${newStatus}`;
        }
          
        case 'CONSUMPTION_CHANGED': {
          const quantity = entry.entryCount || 1;
          const bottleText = quantity === 1 ? 'bottle' : 'bottles';
          
          // Check for consumption transition in the aggregated format first
          if (entry.transitions && entry.transitions.consumption) {
            const consumptionTransition = entry.transitions.consumption;
            return `<strong>${date}:</strong> Updated consumption of ${quantity} ${bottleText} of ${drinkName}${producerName}: ${consumptionTransition}`;
          }
          
          // Fallback to newValue for detailed format
          const consumption = entry.newValue || 'Unknown';
          return `<strong>${date}:</strong> Marked ${quantity} ${bottleText} of ${drinkName}${producerName} as ${consumption.toLowerCase()}`;
        }
          
        case 'LOCATION_CHANGED': {
          const location = entry.newValue || 'New location';
          return `<strong>${date}:</strong> Moved ${drinkName}${producerName} to ${location}`;
        }
          
        case 'NOTES_UPDATED':
          return `<strong>${date}:</strong> Updated notes for ${drinkName}${producerName}`;
          
        case 'FINANCIAL_UPDATED':
          return `<strong>${date}:</strong> Updated pricing for ${drinkName}${producerName}`;
          
        case 'ARCHIVE_CHANGED': {
          const quantity = entry.entryCount || 1;
          const bottleText = quantity === 1 ? 'bottle' : 'bottles';
          
          // Check changeDescription to determine if it was archived or restored
          if (entry.changeDescription && entry.changeDescription.includes('archived')) {
            return `<strong>${date}:</strong> Archived ${quantity} ${bottleText} of ${drinkName}${producerName}`;
          } else if (entry.changeDescription && entry.changeDescription.includes('restored')) {
            return `<strong>${date}:</strong> Restored ${quantity} ${bottleText} of ${drinkName}${producerName}`;
          }
          
          // Fallback to newValue for detailed format
          const archived = entry.newValue === 'true';
          return `<strong>${date}:</strong> ${archived ? 'Archived' : 'Restored'} ${quantity} ${bottleText} of ${drinkName}${producerName}`;
        }
          
        case 'DELETED':
          return `<strong>${date}:</strong> Removed ${drinkName}${producerName} from cellar`;
          
        default:
          return `<strong>${date}:</strong> Updated ${drinkName}${producerName}`;
      }
    },

    formatChangelogDate(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays === 1) {
        return 'Today';
      } else if (diffDays === 2) {
        return 'Yesterday';
      } else if (diffDays <= 7) {
        return `${diffDays - 1} days ago`;
      } else {
        return date.toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric',
          year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
        });
      }
    },

    formatChangeType(changeType) {
      if (!changeType) return 'Unknown';
      
      const typeMap = {
        'CREATED': 'Added',
        'QUANTITY_UPDATED': 'Quantity',
        'STATUS_CHANGED': 'Status',
        'CONSUMPTION_CHANGED': 'Consumption',
        'LOCATION_CHANGED': 'Location',
        'NOTES_UPDATED': 'Notes',
        'FINANCIAL_UPDATED': 'Financial',
        'ARCHIVE_CHANGED': 'Archive',
        'DELETED': 'Deleted'
      };
      return typeMap[changeType] || changeType;
    },

    getChangeTypeBadgeClass(changeType) {
      if (!changeType) return 'bg-secondary';
      
      const classMap = {
        'CREATED': 'bg-success',
        'QUANTITY_UPDATED': 'bg-info',
        'STATUS_CHANGED': 'bg-warning text-dark',
        'CONSUMPTION_CHANGED': 'bg-primary',
        'LOCATION_CHANGED': 'bg-secondary',
        'NOTES_UPDATED': 'bg-info',
        'FINANCIAL_UPDATED': 'bg-dark',
        'ARCHIVE_CHANGED': 'bg-secondary',
        'DELETED': 'bg-danger'
      };
      return classMap[changeType] || 'bg-secondary';
    },

    // Helper method to get top N items from breakdowns
    getTopBreakdowns(breakdownData, limit = 5) {
      if (!breakdownData) return {};
      
      // Convert object to array, sort by count, and take top N
      const sortedEntries = Object.entries(breakdownData)
        .sort(([,a], [,b]) => b.count - a.count)
        .slice(0, limit);
      
      // Convert back to object
      return Object.fromEntries(sortedEntries);
    },

    // Helper method to get filtered purchase locations (excluding unknown)
    getFilteredPurchaseLocations(breakdownData, limit = 5) {
      if (!breakdownData) return {};
      
      // Filter out "Unknown Purchase Location" and sort by count
      const filteredEntries = Object.entries(breakdownData)
        .filter(([location]) => location !== 'Unknown Purchase Location')
        .sort(([,a], [,b]) => b.count - a.count)
        .slice(0, limit);
      
      // Convert back to object
      return Object.fromEntries(filteredEntries);
    },

    // Helper method to count filtered purchase locations
    getFilteredPurchaseLocationsCount(breakdownData) {
      if (!breakdownData) return 0;
      
      return Object.keys(breakdownData).filter(location => location !== 'Unknown Purchase Location').length;
    },

    // Helper method to get dashboard status badge class
    getDashboardStatusBadgeClass(status) {
      const statusClasses = {
        'Purchased': 'bg-success',
        'In Possession': 'bg-primary',
        'On Its Way': 'bg-warning text-dark',
        'Held Elsewhere': 'bg-info',
        'Wishlisted': 'bg-secondary',
        'Consumed': 'bg-dark'
      };
      return statusClasses[status] || 'bg-light text-dark';
    },
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
  padding-right: 1rem;
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

  font-weight: 700;
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
  transition: all 0.3s ease;
}

/* Mobile Filters Toggle Button */
.mobile-filters-toggle {
  padding: 0 1rem;
}

.mobile-filters-toggle .btn {
  border-radius: 8px;
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
}

/* Mobile Collapsible Filters */
@media (max-width: 450px) {
  .filters-container.mobile-collapsed {
    max-height: 0;
    padding: 0 1rem;
    overflow: hidden;
    border-bottom: none;
  }
  
  .filters-container:not(.mobile-collapsed) {
    max-height: 500px; /* Adjust based on your filters height */
    padding: 1rem;
  }
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

/* Responsive adjustments for grid items when sidebar is collapsed */
/* Custom 5-column layout for collapsed sidebar - with responsive breakpoints */
.col-lg-custom-5 {
  flex: 0 0 auto;
}

/* Mobile: 1 column (handled by col-12) */
@media (max-width: 767.98px) {
  .col-lg-custom-5 {
    width: 100%;
  }
}

/* Tablet: 2 columns */
@media (min-width: 768px) and (max-width: 991.98px) {
  .col-lg-custom-5 {
    width: 50%;
  }
}

/* Small Desktop: 3 columns */  
@media (min-width: 992px) and (max-width: 1199.98px) {
  .col-lg-custom-5 {
    width: 33.333333%;
  }
}

/* Medium Desktop: 4 columns */
@media (min-width: 1200px) and (max-width: 1399.98px) {
  .col-lg-custom-5 {
    width: 25%;
  }
}

/* Large Desktop: 5 columns */
@media (min-width: 1400px) {
  .col-lg-custom-5 {
    width: 20%; /* 100% / 5 = 20% per column */
  }
}

@media (min-width: 768px) {
  /* For medium screens (tablets) when sidebar is collapsed, optimize for 3-column layout */
  .col-md-4 .cellar-item-card {
    min-height: 360px;
  }
  
  .col-md-4 .card-title {
    font-size: 0.97rem;
    line-height: 1.3;
  }
  
  .col-md-4 .card-text {
    font-size: 0.87rem;
  }
}

@media (min-width: 992px) {
  /* When sidebar is collapsed, we have more items per row, so ensure consistent spacing */
  .col-lg-custom-5 .cellar-item-card {
    min-height: 320px; /* Smaller height for 5-column layout */
  }
  
  .col-lg-custom-5 .card-title {
    font-size: 0.9rem; /* Smaller title for more compact layout */
    line-height: 1.2;
  }
  
  .col-lg-custom-5 .card-text {
    font-size: 0.8rem; /* Smaller text for more compact layout */
  }
  
  .col-lg-custom-5 .card-body {
    padding: 0.75rem; /* Slightly reduce padding */
  }
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

.quantity-volume-badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background-color: rgba(13, 202, 240, 0.9);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(4px);
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

/* List View Styles */
.cellar-item-list-card {
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
  cursor: pointer;
}

.cellar-item-list-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border-color: #c0c0c0;
}

.cellar-item-list-card:focus {
  outline: 2px solid #007bff;
  outline-offset: 2px;
}

.list-img-container {
  position: relative;
  height: 120px;
  overflow: hidden;
  border-radius: 0.5rem 0 0 0.5rem;
  background-color: #f8f9fa;
}

.list-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cellar-item-list-card .card-body {
  padding: 1rem;
}

.cellar-item-list-card .card-title {
  font-size: 1.1rem;
  font-weight: 600;
  line-height: 1.3;
  margin-bottom: 0.5rem;
}

.cellar-item-list-card .status-breakdown {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

@media (max-width: 991.98px) {
  .list-img-container {
    height: 100px;
  }
  
  .cellar-item-list-card .card-body {
    padding: 0.75rem;
  }
  
  .cellar-item-list-card .card-title {
    font-size: 1rem;
  }
}

@media (max-width: 575.98px) {
  .list-img-container {
    height: 80px;
  }
  
  .cellar-item-list-card .card-body {
    padding: 0.5rem;
  }
}

/* Inline Quantity Volume Badge for List View */
.quantity-volume-badge-inline {
  background-color: rgba(13, 202, 240, 0.9);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(4px);
  display: inline-block;
}

/* View Toggle Button Styles */
.btn-group .btn.active {
  background-color: #f0b358;
  border-color: #f0b358;
  color: #000;
}

.btn-outline-secondary {
  color: #223957;
  border-color: #223957;
}

.btn-outline-secondary:hover {
  background-color: #f0b358;
  border-color: #f0b358;
  color: #000;
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

/* Date Picker Trigger Styling */
.date-picker-trigger {
  cursor: pointer;
  transition: all 0.15s ease-in-out;
  user-select: none;
}

.date-picker-trigger:hover {
  background-color: #e7f3ff !important;
  border-color: #0d6efd !important;
  color: #0d6efd !important;
}

.date-picker-trigger:active {
  background-color: #cce7ff !important;
  border-color: #0a58ca !important;
  color: #0a58ca !important;
  transform: scale(0.98);
}

.date-picker-trigger i {
  font-size: 1.1rem;
  transition: transform 0.15s ease-in-out;
}

.date-picker-trigger:hover i {
  transform: scale(1.1);
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
  /* margin-top: auto; */
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
  flex: 0 0 30%;
  max-width: 100px;
  min-width: 75px;
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
    flex: 0 0 35%;
    max-width: 90px;
    min-width: 70px;
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
    font-size: 0.5rem;
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
    font-size: 0.7rem;
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

/* Google Maps autocomplete dropdown positioning with Y-axis translation */
:global(.pac-container.add-drink-pac-container) {
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 0.375rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  font-family: inherit;
  z-index: 1051 !important;
  transform: translateY(-920px) !important; 
  position: relative !important;
  @media (max-width: 451px){
    transform: translateY(-683px) !important;
  }
}

/* Google Maps autocomplete dropdown positioning with Y-axis translation */
:global(.pac-container) {
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 0.375rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  font-family: inherit;
  z-index: 1051 !important;
  transform: translateY(-920px) !important; 
  position: relative !important;
    @media (max-width: 451px){
    transform: translateY(-753px) !important;
  }
}

/* Specific styling for purchase location autocomplete dropdown */
/* :global(.pac-container.purchase-location-pac) {
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 0.375rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  font-family: inherit;
  z-index: 1051 !important;
  transform: translateY(-920px) !important; 
  position: relative !important;
  border-left: 3px solid #007bff;

  @media (max-width: 991px) {
    transform: translateY(-753px) !important;
  }
} */


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

/* Cellar Change Log Styles */
.cellar-change-log .card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: 1px solid #e0e0e0;
}

.cellar-change-log .card-header {
  background: linear-gradient(45deg, #f8f9fa, #ffffff);
  border-bottom: 1px solid #e0e0e0;
  padding: 1rem 1.25rem;
}

.cellar-change-log .card-title {
  color: #495057;
  font-weight: 600;
  margin: 0;
  display: flex;
  align-items: center;
}

.cellar-change-log .card-title i {
  color: #6c757d;
}

.changelog-entries {
  /* max-height: 400px; */
  overflow-y: auto;
}

.changelog-entry {
  background-color: #fafbfc;
  border: 1px solid #e9ecef !important;
  transition: all 0.2s ease;
}

.changelog-entry:hover {
  background-color: #f1f3f4;
  border-color: #d1ecf1 !important;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.changelog-entry .change-description {
  font-size: 0.9rem;
  line-height: 1.4;
  color: #495057;
}

.changelog-entry .change-details {
  font-size: 0.8rem;
  color: #6c757d;
}

.changelog-entry .change-date {
  font-size: 0.75rem;
  color: #868e96;
  font-weight: 500;
}

.changelog-entry .change-type-badge .badge {
  font-size: 0.65rem;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
}

/* Compact List View Styles */
.cellar-item-compact-card {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  transition: all 0.2s ease;
  cursor: pointer;
  background-color: #ffffff;
}

.cellar-item-compact-card:hover {
  border-color: rgba(13, 202, 240, 0.5);
  box-shadow: 0 4px 8px rgba(13, 202, 240, 0.15);
  transform: translateY(-1px);
}

.cellar-item-compact-card .card-body {
  padding: 0.75rem 1rem;
}

.cellar-item-compact-card .card-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 0.25rem;
  line-height: 1.3;
}

.cellar-item-compact-card .text-muted {
  font-size: 0.8rem;
  color: #6c757d !important;
}

/* Badge row styling for compact view */
.cellar-item-compact-card .d-flex.gap-1 {
  gap: 0.375rem !important;
}

.cellar-item-compact-card .d-flex.gap-1 .badge {
  margin-right: 0 !important;
}

/* Responsive adjustments for compact view */
@media (max-width: 992px) {
  .cellar-item-compact-card .row > div {
    margin-bottom: 0.5rem;
  }
  
  .cellar-item-compact-card .card-title {
    font-size: 0.85rem;
  }
  
  .cellar-item-compact-card .text-muted {
    font-size: 0.75rem;
  }
  
  .cellar-item-compact-card .quantity-volume-badge-inline {
    font-size: 0.7rem;
    padding: 0.2rem 0.4rem;
  }
  
  .cellar-item-compact-card .status-badge {
    font-size: 0.65rem;
    padding: 0.15rem 0.3rem;
  }

  /* Stack badges vertically on mobile if needed */
  .cellar-item-compact-card .d-flex.gap-1 {
    flex-direction: row;
    flex-wrap: wrap;
  }
}

/* Responsive adjustments for changelog */
@media (max-width: 768px) {
  .changelog-entries {
    max-height: 300px;
  }
  
  .changelog-entry {
    padding: 0.75rem !important;
    margin-bottom: 0.75rem !important;
  }
  
  .changelog-entry .change-description {
    font-size: 0.85rem;
  }
  
  .changelog-entry .change-details {
    font-size: 0.75rem;
  }
  
  .changelog-entry .d-flex {
    flex-direction: column;
    align-items: start !important;
  }
  
  .changelog-entry .text-end {
    text-align: start !important;
    margin-top: 0.5rem;
  }
}

/* Collapsible Right Sidebar */
.right-sidebar-tab {
  position: fixed;
  top: 50%;
  right: 0;
  transform: translateY(-50%);
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  padding: 20px 10px;
  border-radius: 12px 0 0 12px;
  cursor: pointer;
  z-index: 1000;
  box-shadow: -3px 0 15px rgba(0, 123, 255, 0.3);
  transition: all 0.3s ease;
  min-height: 100px;
  display: flex;
  align-items: center;
  border: none;
  outline: none;
  opacity:90%;
}

.right-sidebar-tab:hover {
  background: linear-gradient(135deg, #0056b3, #004085);
  transform: translateY(-50%) translateX(-8px);
  box-shadow: -5px 0 20px rgba(0, 123, 255, 0.4);
}

.right-sidebar-tab .tab-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.right-sidebar-tab .tab-text {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}

.right-sidebar-tab i {
  font-size: 1.4rem;
  opacity: 0.9;
}

.right-sidebar-column {
  transition: all 0.3s ease;
}

.right-sidebar-content {
  padding: 1rem;
}

/* Responsive adjustments for mobile */
@media (max-width: 991.98px) {
  .right-sidebar-tab {
    position: fixed;
    top: 50%;
    right: 0;
    transform: translateY(-50%);
    width: auto;
    border-radius: 12px 0 0 12px;
    margin: 0;
    min-height: 100px;
    z-index: 1000;
  }
  
  .right-sidebar-tab .tab-content {
    flex-direction: column;
    gap: 10px;
  }
  
  .right-sidebar-tab .tab-text {
    writing-mode: vertical-rl;
    text-orientation: mixed;
  }
}

/* Extra small screens - make tab much smaller */
@media (max-width: 450px) {
  .right-sidebar-tab {
    padding: 0px 0px !important;
    min-height: 70px !important;
    border-radius: 8px 0 0 8px !important;
  }
  
  .right-sidebar-tab .tab-content {
    gap: 6px !important;
  }
  
  .right-sidebar-tab .tab-text {
    font-size: 0.7rem !important;
    letter-spacing: 1px !important;
  }
  
  .right-sidebar-tab i {
    font-size: 1.1rem !important;
  }
}

/* Mobile Add Drinks Modal */
.add-drink-to-cellar-mobile {
  padding: 0;
}

.add-drink-to-cellar-mobile .form-group {
  margin-bottom: 1rem;
}

.add-drink-to-cellar-mobile .list-group {
  border-radius: 0.375rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.add-drink-to-cellar-mobile .list-group-item {
  border-color: #dee2e6;
}

.add-drink-to-cellar-mobile .list-group-item:hover {
  background-color: #f8f9fa;
}

/* On large screens, make the sidebar slide in */
@media (min-width: 992px) {
  .main-content {
    position: relative;
    overflow-x: hidden;
  }
  
  .right-sidebar-column {
    position: fixed;
    top: 0;
    right: -500px; /* Hide off-screen by default - matches width */
    width: 500px;
    height: 100vh;
    background: white;
    z-index: 999;
    box-shadow: -4px 0 12px rgba(0, 0, 0, 0.15);
    transition: right 0.3s ease;
    overflow-y: auto;
    padding-top: 120px; /* Account for navbar */
  }
  
  .right-sidebar-column.expanded {
    right: 0; /* Slide in when expanded */
  }
  
  .right-sidebar-column:not(.expanded) .right-sidebar-content {
    display: none;
  }
  
  /* Adjust left column when sidebar is expanded */
  .col-12.col-lg-8 {
    transition: all 0.3s ease;
  }
}

/* Fix checkbox label alignment */
.form-check {
  text-align: left !important;
}

.form-check-label {
  text-align: left !important;
}

/* Specifically target the drink-now filter */
#drinkNowFilter + .form-check-label {
  text-align: left !important;
  margin-left: 0.25rem;
}
.input-group-sm > .form-select{
  padding-right:2rem;
}

/* Custom responsive layout for 7 filters */
@media (min-width: 1200px) {
  .col-xl-1_8 {
    flex: 0 0 auto;
    width: 12.5%; /* 100% / 8 = 12.5% for 8 equal filters */
  }
  
  .col-xl-1_7 {
    flex: 0 0 auto;
    width: 14.2857%; /* 100% / 7 = ~14.29% for 7 equal filters */
  }
}

/* Public/Private Toggle Styling */
.form-check.form-switch {
  padding-left: 2.5em;
}

.form-check.form-switch .form-check-input {
  width: 2em;
  margin-left: -2.5em;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='rgba%2855, 63, 81, 0.75%29'/%3e%3c/svg%3e");
}

.form-check.form-switch .form-check-input:checked {
  background-color: #198754;
  border-color: #198754;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='rgba%28255, 255, 255, 1.0%29'/%3e%3c/svg%3e");
}

.form-check.form-switch .form-check-label {
  margin-left: 0.5rem;
  font-weight: 500;
  color: #6c757d;
}

.form-check.form-switch .form-check-input:checked + .form-check-label {
  color: #198754;
}

/* Ensure dropdowns in modals appear above other elements */
.modal .dropdown-menu {
  z-index: 1056 !important; /* Higher than modal backdrop (1055) */
}

/* Group actions dropdown styling */
.action-buttons .dropdown-menu {
  min-width: 200px;
}

.action-buttons .dropdown-item {
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-buttons .dropdown-item:hover {
  background-color: #f8f9fa;
}

.action-buttons .dropdown-item.text-danger:hover {
  background-color: #f8d7da;
  color: #721c24 !important;
}

/* Search Results Dropdown State */
.cellar-change-log.search-results-open {
  transform: translateY(150px);
  transition: transform 0.3s ease-in-out;
}

.cellar-change-log {
  transition: transform 0.3s ease-in-out;
}

</style>
