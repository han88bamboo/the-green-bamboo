<template>
    <div class="square primary-square-green-outline rounded p-3 mb-3">

        <!-- Title if current user is profile owner -->
        <div v-if="selfView" class="d-flex flex-row justify-content-between align-items-center">
            <h4 class="fw-bold text-start">Your Events</h4>

            <!-- Create event button -->
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16" data-bs-toggle="modal" data-bs-target="#createEventModal" 
             :style="{cursor: disableCreateButton ? 'not-allowed' : 'pointer', pointerEvents: disableCreateButton ? 'none' : 'auto'}">
                <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2"/>
            </svg>

        </div>


        <!-- Title if not current user -->
        <div v-else>
            <h4 class="fw-bold text-start">Upcoming Events</h4>
        </div>

        <!-- Cannot create event message -->
        <div v-if="!canCreateEvent" class="alert alert-danger" role="alert">
            {{ canCreateEventMessage }}
        </div>

        <!-- List of events -->
        <div class="row mt-1">
            <!-- No events added yet message -->
            <div v-if="events.length === 0" class="col-12">
                <p>No events added yet.</p>
            </div>

            <!-- List of events -->
            <div v-else class="col-12">

                <!-- Event details-->
                <div v-for="event in events" :key="event.id" class="text-start">
                    <!-- Banner -->
                    <div class="row rounded" style="height: 100px; width: auto; cursor: pointer;" @click="this.$router.push({ name: 'eventview', params: { eventID: event.id, eventName: event.eventName } })">
                        <img v-if="event.eventBanners" :src="event.eventBanners[0]" class="rounded img-fluid event-banner" alt="Event Banner">
                        <img v-else :src="defaultEventBanner" class="rounded img-fluid event-banner" alt="Event Banner">
                    </div>

                    <!-- Event name -->
                    <div class="row">
                        <p class="m-0 mt-2 hover-underline mobile-rating-smaller-text-2" style="cursor: pointer; " @click="this.$router.push({ name: 'eventview', params: { eventID: event.id, eventName: event.eventName } })">{{ event.eventName }}</p>
                    </div>

                    <!-- Event date and time -->
                    <div class="row mt-0 pt-0">
                        <p class="fw-normal small-text mobile-rating-smaller-text-2" style="color: #027562">
                            {{ formatDate(event.eventStartDate) }} 
                            <span v-if="event.eventStartTime"> , {{ formatTime(event.eventStartTime) }}</span>
                            <span v-if="event.eventEndTime"> - {{ formatTime(event.eventEndTime) }}</span>
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Create event modal start -->
        <div v-if="selfView" class="modal fade" id="createEventModal" tabindex="-1" aria-labelledby="createEventModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">

                    <div class="modal-header">
                        <h5 class="modal-title" id="createEventModalLabel">Create New Event</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div class="modal-body text-start">
                        <CreateEventPage @new-event="updateNewEvent"/>
                    </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" :disabled="disableButton">Close</button>
                        <button type="button" class="btn primary-btn-green" @click="createEvent" :disabled="disableButton">Create</button>
                    </div>
                </div>
            </div>  
        </div>
        <!-- Create event modal end -->
    </div>

</template>

<style scoped>
    .event-banner {
        object-fit: cover;
        width: 100%;
        height: 100%;
    }

    .small-text {
        font-size: 0.9rem; /* Adjust the size as needed */
    }

</style>


<script>
import CreateEventPage from './CreateEventPage.vue';
import { useToast } from 'vue-toastification';

