<template>
  <NavBar />

  <div class="image-search">
    <h1 class="p-3">Wondering if a drink is worth a try?</h1>
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
        <div class="input-container">
          <input
            type="text"
            placeholder="Paste image link"
            v-model="imageLink"
            class="image-link-input"
          />
          <img
            src="@../../../Images/Others/search.png"
            alt="View Image"
            class="search-icon"
            @click="onShowImage"
          />
        </div>

        <!-- Replace checkbox with reCAPTCHA widget -->
        <div id="recaptcha"></div>

        <button
          @click="onSubmitImage"
          class="submit-button"
        >
          Submit for Reverse Image Search
        </button>
      </div>

      <!-- Show/Hide Image Button -->
      <button v-if="uploadedImage" @click="toggleImage" class="toggle-button">
        {{ imagePreview ? "Hide Image ▼" : "Show Image ▼" }}
      </button>

      <!-- Display Image -->
      <div v-if="imagePreview" class="uploaded-image">
        <h4>Uploaded Image:</h4>
        <img
          v-if="uploadedImage"
          :src="uploadedImage"
          alt="Uploaded drink label"
          class="image-preview"
        />
        <p v-else>No image</p>
      </div>
    </div>
  </div>

  <!-- Popup Notification -->
  <div v-if="showPopup" class="popup">
    <p>{{ popupMessage }}</p>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";

