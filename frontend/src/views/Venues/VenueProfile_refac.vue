<!--
Normal User (Anonymous & Logged-In)

   * Information Viewing:
       * View the venue's main profile information (name, photo, country, type, description, contact details, social links).
       * Toggle between three main content tabs: Venue Overview, Menu, and Venue Reviews.
       * Venue Overview Tab:
           * View the latest updates posted by the venue owner.
           * View sorted lists of the venue's drinks: "Most Popular," "Most Discussed," and "Recently Added."
       * Menu Tab:
           * Browse the full menu, organized into sections.
           * Search for specific items within the menu.
           * Sort the menu by different criteria.
           * Click on any menu item to navigate to its detailed listing page.
       * Q&A Section:
           * View questions and answers about the venue.
   * User Actions (Logged-In Users Only):
       * Follow or unfollow the venue.
       * Submit a review for the venue.
       * "Like" or "unlike" a venue's updates.
       * Ask a new question in the Q&A section.
   * User Actions (All Users):
       * If a venue is unclaimed, users can click a "Claim This Business" button.
       * Clicking "Review Venue" while logged out redirects to the login page.

  Venue Owner (`isOwner`) - previously selfview 

  Includes all "Normal User" functionalities, plus the following exclusive actions:

   * Profile Management:
       * Edit the main venue profile, including:
           * Profile photo (upload, revert, remove).
           * Venue name, country, type, and description.
           * Contact information (year opened, website, email, phone numbers).
           * Social media links (Instagram, Facebook, TikTok).
           * Reservation availability status.
   * Welcome Dashboard:
       * A dedicated section with quick links to manage their presence:
           * Curate Your Menu
           * Post An Announcement
           * Create An Event
           * Answer Q&A’s
           * Create A Club
           * Claim a free associated Brand Account.
   * Content Management:
       * Updates: Create, edit, and delete venue updates (announcements).
       * Q&A: Answer questions from users, and edit or delete their own answers.
   * Menu Management:
       * Enter a full "Edit Menu" mode.
       * Add, edit, and delete entire menu sections.
       * Add, edit, and delete individual items on the menu.
       * Drag-and-drop to re-order menu sections.
       * Generate a QR code and a shareable link for their menu.

  Admin previously (`powerView`) now isAdmin

  Admins appear to have moderator privileges over a venue's profile. Their capabilities are a subset of the venue owner's:

   * Edit the venue's profile information (shared with the owner).
   * Edit and delete a venue's updates (shared with the owner).

  Misc. & UI Functionalities

   * Loading & Error States:
       * Displays a loading animation while fetching data.
       * Shows a clear error message if the venue does not exist or if data fails to load, with options to go back or return to
         the home page.
   * User Experience:
       * The interface is responsive and adapts to mobile screen sizes.
       * Content sections like "Updates" and "Q&A" are collapsible to save space.
       * Long descriptions are truncated with a "Read More" option.
       * Uses modals for complex actions like sharing the menu or submitting reports.
       * Features client-side search and sorting for the menu.
   * Technical Note:
       * The component uses direct DOM manipulation (e.g., document.getElementById, scrollIntoView) for scrolling to sections,
         which is generally considered an anti-pattern in Vue.js. Using Vue refs would be a more idiomatic approach.
-->

