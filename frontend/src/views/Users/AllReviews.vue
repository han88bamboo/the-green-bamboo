<template>
  <NavBar />

  <!-- Loading -->
  <LoadingWithFunFact v-if="dataLoaded === false" />

  <!-- Error -->
  <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="dataLoaded == null">
    <span>An error occurred while loading this page, please try again!</span>
    <br />
    <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
      <span class="fs-5 fst-italic"> Return to previous page </span>
    </button>
    <router-link :to="'/'" class="mx-1">
      <button class="btn primary-btn btn-sm">
        <span class="fs-5 fst-italic"> Home </span>
      </button>
    </router-link>
  </div>

  <!-- Main Content -->
  <div v-if="dataLoaded" class="userprofile mt-5 mobile-mt-3">
    <div class="container text-start">
      <div class="row mobile-px-3">
        <div class="col-12 col-md-10 mx-auto mobile-px-3">
          <!-- Header -->
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
              <h3 class="mb-1 mobile-mt-3 mobile-fs-5"><b>Drinks Reviewed by {{ displayUser.displayName || displayUser.username }}</b></h3>
              <p class="text-muted mb-0 mobile-rating-smaller-text-2"><span class="fw-bold">
                {{ totalReviews }} drink{{ totalReviews !== 1 ? 's' : '' }} reviewed </span>
                <span v-if="!ownProfile">(private reviews are hidden)</span>
                <span v-if="ownProfile">(your private reviews will be hidden from the public)</span>
              </p>
            </div>
            <button
              class="mobile-view-hide btn primary-btn"
              @click="$router.push(`/profile/user/${displayUserID}/${routeUsername}`)"
            >
              Back to Profile
            </button>
            <button
              class="mobile-view-show btn primary-btn btn-sm fw-bold"
              @click="$router.push(`/profile/user/${displayUserID}/${routeUsername}`)"
            >
              <i class="bi bi-arrow-return-left"></i>
            </button>
          </div>

          <!-- Actions row (mobile-first): View toggle + Sort + Filters -->
          <div class="d-flex align-items-center justify-content-between mb-3 d-md-none">
            <!-- View toggle -->
            <div class="btn-group me-2" role="group" aria-label="View toggle">
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
                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5z"/>
                </svg>
              </button>
            </div>

            <!-- Sort (compact) -->
            <div class="flex-grow-1 mx-2">
              <select v-model="sortBy" @change="loadPageReviews(1)" class="form-select form-select-md">
                <option value="newest">Newest</option>
                <option value="oldest">Oldest</option>
                <option value="highest">Highest ★</option>
                <option value="lowest">Lowest ★</option>
              </select>
            </div>

            <!-- Filters trigger -->
            <button
              class="btn btn-outline-secondary btn-md"
              data-bs-toggle="offcanvas"
              data-bs-target="#filtersSheet"
              type="button"
            >
              Filters <span v-if="activeFilterCount">({{ activeFilterCount }})</span>
            </button>
          </div>

          <!-- Active filter chips -->
          <div v-if="activeFilters.length" class="d-md-none d-flex flex-wrap gap-2 mb-3">
            <span
              v-for="chip in activeFilters"
              :key="chip.key"
              class="badge rounded-pill text-bg-light px-2 py-2 border"
              style="font-weight: 500;"
            >
              {{ chip.label }}
              <button class="btn btn-sm btn-link p-0 ms-1" @click="removeFilter(chip.key)" aria-label="Remove">✕</button>
            </span>
            <button class="btn btn-link p-0 ms-1" @click="clearAllFilters">Clear all</button>
          </div>

          <!-- Desktop filters (original row), hidden on mobile -->
          <div class="row mb-4 d-none d-md-flex">
            <div class="col-md-2">
              <label class="form-label">Filter by Rating:</label>
              <select v-model="ratingFilter" @change="loadPageReviews(1)" class="form-select">
                <option value="">All Ratings</option>
                <option value="9-10">Excellent (9-10)</option>
                <option value="7-8">Good (7-8)</option>
                <option value="5-6">Average (5-6)</option>
                <option value="1-4">Poor (1-4)</option>
              </select>
            </div>
            <div class="col-md-2">
              <label class="form-label">Filter by Country:</label>
              <select v-model="countryFilter" @change="loadPageReviews(1)" class="form-select">
                <option value="">All Countries</option>
                <option v-for="country in availableCountries" :key="country" :value="country">
                  {{ country }}
                </option>
              </select>
            </div>
            <div class="col-md-2">
              <label class="form-label">Filter by Drink Type:</label>
              <select v-model="drinkTypeFilter" @change="onDrinkTypeChange" class="form-select">
                <option value="">All Drink Types</option>
                <option v-for="drinkType in availableDrinkTypes" :key="drinkType" :value="drinkType">
                  {{ drinkType }}
                </option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">
                Filter by Drink Category:
                <span v-if="!drinkTypeFilter" class="text-muted small fst-italic">(Select drink type first)</span>
              </label>
              <select
                v-model="typeCategoryFilter"
                @change="loadPageReviews(1)"
                class="form-select"
                :disabled="!drinkTypeFilter"
                :class="{ 'text-muted': !drinkTypeFilter }"
              >
                <option value="">All Categories</option>
                <option v-for="category in availableTypeCategories" :key="category" :value="category">
                  {{ category }}
                </option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">Sort by:</label>
              <select v-model="sortBy" @change="loadPageReviews(1)" class="form-select">
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
                <option value="highest">Highest Rating</option>
                <option value="lowest">Lowest Rating</option>
              </select>
            </div>
          </div>

          <!-- Offcanvas Filters (mobile) -->
          <div class="offcanvas offcanvas-bottom h-auto d-md-none" tabindex="-1" id="filtersSheet" style="max-height: 80vh;">
            <div class="offcanvas-header">
              <h5 class="offcanvas-title">Filters</h5>
              <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
            </div>

            <div class="offcanvas-body">
              <div class="row g-3">
                <div class="col-12">
                  <label class="form-label mb-1">Rating</label>
                  <select v-model="ratingFilter" class="form-select form-select-sm">
                    <option value="">All Ratings</option>
                    <option value="9-10">Excellent (9–10)</option>
                    <option value="7-8">Good (7–8)</option>
                    <option value="5-6">Average (5–6)</option>
                    <option value="1-4">Poor (1–4)</option>
                  </select>
                </div>

                <div class="col-12">
                  <label class="form-label mb-1">Country</label>
                  <select v-model="countryFilter" class="form-select form-select-sm">
                    <option value="">All Countries</option>
                    <option v-for="c in availableCountries" :key="c" :value="c">{{ c }}</option>
                  </select>
                </div>

                <div class="col-12">
                  <label class="form-label mb-1">Drink Type</label>
                  <select v-model="drinkTypeFilter" @change="onDrinkTypeChange" class="form-select form-select-sm">
                    <option value="">All Drink Types</option>
                    <option v-for="t in availableDrinkTypes" :key="t" :value="t">{{ t }}</option>
                  </select>
                </div>

                <div class="col-12">
                  <label class="form-label mb-1">Category</label>
                  <select
                    v-model="typeCategoryFilter"
                    class="form-select form-select-sm"
                    :disabled="!drinkTypeFilter"
                  >
                    <option value="">All Categories</option>
                    <option v-for="cat in availableTypeCategories" :key="cat" :value="cat">{{ cat }}</option>
                  </select>
                </div>
              </div>
            </div>

            <div class="border-top p-3 d-flex justify-content-between align-items-center bg-white">
              <button class="btn btn-link text-danger" @click="clearAllFilters">Reset</button>
              <button class="btn primary-btn" data-bs-dismiss="offcanvas" @click="loadPageReviews(1)">Apply</button>
            </div>
          </div>

          <!-- View Toggle (desktop alignment) -->
          <div class="d-none d-md-flex justify-content-end mb-3">
            <div class="btn-group" role="group" aria-label="View toggle">
              <button
                type="button"
                class="btn btn-outline-secondary"
                :class="{ active: viewMode === 'grid' }"
                @click="viewMode = 'grid'"
                title="Grid View"
              >
                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M1 2.5A1.5 1.5 0 0 1 2.5 1h3A1.5 1.5 0 0 1 7 2.5v3A1.5 1.5 0 0 1 5.5 7h-3A1.5 1.5 0 0 1 1 5.5v-3zm8 0A1.5 1.5 0 0 1 10.5 1h3A1.5 1.5 0 0 1 15 2.5v3A1.5 1.5 0 0 1 13.5 7h-3A1.5 1.5 0 0 1 9 5.5v-3zm-8 8A1.5 1.5 0 0 1 2.5 9h3A1.5 1.5 0 0 1 7 10.5v3A1.5 1.5 0 0 1 5.5 15h-3A1.5 1.5 0 0 1 1 13.5v-3zm8 0A1.5 1.5 0 0 1 10.5 9h3a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5h-3A1.5 1.5 0 0 1 9 13.5v-3z"/></svg>
              </button>
              <button
                type="button"
                class="btn btn-outline-secondary"
                :class="{ active: viewMode === 'list' }"
                @click="viewMode = 'list'"
                title="List View"
              >
                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5z"/></svg>
              </button>
            </div>
          </div>

          <!-- Loading overlay for page transitions -->
          <div v-if="loadingPage" class="d-flex justify-content-center align-items-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading reviews...</span>
            </div>
            <span class="ms-2">Loading reviews...</span>
          </div>

          <!-- Reviews List (List View) -->
          <div v-else-if="filteredReviews && filteredReviews.length > 0 && viewMode === 'list'">
            <div v-for="review in paginatedReviews" :key="review.id" class="mb-4">
              <div style="display: flex" class="row mb-2 border rounded p-3">
                <div class="col-3 mobile-col-3 mobile-pe-0">
                  <!-- Image wrapper with notch overlay for private reviews -->
                  <div style="position: relative; display: inline-block; border-radius: 10px; overflow: hidden;">
                    <!-- Notch Overlay for Private Review -->
                    <div v-if="!review.isPublic" class="item-notch item-notch-private">
                      <div class="notch-content">
                        <span class="notch-icon"><i class="bi bi-eye-slash"></i></span>
                        <span class="notch-text">Private</span>
                      </div>
                    </div>
                    
                    <img :src="review.photo || defaultDrinkImage" alt="" class="rounded bottle-img" />
                  </div>
                </div>
                <div class="col-9 mobile-col-9 mobile-ps-2">
                  <a
                    :href="'/listing/view/' + review.reviewTarget + '/' + slugify(getListingName(review.reviewTarget) || 'unknown-listing')"
                    style="text-decoration: none; color: #223957"
                  >
                    <p class="fs-5 mobile-fs-6 mb-1 mobile-mb-0_5 default-clickable-text">
                      <b>{{ getListingName(review.reviewTarget) }}</b>
                    </p>
                  </a>

                  <p class="text-muted small mb-2" v-if="getListingProducerName(review.reviewTarget)">
                    by {{ getListingProducerName(review.reviewTarget) }}
                  </p>

                  <p class="mb-2 small" style="color: #f0b358;" v-if="getListingDrinkType(review.reviewTarget) || getListingCountry(review.reviewTarget)">
                    <span v-if="getListingDrinkType(review.reviewTarget)">{{ getListingDrinkType(review.reviewTarget) }}</span>
                    <span v-if="getListingDrinkType(review.reviewTarget) && getListingCountry(review.reviewTarget)"> / </span>
                    <span v-if="getListingCountry(review.reviewTarget)">{{ getListingCountry(review.reviewTarget) }}</span>
                  </p>

                  <div class="d-flex justify-content-between align-items-center">
                    <p v-if="!isNaN(parseFloat(review.rating))" class="fs-4 mobile-fs-5 fw-bold rating-text mobile-mb-1 mb-0">
                      {{ parseFloat(review.rating).toFixed(1) }}★
                    </p>
                  </div>

                  <div class="mb-2">
                    <p class="mobile-fs-7 mb-1" v-if="review.reviewTitle"><b>{{ review.reviewTitle }}</b></p>
                    <p class="mobile-fs-7 mb-2" v-if="review.reviewDesc">{{ review.reviewDesc }}</p>
                  </div>
                  <div class="mb-2">
                    <span
                      v-for="(tag, index) in review.flavorTag"
                      :key="index"
                      class="mobile-view-hide badge rounded-pill-user-profile me-2 mb-1 mobile-me-0_5 mobile-mb-0_5"
                      :style="{ backgroundColor: getTagColor(tag) }"
                    >
                      {{ getTagName(tag) }}
                    </span>
                    <span
                      v-for="(tag, index) in review.observationTag"
                      :key="index"
                      class="mobile-view-hide badge rounded-pill-user-profile me-2 mb-1 mobile-me-0_5 mobile-mb-0_5"
                      style="background-color: #f0b358; color: black"
                    >
                      {{ tag }}
                    </span>

                    <!-- Mobile limited tags -->
                    <span
                      v-for="(tag, index) in review.flavorTag?.slice(0, 2)"
                      :key="index"
                      class="mobile-view-show badge rounded-pill-user-profile me-2 mb-1 mobile-me-0_5 mobile-mb-0_5"
                      :style="{ backgroundColor: getTagColor(tag) }"
                    >
                      {{ getTagName(tag) }}
                    </span>
                    <span
                      v-for="(tag, index) in review.observationTag.slice(0, 1)"
                      :key="index"
                      class="mobile-view-show badge rounded-pill-user-profile me-2 mb-1 mobile-me-0_5 mobile-mb-0_5"
                      style="background-color: #f0b358; color: black"
                    >
                      {{ tag }}
                    </span>
                  </div>



                  
                  <div class="mb-2">
                    <p class="text-muted small mb-0">
                      Drank on {{ formatDate(review.createdDate) }}
                    </p>
                    <p class="text-muted small mb-0" v-if="review.location || review.address">
                      <i class="bi bi-geo"></i>{{ getLocationName(review.location) || review.address }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Reviews Grid (Grid View) -->
          <div v-else-if="filteredReviews && filteredReviews.length > 0 && viewMode === 'grid'" class="row">
            <div v-for="review in paginatedReviews" :key="review.id" class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4">
              <div class="card h-100 review-card border-light">
                <div class="card-img-top-wrapper">
                  <!-- Image wrapper with notch overlay for private reviews -->
                  <div style="position: relative; display: inline-block; border-radius: 10px; overflow: hidden; width: 100%; height: 100%;">
                    <!-- Notch Overlay for Private Review -->
                    <div v-if="!review.isPublic" class="item-notch item-notch-private">
                      <div class="notch-content">
                        <span class="notch-icon"><i class="bi bi-eye-slash"></i></span>
                        <span class="notch-text">Private</span>
                      </div>
                    </div>
                    
                    <img :src="review.photo || defaultDrinkImage" alt="" class="card-img-top review-card-img" />
                  </div>
                </div>

                <div class="card-body d-flex flex-column">
                  <a
                    :href="'/listing/view/' + review.reviewTarget + '/' + slugify(getListingName(review.reviewTarget) || 'unknown-listing')"
                    style="text-decoration: none; color: #223957"
                    class="text-decoration-none"
                  >
                    <h6 class="card-title mb-2 default-clickable-text fw-bold">
                      {{ getListingName(review.reviewTarget) }}
                    </h6>
                  </a>

                  <p class="text-muted small mb-2" v-if="getListingProducerName(review.reviewTarget)">
                    by {{ getListingProducerName(review.reviewTarget) }}
                  </p>

                  <p class="mb-2 small" style="color: #f0b358;" v-if="getListingDrinkType(review.reviewTarget) || getListingCountry(review.reviewTarget)">
                    <span v-if="getListingDrinkType(review.reviewTarget)">{{ getListingDrinkType(review.reviewTarget) }}</span>
                    <span v-if="getListingDrinkType(review.reviewTarget) && getListingCountry(review.reviewTarget)"> / </span>
                    <span v-if="getListingCountry(review.reviewTarget)">{{ getListingCountry(review.reviewTarget) }}</span>
                  </p>

                  <p class="card-text mb-3 flex-grow-1 mobile-rating-smaller-text-2" v-if="review.reviewDesc">
                    {{ getReviewExcerpt(review.reviewDesc) }}
                    <a
                      :href="'/listing/view/' + review.reviewTarget + '/' + slugify(getListingName(review.reviewTarget) || 'unknown-listing')"
                      class="btn btn-sm primary-btn-less-round-blue text-decoration-none mt-2 fw-bold"
                      
                    >
                      See Full Review
                    </a>
                  </p>

                  <div class="d-flex justify-content-between align-items-center mt-auto">
                    <small class="text-muted">Drank on {{ formatDateGrid(review.createdDate) }}</small>
                    <span v-if="!isNaN(parseFloat(review.rating))" class="fw-bold rating-text">{{ parseFloat(review.rating).toFixed(1) }}★</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- No Reviews (standalone, not chained) -->
          <div
            v-else-if="dataLoaded && !loadingPage && (!filteredReviews || filteredReviews.length === 0)"
            class="text-center py-5"
          >
            <h4 class="text-muted">No drink reviews found.</h4>
            <p class="text-muted">
              {{ displayUser.displayName || displayUser.username }} has not reviewed any drinks that match the selected filter yet!
            </p>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="d-flex justify-content-center mt-4">
            <nav aria-label="Reviews pagination">
              <ul class="pagination">
                <li class="page-item" :class="{ disabled: currentPage === 1 || loadingPage }">
                  <button class="page-link" @click="changePage(currentPage - 1)" :disabled="currentPage === 1 || loadingPage">
                    <span v-if="loadingPage" class="spinner-border spinner-border-sm me-1" role="status"></span>
                    Previous
                  </button>
                </li>
                <li v-for="page in visiblePages" :key="page" class="page-item" :class="{ active: page === currentPage, disabled: loadingPage }">
                  <button class="page-link" @click="changePage(page)" :disabled="loadingPage">
                    <span v-if="loadingPage && page === currentPage" class="spinner-border spinner-border-sm me-1" role="status"></span>
                    {{ page }}
                  </button>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === totalPages || loadingPage }">
                  <button class="page-link" @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages || loadingPage">
                    <span v-if="loadingPage" class="spinner-border spinner-border-sm me-1" role="status"></span>
                    Next
                  </button>
                </li>
              </ul>
            </nav>
          </div>

          <!-- Load More (alt) -->
          <div v-if="hasMoreReviews && !showPagination" class="text-center mt-4">
            <button class="btn primary-btn" @click="loadMoreReviews" :disabled="loadingMore">
              {{ loadingMore ? 'Loading...' : 'Load More Reviews' }}
            </button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';

