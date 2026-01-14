<!-- 
  =====================================================================================
  CreateTopic.vue - Create New Story Topic
  =====================================================================================
  Purpose: Form page to create a new story topic.
           Similar to CreateAssembly.vue structure.
  
  Route: /stories/topics/create
  
  Features:
  - Topic name input (with uniqueness validation)
  - Topic description textarea
  - Drink type multi-select (optional)
  - Topic banner image upload
  - Preview card
  - Form validation
  
  Backend Endpoints Used:
  - POST /createTopic - Create new topic
  - GET /checkTopicNameAvailability/<name> - Check name uniqueness
  
  Related Files:
  - backend/scripts/stories.py - Backend API endpoints
  - frontend/src/router/modules/story.js - Route registration
  - frontend/src/views/CreateAssembly.vue - Reference for structure/styling
  - frontend/src/views/BrowseStoryTopics.vue - Topics listing page
  - frontend/src/views/SpecificStoryTopic.vue - Individual topic page
  
  Database Tables:
  - topics
  
  Access Control:
  - Any logged-in user can create a topic
  =====================================================================================
-->
<template>
  <NavBar />
  
  <div class="container px-4 py-5">
    <!-- Page Header -->
    <div class="row mb-4">
      <div class="col-12">
        <button class="btn btn-outline-secondary btn-sm mb-3" @click="goBack">
          <i class="bi bi-arrow-left me-1"></i> Back to Topics
        </button>
        <h1 class="fw-bold">
          <i class="bi bi-hash text-warning me-2"></i>
          Create New Topic
        </h1>
        <p class="text-muted">Topics help organize stories by theme. Anyone can write stories under your topic.</p>
      </div>
    </div>

    <!-- Login Required Message -->
    <div v-if="userID === 'defaultUser'" class="row">
      <div class="col-lg-8 mx-auto">
        <div class="card shadow-sm">
          <div class="card-body text-center py-5">
            <i class="bi bi-lock text-muted" style="font-size: 4rem;"></i>
            <h4 class="mt-3">Login Required</h4>
            <p class="text-muted">You need to be logged in to create a topic.</p>
            <router-link to="/login" class="btn btn-primary mt-2">
              <i class="bi bi-box-arrow-in-right me-2"></i> Login
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Form -->
    <div v-else class="row">
      <!-- Form Column -->
      <div class="col-lg-7">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <form @submit.prevent="submitForm">
              <!-- Topic Name -->
              <div class="mb-4">
                <label for="topicName" class="form-label fw-bold">
                  Topic Name <span class="text-danger">*</span>
                </label>
                <div class="input-group">
                  <span class="input-group-text">#</span>
                  <input 
                    type="text" 
                    id="topicName"
                    class="form-control"
                    :class="{ 
                      'is-invalid': nameError,
                      'is-valid': nameAvailable && formData.topicName.length > 0
                    }"
                    v-model="formData.topicName"
                    @input="checkNameAvailability"
                    placeholder="Enter topic name"
                    maxlength="100"
                    required
                  />
                </div>
                <div v-if="nameError" class="invalid-feedback d-block">{{ nameError }}</div>
                <div v-else-if="nameAvailable" class="valid-feedback d-block">Topic name is available!</div>
                <div v-else-if="checkingName" class="form-text">
                  <span class="spinner-border spinner-border-sm me-1"></span> Checking availability...
                </div>
                <small class="form-text text-muted">
                  Names must be unique (case-insensitive). {{ formData.topicName.length }}/100 characters
                </small>
              </div>

              <!-- Topic Description -->
              <div class="mb-4">
                <label for="topicDesc" class="form-label fw-bold">
                  Description <span class="text-danger">*</span>
                </label>
                <textarea 
                  id="topicDesc"
                  class="form-control"
                  v-model="formData.topicDesc"
                  rows="4"
                  placeholder="Describe what this topic is about..."
                  maxlength="500"
                  required
                ></textarea>
                <small class="form-text text-muted">{{ formData.topicDesc.length }}/500 characters</small>
              </div>

              <!-- Drink Types (Optional) -->
              <div class="mb-4">
                <label class="form-label fw-bold">
                  Drink Types <span class="text-muted fw-normal">(Optional)</span>
                </label>
                <p class="small text-muted mb-2">Select drink types related to this topic</p>
                
                <!-- TODO: Implement multi-select for drink types -->
                <!-- Model after existing drink type selectors in the app -->
                <div class="drink-types-selector border rounded p-3">
                  <div class="row">
                    <div 
                      v-for="drinkType in availableDrinkTypes" 
                      :key="drinkType"
                      class="col-6 col-md-4 mb-2"
                    >
                      <div class="form-check">
                        <input 
                          type="checkbox"
                          class="form-check-input"
                          :id="`drink-${drinkType}`"
                          :value="drinkType"
                          v-model="formData.drinkTypes"
                        />
                        <label class="form-check-label" :for="`drink-${drinkType}`">
                          {{ drinkType }}
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Topic Banner Image -->
              <div class="mb-4">
                <label class="form-label fw-bold">
                  Topic Banner Image <span class="text-muted fw-normal">(Optional)</span>
                </label>
                <p class="small text-muted mb-2">Upload a banner image for your topic (recommended: 1200x400px)</p>
                
                <!-- Image Upload Area -->
                <!-- TODO: Implement image upload using S3 (model after existing image upload in app) -->
                <div 
                  class="upload-area border border-2 border-dashed rounded p-4 text-center"
                  :class="{ 'border-primary': isDragging }"
                  @dragover.prevent="isDragging = true"
                  @dragleave="isDragging = false"
                  @drop.prevent="handleDrop"
                >
                  <div v-if="!formData.topicBannerPreview">
                    <i class="bi bi-cloud-upload text-muted" style="font-size: 2.5rem;"></i>
                    <p class="text-muted mt-2 mb-0">Drag & drop an image here, or</p>
                    <label class="btn btn-outline-primary mt-2">
                      <i class="bi bi-image me-1"></i> Choose Image
                      <input 
                        type="file" 
                        accept="image/*"
                        @change="handleImageSelect"
                        hidden
                      />
                    </label>
                  </div>
                  <div v-else class="position-relative">
                    <img 
                      :src="formData.topicBannerPreview" 
                      alt="Banner preview"
                      class="img-fluid rounded"
                      style="max-height: 200px;"
                    />
                    <button 
                      type="button"
                      class="btn btn-danger btn-sm position-absolute top-0 end-0 m-2"
                      @click="removeImage"
                    >
                      <i class="bi bi-x"></i>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Submit Button -->
              <div class="d-grid">
                <button 
                  type="submit" 
                  class="btn btn-primary btn-lg fw-bold"
                  :disabled="submitting || !isFormValid"
                >
                  <span v-if="submitting">
                    <span class="spinner-border spinner-border-sm me-2"></span>
                    Creating Topic...
                  </span>
                  <span v-else>
                    <i class="bi bi-plus-circle me-2"></i>
                    Create Topic
                  </span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Preview Column -->
      <div class="col-lg-5 mt-4 mt-lg-0">
        <div class="sticky-preview">
          <h6 class="text-muted mb-3 fw-bold">
            <i class="bi bi-eye me-2"></i>Preview
          </h6>
          
          <div class="card shadow-sm topic-preview-card">
            <!-- Preview Banner -->
            <div 
              class="preview-banner"
              :style="previewBannerStyle"
            >
              <div class="banner-overlay p-3 d-flex align-items-end">
                <h5 class="text-white fw-bold mb-0">
                  #{{ formData.topicName || 'Your Topic Name' }}
                </h5>
              </div>
            </div>
            
            <div class="card-body">
              <p class="card-text small text-muted mb-2">
                {{ formData.topicDesc || 'Your topic description will appear here...' }}
              </p>
              
              <!-- Drink Types Preview -->
              <div v-if="formData.drinkTypes.length > 0" class="mb-2">
                <span 
                  v-for="drinkType in formData.drinkTypes" 
                  :key="drinkType"
                  class="badge bg-warning text-dark me-1 mb-1"
                >
                  {{ drinkType }}
                </span>
              </div>
              
              <!-- Stats Preview -->
              <div class="d-flex gap-3 small text-muted">
                <span><i class="bi bi-people-fill me-1"></i> 0 subscribers</span>
                <span><i class="bi bi-journal-richtext me-1"></i> 0 stories</span>
              </div>
            </div>
          </div>

          <!-- Tips Card -->
          <div class="card mt-4 bg-light">
            <div class="card-body">
              <h6 class="fw-bold mb-3">
                <i class="bi bi-lightbulb text-warning me-2"></i>Tips for a Great Topic
              </h6>
              <ul class="small text-muted mb-0 ps-3">
                <li class="mb-2">Choose a descriptive, memorable name</li>
                <li class="mb-2">Write a clear description of what stories fit here</li>
                <li class="mb-2">Add relevant drink types to help with discovery</li>
                <li class="mb-2">Use a high-quality banner image to stand out</li>
                <li>Consider broader themes that can host many stories</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import { useToast } from "vue-toastification";

