<template>
    <div>
        <!-- If venue is unclaimed -->
        <div v-if="!claimStatus" class="text-center p-4 rounded" style="background-color: rgb(221, 200, 169);">
            <p class="fs-5 fw-bold">Do you own this business?</p>
            <p>Sign up for a venue account to share your bar's menu with your fans!</p>
            <button class="btn btn-warning fw-bold">Claim This Business</button>
        </div>

        <!-- If venue is claimed -->
        <div v-else>
            <!-- Menu header -->
            <div class="d-flex justify-content-between align-items-center mb-3">
                <!-- <p class="fs-5 fw-bold m-0">{{ (venue_menu.menu && venue_menu.menu.length) || 0 }} Sections On The Menu</p> -->
                <p class="fs-5 fw-bold m-0">{{ (displayMenu.menu && displayMenu.menu.length) || 0 }} Sections On The Menu</p>
                <div v-if="isSelfView" class="d-flex gap-2">
                    <button v-if="!isEditMode" class="btn btn-outline-primary" @click="toggleEditMode"><i class="bi bi-pencil me-1"></i>Edit Menu</button>
                    <button v-if="!isEditMode" class="btn btn-outline-secondary" data-bs-toggle="modal"
                        data-bs-target="#shareMenuModal"><i class="bi bi-share me-1"></i>Share Menu</button>
                </div>
            </div>

            <input id="menu_searchbar" type="text" class="form-control mb-3" placeholder="Search menu..." v-model="searchQuery"/>

            <!-- Edit Mode -->
            <div v-if="isEditMode">
                <VenueMenuEdit ref="venueMenuEdit" :menu-data="editableMenu" @cancel="toggleEditMode"
                    @save="handleSaveChanges" @request-add-listing="handleRequestAddListing" />

                <VenueMenuItems
                    v-if="sectionToAddTo"
                    :target-section="sectionToAddTo"
                    @items-selected="handleItemsSelected"
                    @hidden="sectionToAddTo = null"
                />
            </div>

            <!-- View Mode -->
            <div v-else>
                <!-- <div v-if="venue_menu.menu && venue_menu.menu.length > 0">
                    <div v-for="(section, index) in venue_menu.menu" :key="index" class="mb-2"> -->
                <div v-if="displayMenu.menu && displayMenu.menu.length > 0">
                    <div v-for="(section, index) in displayMenu.menu" :key="index" class="mb-2">
                        <!-- Section Header -->
                        <div class="d-flex justify-content-between align-items-center py-2 px-3 rounded"
                            style="background-color: #f0b258; cursor: pointer; user-select: none;"
                            @click="toggleSection(section, index)">
                            <div class="d-flex align-items-center">
                                <h6 class="mb-0 fw-semibold text-dark">{{ section.sectionName }}</h6>
                                <i :class="['bi', 'ms-2', section.isExpanded ? 'bi-chevron-up' : 'bi-chevron-down']"
                                    style="font-size: 12px;"></i>
                            </div>
                        </div>
                        <transition name="slide">
                            <div v-show="section.isExpanded" class="p-3 bg-white border border-top-0 rounded-bottom">
                                <!-- Sub-sections -->
                                <div v-if="section.subSections && section.subSections.length > 0" class="ps-4">
                                    <div v-for="(subSection, subIndex) in section.subSections" :key="subIndex" class="mb-2">
                                        <!-- Sub-section Header -->
                                        <div class="d-flex justify-content-between align-items-center py-2 px-3 rounded"
                                            style="background-color: #f0b258; cursor: pointer; user-select: none;"
                                            @click="toggleSubSection(subSection)">
                                            <div class="d-flex align-items-center">
                                                <h6 class="mb-0 fw-semibold text-dark">{{ subSection.sectionName }}</h6>
                                                <i :class="['bi', 'ms-2', subSection.isExpanded ? 'bi-chevron-up' : 'bi-chevron-down']"
                                                    style="font-size: 12px;"></i>
                                            </div>
                                        </div>
                                        <!-- Sub-section Content (Listings) -->
                                        <transition name="slide">
                                            <div v-show="subSection.isExpanded">
                                                <div v-if="subSection.isLoading" class="text-center p-4">
                                                    <div class="spinner-border spinner-border-sm me-2" role="status"></div>
                                                    Loading...
                                                </div>
                                                <div v-else-if="subSection.sectionMenu && subSection.sectionMenu.length > 0">
                                                    <div v-for="(item, itemIndex) in subSection.sectionMenu" :key="itemIndex" class="py-1 px-3">
                                                        <router-link :to="{ path: '/listing/view/' + item.itemID + '/' + item.name }" class="listing-item-link text-decoration-none">
                                                            <div class="card mb-3 listing-card border-0 shadow-sm">
                                                                <div class="card-body p-3">
                                                                    <div class="d-flex align-items-start">
                                                                        <div class="flex-shrink-0 me-3">
                                                                            <div class="image-wrapper d-flex align-items-center justify-content-center rounded-2" :style="{'width': '80px', 'height': '80px', 'background-color': '#f8f6f0', 'filter': item.itemAvailability === false ? 'grayscale(100%)' : 'none'}">
                                                                                <img v-if="item.photo && item.photo.trim() !== ''" :src="item.photo" :alt="item.name" class="img-fluid rounded" style="max-width: 70px; max-height: 70px; object-fit: contain;">
                                                                                <i v-else class="bi bi-cup-straw" style="font-size: 28px; color: #d4941e;"></i>
                                                                            </div>
                                                                        </div>
                                                                        <div class="flex-grow-1" style="min-width: 0;">
                                                                            <div class="d-flex justify-content-between align-items-start mb-1">
                                                                                <h5 class="card-title fw-semibold mb-0 me-2 item-title">{{ item.name }} {{ item.variant ? ' [' + item.variant + ' Vintage]' : '' }}</h5>
                                                                                <i class="bi bi-star text-warning flex-shrink-0"></i>
                                                                            </div>
                                                                            <p class="card-text text-muted small mb-2 lh-sm text-start">{{ item.bottler ? item.bottler : 'Unknown Producer' }} | {{ item.drinkType ? item.drinkType : 'N/A type' }} | {{ item.abv ? item.abv + '%' : 'N/A ABV' }}</p>
                                                                            <p class="card-text fw-medium mb-0 text-start">{{ item.itemPrice <= 0 ? '-' : `$ ${item.itemPrice} / ${item.servingTypeText}` }}</p>
                                                                            <p v-if="item.itemAvailability == false" class="text-start text-danger fw-bold fst-italic text-decoration-underline mb-0">Temporarily Unavailable</p>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </router-link>
                                                    </div>
                                                    <div v-if="subSection.pagination && subSection.pagination.total_pages > 1" class="p-2 bg-light">
                                                        <button class="btn btn-sm btn-outline-secondary me-1" :disabled="subSection.pagination.page <= 1" @click="loadSectionMenu(subSection, -1, subSection.pagination.page - 1)">Previous</button>
                                                        <span>Page {{ subSection.pagination.page }} of {{ subSection.pagination.total_pages }}</span>
                                                        <button class="btn btn-sm btn-outline-secondary ms-1" :disabled="subSection.pagination.page >= subSection.pagination.total_pages" @click="loadSectionMenu(subSection, -1, subSection.pagination.page + 1)">Next</button>
                                                    </div>
                                                </div>
                                                <div v-else class="py-2 px-3 text-muted small">No items in this sub-section.</div>
                                            </div>
                                        </transition>
                                    </div>
                                </div>

                                <!-- Separator -->
                                <hr v-if="section.subSections && section.subSections.length > 0 && section.sectionMenu && section.sectionMenu.length > 0" class="my-3">

                                <!-- Listings directly in section -->
                                <div v-if="section.isLoading" class="text-center p-4">
                                    <div class="spinner-border spinner-border-sm me-2" role="status"></div>
                                    Loading menu items...
                                </div>
                                <div v-else-if="section.sectionMenu && section.sectionMenu.length > 0">
                                    <div v-for="(item, itemIndex) in section.sectionMenu" :key="itemIndex" class="py-1 px-3">
                                        <router-link :to="{ path: '/listing/view/' + item.itemID + '/' + item.name }" class="listing-item-link text-decoration-none">
                                            <div class="card mb-3 listing-card border-0 shadow-sm">
                                                <div class="card-body p-3">
                                                    <div class="d-flex align-items-start">
                                                        <div class="flex-shrink-0 me-3">
                                                            <div class="image-wrapper d-flex align-items-center justify-content-center rounded-2" :style="{'width': '80px', 'height': '80px', 'background-color': '#f8f6f0', 'filter': item.itemAvailability === false ? 'grayscale(100%)' : 'none'}">
                                                                <img v-if="item.photo && item.photo.trim() !== ''" :src="item.photo" :alt="item.name" class="img-fluid rounded" style="max-width: 70px; max-height: 70px; object-fit: contain;">
                                                                <i v-else class="bi bi-cup-straw" style="font-size: 28px; color: #d4941e;"></i>
                                                            </div>
                                                        </div>
                                                        <div class="flex-grow-1" style="min-width: 0;">
                                                            <div class="d-flex justify-content-between align-items-start mb-1">
                                                                <h5 class="card-title fw-semibold mb-0 me-2 item-title">{{ item.name }} {{ item.variant ? ' [' + item.variant + ' Vintage]' : '' }}</h5>
                                                                <i class="bi bi-star text-warning flex-shrink-0"></i>
                                                            </div>
                                                            <p class="card-text text-muted small mb-2 lh-sm text-start">{{ item.bottler ? item.bottler : 'Unknown Producer' }} | {{ item.drinkType ? item.drinkType : 'N/A type' }} | {{ item.abv ? item.abv + '%' : 'N/A ABV' }}</p>
                                                            <p class="card-text fw-medium mb-0 text-start">{{ item.itemPrice <= 0 ? '-' : `$ ${item.itemPrice} / ${item.servingTypeText}` }}</p>
                                                            <p v-if="item.itemAvailability == false" class="text-start text-danger fw-bold fst-italic text-decoration-underline mb-0">Temporarily Unavailable</p>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </router-link>
                                    </div>
                                    <div v-if="section.pagination && section.pagination.total_pages > 1" class="p-2 bg-light">
                                        <button class="btn btn-sm btn-outline-secondary me-1" :disabled="section.pagination.page <= 1" @click="loadSectionMenu(section, index, section.pagination.page - 1)">Previous</button>
                                        <span>Page {{ section.pagination.page }} of {{ section.pagination.total_pages }}</span>
                                        <button class="btn btn-sm btn-outline-secondary ms-1" :disabled="section.pagination.page >= section.pagination.total_pages" @click="loadSectionMenu(section, index, section.pagination.page + 1)">Next</button>
                                    </div>
                                </div>
                                
                                <!-- Empty State for parent section -->
                                <div v-if="(!section.subSections || section.subSections.length === 0) && (!section.sectionMenu || section.sectionMenu.length === 0) && !section.isLoading" class="py-2 px-3 text-muted small">
                                    No items or sub-sections in this section.
                                </div>
                            </div>
                        </transition>
                    </div>
                </div>
                 <div v-else class="text-center text-muted p-4">
                    This venue hasn't added any drinks to their menu yet.
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import VenueMenuEdit from './VenueMenuEdit.vue';
import VenueMenuItems from './VenueMenuItems.vue';

