<!-- Component for drinks display. Used in all profile pages. -->

<template>
    <h5 class="text-body-secondary text-start pt-1 mb-3"> 
        <b> {{ displayName }} </b> 
    </h5>
    <div class="container pe-lg-0 mobile-ps-0 mobile-pe-0 mobile-view-hide">
        <div class="d-flex justify-content-between flex-row w-100" v-if="listingArr.length > 0" style="flex-wrap: nowrap;">
        <div v-for="(listing, index) in listingArr.filter(l => l?.id)" :key="index" class="d-flex flex-column align-items-center" style="flex: 0 0 19%; max-width: 19%;">
                   <div class="drink-photo-container-row image-container-150 mb-2" v-if="listing?.id">
                    <router-link :to="{ path: '/listing/view/' + slugify(listing.listingName) + '/' + listing.id }" class="default-text-no-background">
                        <img v-if="listing.photo !== '' && listing.photo !== null" :src="listing.photo" class="add-drink-photo-background centered rounded"> 
                        <img v-else src="https://drinkximages.s3.us-east-1.amazonaws.com/images/2d4d94bc-313e-4621-9a15-4bfbf77958de.jpg" class="add-drink-photo-background centered rounded">
                    </router-link>
                    
                    <BookmarkIcon 
                        v-if="user && Object.keys(user).length > 0" 
                        :user="user" 
                        :listing="listing" 
                        :overlay="true"
                        size="20"
                        @icon-clicked="handleIconClick" />

                </div>
                <router-link :to="{ path: '/listing/view/' + slugify(listing.listingName) + '/' + listing.id }" class="default-clickable-text scrollable mt-2 mb-3" style="text-align: center; max-height: 75px;" v-if="listing?.id">
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
        <div v-if="listingArr.length > 0">
          
          <div class="mobile-scroll-row">
            
            <div v-for="(listing, index) in listingArr.filter(l => l?.id)" 
                 :key="index" 
                 class="scroll-item">
      
              <!-- Image + BookmarkIcon block -->
              <div class="drink-photo-container-row-producer-profile image-container-150">
                
                <router-link 
                  :to="{ path: '/listing/view/' + slugify(listing.listingName) + '/' + listing.id }" 
                  class="default-text-no-background">
      
                  <img v-if="listing.photo !== '' && listing.photo !== null" 
                       :src="'data:image/jpeg;base64,' + listing.photo" 
                       class="add-drink-photo-background centered rounded review-image">
      
                  <img v-else 
                       src="../../Images/Drinks/Placeholder.png" 
                       class="add-drink-photo-background centered rounded review-image">
                
                </router-link>
      
                <BookmarkIcon 
                  v-if="user && Object.keys(user).length > 0" 
                  :user="user" 
                  :listing="listing" 
                  :overlay="true"
                  size="20"
                  @icon-clicked="handleIconClick" />
      
              </div>
      
              <!-- Listing Name block -->
              <router-link 
                :to="{ path: '/listing/view/' + slugify(listing.listingName) + '/' + listing.id }" 
                class="default-clickable-text mobile-rating-smaller-text-2 scrollable mt-2" 
                style="text-align: center; max-height: 75px;">
      
                <div v-if="listing.listingName.length > 25"> <!--kai edited to truncate text earlier-->
                  {{ listing.listingName.slice(0, 25) + '...' }}
                </div>
                <div v-else>
                  {{ listing.listingName }}
                </div>
      
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
            slugify(text) {
                return text
                    .toString()
                    .toLowerCase()
                    .replace(/['’]/g, '')
                    .replace(/[^\w\s-]/g, '')
                    .trim()
                    .replace(/\s+/g, '-')
                    .replace(/-+/g, '-')
            },
            handleIconClick(data) {
                this.$emit('icon-clicked', data);
            },

        }
    }
</script>