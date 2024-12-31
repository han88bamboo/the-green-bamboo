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
                            <div v-for="post in posts" :key="post.id" class="row mb-4">

                                <!-- Column 1: Poster Photo -->
                                <div class="col-md-1 d-flex flex-column align-items-start">
                                    <router-link :to="profileURL(post.posterInfo.id, post.posterInfo.userType)">
                                        <p class="fw-bold">{{ post.posterName }}</p>

                                    </router-link>
                                    <img v-if="post.posterPhoto" :src="post.posterPhoto" class="img-fluid rounded-circle" alt="Poster Photo">
                                    <svg v-else xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                                        <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                                        <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                                    </svg>
                                </div>
                                
                                <!-- Column 2: Post Details -->
                                <div class="col-md-11">

                                    <!-- Row 1: User name and post date -->
                                    <div class="row text-start">
                                        <div class="col-md-3">
                                            <router-link :to="profileURL(post.posterInfo.id, post.posterInfo.userType)" class="text-black">
                                                <p v-if="post.posterInfo.userType == 'user'" class="fw-bold">{{ post.posterInfo.displayName }}</p>
                                                <p v-else-if="post.posterInfo.userType == 'producer'" class="fw-bold">{{ post.posterInfo.producerName }}</p>
                                                <p v-else class="fw-bold">{{ post.posterInfo.venueName }}</p>
                                            </router-link>
                                        </div>
                                        <div class="col-md-6">
                                            <p>{{ post.postDate }}</p>
                                        </div>
                                    </div>

                                    <!-- Row 2: Post photo (optional) -->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <img v-if="post.postPhoto" :src="post.postPhoto" class="img-fluid" alt="Post Photo">
                                        </div>
                                    </div>

                                    <!-- Row 3: Post content -->
                                    <div class="row text-start">
                                        <div class="col-md-12">
                                            <p>{{ post.postContent }}</p>
                                        </div>
                                    </div>

                                    <!-- Row 4: Post info such as total likes, total comments -->
                                    <div class="row text-start">
                                        <div class="col-md-12 d-flex gap-4">
                                            <p class="fw-bold">Total Likes: {{ post.totalLikes }}</p>
                                            <p class="fw-bold">Total Comments: {{ post.totalComments }} </p>
                                        </div>
                                    </div>

                                    <!-- Row 5: Like button image -->
                                    <div v-if="!isMember" class="row text-start">
                                        <div class="col-12 d-flex gap-4">

                                            <!-- Red thumbs up with red fill if user already liked the post -->
                                            <p v-if="postLikes.includes(post.id)">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="red" class="bi bi-hand-thumbs-up-fill" viewBox="0 0 16 16"
                                                    style="cursor: pointer;" @click="likePost(post.id)">
                                                    <path d="M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a10 10 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733q.086.18.138.363c.077.27.113.567.113.856s-.036.586-.113.856c-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.2 3.2 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.8 4.8 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"/>
                                                </svg>
                                            </p>

                                            <!-- Black thumbs up with no fill if user has not liked the post -->
                                            <p v-else>
                                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-hand-thumbs-up cursor-pointer" viewBox="0 0 16 16"
                                                    style="cursor: pointer;" @click="likePost(post.id)" 
                                                    >
                                                    <path d="M8.864.046C7.908-.193 7.02.53 6.956 1.466c-.072 1.051-.23 2.016-.428 2.59-.125.36-.479 1.013-1.04 1.639-.557.623-1.282 1.178-2.131 1.41C2.685 7.288 2 7.87 2 8.72v4.001c0 .845.682 1.464 1.448 1.545 1.07.114 1.564.415 2.068.723l.048.03c.272.165.578.348.97.484.397.136.861.217 1.466.217h3.5c.937 0 1.599-.477 1.934-1.064a1.86 1.86 0 0 0 .254-.912c0-.152-.023-.312-.077-.464.201-.263.38-.578.488-.901.11-.33.172-.762.004-1.149.069-.13.12-.269.159-.403.077-.27.113-.568.113-.857 0-.288-.036-.585-.113-.856a2 2 0 0 0-.138-.362 1.9 1.9 0 0 0 .234-1.734c-.206-.592-.682-1.1-1.2-1.272-.847-.282-1.803-.276-2.516-.211a10 10 0 0 0-.443.05 9.4 9.4 0 0 0-.062-4.509A1.38 1.38 0 0 0 9.125.111zM11.5 14.721H8c-.51 0-.863-.069-1.14-.164-.281-.097-.506-.228-.776-.393l-.04-.024c-.555-.339-1.198-.731-2.49-.868-.333-.036-.554-.29-.554-.55V8.72c0-.254.226-.543.62-.65 1.095-.3 1.977-.996 2.614-1.708.635-.71 1.064-1.475 1.238-1.978.243-.7.407-1.768.482-2.85.025-.362.36-.594.667-.518l.262.066c.16.04.258.143.288.255a8.34 8.34 0 0 1-.145 4.725.5.5 0 0 0 .595.644l.003-.001.014-.003.058-.014a9 9 0 0 1 1.036-.157c.663-.06 1.457-.054 2.11.164.175.058.45.3.57.65.107.308.087.67-.266 1.022l-.353.353.353.354c.043.043.105.141.154.315.048.167.075.37.075.581 0 .212-.027.414-.075.582-.05.174-.111.272-.154.315l-.353.353.353.354c.047.047.109.177.005.488a2.2 2.2 0 0 1-.505.805l-.353.353.353.354c.006.005.041.05.041.17a.9.9 0 0 1-.121.416c-.165.288-.503.56-1.066.56z"/>
                                                </svg>
                                            </p>

                                            <!-- Comment icon -->
                                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-chat-dots" viewBox="0 0 16 16"
                                                style="cursor: pointer;"
                                                data-bs-toggle="tooltip"
                                                title="Tooltip text">
                                                <path d="M5 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0m4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0m3 1a1 1 0 1 0 0-2 1 1 0 0 0 0 2"/>
                                                <path d="m2.165 15.803.02-.004c1.83-.363 2.948-.842 3.468-1.105A9 9 0 0 0 8 15c4.418 0 8-3.134 8-7s-3.582-7-8-7-8 3.134-8 7c0 1.76.743 3.37 1.97 4.6a10.4 10.4 0 0 1-.524 2.318l-.003.011a11 11 0 0 1-.244.637c-.079.186.074.394.273.362a22 22 0 0 0 .693-.125m.8-3.108a1 1 0 0 0-.287-.801C1.618 10.83 1 9.468 1 8c0-3.192 3.004-6 7-6s7 2.808 7 6-3.004 6-7 6a8 8 0 0 1-2.088-.272 1 1 0 0 0-.711.074c-.387.196-1.24.57-2.634.893a11 11 0 0 0 .398-2"/>
                                            </svg>
                                        </div>
                                    </div>
                                </div>

                            </div>

                            <!-- Load more post -->
                            <div v-if="showButton" class="d-flex justify-content-center mt-3">
                                <button type="button" class="btn secondary-btn btn-md" @click="loadMorePosts">Load More</button>
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
import Tooltip from 'bootstrap/js/dist/tooltip'; // Import Tooltip class from Bootstrap


