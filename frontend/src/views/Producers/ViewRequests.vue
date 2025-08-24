<!-- Users can access this page to view requests of bottle listings that they have previously submitted. -->
<!-- Producers can access this page to view requests of bottle listings that have them specified as the producer. -->
<!-- Moderators can access this page to view user-submitted requests of bottle listings related to their drink type(s). -->
<!-- Admins can access this page to view user-submitted requests of ALL bottle listings. -->

<template>
    <NavBar />
    <!-- Header -->
    <div class="container pt-3">
        
        <!-- Display when data is being loaded -->
        <div class="text-info-emphasis fst-italic fw-bold fs-5" v-if="!dataLoaded"> 
            <span>Currently loading data, please hold on!</span>
            <br><br>
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        
        <!-- Display when data loading encounters an error -->
        <div class="text-danger fst-italic fw-bold fs-3" v-if="loadError"> 
            <span>An error occurred while loading data, please try refreshing the page!</span>
            <br>
            <button class="btn primary-btn btn-sm" @click="()=>{this.$router.go(0)}">
                <span class="fs-5 fst-italic"> Refresh Page </span>
            </button>
        </div>

        <!-- Display requests after data loaded -->
        <div v-if="dataLoaded && !loadError">

            <!-- Form Title -->
            <div class="col-12">
                <div class="d-grid gap-2">
                    <p class="fw-bold fs-1 m-0">View Bottle Listing Requests</p>
                </div>
            </div>

            <!-- Navtab Buttons-->
            <hr>
            <!-- Navtab to toggle between requests -->
            <nav class="pb-0">
                <div class="nav nav-tabs justify-content-center" id="nav-tab" role="tablist">
                    <!-- New Listing Requests -->
                    <button class="nav-link active flex-grow-1" id="nav-listing-request-tab" data-bs-toggle="tab" data-bs-target="#nav-listing-request" type="button" role="tab" aria-controls="nav-listing-request" aria-selected="true"> 
                        <span class="d-flex align-items-center justify-content-center mb-0">
                            New Listing Requests
                            <span class="rounded-circle mx-3 d-flex align-items-center justify-content-center"> 
                                <p class="m-0">{{ requestListings.length }}</p>
                            </span> 
                        </span>
                    </button>
                    <!-- Listing Edit Requests -->
                    <button class="nav-link flex-grow-1" id="nav-listing-edit-tab" data-bs-toggle="tab" data-bs-target="#nav-listing-edit" type="button" role="tab" aria-controls="nav-listing-edit" aria-selected="false">
                        <span class="d-flex align-items-center justify-content-center mb-0">
                            Listing Edit Requests
                            <span class="rounded-circle mx-3 d-flex align-items-center justify-content-center"> 
                                <p class="m-0">{{ requestEdits.length }}</p>
                            </span> 
                        </span>
                    </button>
                    <!-- Duplicate Reports -->
                    <button class="nav-link flex-grow-1" id="nav-duplicate-reports-tab" data-bs-toggle="tab" data-bs-target="#nav-duplicate-reports" type="button" role="tab" aria-controls="nav-duplicate-reports" aria-selected="false">
                        <span class="d-flex align-items-center justify-content-center mb-0">
                            Duplicate Reports
                            <span class="rounded-circle mx-3 d-flex align-items-center justify-content-center"> 
                                <p class="m-0">{{ requestDupes.length }}</p>
                            </span> 
                        </span>
                    </button>
                </div>
            </nav>
            
            <!-- Navtab Content -->
            <div class="container tab-content" id="nav-tabContent">

                <!-- Tab 1: Display New Listing Requests -->
                <div class="row tab-pane fade show active" id="nav-listing-request" role="tabpanel" aria-labelledby="nav-listing-request-tab">
                    <div class="row">
                        <hr> 
                        <p class="fw-bold fst-italic fs-4 m-0" v-if="requestListings.length > 0">Viewing: New Listing Requests</p>
                        <p class="fw-bold fst-italic fs-4 m-0" v-else>No New Listing Requests!</p>
                        <div class="col-xxl-2 col-lg-3 col-md-4 col-sm-6 col-12 my-1 px-1" v-for="requestNew in requestListings" :key="requestNew.id">
                            <div class="card border-warning h-100">
                                <div class="card-header">
                                    New Listing
                                </div>
                                <!-- <img :src="'data:image/jpeg;base64,' + (requestNew['photo'] || defaultPhoto)" class="card-img-top p-2 img-thumbnail" style="object-fit: cover;"> -->
                                <img :src="(requestNew['photo'] || defaultPhoto)" class="card-img-top p-2 img-thumbnail" style="object-fit: cover;">
                                <div class="card-body">
                                    <h5 class="card-title">{{ requestNew['listingName'] }}</h5>
                                </div>
                                <ul class="list-group list-group-flush text-start">
                                    <li class="list-group-item" v-if="requestNew['bottler'] != 'OB'"><span class="fw-bold">Bottler: </span>{{ requestNew['bottler'] }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Producer: </span>{{ requestNew['producerName'] }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Type: </span>{{ requestNew['drinkType'] }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Requested By: </span>{{ requestNew["requesterUsername"] }}</li>
                                </ul>
                                <div class="card-footer">
                                    <router-link v-if="role == 'producer' || isAdmin || types.includes(requestNew['drinkType'])" :to="{ path: '/listing/create/' + requestNew.id }">
                                        <button class="border btn btn-warning btn-sm align-bottom">Review Request</button>
                                    </router-link>
                                    <router-link v-if="role == 'user' && requestNew['userID'] == accID" :to="{ path: '/request/new/' + requestNew.id }">
                                        <button class="border btn btn-warning btn-sm align-bottom">Modify Request</button>
                                    </router-link>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Tab 2: Display Listing Edit Requests -->
                <div class="row tab-pane fade show" id="nav-listing-edit" role="tabpanel" aria-labelledby="nav-listing-edit-tab">
                    <div class="row">
                        <hr>
                        <p class="fw-bold fst-italic fs-4 m-0" v-if="requestEdits.length > 0">Viewing: Listing Edit Requests</p>
                        <p class="fw-bold fst-italic fs-4 m-0" v-else>No Listing Edit Requests!</p>
                        <div class="col-xxl-2 col-lg-3 col-md-4 col-sm-6 col-12 my-1 px-1" v-for="requestEdit in requestEdits" :key="requestEdit.id">
                            <div class="card border-secondary h-100">
                                <div class="card-header">
                                    Listing Edit
                                </div>
                                <!-- <img :src="'data:image/jpeg;base64,' + (requestEdit['photo'] || defaultPhoto)" class="card-img-top p-2 img-thumbnail" style="object-fit: cover;"> -->
                                <img :src="(requestEdit['photo'] || defaultPhoto)" class="card-img-top p-2 img-thumbnail" style="object-fit: cover;">
                                <div class="card-body">
                                    <h5 class="card-title">{{ requestEdit['listingName'] }}</h5>
                                </div>
                                <ul class="list-group list-group-flush text-start">
                                    <li class="list-group-item" v-if="requestEdit['sourceLink']"><span class="fw-bold">Source Link: </span>{{ requestEdit['sourceLink'] }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Producer: </span>{{ requestEdit['producerName'] }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Brand Relation: </span>{{ requestEdit['brandRelation'] }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Requested By: </span>{{ requestEdit["requesterUsername"] }}</li>
                                </ul>
                                <div class="card-footer">
                                    <router-link v-if="role == 'producer' || isAdmin || types.includes(requestEdit['drinkType'])" :to="{ path: '/listing/edit/' + requestEdit.listingID + '/' + requestEdit.id }">
                                        <button class="border btn btn-secondary btn-sm align-bottom">Review Request</button>
                                    </router-link>
                                    <router-link v-if="role == 'user' && requestEdit['userID'] == accID" :to="{ path: '/request/modify/edit/' + requestEdit.listingID + '/' + requestEdit.id }">
                                        <button class="border btn btn-secondary btn-sm align-bottom">Modify Request</button>
                                    </router-link>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Tab 3: Display Duplicate Reports -->
                <div class="tab-pane fade show" id="nav-duplicate-reports" role="tabpanel" aria-labelledby="nav-duplicate-reports-tab">
                    <div class="row">
                        <hr>
                        <p class="fw-bold fst-italic fs-4 m-0" v-if="requestDupes.length > 0">Viewing: Duplicate Reports</p>
                        <p class="fw-bold fst-italic fs-4 m-0" v-else>No Duplicate Reports!</p>
                        <div class="col-xxl-2 col-lg-3 col-md-4 col-sm-6 col-12 my-1 px-1" v-for="requestDupe in requestDupes" :key="requestDupe.id">
                            <div class="card border-dark h-100">
                                <div class="card-header">
                                    Duplicate Report
                                </div>
                                <!-- <img :src="'data:image/jpeg;base64,' + (requestDupe['photo'] || defaultPhoto)" class="card-img-top p-2 img-thumbnail" style="object-fit: cover;"> -->
                                <img :src="(requestDupe['photo'] || defaultPhoto)" class="card-img-top p-2 img-thumbnail" style="object-fit: cover;">
                                <div class="card-body">
                                    <h5 class="card-title">{{ requestDupe['listingName'] }}</h5>
                                </div>
                                <ul class="list-group list-group-flush text-start">
                                    <li class="list-group-item" v-if="requestDupe['duplicateLink']"><span class="fw-bold">Duplicate Link: </span>{{ requestDupe['duplicateLink'] }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Producer: </span>{{ requestDupe['producerName'] }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Brand Relation: </span>{{ requestDupe['brandRelation'] }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Requested By: </span>{{ requestDupe["requesterUsername"] }}</li>
                                </ul>
                                <div class="card-footer">
                                    <router-link v-if="role == 'producer' || isAdmin || types.includes(requestDupe['drinkType'])" :to="{ path: '/listing/edit/' + requestDupe.listingID + '/' + requestDupe.id }">
                                        <button class="border btn btn-dark btn-sm align-bottom">Review Request</button>
                                    </router-link>
                                    <router-link v-if="role == 'user' && requestDupe['userID'] == accID" :to="{ path: '/request/modify/duplicate/' + requestDupe.listingID + '/' + requestDupe.id }">
                                        <button class="border btn btn-dark btn-sm align-bottom">Modify Request</button>
                                    </router-link>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

        </div>
    </div>
</template>

<script>
    import NavBar from '@/components/NavBar.vue';

        export default {
            name: 'RequestListingNew',
            components: {
                NavBar
            },
            data() {
                return {
                    // data from database
                    requestListings: [],
                    requestEdits: [],
                    requestDupes: [],

                    // flags
                    dataLoaded: false,
                    loadError: false,
                    accID: localStorage.getItem('88B_accID'),
                    role: localStorage.getItem('88B_accType'),
                    isAdmin: localStorage.getItem('88B_accType') === 'admin', // Add this line
                    types: [],
                    // Default Photo
                    defaultPhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",
                }
            },
            mounted() {
                if (this.accID == null) {
                    this.$router.push('/login');
                }
                else {
                    this.loadData();
                }
            },
            methods: {
                // load data from database
                async loadData() {
                    console.log("========== ViewRequests.vue loadData() ==========");
                    console.log(`Loading data for user type: ${this.role} with ID: ${this.accID}`);
    
                // First, fetch user data to check actual admin status
                    try {
                        console.log("Fetching user data to check admin status...");
                        const userResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUser/${this.accID}`);
                        console.log("User data response:", userResponse);
                        
                        // Update admin status based on database value
                        if (userResponse.data && userResponse.data.isAdmin) {
                            console.log("User has admin privileges in database, setting isAdmin = true");
                            this.isAdmin = true;
                        }
                        
                        // If user is a moderator, load their drink types
                        if (userResponse.data && userResponse.data.modType) {
                            console.log("User is a moderator for drink types:", userResponse.data.modType);
                            this.types = userResponse.data.modType;
                        }
                    } catch (error) {
                        console.error("Error fetching user data:", error);
                    }
                    
                    // Request Listings
                    try {
                        console.log("Fetching request listings data...");
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getRequestListingsByRole/${this.role}/${this.accID}`);
                        console.log("Request listings API URL:", response);

                        this.requestListings = response.data
                        console.log("component data loaded successfully");
                    } 
                    catch (error) {
                        console.error("ERROR LOADING REQUEST LISTINGS:",error);
                        this.loadError = true;
                    }
                    // Request Edits
                    try {
                        console.log("loading request edits");
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getRequestEditsByRole/${this.role}/${this.accID}`);
                        console.log("Request edits API URL:", response);

                        if ('requestEdits' in response.data) {
                            console.log(`Loaded ${response.data.requestEdits.length} request edits`);
                            this.requestEdits = response.data['requestEdits'];
                            console.log(`Loaded ${response.data.requestDups.length} request duplicates`);
                            this.requestDupes = response.data['requestDups'];
                        }
                    } 
                    catch (error) {
                        console.error("ERROR LOADING REQUEST EDITS:",error);
                        this.loadError = true;
                    }

                    this.dataLoaded = true;
                },
            }
        }
</script>