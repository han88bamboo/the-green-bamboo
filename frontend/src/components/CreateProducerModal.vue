<!-- src/components/CreateProducerModal.vue -->
<template>
  <teleport to="body">
    <div class="modal fade show d-block" tabindex="-1" data-bs-backdrop="static">
      <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add a New Producer</h5>
            <button type="button" class="btn-close" @click="close" aria-label="Close"></button>
          </div>
          <div class="modal-body">
        
            <!-- Success Message -->
            <div v-if="successMessage" class="alert alert-success">
              <p class="fw-bold">Producer account created successfully!</p>
              <p>You can now select the newly created producer for your listing.</p>
              <hr>
              <p><strong>Producer:</strong> {{ createdProducer.name }}</p>
            </div>

            <!-- Error Message -->
            <div v-if="error" class="alert alert-danger">{{ error }}</div>

            <!-- Form -->
            <form v-if="!successMessage" @submit.prevent="createProducer">
              <!-- Producer Name -->
              <div class="mb-3">
                <label for="producerName" class="form-label fw-bold">Producer Name <span class="text-danger">*</span></label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="producerName" 
                  v-model="form.producerName" 
                  required
                  placeholder="Enter the producer's name"
                >
              </div>

              <!-- Description -->
              <div class="mb-3">
                <label for="producerDesc" class="form-label fw-bold">Description <span class="text-danger">*</span></label>
                <textarea 
                  class="form-control" 
                  id="producerDesc" 
                  rows="3" 
                  v-model="form.producerDesc" 
                  required
                  placeholder="Enter a description of the producer"
                ></textarea>
              </div>

              <!-- Country -->
              <div class="mb-3">
                <label for="countrySelect" class="form-label fw-bold">Country of Origin <span class="text-danger">*</span></label>
                <select class="form-select" id="countrySelect" v-model="form.originCountry" required>
                  <option disabled value="">Please select one</option>
                  <option v-for="country in countries" :key="country" :value="country">
                    {{ country }}
                  </option>
                </select>
              </div>

              <!-- Independent Bottler -->
              <div class="mb-3">
                <label class="form-label fw-bold">Independent Bottler <span class="text-danger">*</span></label>
                <div>
                  <div class="form-check form-check-inline">
                    <input 
                      class="form-check-input" 
                      type="radio" 
                      id="independentBottlerYes" 
                      value="true" 
                      v-model="form.isIndependentBottler"
                    >
                    <label class="form-check-label" for="independentBottlerYes">Yes</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input 
                      class="form-check-input" 
                      type="radio" 
                      id="independentBottlerNo" 
                      value="false" 
                      v-model="form.isIndependentBottler"
                    >
                    <label class="form-check-label" for="independentBottlerNo">No</label>
                  </div>
                </div>
              </div>

              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="close">Cancel</button>
                <button type="submit" class="btn primary-btn" :disabled="isLoading">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Create Producer
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show"></div>
  </teleport>
</template>

<script>
export default {
  name: 'CreateProducerModal',
  props: {
    countries: { 
      type: Array, 
      required: true 
    }
  },
  emits: ['close', 'producerCreated'],
  data() {
    return {
      isLoading: false,
      error: null,
      successMessage: false,
      createdProducer: {
        name: '',
        id: null
      },
      form: {
        producerName: '',
        producerDesc: '',
        originCountry: '',
        isIndependentBottler: 'false'
      }
    };
  },
  methods: {
    resetForm() {
      this.form = {
        producerName: '',
        producerDesc: '',
        originCountry: '',
        isIndependentBottler: 'false'
      };
      this.isLoading = false;
      this.error = null;
      this.successMessage = false;
      this.createdProducer = {
        name: '',
        id: null
      };
    },
    close() {
      // If we successfully created a producer, emit producerCreated to update parent data
      if (this.successMessage) {
        this.$emit('producerCreated', { 
          id: this.createdProducer.id, 
          name: this.createdProducer.name,
          isIndependentBottler: this.form.isIndependentBottler === 'true'
        });
      }
      
      this.resetForm();
      this.$emit('close');
    },
    async createProducer() {
      // Form validation
      if (!this.form.producerName || !this.form.producerDesc || !this.form.originCountry) {
        this.error = "Please fill in all required fields.";
        return;
      }

      this.isLoading = true;
      this.error = null;

      try {
        // Prepare data for API
        const producerData = {
          producerName: this.form.producerName,
          producerDesc: this.form.producerDesc,
          originCountry: this.form.originCountry,
          isIndependentBottler: this.form.isIndependentBottler === 'true',
          // User info
          userID: localStorage.getItem('88B_accID')
        };

        // Call the API to create producer
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/createUserProducer/createUserProducer`, 
          producerData
        );

        if (response.status === 201) {
          this.createdProducer = {
            name: this.form.producerName,
            id: response.data.id
          };
          this.successMessage = true;
        } else {
          throw new Error("Failed to create producer");
        }
      } catch (error) {
        console.error("Error creating producer:", error);
        this.error = error.response?.data?.message || 
                    "Failed to create producer. Please try again.";
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
