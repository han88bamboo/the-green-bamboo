<!-- Component for drinks display. Used in all profile pages. -->

<template>
    <h3 class="text-body-secondary text-start pt-1"> 
        <b> {{ displayName }} </b> 
    </h3>
    <div class=""> <!-- container pe-lg-0-->
        <div v-if="Object.keys(listingArr).length > 0">
        <div v-for="(listing, index) in listingArr" :key="index"  class="row mb-3" :style="{ display: 'flex' }" > <!--    , flexDirection: 'column' , width: columnWidth -->
            <div class="col-3 mobile-col-4 mobile-pe-0" > <!-- col-12 col-sm-6 col-md-6 col-lg-3 col-xl-2 align-items-center p-lg-0 me-4    -->
                <div class="Xdrink-photo-container-row Ximage-container-150">
                    <router-link :to="{ path: '/listing/view/' + listing._id.$oid }" class="default-text-no-background">
                        <img v-if="listing.photo !== '' && listing.photo !== null" :src="'data:image/jpeg;base64,' + listing.photo" class="add-drink-photo-background-user-profile centered rounded"> 
                        <img v-else src="../../Images/Drinks/Placeholder.png" class="add-drink-photo-background-user-profile centered rounded">
                    </router-link>
                    
                    <!--<BookmarkIcon 
                        v-if="user && Object.keys(user).length > 0" 
                        :user="user" 
                        :listing="listing" 
                        :overlay="true"
                        size="20"
                        @icon-clicked="handleIconClick" />-->

                </div>

            </div>
            <div class="col-9 mobile-col-8 mobile-ps-1" >
                <router-link :to="{ path: '/listing/view/' +listing._id.$oid }" class="default-clickable-text scrollable mt-2 " style="text-decoration: none; color: rgb(34, 57, 87);">
                    <p v-if="listing.listingName.length > 63" class="fs-5 mobile-fs-6 mb-1" > 
                        <b>{{ listing.listingName.slice(0,63) + (listing.listingName.length > 63 ? '...' : '') }}</b>
                    </p>
                    <p v-else class="fs-5 mobile-fs-6 mb-1" > 
                        <b>{{ listing.listingName }}</b>
                    </p>    
                </router-link>                
            </div>
        </div>
        </div>
        <div v-else class="m-2 text-start">
            No {{ displayName.toLowerCase() }} yet. To explore more drinks in the home page, 
            <router-link to="/" style="color: inherit;">click here</router-link>. 
        </div>
    </div>

</template>

<script>
/*import BookmarkIcon from '@/components/BookmarkIcon.vue';*/

    export default {
        name: "ListingRowDisplay",
         /*components: {
            BookmarkIcon,
            // BookmarkModal,
        },*/
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