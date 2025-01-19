<template>
    <div class="square primary-square-green-outline rounded p-3 mb-3">

        <!-- Title if current user is profile owner -->
        <div v-if="selfView" class="d-flex justify-content-between align-items-center">
            <h3>Your Events</h3>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2"/>
            </svg>
        </div>

        <!-- Title if not current user -->
        <div v-else>
            <h3>Upcoming Events</h3>
        </div>

        <!-- List of events -->
        <div class="row">
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
            // Variable to store 
            events: [],

            // Variable to store default event banner
            defaultEventBanner: require("@/assets/defaultEventBanner.jpg"),
        }
    },
    methods: {
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
        }
    },
    mounted() {
        this.getEvents();
    }
}
</script>