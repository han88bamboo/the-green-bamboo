<template>
    <NavBar />

    <!-- Display when data is still loading -->
    <div class="text-info-emphasis fst-italic fw-bold fs-5 pt-5" v-if="validToken == true && dataLoaded == false">
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

    <!-- Display when token is invalid -->
    <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="validToken == false"> 
        <span>The link provided is either invalid or expired; please contact the administrator for assistance.</span>
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

    <div class="" v-if="dataLoaded && validToken">

        <div class="container text-start" style="width: 50%">
            <p style="font-family: radley; font-size: 50px;" class="mt-5 mb-0">You’re almost all set up!</p>
            <p style="font-family: radley; font-size: 30px;">Enter your payment details and set up your login details.</p>

            <!-- choose plan -->
            <div class="row justify-content-between">
                <div class="col-6">
                    <button class="btn rounded p-3 text-start mb-3 w-100" @click="toggleMonthlyPricing" :style="{ backgroundColor: selectedMonthlyPricing ? '#DD9E54' :'white', 
                                                                                                                        color: selectedMonthlyPricing ? 'white' :'black', 
                                                                                                                        borderColor: '#DD9E54', 
                                                                                                                        borderWidth:'3px' }">
                        <span>
                            <h6> <b> Monthly plan </b> </h6>
                            <p class="m-0"> $65 / Month </p> 
                            <small class="fst-italic p-0"> Billed monthly </small>
                        </span>
                    </button>
                </div>
                <div class="col-6">
                    <button class="btn rounded p-3 text-start mb-3 w-100" @click="toggleYearlyPricing" :style="{ backgroundColor: selectedYearlyPricing ? '#DD9E54' :'white', 
                                                                                                                        color: selectedYearlyPricing ? 'white' :'black', 
                                                                                                                        borderColor: '#DD9E54', 
                                                                                                                        borderWidth:'3px' }">
                        <div class="row">
                            <div class="col-7"> <h6> <b> Yearly plan </b> </h6> </div> 
                            <div class="rounded col-5 text-center" style="background-color: green; color: white;">Save 23%</div>
                        </div>
                        <span>
                            <p class="m-0"> $50 / Month </p> 
                            <small class="fst-italic p-0"> $600 Billed annually </small>
                        </span>
                    
                    </button>
                </div>
            </div>
            
            <div v-if="selectedMonthlyPricing || selectedYearlyPricing">
                <form id="payment-form">
                    <div id="payment-element">
                        <!-- Elements will create form elements here -->
                    </div>
                </form>
            </div>
            <div v-else>
                <span class="text-danger">Please select a plan</span>
            </div>

            <!-- username and password -->
            <div v-if="accountRequest.isNew" style="width: 75%;">
                <!-- Input: Username -->
                    <div class="form-group mb-3">
                        <p class="text-start mb-1" style="font-family: radley; font-size: 25px;">Username</p>
                        <input type="text" class="form-control" :style="formError.username.length > 0 ? 'border-color: red;' : 'border-color: black;'" v-model="username" id="username" @blur="checkUsername"/>
                        <span v-if="formError.username.length>0" class="text-danger">{{ formError.username }}</span>
                    </div>

                <!-- Input: Password -->
                    <div class="form-group mb-3">
                        <p class="text-start mb-1" style="font-family: radley; font-size: 25px;">New Password</p>
                        <p class="fst-italic">Password should be at least 8 characters long, and contain: 1 uppercase, 1 lowercase, 1 symbol and 1 number.</p>
                        <input type="password" class="form-control" :style="formError.newPassword.length > 0 ? 'border-color: red;' : 'border-color: black;'" v-model="newPassword" id="newPassword" @blur="checkNewPassword"/>
                        <span v-if="formError.newPassword.length>0" class="text-danger">
                            <span v-for="(error, index) in formError.newPassword" :key="index">{{ error }}<br></span>
                        </span>
                    </div>

                <!-- Input: Confirm Password -->
                    <div class="form-group mb-3">
                        <p class="text-start mb-1" style="font-family: radley; font-size: 25px;">Confirm Password</p>
                        <input type="password" class="form-control" :style="formError.confirmPassword.length > 0 ? 'border-color: red;' : 'border-color: black;'" v-model="confirmPassword" id="confirmPassword" @blur="checkConfirmPassword"/>
                        <span v-if="formError.confirmPassword.length>0" class="text-danger">{{ formError.confirmPassword }}</span>
                    </div>
            </div>


            <div class="row">
                <div class="col-lg-8 col-md-12">
                    <button v-if="accountRequest.isNew" type="submit" class="btn btn-lg secondary-btn-border-thick mx-auto my-3" @click="createAccount">Create Account</button>
                    <button v-else type="submit" class="btn btn-lg secondary-btn-border-thick mx-auto my-3" @click="createAccount">Subscribe</button>
                </div>
            </div>


        </div>



        
    </div>

