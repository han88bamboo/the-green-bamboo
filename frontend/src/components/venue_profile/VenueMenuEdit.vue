<template>
    <div class="edit-menu-container p-3 bg-light rounded-3 mt-3">
        <!-- Header -->
        <div class="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom">
            <h4 class="mb-0 fw-bold">
                <i class="bi bi-pencil-square me-2"></i>Edit Menu
            </h4>
            <div>
                <button class="btn btn-outline-secondary me-2" @click="$emit('cancel')">
                    <i class="bi bi-x-lg me-1"></i>Cancel
                </button>
                <button class="btn btn-primary" @click="saveChanges">
                    <i class="bi bi-check-lg me-1"></i>Save Changes
                </button>
            </div>
        </div>

        <!-- Instructions -->
        <div class="alert alert-info d-flex align-items-center" role="alert">
            <i class="bi bi-info-circle-fill me-3 fs-4"></i>
            <div>
                Drag and drop sections or sub-sections to reorder them. Click to expand and manage contents.
            </div>
        </div>

        <!-- Draggable Sections -->
        <draggable v-model="localMenu" item-key="id" handle=".drag-handle" ghost-class="ghost" @end="updateSectionOrder">
            <template #item="{ element: section, index }">
                <div class="mb-2">
                    <div class="d-flex justify-content-between align-items-center py-2 px-3 rounded"
                        style="background-color: #f0b258; cursor: default;">
                        <div class="d-flex align-items-center flex-grow-1">
                            <i class="bi bi-grip-vertical drag-handle me-2" style="cursor: grab;"></i>
                            <input v-if="section.isEditingName" v-model="section.sectionName" 
                                   @blur="finishEditingName(section)" @keyup.enter="finishEditingName(section)" 
                                   class="form-control form-control-sm me-2" type="text" v-focus>
                            <h6 v-else class="mb-0 fw-semibold text-dark" @click="toggleSection(section)" style="cursor: pointer;">
                                {{ section.sectionName }}
                            </h6>
                            <i :class="['bi', 'ms-2', section.isExpanded ? 'bi-chevron-up' : 'bi-chevron-down']"
                                style="font-size: 12px; cursor: pointer;" @click="toggleSection(section)"></i>
                        </div>
                        <div>
                            <button class="btn btn-sm btn-outline-secondary me-1" @click="editSectionName(section)" title="Edit name">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-danger" @click="confirmDeleteSection(section, index)" title="Delete section">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Expanded Section Content -->
                    <transition name="slide">
                        <div v-if="section.isExpanded" class="p-3 bg-white border border-top-0 rounded-bottom">
                            <!-- Action Buttons -->
                            <div class="d-flex gap-2 mb-3">
                                <button class="btn btn-sm btn-outline-primary" @click="addSubsection(section)">
                                    <i class="bi bi-plus-lg"></i> Add Sub-section
                                </button>
                                <button class="btn btn-sm btn-outline-success" @click="addListing(section)" :disabled="section.isLoading">
                                    <i class="bi bi-plus-lg"></i> Add Listing
                                </button>
                            </div>

                            <!-- Sub-sections -->
                            <div class="ps-4"> <!-- Indentation for sub-sections -->
                                <draggable v-model="section.subSections" item-key="id" handle=".drag-handle-subsection" ghost-class="ghost" @end="updateSubSectionOrder(section)">
                                    <template #item="{ element: subSection, index: subSectionIndex }">
                                        <div class="mb-2">
                                            <div class="d-flex justify-content-between align-items-center py-2 px-3 rounded" style="background-color: #e9ecef; cursor: default;">
                                                <div class="d-flex align-items-center flex-grow-1">
                                                    <i class="bi bi-grip-vertical drag-handle-subsection me-2" style="cursor: grab;"></i>
                                                    <input v-if="subSection.isEditingName" v-model="subSection.sectionName" 
                                                           @blur="finishEditingName(subSection)" @keyup.enter="finishEditingName(subSection)" 
                                                           class="form-control form-control-sm me-2" type="text" v-focus>
                                                    <h6 v-else class="mb-0 fw-semibold text-dark" @click="toggleSubSection(subSection)" style="cursor: pointer;">
                                                        {{ subSection.sectionName }}
                                                    </h6>
                                                    <i :class="['bi', 'ms-2', subSection.isExpanded ? 'bi-chevron-up' : 'bi-chevron-down']"
                                                        style="font-size: 12px; cursor: pointer;" @click="toggleSubSection(subSection)"></i>
                                                </div>
                                                <div>
                                                    <button class="btn btn-sm btn-outline-secondary me-1" @click="editSectionName(subSection)" title="Edit name">
                                                        <i class="bi bi-pencil"></i>
                                                    </button>
                                                    <button class="btn btn-sm btn-outline-danger" @click="confirmDeleteSubSection(section, subSectionIndex)" title="Delete sub-section">
                                                        <i class="bi bi-trash"></i>
                                                    </button>
                                                </div>
                                            </div>
                                            <!-- Listings within sub-section -->
                                            <transition name="slide">
                                                <div v-if="subSection.isExpanded" class="p-3 bg-white border border-top-0 rounded-bottom">
                                                    <draggable 
                                                        v-if="subSection.sectionMenu && subSection.sectionMenu.length" 
                                                        v-model="subSection.sectionMenu" 
                                                        item-key="itemID" 
                                                        handle=".drag-handle-item" 
                                                        ghost-class="ghost" 
                                                        group="menu-items"
                                                        @change="onItemChange">
                                                        <template #item="{ element: item, index: itemIndex }">
                                                            <div class="d-flex align-items-center p-2 border-bottom listing-edit-item">
                                                                <i class="bi bi-grip-vertical drag-handle-item me-2" style="cursor: grab;"></i>
                                                                <span class="flex-grow-1">{{ item.name }}</span>
                                                                <div class="d-flex gap-2">
                                                                    <button class="btn btn-sm btn-outline-secondary" title="Move to Top" @click="moveToTop(subSection.sectionMenu, itemIndex)">
                                                                        <i class="bi bi-arrow-up"></i>
                                                                    </button>
                                                                    <button class="btn btn-sm btn-outline-danger" title="Remove from section" @click="removeItem(subSection.sectionMenu, itemIndex)">
                                                                        <i class="bi bi-x"></i>
                                                                    </button>
                                                                </div>
                                                            </div>
                                                        </template>
                                                    </draggable>
                                                    <!-- Empty state and drop zone for sub-sections -->
                                                    <draggable 
                                                        v-else 
                                                        v-model="subSection.sectionMenu" 
                                                        item-key="itemID" 
                                                        handle=".drag-handle-item" 
                                                        ghost-class="ghost" 
                                                        group="menu-items"
                                                        @change="onItemChange"
                                                        class="empty-drop-zone">
                                                        <template #item="{ element: item, index: itemIndex }">
                                                            <div class="d-flex align-items-center p-2 border-bottom listing-edit-item">
                                                                <i class="bi bi-grip-vertical drag-handle-item me-2" style="cursor: grab;"></i>
                                                                <span class="flex-grow-1">{{ item.name }}</span>
                                                                <div class="d-flex gap-2">
                                                                    <button class="btn btn-sm btn-outline-secondary" title="Move to Top" @click="moveToTop(subSection.sectionMenu, itemIndex)">
                                                                        <i class="bi bi-arrow-up"></i>
                                                                    </button>
                                                                    <button class="btn btn-sm btn-outline-danger" title="Remove from section" @click="removeItem(subSection.sectionMenu, itemIndex)">
                                                                        <i class="bi bi-x"></i>
                                                                    </button>
                                                                </div>
                                                            </div>
                                                        </template>
                                                        <template #footer>
                                                            <div v-if="subSection.sectionMenu.length === 0" class="text-muted p-3 text-center border-2 border-dashed rounded" style="border-color: #dee2e6 !important;">
                                                                Drop items here or click button below to add
                                                            </div>
                                                        </template>
                                                    </draggable>
                                                    <div class="mt-2">
                                                        <button class="btn btn-sm btn-outline-success w-100" @click="addListing(subSection)" :disabled="subSection.isLoading">
                                                            <i class="bi bi-plus-lg"></i> Add Listing to Sub-section
                                                        </button>
                                                    </div>
                                                </div>
                                            </transition>
                                        </div>
                                    </template>
                                </draggable>
                            </div>

                            <hr v-if="section.subSections && section.subSections.length > 0 && section.sectionMenu && section.sectionMenu.length > 0" class="my-3">

                            <!-- Listings directly in section -->
                            <div v-if="section.isLoading" class="text-center p-4">
                                <div class="spinner-border spinner-border-sm me-2" role="status"></div>
                                Loading all items...
                            </div>
                            <draggable 
                                v-else-if="section.sectionMenu && section.sectionMenu.length" 
                                v-model="section.sectionMenu" 
                                item-key="itemID" 
                                handle=".drag-handle-item" 
                                ghost-class="ghost" 
                                group="menu-items"
                                @change="onItemChange">
                                <template #item="{ element: item, index: itemIndex }">
                                    <div class="d-flex align-items-center p-2 border-bottom listing-edit-item">
                                        <i class="bi bi-grip-vertical drag-handle-item me-2" style="cursor: grab;"></i>
                                        <span class="flex-grow-1">{{ item.name }}</span>
                                        <div class="d-flex gap-2">
                                            <button class="btn btn-sm btn-outline-secondary" title="Move to Top" @click="moveToTop(section.sectionMenu, itemIndex)">
                                                <i class="bi bi-arrow-up"></i>
                                            </button>
                                            <button class="btn btn-sm btn-outline-danger" title="Remove from section" @click="removeItem(section.sectionMenu, itemIndex)">
                                                <i class="bi bi-x"></i>
                                            </button>
                                        </div>
                                    </div>
                                </template>
                            </draggable>
                            <!-- Empty state for parent section -->
                            <draggable 
                                v-else-if="!section.isLoading" 
                                v-model="section.sectionMenu" 
                                item-key="itemID" 
                                handle=".drag-handle-item" 
                                ghost-class="ghost" 
                                group="menu-items"
                                @change="onItemChange"
                                class="empty-drop-zone">
                                <template #item="{ element: item, index: itemIndex }">
                                    <div class="d-flex align-items-center p-2 border-bottom listing-edit-item">
                                        <i class="bi bi-grip-vertical drag-handle-item me-2" style="cursor: grab;"></i>
                                        <span class="flex-grow-1">{{ item.name }}</span>
                                        <div class="d-flex gap-2">
                                            <button class="btn btn-sm btn-outline-secondary" title="Move to Top" @click="moveToTop(section.sectionMenu, itemIndex)">
                                                <i class="bi bi-arrow-up"></i>
                                            </button>
                                            <button class="btn btn-sm btn-outline-danger" title="Remove from section" @click="removeItem(section.sectionMenu, itemIndex)">
                                                <i class="bi bi-x"></i>
                                            </button>
                                        </div>
                                    </div>
                                </template>
                                <template #footer>
                                    <!--<div v-if="section.sectionMenu.length === 0 && (!section.subSections || section.subSections.length === 0)" class="text-muted p-3 text-center border-2 border-dashed rounded" style="border-color: #dee2e6 !important;">
                                        Drop items here or click button above to add
                                    </div> -->
                                </template> 
                            </draggable>
                            
                            <div v-if="!section.isLoading && (!section.sectionMenu || section.sectionMenu.length === 0) && (!section.subSections || section.subSections.length === 0)" class="text-muted p-2">
                                No items or sub-sections in this section.
                            </div>
                        </div>
                    </transition>
                </div>
            </template>
        </draggable>

        <!-- Add Section Button -->
        <div class="mt-3">
            <button class="btn btn-outline-primary w-100" @click="addSection">
                <i class="bi bi-plus-lg me-1"></i> Add New Section
            </button>
        </div>
    </div>
