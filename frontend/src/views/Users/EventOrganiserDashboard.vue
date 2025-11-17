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

        <div class="main-content">
            <!-- Main Content -->
            <div v-if="dataLoaded" class="container-fluid ">
                <!-- Dashboard Header -->
                <div class="row border-bottom pb-4 pt-3 shadow">
                    <div class="col-12">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h3 class="fw-bold mb-1" style="color:#027562">
                                    Manage events and attendees<span v-if="dashboardUserDisplayName">: <span style="color:black;">{{ dashboardUserDisplayName }}</span></span>
                                </h3>
                                
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
                    <div class="dashboard-content mt-3">
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
                                <template v-for="event in upcomingAndOngoingEvents" :key="event.id">
                                    <div class="event-card ps-3">
                                        <div class="event-thumbnail">
                                            <img :src="(event.eventBanners && event.eventBanners[0]) || defaultEventBanner" :alt="event.eventName" />
                                        </div>
                                        <div class="event-details">
                                            <router-link 
                                                :to="`/event/${event.id}/${slugify(event.eventName)}`"
                                                class="event-title-link"
                                            >
                                                <h4 class="event-title">{{ event.eventName }}</h4>
                                            </router-link>
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
                                            <button 
                                                class="attendee-count-btn"
                                                @click="toggleAttendeeManagement(event)"
                                                :class="{ 'active': expandedEventId === event.id, 'compressed': expandedEventId === event.id }"
                                                title="Manage Attendees"
                                                style=" display: inline-flex; flex-direction: row;"
                                            >
                                                <span class="count">{{ event.attendeeCount || 0 }}/{{ event.eventLimit || 'N/A' }}</span>
                                                <span class="label">&nbsp;Attendees</span>
                                            </button>
                                            <div class="button-group">
                                                <button 
                                                    class="btn primary-btn btn-sm edit-event-btn"
                                                    @click="openEventManagementModal(event)"
                                                    title="Edit Event"
                                                >
                                                    <i class="bi bi-pencil me-1"></i>
                                                    Edit
                                                </button>
                                                <button
                                                    v-if="isSignupOpen(event)"
                                                    class="btn btn-sm lock-signup-btn"
                                                    @click="openSignupManagementModal(event)"
                                                    title="Lock Signups"
                                                >
                                                    Lock Signups
                                                </button>
                                                <button
                                                    v-if="!isSignupOpen(event)"
                                                    class="btn btn-sm lock-signup-btn"
                                                    @click="openSignupManagementModal(event)"
                                                    title="Unlock Signups"
                                                >
                                                    Unlock Signups
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <!-- Attendee Management Drawer (appears below the event card) -->
                                    <div 
                                        v-if="expandedEventId === event.id" 
                                        class="attendee-management-drawer mt-0"
                                    >
                                        <div class="attendee-management-content">
                                            <h5 class="fw-bold mb-3" style="color:#027562">
                                                Manage Attendees for "{{ event.eventName }}" ({{ event.attendeeCount || 0 }}/{{ event.eventLimit }})
                                            </h5>
                                            
                                            <!-- Loading state -->
                                            <div v-if="loadingAttendeeManagement[event.id]" class="text-center py-3">
                                                <div class="spinner-border spinner-border-sm text-primary" role="status">
                                                    <span class="visually-hidden">Loading attendees...</span>
                                                </div>
                                                <span class="ms-2">Loading attendees...</span>
                                            </div>
                                            
                                            <!-- Attendee table -->
                                            <div v-else-if="attendeesForManagement[event.id] && attendeesForManagement[event.id].length > 0" class="table-responsive">
                                                <table class="table table-striped table-sm">
                                                    <thead>
                                                        <tr>
                                                            <th>Account Name</th>
                                                            <th>Full Name</th>
                                                            <th>Phone Number</th>
                                                            <th>Email</th>
                                                            <th>RSVP Date</th>
                                                            <th v-if="event.paidEvent">Has Paid? <span class="text-muted">(Marked by Organiser)</span></th>
                                                            <th>Attendance <span class="text-muted">(Marked by Organiser)</span></th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="attendee in attendeesForManagement[event.id]" :key="attendee.attendeeId">
                                                            <td>
                                                                {{ attendee.displayName || attendee.venueName || attendee.producerName }}
                                                            </td>
                                                            <td>
                                                                <span v-if="attendee.firstName || attendee.lastName">
                                                                    {{ attendee.firstName }} {{ attendee.lastName }}
                                                                </span>
                                                                <span v-else class="text-muted">N/A</span>
                                                            </td>
                                                            <td>
                                                                <span v-if="attendee.phoneNumber">{{ attendee.phoneNumber }}</span>
                                                                <span v-else class="text-muted">N/A</span>
                                                            </td>
                                                            <td>
                                                                <span v-if="attendee.email">{{ attendee.email }}</span>
                                                                <span v-else class="text-muted">N/A</span>
                                                            </td>
                                                            <td>
                                                                {{ formatRSVPDate(attendee.rsvpDate) }}
                                                            </td>
                                                            <td v-if="event.paidEvent" class="text-center">
                                                                <div class="form-check d-flex justify-content-center">
                                                                    <input 
                                                                        class="form-check-input" 
                                                                        type="checkbox" 
                                                                        :checked="attendee.hasPaid"
                                                                        @change="updatePaymentStatus(attendee.attendeeId, $event.target.checked)"
                                                                    >
                                                                </div>
                                                            </td>
                                                            <td>
                                                                <select 
                                                                    class="form-select form-select-sm"
                                                                    :value="attendee.attendanceStatus"
                                                                    @change="updateAttendanceStatus(attendee.attendeeId, $event.target.value)"
                                                                >
                                                                    <option value="Not Checked In">Not Checked In</option>
                                                                    <option value="Checked In">Checked In</option>
                                                                </select>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </div>
                                            
                                            <!-- No attendees message -->
                                            <div v-else class="text-center py-4 text-muted">
                                                <i class="bi bi-people fs-3 mb-2"></i>
                                                <p class="mb-0">No attendees registered for this event yet.</p>
                                            </div>
                                        </div>
                                    </div>
                                </template>

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
                                <template v-for="event in completedEvents" :key="event.id">
                                    <div class="event-card past-event ps-3">
                                        <div class="event-thumbnail">
                                            <img :src="(event.eventBanners && event.eventBanners[0]) || defaultEventBanner" :alt="event.eventName" />
                                            <div class="past-overlay">
                                                <i class="bi bi-check-circle"></i>
                                            </div>
                                        </div>
                                        <div class="event-details">
                                            <router-link 
                                                :to="`/event/${event.id}/${slugify(event.eventName)}`"
                                                class="event-title-link"
                                            >
                                                <h4 class="event-title">{{ event.eventName }}</h4>
                                            </router-link>
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
                                            <button 
                                                class="attendee-count-btn"
                                                @click="toggleAttendeeManagement(event)"
                                                :class="{ 'active': expandedEventId === event.id, 'compressed': expandedEventId === event.id }"
                                                title="Manage Attendees"
                                            >
                                                <span class="count">{{ event.attendeeCount || 0 }}/{{ event.eventLimit || 'N/A' }}</span>
                                                <span class="label">Attended</span>
                                            </button>
                                            <button 
                                                class="btn btn-outline-primary btn-sm edit-event-btn"
                                                @click="openEventManagementModal(event)"
                                                title="Edit Event"
                                            >
                                                <i class="bi bi-pencil me-1"></i>
                                                Edit
                                            </button>
                                        </div>
                                    </div>
                                    
                                    <!-- Attendee Management Drawer (appears below the event card) -->
                                    <div 
                                        v-if="expandedEventId === event.id" 
                                        class="attendee-management-drawer mt-0"
                                    >
                                        <div class="attendee-management-content">
                                            <h5 class="fw-bold mb-3" style="color:#027562">
                                                Manage Attendees for "{{ event.eventName }}" ({{ event.attendeeCount || 0 }}/{{ event.eventLimit }})
                                            </h5>
                                            
                                            <!-- Loading state -->
                                            <div v-if="loadingAttendeeManagement[event.id]" class="text-center py-3">
                                                <div class="spinner-border spinner-border-sm text-primary" role="status">
                                                    <span class="visually-hidden">Loading attendees...</span>
                                                </div>
                                                <span class="ms-2">Loading attendees...</span>
                                            </div>
                                            
                                            <!-- Attendee table -->
                                            <div v-else-if="attendeesForManagement[event.id] && attendeesForManagement[event.id].length > 0" class="table-responsive">
                                                <table class="table table-striped table-sm">
                                                    <thead>
                                                        <tr>
                                                            <th>Account Name</th>
                                                            <th>Full Name</th>
                                                            <th>Phone Number</th>
                                                            <th>Email</th>
                                                            <th>RSVP Date</th>
                                                            <th v-if="event.paidEvent">Has Paid? <span class="text-muted">(Marked by Organiser)</span></th>
                                                            <th>Attendance <span class="text-muted">(Marked by Organiser)</span></th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="attendee in attendeesForManagement[event.id]" :key="attendee.attendeeId">
                                                            <td>
                                                                {{ attendee.displayName || attendee.venueName || attendee.producerName }}
                                                            </td>
                                                            <td>
                                                                <span v-if="attendee.firstName || attendee.lastName">
                                                                    {{ attendee.firstName }} {{ attendee.lastName }}
                                                                </span>
                                                                <span v-else class="text-muted">N/A</span>
                                                            </td>
                                                            <td>
                                                                <span v-if="attendee.phoneNumber">{{ attendee.phoneNumber }}</span>
                                                                <span v-else class="text-muted">N/A</span>
                                                            </td>
                                                            <td>
                                                                <span v-if="attendee.email">{{ attendee.email }}</span>
                                                                <span v-else class="text-muted">N/A</span>
                                                            </td>
                                                            <td>
                                                                {{ formatRSVPDate(attendee.rsvpDate) }}
                                                            </td>
                                                            <td v-if="event.paidEvent" class="text-center">
                                                                <div class="form-check d-flex justify-content-center">
                                                                    <input 
                                                                        class="form-check-input" 
                                                                        type="checkbox" 
                                                                        :checked="attendee.hasPaid"
                                                                        @change="updatePaymentStatus(attendee.attendeeId, $event.target.checked)"
                                                                    >
                                                                </div>
                                                            </td>
                                                            <td>
                                                                <select 
                                                                    class="form-select form-select-sm"
                                                                    :value="attendee.attendanceStatus"
                                                                    @change="updateAttendanceStatus(attendee.attendeeId, $event.target.value)"
                                                                >
                                                                    <option value="Not Checked In">Not Checked In</option>
                                                                    <option value="Checked In">Checked In</option>
                                                                </select>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </div>
                                            
                                            <!-- No attendees message -->
                                            <div v-else class="text-center py-4 text-muted">
                                                <i class="bi bi-people fs-3 mb-2"></i>
                                                <p class="mb-0">No attendees registered for this event yet.</p>
                                            </div>
                                        </div>
                                    </div>
                                </template>

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
                                <h5 class="modal-title">Edit Event: {{ selectedEvent?.eventName || selectedEvent?.name }}</h5>
                                <button type="button" class="btn-close" @click="closeEventManagementModal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body text-start">

                                                <!-- Event Name Edit Field -->
                                                <div class="mb-3">
                                                    <label for="eventName" class="form-label fw-bold">Event Name <span style="color: red;">*</span></label>
                                                    <input type="text" class="form-control" id="eventName" v-model="selectedEventCopy.eventName">
                                                </div>

                                                <!-- Event description editor -->
                                                <div class="mb-3">
                                                    <label for="eventDescEditor" class="form-label fw-bold">Event Description</label>
                                                    <div id="dashboard-editor-container" style="height: 300px;" class="mb-3"></div>
                                                </div>

                                                <!-- Event type -->
                                                <div class="mb-3 row">
                                                    <label for="eventType" class="fw-bold">Event Type <span style="color: red;">*</span></label>
                                                
                                                <div>
                                                    <div class="form-check form-check-inline">
                                                        <!-- Online option -->
                                                        <input type="radio" id="onlineEvent" name="eventType" value="Online" v-model="selectedEventCopy.eventType" class="form-check-input" required>
                                                        <label for="onlineEvent" class="form-check-label">&nbsp;Online</label>
                                                    </div>
                                                    <div class="form-check form-check-inline">
                                                        <!-- In Person option -->
                                                        <input type="radio" id="inPersonEvent" name="eventType" value="Location" v-model="selectedEventCopy.eventType" class="form-check-input">
                                                        <label for="inPersonEvent" class="form-check-label">&nbsp;In Person</label>
                                                    </div>
                                                </div>
                                            </div>

                                            <hr>

                                                <div class="mb-3 row">
                                                    <!-- Event start date -->
                                                    <div class="col">
                                                        <label for="eventStartDate" class="form-label fw-bold text-start">Event Start Date <span style="color: red;">*</span></label>
                                                        <input type="date" class="form-control" id="eventStartDate" required v-model="selectedEventCopy.eventStartDate" :min="new Date().toISOString().split('T')[0]"> 
                                                    </div>

                                                    <!-- Event start time -->
                                                    <div class="col">
                                                        <label for="eventStartTime" class="form-label fw-bold text-start">Event Start Time</label>
                                                        <input type="time" class="form-control" id="eventStartTime" v-model="selectedEventCopy.eventStartTime">
                                                    </div>
                                                </div>

                                                <div class="mb-3 row">
                                                    <!-- Event end date -->
                                                    <div class="col">
                                                        <label for="eventEndDate" class="form-label fw-bold text-start">Event End Date</label>
                                                        <input type="date" class="form-control" id="eventEndDate" required v-model="selectedEventCopy.eventEndDate" :min="selectedEventCopy.eventStartDate">
                                                    </div>

                                                    <!-- Event end time -->
                                                    <div class="col">
                                                        <label for="eventEndTime" class="form-label fw-bold text-start">Event End Time</label>
                                                        <input type="time" class="form-control" id="eventEndTime" v-model="selectedEventCopy.eventEndTime">
                                                    </div>
                                                </div>                                            <!-- All Day Checkbox -->
                                            <div class="mb-3">
                                                <input class="form-check-input" type="checkbox" id="allDay" 
                                                    v-model="selectedEventCopy.allDay">
                                                <label class="form-check-label" for="allDay">
                                                    All Day Event
                                                </label>
                                            </div>

                                            <hr>

                                            <!-- Event wallpaper upload -->
                                            <div class="mb-3">
                                                <label for="eventBanner" class="form-label fw-bold">Add Event Wallpaper (upload up to 3 images)</label>
                                                <input type="file" class="form-control" id="eventBanner" multiple accept="image/*" @change="uploadImages" :disabled="selectedEventCopy.eventBanners && selectedEventCopy.eventBanners.length == 3">
                                            </div>

                                            <!-- Display uploaded banners --> 
                                            <div class="mb-3 row">
                                                <div v-for="(banner, index) in selectedEventCopy.eventBanners" :key="index" class="col-4 position-relative">
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
                                                <label for="eventLimit" class="form-label fw-bold">Event Limit</label>
                                                <input type="number" class="form-control" min="1" id="eventLimit" required v-model="selectedEventCopy.eventLimit">
                                            </div>

                                            <!-- Ticketed event -->
                                            <div class="mb-3">
                                                <label for="ticketedEventYes" class="fw-bold d-block">Is this a ticketed event? (Click yes if this event requires a pre-sign up for entry.) <span style="color: red;">*</span></label>
                                                <div>
                                                    <div class="form-check form-check-inline">
                                                        <!-- Yes Option -->
                                                        <input type="radio" id="ticketedEventYes" name="ticketedEvent" value="true" v-model="selectedEventCopy.ticketed" class="form-check-input" required>
                                                        <label for="ticketedEventYes" class="form-check-label">&nbsp;Yes</label>
                                                    </div>
                                                    <div class="form-check form-check-inline">
                                                        <!-- No Option -->
                                                        <input type="radio" id="ticketedEventNo" name="ticketedEvent" value="false" v-model="selectedEventCopy.ticketed" class="form-check-input">
                                                        <label for="ticketedEventNo" class="form-check-label">&nbsp;No</label>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- Paid event -->
                                            <div v-if="selectedEventCopy.ticketed == true" class="mb-3">
                                                <label for="paidEventYes" class="fw-bold">If it is a ticketed event, are tickets free or paid?</label>
                                                <div>
                                                    <!-- Yes Option -->
                                                    <input type="radio" id="paidEventYes" name="paidEvent" value="false" v-model="selectedEventCopy.paidEvent" required>
                                                    <label for="paidEventYes">&nbsp;Tickets are free, but participants must RSVP first to enter.</label>
                                                </div>
                                                <div>
                                                    <!-- No Option -->
                                                    <input type="radio" id="paidEventNo" name="paidEvent" value="true" v-model="selectedEventCopy.paidEvent">
                                                    <label for="paidEventNo">&nbsp;Tickets are paid, and participants will have to make payment at the below link:</label>

                                                    <!-- Payment link -->
                                                    <input v-if="selectedEventCopy.paidEvent == 'true'" type="text" class="form-control" id="paymentLink" v-model="selectedEventCopy.paymentLink" required>
                                                </div>
                                            </div>

                                            <!-- Event location -->
                                            <div class="mb-3">
                                                <label for="eventLocation" class="form-label fw-bold">
                                                    <span v-if="selectedEventCopy.eventType == 'Location'">Event Location</span>
                                                    <span v-else>Event Link</span>
                                                </label>
                                                <input type="text" class="form-control" id="eventLocation" v-model="selectedEventCopy.eventLocation">
                                            </div>

                                            <!-- Event passcodes -->
                                            <div class="mb-3">
                                                <label class="form-label fw-bold">Event Passcodes <span class="text-muted">Optional</span></label>
                                                <small class="text-muted d-block mb-2">Set passcodes with usage limits to control access to your event</small>
                                                
                                                <!-- Passcode input fields -->
                                                <div v-for="(passcode, index) in selectedEventCopy.eventPasscodes" :key="index" class="mb-3 p-3 border rounded">
                                                    <div class="row align-items-end">
                                                        <!-- Passcode input -->
                                                        <div class="col-md-5">
                                                            <label :for="'dashboard-passcode-' + index" class="form-label small">Passcode {{ index + 1 }}</label>
                                                            <input 
                                                                type="text" 
                                                                class="form-control" 
                                                                :id="'dashboard-passcode-' + index"
                                                                v-model="passcode.code" 
                                                                :placeholder="'Enter passcode ' + (index + 1)"
                                                            >
                                                        </div>
                                                        
                                                        <!-- Limit input -->
                                                        <div class="col-md-2">
                                                            <label :for="'dashboard-limit-' + index" class="form-label small">Limit</label>
                                                            <input 
                                                                type="number" 
                                                                class="form-control" 
                                                                :id="'dashboard-limit-' + index"
                                                                v-model.number="passcode.limit" 
                                                                min="1" 
                                                                max="10000"
                                                                placeholder="50"
                                                            >
                                                        </div>
                                                        
                                                        <!-- Usage display -->
                                                        <div class="col-md-3">
                                                            <label class="form-label small">Usage Limit</label>
                                                            <div class="form-control-plaintext small">
                                                                <span class="badge bg-secondary">Max: {{ passcode.limit }}</span>
                                                                <div class="text-muted">Usage tracked via attendees</div>
                                                            </div>
                                                        </div>
                                                        
                                                        <!-- Remove button -->
                                                        <div class="col-md-2">
                                                            <button 
                                                                type="button" 
                                                                class="btn btn-outline-danger btn-sm w-100"
                                                                @click="removePasscodeEdit(index)"
                                                                :disabled="selectedEventCopy.eventPasscodes.length <= 1"
                                                            >
                                                                Remove
                                                            </button>
                                                        </div>
                                                    </div>
                                                </div>
                                                
                                                <!-- Add passcode button -->
                                                <button 
                                                    type="button" 
                                                    class="btn btn-outline-primary btn-sm" 
                                                    @click="addPasscodeEdit"
                                                >
                                                    Add Passcode
                                                </button>
                                            </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" @click="cancelEdit">Close</button>
                                <button type="button" class="btn btn-primary" @click="updateEvent">Save Changes</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Lock/Unlock Signups Modal Start -->
                <div 
                    v-if="showLockSignupsModal" 
                    class="modal d-block" 
                    style="background-color: rgba(0, 0, 0, 0.5); position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1050;"
                    @click.self="closeLockSignupsModal"
                >
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">
                                    <span v-if="selectedEventForSignupManagement && isSignupOpen(selectedEventForSignupManagement)">Lock Event Signups</span>
                                    <span v-else>Unlock Event Signups</span>
                                </h5>
                                <button type="button" class="btn-close" @click="closeLockSignupsModal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <!-- Lock Signups Content -->
                                <div v-if="selectedEventForSignupManagement && isSignupOpen(selectedEventForSignupManagement)">
                                    <p class="fw-bold">Are you sure you want to lock signups for "{{ selectedEventForSignupManagement.eventName }}"?</p>
                                    <p class="text-muted">This action will prevent anyone from RSVPing or withdrawing their RSVP. Existing attendees will remain registered, but no new signups will be allowed.</p>
                                </div>
                                <!-- Unlock Signups Content -->
                                <div v-else-if="selectedEventForSignupManagement">
                                    <p class="fw-bold">Are you sure you want to reopen signups for "{{ selectedEventForSignupManagement.eventName }}"?</p>
                                    <p class="text-muted">This will allow people to RSVP and withdraw their RSVPs again. New attendees will be able to register for the event.</p>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" @click="closeLockSignupsModal">Cancel</button>
                                <button 
                                    v-if="selectedEventForSignupManagement && isSignupOpen(selectedEventForSignupManagement)" 
                                    type="button" 
                                    class="btn lock-signup-btn" 
                                    @click="lockSignups"
                                >
                                    Lock Signups
                                </button>
                                <button 
                                    v-else-if="selectedEventForSignupManagement"
                                    type="button" 
                                    class="btn lock-signup-btn" 
                                    @click="unlockSignups"
                                >
                                    Unlock Signups
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Lock/Unlock Signups Modal End -->

            </div>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import { useToast } from 'vue-toastification';
