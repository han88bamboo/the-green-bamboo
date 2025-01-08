<template>
    <div class="container mb-3 text-start">

        <!-- Club Information Section -->
        <div class="row mt-3">

            <!-- Row 1: Club setting title and edit buttons -->
            <div class="row d-flex justify-content-between align-items-center">

                <!-- Column 1: Club setting title -->
                <div class="col-auto d-flex">
                    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="32" fill="currentColor" class="bi bi-arrow-left" viewBox="0 0 16 16" @click="backToClub" style="cursor: pointer;">
                        <path fill-rule="evenodd" d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8"/>
                    </svg>
                    <h3 class="fw-bold ms-2">Club Settings</h3>
                </div>

                <!-- Column 2: Edit / Save button -->
                <div class="col-auto">
                    <button v-if="editMode && !loading" class="btn" @click="cancelUpdate" :disabled="loading">
                        Cancel
                    </button>
                    <button v-if="!editMode" class="btn btn-primary" @click="editMode = true">
                        Edit
                    </button>
                    <button v-if="editMode && !loading" class="btn btn-primary" @click="updateClubInfo" :disabled="!editMode">
                        Save
                    </button>
                    <button v-if="loading" class="btn btn-primary" disabled>
                        <div class="spinner-border  spinner-border-sm" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </button>
                </div>
            </div>

            <!-- Row 2: Club Name -->
            <div class="row mt-3">
                <label for="clubName" class="form-label">Club Name</label>
                <input type="text" class="form-control" id="clubName" v-model="localClubInfo.clubName" :disabled="!editMode">
            </div>

            <!-- Row 3: Club Description -->
            <div class="row mt-3">
                <label for="clubDescription" class="form-label">Club Description</label>
                <textarea class="form-control" id="clubDescription" rows="3" v-model="localClubInfo.clubDescription" :disabled="!editMode"></textarea>
            </div>

            <!-- Row 4: Club Banner -->
            <div class="row mt-3">
                <label for="clubBanner" class="form-label">Club Banner</label>
                <!-- Show current Banner -->
                <img v-if="clubInfo.clubBanner !=''" :src="clubInfo.clubBanner" alt="Club Banner" class="img-thumbnail" style="max-width: 200px;">
                <img v-else :src="defaultBanner" alt="Default Banner" class="img-thumbnail" style="max-width: 200px;">
                <input v-if="editMode" type="file" class="form-control mt-3" id="clubBanner" accept="image/*" @change="uploadImage" :disabled="!editMode"> 
            </div>

            <!-- Row 5: Is Invite Only -->
            <div class="row mt-3">
                <label for="isInviteOnly" class="form-label">Group Type</label>
                <div class="form-check d-flex align-items-center">
                    <input type="checkbox" class="form-check-input me-2" id="isInviteOnly" v-model="localClubInfo.isInviteOnly" :disabled="!editMode" style="cursor: pointer;">
                    <label for="isInviteOnly" class="form-check-label">Is Invite Only</label>
                </div>
            </div>

        </div>

        <!-- Horizontal line divider to seperate sections -->
        <hr>

        <!-- Club Member Management Section -->
        <div class="row mt-3">

            <!-- Row 6: -->
            <div class="row d-flex justify-content-between align-items-center">

                <!-- Column 1: Club Member Management Title -->
                <div class="col-auto d-flex">
                    <h4 class="fw-bold"> Club Member Management </h4>
                </div>

                <!-- Column 2: Edit / Save button -->
                <div class="col-auto">
                    <button class="btn btn-primary" @click="manageMode = true">
                        Manage
                    </button>
                </div>
                
            </div>

            <!-- Row 7: Table of club members -->
            

        </div>

        <!-- Horizontal line divider to seperate sections -->
        <hr>



        <!-- Club Member Request Section-->



        <!-- Delete club Section -->
        <div class="row mt-3">
            <h4 class="fw-bold"> Delete Club </h4>
            <p><span class="text-danger fw-bold">Warning:</span> This action is irreversible. Deleting the club will remove all posts and comments from the database.</p>
            <button class=" col-3 btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteClubModal" style="cursor: pointer;">
                Delete Club
            </button>
        </div>

        <!-- Delete club modal start -->
        <div class="modal fade" id="deleteClubModal" tabindex="-1" aria-labelledby="deleteClubModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="deleteClubModalLabel">Delete Club</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        Are you sure you want to delete the club? This action is irreversible. Deleting the club will remove all posts and comments from the database.
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn" data-bs-dismiss="modal" :disabled="loading">Close</button>
                        <button v-if="!loading" type="button" class="btn btn-danger" @click="deleteClub" :disabled="loading" data-bs-dismiss="modal">Delete</button>
                        <button v-if="loading" class="btn btn-primary" disabled>
                            <div class="spinner-border  spinner-border-sm" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                        </button>

                    </div>
                </div>
            </div>
        </div>
        <!-- Delete club modal end -->
    </div>
