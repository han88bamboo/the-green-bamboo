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
        <div class="event-club-banner mobile-view-show">
            <img src="@/assets/defaultGroupBanner.png" alt="Banner" />
            </div>
        <!-- Main content -->
        <div v-if="dataLoaded" class="container mobile-mt-3 mobile-px-4 mt-5 px-5">
            <div class="row">
                <!-- Search, create, clubs you manage and in-->
                <div class="col-12 col-md-4">
                    <!-- Header -->
                    <div>
                        <h5 class="text-start fw-bold">Find your drinking buddies!</h5>
                    </div>

                    <!-- Search Input -->
                    <div>
                        <div class="input-group mb-3 position-relative">
                            <input type="text" class="form-control rounded-pill" style="border: solid 2px #827c75" placeholder="Search for clubs" aria-label="Search for clubs" aria-describedby="search-club" v-model="searchQuery" @keyup.enter="searchClubs">
                            <!-- Search Icon -->
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-search position-absolute" viewBox="0 0 16 16" style="right: 10px; top: 50%; transform: translateY(-50%); cursor: pointer; z-index: 5;"
                                @click="searchClubs">
                                <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                            </svg>
                        </div>
                    </div> 

                    <div class="d-flex flex-wrap gap-2 pb-3">
                        <!-- Create Club Button -->
                        <button
                        class="btn primary-btn-less-round-blue btn-lg mobile-rating-smaller-text-2 fw-bold"
                        @click="canCreateClub ? createClub() : showClubLimitError = true"
                        >+ Create Club</button>
                        <!-- View My Clubs Toggle Button -->
                        <button 
                        class="btn primary-btn-less-round-blue d-md-none mobile-rating-smaller-text-2" 
                        style="font-weight: bold;"
                        type="button" 
                        data-bs-toggle="collapse" 
                        data-bs-target="#sidebarContent" 
                        aria-expanded="false" 
                        aria-controls="sidebarContent"
                        >
                        View My Clubs! &#8595;
                        </button>
                    </div>

                    <!-- Message for why user cannot create club -->
                    <div v-if="userType != 'defaultUser' && !canCreateClub && showClubLimitError" class="alert alert-danger mt-3" role="alert">
                        <p class="text-danger">{{ cannotCreateClubMsg }}</p>
                    </div>
                    
                    <!-- Club Invite-->
                    <div v-if="invitedClubs.length > 0" class="collapse d-md-block my-4" id="sidebarContent">
                        <h5 class="text-start fw-bold my-3 collapse d-md-block">Clubs You Are Invited To</h5>

                        <div v-for="club in invitedClubs.slice(0, 5)" class="event-club-box" :key="club.id">

                            <div class="row w-100 align-items-start mb-3">
                                <!-- First row (club info) -->
                                <div class="col-12 col-lg-7 mb-2 mb-md-0 text-start">
                                    <!-- Club title -->
                                    <router-link
                                        v-if="club.clubID && club.clubName"
                                        :to="{ name: 'clubview', params: { clubID: club.clubID, clubName: slugify(club.clubName || 'unknown-club') }}"
                                        class="text-dark hover-underline fw-bold d-block"
                                    >
                                        {{ club.clubName }}
                                    </router-link>

                                    <!-- Invited by -->
                                    <p class="mb-0">Invited by: {{ club.inviterInfo.displayName }}</p>
                                </div>

                                <!-- Second row (buttons) -->
                                <div class="col-12 col-lg-5 d-flex justify-content-start justify-content-lg-end">
                                    <!-- Decline Button -->
                                    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="red"
                                        class="bi bi-x-circle me-3" viewBox="0 0 16 16"
                                        style="cursor: pointer;" @click="declineInvite(club.clubID)">
                                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                                    </svg>

                                    <!-- Accept Button -->
                                    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="green"
                                        class="bi bi-check-circle" viewBox="0 0 16 16"
                                        style="cursor: pointer;" @click="acceptInvite(club.clubID)">
                                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                                        <path d="m10.97 4.97-.02.022-3.473 4.425-2.093-2.094a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05"/>
                                    </svg>
                                </div>

                                <hr class="w-100 mt-3">
                            </div>
                        </div>
                    </div>

                    <!-- Clubs you manage -->
                    <div v-if="userClubs.length > 0 && adminClubs.length > 0" class="collapse d-md-block my-4" id="sidebarContent">
                        <h5 class="text-start fw-bold my-3 collapse d-md-block">Clubs You Manage <button v-if="adminClubs.length > 5" type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#showAllManagedClubs">View All</button></h5>

                        <div v-for="club in adminClubs.slice(0, 5)" class="event-club-box" :key="club.id">

                            <!-- Club Banner Image -->
                            <div style="flex: 0 0 40%; max-width: 40%; height: 100px;">
                                <img v-if="club.clubInfo.clubBanner" :src="club.clubInfo.clubBanner" class="img-fluid event-banner;" alt="..." style="object-fit: cover;">
                                <img v-else :src="defaultBanner" class="img-fluid event-banner;" alt="..." style="object-fit: cover;">
                            </div>
                            <!-- Club title -->
                                <div class="container text-start ">
                                <router-link v-if="club.clubID && club.clubInfo?.clubName" :to="{ name: 'clubview', params: { clubID: club.clubID, clubName: slugify(club.clubInfo?.clubName || 'unknown-club') }}" class="fw-bold text-black hover-underline">
                                    {{ club.clubInfo?.clubName }}
                                </router-link>
                                <!-- Club details -->
                                <p class="text-success text-start small">
                                        <span v-if="club.isInviteOnly == false">Public Group | </span>
                                        <span v-else>Private Group | </span>
                                        <span>{{ club.totalMembers }} Members</span>
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Clubs you managed modal -->
                    <div class="modal fade" id="showAllManagedClubs" tabindex="-1" aria-labelledby="showAllManagedClubsLabel" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-scrollable modal-xl">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="showAllManagedClubsLabel">Clubs You Manage</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <div class="row">
                                        <div v-for="club in adminClubs" class="col-12 col-md-4 d-flex gap-3 mb-3" :key="club.id">
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
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Clubs you are in -->
                    <div v-if="userClubs.length > 0 && memberClubs.length > 0" class="collapse d-md-block my-4" id="sidebarContent">
                        <h5 class="text-start fw-bold my-3 collapse d-md-block">Clubs You Are In <button v-if="memberClubs.length > 5" type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#showAllJoinedClubs">View all</button></h5>

                        <div v-for="club in memberClubs.slice(0, 5)" class="event-club-box" :key="club.id">

                            <!-- Club Banner Image -->
                            <div style="flex: 0 0 40%; max-width: 40%; height: 100px;">
                                <img v-if="club.clubInfo.clubBanner" :src="club.clubInfo.clubBanner" class="img-fluid event-banner;" alt="..." style="object-fit: cover;">
                                <img v-else :src="defaultBanner" class="img-fluid event-banner;" alt="..." style="object-fit: cover;">
                            </div>
                            <!-- CLub title -->
                            <div class="container text-start ">
                                <router-link :to="{ name: 'clubview', params: { clubID: club.clubID, clubName: slugify(club.clubInfo.clubName) }}" class="fw-bold text-black hover-underline">
                                    {{ club.clubInfo.clubName }}
                                </router-link>
                                <!-- Club details -->
                                <p class="text-success text-start small">
                                        <span v-if="club.isInviteOnly == false">Public Group | </span>
                                        <span v-else>Private Group | </span>
                                        <span>{{ club.totalMembers }} Members</span>
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Clubs you are in modal -->
                    <div class="modal fade" id="showAllJoinedClubs" tabindex="-1" aria-labelledby="showAllJoinedClubsLabel" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-scrollable modal-xl">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="showAllJoinedClubsLabel">Clubs You Are In</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <div class="row">
                                        <div v-for="club in memberClubs" class="col-12 col-md-4 d-flex gap-3 mb-3" :key="club.id">
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
                            </div>  
                        </div>  
                    </div>
                </div>

                <!-- Recent activity [has joined club(s)] or browse club [not yet joined club]-->
                <div class="col-12 col-md-8 ps-3 ps-md-5">

                    <!-- Recent activity [there is recent activity]-->
                    <div v-if="latestPosts.length > 0 && !searchQuery">

                        <!-- Recent Activity Header -->
                        <h5 class="fw-bold mb-3 text-start mobile-fs-5">Recent Activity in Your Clubs</h5>

                        <!-- Bootstrap Horizontal Card for each recent activity -->
                        <div v-for="post in latestPosts" :key="post.id" class="card mb-3">
                            <div class="row g-0">

                                <!-- Recent Activity Information -->
                                <div class="col-12">
                                    <div class="card-body row h-100 mobile-pb-1">
                
                                        <!-- Column 1: Post information -->
                                        <div class="col-12">
                                            <!-- Club Photo + Club Name on same row, aligned left -->
                                            <div class="d-flex flex-row align-items-center justify-content-start">
                                                <!-- Club Photo -->
                                                <img v-if="post.clubBanner" :src="post.clubBanner" class="rounded-circle" alt="..." style="height: 50px; width: 50px; object-fit: cover;">
                                                <img v-else :src="defaultBanner" class="rounded-circle" alt="Default Club Banner" style="height: 50px; width: 50px; object-fit: cover;">
                                                <!-- Poster name and rank on the same line -->
                                                <div class="row">
                                                   <h6 class="ms-2 text-start">
                                                    <router-link :to="profileURL(post.posterInfo.id, post.posterInfo.userType)" class="text-decoration-none hover-underline" style="color:#027562">
                                                        <span class="name-container fw-bold">
                                                            <template v-if="post.posterInfo.userType === 'user'">{{ post.posterInfo.displayName }}</template>
                                                            <template v-else-if="post.posterInfo.userType === 'producer'">{{ post.posterInfo.producerName }}</template>
                                                            <template v-else>{{ post.posterInfo.venueName }}</template>
                                                        </span>
                                                    </router-link>
                                                    <span class="fw-bold fst-italic"> ({{ post.posterInfo.rank }})</span>
                                                    posted in
                                                    <router-link :to="{ name: 'clubview', params: { clubID: post.clubID, clubName: slugify(post.clubName || 'unknown-club') }}" class="fw-bold text-decoration-none hover-underline" style="color:#027562">
                                                        {{ post.clubName }}
                                                    </router-link>
                                                    </h6>
                                                    <!-- Post date -->
                                                    <p class="card-text text-start ms-2 mobile-view-hide">on {{ post.postDate }}
                                                    </p>
                                                </div>
                                            </div>

                                            <div class="text-start d-flex gap-3 mobile-view-show">
                                                <!-- Post date -->
                                                    <p class="card-text text-start mobile-rating-smaller-text-2">on {{ post.postDate }}
                                                    </p>
                                            </div>
                                            
                                            <!-- Post content -->
                                            <p class="card-text text-start mt-2 mobile-rating-smaller-text-2">{{ post.postContent }}</p>
                                            
                                            <!-- Comment input field -->
                                            <div class="row mt-3 pt-3" style="border-top: solid 1px lightgrey;">
                                                <div class="col-12 mb-0">
                                                    <div class="input-group gap-2">
                                                        <input
                                                        type="text"
                                                        class="form-control rounded"
                                                        placeholder="Write a comment..."
                                                        aria-label="Write a comment..."
                                                        aria-describedby="button-addon2"
                                                        v-model="newComments[post.id]"
                                                        />
                                                        <button
                                                        class="mobile-view-hide btn primary-btn-less-round-blue rounded fw-bold"
                                                        type="button"
                                                        id="button-addon2"
                                                        @click="addComment(post.id, post.memberID)"
                                                        >
                                                        Comment
                                                        </button>
                                                        <button
                                                        class="mobile-view-show btn primary-btn-less-round-blue rounded fw-bold"
                                                        type="button"
                                                        id="button-addon2"
                                                        @click="addComment(post.id, post.memberID)"
                                                        >
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                                            <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                                            </svg>
                                                        </button>
                                                        <!-- View Post Button -->
                                                        <button 
                                                        type="button" 
                                                        class="mobile-view-hide btn primary-btn rounded" 
                                                        @click="viewPost(post.id)">
                                                        View Post
                                                        </button>
                                                    
                                                    </div>
                                                    <span @click="viewPost(post.id)" style="cursor: pointer; text-decoration: underline;" class="mt-1 fst-italic mobile-rating-smaller-text-2 mobile-view-show">
                                                        View Post
                                                        </span>
                                                </div>
                                            </div>

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
                    <div v-if="userClubs.length == 0" class="mt-3 mobile-view-hide">
                        <h3 class="text-center fw-bold">You haven't joined a club yet!</h3>
                        <p class="text-center fw-bold">Get on it! Here are some we'd like to recommend!</p>
                    </div>

                    <div v-if="searchResults == ''">
                        <h5 class="fw-bold my-3 text-start mobile-fs-5 mobile-mb-1">Join A New Club!</h5>
                        <p class="text-start small fw-bold mobile-view-show">Get on it! Here are some we'd like to recommend!</p>
                    </div>

                    <!-- Display no results found if search term does not exist in any of the clubs -->
                    <div v-if="searchResults && searchQuery" class="mt-3 text-start">
                        <p class="fw-bold">{{ searchResults }} 
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-x-lg" viewBox="0 0 16 16" style="cursor: pointer;" @click="resetSearch">
                            <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>
                        </svg>
                        </p>
                    </div>

                    <!-- Club Lists --> 
                    <!-- Bootstrap Horizontal Card for each club -->
                    <div class="row mt-3">
                        <div v-for="club in filteredClubs" :key="club.id" class="col-md-6 mb-3 justify-content-center">
                            <div class="rounded-4 shadow-sm p-3 h-100">

                                <!-- Club Banner Image -->
                                <div class="col-md-2 text-start w-100 mb-3" style="width: 400px; height: 150px;">
                                    <img v-if="club.clubBanner" :src="club.clubBanner" 
                                        class="img-fluid border" 
                                        alt="..." 
                                        style="height: 160px; object-fit: cover; border-radius: 0.5rem;"/>
                                    
                                    <img v-else :src="defaultBanner" 
                                        class="img-fluid w-100 border" 
                                        alt="..." 
                                        style="height: 160px; object-fit: cover; border-radius: 0.5rem;"/>
                                </div>

                                <!-- Club Name-->
                                <p class="card-title fw-bold">
                                    <router-link v-if="club.id && club.clubName" :to="{ name: 'clubview', params: { clubID: club.id, clubName: slugify(club.clubName) }}" class="text-dark hover-underline">
                                        {{ club.clubName }}
                                    </router-link>
                                </p>

                                <!-- Club type and number of members -->
                                <p class="text-success small mb-2">
                                    <span v-if="club.isInviteOnly == false">Public Group | </span>
                                    <span v-else>Private Group | </span>
                                    <span>{{ club.totalMembers }} Members</span>
                                </p>

                                <!-- Club Description -->
                                <p class="text-muted small mb-3">{{ club.clubDesc }}</p>

                                <!-- Join Club Button -->
                                <!-- <button v-if="userClubs.includes(club.id)" type="button" class="btn primary-btn-less-round-blue mt-auto align-self-start" disabled>Joined</button> -->
                                <button v-if="requestedClubs.includes(club.id)" type="button" class="btn primary-btn-less-round-blue mt-auto align-self-start w-md-25 fw-bold" disabled>Request Sent!</button>
                                <button v-if="!userClubs.includes(club.id) && club.isInviteOnly == false" type="button" class="btn primary-btn-less-round-blue mt-auto align-self-start w-md-25 fw-bold" @click="joinClub(club.id, club.clubName)">Join Club</button>
                                <button v-if="!userClubs.includes(club.id) && club.isInviteOnly == true && !requestedClubs.includes(club.id)" type="button" class="btn primary-btn-less-round-blue mt-auto align-self-start w-md-25 fw-bold" @click="requestJoin(club.id, club.clubName)">Request to Join</button>
                            </div>
                        </div>
                    </div>

                    <!-- Load More Button -->
                    <div v-if="showButton" class="d-flex justify-content-center mt-3">
                        <button type="button" class="btn secondary-btn btn-md" @click="loadMoreClubs">Load More</button>
                    </div>    
                    
                    <!--Display no clubs yet message -->
                    <div v-if="clubs.length == 0" class="mt-3">
                        <h3>No clubs yet!</h3>
                    </div>
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

            // Variable to store user proof point
            proofPoint: localStorage.getItem("88B_proofPoints") ? localStorage.getItem("88B_proofPoints") : null,
            maxProofPoints: localStorage.getItem("88B_maxProofPoints") ? localStorage.getItem("88B_maxProofPoints") : null,

            // new comment variable
            newComments: {}, // key: post.id, value: comment string

            // Variable for can create club status
            canCreateClub: false,
            cannotCreateClubMsg: "",
            disableCreateClubBtn: false,

             showClubLimitError: false

        }
    },

    methods: {
        slugify(text) {
                if (!text || typeof text !== 'string') return 'unknown';
                    return text
                    .toLowerCase()
                    .replace(/\s+/g, '')
                    .replace(/[^\w]/g, '');
            },
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

        // Function to get create club status
        async getCanCreateClubStatus() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/canCreate/${this.userID}/${this.userType}`);
                this.canCreateClub = response.data.canCreate;

                // cannot create 
                if (!this.canCreateClub) {
                    this.disableCreateClubBtn = true;

                    if (this.userType == "user") {

                        if (response.data.reason == "insufficient points") {
                            this.cannotCreateClubMsg = response.data.message + ". You need a minimum of " + response.data.pointsNeeded + " proof points to create a club.";
                        } else {
                            this.cannotCreateClubMsg = response.data.message;
                        }
                    } 
                    else {
                        this.cannotCreateClubMsg = response.data.message;
                    }
                } else {
                    this.disableCreateClubBtn = false;
                }
                
            } catch (error) {
                console.log(error);
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
                        this.searchResults = "Results with the search term: \"" + this.searchQuery + "\"";
                    }
                }

            }
            catch (error) {
                console.log(error);
                if (error.response.status == 404) {
                    this.searchResults = "No results found for the search term!";
                }
                else
                this.dataLoaded = null;
            }
        },

        // Function to reset the search query
        resetSearch() {
            this.searchQuery = "";
            this.searchResults = "";
            this.getClubs();
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

            const club = this.clubs.find(c => c.id === clubId || c.clubID === clubId);
            const clubName = club ? (club.clubName || club.clubInfo?.clubName) : 'unknown-club';

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
                    this.$router.push({ name: 'clubview', params: { clubID: clubId, clubName: this.slugify(clubName) 
                    } });
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

            const club = this.clubs.find(c => c.id === clubId || c.clubID === clubId);
            const clubName = club ? (club.clubName || club.clubInfo?.clubName) : 'unknown-club';

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
                    this.$router.push({ name: 'clubview', params: { clubID: clubId, clubName: this.slugify(clubName)  } });
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
                return `/profile/user/${posterID}/${this.userName}`;
            }
            else if (userType == 'producer') {
                return `/profile/producer/${posterID}/${this.userName}`;
            }
            else {
                return `/profile/venue/${posterID}/${this.userName}`;
            }
        },

        // Function to decline an invite to join a club
        async declineInvite(clubID) {
            try {
                const response = await this.$axios.delete(`${process.env.VUE_APP_API_URL}/club/declineClubInvites`, 
                {
                    data: {
                        userID: this.userID,
                        clubID: clubID,
                        userType: this.userType
                    }
                }
                );

                if (response.status == 200) {
                    const toast = useToast();
                    toast.success("You have declined the club invite!");
                    // Remove the club from the list of invited clubs
                    this.invitedClubs = this.invitedClubs.filter(club => club.clubID != clubID);
                }
            } catch (error) {
                console.log(error);
                const toast = useToast();
                toast.error("An error occurred while declining the club invite. Please try again later!");
            }
        },

        // Function to accept an invite to join a club
        async acceptInvite(clubID) {

            const club = this.clubs.find(c => c.id === clubID || c.clubID === clubID);
            const clubName = club ? (club.clubName || club.clubInfo?.clubName) : 'unknown-club';

            try {
                const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/club/acceptClubInvite`, {
                    userID: this.userID,
                    clubID: clubID,
                    userType: this.userType
                });

                if (response.status == 201) {
                    const toast = useToast();
                    toast.success("You have successfully joined the club!");
                    // Redirect to the club page
                    this.$router.push({ name: 'clubview', params: { clubID: clubID, clubName: this.slugify(clubName) } });
                }
            } catch (error) {
                console.log(error);
                const toast = useToast();
                toast.error("An error occurred while joining the club. Please try again later!");
            }
        },

        // Function to add comment on a post
        async addComment(id, memberID) {

            const comment = this.newComments[id];

            // Check if the comment is empty
            if (!comment || comment.trim() === "") {
                const toast = useToast();
                toast.error("Please enter a comment before submitting.");
                return;
            }
            try {
                // Comment on the post
                const commentData = await this.$axios.post(
                    `${process.env.VUE_APP_API_URL}/club/addComment`,
                    {
                        postID: id,
                        commenterID: memberID,
                        commentContent: comment
                    }
                );

                // Check if the comment is successful
                if (commentData.status == 201) {
                    // Add the comment to the front of the comments array
                    // this.comments.unshift(commentData.data.comment_obj); 

                    // Clear the comment input
                    this.newComment = "";

                    const toast = useToast();
                    toast.success("Comment added successfully.");
                }
            } catch (error) {
                console.log(error);
                const toast = useToast();
                toast.error(
                "An error occurred while adding the comment. Please try again later."
                );
            }
        },
    },

    computed: {
        // Function to filter clubs by excluding the clubs the user is already a member of
        filteredClubs() {
            return this.clubs.filter(club => !this.userClubs.includes(club.id));
        },
    },

    mounted() {
        // Get all clubs when the page is loaded
        this.getClubs();
        // Get the account id and type of the user
        this.userID = localStorage.getItem("88B_accID");
        let userType = localStorage.getItem("88B_accType");
        this.userName = localStorage.getItem("88B_accUsername");


        if (userType) {
            this.userType = userType;
        }

        if (this.userID && this.userType !== "defaultUser") {

            // Get the create club status 
            this.getCanCreateClubStatus();
            // Get the list of clubs the user is a member of
            this.getMemberClubs();
            // Get the list of clubs the user has requested to join
            this.getRequestedClubs();
            // Get the list of clubs the user has been invited to join
            this.getInvitedClubs();
        }

    }
}

</script>