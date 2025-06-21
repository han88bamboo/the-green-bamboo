<template>
<div class="d-flex justify-content-between align-items-start flex-wrap px-3">
    <div class="card p-0 mobile-view-hide" style="width: 200px; height:400px">
        <img :src="photoURL" class="card-img-top" alt="listing image" style="height: 200px;" />
        <div class="card-body d-flex flex-column p-3">

            <!-- Listing Name -->
            <router-link
                :to="{
                path: '/listing/view/' + listing.listingID + '/' + slugify(listing.listingName),
                }"
                class="primary-clickable-text text-decoration-none"
                style="color: #027562"
            >
                <h6 class="card-title fw-bold text-start">{{ listing.listingName.slice(0, 40) }}</h6>
            </router-link>
            
        

            <!-- Producer Name -->
            <router-link
                :to="{
                path:
                    '/profile/producer/' +
                    listing.producerID +
                    '/' +
                    listing.producerName,
                }"
                class="primary-clickable-text"
            >
                 <p class="card-text fw-bold">{{ listing.producerName.slice(0, 40) }}</p>
            </router-link>
           

            <!--Rating-->
            <div class="text-center gap-2  mt-auto">
                <h4 class="fw-bold text-warning">
                    <span v-if="listing.averageRating == null || listing.averageRating == ''">
                        --
                    </span>
                    <span v-else>
                        {{ listing.averageRating }}
                    </span>
                    ★
                </h4>
            </div>
            

            <!--Read more button-->
            <router-link
                :to="{
                path: '/listing/view/' + listing.listingID + '/' + slugify(listing.listingName),
                }"
                class="primary-clickable-text text-center mt-auto"
            >
                <button class="btn btn-read-more btn-sm fw-bold">
                    Read More
                </button>
            </router-link>
        </div>
    </div>


    <div class="card d-flex flex-row p-0 mobile-view-show mb-3" style="width:300px;height:100px">

        <img :src="photoURL" class="image-wrapper position-relative d-inline-block" alt="listing image" style="width: 100px;" />
        <div class="flex-md-row justify-content-between">

            <div class="flex-grow-1 col-12 d-flex flex-column justify-content-between px-3 pt-2 ">
            <!-- Listing Name -->
            <router-link
                :to="{
                path: '/listing/view/' + listing.listingID + '/' + slugify(listing.listingName),
                }"
                class="primary-clickable-text text-decoration-none"
                style="color: #027562"
            >
                <p class="mobile-rating-smaller-text-2 fw-bold text-start mb-1">{{ listing.listingName.slice(0, 22) }}</p>
            </router-link>
            </div>
            
            <div class="flex-grow-1 col-12 d-flex flex-column justify-content-between px-3 pt-0">
            <!-- Producer Name -->
            <router-link
                :to="{
                path:
                    '/profile/producer/' +
                    listing.producerID +
                    '/' +
                    listing.producerName,
                }"
                class="mobile-rating-smaller-text-2 primary-clickable-text"
            >
                 <p class="card-text fw-bold">{{ listing.producerName.slice(0, 20) }}</p>
            </router-link>
            </div>

            <div class="col-12 d-flex flex-column justify-content-between px-3 mt-2">
            <!--Rating-->
            <div class="text-start">
                <h4 class="fw-bold text-warning">
                    <span v-if="listing.averageRating == null || listing.averageRating == ''">
                        --
                    </span>
                    <span v-else>
                        {{ listing.averageRating }}
                    </span>
                    ★
                </h4>
            </div>
            </div>

            
        </div>
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
                "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",
        }
    },
    computed: {
        // Set the photo URL to the default photo if it doesn't exist
        photoURL() {
            return (this.listing.photo != "" && this.listing.photo != null) ? this.listing.photoURL : this.defaultPhoto;
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