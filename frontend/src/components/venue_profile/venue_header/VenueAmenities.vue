<template>
  <!-- Amenities Section -->
  <div v-if="!isEditing">
    <div v-if="amenityBadges.length > 0" class="mt-3">
      <h6 class="fw-bold mb-2" style="text-align:left">Amenities & Features</h6>
      <div class="d-flex flex-wrap gap-1">
        <span v-for="amenity in amenityBadges" :key="amenity.key"
          :class="['badge', `bg-${amenity.color}`, amenity.textClass, 'me-1', 'mb-1']">
          <component v-if="amenity.component" :is="amenity.component" :size="16" class="me-1" />
          <i v-else-if="amenity.icon" :class="`bi ${amenity.icon} me-1`"></i>
          {{ amenity.label }}
        </span>
      </div>
    </div>
  </div>
  <div v-else>
    <div class="col-12 mt-4">
      <h6 class="fw-bold mb-2">Amenities & Features</h6>

      <!-- Payment Methods -->
      <div class="mb-3">
        <h6 class="text-muted mb-2">Payment Methods</h6>
        <div class="d-flex flex-wrap gap-2">
          <span :class="getBadgeClasses('paymentCash', localEditAmenities.paymentCash)"
            @click="localEditAmenities.paymentCash = !localEditAmenities.paymentCash" style="cursor: pointer;">
            <i class="bi bi-cash me-1"></i>Cash Payment
          </span>
          <span :class="getBadgeClasses('paymentVisa', localEditAmenities.paymentVisa)"
            @click="localEditAmenities.paymentVisa = !localEditAmenities.paymentVisa" style="cursor: pointer;">
            <i class="bi bi-credit-card me-1"></i>Visa
          </span>
          <span :class="getBadgeClasses('paymentMasterCard', localEditAmenities.paymentMasterCard)"
            @click="localEditAmenities.paymentMasterCard = !localEditAmenities.paymentMasterCard" style="cursor: pointer;">
            <i class="bi bi-credit-card me-1"></i>MasterCard
          </span>
          <span :class="getBadgeClasses('paymentAmericanExpress', localEditAmenities.paymentAmericanExpress)"
            @click="localEditAmenities.paymentAmericanExpress = !localEditAmenities.paymentAmericanExpress" style="cursor: pointer;">
            <i class="bi bi-credit-card me-1"></i>American Express
          </span>
          <span :class="getBadgeClasses('paymentDiscover', localEditAmenities.paymentDiscover)"
            @click="localEditAmenities.paymentDiscover = !localEditAmenities.paymentDiscover" style="cursor: pointer;">
            <i class="bi bi-credit-card me-1"></i>Discover
          </span>
          <span :class="getBadgeClasses('paymentApplePay', localEditAmenities.paymentApplePay)"
            @click="localEditAmenities.paymentApplePay = !localEditAmenities.paymentApplePay" style="cursor: pointer;">
            <i class="bi bi-phone me-1"></i>Apple Pay
          </span>
          <span :class="getBadgeClasses('paymentGooglePay', localEditAmenities.paymentGooglePay)"
            @click="localEditAmenities.paymentGooglePay = !localEditAmenities.paymentGooglePay" style="cursor: pointer;">
            <i class="bi bi-google me-1"></i>Google Pay
          </span>
          <span :class="getBadgeClasses('paymentPayNow', localEditAmenities.paymentPayNow)"
            @click="localEditAmenities.paymentPayNow = !localEditAmenities.paymentPayNow" style="cursor: pointer;">
            <i class="bi bi-qr-code me-1"></i>PayNow
          </span>
          <span :class="getBadgeClasses('paymentSamsungPay', localEditAmenities.paymentSamsungPay)"
            @click="localEditAmenities.paymentSamsungPay = !localEditAmenities.paymentSamsungPay" style="cursor: pointer;">
            <i class="bi bi-phone me-1"></i>Samsung Pay
          </span>
        </div>
      </div>

      <!-- Beverage Offerings -->
      <div class="mb-3">
        <h6 class="text-muted mb-2">Beverage Offerings</h6>
        <div class="d-flex flex-wrap gap-2">
          <span :class="getBadgeClasses('beverageCocktails', localEditAmenities.beverageCocktails)"
            @click="localEditAmenities.beverageCocktails = !localEditAmenities.beverageCocktails" style="cursor: pointer;">
            <PhMartini :size="16" class="me-1" />Cocktails
          </span>
          <span :class="getBadgeClasses('beverageWine', localEditAmenities.beverageWine)"
            @click="localEditAmenities.beverageWine = !localEditAmenities.beverageWine" style="cursor: pointer;">
            <PhChampagne :size="16" class="me-1" />Wine
          </span>
          <span :class="getBadgeClasses('beverageBeer', localEditAmenities.beverageBeer)"
            @click="localEditAmenities.beverageBeer = !localEditAmenities.beverageBeer" style="cursor: pointer;">
            <PhBeerStein :size="16" class="me-1" />Beer
          </span>
          <span :class="getBadgeClasses('beverageWhisky', localEditAmenities.beverageWhisky)"
            @click="localEditAmenities.beverageWhisky = !localEditAmenities.beverageWhisky" style="cursor: pointer;">
            <PhBrandy :size="16" class="me-1" />Whisky
          </span>
          <span :class="getBadgeClasses('beverageBrandy', localEditAmenities.beverageBrandy)"
            @click="localEditAmenities.beverageBrandy = !localEditAmenities.beverageBrandy" style="cursor: pointer;">
            <PhBrandy :size="16" class="me-1" />Brandy
          </span>
          <span :class="getBadgeClasses('beverageTequila', localEditAmenities.beverageTequila)"
            @click="localEditAmenities.beverageTequila = !localEditAmenities.beverageTequila" style="cursor: pointer;">
            <PhFlowerLotus :size="16" class="me-1" />Tequila
          </span>
          <span :class="getBadgeClasses('beverageMezcal', localEditAmenities.beverageMezcal)"
            @click="localEditAmenities.beverageMezcal = !localEditAmenities.beverageMezcal" style="cursor: pointer;">
            <PhFlowerLotus :size="16" class="me-1" />Mezcal
          </span>
          <span :class="getBadgeClasses('beverageRum', localEditAmenities.beverageRum)"
            @click="localEditAmenities.beverageRum = !localEditAmenities.beverageRum" style="cursor: pointer;">
            <PhBrandy :size="16" class="me-1" />Rum
          </span>
          <span :class="getBadgeClasses('beverageSake', localEditAmenities.beverageSake)"
            @click="localEditAmenities.beverageSake = !localEditAmenities.beverageSake" style="cursor: pointer;">
            <PhWine :size="16" class="me-1" />Sake
          </span>
          <span :class="getBadgeClasses('beverageShochu', localEditAmenities.beverageShochu)"
            @click="localEditAmenities.beverageShochu = !localEditAmenities.beverageShochu" style="cursor: pointer;">
            <PhBrandy :size="16" class="me-1" />Shochu
          </span>
          <span :class="getBadgeClasses('beverageSoju', localEditAmenities.beverageSoju)"
            @click="localEditAmenities.beverageSoju = !localEditAmenities.beverageSoju" style="cursor: pointer;">
            <PhBrandy :size="16" class="me-1" />Soju
          </span>
          <span :class="getBadgeClasses('beverageBaijiu', localEditAmenities.beverageBaijiu)"
            @click="localEditAmenities.beverageBaijiu = !localEditAmenities.beverageBaijiu" style="cursor: pointer;">
            <PhBrandy :size="16" class="me-1" />Baijiu
          </span>
          <span :class="getBadgeClasses('beverageGin', localEditAmenities.beverageGin)"
            @click="localEditAmenities.beverageGin = !localEditAmenities.beverageGin" style="cursor: pointer;">
            <PhBrandy :size="16" class="me-1" />Gin
          </span>
          <span :class="getBadgeClasses('beverageVodka', localEditAmenities.beverageVodka)"
            @click="localEditAmenities.beverageVodka = !localEditAmenities.beverageVodka" style="cursor: pointer;">
            <PhBrandy :size="16" class="me-1" />Vodka
          </span>
          <span :class="getBadgeClasses('beverageAbsinthe', localEditAmenities.beverageAbsinthe)"
            @click="localEditAmenities.beverageAbsinthe = !localEditAmenities.beverageAbsinthe" style="cursor: pointer;">
            <PhBrandy :size="16" class="me-1" />Absinthe
          </span>
          <span :class="getBadgeClasses('beverageArrack', localEditAmenities.beverageArrack)"
            @click="localEditAmenities.beverageArrack = !localEditAmenities.beverageArrack" style="cursor: pointer;">
            <PhBrandy :size="16" class="me-1" />Arrack
          </span>
        </div>
      </div>

      <!-- General Amenities -->
      <div class="mb-3">
        <h6 class="text-muted mb-2">General Amenities</h6>
        <div class="d-flex flex-wrap gap-2">
          <span :class="getBadgeClasses('foodServed', localEditAmenities.foodServed)"
            @click="localEditAmenities.foodServed = !localEditAmenities.foodServed" style="cursor: pointer;">
            <i class="bi bi-egg-fried me-1"></i>Food Served
          </span>
          <span :class="getBadgeClasses('outdoorSeating', localEditAmenities.outdoorSeating)"
            @click="localEditAmenities.outdoorSeating = !localEditAmenities.outdoorSeating" style="cursor: pointer;">
            <i class="bi bi-tree me-1"></i>Outdoor Seating
          </span>
          <span :class="getBadgeClasses('indoorSeating', localEditAmenities.indoorSeating)"
            @click="localEditAmenities.indoorSeating = !localEditAmenities.indoorSeating" style="cursor: pointer;">
            <i class="bi bi-house me-1"></i>Indoor Seating
          </span>
          <span :class="getBadgeClasses('petFriendly', localEditAmenities.petFriendly)"
            @click="localEditAmenities.petFriendly = !localEditAmenities.petFriendly" style="cursor: pointer;">
            <i class="bi bi-heart me-1"></i>Pet Friendly
          </span>
          <span :class="getBadgeClasses('childFriendly', localEditAmenities.childFriendly)"
            @click="localEditAmenities.childFriendly = !localEditAmenities.childFriendly" style="cursor: pointer;">
            <i class="bi bi-people me-1"></i>Child Friendly
          </span>
          <span :class="getBadgeClasses('familyFriendly', localEditAmenities.familyFriendly)"
            @click="localEditAmenities.familyFriendly = !localEditAmenities.familyFriendly" style="cursor: pointer;">
            <i class="bi bi-house-heart me-1"></i>Family Friendly
          </span>
          <span :class="getBadgeClasses('smokeFriendly', localEditAmenities.smokeFriendly)"
            @click="localEditAmenities.smokeFriendly = !localEditAmenities.smokeFriendly" style="cursor: pointer;">
            <i class="bi bi-cloud me-1"></i>Smoking Friendly
          </span>
          <span :class="getBadgeClasses('wheelchairAccessibility', localEditAmenities.wheelchairAccessibility)"
            @click="localEditAmenities.wheelchairAccessibility = !localEditAmenities.wheelchairAccessibility" style="cursor: pointer;">
            <i class="bi bi-universal-access me-1"></i>Wheelchair Accessible
          </span>
          <span :class="getBadgeClasses('freeWiFi', localEditAmenities.freeWiFi)"
            @click="localEditAmenities.freeWiFi = !localEditAmenities.freeWiFi" style="cursor: pointer;">
            <i class="bi bi-wifi me-1"></i>Free WiFi
          </span>
          <span :class="getBadgeClasses('liveMusic', localEditAmenities.liveMusic)"
            @click="localEditAmenities.liveMusic = !localEditAmenities.liveMusic" style="cursor: pointer;">
            <i class="bi bi-music-note me-1"></i>Live Music
          </span>
          <span :class="getBadgeClasses('barGames', localEditAmenities.barGames)"
            @click="localEditAmenities.barGames = !localEditAmenities.barGames" style="cursor: pointer;">
            <i class="bi bi-controller me-1"></i>Bar Games
          </span>
          <span :class="getBadgeClasses('happyHourDrinks', localEditAmenities.happyHourDrinks)"
            @click="localEditAmenities.happyHourDrinks = !localEditAmenities.happyHourDrinks" style="cursor: pointer;">
            <i class="bi bi-clock me-1"></i>Happy Hour
          </span>
          <span :class="getBadgeClasses('deliveryAvailable', localEditAmenities.deliveryAvailable)"
            @click="localEditAmenities.deliveryAvailable = !localEditAmenities.deliveryAvailable" style="cursor: pointer;">
            <i class="bi bi-truck me-1"></i>Delivery Available
          </span>
          <span :class="getBadgeClasses('lgbtqFriendly', localEditAmenities.lgbtqFriendly)"
            @click="localEditAmenities.lgbtqFriendly = !localEditAmenities.lgbtqFriendly" style="cursor: pointer;">
            <i class="bi bi-rainbow me-1"></i>LGBTQ+ Friendly
          </span>
          <span :class="getBadgeClasses('reservationsRequired', localEditAmenities.reservationsRequired)"
            @click="localEditAmenities.reservationsRequired = !localEditAmenities.reservationsRequired" style="cursor: pointer;">
            <i class="bi bi-calendar-check me-1"></i>Reservations Required
          </span>
          <span :class="getBadgeClasses('membershipRequired', localEditAmenities.membershipRequired)"
            @click="localEditAmenities.membershipRequired = !localEditAmenities.membershipRequired" style="cursor: pointer;">
            <i class="bi bi-person-badge me-1"></i>Membership Required
          </span>
          <span :class="getBadgeClasses('sommelierService', localEditAmenities.sommelierService)"
            @click="localEditAmenities.sommelierService = !localEditAmenities.sommelierService" style="cursor: pointer;">
            <i class="bi bi-award me-1"></i>Sommelier Service
          </span>
          <span :class="getBadgeClasses('inStoreScheduling', localEditAmenities.inStoreScheduling)"
            @click="localEditAmenities.inStoreScheduling = !localEditAmenities.inStoreScheduling" style="cursor: pointer;">
            <i class="bi bi-calendar3 me-1"></i>In-Store Scheduling
          </span>
          <span :class="getBadgeClasses('ticketed', localEditAmenities.ticketed)"
            @click="localEditAmenities.ticketed = !localEditAmenities.ticketed" style="cursor: pointer;">
            <i class="bi bi-ticket-perforated me-1"></i>Tickets Required
          </span>
        </div>
      </div>

      <!-- Other Amenities Text Field -->
      <div class="mb-3">
        <h6 class="text-muted mb-2">Other Amenities</h6>
        <textarea class="form-control" id="otherAmenities" v-model="localEditAmenities.otherAmenities" rows="3"
          placeholder="Describe any other amenities not listed above..."></textarea>
      </div>
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
    // Whether component is in edit mode
    isEditing: {
      type: Boolean,
      default: false
    },

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
        lgbtqFriendly: { label: 'LGBTQ+ Friendly', icon: 'bi-rainbow', color: 'light', textClass: 'text-dark' },
        ticketed: { label: 'Tickets Required', icon: 'bi-ticket-perforated', color: 'warning', textClass: 'text-dark' }
      },

      localEditAmenities: {
        // Payment Methods (match database schema)
        paymentCash: false,
        paymentVisa: false,
        paymentMasterCard: false,
        paymentAmericanExpress: false,
        paymentDiscover: false,
        paymentApplePay: false,
        paymentPayNow: false,
        paymentGooglePay: false,
        paymentSamsungPay: false,
        // Beverage Offerings (match database schema)
        beverageCocktails: false,
        beverageWine: false,
        beverageBeer: false,
        beverageWhisky: false,
        beverageBrandy: false,
        beverageTequila: false,
        beverageMezcal: false,
        beverageRum: false,
        beverageSake: false,
        beverageShochu: false,
        beverageSoju: false,
        beverageBaijiu: false,
        beverageGin: false,
        beverageVodka: false,
        beverageAbsinthe: false,
        beverageArrack: false,
        // Other Amenities (match database schema)
        foodServed: false,
        outdoorSeating: false,
        indoorSeating: false,
        petFriendly: false,
        childFriendly: false,
        familyFriendly: false,
        smokeFriendly: false,
        wheelchairAccessibility: false,
        freeWiFi: false,
        happyHourDrinks: false,
        liveMusic: false,
        barGames: false,
        sommelierService: false,
        deliveryAvailable: false,
        lgbtqFriendly: false,
        reservationsRequired: false,
        membershipRequired: false,
        inStoreScheduling: false,
        ticketed: false,
        otherAmenities: ''
      }

    }
  },

  watch: {
    isEditing: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.initializeEditData();
        }
      }
    },
    localEditAmenities: {
      deep: true,
      handler(newVal) {
        this.$emit('update:editData', newVal);
      }
    }
  },

  methods: {
    initializeEditData() {
      // Create a new object to ensure reactivity is triggered
      const newEditData = {};
      // Use the component's initial data as a source for all possible keys
      const defaultData = this.$options.data().localEditAmenities;

      for (const key in defaultData) {
        if (this.amenities && Object.prototype.hasOwnProperty.call(this.amenities, key)) {
          newEditData[key] = this.amenities[key];
        } else {
          newEditData[key] = defaultData[key];
        }
      }
      this.localEditAmenities = newEditData;
    },
    getEditData() {
      return this.localEditAmenities;
    },
    handleInputChange() {
      this.$emit('update:editData', this.localEditAmenities);
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
    }, 

    getBadgeClasses() {
        return (amenityKey, isActive) => {
          const config = this.amenityConfig[amenityKey];
          if (!config) return ['badge', 'bg-light', 'text-dark'];
          
          if (isActive) {
            // Handle 'light' color specially - use a darker color when active
            const color = config.color === 'light' ? 'secondary' : config.color;
            return [
              'badge',
              `bg-${color}`,
              color === 'light' ? 'text-dark' : 'text-white'
            ];
          } else {
            return ['badge', 'bg-light', 'text-dark'];
          }
        };
      }
  },

  expose: ['getEditData']
}
</script>

<style scoped>
</style>