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
                        <h1 class="mb-4">Event Report - {{ venueName }}</h1>
                        <p class="text-muted">Comprehensive analytics and insights for your event</p>
                        
                        <!-- Placeholder for future content -->
                        <div class="alert alert-info">
                            <h5>Coming Soon!</h5>
                            <p class="mb-0">Event analytics and reporting features will be implemented here.</p>
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
        }
    },
    watch: {
        '$route.params.venueID': function(newId, oldId) {
            if (newId !== oldId) {
                this.venueID = newId;
                this.dataLoaded = false;
                this.loadVenueData().then(() => {
                    this.checkAuthorization();
                    this.dataLoaded = true;
                });
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