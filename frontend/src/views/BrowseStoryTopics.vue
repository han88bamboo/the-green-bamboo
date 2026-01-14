<!-- 
  =====================================================================================
  BrowseStoryTopics.vue - Browse All Story Topics
  =====================================================================================
  Purpose: Display all topics for categorizing stories, with search and pagination.
           Similar to BrowseAssemblies.vue structure.
  
  Route: /stories/topics
  
  Features:
  - Grid display of topic cards
  - Search functionality
  - Sort by most recent
  - Create Topic button (for logged-in users)
  - Topic card shows: name, description, drinkTypes, subscriber count, story count, preview images
  
  Backend Endpoints Used:
  - GET /getTopics/<offset> - Get paginated topics
  - GET /getTopicswSearch/<offset>/<search> - Search topics
  
  Related Files:
  - backend/scripts/stories.py - Backend API endpoints
  - frontend/src/router/modules/story.js - Route registration
  - frontend/src/views/BrowseAssemblies.vue - Reference for structure/styling
  - frontend/src/views/SpecificStoryTopic.vue - Topic detail page
  - frontend/src/views/CreateTopic.vue - Create new topic
  
  Database Tables:
  - topics
  - topicSubscribers
  - stories
  =====================================================================================
-->
<template>
  <NavBar />
  
  <div class="container px-4 mt-4">
    <div class="container">
      <!-- Header with Search -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="row justify-content-left mb-2">
            <h3 class="text-start fw-bold mobile-fs-4">Story Topics: Discover Ideas & Inspiration 📚</h3>
            <h5 class="text-start fw-bold mobile-fs-6">Browse topics about wine, whisky, cocktails, and more...</h5>
          </div>

          <!-- Controls row -->
          <div class="row align-items-center g-2">
            <!-- Left: Search and Create -->
            <div class="col-12 col-md d-flex align-items-center justify-content-start gap-2 flex-wrap flex-md-nowrap">
              <div class="input-group search-compact" style="max-width: 400px;">
                <input
                  type="text"
                  class="form-control"
                  placeholder="Search topics"
                  v-model="searchTerm"
                  @input="filterTopics"
                />
                <button class="btn btn-outline-secondary" type="button">
                  <i class="bi bi-search"></i>
                </button>
              </div>

              <!-- Create Topic button -->
              <router-link 
                v-if="userID && userID !== 'defaultUser'"
                to="/stories/topics/create"
                class="btn primary-btn-less-round-blue fw-bold btn-md"
              >
                Create Topic
              </router-link>
            </div>

            <!-- Right: Sort options (when there are topics) -->
            <div
              v-if="filteredTopics.length > 0"
              class="col-12 col-md d-flex justify-content-center justify-content-md-end mobile-mt-3"
            >
              <div class="btn-group btn-group-md" role="group">
                <button 
                  type="button" 
                  class="btn"
                  :class="sortBy === 'recent' ? 'btn-primary' : 'btn-outline-secondary'"
                  @click="setSortBy('recent')"
                >
                  Most Recent
                </button>
                <button 
                  type="button" 
                  class="btn"
                  :class="sortBy === 'alphabetical' ? 'btn-primary' : 'btn-outline-secondary'"
                  @click="setSortBy('alphabetical')"
                >
                  Alphabetical
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3 text-muted">Loading topics...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <h4 class="alert-heading">Error Loading Topics</h4>
        <p>{{ error }}</p>
        <button class="btn btn-outline-danger" @click="loadTopics">Try Again</button>
      </div>

      <!-- Topics Grid -->
      <div v-else class="row g-4 mb-5">
        <!-- TODO: Implement topic cards (model after BrowseAssemblies.vue) -->
        <div
          v-for="topic in paginatedTopics"
          :key="topic.id"
          class="col-12 col-md-6 col-lg-4"
        >
          <div class="card h-100 shadow-sm topic-card">
            <!-- Topic Preview Images (Pinterest-style grid from recent stories) -->
            <div class="card-img-top position-relative" style="height: 200px; overflow: hidden;">
              <div class="pin-grid" v-if="topic.previewStories && topic.previewStories.length > 0">
                <!-- Main image (larger) -->
                <div class="pin-cell pin-main">
                  <img
                    v-if="topic.previewStories[0] && topic.previewStories[0].photo"
                    :src="topic.previewStories[0].photo"
                    class="pin-img"
                    :alt="topic.previewStories[0].title || 'Story preview'"
                  />
                  <div v-else class="pin-placeholder bg-light">
                    <i class="bi bi-image text-muted" style="font-size: 2rem;"></i>
                  </div>
                </div>
                
                <!-- Side images -->
                <div class="pin-cell pin-side1">
                  <img
                    v-if="topic.previewStories[1] && topic.previewStories[1].photo"
                    :src="topic.previewStories[1].photo"
                    class="pin-img"
                    :alt="topic.previewStories[1].title || 'Story preview'"
                  />
                  <div v-else class="pin-placeholder bg-light"></div>
                </div>
                
                <div class="pin-cell pin-side2">
                  <img
                    v-if="topic.previewStories[2] && topic.previewStories[2].photo"
                    :src="topic.previewStories[2].photo"
                    class="pin-img"
                    :alt="topic.previewStories[2].title || 'Story preview'"
                  />
                  <div v-else class="pin-placeholder bg-light"></div>
                </div>
              </div>
              
              <!-- Default placeholder if no preview stories -->
              <div v-else class="d-flex align-items-center justify-content-center h-100 bg-light">
                <i class="bi bi-journal-richtext text-muted" style="font-size: 3rem;"></i>
              </div>
            </div>

            <!-- Card Body -->
            <div class="card-body d-flex flex-column p-3">
              <!-- Topic Name and Stats -->
              <div class="d-flex justify-content-between align-items-center mb-2">
                <a href="#" class="text-decoration-underline default-clickable-text" style="color: inherit;" @click.prevent="viewTopic(topic)">
                  <h5 class="card-title fw-bold mb-0 flex-grow-1 text-start">{{ topic.topicName }}</h5>
                </a>
                <small class="text-muted ms-2">{{ topic.subscriberCount || 0 }} Subscriber{{ topic.subscriberCount !== 1 ? 's' : '' }}</small>
              </div>

              <!-- Story Count -->
              <div class="mb-2 text-start">
                <small class="text-muted">
                  <i class="bi bi-journal-richtext me-1"></i>
                  {{ topic.storyCount || 0 }} Stor{{ topic.storyCount !== 1 ? 'ies' : 'y' }}
                </small>
              </div>

              <!-- Drink Type Tags -->
              <div v-if="topic.drinkTypes && topic.drinkTypes.length > 0" class="mb-2 text-start">
                <span 
                  v-for="drinkType in topic.drinkTypes.slice(0, 3)" 
                  :key="drinkType" 
                  class="badge bg-warning text-dark me-1 mb-1"
                >
                  {{ drinkType }}
                </span>
                <span v-if="topic.drinkTypes.length > 3" class="badge bg-secondary">
                  +{{ topic.drinkTypes.length - 3 }} more
                </span>
              </div>

              <!-- Topic Description -->
              <p class="card-text text-muted mb-3 description-text text-start">
                {{ topic.topicDesc || '' }}
              </p>

              <!-- Action Buttons Row -->
              <div class="d-flex justify-content-between align-items-center mb-3 mt-auto">
                <!-- View Button -->
                <a
                  href="#"
                  class="btn btn-outline-secondary fw-semibold mobile-rating-smaller-text-2"
                  style="background-color: rgb(240, 68, 68); border-color: rgb(240, 68, 68); color: white;"
                  @click.prevent="viewTopic(topic)"
                >
                  View
                </a>

                <!-- Share Button -->
                <div class="d-flex gap-2">
                  <button 
                    class="btn btn-outline-secondary btn-sm"
                    @click="shareTopic(topic)"
                    title="Share topic"
                  >
                    <i class="bi bi-share"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="filteredTopics.length === 0 && !loading" class="col-12 text-center py-5">
          <i class="bi bi-journal-richtext text-muted" style="font-size: 4rem;"></i>
          <h4 class="text-muted mt-3">No Topics Found</h4>
          <p class="text-muted">
            {{ searchTerm ? 'Try a different search term' : 'Be the first to create a topic!' }}
          </p>
          <router-link 
            v-if="userID && userID !== 'defaultUser'"
            to="/stories/topics/create"
            class="btn primary-btn-less-round-blue fw-bold mt-2"
          >
            Create Topic
          </router-link>
        </div>
      </div>

      <!-- Load More Button -->
      <div v-if="hasMoreTopics && filteredTopics.length > 0" class="text-center mt-4 mb-5">
        <button 
          class="btn btn-outline-primary" 
          @click="loadMoreTopics"
          :disabled="loadingMore"
        >
          <span v-if="loadingMore">
            <span class="spinner-border spinner-border-sm me-1"></span>
            Loading...
          </span>
          <span v-else>Load More Topics</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import { useToast } from "vue-toastification";

