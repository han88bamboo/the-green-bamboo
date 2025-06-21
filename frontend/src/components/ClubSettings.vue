<template>
    <div class="container mb-3 text-start">

        <!-- Back Button to return to club view page -->
        <button class="btn hover-underline fs-5 p-0" style="cursor: pointer;" @click="backToClub">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="32" fill="currentColor" class="bi bi-arrow-left" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8"/>
            </svg>
            Back to Club Page
        </button>

        <!-- Club Information Section -->
        <div class="row mt-3">

            <!-- Row 1: Club setting title and edit buttons -->
            <div class="row d-flex justify-content-between align-items-center">

                <!-- Column 1: Club setting title -->
                <div class="col-auto">
                    <h3 class="fw-bold">Club Settings</h3>
                </div>

                <!-- Column 2: Edit / Save button -->
                <div class="col-auto pe-0">
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
                <input type="text" class="form-control ms-2 md-ms-0" id="clubName" v-model="localClubInfo.clubName" :disabled="!editMode">
            </div>

            <!-- Row 3: Club Description -->
            <div class="row mt-3">
                <label for="clubDescription" class="form-label">Club Description</label>
                <textarea class="form-control ms-2 md-ms-0" id="clubDescription" rows="3" v-model="localClubInfo.clubDescription" :disabled="!editMode"></textarea>
            </div>

            <!-- Row 4: Club Banner -->
            <div class="row mt-3">
                <label for="clubBanner" class="form-label">Club Banner</label>
                <!-- Show current Banner -->
                <img v-if="clubInfo.clubBanner !=''" :src="clubInfo.clubBanner" alt="Club Banner" class="img-thumbnail ms-2 md-ms-0" style="max-width: 200px;">
                <img v-else :src="defaultBanner" alt="Default Banner" class="img-thumbnail ms-2 md-ms-0" style="max-width: 200px;">
                <input v-if="editMode" type="file" class="form-control mt-3 ms-2 md-ms-0" id="clubBanner" accept="image/*" @change="uploadImage" :disabled="!editMode"> 
            </div>

            <!-- Row 5: Is Invite Only -->
            <div class="row mt-3">
                <label for="isInviteOnly" class="form-label">Group Type</label>
                <div class="form-check d-flex align-items-center">
                    <input type="checkbox" class="form-check-input ms-2 md-ms-0 me-2" id="isInviteOnly" v-model="localClubInfo.isInviteOnly" :disabled="!editMode" style="cursor: pointer;">
                    <label for="isInviteOnly" class="form-check-label">Is Invite Only</label>
                </div>
            </div>

        </div>

        <!-- Horizontal line divider to seperate sections -->
        <hr>

        <!-- Manage Members Section -->
        <div class="row mt-3">

            <!-- Row 6: -->
            <div class="row d-flex justify-content-between align-items-center">

                <!-- Column 1: Manage Members Title -->
                <div class="col-auto d-flex">
                    <h4 class="fw-bold"> Manage Members ({{ numMembers }})</h4>
                </div>

                <!-- Column 2: Edit / Save button -->
                <div class="col-auto">
                    <button v-if="!manageMode" class="btn btn-primary" @click="manageMode = true">
                        Manage
                    </button>
                    <button v-if="manageMode" class="btn btn-primary" @click="manageMode = false">
                        Done
                    </button>
                </div>
                
            </div>

            <!-- Row 7: Table of club members -->
            <table class="table table-striped ms-2 md-ms-0 mt-3" >
                <thead>
                    <tr>
                        <th scope="col">Member Photo</th>
                        <th scope="col">Member Name</th>
                        <th scope="col">Role</th>
                        <th scope="col">Data Joined</th>
                        <th scope="col" v-if="manageMode">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="member in paginatedMembers" :key="member.id">
                        <!-- Column 1: Photo -->
                        <td>
                            <img v-if="member.photo" :src="member.photo" class="rounded-circle" style="width: 50px; height: 50px;" alt="profile-photo">
                            <svg v-else xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                                <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                                <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                            </svg>
                        </td>
                        <!-- Column 2: Name -->
                        <td>
                            <span v-if="member.displayName">{{ member.displayName }}</span>
                            <span v-if="member.producerName">{{ member.producerName }}</span>
                            <span v-else>{{ member.venueName }}</span>
                        </td>
                        <!-- Column 3: Role -->
                        <td>
                            <span v-if="member.isAdmin">Admin</span>
                            <span v-else>Member</span>
                        </td>
                        <!-- Column 4: Date joined -->
                        <td>{{ member.joinDate }}</td>
                        <!-- Column 5: Action Buttons -->
                        <td v-if="manageMode">
                            <button v-if="!member.isAdmin && member.joinStatus" class="btn btn-primary me-3" style="cursor: pointer;" data-bs-toggle="modal" data-bs-target="#makeAdminModal" @click="selectedMemberMakeAdmin = member">
                                Make Admin
                            </button>
                            <button v-if="member.memberID != memberID && member.isAdmin" class="btn btn-primary me-3" style="cursor: pointer;" @click="revokeAdmin(member.memberID)">
                                Revoke Admin
                            </button>
                            <button v-if="member.memberID != memberID" class="btn btn-danger" style="cursor: pointer;" data-bs-toggle="modal" data-bs-target="#removeMemberModal" @click="selectedMemberRemove = member">
                                Remove
                            </button>
                        </td>

                    </tr>
                </tbody>
            </table>

            <!-- Pagination Controls for members table -->
            <nav>
                <ul class="pagination justify-content-center mt-3">
                    <!-- << -->
                    <li class="page-item" :class="{ disabled: currentMemberTablePage === 1 }">
                        <button class="page-link" @click="goToMemberPage(currentMemberTablePage - 1)" aria-label="Previous">
                            &laquo;
                        </button>
                    </li>
                    <!-- Page numbers -->
                    <li v-for="page in totalMemberPages" :key="page" class="page-item" :class="{ active: page === currentMemberTablePage }">
                        <button class="page-link" @click="goToMemberPage(page)">{{ page }}</button>
                    </li>
                    <!-- >> -->
                    <li class="page-item" :class="{ disabled: currentMemberTablePage === totalMemberPages }">
                        <button class="page-link" @click="goToMemberPage(currentMemberTablePage + 1)" aria-label="Next">
                            &raquo;
                        </button>
                    </li>
                </ul>
            </nav>

            <!-- Make admin modal -->
            <div class="modal fade" id="makeAdminModal" tabindex="-1" aria-labelledby="makeAdminModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="makeAdminModalLabel">Make Admin</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            Are you sure you want to make this member an admin of the club? This will grant this member admin privileges to manage the club.
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn" data-bs-dismiss="modal" :disabled="loading">Close</button>
                            <button v-if="!loading" type="button" class="btn btn-primary" @click="makeAdmin(selectedMemberMakeAdmin.memberID)" :disabled="loading" data-bs-dismiss="modal">Make Admin</button>
                            <button v-if="loading" class="btn btn-primary" disabled>
                                <div class="spinner-border  spinner-border-sm" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Remove member modal -->
            <div class="modal fade" id="removeMemberModal" tabindex="-1" aria-labelledby="removeMemberModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="removeMemberModalLabel">Remove Member</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            Are you sure you want to remove this member from the club? This will also remove all posts and comments made by the member.
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn" data-bs-dismiss="modal" :disabled="loading">Close</button>
                            <button v-if="!loading" type="button" class="btn btn-danger" @click="removeMember" :disabled="loading" data-bs-dismiss="modal">Remove</button>
                            <button v-if="loading" class="btn btn-primary" disabled>
                                <div class="spinner-border  spinner-border-sm" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Error message if fail to retrieve member list -->
            <p v-if="errorMessage" class="text-danger ms-2 md-ms-0">
                {{ errorMessage }}
            </p>
        </div>

        <!-- Horizontal line divider to seperate sections -->
        <hr>

        <!-- Invited Member Section -->
        <div class="row mt-3">
            <h4 class="fw-bold"> Club Member Invites ({{ invitedMembers.length }}) </h4>
            <p>Users who have been invited but has yet to accept the invite.</p>

            <table v-if="invitedMembers.length > 0" class="table table-striped mt-3 ms-2 md-ms-0">
                <thead>
                    <tr>
                        <th scope="col">Member Photo</th>
                        <th scope="col">Member Name</th>
                        <th scope="col">Date Invited</th>
                        <th scope="col">Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="member in invitedMembers" :key="member.memberID">
                        <!-- Column 1: Photo -->
                        <td>
                            <img v-if="member.photo" :src="member.photo" class="rounded-circle" style="width: 50px; height: 50px;" alt="profile-photo">
                            <svg v-else xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                                <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                                <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                            </svg>
                        </td>
                        <!-- Column2: Name -->
                        <td>{{ member.displayName }}</td>
                        <!-- Column3: Date Invited -->
                        <td>{{ member.inviteDate }}</td>
                        <!-- Column4: Status -->
                        <td>Pending</td>
                    </tr>
                </tbody>

            </table>

            <!-- Pagination Controls for member invite table -->
            <nav v-if="invitedMembers.length > 0">
                <ul class="pagination justify-content-center mt-3">
                    <!-- << -->
                    <li class="page-item" :class="{ disabled: currentInvitedTablePage === 1 }">
                        <button class="page-link" @click="goToInvitedPage(currentInvitedTablePage - 1)" aria-label="Previous">
                            &laquo;
                        </button>
                    </li>
                    <!-- Page numbers -->
                    <li v-for="page in totalRequestPages" :key="page" class="page-item" :class="{ active: page === currentRequestTablePage }">
                        <button class="page-link" @click="goToInvitedPage(page)">{{ page }}</button>
                    </li>
                    <!-- >> -->
                    <li class="page-item" :class="{ disabled: currentInvitedTablePage === totalRequestPages }">
                        <button class="page-link" @click="goTogoToInvitedPageRequestPage(currentInvitedTablePage + 1)" aria-label="Next">
                            &raquo;
                        </button>
                    </li>
                </ul>
            </nav>
        </div>


        <!-- Horizontal line divider to seperate sections -->
        <hr>

        <!-- Club Member Request Section--> <!-- If club is private, this section will show, which displays a list of users who have requested to join this club -->
        <div class="row mt-3">
            <!-- Row 8: Club Member Request Title -->
            <h4 class="fw-bold"> Club Member Requests ({{ totalRequest }}) </h4>
            <p>Will only receive request if the club is Invite Only or there are pending request.</p>

            <!-- Row 9: Table of club member requests -->
            <table v-if="requests.length > 0" class="table table-striped mt-3 ms-2 md-ms-0">
                <thead>
                    <tr>
                        <th scope="col">Member Photo</th>
                        <th scope="col">Member Name</th>
                        <th scope="col">Date Requested</th>
                        <th scope="col">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in paginatedRequsts" :key="request.userID">
                        <!-- Column 1: Photo -->
                        <td>
                            <img v-if="request.photo" :src="request.photo" class="rounded-circle" style="width: 50px; height: 50px;" alt="profile-photo">
                            <svg v-else xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                                <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                                <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                            </svg>
                        </td>
                        <!-- Column 2: Name -->
                        <td>{{ request.displayName }}</td>
                        <!-- Column 3: Date Requested -->
                        <td>{{ request.requestDate }}</td>
                        <!-- Column 4: Action Buttons -->
                        <td>
                            <button class="btn btn-primary me-3" style="cursor: pointer;" @click="acceptRequest(request.userID, request.userType)">
                                Accept
                            </button>
                            <button class="btn btn-danger" style="cursor: pointer;" @click="rejectRequest(request.userID, request.userType)">
                                Reject
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <!-- Pagination Controls for member request table -->
            <nav v-if="requests.length > 0">
                <ul class="pagination justify-content-center mt-3">
                    <!-- << -->
                    <li class="page-item" :class="{ disabled: currentRequestTablePage === 1 }">
                        <button class="page-link" @click="goToRequestPage(currentRequestTablePage - 1)" aria-label="Previous">
                            &laquo;
                        </button>
                    </li>
                    <!-- Page numbers -->
                    <li v-for="page in totalRequestPages" :key="page" class="page-item" :class="{ active: page === currentRequestTablePage }">
                        <button class="page-link" @click="goToRequestPage(page)">{{ page }}</button>
                    </li>
                    <!-- >> -->
                    <li class="page-item" :class="{ disabled: currentRequestTablePage === totalRequestPages }">
                        <button class="page-link" @click="goToRequestPage(currentRequestTablePage + 1)" aria-label="Next">
                            &raquo;
                        </button>
                    </li>
                </ul>
            </nav>

            <p v-else class="ms-2 md-ms-0 ps-0">
                No member requests to join this club
            </p>

            <!-- Error message if fail to retrieve member request list -->
            <p v-if="requestListError" class="text-danger ms-2 md-ms-0">
                {{ requestListError }}
            </p>
        </div>

        <!-- Horizontal line divider to seperate sections -->
        <hr>

        <!-- Delete club Section -->
        <div class="row mt-3">
            <h4 class="fw-bold"> Delete Club </h4>
            <p class="ps-1 ms-2 md-ms-0"><span class="text-danger fw-bold">Warning:</span> This action is irreversible. Deleting the club will remove all posts and comments from the database.</p>
            <button class=" col-3 btn btn-danger ms-2 md-ms-0" data-bs-toggle="modal" data-bs-target="#deleteClubModal" style="cursor: pointer;">
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
        },
        numMembers: {
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
            manageMode: false,

            // Variables to store club members (current member and invited members)
            members: [],
            currentMemberTablePage: 1, // Tracks the current member table page the user is on
            pageSizeMembers: 1, // Determine number of members to show per member table page (value here should be the same as LIMIT VALUE IN THE BACKEND)
            errorMessage: '', // Variable for error message if fail to retrieve member list

            // Variables to store invited members
            invitedMembers: [],
            currentInvitedTablePage: 1, // Tracks the current invited member table page the user is on
            pageSizeInvited: 1, // Determine number of invited members to show per invited member table page (value here should be the same as LIMIT VALUE IN THE BACKEND)
            invitedListError: '', // Variable for error message if fail to retrieve invited member list

            // Variable to store request to join club
            requests: [],
            totalRequest: null,
            currentRequestTablePage: 1, // Tracks the current request table page the user is on
            pageSizeRequests: 1, // Determine number of requests to show per request table page (value here should be the same as LIMIT VALUE IN THE BACKEND)
            requestListError: '', // Variable for error message if fail to retrieve member request list
            
            // Variable to store member information for granting admin status
            selectedMemberMakeAdmin: {},

            // Variable to store member information for removing member
            selectedMemberRemove: {}
        };
    },
    computed: {
        paginatedMembers() {
            const start = (this.currentMemberTablePage - 1) * this.pageSizeMembers;
            return this.members.slice(start, start + this.pageSizeMembers);
        },
        paginatedRequsts() {
            const start = (this.currentRequestTablePage - 1) * this.pageSizeRequests;
            return this.requests.slice(start, start + this.pageSizeRequests);
        },
        totalMemberPages() {
            return Math.ceil(this.numMembers / this.pageSizeMembers);
        },
        totalRequestPages() {
            return Math.ceil(this.totalRequest / this.pageSizeRequests);
        }
    },
    methods: {
        // Functions to load page data start ========================================
        // Function to get club members
        async getClubMembers() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getClubMembers/${this.clubId}/0`);
                this.members = response.data.members;
            } catch (error) {
                console.error(error);
                if (error.response.status != 404) {
                    this.errorMessage = 'Failed to retrieve club member requests';
                } 
            }
        },

        // Function to get the next page of club members
        async getNextMemberTablePage() {
            try {
                let latestMemberID = this.members[this.members.length - 1].memberID;
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getClubMembers/${this.clubId}/${latestMemberID}`);
                this.members = this.members.concat(response.data.members);
            } catch (error) {
                console.error(error);
                if (error.response.status != 404) {
                    this.errorMessage = 'Failed to retrieve club members';
                }
            }
        },

        // Function to get invited members
        async getInvitedMembers() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getInvitedMembers/${this.clubId}/0`);
                this.invitedMembers = response.data.invitedMembers;
            } catch (error) {
                console.error(error);
                if (error.response.status != 404) {
                    this.errorMessage = 'Failed to retrieve invited members';
                }
            }
        },

        // Function to get the next page of invited members
        async getNextInvitedTablePage() {
            try {
                let latestMemberID = this.invitedMembers[this.invitedMembers.length - 1].memberID;
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getInvitedMembers/${this.clubId}/${latestMemberID}`);
                this.invitedMembers = this.invitedMembers.concat(response.data.invitedMembers);
            } catch (error) {
                console.error(error);
                if (error.response.status != 404) {
                    this.errorMessage = 'Failed to retrieve invited members';
                }
            }
        },

        // Function to get club member requests (when the page first loads)
        async getClubRequests() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getClubRequests/${this.clubId}/0`);
                this.requests = response.data.requests;
                this.totalRequest = response.data.totalRequests;
            } catch (error) {
                console.error(error);
                if (error.response.status != 404) {
                    this.requestListError = 'Failed to retrieve club member requests';
                }
            }
        },

        // Function to get the next page of club member requests
        async getNextRequestTablePage() {
            try {
                let latestRequestID = this.requests[this.requests.length - 1].requestID;
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/club/getClubRequests/${this.clubId}/${latestRequestID}`);
                this.requests = this.requests.concat(response.data.requests);
            } catch (error) {
                if (error.response.status != 404) {
                    this.requestListError = 'Failed to retrieve club member requests';
                }
            }
        },
        // Functions to load page data end ==========================================

        // Functions for user interaction start **************************************
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

                    // Exit settings page by refreshing the page
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);

                })
                .catch((error) => {
                    console.error(error);
                    const toast = useToast();
                    toast.error('Failed to update club information');
                    this.loading = false;
                    this.cancelUpdate();
                });
        },

        // Function to go to a specific member table page
        goToMemberPage(page) {
            this.getNextMemberTablePage();
            this.currentMemberTablePage = page;
        },

        // Function to go to a specific invited member table page
        goToInvitedPage(page) {
            this.getNextInvitedTablePage();
            this.currentInvitedTablePage = page;
        },

        // Function to go to a specific request table page
        goToRequestPage(page) {
            this.getNextRequestTablePage();
            this.currentRequestTablePage = page;
            
        },

        // Function to make member an admin
        makeAdmin(memberID) {

            this.loading = true;

            this.$axios.put(`${process.env.VUE_APP_API_URL}/club/makeAdmin`, { 
                    clubID: this.clubId, 
                    memberID: memberID,
                    adminID: this.memberID
                })
                .then((response) => {
                    console.log(response.data);
                    const toast = useToast();
                    toast.success('Member promoted to admin');
                    this.getClubMembers();
                })
                .catch((error) => {
                    console.error(error);
                    const toast = useToast();
                    toast.error('Failed to promote member to admin');
                });

            this.loading = false;
        },

        // Function to revoke admin status 
        revokeAdmin(memberID) {
            this.$axios.put(`${process.env.VUE_APP_API_URL}/club/revokeAdmin`, { 
                    clubID: this.clubId, 
                    memberID: memberID,
                    adminID: this.memberID
                })
                .then((response) => {
                    console.log(response.data);
                    const toast = useToast();
                    toast.success('Admin status revoked');
                    this.getClubMembers();
                })
                .catch((error) => {
                    console.error(error);
                    const toast = useToast();
                    toast.error('Failed to revoke admin status');
                });
        },

        // Function to remove member 
        removeMember() {
            this.loading = true;

            // Create a club object to send to backend
            const clubObj = {
                clubID: this.clubId,
                members: [this.selectedMemberRemove.memberID],
                removerID: this.memberID
            };

            // Send a post request to remove member
            this.$axios.delete(`${process.env.VUE_APP_API_URL}/club/removeMembers`, { data: clubObj })
                .then((response) => {
                    console.log(response.data);
                    const toast = useToast();
                    toast.success('Member removed successfully');
                    this.getClubMembers();
                    this.loading = false;
                })
                .catch((error) => {
                    console.error(error);
                    const toast = useToast();
                    toast.error('Failed to remove member');
                    this.loading = false;
                });
        },

        // Function to accept member request
        acceptRequest(requesterID, userType) {
            this.$axios.post(`${process.env.VUE_APP_API_URL}/club/acceptClubRequest`, { 
                    clubID: this.clubId, 
                    requesterID: requesterID,
                    userType: userType,
                    adminID: this.memberID
                })
                .then((response) => {
                    console.log(response.data);
                    const toast = useToast();
                    toast.success('Member request accepted');
                    this.getClubMembers();
                    this.getClubRequests();
                })
                .catch((error) => {
                    console.error(error);
                    const toast = useToast();
                    toast.error('Failed to accept member request');
                });
        },

        // Function to reject member request
        rejectRequest(requesterID, userType) {
            this.$axios.delete(`${process.env.VUE_APP_API_URL}/club/rejectClubRequests`, { 
                data: {
                    clubID: this.clubId, 
                    requesterID: requesterID,
                    userType: userType,
                    adminID: this.memberID
                     }
                })
                .then((response) => {
                    console.log(response.data);
                    const toast = useToast();
                    toast.success('Member request rejected');
                    this.getClubRequests();
                })
                .catch((error) => {
                    console.error(error);
                    const toast = useToast();
                    toast.error('Failed to reject member request');
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
        // Functions for user interaction end **************************************

        // Helper functions start ===================================================
        // Function to upload images and convert them to base64String
        uploadImage(e) {
            const file = e.target.files[0];
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = (e) => {
                this.localClubInfo.clubBanner = e.target.result;
            }
        },
        // Helper functions end =====================================================

    },
    mounted() {
        this.getClubMembers();
        this.getClubRequests();
    },
};
</script>