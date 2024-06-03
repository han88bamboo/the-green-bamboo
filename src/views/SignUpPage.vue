<!-- HTML -->
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
        <div class="text-success fst-italic fw-bold fs-3" v-if="successSubmission"> 
            <span>The account has successfully been created!</span> <!-- for user -->
            <br>
            <!-- <button class="btn primary-btn btn-sm">
                <router-link :to="{ path: '/login' }" class="primary-clickable-text">
                    <span class="fs-5 fst-italic" style="color: white;"> Click to login here! </span>
                </router-link>
            </button> -->
            <button class="btn primary-btn btn-sm" @click="loginUser">
                    <span class="fs-5 fst-italic" style="color: white;"> Click to get login-ed! </span>
            </button>
        </div>
        
        <!-- Display when login encounters an error -->
        <div class="text-danger fst-italic fw-bold fs-3" v-if="loginError"> 
            <span>An error occurred while attempting to login!</span>
            <br>
            <button class="btn primary-btn btn-sm" @click="reset">
                <router-link :to="{ path: '/login' }" class="primary-clickable-text">
                    <span class="fs-5 fst-italic" style="color: white;"> Click to login here! </span>
                </router-link>
            </button>
        </div>

        <!-- Display when bottle listing submission encounters an error -->
        <div class="text-danger fst-italic fw-bold fs-3" v-if="errorSubmission"> 
            <span v-if="errorMessage">An error occurred while attempting to create account, please try again!</span>
            <span v-if="duplicateEntry">The account has already been created.</span>
            <br>
            <button class="btn primary-btn btn-sm" @click="reset">
                <span class="fs-5 fst-italic"> Retry sign up again! </span>
            </button>
        </div>

    <div class="body-login" v-if="fillForm && dataLoaded">
        <div class="container rounded">
            <div class="row">
                <div class="col-12 col-sm-10 col-md-8 m-auto">
                    <div class="py-5">
                        <div>
                            <div class="container rounded pt-3 pb-5" style="background-color:#DDC8A9;">
                                <div class="d-grid gap-2" style="position: relative;">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="ms-5 bi bi-arrow-left-circle" viewBox="0 0 16 16" style="position: absolute; top: 10; left: 0;" v-on:click="goBack">
                                        <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-4.5-.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"/>
                                    </svg>
                                    <p class="fw-bold fs-1" style="font-style: italic; ">Create an Account</p>
                                </div>

                            <!-- <div class="row pt-5">
                                <div class="d-grid gap-2 col-md-5 col-10 mx-auto">
                                    <div class="form-floating">
                                        <input type="text" class="form-control form-box-outline" id="id" placeholder="Username" v-model="ID">
                                        <label for="username"> Username </label>
                                    </div>
                                </div>
                            </div> -->

                            <!-- Start of form -->
                            <form v-on:submit.prevent="submitListing" id="frm">
                                        
                                <!-- Input: Username -->
                                <div class="row pt-4">
                                    <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                                        <div class="form-floating">
                                            <input type="text" class="form-control form-box-outline" v-model="username" id="username" placeholder="Username">
                                            <label for="username"> Username </label>
                                            <span v-if="missingUsername" class="text-danger">Please enter a username.</span>
                                            <span v-if="duplicateUser" class="text-danger">Username is already taken, if this is you, login instead!</span>
                                        </div>
                                    </div>
                                </div>
                                <!-- Input: Display Name -->
                                <div class="row pt-2">
                                    <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                                        <div class="form-floating">
                                            <input type="text" class="form-control form-box-outline" v-model="displayName" id="displayName" placeholder="Display Name">
                                            <label for="displayName"> Display Name </label>
                                            <span v-if="missingDisplayName" class="text-danger">Please enter a display name.</span>
                                        </div>
                                    </div>
                                </div>

                                <!-- Input: First Name -->
                                <div class="row pt-2">
                                    <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                                        <div class="form-floating">
                                            <div class="row">
                                                <div class="form-group pb-md-0 pb-2 col-md-6 col-12">
                                                    <div class="form-floating">
                                                        <input type="text" class="form-control form-box-outline" v-model="firstName" id="firstName" placeholder="First Name">
                                                        <label for="firstName"> First Name </label>
                                                        <span v-if="missingFirstName" class="text-danger">Please enter your First Name.</span>
                                                    </div>
                                                </div>
                                                <!-- Input: Last Name -->
                                                <div class="form-group col-md-6 col-12">
                                                    <div class="form-floating">
                                                        <input type="text" class="form-control form-box-outline" v-model="lastName" id="lastName" placeholder="Last Name">
                                                        <label for="lastName"> Last Name </label>
                                                        <span v-if="missingLastName" class="text-danger">Please enter your Last Name.</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <!-- Input: Email -->
                                <div class="row pt-2">
                                    <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                                        <div class="form-floating">
                                            <input type="text" class="form-control form-box-outline" v-model="email" id="email" placeholder="Email">
                                            <label for="email"> Email </label>
                                            <span v-if="missingEmail" class="text-danger">Please enter an email.</span>
                                            <span v-if="invalidEmail" class="text-danger">Please enter a valid email.</span>
                                        </div>
                                    </div>
                                </div>
                                <!-- Input: Password -->
                                <div class="row pt-2">
                                    <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                                        <div class="form-floating">
                                            <input type="password" class="form-control form-box-outline" v-model="password" id="password" placeholder="Password">
                                            <label for="password"> Password </label>
                                            <span v-if="missingPassword" class="text-danger">Please enter a password.</span>
                                        </div>
                                    </div>
                                </div>
                                <!-- Input: Repeat Password -->
                                <div class="row pt-2">
                                    <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                                        <div class="form-floating">
                                            <input type="password" class="form-control form-box-outline" v-model="passwordRepeat" id="passwordRepeat" placeholder="Repeat Password">
                                            <label for="passwordRepeat"> Repeat Password </label>
                                            <span v-if="missingPasswordRepeat && !missingPassword" class="text-danger">Please repeat your password.</span>
                                            <span v-if="passwordMismatch && !missingPasswordRepeat" class="text-danger">Passwords do not match, please try again.</span>
                                        </div>
                                    </div>
                                </div>
                                <!-- Input: Country -->
                                <div class="row pt-2">
                                    <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                                        <div class="form-floating">
                                            <div class="input-group mb-0">
                                                <span class="input-group-text" id="basic-addon1">Country</span>
                                                <select v-model="selectedCountry" class="form-select form-box-outline" id="inputGroupSelect01">
                                                    <!-- Add in the languages here -->
                                                    <option v-for="country in countries" v-bind:key="country['_id']">{{ country['originCountry'] }}</option>
                                                </select>
                                            </div>
                                            <span v-if="missingCountry" class="text-danger mt-0 mb-3">Please select your country.</span>
                                        </div>
                                    </div>
                                </div>
                                <!-- Input: Birthday -->
                                <div class="row pt-2">
                                    <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                                        <div class="form-floating">
                                            <div class="input-group mb-0">
                                                <span class="input-group-text" id="basic-addon1">Birthday</span>
                                                <input type="date" class="form-control form-box-outline" v-model="birthday" id="birthday" placeholder="Birthday">
                                            </div>
                                            <div class="text-center mb-3">
                                                <span v-if="missingBirthday" class="text-danger mt-0 mb-3">Please enter your birthday.</span>
                                                <span v-if="underAge" class="text-danger mt-0 mb-3">You are underage, creation of account is not allowed.</span>
                                                <span v-if="illegalCountry" class="text-danger mt-0 mb-3">It is illegal to drink in your country, creation of account is not allowed.</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="text-center mt-3">
                                    <div class="form-check form-check-inline">
                                        <label class="form-check-label">I verify I am above legal drinking age in my country of location</label>
                                        <input class="form-check-input" type="checkbox" v-model="ageCheck">
                                    </div>
                                </div>
                                <div class="text-center mb-3">
                                    <span v-if="missingAgeCheck" class="text-danger">Please verify this.</span>
                                </div>
                                
                                <button type="submit" class="btn secondary-btn mx-1 mb-3" @click="signUp">Sign Up</button>
                                <!-- <button type="button" class="btn primary-btn mx-1 mb-3" @click="goBack">Return</button> -->
                            
                            </form>
                            <b>
                                <i>
                                    <p class="mb-2">
                                        If you are a drinks brand, bottler or venue owner trying to create an account, 
                                        <router-link :to="{ path: '/businessSignup' }"  class="default-body-text-no-background">click here</router-link>.
                                    </p>
                                    <p>
                                        If you already have an account and would like to login,
                                    <router-link :to="{ path: '/login' }"  class="default-body-text-no-background">click here</router-link>.
                                    </p>
                                </i>
                            </b>
                            <!-- End of Form -->
                            <!-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- End of display -->

    
