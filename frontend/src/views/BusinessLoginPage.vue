<!-- HTML -->
<template>
  <NavBar />

  <div class="body-login background-login">
    <!-- Business login header banner -->
    <div class="login-header-banner mobile-view-show">
      <img src="@/assets/login-bg.jpg" alt="Banner" />
    </div>
      <div class="container mb-5 mobile-mb-0">
      <div class="row">
        <div class="mobile-col-12 col-8 m-auto mobile-ps-0 mobile-pe-0">
          <div class="pt-5 mobile-pt-0">
            <form
              id="businessLogin"
              v-if="!showResetPWForm"
              v-on:submit.prevent="checkBusinessLogin"
              class="login-form-box business-login-form"
            >
              <!-- Business login header text -->
              <p
                class="fw-bold fs-3 pt-4 mx-3 mobile-fs-5 mb-1"
              >
                Business Portal Access
              </p>
              <p
                class="fw-bold mx-4 fs-6 mobile-fs-7"
                style="font-style: italic"
              >
                {{ getBusinessTaglineText() }}
              </p>

              <p class="text-muted small mx-4 mb-2">
                Business Account Login
              </p>

              <!-- Role tabs -->
              <div class="row">
                <div class="d-grid gap-2 col-xl-6 col-md-8 col-10 mx-auto">
                  <div class="role-tabs-container">
                    <div 
                      class="role-tab-option" 
                      :class="{ 'role-tab-active': selectedRole === 'venue' }" 
                      @click="setSelectedRole('venue')"
                    >
                      Venues & Festivals
                    </div>
                    <div 
                      class="role-tab-option" 
                      :class="{ 'role-tab-active': selectedRole === 'producer' }" 
                      @click="setSelectedRole('producer')"
                    >
                      Brands & Producers
                    </div>
                  </div>
                </div>
              </div>

              <p class="text-muted small mx-4 mb-2 mt-3">
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
                      id="businessId"
                      placeholder="Username"
                      v-model="businessID"
                    />
                    <label for="businessId"> Username </label>
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
                      id="businessEmail"
                      placeholder="Email Address"
                      v-model="businessEmail"
                    />
                    <label for="businessEmail"> Email Address </label>
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
                      id="businessPassword"
                      placeholder="Password"
                      v-model="businessPassword"
                    />
                    <label for="businessPassword"> Password </label>
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
                        v-on:click="showBusinessPassword()"
                        class="form-check-input "
                      />
                      <label for="businessPassword" class="form-check-label mobile-rating-smaller-text-2">
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
              <!-- Business Login Button -->
              <div class="row">
                <div class="col">
                  <button
                    v-if="authPending"
                    type="submit"
                    class="btn business-btn btn-sm px-5 fw-bold"
                    disabled
                  >
                    Loading...
                  </button>
                  <button
                    v-else
                    type="submit"
                    class="btn business-btn btn-sm px-5 fw-bold"
                  >
                    Login
                  </button>
                </div>
              </div>

              <div class="row py-1">
                <div class="col-9 mx-auto">
                  <hr>
                </div>
              </div>

              <!-- Regular User Login -->
              <p class=" fw-bold fs-4 mobile-fs-5 mb-1">
                Not a Business User?
              </p>
              <p class="fw-bold fst-italic fs-6 mobile-fs-7">
                Access the regular user login page.
              </p>
              <div class="row">
                <div class="col">
                  <router-link
                    :to="{ path: '/login' }"
                    class="default-text-no-background"
                  >
                    <button class="btn secondary-btn btn-sm px-5 fw-bold w-50">
                      Regular Login
                    </button>
                  </router-link>
                </div>
              </div>
              <br>

              <div class="row py-1">
                <div class="col-9 mx-auto">
                  <hr>
                </div>
              </div>

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
                          <button class="btn business-btn fw-bold py-2 w-100">
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

.business-login-form {
  background-color: #e3f2fd !important; /* Light blue background for business */
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
  background-color: #007bff;
  color: white;
  font-weight: bold;
}

