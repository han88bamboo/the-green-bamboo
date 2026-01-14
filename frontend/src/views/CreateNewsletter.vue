<!-- 
  =====================================================================================
  CreateNewsletter.vue - Create New Story Newsletter
  =====================================================================================
  Purpose: Form page to create a new story newsletter.
           Similar to CreateAssembly.vue structure.
  
  Route: /stories/newsletters/create
  
  Features:
  - Newsletter name input (with uniqueness validation)
  - Newsletter description textarea
  - Drink type multi-select (optional)
  - Newsletter cover image upload
  - Topic association (optional - link newsletter to a topic)
  - Preview card
  - Form validation
  
  Backend Endpoints Used:
  - POST /createNewsletter - Create new newsletter
  - GET /checkNewsletterNameAvailability/<name> - Check name uniqueness
  - GET /getAllTopics - Get topics for association dropdown
  
  Related Files:
  - backend/scripts/stories.py - Backend API endpoints
  - frontend/src/router/modules/story.js - Route registration
  - frontend/src/views/CreateAssembly.vue - Reference for structure/styling
  - frontend/src/views/BrowseStoryNewsletters.vue - Newsletters listing page
  - frontend/src/views/SpecificStoryNewsletter.vue - Individual newsletter page
  
  Database Tables:
  - newsletters
  - topics (for association)
  
  Access Control:
  - Any logged-in user can create a newsletter
  - Only the creator can publish stories to their newsletter
  
  NOTE: For MVP, all newsletters are "free" (no paywall). 
  Email delivery feature is TODO for future implementation.
  =====================================================================================
