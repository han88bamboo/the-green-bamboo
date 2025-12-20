<template>
  <NavBar />

  <!-- User Profile Header and Navigation (always visible) -->
  <div v-if="displayUserID && routeUsername" class="userprofile mt-5 mobile-mt-3">
    <div class="container text-start">
      <UserProfileHeader />
    </div>
    <br>
    <!-- User Profile Navigation -->
    <div class="container text-start">
      <UserProfileNavbar :userID="displayUserID" :username="routeUsername" />
    </div>
  </div>

  <!-- Display when data is still loading -->
  <LoadingWithFunFact v-if="dataLoaded === false" />

  <!-- Display when data fails to load -->
  <div
    class="text-danger fst-italic fw-bold fs-3 pt-5"
    v-if="dataLoaded == null"
  >
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
  <div
    v-if="dataLoaded"
    class="userprofile  mobile-mt-3"
  >
      <div class="row mobile-px-3">
        <div class="col-12 col-md-10 mx-auto px-2">
          <!-- Placeholder Content -->
          <div class="text-center mobile-spacer">
             <!-- cellar tab -->
              
                <!-- Collection Overview -->
                <div v-if="!viewingCellarCollection">
                  <!-- Create New Collection Button -->
                  <router-link
                    v-if="ownProfile"
                    :to="`/my-cellar/user/${displayUserID}/${routeUsername}`"
                    class="btn fw-bold primary-btn-less-round-blue xprimary-btn-outline-less-round my-3"
                  >
                    Manage Cellar
                  </router-link>
                
                <!-- Display all cellar collections -->
                <div v-if="Object.keys(displayUserCellarCollections).length > 0" class="row g-3">
                  <div
                    v-for="(cellarCollection, name) in displayUserCellarCollections"
                    :key="name"
                    class="col-12 col-md-6"
                  >
                    <div
                      class="pin-card h-100"
                      @click="viewCellarCollection(name)"
                      role="button"
                      tabindex="0"
                    >
                      <!-- 3-image grid -->
                      <div class="pin-grid">
                        <!-- Main (first item) -->
                        <div class="pin-cell pin-main">
                          <template v-if="cellarCollection.items && cellarCollection.items[0]">
                            <img
                              class="pin-img"
                              :src="getCellarItemPhoto(cellarCollection.items[0])"
                              :alt="`${name} preview 1`"
                            />
                          </template>
                          <div v-else class="pin-placeholder"></div>
                        </div>

                        <!-- Right-top (second item) -->
                        <div class="pin-cell pin-side1">
                          <template v-if="cellarCollection.items && cellarCollection.items[1]">
                            <img
                              class="pin-img"
                              :src="getCellarItemPhoto(cellarCollection.items[1])"
                              :alt="`${name} preview 2`"
                            />
                          </template>
                          <div v-else class="pin-placeholder"></div>
                        </div>

                        <!-- Right-bottom (third item) -->
                        <div class="pin-cell pin-side2">
                          <template v-if="cellarCollection.items && cellarCollection.items[2]">
                            <img
                              class="pin-img"
                              :src="getCellarItemPhoto(cellarCollection.items[2])"
                              :alt="`${name} preview 3`"
                            />
                          </template>
                          <div v-else class="pin-placeholder"></div>
                        </div>
                      </div>
                      <div class="pin-body">
                        <!-- Meta -->
                        <div class="pin-meta">
                          <h5 class="pin-title">{{ name }}</h5>
                          <div class="pin-count">
                            {{ getTotalCellarItemCount(cellarCollection) }}
                            {{ getTotalCellarItemCount(cellarCollection) === 1 ? 'Bottle' : 'Bottles' }}
                          </div>
                          <div v-if="cellarCollection.isDefault" class="pin-badge">
                            <small class="badge bg-success">Default</small>
                          </div>
                        </div>
                        <div class="pin-desc">
                          <div v-if="cellarCollection.description">
                            {{ cellarCollection.description }}
                          </div>
                          <div v-else class="text-muted">
                            <small>{{ cellarCollection.isPublic ? 'Public' : 'Private' }} collection</small>
                          </div>
                        </div>
                        <div class="pin-actions">
                          <b>
                            <a
                              class="me-2 my-3"
                              @click="viewCellarCollection(name)"
                              href="#"
                              style="color: #027562"
                            >View</a>
                          </b>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Empty state for no collections -->
                <div v-else-if="cellarDataLoaded" class="text-center py-4">
                  <div class="text-muted">
                    <i class="bi bi-archive" style="font-size: 3rem;"></i>
                    <h5 class="mt-3">No Cellar Collections</h5>
                    <p v-if="ownProfile">Start building your cellar by creating your first collection!</p>
                    <p v-else>This user hasn't created any public cellar collections yet.</p>
                  </div>
                </div>
                
                <!-- Loading state -->
                <div v-else class="text-center py-4">
                  <div class="spinner-border spinner-border-sm me-2"></div>
                  Loading cellar data...
                </div>
                </div>

                <!-- Collection Detail View -->
                <div v-else>
                  <!-- Back button and collection header -->
                  <div class="d-flex align-items-center justify-content-between mb-4">
                    <div class="d-flex align-items-center">
                      <button 
                        class="btn btn-outline-secondary me-3"
                        @click="backToCellarCollections()"
                      >
                        <i class="bi bi-arrow-left"></i> Back to Collections
                      </button>
                      <div>
                        <h4 class="mb-0">{{ selectedCellarCollection }}</h4>
                        <small class="text-muted">
                          {{ groupedCellarItems.length }} 
                          {{ groupedCellarItems.length === 1 ? 'variant' : 'variants' }}
                          ({{ selectedCellarCollectionItems.length }} total {{ selectedCellarCollectionItems.length === 1 ? 'item' : 'items' }})
                        </small>
                      </div>
                    </div>
                    
                    <!-- Share Button -->
                    <button 
                      v-if="selectedCellarCollectionData && selectedCellarCollectionData.isPublic"
                      class="btn btn-outline-primary"
                      @click="shareCellarCollection()"
                      title="Share this collection"
                    >
                      <i class="bi bi-reply share-icon"></i> Share
                    </button>
                  </div>

                  <!-- Items Grid -->
                  <div class="row" v-if="groupedCellarItems.length > 0">
                    <div 
                      v-for="group in groupedCellarItems" 
                      :key="group.representative.cellarItemId"
                      class="col-12 col-md-6 col-lg-4 mb-3"
                    >
                      <div class="card cellar-item-card h-100">
                        <!-- Image Area -->
                        <div class="card-img-container" style="width:100%;">
                          <img 
                            :src="getItemImageUrl(group.representative)"
                            :alt="group.representative.listingName"
                            class="card-img-top"
                          >
                          <!-- Quantity and Volume Badge -->
                          <div class="quantity-volume-badge">
                            {{ group.itemCount }} {{ getContainerType(group.representative.drinkFormat, group.itemCount).toLowerCase() }}{{ getVolumeText(group.representative) }}
                          </div>
                        </div>

                        <!-- Info Band -->
                        <div class="card-body text-center">
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

                            <!-- Status Info -->
                            <div class="status-info mt-2">
                              <!-- Status Breakdown -->
                              <div class="status-breakdown">
                                <span 
                                  v-for="(count, status) in getGroupStatusBreakdown(group.items)"
                                  :key="status"
                                  class="status-badge badge me-1 mb-2"
                                  :class="getStatusBadgeClass(status)"
                                  :title="`${count} bottle${count !== 1 ? 's' : ''} ${status.toLowerCase()}`"
                                >
                                  {{ count }}x {{ status }}
                                </span>
                              </div>
                              
                              <!-- Drink dates -->
                              <div class="drink-dates mt-1" v-if="group.representative.drinkByDate || group.representative.drinkOnwardsDate">
                                <small class="text-muted">
                                  <span v-if="group.representative.drinkOnwardsDate">
                                    Drink from: {{ formatDate(group.representative.drinkOnwardsDate) }}
                                  </span>
                                  <span v-if="group.representative.drinkByDate">
                                    <br>Drink by: {{ formatDate(group.representative.drinkByDate) }}
                                  </span>
                                </small>
                              </div>
                              
                              <!-- Notes -->
                              <div 
                                class="card-notes text-muted small mt-2 border rounded p-2 position-relative" 
                                v-if="group.representative.noteToSelf"
                                :title="group.representative.noteToSelf"
                              >
                                <!-- Note icon -->
                                <svg class="position-absolute" style="top: 2px; right: 3px; width: 12px; height: 12px; opacity: 0.8;" viewBox="0 0 16 16" fill="#dc3545">
                                  <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2z"/>
                                </svg>
                                {{ group.representative.noteToSelf }}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Empty state for collection -->
                  <div v-else class="text-center py-4">
                    <div class="text-muted">
                      <i class="bi bi-archive" style="font-size: 3rem;"></i>
                      <h5 class="mt-3">No Items in Collection</h5>
                      <p>This collection is currently empty.</p>
                    </div>
                  </div>
                </div>
          </div>
        </div>
      </div>

  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';