<template>

    <NavBar />

    <!-- Main Content -->
    <div class="container pt-5 pb-5">

        <!-- Display when venue does not exist -->
        <!-- <div v-if="!venueExists && dataLoaded" class="text-danger fst-italic fw-bold fs-3">
            <span>An error occurred while loading this page, please try again!</span>
            <br>
            <span class="text-danger-emphasis fw-normal">Are you sure that this venue exists?</span>
        </div> -->

        <!-- Main layout when data is loaded -->
        <div class="row">

            <!-- Main Content Column -->
            <div class="col-xl-9 col-12">
                <!-- Welcome banner for venue owners -->
                <VenueWelcome v-if="isOwner" @navigate-to-section="scrollToSection" />

                <!-- Venue Header -->
                <VenueHeader :isLoading="isLoadingVenue"
                    :venue="targetVenue" :isFollowing="isFollowing"
                    :isOwner="isOwner" :isAdmin="isAdmin"
                    :is-editing="editProfile" @toggle-edit="editProfile = !editProfile" 
                    @save-profile="saveProfileEdits" @photo-updated="handlePhotoUpdate" 
                    @follow-clicked="handleFollowClick"
                    @review-clicked="openModal('review')"    
                />

                <!-- Content Tabs -->
                <VenueContentTabs :active-tab="contentMode" @update:activeTab="contentMode = $event" />
                <hr class="mt-0">

                <!-- Tab Content -->
                <div class="tab-content">
                    <!-- Overview Tab -->
                    <div v-show="contentMode === 'overview'" id="overview-section">
                        <VenueOverviewTab :updates="targetVenue.updates" :venue-name="targetVenue.venueName"
                            :isOwner="isOwner" :overview="overview"
                            :user-info="userInfo" 
                            @submit-update="handleUpdateSubmit"    
                        />
                    </div>

                    <!-- Menu Tab -->
                    <div v-show="contentMode === 'menu'" id="menu-section">
                        <VenueMenuTab :venue_menu="venue_menu" :is-self-view="isOwner"
                            :venue_id="targetVenue.id"
                            :claim-status="targetVenue.claimStatus" @save-menu="handleMenuSave"        
                        />
                    </div>

                    <!-- Reviews Tab -->
                    <div v-show="contentMode === 'venueReviews'">
                        <VenueReviewsTab :venue-reviews="filteredVenueReviews" :bottle-reviews="bottleReviews"
                            :user-id="user_id" :can-mod="isAdmin" />
                    </div>

                    <!-- Activities Tab -->
                    <div v-show="contentMode === 'recentActivities'">
                        <VenueActivityTab :venue-reviews="filteredVenueReviews" :bottle-reviews="bottleReviews"
                            :user-id="user_id" :can-mod="isAdmin" />
                    </div>
                </div>
            </div>

            <!-- Sidebar Column -->
            <div class="col-xl-3 col-12" id="qna-section">
                <ProfileSidebar :loading="isLoadingVenue" :error="dataLoadingError" :venue="targetVenue" 
                    :is-self-view="isOwner" :answered-questions="answeredQuestions"
                    :unanswered-questions="unansweredQuestions" :opening-hours="openingHours" />
            </div>
        </div>
    </div>

    <!-- review modal goes here -->
    <VenueReviewModal 
      :user_id="viewerID"
      :venueId="targetVenue.id"
      :filteredVenueReviews="filteredVenueReviews"
    />

    <VenueQRModal 
      :pageURL="pageURL"
    /> 
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import VenueWelcome from '@/components/venue_profile/VenueWelcome.vue';
import VenueHeader from '@/components/venue_profile/VenueHeader.vue';
import VenueContentTabs from '@/components/venue_profile/VenueContentTabs.vue';
import VenueOverviewTab from '@/components/venue_profile/VenueOverviewTab.vue';
import VenueMenuTab from '@/components/venue_profile/VenueMenuTab.vue';
import VenueReviewsTab from '@/components/venue_profile/VenueReviewsTab.vue';
import VenueActivityTab from '@/components/venue_profile/VenueActivityTab.vue';
import ProfileSidebar from '@/components/elements/ProfileSidebar.vue';

import VenueReviewModal from '@/components/venue_profile/VenueReviewModal.vue';
import VenueQRModal from '@/components/venue_profile/VenueQRModal.vue';

import { computed } from 'vue'
import { useRoute } from 'vue-router'

// Constants and utilities
const DAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
const DEFAULT_MAP_COORDS = { lat: 25, lng: -71 };
const BERMUDA_TRIANGLE_ADDRESS = "(The Bermuda Triangle)";

// Data processing utilities
const processUtils = {
    sortObjectByKeys(obj, keyOrder) {
        return Object.fromEntries(
            keyOrder
                .filter(key => key in obj)
                .map(key => [key, obj[key]])
        );
    },

    sortByProperty(array, property, direction = 'asc') {
        return array.sort((a, b) => {
            const comparison = a[property] > b[property] ? 1 : -1;
            return direction === 'desc' ? -comparison : comparison;
        });
    },

    formatDateForDisplay(dateString) {
        return dateString.split('T')[0].split('-').reverse().join('/');
    },

    isValidResponse(response) {
        return response?.data &&
            response.data !== "" &&
            !(Array.isArray(response.data) && response.data.length === 0);
    }
};

