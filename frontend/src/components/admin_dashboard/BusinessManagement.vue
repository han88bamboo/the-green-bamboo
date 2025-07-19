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
      <div v-for="status in availableStatuses" :key="status.value"
        class="form-check form-check-inline alert py-1 px-3 m-0" :class="status.class">
        <input class="form-check-input" type="checkbox" :id="`check-${status.value}`" :value="status.value"
          v-model="selectedStatuses">
        <label class="form-check-label" :for="`check-${status.value}`">{{ status.label }}</label>
      </div>
    </div>

    <!-- Request List -->
    <div v-if="isLoading" class="text-center my-4">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else-if="filteredRequests.length > 0" class="row g-3" style="max-height: 525px; overflow-y: auto;">
      <div v-for="request in filteredRequests" :key="request.id" class="col-md-6 col-lg-4">
        <div class="card h-100" :class="request.cardClass">
          <div class="card-header fw-bold">{{ request.businessName }}</div>
          <div class="card-body">
            <h6 class="card-subtitle mb-2 text-muted">{{ 'Type: ' + request.businessType }}</h6>
            <h6 class="card-subtitle mb-2 text-muted">{{ 'Country: ' + request.country }}</h6>
            <p class="card-text"><small>{{ request.businessDesc }}</small></p>
            <h6 class="card-subtitle mb-2 text-muted">{{ 'Site: ' }}
              <router-link v-if="request.businessLink" :to="{ path: request.businessLink }" style="color: inherit;">
                Link
              </router-link>
              <span v-if="!request.businessLink">N/A</span>
            </h6>
            <a :href="`mailto:${request.email}`" class="card-link">Contact Requestor</a>
            <a v-if="request.referenceDocument" @click.prevent="openDocument(request.referenceDocument)" href="#"
              class="card-link">View Document</a>

            <hr>
            <span class="fw-bold">Requestor Information</span>
            <hr>

            <ul class="list-group list-group-flush text-start">
              <li class="list-group-item" :class="request.liClass"><span class="fw-bold">First Name: </span> {{
                request.firstName }} </li>
              <li class="list-group-item" :class="request.liClass"><span class="fw-bold">Last Name: </span> {{
                request.lastName }} </li>
              <li class="list-group-item" :class="request.liClass"><span class="fw-bold">Relationship: </span> {{
                request.relationship }} </li>
              <li class="list-group-item" :class="request.liClass"><span class="fw-bold">Email: </span> {{ request.email
              }} </li>
              <li class="list-group-item" :class="request.liClass"><span class="fw-bold">Price Plan: </span> {{
                request.pricing }} </li>
            </ul>
          </div>
          <div v-if="request.isPending" class="card-footer bg-transparent border-top-0">
            <div v-if="isReviewing === request.id" class="d-flex justify-content-center">
              <div class="spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-else class="d-grid gap-2 d-sm-flex justify-content-center">
              <button v-if="request.status === 'pendingApproval'" class="btn btn-success btn-sm"
                @click="reviewRequest(request, 'approve')" :disabled="isReviewing">Approve</button>
              <button v-if="request.status === 'pendingPayment'" class="btn btn-info btn-sm"
                @click="reviewRequest(request, 'resend')" :disabled="isReviewing">Resend Email</button>
              <button class="btn btn-danger btn-sm" @click="reviewRequest(request, 'reject')"
                :disabled="isReviewing">Reject</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="alert alert-info text-center">
      No business account requests match the current filters.
    </div>

    <!-- Add Business Modal -->
    <AddBusinessModal v-if="isModalOpen" :countries="countries" @close="closeModal" @save="handleSave" />
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
    isLoading: { type: Boolean, default: false },
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
      // DON'T close the modal here - let the child component handle it
      // this.closeModal();

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

    checkBusinessExist(businessLink) {
      if (businessLink) {
        // const businessID = businessLink.split("/").pop()
        const businessId = parseInt(businessLink.match(/\d+/)[0])
        if (this.producers.find(producer => producer.id == businessId)) {
          return true;
        }
        if (this.venues.find(venue => venue.id == businessId)) {
          return true;
        }
      }
      return false;
    },

    async generateToken(businessId, request) {
      try {
        const response = await axios.post(`${this.API_URL}/createAccount/createToken`,
          {
            businessId: businessId,
            requestId: request.id,
            businessType: request.businessType,
            isNew: true,
          }, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        const link = `https://drink-x.com/billingSecurity?token=${response.data.data.token}`;
        return link;
      } catch (error) {
        console.error(error);
      }
    },

    async emailLink(request, link) {
      const emailDetails = {
        recipient: request.email,
        subject: "Set Up Your Drink-X Business Account",
        message: `Hi ${request.firstName}, 

Your request to create a business account on Drink X has been approved! 
                Click on the link below to complete your account setup and create your password: 
${link} 

If you did not initiate this request, please contact us immediately. 

Thank you, 
Drink-X`
      };
      try {
        await axios.post(`${this.API_URL}/createAccount/sendEmail`, emailDetails);
      } catch (error) {
        console.error('Failed to send email:', error);
      }
    },

    async reviewRequest(request, action) {
      this.isReviewing = request.id;
      try {
        if (action === 'approve') {
          const businessExist = this.checkBusinessExist(request.businessLink);
          if (businessExist) {
            const businessID = parseInt(request.businessLink.match(/\d+/)[0])
            const tempPassword = "admin1234"
            const hashedPassword = this.hashPassword(request.businessName, tempPassword);
            const newBusinessData = {
              businessName: request.businessName,
              businessDesc: request.businessDesc,
              originCountry: request.country,
              isIndependentBottler: request.isIndependentBottler === "true" || request.isIndependentBottler === true,
              statusOB: "",
              mainDrinks: [],
              photo: "",
              hashedPassword: hashedPassword,
              questionsAnswers: [],
              updates: [],
              username: request.businessName,
              website: "",
              claimStatus: request.claimStatus !== undefined ? request.claimStatus : false,
              requestId: request.id
            }
            let apiURL = '';
            if (request.businessType == "producer") {
              apiURL = `${this.API_URL}/editProducerProfile/updateProducerStatus`;
            }
            else if (request.businessType == "venue") {
              apiURL = `${this.API_URL}/editVenueProfile/updateVenueStatus`;
            }
            if (apiURL != '') {
              try {
                const response = await axios.post(apiURL, {
                  businessID: businessID,
                  newBusinessData: newBusinessData,
                }, {
                  headers: { 'Content-Type': 'application/json' }
                });
                console.log(response.data)
                if (response.data.code == 201) {
                  this.$emit('update-data');
                }
              } catch (error) {
                console.log(error)
                console.error("Error details:", error.response ? error.response.data : error);
              }
            }
            const link = await this.generateToken(businessID, request);
            this.emailLink(request, link);
          }
          else {
            this.businessToCreate = {
              businessType: request.businessType,
              businessName: request.businessName,
              businessDesc: request.businessDesc,
              country: request.country,
              isIndependentBottler: request.isIndependentBottler,
              claimStatus: false,
              requestId: request.id
            }
            this.openModal();
          }
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
        } else if (action === 'resend') {
          const link = await this.generateToken(request.businessID, request)
          this.emailLink(request, link);
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