function debounce(fn, delay) {
    var timeoutID = null;
    return function () {
        clearTimeout(timeoutID);
        var args = arguments;
        var that = this;
        timeoutID = setTimeout(function () {
            fn.apply(that, args);
        }, delay);
    };
}

export default {
    components: {
        VenueMenuEdit,
        VenueMenuItems
    },
    props: {
        claimStatus: Boolean,
        isSelfView: Boolean,
        venue_id: Number,
        venue_menu: Object,
    },
    emits: ['section-load-error', 'share-menu-clicked', 'menu-updated', 'save-menu', 'update:venue_menu'],
    data() {
        return {
            isEditMode: false,
            editableMenu: [],
            sectionToAddTo: null,
            searchQuery: '',
            original_venue_menu: null,
            // Add local menu data
            localMenu: null,
            isSearchActive: false,
        }
    },

    // Add computed property:
    computed: {
        displayMenu() {
            // Use local menu if search is active, otherwise use the prop
            if (this.isSearchActive && this.localMenu) {
                return this.localMenu;
            }
            return this.venue_menu;
        }
    },

    watch: {
        searchQuery() {
            this.debouncedSearch();
        },

        // Add watcher for venue_menu prop
        venue_menu: {
            handler(newMenu) {
                console.log('venue_menu prop changed:', newMenu);
                
                // Save original menu if not already saved and menu data is available
                if (newMenu && newMenu.menu && newMenu.menu.length > 0 && !this.original_venue_menu) {
                    this.original_venue_menu = JSON.parse(JSON.stringify(newMenu));
                    console.log('Saved original menu from prop update:', this.original_venue_menu);
                    
                    // Initialize expanded states
                    newMenu.menu.forEach(section => {
                        if (section.isExpanded === undefined) {
                            Object.assign(section, { isExpanded: false });
                        }
                        if (section.subSections) {
                            section.subSections.forEach(sub => {
                                if (sub.isExpanded === undefined) {
                                    Object.assign(sub, { isExpanded: false });
                                }
                            });
                        }
                    });
                }
            },
            immediate: true,
            deep: false
        }
    },
    created() {
        this.debouncedSearch = debounce(this.searchMenu, 500);
    },
    mounted() {
        console.log('Component mounted, venue_menu:', this.venue_menu);
        
        // Save original menu state
        if (this.venue_menu && this.venue_menu.menu) {
            this.original_venue_menu = JSON.parse(JSON.stringify(this.venue_menu));
            console.log('Saved original menu:', this.original_venue_menu);
            
            this.venue_menu.menu.forEach(section => {
                if (section.isExpanded === undefined) {
                    Object.assign(section, { isExpanded: false });
                }
                // Initialize isExpanded for subSections
                if (section.subSections) {
                    section.subSections.forEach(sub => {
                        if (sub.isExpanded === undefined) {
                            Object.assign(sub, { isExpanded: false });
                        }
                    });
                }
            });
        } else {
            console.warn('No venue_menu data available at mount time');
            // Try to save it later when it becomes available
            this.$nextTick(() => {
                if (this.venue_menu && this.venue_menu.menu && !this.original_venue_menu) {
                    this.original_venue_menu = JSON.parse(JSON.stringify(this.venue_menu));
                    console.log('Delayed save of original menu:', this.original_venue_menu);
                }
            });
        }
    },
    methods: {
        
        async searchMenu() {
            if (this.searchQuery.trim() === '') {
                // Reset to original menu
                this.isSearchActive = false;
                this.localMenu = null;
                return;
            }

            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getVenueMenuBySearch/${this.venue_id}`,
                    {
                        params: { searchTerm: this.searchQuery },
                        timeout: 10000,
                        headers: { 'Accept': 'application/json' }
                    }
                );
                
                if (response.data && response.data.menu) {
                    console.log('Search results:', response.data.menu);
                    
                    // Use current venue_menu as source
                    const sourceMenu = this.venue_menu?.menu || [];
                    console.log('Using source menu:', sourceMenu);
                    
                    // Clone the menu structure
                    const menuWithState = JSON.parse(JSON.stringify(sourceMenu));
                    
                    // Clear all menu items first
                    menuWithState.forEach(section => {
                        section.sectionMenu = [];
                        section.isExpanded = false;
                        if (section.subSections) {
                            section.subSections.forEach(sub => {
                                sub.sectionMenu = [];
                                sub.isExpanded = false;
                            });
                        }
                    });
                    
                    // Populate with search results
                    response.data.menu.forEach(searchSection => {
                        console.log(`Processing search section: ${searchSection.sectionName} (ID: ${searchSection.id}, Order: ${searchSection.sectionOrder})`);
                        
                        // Find matching section in original menu
                        const matchingSection = menuWithState.find(originalSection => {
                            const idMatch = originalSection.id === searchSection.id;
                            const nameMatch = originalSection.sectionName === searchSection.sectionName;
                            const orderMatch = originalSection.sectionOrder === searchSection.sectionOrder;
                            
                            return idMatch || nameMatch || orderMatch;
                        });
                        
                        if (matchingSection) {
                            console.log(`✓ Found match: ${matchingSection.sectionName}`);
                            
                            // Handle direct section menu items
                            matchingSection.sectionMenu = searchSection.sectionMenu || [];
                            let sectionHasContent = matchingSection.sectionMenu.length > 0;
                            
                            console.log(`✓ Section direct items: ${matchingSection.sectionMenu.length}`);
                            
                            // Handle subsections
                            if (searchSection.subSections && searchSection.subSections.length > 0) {
                                console.log(`Processing ${searchSection.subSections.length} subsections for ${searchSection.sectionName}`);
                                
                                searchSection.subSections.forEach(searchSub => {
                                    console.log(`  Processing subsection: ${searchSub.sectionName} (ID: ${searchSub.id})`);
                                    
                                    // Find matching subsection
                                    if (matchingSection.subSections) {
                                        const matchingSubSection = matchingSection.subSections.find(originalSub => {
                                            const idMatch = originalSub.id === searchSub.id;
                                            const nameMatch = originalSub.sectionName === searchSub.sectionName;
                                            const orderMatch = originalSub.sectionOrder === searchSub.sectionOrder;
                                            
                                            return idMatch || nameMatch || orderMatch;
                                        });
                                        
                                        if (matchingSubSection) {
                                            matchingSubSection.sectionMenu = searchSub.sectionMenu || [];
                                            const subHasContent = matchingSubSection.sectionMenu.length > 0;
                                            matchingSubSection.isExpanded = subHasContent;
                                            
                                            console.log(`  ✓ Subsection "${matchingSubSection.sectionName}" has ${matchingSubSection.sectionMenu.length} items, expanded: ${subHasContent}`);
                                            
                                            if (subHasContent) {
                                                sectionHasContent = true;
                                            }
                                        } else {
                                            console.log(`  ✗ No matching subsection found for "${searchSub.sectionName}"`);
                                        }
                                    }
                                });
                            }
                            
                            // Also check if the search section itself might be a subsection result
                            // (API might return subsections as top-level sections in search results)
                            if (searchSection.parentSectionId) {
                                console.log(`Search section ${searchSection.sectionName} has parentSectionId: ${searchSection.parentSectionId}`);
                                
                                // Find the parent section
                                const parentSection = menuWithState.find(section => section.id === searchSection.parentSectionId);
                                if (parentSection && parentSection.subSections) {
                                    const targetSubSection = parentSection.subSections.find(sub => 
                                        sub.id === searchSection.id || 
                                        sub.sectionName === searchSection.sectionName ||
                                        sub.sectionOrder === searchSection.sectionOrder
                                    );
                                    
                                    if (targetSubSection) {
                                        targetSubSection.sectionMenu = searchSection.sectionMenu || [];
                                        targetSubSection.isExpanded = targetSubSection.sectionMenu.length > 0;
                                        
                                        // Expand parent section too
                                        if (targetSubSection.isExpanded) {
                                            parentSection.isExpanded = true;
                                        }
                                        
                                        console.log(`✓ Updated subsection "${targetSubSection.sectionName}" in parent "${parentSection.sectionName}"`);
                                    }
                                }
                            }
                            
                            matchingSection.isExpanded = sectionHasContent;
                            console.log(`✓ Section "${matchingSection.sectionName}" final state - expanded: ${sectionHasContent}, direct items: ${matchingSection.sectionMenu.length}`);
                        } else {
                            console.log(`✗ No matching section found for "${searchSection.sectionName}"`);
                        }
                    });
                    
                    console.log('Final menu state:', menuWithState.map(s => ({
                        name: s.sectionName,
                        expanded: s.isExpanded,
                        itemCount: s.sectionMenu?.length || 0
                    })));

                    // Set local menu and activate search mode
                    this.localMenu = { ...this.venue_menu, menu: menuWithState };
                    this.isSearchActive = true;
                }

            } catch (error) {
                console.error('Error searching menu:', error);
            }
        },

        toggleEditMode() {
            this.isEditMode = !this.isEditMode;
            if (this.isEditMode) {
                this.editableMenu = JSON.parse(JSON.stringify(this.venue_menu.menu));
            }
        },
        async handleSaveChanges(updatedMenu) {
            console.log('Emitting save-menu event:', updatedMenu);
            this.$emit('save-menu', updatedMenu);
            this.isEditMode = false;
        },
        handleRequestAddListing(section) {
            this.sectionToAddTo = section;
        },
        handleItemsSelected({ newItems, targetSection }) {
            if (this.$refs.venueMenuEdit) {
                newItems.forEach(item => {
                    this.$refs.venueMenuEdit.addListingItem(item, targetSection);
                });
            }
        },
        async toggleSection(section, index) {
            section.isExpanded = !section.isExpanded;
            if (this.searchQuery.trim() === '' && section.isExpanded && (!section.sectionMenu || section.sectionMenu.length === 0)) {
                await this.loadSectionMenu(section, index);
            }
        },
        async loadSectionMenu(section, index, page = 1, limit = 30) {
            if (!section || !section.id) {
                console.error('Invalid section provided to loadSectionMenu');
                return;
            }
            if (section.isLoading) return;

            try {
                section.isLoading = true;
                section.hasError = false;
                section.errorMessage = null;

                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getVenueMenu/${section.id}`,
                    {
                        params: { page, limit },
                        timeout: 10000,
                        headers: { 'Accept': 'application/json' }
                    }
                );

                if (!response.data) throw new Error('Invalid response format');

                const items = response.data.data || [];
                const pagination = response.data.pagination || { page, limit, total_pages: 1 };

                section.sectionMenu = items;
                section.pagination = pagination;
                section.itemCount = pagination.total_items || items.length;

            } catch (error) {
                console.error(`Error loading menu section ${section.id}:`, error);
                section.hasError = true;
                section.sectionMenu = [];
                section.itemCount = 0;

                if (error.code === 'ECONNABORTED') {
                    section.errorMessage = 'Request timed out. Please try again.';
                } else if (error.response?.status === 404) {
                    section.errorMessage = 'Menu section not found.';
                } else if (error.response?.status >= 500) {
                    section.errorMessage = 'Server error. Please try again later.';
                } else if (!navigator.onLine) {
                    section.errorMessage = 'No internet connection.';
                } else {
                    section.errorMessage = 'Failed to load menu. Please try again.';
                }

                this.$emit('section-load-error', {
                    section,
                    index,
                    error,
                    errorMessage: section.errorMessage,
                    canRetry: error.response?.status !== 404
                });

            } finally {
                section.isLoading = false;
            }
        },
        toggleSubSection(subSection) {
            subSection.isExpanded = !subSection.isExpanded;
            if (this.searchQuery.trim() === '' && subSection.isExpanded && (!subSection.sectionMenu || subSection.sectionMenu.length === 0)) {
                // The index is not critical here, passing a placeholder
                this.loadSectionMenu(subSection, -1);
            }
        }
    }
};
</script>

<style scoped>
.listing-item-link {
    color: inherit;
}

.listing-card {
    transition: all 0.2s ease;
    border-radius: 12px !important;
}

.listing-card:hover {
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
    transform: translateY(-2px);
}

.item-title {
    text-decoration: underline;
    color: #2c3e50;
    font-size: 1rem;
}

.card-text.text-muted {
    color: #6c757d !important;
}

.card-text.fw-medium {
    color: #2c3e50;
}

/* Responsive adjustments */
@media (max-width: 576px) {
    .image-wrapper {
        width: 60px !important;
        height: 60px !important;
    }

    .image-wrapper img {
        max-width: 50px !important;
        max-height: 50px !important;
    }

    .item-title {
        font-size: 0.9rem;
    }

    .card-text.small {
        font-size: 0.8rem !important;
    }
}

/* Slide animation */
.slide-enter-active,
.slide-leave-active {
    transition: all 0.3s ease;
    overflow: hidden;
}

.slide-enter-from,
.slide-leave-to {
    max-height: 0;
    opacity: 0;
}

.slide-enter-to,
.slide-leave-from {
    max-height: 1000px; /* Adjust as needed */
    opacity: 1;
}
</style>