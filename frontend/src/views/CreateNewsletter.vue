<!-- 
  =====================================================================================
  CreateNewsletter.vue - Create New Story Newsletter
  =====================================================================================
  Purpose: Form page to create a new story newsletter.
           Similar to CreateTopic.vue structure.
  
  Route: /stories/newsletters/create
  
  Features:
  - Newsletter name input (4-255 chars, emojis allowed, per-creator uniqueness)
  - Newsletter description textarea (max 500 chars)
  - Newsletter banner image upload (for hero sections)
  - Newsletter display photo upload (for cards)
  - Preview card
  - Form validation
  
  Backend Endpoints Used:
  - POST /stories/createNewsletter - Create new newsletter
  
  Related Files:
  - backend/scripts/stories.py - Backend API endpoints
  - frontend/src/router/modules/story.js - Route registration
  - frontend/src/views/CreateTopic.vue - Reference for structure/styling
  - frontend/src/views/BrowseStoryNewsletters.vue - Newsletters listing page
  - frontend/src/views/SpecificStoryNewsletter.vue - Individual newsletter page
  
  Database Tables:
  - newsletters
  
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
                    'is-valid': nameAvailable && formData.newsletterName.length >= 4
                  }"
                  v-model="formData.newsletterName"
                  @input="validateName"
                  placeholder="Enter newsletter name (4-255 characters)"
                  maxlength="255"
                  required
                />
                <div v-if="nameError" class="invalid-feedback d-block">{{ nameError }}</div>
                <div v-else-if="nameAvailable" class="valid-feedback d-block">Newsletter name looks good!</div>
                <small class="form-text text-muted">
                  {{ formData.newsletterName.length }}/255 characters. Emojis allowed. Must be unique among your newsletters.
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

              <!-- Newsletter Banner Image -->
              <div class="mb-4">
                <label class="form-label fw-bold">
                  Newsletter Banner Image <span class="text-muted fw-normal">(Optional)</span>
                </label>
                <p class="small text-muted mb-2">Upload a banner image for the newsletter hero section (recommended: 1200x400px)</p>
                
                <div 
                  class="upload-area border border-2 border-dashed rounded p-4 text-center"
                  :class="{ 'border-primary': isDraggingBanner }"
                  @dragover.prevent="isDraggingBanner = true"
                  @dragleave="isDraggingBanner = false"
                  @drop.prevent="handleBannerDrop"
                >
                  <div v-if="!formData.bannerImagePreview">
                    <i class="bi bi-panorama text-muted" style="font-size: 2.5rem;"></i>
                    <p class="text-muted mt-2 mb-0">Drag & drop a banner image here, or</p>
                    <label class="btn btn-outline-primary mt-2">
                      <i class="bi bi-image me-1"></i> Choose Banner
                      <input 
                        type="file" 
                        accept="image/*"
                        @change="handleBannerSelect"
                        hidden
                      />
                    </label>
                  </div>
                  <div v-else class="position-relative">
                    <img 
                      :src="formData.bannerImagePreview" 
                      alt="Banner preview"
                      class="img-fluid rounded"
                      style="max-height: 150px;"
                    />
                    <button 
                      type="button"
                      class="btn btn-danger btn-sm position-absolute top-0 end-0 m-2"
                      @click="removeBannerImage"
                    >
                      <i class="bi bi-x"></i>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Newsletter Display Photo -->
              <div class="mb-4">
                <label class="form-label fw-bold">
                  Newsletter Display Photo <span class="text-muted fw-normal">(Optional)</span>
                </label>
                <p class="small text-muted mb-2">Upload a display photo for newsletter cards (recommended: 800x600px)</p>
                
                <div 
                  class="upload-area border border-2 border-dashed rounded p-4 text-center"
                  :class="{ 'border-primary': isDraggingDisplay }"
                  @dragover.prevent="isDraggingDisplay = true"
                  @dragleave="isDraggingDisplay = false"
                  @drop.prevent="handleDisplayDrop"
                >
                  <div v-if="!formData.displayImagePreview">
                    <i class="bi bi-card-image text-muted" style="font-size: 2.5rem;"></i>
                    <p class="text-muted mt-2 mb-0">Drag & drop a display photo here, or</p>
                    <label class="btn btn-outline-primary mt-2">
                      <i class="bi bi-image me-1"></i> Choose Photo
                      <input 
                        type="file" 
                        accept="image/*"
                        @change="handleDisplaySelect"
                        hidden
                      />
                    </label>
                  </div>
                  <div v-else class="position-relative">
                    <img 
                      :src="formData.displayImagePreview" 
                      alt="Display photo preview"
                      class="img-fluid rounded"
                      style="max-height: 150px;"
                    />
                    <button 
                      type="button"
                      class="btn btn-danger btn-sm position-absolute top-0 end-0 m-2"
                      @click="removeDisplayImage"
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
                <li class="mb-2">Use an eye-catching banner and display photo</li>
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
        // Banner image (1200x400px) - displayed on newsletter detail page
        bannerImage: null,
        bannerImagePreview: null,
        // Display photo (800x600px) - shown on cards in browse/list views
        displayImage: null,
        displayImagePreview: null,
      },
      
      // Validation
      nameError: '',
      
      // UI State
      submitting: false,
      isDraggingBanner: false,
      isDraggingDisplay: false,
      
      // Default images
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
      defaultCoverImage: "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800",
    };
  },

  computed: {
    isFormValid() {
      const name = this.formData.newsletterName.trim();
      const desc = this.formData.newsletterDesc.trim();
      return name.length >= 4 &&
             name.length <= 255 &&
             desc.length > 0 &&
             !this.nameError;
    },

    previewCoverStyle() {
      // Use banner image for preview, fall back to display image, then default
      const imageUrl = this.formData.bannerImagePreview || 
                       this.formData.displayImagePreview || 
                       this.defaultCoverImage;
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

    const accUsername = localStorage.getItem("88B_accUsername");
    if (accUsername) {
      this.currentUsername = accUsername;
    }

    const accPhoto = localStorage.getItem("88B_accPhoto");
    if (accPhoto) {
      this.currentUserPhoto = accPhoto;
    }
  },

  methods: {
    /**
     * Validate newsletter name
     * Rules: 4-255 characters, emojis allowed, per-creator uniqueness
     * Uniqueness is checked on backend at submit time (not real-time)
     */
    validateName() {
      this.nameError = '';
      const name = this.formData.newsletterName.trim();
      
      if (!name) {
        return;
      }

      if (name.length < 4) {
        this.nameError = 'Newsletter name must be at least 4 characters';
        return;
      }

      if (name.length > 255) {
        this.nameError = 'Newsletter name must be 255 characters or less';
        return;
      }

      // Name is valid (uniqueness checked on submit)
    },

    // ==================== Banner Image Handling ====================
    handleBannerSelect(event) {
      const file = event.target.files[0];
      if (file) {
        this.processBannerImage(file);
      }
    },

    handleBannerDrop(event) {
      this.isDraggingBanner = false;
      const file = event.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) {
        this.processBannerImage(file);
      }
    },

    processBannerImage(file) {
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        useToast().error("Image must be less than 5MB");
        return;
      }

      // Create preview and store base64
      const reader = new FileReader();
      reader.onload = (e) => {
        this.formData.bannerImagePreview = e.target.result;
        this.formData.bannerImage = e.target.result; // Store base64 for API
      };
      reader.readAsDataURL(file);
    },

    removeBannerImage() {
      this.formData.bannerImage = null;
      this.formData.bannerImagePreview = null;
    },

    // ==================== Display Photo Handling ====================
    handleDisplaySelect(event) {
      const file = event.target.files[0];
      if (file) {
        this.processDisplayImage(file);
      }
    },

    handleDisplayDrop(event) {
      this.isDraggingDisplay = false;
      const file = event.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) {
        this.processDisplayImage(file);
      }
    },

    processDisplayImage(file) {
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        useToast().error("Image must be less than 5MB");
        return;
      }

      // Create preview and store base64
      const reader = new FileReader();
      reader.onload = (e) => {
        this.formData.displayImagePreview = e.target.result;
        this.formData.displayImage = e.target.result; // Store base64 for API
      };
      reader.readAsDataURL(file);
    },

    removeDisplayImage() {
      this.formData.displayImage = null;
      this.formData.displayImagePreview = null;
    },

    // ==================== Form Submission ====================
    async submitForm() {
      if (!this.isFormValid) return;

      this.submitting = true;

      try {
        const formPayload = {
          newsletterName: this.formData.newsletterName.trim(),
          newsletterDesc: this.formData.newsletterDesc.trim(),
          creatorUserID: this.userID,
          creatorUserType: this.userType,
          // Base64 images - backend will upload to S3
          bannerImage64: this.formData.bannerImage || null,
          displayImage64: this.formData.displayImage || null,
        };
        
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/stories/createNewsletter`,
          formPayload
        );
        
        if (response.data.code === 201) {
          useToast().success("Newsletter created successfully!");
          const newsletterId = response.data.data.newsletterID;
          const slug = this.slugify(this.formData.newsletterName);
          this.$router.push(`/stories/newsletters/${newsletterId}/${slug}`);
        } else if (response.data.code === 409) {
          // Duplicate name for this creator
          this.nameError = 'You already have a newsletter with this name';
          useToast().error("Newsletter name already exists for your account");
        } else {
          useToast().error(response.data.message || "Failed to create newsletter");
        }
      } catch (error) {
        console.error("Error creating newsletter:", error);
        if (error.response?.data?.code === 409) {
          this.nameError = 'You already have a newsletter with this name';
          useToast().error("Newsletter name already exists for your account");
        } else {
          useToast().error("Failed to create newsletter. Please try again.");
        }
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
</style>
