<template>
  <NavBar />
  
  <div class="container px-4 mt-4">
    <div class="container">
      <!-- Header with Search and Add List Button (only show when not viewing individual list) -->
      <div v-if="!selectedList" class="row mb-4">
        <div class="col-12">
          <div class="row justify-content-left mb-2">
              <h3 class="text-start fw-bold mobile-fs-4">Browse, create and share drinks list. 📋✨</h3>
              <h5 class="text-start fw-bold mobile-fs-6">Bucket list wines 🍷, bar cart holy grails 👑, beers for the bottle share🍻... </h5>
          </div>
          <div class="d-flex justify-content-left align-items-center mb-4">
            <!-- Header -->
            <div class="input-group" style="max-width: 400px;">
              <input
                type="text"
                class="form-control"
                placeholder="Search for lists"
                v-model="searchTerm"
                @input="filterLists"
              />
              <button class="btn btn-outline-secondary" type="button">
                <i class="bi bi-search"></i>
              </button>
            </div>
            <button 
              v-if="userID"
              class="btn primary-btn-less-round-blue fw-bold btn-md ms-2 mobile-rating-smaller-text-2 "
              @click="goToMyProfile"
            >
              Add List
            </button>
          </div>
        </div>
      </div>

      <!-- Sort Options (Top Right) - only show when not viewing individual list -->
      <div v-if="!selectedList && filteredLists.length > 0" class="row mb-3">
        <div class="col-12 d-flex justify-content-end">
          <div class="btn-group btn-group-sm" role="group">
            <button 
              type="button" 
              class="btn"
              :class="sortBy === 'popular' ? 'btn-primary' : 'btn-outline-secondary'"
              @click="setSortBy('popular')"
            >
              Most Popular
            </button>
            <button 
              type="button" 
              class="btn"
              :class="sortBy === 'recent' ? 'btn-primary' : 'btn-outline-secondary'"
              @click="setSortBy('recent')"
            >
              Most Recent
            </button>
            <button 
              type="button" 
              class="btn"
              :class="sortBy === 'alphabetical' ? 'btn-primary' : 'btn-outline-secondary'"
              @click="setSortBy('alphabetical')"
            >
              Alphabetical
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3 text-muted">Loading public lists...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <h4 class="alert-heading">Error Loading Lists</h4>
        <p>{{ error }}</p>
        <button class="btn btn-outline-danger" @click="loadPublicLists">Try Again</button>
      </div>

      <!-- Individual List View -->
      <div v-else-if="selectedList" class="list-detail-view">
        <!-- Back Button (Left aligned) -->
        <div class="row mb-3">
          <div class="col-12 d-flex justify-content-start">
            <button class="btn btn-outline-secondary" @click="goBackToLists">
              <i class="bi bi-arrow-left"></i> Back to Find Lists
            </button>
          </div>
        </div>

        <!-- List Header -->
        <div class="row mb-4">
          <div class="col-12">
            <h2 class="fw-bold text-start">{{ selectedList.listName }}</h2>
            <p class="text-muted mb-2 text-start">{{ selectedList.listDesc || 'No description provided.' }}</p>
            <div class="d-flex align-items-center justify-content-between">
              <div class="d-flex align-items-center">
                <img
                  :src="selectedList.userPhoto || defaultProfilePhoto"
                  alt="Creator"
                  class="rounded-circle me-2"
                  style="width: 32px; height: 32px; object-fit: cover;"
                />
                <span class="text-muted">Created by</span>
                <span class="fw-bold ms-1">{{ selectedList.displayName || selectedList.username }}</span>
              </div>
              
              <div class="d-flex gap-2">
                <button
                  class="btn btn-sm d-flex align-items-center gap-1"
                  :class="hasUserUpvoted(selectedList) ? 'btn-dark' : 'btn-outline-secondary'"
                  @click="toggleUpvote(selectedList)"
                  :disabled="upvoting || !userID"
                  style="background-color: #f8f9fa; border-color: #dee2e6; color: #212529;"
                >
                  <i 
                    class="bi"
                    :class="hasUserUpvoted(selectedList) ? 'bi-hand-thumbs-up-fill' : 'bi-hand-thumbs-up'"
                  ></i>
                  <span>{{ selectedList.upvotes || 0 }}</span>
                </button>

                <button
                  class="btn btn-sm btn-outline-secondary d-flex align-items-center gap-1"
                  @click="shareList(selectedList)"
                  style="background-color: #f8f9fa; border-color: #dee2e6; color: #212529;"
                >
                  <i class="bi bi-reply share-icon"></i>
                  <span>Share</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- List Items Grid (Similar to UserProfile grid view) -->
        <div class="row" v-if="selectedListItems.length > 0">
          <div
            class="col-6 col-md-4 col-lg-3 mb-4"
            v-for="(item, index) in selectedListItems"
            :key="index"
          >
            <div class="card h-100 review-card border shadow-sm position-relative">
              <!-- Image -->
              <div class="card-img-top-wrapper">
                <img
                  :src="item.photo || defaultDrinkImage"
                  :alt="item.listingName"
                  class="card-img-top review-card-img"
                />
              </div>

              <!-- Body -->
              <div class="card-body d-flex flex-column">
                <!-- Title -->
                <a
                  :href="`/listing/view/${item.drinkId}/${encodeURIComponent(item.listingName)}`"
                  class="text-decoration-none"
                  style="color: #223957"
                >
                  <h6 class="card-title mb-2 fw-bold">{{ item.listingName }}</h6>
                </a>

                <!-- Type / Country -->
                <p class="mb-2 small fw-bold" style="color: #f0b358;" v-if="item.drinkType || item.originCountry">
                  {{ item.drinkType }}{{ item.drinkType && item.originCountry ? ' / ' : '' }}{{ item.originCountry || '' }}
                </p>

                <!-- Rating -->
                <h4 class="fw-bold mb-3" style="color:#f0b358">
                  {{
                    item.avgRating !== null && item.avgRating !== undefined
                      ? parseFloat(item.avgRating).toFixed(1)
                      : "-"
                  }}★
                </h4>

                <!-- Creator's Note (View-only for public lists) -->
                <div class="mt-auto" v-if="item.note && item.note.trim()">
                  <button
                    class="btn btn-sm w-100 text-white"
                    style="background-color: #ff3e31; border-color: #ff3e31;"
                    data-bs-toggle="modal"
                    :data-bs-target="`#noteModal${index}`"
                    @click="prepareNoteModal(item, index)"
                  >
                    View Note
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Note Modals (one for each listing) -->
          <div
            class="modal fade"
            v-for="(item, index) in selectedListItems"
            :key="`noteModal${index}`"
            :id="`noteModal${index}`"
            tabindex="-1"
            :aria-labelledby="`noteModalLabel${index}`"
            aria-hidden="true"
          >
            <div class="modal-dialog modal-dialog-centered">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" :id="`noteModalLabel${index}`">Creator's Note</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <p v-if="currentNote && currentNote.trim()" class="text-start">{{ currentNote }}</p>
                  <p v-else class="text-muted">No note provided.</p>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty state for selected list -->
        <div v-else class="text-center py-5">
          <p class="text-muted">This list is empty.</p>
        </div>
      </div>

      <!-- Lists Grid -->
      <div v-else class="row g-4 mb-5">
        <div
          v-for="list in paginatedLists"
          :key="list.id"
          class="col-12 col-md-6 col-lg-4"
        >
          <div class="card h-100 shadow-sm list-card">
            <!-- List Preview Images -->
            <div class="card-img-top position-relative" style="height: 200px; overflow: hidden;">
              <div class="pin-grid" v-if="list.previewItems && list.previewItems.length > 0">
                <!-- Main image (larger) -->
                <div class="pin-cell pin-main">
                  <img
                    v-if="list.previewItems[0]"
                    :src="list.previewItems[0].photo || defaultDrinkImage"
                    class="pin-img"
                    :alt="list.previewItems[0].listingName"
                  />
                  <div v-else class="pin-placeholder bg-light"></div>
                </div>
                
                <!-- Side images -->
                <div class="pin-cell pin-side1">
                  <img
                    v-if="list.previewItems[1]"
                    :src="list.previewItems[1].photo || defaultDrinkImage"
                    class="pin-img"
                    :alt="list.previewItems[1].listingName"
                  />
                  <div v-else class="pin-placeholder bg-light"></div>
                </div>
                
                <div class="pin-cell pin-side2">
                  <img
                    v-if="list.previewItems[2]"
                    :src="list.previewItems[2].photo || defaultDrinkImage"
                    class="pin-img"
                    :alt="list.previewItems[2].listingName"
                  />
                  <div v-else class="pin-placeholder bg-light"></div>
                </div>
              </div>
              
              <!-- Default placeholder if no preview items -->
              <div v-else class="d-flex align-items-center justify-content-center h-100 bg-light">
                <i class="bi bi-list-ul text-muted" style="font-size: 3rem;"></i>
              </div>
            </div>

            <!-- Card Body -->
            <div class="card-body d-flex flex-column p-3">
              <!-- List Name and Drink Count -->
              <div class="d-flex justify-content-between align-items-center mb-2">
                <a href="#" class="text-decoration-underline text-decoration-none" style="color: inherit;" @click.prevent="viewListDetails(list)">
                  <h5 class="card-title fw-bold mb-0 flex-grow-1 text-start">{{ list.listName }}</h5>
                </a>
                <small class="text-muted ms-2">{{ list.itemCount }} Drink{{ list.itemCount !== 1 ? 's' : '' }}</small>
              </div>
              <!-- Creator Info  -->
              <div class="mt-auto mb-2">
                <div class="text-center">
                  <div class="d-flex align-items-center justify-content-left ps-0">
                    <img
                      :src="list.userPhoto || defaultProfilePhoto"
                      alt="Creator"
                      class="rounded-circle me-2"
                      style="width: 24px; height: 24px; object-fit: cover;"
                    />
                    <span>Created by</span>
                    <span class="fw-bold ms-1">{{ list.displayName || list.username }}</span>
                  </div>
                </div>
              </div>

              <!-- List Description -->
              <p class="card-text text-muted mb-3 description-text text-start">
                {{ list.listDesc || '' }}
              </p>

              <!-- Action Buttons Row -->
              <div class="d-flex justify-content-between align-items-center mb-3">
                <!-- View Button (Left) -->
                <a
                  href="#"
                  class="btn btn-outline-secondary fw-semibold mobile-rating-smaller-text-2"
                  @click="viewListDetails(list)"
                >
                  View
                </a>

                <!-- Upvote and Share Buttons (Right) -->
                <div class="d-flex gap-2">
                  <!-- Upvote Button -->
                  <button
                    class="btn btn-sm d-flex align-items-center gap-1"
                    :class="hasUserUpvoted(list) ? 'btn-dark' : 'btn-outline-secondary'"
                    @click="toggleUpvote(list)"
                    :disabled="upvoting || !userID"
                    style="background-color: #f8f9fa; border-color: #dee2e6; color: #212529;"
                  >
                    <i 
                      class="bi"
                      :class="hasUserUpvoted(list) ? 'bi-hand-thumbs-up-fill' : 'bi-hand-thumbs-up'"
                    ></i>
                    <span>{{ list.upvotes || 0 }}</span>
                  </button>

                  <!-- Share Button -->
                  <button
                    class="btn btn-sm btn-outline-secondary d-flex align-items-center gap-1"
                    @click="shareList(list)"
                    style="background-color: #f8f9fa; border-color: #dee2e6; color: #212529;"
                  >
                    <i class="bi bi-reply share-icon"></i>
                    <span>Share</span>
                  </button>
                </div>
              </div>

              
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && !selectedList && filteredLists.length === 0" class="text-center py-5">
        <i class="bi bi-search text-muted mb-3" style="font-size: 4rem;"></i>
        <h4 class="text-muted">No lists found</h4>
        <p class="text-muted">Try adjusting your search criteria or check back later for new lists.</p>
      </div>

      <!-- Show More Button -->
      <div v-if="!selectedList && filteredLists.length > currentPage * itemsPerPage" class="text-center mt-4 mb-5">
        <button class="btn btn-warning" @click="loadMore">
          Show More
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import { useToast } from "vue-toastification";

