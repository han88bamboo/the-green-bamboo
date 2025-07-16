<!-- Admin can access this page to handle admin controls. -->
<template>
  <NavBar />

  <div class="container pt-3">

    <!-- Main Content -->
    <div v-if="!loadError">
      <h1 class="fw-bold fs-1 m-0">Admin Dashboard</h1>
      
      <div>
        <DateRangePicker @date-range-selected="handleRangeUpdate" 
            :initial-start-date="selectedDates.startDate"
            :initial-end-date="selectedDates.endDate"
        />

        <!-- <div class="mt-4 p-3 bg-light border rounded">
            <h5>Selected Date Range:</h5>
            <p v-if="selectedDates.startDate && selectedDates.endDate">
                <strong>Start:</strong> {{ formatFinalDate(selectedDates.startDate) }} <br/>
                <strong>End:</strong> {{ formatFinalDate(selectedDates.endDate) }}
            </p>
            <p v-else>
                No date range selected.
            </p>
        </div> -->

        <InfographicDashboard :signup_data="signup_data"
            :review_data="review_data" 
            :business_data="business_data" 
            :event_data="event_data"
        />
      </div>

      <!-- Navigation Tabs -->
      <nav>
        <div class="nav nav-tabs justify-content-center" id="nav-tab" role="tablist">
          <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#nav-tag">Tag Controls</button>
          <button class="nav-link" data-bs-toggle="tab" data-bs-target="#nav-moderator">Moderators</button>
          <button class="nav-link" data-bs-toggle="tab" data-bs-target="#nav-business">Business Accounts</button>
          <button class="nav-link" data-bs-toggle="tab" data-bs-target="#nav-proofpoints">Proof Points</button>
        </div>
      </nav>

        <!-- Loading and Error States (managed here) -->
        <!-- <div v-if="isLoading">Loading...</div>
        <div v-if="loadError" class="text-danger">
        An error occurred while loading data.
        <button @click="fetchData">Refresh</button>
        </div> -->

      <!-- Tab Content -->
      <div class="tab-content" id="nav-tabContent">
        <div class="tab-pane fade show active" id="nav-tag">
          <!-- Pass data down as props, listen for events up -->
          <TagManagement 
            :observation-tags="observationTags" 
            :flavour-tags="combinedFlavourTags"
            @update-tags="handleDataUpdate" 
          />
        </div>
        <div class="tab-pane fade" id="nav-moderator">
          <ModeratorManagement 
            :users="users" 
            :moderators="moderators" 
            :requests="pendingModRequests"
            :drink-types="drinkTypes"
            @update-moderators="handleDataUpdate"
          />
        </div>
        <div class="tab-pane fade" id="nav-business">
          <BusinessManagement 
            :countries="countries"
            :requests="businessAccountRequests"
            :producers="producers"
            :venues="venues"
            @update-businesses="handleDataUpdate"
          />
        </div>
        <div class="tab-pane fade" id="nav-proofpoints">
          <ProofPointsDashboard :userType="'admin'" />
        </div>
      </div>
    </div>
  </div>
</template>


<!-- AdminDashboard.vue -->
<script>
import axios from 'axios';

// Import child components
import NavBar from '@/components/NavBar.vue';
import DateRangePicker from '@/components/DateRangePicker.vue';
import InfographicDashboard from '@/components/admin_dashboard/InfographicDashboard.vue';
import TagManagement from '@/components/admin_dashboard/TagManagement.vue';
import ModeratorManagement from '@/components/admin_dashboard/ModeratorManagement.vue';
import BusinessManagement from '@/components/admin_dashboard/BusinessManagement.vue';
import ProofPointsDashboard from '@/components/ProofPointsDashboard.vue';

