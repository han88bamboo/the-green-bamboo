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
              <p><strong>Username:</strong> {{ createdBusiness.name }}</p>
              <p><strong>Password:</strong> {{ createdBusiness.tempPassword }}</p>
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
// import { api } from '@/services/api';

export default {
    name: 'AddBusinessModal',
    props: {
      countries: { type: Array, required: true },
    },
    components: {
    },
    data() {
        return {
            isLoading: false,
            error: null,
            successMessage: false,
            createdBusiness: null,
            
            form: {
                type: 'producer',
                name: '',
                description: '',
                country: '',
            },
        };
    },
    computed: {
    },
    async mounted() {
    },
    methods: {
        close() {
            this.$emit('close');
        },

        async createBusiness() {
            if (!this.form.name || !this.form.description || !this.form.country) {
                this.error = "Please fill in all required fields.";
                return;
            }

            this.isLoading = true;
            this.error = null;

            try {
                // const response = await api.createBusiness(this.form);
                // Mock API response
                const response = {
                    name: this.form.name,
                    tempPassword: `temp_${Math.random().toString(36).slice(-8)}`,
                };
                
                this.createdBusiness = response;
                this.successMessage = true;
                this.$emit('save'); // Notify parent that data has changed
            } catch (e) {
                console.error(e);
                this.error = "Failed to create business. Please try again.";
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