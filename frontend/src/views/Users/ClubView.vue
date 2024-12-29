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
        <div v-if="dataLoaded == true">

            <!-- Club Banner -->
            <div class="container-fluid p-0 border-bottom">
                <img :src="defaultBanner" class="img-fluid" alt="Club Banner">
            </div>

            <!-- Main content -->
            <div class=" container mt-5">
                <div class="row">

                    <!-- Column 1: Club name, join button / add post button, posts-->
                    <div class="col-md-9 order-md-1 order-2">

                        <!-- Row 1: Club name, join button / add post button -->
                        <div class="row">
                            <div class="col-md-6">
                                <h1 class="fw-bold text-start">{{ clubInfo.clubName }}</h1>
                            </div>
                            <div class="col-md-6 text-end">
                                <button v-if="isMember" class="btn primary-btn-green">Add Post</button>
                                <button v-else class="btn primary-btn-green">Join Club</button>
                            </div>
                        </div>

                        <h4 class="fst-italic text-start mt-3">Latest Posts</h4>

                        <!-- Row 2: Post -->
                        <div v-if="posts.length == 0" class="text-center mt-5">
                            <h3 class="fw-bold">No posts available yet!</h3>
                        </div>

                        <div v-else>
                            <!-- Post -->
                            <div v-for="post in posts" :key="post.postID" class="row">

                                <!-- Column 1: Poster Photo -->
                                <div class="col-md-2">
                                    <router-link :to="profileURL(post.posterID)">
                                        <p class="fw-bold">{{ post.posterName }}</p>

                                    </router-link>
                                    <img v-if="post.posterPhoto" :src="post.posterPhoto" class="img-fluid rounded-circle" alt="Poster Photo">
                                    <svg v-else xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                                        <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                                        <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                                    </svg>
                                </div>
                                
                                <!-- Column 2: Post Details -->
                            </div>
                        </div>
                    </div>

                    <!-- Column 2: Club type, number of members, club description and invite button -->
                    <div class="col-md-3 order-md-2 order-1 ps-md-3">

                        <!-- Club type and number of members -->
                        <p class="text-start">
                            <span v-if="clubInfo.isInviteOnly" class="fw-bold"> Private Group </span>
                            <span v-else class="fw-bold"> Public Group </span>
                            <span> | </span>
                            <span class="fw-bold">Number of Members:</span> {{ clubInfo.totalMembers }}
                        </p>

                        <!-- Club description -->
                        <p class="text-start">{{ clubInfo.clubDesc }}</p>

                        <!-- Invite button -->
                        <button class="ps-0 btn d-flex align-items-center hover-underline">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-share" viewBox="0 0 16 16">
                                <path d="M13.5 1a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3M11 2.5a2.5 2.5 0 1 1 .603 1.628l-6.718 3.12a2.5 2.5 0 0 1 0 1.504l6.718 3.12a2.5 2.5 0 1 1-.488.876l-6.718-3.12a2.5 2.5 0 1 1 0-3.256l6.718-3.12A2.5 2.5 0 0 1 11 2.5m-8.5 4a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3m11 5.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3"/>
                            </svg>
                            <span class="ms-2">Invite your friends!</span>
                        </button>
                    </div>

                </div>
            </div>


        </div>
    </div>
</template>

<script>
// Import the necessary libraries
import NavBar from '@/components/NavBar.vue';

export default {
    name: "ClubView",
    components: {
        NavBar
    },
    data() {
        return {
            // Variable for page loading 
            dataLoaded: false,

            // Variables for user data
            userID: null,
            userType: null,
            isMember: false,
            isAdmin: false,

            // Variable for default banner
            defaultBanner: require('@/assets/defaultGroupBanner.png'),

            // Variable for club data
            clubId: null,
            clubInfo: null,
            posts: [], // Array to store posts

            // Variable for lazy loading for posts
            offsetNum: 0, // Number of posts to skip (initial loading is 0)
        }
    },
    computed: {
        // Computed property to get the profile URL of the poster
        profileURL(posterID) {
            if (this.userType == 'user') {
                return `/profile/user/${posterID}`;
            }
            else if (this.userType == 'producer') {
                return `/profile/producer/${posterID}`;
            }
            else {
                return `/profile/venue/${posterID}`;
            }

        }
    },
    methods: {
        // Function to get club information
        async getPageData() {
            try {
                // Get club data
                const clubData = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getSpecificClubInfo/${this.clubId}`);
                this.clubInfo = clubData.data.club_info;

                this.dataLoaded = true;

                // Get posts
                this.getPosts();

            } catch (error) {
                // Check if status code is 404
                if (error.response.status == 404) {
                    this.dataLoaded = null;
                }
                console.log(error);
                this.dataLoaded = null;
            }
        },

        // Function to get posts
        async getPosts() {
            try {
                // Get posts
                const postsData = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getClubPosts/${this.clubId}/${this.offsetNum}`);
                this.posts = postsData.data.data;
            } catch (error) {
                console.log(error);
                if (error.response.status == 404) {
                    this.dataLoaded = true;
                }
                else {
                    this.dataLoaded = null;
                }
            }
        },

        // Function to check if the user is a member of the club (used to display join or add post button & to determine admin privileges)
        async checkMembership() {
            try {
                // Get membership status
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/checkUserMembership/${this.userID}/${this.clubId}`);
                this.isMember = response.data.isMember;
                this.isAdmin = response.data.isAdmin;
            } catch (error) {
                console.log(error);
            }
        }
    },
    mounted() {
        // Get club id from the URL
        this.clubId = this.$route.params.clubID;
        // Get the account id and type of the user
        this.userID = localStorage.getItem("88B_accID");
        this.userType = localStorage.getItem("88B_accType");

        this.getPageData();
        this.checkMembership();

    }
}
</script>