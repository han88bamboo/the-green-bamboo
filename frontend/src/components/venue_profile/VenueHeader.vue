<!-- Parent Component - Safe Integration -->
<template>
    <div class="venue-profile-container">

        <!-- Main Content - Only render when venue data is available -->
        <div v-if="venue && Object.keys(venue).length > 0" class="row">
            <!-- VenueImage Component -->
            <VenueImage :venue-photo="venue.photo || ''" :default-photo="defaultProfilePhoto" :is-editing="isEditing"
                :selected-image="selectedImage" :loading="imageUploadLoading" @image-selected="handleImageSelected"
                @image-reverted="handleImageReverted" @image-removed="handleImageRemoved" @error="handleImageError"
                ref="venueImageRef" />

            <!-- VenueDetails Component -->
            <VenueDetails :isLoading="isLoading" :venue="venue" :is-editing="isEditing" 
                :edit-data="venueEditData" :description-limit="150"
                :venue-types="availableVenueTypes" :validation-rules="venueValidationRules"
                @update:editData="handleVenueDetailsUpdate" @validation-changed="handleValidationChanged"
                ref="venueDetailsRef">
                <!-- Actions slot for buttons -->
                <template #actions>
                    <div class="d-grid no-padding text-end" v-if="!isOwner && !isAdmin">
                        <!-- Claim Venue -->
                        <p v-if="!venue.claimStatus"
                            class="text-body-secondary no-margin text-decoration-underline fst-italic"
                            style="color: #027562; cursor: pointer;" @click="claimVenueAccount">
                            Claim This Business
                        </p>
                        <p v-else class="text-success no-margin fw-bold fst-italic">
                            ✓ Verified Venue
                        </p>
                    </div>
                    <!-- Edit Profile Toggle -->
                    <div class="d-grid no-padding text-end" v-else>
                        <button v-if="!isEditing" type="button"
                            class="btn tertiary-btn-blue-outline rounded-0 reverse-clickable-text"
                            @click="toggleEditProfile">
                            <i class="bi bi-pencil-square"></i>
                            <span class="d-none d-lg-inline ms-2">Edit Profile</span>
                        </button>

                        <div v-else class="d-flex justify-content-end gap-2">
                            <button type="button" class="btn success-btn rounded-0 reverse-clickable-text"
                                @click="consolidateAndEmitData" :disabled="!isFormValid || isSaving">
                                <span v-if="isSaving" class="spinner-border spinner-border-sm" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </span>
                                <i v-else class="bi bi-save"></i>
                                <span class="d-none d-lg-inline ms-2">{{ isSaving ? 'Saving...' : 'Save' }}</span>
                            </button>
                            <button type="button" class="btn btn-danger rounded-0 reverse-clickable-text" @click="confirmExitEdit" :disabled="isSaving">
                                <i class="bi bi-x-circle"></i>
                                <span class="d-none d-lg-inline ms-2">Cancel</span>
                            </button>
                        </div>
                    </div>
                </template>

            </VenueDetails>

            <VenueAddDetails :venue="venue" :isFollowing="isFollowing" :is-editing="isEditing"
                :isOwner="isOwner" :isAdmin="isAdmin"
                @follow-clicked="$emit('follow-clicked')"
                @review-clicked="$emit('review-clicked')"
                @update:editData="handleVenueDetailsUpdate"
                ref="venueAddDetailsRef"
            />

            <!-- Amenity badge section -->
            <VenueAmenities :amenities="venue.amenities" :is-editing="isEditing"
                @update:editData="handleVenueDetailsUpdate"
                ref="venueAmenitiesRef"
            />
        </div>

        <!-- Empty State -->
        <div v-else class="alert alert-info">
            <h4>No Venue Data</h4>
            <p>Something went wrong. Try again later</p>
        </div>
    </div>
</template>

<script>
import VenueImage from './venue_header/VenueImage.vue';
import VenueDetails from './venue_header/VenueDetails.vue'
import VenueAddDetails from './venue_header/VenueAddDetails.vue';
import VenueAmenities from './venue_header/VenueAmenities.vue';

