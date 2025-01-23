<template>
    <div class="square primary-square-green-outline rounded p-3 mb-3">

        <!-- Title if current user is profile owner -->
        <div v-if="selfView" class="d-flex flex-row justify-content-between align-items-center">
            <h3 class="m-0">Your Events</h3>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16" data-bs-toggle="modal" data-bs-target="#createEventModal" style="cursor: pointer;">
                <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2"/>
            </svg>
        </div>

        <!-- Title if not current user -->
        <div v-else>
            <h3>Upcoming Events</h3>
        </div>

        <!-- List of events -->
        <div class="row mt-3">
            <!-- No events added yet message -->
            <div v-if="events.length === 0" class="col-12">
                <p>No events added yet.</p>
            </div>

            <!-- List of events -->
            <div v-else class="col-12">

                <!-- Event details-->
                <div v-for="event in events" :key="event.id" class="text-start">
                    <!-- Banner -->
                    <div class="row" style="height: 100px; width: auto; cursor: pointer;" @click="this.$router.push({ name: 'eventview', params: { eventID: event.id } })">
                        <img v-if="event.eventBanners" :src="event.eventBanners[0]" class="img-fluid event-banner" alt="Event Banner">
                        <img v-else :src="defaultEventBanner" class="img-fluid event-banner" alt="Event Banner">
                    </div>

                    <!-- Event name -->
                    <div class="row">
                        <p class="m-0" style="cursor: pointer;" @click="this.$router.push({ name: 'eventview', params: { eventID: event.id } })">{{ event.eventName }}</p>
                    </div>

                    <!-- Event date and time -->
                    <div class="row mt-0 pt-0">
                        <p class=" fw-normal small-text">{{ formatDate(event.eventStartDate) }} , {{ formatTime(event.eventStartTime) }} - {{ formatTime(event.eventEndTime) }}</p>
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
                        <form>
                            <!-- Event name -->
                            <div class="mb-3">
                                <label for="eventName" class="form-label">Event Name:</label>
                                <input type="text" class="form-control" id="eventName" required v-model="newEvent.eventName">
                            </div>

                            <!-- Event description input editor -->
                            <p class="fw-bold">Event Description:</p>
                            <div id="editor-container" style="height: 300px;" class="mb-3"></div>

                            <div class="mb-3 row">
                                <!-- Event start date -->
                                <div class="col">
                                    <label for="eventStartDate" class="form-label">Event Start Date:</label>
                                    <input type="date" class="form-control" id="eventStartDate" required v-model="newEvent.eventStartDate" :min="new Date().toISOString().split('T')[0]"> 
                                </div>

                                <!-- Event start time -->
                                <div class="col">
                                    <label for="eventStartTime" class="form-label">Event Start Time:</label>
                                    <input type="time" class="form-control" id="eventStartTime" required v-model="newEvent.eventStartTime">
                                </div>
                            </div>

                         
                            <div class="mb-3 row">
                                <!-- Event end date -->
                                <div class="col">
                                    <label for="eventEndDate" class="form-label">Event End Date:</label>
                                    <input type="date" class="form-control" id="eventEndDate" required v-model="newEvent.eventEndDate" :min="newEvent.eventStartDate">
                                </div>

                                <!-- Event end time -->
                                <div class="col">
                                    <label for="eventEndTime" class="form-label">Event End Time:</label>
                                    <input type="time" class="form-control" id="eventEndTime" required v-model="newEvent.eventEndTime">
                                </div>
                            </div>

                            <!-- Event wallpaper upload -->
                            <div class="mb-3">
                                <label for="eventBanner" class="form-label">Add Event Wallpaper (upload up to 3 images):</label>
                                <input type="file" class="form-control" id="eventBanner" multiple accept="image/*" @change="uploadImages">
                            </div>

                            <!-- Display uploaded banners -->
                            <div v-if="newEvent.eventBanners.length > 0" class="mb-3 row">
                                <div v-for="(banner, index) in newEvent.eventBanners" :key="index" class="col-4 position-relative">
                                    <img :src="banner" class="img-fluid" alt="Event Banner">
                                    <button class="btn primary-btn-red btn-sm position-absolute top-0 end-0 mt-3 me-3" @click="removePhotoNew(index)">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                                            <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0"/>
                                        </svg>
                                    </button>
                                </div>
                            </div>

                            <!-- Event limit -->
                            <div class="mb-3">
                                <label for="eventLimit" class="form-label">Event Limit:</label>
                                <input type="number" class="form-control" min="1" id="eventLimit" required v-model="newEvent.eventLimit">
                            </div>

                            <!-- Ticketed event -->
                            <div class="mb-3">
                                <label for="ticketedEventYes">Is this a ticketed event? (Click yes if this event requires a pre-sign up for entry.)</label>
                                <div>
                                    <div class="form-check form-check-inline">
                                        <!-- Yes Option -->
                                        <input type="radio" id="ticketedEventYes" name="ticketedEvent" value="true" v-model="newEvent.ticketed" class="form-check-input" required>
                                        <label for="ticketedEventYes" class="form-check-label">&nbsp;Yes</label>
                                    </div>
                                    <div class="form-check form-check-inline">
                                        <!-- No Option -->
                                        <input type="radio" id="ticketedEventNo" name="ticketedEvent" value="false" v-model="newEvent.ticketed" class="form-check-input">
                                        <label for="ticketedEventNo" class="form-check-label">&nbsp;No</label>
                                    </div>
                                </div>
                            </div>

                            <!-- Paid event -->
                            <div v-if="newEvent.ticketed == 'true'" class="mb-3">
                                <label for="paidEventYes">If it is a ticketed event, are tickets free or paid?</label>
                                <div>
                                    <!-- Yes Option -->
                                    <input type="radio" id="paidEventYes" name="paidEvent" value="false" v-model="newEvent.paidEvent" required>
                                    <label for="paidEventYes">&nbsp;Tickets are free, but participants must RSVP first to enter.</label>
                                </div>
                                <div>
                                    <!-- No Option -->
                                    <input type="radio" id="paidEventNo" name="paidEvent" value="true" v-model="newEvent.paidEvent">
                                    <label for="paidEventNo">&nbsp;Tickets are paid, and participants will have to make payment at the below link:</label>

                                    <!-- Payment link -->
                                    <input v-if="newEvent.paidEvent == 'true'" type="text" class="form-control" id="paymentLink" v-model="newEvent.paymentLink" required>
                                </div>
                            </div>

                            <!-- Event location -->
                            <div class="mb-3">
                                <label for="eventLocation" class="form-label">Event Location:</label>
                                <input type="text" class="form-control" id="eventLocation" required v-model="newEvent.eventLocation">
                            </div>
                        </form>
                    </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" :disabled="disableButton">Close</button>
                        <button type="button" class="btn primary-btn-green" data-bs-dismiss="modal" @click="createEvent" :disabled="disableButton">Create</button>
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


