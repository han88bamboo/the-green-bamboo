<template>
    <div class="menu-wrapper position-relative">
        <!-- Menu Loading Overlay -->
        <div class="menu-loading-overlay" :class="{ visible: showMenuLoadingOverlay }">
            <span class="spinner">⟳</span>
            Loading Menu Editor...
        </div>

        <!-- Menu Edit Mode -->
        <div v-if="editMenuMode">
            <!-- ------- START Edit Menu Header ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Edit Menu Header -->
            <div class="row">
                <div class="col-12 text-center py-3" style="background-color: #f0b358;">
                    <h1 class="fs-5 fw-bold mb-0">Menu Edit Mode</h1>
                </div>
            </div>

            <!-- ------- END Edit Menu Header / START Edit Menu Actions ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Edit Menu Actions -->
            <div class="row">
                <div class="col-12 text-center py-3" style="background-color: #f9f9f9;">
                    <div class="d-flex justify-content-center align-items-center flex-wrap gap-2">
                        
                        <!-- Cancel Button -->
                        <button type="button" class="btn btn-outline-danger" @click="cancelEditMode">
                            Cancel
                        </button>

                        <!-- Add Menu Section Button -->
                        <button type="button" class="btn btn-outline-primary" @click="addMenuSection">
                            Add Menu Section
                        </button>

                        <!-- Add Menu Item Button -->
                        <button type="button" class="btn btn-outline-success" data-bs-toggle="modal"
                            data-bs-target="#addMenuItemModal" @click="resetMultipleMenuItems">
                            Add Menu Item
                        </button>

                        <!-- Save Menu Button -->
                        <button type="button" class="btn btn-primary" @click="updateMenu">
                            Save Menu
                        </button>

                    </div>
                </div>
            </div>

            <!-- ------- END Edit Menu Actions / START Edit Menu Sections ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Edit Menu Sections -->
            <div class="row">
                <div class="col-12 py-3">

                    <!-- Draggable Menu Sections -->
                    <draggable 
                        v-model="editMenu" 
                        item-key="sectionOrder" 
                        handle=".section-drag-handle" 
                        ghost-class="ghost"
                        @start="dragStart"
                        @end="dragEnd"
                    >
                        <template #item="{ element: menuSection }">
                            <div class="mb-3">

                                <!-- Section Header -->
                                <div class="row align-items-center py-2 px-3" style="background-color: #f0b358;">
                                    <div class="col-8 d-flex align-items-center">
                                        <span class="section-drag-handle me-2" style="cursor: grab;">
                                            ⋮⋮
                                        </span>
                                        <h5 class="fw-bold mb-0">{{ menuSection.sectionName }}</h5>
                                    </div>
                                    <div class="col-4 text-end">
                                        <!-- Rename Section Button -->
                                        <button type="button" class="btn btn-sm btn-outline-secondary me-1"
                                            data-bs-toggle="modal" data-bs-target="#renameMenuSectionModal"
                                            @click="populateRenameMenuSectionModal(menuSection.sectionOrder)">
                                            Rename
                                        </button>
                                        <!-- Delete Section Button -->
                                        <button type="button" class="btn btn-sm btn-outline-danger"
                                            @click="deleteMenuSection(menuSection.sectionOrder)">
                                            Delete
                                        </button>
                                    </div>
                                </div>

                                <!-- Section Contents -->
                                <div class="border border-top-0 p-3" style="background-color: #ffffff;">

                                    <!-- Draggable Menu Items within Section -->
                                    <draggable 
                                        v-model="menuSection.sectionMenu" 
                                        item-key="itemOrder" 
                                        handle=".item-drag-handle" 
                                        ghost-class="ghost"
                                        @start="dragItemStart(menuSection)"
                                        @end="dragItemEnd(menuSection)"
                                    >
                                        <template #item="{ element: menuItem }">
                                            <div class="row align-items-center py-2 px-3 mb-2 border rounded">

                                                <!-- Drag Handle -->
                                                <div class="col-1">
                                                    <span class="item-drag-handle" style="cursor: grab;">
                                                        ⋮⋮
                                                    </span>
                                                </div>

                                                <!-- Item Photo -->
                                                <div class="col-2">
                                                    <img :src="menuItem.itemDetails['itemPhoto'] || defaultPhoto"
                                                        class="img-fluid rounded" style="max-height: 80px;">
                                                </div>

                                                <!-- Item Details -->
                                                <div class="col-6">
                                                    <h6 class="fw-bold mb-1">{{ menuItem.itemDetails['itemName'] }}</h6>
                                                    <p class="text-muted mb-1 small">
                                                        <span v-if="menuItem.itemDetails['itemProducer']">
                                                            {{ menuItem.itemDetails['itemProducer'] }} |
                                                        </span>
                                                        <span v-if="menuItem.itemDetails['itemType']">
                                                            {{ menuItem.itemDetails['itemType'] }} |
                                                        </span>
                                                        <span v-if="menuItem.itemDetails['itemABV']">
                                                            {{ menuItem.itemDetails['itemABV'] }} ABV |
                                                        </span>
                                                        <span v-if="menuItem.itemDetails['itemCountry']">
                                                            {{ menuItem.itemDetails['itemCountry'] }}
                                                        </span>
                                                    </p>
                                                </div>

                                                <!-- Item Controls -->
                                                <div class="col-3">
                                                    <!-- Availability Toggle -->
                                                    <div class="form-check form-switch mb-2">
                                                        <input class="form-check-input" type="checkbox" 
                                                            v-model="menuItem.itemAvailability"
                                                            :id="'avail-' + menuSection.sectionOrder + '-' + menuItem.itemOrder">
                                                        <label class="form-check-label text-small" 
                                                            :for="'avail-' + menuSection.sectionOrder + '-' + menuItem.itemOrder">
                                                            {{ menuItem.itemAvailability ? 'Available' : 'Unavailable' }}
                                                        </label>
                                                    </div>

                                                    <!-- Price Input -->
                                                    <div class="input-group input-group-sm mb-2">
                                                        <span class="input-group-text">$</span>
                                                        <input type="number" class="form-control" 
                                                            v-model="menuItem.itemPrice" 
                                                            placeholder="-" min="0" step="0.01">
                                                    </div>

                                                    <!-- Serving Type -->
                                                    <div class="input-group input-group-sm mb-2">
                                                        <span class="input-group-text">/</span>
                                                        <select class="form-select" v-model="menuItem.itemServingType">
                                                            <option v-for="servingType in servingTypes"
                                                                :key="servingType.id" :value="servingType.id">
                                                                {{ servingType.servingType }}
                                                            </option>
                                                        </select>
                                                    </div>

                                                    <!-- Delete Item Button -->
                                                    <button type="button" class="btn btn-sm btn-outline-danger w-100"
                                                        @click="deleteMenuItem(menuSection.sectionOrder, menuItem.itemOrder)">
                                                        Remove
                                                    </button>
                                                </div>

                                            </div>
                                        </template>
                                    </draggable>

                                    <!-- Empty Section Message -->
                                    <div v-if="!menuSection.sectionMenu || menuSection.sectionMenu.length === 0" 
                                        class="text-center py-4 text-muted">
                                        <p>No items in this section. Use "Add Menu Item" to add drinks.</p>
                                    </div>

                                </div>

                            </div>
                        </template>
                    </draggable>

                    <!-- Empty Menu Message -->
                    <div v-if="!editMenu || editMenu.length === 0" class="text-center py-4 text-muted">
                        <p>No menu sections yet. Use "Add Menu Section" to get started.</p>
                    </div>

                </div>
            </div>

            <!-- ------- END Edit Menu Sections ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

        </div>

        <!-- Rename Menu Section Modal -->
        <div class="modal fade" id="renameMenuSectionModal" tabindex="-1" aria-labelledby="renameMenuSectionModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="renameMenuSectionModalLabel">Rename Menu Section</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="form-group">
                            <label for="renameMenuSectionInput" class="form-label">Section Name</label>
                            <input type="text" class="form-control" id="renameMenuSectionInput" 
                                v-model="renameMenuSectionModalNew" placeholder="Enter new section name">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="renameMenuSection">
                            Save Changes
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Add Menu Item Modal -->
        <div class="modal fade" id="addMenuItemModal" tabindex="-1" aria-labelledby="addMenuItemModal" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <!-- Modal Header -->
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="addMenuItemModalLabel">Add Menu Items</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <!-- Modal Body -->
                    <div class="modal-body modal-body-scrollable">
                        <!-- Note -->
                        <p class="fw-bold" style="color: #ae3e3e">You will need an existing Menu Section to be created first before you can start adding menu items to your menu!</p>
                        <p class="fw-bold" style="color: #ae3e3e">If you have just added a new Menu Section, remember to click "Save" first before adding a new menu item.</p>

                        <!-- Global Target Menu Section -->
                        <div class="form-group mb-4 p-3" style="background-color: #f8f9fa; border-radius: 8px;">
                            <p class="text-start mb-1 fw-bold">Target Menu Section (applies to all items) <span class="text-danger">*</span></p>
                            <select class="form-select" aria-label="globalMenuItemTargetSection"
                                v-model="globalMenuItemTargetSection" @change="updateGlobalMenuItemTargetSection">
                                <option value="">Select a menu section...</option>
                                <option v-for="(menuSection, sectionIndex) in editMenu" :key="menuSection" :value="menuSection">
                                    #{{ sectionIndex }}: {{ menuSection.sectionName }}
                                </option>
                            </select>
                            <p v-show="Object.keys(this.globalMenuItemTargetSection).length !== 0"
                                class="text-start mb-1 text-danger" id="globalMenuItemTargetSectionError"></p>
                        </div>

                        <!-- Multiple Menu Items Container -->
                        <div v-for="(item, itemIndex) in multipleMenuItems" :key="'item-' + itemIndex" class="mb-4">
                            <!-- Item Header -->
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="fw-bold text-primary mb-0">Item {{ itemIndex + 1 }}</h5>
                                <button v-if="itemIndex > 0" type="button" class="btn btn-outline-danger btn-sm"
                                    @click="removeMenuItem(itemIndex)">
                                    Remove Item
                                </button>
                            </div>

                            <div class="border rounded p-3" style="background-color: #fafafa;">
                                <!-- Producer search -->
                                <div class="form-group mb-3">
                                    <p class="text-start mb-1">Producer (Distillery, Brewery, Winery, etc.) (Optional)
                                        <span class="text-muted" style="font-size: 14px;"> Select a producer to filter drink search</span>
                                    </p>
                                    <input type="text" class="form-control" v-model="item.producerSearchQuery"
                                        @input="debouncedSearchProducers(itemIndex)"
                                        :placeholder="'Search for a producer to filter drinks (Item ' + (itemIndex + 1) + ')'" />

                                    <ul class="list-group" v-if="item.producerSearchResults && item.producerSearchResults.length > 0 && item.producerSearchQuery">
                                        <li v-for="producer in item.producerSearchResults" :key="producer.id"
                                            class="list-group-item list-group-item-action" @click="selectProducer(producer, itemIndex)">
                                            {{ producer.producerName }}
                                            <small class="text-muted">({{ producer.originCountry }})</small>
                                        </li>
                                    </ul>

                                    <!-- Show selected producer -->
                                    <div v-if="item.selectedProducer && item.selectedProducer.id" class="mt-2">
                                        <div class="d-flex align-items-center p-2 bg-light rounded">
                                            <span class="me-2">Selected Producer:</span>
                                            <strong>{{ item.selectedProducer.producerName }}</strong>
                                            <button type="button" class="btn btn-sm btn-outline-danger ms-auto"
                                                @click="item.selectedProducer = {}; item.producerSearchQuery = ''">
                                                Clear
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                <!-- Drink search -->
                                <div class="form-group mb-3">
                                    <p class="text-start mb-1">Drink <span class="text-danger">*</span></p>
                                    <input type="text" class="form-control" v-model="item.searchQuery"
                                        @input="debouncedSearchMultiple(itemIndex)"
                                        :placeholder="'Search for a drink (Item ' + (itemIndex + 1) + ')'" />

                                    <ul class="list-group" v-if="item.searchResults && item.searchResults.length > 0 && item.searchQuery">
                                        <li v-for="listing in item.searchResults" :key="listing.id"
                                            class="list-group-item list-group-item-action" @click="selectListingMultiple(listing, itemIndex)">
                                            {{ listing.listingName }}
                                            <small class="text-muted">({{ listing.producerName }})</small>
                                        </li>
                                    </ul>

                                    <!-- Show selected drink -->
                                    <div v-if="item.newMenuItemTarget && item.newMenuItemTarget.id" class="mt-2">
                                        <div class="d-flex align-items-center p-2 bg-success bg-opacity-10 rounded">
                                            <span class="me-2">Selected Drink:</span>
                                            <strong>{{ item.newMenuItemTarget.listingName }}</strong>
                                        </div>
                                    </div>
                                </div>

                                <!-- Price and Serving Type -->
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group mb-3">
                                            <p class="text-start mb-1">Price (Optional)</p>
                                            <div class="input-group">
                                                <span class="input-group-text">$</span>
                                                <input type="number" class="form-control" v-model="item.newMenuItemPrice"
                                                    placeholder="0.00" min="0" step="0.01">
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group mb-3">
                                            <p class="text-start mb-1">Serving Type</p>
                                            <select class="form-select" v-model="item.newMenuItemServingType">
                                                <option v-for="servingType in servingTypes" :key="servingType.id" :value="servingType.id">
                                                    {{ servingType.servingType }}
                                                </option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Add More Items Button -->
                        <div class="text-center mb-3">
                            <button type="button" class="btn btn-outline-primary" @click="addAdditionalItem" 
                                v-if="multipleMenuItems.length < 20">
                                Add Another Item
                            </button>
                        </div>
                    </div>

                    <!-- Modal Footer -->
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" @click="addMultipleMenuItems" 
                            :disabled="!isValidToSubmitMultiple()">
                            Add {{ getValidItemsCount() }} Item(s) to Menu
                        </button>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import draggable from 'vuedraggable';

