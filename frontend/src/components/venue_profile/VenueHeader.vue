<!-- Parent Component - Safe Integration -->
<template>
    <div class="venue-profile-container">
        <!-- Loading State -->
        <!-- <div v-if="isLoading" class="d-flex justify-content-center align-items-center" style="min-height: 400px;">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading venue...</span>
            </div>
        </div> -->

        <!-- Error State -->
        <!-- <div v-else-if="loadError" class="alert alert-danger">
            <h4>Error Loading Venue</h4>
            <p>{{ loadError }}</p>
            <button class="btn btn-primary" @click="loadVenueData">Try Again</button>
        </div> -->

        <!-- Main Content - Only render when venue data is available -->
        <div v-if="venue && Object.keys(venue).length > 0" class="row">
            <!-- VenueImage Component -->
            <VenueImage :venue-photo="venue.photo || ''" :default-photo="defaultProfilePhoto" :is-editing="editProfile"
                :selected-image="selectedImage" :loading="imageUploadLoading" @image-selected="handleImageSelected"
                @image-reverted="handleImageReverted" @image-removed="handleImageRemoved" @error="handleImageError"
                ref="venueImageRef" />

            <!-- VenueDetails Component -->
            <VenueDetails :isLoading="isLoading" :venue="venue" :is-editing="editProfile" 
                :edit-data="venueEditData" :description-limit="150"
                :venue-types="availableVenueTypes" :validation-rules="venueValidationRules"
                @update:editData="handleVenueDetailsUpdate" @validation-changed="handleValidationChanged"
                ref="venueDetailsRef">
                <!-- Actions slot for buttons -->
                <template #actions>
                    <div class="d-grid no-padding text-end" v-if="!isSelfView && !isPowerView">
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
                        <button v-if="!editProfile" type="button"
                            class="btn tertiary-btn-blue-outline rounded-0 reverse-clickable-text"
                            @click="toggleEditProfile">
                            <i class="bi bi-pencil-square"></i>
                            <span class="d-none d-lg-inline ms-2">Edit Profile</span>
                        </button>

                        <div v-else class="d-flex justify-content-end gap-2">
                            <button type="button" class="btn success-btn rounded-0 reverse-clickable-text"
                                @click="saveProfileEdits" :disabled="!isFormValid || isSaving">
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

            <VenueAddDetails :venue="venue" :isFollowing="isFollowing" :is-editing="editProfile"
                @follow-clicked="$emit('follow-clicked')"
                @review-clicked="$emit('review-clicked')"
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

