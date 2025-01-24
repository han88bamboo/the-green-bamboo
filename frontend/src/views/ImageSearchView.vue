<template>
  <NavBar />

  <div class="image-search">
    <h1>Wondering if a drink is worth a try?</h1>
    <p>Scan the drink label to discover more info!</p>

    <div
      class="greybox"
      :class="{ dragging: isDragging }"
      @dragover.prevent="onDragOver"
      @dragleave="onDragLeave"
      @drop="onDrop"
    >
      <label for="file-upload" class="custom-file-upload">
        <img
          src="@../../../Images/Others/camera.png"
          alt="Camera"
          class="camera-icon"
        />
        Drag an image here or upload a file.
      </label>
      <input id="file-upload" type="file" @change="onFileChange" hidden />

      <div>OR</div>

      <div class="link-section">
        <input
          type="text"
          placeholder="Paste image link"
          v-model="imageLink"
          @keypress.enter="onImageLinkSubmit"
        />
        <img
          src="@../../../Images/Others/search.png"
          alt="Search"
          class="search-icon"
          @click="onImageLinkSubmit"
        />
      </div>

      <!-- Display the uploaded image -->
      <div class="uploaded-image" v-if="uploadedImage">
        <h3>Uploaded Image:</h3>
        <img
          :src="uploadedImage"
          alt="Uploaded drink label"
          class="image-preview"
        />
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";

export default {
  name: "ImageSearchView",
  components: {
    NavBar,
  },
  data() {
    return {
      imageLink: "",
      uploadedImage: "", // To store the uploaded image data URL
      isDragging: false, // To style the drag area
    };
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          this.uploadedImage = reader.result;
        };
        reader.readAsDataURL(file);
      } else {
        console.error("No file selected");
      }
    },
    onImageLinkSubmit() {
      if (this.imageLink.trim()) {
        console.log(this.imageLink);
        // Implement the logic for processing the image link here
      } else {
        console.error("Image link is empty");
      }
    },
    onDragOver(event) {
      event.preventDefault(); // Prevent default behavior
      this.isDragging = true; // Add visual feedback for drag
    },
    onDragLeave() {
      this.isDragging = false; // Reset visual feedback
    },
    onDrop(event) {
      event.preventDefault(); // Prevent default behavior
      this.isDragging = false; // Reset visual feedback

      const file = event.dataTransfer.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          this.uploadedImage = reader.result;
        };
        reader.readAsDataURL(file);
      } else {
        console.error("No file dropped");
      }
    },
  },
};
</script>

<style scoped>
.image-search {
  text-align: center;
  margin-top: 50px;
}

.greybox {
  width: 50%;
  margin: 50px auto;
  background-color: #f4f4f47d;
  border-radius: 5px;
  display: block;
  text-align: center;
  border: 5px solid #027562;
  padding: 50px 10px;
}

.upload-section,
.link-section {
  margin: 20px auto;
  width: 80%;
}

.image-search h1,
.image-search p {
  color: #027562;
}

.custom-file-upload {
  display: inline-block;
  padding: 10px 20px;
  cursor: pointer;
  background-color: #f4f4f4;
  border: 2px dashed #ccc;
}

input[type="text"] {
  width: calc(100% - 50px);
  padding: 10px;
  display: inline-block;
  vertical-align: middle;
}

button {
  padding: 10px 20px;
  background-color: #027562;
  color: white;
  border: none;
  cursor: pointer;
}

.link-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-icon {
  width: 5%;
  cursor: pointer;
  display: inline-block;
  vertical-align: middle;
  margin-left: 10px;
}

.custom-file-upload {
  display: inline-block;
  padding: 10px 20px;
  margin: 20px auto;
  cursor: pointer;
  background-color: #f4f4f4;
  border: 2px dashed #ccc;
  text-align: center;
}
.camera-icon {
  width: 24px;
  height: 24px;
  margin-right: 10px;
  vertical-align: middle;
}
.image-preview {
  max-width: 100%;
  height: auto;
  margin-top: 20px;
  border: 2px solid #ccc;
  border-radius: 5px;
}

.dragging {
  background-color: #d9f7e1; /* Light green to indicate drop area is active */
  border-color: #027562;
}
</style>
