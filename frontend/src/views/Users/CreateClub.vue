<template>
    <div>
        <NavBar />

        <!-- Main Content -->
        <div class="container mt-5">
            <div class="row">

                <!-- Column 1: Create club form -->
                <div class="col-md-9 text-start">

                    <!-- Header -->
                    <h3 class="fw-bold">Create your club</h3>

                    <!-- Form -->
                    <form>

                        <!-- Club name -->
                        <div class="mb-3">
                            <label for="name" class="form-label">Your Club Name <span class="text-danger">*</span></label>
                            <input type="text" class="form-control" id="name" v-model="club.clubName" required>
                        </div>

                        <!-- Club description -->
                        <div class="mb-3">
                            <label for="description" class="form-label">Your Club Description <span class="text-danger">*</span></label>
                            <textarea class="form-control" id="description" v-model="club.clubDesc" required></textarea>
                        </div>

                        <!-- CLub banner -->
                        <div class="mb-3">
                            <label for="banner" class="form-label">Upload Your Club Banner (optional)</label>
                            <input type="file" class="form-control" id="banner" @change="uploadImage" accept="image/*">

                            <!-- Preview of the banner -->
                            <div v-if="club.clubBanner">
                                <img :src="club.clubBanner" alt="Banner Preview" class="img-fluid mt-3" style="max-height: 300px;">
                                <!-- Remove banner button  -->
                                <button class="btn btn-danger ms-3" @click="removeImage()">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                                        <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0"/>
                                    </svg>
                                </button>
                            </div>
                        </div>

                        <!-- Make club private or public -->
                        <div class="mb-3">
                            <input type="checkbox" class="me-3" v-model="club.isInviteOnly"> Make Your Club Invite-Only
                        </div>
                    </form>
                </div>

                <!-- Column 2: Invite friends section -->
                <div class="col-md-3 text-start">

                    <!-- Header -->
                    <h5 class="fw-bold">Invite Friends (optional)</h5>
                    <p>Note: You can only invite friends who you are already following.</p>

                    <!-- Search bar -->
                    <div class="input-group mb-3 position-relative">
                        <input type="text" class="form-control rounded" placeholder="Search for your friends" aria-label="Search for clubs" aria-describedby="search-club" v-model="searchQuery" @change="searchFriend">
                        <!-- Search Icon -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-search position-absolute" viewBox="0 0 16 16" style="right: 10px; top: 50%; transform: translateY(-50%); cursor: pointer; z-index: 5;"
                            @click="searchClubs">
                            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                        </svg>
                        <!-- Dropdown list -->
                        <ul v-if="Object.keys(searchResults).length > 0" class="dropdown-menu show position-absolute" style="width: 100%; top: 100%; margin-top: 0.5rem;">
                            <li v-for="(friend, id) in searchResults" :key="id" class="dropdown-item" @click="addFriend(id)" style="cursor: pointer;">
                                {{ friend.displayName }}
                            </li>
                        </ul>
                    </div>

                    <!-- Error message if fetching of friend list fails -->
                    <p v-if="errorFriendList != ''" class="text-danger">{{ errorFriendList }}</p>
                
                    <!-- List of selected friends (icons of their profile photo)-->
                    <h6 v-if="friendsToInvite.length > 0" class="fw-bold">Selected Friends</h6>
                    <div v-if="friendsToInvite.length > 0" class="d-flex flex-wrap">
                        <div v-for="id in friendsToInvite" :key="id" class="me-2 mb-2 position-relative">
                            <!-- Details of each friend -->
                            <div class="d-flex flex-column align-items-center">
                                <!-- Display the profile photo of the friend, if available, else use a default profile pic -->
                                <img v-if="friends[id].photo" :src="friends[id].photo" class="rounded-circle" style="width: 50px; height: 50px;" alt="profile-photo">
                                <svg v-else xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                                    <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                                    <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                                </svg>

                                <!-- Name of friend -->
                                <p class="text-center">{{ friends[id].displayName }}</p>
                            </div>
                            
                            <!-- Remove friend button -->
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="red" 
                                class="bi bi-x-circle-fill position-absolute top-0 end-0" viewBox="0 0 16 16"
                                style="cursor: pointer;" @click="removeFriend(id)">
                                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/>
                            </svg>
                            
                        </div>
                    </div>


                </div>
            </div>

            <!-- Create club button -->
            <div class="d-flex justify-content-end mt-3">
                <button type="submit" class="btn btn-primary" :disabled="loading" @click="createClub">
                    <span v-if="!loading">Create Club</span>
                    <div v-else class="spinner-border  spinner-border-sm" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </button>
            </div>
        </div>
        
    </div>
</template>

<script>
// Import the necessary libraries
import NavBar from '@/components/NavBar.vue';