export default {
    name: "ClubView",
    components: {
        NavBar
    },
    data() {
        return {
            // Variable for page loading 
            dataLoaded: false,

            // Variable for thumbs up icon
            outlineColor: "black",
            innerFill: "blue",

            // Variable for show more button
            showButton: true,

            // Variables for user data
            userID: null,
            userType: null,
            isMember: false,
            isAdmin: false,
            memberID: null,

            // Variable for default banner
            defaultBanner: require('@/assets/defaultGroupBanner.png'),

            // Variable for club data
            clubId: null,
            clubInfo: null,
            posts: [], // Array to store posts
            postLikes: [], // Array to store user's likes for the posts

            // Variable for lazy loading for posts
            offsetNum: 0, // Number of posts to skip (initial loading is 0)
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

        // Function to load more posts
        async loadMorePosts() {
            try {
                // Increase the offset number
                this.offsetNum += 10;

                // Get more posts
                const postsData = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getClubPosts/${this.clubId}/${this.offsetNum}`);
                this.posts = this.posts.concat(postsData.data.data);

                // Check if there are more posts to load
                if (postsData.data.data.length < 5) {
                    this.showButton = false;
                }

            } catch (error) {
                console.log(error);
            }
        },

        // Function to check if the user is a member of the club (used to display join or add post button & to determine admin privileges)
        async checkMembership() {
            try {
                // Get membership status
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/checkUserMembership/${this.userID}/${this.clubId}`);
                this.isMember = response.data.isMember;
                this.isAdmin = response.data.isAdmin;
                this.memberID = response.data.memberID;

                // If current user is a member, get the user's likes for the posts
                if (this.isMember) {
                    this.getPostLikes();
                }

            } catch (error) {
                console.log(error);
            }
        },

        // Function to get the profile URL of the poster
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

        // Function to get the user's likes for the posts
        async getPostLikes() {
            try {
                // Get likes
                const postLikesData = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getUserLikesPost/${this.memberID}/${this.clubId}`);
                return postLikesData.data.liked_posts;
            } catch (error) {
                console.log(error);
            }
        },

        // Function to like a post
        async likePost(postID) {
            try {
                // Like the post
                const likeData = await this.$axios.put(`${process.env.VUE_APP_API_URL}/club/likeUnlikePost`, {
                    postID: postID,
                    memberID: this.memberID,
                    clubID: this.clubId
                });

                // Check if the post is liked or unliked
                if (likeData.data.liked) {
                    this.postLikes.push(postID);
                }
                else {
                    // Get the current index of the postID in the postLikes array
                    const index = this.postLikes.indexOf(postID);

                    // If the postID is found, remove it from the array [index is -1 if not found]
                    if (index > -1) {
                        this.postLikes.splice(index, 1);
                    }
                }

                // Refresh the page to update the like status
                window.location.reload();

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

        // Ensure DOM is fully rendered before initializing tooltips
        this.$nextTick(() => {
            const tooltipTriggerEl = this.$el.querySelector('[data-bs-toggle="tooltip"]');

            // Initialize tooltip if element exists
            if (tooltipTriggerEl) {
                this.tooltipInstance = new Tooltip(tooltipTriggerEl);
            } else {
                console.error('Tooltip trigger element not found');
            }
        });

    },
    beforeUnmount() {
        // Dispose of the tooltip to prevent memory leaks
        if (this.tooltipInstance) {
            this.tooltipInstance.dispose();
        }
    },
}
</script>