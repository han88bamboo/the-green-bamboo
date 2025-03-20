<template>
  <div v-if="isVisible" class="popup-container">
    <div class="popup-content">
      <div class="popup-header">
        <h2 class="popup-title">{{ title }}</h2>
        <button class="popup-close" @click="onClose">X</button>
      </div>
      
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
    this.$emit("search", this.searchText);
    console.log("Search Text:", this.searchText);
  },
  async onClose() {
    this.$emit("close");
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
padding: 15px;
border-radius: 10px;
text-align: center;
width: 90%;
max-width: 400px;
max-height: 90vh;
overflow-y: auto;
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
position: relative;
}

/* Header container */
.popup-header {
position: relative;
display: flex;
flex-direction: column;
align-items: center;
width: 100%;
padding-top: 20px;
}

.popup-title {
font-size: 1.5rem;
font-weight: bold;
margin: 0;
}

/* Close button positioned above the title */
.popup-close {
position: absolute;
top: -10px;
right: -10px;
background: none;
border: none;
font-size: 1.5rem;
font-weight: bold;
color: #000;
cursor: pointer;
transition: color 0.3s ease;
}

.popup-close:hover {
color: #ff0000;
}

.popup-image {
width: 80%;
max-width: 300px;
height: auto;
margin: 10px auto;
display: block;
}

.popup-message {
font-size: 1rem;
margin-bottom: 20px;
}

.popup-input {
width: 100%;
padding: 10px;
margin-bottom: 15px;
border: 1px solid #ccc;
border-radius: 5px;
font-size: 1rem;
}

.popup-search {
padding: 12px 20px;
border: none;
background: #027562;
color: white;
font-size: 1rem;
border-radius: 5px;
cursor: pointer;
transition: background-color 0.3s ease;
width: 100%;
}

.popup-search:hover {
background: #025d4f;
}

/* Responsive Design */
@media screen and (max-width: 480px) {
.popup-content {
  width: 95%;
  padding: 10px;
}

.popup-title {
  font-size: 1.3rem;
}

.popup-message {
  font-size: 0.9rem;
}

.popup-search {
  font-size: 0.9rem;
  padding: 10px;
}

.popup-close {
  font-size: 1.2rem;
  top: -5px;
  right: -5px;
}
}
</style>