.login-toggle-option:hover:not(.login-toggle-active) {
  background-color: #e9ecef;
}

.business-btn {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
  border-radius: 25px; /* Same border radius as secondary-btn */
}

.business-btn:hover {
  background-color: #0056b3;
  border-color: #0056b3;
  color: white;
}

.business-btn:focus, .business-btn:active {
  background-color: #0056b3;
  border-color: #0056b3;
  color: white;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.business-role-tabs-container {
  display: flex;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: 1px solid #ddd;
}

.business-role-tab-option {
  flex: 1;
  text-align: center;
  padding: 12px 8px;
  cursor: pointer;
  font-weight: 500;
  background-color: #f8f9fa;
  transition: all 0.2s ease;
  color: #6c757d;
  font-size: 14px;
}

.business-role-tab-active {
  background-color: #007bff;
  color: white;
  font-weight: bold;
}

.business-role-tab-option:hover:not(.business-role-tab-active) {
  background-color: #e9ecef;
}

@media (max-width: 767px) {
  .business-role-tab-option {
    padding: 10px 4px;
    font-size: 12px;
  }
}

.role-tabs-container {
  display: flex;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: 1px solid #ddd;
}

.role-tab-option {
  flex: 1;
  text-align: center;
  padding: 12px 8px;
  cursor: pointer;
  font-weight: 500;
  background-color: #f8f9fa;
  transition: all 0.2s ease;
  color: #6c757d;
  font-size: 14px;
}

.role-tab-active {
  background-color: #0E6350;
  color: white;
  font-weight: bold;
}

.role-tab-option:hover:not(.role-tab-active) {
  background-color: #e9ecef;
}

@media (max-width: 767px) {
  .role-tab-option {
    padding: 10px 4px;
    font-size: 12px;
  }
}

.business-signup-card {
  background-color: white;
  border: 2px solid #007bff;
  border-radius: 8px;
  padding: 18px;
  margin-bottom: 10px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
  position: relative;
}

@media (max-width: 767px) {
  .business-signup-card {
    padding: 15px;
  }
  
  .business-signup-card ul {
    margin-bottom: 15px;
  }
}

</style>

<script>
// import components used
import NavBar from "@/components/NavBar.vue";
import ForgotPasswordForm from "@/components/ForgotPasswordForm.vue";

// specify components used
export default {
  name: "BusinessLoginPage",
  components: {
    NavBar,
    ForgotPasswordForm,
  },

  data() {
    return {
      authPending: false,
      accountID: {},
      errors: [],
      loginMethod: 'username',
      selectedRole: 'venue', // Default to venue for business

      // business form values
      role: "",
      businessID: "",
      businessEmail: "",
      businessPassword: "",

      // variable to toggle password reset form
      showResetPWForm: false,
    };
  },
  mounted() {
    this.businessLoginCheck();
  },
  methods: {
    // Check if business user is already logged in
    businessLoginCheck() {
      if (localStorage.getItem("88B_accID") != null) {
        this.accountID = localStorage.getItem("88B_accID");
        this.role = localStorage.getItem("88B_accType");
        this.businessID = localStorage.getItem("88B_accUsername");
        // Only redirect if it's a business account
        if (this.role === "venue" || this.role === "producer") {
          this.redirectBusinessPage();
        }
      }
    },

    // toggle business password visibility
    showBusinessPassword() {
      var password = document.getElementById("businessPassword");
      if (password.type === "password") {
        password.type = "text";
      } else {
        password.type = "password";
      }
    },

    // Business Form Submission Function
    checkBusinessLogin() {
      // set authentication pending flag to true
      this.authPending = true;
      // clear previous values
      this.errors = [];

      // check if user is already logged in
      this.businessLoginCheck();

      // Check if either username or email is provided
      if ((this.businessID == "" && this.businessEmail == "") || this.businessPassword == "") {
        // check if both ID and email are empty
        if (this.businessID == "" && this.businessEmail == "") {
          this.errors.push("Please enter either a username or email address");
        }
        // check if password keyed in
        if (this.businessPassword == "") {
          this.errors.push("No password entered");
        }

        // set authentication pending flag to false
        this.authPending = false;
      }

      // [else] required details keyed in
      else {
        // If email is provided, get username from email first
        if (this.businessEmail != "") {
          this.getBusinessUsernameFromEmail();
        } else {
          // Use username directly
          this.proceedWithBusinessLogin(this.businessID);
        }
      }
    },

    // Get business username from email address
    async getBusinessUsernameFromEmail() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUsernameFromEmail/${this.businessEmail}`
        );
        
        if (response.data.username) {
          // Save the username to this.businessID so it will be stored in localStorage
          this.businessID = response.data.username;
          this.proceedWithBusinessLogin(response.data.username);
        } else {
          this.errors.push("No business account found with this email address");
          this.authPending = false;
        }
      } catch (error) {
        this.errors.push("Error verifying email address");
        this.authPending = false;
      }
    },

    // Proceed with business login using username
    async proceedWithBusinessLogin(username) {
      try {
        // First get the canonical username from the database
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getCanonicalUsername/${username}`
        );
        if (response.data.username) {
          // Use the canonical username from database for hashing
          const canonicalUsername = response.data.username;

          // Check login validity using the canonical username
          let hashedPassword = this.hashPassword(canonicalUsername, this.businessPassword);
          let loginInfo = { 
            username: username, 
            password: hashedPassword, 
            canonicalUsername: canonicalUsername,
            expectedRole: this.selectedRole // Send expected business role
          };
          this.businessAuth(
            loginInfo,
            `${process.env.VUE_APP_API_URL}/authcheck/businessAuthcheck`
          );
        } else {
          this.errors.push("Error retrieving business account information");
          this.authPending = false;
        }
      } catch (error) {
        this.errors.push("Error verifying business account information");
        this.authPending = false;
      }
    },

    // Business Authentication
    async businessAuth(loginInfo, authURL) {
      try {
        const response = await this.$axios.post(authURL, loginInfo);
        let responseCode = response.data.code;

        // Authentication successful
        if (responseCode == 200) {
          // Verify that the user has business privileges
          if (response.data.role === "venue" || response.data.role === "producer") {
            this.accountID = response.data.id;
            this.role = response.data.role;
            localStorage.setItem("88B_accID", this.accountID);
            localStorage.setItem("88B_accType", this.role);
            localStorage.setItem("88B_accUsername", this.businessID);

            this.authPending = false;
            this.redirectBusinessPage();
          } else {
            this.errors.push("This account does not have business privileges");
            this.authPending = false;
          }
        }
        // Authentication failed
        else {
          this.errors.push(response.data.message);
          this.authPending = false;
        }
      } catch (error) {
        this.errors.push(error.response?.data?.message || "Business authentication failed");
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

    redirectBusinessPage() {
      // Redirect for business roles only
      
      // [Producer]
      if (this.role == "producer") {
        this.$router.push({
          path: `/profile/producer/${this.accountID}/${this.businessID}`,
        });
      }
      // [Venue]
      else if (this.role == "venue") {
        this.$router.push({ 
          path: `/profile/venue/${this.accountID}/${this.businessID}` 
        });
      }
      // [Fallback] - shouldn't happen, but redirect to general business dashboard
      else {
        this.$router.push({ 
          path: `/business-dashboard` 
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
        this.businessEmail = '';
      } else {
        this.businessID = '';
      }
    },

    // Get business tagline text based on selected role
    getBusinessTaglineText() {
      switch(this.selectedRole) {
        case 'venue':
          return 'Bring more thirsty patrons through your doors';
        case 'producer':
          return 'Put your brand under the spotlight';
        default:
          return 'Access your Venue or Brand account here.';
      }
    },

    // Set selected role
    setSelectedRole(role) {
      this.selectedRole = role;
    },
    
  },
};
</script>
