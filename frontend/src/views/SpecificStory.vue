<!-- 
  =====================================================================================
  SpecificStory.vue - Individual Story Detail Page
  =====================================================================================
  Purpose: Display full story content with comments, likes, and related info.
           Similar to SpecificAssemblyPost.vue structure.
  
  Route: /stories/:storyId/:storyTitle
  
  Features:
  - Full story content (rich text with images)
  - Story metadata (author, date, topic/newsletter, drinks mentioned)
  - Like button (likes only, no dislikes)
  - Comments section (likes AND dislikes for comments)
  - Related drinks section (linked drink entities)
  - Share functionality
  - Edit/Delete buttons (for story owner)
  - Hashtags display
  
  Backend Endpoints Used:
  - GET /getSpecificStory/<storyID> - Get full story details
  - POST /likeStory - Like a story
  - DELETE /unlikeStory - Unlike a story
  - GET /getStoryComments/<storyID>/<offset> - Get story comments
  - POST /addStoryComment - Add a comment
  - POST /likeStoryComment - Like a comment
  - POST /dislikeStoryComment - Dislike a comment
  - DELETE /deleteStoryComment/<commentID> - Delete a comment
  
  Related Files:
  - backend/scripts/stories.py - Backend API endpoints
  - frontend/src/router/modules/story.js - Route registration
  - frontend/src/views/SpecificAssemblyPost.vue - Reference for structure/styling
  - frontend/src/views/SpecificStoryTopic.vue - Topic context
  - frontend/src/views/SpecificStoryNewsletter.vue - Newsletter context
  
  Database Tables:
  - stories
  - storiesLikes
  - storyComments
  - storyCommentLikes
  - storyDrinks
  - storyHashtags
  - hashtags
  - topics
  - newsletters
  =====================================================================================
