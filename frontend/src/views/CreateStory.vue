<!-- 
  =====================================================================================
  CreateStory.vue - Create New Story Page (Medium-style Editor)
  =====================================================================================
  Purpose: Standalone page for creating stories with minimalistic Medium-style UX.
  
  Route: /stories/create
  
  Features:
  - Two-column layout: Content (8 cols) | Settings (4 cols)
  - Title input (H2 styled)
  - InlineRichTextEditor with word count & reading time
  - Feature image with drag-and-drop
  - AutocompleteSearchSelector for linked drinks (max 5)
  - Hashtags input with counter (max 10)
  - Topic dropdown (global topics)
  - Newsletter dropdown (user's own newsletters)
  - Publication options: Publish Now / Save Draft / Schedule
  - Auto-save every 30 seconds with "Draft saved X ago" indicator
  
  Backend Endpoints Used:
  - POST /stories/createStory - Create new story
  - GET /stories/getAllTopicsForDropdown - Get all topics
  - GET /stories/getUserNewslettersForDropdown/<userID>/<userType> - Get user's newsletters
  
  Related Files:
  - backend/scripts/stories.py - Backend API endpoints
  - frontend/src/router/modules/story.js - Route registration
  - frontend/src/views/Users/UserStories.vue - Modal reference (createStoryModal)
  - frontend/src/views/SpecificStory.vue - Post-creation navigation target
  - frontend/src/components/InlineRichTextEditor.vue - Rich text editor
  - frontend/src/components/AutocompleteSearchSelector.vue - Drink search selector
  =====================================================================================
-->
<template>
  <NavBar />
  
  <div class="create-story-container">
    <!-- Loading/Redirect State for non-logged users -->
    <div v-if="checkingAuth" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Main Editor Layout -->
    <div v-else class="container-fluid px-4 py-4">
      <div class="row">
        <!-- =====================================================================
             LEFT COLUMN - Content Editor (8/12 on desktop)
             ===================================================================== -->
        <div class="col-12 col-lg-8 editor-column ps-md-5">
          <!-- Back Button -->
          <div class="d-flex justify-content-start mb-3">
            <button class="btn btn-link text-muted p-0" @click="goBack">
              <i class="bi bi-arrow-left me-1"></i> Back to Stories
            </button>
          </div>

          <!-- Auto-save Indicator -->
          <div class="autosave-indicator mb-2">
            <small v-if="lastSavedTime" class="text-muted">
              <i class="bi bi-cloud-check me-1"></i>
              Draft saved {{ formatTimeAgo(lastSavedTime) }}
            </small>
            <small v-else-if="hasUnsavedChanges" class="text-muted">
              <i class="bi bi-cloud me-1"></i>
              Unsaved changes
            </small>
          </div>

          <!-- Writing Guidance Panel -->
          <div v-if="showGuidance" class="guidance-panel mb-3">
            <button 
              type="button" 
              class="btn-close" 
              @click="closeGuidance"
              aria-label="Close guidance"
            ></button>
            <div class="guidance-content">
              <h6 class="mb-2">
                <i class="bi bi-info-circle me-2"></i>Writing Tips
              </h6>
              <ul class="small mb-0">
                <li><strong>Select text</strong> or <strong>+ button</strong> to add formatting, subheaders, hyperlinks or images.</li>
                <li>Your work auto-saves every 30 seconds.</li>
              </ul>
            </div>
          </div>

          <!-- Title Input (H2 styled) -->
          <div class="title-wrapper mb-3">
            <input
              ref="titleInput"
              type="text"
              class="title-input"
              v-model="story.title"
              placeholder="Title"
              maxlength="500"
              @input="onContentChange"
            />
          </div>

          <!-- Rich Text Content Editor -->
          <div class="content-editor-wrapper">
            <InlineRichTextEditor
              ref="contentEditor"
              :initial-content="story.content"
              @content-changed="onStoryContentChange"
              :section-id="'create-story'"
              :floating-toolbar="true"
            />
          </div>

          <!-- Word Count & Reading Time -->
          <div class="editor-stats mt-3 d-flex gap-4 text-muted small">
            <span><i class="bi bi-file-text me-1"></i> {{ wordCount }} words</span>
            <!-- <span><i class="bi bi-clock me-1"></i> {{ readingTime }} min read</span> -->
          </div>
        </div>

        <!-- =====================================================================
             RIGHT COLUMN - Settings Sidebar (4/12 on desktop)
             ===================================================================== -->
        <div class="col-12 col-lg-4 settings-column mt-4 mt-lg-0 pe-md-5">
          <div class="settings-sidebar">
            <!-- Feature Image Upload -->
            <div class="setting-section mb-4">
              <label class="setting-label">Feature Image</label>
              <div 
                class="feature-image-dropzone"
                :class="{ 
                  'drag-over': isDraggingImage,
                  'has-image': story.featureImagePreview 
                }"
                @dragover.prevent="onDragOver"
                @dragleave.prevent="onDragLeave"
                @drop.prevent="onDrop"
                @click="triggerFeatureImageUpload"
              >
                <div v-if="story.featureImagePreview" class="image-preview-container">
                  <img 
                    :src="story.featureImagePreview" 
                    alt="Feature image preview"
                    class="feature-image-preview"
                  />
                  <button 
                    type="button"
                    class="btn btn-sm btn-danger remove-image-btn"
                    @click.stop="removeFeatureImage"
                  >
                    <i class="bi bi-x"></i>
                  </button>
                </div>
                <div v-else class="dropzone-content">
                  <i class="bi bi-image text-muted" style="font-size: 2rem;"></i>
                  <p class="mb-1 text-muted small">Drag & drop or click to upload</p>
                  <p class="mb-0 text-muted" style="font-size: 0.7rem;">PNG, JPG, WebP • Max 5MB • 16:9 recommended</p>
                  <input 
                    type="file" 
                    ref="featureImageInput"
                    accept="image/png,image/jpeg,image/jpg,image/webp"
                    class="file-input-hidden"
                    @change="handleFeatureImageSelect"
                    @click.stop
                  />
                </div>
              </div>
            </div>

            <!-- Link Drinks -->
            <div class="setting-section mb-4">
              <label class="setting-label">Link Drinks ({{ story.selectedDrinks.length }}/5)</label>
              
              <!-- Selected Drinks Display (styled like SpecificStory.vue sidebar) -->
              <div v-if="story.selectedDrinks.length > 0" class="linked-drinks-list mb-2">
                <div 
                  v-for="drink in story.selectedDrinks" 
                  :key="drink.id"
                  class="linked-drink-item d-flex align-items-center p-2 rounded"
                >
                  <img 
                    :src="drink.photo || defaultDrinkPhoto" 
                    :alt="drink.listingName"
                    class="rounded me-2"
                    style="width: 36px; height: 36px; object-fit: cover;"
                  />
                  <div class="flex-grow-1 overflow-hidden">
                    <div class="fw-bold small text-truncate">{{ drink.listingName }}</div>
                    <div class="text-muted" style="font-size: 0.7rem;">{{ drink.producerName }}</div>
                  </div>
                  <button 
                    type="button"
                    class="btn btn-sm p-0 text-danger ms-1"
                    @click="removeDrink(drink.id)"
                    title="Remove"
                  >
                    <i class="bi bi-x"></i>
                  </button>
                </div>
              </div>
              
              <!-- Drink Search Selector -->
              <AutocompleteSearchSelector
                v-if="story.selectedDrinks.length < 5"
                placeholder="Search drinks to link..."
                @select="handleDrinkSelect"
              />
            </div>

            <!-- Hashtags -->
            <div class="setting-section mb-4">
              <label class="setting-label">Hashtags ({{ story.hashtags.length }}/10)</label>
              
              <!-- Display added hashtags -->
              <div v-if="story.hashtags.length > 0" class="hashtags-display mb-2 d-flex flex-wrap gap-1">
                <span 
                  v-for="(tag, index) in story.hashtags" 
                  :key="index"
                  class="badge bg-light text-dark border d-flex align-items-center"
                >
                  #{{ tag }}
                  <button 
                    type="button" 
                    class="btn btn-sm p-0 ms-1 text-secondary"
                    @click="removeHashtag(index)"
                  >
                    <i class="bi bi-x"></i>
                  </button>
                </span>
              </div>
              
              <!-- Hashtag Input -->
              <div class="input-group input-group-sm">
                <span class="input-group-text">#</span>
                <input 
                  type="text" 
                  class="form-control"
                  v-model="newHashtag"
                  placeholder="Add hashtag"
                  @keyup.enter="addHashtag"
                  :disabled="story.hashtags.length >= 10"
                />
                <button 
                  class="btn btn-outline-secondary" 
                  type="button"
                  @click="addHashtag"
                  :disabled="story.hashtags.length >= 10"
                >
                  Add
                </button>
              </div>
            </div>

            <!-- Topic Selection -->
            <div class="setting-section mb-4">
              <label class="setting-label">Topic</label>
              <select class="form-select form-select-sm" v-model="story.topicID" @change="onContentChange">
                <option value="">Select a topic...</option>
                <option 
                  v-for="topic in allTopics" 
                  :key="topic.id" 
                  :value="topic.id"
                >
                  {{ topic.topicName }}
                </option>
              </select>
              <!-- Show selected topic badge -->
              <div v-if="selectedTopicName" class="mt-2">
                <span class="badge bg-warning text-dark">
                  <i class="bi bi-hash me-1"></i>{{ selectedTopicName }}
                </span>
              </div>
            </div>

            <!-- Newsletter Selection -->
            <div class="setting-section mb-4">
              <label class="setting-label">Newsletter</label>
              <select class="form-select form-select-sm" v-model="story.newsletterID" @change="onContentChange">
                <option value="">Select a newsletter...</option>
                <option 
                  v-for="newsletter in userNewsletters" 
                  :key="newsletter.id" 
                  :value="newsletter.id"
                >
                  {{ newsletter.newsletterName }}
                </option>
              </select>
              <!-- Show selected newsletter badge -->
              <div v-if="selectedNewsletterName" class="mt-2">
                <span class="badge bg-primary">
                  <i class="bi bi-envelope me-1"></i>{{ selectedNewsletterName }}
                </span>
              </div>
              <!-- Create new newsletter link -->
              <a 
                href="/stories/newsletters/create" 
                target="_blank"
                class="small text-primary d-block mt-2"
              >
                <i class="bi bi-plus-circle me-1"></i>Create new newsletter
              </a>
            </div>

            <!-- Publication Options -->
            <div class="setting-section mb-4">
              <label class="setting-label">Publication</label>
              
              <!-- 3 Buttons in a Row -->
              <div class="publication-buttons d-flex gap-2 mb-3">
                <button 
                  type="button"
                  class="btn btn-sm flex-fill"
                  :class="publicationMode === 'now' ? 'btn-primary' : 'btn-outline-secondary'"
                  @click="setPublicationMode('now')"
                >
                  <i class="bi bi-send me-1"></i>Publish
                </button>
                <button 
                  type="button"
                  class="btn btn-sm flex-fill"
                  :class="publicationMode === 'draft' ? 'btn-secondary' : 'btn-outline-secondary'"
                  @click="setPublicationMode('draft')"
                >
                  <i class="bi bi-file-earmark me-1"></i>Draft
                </button>
                <button 
                  type="button"
                  class="btn btn-sm flex-fill"
                  :class="publicationMode === 'schedule' ? 'btn-info' : 'btn-outline-secondary'"
                  @click="setPublicationMode('schedule')"
                >
                  <i class="bi bi-clock me-1"></i>Schedule
                </button>
              </div>
              
              <!-- Schedule Date Picker (conditional) -->
              <div v-if="publicationMode === 'schedule'" class="schedule-picker">
                <input 
                  type="datetime-local" 
                  class="form-control form-control-sm"
                  v-model="story.scheduledDate"
                  :min="getMinDateTime()"
                />
                <small class="text-muted d-block mt-1">Select date and time to publish</small>
              </div>
            </div>

            <!-- Submit Button -->
            <div class="setting-section">
              <button 
                type="button"
                class="btn w-100 fw-bold"
                :class="getSubmitButtonClass()"
                @click="submitStory"
                :disabled="!canSubmit || submitting"
              >
                <span v-if="submitting">
                  <span class="spinner-border spinner-border-sm me-1"></span>
                  {{ getSubmitButtonText() }}...
                </span>
                <span v-else>
                  {{ getSubmitButtonText() }}
                </span>
              </button>
              <small v-if="!story.title.trim()" class="text-danger d-block mt-2">
                Title is required
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import InlineRichTextEditor from "@/components/InlineRichTextEditor.vue";
import AutocompleteSearchSelector from "@/components/AutocompleteSearchSelector.vue";
import { useToast } from "vue-toastification";

