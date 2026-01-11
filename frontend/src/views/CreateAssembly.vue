<template>
    <div>
        <NavBar />

        <!-- Main Content -->
        <div class="container mt-5 mb-5">
            <div class="row">

                <!-- Column 1: Create assembly form -->
                <div class="col-md-9 text-start">

                    <!-- Header -->
                    <h3 class="fw-bold">Create your assembly</h3>

                    <!-- Error Alert -->
                    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                        <strong>Error:</strong> {{ error }}
                        <button type="button" class="btn-close" @click="error = null" aria-label="Close"></button>
                    </div>

                    <!-- Form -->
                    <form @submit.prevent="createAssembly">

                        <!-- Assembly name -->
                        <div class="mb-3">
                            <label for="name" class="form-label">Your Assembly Name <span class="text-danger">*</span></label>
                            <input 
                                type="text" 
                                class="form-control" 
                                :class="{ 'is-invalid': nameError }"
                                id="name" 
                                v-model="assembly.assemblyName" 
                                @input="validateName"
                                maxlength="50"
                                placeholder="Enter assembly name (4-50 characters)"
                                required
                            >
                            <div v-if="nameError" class="invalid-feedback">{{ nameError }}</div>
                            <small class="text-muted">{{ assembly.assemblyName.length }}/50 characters</small>
                        </div>

                        <!-- Assembly description -->
                        <div class="mb-3">
                            <label for="description" class="form-label">Your Assembly Description <span class="text-danger">*</span></label>
                            <textarea 
                                class="form-control" 
                                :class="{ 'is-invalid': descError }"
                                id="description" 
                                v-model="assembly.assemblyDesc" 
                                @input="validateDesc"
                                maxlength="500"
                                rows="4"
                                placeholder="Describe what your assembly is about..."
                                required
                            ></textarea>
                            <div v-if="descError" class="invalid-feedback">{{ descError }}</div>
                            <small class="text-muted" :class="{ 'text-danger': assembly.assemblyDesc.length > 450 }">
                                {{ assembly.assemblyDesc.length }}/500 characters
                            </small>
                        </div>

                        <!-- Drink Types Selection (Multiple) -->
                        <div class="mb-3">
                            <label class="form-label">Drink Types (optional)</label>
                            <p class="text-muted small mb-2">Select the drink categories this assembly focuses on. You can select multiple.</p>
                            
                            <!-- Loading state for drink types -->
                            <div v-if="loadingDrinkTypes" class="text-muted">
                                <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                                Loading drink types...
                            </div>
                            
                            <!-- Drink types checkboxes (pill-style) -->
                            <div v-else class="d-flex flex-wrap gap-2">
                                <div 
                                    v-for="drinkType in drinkTypesList" 
                                    :key="drinkType.drinkType"
                                    class="drink-type-pill"
                                    :class="{ 'selected': assembly.drinkTypes.includes(drinkType.drinkType) }"
                                    @click="toggleDrinkType(drinkType.drinkType)"
                                >
                                    {{ drinkType.drinkType }}
                                </div>
                            </div>
                            
                            <!-- Selected drink types display -->
                            <div v-if="assembly.drinkTypes.length > 0" class="mt-2">
                                <small class="text-success">
                                    <i class="bi bi-check-circle me-1"></i>
                                    Selected: {{ assembly.drinkTypes.join(', ') }}
                                </small>
                            </div>
                        </div>

                        <!-- Assembly banner -->
                        <div class="mb-3">
                            <label for="banner" class="form-label">Upload Your Assembly Banner (optional)</label>
                            <input 
                                type="file" 
                                class="form-control" 
                                id="banner" 
                                @change="uploadImage" 
                                accept="image/*"
                            >

                            <!-- Preview of the banner -->
                            <div v-if="assembly.assemblyBanner" class="mt-3">
                                <img 
                                    :src="assembly.assemblyBanner" 
                                    alt="Banner Preview" 
                                    class="img-fluid rounded" 
                                    style="max-height: 300px;"
                                >
                                <!-- Remove banner button -->
                                <button type="button" class="btn btn-danger ms-3" @click="removeImage">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                                        <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0"/>
                                    </svg>
                                </button>
                            </div>
                        </div>

                        <!-- Make assembly private/invite-only (always public for now - checkbox hidden) -->
                        <!-- <div class="mb-3">
                            <input type="checkbox" class="me-3" v-model="assembly.isInviteOnly"> Make Your Assembly Invite-Only
                        </div> -->
                    </form>
                </div>

                <!-- Column 2: Invite friends section -->
                <div class="col-md-3 text-start">

                    <!-- Header -->
                    <h5 class="fw-bold">Invite Friends (optional)</h5>
                    <p>Note: You can only invite friends who you are already following.</p>

                    <!-- Search bar -->
                    <div class="input-group mb-3 position-relative">
                        <input 
                            type="text" 
                            class="form-control rounded" 
                            placeholder="Search for your friends" 
                            aria-label="Search for friends" 
                            v-model="searchQuery" 
                            @input="searchFriend"
                        >
                        <!-- Search Icon -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" 
                            class="bi bi-search position-absolute" viewBox="0 0 16 16" 
                            style="right: 10px; top: 50%; transform: translateY(-50%); cursor: pointer; z-index: 5;">
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
                
                    <!-- List of selected friends (icons of their profile photo) -->
                    <h6 v-if="friendsToInvite.length > 0" class="fw-bold">Selected Friends</h6>
                    <div v-if="friendsToInvite.length > 0" class="d-flex flex-wrap">
                        <div v-for="id in friendsToInvite" :key="id" class="me-2 mb-2 position-relative">
                            <!-- Details of each friend -->
                            <div class="d-flex flex-column align-items-center">
                                <!-- Display the profile photo of the friend, if available, else use a default profile pic -->
                                <img v-if="friends[id] && friends[id].photo" :src="friends[id].photo" class="rounded-circle" style="width: 50px; height: 50px; object-fit: cover;" alt="profile-photo">
                                <svg v-else xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                                    <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                                    <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                                </svg>

                                <!-- Name of friend -->
                                <p class="text-center small mt-1" style="max-width: 60px; word-wrap: break-word;">
                                    {{ friends[id] ? friends[id].displayName : 'Unknown' }}
                                </p>
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

            <!-- Create assembly button -->
            <div class="d-flex justify-content-end mt-3">
                <button 
                    type="submit" 
                    class="btn btn-primary" 
                    :disabled="loading || !isFormValid" 
                    @click="createAssembly"
                >
                    <span v-if="!loading">Create Assembly</span>
                    <div v-else class="spinner-border spinner-border-sm" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </button>
            </div>
        </div>
        
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import { useToast } from "vue-toastification";

