<!-- 
  =====================================================================================
  SpecificStoryNewsletter.vue - View Stories Under a Specific Newsletter
  =====================================================================================
  Purpose: Display all stories published in a specific newsletter, with newsletter info header.
           Only the creator can publish new stories to this newsletter.
  
  Route: /stories/newsletters/:newsletterId/:newsletterName
  
  Features:
  - Hero banner with newsletter info (uses newsletterBanner)
  - Subscribe/Unsubscribe button (in-app subscription, email delivery future TODO)
  - Create Story button (only for newsletter owner)
  - Stories feed sorted by most recent
  - Sorting options (Newest, Most Liked)
  - Story cards with like/comment counts
  - 404 handling for newsletter not found
  
  Backend Endpoints Used:
  - GET /stories/getSpecificNewsletterInfo/<newsletterID>?userID=X&userType=Y - Get newsletter details + isOwner, isSubscribed
  - GET /stories/getNewsletterStories/<newsletterID>/<offset> - Get stories in newsletter
  - POST /stories/subscribeNewsletter - Subscribe to newsletter (inserts into newsletterPatrons)
  - DELETE /stories/unsubscribeNewsletter - Unsubscribe from newsletter (sets status='cancelled')
  
  Related Files:
  - backend/scripts/stories.py - Backend API endpoints
  - frontend/src/router/modules/story.js - Route registration
  - frontend/src/views/SpecificStoryTopic.vue - Similar structure (topics version)
  - frontend/src/views/BrowseStoryNewsletters.vue - Newsletters listing page
  - frontend/src/views/SpecificStory.vue - Individual story page
  
  Database Tables:
  - newsletters (includes newsletterBanner, newsletterDisplayPhoto)
  - newsletterPatrons (NOT newsletterSubscribers)
  - stories
  - storiesLikes
  - storyComments
  
  NOTE: Subscription for newsletters in this MVP is in-app only.
  Email delivery feature is TODO for future implementation.
  
  NOTE: isOwner flag is returned from backend - no need to compute locally.
  =====================================================================================