export default {
  name: "BrowseStoryTopics",
  components: {
    NavBar,
  },
  data() {
    return {
      // User info
      userID: "defaultUser",
      userType: null,
      
      // Topics data
      topics: [],
      filteredTopics: [],
      paginatedTopics: [],
      
      // UI State
      loading: true,
      loadingMore: false,
      error: null,
      searchTerm: '',
      sortBy: 'recent',
      
      // Pagination
      currentOffset: 0,
      pageSize: 12,
      hasMoreTopics: false,
      
      // Default images
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
    };
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

    await this.loadTopics();
  },

  methods: {
    async loadTopics() {
      // TODO: Implement API call to /getTopics/<offset>
      this.loading = true;
      this.error = null;
      
      try {
        // const response = await fetch(`${process.env.VUE_APP_BACKEND_LINK}/getTopics/${this.currentOffset}`);
        // const data = await response.json();
        // this.topics = data.data || [];
        
        // Placeholder: empty topics for now
        this.topics = [];
        this.filterTopics();
      } catch (error) {
        console.error("Error loading topics:", error);
        this.error = "Failed to load topics. Please try again.";
      } finally {
        this.loading = false;
      }
    },

    filterTopics() {
      // TODO: Implement search filter
      let filtered = [...this.topics];
      
      if (this.searchTerm) {
        const search = this.searchTerm.toLowerCase();
        filtered = filtered.filter(topic => 
          topic.topicName.toLowerCase().includes(search) ||
          (topic.topicDesc && topic.topicDesc.toLowerCase().includes(search))
        );
      }
      
      // Sort
      if (this.sortBy === 'alphabetical') {
        filtered.sort((a, b) => a.topicName.localeCompare(b.topicName));
      } else {
        // Most recent (by dateCreated DESC)
        filtered.sort((a, b) => new Date(b.dateCreated) - new Date(a.dateCreated));
      }
      
      this.filteredTopics = filtered;
      this.paginatedTopics = filtered.slice(0, this.pageSize);
      this.hasMoreTopics = filtered.length > this.pageSize;
    },

    setSortBy(sort) {
      this.sortBy = sort;
      this.filterTopics();
    },

    async loadMoreTopics() {
      // TODO: Implement pagination
      this.loadingMore = true;
      try {
        this.currentOffset += this.pageSize;
        // API call...
      } catch (error) {
        console.error("Error loading more topics:", error);
      } finally {
        this.loadingMore = false;
      }
    },

    viewTopic(topic) {
      const slugName = this.slugify(topic.topicName);
      this.$router.push(`/stories/topics/${topic.id}/${slugName}`);
    },

    shareTopic(topic) {
      // TODO: Implement share functionality
      const url = `${window.location.origin}/stories/topics/${topic.id}/${this.slugify(topic.topicName)}`;
      navigator.clipboard.writeText(url);
      useToast().success("Link copied to clipboard!");
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
/* Card styles - copied from BrowseAssemblies.vue */
.topic-card {
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.topic-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
}

.description-text {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 2.4em;
}

/* Pinterest-style grid */
.pin-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 2px;
  height: 100%;
}

.pin-cell {
  overflow: hidden;
  background: #f0f0f0;
}

.pin-main {
  grid-row: 1 / 3;
}

.pin-side1 {
  grid-column: 2;
  grid-row: 1;
}

.pin-side2 {
  grid-column: 2;
  grid-row: 2;
}

.pin-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pin-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .mobile-fs-4 {
    font-size: 1.25rem !important;
  }
  .mobile-fs-6 {
    font-size: 1rem !important;
  }
  .mobile-mt-3 {
    margin-top: 1rem !important;
  }
}
</style>
