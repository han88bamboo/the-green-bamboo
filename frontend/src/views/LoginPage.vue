<!-- HTML -->
<template>
  <NavBar />

  <div class="body-login background-login">
    <!-- select buttons -->
    <!-- <div class="container row" style="width: 50%"> -->
    <div class="login-header-banner mobile-view-show">
      <img src="@/assets/login-bg.jpg" alt="Banner" />
    </div>
      <div class="container mb-5 mobile-mb-0">
      <div class="row">
        <div class="mobile-col-12 col-8 m-auto mobile-ps-0 mobile-pe-0">
          <div class="pt-5 mobile-pt-0">
            <form
              id="login"
              v-if="!showResetPWForm"
              v-on:submit.prevent="checkLogin"
              class="login-form-box"
            >
              <!-- login header text -->
              <p
                class="fw-bold fs-3 pt-4 mx-3 mobile-fs-5 mb-1"
              >
                A World of Drinks Awaits.
              </p>
              <p
                class="fw-bold mx-4 fs-6 mobile-fs-7"
                style="font-style: italic"
              >
                Discover new juice, find friends and log your tasting notes!
              </p>

              <p class="text-muted small mx-4 mb-2">
                Choose how you want to log in
              </p>

              <!-- Login method toggle -->
              <div class="row">
                <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                  <div class="login-toggle-container">
                    <div 
                      class="login-toggle-option" 
                      :class="{ 'login-toggle-active': loginMethod === 'username' }" 
                      @click="setLoginMethod('username')"
                    >
                      Username
                    </div>
                    <div 
                      class="login-toggle-option" 
                      :class="{ 'login-toggle-active': loginMethod === 'email' }" 
                      @click="setLoginMethod('email')"
                    >
                      Email Address
                    </div>
                  </div>
                </div>
              </div>

              <!-- username -->
              <div class="row pt-3" v-if="loginMethod === 'username'">
                <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                  <div class="form-floating">
                    <input
                      type="text"
                      class="form-control form-box-outline"
                      id="id"
                      placeholder="Username"
                      v-model="ID"
                    />
                    <label for="username"> Username </label>
                  </div>
                </div>
              </div>
              <!-- email -->
              <div class="row pt-3" v-if="loginMethod === 'email'" >
                <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                  <div class="form-floating">
                    <input
                      type="email"
                      class="form-control form-box-outline"
                      id="email"
                      placeholder="Email Address"
                      v-model="email"
                    />
                    <label for="email"> Email Address </label>
                  </div>
                </div>
              </div>

              <!-- password -->
              <div class="row pt-2">
                <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                  <div class="form-floating">
                    <input
                      type="password"
                      class="form-control form-box-outline"
                      id="password"
                      placeholder="Password"
                      v-model="password"
                    />
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
                    <div class="col text-start">
                      <input
                        type="checkbox"
                        v-on:click="showPassword()"
                        class="form-check-input "
                      />
                      <label for="password" class="form-check-label mobile-rating-smaller-text-2">
                        &nbsp; Show password
                      </label>
                    </div>

                    <!-- Column for forget password link -->
                    <div class="col text-end">
                      <p
                        class="default-body-text-no-background mobile-rating-smaller-text-2 hover-text-primary text-decoration-underline"
                        role="button"
                        @click="showResetPWForm = true"
                      >
                        Forgot password?
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- error handling -->
              <div class="row p-3 text-left" v-show="errors.length > 0">
                <div class="d-grid gap-2 col-md-5 col-10 mx-auto">
                  <div class="alert alert-danger" role="alert">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      fill="currentColor"
                      class="bi bi-exclamation-triangle"
                      viewBox="0 0 16 16"
                    >
                      <path
                        d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.146.146 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.163.163 0 0 1-.054.06.116.116 0 0 1-.066.017H1.146a.115.115 0 0 1-.066-.017.163.163 0 0 1-.054-.06.176.176 0 0 1 .002-.183L7.884 2.073a.147.147 0 0 1 .054-.057zm1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566z"
                      />
                      <path
                        d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995z"
                      />
                    </svg>
                    <h5>Error</h5>
                    <li v-for="error in errors" :key="error">{{ error }}</li>
                  </div>
                </div>
              </div>
              <!-- Confirm Selection -->
              <div class="row">
                <div class="col">
                  <button
                    v-if="authPending"
                    type="submit"
                    class="btn secondary-btn btn-sm px-5 fw-bold"
                    disabled
                  >
                    Loading...
                  </button>
                  <button
                    v-else
                    type="submit"
                    class="btn secondary-btn btn-sm px-5 fw-bold"
                  >
                    Log In
                  </button>
                  <GoogleSignIn />
                </div>
              </div>

              <div class="row py-1">
                <div class="col-9 mx-auto">
                  <hr>
                </div>
              </div>

              <!-- Prompt sign up -->
              <p class=" fw-bold fs-4 mobile-fs-5 mb-1">
                Don't have an account?
              </p>
              <p class="fw-bold fst-italic fs-6 mobile-fs-7">
                Get Started! It's Free!
              </p>
              <div class="row">
                <div class="col">
                  <router-link
                    :to="{ path: '/signup' }"
                    class="default-text-no-background"
                  >
                    <button class="btn secondary-btn btn-sm px-5 fw-bold w-50">
                      Sign Up for Free!
                    </button>
                  </router-link>
                </div>
              </div>
              <br>
              <!-- Business sign up -->
              <div class="row pt-4 pb-3">
                <div class="col-10 col-md-8 mx-auto">
                  <div class="business-signup-card">
                    <div class="row">
                      <div class="col-md-8">
                        <h5 class="text-start fw-bold mb-2">Brand or Venue Owner?</h5>
                        <p class="text-start mb-2">Grow your business with a dedicated business profile.</p>
                        <ul class="text-start ps-3 mb-3">
                          <li>Be found by drinks lovers searching for new experiences</li>
                          <li>Showcase your offerings with a customizable menu</li>
                          <li>Connect with your audience and build your community</li>
                        </ul>
                      </div>
                      <div class="col-md-4 d-flex align-items-center justify-content-center">
                        <router-link :to="{ path: '/businessSignup' }" class="d-block w-100">
                          <button class="btn secondary-btn fw-bold py-2 w-100">
                            Drink-X for Business
                          </button>
                        </router-link>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </form>

            <!-- forgot password form-->
            <ForgotPasswordForm
              v-if="showResetPWForm"
              v-on:close="showResetPWForm = false"
              style="background-color: #ddc8a9"
              class="rounded"
              @returnToLogin="hideResetForm"
            />
          </div>
        </div>
      </div>
    </div>
    <FooterBar />
  </div>
