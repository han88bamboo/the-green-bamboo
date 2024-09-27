<!-- Admin can access this page to handle admin controls. -->

<template>
    <NavBar />
    
    <!-- Display when data is still loading -->
    <div class="text-info-emphasis fst-italic fw-bold fs-5 pt-5" v-if="dataLoaded == false">
        <span>Loading page, please wait...</span>
        <br><br>
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>

    <!-- Display when data fails to load -->
    <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="dataLoaded == null"> 
        <span>An error occurred while loading this page, please try again!</span>
        <br>
        <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
            <span class="fs-5 fst-italic"> Return to previous page </span>
        </button>
        <router-link :to="'/'" class="mx-1">
            <button class="btn primary-btn btn-sm">
                <span class="fs-5 fst-italic"> Go to Home page </span>
            </button>
        </router-link>
    </div>

    <div v-if="!importSuccess && dataLoaded" class="container mt-5 mb-5">

            
            
            <div>
                <div class="form-group mb-2" >
                    <h1>Bulk Import Listings</h1>

                    <h3 class="mt-5"> 
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">
                            <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5"/>
                            <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708z"/>
                        </svg>
                        Download Listings Import Template 
                    </h3>
                    <button type="button" class="btn secondary-btn-less-round"  @click="downloadCSV()"> Download Template </button>

                    <h3 class="mt-5"> 
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-upload" viewBox="0 0 16 16">
                            <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5"/>
                            <path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708z"/>
                        </svg>
                        Upload Listings CSV File 
                    </h3>
                    <div class="row align-items-center my-3">
                        <div class="col-3"></div>
                        <div class="col-6"> 
                            <input type="file" name="file" id="csvFile" accept=".csv" @change="handleFileUpload" class="form-control">
                        </div>
                        <div class="col-3"></div>
                    </div>

                    <button v-if="csvFile" type="button" class="btn primary-btn-less-round" @click="importCSV">Import</button>
                    <button v-else type="button" class="btn primary-btn-less-round" disabled>Import</button>

                    
                </div>

                <!-- TO CHECK -->
            </div>
        </div>

        <div v-if="importSuccess && dataLoaded" class="container mt-5 mb-5">

            <h1 class="text-success">Import Success</h1>

            <button type="button" class="btn primary-btn-less-round me-2" @click="moreImports">Import more listings</button>

            <router-link :to="'/'" class="btn secondary-btn-less-round ms-2">
                Back to home
            </router-link>


        </div>

        

