<!-- src/components/admin/AddBusinessModal.vue -->
<template>
  <teleport to="body">
    <div class="modal fade show d-block" tabindex="-1" data-bs-backdrop="static">
      <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add a Business</h5>
            <button type="button" class="btn-close" @click="close" aria-label="Close"></button>
          </div>
          <div class="modal-body">
        
            <!-- Success Message -->
            <div v-if="successMessage" class="alert alert-success">
              <p class="fw-bold">Business account created successfully!</p>
              <p>Please save the temporary login details below. This is the only time the password will be shown.</p>
              <hr>
              <p><strong>Username:</strong> {{ createdBusiness.username }}</p>
              <p><strong>Password:</strong> {{ createdBusiness.tempPassword }}</p>
              <button type="button" class="btn btn-sm btn-secondary" @click="downloadCSV">Download login details</button>
            </div>

            <!-- Error Message -->
            <div v-if="error" class="alert alert-danger">{{ error }}</div>

            <!-- Form -->
            <form v-if="!successMessage" @submit.prevent="createBusiness">
              <!-- Business Type -->
              <div class="mb-3">
                <label class="form-label fw-bold">Profile Type <span class="text-danger">*</span></label>
                <div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" id="typeProducer" value="producer" v-model="form.type">
                    <label class="form-check-label" for="typeProducer">Brand/Producer</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" id="typeVenue" value="venue" v-model="form.type">
                    <label class="form-check-label" for="typeVenue">Venue</label>
                  </div>
                </div>
              </div>

              <!-- Independent Bottler (Producer only) -->
              <div v-if="form.type === 'producer'" class="mb-3">
                <label class="form-label fw-bold">Independent Bottler <span class="text-danger">*</span></label>
                <div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" id="independentBottlerYes" value="true" v-model="form.independentBottler">
                    <label class="form-check-label" for="independentBottlerYes">Yes</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" id="independentBottlerNo" value="false" v-model="form.independentBottler">
                    <label class="form-check-label" for="independentBottlerNo">No</label>
                  </div>
                </div>
              </div>

              <!-- Business Name -->
              <div class="mb-3">
                <label for="businessName" class="form-label fw-bold">Name <span class="text-danger">*</span></label>
                <input type="text" class="form-control" id="businessName" v-model="form.name" required>
              </div>

              <!-- Description -->
              <div class="mb-3">
                <label for="businessDesc" class="form-label fw-bold">Description <span class="text-danger">*</span></label>
                <textarea class="form-control" id="businessDesc" rows="3" v-model="form.description" required></textarea>
              </div>

              <!-- Country -->
              <div class="mb-3">
                <label for="countrySelect" class="form-label fw-bold">Country <span class="text-danger">*</span></label>
                <select class="form-select" id="countrySelect" v-model="form.country" required>
                  <option disabled value="">Please select one</option>
                  <option v-for="c in countries" :key="c.originCountry" :value="c.originCountry">{{ c.originCountry }}</option>
                </select>
              </div>

              <!-- Address (Venue only) -->
              <div v-if="form.type === 'venue'" class="mb-3">
                <label for="venueAddress" class="form-label fw-bold">Address <span class="text-danger">*</span></label>
                <input type="text" class="form-control" id="venueAddress" v-model="form.address">
              </div>

              <!-- Venue Type (Venue only) -->
              <div v-if="form.type === 'venue'" class="mb-3">
                <label for="venueType" class="form-label fw-bold">Venue Type <span class="text-danger">*</span></label>
                <input type="text" class="form-control" id="venueType" v-model="form.venueType">
              </div>

              <!-- Claim Status -->
              <div class="mb-3">
                <label class="form-label fw-bold">Claim Status <span class="text-danger">*</span></label>
                <div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" id="claimed" value="true" v-model="form.claimStatus">
                    <label class="form-check-label" for="claimed">Claimed</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" id="unclaimed" value="false" v-model="form.claimStatus">
                    <label class="form-check-label" for="unclaimed">Unclaimed</label>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="close">Close</button>
            <button v-if="!successMessage" type="button" class="btn btn-primary" @click="createBusiness" :disabled="isLoading">
              <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              Save Business
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show"></div>
  </teleport>
</template>

