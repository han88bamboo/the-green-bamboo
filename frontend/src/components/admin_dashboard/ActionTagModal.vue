<!-- src/components/admin/ActionTagModal.vue -->
<template>
  <teleport to="body">
    <div class="modal fade show d-block" tabindex="-1" data-bs-backdrop="static">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ title }}</h5>
            <button type="button" class="btn-close" @click="close" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-if="isLoading" class="text-center">
              <div class="spinner-border" role="status"></div>
            </div>
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

            <!-- Add Form -->
            <form v-if="mode === 'add' && !isLoading && !successMessage" @submit.prevent="handleSave">
              <div class="mb-3">
                <label for="newTagName" class="form-label">New Action Tag Name</label>
                <input type="text" class="form-control" id="newTagName" v-model="newTagName" required>
              </div>
            </form>

            <!-- Edit Form -->
            <form v-if="mode === 'edit' && !isLoading && !successMessage" @submit.prevent="handleSave">
              <p>Edit the names of existing action tags.</p>
              <div v-for="tag in editableTags" :key="tag.id" class="mb-2">
                <input type="text" class="form-control" v-model="tag.observationTag">
              </div>
            </form>

            <!-- Delete Form -->
            <div v-if="mode === 'delete' && !isLoading && !successMessage">
              <p class="text-danger">Select an action tag to permanently delete it.</p>
              <div class="d-flex flex-wrap gap-2">
                <button v-for="tag in tags" :key="tag.id" class="btn btn-outline-danger" @click="confirmDelete(tag)">
                  {{ tag.observationTag }}
                </button>
              </div>
              <div v-if="tagToDelete" class="alert alert-warning mt-3">
                Are you sure you want to delete <strong>{{ tagToDelete.observationTag }}</strong>? This cannot be undone.
                <hr>
                <button class="btn btn-danger" @click="handleSave">Yes, Delete</button>
                <button class="btn btn-secondary ms-2" @click="tagToDelete = null">Cancel</button>
              </div>
            </div>

          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="close">Cancel</button>
            <button v-if="mode !== 'delete' || tagToDelete" type="button" class="btn btn-primary" @click="handleSave" :disabled="isLoading">
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show"></div>
  </teleport>
</template>

<script>
import axios from 'axios';

export default {
    name: 'ActionTagModal',
    emits: ['close', 'save'],
    props: {
        mode: { type: String, required: true }, // 'add', 'edit', 'delete'
        tags: { type: Array, required: true },
    },
    components: {
    },
    data() {
        return {
            API_URL: process.env.VUE_APP_API_URL,
            
            // --- STATE ---
            isLoading: false,
            error: null, // A single string for all error messages
            successMessage: null,
            
            // State for 'add' mode
            newTagName: '',
            
            // State for 'edit' mode
            editableTags: [],
            
            // State for 'delete' mode
            tagToDelete: null,
        };
    },
    computed: {
        title() {
            if (this.mode === 'add') return 'Add Action Tag';
            if (this.mode === 'edit') return 'Edit Action Tags';
            return 'Delete Action Tag';
        }
    },
    async mounted() {
        // For 'edit' mode, create a deep copy of the tags to avoid mutating props
        if (this.mode === 'edit') {
            this.editableTags = JSON.parse(JSON.stringify(this.tags));
        }
    },
    methods: {
        close() {
            this.$emit('close');
        },

        confirmDelete(tag) {
            this.tagToDelete = tag;
        },

        async handleSave() {
            this.isLoading = true;
            this.error = null;
            this.successMessage = null;

            try {
                if (this.mode === 'add') {
                    if (!this.newTagName) throw new Error("Tag name cannot be empty.");
                    await axios.post(`${this.API_URL}/adminFunctions/createObservationTag`, {
                        observationTag: this.newTagName
                    });
                    this.successMessage = "Action tag created successfully!";
                } else if (this.mode === 'edit') {
                    const changes = this.editableTags.filter((tag, index) => {
                        return tag.observationTag !== this.tags[index].observationTag;
                    });

                    if (changes.some(tag => !tag.observationTag)) {
                        throw new Error("Tag names cannot be empty.");
                    }

                    if (changes.length > 0) {
                        await axios.put(`${this.API_URL}/adminFunctions/updateObservationTag`, changes);
                        this.successMessage = "Action tags updated successfully!";
                    } else {
                        this.successMessage = "No changes were made.";
                    }
                } else if (this.mode === 'delete' && this.tagToDelete) {
                    await axios.delete(`${this.API_URL}/adminFunctions/deleteObservationTag/${this.tagToDelete.id}`);
                    this.successMessage = `Tag '${this.tagToDelete.observationTag}' deleted successfully.`;
                }

                // Instead of emitting straight away, show success message and then close
                setTimeout(() => {
                    this.$emit('save');
                }, 1500); // Wait 1.5 seconds

            } catch (e) {
                console.error(e);
                this.error = e.response?.data?.message || e.message || "An unknown error occurred.";
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