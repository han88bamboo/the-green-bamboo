<!-- HTML -->
<template>
    <NavBar />

    <div class="body-login">
        <!-- select buttons -->
        <!-- <div class="container row" style="width: 50%"> -->
        <div class="container">
            <div class="row">
                <div class="col-12 col-sm-10 col-md-8 m-auto mobile-ps-0 mobile-pe-0">
                    <div class="pt-5 mobile-pt-0">
                        <form id="login" v-on:submit.prevent="checkLogin" style="background-color:#DDC8A9;" class="rounded">
                            <!-- login header text -->
                            <p class="fw-bold fs-1 pt-4 mx-3 mobile-fs-4 mobile-mb-1" style="font-style: italic; ">
                                Join a community of drink lovers.
                            </p>
                            <p class="fw-bold  mx-4 mobile-fs-6 mobile-view-show" style="font-style: italic; ">
                                Discover new juice and log your tasting notes!
                            </p>
                            <!-- username -->
                            <div class="row pt-5 mobile-pt-2">
                                <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                                    <div class="form-floating">
                                        <input type="text" class="form-control form-box-outline" id="id" placeholder="Username" v-model="ID">
                                        <label for="username"> Username </label>
                                    </div>
                                </div>
                            </div>
                            <!-- password -->
                            <div class="row pt-2">
                                <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                                    <div class="form-floating">
                                        <input type="password" class="form-control form-box-outline" id="password" placeholder="Password" v-model="password">
                                        <label for="password"> Password </label>
                                    </div>
                                </div>
                            </div>
                            <!-- checkbox -->
                            <div class="row pt-1 pb-3">
                                <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                                    <!-- Use Bootstrap grid classes for layout -->
                                    <div class="row g-2">
                                        <!-- Column for the checkbox -->
                                        <div class="col-12 text-start">
                                            <input type="checkbox" v-on:click="showPassword()" class="form-check-input">
                                            <label for="password" class="form-check-label"> &nbsp; Show password </label>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- error handling -->
                            <div class="row p-3 text-left" v-show="errors.length > 0">
                                <div class="d-grid gap-2 col-md-5 col-10 mx-auto">
                                    <div class="alert alert-danger" role="alert">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-triangle" viewBox="0 0 16 16">
                                        <path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.146.146 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.163.163 0 0 1-.054.06.116.116 0 0 1-.066.017H1.146a.115.115 0 0 1-.066-.017.163.163 0 0 1-.054-.06.176.176 0 0 1 .002-.183L7.884 2.073a.147.147 0 0 1 .054-.057zm1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566z"/>
                                        <path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995z"/>
                                        </svg>
                                        <h5> Error </h5>
                                        <li v-for="error in errors" :key="error"> {{ error }} </li>
                                    </div>
                                </div>
                            </div>
                            <!-- Confirm Selection -->
                            <div class="row pt-3">
                                <div class="col">
                                    <button v-if="authPending" type="submit" class="btn secondary-btn-border-thick btn-lg" disabled>Loading...</button>
                                    <button v-else type="submit" class="btn secondary-btn-border-thick btn-lg px-5">Log In</button>
                                    <GoogleSignIn />
                                </div>
                            </div>



                            <div class="row py-2">
                                <div class="col-6 mx-auto">
                                    <hr class="darker-hr">
                                </div>
                            </div>

                            <!-- Prompt sign up -->
                            <p class="mt-2 fw-bold fs-3" style="font-style: italic; ">
                                Don't have an account?
                            </p>
                            <div class="row">
                                <div class="col">
                                    <router-link :to="{ path: '/signup' }" class="default-text-no-background">
                                        <button class="btn secondary-btn-border-thick btn-lg px-5"> Sign Up </button>
                                    </router-link>
                                </div>
                            </div>

                            <!-- Business sign up -->
                            <div class="row pt-5 pb-3 mx-3">
                                <div class="col">
                                    <p>
                                        <b>
                                            <i>
                                                If you are a drinks brand, bottler or venue owner trying to create an account, 
                                                <router-link :to="{ path: '/businessSignup' }"  class="default-body-text-no-background">click here</router-link>.
                                            </i>
                                        </b>
                                    </p>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    // import components used
    import NavBar from '@/components/NavBar.vue';
    import GoogleSignIn from '@/components/GoogleSignIn.vue';

    // specify components used
    export default {
        name: 'LoginPage',
        components: {
            NavBar,
            GoogleSignIn
        },

        data() {
            return {
                authPending: false,
                accountID: {},
                errors: [],

                // form values
                role: '',
                ID: '',
                password: '',
            };
        },
        mounted() {
            this.loginCheck();
        },
        methods: {

            // Check if user is already logged in
            loginCheck() {
                if (localStorage.getItem("88B_accID") != null) {
                    this.accountID = localStorage.getItem("88B_accID");
                    this.role = localStorage.getItem("88B_accType");
                    this.redirectPage();
                }
            },

            // toggle password visibility
            showPassword() {
                var password = document.getElementById("password");
                if (password.type === "password") {
                        password.type = "text";
                    } 
                else {
                    password.type = "password";
                }
            },

            // Form Submission Function
            checkLogin() {

                // set authentication pending flag to true
                this.authPending = true
                // clear previous values
                this.errors = []
                // check if user is already logged in
                this.loginCheck();

                // [if] check if all details keyed in
                if (this.ID == "" || this.password == "") {
                    // check if ID keyed in
                    if (this.ID == "") {
                        this.errors.push("No username entered")
                    }
                    // check if password keyed in
                    if (this.password == "") {
                        this.errors.push("No password entered")
                    }

                    // set authentication pending flag to false
                    this.authPending = false
                }

                // [else] all details keyed in
                else {

                    // Check login validity
                    let hashedPassword = this.hashPassword(this.ID, this.password)
                    let loginInfo = { "username": this.ID, "password": hashedPassword }
                    this.auth(loginInfo, "${process.env.VUE_APP_API_URL}/authcheck/authcheck");
                }

            },

            // Authentication
            async auth(loginInfo, authURL) {

                try {
                    const response = await this.$axios.post(authURL, loginInfo);
                    let responseCode = response.data.code

                    // Authentication successful
                    if (responseCode == 200) {
                        this.accountID = response.data.id;
                        this.role = response.data.role;
                        localStorage.setItem("88B_accID", this.accountID);
                        localStorage.setItem("88B_accType", this.role);

                        this.authPending = false
                        this.redirectPage();
                    }
                    // Authentication failed
                    else {
                        this.errors.push(response.data.message)
                        this.authPending = false
                    }
                }
                catch (error) {
                    this.errors.push(error.response.data.message)
                    this.authPending = false
                }

            },

            // create unique hash based on ID and password
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

            redirectPage() {
                // Redirect for selected roles 
                
                // [TODO] change to correct page and use router pushing
                // this.$router.push({path: '/Users/Bottle-Listings'})

                // [User]
                if (this.role == "user") {
                    this.$router.push({path: '/'});
                }
                // [Producer]
                if (this.role == "producer") {
                    this.$router.push({path: `/profile/producer/${this.accountID}`});
                }
                // [Venue]
                if (this.role == "venue") {
                    this.$router.push({path: `/profile/venue`});
                }
            }
        }
    };

</script>