// API service methods
const apiService = {
    async fetchWithRetry(axiosInstance, url, options = {}, retries = 3) {
        for (let i = 0; i < retries; i++) {
            try {
                const response = await axiosInstance.get(url, options);
                return response;
            } catch (error) {
                if (i === retries - 1) throw error;
                await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, i)));
            }
        }
    },

    async batchRequest(axiosInstance, requests) {
        try {
            return await Promise.allSettled(requests.map(req =>
                axiosInstance.get(req.url, req.options)
            ));
        } catch (error) {
            console.error('Batch request failed:', error);
            return [];
        }
    }
};

export default {
    name: 'VenueProfilePage',
    components: {
        NavBar,
        VenueWelcome,
        VenueHeader,
        VenueContentTabs,
        VenueOverviewTab,
        VenueMenuTab,
        VenueReviewsTab,
        VenueActivityTab,
        ProfileSidebar,
        VenueReviewModal,
        VenueQRModal,
    },
    setup() {
        const route = useRoute()
        const pageURL = computed(() => `${process.env.VUE_APP_BASE_URL}${route.fullPath}`)
        
        return { pageURL }
    }, 
    data() {
        return {
            // Caching and performance
            loadedListings: new Map(), // Use Map for O(1) lookups
            loadedProducers: new Map(),
            processingQueue: new Set(), // Prevent duplicate requests

            // Loading states
            isLoadingVenue: false,
            isLoadingMenu: false,
            dataLoadingError: null,

            viewerID: localStorage.getItem('88B_accID'),
            viewerType: localStorage.getItem('88B_accType'),
        
            venueExists: true,
            dataLoaded: true,
            isOwner: false, // Set to true to show the welcome banner for demonstration
            isAdmin: false,
            editProfile: false,
            contentMode: 'menu', // Default tab
            targetVenue: {
                updates: [],
                venueName: 'Unknown',
                claimStatus: false,
                photo: '',
                id: null, // Ensure venue ID is available for checks
                address: '',
                loc: {
                    long: 0,
                    lat: 0,
                },
                amenities: {}
            },

            userInfo: {},
            filteredVenueReviews: [],
            bottleReviews: [],
            user_id: '',
            // viewerID: null,
            // viewerType: '',
            isFollowing: false,
            answeredQuestions: [],
            unansweredQuestions: [],
            openingHours: {},

            venue_menu: {
                loading: false, 
                error: null, 
                menu: []
            },

            overview: {
                loading: false, // most popular loading state
                error: null, // most popular error 
                mostPopular: [], // most popular list 
                mostDiscussed: [], // most discussed list 
                recentlyAdded: [] // recently added list
            },

            // Properties to hold data from the child component
            updateText: '',
            updatePhoto: null,
        };
    },
    mounted() {
        // Load viewer's info from localStorage to determine access rights
        // this.viewerID = localStorage.getItem('userID');
        // this.viewerType = localStorage.getItem('userType');
        // this.isAdmin = localStorage.getItem('power') === 'true';

        // check if user has the prviledge to run owner rights
        this.isOwner = this.checkOwnerPriviledge();
        
        // console.log('-------------------------------')
        // console.log(this.isOwner)
        // console.log('-------------------------------')

        // set basic information to get fetch venue information and checks 
        this.handleVenueRoute()

        // Fetch venue data and then check permissions
        // this.getVenueData();
        this.loadData();
    },
    methods: {
        handleUpdateSubmit(updateData) {
            // Store the received data
            this.updateText = updateData.text;
            this.updatePhoto = updateData.photo;

            // Log to console for verification
            // console.log('Received update text:', this.updateText);
            // console.log('Received update photo (base64):', this.updatePhoto);
            // alert('Update received! Check the console for the data.');

            // --- Placeholder for backend submission ---
            const payload = {
                venueID: this.targetVenue.id,
                date: new Date().toISOString(), // backend expects this exact format
                text: this.updateText,
                image64: this.updatePhoto
            };

            this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/addUpdates`, payload)
                .then(() => {
                    this.getVenueData();
                })
                .catch(error => {
                    console.error('Error posting update:', error);
                });
            
        },
        // Logic to determine if the current viewer is the owner of the venue profile
        checkOwnerPriviledge() {
            const isVenueOwner =
                this.viewerType === 'venue' && this.viewerID === this.targetVenue;

            // Power users have owner privileges for claimed venues
            const isPowerUserWithClaim =
                this.isAdmin && Boolean(this.targetVenue.claimStatus);
            // console.log('viewerType : ', this.viewerType)
            // console.log('viewerID : ', this.viewerID)
            // console.log('targetVenue', this.targetVenue)
            // console.log('veunue owner : ', isVenueOwner)
            // console.log('power user : ', isPowerUserWithClaim)
            return isVenueOwner || isPowerUserWithClaim;
        },

        handleVenueRoute() {
            const { venueID, username } = this.$route.params;
            const hasVenueID = Boolean(venueID);

            if (hasVenueID) {
                this.targetVenue = venueID;
                this.targetVenueID = venueID;
                this.userName = username || this.userName;
            }
            else if (this.viewerType === 'venue') {
                // Show logged-in venue's profile
                this.targetVenue = this.viewerID;
                this.targetVenueID = this.viewerID;
                this.userName = this.userName || ''; // Ensure it's not undefined
                this.pageURL = `${this.pageURL}/${this.targetVenue}/${this.userName}`;
            }
            else {
                // Redirect non-venue users without venueID
                this.$router.push('/login');
                return; // Stop further execution
            }

            // Run a single, unified ownership check
            this.isOwner = this.checkOwnerPriviledge();
        },

        // Separated venue fetching for better error handling and testability `${process.env.VUE_APP_API_URL}/getData/getVenue/${this.targetVenueID}`
        async fetchVenueDetails() {
            const response = await apiService.fetchWithRetry(
                this.$axios,
                `${process.env.VUE_APP_API_URL}/getData/venue/${this.targetVenueID}`
            );

            if (!processUtils.isValidResponse(response)) {
                return null;
            }

            return response.data;
        },

        async loadData() {
            try {
                await Promise.all([
                    this.getVenueData(),
                    this.getMenu(),
                    this.getOverview(), 
                    this.getReviews()
                ]);

            } catch (error) {
                console.error(error)
            } 
        },

        async getMenu() {
            this.venue_menu.loading = true
            this.venue_menu.menu = [];

            try {
                const response = await apiService.fetchWithRetry(
                    this.$axios,
                    `${process.env.VUE_APP_API_URL}/menu/${this.targetVenueID}`
                );

                // Transform the menu to nest subsections (one-liner approach)
                this.venue_menu.menu = response.data
                    .filter(item => !item.isSubSection)
                    .map(section => ({
                        ...section,
                        subSections: response.data
                            .filter(item => item.isSubSection && item.parentSectionId === section.id)
                            .map(({id, sectionName, sectionOrder}) => ({id, sectionName, sectionOrder}))
                    }));
                
                // console.log(this.venue_menu);

            } catch (error) {
                // show error to user
                this.venue_menu.error = error;
            } finally {
                this.venue_menu.loading = false;
            }
        },

        async getOverview() {
            this.overview.loading = true;
            this.overview.error = null; // Clear previous errors

            try {
                const response = await apiService.fetchWithRetry(
                    this.$axios,
                    `${process.env.VUE_APP_API_URL}/menu/${this.targetVenueID}/overview`
                );

                // Update only the data properties
                this.overview.mostPopular = response.data.most_popular;
                this.overview.mostDiscussed = response.data.most_discussed;
                this.overview.recentlyAdded = response.data.most_recent;

                console.log("-----------------------------------------")
                console.log(this.overview)
            } catch (error) {
                this.overview.error = error;
            } finally {
                this.overview.loading = false;
            }
        },

        async getReviews() {
            return 
        },

        // Main venue data fetching method - optimized for SSR
        async getVenueData() {
            if (this.isLoadingVenue) return;

            this.isLoadingVenue = true;
            this.dataLoadingError = null;

            try {
                const venueData = await this.fetchVenueDetails();
                // console.log(venueData);
                if (!venueData) {
                    this.venueExists = false;
                    return;
                }

                // Process venue data in parallel where possible
                await Promise.all([
                    this.processVenueBasicData(venueData),
                    this.processVenueQuestionsAnswers(venueData),
                    this.processVenueHours(venueData),
                    // this.processVenueMenu(venueData),
                    // this.processVenueUpdates(venueData),
                    this.processMapData(venueData.address),
                    this.processClaimStatus(venueData)
                ]);
                // console.log(this.menuSections)

                this.venueExists = true;
                // await this.loadMenuData(); 
            } catch (error) {
                console.error('Error fetching venue data:', error);
                this.dataLoadingError = error.message;
                this.dataLoaded = null;
            } finally {
                this.isLoadingVenue = false;
            }
        },

        // Process basic venue data
        processVenueBasicData(venueData) {
            this.targetVenue = venueData;

            // Batch assign editable data
            const editableFields = {
                editProfilePhoto: venueData.photo,
                targetVenueOriginalPhoto: venueData.photo,
                editVenueName: venueData.venueName,
                editVenueType: venueData.venueType,
                editVenueDesc: venueData.venueDesc,
                editCountry: venueData.originLocation,
                editYearOpened: venueData.yearOpened,
                editOpenForReservations: venueData.openForReservations,
                editWebsite: venueData.website,
                editInstagram: venueData.instagram,
                editFacebook: venueData.facebook,
                editTiktok: venueData.tiktok,
                editEmail: venueData.email,
                editPhoneNumber: venueData.phoneNumber,
                editWhatsappNumber: venueData.whatsappNumber,
                newAddress: venueData.address,
                newPublicHolidays: venueData.publicHolidays,
                newReservationDetails: venueData.reservationDetails
            };

            Object.assign(this, editableFields);
        },

        // Process Q&A data
        processVenueQuestionsAnswers(venueData) {
            const qaData = venueData.questionsAnswers || [];

            this.answeredQuestions = [];
            this.unansweredQuestions = [];

            qaData.forEach(qa => {
                const targetArray = qa.answer ? this.answeredQuestions : this.unansweredQuestions;
                targetArray.push(qa);
            });
        },

        // Process opening hours
        processVenueHours(venueData) {
            const rawHours = venueData.openingHours || {};
            this.openingHours = processUtils.sortObjectByKeys(rawHours, DAY_ORDER);
            this.newOpeningHours = JSON.parse(JSON.stringify(this.openingHours));
        },

        // Process menu data
        processVenueMenu(venueData) {
            // const menu = venueData.menu || [];

            // Sort sections and items
            this.menuSections = venueData.menu || [];
            //  processUtils.sortByProperty(menu, 'sectionOrder');
            // this.menuSections.forEach(section => {
            //     section.sectionMenu = processUtils.sortByProperty(section.sectionMenu, 'itemOrder');
            // });
        },

        // Process updates
        processVenueUpdates(venueData) {
            const updates = venueData.updates || [];

            if (updates.length > 0) {
                const sortedUpdates = processUtils.sortByProperty(updates, 'date', 'desc');
                this.targetVenue.updates = sortedUpdates.map(update => ({
                    ...update,
                    date: processUtils.formatDateForDisplay(update.date)
                }));
            }
        },

        // Process map data with better error handling
        async processMapData(address) {

            if (!address || typeof window === 'undefined') {
                // SSR or no address - use defaults
                this.setDefaultMapLocation();
                return;
            }

            try {
                const response = await this.$axios.get('https://maps.googleapis.com/maps/api/geocode/json', {
                    params: {
                        address,
                        key: process.env.VUE_APP_GOOGLE_MAPS_API_KEY
                    }
                });

                if (response.data.status === "OK") {
                    const { lat, lng } = response.data.results[0].geometry.location;
                    this.setMapLocation(lat, lng);
                } else {
                    this.setDefaultMapLocation();
                }

            } catch (error) {
                console.error(error)
                // console.error("Error getting maps data:", error);
                this.setDefaultMapLocation();
            }
        },

        setMapLocation(lat, lng) {
            // this.mapLat = lat;
            // this.mapLong = lng;
            // this.targetVenue.loc.lat = lat
            // this.targetVenue.loc.long = lng
            // this.mapMarkers = [{ position: { lat, lng } }];
            if (!this.targetVenue.loc) {
                this.targetVenue.loc = { lat: 0, long: 0 };
            }
            this.targetVenue.loc.lat = lat;
            this.targetVenue.loc.long = lng;
            // this.mapMarkers = [{ position: { lat, lng } }];
        },

        setDefaultMapLocation() {
            this.setMapLocation(DEFAULT_MAP_COORDS.lat, DEFAULT_MAP_COORDS.lng);
            if (this.targetVenue) {
                this.targetVenue.address = BERMUDA_TRIANGLE_ADDRESS;
            }
        },

        // claim status processing
        async processClaimStatus(venueData) {
            if (!venueData.stripeCustomerId) return;

            const shouldCheckStatus = this.shouldCheckClaimStatus(venueData.claimStatusCheckDate);
            if (!shouldCheckStatus) return;

            try {
                const claimStatus = await this.checkActiveSubscription(venueData.stripeCustomerId);
                await this.updateClaimStatusIfNeeded(venueData, claimStatus);
                await this.updateClaimStatusCheckDate(venueData.id);
            } catch (error) {
                console.error('Error processing claim status:', error);
            }
        },

        shouldCheckClaimStatus(lastCheckDate) {
            if (!lastCheckDate) return true;
            const today = new Date().toISOString().split('T')[0];
            const checkDate = lastCheckDate.split('T')[0];
            return checkDate < today;
        },

        async checkActiveSubscription(customerId) {
            try {
                const response = await this.$axios.post(
                    `${process.env.VUE_APP_API_URL}/payment/retrieve-latest-subscription`,
                    { customerId },
                    { headers: { 'Content-Type': 'application/json' } }
                );

                return response.data?.status === "active";
            } catch (error) {
                if (error.response?.status !== 404) {
                    console.error('Error retrieving subscription:', error);
                }
                return false;
            }
        },

        async updateClaimStatusIfNeeded(venueData, newClaimStatus) {
            if (venueData.claimStatus === newClaimStatus) return;

            venueData.claimStatus = newClaimStatus;

            await this.$axios.post(
                `${process.env.VUE_APP_API_URL}/editVenueProfile/updateVenueClaimStatus`,
                { businessId: venueData.id, claimStatus: newClaimStatus },
                { headers: { 'Content-Type': 'application/json' } }
            );
        },

        async updateClaimStatusCheckDate(businessId) {
            await this.$axios.post(
                `${process.env.VUE_APP_API_URL}/editVenueProfile/updateVenueClaimStatusCheckDate`,
                { businessId, claimStatusCheckDate: new Date().toISOString() },
                { headers: { 'Content-Type': 'application/json' } }
            );
        },

        async loadMenuData() {
            if (this.isLoadingMenu) return;
            this.isLoadingMenu = true;

            try {
                const itemsToProcess = this.collectMenuItems();

                if (itemsToProcess.length === 0) {
                    this.isLoadingMenu = false;
                    return;
                }

                // Process items in batches to avoid overwhelming the server
                const batchSize = 10;
                const batches = this.createBatches(itemsToProcess, batchSize);

                for (const batch of batches) {
                    await this.processBatch(batch);
                }
            } catch (error) {
                console.error('Error loading menu data:', error);
            } finally {
                this.isLoadingMenu = false;
            }
        },

        collectMenuItems() {
            const items = [];

            for (const section of this.detailedMenu) {
                for (const item of section.sectionMenu) {
                    items.push({ section, item });
                }
            }

            return items;
        },

        createBatches(items, batchSize) {
            const batches = [];
            for (let i = 0; i < items.length; i += batchSize) {
                batches.push(items.slice(i, i + batchSize));
            }
            return batches;
        },

        async processBatch(batch) {
            const promises = batch.map(({ section, item }) =>
                this.processMenuItem(section, item)
            );

            await Promise.allSettled(promises);
        },

        async processMenuItem(section, item) {
            const itemId = item.itemID;

            // Check if already processing this item
            if (this.processingQueue.has(itemId)) return;
            this.processingQueue.add(itemId);

            try {
                // Check cache first
                let listingData = this.loadedListings.get(itemId);

                if (!listingData) {
                    listingData = await this.fetchListingData(itemId);

                    if (!listingData) {
                        this.removeItemFromSection(section, itemId);
                        return;
                    }

                    // Cache the result
                    this.loadedListings.set(itemId, listingData);
                }

                await this.enrichItemData(section, item, listingData);

            } catch (error) {
                console.error(`Error processing menu item ${itemId}:`, error);
                this.removeItemFromSection(section, itemId);
            } finally {
                this.processingQueue.delete(itemId);
            }
        },

        async fetchListingData(itemId) {
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getListing/${itemId}`
                );

                if (!processUtils.isValidResponse(response)) {
                    return null;
                }

                return response.data;
            } catch (error) {
                console.error(`Error fetching listing ${itemId}:`, error);
                return null;
            }
        },

        async enrichItemData(section, item, listingData) {
            try {
                // Fetch additional data in parallel
                const [reviewData, producerData] = await Promise.all([
                    this.fetchReviewData(item.itemID),
                    this.fetchProducerData(listingData.producerID)
                ]);

                if (!producerData) {
                    this.removeItemFromSection(section, item.itemID);
                    return;
                }

                // Enrich listing data
                Object.assign(listingData, {
                    avgRating: reviewData.averageRating,
                    reviewCount: reviewData.reviewCount,
                    producerName: producerData.producerName
                });

                // Update cache
                this.loadedListings.set(item.itemID, listingData);

                // Set item details
                this.setItemDetails(item, listingData);

            } catch (error) {
                console.error('Error enriching item data:', error);
                this.removeItemFromSection(section, item.itemID);
            }
        },

        async fetchReviewData(itemId) {
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getListingReviewsRating/${itemId}`
                );
                return response.data;
            } catch (error) {
                console.error(`Error fetching reviews for ${itemId}:`, error);
                return { averageRating: 0, reviewCount: 0 };
            }
        },

        async fetchProducerData(producerId) {
            // Check cache first
            let producerData = this.loadedProducers.get(producerId);

            if (producerData) {
                return producerData;
            }

            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getProducer/${producerId}`
                );

                if (!processUtils.isValidResponse(response)) {
                    return null;
                }

                producerData = response.data;
                this.loadedProducers.set(producerId, producerData);

                return producerData;
            } catch (error) {
                console.error(`Error fetching producer ${producerId}:`, error);
                return null;
            }
        },

        setItemDetails(item, listingData) {
            const servingType = this.servingTypes?.find(s => s.id === item.itemServingType);

            item.itemDetails = {
                itemPhoto: listingData.photo,
                itemName: listingData.listingName,
                itemType: listingData.drinkType,
                itemTypeCategory: listingData.typeCategory,
                itemABV: listingData.abv,
                itemCountry: listingData.originCountry,
                itemDesc: listingData.officialDesc,
                itemRating: listingData.avgRating,
                itemProducer: listingData.producerName,
                itemProducerID: listingData.producerID,
                itemServingTypeName: servingType?.servingType || "(Unknown)"
            };
        },

        removeItemFromSection(section, itemId) {
            section.sectionMenu = section.sectionMenu.filter(i => i.itemID !== itemId);
        },

        // SSR-friendly method to check if we're in browser
        isBrowser() {
            return typeof window !== 'undefined';
        },

        scrollToSection(sectionId) {
            let targetElementId = '';
            let tab = this.contentMode;

            switch (sectionId) {
                case 'menu':
                    targetElementId = 'menu-section';
                    tab = 'menu';
                    break;
                case 'updates':
                    targetElementId = 'overview-section';
                    tab = 'overview';
                    break;
                case 'qna':
                    targetElementId = 'qna-section';
                    // No tab change needed for Q&A as it's in the sidebar
                    break;
            }

            this.contentMode = tab;

            this.$nextTick(() => {
                const element = document.getElementById(targetElementId);
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth', block: 'start' });

                    // Adjust for fixed navbar height
                    const navbarHeight = 80; // Adjust this value based on your actual navbar height
                    const elementPosition = element.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - navbarHeight;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });

                    // Highlight effect
                    element.style.transition = 'background-color 0.5s ease-in-out';
                    element.style.backgroundColor = '#fff3cd'; // A light, noticeable color
                    setTimeout(() => {
                        element.style.backgroundColor = 'transparent';
                    }, 2500);
                }
            });
        },

        async saveProfileEdits(consolidatedData) {
            // console.log('Original consolidatedData:', consolidatedData);
            try {
                this.isSaving = true;
                this.imageUploadLoading = true;

                const formData = new FormData();
                // Better iteration and debugging
                Object.entries(consolidatedData).forEach(([key, value]) => {
                    if (value !== null && value !== undefined && value !== '') {
                        const apiFieldName = key === 'country' ? 'originLocation' : key;
                        formData.append(apiFieldName, value);
                    }
                });

                // Properly log FormData contents
                // for (let [key, value] of formData.entries()) {
                //     console.log(`${key}: ${value}`);
                // }

                const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/venueInfo`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    timeout: 30000, // 30 second timeout
                });

                if (response.data && response.data.success) {
                    this.targetVenue = { ...this.targetVenue, ...response.data.targetVenue };
                    this.editProfile = false;
                    // Show success message
                    alert('Profile updated successfully!');
                } else {
                    const errorMessage = response.data?.message || 'Failed to update profile.';
                    alert(errorMessage);
                }
            } catch (error) {
                console.error('Save profile error:', error);
                alert('An error occurred while saving the profile.');
            } finally {
                this.isSaving = false;
                this.imageUploadLoading = false;
            }
        },
        handlePhotoUpdate(newPhoto) {
            // Placeholder for handling photo updates
            this.targetVenue.photo = newPhoto;
        },

        async handleMenuSave(updatedMenu) {
            console.log('Saving menu changes from VenueProfile_refac:', updatedMenu);
            try {
                const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/menu/`, {
                    venueID: this.targetVenue.id, // Use the venue ID from VenueProfile_refac
                    updatedMenu: updatedMenu 
                });
                if (response.data.code === 200) {
                    console.log("Menu changes saved successfully via VenueProfile_refac!");
                    // Optionally, re-fetch menu data or update local state
                    this.getMenu(); // Re-fetch all venue data to update menu
                    this.contentMode = 'menu'; // Stay on menu tab
                } else {
                    console.error("Failed to save menu changes via VenueProfile_refac:", response.data.message);
                }
            } catch (error) {
                console.error("Error saving menu changes via VenueProfile_refac:", error);
            }
        },

        cleanup() {
            this.processingQueue.clear();
            this.loadedListings.clear();
            this.loadedProducers.clear();
        },

        openShareModal() {
            if (this.shareModalInstance) {
                this.shareModalInstance.show();
            }
        },

        copyPageURL() {
            this.copyToClipboard(this.pageURL);
        },

        async handleFollowClick() {
            // based on click we swap between true and false
            this.isFollowing = !this.isFollowing
            try {
                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editProfile/updateFollowLists`,
                    {
                        userID: this.viewerID,
                        action: this.userFollowing? 'follow' : 'unfollow', // use tenary operation
                        target: "venues",
                        followerID: this.targetVenue['id'],
                    }, { headers: { 'Content-Type': 'application/json'}});
            }
            catch (error) {
                if (this.isFollowing) {
                    this.isFollowing = false; 
                } else {
                    this.isFollowing = true;
                }
                // Reload page, but why ? 
                // this.$router.go(0);
                console.error(error)
            }
        },

        // Copy to Clipboard
        copyToClipboard(text) {
            // if (process.server) return; // Skip on server-side for nuxt js 

            navigator.clipboard.writeText(text)
                .then(() => {
                    this.clipboardCopied = true;
                    setTimeout(() => {
                        this.clipboardCopied = false;
                    }, 2000);
                })
                .catch(err => {
                    console.error('Failed to copy text: ', err);
                });
        },
        
    },
    // Lifecycle hooks
    beforeUnmount() {
        this.cleanup();
    },
}
</script>

<style scoped></style>