export default {
    name: 'VenueMenuEditOriginal',
    components: {
        draggable
    },
    props: {
        editMenuMode: {
            type: Boolean,
            default: false
        },
        editMenu: {
            type: Array,
            default: () => []
        },
        servingTypes: {
            type: Array,
            default: () => []
        },
        targetVenue: {
            type: Object,
            default: () => ({})
        },
        defaultPhoto: {
            type: String,
            default: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
        },
        multipleMenuItems: {
            type: Array,
            default: () => []
        },
        globalMenuItemTargetSection: {
            type: Object,
            default: () => ({})
        },
        renameMenuSectionModalTarget: {
            type: Object,
            default: () => ({})
        },
        renameMenuSectionModalOld: {
            type: String,
            default: ''
        },
        renameMenuSectionModalNew: {
            type: String,
            default: ''
        },
        showMenuLoadingOverlay: {
            type: Boolean,
            default: false
        },
        menuSnapshot: {
            type: String,
            default: null
        }
    },
    data() {
        return {
            // No additional data needed - using props
        }
    },
    methods: {
        // Cancel Edit Mode
        cancelEditMode() {
            this.$emit('cancel-edit');
        },

        // Reset Edit Menu
        resetEditMenu() {
            this.$emit('reset-edit-menu');
        },

        // Add Menu Section
        addMenuSection() {
            this.$emit('add-menu-section');
        },

        // Delete Menu Section
        deleteMenuSection(index) {
            this.$emit('delete-menu-section', index);
        },

        // Populate Rename Menu Section Modal
        populateRenameMenuSectionModal(index) {
            this.$emit('populate-rename-modal', index);
        },

        // Rename Menu Section
        renameMenuSection() {
            this.$emit('rename-menu-section');
        },

        // Delete Menu Item
        deleteMenuItem(sectionIndex, itemIndex) {
            this.$emit('delete-menu-item', sectionIndex, itemIndex);
        },

        // Update Menu
        updateMenu() {
            this.$emit('update-menu');
        },

        // Add Additional Item (for multiple items modal)
        addAdditionalItem() {
            this.$emit('add-additional-item');
        },

        // Remove Menu Item (for multiple items modal)
        removeMenuItem(itemIndex) {
            this.$emit('remove-menu-item', itemIndex);
        },

        // Reset Multiple Menu Items
        resetMultipleMenuItems() {
            this.$emit('reset-multiple-menu-items');
        },

        // Debounced Search for Producers
        debouncedSearchProducers(itemIndex) {
            this.$emit('debounced-search-producers', itemIndex);
        },

        // Select Producer
        selectProducer(producer, itemIndex) {
            this.$emit('select-producer', producer, itemIndex);
        },

        // Debounced Search for Multiple Items
        debouncedSearchMultiple(itemIndex) {
            this.$emit('debounced-search-multiple', itemIndex);
        },

        // Select Listing for Multiple Items
        selectListingMultiple(listing, itemIndex) {
            this.$emit('select-listing-multiple', listing, itemIndex);
        },

        // Update Global Menu Item Target Section
        updateGlobalMenuItemTargetSection() {
            this.$emit('update-global-target-section');
        },

        // Check if valid to submit multiple items
        isValidToSubmitMultiple() {
            if (Object.keys(this.globalMenuItemTargetSection).length === 0) {
                return false;
            }
            return this.multipleMenuItems.some(item =>
                item.newMenuItemID && Object.keys(item.newMenuItemTarget).length > 0
            );
        },

        // Get count of valid items
        getValidItemsCount() {
            return this.multipleMenuItems.filter(item =>
                item.newMenuItemID && Object.keys(item.newMenuItemTarget).length > 0
            ).length;
        },

        // Add Multiple Menu Items
        addMultipleMenuItems() {
            this.$emit('add-multiple-menu-items');
        },

        // Drag handlers
        dragStart() {
            this.$emit('drag-start');
        },

        dragEnd() {
            this.$emit('drag-end');
        },

        dragItemStart(menuSection) {
            this.$emit('drag-item-start', menuSection);
        },

        dragItemEnd(menuSection) {
            this.$emit('drag-item-end', menuSection);
        }
    }
}
</script>

<style scoped>
.ghost {
    opacity: 0.5;
    background: #c8ebfb;
}

.section-drag-handle,
.item-drag-handle {
    font-size: 1.2em;
    color: #666;
    user-select: none;
}

.section-drag-handle:hover,
.item-drag-handle:hover {
    color: #333;
}

/* Menu-specific overlay styling */
.menu-wrapper {
    position: relative;
}

.menu-loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 9999;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 24px;
    font-weight: bold;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
}

.menu-loading-overlay.visible {
    opacity: 1;
    pointer-events: all;
}

.menu-loading-overlay .spinner {
    margin-right: 10px;
    animation: spin 1s infinite linear;
    display: inline-block;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}
</style>