</template>

<!-- ------------------------------------------------------------------------------ -->

<script>
    // import components used
    import NavBar from '@/components/NavBar.vue';
    import { loadStripe } from '@stripe/stripe-js';

    export default {
        name: 'BillingSecurity',
        components: {
            NavBar
        },
        data(){
            return{
                dataLoaded: false,
                monthlyPriceId: "price_1PV7PCDnjokAiSGzX84MZogY",
                yearlyPriceId: "price_1PV7PsDnjokAiSGz02ZZTJdu",

                // owner details
                stripe: null,
                elements: null,

                // customer details
                token: "",
                tokenData: {},
                validToken: null,
                businessId: "",
                requestId: "",
                accountRequest: {},
                businessType: "",
                business: {},
                customerName: "",
                customerEmail: "",

                // plan details
                selectedMonthlyPricing: false,
                selectedYearlyPricing: true,

                // stripe details
                priceId: "",
                customerId: "",
                clientSecret: "",

                paymentFilled: false,

                // username and password
                usernames: null,
                username: "",
                newPassword: "",
                confirmPassword: "",
                formError: {
                    username: "",
                    newPassword: [],
                    confirmPassword: "",
                },
            }
        },
        async mounted(){

            this.token = this.$route.query.token;
            
            this.stripe = await loadStripe('pk_test_51PV6CNDnjokAiSGzhdAambzILFYOByYtxMRMsVQCcQobPIxlFDi2a6gKYe8BQD021FQxFUejn4eIcjSLBHsHbD9A00T4Z8sPPl');

            async function initiateProcess() {
                await this.verifyToken();

                if (!this.validToken) {
                    return;
                }

                await this.loadData();

                if (this.business.stripeCustomerId) {
                    this.customerId = this.business.stripeCustomerId;
                } else {
                    await this.create_customer();
                }

                await this.create_subscription();
                this.paymentElement();
            }

            initiateProcess.call(this);


        },
        methods: {
            async toggleYearlyPricing(){
                if(this.selectedMonthlyPricing && !this.selectedYearlyPricing){
                    this.selectedMonthlyPricing= false
                }
                if(this.selectedYearlyPricing){
                    this.selectedYearlyPricing=false
                }else{
                    this.selectedYearlyPricing = true
                    await this.create_subscription()
                    this.paymentElement()
                }
            },
            async toggleMonthlyPricing(){
                if(this.selectedYearlyPricing && ! this.selectedMonthlyPricing){
                    this.selectedYearlyPricing= false
                }
                if(this.selectedMonthlyPricing){
                    this.selectedMonthlyPricing=false
                }else{
                    this.selectedMonthlyPricing = true
                    await this.create_subscription()
                    this.paymentElement()
                }
            },
            async loadData(){
                // get token
                try {
                    const response = await this.$axios.get(`http://127.0.0.1:5000/getToken/${this.token}`);
                    this.tokenData = response.data;
                    this.businessId = response.data.userId;
                    this.requestId = response.data.requestId;
                } 
                catch (error) {
                    console.error(error);
                    this.loadError = true;
                }

                // get request
                try {
                    const response = await this.$axios.get(`http://127.0.0.1:5000/getAccountRequest/${this.requestId.$oid}`);
                    this.accountRequest = response.data;
                    this.businessType = this.accountRequest.businessType;
                    this.customerName = this.accountRequest.firstName + " " + this.accountRequest.lastName;
                    this.customerEmail = this.accountRequest.email;
                    this.selectedMonthlyPricing = (this.accountRequest.pricing == "monthly");
                    this.selectedYearlyPricing = (this.accountRequest.pricing == "yearly");
                } 
                catch (error) {
                    console.error(error);
                    this.loadError = true;
                }

                // get business
                try {
                    const response = await this.$axios.get(`http://127.0.0.1:5000/get${this.businessType.charAt(0).toUpperCase()}${this.businessType.slice(1)}/${this.businessId.$oid}`);
                    this.business = response.data;
                    this.username = this.business.username;
                }
                catch (error) {
                    console.error(error);
                    this.loadError = true;
                }

                this.dataLoaded = true;
            },

            async create_customer() {
                // create customer
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5009/create-customer',
                        {
                            customerEmail: this.customerEmail,
                            customerName: this.customerName,
                        }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    console.log(response.data);
                    this.customerId = response.data.customerId;

                    // update business with customerId
                    const response2 = await this.$axios.post(`http://127.0.0.1:5031/updateCustomerId`,
                        {
                            businessId: this.businessId,
                            customerId: this.customerId,
                            businessType: this.businessType
                        }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    console.log(response2.data);

                } catch (error) {
                    console.error(error);
                }
            },

            async create_subscription() {
                if (this.selectedMonthlyPricing) {
                    this.priceId = this.monthlyPriceId;
                } else {
                    this.priceId = this.yearlyPriceId;
                }
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5009/create-subscription',
                        {
                            priceId: this.priceId,
                            customerId: this.customerId,
                        }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    console.log(response.data);
                    this.clientSecret = response.data.clientSecret;
                } catch (error) {
                    console.error(error);
                }
            },

            async paymentElement() {

                const stripe = this.stripe;
                const clientSecret = this.clientSecret;
                const appearance = {
                    theme: 'stripe',
                };

                this.elements = stripe.elements({clientSecret, appearance});
                const elements = this.elements;

                const paymentElement = elements.create('payment');
                paymentElement.mount('#payment-element');

                paymentElement.on('change', (event) => {
                    this.paymentFilled = event.complete;
                });

            },

            async processPayment() {

                const stripe = this.stripe;
                const elements = this.elements;

                const { error, paymentIntent } = await stripe.confirmPayment({
                    elements,
                    redirect: 'if_required' // Prevents automatic redirection

                });

                if (error) {
                    if (error.type === "card_error" || error.type === "validation_error") {
                        console.log(error.message);
                    } else {
                        console.log("An unexpected error occurred.");
                    }

                } else if (paymentIntent && paymentIntent.status === 'succeeded') {
                    // sucessful payment -> business is now verified

                    // update account request
                    try {
                        await this.$axios.post('http://127.0.0.1:5031/updateAccountRequest', 
                            {
                                requestID: this.requestId.$oid,
                                isPending: false,
                                isApproved: true,
                            }, {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });
                    } catch (error) {
                        console.error(error);
                    }
                    
                    // update business claim status
                    const port = this.businessType == "producer" ? "5200" : "5300";
                    try {
                        await this.$axios.post(`http://127.0.0.1:${port}/update${this.businessType.charAt(0).toUpperCase()}${this.businessType.slice(1)}ClaimStatus`, 
                            {
                                businessId: this.businessId.$oid,
                                claimStatus: true,
                            }, {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });
                    } catch (error) {
                        console.error(error);
                    }

                    return true;


                } else {
                    console.log("Payment processing...");
                }

            },

            async deleteToken() {
                try {
                    const response = await this.$axios.post(`http://127.0.0.1:5031/deleteToken`,
                        {
                            token: this.token,
                        }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    console.log(response.data);

                } catch (error) {
                    console.error(error);
                }
            },

            async createAccount () {
                
                if (!this.paymentFilled) {
                    return;
                }

                var updateSuccess = false;

                if (this.accountRequest.isNew) {
                    this.checkUsername();
                    this.checkNewPassword();
                    this.checkConfirmPassword();
    
                    if (this.formError.username.length > 0 || this.formError.newPassword.length > 0 || this.formError.confirmPassword.length > 0) {
                        return;
                    }

                    updateSuccess = await this.updateUsernamePassword();
                }

                var paymentSuccess = false;

                if (updateSuccess || !this.accountRequest.isNew) {
                    paymentSuccess = await this.processPayment();
                }

                if ( (updateSuccess || !this.accountRequest.isNew) && paymentSuccess ) {
                    await this.deleteToken();
                    // save details to local storage 
                    localStorage.setItem("88B_accID", this.businessId.$oid);
                    localStorage.setItem("88B_accType", this.businessType);
                    // redirect to profile page
                    this.$router.push(`/profile/${this.businessType}/${this.businessId.$oid}`)
                }
                
            }, 

            async verifyToken() {
                try {
                    const response = await this.$axios.get(`http://127.0.0.1:5000/getToken/${this.token}`);
                    this.tokenData = response.data;
                    console.log(this.tokenData);
                    if (Object.keys(this.tokenData).length > 0) {
                        const expiry = new Date(this.tokenData.expiry.$date);
                        const now = new Date();
                        if (expiry > now) {
                            this.validToken = true;
                            return;
                        }
                    }
                    this.validToken = false;
                } 
                catch (error) {
                    console.error(error);
                    this.loadError = true;
                }
            }, 

            async checkUsername() {

                // username empty
                if (this.username == "") {
                    this.formError["username"] = "Please enter a username.";
                    return;

                // username not empty
                } else {
                    // username changed
                    if (this.username != this.business.username) {

                        // check if usernames have been loaded
                        if (!this.usernames) {
                            try {
                                const response = await this.$axios.get(`http://127.0.0.1:5000/getUsernames`);
                                this.usernames = response.data;
                            } 
                            catch (error) {
                                console.error(error);
                                this.loadError = true;
                            }
                        }
                        // check if username exists
                        if (this.usernames.includes(this.username)) {
                            this.formError["username"] = "Username already exists. Please choose another username.";
                            return
                        } 
                    }
                }
                this.formError["username"] = "";
            },
            
            checkNewPassword() {
                // Password should be at least 8 characters long, and contain: 1 uppercase, 1 lowercase, 1 symbol and 1 number.
                // Check if password length is at least 8 characters
                this.formError["newPassword"] = [];

                if (this.newPassword == "") {
                    this.formError["newPassword"].push("Please enter a password.");
                } else {

                    if (this.newPassword.length < 8) {
                        this.formError["newPassword"].push("Password must be at least 8 characters long.");
                    }
    
                    // Check for at least one uppercase letter
                    if (!/[A-Z]/.test(this.newPassword)) {
                        this.formError["newPassword"].push("Password must contain at least one uppercase letter.");
                    }
    
                    // Check for at least one lowercase letter
                    if (!/[a-z]/.test(this.newPassword)) {
                        this.formError["newPassword"].push("Password must contain at least one lowercase letter.");
                    }
    
                    // Check for at least one digit
                    if (!/[0-9]/.test(this.newPassword)) {
                        this.formError["newPassword"].push("Password must contain at least one number.");
                    }
    
                    // Check for at least one symbol
                    if (!/[^A-Za-z0-9]/.test(this.newPassword)) {
                        this.formError["newPassword"].push("Password must contain at least one symbol.");
                    }
                }
            }, 

            checkConfirmPassword() {
                if (this.confirmPassword == "") {
                    this.formError["confirmPassword"] = "Please confirm your password.";
                } else {
                    if (this.newPassword != this.confirmPassword) {
                        this.formError["confirmPassword"] = "Passwords do not match.";
                    } else {
                        this.formError["confirmPassword"] = "";
                    }
                }
            }, 

            async updateUsernamePassword() {
                const hashedPassword = this.hashPassword(this.username, this.newPassword);
                try {
                    const response = await this.$axios.post(`http://127.0.0.1:5031/updateUsernamePassword`,
                        {
                            businessId: this.businessId,
                            username: this.username,
                            hashedPassword: hashedPassword,
                            businessType: this.businessType
                        }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    console.log(response.data);

                    return true;

                } catch (error) {
                    console.error(error);
                }
            }, 

            hashPassword(id, password) {
                const combinedString = id.toString() + password;
                let hash = 0;

                for (let i = 0; i < combinedString.length; i++) {
                    const char = combinedString.charCodeAt(i);
                    hash = (hash << 5) - hash + char;
                    hash |= 0; // convert to 32-bit integer
                }

                return hash;
            },

        
        }
    }

</script>