<template>
    <div class="card" style="width: 18rem;">
        <img :src="photoURL" class="card-img-top" alt="listing image" />
        <div class="card-body">
            <h5 class="card-title">{{ listing.listingName }}</h5>
            <p class="card-text">{{ listing.producerName }}</p>

            <!--Rating-->
            {{ listing.rating }}
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
            </svg>

            <!--Read more button-->
            <router-link
                :to="{
                path: '/listing/view/' + listing.listingID + '/' + slugify(listing.listingName),
                }"
                class="primary-clickable-text"
            >
                <button class="btn btn-read-more btn-sm fw-bold rounded-pill mobile-pb-1 mobile-pt-1 mobile-mb-2 mobile-fs-7">
                    Read More
                </button>
            </router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: 'BestOfCard',
    props: {
        listing: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            defaultPhoto:
                "https://drinkximages.s3.us-east-1.amazonaws.com/images/2d4d94bc-313e-4621-9a15-4bfbf77958de.jpg",
        }
    },
    computed: {
        // Set the photo URL to the default photo if it doesn't exist
        photoURL() {
            return (this.listing.photo != "" || this.listing.photo) ? this.listing.photoURL : this.defaultPhoto;
        }
    },
    methods: {
        //remove %20 from url
        slugify(text) {
            if (!text) return "";
            return text
                .toString()
                .toLowerCase()
                .replace(/\s+/g, '')
                .replace(/[^\w]/g, '');
        },
    }
}
</script>