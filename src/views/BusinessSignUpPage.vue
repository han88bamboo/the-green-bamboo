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

    <!-- Display when form is being submitted -->
    <div class="text-info-emphasis fst-italic fw-bold fs-5" v-if="submitForm"> 
        <span>The form is being submitted, please hold on!</span>
        <br><br>
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>

    <!-- Display when bottle listing is successfully submitted -->
    <div class="text-success fst-italic fw-bold fs-3"  v-if="successSubmission"> 
        <span>The sign up details has successfully been submitted to our admins for approval!</span> <!-- for user -->
        <br>
        <button class="btn primary-btn btn-sm">
            <router-link :to="{ path: '/login' }" class="primary-clickable-text">
                <span class="fs-5 fst-italic" style="color: white;"> Click to login here! </span>
            </router-link>
        </button>
    </div>
    
    <!-- Display when bottle listing submission encounters an error -->
    <div class="text-danger fst-italic fw-bold fs-3" v-if="errorSubmission"> 
        <span v-if="errorMessage">An error occurred while attempting to send sign up details, please try again!</span>
        <span v-if="duplicateEntry">The sign up details have already been sent.</span>
        <br>
        <button class="btn primary-btn btn-sm" @click="reset">
            <span class="fs-5 fst-italic"> Retry sign up again! </span>
        </button>
    </div>

    <div class="body-login" v-if="dataLoaded">
        <div class="container py-5 mobile-ps-0 mobile-pe-0 mobile-pt-0">

            <div class="rounded px-5 py-2 mobile-px-4" v-if="fillForm" style="background-color: #DDC8A9;">

                <div class="row">

                    <!-- start of the elements -->
                    <div class="col-lg-8 col-md-12" style="background-color:#DDC8A9;">

                        <div class="d-grid gap-2" style="position: relative;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="ms-1 mt-2 bi bi-arrow-left-circle mobile-view-hide" viewBox="0 0 16 16" style="position: absolute; top: 10; left: 0;" v-on:click="goBack">
                                <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-4.5-.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"/>
                            </svg>
                            <p class="fw-bold fs-3 mb-0 mx-5 mt-2 mobile-mx-0 mobile-text-align-left" style="font-style: italic; ">Are you a distiller, brewery or bar owner?</p>
                        </div>

                        <h3 class="text-start my-3">Apply for a Business Account to connect to a community of drink lovers!</h3>


                        <!-- Start of form -->
                        <form v-on:submit.prevent="submitListing" id="frm">

                        
                        <!-- Profile Type -->
                        <!-- Radio for would recommend and would buy again -->
                            <div class='row justify-content-start mb-3 text-start'>
                                <p class="text-start mb-1">Choose Your Profile Type <span style="color: red;">*</span></p>
                                <div class="col-md-12 justify-content-between">
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input" type="radio" id="inlineCheckbox1" v-model="businessType" value="producer" name="business">
                                        <label class="form-check-label text-start fw-bold" for="inlineCheckbox1">Brand/Producer</label>
                                    </div>
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input" type="radio" id="inlineCheckbox2" v-model="businessType" value="venue" name="business">
                                        <label class="form-check-label text-start fw-bold" for="inlineCheckbox2">Venue</label>
                                    </div>                                                                                                   
                                </div>   
                                <span v-if="missingBusinessType" class="text-danger">Please choose your business type.</span>                                      
                            </div>

                        <!-- Input: Username -->
                            <div class="form-group mb-3">
                                <p class="text-start mb-1">Business Name <span style="color: red;">*</span></p>
                                <input type="text" class="form-control" style="border-color: black" v-model="businessName" id="businessName" placeholder="Business Name">
                                <span v-if="missingBusinessName" class="text-danger">Please enter a business name.</span>
                            </div>

                        <!-- Input: Business description -->
                            <div class="form-group mb-3">
                                <p class="text-start mb-1">Business Description <span style="color: red;">*</span></p>
                                <textarea rows=3 class="form-control" style="border-color: black" v-model="businessDesc" id="businessDesc" placeholder="Enter Business Description"></textarea>
                                <span v-if="missingBusinessDesc" class="text-danger">Please enter a business description.</span>
                            </div>

                        <!-- Input: Country of Origin -->
                        <div class="form-group mb-3">
                            <div class=" mb-3">
                                <p class="text-start mb-1">Country of Origin/Location <span style="color: red;">*</span></p>
                                <div class="input-group">
                                    <select class="form-select" id="countrySelect" v-model="selectedCountry" style="border-color: black;">
                                        <option v-for="country in countries" :key="country" :value="country">
                                        {{ country }}
                                        </option>
                                    </select>
                                </div>
                                <span v-if="missingSelectedCountry" class="text-danger">Please choose the country you are based in.</span>
                            </div>
                        </div>



                        
                        <!-- Input: Is business account on the site already, provide link -->
                            <div class="form-group mb-3">
                                <p class="text-start mb-1">Is your brand/venue profile already on the site? If yes, Enter Link:</p>
                                <input type="text" class="form-control" style="border-color: black" v-model="businessLink" id="businessLink" placeholder="Profile Link">
                            </div>


                        <!-- First name and last name -->
                        <div class="row">
                            <!-- Input: First Name -->
                            <div class="form-group mb-3 col-6">
                                <p class="text-start mb-1">First Name <span style="color: red;">*</span></p>
                                <input type="text" class="form-control" style="border-color: black" v-model="firstName" id="firstName" placeholder="First Name">
                                <span v-if="missingFirstName" class="text-danger">Please enter your First Name.</span>
                            </div>
                            <!-- Input: Last Name -->
                            <div class="form-group mb-3 col-6">
                                <p class="text-start mb-1">Last Name <span style="color: red;">*</span></p>
                                <input type="text" class="form-control" style="border-color: black" v-model="lastName" id="lastName" placeholder="Last Name">
                                <span v-if="missingLastName" class="text-danger">Please enter your Last Name.</span>
                            </div>
                        </div>

                        <!-- Input: Is business account on the site already, provide link -->
                        <div class="form-group mb-3">
                            <p class="text-start mb-1">Representative's Relationship to Brand/Venue <span style="color: red;">*</span></p>
                            <input type="text" class="form-control" style="border-color: black" v-model="relationship" id="relationship" placeholder="Relationship">
                            <span v-if="missingRelationship" class="text-danger">Please enter your relationship with the business.</span>
                        </div>

                        <!-- Input: Email -->
                        <div class="form-group mb-3">
                            <p class="text-start mb-1">Email Address (This will be the email tied to the account) <span style="color: red;">*</span></p>
                            <input type="text" class="form-control" style="border-color: black" v-model="email" id="email" placeholder="Email">
                            <span v-if="missingEmail" class="text-danger">Please enter an email.</span>
                            <span v-if="invalidEmail" class="text-danger">Please enter a valid email.</span>
                        </div>

                        <!-- Input: Contact Number -->
                        <div class="form-group mb-3">
                            <p class="text-start mb-1">Contact Number <span style="color: red;">*</span></p>
                            <input type="text" class="form-control" style="border-color: black" v-model="contact" id="contact" placeholder="Contact">
                            <span v-if="missingContact" class="text-danger">Please enter a contact number.</span>
                            <span v-if="invalidContact" class="text-danger">Please enter a valid contact number.</span>
                        </div>

                        <!-- Input Reference Document -->
                        <div class="form-group">
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <p class="text-start my-auto">Upload Reference Document <span style="color: red;">*</span></p>
                                    <div>
                                        <a v-if="fileName" :href="pdfPreview" target="_blank" class="me-2 my-auto" style="font-size: 12px;">
                                            {{ fileName.length > 50 ? fileName.slice(0, 50) + '...' : fileName }}
                                        </a>
                                        <button type="button" class="btn" style="background-color: white; border: 1px solid black; border-radius: 0px;">
                                            <input type="file" id="actual-btn" hidden accept="application/pdf" @change="handleFileSelect"/>
                                            <label for="actual-btn">Upload Document</label>
                                        </button>
                                    </div>
                                </div>
                                <span v-if="missingDocument" class="text-danger">Please upload a reference document.</span>
                            </div>
                            <p class="text-start" style="font-style: italic; font-size: 15px;">Documents should reflect the relevant business name and location details to verify your identity as the company representative. </p>
                        
                        </div>


                        </form>
                    </div>

                    <!-- right side of elements -->
                    <div class="col-lg-4 col-md-12" style="background-color:#DDC8A9;">
                        <div class="d-grid gap-2 mt-3">
                            <p class="fs-3">Subscribe to a Business Account to connect directly with your fans and grow your business.</p>
                        </div>
                        <div class="row justify-content-center mobile-view-hide">
                            <!-- <div class="col-xl-2 col-lg-1 col-md-1"></div> -->
                            <button class="btn rounded p-3 text-start mx-3 mb-3 col-8" @click="toggleMonthlyPricing" :style="{ backgroundColor: selectedMonthlyPricing ? '#DD9E54' :'white', 
                                                                                                                                color: selectedMonthlyPricing ? 'white' :'black', 
                                                                                                                                borderColor: '#DD9E54', 
                                                                                                                                borderWidth:'3px' }">
                                <span>
                                    <h6> <b> Monthly plan </b> </h6>
                                    <p class="m-0"> $65 / Month </p> 
                                    <small class="fst-italic p-0"> Billed monthly </small>
                                    <h6 class="mt-1" style="color: green;"><b>Cancel anytime.</b></h6>
                                </span>
                            </button>
                        </div>
                        <div class="row justify-content-center mobile-view-hide">
                            <!-- <div class="col-xl-2 col-lg-1 col-md-1"></div> -->
                            <button class="btn rounded p-3 text-start mx-3 mb-3 col-8" @click="toggleYearlyPricing" :style="{ backgroundColor: selectedYearlyPricing ? '#DD9E54' :'white', 
                                                                                                                                color: selectedYearlyPricing ? 'white' :'black', 
                                                                                                                                borderColor: '#DD9E54', 
                                                                                                                                borderWidth:'3px' }">
                                <div class="row">
                                    <div class="col-7"> <h6> <b> Yearly plan </b> </h6> </div> 
                                    
                                </div>
                                <span>
                                    <p class="m-0"> $50 / Month </p> 
                                    <small class="fst-italic p-0"> $600 Billed annually </small>
                                    <h6 class="mt-2" style="color: green;"><b>Save 23%!</b></h6>
                                </span>
                            
                            </button>
                        </div>
                        <div class="row justify-content-center mobile-view-show">
                            <button class="btn rounded p-3 text-start mx-0 mb-3 col-6" @click="toggleMonthlyPricing" :style="{ backgroundColor: selectedMonthlyPricing ? '#DD9E54' :'white', 
                                                                                                                                color: selectedMonthlyPricing ? 'white' :'black', 
                                                                                                                                borderColor: '#DD9E54', 
                                                                                                                                borderWidth:'3px' }">
                                <span>
                                    <h6> <b> Monthly plan </b> </h6>
                                    <p class="m-0"> $65 / Month </p> 
                                    <small class="fst-italic p-0"> Billed monthly </small>
                                    <h6 class="mt-2" style="color: green;"><b>Cancel anytime.</b></h6>
                                </span>
                            </button>
                            <button class="btn rounded p-3 text-start mx-0 mb-3 col-6" @click="toggleYearlyPricing" :style="{ backgroundColor: selectedYearlyPricing ? '#DD9E54' :'white', 
                                                                                                                                color: selectedYearlyPricing ? 'white' :'black', 
                                                                                                                                borderColor: '#DD9E54', 
                                                                                                                                borderWidth:'3px' }">
                                <div class="row">
                                    <div class="col-7"> <h6> <b> Yearly plan </b> </h6> </div> 
                                    
                                </div>
                                <span>
                                    <p class="m-0"> $50 / Month </p> 
                                    <small class="fst-italic p-0"> $600 Billed annually </small>
                                    <h5 class="mt-2" style="color: green;"><b>Save 23%!</b></h5>
                                </span>
                            
                            </button>
                        </div>    
                        <span v-if="missingPlan" class="text-danger">Please select a plan.</span>
                    </div>

                </div>

                <div class="row">
                    <div class="col-lg-8 col-md-12">
                        <button type="submit" class="btn btn-lg secondary-btn-border-thick mx-auto mb-3" @click="signUp">Register for Account</button>
                    </div>
                </div>


            </div>
            
        </div>
    </div>

