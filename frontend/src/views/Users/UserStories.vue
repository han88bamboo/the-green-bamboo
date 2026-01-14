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
        <div class="row">
          <!-- Stories Column (left) -->
          <div class="col-12 col-lg-8 order-2 order-lg-1">
            <!-- Page Header and Actions -->
            <div class="d-flex justify-content-between align-items-center mb-4">
              <h5 class="fw-bold mobile-fs-6 mb-0">
                <i class="bi bi-journal-richtext"></i> All Stories by @{{ displayUser.username }}
              </h5>
              
              <!-- Create Story Button (only for own profile) -->
              <button 
                v-if="ownProfile"
                class="btn primary-btn-less-round-blue fw-bold"
                @click="$router.push('/stories/create')"
              >
                <i class="bi bi-plus-circle me-1"></i> Create Story
              </button>
            </div>

        <!-- Stories List (Medium-style row layout) -->
        <div v-if="stories.length > 0" class="stories-list">
          <div 
            v-for="story in stories" 
            :key="story.id"
            class="story-card card mb-3 shadow-sm"
            :class="{ 
              'draft-story-card': isDraft(story),
              'scheduled-story-card': isScheduled(story)
            }"
            @click="viewStory(story)"
            role="button"
          >
            <div class="card-body p-0">
              <div class="row g-0">
                <!-- Story Content (left side) -->
                <div class="col-8 col-md-9 p-3 d-flex flex-column">
                  <!-- Story Title -->
                  <h5 class="text-start story-title fw-bold mb-2 line-clamp-2">
                    {{ story.title || story.storyTitle }}
                  </h5>
                  
                  <!-- Story Preview (150 chars) -->
                  <p class="text-start story-preview text-muted mb-2 flex-grow-1 line-clamp-3">
                    {{ story.previewExcerpt || getExcerpt(story.content || story.storyContent, 150) }}
                  </p>
                  
                  <!-- Story Meta (bottom) -->
                  <div class="story-meta d-flex align-items-center flex-wrap gap-2 mt-auto">
                    <!-- Author Username -->
                    <small class="text-muted">
                      {{ story.creatorDisplayName || story.creatorUsername }}
                    </small>
                    
                    <!-- Draft Badge (in place of date) -->
                    <span v-if="ownProfile && isDraft(story)" class="badge bg-secondary">
                      <i class="bi bi-file-earmark-text me-1"></i>Draft
                    </span>
                    
                    <!-- Scheduled Badge (in place of date) -->
                    <span v-else-if="ownProfile && isScheduled(story)" class="badge bg-info text-dark">
                      <i class="bi bi-clock me-1"></i>Scheduled for {{ formatScheduledDate(story.publicationDate) }}
                    </span>
                    
                    <!-- Published Date (normal stories) -->
                    <small class="text-muted" v-else-if="!isDraft(story) && !isScheduled(story)">
                      · {{ formatDate(story.publicationDate) }}
                    </small>
                    
                    <!-- Topic Badge -->
                    <span 
                      v-if="story.topicName" 
                      class="badge bg-primary-subtle text-primary"
                    >
                      <i class="bi bi-folder me-1"></i>{{ story.topicName }}
                    </span>
                    
                    <!-- Newsletter Badge -->
                    <span 
                      v-if="story.newsletterName" 
                      class="badge bg-success-subtle text-success"
                    >
                      <i class="bi bi-envelope me-1"></i>{{ story.newsletterName }}
                    </span>
                    
                    <!-- Reading Time -->
                    <small v-if="story.readingTime" class="text-muted">
                      · {{ story.readingTime }} min read
                    </small>
                    
                    <!-- Like/Comment Counts (read-only) -->
                    <small class="text-muted">
                      <i class="bi bi-heart me-1"></i>{{ story.likeCount || 0 }}
                    </small>
                    <small class="text-muted">
                      <i class="bi bi-chat-square me-1"></i>{{ story.commentCount || 0 }}
                    </small>
                  </div>
                </div>
                
                <!-- Feature Image (right side) -->
                <div class="col-4 col-md-3 d-flex align-items-center justify-content-center p-2">
                  <div class="story-image-wrapper">
                    <img 
                      :src="getFeatureImage(story)" 
                      :alt="story.title || story.storyTitle"
                      class="story-feature-image rounded"
                    />
                  </div>
                </div>
              </div>
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
            @click="$router.push('/stories/create')"
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
          
          <!-- Newsletters Sidebar (right) -->
          <div class="col-12 col-lg-4 order-1 order-lg-2 mb-4 mb-lg-0">
            <!-- Header -->
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-bold mobile-fs-6 mb-0">
                <i class="bi bi-envelope-paper"></i> Newsletters
              </h5>
              <router-link 
                v-if="ownProfile"
                to="/stories/newsletters/create" 
                class="btn btn-primary fw-bold"
              >
                <i class="bi bi-plus-circle me-1"></i> Create
              </router-link>
            </div>
            
            <!-- Explanation Guide -->
            <p class="small text-muted mb-3">
              <i class="bi bi-info-circle me-1"></i>
              Newsletters are curated collections of stories. Subscribe to get updates when new stories are published!
            </p>
            
            <!-- Newsletters List -->
            <div v-if="displayUserNewsletters.length > 0" class="newsletter-list">
              <div 
                v-for="newsletter in displayedNewsletters" 
                :key="newsletter.id"
                class="newsletter-item d-flex align-items-center gap-2 p-2 rounded mb-2"
                @click="goToNewsletter(newsletter)"
                role="button"
              >
                <!-- Newsletter Thumbnail -->
                <img 
                  :src="newsletter.newsletterDisplayPhoto || defaultProfilePhoto" 
                  :alt="newsletter.newsletterName"
                  class="newsletter-thumbnail rounded"
                />
                
                <!-- Newsletter Info -->
                <div class="flex-grow-1 min-width-0">
                  <div class="fw-bold small text-truncate">{{ newsletter.newsletterName }}</div>
                  <small class="text-muted">
                    <i class="bi bi-journal-richtext me-1"></i>{{ newsletter.storyCount || 0 }} stories
                  </small>
                </div>
                
                <!-- Arrow -->
                <i class="bi bi-chevron-right text-muted"></i>
              </div>
              
              <!-- View All Link -->
              <div v-if="displayUserNewsletters.length > 5" class="text-center mt-2">
                <router-link 
                  :to="`/stories/newsletters?creator=${displayUserID}`" 
                  class="small text-primary text-decoration-none"
                >
                  View all {{ displayUserNewsletters.length }} newsletters <i class="bi bi-arrow-right"></i>
                </router-link>
              </div>
            </div>
            
            <!-- Empty State -->
            <div v-else class="text-center py-3">
              <i class="bi bi-envelope-paper text-muted" style="font-size: 2rem;"></i>
              <p class="small text-muted mt-2 mb-2">No newsletters yet</p>
              <router-link 
                v-if="ownProfile"
                to="/stories/newsletters/create" 
                class="btn btn-sm btn-primary fw-bold"
              >
                <i class="bi bi-plus-circle me-1"></i> Create Your First Newsletter
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- =====================================================================================
       CREATE STORY MODAL - COMMENTED OUT (Now using /stories/create page instead)
       Modeled after the "Create a Post" modal in SpecificAssembly.vue
       ===================================================================================== -->
  <!-- <div class="modal fade" id="createStoryModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title fw-bold">Create a Story</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          
         
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
          
         
          <div class="mb-3">
            <label class="form-label fw-bold">Content</label>
            <InlineRichTextEditor
              ref="storyEditor"
              :initial-content="newStory.content"
              @content-changed="onStoryContentChange"
              :section-id="'new-story'"
            />
          </div>

          
          <div class="mb-3">
            <label class="form-label fw-bold">Feature Image</label>
            <div class="form-text mb-2">This image will appear on story cards when browsing.</div>
            <div class="d-flex align-items-start gap-3">
          
              <div v-if="newStory.featureImagePreview" class="position-relative">
                <img 
                  :src="newStory.featureImagePreview" 
                  class="rounded"
                  style="width: 120px; height: 80px; object-fit: cover;"
                  alt="Feature image preview"
                />
                <button 
                  class="btn btn-sm btn-danger position-absolute top-0 end-0 rounded-circle p-0"
                  style="width: 20px; height: 20px; line-height: 1;"
                  @click="removeFeatureImage"
                  type="button"
                >
                  <i class="bi bi-x"></i>
                </button>
              </div>
              
              <label 
                v-else
                class="upload-placeholder d-flex align-items-center justify-content-center rounded border border-dashed"
                style="width: 120px; height: 80px; cursor: pointer;"
              >
                <input 
                  type="file" 
                  accept="image/*" 
                  class="d-none"
                  @change="handleFeatureImageUpload"
                />
                <div class="text-center text-muted">
                  <i class="bi bi-image fs-4"></i>
                  <div class="small">Add image</div>
                </div>
              </label>
            </div>
          </div>

          
          <div class="mb-3">
            <label class="form-label fw-bold">Link Drinks (Optional, max 5)</label>
            <AutocompleteSearchSelector
              placeholder="Search for drinks to link..."
              :disabled="newStory.selectedDrinks.length >= 5"
              @select="handleDrinkSelect"
            />
            <div class="form-text">Link drinks you're discussing in your story</div>
            
          
            <div v-if="newStory.selectedDrinks.length > 0" class="selected-drinks mt-3">
              <div 
                v-for="drink in newStory.selectedDrinks" 
                :key="drink.id"
                class="selected-drink-card d-flex align-items-center p-2 mb-2 border rounded bg-light"
              >
                <img 
                  :src="drink.photo || defaultDrinkPhoto" 
                  :alt="drink.listingName"
                  class="rounded me-3"
                  style="width: 50px; height: 50px; object-fit: cover;"
                />
                <div class="flex-grow-1 overflow-hidden">
                  <div class="fw-bold text-truncate">{{ drink.listingName }}</div>
                  <div class="small text-muted text-truncate">
                    <span v-if="drink.producerName">{{ drink.producerName }}</span>
                    <span v-if="drink.producerName && drink.drinkType"> · </span>
                    <span v-if="drink.drinkType">{{ drink.drinkType }}</span>
                    <span v-if="drink.abv"> · {{ drink.abv }}%</span>
                    <span v-if="drink.originCountry"> · {{ drink.originCountry }}</span>
                  </div>
                </div>
                <button 
                  type="button" 
                  class="btn btn-sm btn-outline-danger ms-2"
                  @click="removeDrink(drink.id)"
                  title="Remove drink"
                >
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
          </div>

          
          <div class="mb-3">
            <label class="form-label fw-bold">Hashtags (Optional)</label>
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

          
          <div class="mb-3">
            <label class="form-label fw-bold">Topic (Optional)</label>
            <select class="form-select" v-model="newStory.topicID">
              <option value="">Select a topic...</option>
              <option 
                v-for="topic in allTopics" 
                :key="topic.id" 
                :value="topic.id"
              >
                {{ topic.topicName }}
              </option>
            </select>
            <div class="form-text">Categorize your story under a topic for better discoverability</div>
          </div>

          
          <div class="mb-3">
            <label class="form-label fw-bold">Newsletter (Optional)</label>
            <select class="form-select" v-model="newStory.newsletterID">
              <option value="">Select a newsletter...</option>
              <option 
                v-for="newsletter in userNewsletters" 
                :key="newsletter.id" 
                :value="newsletter.id"
              >
                {{ newsletter.newsletterName }}
              </option>
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

        
          <div class="mb-3">
            <label class="form-label fw-bold">Publication</label>
            <div class="form-check mb-2">
              <input 
                class="form-check-input" 
                type="radio" 
                name="publicationType" 
                id="publishNow"
                v-model="newStory.saveAsDraft"
                :value="false"
                checked
              />
              <label class="form-check-label" for="publishNow">
                Publish now
              </label>
            </div>
            <div class="form-check mb-2">
              <input 
                class="form-check-input" 
                type="radio" 
                name="publicationType" 
                id="saveAsDraft"
                v-model="newStory.saveAsDraft"
                :value="true"
              />
              <label class="form-check-label" for="saveAsDraft">
                Save as draft
              </label>
            </div>
            
           
            <div class="mt-3" v-if="!newStory.saveAsDraft">
              <label class="form-label small">Or schedule for later:</label>
              <input 
                type="datetime-local" 
                class="form-control"
                v-model="newStory.publicationDate"
                :min="getMinDateTime()"
              />
              <div class="form-text">Leave empty to publish immediately</div>
            </div>
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
              {{ newStory.saveAsDraft ? 'Saving...' : (newStory.publicationDate ? 'Scheduling...' : 'Publishing...') }}
            </span>
            <span v-else>
              <template v-if="newStory.saveAsDraft">
                <i class="bi bi-file-earmark me-1"></i>Save Draft
              </template>
              <template v-else-if="newStory.publicationDate">
                <i class="bi bi-clock me-1"></i>Schedule Story
              </template>
              <template v-else>
                <i class="bi bi-send me-1"></i>Publish Story
              </template>
            </span>
          </button>
        </div>
      </div>
    </div>
  </div> -->

