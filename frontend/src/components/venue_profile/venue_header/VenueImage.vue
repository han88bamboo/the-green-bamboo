<template>
  <div class="col-lg-3 col-12 mb-lg-0 mb-3 image-container text-start mobile-col-5">
    
    <!-- Unified Image Display Area -->
    <div :style="isEditing ? 'position: relative; text-align: center;' : ''">
      <div class="image-wrapper">
        <!-- Shimmer overlay during image load (This is the only one we need) -->
        <div v-if="isImageLoading" class="shimmer-overlay">
          <div class="shimmer-animation"></div>
        </div>
        
        <img 
          :src="currentImageSrc" 
          alt="Venue"
          class="producer-bottle-listing-page-image"
          :class="{ 'image-loading': isImageLoading }"
          @error="handleImageError"
          @load="handleImageLoaded"
          @loadstart="handleImageLoadStart"
        >
      </div>
      
      <!-- Edit Mode Controls (conditionally rendered) -->
      <div v-if="isEditing">
        <!-- File Upload Controls -->
        <label 
          for="fileSelectPFP" 
          class="btn primary-light-dropdown"
          style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 2;"
        >
          Choose File
        </label>
        
        <input 
          id="fileSelectPFP" 
          type="file" 
          @change="handleFileSelect" 
          ref="fileInput"
          accept="image/*"
          style="width: 0px; height: 0px; display: none;"
        >
        
        <!-- Action Buttons -->
        <div class="image-controls mt-2">
          <button 
            class="btn primary-light-dropdown m-1"
            @click="revertImage"
            :disabled="!hasChanges"
          >
            Revert
          </button>
          
          <button 
            class="btn primary-light-dropdown m-1"
            @click="removeImage"
          >
            Remove
          </button>
        </div>
      </div>
    </div>

    <!-- Error State - Only show if all images fail -->
    <div v-if="hasError && allImagesFailed" class="alert alert-warning mt-2">
      <small>Failed to load image</small>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VenueImage',
  
  props: {
    // Current venue photo URL
    venuePhoto: {
      type: String,
      default: ''
    },
    
    // Default fallback image
    defaultPhoto: {
      type: String,
      required: true
    },
    
    // Whether component is in edit mode
    isEditing: {
      type: Boolean,
      default: false
    },
    
    // Currently selected new image (from parent)
    selectedImage: {
      type: String,
      default: ''
    },
    
    // Loading state from parent
    loading: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      // Local state
      isLoading: false,
      isImageLoading: true, // Track individual image loading state
      hasError: false,
      originalPhoto: '', // Store original for revert functionality
      failedImages: new Set(), // Track which images have failed
      currentlyDisplayedSrc: '', // Track what's currently being displayed
    }
  },

  computed: {
    /**
     * Determine which image to display based on priority:
     * 1. Selected image (during editing)
     * 2. Venue photo (if not failed)
     * 3. Default photo
     */
    currentImageSrc() {
      // Priority 1: Selected image during editing
      if (this.selectedImage && !this.failedImages.has(this.selectedImage)) {
        return this.selectedImage
      }
      
      // Priority 2: Venue photo (if exists and hasn't failed)
      if (this.venuePhoto && !this.failedImages.has(this.venuePhoto)) {
        return this.venuePhoto
      }
      
      // Priority 3: Default photo
      return this.defaultPhoto
    },

    /**
     * Check if there are unsaved changes
     */
    hasChanges() {
      return this.selectedImage && this.selectedImage !== this.originalPhoto
    },

    /**
     * Check if all possible images have failed to load
     */
    allImagesFailed() {
      return this.failedImages.has(this.defaultPhoto) && 
             (!this.venuePhoto || this.failedImages.has(this.venuePhoto)) &&
             (!this.selectedImage || this.failedImages.has(this.selectedImage))
    }
  },

  watch: {
    // Watch for changes in venue photo to update original
    venuePhoto: {
      immediate: true,
      handler(newPhoto) {
        if (newPhoto && !this.originalPhoto) {
          this.originalPhoto = newPhoto
        }
      }
    },

    // Watch loading prop from parent
    loading(newVal) {
      this.isLoading = newVal
    },

    // Watch for changes in current image source
    currentImageSrc(newSrc) {
      if (newSrc !== this.currentlyDisplayedSrc) {
        this.hasError = false // Reset error state when image changes
        this.isImageLoading = true // Show shimmer when switching images
        this.currentlyDisplayedSrc = newSrc
      }
    }
  },

  methods: {
    /**
     * Handle file selection from input
     * @param {Event} event - File input change event
     */
    handleFileSelect(event) {
      const file = event.target.files[0]
      
      if (!file) {
        return
      }

      // Validate file type
      if (!this.isValidImageFile(file)) {
        this.$emit('error', 'Please select a valid image file (JPG, PNG, GIF)')
        return
      }

      // Validate file size (e.g., max 5MB)
      if (!this.isValidFileSize(file)) {
        this.$emit('error', 'File size must be less than 5MB')
        return
      }

      this.processImageFile(file)
    },

    /**
     * Process the selected image file
     * @param {File} file - Selected image file
     */
    processImageFile(file) {
      this.isLoading = true
      this.hasError = false

      const reader = new FileReader()
      
      reader.onload = (e) => {
        const imageUrl = e.target.result
        this.isLoading = false
        
        // Remove from failed images set if it was there
        this.failedImages.delete(imageUrl)
        
        // Emit the selected image to parent
        this.$emit('image-selected', {
          file: file,
          url: imageUrl,
          name: file.name
        })
      }

      reader.onerror = () => {
        this.isLoading = false
        this.hasError = true
        this.$emit('error', 'Failed to read selected file')
      }

      reader.readAsDataURL(file)
    },

    /**
     * Revert image to original
     */
    revertImage() {
      // Clear file input
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
      
      this.hasError = false
      
      // Emit revert event to parent
      this.$emit('image-reverted', {
        originalPhoto: this.originalPhoto
      })
    },

    /**
     * Remove current image
     */
    removeImage() {
      // Clear file input
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
      
      this.hasError = false
      
      // Emit remove event to parent
      this.$emit('image-removed')
    },

    /**
     * Handle image load start (when loading begins)
     */
    handleImageLoadStart() {
      this.isImageLoading = true
    },

    /**
     * Handle image load errors
     */
    handleImageError(event) {
      const failedSrc = event.target.src
      // console.log('Image failed to load:', failedSrc)
      
      // Add to failed images set
      this.failedImages.add(failedSrc)
      
      // Clear loading state
      this.isImageLoading = false
      
      // If this wasn't the default image, the computed property will automatically 
      // switch to the next available image (including default)
      if (failedSrc !== this.defaultPhoto) {
        // The computed property will handle switching to default
        return
      }
      
      // If even the default image failed, show error state
      this.hasError = true
    },

    /**
     * Handle successful image load
     */
    handleImageLoaded(event) {
      const loadedSrc = event.target.src
      
      // Remove from failed images set if it was there
      this.failedImages.delete(loadedSrc)
      
      // Clear error and loading states
      this.hasError = false
      this.isImageLoading = false
      
      // console.log('Image loaded successfully:', loadedSrc)
    },

    /**
     * Validate if file is a valid image
     * @param {File} file - File to validate
     * @returns {boolean} - Is valid image
     */
    isValidImageFile(file) {
      const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
      return validTypes.includes(file.type)
    },

    /**
     * Validate file size
     * @param {File} file - File to validate
     * @returns {boolean} - Is valid size
     */
    isValidFileSize(file, maxSizeMB = 5) {
      const maxSizeBytes = maxSizeMB * 1024 * 1024
      return file.size <= maxSizeBytes
    },

    /**
     * Public method to trigger file selection
     * Can be called from parent component
     */
    triggerFileSelect() {
      if (this.$refs.fileInput) {
        this.$refs.fileInput.click()
      }
    }
  },

  // Expose methods for parent component access
  expose: ['triggerFileSelect']
}
</script>

