<!-- 
  =====================================================================================
  SpecificStoryTopic.vue - View Stories Under a Specific Topic
  =====================================================================================
  Purpose: Display all stories published under a specific topic, with topic info header.
           Similar to SpecificAssembly.vue structure.
  
  Route: /stories/topics/:topicId/:topicName
  
  Features:
  - Hero banner with topic info
  - Subscribe/Unsubscribe button
  - Create Story button (for any logged-in user)
  - Stories feed sorted by most recent
  - Sorting options (Newest, Most Liked)
  - Story cards with like/comment counts
  
  Backend Endpoints Used:
  - GET /getSpecificTopicInfo/<topicID> - Get topic details
  - GET /getTopicStories/<topicID>/<offset> - Get stories under topic
  - POST /subscribeTopic - Subscribe to topic
  - DELETE /unsubscribeTopic - Unsubscribe from topic
  
  Related Files:
  - backend/scripts/stories.py - Backend API endpoints
  - frontend/src/router/modules/story.js - Route registration
  - frontend/src/views/SpecificAssembly.vue - Reference for structure/styling
  - frontend/src/views/BrowseStoryTopics.vue - Topics listing page
  - frontend/src/views/SpecificStory.vue - Individual story page
  
  Database Tables:
  - topics
  - topicSubscribers
  - stories
  - storiesLikes
  - storyComments
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
              <i class="bi bi-arrow-left me-1"></i> Back to All Topics
            </button>
          </div>
          <h1 class="hero-title fw-bold text-white mb-2">Stories on {{ topicInfo.topicName || 'Loading...' }}</h1>
          <p class="hero-desc text-white-50 mb-3">{{ topicInfo.topicDesc || '' }}</p>
          
          <!-- Drink Type Tags -->
          <div v-if="topicInfo.drinkTypes && topicInfo.drinkTypes.length > 0" class="drink-tags mb-3">
            <span 
              v-for="drinkType in topicInfo.drinkTypes" 
              :key="drinkType" 
              class="badge bg-warning text-dark me-2 mb-1"
            >
              {{ drinkType }}
            </span>
          </div>
          
          <!-- Stats & Actions Row -->
          <div class="d-flex align-items-center flex-wrap gap-3">
            <span class="text-white-50">
              <i class="bi bi-people-fill me-1"></i>
              {{ topicInfo.subscriberCount || 0 }} Subscribers
            </span>
            <span class="text-white-50">
              <i class="bi bi-journal-richtext me-1"></i>
              {{ topicInfo.storyCount || 0 }} Stories
            </span>
            <!-- <span class="text-white-50">
              <i class="bi bi-calendar me-1"></i>
              Created {{ formatDate(topicInfo.dateCreated) }}
            </span> -->
            
            <!-- Subscribe/Unsubscribe Button -->
            <button
              v-if="!isSubscribed && userID !== 'defaultUser'"
              class="btn btn-warning fw-bold ms-auto"
              @click="subscribeTopic"
              :disabled="subscribing"
            >
              <span v-if="subscribing"><i class="bi bi-hourglass-split me-1"></i> Subscribing...</span>
              <span v-else><i class="bi bi-plus-circle me-1"></i> Subscribe</span>
            </button>
            <div v-else-if="isSubscribed" class="btn-group ms-auto">
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
            <button
              v-else
              class="btn btn-warning fw-bold ms-auto"
              @click="$router.push('/login')"
            >
              Login to Subscribe
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-if="!notFound && !initialLoading" class="container px-4 mt-4">
    <div class="row">
      <!-- Main Content Column -->
      <div class="col-lg-8">
        <!-- commented out because this page should feel more like a news feed
        Create Story Button (for any logged-in user) 
        <div v-if="userID !== 'defaultUser'" class="card mb-4 shadow-sm create-story-card">
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
              Write a story about {{ topicInfo.topicName || 'this topic' }}...
            </button>
            <button class="btn btn-outline-secondary" @click="openCreateStoryModal">
              <i class="bi bi-pencil-square"></i>
            </button>
          </div>
        </div>-->

        <!-- Sorting Options -->
        <div class="d-flex align-items-center gap-2 mb-3">
          <span class="text-muted small">Sort by:</span>
          <button 
            class="btn btn-sm"
            :class="sortBy === 'newest' ? 'btn-dark' : 'btn-outline-secondary'"
            @click="changeSortBy('newest')"
          >
            <i class="bi bi-clock me-1"></i> Newest
          </button>
          <button 
            class="btn btn-sm"
            :class="sortBy === 'mostLiked' ? 'btn-dark' : 'btn-outline-secondary'"
            @click="changeSortBy('mostLiked')"
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

          <!-- Stories List (Medium-style row layout) -->
          <div v-else>
            <div v-if="stories.length > 0" class="stories-list">
              <div 
                v-for="story in stories" 
                :key="story.id"
                class="story-card card mb-3 shadow-sm"
                @click="viewStory(story)"
                role="button"
              >
                <div class="card-body p-0">
                  <div class="row g-0">
                    <!-- Story Content (left side) -->
                    <div class="col-8 col-md-9 p-3 d-flex flex-column">
                      <!-- Story Title -->
                      <h5 class="text-start story-title fw-bold mb-2 line-clamp-2">
                        {{ story.storyTitle }}
                      </h5>
                      
                      <!-- Story Preview (150 chars) -->
                      <p class="text-start story-preview text-muted mb-2 flex-grow-1 line-clamp-3">
                        {{ story.previewExcerpt || getExcerpt(story.storyContent, 150) }}
                      </p>
                      
                      <!-- Story Meta (bottom) -->
                      <div class="story-meta d-flex align-items-center flex-wrap gap-2 mt-auto">
                        <!-- Author Username -->
                        <small class="text-muted">
                          {{ story.creatorDisplayName || story.creatorUsername }}
                        </small>
                        
                        <!-- Published Date -->
                        <small class="text-muted">
                          · {{ formatDate(story.publicationDate) }}
                        </small>
                        
                        <!-- Newsletter Badge (show newsletter if story is part of one) -->
                        <span 
                          v-if="story.newsletterName" 
                          class="badge bg-success-subtle text-success"
                          @click.stop="goToNewsletter(story)"
                        >
                          <i class="bi bi-newspaper me-1"></i>{{ story.newsletterName }}
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
                          :alt="story.storyTitle"
                          class="story-feature-image rounded"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="stories.length === 0" class="text-center py-5">
              <i class="bi bi-journal-richtext text-muted" style="font-size: 4rem;"></i>
              <h4 class="text-muted mt-3">No stories yet</h4>
              <p class="text-muted">Be the first to write a story about this topic!</p>
              <button 
                v-if="userID !== 'defaultUser'"
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
          <div class="card-header bg-dark text-white">
            <h6 class="mb-0 fw-bold">About This Topic</h6>
          </div>
          <div class="card-body">
            <p class="small text-muted mb-3">{{ topicInfo.topicDesc || 'No description available.' }}</p>
            
            <!-- Creator Info -->
            <div v-if="topicInfo.creatorUsername" class="mb-3">
              <span class="small text-muted">Created by </span>
              <a 
                :href="getCreatorProfileUrl()" 
                class="text-decoration-none small fw-bold"
                @click.prevent="goToCreatorProfile"
              >
                {{ topicInfo.creatorUsername }}
              </a>
            </div>
            
            <!-- Stats -->
            <div class="d-flex justify-content-around text-center py-2 border-top border-bottom">
              <div>
                <div class="fw-bold">{{ topicInfo.subscriberCount || 0 }}</div>
                <div class="small text-muted">Subscribers</div>
              </div>
              <div>
                <div class="fw-bold">{{ topicInfo.storyCount || 0 }}</div>
                <div class="small text-muted">Stories</div>
              </div>
            </div>
            
            <!-- Create Story Button -->
            <button 
              v-if="userID !== 'defaultUser'"
              class="btn btn-warning w-100 mt-3 fw-bold"
              @click="openCreateStoryModal"
            >
              Write Story
            </button>
            <button 
              v-else
              class="btn btn-outline-warning w-100 mt-3 fw-bold"
              @click="$router.push('/login')"
            >
              Login to Write
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Initial Loading State -->
  <div v-if="initialLoading && !notFound" class="container px-4 mt-5">
    <div class="text-center py-5">
      <div class="spinner-border text-warning" style="width: 3rem; height: 3rem;" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading topic...</p>
    </div>
  </div>

  <!-- Topic Not Found State -->
  <div v-if="notFound" class="container px-4 mt-5">
    <div class="text-center py-5">
      <i class="bi bi-hash text-muted" style="font-size: 5rem;"></i>
      <h2 class="mt-4 text-muted">Topic Not Found</h2>
      <p class="text-muted mb-4">
        The topic you're looking for doesn't exist or may have been removed.
      </p>
      <button class="btn btn-warning" @click="$router.push('/stories/topics')">
        <i class="bi bi-arrow-left me-2"></i>Browse Topics
      </button>
    </div>
  </div>

  <!-- TODO: Create Story Modal - implement similar to UserStories.vue modal -->
  <!-- For now, clicking "Create Story" will navigate to /stories/my-stories with query params -->
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import { useToast } from "vue-toastification";

