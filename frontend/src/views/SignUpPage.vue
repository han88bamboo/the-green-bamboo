<!-- HTML -->
<template>
  <NavBar />

  <!-- Display when data is still loading -->
  <div
    class="text-info-emphasis fst-italic fw-bold fs-5 pt-5"
    v-if="dataLoaded == false"
  >
    <span>Loading page, please wait...</span>
    <br /><br />
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>

  <!-- Display when data fails to load -->
  <div
    class="text-danger fst-italic fw-bold fs-3 pt-5"
    v-if="dataLoaded == null"
  >
    <span>An error occurred while loading this page, please try again!</span>
    <br />
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
    <br /><br />
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>

  <!-- Display when sign up is successful -->
  <div class="text-success fw-bold fs-5" v-if="successSubmission">
    <div class="login-header-banner mb-3">
      <img src="@/assets/signup-error.jpg" alt="Banner" />
    </div>
    <span class="pt-3 fw-bold mobile-rating-smaller-text-2">Your account has successfully been created!</span>
    <button class="btn primary-btn btn-sm mt-0 mb-3" @click="loginUser">
      <span class="fs-6">
        Let the good times roll!
      </span>
    </button>
  </div>

  <!-- Display when login encounters an error -->
  <div class="text-danger fw-bold fs-5 mt-2" v-if="loginError">
    <span>An error occurred while attempting to login!</span>
    <br />
    <button class="btn primary-btn btn-sm" @click="reset">
      <router-link :to="{ path: '/login' }" class="primary-clickable-text">
        <span class="fs-5 fst-italic" style="color: white">
          Click to login here!
        </span>
      </router-link>
    </button>
  </div>

  <!-- Display when sign up encounters an error -->
  <div class="text-danger fw-bold fs-5" v-if="errorSubmission">
    <div class="login-header-banner mb-3">
      <img src="@/assets/signup-error.jpg" alt="Banner" />
    </div>
    <h5 class="pt-3 fw-bold mobile-rating-smaller-text-2" v-if="errorMessage"
      >Oops! An error occured while creating account, please try
      again!</h5>
    <h5 class="pt-3 fw-bold mobile-rating-smaller-text-2" v-if="duplicateEntry">The credentials you used have already been taken! Please try a different username / email address!</h5>
    <button class="btn primary-btn btn-sm mt-0 mb-3" @click="reset">
      <span class="fs-6"> Retry sign up again! </span>
    </button>
  </div>
  
  
  <div class="body-login background-login" v-if="fillForm && dataLoaded">
    <div class="login-header-banner mobile-view-show">
      <img src="@/assets/login-bg.jpg" alt="Banner" />
  </div>
    <div class="container rounded mobile-ps-0 mobile-pe-0">
      <div class="row">
        <div class="col-12 col-sm-10 col-md-8 m-auto">
          <div class="py-5 mobile-pt-0">
            <div>
              <div
                class="login-form-box"
              >
                <div class="d-grid gap-2" style="position: relative">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="30"
                    height="30"
                    fill="currentColor"
                    class="ms-5 bi bi-arrow-left-circle mobile-view-hide"
                    viewBox="0 0 16 16"
                    style="position: absolute; top: 25; left: 10"
                    v-on:click="goBack"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-4.5-.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"
                    />
                  </svg>
                  <p
                    class="fw-bold fs-3 pt-4 mx-3 mobile-fs-5 mb-1"
                  >
                    Create Your Account
                  </p>
                  <p
                    class="fw-bold mx-4 fs-6 mobile-fs-7"
                    style="font-style: italic"
                  >
                    Discover new juice and log your tasting notes!
                  </p>
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
                  <div class="row pt-2">
                    <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                      <div class="form-floating">
                        <input
                          type="text"
                          class="form-control form-box-outline"
                          v-model="username"
                          id="username"
                          placeholder="Username"
                        />
                        <label for="username"> Username </label>
                        <span v-if="missingUsername" class="text-danger"
                          >Please enter a username.</span
                        >
                        <span v-if="duplicateUser" class="text-danger"
                          >Username is already taken, if this is you, login
                          instead!</span
                        >
                        <span v-if="invalidUsernameFormat" class="text-danger"
                          >Username can only contain letters and numbers (no spaces or special characters).</span
                        >
                      </div>
                    </div>
                  </div>
                  <!-- Input: Email -->
                  <div class="row pt-2">
                    <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                      <div class="form-floating">
                        <input
                          type="text"
                          class="form-control form-box-outline"
                          v-model="email"
                          id="email"
                          placeholder="Email"
                        />
                        <label for="email"> Email </label>
                        <span v-if="missingEmail" class="text-danger"
                          >Please enter an email.</span
                        >
                        <span v-if="invalidEmail" class="text-danger"
                          >Please enter a valid email.</span
                        >
                      </div>
                    </div>
                  </div>

                  <!-- Input: Password with strength check -->
                  <div class="row pt-2">
                    <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                      <!-- <PWStrengthChecker v-model="password"/> -->
                      <!-- Listen to individual events -->
                      <PWStrengthChecker 
                        @password-change="password = $event"
                        @strength-change="passwordStrength = $event"
                      />
                      <span v-if="missingPassword" class="text-danger">
                        Please enter a password.
                      </span>
                      <span v-if="weakPassword && !missingPassword" class="text-danger">
                        Please use password that meets the requirement.
                      </span>
                    </div>
                  </div>                 
                  
                  <!-- Input: Repeat Password -->
                  <div class="row pt-2">
                    <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                      <div class="form-floating">
                        <input
                          type="password"
                          class="form-control form-box-outline"
                          v-model="passwordRepeat"
                          id="passwordRepeat"
                          placeholder="Repeat Password"
                        />
                        <label for="passwordRepeat"> Repeat Password </label>
                        <span
                          v-if="missingPasswordRepeat && !missingPassword"
                          class="text-danger"
                          >Please repeat your password.</span
                        >
                        <span
                          v-if="passwordMismatch && !missingPasswordRepeat"
                          class="text-danger"
                          >Passwords do not match, please try again.</span
                        >
                      </div>
                    </div>
                  </div>
                  <!-- Input: Country -->
                  <div class="row pt-2">
                    <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                      <div class="form-floating" style="position: relative;">
                        <div class="input-group mb-0">
                          <span class="input-group-text" id="basic-addon1"
                            >Country</span
                          >
                          <!-- Searchable input that opens country dropdown -->
                          <input
                            ref="countryInput"
                            type="text"
                            class="form-control form-box-outline"
                            v-model="countryInputValue"
                            placeholder="Select your country"
                            @input="handleCountryInput"
                            @focus="openCountryDrawer"
                            style="cursor: text; background-color: white;"
                          />
                          <!-- Search icon -->
                          <span class="input-group-text" style="cursor: pointer;" @click="openCountryDrawer">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                              <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
                            </svg>
                          </span>
                        </div>
                        
                        <!-- Country Selection Dropdown - attached directly below input -->
                        <div v-if="showCountryDrawer" class="country-dropdown">
                          <div class="country-dropdown-body">
                            <div 
                              v-for="country in filteredCountries" 
                              :key="country.originCountry"
                              class="country-item"
                              @click="selectCountry(country.originCountry)"
                            >
                              <span class="country-name">{{ country.originCountry }}</span>
                              <svg v-if="selectedCountry === country.originCountry" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="check-icon" viewBox="0 0 16 16">
                                <path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.061L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z"/>
                              </svg>
                            </div>
                            <div v-if="filteredCountries.length === 0" class="no-results">
                              No countries found
                            </div>
                          </div>
                        </div>

                        <span
                          v-if="missingCountry"
                          class="text-danger mt-0 mb-3"
                          >Please select your country.</span
                        >
                      </div>
                    </div>
                  </div>
                  <!-- Input: Birthday -->
                  <div class="row pt-2">
                    <div class="d-grid gap-2 col-xl-5 col-md-7 col-9 mx-auto">
                      <div class="form-floating">
                        <div class="input-group mb-0">
                          <span class="input-group-text" id="basic-addon1"
                            >Birthday</span
                          >
                          <input
                            type="date"
                            class="form-control form-box-outline"
                            v-model="birthday"
                            id="birthday"
                            placeholder="Birthday"
                          />
                        </div>
                        <div class="text-center mb-3">
                          <span
                            v-if="missingBirthday"
                            class="text-danger mt-0 mb-3"
                            >Please enter your birthday.</span
                          >
                          <span v-if="underAge" class="text-danger mt-0 mb-3"
                            >You are underage, creation of account is not
                            allowed.</span
                          >
                          <span
                            v-if="illegalCountry"
                            class="text-danger mt-0 mb-3"
                            >It is illegal to drink in your country, creation of
                            account is not allowed.</span
                          >
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Age Verification Section -->
                  <!-- ORIGINAL CHECKBOX VERSION (COMMENTED OUT) -->
                  <!--
                  <div class="text-center mt-3 col mx-3 mobile-fs-7">
                    <div class="form-check form-check-inline">
                      <label class="form-check-label"
                        >I verify I am above legal drinking age in my country of
                        location</label
                      >
                      <input
                        class="form-check-input"
                        type="checkbox"
                        v-model="ageCheck"
                      />
                    </div>
                  </div>
                  <div class="text-center mb-3">
                    <span v-if="missingAgeCheck" class="text-danger"
                      >Please verify this.</span
                    >
                  </div>
                  -->

                  <!-- SIMPLIFIED VERSION (CURRENT) -->
                  <div class="text-center mt-3 col mx-3 mobile-fs-7">
                    <p class="fw-normal fs-6 mobile-fs-7 text-muted">
                      By signing up, you verify you are of legal drinking age in your country.
                    </p>
                  </div>

                  <button
                    type="submit"
                    class="btn secondary-btn btn-sm px-5 fw-bold"
                    @click="signUp"
                  >
                    Sign Up
                  </button>
                  <!-- <button type="button" class="btn primary-btn mx-1 mb-3" @click="goBack">Return</button> -->
                </form>
                <div class="col mx-3">
                  <b>
                    <i>
                      <p class="fw-bold m-4 fs-6 mobile-fs-7">
                        If you are a drinks brand, bottler or venue owner trying
                        to create an account,
                        <router-link
                          :to="{
                            path: '/businessSignup',
                          }"
                          class="default-body-text-no-background"
                          >click here</router-link
                        >.
                      </p>
                      <p class="fw-bold m-4 fs-6 mobile-fs-7 pb-5">
                        If you already have an account and would like to login,
                        <router-link
                          :to="{ path: '/login' }"
                          class="default-body-text-no-background"
                          >click here</router-link
                        >.
                      </p>
                    </i>
                  </b>
                </div>
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
  <!-- Footer End -->
  <!-- Popup 1 -->
    <!-- End of display -->
  <!-- Footer End -->
  
  <!-- ========== POPUP WORKFLOW COMMENTED OUT FOR SHORT CIRCUIT ========== -->
  <!-- ORIGINAL WORKFLOW: Popup 1 → Popup 2 → Popup 3 → Preferences Update → Onboarding -->
  <!-- NEW WORKFLOW: Skip directly to auto-login after account creation -->
  
  <!-- Popup 1 -->
  <!--
  <ReusablePopup
    v-if="showPopup1"
    :isVisible="true"
    title="Create your profile and build your taste palate!"
    question="What's your drink of choice?"
    note="(Please pick at least 1 drink)"
    :options="drinkType"
    :preselectedOptions="selectedDrinks"
    :minSelections="1"
    nextButtonText="Next"
    @updateSelection="selectedDrinks = $event"
    @next="goToPopup2"
  />
  -->

  <!-- Popup 2 -->
  <!--
  <ReusablePopup
    v-if="showPopup2"
    :isVisible="true"
    title="Create your profile and build your taste palate!"
    question="What types of flavours do you usually prefer?"
    note="(Please pick at least 3 flavours)"
    :options="flavourTags"
    :preselectedOptions="selectedFlavors"
    :minSelections="3"
    showBackButton
    @updateSelection="selectedFlavors = $event"
    @back="
      showPopup1 = true;
      showPopup2 = false;
    "
    @next="goToPopup3"
  />
  -->

  <!-- Popup 3 -->
  <!--
  <ReusablePopup
    v-if="showPopup3"
    :isVisible="true"
    title="Create your profile and build your taste palate!"
    question="Which of these drinks would you most like to try?"
    note="(Please pick at least 1 category)"
    :options="observationTags"
    showBackButton
    nextButtonText="Done"
    @back="goToPopup2From3"
    @next="completeSetup"
  />
  -->

  <!-- Onboarding Popup -->
  <!--
  <OnboardPopup
    v-if="showOnboardPopup"
    :isVisible="true"
    title="Now it's time to log your first review!"
    message="Search for a drink and share your review with the community!"
    @close="loginUser"
    @search="goSearch"
  /> -->
        <!-- Onboarding Popup 
  <OnboardPopup
    v-if="showOnboardPopup"
    :isVisible="true"
    title="Now it’s time to log your first review!"
    message="Search for a drink and share your review with the community!"
    @close="loginUser"
    @search="goSearch"
  />-->