export default {
    name: 'VenueHeader',
    emits: ["follow-clicked", 'review-clicked'], // declare emits
    components: {
        VenueImage,
        VenueDetails,
        VenueAddDetails
    },
    props: {
        isLoading: Boolean,
        venue: {
            type: Object,
            required: true,
        },
        isFollowing: Boolean, 
        isSelfView: Boolean,
        isPowerView: Boolean,
        isEditing: Boolean,
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

            // Other existing state...
            editProfile: false,

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
         * Save profile edits (existing method, now handles image)
         */
        // async saveProfileEdits() {
        //   try {
        //     this.imageUploadLoading = true

        //     // Create form data for API call
        //     const formData = new FormData()

        //     // Add venue details
        //     formData.append('venueName', this.editVenueName)
        //     formData.append('venueType', this.editVenueType)
        //     formData.append('venueDesc', this.editVenueDesc)
        //     formData.append('country', this.editCountry)

        //     // Add image if selected
        //     if (this.editedProfilePhoto) {
        //       formData.append('photo', this.editedProfilePhoto)
        //     }

        //     // Add flag if image should be deleted
        //     if (this.imageToDelete) {
        //       formData.append('deleteImage', true)
        //     }

        //     // Make API call
        //     const response = await this.$http.post('/api/venue/update', formData, {
        //       headers: {
        //         'Content-Type': 'multipart/form-data'
        //       }
        //     })

        //     if (response.data.success) {
        //       // Update venue data with response
        //       this.targetVenue = { ...this.targetVenue, ...response.data.venue }

        //       // Reset edit state
        //       this.editProfile = false
        //       this.selectedImage = ''
        //       this.editedProfilePhoto = ''
        //       this.imageToDelete = false

        //       this.showSuccessMessage('Profile updated successfully!')
        //     }

        //   } catch (error) {
        //     console.error('Save error:', error)
        //     this.handleImageError('Failed to save profile changes')
        //   } finally {
        //     this.imageUploadLoading = false
        //   }
        // },

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
            if (this.editProfile) {
                // Exiting edit mode - you might want to show a confirmation dialog
                this.confirmExitEdit()
            } else {
                // Entering edit mode
                this.initializeEditMode()
            }
        },

        /**
         * Initialize edit mode with current venue data
         */
        initializeEditMode() {
            this.editProfile = true

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
                openForReservations: this.venue.openForReservations || false
            }

            // Reset validation state
            this.isFormValid = true
            this.validationErrors = {}
        },

        /**
         * Confirm exit from edit mode
         */
        confirmExitEdit() {
            // Check if there are unsaved changes
            if (this.hasUnsavedChanges()) {
                if (confirm('You have unsaved changes. Are you sure you want to exit without saving?')) {
                    this.exitEditMode()
                }
            } else {
                this.exitEditMode()
            }
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
                openForReservations: false
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
         * Combined saveProfileEdits method that handles:
         * - Component validation
         * - Form data preparation  
         * - Image handling (upload/delete)
         * - API communication
         * - State management
         */
        async saveProfileEdits() {
            try {
                // Step 1: Validate all components first
                const venueDetailsValid = this.$refs.venueDetailsRef?.validate()
                // const venueImageValid = this.$refs.venueImageRef // Image component doesn't need validation per se

                if (!venueDetailsValid || !this.isFormValid) {
                    this.showErrorMessage('Please fix all validation errors before saving.')
                    return
                }

                // Step 2: Set loading state
                this.isSaving = true
                this.imageUploadLoading = true

                // Step 3: Prepare form data for multipart upload
                const formData = new FormData()

                // Add venue basic details from VenueDetails component
                const venueFields = ['country', 'venueName', 'venueType', 'venueDesc']
                venueFields.forEach(field => {
                    const value = this.venueEditData[field]
                    if (value !== null && value !== undefined && value !== '') {
                        // Map field names to match your API expectations
                        const apiFieldName = field === 'country' ? 'originLocation' : field
                        formData.append(apiFieldName, value)
                    }
                })

                // Add additional venue details (contact info, social media, etc.)
                const additionalFields = [
                    'yearOpened', 'website', 'instagram', 'facebook', 'tiktok',
                    'email', 'phoneNumber', 'whatsappNumber', 'openForReservations'
                ]
                additionalFields.forEach(field => {
                    const value = this.venueEditData[field]
                    if (value !== null && value !== undefined && value !== '') {
                        formData.append(field, value)
                    }
                })

                // Step 4: Handle image operations
                if (this.editedProfilePhoto && this.editedProfilePhoto instanceof File) {
                    // New image selected - upload it
                    formData.append('photo', this.editedProfilePhoto)
                    console.log('Adding new photo to upload:', this.editedProfilePhoto.name)
                } else if (this.imageToDelete) {
                    // Image should be removed
                    formData.append('deleteImage', 'true')
                    console.log('Marking image for deletion')
                }

                // Add venue ID if updating existing venue
                if (this.venue.id || this.venue.venueId) {
                    formData.append('venueId', this.venue.id || this.venue.venueId)
                }

                // Step 5: Debug log (remove in production)
                console.log('Saving profile with data:', {
                    venueEditData: this.venueEditData,
                    hasImage: !!this.editedProfilePhoto,
                    deleteImage: this.imageToDelete,
                    venueId: this.venue.id || this.venue.venueId
                })

                // Step 6: Make API call
                const response = await this.$http.post('/api/venue/update', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    timeout: 30000, // 30 second timeout for large image uploads
                })

                // Step 7: Handle successful response
                if (response.data && response.data.success) {
                    // Update local venue data with response
                    this.targetVenue = {
                        ...this.targetVenue,
                        ...response.data.targetVenue,
                        // Ensure we update the correct field names
                        originLocation: response.data.venue.originLocation || response.data.targetVenue.country,
                        photo: response.data.targetVenue.photo || (this.imageToDelete ? '' : this.targetVenue.photo)
                    }

                    // Step 8: Reset all edit states
                    this.exitEditMode()

                    // Reset image-related state
                    this.selectedImage = ''
                    this.editedProfilePhoto = ''
                    this.imageToDelete = false

                    // Reset validation state
                    this.isFormValid = false
                    this.validationErrors = {}

                    // Show success message
                    this.showSuccessMessage('Profile updated successfully!')

                    // Emit event for parent components or analytics
                    this.$emit('profile-updated', {
                        venue: this.targetVenue,
                        changes: this.venueEditData
                    })

                } else {
                    // Handle API error response
                    const errorMessage = response.data?.message || 'Failed to update profile. Please try again.'
                    this.showErrorMessage(errorMessage)

                    console.error('API returned error:', response.data)
                }

            } catch (error) {
                // Step 9: Handle different types of errors
                console.error('Save profile error:', error)

                let errorMessage = 'Failed to save profile changes. Please try again.'

                if (error.response) {
                    // Server responded with error status
                    const status = error.response.status
                    const serverMessage = error.response.data?.message

                    switch (status) {
                        case 400:
                            errorMessage = serverMessage || 'Invalid data provided. Please check your entries.'
                            break
                        case 401:
                            errorMessage = 'You are not authorized to make this change. Please log in again.'
                            // Redirect to login if needed
                            // this.$router.push('/login')
                            break
                        case 403:
                            errorMessage = 'You do not have permission to edit this venue.'
                            break
                        case 413:
                            errorMessage = 'The uploaded image is too large. Please choose a smaller file.'
                            break
                        case 422:
                            errorMessage = serverMessage || 'Validation failed. Please check your entries.'
                            // Handle validation errors from server
                            if (error.response.data?.errors) {
                                this.validationErrors = { ...this.validationErrors, ...error.response.data.errors }
                            }
                            break
                        case 500:
                            errorMessage = 'Server error occurred. Please try again later.'
                            break
                        default:
                            errorMessage = serverMessage || `Server error (${status}). Please try again.`
                    }
                } else if (error.request) {
                    // Network error
                    errorMessage = 'Network error. Please check your connection and try again.'
                } else if (error.code === 'ECONNABORTED') {
                    // Timeout error
                    errorMessage = 'Upload took too long. Please try again with a smaller image.'
                }

                this.showErrorMessage(errorMessage)

            } finally {
                // Step 10: Always reset loading states
                this.isSaving = false
                this.imageUploadLoading = false
            }
        },

        /**
         * Save profile edits
         */
        // async saveProfileEdits() {
        //   try {
        //     // Validate all components first
        //     const venueDetailsValid = this.$refs.venueDetailsRef?.validate()

        //     if (!venueDetailsValid || !this.isFormValid) {
        //       this.showErrorMessage('Please fix all validation errors before saving.')
        //       return
        //     }

        //     this.isSaving = true

        //     // Prepare form data
        //     const formData = new FormData()

        //     // Add venue details
        //     Object.keys(this.venueEditData).forEach(key => {
        //       if (this.venueEditData[key] !== null && this.venueEditData[key] !== '') {
        //         formData.append(key, this.venueEditData[key])
        //       }
        //     })

        //     // Add image if selected
        //     if (this.editedProfilePhoto) {
        //       formData.append('photo', this.editedProfilePhoto)
        //     }

        //     // API call
        //     const response = await this.$http.post('/api/venue/update', formData, {
        //       headers: { 'Content-Type': 'multipart/form-data' }
        //     })

        //     if (response.data.success) {
        //       // Update venue data
        //       this.targetVenue = { ...this.targetVenue, ...response.data.venue }

        //       // Exit edit mode
        //       this.exitEditMode()

        //       // Reset image state
        //       this.selectedImage = ''
        //       this.editedProfilePhoto = ''

        //       this.showSuccessMessage('Profile updated successfully!')
        //     }

        //   } catch (error) {
        //     console.error('Save error:', error)
        //     this.showErrorMessage('Failed to save profile changes. Please try again.')
        //   } finally {
        //     this.isSaving = false
        //   }
        // },

        /**
         * Handle additional fields update (for fields not in VenueDetails)
         */
        handleAdditionalFieldsUpdate() {
            // This will be moved to VenueContactInfo component later
            console.log('Additional fields updated')
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