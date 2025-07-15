<!-- src/components/admin/BusinessManagement.vue -->
<template>
  <div>
    <!-- Add Business Action -->
    <div class="row text-center mt-3">
      <div class="col-12">
        <h3><b>Manage Businesses</b></h3>
        <p>Create new business profiles for producers and venues.</p>
      </div>
      <div class="col-12">
        <button class="btn tertiary-btn" @click="openModal">
          Add a Business
        </button>
      </div>
    </div>

    <hr class="my-4">

    <!-- Business Account Requests -->
    <div class="row text-center">
      <div class="col-12">
        <h3><b>Business Account Requests</b></h3>
      </div>
    </div>
    
    <!-- Filters -->
    <div class="d-flex flex-wrap justify-content-center gap-2 my-3">
      <div v-for="status in availableStatuses" :key="status.value" class="form-check form-check-inline alert py-1 px-3 m-0" :class="status.class">
        <input class="form-check-input" type="checkbox" :id="`check-${status.value}`" :value="status.value" v-model="selectedStatuses">
        <label class="form-check-label" :for="`check-${status.value}`">{{ status.label }}</label>
      </div>
    </div>

    <!-- Request List -->
    <div v-if="filteredRequests.length > 0" class="row g-3" style="max-height: 525px; overflow-y: auto;">
      <div v-for="request in filteredRequests" :key="request.id" class="col-md-6 col-lg-4">
        <div class="card h-100" :class="request.cardClass">
          <div class="card-header fw-bold">{{ request.businessName }}</div>
          <div class="card-body">
            <h6 class="card-subtitle mb-2 text-muted">{{ request.businessType }} - {{ request.country }}</h6>
            <p class="card-text"><small>{{ request.businessDesc }}</small></p>
            <a :href="`mailto:${request.email}`" class="card-link">Contact Requestor</a>
            <a v-if="request.referenceDocument" @click.prevent="openDocument(request.referenceDocument)" href="#" class="card-link">View Document</a>
          </div>
          <div v-if="request.isPending" class="card-footer bg-transparent border-top-0">
            <div class="d-grid gap-2 d-sm-flex justify-content-center">
              <button v-if="request.status === 'pendingApproval'" class="btn btn-success btn-sm" @click="reviewRequest(request, 'approve')">Approve</button>
              <button v-if="request.status === 'pendingPayment'" class="btn btn-info btn-sm" @click="reviewRequest(request, 'resend')">Resend Email</button>
              <button class="btn btn-danger btn-sm" @click="reviewRequest(request, 'reject')">Reject</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="alert alert-info text-center">
      No business account requests match the current filters.
    </div>

    <!-- Add Business Modal -->
    <AddBusinessModal
      v-if="isModalOpen"
      :countries="countries"
      @close="closeModal"
      @save="handleSave"
    />
  </div>
</template>

<script>
import axios from 'axios';
import AddBusinessModal from './AddBusinessModal.vue';

export default {
    name: 'BusinessManagement',
    props: {
        countries: { type: Array, required: true },
        requests: { type: Array, required: true },
        producers: { type: Array, required: true },
        venues: { type: Array, required: true },
    },
    components: {
        AddBusinessModal,
    },
    data() {
        return {
            API_URL: process.env.VUE_APP_API_URL,
            
            // --- STATE ---
            isModalOpen: false,
            selectedStatuses: ['pendingApproval', 'pendingPayment'],
            isReviewing: null, // For showing spinners on cards
            
            // This will hold data for the modal if we need to pre-fill it from a request
            businessToCreate: {
                businessType: 'producer',
                businessName: '',
                businessDesc: '',
                country: '',
                isIndependentBottler: false,
                claimStatus: false,
                requestId: null,
            },
            
            availableStatuses: [
                { value: 'pendingApproval', label: 'Pending Approval', class: 'alert-warning' },
                { value: 'pendingPayment', label: 'Pending Payment', class: 'alert-info' },
                { value: 'verified', label: 'Verified', class: 'alert-success' },
                { value: 'rejected', label: 'Rejected', class: 'alert-danger' },
            ],
        };
    },
    computed: {
        processedRequests() {
            return this.requests.map(request => {
                let status = 'rejected';
                if (request.isPending && !request.isApproved) status = 'pendingApproval';
                else if (request.isPending && request.isApproved) status = 'pendingPayment';
                else if (!request.isPending && request.isApproved) status = 'verified';
                
                const statusInfo = this.availableStatuses.find(s => s.value === status);
                return {
                    ...request,
                    status,
                    isPending: ['pendingApproval', 'pendingPayment'].includes(status),
                    cardClass: statusInfo?.class.replace('alert', 'border') || 'border-secondary',
                };
            });
        },

        filteredRequests() {
            return this.processedRequests.filter(req => this.selectedStatuses.includes(req.status));
        }
    },
    async mounted() {
    },
    methods: {
        openModal() {
            this.isModalOpen = true;
        },

        closeModal() {
            this.isModalOpen = false;
        },

        handleSave() {
            this.closeModal();
            this.$emit('update-data');
        },

        openDocument(docData) {
            const byteCharacters = atob(docData);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }
            const byteArray = new Uint8Array(byteNumbers);
            const blob = new Blob([byteArray], { type: 'application/pdf' });
            const blobUrl = URL.createObjectURL(blob);
            window.open(blobUrl, '_blank');
        },

        async reviewRequest(request, action) {
            this.isReviewing = request.id;
            try {
                if (action === 'approve') {
                    // Logic to create/update business, then update request status
                    // This is a simplified version of your original complex logic
                    console.log("Approving request:", request.businessName);
                    // You would call your createBusiness or updateBusiness logic here
                    // For now, we'll just update the status
                    await axios.post(`${this.API_URL}/createAccount/updateAccountRequest`, {
                        requestID: request.id,
                        isPending: true,
                        isApproved: true,
                    });
                } else if (action === 'reject') {
                    await axios.post(`${this.API_URL}/createAccount/updateAccountRequest`, {
                        requestID: request.id,
                        isPending: false,
                        isApproved: false,
                    });
                    // You might also want to delete any associated tokens
                } else if (action === 'resend') {
                    console.log("Resending email for:", request.businessName);
                    // Your email sending logic would go here
                }
                this.$emit('update-data');
            } catch (error) {
                console.error(`Failed to ${action} request`, error);
                alert(`An error occurred while trying to ${action} the request.`);
            } finally {
                this.isReviewing = null;
            }
        }
    }
};
</script>

<style scoped>
.tertiary-btn {
  background-color: #747D92;
  color: whitesmoke;
}
.tertiary-btn:hover {
  background-color: #535C72;
}
.card-link {
  cursor: pointer;
}
</style>