export default {
    name: 'VenueHeader',
    emits: ["follow-clicked", 'review-clicked', 'save-profile', 'toggle-edit'], // declare emits
    components: {
        VenueImage,
        VenueDetails,
        VenueAddDetails,
        VenueAmenities
    },
    props: {
        isLoading: Boolean,
        venue: {
            type: Object,
            required: true,
        },
        isFollowing: Boolean, 
        isEditing: Boolean,
        
        isOwner: {
            type: Boolean,
            default: false
        },

        isAdmin: {
            type: Boolean,
            default: false
        },
    },
    data() {
        return {
            defaultProfilePhoto: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultVenueProfilePhoto.png?v=1748435337',
            showFullDescription: true, // To match the image showing "(Read Less)"
            newPhotoPreview: null,

            // Image-related state
            selectedImage: '',
            editedProfilePhoto: '',
            imageUploadLoading: false,

            

            // Structured edit data for venue details
            venueEditData: {
                country: '',
                venueName: '',
                venueType: '',
                venueDesc: '',
                yearOpened: null,
                website: '',
                instagram: '',
                facebook: '',
                tiktok: '',
                email: '',
                phoneNumber: '',
                whatsappNumber: '',
                openForReservations: false
            },

            // Validation state
            isFormValid: false,
            validationErrors: {},
            isSaving: false,

            // Available venue types (you can move this to a config file)
            availableVenueTypes: [
                { value: 'restaurant', label: 'Restaurant' },
                { value: 'bar', label: 'Bar' },
                { value: 'cafe', label: 'Cafe' },
                { value: 'pub', label: 'Pub' },
                { value: 'lounge', label: 'Lounge' },
                { value: 'nightclub', label: 'Nightclub' },
                { value: 'brewery', label: 'Brewery' },
                { value: 'winery', label: 'Winery' },
                { value: 'hotel', label: 'Hotel' },
                { value: 'resort', label: 'Resort' },
                { value: 'other', label: 'Other' }
            ],

            // Validation rules
            venueValidationRules: {
                venueName: { required: true, minLength: 2, maxLength: 100 },
                country: { required: true, minLength: 2 },
                venueType: { required: false },
                venueDesc: { required: false, maxLength: 500 }
            }
        };
    },
    methods: {
        handleImageSelected(imageData) {
            console.log('Image selected:', imageData)

            // Update local state
            this.selectedImage = imageData.url
            this.editedProfilePhoto = imageData.file

            // You can also trigger upload immediately or wait for save
            // this.uploadImageImmediately(imageData.file)
        },

        /**
         * Handle image revert action
         * @param {Object} revertData - Contains original photo info
         */
        handleImageReverted(revertData) {
            console.log('Image reverted to:', revertData.originalPhoto)

            // Reset to original state
            this.selectedImage = ''
            this.editedProfilePhoto = ''

            // You might want to emit an event or update some state
            this.$emit('image-reverted')
        },

        /**
         * Handle image removal
         */
        handleImageRemoved() {
            console.log('Image removed')

            // Clear all image-related state
            this.selectedImage = ''
            this.editedProfilePhoto = ''

            // You might want to set a flag to indicate image should be deleted
            this.imageToDelete = true
        },

        /**
         * Handle image-related errors
         * @param {string} errorMessage - Error message from component
         */
        handleImageError(errorMessage) {
            console.error('Image error:', errorMessage)

            // Show user-friendly error message
            this.showErrorMessage(errorMessage)

            // You could also use a toast notification library
            // this.$toast.error(errorMessage)
        },

        /**
             * Handle venue details updates from the component
             */
        handleVenueDetailsUpdate(updatedData) {
            // Update the venue edit data
            this.venueEditData = { ...this.venueEditData, ...updatedData }

            // You can also trigger auto-save or other logic here
            console.log('Venue details updated:', updatedData)
        },

        /**
         * Handle validation changes from VenueDetails component
         */
        handleValidationChanged({ isValid, errors, data }) {
            this.isFormValid = isValid
            this.validationErrors = { ...this.validationErrors, ...errors }

            // Update edit data
            this.venueEditData = { ...this.venueEditData, ...data }

            console.log('Validation changed:', { isValid, errors })
        },

        /**
         * Toggle edit profile mode
         */
        toggleEditProfile() {
            this.$emit('toggle-edit');
        },

        /**
         * Initialize edit mode with current venue data
         */
        initializeEditMode() {
            this.editProfile = true
            const amenities = this.venue.amenities || {};

            // Initialize edit data with current venue values
            this.venueEditData = {
                country: this.venue.originLocation || '',
                venueName: this.venue.venueName || '',
                venueType: this.venue.venueType || '',
                venueDesc: this.venue.venueDesc || '',
                yearOpened: this.venue.yearOpened || null,
                website: this.venue.website || '',
                instagram: this.venue.instagram || '',
                facebook: this.venue.facebook || '',
                tiktok: this.venue.tiktok || '',
                email: this.venue.email || '',
                phoneNumber: this.venue.phoneNumber || '',
                whatsappNumber: this.venue.whatsappNumber || '',
                openForReservations: this.venue.openForReservations || false,

                // Payment Methods (match database schema)
                paymentCash: amenities.paymentCash || false,
                paymentVisa: amenities.paymentVisa || false,
                paymentMasterCard: amenities.paymentMasterCard || false,
                paymentAmericanExpress: amenities.paymentAmericanExpress || false,
                paymentDiscover: amenities.paymentDiscover || false,
                paymentApplePay: amenities.paymentApplePay || false,
                paymentPayNow: amenities.paymentPayNow || false,
                paymentGooglePay: amenities.paymentGooglePay || false,
                paymentSamsungPay: amenities.paymentSamsungPay || false,
                // Beverage Offerings (match database schema)
                beverageCocktails: amenities.beverageCocktails || false,
                beverageWine: amenities.beverageWine || false,
                beverageBeer: amenities.beverageBeer || false,
                beverageWhisky: amenities.beverageWhisky || false,
                beverageBrandy: amenities.beverageBrandy || false,
                beverageTequila: amenities.beverageTequila || false,
                beverageMezcal: amenities.beverageMezcal || false,
                beverageRum: amenities.beverageRum || false,
                beverageSake: amenities.beverageSake || false,
                beverageShochu: amenities.beverageShochu || false,
                beverageSoju: amenities.beverageSoju || false,
                beverageBaijiu: amenities.beverageBaijiu || false,
                beverageGin: amenities.beverageGin || false,
                beverageVodka: amenities.beverageVodka || false,
                beverageAbsinthe: amenities.beverageAbsinthe || false,
                beverageArrack: amenities.beverageArrack || false,
                // Other Amenities (match database schema)
                foodServed: amenities.foodServed || false,
                outdoorSeating: amenities.outdoorSeating || false,
                indoorSeating: amenities.indoorSeating || false,
                petFriendly: amenities.petFriendly || false,
                childFriendly: amenities.childFriendly || false,
                familyFriendly: amenities.familyFriendly || false,
                smokeFriendly: amenities.smokeFriendly || false,
                wheelchairAccessibility: amenities.wheelchairAccessibility || false,
                freeWiFi: amenities.freeWiFi || false,
                happyHourDrinks: amenities.happyHourDrinks || false,
                liveMusic: amenities.liveMusic || false,
                barGames: amenities.barGames || false,
                sommelierService: amenities.sommelierService || false,
                deliveryAvailable: amenities.deliveryAvailable || false,
                lgbtqFriendly: amenities.lgbtqFriendly || false,
                reservationsRequired: amenities.reservationsRequired || false,
                membershipRequired: amenities.membershipRequired || false,
                inStoreScheduling: amenities.inStoreScheduling || false,
                otherAmenities: amenities.otherAmenities || ''
            }

            // Reset validation state
            this.isFormValid = true
            this.validationErrors = {}
        },

        /**
         * Confirm exit from edit mode
         */
        confirmExitEdit() {
            this.exitEditMode();
            this.toggleEditProfile();
        },

        /**
         * Helper method to exit edit mode cleanly
         */
        exitEditMode() {
            this.editProfile = false
            this.isFormValid = false
            this.validationErrors = {}

            // Reset edit data to empty state
            this.venueEditData = {
                country: '',
                venueName: '',
                venueType: '',
                venueDesc: '',
                yearOpened: null,
                website: '',
                instagram: '',
                facebook: '',
                tiktok: '',
                email: '',
                phoneNumber: '',
                whatsappNumber: '',
                openForReservations: false,
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
                otherAmenities: ''
            }

            // Reset component states if they have reset methods
            if (this.$refs.venueDetailsRef && typeof this.$refs.venueDetailsRef.resetComponent === 'function') {
                this.$refs.venueDetailsRef.resetComponent()
            }
        },
        /**
         * Check if there are unsaved changes
         */
        hasUnsavedChanges() {
            return (
                this.venueEditData.country !== (this.venue.originLocation || '') ||
                this.venueEditData.venueName !== (this.venue.venueName || '') ||
                this.venueEditData.venueType !== (this.venue.venueType || '') ||
                this.venueEditData.venueDesc !== (this.venue.venueDesc || '') ||
                // Check other fields...
                this.selectedImage // Image changes
            )
        },

        /**
         * Consolidate data from child components and emit to parent
         */
        consolidateAndEmitData() {
            const venueDetailsData = this.$refs.venueDetailsRef.getEditData();
            const venueAddDetailsData = this.$refs.venueAddDetailsRef.getEditData();
            const venueAmenitiesData = this.$refs.venueAmenitiesRef.getEditData();

            const consolidatedData = {
                ...venueDetailsData,
                ...venueAddDetailsData,
                ...venueAmenitiesData,
                photo: this.editedProfilePhoto, // The file object
                deleteImage: this.imageToDelete,
                venueId: this.venue.id || this.venue.venueId
            };

            this.$emit('save-profile', consolidatedData);
            this.toggleEditProfile();
        },

        // Claim Venue Account
        claimVenueAccount() {
            let accountDetails = {
                userID: this.$route.params.venueID,
                businessType: "venue",
                businessName: this.targetVenue.venueName,
                businessDesc: this.targetVenue.venueDesc,
                businessLink: this.$route.fullPath,
                originCountry: this.targetVenue.originLocation,
            }
            this.$router.push({
                path: '/BusinessSignup',
                query: accountDetails
            });
        },

        showErrorMessage(message) {
            // Your existing implementation
            alert(message) // Replace with your preferred notification system
        },

        showSuccessMessage(message) {
            // Your existing implementation  
            alert(message) // Replace with your preferred notification system
        },

    },
    computed: {}
}
</script>


<style scoped>
</style>