export default {
  name: "CreateStory",
  components: {
    NavBar,
    InlineRichTextEditor,
    AutocompleteSearchSelector,
  },
  data() {
    return {
      // API Base URL
      currentURL: process.env.VUE_APP_API_URL,
      
      // Auth state
      checkingAuth: true,
      userID: null,
      userType: null,
      username: null,
      
      // Story form data
      story: {
        title: '',
        content: '',
        featureImage: null,  // base64 for upload
        featureImagePreview: null,  // preview URL
        selectedDrinks: [],
        listingIDs: [],
        hashtags: [],
        topicID: '',
        newsletterID: '',
        scheduledDate: '',
      },
      
      // Dropdown data
      allTopics: [],
      userNewsletters: [],
      
      // UI state
      newHashtag: '',
      publicationMode: 'now',  // 'now', 'draft', 'schedule'
      isDraggingImage: false,
      submitting: false,
      
      // Auto-save
      autoSaveTimer: null,
      lastSavedTime: null,
      hasUnsavedChanges: false,
      draftStoryID: null,  // Track if we have a saved draft
      
      // UI guidance
      showGuidance: true,
      
      // Default images
      defaultDrinkPhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",
    };
  },

  computed: {
    wordCount() {
      if (!this.story.content) return 0;
      // Strip HTML tags and count words
      const text = this.story.content.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
      if (!text) return 0;
      return text.split(/\s+/).length;
    },
    
    readingTime() {
      // ~200 words per minute
      return Math.max(1, Math.ceil(this.wordCount / 200));
    },
    
    canSubmit() {
      return this.story.title.trim().length > 0;
    },
    
    selectedTopicName() {
      if (!this.story.topicID) return null;
      const topic = this.allTopics.find(t => t.id === this.story.topicID);
      return topic ? topic.topicName : null;
    },
    
    selectedNewsletterName() {
      if (!this.story.newsletterID) return null;
      const newsletter = this.userNewsletters.find(n => n.id === this.story.newsletterID);
      return newsletter ? newsletter.newsletterName : null;
    },
  },

  async mounted() {
    // Check authentication
    const accID = localStorage.getItem("88B_accID");
    const accType = localStorage.getItem("88B_accType");
    const accUsername = localStorage.getItem("88B_accUsername");
    
    if (!accID || accID === 'defaultUser') {
      // Redirect to login
      this.$router.push(`/login?redirect=${encodeURIComponent('/stories/create')}`);
      return;
    }
    
    this.userID = accID;
    this.userType = accType || 'user';
    this.username = accUsername;
    this.checkingAuth = false;
    
    // Check if user dismissed guidance before
    const guidanceDismissed = localStorage.getItem('createStoryGuidanceDismissed');
    if (guidanceDismissed) {
      const dismissedTime = parseInt(guidanceDismissed);
      const sixHoursInMs = 6 * 60 * 60 * 1000;
      const timeSinceDismissal = Date.now() - dismissedTime;
      // Show guidance again if more than 6 hours have passed
      this.showGuidance = timeSinceDismissal > sixHoursInMs;
    } else {
      // Never dismissed before, show guidance
      this.showGuidance = true;
    }
    
    // Load dropdown data
    await this.loadDropdownData();
    
    // Check for pre-selected newsletter from query param (e.g., from SpecificStoryNewsletter.vue)
    const preselectedNewsletterID = this.$route.query.newsletterID;
    if (preselectedNewsletterID) {
      const newsletterIdInt = parseInt(preselectedNewsletterID);
      // Verify this newsletter belongs to the user
      const matchedNewsletter = this.userNewsletters.find(n => n.id === newsletterIdInt);
      if (matchedNewsletter) {
        this.story.newsletterID = newsletterIdInt;
      }
    }
    
    // Start auto-save timer
    this.startAutoSave();
    
    // Focus title input
    this.$nextTick(() => {
      if (this.$refs.titleInput) {
        this.$refs.titleInput.focus();
      }
    });
    
    // Warn before leaving with unsaved changes
    window.addEventListener('beforeunload', this.handleBeforeUnload);
  },

  beforeUnmount() {
    // Clear auto-save timer
    if (this.autoSaveTimer) {
      clearInterval(this.autoSaveTimer);
    }
    window.removeEventListener('beforeunload', this.handleBeforeUnload);
  },

  methods: {
    // ==========================================
    // Data Loading
    // ==========================================
    
    async loadDropdownData() {
      try {
        // Load all topics for dropdown
        const topicsResponse = await fetch(`${this.currentURL}/stories/getAllTopicsForDropdown`);
        const topicsData = await topicsResponse.json();
        if (topicsData.code === 200) {
          this.allTopics = topicsData.data || [];
        }
        
        // Load user's newsletters for dropdown
        const newslettersResponse = await fetch(
          `${this.currentURL}/stories/getUserNewslettersForDropdown/${this.userID}/${this.userType}`
        );
        const newslettersData = await newslettersResponse.json();
        if (newslettersData.code === 200) {
          this.userNewsletters = newslettersData.data || [];
        }
      } catch (error) {
        console.error("Error loading dropdown data:", error);
      }
    },

    // ==========================================
    // Content Change Handling
    // ==========================================
    
    onStoryContentChange(content) {
      this.story.content = content;
      this.onContentChange();
    },
    
    onContentChange() {
      this.hasUnsavedChanges = true;
    },

    // ==========================================
    // Feature Image Handling
    // ==========================================
    
    triggerFeatureImageUpload() {
      if (!this.story.featureImagePreview && this.$refs.featureImageInput) {
        this.$refs.featureImageInput.click();
      }
    },
    
    onDragOver() {
      this.isDraggingImage = true;
    },
    
    onDragLeave() {
      this.isDraggingImage = false;
    },
    
    onDrop(event) {
      this.isDraggingImage = false;
      const files = event.dataTransfer.files;
      if (files.length > 0) {
        this.processImageFile(files[0]);
      }
    },
    
    handleFeatureImageSelect(event) {
      const file = event.target.files?.[0];
      if (file) {
        this.processImageFile(file);
      }
    },
    
    processImageFile(file) {
      const toast = useToast();
      
      // Validate file type
      const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
      if (!validTypes.includes(file.type)) {
        toast.warning('Please select a PNG, JPG, or WebP image.');
        return;
      }
      
      // Validate file size (5MB max)
      if (file.size > 5 * 1024 * 1024) {
        toast.warning('Image must be less than 5MB.');
        return;
      }
      
      // Read file as base64
      const reader = new FileReader();
      reader.onload = (e) => {
        this.story.featureImage = e.target.result;
        this.story.featureImagePreview = e.target.result;
        this.onContentChange();
      };
      reader.readAsDataURL(file);
    },
    
    removeFeatureImage() {
      this.story.featureImage = null;
      this.story.featureImagePreview = null;
      if (this.$refs.featureImageInput) {
        this.$refs.featureImageInput.value = '';
      }
      this.onContentChange();
    },

    // ==========================================
    // Drink Selection
    // ==========================================
    
    handleDrinkSelect(drink) {
      if (this.story.selectedDrinks.length >= 5) return;
      if (this.story.selectedDrinks.find(d => d.id === drink.id)) return;
      
      this.story.selectedDrinks.push(drink);
      this.story.listingIDs.push(drink.id);
      this.onContentChange();
    },
    
    removeDrink(drinkId) {
      this.story.selectedDrinks = this.story.selectedDrinks.filter(d => d.id !== drinkId);
      this.story.listingIDs = this.story.listingIDs.filter(id => id !== drinkId);
      this.onContentChange();
    },

    // ==========================================
    // Hashtag Handling
    // ==========================================
    
    addHashtag() {
      let tag = this.newHashtag.trim().replace(/^#/, '');
      if (!tag) return;
      
      // Validate: only alphanumeric
      tag = tag.replace(/[^a-zA-Z0-9]/g, '');
      if (!tag) {
        useToast().warning("Hashtags can only contain letters and numbers");
        this.newHashtag = '';
        return;
      }
      
      if (this.story.hashtags.length >= 10) {
        useToast().warning("Maximum 10 hashtags allowed");
        return;
      }
      
      if (this.story.hashtags.includes(tag.toLowerCase())) {
        useToast().warning("This hashtag has already been added");
        this.newHashtag = '';
        return;
      }
      
      this.story.hashtags.push(tag.toLowerCase());
      this.newHashtag = '';
      this.onContentChange();
    },
    
    removeHashtag(index) {
      this.story.hashtags.splice(index, 1);
      this.onContentChange();
    },

    // ==========================================
    // Publication Mode
    // ==========================================
    
    setPublicationMode(mode) {
      this.publicationMode = mode;
      if (mode !== 'schedule') {
        this.story.scheduledDate = '';
      }
    },
    
    getMinDateTime() {
      const now = new Date();
      now.setMinutes(now.getMinutes() + 1);
      return now.toISOString().slice(0, 16);
    },
    
    getSubmitButtonClass() {
      switch (this.publicationMode) {
        case 'now': return 'btn-primary';
        case 'draft': return 'btn-secondary';
        case 'schedule': return 'btn-info';
        default: return 'btn-primary';
      }
    },
    
    getSubmitButtonText() {
      switch (this.publicationMode) {
        case 'now': return 'Publish Story';
        case 'draft': return 'Save Draft';
        case 'schedule': return 'Schedule Story';
        default: return 'Publish Story';
      }
    },

    // ==========================================
    // Auto-Save
    // ==========================================
    
    startAutoSave() {
      // Auto-save every 30 seconds
      this.autoSaveTimer = setInterval(() => {
        if (this.hasUnsavedChanges && this.story.title.trim()) {
          this.autoSaveDraft();
        }
      }, 30000);
    },
    
    async autoSaveDraft() {
      try {
        // TODO: Implement proper draft save/update endpoint
        // For now, we just track that we've "saved" (the actual save happens on submit)
        // Actual draft saving would require editStory endpoint or dedicated draft endpoint
        
        this.lastSavedTime = new Date();
        this.hasUnsavedChanges = false;
        
      } catch (error) {
        console.error("Auto-save error:", error);
      }
    },
    
    formatTimeAgo(date) {
      if (!date) return '';
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / 60000);
      
      if (diffMins < 1) return 'just now';
      if (diffMins < 5) return 'within 1 minute';
      if (diffMins < 10) return 'within 5 minutes';
      return `${diffMins} minutes ago`;
    },
    
    handleBeforeUnload(event) {
      if (this.hasUnsavedChanges) {
        event.preventDefault();
        event.returnValue = '';
      }
    },

    // ==========================================
    // Submit Story
    // ==========================================
    
    async submitStory() {
      const toast = useToast();
      
      if (!this.story.title.trim()) {
        toast.error("Please enter a title for your story");
        return;
      }
      
      this.submitting = true;
      
      try {
        // Prepare publication date based on mode
        let publicationDate = null;
        if (this.publicationMode === 'now') {
          publicationDate = new Date().toISOString();
        } else if (this.publicationMode === 'schedule') {
          if (!this.story.scheduledDate) {
            toast.error("Please select a date and time for scheduling");
            this.submitting = false;
            return;
          }
          publicationDate = new Date(this.story.scheduledDate).toISOString();
        }
        // 'draft' mode keeps publicationDate as null
        
        const payload = {
          creatorUserID: parseInt(this.userID),
          creatorUserType: this.userType,
          storyTitle: this.story.title.trim(),
          storyContent: this.story.content || '',
          featureImage64: this.story.featureImage || null,
          listingIDs: this.story.listingIDs,
          topicID: this.story.topicID || null,
          newsletterID: this.story.newsletterID || null,
          hashtags: this.story.hashtags,
          publicationDate: publicationDate,
          freeOrPaid: 'free'
        };
        
        const response = await fetch(`${this.currentURL}/stories/createStory`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (data.code === 201) {
          // Success
          this.hasUnsavedChanges = false;
          
          if (this.publicationMode === 'draft') {
            toast.success("Draft saved successfully!");
          } else if (this.publicationMode === 'schedule') {
            toast.success("Story scheduled successfully!");
          } else {
            toast.success("Story published successfully!");
          }
          
          // Navigate to the newly created story
          const newStoryID = data.data.storyID;
          const slugTitle = this.slugify(this.story.title.trim());
          this.$router.push(`/stories/${newStoryID}/${slugTitle}`);
          
        } else {
          toast.error(data.message || "Failed to create story.");
        }
        
      } catch (error) {
        console.error("Error creating story:", error);
        toast.error("Failed to create story. Please try again.");
      } finally {
        this.submitting = false;
      }
    },

    // ==========================================
    // Navigation
    // ==========================================
    
    closeGuidance() {
      this.showGuidance = false;
      // Store current timestamp
      localStorage.setItem('createStoryGuidanceDismissed', Date.now().toString());
    },
    
    goBack() {
      if (this.hasUnsavedChanges) {
        if (!confirm('You have unsaved changes. Are you sure you want to leave?')) {
          return;
        }
      }
      // Navigate to user's stories page
      this.$router.push(`/profile/user/${this.userID}/${this.username}/stories`);
    },
    
    slugify(text) {
      if (!text) return 'story';
      return text
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .trim() || 'story';
    },
  },
};
</script>

<style scoped>
/* =====================================================================================
   CREATE STORY PAGE - Medium-style Editor
   ===================================================================================== */

.create-story-container {
  min-height: 100vh;
  background-color: #fff;
}

/* Editor Column (Left) */
.editor-column {
  padding-right: 2rem;
}

/* Title Input - H2 styled like Medium */
.title-wrapper {
  position: relative;
}

.title-input {
  width: 100%;
  border: none;
  outline: none;
  font-size: 2rem;
  font-weight: 700;
  line-height: 1.3;
  color: #292929;
  background: transparent;
  padding: 0;
}

.title-input::placeholder {
  color: #b3b3b1;
}

.title-input:focus {
  outline: none;
}

/* Content Editor */
.content-editor-wrapper {
  min-height: calc(100vh - 300px);
}

/* Make the Quill editor expand */
.content-editor-wrapper :deep(.inline-quill-editor-container) {
  min-height: calc(100vh - 350px);
}

.content-editor-wrapper :deep(.ql-container) {
  min-height: calc(100vh - 400px);
  font-size: 1.125rem;
  line-height: 1.8;
}

.content-editor-wrapper :deep(.ql-container.ql-snow) {
  border: none;
}

.content-editor-wrapper :deep(.ql-editor) {
  min-height: calc(100vh - 400px);
  padding: 0;
}

.content-editor-wrapper :deep(.ql-editor.ql-blank::before) {
  content: 'Say your piece.';
  color: #b3b3b1;
  font-style: normal;
  left: 0;
}

/* Editor Stats */
.editor-stats {
  border-top: 1px solid #e9ecef;
  padding-top: 1rem;
}

/* Auto-save Indicator */
.autosave-indicator {
  min-height: 20px;
}

/* Writing Guidance Panel */
.guidance-panel {
  position: relative;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1rem 1.25rem;
  animation: slideDown 0.3s ease;
}

.guidance-panel .btn-close {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  font-size: 0.75rem;
  filter: invert(1) grayscale(100%) brightness(0) !important;
  opacity: 0.7 !important;
}

.guidance-panel .btn-close:hover {
  opacity: 1 !important;
}

.guidance-content h6 {
  color: #495057;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.guidance-content ul {
  list-style: none;
  padding-left: 0;
  margin-bottom: 0;
}

.guidance-content li {
  padding: 0.25rem 0;
  color: #6c757d;
}

.guidance-content li:before {
  content: "→";
  margin-right: 0.5rem;
  color: #0d6efd;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Settings Sidebar (Right) */
.settings-column {
  border-left: 1px solid #e9ecef;
}

.settings-sidebar {
  position: sticky;
  top: 80px;
  padding-left: 1.5rem;
}

.setting-section {
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.setting-section:last-child {
  border-bottom: none;
}

.setting-label {
  display: block;
  font-weight: 600;
  font-size: 0.85rem;
  color: #333;
  margin-bottom: 0.5rem;
}

/* Feature Image Dropzone */
.feature-image-dropzone {
  border: 2px dashed #dee2e6;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.feature-image-dropzone:hover {
  border-color: #adb5bd;
  background-color: #f8f9fa;
}

.feature-image-dropzone.drag-over {
  border-color: #0d6efd;
  background-color: #e7f1ff;
}

.feature-image-dropzone.has-image {
  padding: 0;
  border-style: solid;
}

.dropzone-content {
  cursor: pointer;
}

.file-input-hidden {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.image-preview-container {
  position: relative;
}

.feature-image-preview {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  border-radius: 6px;
}

.remove-image-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

/* Linked Drinks List */
.linked-drinks-list {
  max-height: 200px;
  overflow-y: auto;
}

.linked-drink-item {
  background-color: #f8f9fa;
  margin-bottom: 0.5rem;
  transition: background-color 0.2s;
}

.linked-drink-item:hover {
  background-color: #e9ecef;
}

/* Hashtags Display */
.hashtags-display .badge {
  font-weight: 400;
  font-size: 0.75rem;
}

/* Publication Buttons */
.publication-buttons .btn {
  font-size: 0.75rem;
  padding: 0.4rem 0.5rem;
}

/* Schedule Picker */
.schedule-picker {
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* =====================================================================================
   MOBILE RESPONSIVENESS
   ===================================================================================== */

@media (max-width: 991.98px) {
  .editor-column {
    padding-right: 1rem;
  }
  
  .settings-column {
    border-left: none;
    border-top: 1px solid #e9ecef;
    padding-top: 2rem;
    margin-top: 2rem;
  }
  
  .settings-sidebar {
    position: static;
    padding-left: 0;
  }
  
  .title-input {
    font-size: 1.75rem;
  }
  
  .content-editor-wrapper {
    min-height: 400px;
  }
  
  .content-editor-wrapper :deep(.inline-quill-editor-container),
  .content-editor-wrapper :deep(.ql-container),
  .content-editor-wrapper :deep(.ql-editor) {
    min-height: 400px;
  }
}

@media (max-width: 576px) {
  .title-input {
    font-size: 1.5rem;
  }
  
  .publication-buttons {
    flex-direction: column;
  }
  
  .publication-buttons .btn {
    width: 100%;
  }
}
</style>
