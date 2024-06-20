<!-- Component for drinks display. Used in all profile pages. -->

<template>
    <h5 class="text-body-secondary text-start pt-1"> 
        <b> {{ displayName }} </b> 
    </h5>
    <div class="container pe-lg-0 mobile-ps-0 mobile-pe-0 mobile-view-hide">
        <div class="row" v-if="Object.keys(listingArr).length > 0">
            <div v-for="(listing, index) in listingArr" :key="index" class="col-12 col-sm-6 col-md-6 col-lg-3 col-xl-2 align-items-center p-lg-0" :style="{ display: 'flex', flexDirection: 'column', width: columnWidth }">
                <div class="drink-photo-container-row image-container-150">
                    <router-link :to="{ path: '/listing/view/' + listing._id.$oid }" class="default-text-no-background">
                        <img v-if="listing.photo !== '' && listing.photo !== null" :src="'data:image/jpeg;base64,' + listing.photo" class="add-drink-photo-background centered rounded"> 
                        <img v-else src="../../Images/Drinks/Placeholder.png" class="add-drink-photo-background centered rounded">
                    </router-link>
                    
                    <BookmarkIcon 
                        v-if="user && Object.keys(user).length > 0" 
                        :user="user" 
                        :listing="listing" 
                        :overlay="true"
                        size="20"
                        @icon-clicked="handleIconClick" />

                </div>
                <router-link :to="{ path: '/listing/view/' +listing._id.$oid }" class="default-clickable-text scrollable mt-2 " style="text-align: center; max-height: 75px;">
                    <div v-if="listing.listingName.length > 63"> 
                        {{ listing.listingName.slice(0,63) + (listing.listingName.length > 63 ? '...' : '') }}
                    </div>
                    <div v-else> 
                        {{ listing.listingName }}
                    </div>    
                </router-link>
            </div>
        </div>
        <div v-else class="m-2 text-start">
            No {{ displayName.toLowerCase() }} yet. To explore more drinks in the home page, 
            <router-link to="/" style="color: inherit;">click here</router-link>. 
        </div>
    </div>

    <div class="container pe-lg-0 mobile-ps-0 mobile-pe-0 mobile-view-show">
        <div  v-if="Object.keys(listingArr).length > 0" >
            <div class="row d-flex flex-nowrap" style="overflow-x: auto;">
            <div v-for="(listing, index) in listingArr" :key="index" class="col-12 col-sm-6 col-md-6 col-lg-3 col-xl-2 align-items-center p-lg-0 me-4 mobile-col-4 mobile-me-0 mobile-ps-1 mobile-pe-1 mobile-fs-7" :style="{ display: 'flex', flexDirection: 'column' }">
                <div class="drink-photo-container-row-producer-profile image-container-150">
                    <router-link :to="{ path: '/listing/view/' + listing._id.$oid }" class="default-text-no-background">
                        <img v-if="listing.photo !== '' && listing.photo !== null" :src="'data:image/jpeg;base64,' + listing.photo" class="add-drink-photo-background centered rounded review-image"> 
                        <img v-else src="../../Images/Drinks/Placeholder.png" class="add-drink-photo-background centered rounded review-image">
                    </router-link>
                    
                    <BookmarkIcon 
                        v-if="user && Object.keys(user).length > 0" 
                        :user="user" 
                        :listing="listing" 
                        :overlay="true"
                        size="20"
                        @icon-clicked="handleIconClick" />

                </div>
                <router-link :to="{ path: '/listing/view/' +listing._id.$oid }" class="default-clickable-text scrollable mt-2 " style="text-align: center; max-height: 75px;">
                    <div v-if="listing.listingName.length > 63"> 
                        {{ listing.listingName.slice(0,63) + (listing.listingName.length > 63 ? '...' : '') }}
                    </div>
                    <div v-else> 
                        {{ listing.listingName }}
                    </div>    
                </router-link>
            </div>
            </div>
            <p style="font-weight:bold; font-size:0.75rem; text-align: right;">View more ⟶</p>
        </div>
        
        <div v-else class="m-2 text-start">
            No {{ displayName.toLowerCase() }} yet. To explore more drinks in the home page, 
            <router-link to="/" style="color: inherit;">click here</router-link>. 
        </div>
        
    </div>

</template>

<script>
import BookmarkIcon from '@/components/BookmarkIcon.vue';

    export default {
        name: "ListingRowDisplayProducerProfile",
        components: {
            BookmarkIcon,
            // BookmarkModal,
        },
        props: {
            displayName: String,
            listingArr: Array,
            user: Object,
            listing: Object,
            columnWidth: {
                type: String,
                default: '195px'
            }
},
        methods: {
            handleIconClick(data) {
                this.$emit('icon-clicked', data);
            },

        }
    }
</script>