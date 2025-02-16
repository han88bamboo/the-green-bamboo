<template>
  <div v-if="isVisible" class="popup-container">
    <div class="popup-content">
      <h2 class="popup-title">{{ title }}</h2>
      <img src="../../Images/Others/popupimage.png" alt="Popup Image" class="popup-image" />
      <p class="popup-question">{{ question }}</p>

      <p v-if="note" class="popup-note">{{ note }}</p>

      <div class="popup-options">
        <div
          v-for="(option, index) in options"
          :key="index"
          class="popup-option"
          :class="{ 'selected': selectedOptions.includes(option) }"
          @click="toggleOption(option)"
        >
          {{ option }}
        </div>
      </div>

      <div class="popup-actions">
        <button v-if="showBackButton" class="popup-back" @click="onBack">Back</button>
        <button
          class="popup-next"
          :class="{ 'disabled': !canProceed }"
          :disabled="!canProceed"
          @click="onNext"
        >
          {{ nextButtonText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ReusablePopup",
  props: {
    isVisible: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    question: {
      type: String,
      required: true,
    },
    options: {
      type: Array,
      required: true,
    },
    showBackButton: {
      type: Boolean,
      default: false,
    },
    nextButtonText: {
      type: String,
      default: "Next",
    },
    minSelections: {
      type: Number,
      default: 1, // Default to 1 if not specified
    },
    preselectedOptions: {
      type: Array,
      default: () => [],
    },
    note: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      selectedOptions: [...this.preselectedOptions], // Initialize with preselected options
    };
  },
  computed: {
    canProceed() {
      return this.selectedOptions.length >= this.minSelections;
    },
  },
  methods: {
    toggleOption(option) {
      if (this.selectedOptions.includes(option)) {
        // Deselect option
        this.selectedOptions = this.selectedOptions.filter((item) => item !== option);
      } else {
        // Select option
        this.selectedOptions.push(option);
      }
      this.$emit("updateSelection", this.selectedOptions); // Emit selections to parent
    },
    onBack() {
      this.$emit("back");
    },
    onNext() {
      if (this.canProceed) {
        this.$emit("next", this.selectedOptions);
      }
    },
  },
};
</script>

<style scoped>
.popup-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 10px;
}

.popup-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  width: 50vw; /* Default width for desktops */
  max-height: 90vh; /* Prevents scrolling on desktop */
  overflow-y: auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Responsive for Mobile */
@media (max-width: 768px) {
  .popup-content {
    width: 90vw; /* Full width for mobile */
    max-height: 80vh; /* Allows scrolling if needed */
    padding: 15px;
  }
}

.popup-image {
    width: 100%;
    max-width: 300px;
    height: auto;
    margin: 10px 0;
  }

.popup-title {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 10px;
}

.popup-question {
  font-size: 16px;
  margin-bottom: 2px;
}

.popup-note {
  font-size: 14px;
  margin-bottom: 20px;
}

.popup-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 10px;
  margin-bottom: 20px;
}

.popup-option {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  text-align: center;
  border: 2px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
  min-height: 40px; /* Ensures consistent height */
  word-wrap: break-word; /* Wraps long words */
  white-space: normal; /* Ensures text wraps instead of overflowing */
}

/* Selected option turns orange */
.popup-option.selected {
  background-color: #ff8c00 !important;
  color: white;
  border: 1px solid #ff8c00;
}

.popup-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}

.popup-next,
.popup-back {
  padding: 12px 25px;
  border: none;
  font-size: 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.popup-next {
  background: #ff8c00;
  color: white;
}

/* Back button matches next button but is grey */
.popup-back {
  background: #ccc;
  color: black;
}

/* Disabled next button */
.popup-next.disabled {
  background: #ddd;
  cursor: not-allowed;
}
</style>