export default {
    name: 'EventBox',
    components: {
        CreateEventPage
    },
    props: {
        selfView: {
            type: Boolean,
            required: true
        },
        targetUserID: {
            type: Number,
            required: true
        },
        targetUserType: {
            type: String,
            required: true
        }
    },
    data() {
        return {

            // Variable to store 
            events: [],

            // Variable to store current viewer user ID and type
            userID: null,
            userType: null,

            // Variable to disable button
            disableButton: false,

            // Variable to store new event details
            newEvent: null,

            // Variable to store default event banner
            defaultEventBanner: require("@/assets/defaultEventBanner.jpg"),

            // Variable to store can create event status and message 
            canCreateEvent: false,
            canCreateEventMessage: "",
            disableCreateButton: false

        }
    },
    methods: {
        // Function to get all events
        async getEvents() {
            try {
                let response;
                response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUserEvents/` + this.targetUserID + "/" + this.targetUserType + "/0");
                this.events = response.data;
                this.events = response.data.events;
            }
            catch (error) {
                console.error(error);
            }
        },

        // Function to get create event status
        async getCreateEventStatus() {
            try {
                let response;
                response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/canCreateEvents/` + this.userID + "/" + this.userType);
                this.canCreateEvent = response.data.canCreate;

                if (this.canCreateEvent) {
                    this.disableCreateButton = false;
                }
                else {
                    this.disableCreateButton = true;
                }

                this.canCreateEventMessage = response.data.message;
            }
            catch (error) {
                console.error(error);
            }
        },

        // Function to change date "YYYY-MM-DD" to "DD Month YYYY"
        formatDate(date) {
            const options = { day: 'numeric', month: 'long', year: 'numeric' };
            // toLocaleDateString() function converts a date to a string based on the specified locale and formatting options. The first argument is the locale (region), and the second argument is an object specifying the desired format for the date components (e.g., day, month, year).
            return new Date(date).toLocaleDateString("en-GB", options);
        },

        // Function to convert 24-hour time to 12-hour time with AM/PM
        formatTime(time) {
            const [hour, minute] = time.split(':');
            const ampm = hour >= 12 ? 'PM' : 'AM';
            const formattedHour = hour % 12 || 12; // Convert 0 to 12 for 12 AM
            return `${formattedHour}:${minute} ${ampm}`;
        },

        // Update new event details
        updateNewEvent(event) {
            this.newEvent = event;
        },

        // Function to create a new event
        async createEvent() {

            // Check if user is logged in
            if (this.userType == "defaultUser") {
                // Redirect to login page
                this.$router.push({ name: 'login' });
            }

            this.disableButton = true;
            try {

                // Check if the start time is after the current time if the start date is today
                let todayDate = new Date().toISOString().split('T')[0];
                let currentTime = new Date().toTimeString().split(' ')[0];
                
                if (this.newEvent.eventStartDate == todayDate && this.newEvent.eventStartTime <= currentTime) {
                    alert("Start time must be after the current time.");
                    this.disableButton = false;
                    return;
                }

                // Check if the end time is after the start time
                if (this.newEvent.eventEndDate == this.newEvent.eventStartDate && this.newEvent.eventEndTime <= this.newEvent.eventStartTime) {
                    alert("End time must be after start time.");
                    this.disableButton = false;
                    return;
                }

                // Set boolean variables to true or false from string
                this.newEvent.ticketed = this.newEvent.ticketed == 'true';
                this.newEvent.paidEvent = this.newEvent.paidEvent == 'true';

                // Create a new event
                const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/events/createEvent`, {
                    eventName: this.newEvent.eventName,
                    eventDesc: this.newEvent.eventDescription,
                    eventType: this.newEvent.eventType,
                    eventStartDate: this.newEvent.eventStartDate,
                    eventEndDate: this.newEvent.eventEndDate,
                    eventStartTime: this.newEvent.eventStartTime,
                    eventEndTime: this.newEvent.eventEndTime,
                    eventLimit: this.newEvent.eventLimit,
                    eventBanners: this.newEvent.eventBanners,
                    ticketed: this.newEvent.ticketed,
                    paidEvent: this.newEvent.paidEvent,
                    eventLocation: this.newEvent.eventLocation,
                    paymentLink: this.newEvent.paymentLink,
                    eventOwnerID: this.userID,
                    eventOwnerType: this.userType
                });

                // Check if the event is created
                if (response.status == 201) {
                    const toast = useToast();
                    toast.success("Event created successfully.");
                    this.getEvents();

                    // Close modal
                    document.getElementById('createEventModal').classList.remove('show');
                    document.body.classList.remove('modal-open');
                    document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());

                    // Restore scrolling on the body
                    document.body.style.overflow = 'auto'; 
                    document.documentElement.style.overflow = 'auto';
                }
            }
            catch (error) {
                console.error(error);
                const toast = useToast();
                toast.error("Failed to create event.");
            }
        }
    },
    mounted() {
        this.getEvents();

        // Get current user ID and type
        this.userID = localStorage.getItem('88B_accID');
        let userType = localStorage.getItem('88B_accType');

        if (userType) {
            this.userType = userType;

            // Get create event status
            this.getCreateEventStatus();
        }
        else {
            this.userType = "defaultUser";
        }

    }
}
</script>