</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    // import { hashPassword } from '../../../backend/other/hashPassword.js'

        export default {
            name: 'adminDashboard',
            components: {
                NavBar
            },
            data() {
                return {
                    dataLoaded: false,

                    // csv data
                    fileFormat: [],
                    csvData: [],

                    // TO DELETE IF NOT NEEDED

                    // // data from database
                    // observationTags: [],
                    // modRequests: [],
                    // accountRequests: [],
                    // producers: [],
                    // venues: [],
                    // countries: [],

                    // editedObservationTags: [],
                    // pendingModRequests: [],
                    // pendingAccountRequests: [],
                    
                    // //User 
                    // user: null,
                    // users: [],

                    // // creation of new observation tag
                    // newObservation:'',

                    // // Error messages
                    // errorMessages:'',

                    // // flags
                    // dataLoaded: false,
                    // loadError: false,
                    // editingObservation:false,
                    // addingObservation:false,
                    // selectingObservation:true,
                    // nothingChanged:false,
                    // successUpdateObservation:false,
                    // invalidTag:false,
                    // errorMessage:false,
                    // errorUpdateObservation:false,
                    // updatingObservation:false,
                    // duplicateTag:false,
                    // successCreateObservation:false,
                    // submittingObservation:false,
                    // errorCreateObservation:false,

                    // // create business
                    // businessType: "",
                    // businessName: "",
                    // businessDesc: "",
                    // businessCountry: "",
                    // businessClaimStatus: "",
                    // addBizError: "",
                    // tempPassword: "",


                    // Logged in user details
                    userID: null,
                    userType: localStorage.getItem('88B_accType'),

                    
                    // csv file import
                    csvFile: null,
                    importSuccess: false,
                    responseCode :0,

                }
            },
            mounted() {
                // Check if user is logged in
                this.userID = localStorage.getItem('88B_accID');

                if (this.userID == null) {
                    this.$router.push('/login');
                }
                else {
                    this.loadData();
                }
            },
            methods: {
                async loadData(){

                    // csv
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/adminFunctions/readCSV');
                        this.fileFormat = response.data.data;
                        this.convertToCSV();
                    }
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }

                    // Check if admin, if not reroute to home page
                    // users
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getUsers');
                        this.users = response.data;
                        if (this.userType == "user") {
                            this.user = this.users.find(user => user["id"] == this.userID);
                            if(!this.user.isAdmin){
                                this.$router.push('/');
                            }
                        }else{
                            this.$router.push('/');
                        }
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                    // observation tags
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getObservationTags');
                        this.observationTags = response.data;
                        this.editedObservationTags = JSON.parse(JSON.stringify(response.data));
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                    // mod requests
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getModRequests');
                        this.modRequests = response.data;
                        this.pendingModRequests = this.modRequests.filter(request => request.reviewStatus);
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                    // account requests
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getAccountRequests');
                        this.accountRequests = response.data;
                        this.pendingAccountRequests = this.accountRequests.filter(request => request.reviewStatus);
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                    // producer
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getProducers');
                        this.producers = response.data;
                        // check for producer with no producer name and retrieve id
                        // [TO BE REMOVED?]
                        for (let i = 0; i < this.producers.length; i++) {
                            if (!this.producers[i].producerName) {
                                console.log("no name");
                                console.log(this.producers[i].id);
                            }
                        }
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                    // venues
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getVenues');
                        this.venues = response.data;
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                    // countries
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getCountries');
                        this.countries = response.data;
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }

                    // Set data loaded to true
                    if (this.dataLoaded != null) {
                        this.dataLoaded = true;
                    }
                },

                // To recognise which csv file is to be imported
                async handleFileUpload(event) {
                    this.csvFile = event.target.files[0];
                },


                // Calling of backend to import csv file
                async importCSV() {
                    console.log(this.csvFile)
                    
                    if (this.csvFile != []) {
                        const formData = new FormData();
                    formData.append('file', this.csvFile);
                    
                        try {
                            const response = await this.$axios.post('http://127.0.0.1:5000/adminFunctions/importListings', 
                                formData, {
                                headers: {
                                    'Content-Type': 'multipart/form-data'
                                }
                            })
                            .then((response)=>{
                            this.responseCode = response.data.code
                            if(this.responseCode == 201){
                            this.importSuccess=true; // Display success message
                            }else{
                                this.importSuccess = false
                            }
                            })
                            .catch((error)=>{
                                console.error(error);
                                this.responseCode = error.response.data.code
                                
                            });
                            
                            
                        return response
                        } catch (error) {
                            console.error('Error:', error);
                        }
                    }
                },

                // To import more listings
                moreImports(){
                    this.importSuccess = false
                    this.csvFile = []
                },

                convertToCSV() {
                    let keepColumns = this.fileFormat.filter(item => Object.values(item).some(value => value !== ''));

                    this.csvData = keepColumns.map(column => {
                        return { value: column };
                    });
                },

                downloadCSV() {
                    let csvContent = "data:text/csv;charset=utf-8,";

                    this.csvData.forEach(row => {
                        csvContent += row.value + "\n";
                    });

                    const encodedUri = encodeURI(csvContent);
                    const link = document.createElement("a");
                    link.setAttribute("href", encodedUri);
                    link.setAttribute("download", "listingsFormat.csv");
                    document.body.appendChild(link);
                    link.click();
                }

                
            }
        }
</script>