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
                    <form @submit.prevent="createClub">

                        <!-- Club name -->
                        <div class="mb-3">
                            <label for="name" class="form-label">Your Club Name:</label>
                            <input type="text" class="form-control" id="name" v-model="club.clubName" required>
                        </div>

                        <!-- Club description -->
                        <div class="mb-3">
                            <label for="description" class="form-label">Your Club Description</label>
                            <textarea class="form-control" id="description" v-model="club.clubDesc" required></textarea>
                        </div>

                        <!-- CLub banner -->
                        <div class="mb-3">
                            <label for="banner" class="form-label">Upload Your Club Banner</label>
                            <input type="file" class="form-control" id="banner" @change="uploadImage" accept="image/*" required>

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

                        <button type="submit" class="btn btn-primary">Create Club</button>
                    </form>
                </div>

                <!-- Column 2: Invite friends section -->
                <div class="col-md-3 text-start">

                    <!-- Header -->
                    <h5 class="fw-bold">Invite Friends</h5>

                    <!-- Search bar -->
                    <div class="input-group mb-3 position-relative">
                        <input type="text" class="form-control rounded" placeholder="Search for your friends" aria-label="Search for clubs" aria-describedby="search-club" v-model="searchQuery">
                        <!-- Search Icon -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-search position-absolute" viewBox="0 0 16 16" style="right: 10px; top: 50%; transform: translateY(-50%); cursor: pointer; z-index: 5;"
                            @click="searchClubs">
                            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                        </svg>
                    </div>
                
                    <!-- List of friends (icons of their profile photo)-->
                    <div class="d-flex flex-wrap">
                        <div v-for="friend in friends" :key="friend.id" class="me-2 mb-2">
                            <img :src="friend.profilePhoto" class="rounded-circle" style="width: 50px; height: 50px;" alt="profile-photo">
                        </div>
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
    name: "CreateClub",
    components: {
        NavBar
    },
    data() {
        return {

            // Club object to store the club details
            club: {
                clubName: "",
                clubDesc: "",
                isInviteOnly: false,
                clubBanner: ""
            },
        }
    },
    methods: {
        createClub() {
            console.log(this.club);
        },

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

    }
}
</script>