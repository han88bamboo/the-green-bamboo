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
                        <div class="col-xxl-2 col-lg-3 col-md-4 col-sm-6 col-12 my-1 px-1" v-for="requestNew in requestListings" :key="requestNew._id">
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
                                    <li class="list-group-item"><span class="fw-bold">Producer: </span>{{ findProducer(requestNew) }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Type: </span>{{ requestNew['drinkType'] }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Requested By: </span>{{ findUser(requestNew["userID"]["$oid"]) }}</li>
                                </ul>
                                <div class="card-footer">
                                    <router-link v-if="role == 'producer' || isAdmin || types.includes(requestNew['drinkType'])" :to="{ path: '/listing/create/' + requestNew._id['$oid'] }">
                                        <button class="border btn btn-warning btn-sm align-bottom">Review Request</button>
                                    </router-link>
                                    <router-link v-if="role == 'user' && requestNew['userID']['$oid'] == accID" :to="{ path: '/request/new/' + requestNew._id['$oid'] }">
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
                        <div class="col-xxl-2 col-lg-3 col-md-4 col-sm-6 col-12 my-1 px-1" v-for="requestEdit in requestEdits" :key="requestEdit._id">
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
                                    <li class="list-group-item"><span class="fw-bold">Producer: </span>{{ findProducer(requestEdit) }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Brand Relation: </span>{{ requestEdit['brandRelation'] }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Requested By: </span>{{ findUser(requestEdit["userID"]["$oid"]) }}</li>
                                </ul>
                                <div class="card-footer">
                                    <router-link v-if="role == 'producer' || isAdmin || types.includes(requestEdit['drinkType'])" :to="{ path: '/listing/edit/' + requestEdit.listingID['$oid'] + '/' + requestEdit._id['$oid'] }">
                                        <button class="border btn btn-secondary btn-sm align-bottom">Review Request</button>
                                    </router-link>
                                    <router-link v-if="role == 'user' && requestEdit['userID']['$oid'] == accID" :to="{ path: '/request/modify/edit/' + requestEdit.listingID['$oid'] + '/' + requestEdit._id['$oid'] }">
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
                        <div class="col-xxl-2 col-lg-3 col-md-4 col-sm-6 col-12 my-1 px-1" v-for="requestDupe in requestDupes" :key="requestDupe._id">
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
                                    <li class="list-group-item"><span class="fw-bold">Producer: </span>{{ findProducer(requestDupe) }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Brand Relation: </span>{{ requestDupe['brandRelation'] }}</li>
                                    <li class="list-group-item"><span class="fw-bold">Requested By: </span>{{ findUser(requestDupe["userID"]["$oid"]) }}</li>
                                </ul>
                                <div class="card-footer">
                                    <router-link v-if="role == 'producer' || isAdmin || types.includes(requestDupe['drinkType'])" :to="{ path: '/listing/edit/' + requestDupe.listingID['$oid'] + '/' + requestDupe._id['$oid'] }">
                                        <button class="border btn btn-dark btn-sm align-bottom">Review Request</button>
                                    </router-link>
                                    <router-link v-if="role == 'user' && requestDupe['userID']['$oid'] == accID" :to="{ path: '/request/modify/duplicate/' + requestDupe.listingID['$oid'] + '/' + requestDupe._id['$oid'] }">
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
                    listings: [],
                    producers: [],
                    users: [],
                    requestListings: [],
                    requestEdits: [],
                    requestDupes: [],

                    // user info
                    user: null,
                    isAdmin: false, 
                    isModerator: false,

                    // flags
                    dataLoaded: false,
                    loadError: false,
                    accID: null,
                    role: localStorage.getItem('88B_accType'),
                    types: [],
                    // Default Photo
                    defaultPhoto: "https://drinkximages.s3.us-east-1.amazonaws.com/images/2d4d94bc-313e-4621-9a15-4bfbf77958de.jpg",
                }
            },
            mounted() {
                // Check if user is logged in
                this.accID = localStorage.getItem('88B_accID');

                if (this.accID == null) {
                    this.$router.push('/login');
                }
                else {
                    this.loadData();
                }
            },
            methods: {
                // find producer name from producer ID
                findProducer(request) {
                    const producerID = request["producerID"]["$oid"];
                    const producer = this.producers.find((producer) => {
                        return producer["_id"]["$oid"] == producerID;
                    });
                    if (producer == undefined) {
                        return request["producerNew"];
                    }
                    return producer["producerName"];
                },

                // find user name from user ID
                findUser(userID) {
                    const user = this.users.find((user) => {
                        return user["_id"]["$oid"] == userID;
                    });
                    if (user == undefined) {
                        const producer = this.producers.find((producer) => {
                            return producer["_id"]["$oid"] == userID;
                        });
                        if (producer != undefined) {
                            return producer["producerName"];
                        }
                        return "(Anonymous)";
                    }
                    return user["username"];
                },

                // load data from database
                async loadData() {
                    // Listings
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getListings');
                        this.listings = response.data;
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }
                    // Producers
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getProducers');
                        this.producers = response.data;
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }
                    // Users
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getUsers');
                        this.users = response.data;

                        if (this.role == 'user') {
                            this.types = this.users.find((user) => {
                                return user["_id"]["$oid"] == this.accID;
                            }).modType;
                        }
                        this.user = this.users.find(user => user._id.$oid == this.accID)
                        if (this.user) {
                            // check if user is an admin
                            if (this.user.isAdmin) {
                                this.isAdmin = true
                            }
                            // if user is not admin, check if user is a moderator
                            else if (this.user.isModerator) {
                                this.isModerator = true
                            }
                        }
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }
                    // Request Listings
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getRequestListings');

                        // Filter requests based on user role
                        if (this.role == 'producer') {
                            this.requestListings = response.data.filter((request) => {
                                return request["reviewStatus"] == false && request["producerID"]["$oid"] == this.accID;
                            })
                        }
                        else if (this.role == 'user') {
                            if (this.isAdmin) {
                                this.requestListings = response.data.filter((request) => {
                                    return request["reviewStatus"] == false;
                                })
                            } else {
                                this.requestListings = response.data.filter((request) => {
                                    return request["reviewStatus"] == false && (request["userID"]["$oid"] == this.accID || this.types.includes(request["drinkType"]));
                                })
                            }
                        }
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }
                    // Request Edits
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getRequestEdits');
                        let unreviewedRequests = response.data.filter((request) => {
                            return request["reviewStatus"] == false;
                        });

                        // Obtain listing data for each request
                        for (let request of unreviewedRequests) {
                            let targetListing = this.listings.find((listing) => {
                                return listing["_id"]["$oid"] == request["listingID"]["$oid"];
                            });
                            if (targetListing == undefined) {
                                continue;
                            }

                            request['photo'] = targetListing['photo'];
                            request['listingName'] = targetListing['listingName'];
                            request['producerID'] = targetListing['producerID'];

                            if (request['duplicateLink']) {
                                this.requestDupes.push(request);
                            } else {
                                this.requestEdits.push(request);
                            }
                        }

                        // Filter requests based on user role
                        if (this.role == 'producer') {
                            this.requestEdits = this.requestEdits.filter((request) => {
                                return request["producerID"]["$oid"] == this.accID;
                            })
                            this.requestDupes = this.requestDupes.filter((request) => {
                                return request["producerID"]["$oid"] == this.accID;
                            })
                        }
                        else if (this.role == 'user' && !this.isAdmin) {
                            this.requestEdits = this.requestEdits.filter((request) => {
                                return request["userID"]["$oid"] == this.accID || this.types.includes(request["drinkType"]);
                            })
                            this.requestDupes = this.requestDupes.filter((request) => {
                                return request["userID"]["$oid"] == this.accID || this.types.includes(request["drinkType"]);
                            })
                        }
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }

                    this.dataLoaded = true;
                }
            }
        }
</script>