export default {
  name: "ImageSearchView",
  components: { NavBar },
  data() {
    return {
      imageLink: "",
      uploadedImage: "", // Stores the displayed image (uploaded or linked)
      isDragging: false,
      imagePreview: false, // Controls image visibility
      showPopup: false, // Controls popup display
      isHumanChecked: false, // New property to track checkbox state
      apiKey: process.env.VUE_APP_GOOGLE_VISION_API_KEY,
      // CAPTCHA state
      captchaVerified: false,
      captchaToken: "",
      captchaSiteKey: process.env.VUE_APP_GOOGLE_CAPTCHA_API_KEY
    };
  },
  mounted() {
    // If grecaptcha is not already loaded, load the reCAPTCHA API script
    if (!window.grecaptcha) {
      const script = document.createElement("script");
      script.src = "https://www.google.com/recaptcha/api.js?onload=onRecaptchaLoadCallback&render=explicit";
      script.async = true;
      script.defer = true;
      document.head.appendChild(script);
      // Bind the onload callback to the window so the API can call it
      window.onRecaptchaLoadCallback = () => {this.renderRecaptcha();
    };
    } else {
      // If already loaded, render immediately
      this.renderRecaptcha();
    }
  },
  methods: {
    renderRecaptcha() {
      // Render the reCAPTCHA widget in the container with id "recaptcha"
      window.grecaptcha.render("recaptcha", {
        sitekey: this.captchaSiteKey,
        callback: this.onCaptchaSuccess,
        "expired-callback": this.onCaptchaExpired
      });
    },
    onCaptchaSuccess(token) {
      // Callback invoked when CAPTCHA is solved
      this.captchaVerified = true;
      this.captchaToken = token;
      this.captchaTimestamp = Date.now();
      console.log("Captcha verified, token:", token);

      setTimeout(() => {
    // Check if the token is indeed older than 2 minutes
    if (Date.now() - this.captchaTimestamp >= 120000) {
      if (window.grecaptcha) {
        window.grecaptcha.reset();
      }
      this.captchaVerified = false;
      this.captchaToken = "";
      this.triggerPopup("CAPTCHA expired, please complete it again.");
    }
  }, 120000);
    },
    onCaptchaExpired() {
      // Reset CAPTCHA state when it expires
      this.captchaVerified = false;
      this.captchaToken = "";
      console.log("Captcha expired");
    },
    onFileChange(event) {
      const file = event.target.files[0];
      if (file && this.isValidImageType(file)) {
        const reader = new FileReader();
        reader.onload = () => {
          this.uploadedImage = reader.result;
          this.imagePreview = true;
          this.triggerPopup("Image Uploaded Successfully!");
        };
        reader.readAsDataURL(file);
      } else {
        this.triggerPopup(
          "Invalid file type. Please upload a JPG or PNG image!"
        );
      }
    },

    onDrop(event) {
      event.preventDefault();
      this.isDragging = false;

      const file = event.dataTransfer.files[0];
      if (file && this.isValidImageType(file)) {
        const reader = new FileReader();
        reader.onload = () => {
          this.uploadedImage = reader.result;
          this.imagePreview = true;
          this.triggerPopup("Image Uploaded Successfully!");
        };
        reader.readAsDataURL(file);
      } else {
        this.triggerPopup(
          "Invalid file type. Please upload a JPG or PNG image!"
        );
      }
    },

    isValidImageType(file) {
      const allowedExtensions = ["jpg", "jpeg", "png"];
      const fileExtension = file.name.split(".").pop().toLowerCase();
      return allowedExtensions.includes(fileExtension);
    },

    async onShowImage() {
      if (this.imageLink.trim()) {
        if (!this.isValidUrl(this.imageLink)) {
          this.triggerPopup(
            "Invalid URL format. Please enter a valid image link!"
          );
          return;
        }

        const isValidImage = await this.isImageUrl(this.imageLink);
        if (!isValidImage) {
          this.triggerPopup(
            "URL is not a valid image. Please enter an image URL!"
          );
          return;
        }

        this.uploadedImage = this.imageLink;
        this.imagePreview = true;
        this.triggerPopup("Image link successfully loaded!");
      } else {
        console.error("Invalid image link");
      }
    },

    toggleImage() {
      this.imagePreview = !this.imagePreview;
    },
    isValidUrl(string) {
      try {
        new URL(string);
        return true;
      } catch (error) {
        return false;
      }
    },

    async isImageUrl(url) {
      try {
        const response = await fetch(url, { method: "HEAD" });
        const contentType = response.headers.get("content-type");
        return contentType && contentType.startsWith("image/");
      } catch (error) {
        return false;
      }
    },

    onSubmitImage() {
      if (!this.captchaVerified) {
        this.triggerPopup("Please complete the CAPTCHA");
        return;
      }
      if (this.uploadedImage || this.imageLink.trim()) {
        const imageToSend = this.uploadedImage || this.imageLink;
        // Call reverse image search and route to results page
        this.reverseImageSearch(imageToSend)
          .then(({ logo, labels, detectedText }) => {
            if (logo || labels.length > 0 || detectedText) {
              if (window.grecaptcha) {
                window.grecaptcha.reset();
              }
              this.captchaVerified = false;
              this.captchaToken = "";
              // Navigate to results page with detected logo, labels, and text
              this.$router.push({
                path: "/imageSearchResults",
                query: {
                  logo: logo || "",
                  labels: encodeURIComponent(JSON.stringify(labels)), 
                  detectedText: encodeURIComponent(JSON.stringify(detectedText)),
                },
              });
            } else {
              console.error("No logo, labels, or text detected");
            }
          })
          .catch((error) => console.error("Error in reverse image search:", error));
        } else {
          console.error("No image to submit");
          this.triggerPopup("No image detected, please upload an image or enter a link before submitting!")
        }
      },
    
    async reverseImageSearch(image) {

      try {
        let base64Image = image.startsWith("data:image")
          ? image.replace(/^data:image\/(png|jpeg);base64,/, "")
          : await this.convertToBase64(await (await fetch(image)).blob());
        
        const visionApiUrl = `https://vision.googleapis.com/v1/images:annotate?key=${this.apiKey}`;

        const visionRequest = {
          requests: [
            {
              image: { content: base64Image },
              features: [
                { type: "LOGO_DETECTION" },
                { type: "LABEL_DETECTION" },
                { type: "DOCUMENT_TEXT_DETECTION" }, 
              ],
            },
          ],
        };

        const visionResponse = await fetch(visionApiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(visionRequest),
        });

        const visionData = await visionResponse.json();
        console.log("Google Vision API Response:", visionData);

        // Extract the detected logo
        let detectedLogo = visionData.responses[0]?.logoAnnotations?.[0]?.description || null;
        console.log("Detected Logo:", detectedLogo);

        // Extract labels
        let detectedLabels = visionData.responses[0]?.labelAnnotations?.map(labels => labels.description) || [];
        detectedLabels = detectedLabels.filter(Boolean); // Remove undefined/null values
        console.log("Detected Labels:", detectedLabels);

        // Extract detected text from the image
        let detectedText = visionData.responses[0]?.textAnnotations?.map(detectedText => detectedText.description) || [];
        console.log("Detected Text:", detectedText);
        const apiUrl = "http://localhost:5000/getData/getImageSearchResults"; 

      // Send a request to your backend API with the extracted logo, labels, and text
      try {
        const requestData = {
          logo: detectedLogo, // Detected logo from the URL or other source
          text: detectedText, // Detected text (e.g., extracted from the image)
          labels: detectedLabels, // Extracted labels (e.g., categorized text or tags)
        };

        // Log the request data (the dictionary being sent)
        console.log("Request Payload:", JSON.stringify(requestData, null, 2));

        const response = await fetch(apiUrl, {
          method: "POST", // Ensure POST method
          headers: {
            "Content-Type": "application/json", // Correct content type for sending JSON
          },
          body: JSON.stringify(requestData), // Convert request data to JSON string
        });

        // Check if the response is successful (status code 200)
        if (response.ok) {
          // const listings = await response.json(); // Parse JSON response from the backend
          // console.log("Scored Listings:", listings); // Log the response (listings) from the backend
        } else {
          console.error("Error: Failed to fetch listings", response.status);
        }
      } catch (error) {
        console.error("Error during fetch operation:", error);
      }

        if (!detectedLogo && detectedLabels.length === 0 && !detectedText) {
          console.error("No logo, labels, or text detected");
          return null;
        }
        
        return { logo: detectedLogo, labels: detectedLabels, detectedText };
        } catch (error) {
          console.error("Error in reverse image search:", error);
          return null;
        }
      },

    // version 1
    // async reverseImageSearch(image) {
    //   try {
    //     let base64Image = image.startsWith("data:image")
    //       ? image.replace(/^data:image\/(png|jpeg);base64,/, "")
    //       : await this.convertToBase64(await (await fetch(image)).blob());

    //     const visionApiUrl = `https://vision.googleapis.com/v1/images:annotate?key=${this.apiKey}`;

    //     const visionRequest = {
    //       requests: [
    //         {
    //           image: { content: base64Image },
    //           features: [
    //             { type: "LOGO_DETECTION" },
    //             { type: "LABEL_DETECTION" },
    //           ],
    //         },
    //       ],
    //     };

    //     const visionResponse = await fetch(visionApiUrl, {
    //       method: "POST",
    //       headers: { "Content-Type": "application/json" },
    //       body: JSON.stringify(visionRequest),
    //     });

    //     const visionData = await visionResponse.json();
    //     console.log("Google Vision API Response:", visionData);

    //     // Extract the detected logo (if available)
    //     let detectedLogo = null;
    //     if (
    //       visionData.responses &&
    //       visionData.responses[0].logoAnnotations &&
    //       visionData.responses[0].logoAnnotations.length > 0
    //     ) {
    //       detectedLogo = visionData.responses[0].logoAnnotations[0].description;
    //       console.log("Detected Logo:", detectedLogo);
    //     } else {
    //       console.warn("No logo detected");
    //     }

    //     // Extract labels (if available)
    //     let detectedLabels = [];
    //     if (
    //       visionData.responses &&
    //       visionData.responses[0].labelAnnotations &&
    //       visionData.responses[0].labelAnnotations.length > 0
    //     ) {
    //       detectedLabels = visionData.responses[0].labelAnnotations.map(
    //         (label) => label.description
    //       );
    //       console.log("Detected Labels:", detectedLabels);
    //     } else {
    //       console.warn("No labels detected");
    //     }

    //     if (!detectedLogo && detectedLabels.length === 0) {
    //       console.error("No logo or labels detected");
    //       return null;
    //     }

    //     // Return an object with both detected logo and labels
    //     return { logo: detectedLogo, labels: detectedLabels };
    //   } catch (error) {
    //     console.error("Error in reverse image search:", error);
    //     return null;
    //   }
    // },

    // Helper function to convert an image blob to base64
    async convertToBase64(blob) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onload = () =>
          resolve(
            reader.result.replace(/^data:image\/(png|jpeg|jpg);base64,/, "")
          );
        reader.onerror = (error) => reject(error);
      });
    },

    onDragOver(event) {
      event.preventDefault();
      this.isDragging = true;
    },

    onDragLeave() {
      this.isDragging = false;
    },

    triggerPopup(message) {
      this.popupMessage = message;
      this.showPopup = true;
      setTimeout(() => {
        this.showPopup = false;
      }, 3000);
    },
  },
  beforeUnmount() {
    // Clean up reCAPTCHA when the component is about to be destroyed
    if (window.grecaptcha) {
      window.grecaptcha.reset();
    }
  },
};
</script>

