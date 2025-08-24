<!-- src/components/dashboard/LeaderboardColumn.vue -->
<template>
    <div class="col-12 col-md-4 mb-2 mt-2">
        <div class="position-relative d-flex flex-column leaderboard-height">
            <div class="d-flex flex-column align-items-center text-center mt-2 pb-2 border-bottom border-warning">
                <h6 class="fw-bold">{{ title }} {{ emoji }}</h6>
            </div>

            <div v-if="items.length === 0" class="text-center my-2 small mobile-rating-smaller-text-2 d-flex align-items-center justify-content-center">
                {{ placeholder }}
            </div>
            <div v-else class="d-flex flex-column flex-grow-1">
                <div class="overflow-auto">
                    <div v-for="item in items" :key="item.id" class="d-flex align-items-center mt-2">

                        <router-link :to="listingUrl(item)" class="d-flex align-items-center default-clickable-text text-decoration-none mb-3">
                            <!-- Image on the left -->
                            <div class="me-3 image-container">
                                <img :src="item.image || defaultDrinkImage" alt="Drink image" class="drink-image" />
                            </div>

                            <!-- Text content on the right -->
                            <div class="flex-grow-1 text-start">
                                <!-- Name on top -->
                                <div class="fw-bold text-decoration-underline">{{ item.name }}</div>
                                
                                <!-- Bottler at the bottom -->
                                <small class="d-block mobile-rating-smaller-text-2">{{ item.bottler }}</small>
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>

            <div class="d-flex justify-content-center mt-auto pt-2">
                <button
                    class="btn btn-light rounded-circle d-flex align-items-center justify-content-center add-btn"
                    @click="$emit('add-item')"
                >
                    +
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'LeaderboardColumn',
    props: {
        title: String,
        emoji: String,
        items: Array,
        placeholder: String,
    },
    data() {
        return {
            defaultDrinkImage: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739'
        }
    },
    methods: {
        listingUrl(item) {
            // Use optional chaining (?.) to safely access properties that might not exist.
            // Use the OR operator (||) to provide a fallback empty string for the name.
            const name = item?.name || '';
            const id = item?.id;

            // If we don't have an ID or a name, we can't build a valid link.
            // Return a '#' to make the link non-functional but prevent errors.
            if (!id || !name) {
                return '#';
            }
            // https://drink-x.com/listing/view/779737/CooleyHennessyNaGeanna
            // path: '/listing/view/' + activity.reviewTarget + '/' + slugify(activity.listingName) 

            // Now that we know 'name' is a string, .toLowerCase() is always safe.
            const slug = name.toLowerCase().replace(/ /g, '-'); // Added space-to-dash replacement for cleaner URLs
            return `/listing/view/${id}/${slug}`;
        }
    }
}
</script>

<style scoped>
.leaderboard-height { 
    height: 280px; /* Fixed height instead of min-height */
}

.image-container {
    flex-shrink: 0; /* Prevents the image container from shrinking */
    width: 30px; /* Or your desired width */
    height: 30px; /* Or your desired height */
}
.drink-image {
    width: 100%;
    height: 100%;
    object-fit: cover; /* Ensures the image covers the area without distortion */
    border-radius: 4px; /* Optional: adds rounded corners */
}
.add-btn {
    width: 36px;
    height: 36px;
    font-size: 1.5rem;
    font-weight: 300;
    border: none;
    background-color: #F4B754;
    color: white;
}

@media (min-width: 768px) {
    .leaderboard-height { 
        height: 350px; /* Larger for desktop */
    }
}
</style>