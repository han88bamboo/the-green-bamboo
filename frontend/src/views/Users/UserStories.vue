<!-- 
  =====================================================================================
  UserStories.vue - User's Stories Profile Page
  =====================================================================================
  Purpose: Display all stories published by a specific user, sorted by most recent.
           Also provides access to create new stories and manage newsletters.
  
  Route: /profile/user/:userID/:username/stories
  
  Features:
  - Display user's published stories (sorted by publishingDate DESC)
  - Create Story button (opens modal)
  - My Newsletters button (navigates to newsletter management)
  - Story cards modeled after review cards in AllReviews.vue
  
  Backend Endpoints Used:
  - GET /getUserStories/<userID>/<userType>/<offset> - Get user's stories
  - GET /getUserNewsletters/<userID>/<userType> - Get user's newsletters for dropdown
  - POST /createStory - Create a new story
  
  Related Files:
  - backend/scripts/stories.py - Backend API endpoints
  - frontend/src/router/modules/profile.js - Route registration
  - frontend/src/components/UserProfileNavbar.vue - Navigation link
  - frontend/src/views/Users/UserCellarPreview.vue - Similar page structure reference
  - frontend/src/views/Users/AllReviews.vue - Card styling reference
  
  Database Tables:
  - stories
  - newsletters
  - storiesLikes
  - storyComments
  =====================================================================================
