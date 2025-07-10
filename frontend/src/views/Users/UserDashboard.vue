<template>
    <div>
        <NavBar />

        <!-- Display when data is still loading -->
        <LoadingWithFunFact v-if="dataLoaded === false" />

        <!-- Display when data fails to load -->
        <ErrorDisplay v-if="dataLoaded === null" @go-back="this.$router.go(-1)" @go-home="this.$router.push('/')" />

        <!-- Main Content -->
        <div v-if="user && dataLoaded" class="user-dashboard-page">
            <div class="container text-start py-5">
                <div class="row">

                    <!-- Left Pane -->
                    <div class="col-lg-4 col-12">
                        <UserProfileHeader :user="displayUser" :stats="userStats"
                            :default-profile-photo="defaultProfilePhoto" />

                        <!-- Desktop-only Activity Feeds -->
                        <div class="d-none d-lg-block mt-4">
                            <ActivityFeed class="mb-3" title="Your Recent Activity" :activities="recentUserActivity"
                                :current-user-id="userID" />
                            <ActivityFeed class="mb-3" title="Recent Activity on Your Reviews"
                                :activities="recentReviewActivity" :current-user-id="userID" />
                            <ActivityFeed class="mb-3" title="Recent Activity from Your Followers"
                                :activities="recentFollowerActivity" :current-user-id="userID" />
                        </div>
                    </div>

                    <!-- Right Pane -->
                    <div class="col-lg-8 col-12 ps-lg-5 mt-4 mt-lg-0">
                        <LeaderboardSection :grails="grails" :up-and-coming="upAndComing" :goats="goats"
                            @open-popup="handleOpenPopup" />

                        <!-- debug code here -->
                        <!-- <div v-for="item in grails" :key="item.id" class="d-flex align-items-center mt-2">
                            {{ item.id + "•" + item.name + "•" + item.listingName + "•" +  item.bottler + "•" + item.originCountry}}
                        </div> -->

                        <!-- Mobile-only Tabbed Activity Feeds -->
                        <div class="d-lg-none mt-4">
                            <ul class="nav nav-pills nav-fill" role="tablist">
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link active" data-bs-toggle="pill"
                                        data-bs-target="#mobile-user-activity" type="button">My Activity</button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link" data-bs-toggle="pill"
                                        data-bs-target="#mobile-review-activity" type="button">My Reviews</button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link" data-bs-toggle="pill"
                                        data-bs-target="#mobile-follower-activity" type="button">Following</button>
                                </li>
                            </ul>
                            <div class="tab-content pt-3">
                                <div class="tab-pane fade show active" id="mobile-user-activity" role="tabpanel">
                                    <ActivityFeed title="Your Recent Activity" :activities="recentUserActivity"
                                        :current-user-id="userID" />
                                </div>
                                <div class="tab-pane fade" id="mobile-review-activity" role="tabpanel">
                                    <ActivityFeed title="Activity on Your Reviews" :activities="recentReviewActivity"
                                        :current-user-id="userID" />
                                </div>
                                <div class="tab-pane fade" id="mobile-follower-activity" role="tabpanel">
                                    <ActivityFeed title="Recent Activity from Your Followers"
                                        :activities="recentFollowerActivity" :current-user-id="userID" />
                                </div>
                            </div>
                        </div>

                        <!-- Analytics Section (Charts and Lists) -->
                        <div class="row mt-4">
                            <!-- This section can also be further componentized if it grows -->
                            <div class="col-12 col-lg-6 mb-4">
                                <div class="card p-3 h-100 d-flex flex-column">
                                    <h6 class="fw-bold mb-3">Review Count</h6>
                                    <div class="d-flex justify-content-center align-items-center mb-3">
                                        <div class="text-center fw-bold" style="color: #ffc107; font-size: 2.5rem;">
                                            {{ this.reviews.total_reviews || 0 }}
                                        </div>
                                    </div>
                                    <div class="chart-container flex-grow-1">
                                        <Bar :data="monthlyRatingCount" :options="chartOptions" />
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-6 mb-4">
                                <div class="card p-3 h-100">
                                    <h6 class="fw-bold">Spread of Ratings</h6>
                                    <div class="chart-container">
                                        <Bar :data="ratingsData" :options="chartOptions" />
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-6 mb-4">
                                <div class="card p-3 h-100">
                                    <h6 class="fw-bold">Best Rated Drinks</h6>
                                    <!-- This should be its own component: <TopItemsList :items="top5BestReviewedListings" /> -->
                                    <div v-for="item in top5BestReviewedListings" :key="item.id"
                                        class="d-flex align-items-center mb-2">
                                        <img :src="item.photo || defaultProfilePhoto"
                                            style="width: 50px; height: 50px; object-fit: contain;" class="me-3">
                                        <div>
                                            <div class="fw-bold">{{ item.listingName }}</div>
                                            <small class="text-muted">Your Rating: {{ item.rating }} ★</small>
                                        </div>
                                    </div>
                                    <!-- Error message if top brands is empty-->
                                    <div v-if="top5BestReviewedListings.length === 0"
                                        class="text-center text-muted mt-3">
                                        Review listings to show results.
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-6 mb-4">
                                <div class="card p-3 h-100">
                                    <h6 class="fw-bold">Most Reviewed Categories</h6>
                                    <div v-for="(item, index) in top5MostReviewedCategories" :key="item.drinkType"
                                        class="d-flex align-items-center mb-2">
                                        <div class="rank-circle me-3">{{ index + 1 }}</div>
                                        <div>
                                            <div class="fw-bold">{{ item.drinkType }}</div>
                                            <small class="text-muted">{{ item.reviewCount }} reviews</small>
                                        </div>
                                    </div>
                                    <!-- Error message if top brands is empty-->
                                    <div v-if="top5MostReviewedCategories.length === 0"
                                        class="text-center text-muted mt-3">
                                        Review listings to show results.
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-6 mb-4">
                                <div class="card p-3 h-100">
                                    <h6 class="fw-bold">Your Top Venues</h6>
                                    <div v-for="(venue, index) in top5Venues" :key="venue.name"
                                        class="d-flex align-items-center mb-2">
                                        <div class="rank-circle me-3">{{ index + 1 }}</div>
                                        <div>
                                            <div class="fw-bold">{{ venue.venueName }}</div>
                                            <!-- <small class="text-muted">{{ item.reviewCount }} reviews</small> -->
                                        </div>
                                    </div>
                                    <!-- Error message if top brands is empty-->
                                    <div v-if="top5Venues.length === 0" class="text-center text-muted mt-3">
                                        No favourite spots.
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-6 mb-4">
                                <div class="card p-3 h-100">
                                    <h6 class="fw-bold">Your Top Brands</h6>
                                    <div v-for="(item, index) in top5Producers" :key="item.producerName"
                                        class="d-flex align-items-center mb-2">
                                        <div class="rank-circle me-3">{{ index + 1 }}</div>
                                        <div>
                                            <div class="fw-bold">{{ item.producerName }}</div>
                                            <!-- <small class="text-muted">{{ item.reviewCount }} reviews</small> -->
                                        </div>
                                    </div>
                                    <!-- Error message if top brands is empty-->
                                    <div v-if="top5Producers.length === 0" class="text-center text-muted mt-3">
                                        No favourate brands.
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-6 mb-4">
                                <div class="card p-3 h-100">
                                    <h6 class="fw-bold">Your Top Styles</h6>
                                    <div v-for="(item, index) in top5Styles" :key="item.drinkStyle"
                                        class="d-flex align-items-center mb-2">
                                        <div class="rank-circle me-3">{{ index + 1 }}</div>
                                        <div>
                                            <div class="fw-bold">{{ item.drinkStyle }}</div>
                                            <!-- <small class="text-muted">{{ item.reviewCount }} reviews</small> -->
                                        </div>
                                    </div>
                                    <!-- Error message if top drink style is empty-->
                                    <div v-if="top5Styles.length === 0" class="text-center text-muted mt-3">
                                        Review listings to show results.
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <FooterBar />
        </div>

        <!-- The Modal is controlled by this parent component -->
        <LeaderboardEditModal v-if="showPopup" :category="popupCategory"
            :initial-selection="getInitialSelection(popupCategory)" @close="closePopup"
            @confirm="handleConfirmSelection" />
    </div>