export default {
  name: "AllReviews",
  components: { NavBar, LoadingWithFunFact },
  data() {
    return {
      dataLoaded: false,

      // Default images
      defaultDrinkImage: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1748434288",

      // User data
      displayUserID: null,
      routeUsername: null,
      displayUser: {},
      
      // Current user data
      userID: null,
      ownProfile: false,

      // Reviews data
      allReviews: [], // Keep for compatibility, but will only contain current page
      filteredReviews: [],
      listings: {},
      venues: {},
      subTags: [],
      flavourTags: [],

      // Pagination
      currentPage: 1,
      reviewsPerPage: 20,
      totalReviews: 0,
      hasMoreReviews: true,
      loadingMore: false,
      showPagination: true,
      loadingPage: false, // New loading state for page transitions

      // Filtering and sorting
      ratingFilter: '',
      countryFilter: '',
      drinkTypeFilter: '',
      typeCategoryFilter: '',
      sortBy: 'newest',

      // Available options
      availableCountries: [],
      availableDrinkTypes: [],
      availableTypeCategories: [],

      // Loading states
      loadingReviews: false,

      // View mode
      viewMode: 'grid',
    };
  },
  computed: {
    paginatedReviews() {
      // With server-side pagination, filteredReviews already contains only the current page
      return this.filteredReviews;
    },
    totalPages() {
      // Use totalReviews from server response, not filteredReviews.length
      return Math.ceil(this.totalReviews / this.reviewsPerPage);
    },
    visiblePages() {
      const pages = [];
      const maxVisible = 5;
      const start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2));
      const end = Math.min(this.totalPages, start + maxVisible - 1);
      for (let i = start; i <= end; i++) pages.push(i);
      return pages;
    },

    /* ====== NEW: active filter chips/count ====== */
    activeFilters() {
      const chips = [];
      if (this.ratingFilter) chips.push({ key: 'ratingFilter', label: `Rating ${this.ratingFilter}` });
      if (this.countryFilter) chips.push({ key: 'countryFilter', label: this.countryFilter });
      if (this.drinkTypeFilter) chips.push({ key: 'drinkTypeFilter', label: this.drinkTypeFilter });
      if (this.typeCategoryFilter) chips.push({ key: 'typeCategoryFilter', label: this.typeCategoryFilter });
      return chips;
    },
    activeFilterCount() { return this.activeFilters.length; }
  },
  async mounted() {
    // Get current user info from localStorage
    const accID = localStorage.getItem("88B_accID");
    if (accID !== null) {
      this.userID = accID;
    }

    // Get route parameters
    this.displayUserID = parseInt(this.$route.params.userID);
    this.routeUsername = this.$route.params.username;

    // Check if viewing own profile
    if (this.displayUserID === parseInt(this.userID)) {
      this.ownProfile = true;
    }

    await this.loadData();
  },
  methods: {
    slugify(text) {
      if (!text) return '';
      return text
        .toString()
        .toLowerCase()
        .normalize('NFD')                    // Decompose accented characters
        .replace(/[\u0300-\u036f]/g, '')     // Remove diacritical marks
        .replace(/\s+/g, '-')                 // Replace spaces with hyphens
        .replace(/[^\w]/g, '');              // Remove non-word characters
    },
    
    async loadData() {
      try {
        this.dataLoaded = false;

        await this.getDisplayUserProfile();
        await this.loadPageReviews(1); // Load first page instead of all reviews
        await this.loadSupportingData();

        this.dataLoaded = true;
      } catch (error) {
        console.error("Error loading data:", error);
        this.dataLoaded = null;
      }
    },

    async getDisplayUserProfile() {
      const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUser/${this.displayUserID}`);
      this.displayUser = response.data;
    },

    async loadPageReviews(page = 1) {
      try {
        this.loadingPage = true;
        const offset = (page - 1) * this.reviewsPerPage;
        
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getAllUserReviews/${this.displayUserID}`,
          { 
            params: { 
              offset, 
              limit: this.reviewsPerPage 
            } 
          }
        );
        
        this.allReviews = response.data.reviews || []; // Current page only
        this.totalReviews = response.data.total || 0;
        this.hasMoreReviews = response.data.hasMore || false;
        this.currentPage = page;
        
        // Load supporting data for the new reviews (listings, etc.)
        await this.loadSupportingData();
        
        // Apply filters to current page data
        this.applyFilters();
        
      } catch (e) {
        console.error("Error loading reviews:", e);
        this.allReviews = [];
        this.totalReviews = 0;
      } finally {
        this.loadingPage = false;
      }
    },



    async loadSupportingData() {
      try {
        // Listings for review targets
        const listingIDs = [...new Set(this.allReviews.map(r => r.reviewTarget))];
        if (listingIDs.length > 0) {
          const listingsResponse = await this.$axios.post(
            `${process.env.VUE_APP_API_URL}/getData/getListingsByIDs`,
            { listingIDs }
          );

          this.listings = {};
          const countries = new Set();
          const drinkTypes = new Set();

          listingsResponse.data.forEach(listing => {
            this.listings[listing.id] = listing;
            if (listing.originCountry?.trim()) countries.add(listing.originCountry.trim());
            if (listing.drinkType?.trim()) drinkTypes.add(listing.drinkType.trim());
          });

          this.availableCountries = [...countries].sort();
          this.availableDrinkTypes = [...drinkTypes].sort();
        }

        // Venues
        const venueResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenues`);
        this.venues = {};
        venueResponse.data.forEach(v => { this.venues[v.id] = v; });

        // Tags
        const subTagsResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getSubTags`);
        this.subTags = subTagsResponse.data;
        const flavourTagsResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getFlavourTags`);
        this.flavourTags = flavourTagsResponse.data;

        // Initialize type categories
        this.updateAvailableTypeCategories();
      } catch (e) {
        console.error("Error loading supporting data:", e);
      }
    },

    applyFilters() {
      // With server-side pagination, we apply filters to the current page data only
      // For comprehensive filtering across all reviews, we'd need to reload from server with filter params
      let filtered = [...this.allReviews];

      // Privacy filter: Hide private reviews if not viewing own profile
      if (!this.ownProfile) {
        filtered = filtered.filter(r => r.isPublic !== false);
      }

      if (this.ratingFilter) {
        const [min, max] = this.ratingFilter.split('-').map(Number);
        filtered = filtered.filter(r => {
          const rating = parseFloat(r.rating);
          return rating >= min && rating <= max;
        });
      }

      if (this.countryFilter) {
        filtered = filtered.filter(r => {
          const listing = this.listings[r.reviewTarget];
          return listing && listing.originCountry === this.countryFilter;
        });
      }

      if (this.drinkTypeFilter) {
        filtered = filtered.filter(r => {
          const listing = this.listings[r.reviewTarget];
          return listing && listing.drinkType === this.drinkTypeFilter;
        });
      }

      if (this.typeCategoryFilter) {
        filtered = filtered.filter(r => {
          const listing = this.listings[r.reviewTarget];
          return listing && listing.typeCategory === this.typeCategoryFilter;
        });
      }

      filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'newest': return new Date(b.createdDate) - new Date(a.createdDate);
          case 'oldest': return new Date(a.createdDate) - new Date(b.createdDate);
          case 'highest': return parseFloat(b.rating) - parseFloat(a.rating);
          case 'lowest': return parseFloat(a.rating) - parseFloat(b.rating);
          default: return 0;
        }
      });

      this.filteredReviews = filtered;
      // Note: Don't reset currentPage here since we're working with server-side pagination
    },

    onDrinkTypeChange() {
      this.typeCategoryFilter = '';
      this.updateAvailableTypeCategories();
      // Reset to page 1 when filters change and reload data
      this.loadPageReviews(1);
    },

    updateAvailableTypeCategories() {
      if (!this.drinkTypeFilter) {
        this.availableTypeCategories = [];
        return;
      }
      const typeCategories = new Set();
      this.allReviews.forEach(r => {
        const listing = this.listings[r.reviewTarget];
        if (listing && listing.drinkType === this.drinkTypeFilter) {
          if (listing.typeCategory?.trim()) typeCategories.add(listing.typeCategory.trim());
        }
      });
      this.availableTypeCategories = [...typeCategories].sort();
    },

    async changePage(page) {
      if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
        await this.loadPageReviews(page);
        this.$nextTick(() => {
          const reviewsSection = document.querySelector('.userprofile');
          if (reviewsSection) reviewsSection.scrollIntoView({ behavior: 'smooth' });
        });
      }
    },

    getListingName(id) { return this.listings[id]?.listingName || 'Unknown Listing'; },
    getListingCountry(id) { return this.listings[id]?.originCountry || ''; },
    getListingDrinkType(id) { return this.listings[id]?.drinkType || ''; },
    getListingTypeCategory(id) { return this.listings[id]?.typeCategory || ''; },

    getListingProducerName(id) { return this.listings[id]?.producerName || ''; },
    getLocationName(id) { return this.venues[id]?.venueName || ''; },

    getTagName(tag) {
      if (!this.subTags || !this.flavourTags) return tag;
      const subTag = this.subTags.find(s => s.id === tag);
      if (subTag) {
        const flavour = this.flavourTags.find(f => f.id === subTag.familyTagId);
        return flavour ? flavour.familyTag : subTag.subtag;
      } else {
        const flavour = this.flavourTags.find(f => f.id === tag);
        return flavour ? flavour.familyTag : tag;
      }
    },

    getTagColor(tag) {
      if (!this.subTags || !this.flavourTags) return '#6c757d';
      const subTag = this.subTags.find(s => s.id === tag);
      if (subTag) {
        const flavour = this.flavourTags.find(f => f.id === subTag.familyTagId);
        return flavour ? flavour.hexcode : '#6c757d';
      } else {
        const flavour = this.flavourTags.find(f => f.id === tag);
        return flavour ? flavour.hexcode : '#6c757d';
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'Unknown date';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    },

    formatDateGrid(dateString) {
      if (!dateString) return 'Unknown date';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit' }).replace(/\//g, ' / ');
    },

    getReviewExcerpt(text) {
      if (!text) return '';
      const firstSentence = text.match(/^[^.!?]+[.!?]/);
      if (firstSentence && firstSentence[0].length <= 80) return firstSentence[0];
      const excerpt = text.substring(0, 80);
      const lastSpaceIndex = excerpt.lastIndexOf(' ');
      if (lastSpaceIndex > 60) return excerpt.substring(0, lastSpaceIndex) + '...';
      return excerpt + '...';
    },

    /* ====== NEW: chip helpers ====== */
    removeFilter(key) {
      this[key] = '';
      if (key === 'drinkTypeFilter') this.typeCategoryFilter = '';
      // Reset to page 1 when filters change and reload data
      this.loadPageReviews(1);
    },
    clearAllFilters() {
      this.ratingFilter = '';
      this.countryFilter = '';
      this.drinkTypeFilter = '';
      this.typeCategoryFilter = '';
      // Reset to page 1 when filters change and reload data
      this.loadPageReviews(1);
    }
  }
};
</script>

<style scoped>
.bottle-img {
  width: 100%;
  object-fit: cover;
}

.rounded-pill-user-profile {
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
}

.rating-text {
  color: #f0b358;
}

.default-clickable-text:hover {
  text-decoration: underline !important;
}

.border {
  border-color: #e9ecef !important;
}

.border:hover {
  border-color: #dee2e6 !important;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.2s ease;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .mobile-col-3 {
    flex: 0 0 25%;
    max-width: 25%;
  }
  
  .mobile-col-9 {
    flex: 0 0 75%;
    max-width: 75%;
  }
  
  .mobile-pe-0 {
    padding-right: 0 !important;
  }
  
  .mobile-ps-2 {
    padding-left: 0.5rem !important;
  }
  
  .mobile-fs-6 {
    font-size: 1rem !important;
  }
  
  .mobile-fs-5 {
    font-size: 1.125rem !important;
  }
  
  .mobile-fs-7 {
    font-size: 0.875rem !important;
  }
  
  .mobile-mb-0_5 {
    margin-bottom: 0.25rem !important;
  }
  
  .mobile-me-0_5 {
    margin-right: 0.25rem !important;
  }
  
  .mobile-mb-0_5 {
    margin-bottom: 0.25rem !important;
  }
  
  .mobile-mb-1 {
    margin-bottom: 0.5rem !important;
  }
  
  .mobile-mt-3 {
    margin-top: 1rem !important;
  }
  
  .mobile-view-hide {
    display: none !important;
  }
  
  .mobile-view-show {
    display: inline !important;
  }
}

@media (min-width: 769px) {
  .mobile-view-hide {
    display: inline !important;
  }
  
  .mobile-view-show {
    display: none !important;
  }
}

.pagination .page-link {
  color: #223957;
  border-color: #dee2e6;
}

.pagination .page-item.active .page-link {
  background-color: #f0b358;
  border-color: #f0b358;
  color: #000;
}

.pagination .page-link:hover {
  color: #f0b358;
  background-color: #f8f9fa;
}

/* Disabled select styling */
.form-select:disabled {
  background-color: #f8f9fa;
  opacity: 0.6;
}

.form-select.text-muted {
  color: #6c757d !important;
}

/* Grid view styles */
.review-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.review-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.card-img-top-wrapper {
  height: 200px;
  overflow: hidden;
  background-color: #f8f9fa;
}

.review-card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-body {
  padding: 1rem;
}

.card-title {
  font-size: 1rem;
  line-height: 1.3;
}

/* View toggle buttons */
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

/* Notch overlay styles for private reviews */
.item-notch {
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 62px 62px 0 0;
  z-index: 10;
  overflow: visible;
  border-top-left-radius: 10px;
}

/* Private review notch - Dark grey theme */
.item-notch-private {
  border-color: #596269 transparent transparent transparent;
}

/* Notch content container - rotated text and icon */
.notch-content {
  position: absolute;
  top: -55px;
  left: -5px;
  transform: rotate(-45deg);
  transform-origin: center center;
  white-space: nowrap;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

/* Private review text styling */
.item-notch-private .notch-content {
  color: white;
}

/* Icon placeholder */
.notch-icon {
  font-size: 14px;
  font-weight: bold;
  line-height: 1;
}

/* Text label */
.notch-text {
  font-size: 9px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  line-height: 1;
}

/* Responsive sizing for mobile devices */
@media (max-width: 768px) {
  .item-notch {
    border-width: 65px 65px 0 0;
  }
  
  .notch-content {
    top: -56px;
    left: -3px;
  }
  
  .notch-icon {
    font-size: 12px;
  }
  
  .notch-text {
    font-size: 9px;
    letter-spacing: 0.2px;
  }
}

/* Extra small screens */
@media (max-width: 375px) {
  .item-notch {
    border-width: 55px 55px 0 0;
  }
  
  .notch-content {
    top: -50px;
    left: 2px;
  }
  
  .notch-icon {
    font-size: 10px;
  }
  
  .notch-text {
    font-size: 6px;
    letter-spacing: 0.1px;
  }
}
</style>
