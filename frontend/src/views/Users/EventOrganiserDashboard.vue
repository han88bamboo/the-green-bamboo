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

        <div class="main-content py-4">
            <!-- Main Content -->
            <div v-if="dataLoaded" class="container-fluid ">
                <!-- Dashboard Header -->
                <div class="row mb-4">
                    <div class="col-12">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h2 class="fw-bold mb-1" style="color:#027562">Event Organiser Dashboard</h2>
                                <p class="text-muted mb-0">Manage your events and attendees</p>
                            </div>
                            <!-- Quick Actions -->
                            <div class="d-flex gap-2">
                                <router-link to="/events/view" class="btn btn-outline-secondary">
                                    <i class="bi bi-arrow-left me-2"></i>Back to Events
                                </router-link>
                                <!-- TODO: Add Create New Event button -->
                                <!-- <button class="btn primary-btn" @click="createNewEvent">
                                    <i class="bi bi-plus-circle me-2"></i>Create New Event
                                </button> -->
                            </div>
                        </div>
                    </div>
                </div>

                XYZ


            </div>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import { useToast } from 'vue-toastification';

export default {
    name: 'EventOrganiserDashboard',
    components: {
        NavBar
    },
    data() {
        return {
            // Page state
            dataLoaded: false,
            
            // Route parameters
            dashboardUserType: this.$route.params.userType, // 'user', 'venue', or 'producer'
            dashboardUserID: this.$route.params.userID,
            
            // Current user (for access control)
            currentUserID: null,
            currentUserType: null,
            
            // Tab management
            activeTab: 'upcoming',
            
            // Data placeholders (TODO: implement API calls)
            upcomingEvents: [],
            pastEvents: [],
            allAttendees: [],
            
            // Statistics placeholders
            totalEvents: 0,
            totalAttendees: 0,
            
            // Filter and search
            attendeeSearchQuery: '',
            filterByEvent: '',
            
            // Error handling
            error: null,
            
            // Default banner
            defaultEventBanner: require("@/assets/defaultEventBanner.jpg"),
        }
    },
    computed: {
        // Check if current user can view this dashboard
        canViewDashboard() {
            return this.currentUserID === this.dashboardUserID && 
                   this.currentUserType === this.dashboardUserType;
        },
        
        // TODO: Implement filtered attendees computed property
        // filteredAttendees() {
        //     let filtered = this.allAttendees;
        //     
        //     if (this.attendeeSearchQuery) {
        //         filtered = filtered.filter(attendee => 
        //             attendee.firstName.toLowerCase().includes(this.attendeeSearchQuery.toLowerCase()) ||
        //             attendee.lastName.toLowerCase().includes(this.attendeeSearchQuery.toLowerCase()) ||
        //             attendee.email.toLowerCase().includes(this.attendeeSearchQuery.toLowerCase())
        //         );
        //     }
        //     
        //     if (this.filterByEvent) {
        //         filtered = filtered.filter(attendee => attendee.eventId === this.filterByEvent);
        //     }
        //     
        //     return filtered;
        // }
    },
    methods: {
        // Utility methods (same as other Vue components)
        slugify(text = '') {
            return String(text)
                .toString()
                .toLowerCase()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '')
                .replace(/\s+/g, '-')
                .replace(/[^\w]/g, '');
        },
        
        formatDate(date) {
            const options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
            return new Date(date).toLocaleDateString("en-GB", options);
        },
        
        formatRSVPDate(timestamp) {
            if (!timestamp) return 'N/A';
            const date = new Date(timestamp);
            const dateOptions = { day: 'numeric', month: 'short', year: 'numeric' };
            const timeOptions = { hour: '2-digit', minute: '2-digit', hour12: true };
            
            const formattedDate = date.toLocaleDateString("en-GB", dateOptions);
            const formattedTime = date.toLocaleTimeString("en-GB", timeOptions);
            
            return `${formattedDate}, ${formattedTime}`;
        },
        
        truncateText(text, maxLength = 100) {
            if (!text) return '';
            const plainText = text.replace(/<[^>]*>/g, '');
            if (plainText.length <= maxLength) return plainText;
            return plainText.substring(0, maxLength).trim() + '...';
        },
        
        // TODO: Implement API methods for data fetching
        // async fetchOrganizerEvents() {
        //     try {
        //         const response = await this.$axios.get(
        //             `${process.env.VUE_APP_API_URL}/events/getUserEvents/${this.dashboardUserID}/${this.dashboardUserType}`
        //         );
        //         
        //         const events = response.data.events;
        //         this.upcomingEvents = events.filter(event => new Date(event.eventStartDate) >= new Date());
        //         this.pastEvents = events.filter(event => new Date(event.eventStartDate) < new Date());
        //         this.totalEvents = events.length;
        //         
        //         this.dataLoaded = true;
        //     } catch (error) {
        //         console.error('Error fetching organizer events:', error);
        //         this.dataLoaded = null;
        //     }
        // },
        
        // async fetchAllAttendees() {
        //     try {
        //         const response = await this.$axios.get(
        //             `${process.env.VUE_APP_API_URL}/events/getOrganizerAttendees/${this.dashboardUserID}/${this.dashboardUserType}`
        //         );
        //         
        //         this.allAttendees = response.data.attendees;
        //         this.totalAttendees = this.allAttendees.length;
        //     } catch (error) {
        //         console.error('Error fetching attendees:', error);
        //     }
        // },
        
        // TODO: Implement event management methods
        // editEvent(eventId) {
        //     this.$router.push(`/event/${eventId}/edit`);
        // },
        
        // deleteEvent(eventId) {
        //     // Implementation for event deletion
        // },
        
        // viewAttendees(eventId) {
        //     // Implementation for viewing event-specific attendees
        // },
        
        // exportAttendees(eventId) {
        //     // Implementation for exporting attendee data
        // },
        
        // checkInAttendee(attendeeId) {
        //     // Implementation for checking in attendee
        // },
        
        // markPaid(attendeeId) {
        //     // Implementation for marking attendee as paid
        // },
        
        // TODO: Implement initialization method
        async initializeDashboard() {
            // Check access permissions
            if (!this.canViewDashboard) {
                const toast = useToast();
                toast.error('You are not authorized to view this dashboard');
                this.$router.push('/events/view');
                return;
            }
            
            // TODO: Uncomment when API methods are implemented
            // await this.fetchOrganizerEvents();
            // await this.fetchAllAttendees();
            
            // Temporary: Set loaded to true for placeholder content
            this.dataLoaded = true;
        }
    },
    async mounted() {
        // Get current user info
        this.currentUserID = localStorage.getItem("88B_accID");
        this.currentUserType = localStorage.getItem("88B_accType");
        
        if (!this.currentUserID || this.currentUserType === 'defaultUser') {
            const toast = useToast();
            toast.error('Please log in to access the organizer dashboard');
            this.$router.push('/login');
            return;
        }
        
        // Initialize dashboard
        await this.initializeDashboard();
    }
}
</script>

