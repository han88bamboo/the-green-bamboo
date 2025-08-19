<template>
    <div class="d-flex flex-column gap-4">
        <!-- View Analytics Button (Venue) -->
        <div v-if="isSelfView">
            <router-link class="d-grid pb-3 text-decoration-none" :to="{ path: '/dashboard/venue' }">
                <button type="button" class="btn secondary-btn-not-rounded rounded-0" style=" font-weight: bold;"> View
                    My Analytics
                </button>
            </router-link>

            <!-- v-if admincreated account, if yes dont show -->
            <!-- <router-link v-if="!adminCreated" class="d-grid pb-3 text-decoration-none"
                :to="{ path: '/business/settings' }">
                <button type="button" class="btn secondary-btn-not-rounded rounded-0" style=" font-weight: bold;">
                    Settings
                </button>
            </router-link>

            <div v-else class="d-grid pb-3 text-decoration-none">
                <button class="btn secondary-btn-not-rounded rounded-0" type="button" style=" font-weight: bold;"
                    disabled>
                    Settings 
                </button>
            </div> -->

            <!-- Button for change/reset password -->
            <div class="d-grid pb-0 text-decoration-none">
                <button type="button" class="btn secondary-btn-not-rounded rounded-0" data-bs-toggle="modal"
                    data-bs-target="#changePasswordModal">
                    Change/Reset Password
                </button>
            </div>
        </div>

        <!-- Q&A Box -->
        <div class="border rounded p-3 shadow-sm square primary-square-green rounded mb-0">

            <h5 class="fw-bold mb-3">Q&As for {{ venue.venueName }}</h5>

            <div v-if="loading">
                <div class="spinner-border spinner-border-sm text-light me-2" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <span class="text-muted fst-italic">Loading QA data...</span>
            </div>
            <div v-else>
                <!-- Unclaimed View -->
                <div v-if="!venue.claimStatus" class="text-center py-1 m-1 rounded"
                    style="background-color: rgb(221, 200, 169); margin: 10px; color:black">
                    <p class="fs-5 mobile-fs-6 fw-bold mt-3 mb-2">Do you own this business?</p>
                    <p>Sign up for a venue account to answer questions from your fans!</p>
                    <button class="btn btn-warning fw-bold">Claim This Business</button>
                </div>
                <!-- Claimed View -->
                <div v-else>
                    <!-- Q&A content for claimed venues goes here -->
                    <p class="fst-italic text-muted">Q&A content will be displayed here.</p>
                </div>
            </div>

        </div>

        <!-- Map Box -->
        <div class="square primary-square-green-outline rounded p-3 mb-0">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="fw-bold">Venue Location</h5>
                <div v-if="isSelfView">
                    <!-- Edit Mode Buttons -->
                    <div v-if="editLocationMode" class="d-flex gap-2">
                        <button class="btn btn-sm btn-success" @click="saveLocationDetails">
                            <i class="bi bi-check-lg"></i>
                        </button>
                        <button class="btn btn-sm btn-secondary" @click="cancelEditLocationMode">
                            <i class="bi bi-x-lg"></i>
                        </button>
                    </div>
                    <!-- View Mode Button -->
                    <button v-else @click="toggleEditLocationMode" type="button" class="btn btn-sm btn-outline-secondary">
                        <i class="bi bi-pencil"></i>
                    </button>
                </div>
            </div>

            <div v-if="loading">
                <div class="text-center py-2">
                    <div class="spinner-border spinner-border-sm text-light me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <span class="text-muted fst-italic">Loading address and map data...</span>
                </div>
            </div>
            <div v-else>
                <!-- View Mode for Address -->
                <div v-if="!editLocationMode" class="mb-3">
                    <p class="text-start mb-0">{{ venue.address }}</p>
                </div>
                <!-- Edit Mode for Address -->
                <div v-else class="mb-3">
                    <textarea class="form-control form-control-sm" v-model="editedAddress" rows="2"
                              placeholder="Enter venue address..."></textarea>
                </div>

                <!-- Map Container -->
                <div v-if="loading" class="bg-secondary text-white text-center py-5 rounded">
                    <!-- Loading state -->
                    <div class="text-center py-2">
                        <div class="spinner-border spinner-border-sm text-light me-2" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <span class="text-muted fst-italic">Loading map data...</span>
                    </div>
                </div>
                <!-- Map -->
                <GMapMap v-else :center="{ lat: venue.loc.lat, lng: venue.loc.long }" :zoom="15" map-type-id="terrain"
                    style="width: 100%; height: 200px">
                    <GMapMarker :key="index" v-for="(m, index) in mapMarkers" :position="m.position" />
                </GMapMap>
            </div>
        </div>

        <!-- Opening Hours Box -->
        <div class="square primary-square-green-outline rounded p-3 mb-0">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="fw-bold">Opening Hours and Reservation Details</h5>
                <div v-if="isSelfView">
                    <!-- Edit Mode Buttons -->
                    <div v-if="editMode" class="d-flex gap-2">
                        <button class="btn btn-sm btn-success" @click="saveAllDetails">
                            <i class="bi bi-check-lg"></i>
                        </button>
                        <button class="btn btn-sm btn-secondary" @click="cancelEditMode">
                            <i class="bi bi-x-lg"></i>
                        </button>
                    </div>
                    <!-- View Mode Button -->
                    <button v-else @click="toggleEditMode" type="button" class="btn btn-sm btn-outline-secondary">
                        <i class="bi bi-pencil"></i>
                    </button>
                </div>
            </div>

            <!-- Opening Hours Section -->
            <div class="mb-4">
                <h6 class="mobile-fs-6 fw-bold mb-2">Opening Hours</h6>

                <div v-if="loading">
                    <div class="spinner-border spinner-border-sm text-light me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <span class="text-muted fst-italic">Loading opening hours...</span>
                </div>
                <div v-else>
                    <!-- View Mode for Opening Hours -->
                    <div v-if="!editMode">
                        <div v-if="openingHours && Object.keys(openingHours).length > 0">
                            <div v-for="(hours, day) in openingHours" :key="day" class="d-flex justify-content-between mb-1">
                                <span class="text-truncate" style="max-width: 40%;">{{ day }}</span>
                                <span v-if="hours[0] === '00:00' && hours[1] === '00:00'" class="fw-bold text-muted">Closed</span>
                                <span v-else class="fw-bold text-end" style="max-width: 60%;">{{ formatTime(hours[0]) }} - {{ formatTime(hours[1]) }}</span>
                            </div>
                        </div>
                        <div v-else>
                            <p class="text-muted fst-italic">No opening hours information available.</p>
                        </div>
                    </div>
                    <!-- Edit Mode for Opening Hours -->
                    <div v-else>
                        <div v-if="editedOpeningHours" class="row g-2">
                            <div v-for="(hours, day) in editedOpeningHours" :key="day" class="col-12">
                                <div class="row g-2 align-items-center">
                                    <div class="col-4">
                                        <span class="small fw-medium text-truncate d-block">{{ day }}:</span>
                                    </div>
                                    <div class="col-4">
                                        <input type="time" class="form-control form-control-sm" v-model="hours[0]">
                                    </div>
                                    <div class="col-4">
                                        <input type="time" class="form-control form-control-sm" v-model="hours[1]">
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="mt-2">
                            <button class="btn btn-sm btn-warning" @click="resetOpeningHours">Reset Hours</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Public Holiday Information Section -->
            <div class="mb-4">
                <h6 class="mobile-fs-6 fw-bold mb-2">Public Holiday Information</h6>
                <div v-if="loading">
                    <div class="spinner-border spinner-border-sm text-light me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <span class="text-muted fst-italic">Loading public holiday info...</span>
                </div>
                <div v-else>
                    <!-- View Mode for Public Holiday Info -->
                    <div v-if="!editMode">
                        <p v-if="venue.publicHolidayInfo" class="text-body-secondary">{{ venue.publicHolidayInfo }}</p>
                        <p v-else class="text-muted fst-italic">No public holiday information available.</p>
                    </div>
                    <!-- Edit Mode for Public Holiday Info -->
                    <div v-else>
                        <textarea class="form-control form-control-sm" v-model="editedPublicHolidayInfo" rows="2" 
                                  placeholder="Enter public holiday information..."></textarea>
                    </div>
                </div>
            </div>

            <!-- Reservation Details Section -->
            <div>
                <h6 class="mobile-fs-6 fw-bold mb-2">Reservation Details</h6>
                <div v-if="loading">
                    <div class="spinner-border spinner-border-sm text-light me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <span class="text-muted fst-italic">Loading reservation details...</span>
                </div>
                <div v-else>
                    <!-- View Mode for Reservation Details -->
                    <div v-if="!editMode">
                        <p v-if="venue.reservationDetails" class="text-body-secondary">{{ venue.reservationDetails }}</p>
                        <p v-else class="text-muted fst-italic">No reservation details available.</p>
                    </div>
                    <!-- Edit Mode for Reservation Details -->
                    <div v-else>
                        <textarea class="form-control form-control-sm" v-model="editedReservationDetails" rows="3"
                                  placeholder="Enter reservation details..."></textarea>
                    </div>
                </div>
            </div>
        </div>

        <!-- Event Box -->
        <!-- <div class="square primary-square-green-outline rounded p-3 mb-0">
            <div class="d-flex justify-content-between align-items-center mb-0">
                <h5 class="fw-bold">Your Events</h5>
                <button v-if="isSelfView" class="btn btn-sm btn-outline-secondary">Edit</button>
            </div>
            <p v-if="loading" class="text-start">retrieving events ... </p>
            <p v-else class="text-start">{{ venue.events? venue.events : 'No events added yet.' }}</p>
        </div> -->

        <EventBox :selfView="isSelfView" :targetUserID="venue.id" targetUserType="venue" />

    </div>
