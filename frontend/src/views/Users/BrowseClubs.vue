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

        <!-- Display when data is loaded -->
        <!-- Main content -->
        <div v-if="dataLoaded" class="container-fluid mt-5 px-5 row">

            <!-- Search, create, clubs you manage and in-->
            <div class="col-12 col-md-3">
                <!-- Header -->
                <div>
                    <h3 class="text-start fw-bold">Find your drinking buddies!</h3>
                </div>

                <!-- Search Input -->
                <div>
                    <div class="input-group mb-3 position-relative">
                        <input type="text" class="form-control rounded-pill" placeholder="Search for clubs" aria-label="Search for clubs" aria-describedby="search-club" v-model="searchQuery">
                        <!-- Search Icon -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-search position-absolute" viewBox="0 0 16 16" style="right: 10px; top: 50%; transform: translateY(-50%); cursor: pointer; z-index: 5;"
                            @click="searchClubs">
                            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                        </svg>
                    </div>
                </div> 

                <!-- Create Club Button -->
                <div class="text-start">
                    <button class="btn btn-primary" @click="createClub">+ Create a Club</button>
                </div>

                <!-- Clubs you manage -->
                <div v-if="userClubs.length > 0 && adminClubs.length > 0" class="mt-3">
                    <h3 class="text-start fw-bold">Clubs You Manage</h3>

                    <div v-for="club in adminClubs" class="d-flex gap-3 mb-3" :key="club.id">

                        <!-- Club Banner Image -->
                        <div style="width: 100px; height: 150px;">
                            <img v-if="club.clubInfo.clubBanner" :src="club.clubInfo.clubBanner" class="img-fluid w-100 border" alt="..." style="object-fit: cover;">
                            <img v-else :src="defaultBanner" class="img-fluid w-100 border" alt="..." style="object-fit: cover;">
                        </div>
                        <!-- CLub title -->
                        <router-link :to="{ name: 'clubview', params: { clubID: club.clubID }}" class="text-dark hover-underline">
                            {{ club.clubInfo.clubName }}
                        </router-link>
                    </div>
                </div>

                <!-- Clubs you are in -->
                <div v-if="userClubs.length > 0 && memberClubs.length > 0" class="mt-3">
                    <h3 class="text-start fw-bold">Clubs You Are In</h3>

                    <div v-for="club in memberClubs" class="d-flex gap-3 mb-3" :key="club.id">

                        <!-- Club Banner Image -->
                        <div style="width: 100px; height: 150px;">
                            <img v-if="club.clubInfo.clubBanner" :src="club.clubInfo.clubBanner" class="img-fluid w-100 border" alt="..." style="object-fit: cover;">
                            <img v-else :src="defaultBanner" class="img-fluid w-100 border" alt="..." style="object-fit: cover;">
                        </div>
                        <!-- CLub title -->
                        <router-link :to="{ name: 'clubview', params: { clubID: club.clubID }}" class="text-dark hover-underline">
                            {{ club.clubInfo.clubName }}
                        </router-link>
                    </div>
                </div>
            </div>

            <!-- Recent activity [has joined club(s)] or browse club [not yet joined club]-->
            <div class="col-12 col-md-9">

                <!-- Display no results found if search term does not exist in any of the clubs -->
                <div v-if="searchResults" class="mt-3">
                    <h2>{{ searchResults }}</h2>
                </div>

                <!-- Recent activity [there is recent activity]-->
                <div v-if="latestPosts.length > 0" class="mt-3">

                    <!-- Recent Activity Header -->
                    <h3 class="text-start fw-bold">Recent Activity in Your Clubs</h3>

                    <!-- Bootstrap Horizontal Card for each recent activity -->
                    <div v-for="post in latestPosts" :key="post.id" class="card mb-3">
                        <div class="row g-0">

                            <!-- Recent Activity Information -->
                            <div class="col-md-10 ps-md-2">
                                <div class="card-body row h-100">

                                    <!-- Column 1: Poster photo -->
                                    <div class="col-1">
                                        <div class="d-flex flex-row align-items-center">
                                            <img :src="post.posterPhoto" class="rounded-circle" alt="..." style="height: 55px; width: 55px; object-fit: cover;">
                                        </div>
                                    </div>

                                    <!-- Column 2: Post information -->
                                    <div class="col-11">
                                        <!-- Club Name -->
                                        <h2 class="card-title fw-bold text-start">
                                            <router-link :to="{ name: 'clubview', params: { clubID: post.clubID }}" class="text-dark hover-underline">
                                                {{ post.clubName }}
                                            </router-link>  
                                        </h2>  

                                        <div class="text-start d-flex gap-3">
                                            <!-- Poster name -->
                                            <p>
                                                <router-link :to="profileURL(post.posterInfo.id, post.posterInfo.userType)">
                                                    <p v-if="post.posterInfo.userType == 'user'" class="name-container">{{ post.posterInfo.displayName }}</p>
                                                    <p v-else-if="post.posterInfo.userType == 'producer'" class="name-container">{{ post.posterInfo.producerName }}</p>
                                                    <p v-else class="name-container">{{ post.posterInfo.venueName }}</p>
                                                </router-link>
                                            </p>

                                            <!-- Post date -->
                                            <p class="card-text text-start">{{ post.postDate }}</p>
                                        </div>
                                        

                                        <!-- Post content -->
                                        <p class="card-text text-start">{{ post.postContent }}</p>

                                        <!-- View Post Button -->
                                        <button type="button" class="btn btn-primary align-self-start" @click="viewPost(post.id)">View Post</button>
                                    </div>
                                    
                                </div>
                            </div>
                        </div>  
                    </div>
                </div>

                <!--- Error message for error retrieving recent activity or no recent activtiy found -->
                <div v-if="latestPostsError" class="mt-3">
                    <h2>{{ latestPostsError }}</h2>
                    <hr>
                </div>
                
                <!-- browse club [not yet joined club]-->
                <div v-if="userClubs.length == 0" class="mt-3">
                    <p class="text-center fw-bold">You haven't joined a club yet!</p>
                    <p class="text-center fw-bold">Get on it! Here are some we'd like to recommend!</p>
                </div>

                <div v-else>
                    <h3 class="fw-bold text-start text-decoration-underline">Browse clubs here</h3>
                </div>

                <!-- Club Lists --> 
                <!-- Bootstrap Horizontal Card for each club -->
                <div class="row mt-3">
                    <div v-for="club in filteredClubs" :key="club.id" class="col-md-6 mb-3 justify-content-center border border-2 rounded-3 p-3">
                        <div class="row g-0">

                            <!-- Club Banner Image -->
                            <div class="col-md-2 text-start w-100" style="width: 400px; height: 150px;">
                                <img v-if="club.clubBanner" :src="club.clubBanner" 
                                    class="img-fluid border" 
                                    alt="..." 
                                    style="height: 150px; object-fit: contain;">
                                
                                <img v-else :src="defaultBanner" 
                                    class="img-fluid w-100 border" 
                                    alt="..." 
                                    style="height: 150px; object-fit: contain;">
                            </div>

                            <!-- Club Name-->
                            <h2 class="card-title fw-bold text-start">
                                <router-link :to="{ name: 'clubview', params: { clubID: club.id }}" class="text-dark hover-underline">
                                    {{ club.clubName }}
                                </router-link>
                            </h2>

                            <!-- Club type and number of members -->
                            <p class="text-start text-success">
                                <span v-if="club.isInviteOnly == false">Public Group | </span>
                                <span v-else>Private Group | </span>
                                <span>{{ club.totalMembers }} Members</span>
                            </p>

                            <!-- Club Description -->
                            <p class="card-text text-start">{{ club.clubDesc }}</p>

                            <!-- Join Club Button -->
                            <!-- <button v-if="userClubs.includes(club.id)" type="button" class="btn btn-primary mt-auto align-self-start" disabled>Joined</button> -->
                            <button v-if="requestedClubs.includes(club.id)" type="button" class="btn btn-primary mt-auto align-self-start w-md-25" disabled>Request Sent</button>
                            <button v-if="!userClubs.includes(club.id) && club.isInviteOnly == false" type="button" class="btn btn-primary mt-auto align-self-start w-md-25" @click="joinClub(club.id)">+Join This Club</button>
                            <button v-if="!userClubs.includes(club.id) && club.isInviteOnly == true && !requestedClubs.includes(club.id)" type="button" class="btn btn-primary mt-auto align-self-start w-md-25" @click="requestJoin(club.id)">Request to Join</button>
                        </div>
                    </div>
                </div>


                <!-- Load More Button -->
                <div v-if="showButton" class="d-flex justify-content-center mt-3">
                    <button type="button" class="btn secondary-btn btn-md" @click="loadMoreClubs">Load More</button>
                </div>    
                
                <!--Display no clubs yet message -->
                <div v-if="clubs.length == 0" class="mt-3">
                    <h2>No clubs yet!</h2>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// Import the necessary libraries
