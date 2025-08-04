<template>
    <div>
        <!-- If venue is unclaimed, show lock message  bg-light-->
        <div v-if="!claimStatus" class="text-center p-4 rounded" style="background-color: rgb(221, 200, 169);">
            <p class="fs-5 fw-bold">Do you own this business?</p>
            <p>Sign up for a venue account to share your bar's menu with your fans!</p>
            <button class="btn btn-warning fw-bold">Claim This Business</button>
        </div>

        <!-- If venue is claimed, show the menu -->
        <div v-else>
            <!-- Menu Controls: Search, Sort, Edit Buttons -->
            <!-- This should be its own component: MenuControls.vue -->
            <div class="d-flex justify-content-between align-items-center mb-3">
                <p class="fs-5 fw-bold m-0">{{ loadedListings.length }} Drinks On The Menu</p>
                <div v-if="isSelfView" class="d-flex gap-2">
                    <button class="btn btn-outline-primary">Edit Menu</button>
                    <button class="btn btn-outline-secondary">Share Menu</button>
                </div>
            </div>
            <!-- End of potential MenuControls.vue -->

            <!-- Menu Sections -->
            <div v-if="menu && menu.length > 0">
                <!-- Each section here should be a component: MenuSection.vue -->
                <div v-for="(section, index) in menu" :key="index" class="mb-4">
                    <h4 class="text-start bg-light p-2 rounded">{{ section.sectionName }}</h4>
                    <!-- Then inside MenuSection.vue, you would loop through items -->
                    <!-- and each item would be a MenuItem.vue component -->
                    <div v-if="section.sectionMenu.length > 0">
                        <p>Menu items for {{ section.sectionName }} go here.</p>
                    </div>
                    <div v-else>
                        <p class="fst-italic text-muted">No items in this section.</p>
                    </div>
                </div>
            </div>
            <div v-else>
                <p class="fst-italic text-muted">No menu has been created yet. Stay tuned!</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'VenueMenuTab',
    props: {
        menu: Array,
        isSelfView: Boolean,
        claimStatus: Boolean,
        loadedListings: Array,
    }
}
</script>