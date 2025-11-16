<template>
    <div >
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

        <div class="main-content pt-4">
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

                <!-- Dashboard Content -->
                <div class="dashboard-container">
                    <!-- Desktop Vertical Navigation Rail -->
                    <div class="vertical-nav-rail d-none d-md-flex">
                        <div class="nav-tabs-vertical">
                            <button 
                                class="nav-tab-vertical"
                                :class="{ active: activeTab === 'upcoming' }"
                                @click="activeTab = 'upcoming'"
                            >
                                <span class="rotated-text">Upcoming & Ongoing Events</span>
                            </button>
                            <button 
                                class="nav-tab-vertical"
                                :class="{ active: activeTab === 'past' }"
                                @click="activeTab = 'past'"
                            >
                                <span class="rotated-text">Past Events</span>
                            </button>
                            <button 
                                class="nav-tab-vertical"
                                :class="{ active: activeTab === 'analytics' }"
                                @click="activeTab = 'analytics'"
                            >
                                <span class="rotated-text">Analytics</span>
                            </button>
                        </div>
                    </div>

                    <!-- Mobile Horizontal Navigation -->
                    <div class="horizontal-nav d-md-none mb-4">
                        <div class="nav nav-pills nav-fill">
                            <button 
                                class="nav-link"
                                :class="{ active: activeTab === 'upcoming' }"
                                @click="activeTab = 'upcoming'"
                            >
                                Upcoming & Ongoing Events
                            </button>
                            <button 
                                class="nav-link"
                                :class="{ active: activeTab === 'past' }"
                                @click="activeTab = 'past'"
                            >
                                Past Events
                            </button>
                            <button 
                                class="nav-link"
                                :class="{ active: activeTab === 'analytics' }"
                                @click="activeTab = 'analytics'"
                            >
                                Analytics
                            </button>
                        </div>
                    </div>

                    <!-- Content Area -->
                    <div class="dashboard-content">
                        <!-- Upcoming Events Tab -->
                        <div v-if="activeTab === 'upcoming'" class="content-section">
                            <div class="section-header mb-4">
                                <h3 class="section-title">Upcoming & Ongoing Events</h3>
                                <p class="section-subtitle">Manage your scheduled events</p>
                            </div>

                            <!-- Loading State -->
                            <div v-if="loadingEvents || loadingAttendees" class="text-center py-5">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Loading events...</span>
                                </div>
                                <p class="mt-3 text-muted">Loading your events...</p>
                            </div>

                            <!-- Event Cards -->
                            <div v-else class="event-cards-container">
                                <div 
                                    v-for="event in upcomingAndOngoingEvents" 
                                    :key="event.id"
                                    class="event-card"
                                    @click="openEventManagementModal(event)"
                                >
                                    <div class="event-thumbnail">
                                        <img :src="(event.eventBanners && event.eventBanners[0]) || defaultEventBanner" :alt="event.eventName" />
                                    </div>
                                    <div class="event-details">
                                        <h4 class="event-title">{{ event.eventName }}</h4>
                                        <div class="event-datetime">
                                            <div class="datetime-row">
                                                <i class="bi bi-calendar-event"></i>
                                                <span>{{ formatEventDate(event.eventStartDate) }}</span>
                                                <span v-if="event.eventEndDate && event.eventEndDate !== event.eventStartDate"> - {{ formatEventDate(event.eventEndDate) }}</span>
                                            </div>
                                            <div class="datetime-row">
                                                <i class="bi bi-clock"></i>
                                                <span>{{ formatEventTime(event.eventStartTime) }} - {{ formatEventTime(event.eventEndTime) }}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="event-stats">
                                        <div class="attendee-count">
                                            <span class="count">{{ event.attendeeCount || 0 }}/{{ event.eventLimit || 'N/A' }}</span>
                                            <span class="label">Attendees</span>
                                        </div>
                                    </div>
                                </div>

                                <!-- Empty State -->
                                <div v-if="upcomingAndOngoingEvents.length === 0" class="empty-state">
                                    <i class="bi bi-calendar-plus"></i>
                                    <h4>No Upcoming or Ongoing Events</h4>
                                    <p>You don't have any upcoming or ongoing events scheduled.</p>
                                    <router-link to="/events/view" class="btn btn-primary">Create Your First Event</router-link>
                                </div>
                            </div>
                        </div>

                        <!-- Past Events Tab -->
                        <div v-if="activeTab === 'past'" class="content-section">
                            <div class="section-header mb-4">
                                <h3 class="section-title">Past Events</h3>
                                <p class="section-subtitle">Review your completed events</p>
                            </div>

                            <!-- Loading State -->
                            <div v-if="loadingEvents || loadingAttendees" class="text-center py-5">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Loading events...</span>
                                </div>
                                <p class="mt-3 text-muted">Loading your past events...</p>
                            </div>

                            <!-- Event Cards -->
                            <div v-else class="event-cards-container">
                                <div 
                                    v-for="event in completedEvents" 
                                    :key="event.id"
                                    class="event-card past-event"
                                    @click="openEventManagementModal(event)"
                                >
                                    <div class="event-thumbnail">
                                        <img :src="(event.eventBanners && event.eventBanners[0]) || defaultEventBanner" :alt="event.eventName" />
                                        <div class="past-overlay">
                                            <i class="bi bi-check-circle"></i>
                                        </div>
                                    </div>
                                    <div class="event-details">
                                        <h4 class="event-title">{{ event.eventName }}</h4>
                                        <div class="event-datetime">
                                            <div class="datetime-row">
                                                <i class="bi bi-calendar-event"></i>
                                                <span>{{ formatEventDate(event.eventStartDate) }}</span>
                                                <span v-if="event.eventEndDate && event.eventEndDate !== event.eventStartDate"> - {{ formatEventDate(event.eventEndDate) }}</span>
                                            </div>
                                            <div class="datetime-row">
                                                <i class="bi bi-clock"></i>
                                                <span>{{ formatEventTime(event.eventStartTime) }} - {{ formatEventTime(event.eventEndTime) }}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="event-stats">
                                        <div class="attendee-count">
                                            <span class="count">{{ event.attendeeCount || 0 }}/{{ event.eventLimit || 'N/A' }}</span>
                                            <span class="label">Attended</span>
                                        </div>
                                    </div>
                                </div>

                                <!-- Empty State -->
                                <div v-if="completedEvents.length === 0" class="empty-state">
                                    <i class="bi bi-calendar-check"></i>
                                    <h4>No Past Events</h4>
                                    <p>You haven't hosted any events yet.</p>
                                </div>
                            </div>
                        </div>

                        <!-- Analytics Tab -->
                        <div v-if="activeTab === 'analytics'" class="content-section">
                            <div class="section-header mb-4">
                                <h3 class="section-title">Analytics</h3>
                                <p class="section-subtitle">Track your event performance</p>
                            </div>

                            <!-- Analytics Cards -->
                            <div class="analytics-grid">
                                <div class="analytics-card">
                                    <div class="card-header">
                                        <h4 class="card-title">Event Popularity</h4>
                                        <i class="bi bi-bar-chart"></i>
                                    </div>
                                    <div class="card-content">
                                        <div class="metric-large">
                                            <span class="number">{{ analyticsData.averageFillRate }}%</span>
                                            <span class="label">Average Fill Rate</span>
                                        </div>
                                        <div class="chart-placeholder">
                                            <div class="placeholder-bars">
                                                <div class="bar" style="height: 60%"></div>
                                                <div class="bar" style="height: 85%"></div>
                                                <div class="bar" style="height: 45%"></div>
                                                <div class="bar" style="height: 90%"></div>
                                                <div class="bar" style="height: 75%"></div>
                                                <div class="bar" style="height: 65%"></div>
                                            </div>
                                            <p class="chart-label">Event Attendance Rates</p>
                                        </div>
                                    </div>
                                </div>

                                <div class="analytics-card">
                                    <div class="card-header">
                                        <h4 class="card-title">Top Performing Events</h4>
                                        <i class="bi bi-trophy"></i>
                                    </div>
                                    <div class="card-content">
                                        <div v-if="analyticsData.topEvents.length > 0" class="top-events-list">
                                            <div 
                                                v-for="(event, index) in analyticsData.topEvents" 
                                                :key="event.id"
                                                class="top-event-item"
                                            >
                                                <span class="rank">{{ index + 1 }}</span>
                                                <span class="event-name">{{ event.eventName }}</span>
                                                <span class="attendees">{{ event.attendeeCount || 0 }}/{{ event.eventLimit || 'N/A' }}</span>
                                            </div>
                                        </div>
                                        <div v-else class="text-center text-muted py-3">
                                            <p>No event data available yet</p>
                                        </div>
                                    </div>
                                </div>

                                <div class="analytics-card">
                                    <div class="card-header">
                                        <h4 class="card-title">Monthly Overview</h4>
                                        <i class="bi bi-calendar-month"></i>
                                    </div>
                                    <div class="card-content">
                                        <div class="overview-stats">
                                            <div class="stat-item">
                                                <span class="stat-number">{{ analyticsData.totalEvents }}</span>
                                                <span class="stat-label">Total Events</span>
                                            </div>
                                            <div class="stat-item">
                                                <span class="stat-number">{{ analyticsData.totalAttendees }}</span>
                                                <span class="stat-label">Total Attendees</span>
                                            </div>
                                            <div class="stat-item">
                                                <span class="stat-number">{{ analyticsData.averageFillRate }}%</span>
                                                <span class="stat-label">Avg. Fill Rate</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="analytics-card">
                                    <div class="card-header">
                                        <h4 class="card-title">Revenue Insights</h4>
                                        <i class="bi bi-currency-dollar"></i>
                                    </div>
                                    <div class="card-content">
                                        <div class="revenue-summary">
                                            <div class="revenue-item">
                                                <span class="amount">$2,450</span>
                                                <span class="period">This Month</span>
                                            </div>
                                            <div class="revenue-trend">
                                                <span class="trend-indicator positive">+15%</span>
                                                <span class="trend-label">vs Last Month</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Event Management Modal (declarative approach) -->
                <div 
                    v-if="showEventManagementModal" 
                    class="modal d-block" 
                    style="background-color: rgba(0, 0, 0, 0.5); position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1050;"
                    @click.self="closeEventManagementModal"
                >
                    <div class="modal-dialog modal-dialog-centered modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Manage Event: {{ selectedEvent?.eventName || selectedEvent?.name }}</h5>
                                <button type="button" class="btn-close" @click="closeEventManagementModal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <!-- TODO: Implement management tabs similar to SpecificEventPage -->
                                <div class="management-tabs">
                                    <ul class="nav nav-tabs" role="tablist">
                                        <li class="nav-item">
                                            <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#edit-tab">Edit Event</button>
                                        </li>
                                        <li class="nav-item">
                                            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#attendees-tab">Manage Attendees</button>
                                        </li>
                                        <li class="nav-item">
                                            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#analytics-tab">Event Analytics</button>
                                        </li>
                                    </ul>
                                    <div class="tab-content mt-3">
                                        <div class="tab-pane fade show active" id="edit-tab">
                                            <div class="alert alert-info">
                                                <h6>Event Edit Form</h6>
                                                <p class="mb-0">This will contain the same edit form from SpecificEventPage.vue</p>
                                                <!-- TODO: Implement event edit form -->
                                            </div>
                                        </div>
                                        <div class="tab-pane fade" id="attendees-tab">
                                            <div class="alert alert-info">
                                                <h6>Attendee Management</h6>
                                                <p class="mb-0">This will contain the attendee management table from SpecificEventPage.vue</p>
                                                <!-- TODO: Implement attendee management -->
                                            </div>
                                        </div>
                                        <div class="tab-pane fade" id="analytics-tab">
                                            <div class="alert alert-info">
                                                <h6>Event-Specific Analytics</h6>
                                                <p class="mb-0">Individual event performance metrics and attendee insights</p>
                                                <!-- TODO: Implement event-specific analytics -->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" @click="closeEventManagementModal">Close</button>
                                <button type="button" class="btn btn-primary" @click="saveEventChanges">Save Changes</button>
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
            
            // Real data from API
            allOrganisingEvents: [],
            upcomingEvents: [],
            pastEvents: [],
            eventsWithAttendees: [], // Combined event + attendee data
            
            // Statistics 
            totalEvents: 0,
            totalAttendees: 0,
            
            // Loading states
            loadingEvents: false,
            loadingAttendees: false,
            
            // Filter and search
            attendeeSearchQuery: '',
            filterByEvent: '',
            
            // Error handling
            error: null,
            
            // Default banner
            defaultEventBanner: require("@/assets/defaultEventBanner.jpg"),

            // Modal management
            selectedEvent: null,
            showEventManagementModal: false,

            // Mock data for development (TODO: Replace with real API calls)
            mockUpcomingEvents: [
                {
                    id: 1,
                    name: "Wine Tasting Masterclass",
                    startDate: "2025-11-25",
                    endDate: "2025-11-25",
                    startTime: "18:00",
                    endTime: "21:00",
                    attendees: 32,
                    capacity: 50,
                    thumbnail: null
                },
                {
                    id: 2,
                    name: "Cocktail Making Workshop",
                    startDate: "2025-12-02",
                    endDate: "2025-12-02",
                    startTime: "19:30",
                    endTime: "22:00",
                    attendees: 18,
                    capacity: 25,
                    thumbnail: null
                },
                {
                    id: 3,
                    name: "Brewery Tour & Tasting",
                    startDate: "2025-12-10",
                    endDate: "2025-12-10",
                    startTime: "14:00",
                    endTime: "17:30",
                    attendees: 8,
                    capacity: 30,
                    thumbnail: null
                }
            ],
            mockPastEvents: [
                {
                    id: 4,
                    name: "Whiskey Appreciation Evening",
                    startDate: "2025-11-10",
                    endDate: "2025-11-10",
                    startTime: "20:00",
                    endTime: "23:00",
                    attendees: 22,
                    capacity: 25,
                    thumbnail: null
                },
                {
                    id: 5,
                    name: "Craft Beer Festival",
                    startDate: "2025-10-28",
                    endDate: "2025-10-29",
                    startTime: "16:00",
                    endTime: "22:00",
                    attendees: 145,
                    capacity: 150,
                    thumbnail: null
                }
            ],
        }
    },
    computed: {
        // Check if current user can view this dashboard
        canViewDashboard() {
            return this.currentUserID === this.dashboardUserID && 
                   this.currentUserType === this.dashboardUserType;
        },
        
        // Filter events that haven't started yet or are ongoing (upcoming + ongoing)
        upcomingAndOngoingEvents() {
            return this.eventsWithAttendees.filter(event => {
                const now = new Date();
                
                // If event has both start and end date
                if (event.eventEndDate && event.eventEndDate !== event.eventStartDate) {
                    const endDate = new Date(`${event.eventEndDate}T${event.eventEndTime || '23:59'}`);
                    const oneDayAfterEnd = new Date(endDate);
                    oneDayAfterEnd.setDate(oneDayAfterEnd.getDate() + 1);
                    return now < oneDayAfterEnd;
                } else {
                    // Event has only start date
                    const startDate = new Date(`${event.eventStartDate}T${event.eventStartTime || '00:00'}`);
                    const oneDayAfterStart = new Date(startDate);
                    oneDayAfterStart.setDate(oneDayAfterStart.getDate() + 1);
                    return now < oneDayAfterStart;
                }
            });
        },
        
        // Filter events that are classified as past based on the rules
        completedEvents() {
            return this.eventsWithAttendees.filter(event => {
                const now = new Date();
                
                // If event has both start and end date
                if (event.eventEndDate && event.eventEndDate !== event.eventStartDate) {
                    const endDate = new Date(`${event.eventEndDate}T${event.eventEndTime || '23:59'}`);
                    const oneDayAfterEnd = new Date(endDate);
                    oneDayAfterEnd.setDate(oneDayAfterEnd.getDate() + 1);
                    return now >= oneDayAfterEnd;
                } else {
                    // Event has only start date
                    const startDate = new Date(`${event.eventStartDate}T${event.eventStartTime || '00:00'}`);
                    const oneDayAfterStart = new Date(startDate);
                    oneDayAfterStart.setDate(oneDayAfterStart.getDate() + 1);
                    return now >= oneDayAfterStart;
                }
            });
        },
        
        // Calculate analytics data
        analyticsData() {
            const totalEvents = this.eventsWithAttendees.length;
            const totalAttendees = this.eventsWithAttendees.reduce((sum, event) => sum + (event.attendeeCount || 0), 0);
            const totalCapacity = this.eventsWithAttendees.reduce((sum, event) => sum + (event.eventLimit || 0), 0);
            const averageFillRate = totalCapacity > 0 ? Math.round((totalAttendees / totalCapacity) * 100) : 0;
            
            return {
                totalEvents,
                totalAttendees,
                averageFillRate,
                topEvents: [...this.eventsWithAttendees]
                    .sort((a, b) => (b.attendeeCount || 0) - (a.attendeeCount || 0))
                    .slice(0, 3)
            };
        }
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

        // Dashboard-specific formatting methods
        formatEventDate(date) {
            const options = { 
                weekday: 'short', 
                day: 'numeric', 
                month: 'short', 
                year: 'numeric' 
            };
            return new Date(date).toLocaleDateString("en-GB", options);
        },

        formatEventTime(time) {
            if (!time) return '';
            const [hour, minute] = time.split(':');
            const ampm = hour >= 12 ? 'PM' : 'AM';
            const formattedHour = hour % 12 || 12;
            return `${formattedHour}:${minute} ${ampm}`;
        },

        // Event management methods
        openEventManagementModal(event) {
            this.selectedEvent = event;
            this.showEventManagementModal = true;
        },
        
        closeEventManagementModal() {
            this.showEventManagementModal = false;
            this.selectedEvent = null;
        },
        
        saveEventChanges() {
            // TODO: Implement save functionality
            console.log('Saving changes for event:', this.selectedEvent);
            this.closeEventManagementModal();
        },
        
        // Fetch all events the user is organizing
        async fetchOrganizerEvents() {
            this.loadingEvents = true;
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/events/getUserOrganisingEvents/${this.dashboardUserID}/${this.dashboardUserType}`
                );
                
                this.allOrganisingEvents = response.data.events || [];
                console.log('Fetched organizer events:', this.allOrganisingEvents);
                
                // Fetch attendees for each event
                await this.fetchAttendeesForAllEvents();
                
            } catch (error) {
                console.error('Error fetching organizer events:', error);
                if (error.response && error.response.status === 404) {
                    // No events found, that's okay
                    this.allOrganisingEvents = [];
                    this.eventsWithAttendees = [];
                } else {
                    this.dataLoaded = null;
                    const toast = useToast();
                    toast.error('Failed to load events. Please try again.');
                }
            } finally {
                this.loadingEvents = false;
            }
        },
        
        // Fetch attendees for all events
        async fetchAttendeesForAllEvents() {
            this.loadingAttendees = true;
            try {
                const eventsWithAttendees = [];
                
                for (const event of this.allOrganisingEvents) {
                    try {
                        const attendeeResponse = await this.$axios.get(
                            `${process.env.VUE_APP_API_URL}/events/getAttendees/${event.id}`
                        );
                        
                        const attendees = attendeeResponse.data.attendees || [];
                        const eventWithAttendees = {
                            ...event,
                            attendeeCount: attendees.length,
                            attendeesList: attendees // Store full attendee data for modal
                        };
                        
                        eventsWithAttendees.push(eventWithAttendees);
                        console.log(`Event ${event.eventName}: ${attendees.length} attendees`);
                        
                    } catch (attendeeError) {
                        console.warn(`Could not fetch attendees for event ${event.id}:`, attendeeError);
                        // Add event with 0 attendees if attendee fetch fails
                        eventsWithAttendees.push({
                            ...event,
                            attendeeCount: 0,
                            attendeesList: []
                        });
                    }
                }
                
                this.eventsWithAttendees = eventsWithAttendees;
                this.totalEvents = eventsWithAttendees.length;
                this.totalAttendees = eventsWithAttendees.reduce((sum, event) => sum + event.attendeeCount, 0);
                
                console.log('All events with attendees:', this.eventsWithAttendees);
                
            } catch (error) {
                console.error('Error fetching attendees data:', error);
            } finally {
                this.loadingAttendees = false;
            }
        },
        
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
        
        // Initialize dashboard with real data
        async initializeDashboard() {
            // Check access permissions
            if (!this.canViewDashboard) {
                const toast = useToast();
                toast.error('You are not authorized to view this dashboard');
                this.$router.push('/events/view');
                return;
            }
            
            try {
                // Fetch real data
                await this.fetchOrganizerEvents();
                this.dataLoaded = true;
                
            } catch (error) {
                console.error('Dashboard initialization failed:', error);
                this.dataLoaded = null;
            }
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

/* Dashboard Layout */
.dashboard-container {
    display: flex;
    min-height: calc(100vh - 200px);
    gap: 0;
}

/* Vertical Navigation Rail (Desktop) */
.vertical-nav-rail {
    width: 100px;
    flex-shrink: 0;
    background: #dee2e2;
    padding: 1rem 0.75rem;
    box-shadow: inset -1px 0 0 rgba(2, 117, 98, 0.1);
    margin-left: -1rem;
    padding-left: 1.75rem;
    min-height: 100vh;
    position: relative;
}

.nav-tabs-vertical {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.nav-tab-vertical {
    height: 120px;
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
}

.nav-tab-vertical:hover {
    background: #e9ecef;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
    transform: translateY(-1px);
}

.nav-tab-vertical.active {
    background: #027562;
    border-color: #027562;
    color: white;
    box-shadow: 0 6px 16px rgba(2, 117, 98, 0.2);
}

.rotated-text {
    writing-mode: vertical-rl;
    text-orientation: mixed;
    transform: rotate(180deg);
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 0.5px;
}

/* Horizontal Navigation (Mobile) */
.horizontal-nav .nav-pills .nav-link {
    background: #f8f9fa;
    color: #495057;
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.2s ease;
}

.horizontal-nav .nav-pills .nav-link:hover {
    background: #e9ecef;
}

.horizontal-nav .nav-pills .nav-link.active {
    background: #027562;
    color: white;
    box-shadow: 0 2px 8px rgba(2, 117, 98, 0.2);
}

/* Dashboard Content Area */
.dashboard-content {
    flex: 1;
    min-height: 600px;
    margin-left: 2rem;
    padding-right: 1rem;
}

.content-section {
    animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.section-header {
    border-bottom: 1px solid #e9ecef;
    padding-bottom: 1rem;
}

.section-title {
    color: #027562;
    font-weight: 700;
    margin: 0;
}

.section-subtitle {
    color: #6c757d;
    margin: 0.5rem 0 0 0;
    font-size: 0.9rem;
}

/* Event Cards */
.event-cards-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.event-card {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
}

.event-card:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    transform: translateY(-2px);
    border-color: #027562;
}

.event-card.past-event {
    opacity: 0.8;
    background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
}

.event-thumbnail {
    width: 80px;
    height: 80px;
    border-radius: 8px;
    overflow: hidden;
    position: relative;
    flex-shrink: 0;
}

.event-thumbnail img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.past-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(2, 117, 98, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
}

.event-details {
    flex: 1;
}

.event-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
    color: #212529;
}

.event-datetime {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.datetime-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: #6c757d;
}

.datetime-row i {
    width: 16px;
    color: #027562;
}

.event-stats {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.5rem;
    flex-shrink: 0;
}

.attendee-count {
    text-align: right;
}

.attendee-count .count {
    display: block;
    font-size: 1.2rem;
    font-weight: 700;
    color: #027562;
}

.attendee-count .label {
    display: block;
    font-size: 0.75rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-badge.upcoming {
    background: #e3f2fd;
    color: #1976d2;
}

.status-badge.ongoing {
    background: #fff3e0;
    color: #f57c00;
}

.status-badge.completed {
    background: #e8f5e8;
    color: #2e7d32;
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #6c757d;
}

.empty-state i {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: #027562;
    opacity: 0.5;
}

.empty-state h4 {
    margin-bottom: 0.5rem;
    color: #495057;
}

/* Analytics Grid */
.analytics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
}

.analytics-card {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
    transition: box-shadow 0.2s ease;
}

.analytics-card:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.analytics-card .card-header {
    background: #f8f9fa;
    padding: 1.25rem;
    border-bottom: 1px solid #e9ecef;
    display: flex;
    justify-content: between;
    align-items: center;
}

.analytics-card .card-title {
    font-size: 1rem;
    font-weight: 600;
    margin: 0;
    color: #495057;
}

.analytics-card .card-header i {
    color: #027562;
    font-size: 1.2rem;
}

.analytics-card .card-content {
    padding: 1.5rem;
}

.metric-large {
    text-align: center;
    margin-bottom: 1.5rem;
}

.metric-large .number {
    display: block;
    font-size: 2.5rem;
    font-weight: 700;
    color: #027562;
}

.metric-large .label {
    display: block;
    font-size: 0.85rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 0.25rem;
}

/* Chart Placeholder */
.chart-placeholder {
    text-align: center;
}

.placeholder-bars {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    height: 60px;
    margin-bottom: 0.75rem;
    gap: 4px;
}

.placeholder-bars .bar {
    background: linear-gradient(180deg, #027562 0%, #025a4a 100%);
    border-radius: 2px;
    flex: 1;
    min-height: 20%;
}

.chart-label {
    font-size: 0.8rem;
    color: #6c757d;
    margin: 0;
}

/* Top Events List */
.top-events-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.top-event-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    background: #f8f9fa;
    border-radius: 8px;
}

.top-event-item .rank {
    background: #027562;
    color: white;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 600;
    flex-shrink: 0;
}

.top-event-item .event-name {
    flex: 1;
    font-weight: 500;
    color: #495057;
}

.top-event-item .attendees {
    font-weight: 600;
    color: #027562;
}

/* Overview Stats */
.overview-stats {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.stat-item {
    text-align: center;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
}

.stat-item .stat-number {
    display: block;
    font-size: 1.8rem;
    font-weight: 700;
    color: #027562;
}

.stat-item .stat-label {
    display: block;
    font-size: 0.8rem;
    color: #6c757d;
    margin-top: 0.25rem;
}

/* Revenue Summary */
.revenue-summary {
    text-align: center;
}

.revenue-item {
    margin-bottom: 1rem;
}

.revenue-item .amount {
    display: block;
    font-size: 2rem;
    font-weight: 700;
    color: #027562;
}

.revenue-item .period {
    display: block;
    font-size: 0.85rem;
    color: #6c757d;
}

.revenue-trend {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.trend-indicator {
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
}

.trend-indicator.positive {
    background: #e8f5e8;
    color: #2e7d32;
}

.trend-label {
    font-size: 0.8rem;
    color: #6c757d;
}

/* Mobile Responsiveness */
@media (max-width: 991px) {
    .dashboard-container {
        flex-direction: column;
    }
    
    .event-card {
        flex-direction: column;
        text-align: center;
        gap: 1rem;
    }
    
    .event-stats {
        align-items: center;
        flex-direction: row;
        justify-content: space-between;
        width: 100%;
    }
    
    .analytics-grid {
        grid-template-columns: 1fr;
    }
    
    .overview-stats {
        flex-direction: row;
    }
}

@media (max-width: 576px) {
    .event-card {
        padding: 1rem;
    }
    
    .event-thumbnail {
        width: 60px;
        height: 60px;
    }
    
    .overview-stats {
        flex-direction: column;
    }
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