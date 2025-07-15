<!-- src/components/admin_dashboard/FlavourTagModal.vue -->
<template>
  <teleport to="body">
    <div class="modal fade show d-block" tabindex="-1" data-bs-backdrop="static">
      <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ title }}</h5>
            <button type="button" class="btn-close" @click="close" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- Loading Spinner and Error Message -->
            <div v-if="isLoading" class="text-center">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-if="error" class="alert alert-danger">{{ error }}</div>

            <!-- Step 1: Choose Family or Sub-Tag Management -->
            <div v-if="!subMode && !isLoading" class="d-grid gap-3 col-md-8 mx-auto">
              <button class="btn btn-lg btn-outline-primary" @click="subMode = 'family'">Manage Family Tags</button>
              <button class="btn btn-lg btn-outline-info" @click="subMode = 'sub'">Manage Sub-Tags</button>
            </div>

            <!-- ADD MODE -->
            <div v-if="mode === 'add' && subMode">
              <!-- Add Family -->
              <form v-if="subMode === 'family'" @submit.prevent="handleSave">
                <h6>Add New Family Tag</h6>
                <div class="row g-3 align-items-start">
                  <div class="col-md-5">
                    <label class="form-label">Family Name</label>
                    <input type="text" class="form-control" v-model="addFamilyForm.name" required>
                  </div>
                  <div class="col-md-5">
                    <label class="form-label">Hex Color Code (e.g., 8FBC8F)</label>
                    <div class="input-group">
                      <span class="input-group-text">#</span>
                      <input type="text" class="form-control" v-model="addFamilyForm.hexcode" @keyup="isValidHexCode"
                        required>
                    </div>
                    <p v-if="addFamilyForm.hexcode == ''" class='text-danger text-start mb-2 fw-bold'>Hexcode cannot be
                      empty</p>
                    <p v-if="!hexCodeValid && addFamilyForm.hexcode != ''" class='text-danger text-start mb-2 fw-bold'>
                      Hexcode is invalid</p>
                  </div>
                  <div class="col-md-2">
                    <label class="form-label">Preview</label>
                    <div class="p-2 rounded text-center text-white"
                      :style="{ backgroundColor: '#' + addFamilyForm.hexcode }">
                      Tag
                    </div>
                  </div>
                </div>
              </form>
              <!-- Add Sub-Tag -->
              <form v-if="subMode === 'sub'" @submit.prevent="handleSave">
                <h6>Add New Sub-Tag</h6>
                <div class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label">Parent Family</label>
                    <select class="form-select" v-model="addSubForm.parentId" required>
                      <option disabled value="">Select a family</option>
                      <option v-for="family in tags" :key="family.id" :value="family.id">{{ family.familyTag }}</option>
                    </select>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label">New Sub-Tag Name</label>
                    <input type="text" class="form-control" v-model="addSubForm.name" required>
                  </div>
                </div>
              </form>
            </div>

            <!-- EDIT MODE -->
            <div v-if="mode === 'edit' && subMode">
              <!-- Edit Family -->
              <div v-if="subMode === 'family'">
                <h6>Edit Family Tags</h6>
                <div class="row g-2">
                  <div v-for="family in editableTags" :key="family.id" class="col-md-6">
                    <div class="input-group mb-2">
                      <input type="text" class="form-control" v-model="family.familyTag"
                        :style="{ backgroundColor: family.hexcode }">
                      <!-- <span class="input-group-text">#</span> -->
                      <input type="text" class="form-control" v-model="family.hexcode" style="max-width: 100px;">
                    </div>
                  </div>
                </div>
              </div>
              <!-- Edit Sub-Tag -->
              <div v-if="subMode === 'sub'">
                <h6>Edit Sub-Tags</h6>
                <p class="text-muted">Click a family to view and edit its sub-tags.</p>
                <div class="d-flex flex-wrap gap-2">
                  <button v-for="family in editableTags" :key="family.id" class="btn text-white"
                    :style="{ backgroundColor: family.hexcode }" @click="toggleBox(family)">
                    {{ family.familyTag }}
                  </button>
                </div>
                <div v-for="family in editableTags" :key="`editor-${family.id}`">
                  <div v-if="family.showBox" class="p-3 mt-3 rounded"
                    :style="{ border: `2px solid ${family.hexcode}` }">
                    <h6 class="mb-3">Editing sub-tags for <strong :style="{ color: family.hexcode }">{{ family.familyTag
                        }}</strong></h6>
                    <div class="row g-2">
                      <div v-for="sub in family.subTag2" :key="sub.id" class="col-md-4">
                        <input type="text" class="form-control" v-model="sub.subTag">
                      </div>
                      <div v-if="!family.subTag2 || family.subTag2.length === 0" class="col-12">
                        <p class="text-muted fst-italic">This family has no sub-tags to edit.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- DELETE MODE -->
            <div v-if="mode === 'delete' && subMode">
              <!-- Delete Family -->
              <div v-if="subMode === 'family'">
                <h6>Delete Family Tag</h6>
                <p class="text-danger">Warning: Deleting a family tag will also delete all of its sub-tags permanently.
                </p>
                <div class="d-flex flex-wrap gap-2">
                  <button v-for="family in tags" :key="family.id" class="btn btn-outline-danger"
                    @click="selectFamilyToDelete(family)">
                    {{ family.familyTag }}
                  </button>
                </div>
                <div v-if="familyToDelete" class="alert alert-danger mt-3">
                  Are you sure you want to delete <strong>{{ familyToDelete.familyTag }}</strong> and its {{
                    familyToDelete.subTag2.length }} sub-tags?
                  <hr>
                  <button class="btn btn-danger" @click="handleSave">Yes, Confirm Deletion</button>
                  <button class="btn btn-secondary ms-2" @click="cancelDelete">Cancel</button>
                </div>
              </div>
              <!-- Delete Sub-Tag -->
              <div v-if="subMode === 'sub'">
                <h6>Delete Sub-Tag</h6>
                <p class="text-muted">Click a family to view and select a sub-tag to delete.</p>
                <div class="d-flex flex-wrap gap-2">
                  <button v-for="family in editableTags" :key="family.id" class="btn text-white"
                    :style="{ backgroundColor: family.hexcode }" @click="toggleBox(family)">
                    {{ family.familyTag }}
                  </button>
                </div>
                <div v-for="family in editableTags" :key="`deleter-${family.id}`">
                  <div v-if="family.showBox" class="p-3 mt-3 rounded"
                    :style="{ border: `2px solid ${family.hexcode}` }">
                    <h6 class="mb-3">Select a sub-tag from <strong :style="{ color: family.hexcode }">{{
                        family.familyTag }}</strong> to delete:</h6>
                    <div class="d-flex flex-wrap gap-2">
                      <button v-for="sub in family.subTag2" :key="sub.id" 
                        class="btn btn-outline-danger"
                        @click="toggleSubTagForDeletion(sub)">
                        {{ sub.subTag }}
                      </button>
                      <div v-if="!family.subTag2 || family.subTag2.length === 0" class="col-12">
                        <p class="text-muted fst-italic">This family has no sub-tags to delete.</p>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-if="subTagToDelete" class="alert alert-danger mt-3">
                  Are you sure you want to delete <strong>{{ subTagToDelete.subTag }}</strong>?
                  <hr>
                  <button class="btn btn-danger" @click="handleSave">Yes, Confirm Deletion</button>
                  <button class="btn btn-secondary ms-2" @click="cancelSubTagDelete">Cancel</button>
                </div>
              </div>
            </div>

          </div>
          <div class="modal-footer">
            <button v-if="subMode" type="button" class="btn btn-secondary" @click="subMode = null">Back</button>
            <button v-if="mode === 'edit' && subMode" type="button" class="btn btn-warning"
              @click="resetChanges">Reset</button>
            <!-- <button type="button" class="btn btn-secondary" @click="close">Close</button> -->
            <button v-if="mode !== 'delete' && subMode" type="button" class="btn btn-primary" @click="handleSave"
              :disabled="isLoading">
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
  props: {
    mode: {
      type: String,
      required: true
    }, // 'add', 'edit', 'delete'
    tags: {
      type: Array,
      required: true
    },
  },

  emits: ['close', 'save'],

  data() {
    return {
      API_URL: process.env.VUE_APP_API_URL,

      // --- STATE ---
      isLoading: false,
      error: null,
      subMode: null, // 'family' or 'sub'

      // State for Add Mode
      addFamilyForm: {
        name: '',
        hexcode: ''
      },
      addSubForm: {
        parentId: '',
        name: ''
      },

      // State for Edit Mode
      editableTags: [],
      originalTags: [], // To store the initial state for resetting

      // State for Delete Mode
      familyToDelete: null,
      subTagToDelete: null, // New: Stores the single sub-tag selected for deletion

      hexCodeValid: false,
    };
  },

  computed: {
    title() {
      const base = { add: 'Add', edit: 'Edit', delete: 'Delete' }[this.mode];
      const type = { family: 'Family Tag', sub: 'Sub-Tag' }[this.subMode] || 'Flavour Tag';
      return `${base} ${type}`;
    }
  },

  mounted() {
    // Create a deep copy of tags for editing to avoid prop mutation.
    // Also add the 'showBox' property for UI toggling.
    this.editableTags = JSON.parse(JSON.stringify(this.tags)).map(tag => ({
      ...tag,
      showBox: false
    }));
    // Store another deep copy for resetting purposes
    this.originalTags = JSON.parse(JSON.stringify(this.tags)).map(tag => ({
      ...tag,
      showBox: false // Keep structure consistent
    }));
  },

  methods: {
    resetChanges() {
      // Find the ID of the currently open family sub-tag editor, if any
      const openFamilyId = this.editableTags.find(family => family.showBox)?.id;

      // Reset editableTags to its original state
      this.editableTags = JSON.parse(JSON.stringify(this.originalTags));

      // If there was an open family sub-tag editor, re-open it in the reset state
      if (openFamilyId) {
        const familyToReopen = this.editableTags.find(family => family.id === openFamilyId);
        if (familyToReopen) {
          familyToReopen.showBox = true;
        }
      }
    },

    close() {
      this.$emit('close');
    },

    toggleBox(clickedFamily) {
      // First, find the family that was clicked and get its current state
      const targetFamily = this.editableTags.find(f => f.id === clickedFamily.id);
      if (!targetFamily) return;

      const isOpening = !targetFamily.showBox; // Determine if we are opening a new box

      // Always close all other boxes
      this.editableTags.forEach(family => {
        family.showBox = false;
      });

      // If we were opening a new box, set its state to true
      if (isOpening) {
        targetFamily.showBox = true;
      }
      // If we were closing a box (by clicking the same one again), it will remain closed from the loop above.
    },

    selectFamilyToDelete(family) {
      this.familyToDelete = family;
      this.subTagToDelete = null; // Clear sub-tag selection when changing family
    },

    toggleSubTagForDeletion(sub) {
      this.subTagToDelete = sub; // Select the sub-tag for deletion
    },

    cancelSubTagDelete() {
      this.subTagToDelete = null; // Clear the selected sub-tag
    },

    isValidHexCode() {
      // Regular expression to match 3 or 6 character hex codes
      const hexPattern = /^[A-Fa-f0-9]{3}$|^[A-Fa-f0-9]{6}$/;
      this.hexCodeValid = hexPattern.test(this.addFamilyForm.hexcode);
    },

    async handleSave() {
      this.isLoading = true;
      this.error = null;

      try {
        // --- ADD LOGIC ---
        if (this.mode === 'add') {
          if (this.subMode === 'family') {
            if (!this.addFamilyForm.name || !this.addFamilyForm.hexcode) {
              throw new Error("All fields are required.");
            }
            await axios.post(`${this.API_URL}/adminFunctions/createFamilyTag`, {
              familyTag: this.addFamilyForm.name,
              hexcode: '#' + this.addFamilyForm.hexcode,
            });
          } else if (this.subMode === 'sub') {
            if (!this.addSubForm.parentId || !this.addSubForm.name) {
              throw new Error("All fields are required.");
            }
            await axios.post(`${this.API_URL}/adminFunctions/createSubTag`, {
              familyTagId: this.addSubForm.parentId,
              subTag: this.addSubForm.name,
            });
          }
        }
        // --- EDIT LOGIC ---
        else if (this.mode === 'edit') {
          if (this.subMode === 'family') {
            const changes = this.editableTags.filter((tag, i) =>
              tag.familyTag !== this.tags[i].familyTag || tag.hexcode !== this.tags[i].hexcode
            ).map(t => ({
              id: t.id,
              familyTag: t.familyTag,
              hexcode: t.hexcode
            }));

            if (changes.length > 0) {
              await axios.put(`${this.API_URL}/adminFunctions/updateFamilyTag`, changes);
            }
          } else if (this.subMode === 'sub') {
            const changes = [];
            this.editableTags.forEach((family, i) => {
              family.subTag2.forEach((sub, j) => {
                if (sub.subTag !== this.tags[i].subTag2[j]?.subTag) {
                  changes.push({
                    id: sub.id,
                    subTag: sub.subTag
                  });
                }
              });
            });

            if (changes.length > 0) {
              await axios.put(`${this.API_URL}/adminFunctions/updateSubTag`, changes);
            }
          }
        }
        // --- DELETE LOGIC ---
        else if (this.mode === 'delete') {
          if (this.subMode === 'family' && this.familyToDelete) {
            await axios.delete(`${this.API_URL}/adminFunctions/deleteFamilyTag/${this.familyToDelete.id}`);
          } else if (this.subMode === 'sub' && this.subTagToDelete) {
            await axios.delete(`${this.API_URL}/adminFunctions/deleteSubTag/${this.subTagToDelete.id}`);
            this.subTagToDelete = null; // Clear the selected sub-tag after successful deletion
          }
        }

        this.$emit('save'); // Signal success to parent to refetch data
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