</template>

<!-- ------------------------------------------------------------------------------ -->

<!-- JavaScript -->
<script>
    // import components used
    import NavBar from '@/components/NavBar.vue';

    export default{
        name: 'SignUpPage',
        components: {
            NavBar
        },
        data(){
            return{
                dataLoaded: false,

                // Initial user variable
                response:[],

                // Form variables
                username:"",
                displayName:'',
                email:'',
                password:'',
                passwordRepeat:'',
                firstName:'',
                lastName:'',
                birthday:'',
                ageCheck:'',
                selectedCountry:'',

                countries: [],
                // Submission variables

                missingUsername:false,
                missingDisplayName:false,
                missingEmail:false,
                invalidEmail:false,
                passwordMismatch:false,
                missingPassword:false,
                missingPasswordRepeat:false,
                missingFirstName:false,
                missingLastName:false,
                missingBirthday:false,
                missingAgeCheck:false,
                duplicateUser:false,
                missingCountry:false,
                underAge:false,
                illegalCountry: false,

                submitForm: false,
                successSubmission: false,
                errorSubmission: false,
                errorMessage: false,
                duplicateEntry: false,
                fillForm: true,
                responseCode: "",
                loginError:false,
            }
        },
        mounted() {
            this.loadData()
        },
        methods:{
            async loadData(){
                try {
                    const response = await this.$axios.get('http://127.0.0.1:5000/getCountries');
                    this.countries = response.data.sort((a,b)=>{
                            return a.originCountry.localeCompare(b.originCountry)
                            })
                    this.dataLoaded = true;
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
            },

            goBack() {
                this.$router.go(-1)
            },
            signUp(){

                // Reset all errors/success message, just in case
                this.resetError()
                
                // Form validation
                let errorCount = 0

                // username validation
                if(this.username==''){
                    this.missingUsername = true
                    errorCount++
                }else{
                    this.checkUsername(this.username)
                    if(this.duplicateUser){
                        errorCount++
                    }
                }

                if(this.displayName ==''){
                    this.missingDisplayName = true
                    errorCount++
                }

                // Email validation
                if(this.email==''){
                    this.missingEmail = true
                    errorCount++
                }else if(!this.email.match('.+@.+..+')){
                    this.invalidEmail = true
                    errorCount++
                }
                // Password validation
                if(this.password !== this.passwordRepeat){
                    this.passwordMismatch = true
                    errorCount++
                }
                if(this.password == ''){
                    this.missingPassword = true
                    errorCount++
                }
                if(this.passwordRepeat == ''){
                    this.missingPasswordRepeat = true
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
                // country validation
                if(this.selectedCountry== ''){
                    this.missingCountry = true
                    errorCount++
                }

                // Birthday validation
                if(this.birthday == ''){
                    this.missingBirthday = true
                    errorCount++
                }

                // Uncomment to allow age checker
                else{
                    var dob = new Date(this.birthday);
                    var now = new Date();
                    var age = now.getFullYear() - dob.getFullYear();
                    // Check if the birthday has occurred this year
                    if (now.getMonth() < dob.getMonth() || (now.getMonth() === dob.getMonth() && now.getDate() < dob.getDate())) {
                        age--;
                    }
                    let searchResult = this.countries.filter((country) => {
                        return country.originCountry==this.selectedCountry;
                    });
                    if(age<searchResult[0]['legalAge']){
                        this.underAge = true
                        errorCount++
                    }
                    else if(searchResult[0]['legalAge'] == 'Prohibited'){
                        this.illegalCountry = true
                        errorCount++
                    }
                }

                // Age Check validation
                if(!this.ageCheck){
                    this.missingAgeCheck = true
                    errorCount++
                }
                
                if(errorCount > 0){
                    return null
                }


                let hashedPassword = this.hashPassword(this.username, this.password)
                let joinDate = new Date().toISOString();
                let submitAPI =  "http://127.0.0.1:5031/createAccount"
                let submitData = {
                    // pass in first name, last name, email, isadmin
                    "username": this.username,
                    "displayName": this.username,
                    "firstName": this.username,
                    "lastName": this.username,
                    "email": this.email,
                    "choiceDrinks": [],
                    "drinkLists": {
                        "Drinks I Have Tried":{
                            "listDesc":"",
                            "listItems":[]
                        },
                        "Drinks I Want To Try":{
                            "listDesc":"",
                            "listItems":[]
                        }
                    },
                    "modType": [],
                    "photo": "",
                    "hashedPassword": hashedPassword.toString(),
                    "joinDate": joinDate,
                    "followLists": {
                        "users":[],
                        "producers":[],
                        "venues":[]
                    },
                    "birthday":this.birthday,
                    "isAdmin":false,
                }
                this.createAccount(submitAPI, submitData);
            },
            async createAccount(submitAPI, submitData){
                this.submitForm = true
                this.fillForm = false
                try{
                    const response = await this.$axios.post(submitAPI, submitData)
                    .then((response)=>{
                        this.reviewResponseCode = response.data.code
                    })
                    .catch((error)=>{
                        console.error(error);
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
                    console.error(error)
                    this.errorSubmission = true
                    this.errorMessage = true
                    this.submitForm = false
                }
                
            },
            // create unique hash based on username and password
            hashPassword(username, password) {
                const combinedString = username.toString() + password;
                let hash = 0;

                for (let i = 0; i < combinedString.length; i++) {
                    const char = combinedString.charCodeAt(i);
                    hash = (hash << 5) - hash + char;
                    hash |= 0; // convert to 32-bit integer
                }

                return hash;
            },
            reset(){
                this.fillForm = true
                this.errorMessage=false
                this.errorSubmission=false
                this.duplicateEntry=false
                this.successSubmission=false
            },
            resetError(){
                this.missingUsername=false
                this.missingEmail=false
                this.invalidEmail=false
                this.passwordMismatch=false
                this.missingPassword=false
                this.missingPasswordRepeat=false
                this.missingFirstName=false
                this.missingLastName=false
                this.missingBirthday=false
                this.missingAgeCheck=false
                this.missingCountry=false
                this.underAge=false
            },

            async checkUsername(username){
                try {
                    const response = await this.$axios.get('http://127.0.0.1:5000/getUsers');
                    let duplicateUser = response.data.filter((user)=>{
                        return user.username == username
                    })

                    if(duplicateUser.length==0){
                        this.duplicateUser = false
                    }else{
                        this.duplicateUser = true
                    }
                } 
                catch (error) {
                    console.error(error);
                }
            },

            async loginUser(){
                // Get specific user by username and set local storage then redirect
                try {
                    const submitURL = 'http://127.0.0.1:5000/getUserByUsername/' + this.username
                    const response = await this.$axios.get(submitURL);
                    if(response.data.username== this.username){
                        localStorage.setItem("88B_accID", response.data['_id']['$oid']);
                        localStorage.setItem("88B_accType", "user");
                        this.$router.push({path: '/'});
                    }
                } 
                catch (error) {
                    console.error(error);
                    this.loginError = true
                    this.successSubmission = false
                }
            },
            
        }
    }

</script>