</template>

<script>
// --- IMPORTS ---
import NavBar from '@/components/NavBar.vue';
import FooterBar from '@/components/FooterBar.vue';
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';
import ErrorDisplay from '@/components/user_dashboard/ErrorDisplay.vue';
import UserProfileHeader from '@/components/user_dashboard/UserProfileHeader.vue';
import ActivityFeed from '@/components/user_dashboard/ActivityFeed.vue';
import LeaderboardSection from '@/components/user_dashboard/LeaderboardSection.vue';
import LeaderboardEditModal from '@/components/user_dashboard/LeaderboardEditModal.vue';

import { useToast } from "vue-toastification";
import { Bar } from 'vue-chartjs'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js'

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
)

export default {
    name: 'UserDashboard',
    components: {
        NavBar,
        FooterBar,
        LoadingWithFunFact,
        ErrorDisplay,
        UserProfileHeader,
        ActivityFeed,
        LeaderboardSection,
        LeaderboardEditModal,
        Bar,
    },
    data() {
        return {
            // --- Core State ---
            dataLoaded: false,
            userID: null,
            userType: null,
            displayUserID: null,
            ownProfile: false,

            // --- User Data ---
            user: null, // The logged-in user object
            displayUser: {}, // The user object for the profile being viewed

            // --- Dashboard Data ---
            drinkCount: 0,
            followerCount: 0,
            totalBadges: 0, // Assuming this comes from an API
            top5BestReviewedListings: [],
            top5MostReviewedCategories: [],
            top5Venues: [],
            top5Producers: [],
            top5Styles: [],

            // --- Activity Feeds Data ---
            recentUserActivity: [],
            recentReviewActivity: [],
            recentFollowerActivity: [],

            // --- Leaderboard Data ---
            grails: [],
            upAndComing: [],
            goats: [],

            // --- Modal State ---
            showPopup: false,
            popupCategory: '',

            // --- Charting --- initialized to 0 
            reviews: {
                total_reviews: 0,
                monthly_distribution: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                rating_distribution: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            },

            // chart option setup
            chartOptions: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: true,
                        callbacks: {
                            label: function (context) {
                                return `${context.parsed.y} review${context.parsed.y !== 1 ? 's' : ''}`
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        display: false, // Hide Y-axis
                        max: 12 // Set a reasonable max for better visual proportion
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#6c757d',
                            font: {
                                size: 12
                            }
                        }
                    }
                },
                layout: {
                    padding: {
                        top: 5,
                        bottom: 5
                    }
                }
            },

            // --- Misc ---
            defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
        };
    },
    computed: {
        userStats() {
            return {
                drinkCount: this.drinkCount,
                followerCount: this.followerCount,
                totalBadges: this.totalBadges,
            };
        },
        monthlyRatingCount() {
            return {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    data: this.reviews.monthly_distribution,
                    backgroundColor: [
                        '#e9ecef', // Light gray for empty bars
                        '#ffc107',
                        '#ffc107',
                        '#ffc107',
                        '#ffc107',
                        '#ffc107',
                        '#ffc107',
                        '#ffc107',
                        '#ffc107',
                        '#ffc107',
                    ],
                    borderColor: [
                        '#ffb300',
                        '#ffb300',
                        '#ffb300',
                        '#ffb300',
                        '#ffb300',
                        '#ffb300',
                        '#ffb300',
                        '#ffb300',
                        '#ffb300',
                        '#ffb300'
                    ],
                    borderWidth: 1,
                    borderRadius: 4,
                    barThickness: 20
                }]
            }
        },
        ratingsData() {
            return {
                labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                datasets: [{
                    data: this.reviews.rating_distribution,
                    backgroundColor: [
                        '#e9ecef', // Light gray for empty bars
                        '#ffc107',
                        '#ffc107',
                        '#ffc107',
                        '#ffc107',
                        '#ffc107',
                        '#ffc107',
                        '#ffc107',
                        '#ffc107',
                        '#ffc107',
                    ],
                    borderColor: [
                        '#ffb300',
                        '#ffb300',
                        '#ffb300',
                        '#ffb300',
                        '#ffb300',
                        '#ffb300',
                        '#ffb300',
                        '#ffb300',
                        '#ffb300',
                        '#ffb300'
                    ],
                    borderWidth: 1,
                    borderRadius: 4,
                    barThickness: 20
                }]
            }
        }

    },
    async mounted() {
        this.userID = localStorage.getItem('88B_accID');
        this.userType = localStorage.getItem('88B_accType');

        if (!this.userID) {
            this.$router.push('/login');
            return;
        }

        this.displayUserID = this.$route.params.userID;
        this.ownProfile = this.displayUserID === this.userID;

        await this.loadData();
    },
    methods: {
        // --- DATA FETCHING ---
        async loadData() {
            this.dataLoaded = false;
            try {
                // Fetch all data in parallel for better performance
                await Promise.all([
                    this.fetchDisplayUserDetails(),
                    this.fetchDisplayUserDashboardData(),
                    this.fetchDisplayUserRecentFollowerActivity(),
                    this.fetchDisplayUserRecentReviewActivity(),
                    this.fetchDisplayUserRecentActivity(),
                    this.fetchRawReviewsForCharts(),
                ]);
                this.dataLoaded = true;
            } catch (error) {
                console.error("Failed to load dashboard data:", error);
                this.dataLoaded = null; // Trigger error display
            }
        },
        async fetchDisplayUserDetails() {
            if (!this.ownProfile) {
                return
            }

            const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUser/${this.displayUserID}`);
            this.displayUser = response.data;
            this.user = this.displayUser;

            const api_endpoint = `${process.env.VUE_APP_API_URL}/getData/lbListings?id=${encodeURIComponent(this.displayUserID)}`
            const api_response = await fetch(api_endpoint)
            if (api_response.status === 404) {
                // Expected behavior for no results
                this.grails = []
                this.upAndComing = []
                this.goats = []
            }
            if (!api_response.ok) {
                throw new Error(`HTTP ${api_response.status}: ${api_response.statusText}`)
            }
            const data = await api_response.json();
            const merged_listings = [...data["grails"], ...data["upAndComing"], ...data["goats"]];

            // fetch full listing call it once instead of multiple calls
            const detailed_list = await this.fetchFullListingDetails(merged_listings || []);

            // build quick selection 
            const selection = {
                grails: data["grails"],
                upAndComing: data["upAndComing"],
                goats: data["goats"],
            };

            // Create a quick lookup map for detailedData
            const detailMap = Object.fromEntries(detailed_list.map(item => [item.id, item]));
            // Replace IDs in each list with the full detail
            const updatedSelection = {
                goats: selection.goats.map(id => detailMap[id]),
                grails: selection.grails.map(id => detailMap[id]),
                upAndComing: selection.upAndComing.map(id => detailMap[id])
            };

            // // now we will sort all data back to each categories
            this.grails = updatedSelection["grails"]
            this.upAndComing = updatedSelection["upAndComing"]
            this.goats = updatedSelection["goats"]

            // console.log("---------------------")
            // console.log(data)
            // console.log(merged_listings)
            // console.log(detailed_list)
            // console.log(updatedSelection)
            // console.log("---------------------")
        },
        async fetchDisplayUserDashboardData() {
            const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUserDashBoardData/${this.displayUserID}`);
            const responseData = response.data.data;
            this.followerCount = responseData.totalFollowers;
            this.drinkCount = responseData.totalReviews;
            this.top5BestReviewedListings = responseData.top5BestReviewedListings;
            this.top5MostReviewedCategories = responseData.top5MostReviewedCategories;
            this.top5Venues = responseData.top5Venues;
            this.top5Producers = responseData.top5Producers;
            this.top5Styles = responseData.top5DrinkStyles;
        },
        async fetchDisplayUserRecentFollowerActivity() {
            const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getRecentFollowersActivity/${this.displayUserID}`);
            this.recentFollowerActivity = response.data;
        },
        async fetchDisplayUserRecentReviewActivity() {
            const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getRecentReviewsActivity/${this.displayUserID}`);
            this.recentReviewActivity = response.data;
        },
        async fetchDisplayUserRecentActivity() {
            const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getRecentUserActivity/${this.displayUserID}`);
            this.recentUserActivity = response.data;
        },
        async fetchRawReviewsForCharts() {
            const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getReviews/${this.displayUserID}`);
            this.reviews = response.data;
            // console.log("---------------------------")
            // console.log(this.reviews)
            // console.log("---------------------------")
        },

        // --- LEADERBOARD & MODAL HANDLERS ---
        getInitialSelection(category) {
            if (category === 'Grail') return this.grails;
            if (category === 'Up & Coming') return this.upAndComing;
            if (category === 'GOATs') return this.goats;
            return [];
        },
        handleOpenPopup(category) {
            this.popupCategory = category;
            this.showPopup = true;
        },
        closePopup() {
            this.showPopup = false;
        },
        async handleConfirmSelection({ category, drinks }) {
            const safeDrinksCopy = JSON.parse(JSON.stringify(drinks));

            // Transform the drinks data to match the expected format
            const transformedDrinks = safeDrinksCopy.map(drink => ({
                id: drink.id,
                name: drink.listingName || drink.name, // Handle both new and existing items
                bottler: drink.bottler,
                image: drink.image || drink.photo,  // Handle both image and photo properties
                originCountry: drink.originCountry
            }));

            // Update the appropriate category
            if (category === 'Grail') {
                this.grails = transformedDrinks;
            } else if (category === 'Up & Coming') {
                this.upAndComing = transformedDrinks;
            } else if (category === 'GOATs') {
                this.goats = transformedDrinks;
            }

            try {
                await this.saveSelectionsToDatabase();
                this.closePopup();
            } catch (error) {
                console.error("Error saving selections:", error);
                // Don't close popup if save fails - let user try again
            }
        },
        async saveSelectionsToDatabase() {
            const toast = useToast();
            try {
                // Check if user has any selections
                const hasSelections = this.grails.length > 0 ||
                    this.upAndComing.length > 0 ||
                    this.goats.length > 0;

                // this probably will never happen because we disabled 
                // confirm button when theres no selection
                if (!hasSelections) {
                    toast.warning("Please make at least one selection before saving.");
                    return;
                }

                // We only need to send the IDs to the backend
                const payload = {
                    userID: this.userID,
                    grails: this.grails.map(d => d.id),
                    upAndComing: this.upAndComing.map(d => d.id),
                    goats: this.goats.map(d => d.id),
                };

                // Make API call and check response
                const response = await this.$axios.post(
                    `${process.env.VUE_APP_API_URL}/editDashboard/addLeaderBoard`,
                    payload
                );

                // Check response status and data
                if (response.status === 201) {
                    toast.success("Dashboard updated successfully!");
                } else {
                    // Handle unexpected success status
                    toast.warning(`Changes saved but with unexpected status: ${response.status}.`);
                }
                // toast.success("Dashboard updated successfully!");
            } catch (error) {
                console.error("Error updating dashboard:", error);
                toast.error("An error occurred while updating dashboard.");
            }
        },
        async fetchFullListingDetails(listingIDs) {
            if (!listingIDs || listingIDs.length === 0) return [];
            try {
                // Assuming you have an endpoint that can take multiple IDs
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingsByIDs`, {
                    params: new URLSearchParams(listingIDs.map(id => ['ids', id]))
                });
                // Map the response to the format expected by the leaderboard columns
                return response.data.map(d => ({
                    id: d.id,
                    name: d.listingName,
                    drinkType: d.drinkType,
                    bottler: d.bottler,
                    originCountry: d.originCountry,
                    image: d.photo
                }));
            } catch (error) {
                console.error(`Error fetching details for listings:`, error);
                return [];
            }
        },

        // --- UTILITY METHODS ---
        formatDateMonthYear(dateTimeString) {
            const date = new Date(dateTimeString);
            const month = date.toLocaleString('default', { month: 'short' });
            const year = date.getFullYear();
            return `${month}/${year}`;
        },
    },

};
</script>

<style scoped>
.user-dashboard-page {
    margin-bottom: 2rem;
}

.nav-pills .nav-link {
    background-color: #f0f0f0;
    color: #333;
    margin-right: 0.5rem;
}

.nav-pills .nav-link.active {
    background-color: #027562;
    /* Your primary color */
    color: white;
}

.rank-circle {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: #f0b358;
    color: white;
    font-weight: bold;
    flex-shrink: 0;
}

.chart-container {
    height: 250px;
    /* Fixed height */
    position: relative;
    flex: 1;
    /* Take remaining space in the card */
}
</style>