</template>

<script>
import NavBar from "@/components/NavBar.vue";
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';
import UserProfileHeader from '@/components/UserProfileHeader.vue';
import UserProfileNavbar from '@/components/UserProfileNavbar.vue';
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
    // InlineRichTextEditor,
    // AutocompleteSearchSelector,
  },
  data() {
    return {
      dataLoaded: false,
      currentURL: process.env.VUE_APP_API_URL,

      // Default images
      defaultProfilePhoto:
        "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
      defaultFeatureImage:
        "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/fred-moon-0yqa0rMCsYk-unsplash.jpg?v=1763054984",
      defaultDrinkPhoto:
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

      // Dropdown data (for create story form)
      allTopics: [],
      userNewsletters: [],
      
      // Display user's newsletters (for sidebar - loaded for all profiles)
      displayUserNewsletters: [],

      // New story form data
      newStory: {
        title: '',
        content: '',
        featureImage: null,
        featureImagePreview: null,
        selectedDrinks: [],
        listingIDs: [],
        hashtags: [],
        topicID: '',
        newsletterID: '',
        publicationDate: '',  // Empty = publish now, has value = scheduled
        saveAsDraft: false,
      },
      newHashtag: '',
      submittingStory: false,
    };
  },

  computed: {
    // Show first 5 newsletters in sidebar
    displayedNewsletters() {
      return this.displayUserNewsletters.slice(0, 5);
    },
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
        // Load display user info first
        await this.loadDisplayUser();
        
        // Load user's stories via /getUserStories/<userID>/<userType>/<offset>
        await this.loadStories();
        
        // Load display user's newsletters for sidebar (visible to all)
        await this.loadDisplayUserNewsletters();
        
        // If own profile, load topics and newsletters for create story dropdown
        if (this.ownProfile) {
          await this.loadDropdownData();
        }
        
        this.dataLoaded = true;
      } catch (error) {
        console.error("Error loading user stories data:", error);
        this.dataLoaded = null;
      }
    },

    async loadDisplayUser() {
      try {
        const response = await fetch(
          `${this.currentURL}/getData/getUser/${this.displayUserID}`
        );
        const data = await response.json();
        if (data) {
          this.displayUser = data;
        }
      } catch (error) {
        console.error("Error loading user info:", error);
      }
    },

    async loadStories() {
      try {
        // Build URL with viewer params for draft visibility
        let url = `${this.currentURL}/stories/getUserStories/${this.displayUserID}/user/${this.storiesOffset}`;
        if (this.ownProfile && this.userID) {
          url += `?viewerID=${this.userID}&viewerType=${this.userType || 'user'}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.code === 200) {
          this.stories = data.data || [];
          this.hasMoreStories = this.stories.length >= 12;
        } else {
          console.error("Error loading stories:", data.message);
          this.stories = [];
        }
      } catch (error) {
        console.error("Error loading stories:", error);
        this.stories = [];
      }
    },

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
          `${this.currentURL}/stories/getUserNewslettersForDropdown/${this.userID}/${this.userType || 'user'}`
        );
        const newslettersData = await newslettersResponse.json();
        if (newslettersData.code === 200) {
          this.userNewsletters = newslettersData.data || [];
        }
      } catch (error) {
        console.error("Error loading dropdown data:", error);
      }
    },

    async loadDisplayUserNewsletters() {
      try {
        // Load newsletters for the displayed user (for sidebar)
        const response = await fetch(
          `${this.currentURL}/stories/getUserNewsletters/${this.displayUserID}/user`
        );
        const data = await response.json();
        if (data.code === 200) {
          this.displayUserNewsletters = data.data || [];
        }
      } catch (error) {
        console.error("Error loading display user newsletters:", error);
      }
    },

    goToNewsletter(newsletter) {
      const slugName = this.slugify(newsletter.newsletterName);
      this.$router.push(`/stories/newsletters/${newsletter.id}/${slugName}`);
    },

    async loadMoreStories() {
      this.loadingMore = true;
      try {
        this.storiesOffset += 12;
        
        let url = `${this.currentURL}/stories/getUserStories/${this.displayUserID}/user/${this.storiesOffset}`;
        if (this.ownProfile && this.userID) {
          url += `?viewerID=${this.userID}&viewerType=${this.userType || 'user'}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.code === 200) {
          const newStories = data.data || [];
          this.stories = [...this.stories, ...newStories];
          this.hasMoreStories = newStories.length >= 12;
        }
      } catch (error) {
        console.error("Error loading more stories:", error);
      } finally {
        this.loadingMore = false;
      }
    },

    // ==========================================
    // Story Card Helper Methods
    // ==========================================

    isDraft(story) {
      // Draft = publicationDate is null
      return !story.publicationDate;
    },

    isScheduled(story) {
      // Scheduled = publicationDate is in the future
      if (!story.publicationDate) return false;
      return new Date(story.publicationDate) > new Date();
    },

    getFeatureImage(story) {
      // Get feature image from featurePhoto or storyPhotos array (first image)
      if (story.featurePhoto) {
        return story.featurePhoto;
      }
      const photos = story.storyPhotos;
      if (Array.isArray(photos) && photos.length > 0) {
        return photos[0];
      }
      if (typeof photos === 'string' && photos) {
        return photos;
      }
      return this.defaultFeatureImage;
    },

    getExcerpt(content, maxLength = 150) {
      if (!content) return '';
      // Strip HTML tags for preview
      const stripped = content.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
      if (stripped.length <= maxLength) return stripped;
      return stripped.substring(0, maxLength).trim() + '...';
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

    // Format for scheduled date badge: "dd MMM yy"
    formatScheduledDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      const day = date.getDate();
      const month = date.toLocaleDateString('en-US', { month: 'short' });
      const year = date.getFullYear().toString().slice(-2);
      return `${day} ${month} ${year}`;
    },

    // ==========================================
    // Create Story Modal Methods
    // ==========================================

    onStoryContentChange(content) {
      this.newStory.content = content;
    },

    handleFeatureImageUpload(event) {
      const file = event.target.files?.[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        this.newStory.featureImage = e.target.result;  // base64 string
        this.newStory.featureImagePreview = e.target.result;
      };
      reader.readAsDataURL(file);
    },

    removeFeatureImage() {
      this.newStory.featureImage = null;
      this.newStory.featureImagePreview = null;
    },

    handleDrinkSelect(drink) {
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
      let tag = this.newHashtag.trim().replace(/^#/, ''); // Remove leading # if present
      if (!tag) return;
      
      // Frontend validation: only alphanumeric characters (no special chars)
      tag = tag.replace(/[^a-zA-Z0-9]/g, '');
      if (!tag) {
        useToast().warning("Hashtags can only contain letters and numbers");
        this.newHashtag = '';
        return;
      }
      
      if (this.newStory.hashtags.includes(tag.toLowerCase())) {
        useToast().warning("This hashtag has already been added");
        this.newHashtag = '';
        return;
      }
      this.newStory.hashtags.push(tag.toLowerCase());
      this.newHashtag = '';
    },

    removeHashtag(index) {
      this.newStory.hashtags.splice(index, 1);
    },

    getMinDateTime() {
      // Return minimum datetime for scheduling (now + 1 minute)
      const now = new Date();
      now.setMinutes(now.getMinutes() + 1);
      return now.toISOString().slice(0, 16);
    },

    async submitStory() {
      if (!this.newStory.title.trim()) {
        useToast().error("Please enter a title for your story");
        return;
      }

      this.submittingStory = true;
      try {
        // Prepare publication date
        let publicationDate = null;
        if (!this.newStory.saveAsDraft) {
          if (this.newStory.publicationDate) {
            // Scheduled for later
            publicationDate = new Date(this.newStory.publicationDate).toISOString();
          } else {
            // Publish now
            publicationDate = new Date().toISOString();
          }
        }
        // If saveAsDraft is true, publicationDate stays null (draft)

        const payload = {
          creatorUserID: parseInt(this.userID),
          creatorUserType: this.userType || 'user',
          storyTitle: this.newStory.title.trim(),
          storyContent: this.newStory.content || '',
          featureImage64: this.newStory.featureImage || null,
          listingIDs: this.newStory.listingIDs,
          topicID: this.newStory.topicID || null,
          newsletterID: this.newStory.newsletterID || null,
          hashtags: this.newStory.hashtags,
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
          // Success - show toast first
          if (this.newStory.saveAsDraft) {
            useToast().success("Draft saved successfully!");
          } else if (this.newStory.publicationDate) {
            useToast().success("Story scheduled successfully!");
          } else {
            useToast().success("Story published successfully!");
          }
          
          // Get the new story ID for navigation
          const newStoryID = data.data.storyID;
          const storyTitle = this.newStory.title.trim();
          
          // Post-success operations in separate try block to prevent double toasts
          try {
            // Reset form
            this.resetNewStoryForm();
            
            // Close modal
            const modalEl = document.getElementById('createStoryModal');
            const modal = window.bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
            
            // Navigate to the newly created story
            const slugTitle = this.slugify(storyTitle);
            this.$router.push(`/stories/${newStoryID}/${slugTitle}`);
          } catch (postSuccessError) {
            // Don't show error toast - story was already created successfully
            console.error("Error in post-success operations:", postSuccessError);
            // Still try to navigate even if modal close fails
            const slugTitle = this.slugify(storyTitle);
            this.$router.push(`/stories/${newStoryID}/${slugTitle}`);
          }
          
        } else {
          useToast().error(data.message || "Failed to create story.");
        }
        
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
        featureImage: null,
        featureImagePreview: null,
        selectedDrinks: [],
        listingIDs: [],
        hashtags: [],
        topicID: '',
        newsletterID: '',
        publicationDate: '',
        saveAsDraft: false,
      };
      this.newHashtag = '';
      // Clear the rich text editor content
      if (this.$refs.storyEditor) {
        this.$refs.storyEditor.clearContent();
      }
    },

    viewStory(story) {
      // Navigate to specific story page
      const title = story.title || story.storyTitle || 'story';
      const slugTitle = this.slugify(title);
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
/* =====================================================================================
   STORY CARD STYLES - Medium-style row layout
   ===================================================================================== */
.story-card {
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  border: 1px solid #e9ecef;
}

.story-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

/* Draft and scheduled stories - faded like past events */
.draft-story-card,
.scheduled-story-card {
  opacity: 0.7;
}

.draft-story-card:hover,
.scheduled-story-card:hover {
  opacity: 0.85;
}

/* Story title */
.story-title {
  color: #222;
  font-size: 2rem;
  line-height: 1.3;
}

/* Story preview text */
.story-preview {
  font-size: 0.9rem;
  line-height: 1.5;
}

/* Line clamp utilities */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Feature image styling */
.story-image-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.story-feature-image {
  width: 100%;
  max-width: 150px;
  height: 100px;
  object-fit: cover;
}

/* Upload placeholder */
.upload-placeholder {
  border: 2px dashed #dee2e6 !important;
}

.upload-placeholder:hover {
  border-color: #6c757d !important;
  background-color: #f8f9fa;
}

/* Badges - subtle background colors (Bootstrap 5.3 style) */
.bg-primary-subtle {
  background-color: rgba(13, 110, 253, 0.1) !important;
}

.bg-success-subtle {
  background-color: rgba(25, 135, 84, 0.1) !important;
}

/* =====================================================================================
   NEWSLETTER SIDEBAR STYLES
   ===================================================================================== */
.newsletter-item {
  transition: background-color 0.2s;
  cursor: pointer;
  border: 1px solid transparent;
}

.newsletter-item:hover {
  background-color: #f8f9fa;
  border-color: #e9ecef;
}

.newsletter-thumbnail {
  width: 40px;
  height: 40px;
  object-fit: cover;
  flex-shrink: 0;
}

.min-width-0 {
  min-width: 0;
}

/* =====================================================================================
   MOBILE RESPONSIVENESS
   ===================================================================================== */
@media (max-width: 768px) {
  .mobile-fs-6 {
    font-size: 1rem !important;
  }
  
  .story-title {
    font-size: 1.15rem;
  }
  
  .story-preview {
    font-size: 0.85rem;
  }
  
  .story-feature-image {
    max-width: 100px;
    height: 70px;
  }
  
  .story-meta {
    font-size: 0.75rem;
  }
  
  .story-meta .badge {
    font-size: 0.65rem;
  }
}

@media (max-width: 576px) {
  .story-card .row {
    flex-direction: column-reverse;
  }
  
  .story-card .col-8,
  .story-card .col-4 {
    width: 100%;
  }
  
  .story-image-wrapper {
    margin-bottom: 0.5rem;
  }
  
  .story-feature-image {
    max-width: 100%;
    width: 100%;
    height: 150px;
  }
}
</style>
