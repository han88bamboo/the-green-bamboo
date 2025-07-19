<!-- src/components/admin/ModeratorUpdateModal.vue -->
<template>
  <!-- Using a teleport to move the modal to the end of the body is good practice -->
  <teleport to="body">
    <div class="modal fade show d-block" id="moderatorUpdateModal" tabindex="-1" data-bs-backdrop="static">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ title }}</h5>
            <button type="button" class="btn-close" @click="close" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- Loading/Error/Success States -->
            <div v-if="isLoading" class="text-center">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-if="error" class="alert alert-danger">{{ error }}</div>

            <!-- Form Content -->
            <form v-if="!isLoading" @submit.prevent="handleSubmit">
              <!-- User Selection -->
              <div class="mb-3">
                <label for="userSelect" class="form-label">User</label>
                <input class="form-control" list="userDatalist" id="userSelect" placeholder="Type to search..."
                  v-model="selectedUsername">
                <datalist id="userDatalist">
                  <option v-for="user in userList" :key="user.id" :value="user.username" />
                </datalist>
              </div>

              <!-- Drink Type Selection -->
              <div class="mb-3">
                <label for="drinkTypeSelect" class="form-label">Drink Type to Moderate</label>
                <input class="form-control" list="drinkTypeDatalist" id="drinkTypeSelect"
                  placeholder="e.g., Whisky, Gin..." v-model="selectedDrinkType">
                <datalist id="drinkTypeDatalist">
                  <option v-for="dt in drinkTypes" :key="dt.id" :value="dt.drinkType" />
                </datalist>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="close">Cancel</button>
            <button type="button" class="btn btn-primary" @click="handleSubmit" :disabled="!isFormValid || isLoading">
              {{ buttonText }}
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
  props: {
    mode: {
      type: String,
      required: true,
      validator: (val) => ['add', 'remove'].includes(val)
    },
    users: {
      type: Array,
      required: true
    },
    moderators: {
      type: Array,
      required: true
    },
    drinkTypes: {
        type: Array,
        required: true
    }
  },

  emits: ['close', 'save'],

  data() {
    return {
      isLoading: false,
      error: null,
      selectedUsername: '',
      selectedDrinkType: '',
    };
  },

  computed: {
    title() {
      return this.mode === 'add' ? 'Add Moderator' : 'Remove Moderator';
    },

    buttonText() {
      return this.mode === 'add' ? 'Add Moderator' : 'Remove Moderator';
    },

    userList() {
      return this.mode === 'add' ? this.users : this.moderators;
    },

    isFormValid() {
      return this.selectedUsername.trim() !== '' && this.selectedDrinkType.trim() !== '';
    }
  },

  methods: {
    close() {
      this.$emit('close');
    },

    async handleSubmit() {
      if (!this.isFormValid) {
        this.error = "Please fill out all fields.";
        return;
      }

      this.isLoading = true;
      this.error = null;

      try {
        const user = this.userList.find(u => u.username === this.selectedUsername);
        if (!user) {
          throw new Error("Selected user not found.");
        }

        const apiEndpoint = this.mode === 'add' ? 'updateModType' : 'removeModType';
        const payload = {
            userID: user.id,
            [this.mode === 'add' ? 'newModType' : 'removeModType']: this.selectedDrinkType,
        };

        const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/editProfile/${apiEndpoint}`, payload, {
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.data.code !== 201) {
            throw new Error(response.data.message || 'An unknown error occurred.');
        }

        this.$emit('save');
      } catch (e) {
        console.error(e);
        this.error = e.message || 'An error occurred. Please try again.';
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