-->
<template>
  <NavBar />

  <!-- User Profile Header and Navigation (always visible) -->
  <div v-if="displayUserID && routeUsername" class="userprofile mt-5 mobile-mt-3">
    <div class="container text-start">
      <UserProfileHeader 
        :displayUserData="displayUser"
        :loggedInUserData="loggedInUser"
        :isOwnProfile="ownProfile"
      />
    </div>
    <br>
    <!-- User Profile Navigation -->
    <div class="container text-start">
      <UserProfileNavbar :userID="displayUserID" :username="routeUsername" />
    </div>
  </div>

  <!-- Display when data is still loading -->
  <LoadingWithFunFact v-if="dataLoaded === false" />

  <!-- Display when data fails to load -->
  <div
    class="text-danger fst-italic fw-bold fs-3 pt-5"
    v-if="dataLoaded == null"
  >
    <span>An error occurred while loading this page, please try again!</span>
    <br />
    <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
      <span class="fs-5 fst-italic"> Return to previous page </span>
    </button>
    <router-link :to="'/'" class="mx-1">
      <button class="btn primary-btn btn-sm">
        <span class="fs-5 fst-italic"> Home </span>
      </button>
    </router-link>
  </div>

  <!-- Main Content -->
  <div v-if="dataLoaded" class="userprofile">
    <div class="row col-11 mobile-spacer my-4 mobile-my-2">
      <div class="col-12 col-md-10 mx-auto px-2">
        
        <!-- Page Header and Actions -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h5 class="fw-bold mobile-fs-6 mb-0">
            <i class="bi bi-journal-richtext"></i> Stories
          </h5>
          
          <!-- Action Buttons (only for own profile) -->
          <div v-if="ownProfile" class="d-flex gap-2">
            <!-- My Newsletters Button -->
            <button 
              class="btn btn-outline-primary fw-bold"
              @click="openMyNewsletters"
            >
              <i class="bi bi-envelope-paper me-1"></i> My Newsletters
            </button>
            
            <!-- Create Story Button -->
            <button 
              class="btn primary-btn-less-round-blue fw-bold"
              data-bs-toggle="modal"
              data-bs-target="#createStoryModal"
            >
              <i class="bi bi-plus-circle me-1"></i> Create Story
            </button>
          </div>
        </div>

        <!-- Stories List -->
        <div v-if="stories.length > 0" class="stories-list">
          <!-- TODO: Implement story cards (model after review cards in AllReviews.vue) -->
          <!-- Each story card should display:
               - Story title (clickable, navigates to SpecificStory.vue)
               - Story preview (truncated content)
               - Story photo (first image if available)
               - Like count
               - Comment count
               - Publishing date
               - Topic name (if any)
               - Newsletter name (if any)
               - Hashtags
          -->
          <div 
            v-for="story in stories" 
            :key="story.id"
            class="story-card card mb-3 shadow-sm"
          >
            <div class="card-body">
              <!-- TODO: Implement story card content -->
              <h5 class="card-title">{{ story.storyTitle }}</h5>
              <p class="text-muted small">
                Published {{ formatDate(story.publishingDate) }}
              </p>
              <!-- Placeholder for story content -->
              <p class="card-text text-muted">Story card content coming soon...</p>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-5">
          <i class="bi bi-journal-richtext text-muted" style="font-size: 4rem;"></i>
          <h5 class="mt-3 text-muted">No Stories Yet</h5>
          <p class="text-muted" v-if="ownProfile">
            Share your knowledge and experiences by writing your first story!
          </p>
          <p class="text-muted" v-else>
            {{ displayUser.displayName || routeUsername }} hasn't published any stories yet.
          </p>
          <button 
            v-if="ownProfile"
            class="btn primary-btn-less-round-blue fw-bold mt-3"
            data-bs-toggle="modal"
            data-bs-target="#createStoryModal"
          >
            <i class="bi bi-plus-circle me-1"></i> Create Your First Story
          </button>
        </div>

        <!-- Load More Button -->
        <div v-if="hasMoreStories && stories.length > 0" class="text-center mt-4 mb-5">
          <button 
            class="btn btn-outline-primary" 
            @click="loadMoreStories"
            :disabled="loadingMore"
          >
            <span v-if="loadingMore">
              <span class="spinner-border spinner-border-sm me-1"></span>
              Loading...
            </span>
            <span v-else>Load More Stories</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- =====================================================================================
       CREATE STORY MODAL
       Modeled after the "Create a Post" modal in SpecificAssembly.vue
       ===================================================================================== -->
  <div class="modal fade" id="createStoryModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title fw-bold">Create a Story</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          
          <!-- Story Title -->
          <div class="mb-3">
            <label class="form-label fw-bold">Title <span class="text-danger">*</span></label>
            <input 
              type="text" 
              class="form-control" 
              v-model="newStory.title"
              placeholder="An engaging title for your story..."
              maxlength="500"
            />
            <div class="form-text text-end">{{ newStory.title.length }}/500</div>
          </div>
          
          <!-- Story Content (Rich Text) -->
          <div class="mb-3">
            <label class="form-label fw-bold">Content</label>
            <!-- TODO: Integrate InlineRichTextEditor component (same as Assemblies) -->
            <!-- <InlineRichTextEditor
              ref="storyEditor"
              :initial-content="newStory.content"
              @content-changed="onStoryContentChange"
              :section-id="'new-story'"
            /> -->
            <textarea 
              class="form-control" 
              v-model="newStory.content"
              placeholder="Write your story content here... (Rich text editor coming soon)"
              rows="6"
            ></textarea>
          </div>

          <!-- Image Upload -->
          <div class="mb-3">
            <label class="form-label fw-bold">Images (Max 5)</label>
            <!-- TODO: Implement image upload (same as Assembly post creation) -->
            <div class="d-flex flex-wrap gap-2 mb-2">
              <div 
                v-for="(image, index) in newStory.images" 
                :key="index"
                class="position-relative"
              >
                <img 
                  :src="image.preview" 
                  class="rounded"
                  style="width: 80px; height: 80px; object-fit: cover;"
                />
                <button 
                  class="btn btn-sm btn-danger position-absolute top-0 end-0 rounded-circle p-0"
                  style="width: 20px; height: 20px; line-height: 1;"
                  @click="removeImage(index)"
                >
                  <i class="bi bi-x"></i>
                </button>
              </div>
              <label 
                v-if="newStory.images.length < 5"
                class="upload-placeholder d-flex align-items-center justify-content-center rounded border border-dashed"
                style="width: 80px; height: 80px; cursor: pointer;"
              >
                <input 
                  type="file" 
                  accept="image/*" 
                  class="d-none"
                  @change="handleImageUpload"
                  multiple
                />
                <i class="bi bi-plus-lg text-muted"></i>
              </label>
            </div>
          </div>

          <!-- Link Drinks -->
          <div class="mb-3">
            <label class="form-label fw-bold">Link Drinks (Optional, max 5)</label>
            <!-- TODO: Integrate AutocompleteSearchSelector component -->
            <!-- <AutocompleteSearchSelector
              placeholder="Search for drinks to link..."
              :disabled="newStory.selectedDrinks.length >= 5"
              @select="handleDrinkSelect"
            /> -->
            <input 
              type="text" 
              class="form-control" 
              placeholder="Search for drinks to link... (Coming soon)"
              disabled
            />
            <div class="form-text">Link drinks you're discussing in your story</div>
            
            <!-- Selected Drinks Display -->
            <!-- TODO: Display selected drinks (same as Assembly post creation) -->
            <div v-if="newStory.selectedDrinks.length > 0" class="selected-drinks mt-3">
              <!-- Selected drinks cards will go here -->
            </div>
          </div>

          <!-- Hashtags Input -->
          <div class="mb-3">
            <label class="form-label fw-bold">Hashtags (Optional)</label>
            <!-- TODO: Implement hashtag input similar to varietal tags in BulkCreateListingNew -->
            <div class="input-group">
              <input 
                type="text" 
                class="form-control" 
                v-model="newHashtag"
                placeholder="Enter a hashtag and click Add"
                @keyup.enter="addHashtag"
              />
              <button 
                class="btn btn-outline-secondary" 
                type="button"
                @click="addHashtag"
              >
                Add
              </button>
            </div>
            <div class="form-text">Type a hashtag and click Add or press Enter</div>
            
            <!-- Display added hashtags -->
            <div v-if="newStory.hashtags.length > 0" class="mt-2 d-flex flex-wrap gap-2">
              <span 
                v-for="(tag, index) in newStory.hashtags" 
                :key="index"
                class="badge bg-secondary d-flex align-items-center"
              >
                #{{ tag }}
                <button 
                  type="button" 
                  class="btn-close btn-close-white ms-2" 
                  style="font-size: 0.6rem;"
                  @click="removeHashtag(index)"
                ></button>
              </span>
            </div>
          </div>

          <!-- Topic Selection -->
          <div class="mb-3">
            <label class="form-label fw-bold">Topic (Optional)</label>
            <!-- TODO: Implement topic dropdown -->
            <select class="form-select" v-model="newStory.topicID" disabled>
              <option value="">Select a topic... (Coming soon)</option>
            </select>
            <div class="form-text">Categorize your story under a topic for better discoverability</div>
          </div>

          <!-- Newsletter Selection -->
          <div class="mb-3">
            <label class="form-label fw-bold">Newsletter (Optional)</label>
            <!-- TODO: Implement newsletter dropdown populated from getUserNewsletters endpoint -->
            <select class="form-select" v-model="newStory.newsletterID" disabled>
              <option value="">Select a newsletter... (Coming soon)</option>
            </select>
            <div class="form-text">Add this story to one of your newsletters</div>
            <button 
              type="button" 
              class="btn btn-link p-0 mt-1"
              @click="createNewNewsletter"
            >
              <i class="bi bi-plus-circle me-1"></i> Create a new newsletter
            </button>
          </div>

        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button 
            type="button" 
            class="btn btn-primary fw-bold" 
            @click="submitStory"
            :disabled="!newStory.title.trim() || submittingStory"
          >
            <span v-if="submittingStory">
              <span class="spinner-border spinner-border-sm me-1"></span>
              Publishing...
            </span>
            <span v-else>Publish Story</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- =====================================================================================
       MY NEWSLETTERS MODAL
       Quick access to manage user's newsletters
       ===================================================================================== -->
  <div class="modal fade" id="myNewslettersModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title fw-bold">My Newsletters</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <!-- TODO: Implement newsletters list -->
          <div class="text-center py-4 text-muted">
            <i class="bi bi-envelope-paper" style="font-size: 3rem;"></i>
            <p class="mt-3">Newsletter management coming soon!</p>
            <router-link 
              to="/stories/newsletters/create" 
              class="btn btn-primary mt-2"
              data-bs-dismiss="modal"
            >
              <i class="bi bi-plus-circle me-1"></i> Create Newsletter
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import NavBar from "@/components/NavBar.vue";
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';
import UserProfileHeader from '@/components/UserProfileHeader.vue';
import UserProfileNavbar from '@/components/UserProfileNavbar.vue';
// TODO: Import these when implementing full functionality
// import InlineRichTextEditor from "@/components/InlineRichTextEditor.vue";
// import AutocompleteSearchSelector from "@/components/AutocompleteSearchSelector.vue";
import { useToast } from "vue-toastification";