</template>

<!-- ------------------------------------------------------------------------------ -->

<script>
    // import components used
    import NavBar from '@/components/NavBar.vue';

    export default{
        name: 'BusinessSignUpPage',
        components: {
            NavBar
        },
        data(){
            return{
                dataLoaded:false,
                fillForm:true,
                submitForm:false,
                successSubmission:false,
                errorSubmission:false,
                errorMessage:false,
                duplicateEntry:false,

                // Form validation
                missingBusinessDesc:false,
                missingBusinessName:false,
                missingBusinessType:false,
                missingEmail:false,
                invalidEmail:false,
                missingContact:false,
                invalidContact:false,
                missingFirstName:false,
                missingLastName:false,
                missingRelationship:false,
                missingSelectedCountry:false,
                missingPlan:false,
                missingDocument:false,

                // form variables
                businessType:'',
                businessName:'',
                businessDesc:'',
                businessLink:'',
                firstName:'',
                lastName:'',
                email:'',
                contact:'',
                relationship:'',
                selectedCountry:'',
                countries: [],
                fileName:'',
                selectedFile: null,
                pdfPreview: null,
                pdfBase64:'',
                selectedMonthlyPricing:false,
                selectedYearlyPricing:false,
                selectedPricing:'',

            }
        },
        created() {
            let accountDetails = this.$route.query
            this.businessType = accountDetails.businessType
            this.businessName = accountDetails.businessName
            this.businessDesc = accountDetails.businessDesc
            this.businessLink = accountDetails.businessLink
            this.selectedCountry = accountDetails.originCountry
        },
        mounted(){
            this.loadData()
        },
        methods:{
            toggleYearlyPricing(){
                if(this.selectedMonthlyPricing && !this.selectedYearlyPricing){
                    this.selectedMonthlyPricing= false
                }
                if(this.selectedYearlyPricing){
                    this.selectedYearlyPricing=false
                }else{
                    this.selectedYearlyPricing = true
                }
            },
            toggleMonthlyPricing(){
                if(this.selectedYearlyPricing && ! this.selectedMonthlyPricing){
                    this.selectedYearlyPricing= false
                }
                if(this.selectedMonthlyPricing){
                    this.selectedMonthlyPricing=false
                }else{
                    this.selectedMonthlyPricing = true
                }
            },
            async loadData(){
                try {
                    const response = await this.$axios.get('http://127.0.0.1:5000/getData/getCountries');
                    for (let country of response.data) {
                        this.countries.push(country.originCountry);
                    }
                    this.countries = this.countries.sort();
                    this.dataLoaded = true;
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
            },
            handleFileSelect(event){
                const file = event.target.files[0];

                if (file && file.type === "application/pdf") {
                    this.fileName = file.name
                    this.pdfPreview = URL.createObjectURL(file);

                    // convert to base64
                    this.selectedFile = file;

                    const reader = new FileReader();
                    reader.onload = (e) => {
                        this.pdfBase64 = e.target.result; // Assigns Base64 string to pdfBase64
                        this.pdfBase64 = this.pdfBase64.split('data:application/pdf;base64,')[1];
                    };
                    reader.readAsDataURL(this.selectedFile);


                } else {
                    this.pdfPreview = null;
                }
            },

            goBack(){
                this.$router.go(-1)
            },

            signUp(){
                this.resetError()
                this.selectedPricing=''

                let errorCount =0
                // Form validation

                // Business desc check
                if(this.businessDesc == ''){
                    this.missingBusinessDesc = true
                    errorCount++
                }
                // Business name check
                if(this.businessName == ''){
                    this.missingBusinessName = true
                    errorCount++
                }
                // Business type check
                if(this.businessType == ''){
                    this.missingBusinessType = true
                    errorCount++
                }
                // Select country check
                if(this.selectedCountry==''){
                    this.missingSelectedCountry = true
                    errorCount++
                }
                // Brand relationship check
                if(this.relationship==''){
                    this.missingRelationship = true
                    errorCount++
                }
                // Pricing select check
                if(!(this.selectedMonthlyPricing || this.selectedYearlyPricing)){
                    this.missingPlan=true
                    errorCount++
                }else if(this.selectedMonthlyPricing){
                    this.selectedPricing = 'monthly'
                }else{
                    this.selectedPricing = 'yearly'
                }

                // Email validation
                if(this.email==''){
                    this.missingEmail = true
                    errorCount++
                }else if(!this.email.match('.+@.+..+')){
                    this.invalidEmail = true
                    errorCount++
                }

                // Contact validation
                if(this.contact==''){
                    this.missingContact = true
                    errorCount++
                }else if(!this.contact.match(/^\+?\d+$/)){
                    this.invalidContact = true
                    errorCount++
                }

                // First name validation
                if(this.firstName == ''){
                    this.missingFirstName = true
                    errorCount++
                }

                // Last name validation
                if(this.lastName == ''){
                    this.missingLastName = true
                    errorCount++
                }

                // Document validation
                if(this.pdfPreview == null){
                    this.missingDocument = true
                    errorCount++
                }

                if(errorCount>0){
                    return null
                }

                let joinDate = new Date().toISOString();
                let submitAPI =  "http://127.0.0.1:5000/createAccount/createAccountRequest"
                let submitData = {
                    "businessName": this.businessName,
                    "businessType": this.businessType,
                    "businessDesc": this.businessDesc,
                    "country": this.selectedCountry,
                    "pricing": this.selectedPricing,
                    "businessLink": this.businessLink,
                    "firstName": this.firstName,
                    "lastName": this.lastName,
                    "relationship": this.relationship,
                    "email": this.email,
                    "contact": this.contact,
                    "referenceDocument": this.pdfBase64,
                    "photo": "",
                    "joinDate": joinDate,
                    "isPending": true,
                    "isApproved": false,
                    "isNew": true
                }
                this.createAccount(submitAPI,submitData)
            },

            async createAccount(submitAPI,submitData){
                this.submitForm = true
                this.fillForm = false
                try{
                    const response = await this.$axios.post(submitAPI, submitData)
                    .then((response)=>{
                        this.reviewResponseCode = response.data.code
                    })
                    .catch((error)=>{
                        console.log(error);
                        this.reviewResponseCode = error.response.data.code
                        this.submitForm = false
                    });
                    if(this.reviewResponseCode==201){
                        this.successSubmission=true; // Display success message
                        this.submitForm = false  // Hide submission in progress message
                    }else{
                        this.errorSubmission=true; // Display error message
                        this.submitForm = false  // Hide submission in progress message
    
                        if(this.reviewResponseCode==400){
                            this.duplicateEntry = true // Display duplicate entry message
                        }else{
                            this.errorMessage = true // Display generic error message
                        }
                    }
                    return response
                }
                catch(error){
                    console.log(error)
                    this.errorSubmission = true
                    this.errorMessage = true
                    this.submitForm = false
                }
            },

            reset(){
                this.fillForm = true
                this.errorMessage=false
                this.errorSubmission=false
                this.duplicateEntry=false
                this.successSubmission=false
                this.submitForm = false
            },
            resetError(){
                this.missingBusinessDesc=false
                this.missingBusinessName=false
                this.missingBusinessType=false
                this.missingEmail=false
                this.invalidEmail=false
                this.missingContact=false
                this.invalidContact=false
                this.missingFirstName=false
                this.missingLastName=false
                this.missingRelationship=false
                this.missingSelectedCountry=false
                this.missingPlan=false
                this.missingDocument=false
            },
        },
    }

</script>