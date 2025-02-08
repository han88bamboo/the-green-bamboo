<template>
    <div class="mb-3">

        <NavBar />
        
        <!-- Display when data is still loading -->
        <div class="text-info-emphasis fst-italic fw-bold fs-5 pt-5" v-if="dataLoaded == false">
            <span>Loading page, please wait...</span>
            <br><br>
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <!-- Display when data fails to load-->
        <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="dataLoaded == null"> 
            <span>An error occurred while loading this page, please try again!</span>
            <br>
            <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
                <span class="fs-5 fst-italic"> Return to previous page </span>
            </button>
            <button class="btn primary-btn btn-sm mx-1" @click="this.$router.go(0)">
                <span class="fs-5 fst-italic"> Go to Home page </span>
            </button>
        </div>

        <!-- Display when data is loaded -->
        <!-- Main content -->
        <div v-if="dataLoaded" class="container-fluid mt-5 px-5 row">

            <!-- Search, create, upcoming, past, recommended events -->
            <div class="col-12 col-md-3">
                <!-- Header -->
                <div>
                    <h3 class="text-start fw-bold">Find events near you!</h3>
                </div>

                <!-- Search Input -->
                <div>
                    <div class="input-group mb-3 position-relative">
                        <input type="text" class="form-control rounded-pill" placeholder="Search for events" aria-label="Search for events" aria-describedby="search-event" v-model="searchQuery">
                        <!-- Search Icon -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-search position-absolute" viewBox="0 0 16 16" style="right: 10px; top: 50%; transform: translateY(-50%); cursor: pointer; z-index: 5;"
                            @click="searchEvents">
                            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                        </svg>
                    </div>
                </div> 

                <!-- Create Event Button -->
                <div class="text-start">
                    <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createEventModal">+ Create an Event</button>
                </div>

                <!-- Create Event modal -->
                <div class="modal fade" id="createEventModal" tabindex="-1" aria-labelledby="createEventModalLabel" aria-hidden="true">
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
                                <button type="button" class="btn primary-btn-green" data-bs-dismiss="modal" @click="createEvent" :disabled="disableButton">Create</button>
                            </div>
                        </div>
                    </div>  
                </div>

                <!-- Your Upcoming events -->
                <div v-if="upcomingEvents.length > 0" class="mt-3">
                    <h3 class="text-start fw-bold">Your Upcoming Events <button v-if="pastEvents.length > 5" type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#upcomingEventsModal">View All</button></h3>

                    <div v-for="event in upcomingEvents" class="mt-3 row" :key="event.eventID">
                        
                        <!-- Column 1: banner -->
                        <div class="col-12 col-lg-6" style="max-height: 200px;">
                            <img v-if="event.eventBanners" :src="event.eventBanners[0]" class="img-fluid event-banner" alt="Event Banner" style="object-fit: contain; max-height: 100%;">
                            <img v-else :src="defaultEventBanner" class="img-fluid event-banner" alt="Event Banner" style="object-fit: contain; max-height: 100%;">
                        </div>

                        <!-- Column 2: -->
                        <div class="col-12 col-lg-6 text-start">
                            <!-- Event Name -->
                            <p class="fw-bold">
                                <router-link :to="{ name: 'eventview', params: { eventID: event.eventID } }" class="text-black fs-4">
                                    {{ event.eventName }}
                                </router-link>
                            </p>

                            <!-- Event Details -->
                            <p class="text-success">
                               Happening {{ formatDate(event.eventStartDate) }} | {{ formatTime(event.eventStartTime) }} - {{ formatTime(event.eventEndTime) }} | {{ event.eventType }}
                            </p>

                        </div>
                    </div>
                </div>

                <!-- Error message for error retrieving upcoming events -->
                <div v-if="upcomingEventsError" class="mt-3">
                    <h2>{{ upcomingEventsError }}</h2>
                </div>


                <!-- Upcoming events modal -->
                <div class="modal fade" id="upcomingEventsModal" tabindex="-1" aria-labelledby="upcomingEventsModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-scrollable modal-xl">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="upcomingEventsModalLabel">Your Upcoming Events</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <div class="row">
                                </div>
                                
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Past events -->
                <div v-if="pastEvents.length > 0" class="mt-3">
                    <h3 class="text-start fw-bold">Past Events <button v-if="pastEvents.length > 5" type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#pastEventsModal">View All</button></h3>
                    
                </div>

                <!-- Error message for error retrieving past events -->
                <div v-if="pastEventsError" class="mt-3">
                    <h2>{{ pastEventsError }}</h2>
                </div>

                <!-- Past events modal -->
                <div class="modal fade" id="pastEventsModal" tabindex="-1" aria-labelledby="pastEventsModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-scrollable modal-xl">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="pastEventsModalLabel">Past Events</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <div class="row">
                                    
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            </div>  
                        </div>  
                    </div>  
                </div>

                <!-- Recommended Events -->
                <h3 class="text-start fw-bold mt-3">Recommended Events </h3>
                <div v-if="recommendedEvents.length > 0">

                </div>

                <!-- Error message for error retrieving recommended events -->
                <div v-if="recommendedEventsError" class="mt-3">
                    <h2>{{ recommendedEventsError }}</h2>
                </div>
            </div>

            <!-- Trending events and events from brands/venues you follow -->
            <div class="col-12 col-md-9">

                <!-- Search Term Text -->

                <!-- Search Results -->

                <!-- Trending events -->
                <h3 class="text-start fw-bold text-decoration-underline">Trending Events</h3>
                <div v-if="trendingEvents.length > 0 && !searchQuery">   
                </div>

                <!--- Error message for error retrieving recent activity or no recent activtiy found -->
                <div v-if="trendingEventsError" class="mt-3">
                    <h2>{{ trendingEventsError }}</h2>
                    <hr>
                </div>

                <!-- Display no results found if search term does not exist in any of the clubs -->
                <div v-if="searchResults && searchQuery" class="mt-3 text-start">
                    <p class="fw-bold">{{ searchResults }}</p>
                </div>

                <!-- Events from Brands/Venues You Follow  --> 
                <h3 class="text-start fw-bold text-decoration-underline">Events from Brands / Venues You Follow</h3>
                <div v-if="followedEvents && !searchQuery" class="row mt-3">
                    
                </div>

                
            </div>
        </div>

    </div>

