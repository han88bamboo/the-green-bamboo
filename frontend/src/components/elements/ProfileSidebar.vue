<template>
    <div class="d-flex flex-column gap-4">
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
                <div v-if="!venue.claimStatus" class="text-center py-1 m-1 rounded" style="background-color: rgb(221, 200, 169); margin: 10px; color:black">
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
            <div class="d-flex justify-content-between align-items-center mb-0">
                <h5 class="fw-bold">Venue Location</h5>
                <button v-if="isSelfView" class="btn btn-sm btn-outline-secondary">Edit</button>
            </div>
            <p v-if="loading" class="text-start">retrieving address ... </p>
            <p v-else class="text-start">{{ venue.address }}</p>
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

        <!-- Opening Hours Box -->
        <div class="square primary-square-green-outline rounded p-3 mb-0">
            <h5 class="fw-bold mb-3">Opening Hours and Reservation Details</h5>
            
            <div v-if="loading">
                <div class="spinner-border spinner-border-sm text-light me-2" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <span class="text-muted fst-italic">Loading business data...</span>
            </div>
            <div v-else>
                <!-- Unclaimed View -->
                <div v-if="!venue.claimStatus" class="text-center bg-light-tan p-1 rounded">
                    <p class="fs-5 mobile-fs-6 fw-bold mt-3 mb-2">Do you own this business?</p>
                    <p>Sign up for a venue account to answer questions from your fans!</p>
                    <button class="btn btn-warning fw-bold">Claim This Business</button>
                </div>
                <!-- Claimed View -->
                <div v-else>
                    <div class="square-inline">
                        <h5 class="mr-auto mobile-fs-6 fw-bold"> Opening Hours </h5>
                    </div>
                    <div v-for="(hours, day) in openingHours" :key="day" class="d-flex justify-content-between">
                        <span>{{ day }}:</span>
                        <span class="fw-bold"> {{ formatTime(hours[0]) }} - {{ formatTime(hours[1]) }} </span>
                    </div>

                    <!-- Section Header -->
                    <div class="square-inline">
                        <h5 class="mr-auto mobile-fs-6 fw-bold"> Reservation Details </h5>
                    </div>

                    <div class="text-body-secondary mobile-rating-smaller-text-2">
                        <div v-if="venue['reservationDetails'] == ''" class="fst-italic mobile-rating-smaller-text-2">
                            No reservation details available!
                        </div>
                        <div v-else>
                            {{ venue["reservationDetails"] }}
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
// import EventBox from '@/components/EventBox.vue'; // Assuming path

export default {
    name: 'ProfileSidebar',
    // components: { EventBox },
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
            }]
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
        }
    },
}
</script>

<style scoped>
</style>