</template>


<!-- ------------------------------------------------------------------------------ -->

<!-- JavaScript -->
<script>
// import components used
import NavBar from "@/components/NavBar.vue";
import PWStrengthChecker from "@/components/PWStrengthChecker.vue";
// POPUP COMPONENTS COMMENTED OUT FOR SHORT CIRCUIT WORKFLOW
// import ReusablePopup from "@/components/ReusablePopup.vue";
// import OnboardPopup from "@/components/OnboardPopup.vue";

export default {
  name: "SignUpPage",
  components: {
    NavBar,
    PWStrengthChecker,
    // POPUP COMPONENTS COMMENTED OUT
    // ReusablePopup,
    // OnboardPopup
  },
  data() {
    return {
      dataLoaded: false,
      showPopup1: false,
      showPopup2: false,
      showPopup3: false,
      showOnboardPopup: false,

      // Initial user variable
      response: [],

      // Form variables
      username: "",
      displayName: "",
      email: "",
      password: "",
      passwordStrength: 0,
      passwordRepeat: "",
      firstName: "",
      lastName: "",
      birthday: "",
      ageCheck: "",
      selectedCountry: "",

      countries: [],
      // Country drawer functionality
      showCountryDrawer: false,
      countryInputValue: "", // The actual input value that user types
      filteredCountries: [],
      // Submission variables
      selectedDrinks: [], // Stores selections from Popup 1
      selectedFlavors: [], // Stores selections from Popup 2

      missingUsername: false,
      missingEmail: false,
      invalidEmail: false,
      invalidUsernameFormat: false, // Add this new line
      passwordMismatch: false,
      missingPassword: false,
      weakPassword: false,
      missingPasswordRepeat: false,
      missingFirstName: false,
      missingLastName: false,
      missingBirthday: false,
      missingAgeCheck: false,
      duplicateUser: false,
      missingCountry: false,
      underAge: false,
      illegalCountry: false,

      submitForm: false,
      successSubmission: false,
      errorSubmission: false,
      errorMessage: false,
      duplicateEntry: false,
      fillForm: true,
      reviewResponseCode: "",
      loginError: false,
      flavourTags: [], // Store the flavour tags from database
      observationTags: [], // Store the observation tags from database
      drinkType: [], // Store the drink type from database
    };
  },
  mounted() {
    this.loadData();
    this.loadSignupEmail();
  },
  beforeUnmount() {
    // Clean up event listener when component is destroyed
    document.removeEventListener('click', this.handleClickOutside);
  },
  watch: {
    // Keep input value synced with selected country
    selectedCountry(newVal) {
      if (newVal && this.countryInputValue !== newVal) {
        this.countryInputValue = newVal;
      }
    }
  },
  methods: {
    // Load signup email from localStorage if it exists and clear it after use
    loadSignupEmail() {
      const storedEmail = localStorage.getItem('88B_signupEmail');
      if (storedEmail) {
        this.email = storedEmail;
        // Clear the stored email after loading it to prevent it from being used again
        localStorage.removeItem('88B_signupEmail');
      }
    },

    async loadData() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getCountries`
        ); // use await
        this.countries = response.data.sort((a, b) => {
          return a.originCountry.localeCompare(b.originCountry);
        });
        this.dataLoaded = true;
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
      
      // ========== POPUP DATA LOADING COMMENTED OUT FOR SHORT CIRCUIT ==========
      // No longer need to load drink types, flavour tags, or observation tags
      // since popup workflow has been bypassed
      
      /*
      // get the drink types from database
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getDrinkTypes`
        ); // comment out for local
        // const response = await this.$axios.get(
        //     `http://127.0.0.1:5000/getData/getDrinkTypes`
        // ); // comment out for deployment
        // Set drinkType dynamically based on the API response
        this.drinkType = response.data.map((item) => item.drinkType);

        // Log the transformed array
        console.log("Updated Drink type:", this.drinkType);
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
      // get the flavourTags from database
      try {
        // const response =  `${process.env.VUE_APP_API_URL}/getData/getFlavourTags`  // comment out for local
        // const response = await this.$axios.get(
        //     `http://127.0.0.1:5000/getData/getFlavourTags`
        // ); // comment out for deployment
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getFlavourTags`
        ); // use await
        // Set flavourTags dynamically based on the API response
        this.flavourTags = response.data.map((item) => item.familyTag);

        // Log the transformed array
        console.log("Updated Flavour Tags:", this.flavourTags);
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
      // get the observationTags from database
      try {
        // const response =  `${process.env.VUE_APP_API_URL}/getData/getObservationTags`  // comment out for local
        // const response = await this.$axios.get(
        //     `http://127.0.0.1:5000/getData/getObservationTags`
        // ); // comment out for deployment
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getObservationTags`
        ); // use await
        // Set flavourTags dynamically based on the API response
        this.observationTags = response.data.map((item) => item.observationTag);

        // Log the transformed array
        console.log("Updated Observation Tags:", this.observationTags);
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
      */
    },

    // Country Drawer Methods
    openCountryDrawer() {
      this.showCountryDrawer = true;
      this.filteredCountries = [...this.countries];
      this.$nextTick(() => {
        // Add click outside listener
        document.addEventListener('click', this.handleClickOutside);
      });
    },

    closeCountryDrawer() {
      this.showCountryDrawer = false;
      this.filteredCountries = [];
      // Remove click outside listener
      document.removeEventListener('click', this.handleClickOutside);
    },

    handleCountryInput() {
      // Open dropdown when user starts typing
      if (!this.showCountryDrawer) {
        this.openCountryDrawer();
      }
      // Filter countries based on input
      this.filterCountries();
    },

    filterCountries() {
      const searchTerm = this.countryInputValue.toLowerCase();
      this.filteredCountries = this.countries.filter(country =>
        country.originCountry.toLowerCase().includes(searchTerm)
      );
    },

    handleClickOutside(event) {
      // Check if click was outside the dropdown and input field
      const dropdown = event.target.closest('.country-dropdown');
      const input = event.target.closest('.input-group');
      if (!dropdown && !input) {
        this.closeCountryDrawer();
      }
    },

    selectCountry(countryName) {
      this.selectedCountry = countryName;
      this.countryInputValue = countryName; // Update the input field with selected country
      this.closeCountryDrawer();
    },

    clearCountrySearch() {
      this.countrySearchTerm = "";
      this.filteredCountries = [...this.countries];
      if (this.$refs.countrySearchInput) {
        this.$refs.countrySearchInput.focus();
      }
    },

    goBack() {
      this.$router.go(-1);
    },
    signUp() {
      // Reset all errors/success message, just in case
      this.resetError();

      // Form validation
      let errorCount = 0;

      // username validation
      if (this.username == "") {
        this.missingUsername = true;
        errorCount++;
      } else {
        // Trim username before checking
        this.username = this.username.trim();

        // Check username format
        if (!this.validateUsername(this.username)) {
          this.invalidUsernameFormat = true;
          errorCount++;
        } else {
          // Only check for duplicates if format is valid
          this.checkUsername(this.username);
          if (this.duplicateUser) {
            errorCount++;
          }
        }

        // this.checkUsername(this.username);
        // if (this.duplicateUser) {
        //   errorCount++;
        // }
      }

      // Email validation
      if (this.email == "") {
        this.missingEmail = true;
        errorCount++;
      } else if (!this.email.match(".+@.+..+")) {
        this.invalidEmail = true;
        errorCount++;
      }
      // Password validation
      if (this.password !== this.passwordRepeat) {
        this.passwordMismatch = true;
        errorCount++;
      } else{
        if (this.passwordStrength < 5) {
          this.weakPassword = true;
          errorCount++;}
      }

      if (this.password == "") {
        this.missingPassword = true;
        errorCount++;
      }
      if (this.passwordRepeat == "") {
        this.missingPasswordRepeat = true;
        errorCount++;
      }
      // country validation
      if (this.selectedCountry == "") {
        this.missingCountry = true;
        errorCount++;
      }

      // Birthday validation
      if (this.birthday == "") {
        this.missingBirthday = true;
        errorCount++;
      }

      // Uncomment to allow age checker
      else {
        var dob = new Date(this.birthday);
        var now = new Date();
        var age = now.getFullYear() - dob.getFullYear();
        // Check if the birthday has occurred this year
        if (
          now.getMonth() < dob.getMonth() ||
          (now.getMonth() === dob.getMonth() && now.getDate() < dob.getDate())
        ) {
          age--;
        }
        let searchResult = this.countries.filter((country) => {
          return country.originCountry == this.selectedCountry;
        });
        if (age < searchResult[0]["legalAge"]) {
          this.underAge = true;
          errorCount++;
        } else if (searchResult[0]["legalAge"] == "Prohibited") {
          this.illegalCountry = true;
          errorCount++;
        }
      }

      // Age Check validation - ORIGINAL VERSION (COMMENTED OUT)
      /*
      if (!this.ageCheck) {
        this.missingAgeCheck = true;
        errorCount++;
      }
      */

      // Age verification is now automatic through text acknowledgment
      // Removed checkbox validation as it's no longer required

      if (errorCount > 0) {
        return null;
      }

      // Set default values for optional fields if they are empty
      let firstName = this.firstName.trim() === "" ? "InsertFirstName" : this.firstName;
      let lastName = this.lastName.trim() === "" ? "InsertLastName" : this.lastName;

      let hashedPassword = this.hashPassword(this.username, this.password);
      let joinDate = new Date().toISOString();
      let submitAPI = `${process.env.VUE_APP_API_URL}/createAccount/createAccount`; // comment out for local
      // let submitAPI = "http://127.0.0.1:5000/createAccount/createAccount"; // comment our for deployment
      let submitData = {
        // pass in first name, last name, email, isadmin
        username: this.username,
        displayName: this.username,
        firstName: firstName,
        lastName: lastName,
        email: this.email,
        choiceDrinks: [],
        drinkLists: {
          "Drinks I Have Tried": {
            listDesc: "",
            listItems: [],
          },
          "Drinks I Want To Try": {
            listDesc: "",
            listItems: [],
          },
        },
        modType: [],
        photo: "",
        hashedPassword: hashedPassword.toString(),
        joinDate: joinDate,
        followLists: {
          users: [],
          producers: [],
          venues: [],
        },
        birthday: this.birthday,
        country: this.selectedCountry,
        isAdmin: false,
        choiceFlavours: [],
        preferences: [],
      };
      console.log("=== SIGNUP PAYLOAD ===");
      console.log(JSON.stringify(submitData, null, 2));
      this.createAccount(submitAPI, submitData);
    },
    async createAccount(submitAPI, submitData) {
      this.submitForm = true;
      this.fillForm = false;
      try {
        const response = await this.$axios
          .post(submitAPI, submitData)
          .then((response) => {
            this.reviewResponseCode = response.data.code;
          })
          .catch((error) => {
            console.error(error);
            this.reviewResponseCode = error.response.data.code;
            this.submitForm = false;
          });
        if (this.reviewResponseCode == 201) {
          this.successSubmission = true; // Display success message
          this.submitForm = false; // Hide submission in progress message

          // SHORT CIRCUIT: Skip popup workflow and go directly to login
          // Comment out popup workflow to streamline signup process
          // this.showPopup1 = true;
          // this.showPopup2 = false;
          // this.showPopup3 = false;
          
          // Auto-login user directly after successful account creation
          this.loginUser();
        } else {
          this.errorSubmission = true; // Display error message
          this.submitForm = false; // Hide submission in progress message

          if (this.reviewResponseCode == 400) {
            this.duplicateEntry = true; // Display duplicate entry message
          } else {
            this.errorMessage = true; // Display generic error message
          }
        }
        return response;
      } catch (error) {
        console.error(error);
        this.errorSubmission = true;
        this.errorMessage = true;
        this.submitForm = false;
      }
    },
    
    // ========== POPUP WORKFLOW METHODS COMMENTED OUT FOR SHORT CIRCUIT ==========
    // These methods handled the 3-step preference collection after account creation
    // Commented out to streamline signup process: Account Creation → Auto-Login → Profile
    
    /*
    goToPopup2(selectedOptions = []) {
      if (selectedOptions.length >= 1) {
        this.selectedDrinks = selectedOptions;
        this.showPopup1 = false;
        this.showPopup2 = true;
      } else {
        alert("Please select at least 1 drink option.");
      }
    },
    goToPopup3(selectedOptions) {
      if (selectedOptions.length >= 3) {
        this.selectedFlavors = selectedOptions;
        this.showPopup2 = false;
        this.showPopup3 = true;
      } else {
        alert("Please select at least 3 flavors.");
      }
    },
    async completeSetup(selectedOptions) {
      this.selectedPreferences = selectedOptions;
      console.log("Final selections:", {
        user: this.username,
        drinks: this.selectedDrinks,
        flavors: this.selectedFlavors,
        preferences: this.selectedPreferences,
      });
      this.showOnboardPopup = true;
      this.showPopup3 = false;
      let submitData = {
        choiceDrinks: this.selectedDrinks,
        choiceFlavours: this.selectedFlavors,
        preferences: this.selectedPreferences,
      };
      try {
        // let submitAPI = `http://127.0.0.1:5000/createAccount/addPreferences/${this.username}`; // comment out for deployment
        let submitAPI = `${process.env.VUE_APP_API_URL}/createAccount/addPreferences/${this.username}`; // comment out for local
        const response = await this.$axios.post(submitAPI, submitData);

        return response;
      } catch (error) {
        console.error(error);
        this.errorSubmission = true;
        this.errorMessage = true;
        this.submitForm = false;
      }
    },
    goToPopup1() {
      this.showPopup2 = false;
      this.showPopup1 = true;
    },
    goToPopup2From3() {
      this.showPopup3 = false;
      this.showPopup2 = true;
    },
    closePopup() {
      this.showPopup1 = false;
      this.showPopup2 = false;
      this.showPopup3 = false;
      this.showOnboardPopup = false;
    },
    */
    // goToPopup2() {
    // this.showPopup1 = false;
    // this.showPopup2 = true;
    // this.showPopup3 = false;
    // },
    // goToPopup3() {
    // this.showPopup2 = false;
    // this.showPopup3 = true;
    // },
    // goToOnboardPopup() {
    // this.showPopup3 = false;
    // this.showOnboardPopup = true;
    // },
    // goToPopup1() {
    // this.showPopup2 = false;
    // this.showPopup1 = true;
    // },
    // completeSetup() {
    // this.showPopup3 = false;
    // this.showOnboardPopup = true;
    // console.log("Signup process completed!");
    // },
    // closePopup() {
    // this.showPopup1 = false;
    // this.showPopup2 = false;
    // this.showPopup3 = false;
    // this.showOnboardPopup = false;
    // },

    // create unique hash based on username and password
    hashPassword(username, password) {
      // trim username to ensure consistent hashing
      const trimmedUsername = username.toString().trim();
      const combinedString = trimmedUsername + password;
      let hash = 0;

      for (let i = 0; i < combinedString.length; i++) {
        const char = combinedString.charCodeAt(i);
        hash = (hash << 5) - hash + char;
        hash |= 0; // convert to 32-bit integer
      }

      return hash;
    },
    reset() {
      this.fillForm = true;
      this.errorMessage = false;
      this.errorSubmission = false;
      this.duplicateEntry = false;
      this.successSubmission = false;
    },
    resetError() {
      this.missingUsername = false;
      this.missingEmail = false;
      this.invalidEmail = false;
      this.invalidUsernameFormat = false; 
      this.passwordMismatch = false;
      this.missingPassword = false;
      this.missingPasswordRepeat = false;
      this.missingBirthday = false;
      // this.missingAgeCheck = false; // COMMENTED OUT - no longer using checkbox
      this.missingCountry = false;
      this.underAge = false;
    },

    async checkUsername(username) {
      try {
        // const response = await this.$axios.get(
        //     `http://127.0.0.1:5000/getData/getUsers`
        // );

        // Trim whitespace from username
        const trimmedUsername = username.trim();
    
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUsers`
        );
        let duplicateUser = response.data.filter((user) => {
          return user.username == trimmedUsername;
        });

        if (duplicateUser.length == 0) {
          this.duplicateUser = false;
        } else {
          this.duplicateUser = true;
        }
      } catch (error) {
        console.error(error);
      }
    },

    validateUsername(username) {
      // Only allow letters and numbers (no spaces, special chars, or accented chars)
      const regex = /^[a-zA-Z0-9]+$/;
      return regex.test(username);
    },

    async loginUser() {
      // Get specific user by username and set local storage then redirect
      try {
        // const submitURL =
        //     `http://127.0.0.1:5000/getData/getUserByUsername/` +
        //     this.username;
        const submitURL =
          `${process.env.VUE_APP_API_URL}/getData/getUserByUsername/` +
          this.username;
        const response = await this.$axios.get(submitURL);

        if (response.data.username.toLowerCase() == this.username.toLowerCase()) {
          const userID = response.data["id"];
          const accUsername = response.data["username"];

          localStorage.setItem("88B_accID", response.data["id"]);
          localStorage.setItem("88B_accType", "user");
          localStorage.setItem("88B_accUsername", response.data["username"]);

          // Check for stored redirect URL from venue signup
          const redirectUrl = sessionStorage.getItem('88B_postSignupRedirectUrl');
          if (redirectUrl) {
            console.log('🔗 Found stored redirect URL, redirecting to:', redirectUrl);
            // Remove the stored URL to prevent future unintended redirects
            sessionStorage.removeItem('88B_postSignupRedirectUrl');
            // Redirect to the stored venue page URL
            window.location.href = redirectUrl;
            return;
          }

          //   this.$router.push({
          //     name: "profileuser",
          //     params: {
          //       userID: response.data["id"],
          //       username: response.data["username"],
          //     },
          //   });

          // Default redirect to user profile if no stored redirect URL
          this.$router.push(`/profile/user/${userID}/${accUsername}`);
        }
      } catch (error) {
        console.error(error);
        this.loginError = true;
        this.successSubmission = false;
      }
    },
    
    // ========== SEARCH METHOD COMMENTED OUT (USED IN ONBOARDING POPUP) ==========
    /*
    async goSearch(searchInput) {
      // const submitURL =
      //         `http://127.0.0.1:5000/getData/getUserByUsername/` +
      //         this.username;
      const trimmedUsername = this.username.trim();
      const submitURL =
        `${process.env.VUE_APP_API_URL}/getData/getUserByUsername/` +
        trimmedUsername;
      const response = await this.$axios.get(submitURL);
      if (response.data.username == this.username) {
        localStorage.setItem("88B_accID", response.data["id"]);
        localStorage.setItem("88B_accType", "user");
        localStorage.setItem("88B_accUsername", response.data["username"]);
      }
      if (searchInput.trim() !== "") {
        // Remove any '/' from search input
        searchInput = searchInput.replace(/\//g, "");
        // If already on search page, refresh the page with new search input
        if (this.$route.path.startsWith("/search")) {
          window.location.href = `/search/${searchInput}`;
        } else {
          // Re-route to search page
          this.$router.push({ path: `/search/${searchInput}` });
        }
      }
    },
    */
  },
};
</script>