<style scoped>
.image-container {
  position: relative;
}

.image-wrapper {
  position: relative;
  display: block;
  width: 100%;
  overflow: hidden;
  border-radius: 8px;
}

.producer-bottle-listing-page-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  transition: opacity 0.3s ease;
  display: block;
  position: relative;
  z-index: 1;

  /* --- ADD THIS LINE --- */
  background-color: #f0f0f0; /* This provides a solid fallback background */
}

.producer-bottle-listing-page-image.image-loading {
  opacity: 0.3;
}

/* Shimmer Effect Styles */
.shimmer-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  pointer-events: none;
  z-index: 2;
  overflow: hidden;
}

.shimmer-animation {
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.6) 50%,
    transparent 100%
  );
  animation: shimmer 1.5s infinite;
  border-radius: 8px;
}

.image-loading-container {
  width: 100%;
  height: 200px;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.shimmer-placeholder {
  width: 100%;
  height: 100%;
  background: #f0f0f0;
  position: relative;
  border-radius: 8px;
  overflow: hidden;
}

.shimmer-placeholder .shimmer-animation {
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.8) 50%,
    transparent 100%
  );
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Dark mode shimmer effect */
@media (prefers-color-scheme: dark) {
  .shimmer-placeholder {
    background: #2a2a2a;
  }
  
  .shimmer-placeholder .shimmer-animation {
    background: linear-gradient(
      90deg,
      transparent 0%,
      rgba(255, 255, 255, 0.1) 50%,
      transparent 100%
    );
  }
  
  .shimmer-overlay .shimmer-animation {
    background: linear-gradient(
      90deg,
      transparent 0%,
      rgba(255, 255, 255, 0.2) 50%,
      transparent 100%
    );
  }
}

.image-controls {
  display: flex;
  justify-content: center;
  gap: 8px;
  position: absolute;
  bottom: -45px;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
}

/* Mobile responsive adjustments */
@media (max-width: 768px) {
  .producer-bottle-listing-page-image {
    height: 150px;
  }
  
  .image-loading-container {
    height: 150px;
  }
  
  .image-controls {
    bottom: -35px;
  }
  
  .image-controls .btn {
    font-size: 0.875rem;
    padding: 0.375rem 0.75rem;
  }
}

/* Error state styling */
.alert {
  font-size: 0.875rem;
  margin-bottom: 0;
}

/* Smooth transitions */
.image-wrapper,
.shimmer-overlay,
.shimmer-animation {
  transition: all 0.3s ease;
}
</style>