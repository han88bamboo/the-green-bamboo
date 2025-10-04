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
                                                                <p class="text-muted mb-1">
                                                                    <strong>Section Order:</strong> {{ section.sectionOrder || 'N/A' }}
                                                                    <span v-if="section.isSubSection" class="badge bg-info ms-2">Subsection</span>
                                                                    <span v-else class="badge bg-primary ms-2">Main Section</span>
                                                                </p>
                                                                <p class="mb-0">
                                                                    <span class="badge bg-secondary me-2">{{ section.uniqueItemsTasted || 0 }} Items Tasted</span>
                                                                    <span class="text-muted">{{ section.penetrationRate || 0 }}% Taster Penetration</span>
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
                            <div class="alert alert-info">
                                <i class="fas fa-info-circle me-2"></i>
                                Poll results integration is coming soon. This section will display comprehensive poll analytics and attendee feedback.
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
        }
        
        this.dataLoaded = true;
    },
    methods: {
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