-->
<template>
  <NavBar />
  
  <!-- Hero Banner -->
  <div v-if="!notFound && !initialLoading" class="hero-banner" :style="heroBannerStyle">
    <div class="hero-overlay">
      <div class="container">
        <div class="hero-content py-4">
          <div class="text-start">
            <button class="btn btn-sm btn-light mb-3" @click="goBack">
              <i class="bi bi-arrow-left me-1"></i> Back to Newsletters
            </button>
          </div>
          <h1 class="hero-title fw-bold text-white mb-2">{{ newsletterInfo.newsletterName || 'Loading...' }}</h1>
          <p class="hero-desc text-white-50 mb-3">{{ newsletterInfo.newsletterDesc || '' }}</p>
          
          <!-- Stats & Actions Row -->
          <div class="d-flex align-items-center flex-wrap gap-3">
            <span class="text-white-50">
              <i class="bi bi-people-fill me-1"></i>
              {{ newsletterInfo.subscriberCount || 0 }} Subscribers
            </span>
            <span class="text-white-50">
              <i class="bi bi-journal-richtext me-1"></i>
              {{ newsletterInfo.storyCount || 0 }} Stories
            </span>
            <span class="text-white-50">
              <i class="bi bi-calendar me-1"></i>
              Created {{ formatDate(newsletterInfo.dateCreated) }}
            </span>
            
            <!-- Subscribe/Unsubscribe Button -->
            <button
              v-if="!isSubscribed && userID !== 'defaultUser' && !isOwner"
              class="btn btn-primary fw-bold ms-auto"
              @click="subscribeNewsletter"
              :disabled="subscribing"
            >
              <span v-if="subscribing"><i class="bi bi-hourglass-split me-1"></i> Subscribing...</span>
              <span v-else><i class="bi bi-envelope-plus me-1"></i> Subscribe</span>
            </button>
            <div v-else-if="isSubscribed && !isOwner" class="btn-group ms-auto">
              <button class="btn btn-success fw-bold" disabled>
                <i class="bi bi-check-circle-fill me-1"></i> Subscribed
              </button>
              <button 
                class="btn btn-outline-light" 
                @click="showUnsubscribeConfirm"
                title="Unsubscribe"
              >
                <i class="bi bi-box-arrow-right"></i>
              </button>
            </div>
            <span v-else-if="isOwner" class="badge bg-success ms-auto px-3 py-2">
              <i class="bi bi-star-fill me-1"></i> You Manage This Newsletter
            </span>
            <button
              v-else
              class="btn btn-primary fw-bold ms-auto"
              @click="$router.push('/login')"
            >
              Login to Subscribe
            </button>
          </div>

          <!-- TODO: Add email subscription notice -->
          <div class="mt-2">
            <small class="text-white-50">
              <i class="bi bi-info-circle me-1"></i>
              Email delivery feature coming soon. For now, subscription is in-app only.
            </small>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-if="!notFound && !initialLoading" class="container px-4 mt-4">
    <div class="row">
      <!-- Main Content Column -->
      <div class="col-lg-8">
        <!-- Create Story Button (only for newsletter owner) 
        <div v-if="isOwner" class="card mb-4 shadow-sm create-story-card">
          <div class="card-body d-flex align-items-center gap-3">
            <img 
              :src="currentUserPhoto || defaultProfilePhoto" 
              alt="Your avatar"
              class="rounded-circle"
              style="width: 40px; height: 40px; object-fit: cover;"
            />
            <button 
              type="button" 
              class="form-control text-start text-muted"
              @click="openCreateStoryModal"
              style="cursor: pointer;"
            >
              Write a new story for {{ newsletterInfo.newsletterName || 'your newsletter' }}...
            </button>
            <button class="btn btn-outline-secondary" @click="openCreateStoryModal">
              <i class="bi bi-pencil-square"></i>
            </button>
          </div>
        </div>

         Non-owner info message 
        <div v-else-if="userID !== 'defaultUser'" class="alert alert-light mb-4">
          <i class="bi bi-info-circle me-2"></i>
          Only the newsletter owner can publish stories here.
          <router-link to="/stories/newsletters/create" class="alert-link">
            Create your own newsletter
          </router-link> to start publishing!
        </div>
        -->
        <!-- Sorting Options -->
        <div class="d-flex align-items-center gap-2 mb-3">
          <span class="text-muted small">Sort by:</span>
          <button 
            class="btn btn-sm"
            :class="sortBy === 'newest' ? 'btn-dark' : 'btn-outline-secondary'"
            @click="sortBy = 'newest'; loadStories()"
          >
            <i class="bi bi-clock me-1"></i> Newest
          </button>
          <button 
            class="btn btn-sm"
            :class="sortBy === 'mostLiked' ? 'btn-dark' : 'btn-outline-secondary'"
            @click="sortBy = 'mostLiked'; loadStories()"
          >
            <i class="bi bi-heart me-1"></i> Most Liked
          </button>
        </div>

        <!-- Stories Feed -->
        <div class="stories-feed">
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3 text-muted">Loading stories...</p>
          </div>

          <!-- Stories List -->
          <div v-else>
            <!-- Story Cards -->
            <!-- TODO: Implement story cards (model after SpecificStoryTopic.vue) -->
            <div 
              v-for="story in stories" 
              :key="story.id"
              class="story-card card mb-3 shadow-sm"
            >
              <div class="card-body">
                <!-- Story Meta -->
                <div class="text-start story-meta text-muted small mb-2">
                  <span>Published </span>
                  <span>{{ formatTimeAgo(story.publishingDate) }}</span>
                </div>

                <!-- Story Title (clickable) -->
                <h5 
                  class="text-start story-title fw-bold mb-2 clickable-title"
                  @click="viewStory(story)"
                >{{ story.storyTitle }}</h5>

                <!-- Story Preview (truncated) -->
                <p v-if="story.storyContentPreview" class="text-start story-preview text-muted mb-2">
                  {{ stripHtml(story.storyContentPreview) }}
                </p>

                <!-- Story Image Preview -->
                <div 
                  v-if="story.storyPhotos && story.storyPhotos.length > 0" 
                  class="story-image mb-2"
                  @click="viewStory(story)"
                >
                  <img 
                    :src="story.storyPhotos[0]" 
                    :alt="story.storyTitle"
                    class="img-fluid rounded"
                    style="max-height: 300px; object-fit: cover; width: 100%;"
                  />
                </div>

                <!-- Story Actions -->
                <div class="story-actions d-flex align-items-center gap-3 mt-2">
                  <span class="action-btn text-muted" @click.stop="likeStory(story)">
                    <i class="bi me-1" :class="story.userLiked ? 'bi-heart-fill text-danger' : 'bi-heart'"></i>
                    {{ story.likeCount || 0 }} Likes
                  </span>
                  <span class="action-btn text-muted" @click.stop="viewStory(story)">
                    <i class="bi bi-chat-square me-1"></i>
                    {{ story.commentCount || 0 }} Comments
                  </span>
                  <span class="action-btn text-muted" @click.stop="shareStory(story)">
                    <i class="bi bi-share me-1"></i>
                    Share
                  </span>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="stories.length === 0" class="text-center py-5">
              <i class="bi bi-journal-richtext text-muted" style="font-size: 4rem;"></i>
              <h4 class="text-muted mt-3">No stories yet</h4>
              <p class="text-muted">
                {{ isOwner ? 'Write your first newsletter story!' : 'This newsletter has no stories yet.' }}
              </p>
              <button 
                v-if="isOwner"
                class="btn btn-primary fw-bold mt-2"
                @click="openCreateStoryModal"
              >
                <i class="bi bi-pencil-square me-1"></i> Write Story
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

      <!-- Sidebar -->
      <div class="col-lg-4 d-none d-lg-block">
        <!-- About Card -->
        <div class="card shadow-sm mb-4">
          <div class="card-header bg-primary text-white">
            <h6 class="mb-0 fw-bold">About This Newsletter</h6>
          </div>
          <div class="card-body">
            <p class="small text-muted mb-3">{{ newsletterInfo.newsletterDesc || 'No description available.' }}</p>
            
            <!-- Creator Info -->
            <div class="d-flex align-items-center mb-3">
              <img 
                :src="newsletterInfo.creatorPhoto || defaultProfilePhoto" 
                alt="Creator"
                class="rounded-circle me-2"
                style="width: 32px; height: 32px; object-fit: cover;"
              />
              <div>
                <span class="small text-muted">Published by </span>
                <a 
                  :href="getCreatorProfileUrl()" 
                  class="text-decoration-none small fw-bold"
                  @click.prevent="goToCreatorProfile"
                >
                  {{ newsletterInfo.creatorUsername }}
                </a>
              </div>
            </div>
            
            <!-- Stats -->
            <div class="d-flex justify-content-around text-center py-2 border-top border-bottom">
              <div>
                <div class="fw-bold">{{ newsletterInfo.subscriberCount || 0 }}</div>
                <div class="small text-muted">Subscribers</div>
              </div>
              <div>
                <div class="fw-bold">{{ newsletterInfo.storyCount || 0 }}</div>
                <div class="small text-muted">Stories</div>
              </div>
            </div>
            
            <!-- Subscribe/Owner Button -->
            <button 
              v-if="isOwner"
              class="btn btn-outline-primary w-100 mt-3 fw-bold"
              @click="openCreateStoryModal"
            >
              <i class="bi bi-pencil-square me-1"></i> Write Story
            </button>
            <button 
              v-else-if="!isSubscribed && userID !== 'defaultUser'"
              class="btn btn-primary w-100 mt-3 fw-bold"
              @click="subscribeNewsletter"
              :disabled="subscribing"
            >
              <i class="bi bi-envelope-plus me-1"></i> Subscribe
            </button>
            <button 
              v-else-if="userID === 'defaultUser'"
              class="btn btn-outline-primary w-100 mt-3 fw-bold"
              @click="$router.push('/login')"
            >
              Login to Subscribe
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Initial Loading State -->
  <div v-if="initialLoading && !notFound" class="container px-4 mt-5">
    <div class="text-center py-5">
      <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading newsletter...</p>
    </div>
  </div>

  <!-- Newsletter Not Found State -->
  <div v-if="notFound" class="container px-4 mt-5">
    <div class="text-center py-5">
      <i class="bi bi-journal-x text-muted" style="font-size: 5rem;"></i>
      <h2 class="mt-4 text-muted">Newsletter Not Found</h2>
      <p class="text-muted mb-4">
        The newsletter you're looking for doesn't exist or may have been removed.
      </p>
      <button class="btn btn-primary" @click="$router.push('/stories/newsletters')">
        <i class="bi bi-arrow-left me-2"></i>Browse Newsletters
      </button>
    </div>
  </div>

  <!-- TODO: Create Story Modal - implement similar to UserStories.vue modal -->
  <!-- For newsletters, the newsletter should be pre-selected and read-only -->
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import { useToast } from "vue-toastification";

