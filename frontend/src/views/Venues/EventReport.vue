<!-- Event Report Page -->
<!-- Post-event analytics and insights for festival/event organizers -->

<template>
    <div>
        <NavBar />
        
        <!-- Main Content Container -->
        <div class="container pt-5 mobile-pt-3">
            
            <!-- Loading State -->
            <LoadingWithFunFact v-if="!dataLoaded" />
            
            <!-- Access Denied for Non-Festival Venues -->
            <div v-else-if="!isAuthorized" class="text-center py-5">
                <div class="alert alert-warning" role="alert">
                    <h4 class="alert-heading">Access Denied</h4>
                    <p>This page is only available to festival/event venue owners.</p>
                    <hr>
                    <p class="mb-0">
                        <router-link to="/" class="btn btn-primary">Return to Homepage</router-link>
                    </p>
                </div>
            </div>
            
            <!-- Event Report Content -->
            <div v-else>
                <div class="row">
                    <div class="col-12">
                        <!-- Print Button - Hidden in print view -->
                        <div class="d-print-none mb-4">
                            <button @click="printReport" class="btn btn-outline-primary">
                                <i class="fas fa-print me-2"></i>Print Report
                            </button>
                        </div>
                        
                        <!-- Main Title -->
                        <h1 class="mb-2">Drink-X Event Report: {{ venueName }}</h1>
                        <p class="text-muted mb-4">Date Generated: {{ getCurrentDate() }}</p>
                        
                        <!-- Event Overview & Summary -->
                        <div class="mb-5">
                            <h2 class="mb-3">Event Overview & Summary</h2>
                            <div v-if="analyticsData">
                                <div class="row mt-3">
                                    <div class="col-md-6">
                                        
                                    </div>
                                    <div class="col-md-6">

                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-3 col-6 mb-3">
                                        <div class="card text-center">
                                            <div class="card-body">
                                                <h3 class="text-primary">{{ analyticsData.totalStats.totalTastings }}</h3>
                                                <p class="mb-0">Total Tastings</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3 col-6 mb-3">
                                        <div class="card text-center">
                                            <div class="card-body">
                                                <h3 class="text-success">{{ analyticsData.totalStats.totalUniqueAttendees }}</h3>
                                                <p class="mb-0">Unique Tasters</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3 col-6 mb-3">
                                        <div class="card text-center">
                                            <div class="card-body">
                                                <h3 class="text-warning">{{ analyticsData.totalStats.totalUniqueItems }}</h3>
                                                <p class="mb-0">Items Tasted</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3 col-6 mb-3">
                                        <div class="card text-center">
                                            <div class="card-body">
                                                <h3 class="text-info">{{ analyticsData.totalStats.activeDays }}</h3>
                                                <p class="mb-0">Active Days</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div v-else class="text-center py-4">
                                <p class="text-muted">Loading event overview data...</p>
                            </div>
                        </div>
                        
                        <!-- Attendee Engagement Metrics -->
                        <div class="mb-5">
                            <h2 class="mb-3">Attendee Engagement Metrics</h2>
                            <div v-if="analyticsData">
                                <!-- Average Items Per Attendee -->
                                <div class="card mb-4">
                                    <div class="card-header">
                                        <h4 class="mb-0">Average Items Tasted Per Attendee</h4>
                                    </div>
                                    <div class="card-body">
                                        <div class="row text-center">
                                            <div class="col-md-4">
                                                <h2 class="text-primary">{{ analyticsData.averageItemsPerAttendee.average }}</h2>
                                                <p class="text-muted">Average number of items tasted per attendee</p>
                                            </div>
                                            <div class="col-md-4">
                                                <h5>{{ analyticsData.averageItemsPerAttendee.totalTastings }}</h5>
                                                <p class="text-muted">Total tastings</p>
                                            </div>
                                            <div class="col-md-4">
                                                <h5>{{ analyticsData.averageItemsPerAttendee.uniqueAttendees }}</h5>
                                                <p class="text-muted">Unique tasters</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Top Tasters -->
                                <div class="card mb-4">
                                    <div class="card-header">
                                        <h4 class="mb-0">Top Tasters</h4>
                                    </div>
                                    <div class="card-body">
                                        <div class="table-responsive">
                                            <table class="table">
                                                <thead>
                                                    <tr>
                                                        <th>Rank</th>
                                                        <th>User</th>
                                                        <th>Items Tasted</th>
                                                        <th>Unique Items</th>
                                                        <th>Activity Period</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr v-for="(taster, index) in analyticsData.topTasters" :key="taster.userId">
                                                        <td>{{ index + 1 }}</td>
                                                        <td>
                                                            <div class="d-flex align-items-center">
                                                                <img v-if="taster.photo" :src="taster.photo" 
                                                                     class="rounded-circle me-2" width="32" height="32" 
                                                                     :alt="taster.displayName">
                                                                <div>
                                                                    <div class="fw-bold">{{ taster.displayName || taster.username }}</div>
                                                                    <small class="text-muted">@{{ taster.username }}</small>
                                                                </div>
                                                            </div>
                                                        </td>
                                                        <td><span class="badge bg-primary">{{ taster.itemsTasted }}</span></td>
                                                        <td>{{ taster.uniqueItemsTasted }}</td>
                                                        <td>
                                                            <small>
                                                                {{ formatDate(taster.firstTasting) }} - 
                                                                {{ formatDate(taster.lastTasting) }}
                                                            </small>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>

                                <!-- Daily Tasting Velocity -->
                                <div class="card">
                                    <div class="card-header">
                                        <h4 class="mb-0">Daily Tasting Activity</h4>
                                    </div>
                                    <div class="card-body">
                                        <div class="table-responsive">
                                            <table class="table table-sm">
                                                <thead>
                                                    <tr>
                                                        <th>Date</th>
                                                        <th>Total Tastings</th>
                                                        <th>Unique Tasters</th>
                                                        <th>Unique Items</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr v-for="day in analyticsData.tastingVelocity.slice(0, 10)" :key="day.date">
                                                        <td>{{ formatDate(day.date) }}</td>
                                                        <td><span class="badge bg-success">{{ day.dailyTastings }}</span></td>
                                                        <td>{{ day.dailyUniqueTasters }}</td>
                                                        <td>{{ day.dailyUniqueItems }}</td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                        <div v-if="analyticsData.tastingVelocity.length > 10" class="text-center mt-3">
                                            <button class="btn btn-outline-primary btn-sm" @click="showAllVelocityData = !showAllVelocityData">
                                                {{ showAllVelocityData ? 'Show Less' : `Show All ${analyticsData.tastingVelocity.length} Days` }}
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div v-else class="text-center py-4">
                                <p class="text-muted">Loading engagement metrics...</p>
                            </div>
                        </div>
                        
                        <!-- Item Performance Analytics -->
                        <div class="mb-5">
                            <h2 class="mb-3">Item Performance Analytics</h2>
                            <div v-if="analyticsData">
                                <div class="card">
                                    <div class="card-header">
                                        <h4 class="mb-0">Top 5 Most Popular Items</h4>
                                    </div>
                                    <div class="card-body">
                                        <div class="row">
                                            <div v-for="(item, index) in analyticsData.topItems" :key="item.itemId" class="col-12 mb-4">
                                                <div class="card border">
                                                    <div class="card-body">
                                                        <div class="row align-items-center">
                                                            <div class="col-md-1 text-center">
                                                                <h3 class="text-primary mb-0">#{{ index + 1 }}</h3>
                                                            </div>
                                                            <div class="col-md-2">
                                                                <img v-if="item.photo" :src="item.photo" 
                                                                     class="img-fluid rounded" :alt="item.listingName"
                                                                     style="max-height: 80px; object-fit: cover;">
                                                                <div v-else class="bg-light rounded d-flex align-items-center justify-content-center" 
                                                                     style="height: 80px;">
                                                                    <i class="fas fa-wine-bottle text-muted"></i>
                                                                </div>
                                                            </div>
                                                            <div class="col-md-5">
                                                                <h5 class="mb-1">{{ item.listingName }}</h5>
                                                                <p class="text-muted mb-1">
                                                                    <strong>{{ item.producerName }}</strong>
                                                                    <span v-if="item.originCountry"> • {{ item.originCountry }}</span>
                                                                </p>
                                                                <p class="mb-0">
                                                                    <span class="badge bg-secondary me-2">{{ item.drinkType }}</span>
                                                                    <span v-if="item.drinkStyle" class="badge bg-outline-secondary me-2">{{ item.drinkStyle }}</span>
                                                                    <span v-if="item.abv" class="text-muted">{{ item.abv }}% ABV</span>
                                                                </p>
                                                            </div>
                                                            <div class="col-md-4 text-end">
                                                                <div class="row text-center">
                                                                    <div class="col-6">
                                                                        <h4 class="text-primary mb-0">{{ item.totalTastings }}</h4>
                                                                        <small class="text-muted">Total Tastings</small>
                                                                    </div>
                                                                </div>
                                                                <div v-if="item.variantsTasted && item.variantsTasted.length > 0" class="mt-2">
                                                                    <small class="text-muted">
                                                                        Vintages: {{ item.variantsTasted.join(', ') }}
                                                                    </small>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div v-else class="text-center py-4">
                                <p class="text-muted">Loading item performance data...</p>
                            </div>
                        </div>
                        
                        <!-- Section Performance Analysis -->
                        <div class="mb-5">
                            <h2 class="mb-3">Section Performance Analysis</h2>
                            <div v-if="analyticsData">
                                <div class="card">
                                    <div class="card-header">
                                        <h4 class="mb-0">Top 5 Most Popular Sections</h4>
                                    </div>
                                    <div class="card-body">
                                        <!-- Debug info -->
                                        <div v-if="!analyticsData.topSections || analyticsData.topSections.length === 0" class="alert alert-info">
                                            <i class="fas fa-info-circle me-2"></i>
                                            No section data available. This might indicate that no tasting data exists yet, or there's an issue with the section analytics.
                                        </div>
                                        
                                        <!-- Sections display -->
                                        <div v-else class="row">
                                            <div v-for="(section, index) in analyticsData.topSections" :key="section.sectionId" class="col-12 mb-4">
                                                <div class="card border">
                                                    <div class="card-body">
                                                        <div class="row align-items-center">
                                                            <div class="col-md-1 text-center">
                                                                <h3 class="text-success mb-0">#{{ index + 1 }}</h3>
                                                            </div>
                                                            <div class="col-md-2 text-center">
                                                                <div class="bg-success bg-opacity-10 rounded-circle d-flex align-items-center justify-content-center mx-auto" 
                                                                     style="height: 80px; width: 80px;">
                                                                    <i class="fas fa-list-ul text-success fa-2x"></i>
                                                                </div>
                                                            </div>
                                                            <div class="col-md-5">
                                                                <h5 class="mb-1">{{ section.sectionName || 'Unnamed Section' }}</h5>
                                                                <!--<p class="text-muted mb-1">
                                                                    <strong>Section Order:</strong> {{ section.sectionOrder || 'N/A' }}
                                                                    <span v-if="section.isSubSection" class="badge bg-info ms-2">Subsection</span>
                                                                    <span v-else class="badge bg-primary ms-2">Main Section</span>
                                                                </p>-->
                                                                <p class="mb-0">
                                                                    <span class="badge bg-secondary me-2">{{ section.uniqueItemsTasted || 0 }} Items Tasted</span>
                                                                    <!--<span class="text-muted">{{ section.penetrationRate || 0 }}% Taster Penetration</span>-->
                                                                </p>
                                                            </div>
                                                            <div class="col-md-4">
                                                                <div class="row text-center">
                                                                    <div class="col-6">
                                                                        <h4 class="text-success mb-0">{{ section.totalTastings || 0 }}</h4>
                                                                        <small class="text-muted">Total Tastings</small>
                                                                    </div>
                                                                    <div class="col-6">
                                                                        <h4 class="text-info mb-0">{{ section.uniqueTasters || 0 }}</h4>
                                                                        <small class="text-muted">Unique Tasters</small>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div v-else class="text-center py-4">
                                <p class="text-muted">Loading section performance data...</p>
                            </div>
                        </div>
                        
                        <!-- Poll Results Summary -->
                        <div class="mb-5">
                            <h2 class="mb-3">Poll Results Summary</h2>
                            
                            <!-- Loading State -->
                            <div v-if="!pollsLoaded" class="text-center py-4">
                                <p class="text-muted">Loading poll data...</p>
                            </div>
                            
                            <!-- No Polls State -->
                            <div v-else-if="!pollData || pollData.polls.length === 0" class="alert alert-info">
                                <i class="fas fa-info-circle me-2"></i>
                                No polls found for this venue. Create polls to gather attendee feedback and see results here.
                            </div>
                            
                            <!-- Poll Results Content -->
                            <div v-else>
                                <!-- Summary Stats -->
                                <div class="row mb-4">
                                    <div class="col-md-4 col-6 mb-3">
                                        <div class="card text-center">
                                            <div class="card-body">
                                                <h3 class="text-primary">{{ pollData.summary.totalPolls }}</h3>
                                                <p class="mb-0">Total Polls</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 col-6 mb-3">
                                        <div class="card text-center">
                                            <div class="card-body">
                                                <h3 class="text-success">{{ pollData.summary.totalResponses }}</h3>
                                                <p class="mb-0">Total Responses</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 col-12 mb-3">
                                        <div class="card text-center">
                                            <div class="card-body">
                                                <h3 class="text-info">{{ pollData.summary.uniqueRespondents }}</h3>
                                                <p class="mb-0">Unique Respondents</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Individual Poll Results -->
                                <div class="row">
                                    <div v-for="(poll, index) in pollData.polls" :key="poll.pollId" class="col-12 mb-4">
                                        <div class="card">
                                            <div class="card-header">
                                                <div class="d-flex justify-content-between align-items-start">
                                                    <div>
                                                        <h5 class="mb-1">{{ poll.pollTitle }}</h5>
                                                        <p class="mb-0 text-muted">{{ poll.questionText }}</p>
                                                    </div>
                                                    <span class="badge bg-secondary">{{ poll.totalResponses }} responses</span>
                                                </div>
                                            </div>
                                            <div class="card-body">
                                                <!-- Multiple Choice Results -->
                                                <div v-if="poll.processedResults && poll.processedResults.type === 'multiple_choice'">
                                                    <div class="row">
                                                        <div v-for="(option, optionId) in poll.processedResults.optionCounts" :key="optionId" class="col-md-6 mb-3">
                                                            <div class="d-flex justify-content-between align-items-center mb-1">
                                                                <span class="fw-medium">{{ option.text }}</span>
                                                                <span class="text-muted">{{ option.count }} ({{ option.percentage }}%)</span>
                                                            </div>
                                                            <div class="progress" style="height: 8px;">
                                                                <div class="progress-bar" 
                                                                     :style="{ width: option.percentage + '%' }"
                                                                     :class="'bg-' + getProgressBarColor(index)">
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                                
                                                <!-- Rating Results -->
                                                <div v-else-if="poll.processedResults && poll.processedResults.type === 'rating'">
                                                    <div class="row">
                                                        <div class="col-md-6">
                                                            <div class="text-center mb-3">
                                                                <h2 class="text-primary mb-0">{{ poll.processedResults.average }}</h2>
                                                                <p class="text-muted mb-0">Average Rating</p>
                                                                <small class="text-muted">Based on {{ poll.processedResults.totalRatings }} ratings</small>
                                                            </div>
                                                        </div>
                                                        <div class="col-md-6">
                                                            <h6 class="mb-2">Rating Distribution</h6>
                                                            <div v-for="(count, rating) in poll.processedResults.distribution" :key="rating" class="d-flex align-items-center mb-1">
                                                                <span class="me-2" style="min-width: 30px;">{{ rating }}★</span>
                                                                <div class="progress flex-grow-1 me-2" style="height: 6px;">
                                                                    <div class="progress-bar bg-warning" 
                                                                         :style="{ width: poll.processedResults.totalRatings > 0 ? (count / poll.processedResults.totalRatings * 100) + '%' : '0%' }">
                                                                    </div>
                                                                </div>
                                                                <span class="text-muted" style="min-width: 30px;">{{ count }}</span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                                
                                                <!-- Fallback for other question types -->
                                                <div v-else>
                                                    <p class="text-muted">{{ poll.totalResponses }} responses received</p>
                                                    <small class="text-muted">Question type: {{ poll.questionType }}</small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
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
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';

