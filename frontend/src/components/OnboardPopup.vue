<template>
    <div v-if="isVisible" class="popup-container">
      <div class="popup-content">
        <button class="popup-close" @click="onClose">X</button>
        
        <h2 class="popup-title">{{ title }}</h2>
        <img
          src="../../Images/Others/onboard.png"
          alt="Onboard Image"
          class="popup-image"
        />
        <p class="popup-message">{{ message }}</p>
        <input
          type="text"
          class="popup-input"
          placeholder="Search for a drink"
          v-model="searchText"
        />
        <button class="popup-search" @click="onSearch">Search</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "OnboardPopup",
    props: {
      isVisible: {
        type: Boolean,
        required: true,
      },
      title: {
        type: String,
        required: true,
      },
      message: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        searchText: "",
      };
    },
    methods: {
      onSearch() {
        this.$emit("search", this.searchText); // Emit search event to parent
        console.log("Search Text:", this.searchText);
      },
      onClose() {
        this.$emit("close"); // Emit close event to parent
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
    position: relative;
  }
  
  .popup-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 15px;
  }
  
  .popup-image {
    width: 100%;
    max-width: 400px;
    height: auto;
    margin: 20px;
  }
  
  .popup-message {
    font-size: 16px;
    margin-bottom: 20px;
  }
  
  .popup-input {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .popup-search {
    padding: 10px 20px;
    border: none;
    background: #027562;
    color: white;
    font-size: 14px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .popup-search:hover {
    background: #025d4f;
  }
  
  .popup-close {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 16px;
    font-weight: bold;
    color: #000;
    cursor: pointer;
    transition: color 0.3s ease;
  }
  
  .popup-close:hover {
    color: #ff0000;
  }
  </style>
  