<template>
  <!-- Amenities Section -->
  <div v-if="amenityBadges.length > 0" class="mt-3">
    <h6 class="fw-bold mb-2">Amenities & Features</h6>
    <div class="d-flex flex-wrap gap-1">
      <span 
        v-for="amenity in amenityBadges" 
        :key="amenity.key"
        :class="['badge', `bg-${amenity.color}`, amenity.textClass, 'me-1', 'mb-1']"
      >
        <component 
          v-if="amenity.component" 
          :is="amenity.component" 
          :size="16" 
          class="me-1" 
        />
        <i v-else-if="amenity.icon" :class="`bi ${amenity.icon} me-1`"></i>
        {{ amenity.label }}
      </span>
    </div>
  </div>
</template>

<script>
import { 
  PhChampagne, PhBeerStein, PhMartini, PhBrandy, 
  PhFlowerLotus, PhWine 
} from '@phosphor-icons/vue'

export default {
  name: 'AmenitiesSection',
  
  components: {
    PhChampagne,
    PhBeerStein,
    PhMartini,
    PhBrandy,
    PhFlowerLotus,
    PhWine
  },

  props: {
    amenities: {
      type: Array,
      required: true
    }
  },

  data() {
    return {
      // Amenity configuration - easily maintainable and extensible
      amenityConfig: {
        // Payment Methods
        paymentCash: { label: 'Cash Payment', icon: 'bi-cash', color: 'primary' },
        paymentVisa: { label: 'Visa', icon: 'bi-credit-card', color: 'primary' },
        paymentMasterCard: { label: 'MasterCard', icon: 'bi-credit-card', color: 'primary' },
        paymentAmericanExpress: { label: 'Amex', icon: 'bi-credit-card', color: 'primary' },
        paymentApplePay: { label: 'Apple Pay', icon: 'bi-phone', color: 'primary' },
        paymentGooglePay: { label: 'Google Pay', icon: 'bi-google', color: 'primary' },
        paymentPayNow: { label: 'PayNow', icon: 'bi-qr-code', color: 'primary' },
        paymentDiscover: { label: 'Discover', icon: 'bi-credit-card', color: 'primary' },
        paymentSamsungPay: { label: 'Samsung Pay', icon: 'bi-phone', color: 'primary' },
        
        // Beverages
        beverageWine: { label: 'Wine', component: 'PhChampagne', color: 'success' },
        beverageBeer: { label: 'Beer', component: 'PhBeerStein', color: 'success' },
        beverageCocktails: { label: 'Cocktails', component: 'PhMartini', color: 'success' },
        beverageWhisky: { label: 'Whisky', component: 'PhBrandy', color: 'success' },
        beverageGin: { label: 'Gin', component: 'PhBrandy', color: 'success' },
        beverageVodka: { label: 'Vodka', component: 'PhBrandy', color: 'success' },
        beverageRum: { label: 'Rum', component: 'PhBrandy', color: 'success' },
        beverageTequila: { label: 'Tequila', component: 'PhFlowerLotus', color: 'success' },
        beverageMezcal: { label: 'Mezcal', component: 'PhFlowerLotus', color: 'success' },
        beverageBrandy: { label: 'Brandy', component: 'PhBrandy', color: 'success' },
        beverageSake: { label: 'Sake', component: 'PhWine', color: 'success' },
        beverageShochu: { label: 'Shochu', component: 'PhBrandy', color: 'success' },
        beverageSoju: { label: 'Soju', component: 'PhBrandy', color: 'success' },
        beverageBaijiu: { label: 'Baijiu', component: 'PhBrandy', color: 'success' },
        beverageAbsinthe: { label: 'Absinthe', component: 'PhBrandy', color: 'success' },
        beverageArrack: { label: 'Arrack', component: 'PhBrandy', color: 'success' },
        
        // General Amenities
        foodServed: { label: 'Food Served', icon: 'bi-egg-fried', color: 'info' },
        freeWiFi: { label: 'Free WiFi', icon: 'bi-wifi', color: 'info' },
        outdoorSeating: { label: 'Outdoor Seating', icon: 'bi-tree', color: 'info' },
        indoorSeating: { label: 'Indoor Seating', icon: 'bi-house', color: 'info' },
        liveMusic: { label: 'Live Music', icon: 'bi-music-note', color: 'warning' },
        wheelchairAccessibility: { label: 'Wheelchair Accessible', icon: 'bi-universal-access', color: 'secondary' },
        petFriendly: { label: 'Pet Friendly', icon: 'bi-heart', color: 'secondary' },
        childFriendly: { label: 'Child Friendly', icon: 'bi-people', color: 'secondary' },
        familyFriendly: { label: 'Family Friendly', icon: 'bi-house-heart', color: 'secondary' },
        smokeFriendly: { label: 'Smoking Friendly', icon: 'bi-cloud', color: 'secondary' },
        barGames: { label: 'Bar Games', icon: 'bi-controller', color: 'dark' },
        happyHourDrinks: { label: 'Happy Hour', icon: 'bi-clock', color: 'warning' },
        deliveryAvailable: { label: 'Delivery Available', icon: 'bi-truck', color: 'light', textClass: 'text-dark' },
        reservationsRequired: { label: 'Reservations Required', icon: 'bi-calendar-check', color: 'light', textClass: 'text-dark' },
        membershipRequired: { label: 'Membership Required', icon: 'bi-person-badge', color: 'light', textClass: 'text-dark' },
        sommelierService: { label: 'Sommelier Service', icon: 'bi-award', color: 'light', textClass: 'text-dark' },
        inStoreScheduling: { label: 'In-Store Scheduling', icon: 'bi-calendar3', color: 'light', textClass: 'text-dark' },
        lgbtqFriendly: { label: 'LGBTQ+ Friendly', icon: 'bi-rainbow', color: 'light', textClass: 'text-dark' }
      }
    }
  },

  computed: {
    // Computed property to generate badges array
    amenityBadges() {
      if (!this.amenities) return []
      
      return Object.entries(this.amenityConfig)
        .filter(([key]) => this.amenities[key])
        .map(([key, config]) => ({
          key,
          ...config,
          textClass: config.textClass || ''
        }))
    }
  }
}
</script>

<style scoped>
</style>