import Quill from 'quill';
import DOMPurify from 'dompurify';

export default {
    name: 'EventOrganiserDashboard',
    components: {
        NavBar
    },
    data() {
        return {
            // Page state
            dataLoaded: false,
            
            // Route parameters (will be set in mounted)
            dashboardUserType: null,
            dashboardUserID: null,
            
            // Current user (for access control)
            currentUserID: null,
            currentUserType: null,
            
            // Dashboard user information
            dashboardUserInfo: null,
            
            // Tab management
            activeTab: 'upcoming',
            
            // Real data from API
            allOrganisingEvents: [], // Basic event info from getUserOrganisingEvents
            eventsWithAttendees: [], // Combined event + attendee data from new API
            
            upcomingEvents: [],
            pastEvents: [],

            // Statistics 
            totalEvents: 0,
            totalAttendees: 0,
            
            // Loading states
            loadingEvents: false,
            
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
            
            // Edit form data (adapted from SpecificEventPage.vue)
            selectedEventCopy: {}, // Copy of selected event details for editing
            quill: null, // Quill editor instance
            
            // Attendee management data
            expandedEventId: null, // Track which event's attendees are expanded
            attendeesForManagement: {}, // Object to store attendees by event ID
            loadingAttendeeManagement: {}, // Track loading state per event

            // Signup management
            showLockSignupsModal: false,
            selectedEventForSignupManagement: null,

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
            // Ensure both IDs are strings for comparison
            const currentID = String(this.currentUserID);
            const dashboardID = String(this.dashboardUserID);
            
            return currentID === dashboardID && 
                   this.currentUserType === this.dashboardUserType;
        },
        
        // Merge event details with attendee data
        combinedEventsData() {
            return this.allOrganisingEvents.map(event => {
                // Find corresponding attendee data
                const attendeeData = this.eventsWithAttendees.find(
                    attendeeEvent => attendeeEvent.id === event.eventID
                );
                
                return {
                    ...event, // Basic event info (includes signupOpen)
                    id: event.eventID, // Standardize to 'id' for template consistency
                    attendeeCount: attendeeData?.attendeeCount || 0,
                    attendees: attendeeData?.attendees || [],
                    // Ensure signupOpen is properly preserved with default value
                    signupOpen: event.signupOpen !== undefined ? event.signupOpen : true
                };
            });
        },
        
        // Filter events that haven't started yet or are ongoing (upcoming + ongoing)
        upcomingAndOngoingEvents() {
            return this.combinedEventsData.filter(event => {
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
            return this.combinedEventsData.filter(event => {
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
            const totalEvents = this.combinedEventsData.length;
            const totalAttendees = this.combinedEventsData.reduce((sum, event) => sum + (event.attendeeCount || 0), 0);
            const totalCapacity = this.combinedEventsData.reduce((sum, event) => sum + (event.eventLimit || 0), 0);
            const averageFillRate = totalCapacity > 0 ? Math.round((totalAttendees / totalCapacity) * 100) : 0;
            
            return {
                totalEvents,
                totalAttendees,
                averageFillRate,
                topEvents: [...this.combinedEventsData]
                    .sort((a, b) => (b.attendeeCount || 0) - (a.attendeeCount || 0))
                    .slice(0, 3)
            };
        },
        
        // Format display name for dashboard user
        dashboardUserDisplayName() {
            if (!this.dashboardUserInfo) return '';
            
            switch (this.dashboardUserType) {
                case 'user':
                    return `@${this.dashboardUserInfo.username || this.dashboardUserInfo.displayName || 'Unknown User'}`;
                case 'venue':
                    return this.dashboardUserInfo.venueName || 'Unknown Venue';
                case 'producer':
                    return this.dashboardUserInfo.producerName || 'Unknown Producer';
                default:
                    return '';
            }
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
            this.selectedEventCopy = JSON.parse(JSON.stringify(event));
            this.initializeEventPasscodes();
            this.showEventManagementModal = true;
            
            // Initialize Quill editor after modal is shown
            this.$nextTick(() => {
                setTimeout(() => {
                    this.initializeQuillEditor();
                    this.syncQuillEditor();
                }, 200);
            });
        },
        
        closeEventManagementModal() {
            this.showEventManagementModal = false;
            this.selectedEvent = null;
            this.selectedEventCopy = {};
            
            // Clean up Quill editor
            if (this.quill) {
                this.quill = null;
            }
        },

        // Attendee Management methods (adapted from SpecificEventPage.vue)
        
        // Toggle attendee management section
        async toggleAttendeeManagement(event) {
            if (this.expandedEventId === event.id) {
                // Collapse if already expanded
                this.expandedEventId = null;
            } else {
                // Expand and load attendees
                this.expandedEventId = event.id;
                await this.getAttendeesForManagement(event.id);
            }
        },

        // Get attendees with management data for a specific event
        async getAttendeesForManagement(eventId) {
            this.loadingAttendeeManagement[eventId] = true;
            try {
                // Find the event in our combined events data
                const event = this.combinedEventsData.find(e => e.id === eventId);
                if (event && event.attendees) {
                    // Use the attendees we already have
                    this.attendeesForManagement[eventId] = event.attendees;
                } else {
                    // Fallback to API call if attendees not found locally
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getAttendees/${eventId}`);
                    this.attendeesForManagement[eventId] = response.data.attendees;
                }
            } catch (error) {
                console.error('Error fetching attendees for management:', error);
                this.attendeesForManagement[eventId] = [];
            } finally {
                this.loadingAttendeeManagement[eventId] = false;
            }
        },

        // Update attendee payment status
        async updatePaymentStatus(attendeeId, hasPaid) {
            try {
                await this.$axios.put(`${process.env.VUE_APP_API_URL}/events/updateAttendeeStatus`, {
                    attendeeId: attendeeId,
                    hasPaid: hasPaid,
                    eventOwnerID: this.currentUserID,
                    eventOwnerType: this.currentUserType
                });

                const toast = useToast();
                toast.success('Payment status updated successfully!');
            } catch (error) {
                console.error('Error updating payment status:', error);
                const toast = useToast();
                toast.error('Failed to update payment status');
            }
        },

        // Update attendee attendance status
        async updateAttendanceStatus(attendeeId, attendanceStatus) {
            try {
                await this.$axios.put(`${process.env.VUE_APP_API_URL}/events/updateAttendeeStatus`, {
                    attendeeId: attendeeId,
                    attendanceStatus: attendanceStatus,
                    eventOwnerID: this.currentUserID,
                    eventOwnerType: this.currentUserType
                });

                const toast = useToast();
                toast.success('Attendance status updated successfully!');
            } catch (error) {
                console.error('Error updating attendance status:', error);
                const toast = useToast();
                toast.error('Failed to update attendance status');
            }
        },

        // Signup management methods (adapted from SpecificEventPage.vue)
        
        // Check if signups are open for a specific event
        isSignupOpen(event) {
            // Default to true if signupOpen is undefined, similar to SpecificEventPage.vue logic
            if (event.signupOpen === undefined || event.signupOpen === null) {
                return true;
            }
            return event.signupOpen === true || event.signupOpen === 'true';
        },

        // Open signup management modal
        openSignupManagementModal(event) {
            this.selectedEventForSignupManagement = event;
            this.showLockSignupsModal = true;
        },

        // Close signup management modal
        closeLockSignupsModal() {
            this.showLockSignupsModal = false;
            this.selectedEventForSignupManagement = null;
        },

        // Lock signups for an event
        async lockSignups() {
            const toast = useToast();
            
            try {
                await this.$axios.put(`${process.env.VUE_APP_API_URL}/events/lockSignups`, {
                    eventID: this.selectedEventForSignupManagement.id,
                    eventOwnerID: this.currentUserID,
                    eventOwnerType: this.currentUserType
                });

                toast.success('Signups locked successfully!');
                
                // Update the event's signupOpen status locally in allOrganisingEvents
                const eventIndex = this.allOrganisingEvents.findIndex(e => e.eventID === this.selectedEventForSignupManagement.id);
                if (eventIndex !== -1) {
                    this.allOrganisingEvents[eventIndex].signupOpen = false;
                }
                
                this.closeLockSignupsModal();
            } catch (error) {
                console.error('Error locking signups:', error);
                toast.error('Failed to lock signups. Please try again.');
            }
        },

        // Unlock signups for an event
        async unlockSignups() {
            const toast = useToast();
            
            try {
                await this.$axios.put(`${process.env.VUE_APP_API_URL}/events/unlockSignups`, {
                    eventID: this.selectedEventForSignupManagement.id,
                    eventOwnerID: this.currentUserID,
                    eventOwnerType: this.currentUserType
                });

                toast.success('Signups unlocked successfully!');
                
                // Update the event's signupOpen status locally in allOrganisingEvents
                const eventIndex = this.allOrganisingEvents.findIndex(e => e.eventID === this.selectedEventForSignupManagement.id);
                if (eventIndex !== -1) {
                    this.allOrganisingEvents[eventIndex].signupOpen = true;
                }
                
                this.closeLockSignupsModal();
            } catch (error) {
                console.error('Error unlocking signups:', error);
                toast.error('Failed to unlock signups. Please try again.');
            }
        },

        // Edit form methods (adapted from SpecificEventPage.vue)
        
        // Function to cancel editing event details
        cancelEdit() {
            if (this.selectedEvent) {
                this.selectedEventCopy = JSON.parse(JSON.stringify(this.selectedEvent));
                this.initializeEventPasscodes();
                this.syncQuillEditor();
            }
            this.closeEventManagementModal();
        },

        // Function to add a new passcode field in edit mode
        addPasscodeEdit() {
            this.selectedEventCopy.eventPasscodes.push({ code: '', limit: 50 });
        },

        // Function to remove a passcode field in edit mode
        removePasscodeEdit(index) {
            if (this.selectedEventCopy.eventPasscodes.length > 1) {
                this.selectedEventCopy.eventPasscodes.splice(index, 1);
            }
        },

        // Function to initialize eventPasscodes array for editing
        initializeEventPasscodes() {
            if (this.selectedEvent.passcode && Array.isArray(this.selectedEvent.passcode)) {
                // Handle JSONB format: array of objects with code and limit
                this.selectedEventCopy.eventPasscodes = this.selectedEvent.passcode.map(p => ({
                    code: p.code || '',
                    limit: p.limit || 50
                }));
            } else {
                this.selectedEventCopy.eventPasscodes = [{ code: '', limit: 50 }];
            }
        },

        // Function to sync Quill editor with selectedEventCopy.eventDesc
        syncQuillEditor() {
            if (this.quill) {
                this.$nextTick(() => {
                    setTimeout(() => {
                        if (this.selectedEventCopy.eventDesc) {
                            this.quill.root.innerHTML = this.selectedEventCopy.eventDesc;
                        } else {
                            this.quill.setText('');
                        }
                    }, 100);
                });
            }
        },

        // Function to initialize Quill editor
        initializeQuillEditor() {
            if (!document.getElementById('dashboard-editor-container')) {
                return;
            }
            
            if (this.quill) {
                // Destroy existing instance
                this.quill = null;
            }

            this.quill = new Quill('#dashboard-editor-container', {
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
        },

        // Function to upload images (adapted from SpecificEventPage.vue)
        async uploadImages(event) {
            const files = event.target.files;
            const toast = useToast();

            if (!files || files.length === 0) {
                return;
            }

            if (!this.selectedEventCopy.eventBanners) {
                this.selectedEventCopy.eventBanners = [];
            }

            if (this.selectedEventCopy.eventBanners.length + files.length > 3) {
                toast.error('You can only upload up to 3 images.');
                return;
            }

            for (let file of files) {
                if (file.size > 5 * 1024 * 1024) { // 5MB limit
                    toast.error(`File ${file.name} is too large. Maximum size is 5MB.`);
                    continue;
                }

                try {
                    const formData = new FormData();
                    formData.append('image', file);
                    
                    const response = await this.$axios.post(
                        `${process.env.VUE_APP_API_URL}/events/uploadEventBanner`,
                        formData,
                        {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            }
                        }
                    );

                    if (response.data && response.data.imageUrl) {
                        this.selectedEventCopy.eventBanners.push(response.data.imageUrl);
                    }
                } catch (error) {
                    console.error('Error uploading image:', error);
                    toast.error(`Failed to upload ${file.name}`);
                }
            }
        },

        // Function to remove uploaded photo
        removePhotoNew(index) {
            this.selectedEventCopy.eventBanners.splice(index, 1);
        },

        // Function to update event details (adapted from SpecificEventPage.vue)
        async updateEvent() {
            const toast = useToast();

            // Show loading toast
            const toastId = toast.info('Updating event details...', {
                timeout: false,
                closeOnClick: false,
                pauseOnHover: true,
            });

            try {
                // Get the event description from the editor
                this.selectedEventCopy.eventDesc = this.quill.root.innerHTML;
                
                // Sanitize the event description
                this.selectedEventCopy.eventDesc = DOMPurify.sanitize(this.selectedEventCopy.eventDesc);

                // Get current time
                let currentTime = new Date().toTimeString().split(' ')[0];
                let currentDate = new Date().toISOString().split('T')[0];

                if (this.selectedEventCopy.allDay == true) {
                    this.selectedEventCopy.eventStartTime = '00:00';
                    this.selectedEventCopy.eventEndTime = '23:59';
                } else {
                    // Check if the event time is valid
                    if (this.selectedEventCopy.eventStartDate == currentDate && this.selectedEventCopy.eventStartTime <= currentTime) {
                        toast.dismiss(toastId);
                        toast.error('Event start time cannot be earlier than current time.');
                        return;
                    }
                    if (this.selectedEventCopy.eventEndDate != null && this.selectedEventCopy.eventEndDate != '' ) {
                        if (this.selectedEventCopy.eventEndDate < this.selectedEventCopy.eventStartDate) {
                            toast.dismiss(toastId);
                            toast.error('Event end date cannot be earlier than event start date.');
                            return;
                        }
                        if (this.selectedEventCopy.eventEndDate == this.selectedEventCopy.eventStartDate && this.selectedEventCopy.eventEndTime <= this.selectedEventCopy.eventStartTime) {
                            toast.dismiss(toastId);
                            toast.error('Event end time cannot be earlier than event start time.');
                            return;
                        }
                    }
                }

                // Process eventPasscodes before comparison
                if (this.selectedEventCopy.eventPasscodes) {
                    const validPasscodes = this.selectedEventCopy.eventPasscodes.filter(p => p && p.code && p.code.trim());
                    this.selectedEventCopy.eventPasscodes = validPasscodes.length > 0 ? validPasscodes : null;
                }

                // Compare with original event to find changes
                // Use the correct ID field - try multiple possibilities
                const eventID = this.selectedEvent.id || this.selectedEvent.eventID || this.selectedEvent.ID;
                
                if (!eventID) {
                    toast.dismiss(toastId);
                    toast.error('Event ID is missing. Cannot update event.');
                    return;
                }
                
                const changedFields = { 
                    eventID: eventID,
                    eventOwnerID: this.currentUserID,
                    eventOwnerType: this.currentUserType
                };
                const fieldsToCheck = [
                    'eventName', 'eventDesc', 'eventType', 'eventStartDate', 'eventStartTime',
                    'eventEndDate', 'eventEndTime', 'allDay', 'eventBanners', 'eventLimit',
                    'ticketed', 'paidEvent', 'paymentLink', 'eventLocation', 'eventPasscodes'
                ];

                fieldsToCheck.forEach(field => {
                    if (JSON.stringify(this.selectedEventCopy[field]) !== JSON.stringify(this.selectedEvent[field])) {
                        changedFields[field] = this.selectedEventCopy[field];
                    }
                });

                // Only proceed if there are changes
                if (Object.keys(changedFields).length === 3) { // Only eventID, eventOwnerID, eventOwnerType means no changes
                    toast.dismiss(toastId);
                    toast.info('No changes detected.');
                    this.closeEventManagementModal();
                    return;
                }

                // Make API call to update event
                await this.$axios.put(`${process.env.VUE_APP_API_URL}/events/updateEvent`, changedFields);

                toast.dismiss(toastId);
                toast.success('Event updated successfully!');

                // Close modal and refresh event list
                this.closeEventManagementModal();
                await this.fetchOrganizerEvents();

            } catch (error) {
                toast.dismiss(toastId);
                console.error('Error updating event:', error);
                
                let errorMessage = 'Failed to update event. Please try again.';
                if (error.response && error.response.data && error.response.data.message) {
                    errorMessage = error.response.data.message;
                }
                toast.error(errorMessage);
            }
        },
        
        // Fetch all events the user is organizing with attendee data
        async fetchOrganizerEvents() {
            this.loadingEvents = true;
            try {
                // Fetch basic event information
                const basicEventsResponse = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/events/getUserOrganisingEvents/${this.dashboardUserID}/${this.dashboardUserType}`
                );
                this.allOrganisingEvents = basicEventsResponse.data.events || [];
                
                // Debug log to check what signupOpen data we're getting from the API
                console.log('fetchOrganizerEvents - allOrganisingEvents with signupOpen data:', 
                    this.allOrganisingEvents.map(event => ({
                        id: event.eventID,
                        name: event.eventName,
                        signupOpen: event.signupOpen
                    }))
                );
                
                // Fetch attendee data
                const attendeesResponse = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/events/getOrganizerEventsWithAttendees/${this.dashboardUserID}/${this.dashboardUserType}`
                );
                this.eventsWithAttendees = attendeesResponse.data.events || [];
                this.totalEvents = attendeesResponse.data.totalEvents || 0;
                this.totalAttendees = attendeesResponse.data.totalAttendees || 0;
                
            } catch (error) {
                console.error('Error fetching organizer events:', error);
                if (error.response && error.response.status === 404) {
                    // No events found, that's okay
                    this.allOrganisingEvents = [];
                    this.eventsWithAttendees = [];
                    this.totalEvents = 0;
                    this.totalAttendees = 0;
                } else {
                    this.dataLoaded = null;
                    const toast = useToast();
                    toast.error('Failed to load events. Please try again.');
                }
            } finally {
                this.loadingEvents = false;
            }
        },
        
        // Fetch dashboard user information
        async fetchDashboardUserInfo() {
            console.log('fetchDashboardUserInfo called with:', {
                userType: this.dashboardUserType,
                userID: this.dashboardUserID,
                apiUrl: process.env.VUE_APP_API_URL
            });
            
            let endpoint;
            try {
                switch (this.dashboardUserType) {
                    case 'user':
                        endpoint = `/getData/getUser/${this.dashboardUserID}`;
                        break;
                    case 'venue':
                        endpoint = `/getData/getVenue/${this.dashboardUserID}`;
                        break;
                    case 'producer':
                        endpoint = `/getData/getProducer/${this.dashboardUserID}`;
                        break;
                    default:
                        console.error('Invalid dashboard user type:', this.dashboardUserType);
                        return;
                }
                
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}${endpoint}`);
                this.dashboardUserInfo = response.data;
            } catch (error) {
                console.error('Error fetching dashboard user info:', error);
                console.error('Failed endpoint:', endpoint);
                // Don't fail the whole page if user info fails to load
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
            console.log('initializeDashboard - Access check:', {
                canViewDashboard: this.canViewDashboard,
                currentUserID: this.currentUserID,
                dashboardUserID: this.dashboardUserID,
                currentUserType: this.currentUserType,
                dashboardUserType: this.dashboardUserType
            });
            
            // Check access permissions
            if (!this.canViewDashboard) {
                console.error('Access denied - user cannot view this dashboard');
                const toast = useToast();
                toast.error('You are not authorized to view this dashboard');
                this.$router.push('/events/view');
                return;
            }
            
            try {
                console.log('Access granted - fetching data...');
                // Fetch real data
                await Promise.all([
                    this.fetchOrganizerEvents(),
                    this.fetchDashboardUserInfo()
                ]);
                console.log('Data fetched successfully, dashboardUserInfo:', this.dashboardUserInfo);
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
        
        // Get route parameters
        this.dashboardUserType = this.$route.params.userType;
        this.dashboardUserID = this.$route.params.userID;
        
        console.log('Route params extracted:', {
            dashboardUserType: this.dashboardUserType,
            dashboardUserID: this.dashboardUserID,
            currentUserID: this.currentUserID,
            currentUserType: this.currentUserType
        });
        
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

<style>
/* Import Quill styles */
@import 'quill/dist/quill.snow.css';

/* Resize Quill toolbar icons */
.ql-toolbar .ql-formats button {
    width: 28px;
    height: 28px;
    padding: 3px;
}

.ql-toolbar .ql-formats .ql-picker {
    font-size: 14px;
}

.ql-editor {
    font-size: 14px;
    line-height: 1.5;
}

/* Primary button color for dashboard */
.primary-btn-red {
    background-color: #dc3545;
    border-color: #dc3545;
    color: white;
}

.primary-btn-red:hover {
    background-color: #c82333;
    border-color: #bd2130;
    color: white;
}

/* Lock/Unlock Signups Button Hover Effects */
.lock-signup-btn {
    background-color: #ff6000 !important;
    color: white !important;
    font-weight: bold !important;
    /* border-radius: 30px !important; */
    transition: background-color 0.3s ease !important;
}

.lock-signup-btn:hover {
    background-color: #e55500 !important;
    color: white !important;
}

/* Modal form alignment */
.modal-body .tab-content {
    text-align: left;
}

.modal-body .form-label {
    text-align: left;
    display: block;
}

.modal-body .form-check-label {
    text-align: left;
}
</style>

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

.primary-btn,
.primary-btn-outline:hover {
  color: black; /*TZH changed whitesmoke to black*/
  background-color: #f0b258; /*TZH changed 535C72 to F0B258 */
  border: 4px solid #f0b258; /*TZH changed 535C72 to F0B258 */
  font-weight: bold;
}

.primary-btn-outline,
.primary-btn:hover {
  color: black; /*TZH changed 535C72 to black */
  background-color: #c9964a; /*TZH changed whitesmoke to c9964a */
  border: 4px solid #f0b258; /*TZH changed 535C72 to c9964a */
  font-weight: bold;
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
    padding: 0.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
}

.event-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border-color: #dee2e6;
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

/* Event Title Link Styling */
.event-title-link {
    text-decoration: none;
    color: inherit;
    display: block;
    transition: color 0.2s ease;
}

.event-title-link:hover {
    text-decoration: none;
}

.event-title-link:hover .event-title {
    color: #027562;
}

.event-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
    color: #212529;
    transition: color 0.2s ease;
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
    gap: 0.75rem;
    flex-shrink: 0;
    min-width: 200px;
}

.event-stats .button-group {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: flex-end;
}

.attendee-count {
    text-align: right;
}

.attendee-count .count {
    display: block;
    font-size: 1rem;
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

/* Edit Event Button */
.edit-event-btn {
    font-size: 0.8rem;
    padding: 0.375rem 0.75rem;
    border-radius: 6px;
    transition: all 0.2s ease;
    white-space: nowrap;
}

.edit-event-btn:focus {
    box-shadow: 0 0 0 0.2rem rgba(2, 117, 98, 0.25);
}

.edit-event-btn i {
    font-size: 0.75rem;
}

/* Attendee Count Button */
.attendee-count-btn {
    background: #027562;
    border: 2px solid #027562;
    border-radius: 8px;
    padding: 8px 12px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    color: inherit;
    box-shadow: 0 2px 4px rgba(2, 117, 98, 0.1);
}

.attendee-count-btn:hover {
    background: #ffffff;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(2, 117, 98, 0.2);
}

.attendee-count-btn:hover .count,
.attendee-count-btn:hover .label {
    color: #027562 !important;
}

.attendee-count-btn.active {
    background: #027562;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(2, 117, 98, 0.2);
}

.attendee-count-btn.active .count,
.attendee-count-btn.active .label {
    color: white !important;
}

.attendee-count-btn.compressed {
    transform: scale(0.95);
    opacity: 0.8;
}

.attendee-count-btn .count {
    display: block;
    font-size: 1rem;
    font-weight: 700;
    color: white;
}

.attendee-count-btn .label {
    display: block;
    font-size: 0.75rem;
    color: white;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Attendee Management Drawer */
.attendee-management-drawer {
    width: 100%;
    margin-top: 1rem;
    margin-bottom: 1rem;
    animation: slideDown 0.3s ease-out;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.attendee-management-content {
    background: #f8f9fa;
    padding: 1.5rem;
    border-left: 4px solid #027562;
    width: 100%;
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
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
        gap: 1rem;
    }
    
    .event-stats .button-group {
        flex-direction: column;
        gap: 0.25rem;
        margin-left: auto;
        flex-shrink: 0;
    }
    
    .edit-event-btn {
        flex-shrink: 0;
    }
    
    .attendee-count-btn {
        text-align: center;
    }
    
    .attendee-management-content {
        padding: 1rem;
    }
    
    .attendee-management-drawer .table-responsive {
        font-size: 0.8rem;
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
    
    .attendee-count-btn {
        font-size: 0.9rem;
    }
    
    .attendee-management-content {
        padding: 0.5rem;
    }
    
    .attendee-management-drawer .table-responsive {
        font-size: 0.75rem;
    }
    
    .attendee-management-drawer .table th,
    .attendee-management-drawer .table td {
        padding: 0.3rem 0.2rem;
        white-space: nowrap;
    }
}
</style>