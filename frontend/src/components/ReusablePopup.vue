<template>
    <div v-if="isVisible" class="popup-container">
      <div class="popup-content">
        <h2 class="popup-title">{{ title }}</h2>
        <img
          src="../../Images/Others/popupimage.png"
          alt="Popup Image"
          class="popup-image"
        />
        <p class="popup-question">{{ question }}</p>
        <div class="popup-options">
          <div
            v-for="(option, index) in options"
            :key="index"
            class="popup-option"
            @click="selectOption(option)"
          >
            {{ option }}
          </div>
        </div>
        <div class="popup-actions">
          <button v-if="showBackButton" class="popup-back" @click="onBack">Back</button>
          <button class="popup-next" @click="onNext">{{ nextButtonText }}</button>
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
    },
    methods: {
      selectOption(option) {
        this.$emit("select", option); // Emit the selected option to the parent
        console.log("Selected option:", option);
      },
      onBack() {
        this.$emit("back");
      },
      onNext() {
        this.$emit("next");
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
  }
  
  .popup-content {
    background: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    max-width: 90%;
    max-height: 90%;
    overflow-y: auto;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .popup-image {
    width: 100%;
    max-width: 400px;
    height: auto;
    margin: 20px;
  }
  
  .popup-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 15px;
  }
  
  .popup-question {
    font-size: 16px;
    margin-bottom: 20px;
  }
  
  .popup-options {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .popup-option {
    padding: 10px;
    text-align: center;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .popup-option:hover {
    background-color: #ff8c00;
    color: white;
  }
  
  .popup-actions {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
  }
  
.popup-back {
  padding: 10px 20px;
  border: none;
  background: #d3d3d3;
  color: #000;
  font-size: 14px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.popup-back:hover {
  background: #bfbfbf;
}

/* Next button styles */
.popup-next {
  padding: 10px 20px;
  border: none;
  background: #ff8c00;
  color: #fff;
  font-size: 14px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.popup-next:hover {
  background: #e57c00;
}

.popup-next.done {
  background: #027562; 
  color: #fff;
}

.popup-next.done:hover {
  background: #025d4f;
}
</style>
  