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
                <button class="btn btn-primary" @click="$emit('save', localMenu)">
                    <i class="bi bi-check-lg me-1"></i>Save Changes
                </button>
            </div>
        </div>

        <!-- Instructions -->
        <div class="alert alert-info d-flex align-items-center" role="alert">
            <i class="bi bi-info-circle-fill me-3 fs-4"></i>
            <div>
                Drag and drop sections to reorder them. Click a section to expand and manage its listings.
            </div>
        </div>

        <!-- Draggable Sections -->
        <draggable v-model="localMenu" item-key="id" handle=".drag-handle" ghost-class="ghost">
            <template #item="{ element: section, index }">
                <div class="mb-2">
                    <div class="d-flex justify-content-between align-items-center py-2 px-3 rounded"
                        style="background-color: #e9ecef; cursor: default;">
                        <div class="d-flex align-items-center">
                            <i class="bi bi-grip-vertical drag-handle me-2" style="cursor: grab;"></i>
                            <h6 class="mb-0 fw-semibold text-dark" @click="toggleSection(section)" style="cursor: pointer;">
                                {{ section.sectionName }}
                            </h6>
                            <i :class="['bi', 'ms-2', section.isExpanded ? 'bi-chevron-up' : 'bi-chevron-down']"
                                style="font-size: 12px; cursor: pointer;" @click="toggleSection(section)"></i>
                        </div>
                        <button class="btn btn-sm btn-outline-danger" @click="confirmDeleteSection(section, index)">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>

                    <!-- Listings within section -->
                    <transition name="slide">
                        <div v-if="section.isExpanded" class="p-3 bg-white border border-top-0 rounded-bottom">
                            <!-- Loading state -->
                            <div v-if="section.isLoading" class="text-center p-4">
                                <div class="spinner-border spinner-border-sm me-2" role="status"></div>
                                Loading all items...
                            </div>
                            <!-- Draggable Listings -->
                            <draggable v-else-if="section.sectionMenu && section.sectionMenu.length" v-model="section.sectionMenu" item-key="itemID" handle=".drag-handle-item" ghost-class="ghost">
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
                            <div v-else class="text-muted p-2">No items in this section.</div>
                        </div>
                    </transition>
                </div>
            </template>
        </draggable>
    </div>
</template>

<script>
import draggable from 'vuedraggable';

export default {
    name: 'VenueMenuEdit',
    components: {
        draggable,
    },
    props: {
        menuData: {
            type: Array,
            required: true,
        },
    },
    emits: ['save', 'cancel'],
    data() {
        return {
            localMenu: [],
        };
    },
    watch: {
        menuData: {
            handler(newValue) {
                this.localMenu = JSON.parse(JSON.stringify(newValue));
            },
            immediate: true,
            deep: true,
        },
    },
    methods: {
        async toggleSection(section) {
            section.isExpanded = !section.isExpanded;
            if (section.isExpanded && (!section.sectionMenu || section.sectionMenu.length === 0)) {
                await this.loadAllSectionItems(section);
            }
        },
        async loadAllSectionItems(section) {
            if (!section || !section.id || section.isLoading) return;
            section.isLoading = true;
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getVenueMenu/${section.id}`,
                    { params: { paginate: false } } // Load all items
                );
                section.sectionMenu = response.data.data || [];
            } catch (error) {
                console.error(`Error loading all items for section ${section.id}:`, error);
                section.sectionMenu = [];
                // Optionally, show an error message to the user
            } finally {
                section.isLoading = false;
            }
        },
        confirmDeleteSection(section, index) {
            if (window.confirm(`Are you sure you want to delete the section "${section.sectionName}"? This cannot be undone.`)) {
                this.localMenu.splice(index, 1);
            }
        },
        moveToTop(list, itemIndex) {
            const [item] = list.splice(itemIndex, 1);
            list.unshift(item);
        },
        removeItem(list, itemIndex) {
            list.splice(itemIndex, 1);
        }
    }
};
</script>

<style scoped>
.ghost {
    opacity: 0.5;
    background: #c8ebfb;
}
.drag-handle, .drag-handle-item {
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
</style>
