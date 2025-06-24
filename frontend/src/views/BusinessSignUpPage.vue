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
    <div class="text-danger fst-italic fw-bold fs-5 pt-5" v-if="dataLoaded == null"> 
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
    <div class="text-success fst-italic fw-bold fs-5"  v-if="successSubmission"> 
        <span>The sign up details has successfully been submitted to our admins for approval!</span> <!-- for user -->
        <br>
        <button class="btn primary-btn btn-sm">
            <router-link :to="{ path: '/login' }" class="primary-clickable-text">
                <span class="fs-5 fst-italic" style="color: white;"> Click to login here! </span>
            </router-link>
        </button>
    </div>
    
    <!-- Display when bottle listing submission encounters an error -->
    <div class="text-danger fst-italic fw-bold fs-5" v-if="errorSubmission"> 
        <span v-if="errorMessage">An error occurred while attempting to send sign up details, please try again!</span>
        <span v-if="duplicateEntry">The sign up details have already been sent.</span>
        <br>
        <button class="btn primary-btn btn-sm" @click="reset">
            <span class="fs-5 fst-italic"> Retry sign up again! </span>
        </button>
    </div>
    <div class="login-header-banner mobile-view-show">
      <img src="@/assets/business-signup.jpg" alt="Banner" />
    </div>
    <div class="body-login background-login" v-if="dataLoaded">
        <div class="container py-5 mobile-ps-0 mobile-pe-0 mobile-pt-0">

            <div class="rounded px-5 py-2 mobile-px-4" v-if="fillForm" style="background-color: wheat; opacity:0.95;">

                <div class="row">

                    <!-- start of the elements -->
                    <div class="col-lg-8 col-md-12" style="background-color:wheat;">

                        <div class="d-grid gap-1" style="position: relative;">
                            <p class="fw-bold fs-4 pt-4 mobile-fs-5 mb-1 text-start" style="font-style: italic; ">
                                <span @click="goBack" style="cursor: pointer; font-size: 1.5rem;" class="mobile-view-hide">↩</span> Are you a brand or venue owner?
                            </p>
                        </div>
                        <h5 class="text-start mt-2 mb-3 mobile-fs-6">Apply for a Business Account to connect to a community of drink lovers and grow your business!</h5>
                        <div class="container p-0 mt-3 mb-4">
                        
                        <div class="feature-table">
                            <div class="row feature-row align-items-center py-2">
                                <div class="col-9 text-start fw-bold">
                                    Feature
                                </div>
                                <div class="col-3 text-center fw-bold">
                                    Drink-X for Business
                                </div>
                            </div>
                            <!-- Feature Row 1 -->
                            <div class="row feature-row align-items-center py-2">
                                <div class="col-9 text-start">
                                    Be instantly found by numerous drinks lovers searching for venues, brands or their next favourite drink.
                                </div>
                                <div class="col-3 text-center">
                                    <i class="bi bi-check-circle-fill" style="color: #3CB371; font-size: 1.2rem;"></i>
                                </div>
                            </div>
                            
                            <!-- Feature Row 2 -->
                            <div class="row feature-row align-items-center py-2">
                                <div class="col-9 text-start">
                                    Showcase your offerings/menu on a live, easy-to-update menu.
                                </div>
                                <div class="col-3 text-center">
                                    <i class="bi bi-check-circle-fill" style="color: #3CB371; font-size: 1.2rem;"></i>
                                </div>
                            </div>
                            
                            <!-- Feature Row 3 -->
                            <div class="row feature-row align-items-center py-2">
                                <div class="col-9 text-start">
                                    Announce promotions and brand news directly to your fans.
                                </div>
                                <div class="col-3 text-center">
                                    <i class="bi bi-check-circle-fill" style="color: #3CB371; font-size: 1.2rem;"></i>
                                </div>
                            </div>
                            
                            <!-- Feature Row 4 -->
                            <div class="row feature-row align-items-center py-2">
                                <div class="col-9 text-start">
                                    Host and promote events with seamless RSVP tracking.
                                </div>
                                <div class="col-3 text-center">
                                    <i class="bi bi-check-circle-fill" style="color: #3CB371; font-size: 1.2rem;"></i>
                                </div>
                            </div>
                            
                            <!-- Feature Row 5 -->
                            <div class="row feature-row align-items-center py-2">
                                <div class="col-9 text-start">
                                    Manage your own brand community.
                                </div>
                                <div class="col-3 text-center">
                                    <i class="bi bi-check-circle-fill" style="color: #3CB371; font-size: 1.2rem;"></i>
                                </div>
                            </div>
                            
                            <!-- Feature Row 6 -->
                            <div class="row feature-row align-items-center py-2">
                                <div class="col-9 text-start">
                                    Directly address your customers' questions and build trust.
                                </div>
                                <div class="col-3 text-center">
                                    <i class="bi bi-check-circle-fill" style="color: #3CB371; font-size: 1.2rem;"></i>
                                </div>
                            </div>
                            
                            <!-- Feature Row 7 -->
                            <div class="row feature-row align-items-center py-2">
                                <div class="col-9 text-start">
                                    Gain actionable insights to see what's working – track views and identify your most popular offerings.
                                </div>
                                <div class="col-3 text-center">
                                    <i class="bi bi-check-circle-fill" style="color: #3CB371; font-size: 1.2rem;"></i>
                                </div>
                            </div>
                        </div>
                    </div>

                        <div class="row justify-content-center mobile-view-show">
                            <button class="btn rounded p-3 text-start mx-0 mb-3 col-5 me-2 pricing-plan-card strong-shadow" @click="toggleMonthlyPricing" :style="{ backgroundColor: selectedMonthlyPricing ? '#DD9E54' :'white', color: selectedMonthlyPricing ? 'white' :'black', borderColor: '#DD9E54', borderWidth:'3px' }"> <span>
                                    <h6> <b> Monthly plan </b> </h6>
                                    <p class="m-0"> US$95 / Month </p> 
                                    <small class="fst-italic p-0"> Billed monthly </small>
                                    <h6 class="mt-2" style="color: green;"><b>Cancel anytime.</b></h6>
                                </span>
                            </button>
                            <button class="btn rounded p-3 text-start mx-0 mb-3 col-5 pricing-plan-card strong-shadow" @click="toggleYearlyPricing" :style="{ backgroundColor: selectedYearlyPricing ? '#DD9E54' :'white', color: selectedYearlyPricing ? 'white' :'black',  borderColor: '#DD9E54', borderWidth:'3px' }">  <span>
                                    <h6> <b> Yearly plan </b> </h6> 
                                    <p class="m-0"> US$80 / Month </p> 
                                    <small class="fst-italic p-0"> US$960 Billed annually </small>
                                    <h5 class="mt-2" style="color: green;"><b>Save 15%!</b></h5>
                                </span>
                            
                            </button>
                        </div> 

                        <!-- Start of form -->
                        <form v-on:submit.prevent="submitListing" id="frm">

                        
                        <!-- Profile Type -->
                            <div class='row justify-content-start mb-3 text-start'>
                                <p class="text-start mb-1">Choose Your Profile Type <span style="color: red;">*</span></p>
                                <div class="col-md-12 justify-content-between">
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input" type="radio" id="inlineCheckbox1" v-model="businessType" value="producer" name="business">
                                        <label class="form-check-label text-start" for="inlineCheckbox1">Brand/Producer</label>
                                    </div>
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input" type="radio" id="inlineCheckbox2" v-model="businessType" value="venue" name="business">
                                        <label class="form-check-label text-start" for="inlineCheckbox2">Venue</label>
                                    </div>                                                                                                   
                                </div>   
                                <span v-if="missingBusinessType" class="text-danger">Please choose your business type.</span>                                      
                            </div>

                        <!-- Input: Independent Bottler -->
                            <div v-if="businessType=='producer'" class="row justify-content-start mb-3 text-start">
                                <p class="text-start mb-1">Is your business an Independent Bottler? <span style="color: red;">*</span></p>
                                <div class="col-md-12 justify-content-between">
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input" type="radio" id="inlineCheckbox1" v-model="isIndependentBottler" :value="true" name="Yes">
                                        <label class="form-check-label text-start fw-bold" for="inlineCheckbox1">Yes</label>
                                    </div>
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input" type="radio" id="inlineCheckbox3" v-model="isIndependentBottler" :value="false" name="No">
                                        <label class="form-check-label text-start fw-bold" for="inlineCheckbox3">No</label>
                                    </div>                                                                                                   
                                </div> 
                                <span v-if="missingIndependentBottler" class="text-danger">Please choose if you are an independent bottler.</span>
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
                                <span v-if="invalidBusinessLink" class="text-danger">Please enter a valid business link.</span>
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
                    <div class="col-lg-4 col-md-12" style="background-color: wheat;">
                        <div class="d-grid gap-2 mt-4">
                            <p class="fs-6 fw-bold px-4 mobile-view-hide">Subscribe to a Business Account to connect directly with your fans and grow your business.</p>
                        </div>
                        <div class="row justify-content-center mobile-view-hide">
                            <!-- <div class="col-xl-2 col-lg-1 col-md-1"></div> -->
                            <button class="btn rounded p-3 text-start mx-3 mb-3 col-8 pricing-plan-card strong-shadow" @click="toggleMonthlyPricing" :style="{ backgroundColor: selectedMonthlyPricing ? '#DD9E54' :'white', 
                                                                                                                                color: selectedMonthlyPricing ? 'white' :'black', 
                                                                                                                                borderColor: '#DD9E54', 
                                                                                                                                borderWidth:'3px' }">
                                <span>
                                    <h6> <b> Monthly plan </b> </h6>
                                    <p class="m-0"> US$95 / Month </p> 
                                    <small class="fst-italic p-0"> Billed monthly </small>
                                    <h6 class="mt-1" style="color: green;"><b>Cancel anytime.</b></h6>
                                </span>
                            </button>
                        </div>
                        <div class="row justify-content-center mobile-view-hide">
                            <!-- <div class="col-xl-2 col-lg-1 col-md-1"></div> -->
                            <button class="btn rounded p-3 text-start mx-3 mb-3 col-8 pricing-plan-card strong-shadow" @click="toggleYearlyPricing" :style="{ backgroundColor: selectedYearlyPricing ? '#DD9E54' :'white', 
                                                                                                                                color: selectedYearlyPricing ? 'white' :'black', 
                                                                                                                                borderColor: '#DD9E54', 
                                                                                                                                borderWidth:'3px' }">
                                <div class="row">
                                    <div class="col-7"> <h6> <b> Yearly plan </b> </h6> </div> 
                                    
                                </div>
                                <span>
                                    <p class="m-0"> US$80 / Month </p> 
                                    <small class="fst-italic p-0"> US$960 Billed annually </small>
                                    <h6 class="mt-2" style="color: green;"><b>Save 15%!</b></h6>
                                </span>
                            
                            </button>
                        </div>  
                        <span v-if="missingPlan" class="text-danger">Please select a plan.</span>
                    </div>

                </div>

                <div class="row">
                    <div class="col-lg-8 col-md-12">
                        <button type="submit" class="btn fw-bold btn-md secondary-btn mx-auto mb-3" @click="signUp">Register for Account</button>
                    </div>
                </div>


            </div>
            
        </div>
    </div>

  <!-- Footer End -->
    <FooterBar />