<style scoped>
/* Tab styling consistent with Events.vue */
.nav-tabs .nav-link {
    color: #495057;
    border: none;
    border-bottom: 2px solid transparent;
    background-color: transparent;
    padding: 0.75rem 1rem;
    cursor: pointer;
}

.nav-tabs .nav-link:hover {
    border-color: transparent;
    border-bottom: 2px solid #dee2e6;
}

.nav-tabs .nav-link.active {
    color: #027562;
    background-color: transparent;
    border-color: transparent;
    border-bottom: 2px solid #027562;
    font-weight: bold;
}

.nav-tabs {
    border-bottom: 1px solid #dee2e6;
}

/* Card styling */
.card {
    border: 1px solid #dee2e6;
    border-radius: 0.5rem;
    transition: box-shadow 0.15s ease-in-out;
}

.card:hover {
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

/* Primary button color consistency */
.primary-btn {
    background-color: #027562;
    border-color: #027562;
    color: white;
}

.primary-btn:hover {
    background-color: #025a4a;
    border-color: #025a4a;
}

/* Statistics cards */
.card-title {
    font-size: 2rem;
}

/* Table styling */
.table th {
    color: #027562;
    font-weight: 600;
    border-bottom: 2px solid #dee2e6;
}

/* Badge colors */
.badge.bg-primary {
    background-color: #027562 !important;
}

/* Alert styling */
.alert-info {
    background-color: #e7f3ff;
    border-color: #b3d9ff;
    color: #0c5460;
}

/* Mobile responsiveness */
@media (max-width: 767px) {
    .mobile-mt-3 {
        margin-top: 1rem !important;
    }
    
    .mobile-px-4 {
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
}
</style>