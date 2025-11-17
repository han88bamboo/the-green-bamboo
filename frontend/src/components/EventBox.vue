<template>
    <div class="square primary-square-green-outline rounded p-3 mb-3">

        <!-- Title if current user is profile owner -->
        <div v-if="selfView" class="d-flex flex-row justify-content-between align-items-center">
            <div>
                <h4 class="fw-bold text-start mb-0">Your Events</h4>
                <small v-if="events.length > 0" class="text-muted">
                    {{ events.length }} upcoming event{{ events.length === 1 ? '' : 's' }}
                    <span 
                        class="see-all-events-link ms-2" 
                        @click="openAllEventsModal"
                        style="cursor: pointer; text-decoration: underline;"
                    >
                        (See all events)
                    </span>
                </small>
            </div>

            <!-- Create event button 
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16" data-bs-toggle="modal" data-bs-target="#createEventModal" 
             :style="{cursor: disableCreateButton ? 'not-allowed' : 'pointer', pointerEvents: disableCreateButton ? 'none' : 'auto'}">
                <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2"/>
            </svg>-->

        </div>


        <!-- Title if not current user -->
        <div v-else>
            <h4 class="fw-bold text-start mb-0 mobile-fs-5">Upcoming Events</h4>
            <small v-if="events.length > 0" class="text-muted">
                {{ events.length }} upcoming event{{ events.length === 1 ? '' : 's' }}
                <span 
                    class="see-all-events-link ms-2" 
                    @click="openAllEventsModal"
                    style="cursor: pointer; text-decoration: underline;"
                >
                    (See all events)
                </span>
            </small>
        </div>
 
        <!-- Cannot create event message
        <div v-if="!canCreateEvent" class="alert alert-danger" role="alert">
            {{ canCreateEventMessage }}
        </div> -->

        <!-- Navigation buttons (only show if more than 4 events) -->
        <div v-if="events.length > 4" class="d-flex justify-content-end gap-2 mb-2">
            <!-- Left Arrow in Circle -->
            <button
                class="d-flex align-items-center justify-content-center rounded-circle border-0"
                style="width: 36px; height: 36px; background-color: #f0f0f0;"
                type="button"
                :data-bs-target="'#eventsCarousel' + targetUserID"
                data-bs-slide="prev"
            >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-chevron-left" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L6.707 7l4.647 4.646a.5.5 0 0 1-.708.708l-5-5a.5.5 0 0 1 0-.708l5-5a.5.5 0 0 1 .708 0z"/>
                </svg>
            </button>

            <!-- Right Arrow in Circle -->
            <button
                class="d-flex align-items-center justify-content-center rounded-circle border-0"
                style="width: 36px; height: 36px; background-color: #f0f0f0;"
                type="button"
                :data-bs-target="'#eventsCarousel' + targetUserID"
                data-bs-slide="next"
            >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-chevron-right" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l5 5a.5.5 0 0 1 0 .708l-5 5a.5.5 0 0 1-.708-.708L9.293 7 4.646 2.354a.5.5 0 0 1 0-.708z"/>
                </svg>
            </button>
        </div>

        <!-- List of events -->
        <div class="row mt-1">
            <!-- No events added yet message -->
            <div v-if="events.length === 0" class="col-12 text-start fw-normal mt-1">
                <p>No events added yet.</p>
            </div>

            <!-- Events Carousel -->
            <div v-else class="col-12">
                <div :id="'eventsCarousel' + targetUserID" class="carousel slide events-carousel" data-bs-ride="carousel">
                    <div class="carousel-inner">
                        <div
                            v-for="(chunk, chunkIndex) in eventChunks"
                            :key="chunkIndex"
                            :class="['carousel-item', chunkIndex === 0 ? 'active' : '']"
                        >
                            <!-- Event details for this chunk -->
                            <div v-for="event in chunk" :key="event.id" class="text-start mb-1">
                                <!-- Banner -->
                                <div class="row rounded" style="height: 100px; width: auto; cursor: pointer;" @click="this.$router.push({ name: 'eventview', params: { eventID: event.id, eventName: slugify(event.eventName) } })">
                                    <img v-if="event.eventBanners" :src="event.eventBanners[0]" class="rounded img-fluid event-banner" alt="Event Banner">
                                    <img v-else :src="defaultEventBanner" class="rounded img-fluid event-banner" alt="Event Banner">
                                </div>

                                <!-- Event name -->
                                <div class="row">
                                    <p class="m-0 mt-2 hover-underline mobile-rating-smaller-text-2" style="cursor: pointer;" @click="this.$router.push({ name: 'eventview', params: { eventID: event.id, eventName: slugify(event.eventName) } })">{{ event.eventName }}</p>
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

                    <!-- Dot indicators (only show if more than 4 events) -->
                    <div v-if="events.length > 4" class="carousel-indicators-custom">
                        <button
                            v-for="(chunk, index) in eventChunks"
                            :key="index"
                            type="button"
                            :data-bs-target="'#eventsCarousel' + targetUserID"
                            :data-bs-slide-to="index"
                            :class="{ active: index === 0 }"
                            :aria-label="'Slide ' + (index + 1)"
                        ></button>
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

        <!-- All Events Modal -->
        <div 
            v-if="showAllEventsModal"
            class="modal d-block" 
            :id="'allEventsModal' + targetUserID" 
            style="background-color: rgba(0, 0, 0, 0.5); position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1050;"
        >
            <div class="modal-dialog modal-xl" style="margin: 10vh auto;">
                <div class="modal-content">
                    <div class="modal-header" style="background-color: #f0b358">
                        <h5 class="modal-title" :id="'allEventsModalLabel' + targetUserID" style="color: black; font-weight: bold;">
                            All Events by {{ getVenueName() }}
                        </h5>
                        <button type="button" class="btn-close" @click="closeAllEventsModal" aria-label="Close"></button>
                    </div>
                    
                    <div class="modal-body px-4">
                        <!-- Loading spinner -->
                        <div v-if="allEventsLoading" class="text-center py-5">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Loading events...</span>
                            </div>
                            <p class="mt-3 text-muted">Loading all events...</p>
                        </div>

                        <!-- All Events Grid -->
                        <div v-else-if="allEvents.length > 0" class="row">
                            <div v-for="event in allEvents" :key="event.id" class="col-6 col-sm-4 col-lg-3 mb-3 px-2">
                                <div class="d-flex flex-column h-100 event-card-container rounded-4 shadow-sm p-3">
                                    <!-- Banner -->
                                    <div class="event-banner-container mb-2" style="cursor: pointer; aspect-ratio: 2 / 1; overflow: hidden;" @click="navigateToEvent(event)">
                                        <img
                                            v-if="event.eventBanners"
                                            :src="event.eventBanners[0]"
                                            alt="Event Banner"
                                            class="w-100 h-100 rounded"
                                            style="object-fit: cover;"
                                        />
                                        <img
                                            v-else
                                            :src="defaultEventBanner"
                                            alt="Event Banner"
                                            class="w-100 h-100 rounded"
                                            style="object-fit: cover;"
                                        />
                                    </div>
                                    
                                    <!-- Event content (grows to fill available space) -->
                                    <div class="flex-grow-1 d-flex flex-column justify-content-between">
                                        <div>
                                            <!-- Event Name -->
                                            <div @click="navigateToEvent(event)" style="cursor: pointer;" class="text-center mb-2">
                                                <p class="m-0 fw-semibold mobile-rating-smaller-text-2 event-title" style="color: black; line-height: 1.3;">
                                                    <span v-if="isEventPast(event)" class="text-muted">[Event Ended] </span>{{ event.eventName }}
                                                </p>
                                            </div>

                                            <!-- Event date and time -->
                                            <p class="fw-normal mobile-rating-smaller-text-2 text-center mb-3" style="color: #027562">
                                                {{ formatDate(event.eventStartDate) }}<span v-if="event.eventStartTime">, {{ formatTime(event.eventStartTime) }}</span><span v-if="event.eventEndTime"> - {{ formatTime(event.eventEndTime) }}</span>
                                            </p>
                                        </div>

                                        <!-- View Event button (always at bottom) -->
                                        <div class="text-center">
                                            <button @click="navigateToEvent(event)" class="btn btn-read-more btn-sm fw-bold rounded-pill mobile-pb-1 mobile-pt-1 mobile-fs-7">
                                                View Event
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- No events message -->
                        <div v-else class="text-center py-5">
                            <p class="text-muted">No events found.</p>
                        </div>
                    </div>
                    
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="closeAllEventsModal">Close</button>
                    </div>
                </div>
            </div>
        </div>
        <!-- All Events Modal End -->
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

    .events-carousel {
        max-height: 900px;
        overflow: hidden;
    }

    .carousel-item {
        padding: 10px 0;
    }

    /* Custom dot indicators styling */
    .carousel-indicators-custom {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-top: 15px;
        margin-bottom: 0;
    }

    .carousel-indicators-custom button {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        border: none;
        background-color: #d1d5db;
        opacity: 0.5;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .carousel-indicators-custom button.active {
        background-color: #6b7280;
        opacity: 1;
        transform: scale(1.2);
    }

    .carousel-indicators-custom button:hover {
        opacity: 0.8;
    }

    /* Event card alignment styles - Responsive */
    .event-card-container {
        transition: transform 0.2s ease-in-out;
    }

    .event-card-container:hover {
        transform: translateY(-2px);
    }

    .event-title {
        line-height: 1.3;
        word-wrap: break-word;
        hyphens: auto;
    }

    .event-banner-container {
        flex-shrink: 0; /* Prevent banner from shrinking */
    }

    /* Large devices (col-lg-3) - 4 cards per row */
    @media (max-width: 991px)  {
        .event-card-container {
            min-height: 230px;
        }
        .event-title {
            font-size: 0.95rem;
        }
    }

    /* Extra large devices (col-lg-3) - 4 cards per row with more space */
    @media (min-width: 992px) {
        .event-card-container {
            min-height: 310px;
        }
        .event-title {
            font-size: 1rem;
        }
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
        },
        targetUserName: {
            type: String,
            required: false,
            default: ''
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
            disableCreateButton: false,

            // Variables for all events modal
            allEvents: [],
            allEventsLoading: false,
            showAllEventsModal: false

        }
    },
    computed: {
        // Group events into chunks of 4 for carousel slides
        eventChunks() {
            return this.events.reduce((acc, cur, i) => {
                if (i % 4 === 0) acc.push([cur]);
                else acc[acc.length - 1].push(cur);
                return acc;
            }, []);
        }
    },
    methods: {
        
        slugify(text) {
            if (!text) return ""
            return text
                .toString()
                .toLowerCase()
                .normalize('NFD') // Decompose accented characters
                .replace(/[\u0300-\u036f]/g, '') // Remove diacritical marks
                .replace(/\s+/g, '-')                 // Replace spaces with hyphens
                .replace(/[^\w]/g, '') // Remove non-word characters
        },
        
        // Function to get all events
        async getEvents() {
            try {
                let response;
                response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUserEvents/` + this.targetUserID + "/" + this.targetUserType + "/0");
                this.events = response.data.events;
                
                // Ensure events are sorted chronologically (backend already does this, but adding as extra safety)
                this.events.sort((a, b) => {
                    const dateA = new Date(a.eventStartDate + (a.eventStartTime ? ' ' + a.eventStartTime : ''));
                    const dateB = new Date(b.eventStartDate + (b.eventStartTime ? ' ' + b.eventStartTime : ''));
                    return dateA - dateB;
                });
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
        },

        // Function to open all events modal and fetch all events
        async openAllEventsModal() {
            this.showAllEventsModal = true;
            this.allEventsLoading = true;
            
            try {
                // Try the new endpoint first, fallback to old endpoint if needed
                console.log('Chars Fetching all events for:', this.targetUserID, this.targetUserType);
                
                let response;
                try {
                    // Fetch ALL events (both past and upcoming) organized by this user
                    response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getAllUserEvents/${this.targetUserID}/${this.targetUserType}/0`);
                    console.log('New endpoint response:', response.data);
                } catch (newEndpointError) {
                    console.warn('New endpoint failed, falling back to original:', newEndpointError);
                    // Fallback to original endpoint if new one fails
                    response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUserEvents/${this.targetUserID}/${this.targetUserType}/0`);
                    console.log('Fallback endpoint response:', response.data);
                }
                
                this.allEvents = response.data.events || [];
                console.log('All events loaded:', this.allEvents.length);
                
                // Sort events chronologically (earliest first)
                this.allEvents.sort((a, b) => {
                    const dateA = new Date(a.eventStartDate + (a.eventStartTime ? ' ' + a.eventStartTime : ''));
                    const dateB = new Date(b.eventStartDate + (b.eventStartTime ? ' ' + b.eventStartTime : ''));
                    return dateA - dateB;
                });
            } catch (error) {
                console.error('Error fetching all events:', error);
                // Handle 404 gracefully (no events found)
                if (error.response && error.response.status === 404) {
                    console.log('No events found (404)');
                    this.allEvents = [];
                } else {
                    console.log('Other error occurred:', error.response?.status, error.message);
                    this.allEvents = [];
                }
            } finally {
                this.allEventsLoading = false;
            }
        },

        // Function to close all events modal
        closeAllEventsModal() {
            this.showAllEventsModal = false;
        },

        // Function to check if an event is in the past
        isEventPast(event) {
            const now = new Date();
            const eventDate = new Date(event.eventStartDate + (event.eventStartTime ? ' ' + event.eventStartTime : ' 00:00'));
            return eventDate < now;
        },

        // Function to navigate to event page
        navigateToEvent(event) {
            this.$router.push({
                name: 'eventview',
                params: {
                    eventID: event.id,
                    eventName: this.slugify(event.eventName)
                }
            });
        },

        // Function to get venue name for modal title
        getVenueName() {
            if (this.targetUserName) {
                return this.targetUserName;
            }
            
            // Fallback to generic names if no name provided
            if (this.targetUserType === 'venue') {
                return 'This Venue';
            } else if (this.targetUserType === 'producer') {
                return 'This Producer';
            } else {
                return 'This User';
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