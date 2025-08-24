<template>
  <teleport to="body">
    <div class="modal fade" id="addMenuItemModal" ref="modal" tabindex="-1" aria-labelledby="addMenuItemModal" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-xl">
        <div class="modal-content">

          <!-- Modal Header -->
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="addMenuItemModalLabel">Add Menu Items to {{ targetSection.sectionName }}</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body modal-body-scrollable">

            <!-- Item Add Form -->
            <div class="border rounded p-3 mb-4" style="background-color: #fafafa;">
              <h5 class="fw-bold text-primary mb-3">Add New Item</h5>

              <!-- [input] producer search -->
              <div class="form-group mb-3">
                <p class="text-start mb-1">Producer (Distillery, Brewery, Winery, etc.) (Optional)<span
                    class="text-muted" style="font-size: 14px;"> Select a producer to filter drink search</span></p>
                <input type="text" class="form-control" v-model="newItem.producerSearchQuery"
                  @input="debouncedSearchProducers" placeholder="Search for a producer to filter drinks" />
                <ul class="list-group"
                  v-if="newItem.producerSearchResults && newItem.producerSearchResults.length > 0 && newItem.producerSearchQuery">
                  <li v-for="producer in newItem.producerSearchResults" :key="producer.id"
                    class="list-group-item list-group-item-action" @click="selectProducer(producer)">
                    {{ producer.producerName }}
                    <small class="text-muted">({{ producer.originCountry }})</small>
                  </li>
                </ul>
                <div v-if="newItem.selectedProducer && newItem.selectedProducer.id"
                  class="mt-2 p-2 bg-light border rounded">
                  <small class="text-success fw-bold">
                    ✓ Producer Selected: {{ newItem.selectedProducer.producerName }}
                    <button type="button" class="btn btn-sm btn-outline-danger ms-2" @click="clearProducerSelection">
                      Clear
                    </button>
                  </small>
                </div>
              </div>

              <!-- [input] bottle name -->
              <div class="form-group mb-3">
                <p class="text-start mb-1">Drink Name<span class="text-danger">*</span>
                  <span class="text-muted" style="font-size: 14px;">Just begin typing, then select from the drop-down
                    suggestions.</span>
                  <span v-if="newItem.selectedProducer && newItem.selectedProducer.id" class="text-info fw-bold"
                    style="font-size: 14px;">
                    - Filtered by {{ newItem.selectedProducer.producerName }}
                  </span>
                </p>
                <input type="text" class="form-control" v-model="newItem.searchQuery" @input="debouncedSearchListings"
                  :placeholder="newItem.selectedProducer && newItem.selectedProducer.id ?
                    'Search drinks from ' + newItem.selectedProducer.producerName :
                    'Enter a Drink to Add to Menu'" />
                <ul class="list-group"
                  v-if="newItem.searchResults && newItem.searchResults.length > 0 && newItem.searchQuery">
                  <li v-for="listing in newItem.searchResults" :key="listing.id"
                    class="list-group-item list-group-item-action" @click="selectListing(listing)">
                    {{ listing.listingName }}
                    <small class="text-muted">
                      (Producer: {{ listing.producerName }} |
                      Type: {{ listing.drinkType }} |
                      ABV: {{ listing.abv ? listing.abv + '%' : 'N/A' }} |
                      Country: {{ listing.originCountry }})
                    </small>
                  </li>
                </ul>
              </div>

              <!-- [input] input vintage for wine drink type -->
              <div class="form-group mb-3"
                v-if="Array.isArray(VARIANT_DRNK_TYP) && VARIANT_DRNK_TYP.includes(newItem.newMenuItemTarget.drinkType)">
                <p class="text-start mb-1"> Vintage (Optional) </p>
                <input type="number" class="form-control" v-model="newItem.newMenuItemVintage">
              </div>

              <!-- [input] menu item price -->
              <div class="form-group mb-3">
                <p class="text-start mb-1"> Menu Item Price (Note: If there is no price, leave it as 0)</p>
                <input type="number" class="form-control" v-model="newItem.newMenuItemPrice" min="0" step="0.01">
              </div>

              <!-- [input] menu serving type -->
              <div class="form-group mb-3">
                <p class="text-start mb-1"> Menu Item Serving Type </p>
                <select class="form-select" v-model="newItem.newMenuItemServingType">
                  <option v-for="servingType in servingTypes" :key="servingType.id" :value="servingType.id">{{
                    servingType.servingType }}</option>
                </select>
              </div>

              <div class="text-end">
                <button type="button" class="btn btn-primary" @click="addItemToList" :disabled="!isNewItemValid">
                  Add to Menu
                </button>
              </div>
            </div>

            <!-- Added Menu Items Table -->
            <div v-if="addedMenuItems.length > 0">
              <h5 class="fw-bold text-primary mb-3">Staged Items</h5>
              <div class="table-responsive">
                <table class="table table-striped table-hover">
                  <thead>
                    <tr>
                      <th scope="col">Drink Name</th>
                      <th scope="col">Producer</th>
                      <th scope="col">Price</th>
                      <th scope="col">Serving Type</th>
                      <th scope="col">Vintage</th>
                      <th scope="col"></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in addedMenuItems" :key="index">
                      <td>{{ item.newMenuItemTarget.listingName }}</td>
                      <td>{{ item.newMenuItemTarget.producerName }}</td>
                      <td>$ {{ item.newMenuItemPrice }}</td>
                      <td>{{servingTypes.find(st => st.id === item.newMenuItemServingType)?.servingType || '-'}}</td>
                      <td>{{ item.newMenuItemVintage || 'N/A' }}</td>
                      <td>
                        <button type="button" class="btn btn-outline-danger btn-sm" @click="removeItemFromList(index)">
                          Remove
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal"
              @click="clearAddedItems">Cancel</button>
            <button type="button" class="btn secondary-btn rounded reverse-clickable-text" data-bs-dismiss="modal"
              @click="submitAddedItems" :disabled="addedMenuItems.length === 0">
              Add {{ addedMenuItems.length }} Item(s)
            </button>
          </div>

        </div>
      </div>
    </div>
  </teleport>
