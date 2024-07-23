<!-- Component for drinks display. Used in all profile pages. -->

<template>
    <h3 class="text-body-secondary text-start pt-1"> 
        <b> {{ displayName }} </b> 
    </h3>
    <div class="container pe-lg-0">
        <div class="row" v-if="Object.keys(listingArr).length > 0">
            <div v-for="(listing, index) in listingArr" :key="index" class="col-12 col-sm-6 col-md-6 col-lg-3 col-xl-2 align-items-center p-lg-0" :style="{ display: 'flex', flexDirection: 'column', width: columnWidth }">
                <div class="drink-photo-container-row image-container-150">
                    <router-link :to="{ path: '/listing/view/' + listing._id.$oid }" class="default-text-no-background">
                        <img v-if="listing.photo !== '' && listing.photo !== null" :src="'data:image/jpeg;base64,' + listing.photo" class="add-drink-photo-background centered rounded"> 
                        <!-- <img v-if="listing.photo !== '' && listing.photo !== null" :src="listing.photo" class="add-drink-photo-background centered rounded">  -->
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

</template>

<script>
import BookmarkIcon from '@/components/BookmarkIcon.vue';

    export default {
        name: "ListingRowDisplay",
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