import UserProfileHeader from '@/components/UserProfileHeader.vue';
import UserProfileNavbar from '@/components/UserProfileNavbar.vue';
import { useToast } from "vue-toastification";

export default {
  name: "UserStories",
  components: {
    NavBar,
    LoadingWithFunFact,
    UserProfileHeader,
    UserProfileNavbar,
  },
  data() {
    return {
      dataLoaded: false,
      currentURL: "",

      // default images
      defaultProfilePhoto:
        "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
      defaultDrinkImage:
        "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",

      // User data
      displayUserID: null,
      routeUsername: null,
      displayUser: {},
      userID: null,
      userType: null,
      username: null,
      ownProfile: false,

      // Cellar Data
      displayUserCellarCollections: {},
      cellarItems: [],
      cellarDataLoaded: false,
      
      // Cellar Collection Detail View
      selectedCellarCollection: null,
      selectedCellarCollectionData: null,
      selectedCellarCollectionItems: [],
      viewingCellarCollection: false,
      sharedCollectionId: null, // For handling shared collection URLs
    };
  },
  computed: {
    // Group cellar items by variantGroupID for display
    groupedCellarItems() {
      if (!this.selectedCellarCollectionItems || this.selectedCellarCollectionItems.length === 0) {
        return [];
      }
      return this.groupCellarItems(this.selectedCellarCollectionItems);
    }
  },

  async mounted() {
    // Get route parameters
    this.displayUserID = parseInt(this.$route.params.userID);
    this.routeUsername = this.$route.params.username;

    // get local storage (to determine if this is own profile)
    const accID = localStorage.getItem("88B_accID");
    if (accID !== null) {
      this.userID = accID;
    }

    const accType = localStorage.getItem("88B_accType");
    if (accType !== null) {
      this.userType = accType;
    }

    const accUsername = localStorage.getItem("88B_accUsername");
    if (accUsername !== null) {
      this.username = accUsername;
    }

    if (this.displayUserID && this.userID && parseInt(this.displayUserID) === parseInt(this.userID)) {
      this.ownProfile = true;
    }

    // Handle shared collection query param (if any)
    try {
      const collectionId = this.$route.query.collection;
      if (collectionId) {
        this.sharedCollectionId = collectionId;
      }
    } catch (e) {
      console.error(e);
    }

    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        this.dataLoaded = false;
        
        // Load user profile
        await this.getDisplayUserProfile();

        // Load user's cellar data (used by this page)
        await this.getCellarData();
        
        // Mark as loaded once both profile and cellar data are available
        this.dataLoaded = true;
      } catch (error) {
        console.error("Error loading data:", error);
        this.dataLoaded = null;
      }
    },  

        // Cellar Data
    async getCellarData() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getCellarData/user/${this.displayUserID}`
        );
        
        // Transform data for profile view
        if (response.data && response.data.data) {
          const collections = response.data.data.collections || [];
          const items = response.data.data.items || [];
          
          // Store all items for reference
          this.cellarItems = items;
          
          // Transform collections for card display
          this.displayUserCellarCollections = this.formatCellarCollectionsForProfile(collections, items);
        } else {
          // No data returned
          this.displayUserCellarCollections = {};
          this.cellarItems = [];
        }
        
        this.cellarDataLoaded = true;
        
        // Handle shared collection after data is loaded
        this.handleSharedCollection();
      } catch (error) {
        console.error("Error fetching cellar data:", error);
        if (error.response && error.response.status === 404) {
          // Handle empty cellar as success - user has no cellar data
          this.displayUserCellarCollections = {};
          this.cellarItems = [];
          this.cellarDataLoaded = true;
          // Handle shared collection even if there's no cellar data
          this.handleSharedCollection();
        } else {
          // For other errors, still mark as loaded but with empty data
          // This prevents infinite loading states
          this.displayUserCellarCollections = {};
          this.cellarItems = [];
          this.cellarDataLoaded = true;
          // Handle shared collection even on error
          this.handleSharedCollection();
          console.warn("Cellar data could not be loaded, using empty state");
        }
      }
    },

        formatCellarCollectionsForProfile(collections, items) {
      const formatted = {};
      
      collections.forEach(collection => {
        // Only show public collections if viewing another user's profile
        if (!this.ownProfile && !collection.isPublic) {
          return;
        }
        
        const collectionItems = items.filter(item => item.collectionId === collection.id);
        
        formatted[collection.collectionName] = {
          id: collection.id,
          isDefault: collection.isDefault,
          isPublic: collection.isPublic,
          items: collectionItems.slice(0, 3), // First 3 for preview
          totalCount: collectionItems.length,
          description: collection.description || null
        };
      });
      
      return formatted;
    },

    // Helper methods for cellar
    getCellarItemPhoto(cellarItem) {
      return cellarItem.drinkPhoto || this.defaultDrinkImage;
    },
    
    getTotalCellarItemCount(cellarCollection) {
      return cellarCollection.totalCount || 0;
    },
    
    viewCellarCollection(collectionName) {
      // Show detailed view of collection items on the same page
      const collection = this.displayUserCellarCollections[collectionName];
      if (collection) {
        this.selectedCellarCollection = collectionName;
        this.selectedCellarCollectionItems = this.cellarItems.filter(item => item.collectionId === collection.id);
        this.selectedCellarCollectionData = collection;
        this.viewingCellarCollection = true;
      }
    },

    async getDisplayUserProfile() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUser/${this.displayUserID}`
        );
        this.displayUser = response.data;
      } catch (error) {
        console.error("Error loading user profile:", error);
        throw error;
      }
    },

    // Handle shared collection if ?collection=<id> was provided in URL
    handleSharedCollection() {
      if (!this.sharedCollectionId) return;

      for (const [collectionName, collectionData] of Object.entries(this.displayUserCellarCollections)) {
        if (collectionData.id === parseInt(this.sharedCollectionId)) {
          this.viewCellarCollection(collectionName);
          this.sharedCollectionId = null;
          return;
        }
      }

      console.warn(`Shared collection with ID ${this.sharedCollectionId} not found`);
      this.sharedCollectionId = null;
    },

    backToCellarCollections() {
      this.viewingCellarCollection = false;
      this.selectedCellarCollection = null;
      this.selectedCellarCollectionItems = [];
      this.selectedCellarCollectionData = null;
    },

    // Group cellar items by variantGroupID for display
    groupCellarItems(items) {
      const groups = {};
      
      items.forEach(item => {
        const groupKey = item.variantGroupID || `standalone_${item.cellarItemId}`;
        
        if (!groups[groupKey]) {
          groups[groupKey] = {
            representative: item,
            items: [],
            itemCount: 0,
            variantGroupID: item.variantGroupID,
            listingId: item.listingId,
            variant: item.variant,
            drinkFormat: item.drinkFormat,
            volumeNumber: item.volumeNumber,
            volumeUnit: item.volumeUnit,
            listingName: item.listingName
          };
        }
        
        groups[groupKey].items.push(item);
        groups[groupKey].itemCount = groups[groupKey].items.length;
      });
      
      return Object.values(groups);
    },

    // Helper methods for cellar item display
    getItemImageUrl(item) {
      return item.drinkPhoto || this.defaultDrinkImage;
    },

    getContainerType(drinkFormat, count) {
      if (!drinkFormat) return count === 1 ? 'Item' : 'Items';
      
      const format = drinkFormat.toLowerCase();
      if (format.includes('bottle')) return count === 1 ? 'Bottle' : 'Bottles';
      if (format.includes('can')) return count === 1 ? 'Can' : 'Cans';
      if (format.includes('sample')) return count === 1 ? 'Sample' : 'Samples';
      return drinkFormat;
    },

    getVolumeText(item) {
      if (!item.volumeNumber || !item.volumeUnit) return '';
      return `/${item.volumeNumber}${item.volumeUnit}`;
    },

    getStatusBadgeClass(status) {
      switch (status) {
        case 'In Possession':
          return 'bg-success';
        case 'Consumed':
          return 'bg-secondary';
        case 'On Its Way':
          return 'bg-info';
        case 'Wishlisted':
          return 'bg-warning';
        case 'Held Elsewhere':
          return 'bg-light text-dark';
        case 'Unopened':
          return 'bg-success';
        case 'Opened':
          return 'bg-warning';
        case 'Empty':
          return 'bg-secondary';
        default:
          return 'bg-secondary';
      }
    },

    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },

    // Get status breakdown for a group of cellar items
    getGroupStatusBreakdown(items) {
      const breakdown = {};
      items.forEach(item => {
        const status = item.consumption || 'Unopened';
        breakdown[status] = (breakdown[status] || 0) + 1;
      });
      return breakdown;
    },

    // Share collection by copying a link to clipboard
    shareCellarCollection() {
      if (!this.selectedCellarCollectionData) return;
      const collectionUrl = `${window.location.origin}/profile/user/${this.displayUserID}/${this.displayUser.username}?collection=${this.selectedCellarCollectionData.id}`;
      this.copyToClipboard(collectionUrl);
    },

    copyToClipboard(text) {
      navigator.clipboard
        .writeText(text)
        .then(() => {
          const toast = useToast();
          toast.success("Link copied to clipboard!");
        })
        .catch((err) => {
          console.warn('Could not copy text: ', err);
        });
    },
  }
};
</script>