export default {
    name: "CreateAssembly",
    components: {
        NavBar
    },
    data() {
        return {
            // User ID and user type
            userID: "",
            userType: "",

            // Assembly object to store the assembly details
            assembly: {
                assemblyName: "",
                assemblyDesc: "",
                drinkTypes: [], // Array of selected drink types
                isInviteOnly: false,
                assemblyBanner: null
            },

            // Validation errors
            nameError: null,
            descError: null,

            // Drink types from database
            drinkTypesList: [],
            loadingDrinkTypes: false,

            // Dictionary to store the friends the user is following
            friends: {},
            errorFriendList: "",

            // Variables for searching friends
            searchQuery: "",

            // List of friends to be invited
            friendsToInvite: [],

            // Variable to show loading spinner
            loading: false,

            // General error message
            error: null
        }
    },
    computed: {
        // Check if form is valid
        isFormValid() {
            const nameValid = this.assembly.assemblyName.trim().length >= 4 && 
                              this.assembly.assemblyName.trim().length <= 50 && 
                              !this.nameError;
            const descValid = this.assembly.assemblyDesc.trim().length > 0 && 
                              this.assembly.assemblyDesc.length <= 500;
            return nameValid && descValid;
        },

        // Function to search for friends
        searchResults() {
            if (this.searchQuery) {
                let query = this.searchQuery.toLowerCase();
                let results = {};

                for (const [id, friend] of Object.entries(this.friends)) {
                    // Skip if already invited
                    if (this.friendsToInvite.includes(id)) {
                        continue;
                    }

                    // Check if the display name contains the search query
                    if (friend.displayName && friend.displayName.toLowerCase().includes(query)) {
                        results[id] = friend;
                    }
                }
                return results;
            } else {
                return {};
            }
        }
    },
    methods: {
        // Slugify text for URL
        slugify(text) {
            return text
                .toString()
                .toLowerCase()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '')
                .replace(/\s+/g, '-')
                .replace(/[^\w-]/g, '');
        },

        // Validate assembly name
        validateName() {
            const name = this.assembly.assemblyName.trim();
            
            if (name.length < 4) {
                this.nameError = 'Assembly name must be at least 4 characters.';
            } else if (name.length > 50) {
                this.nameError = 'Assembly name cannot exceed 50 characters.';
            } else {
                // Allow letters, numbers, spaces, emojis, and common punctuation
                // Backend will do thorough validation on submit
                this.nameError = null;
            }
        },

        // Validate description
        validateDesc() {
            if (this.assembly.assemblyDesc.length > 500) {
                this.descError = 'Description cannot exceed 500 characters.';
            } else {
                this.descError = null;
            }
        },

        // Toggle drink type selection
        toggleDrinkType(drinkType) {
            const index = this.assembly.drinkTypes.indexOf(drinkType);
            if (index > -1) {
                // Remove if already selected
                this.assembly.drinkTypes.splice(index, 1);
            } else {
                // Add if not selected
                this.assembly.drinkTypes.push(drinkType);
            }
        },

        // Get drink types from database
        async getDrinkTypes() {
            this.loadingDrinkTypes = true;
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getDrinkTypes`
                );
                // API returns array directly, not wrapped in { drinkTypes: [...] }
                this.drinkTypesList = response.data || [];
            } catch (error) {
                console.error('Error fetching drink types:', error);
                // Don't show error - drink types are optional
            } finally {
                this.loadingDrinkTypes = false;
            }
        },

        // Get list of friends the user is following
        async getFriends() {
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getUserFollowList/${this.userID}`
                );
                this.friends = response.data.followList?.users || {};
            } catch (error) {
                console.error('Error fetching friends:', error);
                this.errorFriendList = "Failed to fetch the list of friends. Please try again later.";
            }
        },

        // Add friend to invite list
        addFriend(friendID) {
            if (!this.friendsToInvite.includes(friendID)) {
                this.friendsToInvite.push(friendID);
            }
            this.searchQuery = "";
        },

        // Remove friend from invite list
        removeFriend(friendID) {
            const index = this.friendsToInvite.indexOf(friendID);
            if (index > -1) {
                this.friendsToInvite.splice(index, 1);
            }
        },

        // Search for friends (just triggers computed property)
        searchFriend() {
            // Computed property handles the search
        },

        // Create the assembly
        async createAssembly() {
            // Clear previous error
            this.error = null;

            // Validate form
            this.validateName();
            this.validateDesc();

            if (!this.isFormValid) {
                this.error = 'Please fill in all required fields correctly.';
                return;
            }

            // Format invited friends as array of {userID, userType} objects
            // This allows the backend to properly create invitations in assemblyInvites table
            const formattedInvites = this.friendsToInvite.map(friendID => ({
                userID: friendID,
                userType: 'user' // Friends from follow list are always users
            }));

            // Create the assembly object
            const assemblyObj = {
                creatorID: this.userID,
                creatorType: this.userType,
                assemblyName: this.assembly.assemblyName.trim(),
                assemblyDesc: this.assembly.assemblyDesc.trim(),
                drinkTypes: this.assembly.drinkTypes,
                invitedFriends: formattedInvites
            };

            // Add banner image if uploaded
            if (this.assembly.assemblyBanner) {
                assemblyObj.image64 = this.assembly.assemblyBanner;
            }

            this.loading = true;

            try {
                const response = await this.$axios.post(
                    `${process.env.VUE_APP_API_URL}/assembly/createAssembly`,
                    assemblyObj
                );

                if (response.data.code === 201) {
                    const toast = useToast();
                    toast.success('Assembly created successfully!');

                    // TODO: Update this redirect to go to SpecificAssembly page once that endpoint is ready
                    // Currently redirecting to BrowseAssemblies because getSpecificAssemblyInfo endpoint is not yet built
                    // Future: this.$router.push(`/assemblies/${response.data.data.assemblyID}/${this.slugify(this.assembly.assemblyName)}`);
                    this.$router.push('/assemblies');
                } else {
                    // Handle validation errors from backend
                    this.error = response.data.message || 'Failed to create assembly. Please try again.';
                }
            } catch (error) {
                console.error('Error creating assembly:', error);
                if (error.response && error.response.data && error.response.data.message) {
                    this.error = error.response.data.message;
                } else {
                    this.error = 'Failed to create assembly. Please try again later.';
                }
            } finally {
                this.loading = false;
            }
        },

        // Upload image and convert to base64
        uploadImage(e) {
            const file = e.target.files && e.target.files[0];
            if (!file) {
                console.warn("No file selected.");
                return;
            }
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = (e) => {
                this.assembly.assemblyBanner = e.target.result;
            };
        },

        // Remove the image and reset the input field
        removeImage() {
            this.assembly.assemblyBanner = null;
            document.getElementById("banner").value = "";
        }
    },
    mounted() {
        // Get user ID and type from local storage
        this.userID = localStorage.getItem("88B_accID");
        this.userType = localStorage.getItem("88B_accType");

        // Redirect if not logged in
        if (!this.userID) {
            const toast = useToast();
            toast.error('Please log in to create an assembly.');
            this.$router.push('/assemblies');
            return;
        }

        // Load drink types
        this.getDrinkTypes();

        // Get friends list (only for users)
        if (this.userType === "user") {
            this.getFriends();
        }
    }
}
</script>

<style scoped>
.drink-type-pill {
    padding: 8px 16px;
    border: 2px solid #dee2e6;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    background-color: #fff;
    font-size: 14px;
}

.drink-type-pill:hover {
    border-color: #0d6efd;
    background-color: #f8f9fa;
}

.drink-type-pill.selected {
    border-color: #0d6efd;
    background-color: #0d6efd;
    color: white;
}

.btn-primary {
    background-color: #0d6efd;
    border-color: #0d6efd;
}

.btn-primary:disabled {
    background-color: #6c757d;
    border-color: #6c757d;
    cursor: not-allowed;
}
</style>