</template>

<!-- CSS -->
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

.login-form-box {
  background-color: wheat;
  opacity: 0.97;
}


@media (max-width: 991px) {
  .login-form-box {
    background-color: white;
  }
}

.hover-text-primary:hover {
  color: var(--bs-primary);
}

.background-login {
  background-image: url('@/assets/login-bg.jpg');
  background-size: cover;
  background-position: center;
  min-height: 100vh;
  width: 100%;
  position: relative;
}

@media (max-width: 991px) {
  .background-login {
    background-image: none;
    background-color: white;
  }
}


.business-signup-card {
  background-color: white;
  border: 2px solid #3CB371;
  border-radius: 8px;
  padding: 18px;
  margin-bottom: 10px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
  position: relative;
}

.business-signup-card::before {
  content: "Business";
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

@media (max-width: 767px) {
  .business-signup-card {
    padding: 15px;
  }
  
  .business-signup-card ul {
    margin-bottom: 15px;
  }
}

.login-toggle-container {
  display: flex;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: 1px solid #ddd;
}

.login-toggle-option {
  flex: 1;
  text-align: center;
  padding: 10px 0;
  cursor: pointer;
  font-weight: 500;
  background-color: #f8f9fa;
  transition: all 0.2s ease;
  color: #6c757d;
}

.login-toggle-active {
  background-color: #EBA446;
  color: black;
  font-weight: bold;
}

.login-toggle-option:hover:not(.login-toggle-active) {
  background-color: #e9ecef;
}

</style>

<script>
// import components used
import NavBar from "@/components/NavBar.vue";
import GoogleSignIn from "@/components/GoogleSignIn.vue";
import ForgotPasswordForm from "@/components/ForgotPasswordForm.vue";
import FooterBar from "@/components/FooterBar.vue";

// specify components used
export default {
  name: "LoginPage",
  components: {
    NavBar,
    GoogleSignIn,
    ForgotPasswordForm,
    FooterBar,
  },

  data() {
    return {
      authPending: false,
      accountID: {},
      errors: [],
      loginMethod: 'username',

      // form values
      role: "",
      ID: "",
      email: "",
      password: "",

      // variable to toggle password reset form
      showResetPWForm: false,
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
        this.ID = localStorage.getItem("88B_accUsername");
        this.redirectPage();
      }
    },

    // toggle password visibility
    showPassword() {
      var password = document.getElementById("password");
      if (password.type === "password") {
        password.type = "text";
      } else {
        password.type = "password";
      }
    },

    // Form Submission Function
    checkLogin() {
      // set authentication pending flag to true
      this.authPending = true;
      // clear previous values
      this.errors = [];

      // check if user is already logged in
      this.loginCheck();

      // // Normalize username: trim, remove all spaces and convert to lowercase
      // this.ID = this.ID.trim().replace(/\s+/g, '').toLowerCase();
      
      // Check if either username or email is provided
      if ((this.ID == "" && this.email == "") || this.password == "") {
        // check if both ID and email are empty
        if (this.ID == "" && this.email == "") {
          this.errors.push("Please enter either a username or email address");
        }
        // check if password keyed in
        if (this.password == "") {
          this.errors.push("No password entered");
        }

        // set authentication pending flag to false
        this.authPending = false;
      }

      // [else] required details keyed in
      else {
        // If email is provided, get username from email first
        if (this.email != "") {
          this.getUsernameFromEmail();
        } else {
          // Use username directly
          this.proceedWithLogin(this.ID);
        }
      }
    },

    // Get username from email address
    async getUsernameFromEmail() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUsernameFromEmail/${this.email}`
        );
        
        if (response.data.username) {
          // Save the username to this.ID so it will be stored in localStorage
          this.ID = response.data.username;
          this.proceedWithLogin(response.data.username);
        } else {
          this.errors.push("No account found with this email address");
          this.authPending = false;
        }
      } catch (error) {
        this.errors.push("Error verifying email address");
        this.authPending = false;
      }
    },

    // Proceed with login using username
    async proceedWithLogin(username) {
      try {
        // First get the canonical username from the database
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getCanonicalUsername/${username}`
        );
        if (response.data.username) {
          // Use the canonical username from database for hashing
          const canonicalUsername = response.data.username;

          // Check login validity using the canonical username
          let hashedPassword = this.hashPassword(canonicalUsername, this.password);
          let loginInfo = { 
            username: username, 
            password: hashedPassword, 
            canonicalUsername: canonicalUsername // Send canonical username for verification
          };
          this.auth(
            loginInfo,
            `${process.env.VUE_APP_API_URL}/authcheck/authcheck`
          );
        } else {
          this.errors.push("Error retrieving account information");
          this.authPending = false;
        }
      } catch (error) {
        this.errors.push("Error verifying account information");
        this.authPending = false;
      }
    },

    // Authentication
    async auth(loginInfo, authURL) {
      try {
        const response = await this.$axios.post(authURL, loginInfo);
        let responseCode = response.data.code;

        // Authentication successful
        if (responseCode == 200) {
          this.accountID = response.data.id;
          this.role = response.data.role;
          localStorage.setItem("88B_accID", this.accountID);
          localStorage.setItem("88B_accType", this.role);
          localStorage.setItem("88B_accUsername", this.ID);

          this.authPending = false;
          this.redirectPage();
        }
        // Authentication failed
        else {
          this.errors.push(response.data.message);
          this.authPending = false;
        }
      } catch (error) {
        this.errors.push(error.response.data.message);
        this.authPending = false;
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
        this.$router.push({ path: "/" });
      }
      // [Producer]
      if (this.role == "producer") {
        this.$router.push({
          path: `/profile/producer/${this.accountID}/${this.ID}`,
        });
      }
      // [Venue]
      if (this.role == "venue") {
        this.$router.push({ 
          path: `/profile/venue/${this.accountID}/${this.ID}` 
        });
      }
    },

    // Hide reset password form
    hideResetForm() {
      this.showResetPWForm = false;
    },

    // Set login method (username or email)
    setLoginMethod(method) {
      this.loginMethod = method;
      // Clear both fields when switching
      if (method === 'username') {
        this.email = '';
      } else {
        this.ID = '';
      }
    },
    
  },
};
</script>