</template>

<script>
import { useToast } from 'vue-toastification';
import NavBar from '@/components/NavBar.vue';
import CreateEventPage from '@/components/CreateEventPage.vue';


export default {
    name: 'EventsPage',
    components: {
        NavBar,
        CreateEventPage
    },
    data() {
        return {
            // Data
            dataLoaded: false,

            // Variable for user details
            userID: null,
            userType: null,

            // Variables for search
            searchQuery: '',

            // Variable to store default event banner
            defaultEventBanner: require("@/assets/defaultEventBanner.jpg"),

            // Variables for creating a new event
            newEvent: {
                eventName: '',
                eventDescription: '',
                eventType: '',
                eventStartDate: '',
                eventEndDate: '',
                eventStartTime: '',
                eventEndTime: '',
                eventLimit: '',
                eventBanners: '',
                ticketed: '',
                paidEvent: '',
                eventLocation: '',
                paymentLink: ''
            },
            disableButton: false,

            // Variable for events lists and respective offsets and respective error messages
            upcomingOffset: 0,
            upcomingEvents: [],
            upcomingEventsError: null,

            pastEventsOffset: 0,
            pastEvents: [],
            pastEventsError: null,

            recommendedEvents: [],
            recommendedEventsError: null,

            trendingEvents: [],
            trendingEventsError: null,

            followedEvents: [],
            followedEventsError: null,
        }
    },
    methods: {
        // Function to get upcoming events 
        async getUpcomingEvents() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUserUpcomingEvents/${this.userID}/${this.upcomingOffset}`);
                this.upcomingEvents = response.data.events;
                this.dataLoaded = true;
            }
            catch (error) {
                if (error.response.status == 404) {
                    this.upcomingEventsError = "No upcoming events found.";
                }
                else {
                    this.upcomingEventsError = "Failed to retrieve upcoming events.";
                }
                console.error(error);
            }
        },

        // Function to get past events
        async getPastEvents() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUserPastEvents/${this.userID}/${this.pastEventsOffset}`);
                this.pastEvents = response.data.events;
                this.dataLoaded = true;
            }
            catch (error) {
                if (error.response.status == 404) {
                    this.pastEventsError = "No past events found.";
                }
                else {
                    this.pastEventsError = "Failed to retrieve past events.";
                }
                console.error(error);
            }
        },

        // Function to get recommended events (as of now is getting recently created events)
        async getRecommendEvents() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getRecentlyAddedEvents`);
                this.recommendedEvents = response.data.events;
                this.dataLoaded = true;
            }
            catch (error) {
                if (error.response.status == 404) {
                    this.recommendedEventsError = "No recommended events found.";
                }
                else {
                    this.recommendedEventsError = "Failed to retrieve recommended events.";
                }
                console.error(error);
            }
        },

        // Function to get trending events
        async getTrendingEvents() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getTop6Events`);
                this.trendingEvents = response.data.events;
                this.dataLoaded = true;
            }
            catch (error) {
                if (error.response.status == 404) {
                    this.trendingEventsError = "No trending events found.";
                }
                else {
                    this.trendingEventsError = "Failed to retrieve trending events.";
                }
                console.error(error);
            }
        },

        // Function to get followed events
        async getFollowedEvents() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUpcomingFollowingEvents/${this.userID}/${this.userType}`);
                this.followedEvents = response.data.events;
                this.dataLoaded = true;
            }
            catch (error) {
                if (error.response.status == 404) {
                    this.followedEventsError = "No followed events found.";
                }
                else {
                    this.followedEventsError = "Failed to retrieve followed events.";
                }
                console.error(error);
            }
        },

        // Function to search events
        searchEvents() {
        },

        // Function to change date "YYYY-MM-DD" to "DD Month YYYY"
        formatDate(date) {
            // toLocaleDateString() function converts a date to a string based on the specified locale and formatting options. The first argument is the locale (region), and the second argument is an object specifying the desired format for the date components (e.g., day, month, year).
            
            const options = { day: 'numeric', month: 'long', year: 'numeric' };
            const weekdayOptions = { weekday: 'long' };
            
            const dateString = new Date(date).toLocaleDateString("en-GB", options);
            const weekdayString = new Date(date).toLocaleDateString("en-GB", weekdayOptions);
            
            return `${dateString}, ${weekdayString}`;
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
                    return;
                }

                // Check if the end time is after the start time
                if (this.newEvent.eventEndDate == this.newEvent.eventStartDate && this.newEvent.eventEndTime <= this.newEvent.eventStartTime) {
                    alert("End time must be after start time.");
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
        this.getRecommendEvents();
        this.getTrendingEvents();
        // Get the account id and type of the user
        this.userID = localStorage.getItem("88B_accID");
        let userType = localStorage.getItem("88B_accType");

        if (userType) {
            this.userType = userType;
        }

        this.getUpcomingEvents();
        this.getPastEvents();
        this.getFollowedEvents();
    }
}
</script>

<style>
/* Resize Quill toolbar icons */
.ql-toolbar .ql-formats svg {
width: 20px;
height: 20px;
}

/* Resize SVGs inside the content */
.ql-editor svg {
width: 20px;
height: 20px;
}
</style>