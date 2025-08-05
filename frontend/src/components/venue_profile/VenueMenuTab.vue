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
                <p class="fs-5 fw-bold m-0">{{ (menu && menu.length) || 0 }} Drinks On The Menu</p>
                <div v-if="isSelfView" class="d-flex gap-2">
                    <button class="btn btn-outline-primary">Edit Menu</button>
                    <button class="btn btn-outline-secondary">Share Menu</button>
                </div>
            </div>

            <!-- Menu Sections -->
            <div v-if="menu && menu.length > 0">
                <div v-for="(section, index) in menu" :key="index" class="mb-2">
                    <!-- Clickable Section Header @click="section.isExpanded = !section.isExpanded" -->
                    <div class="d-flex justify-content-between align-items-center py-2 px-3 rounded"
                        style="background-color: #f0b258; cursor: pointer; user-select: none;"
                        @click="toggleSection(section, index)">
                        <div class="d-flex align-items-center">
                            <h6 class="mb-0 fw-semibold text-dark">{{ section.sectionName }}</h6>
                            <i :class="['bi', 'ms-2', section.isExpanded ? 'bi-chevron-up' : 'bi-chevron-down']"
                                style="font-size: 12px;"></i>
                        </div>
                    </div>

                    <!-- Smooth Slide Transition -->
                    <transition name="slide">
                        <div v-show="section.isExpanded">
                            <!-- Loading state -->
                            <div v-if="section.isLoading" class="text-center p-4 bg-white border border-top-0">
                                <div class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true">
                                </div>
                                Loading menu items...
                            </div>

                            <!-- Menu Items -->
                            <div v-else-if="section.sectionMenu && section.sectionMenu.length > 0" class="bg-white">
                                <div v-for="(item, itemIndex) in section.sectionMenu" :key="itemIndex"
                                    class="py-2 px-3 border-bottom">

                                    <router-link
                                        :to="{ path: '/listing/view/' + item.itemID + '/' + item.name }"
                                        class="listing-item-link text-decoration-none"
                                    >
                                        <div class="card mb-3 listing-card border-0 shadow-sm">
                                        <div class="card-body p-3">
                                            <div class="d-flex align-items-start">
                                            <!-- Item Image -->
                                            <div class="flex-shrink-0 me-3">
                                                <div class="image-wrapper d-flex align-items-center justify-content-center rounded-2"
                                                    style="width: 80px; height: 80px; background-color: #f8f6f0;">
                                                <img v-if="item.photo && item.photo.trim() !== ''" 
                                                    :src="item.photo" 
                                                    :alt="item.name"
                                                    class="img-fluid rounded"
                                                    style="max-width: 70px; max-height: 70px; object-fit: contain;">
                                                <!-- Fallback Icon -->
                                                <i v-else class="bi bi-cup-straw" style="font-size: 28px; color: #d4941e;"></i>
                                                </div>  
                                            </div>

                                            <!-- Item Details -->
                                            <div class="flex-grow-1" style="min-width: 0;">
                                                <div class="d-flex justify-content-between align-items-start mb-1">
                                                    <h5 class="card-title fw-semibold mb-0 me-2 item-title">{{ item.name }}</h5>
                                                    <!-- Star icon -->
                                                    <i class="bi bi-star text-warning flex-shrink-0"></i>
                                                </div>
                                                
                                                <p class="card-text text-muted small mb-2 lh-sm text-start">{{ item.description }}</p>
                                                <p class="card-text fw-medium mb-0 text-start">{{ item.itemPrice }} / {{ item.servingType }}</p>
                                            </div>
                                            </div>
                                        </div>
                                        </div>
                                    </router-link>
                                    
                                    <!-- pagination -->
                                    <div v-if="section.pagination && section.pagination.total_pages > 1" class="p-2 bg-light">
                                        <button 
                                            class="btn btn-sm btn-outline-secondary me-1"
                                            :disabled="section.pagination.page <= 1"
                                            @click="loadSectionMenu(section, index, section.pagination.page - 1)"
                                        >Previous</button>

                                        <span>Page {{ section.pagination.page }} of {{ section.pagination.total_pages }}</span>

                                        <button 
                                            class="btn btn-sm btn-outline-secondary ms-1"
                                            :disabled="section.pagination.page >= section.pagination.total_pages"
                                            @click="loadSectionMenu(section, index, section.pagination.page + 1)"
                                        >Next</button>
                                    </div>
                                </div>

                            </div>

                            <!-- No items -->
                            <div v-else class="py-2 px-3 text-muted small">No items in this section.</div>
                        </div>
                    </transition>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        claimStatus: Boolean,
        isSelfView: Boolean,
        menu: Array
    },
    mounted() {
        // Ensure isExpanded exists for reactivity
        if (this.menu && this.menu.length > 0) {
            this.menu.forEach(section => {
                if (section.isExpanded === undefined) {
                    this.$set(section, 'isExpanded', false);
                }
            });
        }
    },
    methods: {
        async toggleSection(section, index) {
            // Toggle the expanded state
            section.isExpanded = !section.isExpanded;

            // If expanding and no menu items loaded yet, fetch them
            if (section.isExpanded && (!section.sectionMenu || section.sectionMenu.length === 0)) {
                await this.loadSectionMenu(section, index);
            }
        },

        async loadSectionMenu(section, index, page = 1, limit = 10) {
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
                        params: { page, limit }, // pagination params
                        timeout: 10000,
                        headers: { 'Accept': 'application/json' }
                    }
                );

                if (!response.data) throw new Error('Invalid response format');

                // Extract from backend response
                const items = response.data.data || [];
                const pagination = response.data.pagination || { page, limit, total_pages: 1 };

                // Store in section so it’s reactive
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

        async retryLoadSection(section, index) {
            await this.loadSectionMenu(section, index);
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
    max-height: 500px;
    /* adjust to your expected max */
    opacity: 1;
}
</style>