export default {
  name: "UserStories",
  components: {
    NavBar,
    LoadingWithFunFact,
    UserProfileHeader,
    UserProfileNavbar,
    // TODO: Register components when implementing
    // InlineRichTextEditor,
    // AutocompleteSearchSelector,
  },
  data() {
    return {
      dataLoaded: false,
      currentURL: "",

      // Default images
      defaultProfilePhoto:
        "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
      defaultDrinkImage:
        "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",

      // User data
      displayUserID: null,
      routeUsername: null,
      displayUser: {},
      userID: null,
      userType: null,
      username: null,
      ownProfile: false,
      loggedInUser: null,

      // Stories data
      stories: [],
      storiesOffset: 0,
      hasMoreStories: false,
      loadingMore: false,

      // New story form data
      newStory: {
        title: '',
        content: '',
        images: [],
        selectedDrinks: [],
        listingIDs: [],
        hashtags: [],
        topicID: '',
        newsletterID: '',
      },
      newHashtag: '',
      submittingStory: false,

      // User's newsletters (for dropdown)
      userNewsletters: [],
    };
  },

  async mounted() {
    // Get route parameters
    this.displayUserID = parseInt(this.$route.params.userID);
    this.routeUsername = this.$route.params.username;

    // Get local storage (to determine if this is own profile)
    const accID = localStorage.getItem("88B_accID");
    if (accID !== null) {
      this.userID = accID;
    }

    const accType = localStorage.getItem("88B_accType");
    if (accType !== null) {
      this.userType = accType;
    }

    const accUsername = localStorage.getItem("88B_accUsername");
    if (accUsername !== null) {
      this.username = accUsername;
    }

    if (this.displayUserID && this.userID && parseInt(this.displayUserID) === parseInt(this.userID)) {
      this.ownProfile = true;
    }

    // Get logged-in user data from localStorage
    const storedUser = localStorage.getItem("88B_loggedInUser");
    if (storedUser) {
      this.loggedInUser = JSON.parse(storedUser);
    }

    // Load initial data
    await this.loadInitialData();
  },

  methods: {
    async loadInitialData() {
      try {
        // TODO: Implement API calls
        // 1. Load display user info
        // 2. Load user's stories via /getUserStories/<userID>/<userType>/<offset>
        // 3. If own profile, load user's newsletters via /getUserNewsletters/<userID>/<userType>
        
        // Placeholder: Set dataLoaded to true
        this.dataLoaded = true;
      } catch (error) {
        console.error("Error loading user stories data:", error);
        this.dataLoaded = null;
      }
    },

    async loadMoreStories() {
      // TODO: Implement pagination
      // Increment storiesOffset and fetch more stories
      this.loadingMore = true;
      try {
        // API call to get more stories
      } catch (error) {
        console.error("Error loading more stories:", error);
      } finally {
        this.loadingMore = false;
      }
    },

    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    // ==========================================
    // Create Story Modal Methods
    // ==========================================

    onStoryContentChange(content) {
      this.newStory.content = content;
    },

    handleImageUpload(event) {
      // TODO: Implement image upload (same as Assembly post creation)
      const files = event.target.files;
      if (!files) return;

      for (const file of files) {
        if (this.newStory.images.length >= 5) break;
        
        const reader = new FileReader();
        reader.onload = (e) => {
          this.newStory.images.push({
            file: file,
            preview: e.target.result
          });
        };
        reader.readAsDataURL(file);
      }
    },

    removeImage(index) {
      this.newStory.images.splice(index, 1);
    },

    handleDrinkSelect(drink) {
      // TODO: Implement drink selection
      if (this.newStory.selectedDrinks.length >= 5) return;
      if (this.newStory.selectedDrinks.find(d => d.id === drink.id)) return;
      
      this.newStory.selectedDrinks.push(drink);
      this.newStory.listingIDs.push(drink.id);
    },

    removeDrink(drinkId) {
      this.newStory.selectedDrinks = this.newStory.selectedDrinks.filter(d => d.id !== drinkId);
      this.newStory.listingIDs = this.newStory.listingIDs.filter(id => id !== drinkId);
    },

    addHashtag() {
      const tag = this.newHashtag.trim().replace(/^#/, ''); // Remove leading # if present
      if (!tag) return;
      if (this.newStory.hashtags.includes(tag.toLowerCase())) {
        useToast().warning("This hashtag has already been added");
        return;
      }
      this.newStory.hashtags.push(tag.toLowerCase());
      this.newHashtag = '';
    },

    removeHashtag(index) {
      this.newStory.hashtags.splice(index, 1);
    },

    async submitStory() {
      // TODO: Implement story submission via /createStory endpoint
      if (!this.newStory.title.trim()) {
        useToast().error("Please enter a title for your story");
        return;
      }

      this.submittingStory = true;
      try {
        // API call to create story
        // const response = await fetch(...);
        
        useToast().info("Story creation coming soon!");
        
        // Reset form
        this.resetNewStoryForm();
        
        // Close modal
        // bootstrap.Modal.getInstance(document.getElementById('createStoryModal')).hide();
        
      } catch (error) {
        console.error("Error creating story:", error);
        useToast().error("Failed to create story. Please try again.");
      } finally {
        this.submittingStory = false;
      }
    },

    resetNewStoryForm() {
      this.newStory = {
        title: '',
        content: '',
        images: [],
        selectedDrinks: [],
        listingIDs: [],
        hashtags: [],
        topicID: '',
        newsletterID: '',
      };
      this.newHashtag = '';
    },

    openMyNewsletters() {
      // TODO: Open modal or navigate to newsletters management
      // For now, open a modal
      const modal = new window.bootstrap.Modal(document.getElementById('myNewslettersModal'));
      modal.show();
    },

    createNewNewsletter() {
      // Navigate to create newsletter page
      this.$router.push('/stories/newsletters/create');
    },

    viewStory(story) {
      // Navigate to specific story page
      const slugTitle = this.slugify(story.storyTitle);
      this.$router.push(`/stories/${story.id}/${slugTitle}`);
    },

    slugify(text) {
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
/* Story card styles - modeled after AllReviews.vue */
.story-card {
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.story-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

.upload-placeholder {
  border: 2px dashed #dee2e6 !important;
}

.upload-placeholder:hover {
  border-color: #6c757d !important;
  background-color: #f8f9fa;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .mobile-fs-6 {
    font-size: 1rem !important;
  }
}
</style>
