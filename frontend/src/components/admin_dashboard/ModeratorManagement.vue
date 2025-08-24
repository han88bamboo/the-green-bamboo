<!-- src/components/admin/ModeratorManagement.vue -->
<template>
  <div>
    <!-- Moderator Management Actions -->
    <div class="row text-center mt-3">
      <div class="col-12">
        <h3><b>Manage Moderators</b></h3>
        <p>Add or remove moderator permissions for users.</p>
      </div>
      <div class="col-12 d-flex flex-column flex-sm-row gap-2 justify-content-center">
        <button class="btn tertiary-btn" @click="openModal('add')">
          Add a Moderator
        </button>
        <button class="btn tertiary-btn" @click="openModal('remove')">
          Remove a Moderator
        </button>
      </div>
    </div>

    <hr class="my-4">

    <!-- Moderator Requests -->
    <div class="row text-center">
      <div class="col-12">
        <h3><b>Moderator Requests</b></h3>
      </div>
    </div>
    <div v-if="isLoading" class="text-center my-4">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    <div v-else-if="requests.length > 0" class="row g-3" style="max-height: 650px; overflow-y: auto;">
      <div v-for="request in requests" :key="request.id" class="col-md-6 col-lg-4">
        <div class="card h-100">
          <div class="card-body d-flex flex-column">
            <ul class="list-group list-group-flush text-start flex-grow-1">
              <li class="list-group-item">
                <span class="fw-bold">Requested By:</span><br>
                <router-link :to="`/profile/user/${request.userID}/${getUserById(request.userID)?.username}`">
                  @{{ getUserById(request.userID)?.username || 'Unknown User' }}
                </router-link>
              </li>
              <li class="list-group-item">
                <span class="fw-bold">Drink Type:</span><br>
                {{ request.drinkType }}
              </li>
              <li class="list-group-item">
                <span class="fw-bold">Reason:</span><br>
                <small>{{ request.modDesc }}</small>
              </li>
            </ul>
          </div>
          <div class="card-footer bg-transparent border-top-0">
            <div v-if="isReviewing === request.id" class="d-flex justify-content-center">
              <div class="spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-else class="d-grid gap-2 d-sm-flex justify-content-center">
              <button :disabled="isReviewing" class="btn btn-success btn-sm" @click="reviewRequest(request, 'approve')">Approve</button>
              <button :disabled="isReviewing" class="btn btn-danger btn-sm" @click="reviewRequest(request, 'reject')">Reject</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="alert alert-info text-center">
      There are no new moderator requests.
    </div>

    <!-- Modal for Adding/Removing Moderators -->
    <ModeratorUpdateModal
      v-if="isModalOpen"
      :mode="modalMode"
      :users="users"
      :moderators="moderators"
      :drinkTypes="drinkTypes"
      @close="closeModal"
      @save="handleSave"
    />
  </div>
</template>

<script>
import axios from 'axios';
import ModeratorUpdateModal from './ModeratorUpdateModal.vue';

export default {
    name: 'ModeratorManagement',
    props: {
        users: { type: Array, required: true },
        moderators: { type: Array, required: true },
        requests: { type: Array, required: true },
        drinkTypes: { type: Array, required: true },
        isLoading: { type: Boolean, default: false },
    },
    components: {
        ModeratorUpdateModal,
    },
    data() {
        return {
            API_URL: process.env.VUE_APP_API_URL,
            
            // --- STATE ---
            isModalOpen: false,
            modalMode: 'add', // 'add' or 'remove'
            isReviewing: null, // To show a spinner on the specific card being reviewed
        };
    },
    computed: {
        nonModeratorUsers() {
            const moderatorIds = new Set(this.moderators.map(m => m.id));
            return this.users.filter(u => !moderatorIds.has(u.id));
        }
    },
    async mounted() {
    },
    methods: {
        getUserById(userId) {
            return this.users.find(u => u.id === userId);
        },

        openModal(mode) {
            this.modalMode = mode;
            this.isModalOpen = true;
        },

        closeModal() {
            this.isModalOpen = false;
        },

        handleSave() {
            this.closeModal();
            this.$emit('update-moderators');
        },

        async reviewRequest(request, action) {
            this.isReviewing = request.id;
            
            try {
                if (action === 'approve') {
                    // First, update the user's modType
                    await axios.post(`${this.API_URL}/editProfile/updateModType`, {
                        userID: request.userID,
                        newModType: request.drinkType,
                    });
                }

                // Then, update the request status to no longer be pending
                await axios.post(`${this.API_URL}/editModRequests/updateModRequest`, {
                    requestID: request.id,
                    reviewStatus: false,
                });

                // Tell the parent to refresh all data
                this.$emit('update-moderators');
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
</style>