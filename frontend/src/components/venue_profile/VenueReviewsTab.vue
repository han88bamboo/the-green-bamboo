<template>
    <div>
        <!-- Average Rating and Photo Gallery -->
        <!-- This could be a ReviewGallery.vue component -->
        <div class="mb-4">
            <h4 class="text-start fs-4 fw-bold">
                Average Venue Rating: {{ averageRating }} <span style="color: #f0b358">★</span>
            </h4>
            <div class="d-flex gap-2 mt-2">
                <!-- Logic for displaying review images -->
            </div>
        </div>
        <!-- End of potential ReviewGallery.vue -->

        <hr>

        <!-- Venue Reviews List -->
        <h5 class="text-start fw-bold">Venue Reviews</h5>
        <div v-if="venueReviews && venueReviews.length > 0">
            <!-- Each review should be a component: ReviewCard.vue -->
            <div v-for="review in venueReviews" :key="review.id" class="border-bottom py-3">
                <p><strong>@{{ review.username }}</strong> rated it {{ review.rating }} ★</p>
                <p>{{ review.reviewDesc }}</p>
                <!-- Voting and edit/delete logic would go here -->
            </div>
        </div>
        <div v-else>
            <p class="fst-italic text-muted">No venue reviews yet.</p>
        </div>

        <!-- Bottle Reviews List -->
        <h5 class="text-start fw-bold mt-4">Reviews of Drinks Tasted Here</h5>
        <div v-if="bottleReviews && bottleReviews.length > 0">
            <!-- This would also use the ReviewCard.vue component, with different props -->
            <div v-for="review in bottleReviews" :key="review.id" class="border-bottom py-3">
                 <p><strong>@{{ review.username }}</strong> rated <strong>{{ review.bottleName }}</strong> {{ review.rating }} ★</p>
                <p>{{ review.reviewDesc }}</p>
            </div>
        </div>
        <div v-else>
            <p class="fst-italic text-muted">No drink reviews have been tagged at this venue yet.</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'VenueReviewsTab',
    props: {
        venueReviews: Array,
        bottleReviews: Array,
        userId: [String, Number],
        canMod: Boolean,
    },
    computed: {
        averageRating() {
            if (!this.venueReviews || this.venueReviews.length === 0) return 'N/A';
            const total = this.venueReviews.reduce((acc, review) => acc + review.rating, 0);
            return (total / this.venueReviews.length).toFixed(1);
        }
    }
}
</script>