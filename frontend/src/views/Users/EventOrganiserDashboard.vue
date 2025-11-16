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
        <div v-if="dataLoaded" class="container mt-5 mobile-mt-3 mobile-px-4 px-5">
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

            <!-- Dashboard Statistics Cards -->
            <div class="row mb-4">
                <!-- TODO: Implement dashboard statistics -->
                <!-- 
                <div class="col-md-3 col-6">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title fw-bold" style="color:#027562">{{ totalEvents }}</h5>
                            <p class="card-text text-muted">Total Events</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 col-6">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title fw-bold" style="color:#027562">{{ upcomingEvents.length }}</h5>
                            <p class="card-text text-muted">Upcoming Events</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 col-6">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title fw-bold" style="color:#027562">{{ totalAttendees }}</h5>
                            <p class="card-text text-muted">Total Attendees</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 col-6">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title fw-bold" style="color:#027562">{{ pastEvents.length }}</h5>
                            <p class="card-text text-muted">Past Events</p>
                        </div>
                    </div>
                </div>
                -->
            </div>

            <!-- Events Management Section -->
            <div class="row">
                <div class="col-12">
                    <!-- Tab Navigation -->
                    <ul class="nav nav-tabs mb-4" role="tablist">
                        <li class="nav-item">
                            <button class="nav-link active" @click="activeTab = 'upcoming'" :class="{active: activeTab === 'upcoming'}">
                                Upcoming Events
                            </button>
                        </li>
                        <li class="nav-item">
                            <button class="nav-link" @click="activeTab = 'past'" :class="{active: activeTab === 'past'}">
                                Past Events
                            </button>
                        </li>
                        <li class="nav-item">
                            <button class="nav-link" @click="activeTab = 'attendees'" :class="{active: activeTab === 'attendees'}">
                                All Attendees
                            </button>
                        </li>
                    </ul>

                    <!-- Tab Content -->
                    <div class="tab-content">
                        <!-- Upcoming Events Tab -->
                        <div v-if="activeTab === 'upcoming'" class="tab-pane active">
                            <!-- TODO: Implement upcoming events list with management tools -->
                            <!-- 
                            <div v-if="upcomingEvents.length > 0" class="row">
                                <div v-for="event in upcomingEvents" :key="event.id" class="col-md-6 col-lg-4 mb-4">
                                    <div class="card h-100">
                                        <div class="card-header d-flex justify-content-between align-items-center">
                                            <h6 class="mb-0 fw-bold">{{ event.eventName }}</h6>
                                            <div class="dropdown">
                                                <button class="btn btn-sm btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">
                                                    Actions
                                                </button>
                                                <ul class="dropdown-menu">
                                                    <li><a class="dropdown-item" @click="editEvent(event.id)">Edit Event</a></li>
                                                    <li><a class="dropdown-item" @click="viewAttendees(event.id)">View Attendees</a></li>
                                                    <li><a class="dropdown-item" @click="exportAttendees(event.id)">Export Attendees</a></li>
                                                    <li><hr class="dropdown-divider"></li>
                                                    <li><a class="dropdown-item text-danger" @click="deleteEvent(event.id)">Delete Event</a></li>
                                                </ul>
                                            </div>
                                        </div>
                                        <div class="card-body">
                                            <p class="text-muted small mb-2">{{ formatDate(event.eventStartDate) }}</p>
                                            <p class="card-text mb-3">{{ truncateText(event.eventDesc, 100) }}</p>
                                            <div class="d-flex justify-content-between align-items-center">
                                                <span class="badge bg-primary">{{ event.numAttendees || 0 }} attendees</span>
                                                <router-link :to="`/event/${event.id}/${slugify(event.eventName)}`" class="btn btn-sm primary-btn">
                                                    View Event
                                                </router-link>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div v-else class="text-center py-5">
                                <p class="text-muted">No upcoming events found.</p>
                                <button class="btn primary-btn" @click="createNewEvent">Create Your First Event</button>
                            </div>
                            -->
                            <div class="text-center py-5">
                                <div class="alert alert-info">
                                    <h5>Upcoming Events Management</h5>
                                    <p class="mb-0">This section will display your upcoming events with management tools including:</p>
                                    <ul class="mt-2 mb-0">
                                        <li>Event editing and deletion</li>
                                        <li>Attendee management per event</li>
                                        <li>Quick actions for check-in and payment tracking</li>
                                        <li>Export attendee lists</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <!-- Past Events Tab -->
                        <div v-if="activeTab === 'past'" class="tab-pane">
                            <!-- TODO: Implement past events list with analytics -->
                            <!-- 
                            <div v-if="pastEvents.length > 0" class="row">
                                <div v-for="event in pastEvents" :key="event.id" class="col-md-6 col-lg-4 mb-4">
                                    <div class="card h-100 opacity-75">
                                        <div class="card-header">
                                            <h6 class="mb-0 fw-bold">{{ event.eventName }}</h6>
                                            <span class="badge bg-secondary">Completed</span>
                                        </div>
                                        <div class="card-body">
                                            <p class="text-muted small mb-2">{{ formatDate(event.eventStartDate) }}</p>
                                            <p class="card-text mb-3">{{ truncateText(event.eventDesc, 100) }}</p>
                                            <div class="row text-center">
                                                <div class="col-6">
                                                    <div class="fw-bold">{{ event.numAttendees || 0 }}</div>
                                                    <small class="text-muted">Registered</small>
                                                </div>
                                                <div class="col-6">
                                                    <div class="fw-bold">{{ event.checkedInCount || 0 }}</div>
                                                    <small class="text-muted">Attended</small>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="card-footer">
                                            <button class="btn btn-sm btn-outline-primary w-100" @click="viewEventAnalytics(event.id)">
                                                View Analytics
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div v-else class="text-center py-5">
                                <p class="text-muted">No past events found.</p>
                            </div>
                            -->
                            <div class="text-center py-5">
                                <div class="alert alert-info">
                                    <h5>Past Events Analytics</h5>
                                    <p class="mb-0">This section will display your completed events with analytics including:</p>
                                    <ul class="mt-2 mb-0">
                                        <li>Attendance statistics and check-in rates</li>
                                        <li>Payment completion rates for paid events</li>
                                        <li>Event performance metrics</li>
                                        <li>Attendee feedback summaries</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <!-- All Attendees Management Tab -->
                        <div v-if="activeTab === 'attendees'" class="tab-pane">
                            <!-- TODO: Implement consolidated attendee management across all events -->
                            <!-- 
                            <div class="row mb-4">
                                <div class="col-md-6">
                                    <input type="text" class="form-control" placeholder="Search attendees..." v-model="attendeeSearchQuery">
                                </div>
                                <div class="col-md-3">
                                    <select class="form-select" v-model="filterByEvent">
                                        <option value="">All Events</option>
                                        <option v-for="event in allEvents" :key="event.id" :value="event.id">{{ event.eventName }}</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <button class="btn btn-outline-primary w-100" @click="exportAllAttendees">
                                        Export All Attendees
                                    </button>
                                </div>
                            </div>

                            <div class="table-responsive">
                                <table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Email</th>
                                            <th>Phone</th>
                                            <th>Event</th>
                                            <th>RSVP Date</th>
                                            <th>Status</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="attendee in filteredAttendees" :key="attendee.id">
                                            <td>{{ attendee.firstName }} {{ attendee.lastName }}</td>
                                            <td>{{ attendee.email }}</td>
                                            <td>{{ attendee.phoneNumber }}</td>
                                            <td>
                                                <router-link :to="`/event/${attendee.eventId}/${slugify(attendee.eventName)}`" class="text-decoration-none">
                                                    {{ attendee.eventName }}
                                                </router-link>
                                            </td>
                                            <td>{{ formatRSVPDate(attendee.rsvpDate) }}</td>
                                            <td>
                                                <span class="badge" :class="attendee.attendanceStatus === 'Checked In' ? 'bg-success' : 'bg-warning'">
                                                    {{ attendee.attendanceStatus }}
                                                </span>
                                            </td>
                                            <td>
                                                <div class="dropdown">
                                                    <button class="btn btn-sm btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">
                                                        Actions
                                                    </button>
                                                    <ul class="dropdown-menu">
                                                        <li><a class="dropdown-item" @click="checkInAttendee(attendee.id)">Check In</a></li>
                                                        <li><a class="dropdown-item" @click="markPaid(attendee.id)">Mark Paid</a></li>
                                                        <li><a class="dropdown-item" @click="contactAttendee(attendee)">Contact</a></li>
                                                        <li><hr class="dropdown-divider"></li>
                                                        <li><a class="dropdown-item text-danger" @click="removeAttendee(attendee.id)">Remove</a></li>
                                                    </ul>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            -->
                            <div class="text-center py-5">
                                <div class="alert alert-info">
                                    <h5>Consolidated Attendee Management</h5>
                                    <p class="mb-0">This section will provide unified attendee management across all your events including:</p>
                                    <ul class="mt-2 mb-0">
                                        <li>Search and filter attendees across all events</li>
                                        <li>Bulk check-in and payment status updates</li>
                                        <li>Export attendee data with customizable filters</li>
                                        <li>Contact management and communication tools</li>
                                        <li>Attendee analytics and engagement tracking</li>
                                    </ul>
                                </div>
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