<script>
export default {
    name: 'AddBusinessModal',
    props: {
      countries: { type: Array, required: true },
    },
    emits: ['close', 'save'],
    data() {
        return {
            isLoading: false,
            error: null,
            successMessage: false, 
            createdBusiness: {     // Initialize as object instead of null
                name: '',
                tempPassword: '',
                username: ''           // Add username field
            },
            tempPassword: "",
            
            form: {
                type: 'producer',
                name: '',
                description: '',
                country: '',
                independentBottler: 'false',
                address: '',
                venueType: '',
                claimStatus: 'false',
            },
        };
    },
    methods: {
        resetForm() {
            this.form = {
                type: 'producer',
                name: '',
                description: '',
                country: '',
                independentBottler: 'false',
                address: '',
                venueType: '',
                claimStatus: 'false',
            };
            this.isLoading = false;
            this.error = null;
            this.successMessage = false;
            this.createdBusiness = null;
            this.tempPassword = "";
        },
        close() {
            // If we successfully created a business, emit save to refresh parent data
            if (this.successMessage) {
                this.$emit('save');
            }

            this.resetForm();
            this.$emit('close');
        },
        sanitizeUsername(businessName) {
            if (!businessName) return "";
            
            // Step 1: Remove CJK (Chinese, Japanese, Korean) characters
            let cleaned = businessName.replace(/[\u4e00-\u9fff\u3400-\u4dbf\u3040-\u309f\u30a0-\u30ff]+/g, '');
            
            // Step 2: Normalize and remove accented characters
            let normalized = cleaned.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
            
            // Step 3: Remove special characters and spaces, keep only alphanumeric, hyphens, underscores
            let sanitized = normalized.replace(/[^a-zA-Z0-9\-_]/g, '');
            
            // Step 4: Convert to lowercase
            sanitized = sanitized.toLowerCase();
            
            // Step 5: If empty, return original (though this shouldn't happen in normal use)
            return sanitized || businessName;
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
        downloadCSV() {
            let csvContent = "data:text/csv;charset=utf-8,";
            csvContent += `Username,Password
`;
            csvContent += `${this.createdBusiness.username},${this.createdBusiness.tempPassword}
`;
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", `${this.createdBusiness.username}_login_details.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        },
        async createBusiness() {
            // Form validation
            if (!this.form.name || !this.form.description || !this.form.country) {
                this.error = "Please fill in all required fields.";
                return;
            }
            if (this.form.type === 'venue' && (!this.form.address || !this.form.venueType)) {
                this.error = "Please fill in Address and Venue Type for venues.";
                return;
            }

            this.isLoading = true;
            this.error = null;

            this.tempPassword = "admin1234"; // Or generate a random one
            // Use sanitized username for password hashing to match backend
            const sanitizedUsername = this.sanitizeUsername(this.form.name);
            const hashedPassword = this.hashPassword(sanitizedUsername, this.tempPassword);
            
            let apiURL = '';
            let newBusinessData = {};

            if (this.form.type === 'producer') {
                apiURL = `${process.env.VUE_APP_API_URL}/createAccount/createProducerAccount`;
                newBusinessData = {
                    producerName: this.form.name,
                    producerDesc: this.form.description,
                    originCountry: this.form.country,
                    isIndependentBottler: this.form.independentBottler === "true",
                    statusOB: "",
                    mainDrinks: [],
                    photo: "",
                    hashedPassword: hashedPassword,
                    questionsAnswers: [],
                    updates: [],
                    producerLink: "",
                    claimStatus: this.form.claimStatus === "true",
                };
            } else { // venue
                apiURL = `${process.env.VUE_APP_API_URL}/createAccount/createVenueAccount`;
                newBusinessData = {
                    venueName: this.form.name,
                    venueDesc: this.form.description,
                    originLocation: this.form.country,
                    address: this.form.address,
                    venueType: this.form.venueType,
                    menu: [],
                    photo: "",
                    hashedPassword: hashedPassword,
                    questionsAnswers: [],
                    updates: [],
                    claimStatus: this.form.claimStatus === "true",
                    openingHours: { Monday: ["", ""], Tuesday: ["", ""], Wednesday: ["", ""], Thursday: ["", ""], Friday: ["", ""], Saturday: ["", ""], Sunday: ["", ""], },
                    publicHolidays: "",
                    reservationDetails: "",
                };
            }

            try {
                const response = await this.$axios.post(apiURL, { newBusinessData }, {
                    headers: { 'Content-Type': 'application/json' }
                });
                // ADD THESE DEBUG LINES
                console.log('Full API Response:', response);
                console.log('Response Status:', response.status);
                console.log('Response Data:', response.data);
                console.log('Response Data Code:', response.data.code);
                console.log('Response Data Username:', response.data.data?.username);

                if (response.data.code === 201) {
                    this.createdBusiness = {
                        name: this.form.name,
                        tempPassword: this.tempPassword,
                        username: response.data.data.username || this.form.name // Fallback to name if username not provided
                    };
                    
                    this.successMessage = true;
                    // Force Vue to update the DOM
                    // this.$nextTick(() => {
                    //     console.log('DOM should be updated now');
                    // });
                    // console.log('successMessage is now:', this.successMessage);
                    // this.$emit('save'); // Notify parent that data has changed
                } else {
                    console.log('Success condition NOT met. Expected code 201, got:', response.data.code);
                    this.error = response.data.message || "An unknown error occurred.";
                }
            } catch (e) {
                console.error(e);
                this.error = e.response?.data?.message || "Failed to create business. Please try again.";
            } finally {
                this.isLoading = false;
            }
        }
    }
};
</script>

<style scoped>
.modal.d-block {
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
