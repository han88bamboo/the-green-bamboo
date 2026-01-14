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
  - Drink type multi-select (optional, fetched from backend)
  - Topic banner image upload
  - Preview card
  - Form validation
  
  Backend Endpoints Used:
  - POST /stories/createTopic - Create new topic
  
  Related Files:
  - backend/scripts/stories.py - Backend API endpoints
  - frontend/src/router/modules/story.js - Route registration
  - frontend/src/views/CreateAssembly.vue - Reference for structure/styling
  - frontend/src/views/BrowseStoryTopics.vue - Topics listing page
  - frontend/src/views/SpecificStoryTopic.vue - Individual topic page
  
  Database Tables:
  - topics
  
  Access Control:
  - Admin only (users.isAdmin = true)
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

    <!-- Admin Required Message -->
    <div v-else-if="!isAdmin" class="row">
      <div class="col-lg-8 mx-auto">
        <div class="card shadow-sm">
          <div class="card-body text-center py-5">
            <i class="bi bi-shield-lock text-muted" style="font-size: 4rem;"></i>
            <h4 class="mt-3">Admin Access Required</h4>
            <p class="text-muted">Only administrators can create topics.</p>
            <router-link to="/stories/topics" class="btn btn-outline-primary mt-2">
              <i class="bi bi-arrow-left me-2"></i> Back to Topics
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
                  <input 
                    type="text" 
                    id="topicName"
                    class="form-control"
                    :class="{ 
                      'is-invalid': nameError,
                      'is-valid': nameAvailable && formData.topicName.length >= 4
                    }"
                    v-model="formData.topicName"
                    @input="validateName"
                    placeholder="Enter topic name (4-255 characters)"
                    maxlength="255"
                    required
                  />
                </div>
                <div v-if="nameError" class="invalid-feedback d-block">{{ nameError }}</div>
                <div v-else-if="nameAvailable" class="valid-feedback d-block">Topic name looks good!</div>
                <small class="form-text text-muted">
                  {{ formData.topicName.length }}/255 characters. Emojis allowed.
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
                
                <!-- Loading state for drink types -->
                <div v-if="loadingDrinkTypes" class="text-muted">
                  <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                  Loading drink types...
                </div>
                
                <!-- Drink types checkboxes (pill-style like CreateAssembly) -->
                <div v-else class="d-flex flex-wrap gap-2">
                  <div 
                    v-for="drinkType in drinkTypesList" 
                    :key="drinkType.drinkType"
                    class="drink-type-pill"
                    :class="{ 'selected': formData.drinkTypes.includes(drinkType.drinkType) }"
                    @click="toggleDrinkType(drinkType.drinkType)"
                  >
                    {{ drinkType.drinkType }}
                  </div>
                </div>
                
                <!-- Selected drink types display -->
                <div v-if="formData.drinkTypes.length > 0" class="mt-2">
                  <small class="text-success">
                    <i class="bi bi-check-circle me-1"></i>
                    Selected: {{ formData.drinkTypes.join(', ') }}
                  </small>
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
                  {{ formData.topicName || 'Your Topic Name' }}
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
      isAdmin: false,
      
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
      
      // UI State
      submitting: false,
      isDragging: false,
      loading: false,
      error: null,
      
      // Drink types from database
      drinkTypesList: [],
      loadingDrinkTypes: false,
      
      // Default images https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800
      defaultBannerImage: "https://i0.wp.com/highestspirits.com/wp-content/uploads/2018/10/jnpup.jpg?fit=1920%2C1281",
    };
  },

  computed: {
    isFormValid() {
      return this.formData.topicName.trim().length >= 4 &&
             this.formData.topicName.trim().length <= 255 &&
             !this.nameError &&
             this.nameAvailable;
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

  async mounted() {
    // Get user info from localStorage
    const accID = localStorage.getItem("88B_accID");
    if (accID) {
      this.userID = accID;
    }
    
    const accType = localStorage.getItem("88B_accType");
    if (accType) {
      this.userType = accType;
    }

    // Check if user is admin
    const isAdminStr = localStorage.getItem("88B_isAdmin");
    if (isAdminStr !== null) {
      this.isAdmin = isAdminStr === 'true';
    } else if (this.userID !== 'defaultUser' && this.userType === 'user') {
      // Fallback: fetch admin status from API if not in localStorage
      await this.checkAdminStatus();
    }

    // Redirect if not logged in
    if (!this.userID || this.userID === 'defaultUser') {
      const toast = useToast();
      toast.error('Please log in to create a topic.');
      this.$router.push('/stories/topics');
      return;
    }

    // Load drink types from API
    this.getDrinkTypes();
  },

  methods: {
    async checkAdminStatus() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUser/${this.userID}`
        );
        if (response.data && response.data.isAdmin) {
          this.isAdmin = true;
          localStorage.setItem("88B_isAdmin", "true");
        } else {
          this.isAdmin = false;
          localStorage.setItem("88B_isAdmin", "false");
        }
      } catch (error) {
        console.error("Error checking admin status:", error);
      }
    },

    // Validate topic name (4-255 chars, emojis allowed)
    validateName() {
      this.nameAvailable = false;
      this.nameError = '';

      const name = this.formData.topicName.trim();
      
      // Basic validation
      if (!name) {
        return;
      }

      if (name.length < 4) {
        this.nameError = 'Topic name must be at least 4 characters';
        return;
      }

      if (name.length > 255) {
        this.nameError = 'Topic name cannot exceed 255 characters';
        return;
      }

      // Name is valid - we'll check uniqueness on submit (like assemblies)
      this.nameAvailable = true;
    },

    // Toggle drink type selection (like CreateAssembly)
    toggleDrinkType(drinkType) {
      const index = this.formData.drinkTypes.indexOf(drinkType);
      if (index > -1) {
        // Remove if already selected
        this.formData.drinkTypes.splice(index, 1);
      } else {
        // Add if not selected
        this.formData.drinkTypes.push(drinkType);
      }
    },

    // Get drink types from database (like CreateAssembly)
    async getDrinkTypes() {
      this.loadingDrinkTypes = true;
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getDrinkTypes`
        );
        // API returns array directly
        this.drinkTypesList = response.data || [];
      } catch (error) {
        console.error('Error fetching drink types:', error);
        // Don't show error - drink types are optional
      } finally {
        this.loadingDrinkTypes = false;
      }
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

      // Create preview and convert to base64
      const reader = new FileReader();
      reader.onload = (e) => {
        this.formData.topicBannerPreview = e.target.result;
        this.formData.topicBanner = e.target.result; // Store base64 for upload
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
      this.error = null;

      try {
        // Build the request payload (image is base64, backend handles S3 upload)
        const topicPayload = {
          creatorID: this.userID,
          creatorType: this.userType,
          topicName: this.formData.topicName.trim(),
          topicDesc: this.formData.topicDesc.trim() || null,
          drinkTypes: this.formData.drinkTypes,
        };

        // Add banner image if provided (as base64)
        if (this.formData.topicBanner) {
          topicPayload.image64 = this.formData.topicBanner;
        }

        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/stories/createTopic`,
          topicPayload
        );

        if (response.data.code === 201) {
          const toast = useToast();
          toast.success('Topic created successfully!');
          
          // Navigate to the new topic page
          this.$router.push(`/stories/topics/${response.data.data.topicID}/${this.slugify(this.formData.topicName)}`);
        } else {
          // Handle validation errors from backend (e.g., duplicate name)
          this.error = response.data.message || 'Failed to create topic. Please try again.';
          if (response.data.message && response.data.message.includes('already exists')) {
            this.nameError = response.data.message;
            this.nameAvailable = false;
          }
          useToast().error(this.error);
        }
      } catch (error) {
        console.error('Error creating topic:', error);
        if (error.response && error.response.data && error.response.data.message) {
          this.error = error.response.data.message;
          if (this.error.includes('already exists')) {
            this.nameError = this.error;
            this.nameAvailable = false;
          }
        } else {
          this.error = 'Failed to create topic. Please try again later.';
        }
        useToast().error(this.error);
      } finally {
        this.submitting = false;
      }
    },

    goBack() {
      this.$router.back();
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

/* Drink Type Pills (like CreateAssembly) */
.drink-type-pill {
  padding: 8px 16px;
  border: 2px solid #dee2e6;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #fff;
  font-size: 14px;
}

.drink-type-pill:hover {
  border-color: #0d6efd;
  background-color: #f8f9fa;
}

.drink-type-pill.selected {
  border-color: #0d6efd;
  background-color: #0d6efd;
  color: white;
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary:disabled {
  background-color: #6c757d;
  border-color: #6c757d;
  cursor: not-allowed;
}
</style>