</template>

<script>
import axios from 'axios';
import { debounce } from 'lodash';
import { Modal } from 'bootstrap';
// load in control 
import { VARIANT_DRNK_TYP } from '@/composables/useConstants';

export default {
  name: 'VenueMenuItems',
  props: {
    targetSection: {
      type: Object,
      required: true,
    }
  },
  emits: ['items-selected', 'hidden'],
  data() {
    return {
      modalInstance: null,
      newItem: this.getInitialNewItemState(),
      addedMenuItems: [],
      servingTypes: [],
      VARIANT_DRNK_TYP,
    };
  },
  computed: {
    isNewItemValid() {
      return this.newItem.newMenuItemID && this.newItem.newMenuItemPrice >= 0 && this.newItem.newMenuItemServingType;
    }
  },
  watch: {
    targetSection(newVal, oldVal) {
      if (newVal && !oldVal) {
        this.showModal();
      } else if (!newVal && oldVal) {
        this.hideModal();
      }
    }
  },
  mounted() {
    this.modalInstance = new Modal(this.$refs.modal);
    this.$refs.modal.addEventListener('hidden.bs.modal', () => {
      this.$emit('hidden');
    });
    if (this.targetSection) {
      this.showModal();
    }
  },
  beforeUnmount() {
    if (this.modalInstance) {
      this.modalInstance.dispose();
    }
  },
  methods: {
    showModal() {
      if (this.modalInstance) {
        this.modalInstance.show();
      }
    },
    hideModal() {
      if (this.modalInstance) {
        this.modalInstance.hide();
      }
    },
    getInitialNewItemState() {
      return {
        producerSearchQuery: '',
        producerSearchResults: [],
        selectedProducer: {},
        searchQuery: '',
        searchResults: [],
        newMenuItemID: '',
        newMenuItemTarget: {},
        newMenuItemVintage: null,
        newMenuItemPrice: 0,
        newMenuItemServingType: null,
      };
    },
    async fetchServingTypes() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/getData/getServingTypes`);
        this.servingTypes = response.data;
        if (this.servingTypes.length > 0) {
          this.newItem.newMenuItemServingType = this.servingTypes[0].id;
        }
      } catch (error) {
        console.error('Error fetching serving types:', error);
      }
    },
    async searchProducers() {
      if (!this.newItem.producerSearchQuery || this.newItem.producerSearchQuery.trim().length < 2) {
        this.newItem.producerSearchResults = [];
        return;
      }
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducerNamesDynamicSearch/${this.newItem.producerSearchQuery}`);
        if (response.status === 200) {
          this.newItem.producerSearchResults = response.data.slice(0, 10);
        }
      } catch (error) {
        console.error('Error searching producers:', error);
        this.newItem.producerSearchResults = [];
      }
    },
    async searchListings() {
      if (!this.newItem.searchQuery || this.newItem.searchQuery.trim().length < 2) {
        this.newItem.searchResults = [];
        return;
      }
      try {
        let response;
        if (this.newItem.selectedProducer && this.newItem.selectedProducer.id) {
          response = await axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingNamesByProducer/${this.newItem.searchQuery}/${this.newItem.selectedProducer.id}`);
        } else {
          response = await axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingNamesDynamicSearch/${this.newItem.searchQuery}`);
        }
        if (response.status === 200) {
          this.newItem.searchResults = response.data.slice(0, 10);
        }
      } catch (error) {
        console.error('Error searching listings:', error);
        this.newItem.searchResults = [];
      }
    },
    selectProducer(producer) {
      this.newItem.selectedProducer = producer;
      this.newItem.producerSearchQuery = producer.producerName;
      this.newItem.producerSearchResults = [];
      this.newItem.searchQuery = '';
      this.newItem.searchResults = [];
      this.newItem.newMenuItemTarget = {};
    },
    clearProducerSelection() {
      this.newItem.selectedProducer = {};
      this.newItem.producerSearchQuery = '';
      this.newItem.producerSearchResults = [];
    },
    selectListing(listing) {
      this.newItem.newMenuItemTarget = listing;
      this.newItem.newMenuItemID = listing.id;
      this.newItem.searchQuery = listing.listingName;
      this.newItem.searchResults = [];
    },
    addItemToList() {
      if (!this.isNewItemValid) return;
      this.addedMenuItems.push(JSON.parse(JSON.stringify(this.newItem)));
      this.resetNewItemForm();
    },
    removeItemFromList(index) {
      this.addedMenuItems.splice(index, 1);
    },
    resetNewItemForm() {
      const servingTypeId = this.newItem.newMenuItemServingType;
      this.newItem = this.getInitialNewItemState();
      this.newItem.newMenuItemServingType = servingTypeId;
    },
    clearAddedItems() {
      this.addedMenuItems = [];
      this.resetNewItemForm();
    },
    submitAddedItems() {
      if (this.addedMenuItems.length === 0) return;

      const newItems = this.addedMenuItems.map(item => {
        return {
          itemID: item.newMenuItemID,
          name: item.newMenuItemTarget.listingName,
          itemPrice: item.newMenuItemPrice,
          servingType: item.newMenuItemServingType,
          variant: item.newMenuItemVintage,
          itemAvailability: true,
          photo: item.newMenuItemTarget.photo,
          bottler: item.newMenuItemTarget.producerName,
          drinkType: item.newMenuItemTarget.drinkType,
          abv: item.newMenuItemTarget.abv,
        };
      });

      this.$emit('items-selected', {
        newItems: newItems,
        targetSection: this.targetSection
      });

      this.clearAddedItems();
      this.hideModal();
    }
  },
  created() {
    this.fetchServingTypes();
    this.debouncedSearchProducers = debounce(this.searchProducers, 300);
    this.debouncedSearchListings = debounce(this.searchListings, 300);
  },
};
</script>