export default {
    name: "CreateClub",
    components: {
        NavBar
    },
    data() {
        return {
            // User ID and user type
            userID: "",
            userType: "",

            // Club object to store the club details
            club: {
                clubName: "",
                clubDesc: "",
                isInviteOnly: false,
                clubBanner: null
            },

            // Dictionary to store the friends the user is following
            friends: {},
            errorFriendList: "", // Error message if fetching of friend list fails

            // Variables for searching friends
            searchQuery: "",

            // List of friends to be invited
            friendsToInvite: [],

            // Variable to show loading spinner
            loading: false
        }
    },
    computed: {

        // Function to search for friends
        searchResults() {
            if (this.searchQuery) {
                // Convert the search query to lowercase
                let query = this.searchQuery.toLowerCase();
                let results = {};

                // Returns the list of friends display name, whose display name starts with the search query
                for (const [id, friend] of Object.entries(this.friends)) {

                    // Check if the id is already in the list of friends to be invited
                    if (this.friendsToInvite.includes(id)) {
                        continue;
                    }

                    // Else, check if the display name of the friend contains the search query
                    if (friend.displayName.toLowerCase().includes(query)) {
                        results[id] = friend;
                    }
                }
                return results;
            } else {
                return [];
            }
        }
    },
    methods: {

        // Function to retrieve data for the page ========================================
        // Function to get the list of users the current user is following
        async getFriends() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUserFollowList/${this.userID}`);
                this.friends = response.data.followList.users;
            } catch (error) {
                console.log(error);
                this.errorFriendList = "Failed to fetch the list of friends. Please try again later.";
            }
        },
        // ===============================================================================

        // Functions for user interaction ================================================
        // Function to add a friend to the list of friends to be invited
        addFriend(friendID) {
            // Check if the friend is already in the list
            if (!this.friendsToInvite.includes(friendID)) {
                this.friendsToInvite.push(friendID);
            }

            // Clear the search query
            this.searchQuery = "";
        },

        // Function to remove a friend from the list of friends to be invited
        removeFriend(friendID) {
            // Find the index of the friend in the list
            const index = this.friendsToInvite.indexOf(friendID);

            // Remove the friend from the list
            if (index > -1) {
                this.friendsToInvite.splice(index, 1);
            }
        },

        // Function to create the club
        createClub() {
            // Create the club object
            let clubObj = {
                creatorID: this.userID,
                creatorType: this.userType,
                clubName: this.club.clubName,
                clubDesc: this.club.clubDesc,
                isInviteOnly: this.club.isInviteOnly,
            }

            // Check if a banner image is uploaded
            if (this.club.clubBanner) {
                clubObj.image64 = this.club.clubBanner;
            }

            this.loading = true;

            console.log(clubObj);
            return;

            // Send the club object to the backend
            // this.$axios.post(`${process.env.VUE_APP_API_URL}/club/createClubs`, clubObj)
            //     .then((response) => {

            //         if (response.status == 201) {

            //             // Check if any friends are to be invited
            //             if (this.friendsToInvite.length > 0) {
            //                  // Add the friends to the club
            //                 this.addFriendsToClub(response.data.clubID);
            //             } else {
            //                 // Redirect to the club page
            //                 this.$router.push(`/club/view/${response.data.clubID}`);
            //             } 
            //         } 
            //     })
            //     .catch((error) => {
            //         console.log(error);
            //         alert("Failed to create the club. Please try again later.");
            //     });
        },

        // Function to add invited friends to the club
        addFriendsToClub(clubID) {
            // Format the list of friends to be invited
            let newMembers = []
            for (const friendID of this.friendsToInvite) {
                newMembers.push({
                    userID: friendID,
                    isAdmin: false,
                    userType: "user"
                });
            }

            // Send the list of friends to be invited to the backend
            this.$axios.post(`${process.env.VUE_APP_API_URL}/club/addClubMembers`, {
                clubID: clubID,
                new_members: newMembers
            })
                .then(() => {
                    // Redirect to the club page
                    this.$router.push(`/club/view/${clubID}`);
                })
                .catch((error) => {
                    console.log(error);
                    alert("Failed to add friends to the club. Please add your friends in the club page.");
                    // Redirect to the club page
                    this.$router.push(`/club/view/${clubID}`);
                });
        },

        // ===============================================================================

        // Helper functions ==============================================================
        // Function to upload images and convert them to base64String
        uploadImage(e) {
            const file = e.target.files[0];
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = (e) => {
                this.club.clubBanner = e.target.result;
            }
        },

        // Function to remove the image and reset the input field
        removeImage() {
            this.club.clubBanner = "";
            document.getElementById("banner").value = "";
        },
        // ===============================================================================

    },
    mounted() {
        // Get the user id and the user type from the local storage
        this.userID = localStorage.getItem("88B_accID");
        this.userType = localStorage.getItem("88B_accType");

        // Get the list of friends the user is following (only for users who are user type)
        if (this.userType === "user") {
            this.getFriends();
        }
    }
}
</script>