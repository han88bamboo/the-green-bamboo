<!-- EntityMerge.vue -->
<template>
  <div class="entity-merge-container mt-4">
    <!-- Entity Type Selection -->
    <div class="mb-4">
      <h2 class="h4 fw-bold mb-3">Merge Duplicate Entities</h2>
      
      <div class="mb-3">
        <button
          class="btn btn-sm mx-1 mb-1 fw-bold"
          :class="{
            'primary-btn-green': activeEntityType === 'producers',
            'primary-btn-green-thin-outline': activeEntityType !== 'producers'
          }"
          @click="activeEntityType = 'producers'"
        >
          Producers
        </button>
        <button
          class="btn btn-sm mx-1 mb-1 fw-bold"
          :class="{
            'primary-btn-green': activeEntityType === 'listings',
            'primary-btn-green-thin-outline': activeEntityType !== 'listings'
          }"
          @click="activeEntityType = 'listings'"
        >
          Listings
        </button>
        <button
          class="btn btn-sm mx-1 mb-1 fw-bold"
          :class="{
            'primary-btn-green': activeEntityType === 'venues',
            'primary-btn-green-thin-outline': activeEntityType !== 'venues'
          }"
          @click="activeEntityType = 'venues'"
        >
          Venues
        </button>
      </div>
    </div>

    <!-- Search Section -->
    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">Search for Duplicates</h5>
        <div class="row">
          <div class="col-md-8">
            <input
              type="text"
              class="form-control"
              v-model="searchQuery"
              @keyup.enter="performSearch"
              :placeholder="`Search ${activeEntityType} by name or paste URL...`"
            />
          </div>
          <div class="col-md-4">
            <button 
              class="btn btn-primary w-100" 
              @click="performSearch"
              :disabled="!searchQuery || searching"
            >
              <span v-if="searching" class="spinner-border spinner-border-sm me-2"></span>
              Search
            </button>
          </div>
        </div>

        <!-- No Results Message -->
        <div v-if="searchPerformed && searchResults.length === 0" class="alert alert-info mt-3 mb-0">
          No results found for "{{ searchQuery }}". Try a different search term.
        </div>

        <!-- Search Results -->
        <div v-if="searchResults.length > 0" class="mt-3">
          <h6>Search Results:</h6>
          <div class="list-group" style="max-height: 300px; overflow-y: auto;">
            <button
              v-for="result in searchResults"
              :key="result.id"
              class="list-group-item list-group-item-action"
              :class="{ 
                'active': selectedEntities.some(e => e.id === result.id),
                'list-group-item-success': masterEntity?.id === result.id
              }"
              @click="toggleEntitySelection(result)"
            >
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <strong>{{ result.name }}</strong>
                  <small class="d-block text-muted">
                    ID: {{ result.id }}
                    <span v-if="result.producer"> | Producer: {{ result.producer }}</span>
                    <span v-if="result.country"> | {{ result.country }}</span>
                    <span v-if="result.address"> | {{ result.address }}</span>
                    <span v-if="result.type"> | {{ result.type }}</span>
                  </small>
                </div>
                <span v-if="masterEntity?.id === result.id" class="badge bg-success">Master</span>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Selected Entities for Merge -->
    <div v-if="selectedEntities.length > 0" class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">Selected for Merge ({{ selectedEntities.length }} items)</h5>
        
        <!-- Master Selection -->
        <div class="mb-3">
          <label class="form-label fw-bold">Select Master Record:</label>
          <select 
            class="form-select" 
            v-model="masterEntityId"
            @change="updateMasterEntity"
          >
            <option value="" disabled selected>Choose which record to keep as master</option>
            <option 
              v-for="entity in selectedEntities" 
              :key="entity.id" 
              :value="entity.id"
            >
              {{ entity.name }} (ID: {{ entity.id }})
            </option>
          </select>
        </div>

        <!-- Selected List -->
        <div class="selected-entities-list">
          <div 
            v-for="entity in selectedEntities" 
            :key="entity.id"
            class="d-flex justify-content-between align-items-center p-2 border rounded mb-2"
            :class="{ 'bg-success bg-opacity-10': masterEntity?.id === entity.id }"
          >
            <div>
              <strong>{{ entity.name }}</strong>
              <small class="d-block text-muted">ID: {{ entity.id }}</small>
            </div>
            <div>
              <span v-if="masterEntity?.id === entity.id" class="badge bg-success me-2">Master</span>
              <button 
                class="btn btn-sm btn-outline-danger"
                @click="removeFromSelection(entity)"
              >
                Remove
              </button>
            </div>
          </div>
        </div>

        <!-- Preview Button -->
        <button 
          class="btn btn-warning mt-3"
          @click="showPreview"
          :disabled="!masterEntity || selectedEntities.length < 2 || loadingPreview"
        >
          <span v-if="loadingPreview" class="spinner-border spinner-border-sm me-2"></span>
          Preview Merge
        </button>
      </div>
    </div>

    <!-- Merge Preview Modal -->
    <div 
      class="modal fade" 
      id="mergePreviewModal" 
      tabindex="-1" 
      ref="previewModal"
    >
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Merge Preview</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div v-if="previewData">
              <div class="mb-4 p-3 bg-light rounded">
                <label class="form-label fw-bold">Change Master Record:</label>
                <select 
                  class="form-select" 
                  v-model="masterEntityId"
                  @change="handleMasterChangeInPreview"
                >
                  <option 
                    v-for="entity in selectedEntities" 
                    :key="entity.id" 
                    :value="entity.id"
                  >
                    {{ entity.name }} (ID: {{ entity.id }})
                  </option>
                </select>
              </div>
              <!-- Field Comparison Table -->
              <h6 class="fw-bold mb-3">Field Comparison:</h6>
              <div class="table-responsive">
                <table class="table table-bordered">
                  <thead>
                    <tr>
                      <th>Field</th>
                      <th 
                        v-for="entity in previewData[activeEntityType]" 
                        :key="entity.id"
                        :class="{ 'table-success': entity.id === masterEntity?.id }"
                      >
                        {{ entity.id === masterEntity?.id ? '✓ Master' : 'Duplicate' }}
                        <br>
                        <small>ID: {{ entity.id }}</small>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="field in getComparisonFields()" :key="field.key">
                      <td class="fw-bold">{{ field.label }}</td>
                      <td 
                        v-for="entity in previewData[activeEntityType]" 
                        :key="entity.id"
                        :class="{ 'table-success': entity.id === masterEntity?.id }"
                      >
                        {{ entity[field.key] || '-' }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Related Data Impact -->
              <h6 class="fw-bold mb-3 mt-4">Data to be Consolidated:</h6>
              <div class="alert alert-info">
                <div class="row">
                  <div class="col-md-6">
                    <ul class="mb-0">
                      <li v-for="(value, key) in previewData.totalAffected" :key="key">
                        <strong>{{ formatFieldName(key) }}:</strong> {{ value }} records
                      </li>
                    </ul>
                  </div>
                  <div class="col-md-6">
                    <p class="mb-0">
                      <strong>Note:</strong> All related data from duplicate records will be 
                      transferred to the master record before deletion.
                    </p>
                  </div>
                </div>
              </div>

              <!-- Individual Record Counts -->
              <h6 class="fw-bold mb-3">Related Data by Record:</h6>
              <div class="table-responsive">
                <table class="table table-sm">
                  <thead>
                    <tr>
                      <th>Record ID</th>
                      <th v-for="(value, key) in previewData.totalAffected" :key="key">
                        {{ formatFieldName(key) }}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr 
                      v-for="entityId in Object.keys(previewData.relatedCounts)" 
                      :key="entityId"
                      :class="{ 'table-success': parseInt(entityId) === masterEntity?.id }"
                    >
                      <td>
                        {{ entityId }}
                        <span v-if="parseInt(entityId) === masterEntity?.id" class="badge bg-success ms-1">Master</span>
                      </td>
                      <td v-for="(value, key) in previewData.totalAffected" :key="key">
                        {{ previewData.relatedCounts[entityId][key] || 0 }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button 
              type="button" 
              class="btn btn-danger"
              @click="executeMerge"
              :disabled="merging"
            >
              <span v-if="merging" class="spinner-border spinner-border-sm me-2"></span>
              Confirm Merge
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="successMessage" class="alert alert-success alert-dismissible fade show">
      {{ successMessage }}
      <button type="button" class="btn-close" @click="successMessage = ''"></button>
    </div>
    <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show">
      {{ errorMessage }}
      <button type="button" class="btn-close" @click="errorMessage = ''"></button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Modal } from 'bootstrap';

export default {
  name: 'EntityMerge',
  data() {
    return {
      API_URL: process.env.VUE_APP_API_URL,
      
      // Entity selection
      activeEntityType: 'producers',
      searchQuery: '',
      searchResults: [],
      searching: false,
      searchPerformed: false,
      
      // Merge management
      selectedEntities: [],
      masterEntityId: '',
      masterEntity: null,
      
      // Preview
      previewData: null,
      loadingPreview: false,
      previewModal: null,
      
      // Processing
      merging: false,
      successMessage: '',
      errorMessage: ''
    };
  },
  mounted() {
    this.previewModal = new Modal(this.$refs.previewModal);
  },
  methods: {
    async performSearch() {
      this.searching = true;
      this.errorMessage = '';
      
      try {
        // Check if searchQuery is a URL
        const urlPattern = /^https?:\/\//;
        
        if (urlPattern.test(this.searchQuery)) {
          // Parse URL to extract ID
          const url = this.searchQuery;
          let entityId = null;
          
          // Producer URL pattern: /profile/user/{id}/{username}
          const producerPattern = /\/profile\/producer\/(\d+)\//;
          
          // Listing URL pattern: /listing/view/{id}/{name}
          const listingPattern = /\/listing\/view\/(\d+)\//;
          
          // Venue URL pattern: /profile/venue/{id}/{name}
          const venuePattern = /\/profile\/venue\/(\d+)\//;
          
          if (producerPattern.test(url) && this.activeEntityType === 'producers') {
            entityId = url.match(producerPattern)[1];
          } else if (listingPattern.test(url) && this.activeEntityType === 'listings') {
            entityId = url.match(listingPattern)[1];
          } else if (venuePattern.test(url) && this.activeEntityType === 'venues') {
            entityId = url.match(venuePattern)[1];
          }
          
          if (entityId) {
            // Fetch specific entity by ID
            const response = await axios.get(
              `${this.API_URL}/adminFunctions/getEntityById/${this.activeEntityType}/${entityId}`
            );
            this.searchResults = [response.data.data];
          } else {
            this.errorMessage = 'URL does not match the selected entity type';
            this.searchResults = [];
          }
        } else {
          // Regular text search
          const response = await axios.get(
            `${this.API_URL}/adminFunctions/searchDuplicates/${this.activeEntityType}`,
            { params: { q: this.searchQuery } }
          );
          this.searchResults = response.data.data;
        }
      } catch (error) {
        console.error('Search error:', error);
        this.errorMessage = 'Failed to search. Please try again.';
      } finally {
        this.searching = false;
      }
    },
    
    toggleEntitySelection(entity) {
      const index = this.selectedEntities.findIndex(e => e.id === entity.id);
      if (index > -1) {
        this.removeFromSelection(entity);
      } else {
        this.selectedEntities.push(entity);
      }
    },
    
    removeFromSelection(entity) {
      this.selectedEntities = this.selectedEntities.filter(e => e.id !== entity.id);
      if (this.masterEntityId === entity.id) {
        this.masterEntityId = '';
        this.masterEntity = null;
      }
    },
    
    updateMasterEntity() {
      this.masterEntity = this.selectedEntities.find(e => e.id === parseInt(this.masterEntityId));
    },
    
    async showPreview() {
      if (!this.masterEntity || this.selectedEntities.length < 2) {
        this.errorMessage = 'Please select a master and at least one duplicate.';
        return;
      }
      
      this.loadingPreview = true;
      this.errorMessage = '';
      
      const duplicateIds = this.selectedEntities
        .filter(e => e.id !== this.masterEntity.id)
        .map(e => e.id);
      
      try {
        let endpoint = '';
        if (this.activeEntityType === 'producers') {
          endpoint = 'getProducerMergePreview';
        } else if (this.activeEntityType === 'listings') {
          endpoint = 'getListingMergePreview';
        } else if (this.activeEntityType === 'venues') {
          endpoint = 'getVenueMergePreview';
        }
        
        const response = await axios.post(`${this.API_URL}/adminFunctions/${endpoint}`, {
          masterId: this.masterEntity.id,
          duplicateIds: duplicateIds
        });
        
        this.previewData = response.data.data;
        this.previewModal.show();
      } catch (error) {
        console.error('Preview error:', error);
        this.errorMessage = 'Failed to load preview. Please try again.';
      } finally {
        this.loadingPreview = false;
      }
    },

    async handleMasterChangeInPreview() {
      this.masterEntity = this.selectedEntities.find(e => e.id === parseInt(this.masterEntityId));
      // Reload preview with new master
      await this.showPreview();
    },
    
    async executeMerge() {
      this.merging = true;
      this.errorMessage = '';
      
      const duplicateIds = this.selectedEntities
        .filter(e => e.id !== this.masterEntity.id)
        .map(e => e.id);
      
      try {
        let endpoint = '';
        if (this.activeEntityType === 'producers') {
          endpoint = 'mergeProducers';
        } else if (this.activeEntityType === 'listings') {
          endpoint = 'mergeListings';
        } else if (this.activeEntityType === 'venues') {
          endpoint = 'mergeVenues';
        }
        
        const response = await axios.post(`${this.API_URL}/adminFunctions/${endpoint}`, {
          masterId: this.masterEntity.id,
          duplicateIds: duplicateIds
        });
        
        this.successMessage = response.data.message;
        this.previewModal.hide();
        
        // Reset selection
        this.selectedEntities = [];
        this.masterEntity = null;
        this.masterEntityId = '';
        this.searchResults = [];
        this.searchQuery = '';
        this.previewData = null;
        this.searchPerformed = false;
        
      } catch (error) {
        console.error('Merge error:', error);
        this.errorMessage = error.response?.data?.message || 'Failed to complete merge. Please try again.';
      } finally {
        this.merging = false;
      }
    },
    
    getComparisonFields() {
      if (this.activeEntityType === 'producers') {
        return [
          { key: 'producerName', label: 'Name' },
          { key: 'originCountry', label: 'Country' },
          { key: 'yearFounded', label: 'Year Founded' },
          { key: 'activeStatus', label: 'Status' },
          { key: 'owner', label: 'Owner' },
          { key: 'website', label: 'Website' },
          { key: 'claimStatus', label: 'Claimed' }
        ];
      } else if (this.activeEntityType === 'listings') {
        return [
          { key: 'listingName', label: 'Name' },
          { key: 'producerName', label: 'Producer' },
          { key: 'drinkType', label: 'Type' },
          { key: 'typeCategory', label: 'Category' },
          { key: 'abv', label: 'ABV' },
          { key: 'originCountry', label: 'Country' }
        ];
      } else if (this.activeEntityType === 'venues') {
        return [
          { key: 'venueName', label: 'Name' },
          { key: 'address', label: 'Address' },
          { key: 'venueType', label: 'Type' },
          { key: 'originLocation', label: 'Location' },
          { key: 'yearOpened', label: 'Year Opened' },
          { key: 'website', label: 'Website' },
          { key: 'claimStatus', label: 'Claimed' }
        ];
      }
      return [];
    },
    
    formatFieldName(key) {
      const names = {
        listings: 'Listings',
        bottlerListings: 'Bottler Listings',
        reviews: 'Reviews',
        menuItems: 'Menu Items',
        userLists: 'User Lists',
        cellarItems: 'Cellar Items',
        comments: 'Comments',
        likes: 'Likes',
        qa: 'Q&A',
        updates: 'Updates',
        followers: 'Followers',
        menuSections: 'Menu Sections',
        events: 'Events'
      };
      return names[key] || key;
    }
  },
  watch: {
    activeEntityType() {
      // Clear selections when switching entity type
      this.searchQuery = '';
      this.searchResults = [];
      this.selectedEntities = [];
      this.masterEntity = null;
      this.masterEntityId = '';
      this.previewData = null;
      this.searchPerformed = false;
    }
  }
};
</script>

<style scoped>
.entity-merge-container {
  max-width: 100%;
}

.selected-entities-list {
  max-height: 300px;
  overflow-y: auto;
}

.table-responsive {
  max-height: 400px;
  overflow-y: auto;
}
</style>