export default {
    name: 'EventReport',
    components: {
        NavBar,
        LoadingWithFunFact
    },
    data() {
        return {
            dataLoaded: false,
            isAuthorized: false,
            venueName: '',
            venueData: null,
            analyticsData: null,
            analyticsLoaded: false,
            pollData: null,
            pollsLoaded: false,
            showAllVelocityData: false,
            viewerType: localStorage.getItem('88B_accType') || '',
            viewerID: localStorage.getItem('88B_accID') || '',
            venueID: this.$route.params.venueID
        }
    },
    async mounted() {
        console.log('🎪 EventReport: Component mounted');
        console.log('📍 Route params:', this.$route.params);
        console.log('👤 Viewer info:', { type: this.viewerType, id: this.viewerID });
        
        await this.loadVenueData();
        this.checkAuthorization();
        
        // Load analytics data if authorized
        if (this.isAuthorized) {
            await this.loadAnalyticsData();
            await this.loadPollData();
        }
        
        this.dataLoaded = true;
    },
    methods: {
        printReport() {
            // Trigger the browser's print dialog
            // The CSS @media print rules will handle hiding non-report elements
            window.print();
        },
        
        async loadVenueData() {
            try {
                console.log('🔄 Loading venue data for ID:', this.venueID);
                
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getVenue/${this.venueID}`
                );
                
                if (response.status === 200 && response.data) {
                    this.venueData = response.data;
                    this.venueName = response.data.venueName || 'Unknown Venue';
                    console.log('✅ Venue data loaded:', this.venueData);
                } else {
                    console.error('❌ Failed to load venue data');
                    this.venueData = null;
                }
            } catch (error) {
                console.error('❌ Error loading venue data:', error);
                this.venueData = null;
            }
        },
        
        checkAuthorization() {
            // Check if user is logged in as a venue
            const isVenueOwner = this.viewerType === 'venue';
            
            // Check if the logged-in venue is the same as the requested venue
            const isOwnVenue = this.viewerID === this.venueID;
            
            // Check if the venue is a festival/event venue
            const isFestivalVenue = this.venueData?.specialStatus === 'EVENT_FESTIVAL';
            
            this.isAuthorized = isVenueOwner && isOwnVenue && isFestivalVenue;
            
            console.log('🔐 Authorization check:', {
                isVenueOwner,
                isOwnVenue,
                isFestivalVenue,
                specialStatus: this.venueData?.specialStatus,
                isAuthorized: this.isAuthorized
            });
            
            // Redirect if not authorized
            if (!this.isAuthorized && this.dataLoaded) {
                console.log('🚫 Access denied - redirecting');
                this.$router.push('/');
            }
        },
        
        async loadAnalyticsData() {
            try {
                console.log('📊 Loading analytics data for venue:', this.venueID);
                
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getUserFestivalTastedListAggregatedData/${this.venueID}`
                );
                
                console.log('📊 Raw response:', response);
                
                if (response.status === 200 && response.data?.success) {
                    this.analyticsData = response.data.data;
                    this.analyticsLoaded = true;
                    console.log('✅ Analytics data loaded:', this.analyticsData);
                    console.log('🔍 TopSections data:', this.analyticsData.topSections);
                } else {
                    console.error('❌ Failed to load analytics data:', response.data);
                    this.analyticsData = null;
                }
            } catch (error) {
                console.error('❌ Error loading analytics data:', error);
                console.error('❌ Error details:', {
                    message: error.message,
                    response: error.response,
                    status: error.response?.status,
                    data: error.response?.data
                });
                
                // Handle specific error cases
                if (error.response?.status === 500) {
                    console.log('🔧 Server error - analytics may not be available yet');
                } else if (error.response?.status === 404) {
                    console.log('📭 No analytics data found for this venue');
                }
                
                this.analyticsData = null;
            }
        },
        
        async loadPollData() {
            try {
                console.log('📊 Loading poll data for venue:', this.venueID);
                
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getPollResponses/${this.venueID}/venue`
                );
                
                if (response.status === 200 && response.data?.code === 200) {
                    console.log('✅ Poll data loaded successfully');
                    console.log('📊 Poll data:', response.data.data);
                    
                    this.pollData = this.processPollData(response.data.data);
                    this.pollsLoaded = true;
                } else {
                    console.error('❌ Failed to load poll data:', response.data);
                    this.pollData = null;
                }
            } catch (error) {
                console.error('❌ Error loading poll data:', error);
                
                // Handle specific error cases
                if (error.response?.status === 404) {
                    console.log('📭 No poll data found for this venue');
                    this.pollData = { polls: [], summary: { totalPolls: 0, totalResponses: 0, uniqueRespondents: 0 } };
                } else {
                    this.pollData = null;
                }
                this.pollsLoaded = true;
            }
        },
        
        processPollData(rawPollData) {
            if (!rawPollData || rawPollData.length === 0) {
                return { 
                    polls: [], 
                    summary: { 
                        totalPolls: 0, 
                        totalResponses: 0, 
                        uniqueRespondents: 0 
                    } 
                };
            }
            
            const uniqueRespondents = new Set();
            const processedPolls = rawPollData.map(poll => {
                // Count unique respondents across all polls
                poll.responses.forEach(response => {
                    if (response.respondentId) {
                        uniqueRespondents.add(response.respondentId);
                    }
                });
                
                // Process based on question type
                if (poll.questionType === 'multiple_choice_single_selection' || poll.questionType === 'multiple_choice_multi_selection') {
                    return this.processMultipleChoicePoll(poll);
                } else if (poll.questionType === 'rating' || poll.questionType === 'rating_scale') {
                    return this.processRatingPoll(poll);
                } else {
                    return poll; // Return as-is for other types
                }
            });
            
            return {
                polls: processedPolls,
                summary: {
                    totalPolls: rawPollData.length,
                    totalResponses: rawPollData.reduce((sum, poll) => sum + poll.totalResponses, 0),
                    uniqueRespondents: uniqueRespondents.size
                }
            };
        },
        
        processMultipleChoicePoll(poll) {
            const optionCounts = {};
            const totalResponses = poll.responses.length;
            
            // Initialize option counts
            poll.options.forEach(option => {
                optionCounts[option.id] = {
                    text: option.optionText,
                    count: 0,
                    percentage: 0
                };
            });
            
            // Count responses
            poll.responses.forEach(response => {
                if (response.selectedOptionIds && Array.isArray(response.selectedOptionIds)) {
                    response.selectedOptionIds.forEach(optionId => {
                        if (optionCounts[optionId]) {
                            optionCounts[optionId].count++;
                        }
                    });
                }
            });
            
            // Calculate percentages
            Object.values(optionCounts).forEach(option => {
                option.percentage = totalResponses > 0 ? Math.round((option.count / totalResponses) * 100) : 0;
            });
            
            return {
                ...poll,
                processedResults: {
                    type: 'multiple_choice',
                    optionCounts: optionCounts,
                    totalResponses: totalResponses
                }
            };
        },
        
        processRatingPoll(poll) {
            console.log('🔍 Processing rating poll:', poll.pollTitle, 'Type:', poll.questionType);
            console.log('🔍 Poll responses:', poll.responses);
            
            const ratings = [];
            let sum = 0;
            let validRatings = 0;
            
            poll.responses.forEach(response => {
                console.log('🔍 Processing response:', response.ratingValue, typeof response.ratingValue);
                if (response.ratingValue !== null && response.ratingValue !== undefined) {
                    ratings.push(response.ratingValue);
                    sum += response.ratingValue;
                    validRatings++;
                }
            });
            
            const average = validRatings > 0 ? (sum / validRatings).toFixed(1) : 0;
            
            // Count rating distribution (assuming 1-5 scale)
            const distribution = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
            ratings.forEach(rating => {
                if (Object.prototype.hasOwnProperty.call(distribution, rating)) {
                    distribution[rating]++;
                }
            });
            
            const result = {
                ...poll,
                processedResults: {
                    type: 'rating',
                    average: average,
                    totalRatings: validRatings,
                    distribution: distribution,
                    ratings: ratings
                }
            };
            
            console.log('🔍 Processed rating poll result:', result);
            return result;
        },
        
        getProgressBarColor(index) {
            const colors = ['primary', 'success', 'info', 'warning', 'danger', 'secondary'];
            return colors[index % colors.length];
        },
        
        formatDate(dateString) {
            if (!dateString) return 'N/A';
            
            try {
                const date = new Date(dateString);
                return date.toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric'
                });
            } catch (error) {
                console.error('Error formatting date:', error);
                return 'Invalid Date';
            }
        },
        
        getCurrentDate() {
            return new Date().toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        }
    },
    watch: {
        '$route.params.venueID': async function(newId, oldId) {
            if (newId !== oldId) {
                this.venueID = newId;
                this.dataLoaded = false;
                this.analyticsData = null;
                this.analyticsLoaded = false;
                
                await this.loadVenueData();
                this.checkAuthorization();
                
                if (this.isAuthorized) {
                    await this.loadAnalyticsData();
                }
                
                this.dataLoaded = true;
            }
        }
    }
}
</script>

<style scoped>
.mobile-pt-3 {
    padding-top: 1rem;
}

@media (min-width: 768px) {
    .mobile-pt-3 {
        padding-top: 3rem;
    }
}
</style>

<!-- Global print styles to ensure footer hiding works across components -->
<style>
/* Print Styles - Global to affect all components */
@media print {
    /* Hide everything by default */
    * {
        visibility: hidden;
    }
    
    /* Specifically hide common footer and navigation elements */
    footer,
    nav,
    .navbar,
    .footer,
    .nav,
    .navigation,
    [class*="footer"],
    [class*="nav"],
    [id*="footer"],
    [id*="nav"],
    .d-print-none {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Show only the report container and its children */
    .container, .container * {
        visibility: visible;
    }
    
    /* Position the report container to fill the page */
    .container {
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Ensure proper page breaks */
    .mb-5 {
        page-break-inside: avoid;
        margin-bottom: 1.5rem !important;
    }
    
    /* Optimize card layouts for print */
    .card {
        border: 1px solid #dee2e6 !important;
        box-shadow: none !important;
        margin-bottom: 1rem !important;
        page-break-inside: avoid;
    }
    
    /* Ensure proper text colors for print */
    .text-muted {
        color: #6c757d !important;
    }
    
    .text-primary {
        color: #0d6efd !important;
    }
    
    .text-success {
        color: #198754 !important;
    }
    
    .text-warning {
        color: #ffc107 !important;
    }
    
    .text-info {
        color: #0dcaf0 !important;
    }
    
    /* Optimize table layouts */
    .table {
        font-size: 0.85rem !important;
    }
    
    .table th,
    .table td {
        padding: 0.5rem !important;
        border: 1px solid #dee2e6 !important;
    }
    
    /* Optimize badge styles for print */
    .badge {
        border: 1px solid #dee2e6 !important;
        color: #000 !important;
        background-color: #f8f9fa !important;
    }
    
    /* Progress bars for print */
    .progress {
        background-color: #f8f9fa !important;
        border: 1px solid #dee2e6 !important;
    }
    
    .progress-bar {
        background-color: #6c757d !important;
    }
    
    /* Optimize image sizes */
    img {
        max-width: 60px !important;
        max-height: 60px !important;
    }
    
    /* Remove unnecessary spacing */
    .py-4, .py-5 {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Ensure headers are kept with content */
    h1, h2, h3, h4, h5, h6 {
        page-break-after: avoid;
        margin-bottom: 0.5rem !important;
    }
    
    /* Optimize row layouts */
    .row {
        margin: 0 !important;
    }
    
    .col-12, .col-md-3, .col-md-4, .col-md-6 {
        padding: 0.25rem !important;
    }
}
</style>