export default {
  name: "SpecificStoryNewsletter",
  components: {
    NavBar,
  },
  data() {
    return {
      // Newsletter Info
      newsletterInfo: {
        id: null,
        newsletterName: '',
        newsletterDesc: '',
        newsletterBanner: null,       // Banner image for hero
        newsletterDisplayPhoto: null, // Display photo (optional)
        dateCreated: null,
        subscriberCount: 0,
        storyCount: 0,
        createdByID: null,
        createdByType: null,
        creatorUsername: '',
        creatorPhoto: null,
        isFree: true,                 // Always true for MVP
      },
      
      // Stories
      stories: [],
      loading: true,
      loadingMore: false,
      hasMoreStories: false,
      currentOffset: 0,
      sortBy: 'newest',
      
      // User State
      userID: "defaultUser",
      userType: null,
      username: null,
      currentUserPhoto: null,
      isSubscribed: false,    // From backend response
      isOwner: false,         // From backend response (not computed)
      subscribing: false,
      
      // Page State
      initialLoading: true,
      notFound: false,
      
      // Default images
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
      defaultBannerImage: "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=1200",
    };
  },

  computed: {
    heroBannerStyle() {
      const bannerUrl = this.newsletterInfo.newsletterBanner || this.defaultBannerImage;
      return {
        backgroundImage: `url(${bannerUrl})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        minHeight: '300px',
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
      this.username = accUsername;
    }

    const accPhoto = localStorage.getItem("88B_accPhoto");
    if (accPhoto) {
      this.currentUserPhoto = accPhoto;
    }

    // Load newsletter data
    await this.loadNewsletterInfo();
    
    // Only load stories if newsletter was found
    if (!this.notFound) {
      await this.loadStories();
    }
    
    this.initialLoading = false;
  },

  methods: {
    async loadNewsletterInfo() {
      const newsletterId = this.$route.params.newsletterId;
      
      try {
        // Build query params for isSubscribed and isOwner checks
        let queryParams = '';
        if (this.userID !== 'defaultUser') {
          queryParams = `?userID=${this.userID}&userType=${this.userType}`;
        }
        
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/stories/getSpecificNewsletterInfo/${newsletterId}${queryParams}`
        );
        
        if (response.data.code === 200 && response.data.data) {
          const data = response.data.data;
          this.newsletterInfo = {
            id: data.id,  // Backend returns 'id' not 'newsletterID'
            newsletterName: data.newsletterName,
            newsletterDesc: data.newsletterDesc,
            newsletterBanner: data.newsletterBanner,
            newsletterDisplayPhoto: data.newsletterDisplayPhoto,
            dateCreated: data.dateCreated,
            subscriberCount: data.subscriberCount || 0,
            storyCount: data.storyCount || 0,
            createdByID: data.creatorUserID,
            createdByType: data.creatorUserType,
            creatorUsername: data.creatorUsername,
            creatorPhoto: data.creatorPhoto,
            isFree: data.isFree !== false, // Default to true
          };
          // isSubscribed and isOwner come from backend
          this.isSubscribed = data.isSubscribed || false;
          this.isOwner = data.isOwner || false;
        } else if (response.data.code === 404) {
          this.notFound = true;
        } else {
          console.error("Unexpected response:", response.data);
          this.notFound = true;
        }
      } catch (error) {
        console.error("Error loading newsletter info:", error);
        if (error.response?.status === 404 || error.response?.data?.code === 404) {
          this.notFound = true;
        } else {
          useToast().error("Failed to load newsletter. Please try again.");
        }
      }
    },

    async loadStories() {
      this.loading = true;
      const newsletterId = this.$route.params.newsletterId;
      
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/stories/getNewsletterStories/${newsletterId}/${this.currentOffset}`
        );
        
        if (response.data.code === 200) {
          this.stories = response.data.data || [];
          this.hasMoreStories = response.data.hasMore || false;
        }
      } catch (error) {
        console.error("Error loading stories:", error);
      } finally {
        this.loading = false;
      }
    },

    async loadMoreStories() {
      this.loadingMore = true;
      this.currentOffset += 12;
      const newsletterId = this.$route.params.newsletterId;
      
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/stories/getNewsletterStories/${newsletterId}/${this.currentOffset}`
        );
        
        if (response.data.code === 200) {
          const newStories = response.data.data || [];
          this.stories = [...this.stories, ...newStories];
          this.hasMoreStories = response.data.hasMore || false;
        }
      } catch (error) {
        console.error("Error loading more stories:", error);
      } finally {
        this.loadingMore = false;
      }
    },

    async subscribeNewsletter() {
      if (this.userID === 'defaultUser') {
        this.$router.push('/login');
        return;
      }
      
      this.subscribing = true;
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/stories/subscribeNewsletter`,
          {
            newsletterID: this.newsletterInfo.id,
            userID: this.userID,
            userType: this.userType,
          }
        );
        
        if (response.data.code === 201 || response.data.code === 200) {
          this.isSubscribed = true;
          this.newsletterInfo.subscriberCount++;
          useToast().success("Subscribed to newsletter!");
        } else {
          useToast().error(response.data.message || "Failed to subscribe");
        }
      } catch (error) {
        console.error("Error subscribing:", error);
        useToast().error("Failed to subscribe. Please try again.");
      } finally {
        this.subscribing = false;
      }
    },

    showUnsubscribeConfirm() {
      if (confirm('Are you sure you want to unsubscribe from this newsletter?')) {
        this.unsubscribeNewsletter();
      }
    },

    async unsubscribeNewsletter() {
      try {
        const response = await this.$axios.delete(
          `${process.env.VUE_APP_API_URL}/stories/unsubscribeNewsletter`,
          {
            data: {
              newsletterID: this.newsletterInfo.id,
              userID: this.userID,
              userType: this.userType,
            }
          }
        );
        
        if (response.data.code === 200) {
          this.isSubscribed = false;
          this.newsletterInfo.subscriberCount = Math.max(0, this.newsletterInfo.subscriberCount - 1);
          useToast().success("Unsubscribed from newsletter");
        } else {
          useToast().error(response.data.message || "Failed to unsubscribe");
        }
      } catch (error) {
        console.error("Error unsubscribing:", error);
        useToast().error("Failed to unsubscribe. Please try again.");
      }
    },

    openCreateStoryModal() {
      // TODO: Navigate to user profile stories page with query params to pre-select this newsletter
      // Example: /profile/{userType}/{userID}/{username}?tab=stories&createStory=true&newsletterID={id}
      // For now, show a toast message
      useToast().info("Story creation feature coming soon! Newsletter will be pre-selected.");
    },

    viewStory(story) {
      const slugTitle = this.slugify(story.storyTitle);
      this.$router.push(`/stories/${story.id}/${slugTitle}`);
    },

    // eslint-disable-next-line no-unused-vars
    likeStory(_story) {
      // TODO: Implement like/unlike story
      useToast().info("Story liking coming soon!");
    },

    shareStory(story) {
      const url = `${window.location.origin}/stories/${story.id}/${this.slugify(story.storyTitle)}`;
      navigator.clipboard.writeText(url);
      useToast().success("Link copied to clipboard!");
    },

    goBack() {
      this.$router.back();
    },

    goToCreatorProfile() {
      if (this.newsletterInfo.createdByID && this.newsletterInfo.createdByType) {
        this.$router.push(`/profile/${this.newsletterInfo.createdByType}/${this.newsletterInfo.createdByID}/${this.newsletterInfo.creatorUsername}`);
      }
    },

    getCreatorProfileUrl() {
      if (this.newsletterInfo.createdByID && this.newsletterInfo.createdByType) {
        return `/profile/${this.newsletterInfo.createdByType}/${this.newsletterInfo.createdByID}/${this.newsletterInfo.creatorUsername}`;
      }
      return '#';
    },

    formatDate(dateString) {
      if (!dateString) return '';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    formatTimeAgo(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMs / 3600000);
      const diffDays = Math.floor(diffMs / 86400000);

      if (diffMins < 60) return `${diffMins}m ago`;
      if (diffHours < 24) return `${diffHours}h ago`;
      if (diffDays < 7) return `${diffDays}d ago`;
      return this.formatDate(dateString);
    },

    stripHtml(html) {
      if (!html) return '';
      const tmp = document.createElement('div');
      tmp.innerHTML = html;
      return tmp.textContent || tmp.innerText || '';
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
/* Hero Banner Styles */
.hero-banner {
  position: relative;
}

.hero-overlay {
  background: linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.7));
  min-height: 300px;
  display: flex;
  align-items: center;
}

.hero-title {
  font-size: 2.5rem;
}

.hero-desc {
  max-width: 600px;
}

/* Story Card Styles */
.story-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.story-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

.clickable-title {
  cursor: pointer;
}

.clickable-title:hover {
  color: #0d6efd;
}

.action-btn {
  cursor: pointer;
  transition: color 0.2s;
}

.action-btn:hover {
  color: #0d6efd !important;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .hero-title {
    font-size: 1.75rem;
  }
}
</style>