</template>

<script>
import EventBox from '@/components/EventBox.vue'; // Assuming path

export default {
    name: 'ProfileSidebar',
    components: { EventBox },
    props: {
        loading: Boolean,
        error: String,
        venue: Object,
        isSelfView: Boolean,
        answeredQuestions: Array,
        unansweredQuestions: Array,
        openingHours: Object,
    },
    data() {
        return {
            // construct our own mapmarker so that we do not 
            // duplicate known values so many times 
            mapMarkers: [{
                position: {
                    lat: this.venue?.loc?.lat || 0,
                    lng: this.venue?.loc?.long || 0
                }
            }],
            editMode: false,
            editedOpeningHours: null,
            editedPublicHolidayInfo: '',
            editedReservationDetails: '',
            editLocationMode: false,
            editedAddress: '',
        }
    },
    methods: {
        formatTime(timeStr) {
            if (!timeStr) return 'Closed';
            // Basic time formatting, can be improved with a library like date-fns
            const [hour, minute] = timeStr.split(':');
            const hourNum = parseInt(hour, 10);
            const ampm = hourNum >= 12 ? 'PM' : 'AM';
            const formattedHour = hourNum % 12 || 12; // Convert 0 to 12
            return `${formattedHour}:${minute} ${ampm}`;
        },
        toggleEditMode() {
            this.editMode = true;
            // Initialize opening hours
            const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
            const newEditedOpeningHours = {};
            days.forEach(day => {
                if (this.openingHours && this.openingHours[day]) {
                    newEditedOpeningHours[day] = JSON.parse(JSON.stringify(this.openingHours[day]));
                } else {
                    newEditedOpeningHours[day] = ['', ''];
                }
            });
            this.editedOpeningHours = newEditedOpeningHours;
            
            // Initialize other fields
            this.editedPublicHolidayInfo = this.venue.publicHolidayInfo || '';
            this.editedReservationDetails = this.venue.reservationDetails || '';
        },
        saveAllDetails() {
            // Here you would typically emit an event to the parent to save the data
            // For example: this.$emit('save-venue-details', { ... });
            console.log('Saving opening hours:', this.editedOpeningHours);
            console.log('Saving public holiday info:', this.editedPublicHolidayInfo);
            console.log('Saving reservation details:', this.editedReservationDetails);
            this.editMode = false;
        },
        cancelEditMode() {
            this.editMode = false;
            this.editedOpeningHours = null;
            this.editedPublicHolidayInfo = '';
            this.editedReservationDetails = '';
        },
        resetOpeningHours() {
            const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
            const resetHours = {};
            days.forEach(day => {
                resetHours[day] = ['00:00', '00:00']; // Reset to closed
            });
            this.editedOpeningHours = resetHours;
        },
        toggleEditLocationMode() {
            this.editLocationMode = true;
            this.editedAddress = this.venue.address || '';
        },
        saveLocationDetails() {
            // Here you would typically emit an event to the parent to save the data
            // For example: this.$emit('save-location-details', { address: this.editedAddress });
            console.log('Saving address:', this.editedAddress);
            this.editLocationMode = false;
        },
        cancelEditLocationMode() {
            this.editLocationMode = false;
            this.editedAddress = '';
        }
    },
}
</script>

<style scoped>
/* Ensure time inputs don't overflow */
.form-control-sm {
    font-size: 0.875rem;
}

/* Ensure proper spacing and alignment */
.row.g-2 > * {
    padding-right: calc(var(--bs-gutter-x) * 0.5);
    padding-left: calc(var(--bs-gutter-x) * 0.5);
}

/* Prevent text overflow in day labels */
.text-truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>