export default {
  name: "CreateTopic",
  components: {
    NavBar,
  },
  data() {
    return {
      // User State
      userID: "defaultUser",
      userType: null,
      
      // Form Data
      formData: {
        topicName: '',
        topicDesc: '',
        drinkTypes: [],
        topicBanner: null,
        topicBannerPreview: null,
      },
      
      // Validation
      nameError: '',
      nameAvailable: false,
      checkingName: false,
      nameCheckTimeout: null,
      
      // UI State
      submitting: false,
      isDragging: false,
      
      // Available Drink Types
      // TODO: Fetch from backend or use shared constants
      availableDrinkTypes: [
        'Wine',
        'Beer',
        'Whiskey',
        'Gin',
        'Vodka',
        'Rum',
        'Tequila',
        'Brandy',
        'Liqueur',
        'Cocktails',
        'Sake',
        'Other Spirits'
      ],
      
      // Default images
      defaultBannerImage: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
    };
  },

  computed: {
    isFormValid() {
      return this.formData.topicName.trim().length > 0 &&
             this.formData.topicDesc.trim().length > 0 &&
             this.nameAvailable &&
             !this.nameError;
    },

    previewBannerStyle() {
      const imageUrl = this.formData.topicBannerPreview || this.defaultBannerImage;
      return {
        backgroundImage: `url(${imageUrl})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        height: '150px',
      };
    },
  },

  mounted() {
    // Get user info from localStorage
    const accID = localStorage.getItem("88B_accID");
    if (accID) {
      this.userID = accID;
    }
    
    const accType = localStorage.getItem("88B_accType");
    if (accType) {
      this.userType = accType;
    }
  },

  methods: {
    checkNameAvailability() {
      // Debounce the check
      if (this.nameCheckTimeout) {
        clearTimeout(this.nameCheckTimeout);
      }

      this.nameAvailable = false;
      this.nameError = '';

      const name = this.formData.topicName.trim();
      
      // Basic validation
      if (!name) {
        return;
      }

      if (name.length < 3) {
        this.nameError = 'Topic name must be at least 3 characters';
        return;
      }

      if (name.length > 100) {
        this.nameError = 'Topic name must be less than 100 characters';
        return;
      }

      // Check for invalid characters
      if (!/^[a-zA-Z0-9\s\-_]+$/.test(name)) {
        this.nameError = 'Topic name can only contain letters, numbers, spaces, hyphens, and underscores';
        return;
      }

      this.checkingName = true;

      this.nameCheckTimeout = setTimeout(async () => {
        // TODO: Implement API call to /checkTopicNameAvailability/<name>
        try {
          // const response = await fetch(`${process.env.VUE_APP_BACKEND_LINK}/checkTopicNameAvailability/${encodeURIComponent(name)}`);
          // const data = await response.json();
          // if (data.available) {
          //   this.nameAvailable = true;
          // } else {
          //   this.nameError = 'This topic name is already taken';
          // }

          // Placeholder - assume available
          this.nameAvailable = true;
        } catch (error) {
          console.error("Error checking name availability:", error);
          this.nameError = 'Error checking availability';
        } finally {
          this.checkingName = false;
        }
      }, 500);
    },

    handleImageSelect(event) {
      const file = event.target.files[0];
      if (file) {
        this.processImage(file);
      }
    },

    handleDrop(event) {
      this.isDragging = false;
      const file = event.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) {
        this.processImage(file);
      }
    },

    processImage(file) {
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        useToast().error("Image must be less than 5MB");
        return;
      }

      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        this.formData.topicBannerPreview = e.target.result;
        this.formData.topicBanner = file;
      };
      reader.readAsDataURL(file);
    },

    removeImage() {
      this.formData.topicBanner = null;
      this.formData.topicBannerPreview = null;
    },

    async submitForm() {
      if (!this.isFormValid) return;

      this.submitting = true;

      try {
        // TODO: Implement API call to /createTopic
        // 1. First upload image to S3 if provided
        // 2. Then create topic with image URL
        
        // const formPayload = {
        //   topicName: this.formData.topicName.trim(),
        //   topicDesc: this.formData.topicDesc.trim(),
        //   drinkTypes: this.formData.drinkTypes,
        //   topicBanner: uploadedImageUrl,
        //   createdByID: this.userID,
        //   createdByType: this.userType,
        // };
        
        // const response = await fetch(`${process.env.VUE_APP_BACKEND_LINK}/createTopic`, {
        //   method: 'POST',
        //   headers: { 'Content-Type': 'application/json' },
        //   body: JSON.stringify(formPayload),
        // });
        // const data = await response.json();
        
        // if (data.code === 201) {
        //   useToast().success("Topic created successfully!");
        //   this.$router.push(`/stories/topics/${data.topicId}/${this.slugify(this.formData.topicName)}`);
        // }

        useToast().info("Topic creation coming soon!");
      } catch (error) {
        console.error("Error creating topic:", error);
        useToast().error("Failed to create topic. Please try again.");
      } finally {
        this.submitting = false;
      }
    },

    goBack() {
      this.$router.push('/stories/topics');
    },

    slugify(text) {
      if (!text) return '';
      return text
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .trim();
    },
  },
};
</script>

<style scoped>
/* Upload Area Styles */
.upload-area {
  transition: border-color 0.2s, background-color 0.2s;
  cursor: pointer;
}

.upload-area:hover {
  background-color: #f8f9fa;
}

.border-dashed {
  border-style: dashed !important;
}

/* Preview Card Styles */
.topic-preview-card {
  overflow: hidden;
  border-radius: 12px;
}

.preview-banner {
  position: relative;
}

.banner-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  top: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0) 50%);
}

/* Sticky Preview */
.sticky-preview {
  position: sticky;
  top: 100px;
}

/* Drink Types Selector */
.drink-types-selector {
  max-height: 200px;
  overflow-y: auto;
}
</style>
