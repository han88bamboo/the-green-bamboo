<!-- Component for drinks display. Used in all profile pages. -->

<template>
    <h5 class="text-body-secondary text-start pt-1"> 
        <b> {{ displayName }} </b> 
    </h5>
    <div class=""> <!-- container pe-lg-0-->
        <div v-if="listingArr.length > 0">
        <div v-for="(listing, index) in listingArr" :key="index"  class="row mb-3" :style="{ display: 'flex' }" > <!--    , flexDirection: 'column' , width: columnWidth -->
            <div class="col-3 mobile-col-3 mobile-pe-0" v-if="listing?.id"> <!-- col-12 col-sm-6 col-md-6 col-lg-3 col-xl-2 align-items-center p-lg-0 me-4    -->
                <div class="Xdrink-photo-container-row Ximage-container-150">
                    <router-link :to="{ path: '/listing/view/' + listing.id }" class="default-text-no-background">
                        <img v-if="listing.photo !== '' && listing.photo !== null" :src="listing.photo" class="add-drink-photo-background-user-profile centered rounded"> 
                        <img v-else src="https://drinkximages.s3.us-east-1.amazonaws.com/images/2d4d94bc-313e-4621-9a15-4bfbf77958de.jpg" class="add-drink-photo-background-user-profile centered rounded">
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
            <div class="col-9 mobile-col-9 mobile-ps-2" v-if="listing?.id">
                <router-link :to="{ path: '/listing/view/' +listing.id }" class="default-clickable-text scrollable mt-2 mobile-fs-7" style="text-decoration: none">
                    <p v-if="listing.listingName.length > 63" class="fs-5 mobile-fs-6 mb-1" > 
                        <b>{{ listing.listingName.slice(0,63) + (listing.listingName.length > 63 ? '...' : '') }}</b>
                    </p>
                    <p v-else class="fs-5 mobile-fs-6 mb-1" > 
                        <b>{{ listing.listingName }}</b>
                    </p>    
                </router-link>
                <p class="mobile-fs-7 mb-1" style="font-weight:bold; color: #2a6959;">
                    {{ 
                        listing.producerName?.length > 40
                          ? listing.producerName.slice(0, 40) + '...'
                          : listing.producerName || 'Unknown Producer'
                      }}
                </p>
                <p class="mobile-fs-7 mb-0" style="color: #333">
                    {{
                      listing.officialDesc?.length > 100
                        ? listing.officialDesc.slice(0, 100) + "..."
                        : listing.officialDesc
                    }}
                  </p>
                                  
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
        // user: Object,
        // listing: Object,
        columnWidth: {
          type: String,
          default: '195px'
        },
    producers: {
      type: Array,
      default: () => []
    }
        
      },
      methods: {
    getProducerName(listing) {
      if (!this.producers || !listing.producerID) {
        console.log('Producers or producerID is missing:', this.producers, listing.producerID);
        return null;
      }
      const producer = this.producers.find(
        (producer) => producer.id === listing.producerID
      );
      console.log('Matching producer:', producer); // Debug log
      return producer ? producer.producerName : null;
    },
  },    
    }
    </script>
    