export default {
  name: "SpecificStoryTopic",
  components: {
    NavBar,
  },
  data() {
    return {
      // Topic Info
      topicInfo: {
        id: null,
        topicName: '',
        topicDesc: '',
        drinkTypes: [],
        topicBanner: null,
        dateCreated: null,
        subscriberCount: 0,
        storyCount: 0,
        createdByID: null,
        createdByType: null,
        creatorUsername: '',
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
      isSubscribed: false,
      subscribing: false,
      
      // Page State
      initialLoading: true,
      notFound: false,
      
      // Default images
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
      defaultBannerImage: "https://i0.wp.com/highestspirits.com/wp-content/uploads/2018/10/jnpup.jpg?fit=1920%2C1281",
      defaultFeatureImage: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultFeatureImage.png?v=1737012345",
    };
  },

  computed: {
    heroBannerStyle() {
      const bannerUrl = this.topicInfo.topicBanner || this.defaultBannerImage;
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

    // Load topic data
    await this.loadTopicInfo();
    
    // Only load stories if topic was found
    if (!this.notFound) {
      await this.loadStories();
    }
    
    this.initialLoading = false;
  },

  methods: {
    async loadTopicInfo() {
      const topicId = this.$route.params.topicId;
      
      try {
        // Build URL with optional userID/userType for isSubscribed check
        let url = `${process.env.VUE_APP_API_URL}/stories/getSpecificTopicInfo/${topicId}`;
        const params = new URLSearchParams();
        
        if (this.userID !== 'defaultUser' && this.userType) {
          params.append('userID', this.userID);
          params.append('userType', this.userType);
        }
        
        if (params.toString()) {
          url += `?${params.toString()}`;
        }
        
        const response = await this.$axios.get(url);
        const data = response.data;
        
        if (data.code === 200 && data.data) {
          this.topicInfo = {
            id: data.data.id,
            topicName: data.data.topicName,
            topicDesc: data.data.topicDesc,
            drinkTypes: data.data.drinkTypes || [],
            topicBanner: data.data.topicBanner,
            dateCreated: data.data.dateCreated,
            subscriberCount: data.data.subscriberCount || 0,
            storyCount: data.data.storyCount || 0,
            createdByID: data.data.createdByID,
            createdByType: data.data.createdByType,
            creatorUsername: data.data.creatorUsername,
            previewStories: data.data.previewStories || [],
          };
          this.isSubscribed = data.data.isSubscribed || false;
        } else if (data.code === 404) {
          // Topic not found - show not found state
          this.notFound = true;
        }
      } catch (error) {
        console.error("Error loading topic info:", error);
        if (error.response && error.response.status === 404) {
          this.notFound = true;
        } else {
          useToast().error("Failed to load topic information");
        }
      }
    },

    async loadStories() {
      this.loading = true;
      const topicId = this.$route.params.topicId;
      this.currentOffset = 0;
      
      try {
        // Build URL with sortBy query param
        const queryParams = `?sortBy=${this.sortBy}`;
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/stories/getTopicStories/${topicId}/${this.currentOffset}${queryParams}`
        );
        
        if (response.data.code === 200) {
          // New API returns 'data' array with consistent field names
          this.stories = response.data.data || [];
          this.hasMoreStories = response.data.hasMore || false;
        } else {
          console.error("Error loading stories:", response.data.message);
        }
      } catch (error) {
        console.error("Error loading stories:", error);
        useToast().error("Failed to load stories");
      } finally {
        this.loading = false;
      }
    },

    async loadMoreStories() {
      this.loadingMore = true;
      const topicId = this.$route.params.topicId;
      this.currentOffset += 12;
      
      try {
        const queryParams = `?sortBy=${this.sortBy}`;
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/stories/getTopicStories/${topicId}/${this.currentOffset}${queryParams}`
        );
        
        if (response.data.code === 200) {
          const newStories = response.data.data || [];
          this.stories = [...this.stories, ...newStories];
          this.hasMoreStories = response.data.hasMore || false;
        }
      } catch (error) {
        console.error("Error loading more stories:", error);
        useToast().error("Failed to load more stories");
        this.currentOffset -= 12; // Reset offset on error
      } finally {
        this.loadingMore = false;
      }
    },

    changeSortBy(newSort) {
      if (this.sortBy !== newSort) {
        this.sortBy = newSort;
        this.loadStories();
      }
    },

    async subscribeTopic() {
      if (this.userID === 'defaultUser') {
        this.$router.push('/login');
        return;
      }
      
      this.subscribing = true;
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/stories/subscribeTopic`,
          {
            topicID: this.topicInfo.id,
            userID: this.userID,
            userType: this.userType
          }
        );
        
        if (response.data.code === 201) {
          this.isSubscribed = true;
          this.topicInfo.subscriberCount++;
          useToast().success("Successfully subscribed to topic!");
        } else {
          useToast().error(response.data.message || "Failed to subscribe");
        }
      } catch (error) {
        console.error("Error subscribing:", error);
        if (error.response && error.response.data) {
          useToast().error(error.response.data.message || "Failed to subscribe");
        } else {
          useToast().error("Failed to subscribe to topic");
        }
      } finally {
        this.subscribing = false;
      }
    },

    showUnsubscribeConfirm() {
      if (confirm('Are you sure you want to unsubscribe from this topic?')) {
        this.unsubscribeTopic();
      }
    },

    async unsubscribeTopic() {
      try {
        const response = await this.$axios.delete(
          `${process.env.VUE_APP_API_URL}/stories/unsubscribeTopic`,
          {
            data: {
              topicID: this.topicInfo.id,
              userID: this.userID,
              userType: this.userType
            }
          }
        );
        
        if (response.data.code === 200) {
          this.isSubscribed = false;
          this.topicInfo.subscriberCount--;
          useToast().success("Successfully unsubscribed from topic");
        } else {
          useToast().error(response.data.message || "Failed to unsubscribe");
        }
      } catch (error) {
        console.error("Error unsubscribing:", error);
        if (error.response && error.response.data) {
          useToast().error(error.response.data.message || "Failed to unsubscribe");
        } else {
          useToast().error("Failed to unsubscribe from topic");
        }
      }
    },

    openCreateStoryModal() {
      // Navigate to Create Story page with topic pre-selected
      this.$router.push(`/stories/create?topicID=${this.topicInfo.id}`);
    },

    viewStory(story) {
      const slugTitle = this.slugify(story.storyTitle);
      this.$router.push(`/stories/${story.id}/${slugTitle}`);
    },

    goToNewsletter(story) {
      if (story.newsletterID && story.newsletterName) {
        const slugName = this.slugify(story.newsletterName);
        this.$router.push(`/stories/newsletters/${story.newsletterID}/${slugName}`);
      }
    },

    goBack() {
      this.$router.back();
    },

    goToCreatorProfile() {
      if (this.topicInfo.createdByID && this.topicInfo.createdByType) {
        this.$router.push(`/profile/${this.topicInfo.createdByType}/${this.topicInfo.createdByID}/${this.topicInfo.creatorUsername}`);
      }
    },

    getCreatorProfileUrl() {
      if (this.topicInfo.createdByID && this.topicInfo.createdByType) {
        return `/profile/${this.topicInfo.createdByType}/${this.topicInfo.createdByID}/${this.topicInfo.creatorUsername}`;
      }
      return '#';
    },

    // ==========================================
    // Story Card Helper Methods (matching UserStories.vue)
    // ==========================================

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

/* =====================================================================================
   STORY CARD STYLES - Medium-style row layout (matching UserStories.vue)
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

/* Badges - subtle background colors (Bootstrap 5.3 style) */
.bg-primary-subtle {
  background-color: rgba(13, 110, 253, 0.1) !important;
}

.bg-success-subtle {
  background-color: rgba(25, 135, 84, 0.1) !important;
}

/* =====================================================================================
   MOBILE RESPONSIVENESS
   ===================================================================================== */
@media (max-width: 768px) {
  .hero-title {
    font-size: 1.75rem;
  }
  
  .story-title {
    font-size: 2rem;
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