-->
<template>
  <NavBar />
  
  <div class="container px-4 py-4">
    <!-- Back Navigation -->
    <div class="row mb-3">
      <div class="col">
        <button class="btn btn-outline-secondary btn-sm" @click="goBack">
          <i class="bi bi-arrow-left me-1"></i> Back
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading story...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-5">
      <i class="bi bi-exclamation-triangle text-danger" style="font-size: 4rem;"></i>
      <h4 class="text-muted mt-3">Story not found</h4>
      <p class="text-muted">This story may have been deleted or doesn't exist.</p>
      <router-link to="/stories/topics" class="btn btn-primary mt-2">
        Browse Topics
      </router-link>
    </div>

    <!-- Main Content -->
    <div v-else class="row">
      <!-- Story Content Column -->
      <div class="col-lg-8">
        <article class="story-article">
          <!-- Story Header -->
          <header class="story-header mb-4">
            <!-- Topic/Newsletter Context -->
            <div class="context-badges mb-3">
              <router-link 
                v-if="story.topicID"
                :to="`/stories/topics/${story.topicID}/${slugify(story.topicName)}`"
                class="badge bg-warning text-dark text-decoration-none me-2"
              >
                <i class="bi bi-hash me-1"></i>{{ story.topicName }}
              </router-link>
              <router-link 
                v-if="story.newsletterID"
                :to="`/stories/newsletters/${story.newsletterID}/${slugify(story.newsletterName)}`"
                class="badge bg-primary text-decoration-none"
              >
                <i class="bi bi-envelope me-1"></i>{{ story.newsletterName }}
              </router-link>
            </div>

            <!-- Story Title -->
            <h1 class="text-start story-title fw-bold mb-3">{{ story.storyTitle }}</h1>

            <!-- Author Info -->
            <div class="text-start author-info d-flex mb-3">
              <img 
                :src="story.creatorPhoto || defaultProfilePhoto" 
                alt="Author"
                class="rounded-circle me-3"
                style="width: 48px; height: 48px; object-fit: cover; cursor: pointer;"
                @click="goToAuthorProfile"
              />
              <div>
                <a 
                  href="#" 
                  @click.prevent="goToAuthorProfile" 
                  class="fw-bold text-decoration-none"
                >
                  {{ getAuthorDisplayName() }}
                </a>
                <div class="text-muted small">
                  {{ formatDate(story.publicationDate) }}
                  <span v-if="story.editedAt" class="ms-1">(edited)</span>
                  <span v-if="story.readTime" class="mx-1">•</span>
                  <span v-if="story.readTime">{{ story.readTime }} min read</span>
                </div>
              </div>
            </div>

            <!-- Action Buttons (Edit/Delete for owner) -->
            <div v-if="isOwner" class="owner-actions mb-3">
              <button class="btn btn-sm btn-outline-primary me-2" @click="editStory">
                <i class="bi bi-pencil me-1"></i> Edit
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="confirmDelete">
                <i class="bi bi-trash me-1"></i> Delete
              </button>
            </div>
          </header>

          <!-- Story Featured Image -->
          <div v-if="story.storyPhotos && story.storyPhotos.length > 0" class="story-featured-image mb-4">
            <img 
              :src="story.storyPhotos[0]" 
              :alt="story.storyTitle"
              class="img-fluid rounded shadow-sm"
              style="width: 100%; max-height: 500px; object-fit: cover;"
            />
          </div>

          <!-- Story Content (Rich Text) -->
          <!-- TODO: Render rich text content properly (similar to how reviews are displayed) -->
          <div class="text-start story-content mb-4" v-html="story.storyContent">
          </div>

          <!-- Additional Photos Gallery -->
          <div v-if="story.storyPhotos && story.storyPhotos.length > 1" class="photo-gallery mb-4">
            <h6 class="fw-bold mb-3">More Photos</h6>
            <div class="row g-2">
              <div 
                v-for="(photo, index) in story.storyPhotos.slice(1)" 
                :key="index"
                class="col-4"
              >
                <img 
                  :src="photo" 
                  :alt="`Photo ${index + 2}`"
                  class="img-fluid rounded"
                  style="height: 150px; width: 100%; object-fit: cover; cursor: pointer;"
                  @click="openPhotoModal(photo)"
                />
              </div>
            </div>
          </div>

          <!-- Hashtags -->
          <div v-if="story.hashtags && story.hashtags.length > 0" class="hashtags-section mb-4">
            <span 
              v-for="hashtag in story.hashtags" 
              :key="hashtag"
              class="badge bg-light text-dark border me-2 mb-1"
            >
              #{{ hashtag }}
            </span>
          </div>

          <hr />

          <!-- Engagement Actions -->
          <div class="engagement-actions d-flex align-items-center gap-4 mb-4">
            <!-- Like Button -->
            <button 
              class="btn d-flex align-items-center gap-2"
              :class="story.userLiked ? 'btn-danger' : 'btn-outline-danger'"
              @click="toggleLike"
              :disabled="liking"
            >
              <i class="bi" :class="story.userLiked ? 'bi-heart-fill' : 'bi-heart'"></i>
              <span>{{ story.likeCount || 0 }} Likes</span>
            </button>

            <!-- Comments Count -->
            <button class="btn btn-outline-secondary d-flex align-items-center gap-2" @click="scrollToComments">
              <i class="bi bi-chat-square"></i>
              <span>{{ story.commentCount || 0 }} Comments</span>
            </button>

            <!-- Share Button -->
            <button class="btn btn-outline-secondary d-flex align-items-center gap-2" @click="shareStory">
              <i class="bi bi-share"></i>
              <span>Share</span>
            </button>
          </div>

          <hr />

          <!-- Comments Section -->
          <section id="comments-section" class="comments-section">
            <h4 class="fw-bold mb-4">
              <i class="bi bi-chat-square-text me-2"></i>
              Comments ({{ story.commentCount || 0 }})
            </h4>

            <!-- Add Comment Form -->
            <div v-if="userID !== 'defaultUser'" class="add-comment-form mb-4">
              <div class="d-flex gap-3">
                <img 
                  :src="currentUserPhoto || defaultProfilePhoto" 
                  alt="Your avatar"
                  class="rounded-circle"
                  style="width: 40px; height: 40px; object-fit: cover;"
                />
                <div class="flex-grow-1">
                  <textarea 
                    v-model="newComment"
                    class="form-control"
                    rows="3"
                    placeholder="Write a comment..."
                    :disabled="submittingComment"
                  ></textarea>
                  <div class="d-flex justify-content-end mt-2">
                    <button 
                      class="btn btn-primary"
                      @click="submitComment"
                      :disabled="!newComment.trim() || submittingComment"
                    >
                      <span v-if="submittingComment">
                        <span class="spinner-border spinner-border-sm me-1"></span>
                        Posting...
                      </span>
                      <span v-else>Post Comment</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="alert alert-light text-center mb-4">
              <router-link to="/login" class="btn btn-primary">
                Login to comment
              </router-link>
            </div>

            <!-- Comments List -->
            <!-- TODO: Implement comments with likes/dislikes (model after assembly post comments) -->
            <div class="comments-list">
              <div 
                v-for="comment in comments" 
                :key="comment.id"
                class="comment-item mb-3 p-3 bg-light rounded"
              >
                <!-- Comment Header -->
                <div class="d-flex align-items-center mb-2">
                  <img 
                    :src="comment.userPhoto || defaultProfilePhoto" 
                    alt="Commenter"
                    class="rounded-circle me-2"
                    style="width: 32px; height: 32px; object-fit: cover; cursor: pointer;"
                    @click="goToUserProfile(comment)"
                  />
                  <div>
                    <a 
                      href="#" 
                      @click.prevent="goToUserProfile(comment)" 
                      class="fw-bold text-decoration-none small"
                    >
                      {{ comment.username || 'Unknown' }}
                    </a>
                    <div class="text-muted small">{{ formatTimeAgo(comment.dateCreated) }}</div>
                  </div>
                  
                  <!-- Delete button (for comment owner) -->
                  <button 
                    v-if="isCommentOwner(comment)"
                    class="btn btn-sm btn-outline-danger ms-auto"
                    @click="deleteComment(comment)"
                    title="Delete comment"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </div>

                <!-- Comment Content -->
                <p class="comment-content mb-2">{{ comment.commentContent }}</p>

                <!-- Comment Actions (Like/Dislike) -->
                <div class="comment-actions d-flex gap-3 small">
                  <button 
                    class="btn btn-sm p-0 text-muted"
                    :class="{ 'text-success': comment.userLiked }"
                    @click="likeComment(comment)"
                  >
                    <i class="bi" :class="comment.userLiked ? 'bi-hand-thumbs-up-fill' : 'bi-hand-thumbs-up'"></i>
                    {{ comment.likeCount || 0 }}
                  </button>
                  <button 
                    class="btn btn-sm p-0 text-muted"
                    :class="{ 'text-danger': comment.userDisliked }"
                    @click="dislikeComment(comment)"
                  >
                    <i class="bi" :class="comment.userDisliked ? 'bi-hand-thumbs-down-fill' : 'bi-hand-thumbs-down'"></i>
                    {{ comment.dislikeCount || 0 }}
                  </button>
                </div>
              </div>

              <!-- Empty Comments State -->
              <div v-if="comments.length === 0 && !loadingComments" class="text-center py-4 text-muted">
                <i class="bi bi-chat-square text-muted" style="font-size: 2rem;"></i>
                <p class="mt-2">No comments yet. Be the first to comment!</p>
              </div>

              <!-- Load More Comments -->
              <div v-if="hasMoreComments && comments.length > 0" class="text-center mt-3">
                <button 
                  class="btn btn-outline-secondary"
                  @click="loadMoreComments"
                  :disabled="loadingComments"
                >
                  <span v-if="loadingComments">Loading...</span>
                  <span v-else>Load More Comments</span>
                </button>
              </div>
            </div>
          </section>
        </article>
      </div>

      <!-- Sidebar Column -->
      <div class="col-lg-4 d-none d-lg-block">
        <!-- Drinks Mentioned -->
        <div v-if="story.linkedListings && story.linkedListings.length > 0" class="card shadow-sm mb-4">
          <div class="card-header bg-dark text-white">
            <h6 class="mb-0 fw-bold">
              <i class="bi bi-cup-straw me-2"></i>
              Drinks Mentioned
            </h6>
          </div>
          <div class="card-body">
            <div 
              v-for="drink in story.linkedListings" 
              :key="drink.id"
              class="drink-item d-flex align-items-center mb-2 p-2 rounded hover-bg"
              @click="goToDrink(drink)"
            >
              <img 
                :src="drink.photo || drink.listingImage || defaultDrinkImage" 
                :alt="drink.listingName"
                class="rounded me-2"
                style="width: 40px; height: 40px; object-fit: cover;"
              />
              <div>
                <div class="fw-bold small">{{ drink.listingName }}</div>
                <div class="text-muted small">{{ drink.producerName }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Author Card -->
        <div class="card shadow-sm mb-4">
          <div class="card-header bg-light">
            <h6 class="mb-0 fw-bold">About the Author</h6>
          </div>
          <div class="card-body text-center">
            <img 
              :src="story.creatorPhoto || defaultProfilePhoto" 
              alt="Author"
              class="rounded-circle mb-2"
              style="width: 80px; height: 80px; object-fit: cover; cursor: pointer;"
              @click="goToAuthorProfile"
            />
            <h6 class="fw-bold mb-1">
              <a 
                href="#" 
                @click.prevent="goToAuthorProfile" 
                class="text-decoration-none"
              >
                {{ getAuthorDisplayName() }}
              </a>
            </h6>
            <p v-if="story.creatorBio" class="small text-muted">{{ story.creatorBio }}</p>
            <button 
              class="btn btn-sm btn-outline-primary mt-2"
              @click="goToAuthorProfile"
            >
              View Profile
            </button>
          </div>
        </div>

        <!-- Share Card -->
        <div class="card shadow-sm">
          <div class="card-header bg-light">
            <h6 class="mb-0 fw-bold">Share This Story</h6>
          </div>
          <div class="card-body">
            <div class="d-grid gap-2">
              <button class="btn btn-outline-secondary btn-sm" @click="shareStory">
                <i class="bi bi-link-45deg me-2"></i> Copy Link
              </button>
              <button class="btn btn-outline-primary btn-sm" @click="shareToTwitter">
                <i class="bi bi-twitter-x me-2"></i> Share on X
              </button>
              <button class="btn btn-outline-primary btn-sm" @click="shareToFacebook">
                <i class="bi bi-facebook me-2"></i> Share on Facebook
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Delete Confirmation Modal -->
  <div 
    class="modal fade" 
    id="deleteModal" 
    tabindex="-1"
    ref="deleteModal"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title text-danger">
            <i class="bi bi-exclamation-triangle me-2"></i>Delete Story
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete this story?</p>
          <p class="text-muted small">This action cannot be undone.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button 
            type="button" 
            class="btn btn-danger"
            @click="deleteStory"
            :disabled="deleting"
          >
            <span v-if="deleting">Deleting...</span>
            <span v-else>Delete Story</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import { useToast } from "vue-toastification";

export default {
  name: "SpecificStory",
  components: {
    NavBar,
  },
  data() {
    return {
      // API Base URL
      currentURL: process.env.VUE_APP_API_URL,
      
      // Story Data
      story: {
        id: null,
        storyTitle: '',
        storyContent: '',
        storyPhotos: [],
        publicationDate: null,
        likeCount: 0,
        commentCount: 0,
        userLiked: false,
        // Creator info
        creatorUserID: null,
        creatorUserType: null,
        creatorUsername: '',
        creatorDisplayName: '',
        creatorPhoto: null,
        creatorBio: null,
        // Context
        topicID: null,
        topicName: null,
        newsletterID: null,
        newsletterName: null,
        // Related
        linkedListings: [],
        hashtags: [],
        readTime: null,
        editedAt: null,
      },
      
      // Comments
      comments: [],
      loadingComments: false,
      hasMoreComments: false,
      commentsOffset: 0,
      newComment: '',
      submittingComment: false,
      replyingTo: null,  // For nested replies
      
      // Loading States
      loading: true,
      error: false,
      liking: false,
      deleting: false,
      
      // User State
      userID: "defaultUser",
      userType: null,
      username: null,
      currentUserPhoto: null,
      
      // Modals
      deleteModalInstance: null,
      
      // Default images
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
      defaultDrinkImage: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",
    };
  },

  computed: {
    isOwner() {
      if (!this.story.creatorUserID || this.userID === 'defaultUser') return false;
      return String(this.story.creatorUserID) === String(this.userID) &&
             this.story.creatorUserType === this.userType;
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

    // Initialize delete modal
    this.$nextTick(() => {
      if (this.$refs.deleteModal && window.bootstrap?.Modal) {
        this.deleteModalInstance = new window.bootstrap.Modal(this.$refs.deleteModal);
      }
    });

    // Load story data
    await this.loadStory();
    await this.loadComments();
  },

  methods: {
    async loadStory() {
      const storyId = this.$route.params.storyId;
      this.loading = true;
      this.error = false;
      
      try {
        // Build URL with optional viewer params
        let url = `${this.currentURL}/stories/getStory/${storyId}`;
        if (this.userID !== 'defaultUser') {
          url += `?viewerID=${this.userID}&viewerType=${this.userType}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.code === 200) {
          this.story = data.data;
        } else {
          console.error('Failed to load story:', data.message);
          this.error = true;
        }
      } catch (error) {
        console.error("Error loading story:", error);
        this.error = true;
      } finally {
        this.loading = false;
      }
    },

    async loadComments() {
      this.loadingComments = true;
      
      try {
        let url = `${this.currentURL}/stories/getStoryComments/${this.story.id}/${this.commentsOffset}`;
        if (this.userID !== 'defaultUser') {
          url += `?viewerID=${this.userID}&viewerType=${this.userType}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.code === 200) {
          if (this.commentsOffset === 0) {
            this.comments = data.data || [];
          } else {
            this.comments = [...this.comments, ...(data.data || [])];
          }
          this.hasMoreComments = data.hasMore || false;
        }
      } catch (error) {
        console.error("Error loading comments:", error);
      } finally {
        this.loadingComments = false;
      }
    },

    async loadMoreComments() {
      this.commentsOffset += 10;
      await this.loadComments();
    },

    async toggleLike() {
      if (this.userID === 'defaultUser') {
        useToast().warning("Please login to like stories");
        return;
      }
      
      this.liking = true;
      try {
        const endpoint = this.story.userLiked ? '/stories/unlikeStory' : '/stories/likeStory';
        const method = this.story.userLiked ? 'DELETE' : 'POST';
        
        const response = await fetch(`${this.currentURL}${endpoint}`, {
          method: method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            storyID: this.story.id,
            userID: this.userID,
            userType: this.userType
          })
        });
        
        const data = await response.json();
        
        if (data.code === 200 || data.code === 201) {
          // Update local state
          this.story.userLiked = !this.story.userLiked;
          this.story.likeCount = data.data?.likeCount ?? (this.story.likeCount + (this.story.userLiked ? 1 : -1));
        } else {
          useToast().error(data.message || "Failed to update like");
        }
      } catch (error) {
        console.error("Error toggling like:", error);
        useToast().error("Failed to update like");
      } finally {
        this.liking = false;
      }
    },

    async submitComment(parentCommentID = null) {
      if (!this.newComment.trim()) return;
      
      this.submittingComment = true;
      try {
        const response = await fetch(`${this.currentURL}/stories/createStoryComment`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            storyID: this.story.id,
            userID: this.userID,
            userType: this.userType,
            commentContent: this.newComment.trim(),
            parentCommentID: parentCommentID
          })
        });
        
        const data = await response.json();
        
        if (data.code === 201) {
          useToast().success("Comment posted!");
          this.newComment = '';
          this.replyingTo = null;
          // Reload comments to get the new one
          this.commentsOffset = 0;
          await this.loadComments();
          this.story.commentCount++;
        } else {
          useToast().error(data.message || "Failed to post comment");
        }
      } catch (error) {
        console.error("Error posting comment:", error);
        useToast().error("Failed to post comment");
      } finally {
        this.submittingComment = false;
      }
    },

    async likeComment(comment) {
      if (this.userID === 'defaultUser') {
        useToast().warning("Please login to like comments");
        return;
      }
      
      try {
        const response = await fetch(`${this.currentURL}/stories/likeStoryComment`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            commentID: comment.id,
            userID: this.userID,
            userType: this.userType
          })
        });
        
        const data = await response.json();
        
        if (data.code === 200) {
          // Update local state
          comment.likeCount = data.data.likeCount;
          comment.dislikeCount = data.data.dislikeCount;
          comment.userVote = data.data.userVote;
        }
      } catch (error) {
        console.error("Error liking comment:", error);
      }
    },

    async dislikeComment(comment) {
      if (this.userID === 'defaultUser') {
        useToast().warning("Please login to dislike comments");
        return;
      }
      
      try {
        const response = await fetch(`${this.currentURL}/stories/dislikeStoryComment`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            commentID: comment.id,
            userID: this.userID,
            userType: this.userType
          })
        });
        
        const data = await response.json();
        
        if (data.code === 200) {
          // Update local state
          comment.likeCount = data.data.likeCount;
          comment.dislikeCount = data.data.dislikeCount;
          comment.userVote = data.data.userVote;
        }
      } catch (error) {
        console.error("Error disliking comment:", error);
      }
    },

    async deleteComment(comment) {
      if (!confirm('Delete this comment?')) return;
      
      try {
        const response = await fetch(`${this.currentURL}/stories/deleteStoryComment`, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            commentID: comment.id,
            userID: this.userID,
            userType: this.userType
          })
        });
        
        const data = await response.json();
        
        if (data.code === 200) {
          useToast().success("Comment deleted");
          // Remove from local list
          this.comments = this.comments.filter(c => c.id !== comment.id);
          this.story.commentCount--;
        } else {
          useToast().error(data.message || "Failed to delete comment");
        }
      } catch (error) {
        console.error("Error deleting comment:", error);
        useToast().error("Failed to delete comment");
      }
    },

    isCommentOwner(comment) {
      if (this.userID === 'defaultUser') return false;
      // Comment author or story author can delete
      const isCommentAuthor = String(comment.userID) === String(this.userID) && comment.userType === this.userType;
      return isCommentAuthor || this.isOwner;
    },

    editStory() {
      // For now, show toast - inline editing will be implemented later
      useToast().info("Story editing coming soon!");
      // TODO: Implement inline editing similar to assembly posts
    },

    confirmDelete() {
      if (this.deleteModalInstance) {
        this.deleteModalInstance.show();
      } else if (window.bootstrap?.Modal && this.$refs.deleteModal) {
        // Lazy initialization if bootstrap wasn't available on mount
        this.deleteModalInstance = new window.bootstrap.Modal(this.$refs.deleteModal);
        this.deleteModalInstance.show();
      }
    },

    async deleteStory() {
      this.deleting = true;
      try {
        const response = await fetch(`${this.currentURL}/stories/deleteStory`, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            storyID: this.story.id,
            userID: this.userID,
            userType: this.userType
          })
        });
        
        const data = await response.json();
        
        if (data.code === 200) {
          useToast().success("Story deleted");
          if (this.deleteModalInstance) this.deleteModalInstance.hide();
          // Navigate back to user's stories
          this.$router.push(`/profile/user/${this.userID}/${this.username}/stories`);
        } else {
          useToast().error(data.message || "Failed to delete story");
        }
      } catch (error) {
        console.error("Error deleting story:", error);
        useToast().error("Failed to delete story");
      } finally {
        this.deleting = false;
      }
    },

    shareStory() {
      const url = window.location.href;
      navigator.clipboard.writeText(url);
      useToast().success("Link copied to clipboard!");
    },

    shareToTwitter() {
      const url = encodeURIComponent(window.location.href);
      const text = encodeURIComponent(this.story.storyTitle);
      window.open(`https://twitter.com/intent/tweet?url=${url}&text=${text}`, '_blank');
    },

    shareToFacebook() {
      const url = encodeURIComponent(window.location.href);
      window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank');
    },

    scrollToComments() {
      const commentsSection = document.getElementById('comments-section');
      if (commentsSection) {
        commentsSection.scrollIntoView({ behavior: 'smooth' });
      }
    },

    goBack() {
      // Try to go back to previous page, or default to topics
      if (window.history.length > 1) {
        this.$router.back();
      } else {
        this.$router.push('/stories/topics');
      }
    },

    goToAuthorProfile() {
      if (this.story.creatorUserID && this.story.creatorUserType) {
        this.$router.push(`/profile/${this.story.creatorUserType}/${this.story.creatorUserID}/${this.story.creatorUsername}`);
      }
    },

    goToUserProfile(comment) {
      if (comment.userID && comment.userType) {
        this.$router.push(`/profile/${comment.userType}/${comment.userID}/${comment.username}`);
      }
    },

    goToDrink(drink) {
      // TODO: Navigate to listing page
      this.$router.push(`/listing/${drink.id}/${this.slugify(drink.listingName)}`);
    },

    openPhotoModal(photo) {
      // TODO: Implement photo lightbox/modal
      window.open(photo, '_blank');
    },

    getAuthorDisplayName() {
      return this.story.creatorDisplayName || this.story.creatorUsername || 'Unknown Author';
    },

    formatDate(dateString) {
      if (!dateString) return '';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
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
/* Story Article Styles */
.story-article {
  max-width: 750px;
}

.story-title {
  font-size: 2.25rem;
  line-height: 1.3;
}

/* Story Content Rich Text Styles */
.story-content {
  font-size: 1.1rem;
  line-height: 1.8;
}

.story-content :deep(p) {
  margin-bottom: 1.5rem;
}

.story-content :deep(h2),
.story-content :deep(h3) {
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.story-content :deep(img) {
  max-width: 100%;
  border-radius: 8px;
  margin: 1rem 0;
}

.story-content :deep(blockquote) {
  border-left: 4px solid #dee2e6;
  padding-left: 1rem;
  margin: 1.5rem 0;
  font-style: italic;
  color: #6c757d;
}

/* Comment Styles */
.comment-item {
  border-left: 3px solid transparent;
  transition: border-color 0.2s;
}

.comment-item:hover {
  border-left-color: #0d6efd;
}

/* Hover Background */
.hover-bg {
  cursor: pointer;
  transition: background-color 0.2s;
}

.hover-bg:hover {
  background-color: #f8f9fa;
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
  .story-title {
    font-size: 1.75rem;
  }
  
  .story-content {
    font-size: 1rem;
    line-height: 1.7;
  }
}
</style>