</template>

<!-- ------------------------------------------------------------------------------ -->

<script>
    // import components used
    import NavBar from '@/components/NavBar.vue';
    import FooterBar from "@/components/FooterBar.vue";

    export default{
        name: 'BusinessSignUpPage',
        components: {
            NavBar,
            FooterBar
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
                missingIndependentBottler:false,
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
                invalidBusinessLink:false,

                // form variables
                businessType:'',
                businessName:'',
                isIndependentBottler:null,
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
            if(accountDetails.businessType){
                this.businessType = accountDetails.businessType
            }
            if(accountDetails.businessName){
                this.businessName = accountDetails.businessName
            }
            if(accountDetails.businessDesc){
            this.businessDesc = accountDetails.businessDesc
            }
            if(accountDetails.businessLink){
                this.businessLink = accountDetails.businessLink
            }
            if(accountDetails.originCountry){
                this.selectedCountry = accountDetails.originCountry
            }
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
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getCountries`);
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
                if (this.businessType == 'producer' && this.isIndependentBottler == null){
                    this.missingIndependentBottler = true
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

                console.log(1)

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
                
                if(this.businessLink!=''){
                    if (!this.businessLink.includes('/')){
                        this.invalidBusinessLink = true
                        errorCount++
                    }
                }

                if(errorCount>0){
                    return null
                }
                let businessId =null

                if(this.businessLink!=''){
                    businessId = this.businessLink.split("/").pop()
                }
                if (this.businessType == 'venue'){
                    this.isIndependentBottler = false
                }
                let joinDate = new Date().toISOString();
                let submitAPI =  `${process.env.VUE_APP_API_URL}/createAccount/createAccountRequest`
                let submitData = {
                    "businessId" : businessId,
                    "businessName": this.businessName,
                    "businessType": this.businessType,
                    "isIndependentBottler": this.isIndependentBottler,
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
                console.log(submitData)
                console.log(errorCount)
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
                this.missingIndependentBottler=false
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
                this.invalidBusinessLink=false
            },
        },
    }

</script>

<style scoped>

.login-header-banner {
  position: relative;
  width: 100%;
  padding-top: calc(3 / 6 * 100%); /* 2:6 aspect ratio = 33.33% */
  overflow: hidden;
}

.login-header-banner img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.background-login {
  background-image: url('@/assets/business-signup.jpg');
  background-size: cover;
  background-position: center;
  min-height: 100vh;
  width: 100%;
  position: relative;
}

@media (max-width: 991px) {
  .background-login {
    background-image: none;
    background-color: wheat;
  }
}

.feature-row {
  border-bottom: 1px solid #e0e0e0;
}

.feature-row:last-child {
  border-bottom: none;
}

.feature-table {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 0 10px;
  background-color: white;
}


.pricing-plan-card {
  background-color: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.pricing-plan-card:hover {
  border-color: #3CB371;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.pricing-plan-card.selected {
  background-color: #f8fff9;
  border: 2px solid #3CB371;
  box-shadow: 0 4px 12px rgba(60,179,113,0.2);
}

.pricing-plan-card.selected::before {
  content: "Selected";
  position: absolute;
  top: -12px;
  right: 20px;
  background-color: #3CB371;
  color: white;
  font-size: 12px;
  padding: 2px 10px;
  border-radius: 10px;
  font-weight: bold;
}

.strong-shadow {
  box-shadow: 0 8px 16px rgba(0,0,0,0.5) !important;
}
</style>