<script>
import Quill from 'quill';
import DOMPurify from 'dompurify';
import { useToast } from 'vue-toastification';

export default {
    name: 'EventBox',
    props: {
        selfView: {
            type: Boolean,
            required: true
        },
        userID: {
            type: Number,
            required: true
        },
        targetVenueID: {
            type: Number,
            required: true
        },
        userType: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            // Variable to hold the Quill instance
            quill: null,

            // Variable to store 
            events: [],

            // Variable to disable button
            disableButton: false,

            // Variable to store new event details
            newEvent: {
                eventName: null,
                eventDescription: null,
                eventStartDate: null,
                eventEndDate: null,
                eventStartTime: null,
                eventEndTime: null,
                eventLimit: null,
                eventBanners: [],
                ticketed: null,
                paidEvent: null,
                eventLocation: null,
                paymentLink: null
            },

            // Variable to store default event banner
            defaultEventBanner: require("@/assets/defaultEventBanner.jpg"),
        }
    },
    methods: {
        // Function to get all events
        async getEvents() {
            try {
                let response;
                if (this.selfView) {
                    response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUserEvents/` + this.userID + "/venue/0");
                    this.events = response.data;
                }
                else {
                    response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUserEvents/` + this.targetVenueID + "/venue/0");
                    this.events = response.data;
                }
                this.events = response.data.events;
                console.log(this.events);
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

        // Function to upload images (convert images to base64)
        uploadImages(event) {

            this.newEvent.eventBanners = [];

            // Get the files 
            const files = event.target.files;

            // Check if there are more than 3 files
            if (files.length > 3) {
                alert("You can only upload up to 3 images.");
                return;
            }

            // Loop through the files
            for (let i = 0; i < files.length; i++) {

                // Check if the file is an image
                if (files[i].type.match('image.*')) {

                    // Create a file reader
                    const reader = new FileReader();

                    // Read the file
                    reader.readAsDataURL(files[i]);

                    // When the file is read
                    reader.onload = () => {
                        // Push the base64 string to the postPhotos array
                        this.newEvent.eventBanners.push(reader.result);
                    }
                }
            }
        },

        // Function to remove a photo from the new event
        removePhotoNew(index) {
            this.newEvent.eventBanners.splice(index, 1);
        },

        // Function to create a new event
        async createEvent() {
            try {
                // Check if the event description is empty
                const description = this.quill.root.innerHTML;

                // Check if the content is empty
                if (!description || description.trim() === "<p><br></p>") {
                    alert("Content is empty. Please add some text.");
                    return;
                }

                // Sanitize the content using DOMPurify
                let sanitizedContent = DOMPurify.sanitize(description);

                // Set the event description
                this.newEvent.eventDescription = sanitizedContent;

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
        this.getEvents();

        this.quill = new Quill('#editor-container', {
            theme: 'snow',
            modules: {
                toolbar: [
                [{ 'header': '1' }, { 'header': '2' }, { 'font': [] }],
                [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                ['bold', 'italic', 'underline'],
                ['link'],
                ]
            }
        });
    }
}
</script>