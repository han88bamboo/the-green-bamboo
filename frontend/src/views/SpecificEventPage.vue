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

        <!-- Main Content -->
        <div v-if="dataLoaded">
            <div v-if="selfView" class="container mt-3 mb-3">
                <button class="btn primary-btn me-3">Edit Event</button>
                <button class="btn primary-btn-red">Delete Event</button>
            </div>

            <div class="container-fluid">
                
                <!-- Event banner -->
                <div class="row d-flex justify-content-center align-items-center">
                    
                    <!-- Banner carousel if there are more than 1 event banner provided -->
                    <div v-if="event.eventBanners" id="eventBannerCarousel" chan class="carousel slide" data-bs-ride="carousel" style="height: 500px; width: 600px">
                        <div class="carousel-inner h-100">
                            <div v-for="(banner, index) in event.eventBanners" :key="index" class="carousel-item" :class="{ active: index == 0 }">
                                <div class="d-flex justify-content-center align-items-center h-100">
                                    <img :src="banner" class="d-block event-banner" alt="Event Banner">
                                </div>
                            </div>
                        </div>
                        <button class="carousel-control-prev" type="button" data-bs-target="#eventBannerCarousel" data-bs-slide="prev">
                            <span class="carousel-control-prev-icon custom-carousel-color" aria-hidden="true"></span>
                            <span class="visually-hidden">Previous</span>
                        </button>
                        <button class="carousel-control-next" type="button" data-bs-target="#eventBannerCarousel" data-bs-slide="next">
                            <span class="carousel-control-next-icon custom-carousel-color" aria-hidden="true"></span>
                            <span class="visually-hidden">Next</span>
                        </button>
                    </div>

                    <img v-else :src="defaultEventBanner" style="height: 500px; width: 600px" class="img-fluid event-banner" alt="Event Banner">
                </div>
            </div>

            <div class="container mt-3">

                <div class="row text-start">
                    <!-- Column 1 -->
                    <div class="col-12 col-md-8">
                        <!-- Event Start Date, End Date, Start Time and End Time -->
                        <div v-if="event.eventStartDate = event.eventEndDate" class="row m-0 p-0">
                            <p class="fw-bold p-0">{{ formatDate(event.eventStartDate) }}, {{ formatTime(event.eventStartTime )}} - {{ formatTime(event.eventEndTime )}}</p>
                        </div>

                        <div v-else class="row m-0 p-0">
                            <p class="fw-bold p-0">{{ formatDate(event.eventStartDate) }} - {{ formatDate(event.eventEndDate) }}, {{ formatTime(event.eventStartTime )}} - {{ formatTime(event.eventEndTime )}}</p>
                        </div>

                        <!-- Event Name -->
                        <h4 class="fw-bold">{{ event.eventName }}</h4>

                        <!-- Organizer Info -->
                        <div class="d-flex justify-content-between align-items-center p-3 mt-3" style="background-color: #83A9E8;">
                            <div class="ms-5 fw-bold d-flex align-items-center"> 
                                <p v-if="event.eventOwnerType =='venue'" class="m-0">Organized by: 
                                    <router-link :to="profileURL(event.ownerInfo.id, event.ownerInfo.userType)">
                                        <span class="text-decoration-underline" >{{ event.ownerInfo.venueName }}</span>
                                    </router-link>
                                </p>
                                <p v-if="event.eventOwnerType =='producer'" class="m-0">Organized by: 
                                    <router-link :to="profileURL(event.ownerInfo.id, event.ownerInfo.userType)">
                                        <span class="text-decoration-underline" >{{ event.ownerInfo.producerName }}</span>
                                    </router-link>
                                </p>
                                <p v-if="event.eventOwnerType =='user'" class="m-0">Organized by: 
                                    <router-link :to="profileURL(event.ownerInfo.id, event.ownerInfo.userType)">
                                        <span class="text-decoration-underline" >{{ event.ownerInfo.displayName }}</span>
                                    </router-link>
                                </p>
                            </div>
                            <button v-if="!selfView" class="btn primary-btn-green">Follow</button>

                        </div>

                        <!-- Event Description -->
                        <h4 class="fw-bold mt-5">About This Event:</h4>
                        <p>{{ event.eventDesc }}</p>

                        <!-- Event attendees -->
                        <div class="d-flex justify-content-between align-items-center mt-5">
                            <h4 class="fw-bold">Who's Going?</h4>
                            <!-- Invite button -->
                            <button class="ps-0 btn d-flex flex-row align-items-center hover-underline ">
                                <!-- Invite icon -->
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-share" viewBox="0 0 16 16">
                                    <path d="M13.5 1a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3M11 2.5a2.5 2.5 0 1 1 .603 1.628l-6.718 3.12a2.5 2.5 0 0 1 0 1.504l6.718 3.12a2.5 2.5 0 1 1-.488.876l-6.718-3.12a2.5 2.5 0 1 1 0-3.256l6.718-3.12A2.5 2.5 0 0 1 11 2.5m-8.5 4a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3m11 5.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3"/>
                                </svg>
                                <!-- Invite text -->
                                <span class="ms-2">Invite your friends!</span>
                            </button>
                        </div>

                        <!-- Error message if fail to retrieve attendee information -->
                        <p class="text-danger" v-if="attendeesError">{{ attendeesError }}</p>

                        <!-- List of attendees -->
                        <div v-if="attendees.length > 0" class="row mt-3 d-flex justify-content-start align-items-center">

                            <div v-for="attendee in attendees.slice(0, 5)" :key="attendee.id" class="col-4 col-lg-2">
                                <div class="d-flex flex-column justify-content-start align-items-center">
                                    <img v-if="attendee.profilePic" :src="attendee.profilePic" class="img-fluid rounded-circle" alt="Profile Picture">
                                    <svg v-else xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                                        <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                                        <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                                    </svg>
                                    <router-link :to="profileURL(attendee.id, attendee.userType)">
                                        <p v-if="attendee.userType == 'user'" class="ms-2">{{ attendee.displayName }}</p>
                                        <p v-if="attendee.userType == 'venue'" class="ms-2">{{ attendee.venueName }}</p>
                                        <p v-if="attendee.userType == 'producer'" class="ms-2">{{ attendee.producerName }}</p>
                                    </router-link>
                                </div>
                            </div>

                            <!-- See More Icon -->
                            <div v-if="attendees.length > 5" class="d-flex justify-content-center align-items-center col-4 col-lg-2" style="cursor: pointer;" data-bs-toggle="modal" data-bs-target="#attendeesModal">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-plus-circle-dotted" viewBox="0 0 16 16">
                                    <path d="M8 0q-.264 0-.523.017l.064.998a7 7 0 0 1 .918 0l.064-.998A8 8 0 0 0 8 0M6.44.152q-.52.104-1.012.27l.321.948q.43-.147.884-.237L6.44.153zm4.132.271a8 8 0 0 0-1.011-.27l-.194.98q.453.09.884.237zm1.873.925a8 8 0 0 0-.906-.524l-.443.896q.413.205.793.459zM4.46.824q-.471.233-.905.524l.556.83a7 7 0 0 1 .793-.458zM2.725 1.985q-.394.346-.74.74l.752.66q.303-.345.648-.648zm11.29.74a8 8 0 0 0-.74-.74l-.66.752q.346.303.648.648zm1.161 1.735a8 8 0 0 0-.524-.905l-.83.556q.254.38.458.793l.896-.443zM1.348 3.555q-.292.433-.524.906l.896.443q.205-.413.459-.793zM.423 5.428a8 8 0 0 0-.27 1.011l.98.194q.09-.453.237-.884zM15.848 6.44a8 8 0 0 0-.27-1.012l-.948.321q.147.43.237.884zM.017 7.477a8 8 0 0 0 0 1.046l.998-.064a7 7 0 0 1 0-.918zM16 8a8 8 0 0 0-.017-.523l-.998.064a7 7 0 0 1 0 .918l.998.064A8 8 0 0 0 16 8M.152 9.56q.104.52.27 1.012l.948-.321a7 7 0 0 1-.237-.884l-.98.194zm15.425 1.012q.168-.493.27-1.011l-.98-.194q-.09.453-.237.884zM.824 11.54a8 8 0 0 0 .524.905l.83-.556a7 7 0 0 1-.458-.793zm13.828.905q.292-.434.524-.906l-.896-.443q-.205.413-.459.793zm-12.667.83q.346.394.74.74l.66-.752a7 7 0 0 1-.648-.648zm11.29.74q.394-.346.74-.74l-.752-.66q-.302.346-.648.648zm-1.735 1.161q.471-.233.905-.524l-.556-.83a7 7 0 0 1-.793.458zm-7.985-.524q.434.292.906.524l.443-.896a7 7 0 0 1-.793-.459zm1.873.925q.493.168 1.011.27l.194-.98a7 7 0 0 1-.884-.237zm4.132.271a8 8 0 0 0 1.012-.27l-.321-.948a7 7 0 0 1-.884.237l.194.98zm-2.083.135a8 8 0 0 0 1.046 0l-.064-.998a7 7 0 0 1-.918 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
                                </svg>
                                <span class="ms-2 hover-underline">See more</span>
                            </div>

                            <!-- Start of list of attendees Modal -->
                            <div class="modal fade" id="attendeesModal" tabindex="-1" aria-labelledby="attendeesModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-dialog-centered">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" id="attendeesModalLabel">Attendees</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">

                                            <!-- Show full list of attendees -->
                                            <div class="row">
                                                <div v-for="attendee in attendees" :key="attendee.id" class="col-4">
                                                    <div class="d-flex flex-column justify-content-start align-items-center position-relative">
                                                        <img v-if="attendee.profilePic" :src="attendee.profilePic" class="img-fluid rounded-circle" alt="Profile Picture">
                                                        <svg v-else xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                                                            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                                                            <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                                                        </svg>
                                                        <router-link :to="profileURL(attendee.id, attendee.userType)">
                                                            <p v-if="attendee.userType == 'user'" class="ms-2">{{ attendee.displayName }}</p>
                                                            <p v-if="attendee.userType == 'venue'" class="ms-2">{{ attendee.venueName }}</p>
                                                            <p v-if="attendee.userType == 'producer'" class="ms-2">{{ attendee.producerName }}</p>
                                                        </router-link>

                                                        <!-- Button to remove the attendee -->
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="red" 
                                                            class="bi bi-x-circle-fill position-absolute top-0 end-0" viewBox="0 0 16 16"
                                                            style="cursor: pointer;">
                                                            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/>
                                                        </svg>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- End of List of attendees Modal -->
                        </div>

                        <!-- No attendees yet message -->
                        <p v-else class="mt-3">No attendees yet.</p>

                        <!-- More events by organiser -->
                        <div class="mt-5">
                            <h4 v-if="event.eventOwnerType == 'venue'" class="fw-bold">More Events by {{ event.ownerInfo.venueName }}</h4>
                            <h4 v-if="event.eventOwnerType == 'producer'" class="fw-bold">More Events by {{ event.ownerInfo.producerName }}</h4>
                            <h4 v-if="event.eventOwnerType == 'user'" class="fw-bold">More Events by {{ event.ownerInfo.displayName }}</h4>
                        </div>

                        <!-- Other events list -->
                        <div v-if="!otherEventsError" class="row mt-3">
                            <div v-if="otherEvents.length > 0" class="row">
                                <div v-for="otherEvent in otherEvents" :key="otherEvent.id" class="col-6">
                                    <div class="d-flex flex-column justify-content-start align-items-center">

                                        <!-- Banner -->
                                        <div class="row" style="height: 150px; width: auto; cursor: pointer;">
                                            <img v-if="otherEvent.eventBanners" :src="otherEvent.eventBanners[0]" class="img-fluid event-banner" alt="Event Banner">
                                            <img v-else :src="defaultEventBanner" class="img-fluid event-banner" alt="Event Banner">
                                        </div>
                                        
                                        <!-- Event Name -->
                                        <router-link :to="{ name: 'eventview', params: { eventID: otherEvent.id } }">
                                            <p class="m-0">{{ otherEvent.eventName }}</p>
                                        </router-link>

                                        <!-- Event date and time -->
                                        <p class="fw-normal small-text">{{ formatDate(otherEvent.eventStartDate) }}, {{ formatTime(otherEvent.eventStartTime) }} - {{ formatTime(otherEvent.eventEndTime) }}</p>
                                    </div>
                                </div>
                            </div>
                            <p v-else>No other events yet.</p>
                        </div>

                        <!-- Error message if fail to retrieve other events information -->
                        <p class="text-danger" v-if="otherEventsError">{{ otherEventsError }}</p>
                        
                    </div>

                    <!-- Column 2 -->
                    <div class="cold 12 col-md-4">

                        <!-- Event Location -->
                        <h4 class="fw-bold mt-5">Event Location</h4>
                        <p>{{ event.eventLocation }}</p>

                        <!-- Get Event Tickets -->
                        <h4 class="fw-bold mt-5">Get Tickets</h4>

                        <!-- No tickets require -->
                        <p v-if="ticketed == false" class="fw-bold">This event is not ticketed. Walk ins welcome!</p>
                        <div v-else>

                            <!-- Ticketed but free of charge -->
                            <div v-if="event.paidEvent == false">
                                <p class="fw-bold">This event is ticketed. Entry is free but click below to RSVP and save your spot!</p>
                                <!-- button to RSVP -->
                                <button v-if="attendees.length <= (event.eventLimit - 5)" class="btn primary-btn-green">RSVP</button>
                                <p v-else class="text-danger">Event is full. No more RSVPs allowed.</p>
                            </div>

                            <!-- Ticketed and require payment -->
                            <div v-else>
                                <p class="fw-bold">This event is ticketed. Click below to purchase your ticket!</p>
                                <!-- button to purchase ticket -->
                                <a :href="ticketLink" :target="event.paymentLink" class="btn primary-btn-green">Buy Ticket</a>
                            </div>
                            
                        </div>
                    </div>
                </div>
                
            </div>
            
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
    name: 'SpecificEventPage',
    components: {
        NavBar,
    },
    data() {
        return {
            // Variable to store page loading status
            dataLoaded: false,

            // Variable to store current user ID and user type
            userID: null,
            userType: null,

            // Variable to store self view status
            selfView: false,

            // Event ID
            eventID: this.$route.params.eventID,

            // Variable to store event details
            event: {},
            attendees: [],

            // Variable to store message to display when error occurs for attendees
            attendeesError: null,

            // Variable to store default event banner
            defaultEventBanner: require("@/assets/defaultEventBanner.jpg"),

            // Variable to store other events by the same organizer
            otherEvents: [],
            otherEventsError: null,

        }
    },
    methods: {
        // Function to get event information
        async getEvent() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getSpecificEvent/` + this.$route.params.eventID);
                this.event = response.data.event;
                this.dataLoaded = true;

                this.getOtherEvents();

                // Check if the user is viewing their own events
                if (this.userID == this.event.ownerInfo.id && this.userType == this.event.eventOwnerType) {
                    this.selfView = true;
                }
            }
            catch (error) {
                console.log(error);
                this.dataLoaded = null;
            }
        },

        // Function to get attendees information for current event
        async getAttendees() {
            try {
                let response;
                response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getAttendees/` + this.$route.params.eventID);
                this.attendees = response.data.attendees;
            }
            catch (error) {
                this.attendeesError = "An error occurred while loading attendees, please try again!";
                console.log(error);
            }
        },

        // Function to get other events by the same organizer
        async getOtherEvents() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUserEvents/` + this.event.ownerInfo.id + "/" + this.event.eventOwnerType + "/0");
                this.otherEvents = response.data.events;

                // Remove the current event from the list of other events
                this.otherEvents = this.otherEvents.filter(event => event.id != this.event.id);
            }
            catch (error) {
                this.otherEventsError = "An error occurred while loading other events, please try again!";
                console.log(error);
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

        // Function to get the profile URL of the poster 
        profileURL(posterID, userType) {
            if (userType == 'user') {
                return `/profile/user/${posterID}`;
            }
            else if (userType == 'producer') {
                return `/profile/producer/${posterID}`;
            }
            else {
                return `/profile/venue/${posterID}`;
            }

        },
    },
    watch: {
        '$route.params.eventID': {
            immediate: true, // Trigger immediately on component load
            handler(newId) {
                if (newId) {
                    console.log(`Route ID changed to: ${newId}`);
                    this.getEvent();
                    this.getAttendees();
                } else {
                    console.error('New route ID is undefined');
                }
            },
        },
    },
    mounted() {
        // Get the current user's ID and user type
        this.userID = localStorage.getItem("88B_accID");
        let userType = localStorage.getItem("88B_accType");

        if (userType) {
            this.userType = userType;
        }
        else {
            this.userType = 'defaultUser';
        }

        this.getEvent();
        this.getAttendees();
    }
}
</script>

<style scoped>
.event-banner {
    object-fit: cover;
    max-height: 100%;
    max-width: 100%;
}

.carousel-item {
    height: 100%;
}

.custom-carousel-color {
    background-color: #ff0000; 
}
</style>