</template>

<script>
import draggable from 'vuedraggable';

const focus = {
  mounted: (el) => el.focus()
}

export default {
    name: 'VenueMenuEdit',
    components: {
        draggable,
    },
    directives: { focus },
    props: {
        menuData: {
            type: Array,
            required: true,
        },
    },
        emits: ['save', 'cancel', 'request-add-listing'],
    data() {
        return {
            localMenu: [],
        };
    },
    watch: {
        menuData: {
            handler(newValue) {
                this.localMenu = JSON.parse(JSON.stringify(newValue));
                this.localMenu.forEach(section => {
                    if (!section.subSections) {
                        section.subSections = [];
                    }
                    if (!section.sectionMenu) {
                        section.sectionMenu = [];
                    }
                    if (section.subSections) {
                        section.subSections.forEach(sub => {
                            sub.isExpanded = sub.isExpanded ?? false;
                            sub.isEditingName = sub.isEditingName ?? false;
                            if (!sub.sectionMenu) {
                                sub.sectionMenu = [];
                            }
                        });
                    }
                });
            },
            immediate: true,
            deep: true,
        },
    },
    methods: {
        onItemChange(event) {
            // This method is called whenever items are moved between draggable containers
            // Update item orders after a change
            console.log('Item moved:', event);
            
            // Update all item orders after any change
            this.updateAllItemOrders();
        },
        addSection() {
            const newSection = {
                id: `new_${Date.now()}`,
                sectionName: 'New Section',
                sectionOrder: this.localMenu.length,
                isExpanded: false,
                sectionMenu: [],
                subSections: [],
                isEditingName: true,
            };
            this.localMenu.push(newSection);
        },
        editSectionName(section) {
            section.isEditingName = true;
        },
        finishEditingName(section) {
            if (!section.sectionName || section.sectionName.trim() === '') {
                section.sectionName = 'Untitled Section';
            }
            section.isEditingName = false;
        },
        async toggleSection(section) {
            if (section.isEditingName) return;
            section.isExpanded = !section.isExpanded;
            if (section.isExpanded && (!section.sectionMenu || section.sectionMenu.length === 0)) {
                if (!String(section.id).startsWith('new_')) {
                    await this.loadAllSectionItems(section);
                }
            }
        },
        async loadAllSectionItems(section) {
            if (!section || !section.id || section.isLoading) return;
            section.isLoading = true;
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getVenueMenu/${section.id}`,
                    { params: { paginate: false } }
                );
                section.sectionMenu = response.data.data || [];
            } catch (error) {
                console.error(`Error loading all items for section ${section.id}:`, error);
                section.sectionMenu = [];
            } finally {
                section.isLoading = false;
            }
        },
        confirmDeleteSection(section, index) {
            if (window.confirm(`Are you sure you want to delete the section "${section.sectionName}"? This cannot be undone.`)) {
                this.localMenu.splice(index, 1);
                this.updateSectionOrder();
            }
        },
        moveToTop(list, itemIndex) {
            const [item] = list.splice(itemIndex, 1);
            list.unshift(item);
        },
        removeItem(list, itemIndex) {
            list.splice(itemIndex, 1);
        },
        addSubsection(section) {
            if (!section.subSections) {
                section.subSections = [];
            }
            const newSubSection = {
                id: `new_sub_${Date.now()}`,
                sectionName: 'New Sub-section',
                sectionOrder: section.subSections.length,
                isExpanded: false,
                sectionMenu: [],
                isEditingName: true,
            };
            section.subSections.push(newSubSection);
        },
        confirmDeleteSubSection(section, subSectionIndex) {
            const subsection = section.subSections[subSectionIndex];
            if (window.confirm(`Are you sure you want to delete the sub-section "${subsection.sectionName}"? This cannot be undone.`)) {
                section.subSections.splice(subSectionIndex, 1);
                this.updateSubSectionOrder(section);
            }
        },
        async toggleSubSection(subsection) {
            if (subsection.isEditingName) return;
            subsection.isExpanded = !subsection.isExpanded;
            if (subsection.isExpanded && (!subsection.sectionMenu || subsection.sectionMenu.length === 0)) {
                if (!String(subsection.id).startsWith('new_')) {
                    await this.loadAllSectionItems(subsection);
                }
            }
        },
                addListing(itemContainer) {
            this.$emit('request-add-listing', itemContainer);
        },
        updateSectionOrder() {
            this.localMenu.forEach((section, index) => {
                section.sectionOrder = index;
            });
            console.log('Section order updated:', this.localMenu.map(s => ({ name: s.sectionName, order: s.sectionOrder })));
        },
        updateSubSectionOrder(section) {
            if (section.subSections) {
                section.subSections.forEach((subSection, index) => {
                    subSection.sectionOrder = index;
                });
            }
        },
        updateItemOrder(itemList) {
            // Update order for items in a specific list
            if (itemList && itemList.length) {
                itemList.forEach((item, index) => {
                    item.itemOrder = index;
                });
            }
        },
        updateAllItemOrders() {
            // Update item orders for all sections and sub-sections
            this.localMenu.forEach(section => {
                // Update items in main section
                this.updateItemOrder(section.sectionMenu);
                
                // Update items in sub-sections
                if (section.subSections) {
                    section.subSections.forEach(subSection => {
                        this.updateItemOrder(subSection.sectionMenu);
                    });
                }
            });
        },
        saveChanges() {
            // Ensure all orders are up to date before saving
            this.updateSectionOrder();
            this.localMenu.forEach(section => {
                this.updateSubSectionOrder(section);
            });
            this.updateAllItemOrders();
            
            console.log('Final data being saved:', JSON.stringify(this.localMenu, null, 2));
            this.$emit('save', this.localMenu);
        },
    }
};
</script>

<style scoped>
.ghost {
    opacity: 0.5;
    background: #c8ebfb;
}
.drag-handle, .drag-handle-item, .drag-handle-subsection {
    cursor: grab;
}
.listing-edit-item {
    background-color: #fff;
    border: 1px solid #eee;
    border-radius: 4px;
}
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

.empty-drop-zone {
    min-height: 60px;
}
</style>