<style scoped>
.image-search {
  text-align: center;
  margin-top: 50px;
}

.greybox {
  width: 90%;
  margin: 50px auto;
  background-color: #f4f4f47d;
  border-radius: 5px;
  display: block;
  text-align: center;
  border: 5px solid #027562;
  padding: 50px 10px;
  /* max-width: 500px; */
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

.uploaded-image {
  margin-top: 10px;
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

#recaptcha {
  margin-top: 20px; /* Adjust the value as needed */
}


.image-preview {
  width: 300px;
  height: 300px;
  object-fit: contain;
  margin-top: 20px;
  border: 2px solid #ccc;
  border-radius: 5px;
}

.dragging {
  background-color: #d9f7e1; /* Light green to indicate drop area is active */
  border-color: #027562;
}

.submit-button {
  margin-top: 20px;
  padding: 12px 24px;
  background-color: #027562;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.submit-button:hover {
  background-color: #066251;
  transform: translateY(-2px); /* Adds a hover effect to lift the button */
}

.submit-button:active {
  transform: translateY(1px); /* Adds a pressed effect */
}

.submit-button img {
  width: 20px;
  height: 20px;
}

.submit-button span {
  font-size: 18px;
  font-weight: bold;
}

.link-section {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 100%;
}

@media (max-width: 600px) {
  .search-button {
    width: 90%;
    font-size: 14px;
  }
}

/* Popup Style */
.popup {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #0f0275;
  color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0);
  align-items: center;
  justify-content: center;
  min-width: 200px;
}

/* Make input bar longer */
.input-container {
  position: relative;
  width: 100%;
  max-width: 500px;
}

.image-link-input {
  flex: 1;
  width: 100%;
  padding: 10px 40px 10px 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.search-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  height: 24px;
  transform: translateY(-50%);
  margin-left: 5px;
  cursor: pointer;
  background-color: rgb(255, 255, 255); /* Opaque background */
}

.toggle-button {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px auto;
  background-color: #027562;
  color: white;
  border: none;
  padding: 12px 16px;
  cursor: pointer;
  border-radius: 25px; /* More rounded for a modern look */
  width: auto; /* Auto width to fit text */
  min-width: 150px; /* Ensures a decent size */
  font-size: clamp(14px, 1.2vw, 16px);
  text-align: center;
  transition: background-color 0.3s, transform 0.2s;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.toggle-button:hover {
  background-color: #025c4f;
  transform: scale(1.05);
}

.toggle-button:active {
  background-color: #02473c;
  transform: scale(0.98);
}

.check {
  margin-top: 30px;
}
</style>