export default {
  name: "FindLists",
  components: {
    NavBar,
  },
  data() {
    return {
      publicLists: [],
      filteredLists: [],
      selectedList: null,
      selectedListItems: [],
      loading: true,
      error: null,
      searchTerm: '',
      sortBy: 'popular',
      currentPage: 1,
      itemsPerPage: 12,
      upvoting: false,
      userID: null,
      userType: null,
      username: null,
      userUpvotedLists: [],

      currentNote: '',
      currentNoteListingIndex: null,
      
      // Default images
      defaultDrinkImage: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
    };
  },
  computed: {
    paginatedLists() {
      const start = 0;
      const end = this.currentPage * this.itemsPerPage;
      return this.filteredLists.slice(start, end);
    },
  },
  mounted() {
    // Get user info from localStorage
    this.userID = localStorage.getItem("88B_accID");
    this.userType = localStorage.getItem("88B_accType");
    this.username = localStorage.getItem("88B_accUsername");
    
    // Load public lists
    this.loadPublicLists();
  },
  methods: {
    async loadPublicLists() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getPublicLists`
        );
        
        if (response.data.code === 200) {
          this.publicLists = response.data.data;
          this.filterLists();
          
          // Load user's upvoted lists if logged in
          if (this.userID) {
            this.loadUserUpvotedLists();
          }
        }
      } catch (error) {
        console.error('Error loading public lists:', error);
        this.error = 'Failed to load public lists. Please try again later.';
      } finally {
        this.loading = false;
      }
    },

    async loadUserUpvotedLists() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUserUpvotedLists/${this.userID}`
        );
        
        if (response.data.code === 200) {
          this.userUpvotedLists = response.data.data.map(item => item.listId);
        }
      } catch (error) {
        console.error('Error loading user upvoted lists:', error);
      }
    },

    async viewListDetails(list) {
      this.selectedList = list;
      
      try {
        // Load the detailed list items
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getPublicListDetails/${list.id}`
        );
        
        if (response.data.code === 200) {
          this.selectedListItems = response.data.data;
        }
      } catch (error) {
        console.error('Error loading list details:', error);
        const toast = useToast();
        toast.error('Failed to load list details.');
      }
    },

    goBackToLists() {
      this.selectedList = null;
      this.selectedListItems = [];
    },

    goToMyProfile() {
      if (this.userID && this.username) {
        this.$router.push(`/profile/user/${this.userID}/${this.username}`);
      }
    },

    filterLists() {
      let filtered = [...this.publicLists];
      
      // Apply search filter
      if (this.searchTerm.trim()) {
        const term = this.searchTerm.toLowerCase();
        filtered = filtered.filter(list => 
          list.listName.toLowerCase().includes(term) ||
          list.listDesc?.toLowerCase().includes(term) ||
          list.username.toLowerCase().includes(term) ||
          list.displayName?.toLowerCase().includes(term)
        );
      }
      
      // Apply sorting
      filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'popular':
            return (b.upvotes || 0) - (a.upvotes || 0);
          case 'alphabetical':
            return a.listName.localeCompare(b.listName);
          case 'recent':
          default:
            return new Date(b.updatedAt || b.createdAt) - new Date(a.updatedAt || a.createdAt);
        }
      });
      
      this.filteredLists = filtered;
      this.currentPage = 1; // Reset pagination
    },

    setSortBy(sortBy) {
      this.sortBy = sortBy;
      this.filterLists();
    },

    loadMore() {
      this.currentPage++;
    },

    async toggleUpvote(list) {
      if (!this.userID) {
        const toast = useToast();
        toast.warning('Please log in to upvote lists.');
        return;
      }

      const isUpvoted = this.hasUserUpvoted(list);
      this.upvoting = true;
      
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/${isUpvoted ? 'removeUpvote' : 'upvoteList'}`,
          {
            userID: this.userID,
            listId: list.id
          }
        );
        
        if (response.data.code === 201) {
          // Update local data
          list.upvotes = response.data.data.upvotes;
          
          if (isUpvoted) {
            // Remove from upvoted lists
            const index = this.userUpvotedLists.indexOf(list.id);
            if (index > -1) {
              this.userUpvotedLists.splice(index, 1);
            }
          } else {
            // Add to upvoted lists
            this.userUpvotedLists.push(list.id);
          }
          
          const toast = useToast();
          toast.success(isUpvoted ? 'Upvote removed!' : 'List upvoted!');
        }
      } catch (error) {
        console.error('Error toggling upvote:', error);
        const toast = useToast();
        toast.error('Failed to update upvote. Please try again.');
      } finally {
        this.upvoting = false;
      }
    },

    hasUserUpvoted(list) {
      return this.userUpvotedLists.includes(list.id);
    },

    shareList(list) {
      const shareUrl = `${window.location.origin}/profile/user/${list.userId}/${list.username}/${encodeURIComponent(list.listName)}`;
      
      // Copy to clipboard
      navigator.clipboard.writeText(shareUrl).then(() => {
        const toast = useToast();
        toast.success('List link copied to clipboard!');
      }).catch((err) => {
        console.error('Failed to copy text: ', err);
        const toast = useToast();
        toast.error('Failed to copy link.');
      });
    },

    prepareNoteModal(listing, index) {
      this.currentNote = listing.note || '';
      this.currentNoteListingIndex = index;
    },

    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },
  },
};
</script>

<style scoped>
.list-card {
  transition: transform 0.2s ease-in-out;
}

.list-card:hover {
  transform: translateY(-2px);
}

.pin-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 4px;
  height: 100%;
  width: 100%;
}

.pin-cell {
  overflow: hidden;
  border-radius: 4px;
}

.pin-main {
  grid-column: 1;
  grid-row: 1 / 3;
}

.pin-side1 {
  grid-column: 2;
  grid-row: 1;
}

.pin-side2 {
  grid-column: 2;
  grid-row: 2;
}

.pin-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pin-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  color: #6c757d;
}



.text-muted-white {
  color: #999999 !important;
}

.description-text {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
  max-height: 2.8em;
}

.card-img-top-wrapper {
  height: 180px;
  overflow: hidden;
}

.card-img-top {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

/* Review card styles similar to UserProfile */
.review-card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.review-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
}

.review-card-img {
  height: 180px;
  width: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.review-card:hover .review-card-img {
  transform: scale(1.05);
}

.card-img-top-wrapper {
  overflow: hidden;
  position: relative;
}
</style>