<style scoped>
.login-header-banner {
  position: relative;
  width: 100%;
  padding-top: calc(3 / 6 * 100%); /* 2:6 aspect ratio = 33.33% */
  overflow: hidden;
}

@media (min-width: 768px) {
  .login-header-banner {
    padding-top: 16.67%; /* 1:6 ratio for tablets and up */
  }
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

/* Country Dropdown Styles */
.country-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1050;
  max-height: 300px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.country-dropdown-body {
  flex: 1;
  overflow-y: auto;
  max-height: 240px;
}

.country-item {
  padding: 10px 12px;
  cursor: pointer;
  transition: background-color 0.15s ease;
  border-bottom: 1px solid #f5f5f5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.country-item:hover {
  background-color: #f8f9fa;
}

.country-item:last-child {
  border-bottom: none;
}

.country-name {
  font-size: 14px;
  color: #333;
}

.check-icon {
  color: #28a745;
  flex-shrink: 0;
  margin-left: 8px;
}

.no-results {
  padding: 15px 12px;
  text-align: center;
  color: #666;
  font-style: italic;
  font-size: 14px;
}

/* Responsive adjustments */
@media (max-width: 767px) {
  .country-dropdown {
    max-height: 250px;
  }
  
  .country-dropdown-body {
    max-height: 190px;
  }
}
</style>