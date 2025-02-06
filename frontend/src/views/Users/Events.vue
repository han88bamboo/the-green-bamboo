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
                    <h3 class="text-start fw-bold">Find events near you!</h3>
                </div>

                <!-- Search Input -->
                <div>
                    <div class="input-group mb-3 position-relative">
                        <input type="text" class="form-control rounded-pill" placeholder="Search for events" aria-label="Search for clubs" aria-describedby="search-club" v-model="searchQuery">
                        <!-- Search Icon -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-search position-absolute" viewBox="0 0 16 16" style="right: 10px; top: 50%; transform: translateY(-50%); cursor: pointer; z-index: 5;"
                            @click="searchClubs">
                            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                        </svg>
                    </div>
                </div> 

                <!-- Create Club Button -->
                <div class="text-start">
                    <button class="btn btn-primary">+ Create an Event</button>
                </div>

                <!-- Club Invite-->
                <div v-if="invitedClubs.length > 0" class="mt-3">
                    <h3 class="text-start fw-bold">Clubs You Are Invited To</h3>

                    <div v-for="club in invitedClubs.slice(0, 5)" class="d-flex gap-3" :key="club.id">

                        <div class="row w-100 align-items-center">
                            <div class="col-7 text-start">
                                <!-- CLub title -->
                                <router-link :to="{ name: 'clubview', params: { clubID: club.clubID }}" class="text-dark hover-underline fw-bold">
                                    {{ club.clubName }}
                                </router-link>

                                <!-- Invited by -->
                                <p class="text-start">Invited by: {{ club.inviterInfo.displayName }}</p>
                            </div>

                            <div class="col-5">
                                <!-- Decline Button -->
                                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="red" class="bi bi-x-circle me-3" viewBox="0 0 16 16" style="cursor: pointer;" @click="declineInvite(club.clubID)">
                                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                                    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                                </svg>
                                <!-- Accept Button -->
                                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="green" class="bi bi-check-circle" viewBox="0 0 16 16" style="cursor: pointer;" @click="acceptInvite(club.clubID)">
                                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                                    <path d="m10.97 4.97-.02.022-3.473 4.425-2.093-2.094a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05"/>
                                </svg>
                            </div>

                            <hr>
                        </div>

                        
                    </div>
                </div>

                <!-- Clubs you manage -->
                <div v-if="userClubs.length > 0 && adminClubs.length > 0" class="mt-3">
                    <h3 class="text-start fw-bold">Clubs You Manage <button v-if="adminClubs.length > 5" type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#showAllManagedClubs">View All</button></h3>

                    <div v-for="club in adminClubs.slice(0, 5)" class="d-flex gap-3" :key="club.id">

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
                <div v-if="userClubs.length > 0 && memberClubs.length > 0" class="mt-3">
                    <h3 class="text-start fw-bold">Clubs You Are In <button v-if="memberClubs.length > 5" type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#showAllJoinedClubs">View all</button></h3>

                    <div v-for="club in memberClubs.slice(0, 5)" class="d-flex gap-3 mb-3" :key="club.id">

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
            <div class="col-12 col-md-9">

                <!-- Recent activity [there is recent activity]-->
                <div v-if="latestPosts.length > 0 && !searchQuery">

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

                <!-- Display no results found if search term does not exist in any of the clubs -->
                <div v-if="searchResults && searchQuery" class="mt-3 text-start">
                    <p class="fw-bold">{{ searchResults }}</p>
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
import NavBar from '@/components/NavBar.vue';


export default {
    name: 'EventsPage',
    components: {
        NavBar
    },
    data() {
        return {
            // Data
            dataLoaded: false,
        }
    },
}
</script>

<style>
/* Resize Quill toolbar icons */
.ql-toolbar .ql-formats svg {
width: 20px;
height: 20px;
}

/* Resize SVGs inside the content */
.ql-editor svg {
width: 20px;
height: 20px;
}
</style>