import NavBar from '@/components/NavBar.vue';
import { useToast } from 'vue-toastification';

export default {
    name: "BrowseClubs",
    components: {
        NavBar
    },
    data() {
        return {
            // Variable to store the user ID
            userID: null,
            userType: 'defaultUser',

            // Variables for page loading
            dataLoaded: false,

            // Variable for default Banner 
            defaultBanner: require("@/assets/defaultGroupBanner.png"),

            // Variables for lazy loading
            offset: 0,
            clubIndex: 1, 
            showButton: true,

            // Variables for page data
            clubs: [],

            // Variable for search bar
            searchQuery: "",

            // Variable for search results message
            searchResults: "",

            // Variable to store the list of clubs the user is a member of
            userClubs: [],

            // Variable to store clubs that the user is an admin of
            adminClubs: [],

            // Variable to store the list of clubs the user is a member of
            memberClubs: [],

            // Variable to store the list of clubs the user has requested to join (not yet joined)
            requestedClubs: [],

            // Variable to store the list of clubs the user has been invited to join but not yet accepted
            invitedClubs: [],

            // Variable to store recent activities
            latestPosts: [],

            // Variable to store error message
            latestPostsError: null,
        }
    },

    methods: {
        // Function to get 5 latest posts if the user is a member of at least one club
        async getLatestPosts() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getRecentActivity/${this.userID}/${this.userType}`);
                this.latestPosts = response.data.recent_activities;
            } catch (error) {
                if (error.response.status == 404) {
                    this.latestPostsError = "No recent activities found!";
                }
                else
                this.latestPostsError = "An error occurred while loading recent activities. Please try again later!";
                console.log(error);
            }
        },

        // Function to get all clubs information 
        async getClubs() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getClubs/` + this.offset);
                this.clubs = response.data.clubs_info;

                this.dataLoaded = true;
            // If status code is not 2xx, it will go to the catch block
            } catch (error) {
                console.log(error);
                // Check if status code is 404
                if (error.response.status == 404) {
                    this.dataLoaded = true;
                    
                }
                else {
                    this.dataLoaded = null;
                }   
            }
        },

        // Function to search clubs
        async searchClubs() {
            // Reset the club index
            this.clubIndex = 1;

            try {
                if (this.searchQuery == "") {
                    this.getClubs();
                } else {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getClubwSearch/` + this.clubIndex + "/" + this.searchQuery);
                    this.clubs = response.data.clubs_info;

                    if (response.status == 404) {
                        this.searchResults = "No results found for the search term!";
                    } else {
                        this.searchResults = "";
                    }
                }

            }
            catch (error) {
                console.log(error);
                this.dataLoaded = null;
            }
        },

        // Function to load more clubs
        async loadMoreClubs() {
            // increment the offset
            this.offset += 20;
            this.clubIndex += 20;

            let response;

            try {
                if (this.searchQuery != "") {
                    response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getClubwSearch/` + this.clubIndex + "/" + this.searchQuery);
                } else {
                    response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getClubs/` + this.clubIndex);
                }

                // If there are more clubs, append them to the existing clubs
                if (response.data.clubs_info.length > 0) {


                    this.clubs = this.clubs.concat(response.data.clubs_info);
                } else {
                    this.showButton = false;
                }

            // If status code is not 2xx, it will go to the catch block
            } catch (error) {
                console.log(error);
                this.showButton = false;
            }
        },

        // Function to direct user to create club page
        createClub() {

            // Check if the user is logged in
            if (this.userType == "defaultUser") {
                    // Redirect to login page
                    this.$router.push('/login');
                    return;
                }
            
            // Redirect to create club page
            this.$router.push("/club/create");
        },

        // Function to join a club
        async joinClub(clubId) {

            // Check if the user is logged in
            if (this.userType == "defaultUser") {
                // Redirect to login page
                this.$router.push('/login');
                return;
            }

            try {
                // Disable the button to prevent multiple clicks
                this.disableButton = true;

                // Join the club
                const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/club/joinClub`, {
                    userID: this.userID,
                    clubID: clubId,
                    userType: this.userType
                });

                if (response.status == 201) {
                    const toast = useToast();
                    toast.success("You have successfully joined the club!");
                    // Redirect to the club page
                    this.$router.push({ name: 'clubview', params: { clubID: clubId } });
                }

            } catch (error) {
                console.log(error);
                const toast = useToast();
                toast.error("An error occurred while joining the club. Please try again later!");
            }
        },

        // Function to request to join a club
        async requestJoin(clubId) {

            // Check if the user is logged in
            if (this.userType == "defaultUser") {
                // Redirect to login page
                this.$router.push('/login');
                return;
            }

            try {
                // Disable the button to prevent multiple clicks
                this.disableButton = true;

                // Request to join the club
                const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/club/requestToJoinClub`, {
                    userID: this.userID,
                    clubID: clubId,
                    userType: this.userType
                });

                if (response.status == 201) {
                    const toast = useToast();
                    toast.success("Your request to join the club has been sent successfully!");
                    // Redirect to the club page
                    this.$router.push({ name: 'clubview', params: { clubID: clubId } });
                }

            } catch (error) {
                console.log(error);
                const toast = useToast();
                toast.error("An error occurred while requesting to join the club. Please try again later!");
                
            }
        },

        // Function to retrieve a list of clubs the user is a member of (to show join or leave button)
        async getMemberClubs() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getUserClubs/${this.userID}/${this.userType}`);
                this.userClubs = response.data.user_clubs;
                this.adminClubs = response.data.user_club_admin;
                this.memberClubs = response.data.user_club_member;

                // Get the latest posts if the user is a member of at least one club
                if (this.userClubs.length > 0) {
                    this.getLatestPosts();
                }
            } catch (error) {
                console.log(error);
            }
        },

        // Function to retrieve a list of clubs the user has requested to join (not yet joined)
        async getRequestedClubs() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getUserClubRequests/${this.userID}/${this.userType}`);
                this.requestedClubs = response.data.club_request_list;
            } catch (error) {
                console.log(error);
            }
        },

        // Function to retrieve the list of clubs the user has been invited to join but not yet accepted
        async getInvitedClubs() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getUserInvitedClubs/${this.userID}/${this.userType}`);
                this.invitedClubs = response.data.club_invite_list;
            } catch (error) {
                console.log(error);
            }
        },  
        
        // Function to view a post
        viewPost(postID) {
            this.$router.push(`/club/${this.clubId}/post/${postID}`);
        },

        // Function to redirect to the profile page of the poster
        profileURL(posterID, userType) {
            if (userType == 'user') {
                return `/profile/user/${posterID}`;
            }
            else if (userType == 'producer') {
                return `/profile/producer/${posterID}`;
            }
            else {
                return `/profile/venue/${posterID}`;
            }
        },
    },

    computed: {
        // Function to filter clubs by excluding the clubs the user is already a member of
        filteredClubs() {
            return this.clubs.filter(club => !this.userClubs.includes(club.id));
        }
    },

    mounted() {
        // Get all clubs when the page is loaded
        this.getClubs();
        // Get the account id and type of the user
        this.userID = localStorage.getItem("88B_accID");
        let userType = localStorage.getItem("88B_accType");

        if (userType) {
            this.userType = userType;
        }

        if (this.userID && this.userType !== "defaultUser") {
            // Get the list of clubs the user is a member of
            this.getMemberClubs();
            // Get the list of clubs the user has requested to join
            this.getRequestedClubs();
        }
    }
}

</script>