</template>

<script>
import { useToast } from 'vue-toastification';

export default {
    name: "ClubSettings",
    props: {
        // Original clubInfo object
        clubInfo: {
            type: Object,
            required: true
        },
        clubId: {
            type: Number,
            required: true
        },
        memberID: {
            type: Number,
            required: true
        }
    },
    data() {
        return {

            // Create a local deep copy of the clubInfo object as clubInfo prop is readonly (cannot be modified)
            localClubInfo: JSON.parse(JSON.stringify(this.clubInfo)),

            // Variable to toggle edit mode to edit club information
            editMode: false,

            // Variable for default banner
            defaultBanner: require('@/assets/defaultGroupBanner.png'),

            // Variable to show loading spinner
            loading: false,

            // Variable to manage club members to make them admin or remove them
            manageMode: false
        };
    },
    methods: {

        // Function to go back to close club settings component
        backToClub() {
            this.$emit('close-club-settings');
        },

        // Function to cancel update
        cancelUpdate() {
            this.localClubInfo = JSON.parse(JSON.stringify(this.clubInfo));
            this.editMode = false;
        },

        // Function to update club information
        updateClubInfo() {

            this.loading = true;

            // Create a club object to send to backend
            const clubObj = {
                clubID: this.clubId,
                clubName: this.localClubInfo.clubName,
                clubDesc: this.localClubInfo.clubDesc,
                image64: this.localClubInfo.clubBanner,
                isInviteOnly: this.localClubInfo.isInviteOnly,
                editorID: this.memberID
            };

            // Send a post request to update club information
            this.$axios.put(`${process.env.VUE_APP_API_URL}/club/updateClubInfo`, clubObj)
                .then((response) => {
                    console.log(response.data);
                    const toast = useToast();
                    toast.success('Club information updated successfully');
                    this.editMode = false;
                    this.loading = false;
                })
                .catch((error) => {
                    console.error(error);
                    const toast = useToast();
                    toast.error('Failed to update club information');
                    this.loading = false;
                    this.cancelUpdate();
                });
        },

        // Function to delete club
        deleteClub() {
            this.loading = true;

            // Create a club object to send to backend
            const clubObj = {
                clubID: this.clubId,
                removerID: this.memberID
            };

            // Send a post request to delete club
            this.$axios.delete(`${process.env.VUE_APP_API_URL}/club/deleteClub`, { data: clubObj })
                .then((response) => {
                    console.log(response.data);
                    const toast = useToast();
                    toast.success('Club deleted successfully');

                    // Redirect user to browse clubs page
                    this.$router.push('/clubs/view');
                })
                .catch((error) => {
                    console.error(error);
                    const toast = useToast();
                    toast.error('Failed to delete club');
                    this.loading = false;
                });
        },

        // Function to upload images and convert them to base64String
        uploadImage(e) {
            const file = e.target.files[0];
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = (e) => {
                this.localClubInfo.clubBanner = e.target.result;
            }
        },

    },
    mounted() {
    },
};
</script>