-->
<template>
  <NavBar />
  
  <div class="container px-4 py-5">
    <!-- Page Header -->
    <div class="row mb-4">
      <div class="col-12">
        <button class="btn btn-outline-secondary btn-sm mb-3" @click="goBack">
          <i class="bi bi-arrow-left me-1"></i> Back to Newsletters
        </button>
        <h1 class="fw-bold">
          <i class="bi bi-envelope-paper-fill text-primary me-2"></i>
          Create New Newsletter
        </h1>
        <p class="text-muted">Newsletters are your personal publishing channel. Only you can publish stories to your newsletter.</p>
      </div>
    </div>

    <!-- Login Required Message -->
    <div v-if="userID === 'defaultUser'" class="row">
      <div class="col-lg-8 mx-auto">
        <div class="card shadow-sm">
          <div class="card-body text-center py-5">
            <i class="bi bi-lock text-muted" style="font-size: 4rem;"></i>
            <h4 class="mt-3">Login Required</h4>
            <p class="text-muted">You need to be logged in to create a newsletter.</p>
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
              <!-- Newsletter Name -->
              <div class="mb-4">
                <label for="newsletterName" class="form-label fw-bold">
                  Newsletter Name <span class="text-danger">*</span>
                </label>
                <input 
                  type="text" 
                  id="newsletterName"
                  class="form-control"
                  :class="{ 
                    'is-invalid': nameError,
                    'is-valid': nameAvailable && formData.newsletterName.length > 0
                  }"
                  v-model="formData.newsletterName"
                  @input="checkNameAvailability"
                  placeholder="Enter newsletter name"
                  maxlength="100"
                  required
                />
                <div v-if="nameError" class="invalid-feedback">{{ nameError }}</div>
                <div v-else-if="nameAvailable" class="valid-feedback">Newsletter name is available!</div>
                <div v-else-if="checkingName" class="form-text">
                  <span class="spinner-border spinner-border-sm me-1"></span> Checking availability...
                </div>
                <small class="form-text text-muted">
                  Names must be unique (case-insensitive). {{ formData.newsletterName.length }}/100 characters
                </small>
              </div>

              <!-- Newsletter Description -->
              <div class="mb-4">
                <label for="newsletterDesc" class="form-label fw-bold">
                  Description <span class="text-danger">*</span>
                </label>
                <textarea 
                  id="newsletterDesc"
                  class="form-control"
                  v-model="formData.newsletterDesc"
                  rows="4"
                  placeholder="What will your newsletter be about? What can subscribers expect?"
                  maxlength="500"
                  required
                ></textarea>
                <small class="form-text text-muted">{{ formData.newsletterDesc.length }}/500 characters</small>
              </div>

              <!-- Associated Topic (Optional) -->
              <div class="mb-4">
                <label for="associatedTopic" class="form-label fw-bold">
                  Associated Topic <span class="text-muted fw-normal">(Optional)</span>
                </label>
                <p class="small text-muted mb-2">Link your newsletter to an existing topic for better discoverability</p>
                
                <!-- TODO: Implement topic selector with autocomplete -->
                <!-- Model after AutocompleteSearchSelector component -->
                <select 
                  id="associatedTopic"
                  class="form-select"
                  v-model="formData.associatedTopicId"
                >
                  <option value="">-- No topic association --</option>
                  <option 
                    v-for="topic in availableTopics" 
                    :key="topic.id"
                    :value="topic.id"
                  >
                    {{ topic.topicName }}
                  </option>
                </select>
              </div>

              <!-- Drink Types (Optional) -->
              <div class="mb-4">
                <label class="form-label fw-bold">
                  Drink Types <span class="text-muted fw-normal">(Optional)</span>
                </label>
                <p class="small text-muted mb-2">Select drink types related to your newsletter content</p>
                
                <!-- TODO: Implement multi-select for drink types -->
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

              <!-- Newsletter Cover Image -->
              <div class="mb-4">
                <label class="form-label fw-bold">
                  Newsletter Cover Image <span class="text-muted fw-normal">(Optional)</span>
                </label>
                <p class="small text-muted mb-2">Upload a cover image for your newsletter (recommended: 800x600px)</p>
                
                <!-- Image Upload Area -->
                <!-- TODO: Implement image upload using S3 -->
                <div 
                  class="upload-area border border-2 border-dashed rounded p-4 text-center"
                  :class="{ 'border-primary': isDragging }"
                  @dragover.prevent="isDragging = true"
                  @dragleave="isDragging = false"
                  @drop.prevent="handleDrop"
                >
                  <div v-if="!formData.coverImagePreview">
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
                      :src="formData.coverImagePreview" 
                      alt="Cover preview"
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

              <!-- Future Feature Notice -->
              <div class="alert alert-info mb-4">
                <i class="bi bi-info-circle me-2"></i>
                <strong>Coming Soon:</strong> Email delivery for subscribers. For now, subscriptions are in-app only.
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
                    Creating Newsletter...
                  </span>
                  <span v-else>
                    <i class="bi bi-plus-circle me-2"></i>
                    Create Newsletter
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
          
          <div class="card shadow-sm newsletter-preview-card">
            <!-- Preview Cover -->
            <div 
              class="preview-cover"
              :style="previewCoverStyle"
            >
              <div class="cover-overlay p-3 d-flex align-items-end">
                <h5 class="text-white fw-bold mb-0">
                  {{ formData.newsletterName || 'Your Newsletter Name' }}
                </h5>
              </div>
            </div>
            
            <div class="card-body">
              <p class="card-text small text-muted mb-2">
                {{ formData.newsletterDesc || 'Your newsletter description will appear here...' }}
              </p>
              
              <!-- Creator Info Preview -->
              <div class="d-flex align-items-center mb-2">
                <img 
                  :src="currentUserPhoto || defaultProfilePhoto" 
                  alt="You"
                  class="rounded-circle me-2"
                  style="width: 24px; height: 24px; object-fit: cover;"
                />
                <small class="text-muted">By {{ currentUsername || 'You' }}</small>
              </div>
              
              <!-- Drink Types Preview -->
              <div v-if="formData.drinkTypes.length > 0" class="mb-2">
                <span 
                  v-for="drinkType in formData.drinkTypes" 
                  :key="drinkType"
                  class="badge bg-primary me-1 mb-1"
                >
                  {{ drinkType }}
                </span>
              </div>

              <!-- Associated Topic Preview -->
              <div v-if="formData.associatedTopicId && getAssociatedTopicName()" class="mb-2">
                <span class="badge bg-warning text-dark">
                  <i class="bi bi-hash me-1"></i>{{ getAssociatedTopicName() }}
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
                <i class="bi bi-lightbulb text-warning me-2"></i>Tips for a Great Newsletter
              </h6>
              <ul class="small text-muted mb-0 ps-3">
                <li class="mb-2">Choose a name that reflects your content focus</li>
                <li class="mb-2">Write a compelling description to attract subscribers</li>
                <li class="mb-2">Associate with a topic to reach a wider audience</li>
                <li class="mb-2">Use an eye-catching cover image</li>
                <li>Post consistently to keep subscribers engaged</li>
              </ul>
            </div>
          </div>

          <!-- What's Different Card -->
          <div class="card mt-4 border-primary">
            <div class="card-header bg-primary text-white">
              <h6 class="mb-0 fw-bold">
                <i class="bi bi-question-circle me-2"></i>Newsletter vs Topic
              </h6>
            </div>
            <div class="card-body small">
              <p class="mb-2"><strong>Topics</strong> are community spaces where anyone can write stories.</p>
              <p class="mb-0"><strong>Newsletters</strong> are your personal channel — only you can publish here, and subscribers follow your content specifically.</p>
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
  name: "CreateNewsletter",
  components: {
    NavBar,
  },
  data() {
    return {
      // User State
      userID: "defaultUser",
      userType: null,
      currentUsername: null,
      currentUserPhoto: null,
      
      // Form Data
      formData: {
        newsletterName: '',
        newsletterDesc: '',
        drinkTypes: [],
        associatedTopicId: '',
        coverImage: null,
        coverImagePreview: null,
      },
      
      // Validation
      nameError: '',
      nameAvailable: false,
      checkingName: false,
      nameCheckTimeout: null,
      
      // UI State
      submitting: false,
      isDragging: false,
      
      // Available Topics
      availableTopics: [],
      loadingTopics: false,
      
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
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
      defaultCoverImage: "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800",
    };
  },

  computed: {
    isFormValid() {
      return this.formData.newsletterName.trim().length > 0 &&
             this.formData.newsletterDesc.trim().length > 0 &&
             this.nameAvailable &&
             !this.nameError;
    },

    previewCoverStyle() {
      const imageUrl = this.formData.coverImagePreview || this.defaultCoverImage;
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

    const accUsername = localStorage.getItem("88B_accUsername");
    if (accUsername) {
      this.currentUsername = accUsername;
    }

    // Load available topics for association dropdown
    await this.loadAvailableTopics();
  },

  methods: {
    async loadAvailableTopics() {
      // TODO: Implement API call to get topics for dropdown
      this.loadingTopics = true;
      try {
        // const response = await fetch(`${process.env.VUE_APP_BACKEND_LINK}/getAllTopics/0`);
        // const data = await response.json();
        // this.availableTopics = data.data || [];
        
        // Placeholder
        this.availableTopics = [];
      } catch (error) {
        console.error("Error loading topics:", error);
      } finally {
        this.loadingTopics = false;
      }
    },

    checkNameAvailability() {
      // Debounce the check
      if (this.nameCheckTimeout) {
        clearTimeout(this.nameCheckTimeout);
      }

      this.nameAvailable = false;
      this.nameError = '';

      const name = this.formData.newsletterName.trim();
      
      // Basic validation
      if (!name) {
        return;
      }

      if (name.length < 3) {
        this.nameError = 'Newsletter name must be at least 3 characters';
        return;
      }

      if (name.length > 100) {
        this.nameError = 'Newsletter name must be less than 100 characters';
        return;
      }

      // Check for invalid characters
      if (!/^[a-zA-Z0-9\s\-_'&]+$/.test(name)) {
        this.nameError = 'Newsletter name contains invalid characters';
        return;
      }

      this.checkingName = true;

      this.nameCheckTimeout = setTimeout(async () => {
        // TODO: Implement API call to /checkNewsletterNameAvailability/<name>
        try {
          // const response = await fetch(`${process.env.VUE_APP_BACKEND_LINK}/checkNewsletterNameAvailability/${encodeURIComponent(name)}`);
          // const data = await response.json();
          // if (data.available) {
          //   this.nameAvailable = true;
          // } else {
          //   this.nameError = 'This newsletter name is already taken';
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

    getAssociatedTopicName() {
      if (!this.formData.associatedTopicId) return null;
      const topic = this.availableTopics.find(t => t.id === this.formData.associatedTopicId);
      return topic ? topic.topicName : null;
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
        this.formData.coverImagePreview = e.target.result;
        this.formData.coverImage = file;
      };
      reader.readAsDataURL(file);
    },

    removeImage() {
      this.formData.coverImage = null;
      this.formData.coverImagePreview = null;
    },

    async submitForm() {
      if (!this.isFormValid) return;

      this.submitting = true;

      try {
        // TODO: Implement API call to /createNewsletter
        // 1. First upload image to S3 if provided
        // 2. Then create newsletter with image URL
        
        // const formPayload = {
        //   newsletterName: this.formData.newsletterName.trim(),
        //   newsletterDesc: this.formData.newsletterDesc.trim(),
        //   drinkTypes: this.formData.drinkTypes,
        //   associatedTopicId: this.formData.associatedTopicId || null,
        //   newsletterPhoto: uploadedImageUrl,
        //   createdByID: this.userID,
        //   createdByType: this.userType,
        // };
        
        // const response = await fetch(`${process.env.VUE_APP_BACKEND_LINK}/createNewsletter`, {
        //   method: 'POST',
        //   headers: { 'Content-Type': 'application/json' },
        //   body: JSON.stringify(formPayload),
        // });
        // const data = await response.json();
        
        // if (data.code === 201) {
        //   useToast().success("Newsletter created successfully!");
        //   this.$router.push(`/stories/newsletters/${data.newsletterId}/${this.slugify(this.formData.newsletterName)}`);
        // }

        useToast().info("Newsletter creation coming soon!");
      } catch (error) {
        console.error("Error creating newsletter:", error);
        useToast().error("Failed to create newsletter. Please try again.");
      } finally {
        this.submitting = false;
      }
    },

    goBack() {
      this.$router.push('/stories/newsletters');
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
.newsletter-preview-card {
  overflow: hidden;
  border-radius: 12px;
}

.preview-cover {
  position: relative;
}

.cover-overlay {
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