<style scoped>
/* Add any custom styles here */
/* List Card Styles */
.pin-card {
  border-radius: 16px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 1px 6px rgba(0,0,0,0.06);
}

.pin-body {
  padding: 0px 12px 12px; /* apply consistent left padding */
}

.pin-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 1fr 1fr;
  grid-template-areas:
    "main side1"
    "main side2";
  gap: 8px;
  padding: 8px;
  height: 180px; 
   /* tweak as you like */
}

.pin-cell { width: 100%; height: 100%; border-radius: 12px; overflow: hidden; }
.pin-main  { grid-area: main; }
.pin-side1 { grid-area: side1; }
.pin-side2 { grid-area: side2; }

.pin-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.pin-placeholder {
  width: 100%;
  height: 100%;
  background: #e9ecef;   /* greyed-out box */
}

.pin-meta {
  padding: 8px 0 12px;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.pin-title {
  margin: 0;
  font-weight: 700;
  cursor: pointer;
}

.pin-count {
  font-size: 0.9rem;
  color: #6c757d;
}

.pin-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); }

.pin-desc {
  padding: 0;
  margin: 0;
}

.pin-actions {
  padding: 0;   /* top/bottom handled separately, left/right small (or 0) */
  padding-top: 0.5rem; /* ≈ py-2 top */
  padding-bottom: 0.5rem; /* ≈ py-2 bottom */
  margin: 0;
}
</style>
