<template>
  <div class="text-center">
    <h3><b>Tag Controls</b></h3>
    
    <div class="my-3">
      <button 
        class="btn m-1" 
        :class="showObservationControl ? 'btn-dark' : 'btn-secondary'"
        @click="toggleControl('observation')">
        Action Tags
      </button>
      <button 
        class="btn m-1" 
        :class="showFlavourControl ? 'btn-dark' : 'btn-secondary'"
        @click="toggleControl('flavour')">
        Flavour Tags
      </button>
    </div>

    <!-- Action Tag Controls -->
    <div v-if="showObservationControl" class="p-3 border rounded">
      <div class="d-flex flex-column flex-sm-row gap-2 justify-content-center">
        <button class="btn btn-warning" @click="openModal('action', 'add')" :disabled="isLoading">Add Action Tag</button>
        <button class="btn btn-primary" @click="openModal('action', 'edit')" :disabled="isLoading">Edit Action Tags</button>
        <button class="btn btn-danger" @click="openModal('action', 'delete')" :disabled="isLoading">Delete Action Tags</button>
      </div>
    </div>

    <!-- Flavour Tag Controls -->
    <div v-if="showFlavourControl" class="p-3 border rounded">
      <div class="d-flex flex-column flex-sm-row gap-2 justify-content-center">
        <button class="btn btn-warning" @click="openModal('flavour', 'add')" :disabled="isLoading">Add Flavour Tag</button>
        <button class="btn btn-primary" @click="openModal('flavour', 'edit')" :disabled="isLoading">Edit Flavour Tags</button>
        <button class="btn btn-danger" @click="openModal('flavour', 'delete')" :disabled="isLoading">Delete Flavour Tags</button>
      </div>
    </div>

    <!-- Modals (only one will be rendered at a time) -->
    <ActionTagModal 
      v-if="isActionModalOpen" 
      :mode="modalMode" 
      :tags="observationTags"
      @close="closeModal"
      @save="handleSave"
    />
    <FlavourTagModal 
      v-if="isFlavourModalOpen" 
      :mode="modalMode" 
      :tags="flavourTags"
      @close="closeModal"
      @save="handleSave"
    />
  </div>
</template>

<!-- src/components/admin_dashboard/TagManagement.vue -->
<script>
import ActionTagModal from './ActionTagModal.vue';
import FlavourTagModal from './FlavourTagModal.vue';

export default {
    name: 'TagManagement',
    props: {
        isLoading: { type: Boolean, required: true },
        observationTags: { type: Array, required: true },
        flavourTags: { type: Array, required: true },
    },
    components: {
        ActionTagModal,
        FlavourTagModal,
    },
    data() {
        return {
            // Controls which set of buttons is visible
            showObservationControl: false,
            showFlavourControl: false,
            
            // Controls the visibility and mode of the modals
            isActionModalOpen: false,
            isFlavourModalOpen: false,
            modalMode: 'add', // 'add', 'edit', or 'delete'
        };
    },
    computed: {
    },
    async mounted() {
    },
    methods: {
        toggleControl(type) {
            if (type === 'observation') {
                this.showObservationControl = !this.showObservationControl;
                this.showFlavourControl = false;
            } else {
                this.showFlavourControl = !this.showFlavourControl;
                this.showObservationControl = false;
            }
        },

        openModal(type, modeValue) {
            this.modalMode = modeValue;
            if (type === 'action') {
                this.isActionModalOpen = true;
            } else {
                this.isFlavourModalOpen = true;
            }
        },

        closeModal() {
            this.isActionModalOpen = false;
            this.isFlavourModalOpen = false;
        },

        handleSave() {
            this.closeModal();
            // Tell the parent dashboard to refresh all data
            this.$emit('update-tags');
        }
    }
};
</script>