export default {
    name: 'AdminDashboard',
    props: {
    },
    components: {
        NavBar,
        DateRangePicker,
        InfographicDashboard,
        TagManagement,
        ModeratorManagement,
        BusinessManagement,
        ProofPointsDashboard,
    },
    data() {
        const strDate = new Date(new Date().toISOString());
        const endDate = new Date(new Date().toISOString());
        strDate.setDate(strDate.getDate() - 90);

        return {
            API_URL: process.env.VUE_APP_API_URL,
            
            // --- STATE MANAGEMENT ---
            // High-level state for the entire dashboard
            isLoading: true,
            loadError: false,
            user: null,

            // for data range picker component
            selectedDates: {
                // Example of setting an initial date range
                startDate: strDate, // April 2, 2024
                endDate: endDate, // July 15, 2025
            },

            signup_data: {
                loading: true, 
                error: '',
                total_signups: 0,
                users: [],
                // producers: [],
                // venues: [], 
                qualified_user: 0
            },

            review_data: {
                loading: true, 
                error: '',
                listing_review: 0,
                producer_review: 0,
                venue_review: 0, 
                total_listings: 0, 
                total_clubs: 0,
                lr_counts: [],  // listing reviews cummulative count
                pr_counts: [],  // producer reviews cummulative count
                vr_counts: [],  // venue reviews cummulative count 
            },

            event_data: {
                loading: true, 
                error: '',
                'active_events_count': 0,
                'all_events_count': 0
            },

            business_data: {
                loading: true, 
                error: '',
                total_signups: 0,
                producers: [],
                venues: [], 
            }, 
            
            // Raw data from the database, managed by the parent component
            observationTags: [],
            flavourTags: [],
            subTags: [],
            modRequests: [],
            businessAccountRequests: [],
            users: [],
            producers: [],
            venues: [],
            countries: [],
            drinkTypes: [],
        };
    },
    computed: {        
        pendingModRequests() {
            return this.modRequests.filter(request => request.reviewStatus);
        },

        moderators() {
            return this.users.filter(u => u.modType && u.modType.length > 0);
        },

        // Combine flavourTags and subTags into a more useful structure for the child component
        combinedFlavourTags() {
            if (this.flavourTags.length === 0 || this.subTags.length === 0) {
                return this.flavourTags;
            }
            return this.flavourTags.map(family => {
                const relatedSubTags = this.subTags
                    .filter(sub => sub.familyTagId === family.id)
                    .map(sub => ({ id: sub.id, subTag: sub.subTag }));
                return { ...family, showBox: false, subTag2: relatedSubTags };
            });
        }
    },
    async mounted() {
        const userID = localStorage.getItem('88B_accID');
        if (!userID) {
            this.$router.push('/login');
            return;
        }

        try {
            // 1. Authenticate and authorize the user first
            const response = await axios.get(`${this.API_URL}/getData/getUser/${userID}`);
            this.user = response.data;
            if (!this.user.isAdmin) {
                this.$router.push('/');
                return;
            }

            // 2. If authorized, load all dashboard data
            await this.loadStasData();
            await this.loadData();

        } catch (error) {
            console.error("Authentication or data loading failed:", error);
            // this.loadError = true;
            // this.isLoading = false;
        }
    },
    methods: {
        async loadStasData() {            
            try {
                const responses = await Promise.all([
                    this.retrieveStats(`${this.API_URL}/getData/getSignupStats`, this.signup_data, this.selectedDates),
                    this.retrieveStats(`${this.API_URL}/getData/getReviewStats`, this.review_data, this.selectedDates),
                    this.retrieveStats(`${this.API_URL}/getData/getClaimStats`, this.business_data, this.selectedDates),
                    this.retrieveStats(`${this.API_URL}/getData/getFutureEventsCount`, this.event_data, this.selectedDates),
                ]);

                // Assign data from responses
                this.signup_data = responses[0];
                this.review_data = responses[1];
                this.business_data = responses[2];
                this.event_data = responses[3];
            } catch (error) {
                console.error("Failed to load dashboard data:", error);
            }
        },

        async loadData() {
            this.isLoading = true;
            this.loadError = false;
            
            try {
                const responses = await Promise.all([
                    axios.get(`${this.API_URL}/getData/getObservationTags`),
                    axios.get(`${this.API_URL}/getData/getFlavourTags`),
                    axios.get(`${this.API_URL}/getData/getSubTags`),
                    axios.get(`${this.API_URL}/getData/getModRequests`),
                    axios.get(`${this.API_URL}/getData/getAccountRequests`),
                    axios.get(`${this.API_URL}/getData/getUsers`),
                    axios.get(`${this.API_URL}/getData/getProducers`),
                    axios.get(`${this.API_URL}/getData/getVenues`),
                    axios.get(`${this.API_URL}/getData/getCountries`),
                    axios.get(`${this.API_URL}/getData/getDrinkTypes`),
                ]);

                // Assign data from responses
                this.observationTags = responses[0].data;
                this.flavourTags = responses[1].data;
                this.subTags = responses[2].data;
                this.modRequests = responses[3].data;
                this.businessAccountRequests = responses[4].data;
                this.users = responses[5].data;
                this.producers = responses[6].data;
                this.venues = responses[7].data;
                this.countries = responses[8].data;
                this.drinkTypes = responses[9].data;

            } catch (error) {
                console.error("Failed to load dashboard data:", error);
                this.loadError = true;
            } finally {
                this.isLoading = false;
            }
        },
        async retrieveStats(url, api_data, dateRange) {
            api_data.loading = true
            api_data.error = ''
            
            try {
                const response = await axios.get(url, { params: dateRange });
                api_data = response.data;
            } catch (error) {
                //console.error("Failed to load recent activity:", error);
                api_data.error = "Failed to load recent activity. Please try again later.";
                
                // Specific error handling
                if (!navigator.onLine) {
                    api_data.error = "No internet connection. Please check your connection and try again.";
                } else if (error.response) {
                    // Server responded but with error status
                    if (error.response.status === 404) {
                        api_data.error = "Activity data not found.";
                    } else if (error.response.status >= 500) {
                        api_data.error = "Server error. Please try again later.";
                    }
                } else if (error.code === "ECONNABORTED") {
                    api_data.error = "Request timed out. Please try again.";
                } else if (error.message.includes("Network Error") || error.message.includes("ERR_CONNECTION_REFUSED")) {
                    api_data.error = "Unable to connect to the server.";
                }
            } finally {
                api_data.loading = false;
            }

            return api_data
        },

        /**
         * This function is triggered by child components when they
         * make a change, ensuring the entire dashboard has fresh data.
         */
        handleDataUpdate() {
            console.log('Child component requested a data refresh.');
            this.loadData(); // Pass false to prevent the loading screen
        },

        fetchData() {
            this.loadStasData();
            this.loadData();
        }, 

        handleRangeUpdate(range) {
            console.log('New range selected:', range);
            this.selectedDates.startDate = range.startDate;
            this.selectedDates.endDate = range.endDate;
            this.loadStasData();
        }, 

        // A helper method for consistent date formatting
        formatFinalDate(date) {
        if (!date) return '';
        return date.toLocaleDateString('en-GB', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        }); // e.g., "15/05/2025"
        }        
    }
};
</script>