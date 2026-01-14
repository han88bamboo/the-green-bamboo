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
    <!-- Back Navigation + Owner Actions -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <button class="btn btn-outline-secondary btn-sm" @click="goBack">
        <i class="bi bi-arrow-left me-1"></i> Back
      </button>
      
      <!-- Owner Actions (Edit/Delete) - only visible to story owner, hidden during editing -->
      <div v-if="isOwner && !loading && !error && !isEditingStory" class="owner-actions">
        <button class="btn btn-sm btn-outline-primary me-2" @click="startEditStory">
          <i class="bi bi-pencil me-1"></i> Edit
        </button>
        <button class="btn btn-sm btn-outline-danger" @click="confirmDelete">
          <i class="bi bi-trash me-1"></i> Delete
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
            <!-- Topic/Newsletter Context (View Mode) -->
            <div v-if="!isEditingStory" class="context-badges mb-3">
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

            <!-- Story Title - View Mode -->
            <div v-if="!isEditingStory" class="text-start d-flex align-items-start gap-2 mb-3">
              <h1 class="story-title fw-bold mb-0 flex-grow-1">{{ story.storyTitle }}</h1>
              <button 
                v-if="isOwner"
                class="btn btn-sm p-0 text-secondary edit-icon-btn"
                @click="startEditStory"
                title="Edit story"
              >
                <i class="bi bi-pencil"></i>
              </button>
            </div>
            
            <!-- Story Title - Edit Mode -->
            <div v-if="isEditingStory" class="mb-3">
              <label class="form-label fw-bold">Title</label>
              <input 
                type="text"
                class="form-control form-control-lg fw-bold"
                v-model="editStory.title"
                placeholder="Story title..."
                maxlength="500"
              />
              <div class="form-text text-end">{{ editStory.title.length }}/500</div>
            </div>

            <!-- Author Info (always visible) -->
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
          </header>

          <!-- Feature Image - View Mode -->
          <div v-if="!isEditingStory && story.storyPhotos && story.storyPhotos.length > 0" class="story-featured-image mb-4">
            <img 
              :src="story.storyPhotos[0]" 
              :alt="story.storyTitle"
              class="featured-image-medium rounded shadow-sm"
            />
          </div>
          
          <!-- Feature Image - Edit Mode -->
          <div v-if="isEditingStory" class="mb-4">
            <label class="form-label fw-bold">Feature Image</label>
            <div v-if="editStory.featureImage" class="position-relative d-inline-block">
              <img 
                :src="editStory.featureImage" 
                alt="Feature image"
                class="featured-image-medium rounded shadow-sm"
              />
              <button 
                class="btn btn-sm btn-danger position-absolute top-0 end-0 m-2 rounded-circle"
                @click="removeEditFeatureImage"
                title="Remove image"
              >
                <i class="bi bi-x"></i>
              </button>
            </div>
            <div v-else class="mb-2">
              <label class="upload-placeholder d-flex align-items-center justify-content-center rounded border border-dashed p-4" style="cursor: pointer; background: #f8f9fa;">
                <input 
                  type="file" 
                  accept="image/png,image/jpeg,image/jpg,image/webp" 
                  class="d-none"
                  @change="handleEditFeatureImageUpload"
                />
                <div class="text-center text-muted">
                  <i class="bi bi-image" style="font-size: 2rem;"></i>
                  <div class="mt-2">Click to upload feature image</div>
                  <small>PNG, JPG, WebP • Max 5MB</small>
                </div>
              </label>
            </div>
          </div>

          <!-- Story Content - View Mode -->
          <div v-if="!isEditingStory" class="text-start d-flex align-items-start gap-2 mb-4">
            <div class="story-content flex-grow-1" v-html="story.storyContent"></div>
            <button 
              v-if="isOwner && story.storyContent"
              class="btn btn-sm p-0 text-secondary edit-icon-btn"
              @click="startEditStory"
              title="Edit content"
            >
              <i class="bi bi-pencil"></i>
            </button>
          </div>
          
          <!-- Story Content - Edit Mode -->
          <div v-if="isEditingStory" class="mb-4">
            <label class="form-label fw-bold">Content</label>
            <InlineRichTextEditor
              ref="storyContentEditor"
              :initial-content="editStory.content"
              @content-changed="onEditStoryContentChange"
              :section-id="'edit-story-content'"
            />
          </div>

          <!-- Linked Drinks - Edit Mode -->
          <div v-if="isEditingStory" class="mb-4">
            <label class="form-label fw-bold">Linked Drinks (Max 5)</label>
            <!-- Selected drinks display -->
            <div v-if="editStory.linkedListings.length > 0" class="d-flex flex-wrap gap-2 mb-2">
              <div 
                v-for="(drink, index) in editStory.linkedListings" 
                :key="drink.id"
                class="drink-tag d-flex align-items-center gap-2 rounded px-2 py-1"
              >
                <img 
                  :src="drink.photo || drink.listingImage || defaultDrinkImage" 
                  :alt="drink.listingName"
                  class="rounded"
                  style="width: 24px; height: 24px; object-fit: cover;"
                />
                <span class="small">{{ drink.listingName }}</span>
                <button 
                  type="button"
                  class="btn btn-sm p-0 text-danger"
                  @click="removeEditLinkedDrink(index)"
                >
                  <i class="bi bi-x"></i>
                </button>
              </div>
            </div>
            <!-- Autocomplete selector -->
            <AutocompleteSearchSelector
              v-if="editStory.linkedListings.length < 5"
              placeholder="Search for drinks to link..."
              @drink-selected="onEditLinkedDrinkSelected"
            />
          </div>

          <!-- Hashtags - Edit Mode -->
          <div v-if="isEditingStory" class="mb-4">
            <label class="form-label fw-bold">Hashtags</label>
            <div class="d-flex flex-wrap gap-2 mb-2">
              <span 
                v-for="(tag, index) in editStory.hashtags" 
                :key="tag"
                class="badge bg-light text-dark border d-flex align-items-center gap-1"
              >
                #{{ tag }}
                <button 
                  type="button"
                  class="btn btn-sm p-0 text-secondary"
                  @click="removeEditHashtag(index)"
                >
                  <i class="bi bi-x"></i>
                </button>
              </span>
            </div>
            <div class="input-group input-group-sm" style="max-width: 250px;">
              <span class="input-group-text">#</span>
              <input 
                type="text" 
                class="form-control"
                v-model="editStory.hashtagInput"
                placeholder="Add hashtag"
                @keypress.enter.prevent="addEditHashtag"
              />
              <button 
                class="btn btn-outline-secondary"
                type="button"
                @click="addEditHashtag"
              >
                Add
              </button>
            </div>
            <div class="form-text">Only letters and numbers allowed. Max 10 hashtags.</div>
          </div>

          <!-- Edit Actions -->
          <div v-if="isEditingStory" class="edit-actions d-flex gap-2 mb-4 pt-2 border-top">
            <button 
              class="btn btn-secondary btn-sm"
              @click="cancelEditStory"
              :disabled="savingStory"
            >
              Cancel
            </button>
            <button 
              class="btn btn-primary btn-sm"
              @click="saveEditStory"
              :disabled="!editStory.title.trim() || !editStory.content.trim() || savingStory"
            >
              <span v-if="savingStory">
                <span class="spinner-border spinner-border-sm me-1"></span>
                Saving...
              </span>
              <span v-else>Save Changes</span>
            </button>
          </div>

          <!-- Additional Photos Gallery (View Mode Only) -->
          <div v-if="!isEditingStory && story.storyPhotos && story.storyPhotos.length > 1" class="photo-gallery mb-4">
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

          <!-- Hashtags (View Mode Only) -->
          <div v-if="!isEditingStory && story.hashtags && story.hashtags.length > 0" class="hashtags-section mb-4">
            <span 
              v-for="hashtag in story.hashtags" 
              :key="hashtag"
              class="badge bg-light text-dark border me-2 mb-1"
            >
              #{{ hashtag }}
            </span>
          </div>

          <hr v-if="!isEditingStory" />

          <!-- Engagement Actions (View Mode Only) -->
          <div v-if="!isEditingStory" class="engagement-actions d-flex align-items-center gap-4 mb-4">
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

          <hr v-if="!isEditingStory" />

          <!-- Comments Section (View Mode Only) -->
          <section v-if="!isEditingStory" id="comments-section" class="comments-section">
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
                      @click="submitComment(null)"
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
            <div class="comments-list">
              <!-- Root Comment -->
              <div 
                v-for="comment in comments" 
                :key="comment.id"
                class="comment-item"
              >
                <div class="d-flex">
                  <!-- Commenter Avatar -->
                  <img 
                    :src="comment.userPhoto || defaultProfilePhoto" 
                    :alt="comment.username || 'Commenter'"
                    class="rounded-circle me-3 comment-avatar"
                    @click="goToUserProfile(comment)"
                  />
                  
                  <div class="flex-grow-1">
                    <!-- Comment Header -->
                    <div class="comment-header d-flex align-items-center flex-wrap gap-1 mb-1">
                      <a 
                        href="#" 
                        @click.prevent="goToUserProfile(comment)" 
                        class="fw-bold text-decoration-none comment-author"
                      >
                        {{ comment.displayName || comment.username || 'Unknown' }}
                      </a>
                      <span class="text-muted small">•</span>
                      <span class="text-muted small">{{ formatTimeAgo(comment.dateCreated) }}</span>
                    </div>
                    
                    <!-- Comment Content -->
                    <div class="text-start comment-content mb-2">{{ comment.commentContent }}</div>
                    
                    <!-- Comment Actions -->
                    <div class="comment-actions d-flex align-items-center gap-3 small">
                      <!-- Vote Buttons -->
                      <div class="d-flex align-items-center gap-1">
                        <button 
                          class="btn btn-sm p-0 comment-vote-btn"
                          @click="voteComment(comment, 'up')"
                          :disabled="userID === 'defaultUser'"
                          title="Upvote"
                        >
                          <i class="bi bi-arrow-up" :class="{ 'text-primary fw-bold': comment.userVote === 'up' }"></i>
                        </button>
                        <span 
                          class="vote-count-small fw-bold"
                          :class="getVoteCountClass(comment.voteCount)"
                        >
                          {{ comment.voteCount || 0 }}
                        </span>
                        <button 
                          class="btn btn-sm p-0 comment-vote-btn"
                          @click="voteComment(comment, 'down')"
                          :disabled="userID === 'defaultUser'"
                          title="Downvote"
                        >
                          <i class="bi bi-arrow-down" :class="{ 'text-danger fw-bold': comment.userVote === 'down' }"></i>
                        </button>
                      </div>
                      
                      <!-- Reply Button -->
                      <button 
                        v-if="userID !== 'defaultUser'"
                        class="btn btn-sm p-0 text-muted comment-action-btn"
                        @click="startReply(comment)"
                      >
                        <i class="bi bi-chat me-1"></i>Reply
                      </button>
                      
                      <!-- Delete Button (comment author or admin) -->
                      <button 
                        v-if="canDeleteComment(comment)"
                        class="btn btn-sm p-0 text-muted comment-action-btn"
                        @click="deleteComment(comment)"
                      >
                        <i class="bi bi-trash me-1"></i>Delete
                      </button>
                    </div>
                    
                    <!-- Reply Input (shown when replying to this comment) -->
                    <div v-if="replyingToCommentId === comment.id" class="reply-input mt-3">
                      <div class="d-flex gap-2">
                        <img 
                          :src="currentUserPhoto || defaultProfilePhoto" 
                          alt="Your avatar"
                          class="rounded-circle"
                          style="width: 32px; height: 32px; object-fit: cover;"
                        />
                        <div class="flex-grow-1">
                          <textarea 
                            class="form-control form-control-sm mb-2" 
                            rows="2" 
                            :placeholder="`Reply to ${comment.displayName || comment.username}...`"
                            v-model="replyContent"
                            maxlength="5000"
                            :ref="'replyTextarea-' + comment.id"
                          ></textarea>
                          <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">{{ replyContent.length }}/5000</small>
                            <div class="d-flex gap-2">
                              <button 
                                class="btn btn-sm btn-outline-secondary" 
                                @click="cancelReply"
                              >
                                Cancel
                              </button>
                              <button 
                                class="btn btn-sm btn-primary" 
                                @click="submitReply(comment)"
                                :disabled="!replyContent.trim() || submittingReply"
                              >
                                <span v-if="submittingReply">
                                  <span class="spinner-border spinner-border-sm me-1"></span>
                                </span>
                                <span v-else>Reply</span>
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Replies Section (2nd level - flattened) -->
                    <div v-if="comment.replies && comment.replies.length > 0" class="replies-section mt-3">
                      <div 
                        v-for="reply in comment.replies" 
                        :key="reply.id"
                        class="reply-item"
                      >
                        <div class="d-flex">
                          <!-- Reply Author Avatar -->
                          <img 
                            :src="reply.userPhoto || defaultProfilePhoto" 
                            :alt="reply.username || 'Replier'"
                            class="rounded-circle me-2 reply-avatar"
                            @click="goToUserProfile(reply)"
                          />
                          
                          <div class="flex-grow-1">
                            <!-- Reply Header -->
                            <div class="comment-header d-flex align-items-center flex-wrap gap-1 mb-1">
                              <a 
                                href="#" 
                                @click.prevent="goToUserProfile(reply)" 
                                class="fw-bold text-decoration-none comment-author"
                              >
                                {{ reply.displayName || reply.username || 'Unknown' }}
                              </a>
                              <span class="text-muted small">•</span>
                              <span class="text-muted small">{{ formatTimeAgo(reply.dateCreated) }}</span>
                            </div>
                            
                            <!-- Reply Content -->
                            <div class="text-start comment-content mb-2 small">{{ reply.commentContent }}</div>
                            
                            <!-- Reply Actions -->
                            <div class="comment-actions d-flex align-items-center gap-3 small">
                              <!-- Vote Buttons -->
                              <div class="d-flex align-items-center gap-1">
                                <button 
                                  class="btn btn-sm p-0 comment-vote-btn"
                                  @click="voteComment(reply, 'up')"
                                  :disabled="userID === 'defaultUser'"
                                >
                                  <i class="bi bi-arrow-up" :class="{ 'text-primary fw-bold': reply.userVote === 'up' }"></i>
                                </button>
                                <span 
                                  class="vote-count-small fw-bold"
                                  :class="getVoteCountClass(reply.voteCount)"
                                >
                                  {{ reply.voteCount || 0 }}
                                </span>
                                <button 
                                  class="btn btn-sm p-0 comment-vote-btn"
                                  @click="voteComment(reply, 'down')"
                                  :disabled="userID === 'defaultUser'"
                                >
                                  <i class="bi bi-arrow-down" :class="{ 'text-danger fw-bold': reply.userVote === 'down' }"></i>
                                </button>
                              </div>
                              
                              <!-- Reply to Reply (prepends @username to parent) -->
                              <button 
                                v-if="userID !== 'defaultUser'"
                                class="btn btn-sm p-0 text-muted comment-action-btn"
                                @click="startReplyToReply(comment, reply)"
                              >
                                <i class="bi bi-chat me-1"></i>Reply
                              </button>
                              
                              <!-- Delete Button -->
                              <button 
                                v-if="canDeleteComment(reply)"
                                class="btn btn-sm p-0 text-muted comment-action-btn"
                                @click="deleteReply(comment, reply)"
                              >
                                <i class="bi bi-trash me-1"></i>Delete
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <!-- Load More Replies Button -->
                      <button 
                        v-if="comment.hasMoreReplies"
                        class="btn btn-sm btn-link text-muted ps-0 mt-2"
                        @click="loadMoreReplies(comment)"
                        :disabled="comment.loadingMoreReplies"
                      >
                        <span v-if="comment.loadingMoreReplies">
                          <span class="spinner-border spinner-border-sm me-1"></span>
                          Loading...
                        </span>
                        <span v-else>
                          <i class="bi bi-arrow-return-right me-1"></i>
                          Load more replies ({{ comment.replyCount - comment.replies.length }})
                        </span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Empty Comments State -->
              <div v-if="comments.length === 0 && !loadingComments" class="text-center py-5 text-muted">
                <i class="bi bi-chat-square-text" style="font-size: 3rem;"></i>
                <p class="mt-3">No comments yet. Be the first to share your thoughts!</p>
              </div>

              <!-- Load More Comments -->
              <div v-if="hasMoreComments && comments.length > 0" class="text-center mt-4">
                <button 
                  class="btn btn-outline-primary"
                  @click="loadMoreComments"
                  :disabled="loadingComments"
                >
                  <span v-if="loadingComments">
                    <span class="spinner-border spinner-border-sm me-1"></span>
                    Loading...
                  </span>
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
import InlineRichTextEditor from "@/components/InlineRichTextEditor.vue";
import AutocompleteSearchSelector from "@/components/AutocompleteSearchSelector.vue";
import { useToast } from "vue-toastification";

export default {
  name: "SpecificStory",
  components: {
    NavBar,
    InlineRichTextEditor,
    AutocompleteSearchSelector,
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
      replyingToCommentId: null,  // Track which comment we're replying to
      replyContent: '',  // Content of the reply
      submittingReply: false,
      isAdmin: false,  // Track if current user is admin
      
      // Loading States
      loading: true,
      error: false,
      liking: false,
      deleting: false,
      
      // Edit Story State
      isEditingStory: false,
      savingStory: false,
      editStory: {
        title: '',
        content: '',
        featureImage: null,
        featureImageFile: null,
        linkedListings: [],
        topicID: null,
        newsletterID: null,
        hashtags: [],
        publicationDate: null,
        hashtagInput: '',
      },
      originalStoryState: null,
      
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

    // Check if user is admin
    const isAdminStr = localStorage.getItem("88B_isAdmin");
    this.isAdmin = isAdminStr === "true";

    // Get current user photo
    const storedUser = localStorage.getItem("88B_loggedInUser");
    if (storedUser) {
      try {
        const userData = JSON.parse(storedUser);
        this.currentUserPhoto = userData.photo || null;
      } catch (e) {
        console.error("Error parsing user data:", e);
      }
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

    // Unified vote method for both comments and replies (toggle upvote/downvote)
    async voteComment(comment, voteType) {
      if (this.userID === 'defaultUser') {
        useToast().warning("Please login to vote on comments");
        return;
      }
      
      try {
        const endpoint = voteType === 'up' ? '/stories/likeStoryComment' : '/stories/dislikeStoryComment';
        const response = await fetch(`${this.currentURL}${endpoint}`, {
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
          comment.voteCount = data.data.voteCount;
          comment.userVote = data.data.userVote;
        }
      } catch (error) {
        console.error("Error voting on comment:", error);
      }
    },

    // Reply methods (same pattern as SpecificAssemblyPost.vue)
    startReply(comment) {
      this.replyingToCommentId = comment.id;
      this.replyContent = '';
      this.$nextTick(() => {
        const textareaRef = this.$refs['replyTextarea-' + comment.id];
        const textarea = Array.isArray(textareaRef) ? textareaRef[0] : textareaRef;
        if (textarea && textarea.focus) textarea.focus();
      });
    },

    startReplyToReply(parentComment, reply) {
      // Reply to a reply prepends @username to parent comment
      this.replyingToCommentId = parentComment.id;
      const username = reply.displayName || reply.username || 'user';
      this.replyContent = `@${username} `;
      this.$nextTick(() => {
        const textareaRef = this.$refs['replyTextarea-' + parentComment.id];
        const textarea = Array.isArray(textareaRef) ? textareaRef[0] : textareaRef;
        if (textarea && textarea.focus) {
          textarea.focus();
          // Move cursor to end
          textarea.setSelectionRange(textarea.value.length, textarea.value.length);
        }
      });
    },

    cancelReply() {
      this.replyingToCommentId = null;
      this.replyContent = '';
    },

    async submitReply(parentComment) {
      if (!this.replyContent.trim()) return;
      
      this.submittingReply = true;
      try {
        const response = await fetch(`${this.currentURL}/stories/createStoryComment`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            storyID: this.story.id,
            userID: this.userID,
            userType: this.userType,
            commentContent: this.replyContent.trim(),
            parentCommentID: parentComment.id
          })
        });
        
        const data = await response.json();
        
        if (data.code === 201) {
          useToast().success("Reply posted!");
          this.replyContent = '';
          this.replyingToCommentId = null;
          // Reload comments to get the new reply
          this.commentsOffset = 0;
          await this.loadComments();
          this.story.commentCount++;
        } else {
          useToast().error(data.message || "Failed to post reply");
        }
      } catch (error) {
        console.error("Error posting reply:", error);
        useToast().error("Failed to post reply");
      } finally {
        this.submittingReply = false;
      }
    },

    async loadMoreReplies(comment) {
      // Set loading state
      this.$set ? this.$set(comment, 'loadingMoreReplies', true) : (comment.loadingMoreReplies = true);
      
      try {
        const currentRepliesCount = comment.replies ? comment.replies.length : 0;
        const response = await fetch(
          `${this.currentURL}/stories/getCommentReplies/${comment.id}/${currentRepliesCount}?userID=${this.userID}&userType=${this.userType}`
        );
        
        const data = await response.json();
        
        if (data.code === 200) {
          // Append new replies
          if (!comment.replies) comment.replies = [];
          comment.replies = [...comment.replies, ...(data.data || [])];
          comment.hasMoreReplies = comment.replies.length < comment.replyCount;
        }
      } catch (error) {
        console.error("Error loading more replies:", error);
      } finally {
        comment.loadingMoreReplies = false;
      }
    },

    // Check if user can delete this comment (comment author or admin)
    canDeleteComment(comment) {
      if (this.userID === 'defaultUser') return false;
      const isCommentAuthor = String(comment.userID) === String(this.userID) && comment.userType === this.userType;
      return isCommentAuthor || this.isAdmin;
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

    async deleteReply(parentComment, reply) {
      if (!confirm('Delete this reply?')) return;
      
      try {
        const response = await fetch(`${this.currentURL}/stories/deleteStoryComment`, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            commentID: reply.id,
            userID: this.userID,
            userType: this.userType
          })
        });
        
        const data = await response.json();
        
        if (data.code === 200) {
          useToast().success("Reply deleted");
          // Remove from local list
          parentComment.replies = parentComment.replies.filter(r => r.id !== reply.id);
          parentComment.replyCount--;
          this.story.commentCount--;
        } else {
          useToast().error(data.message || "Failed to delete reply");
        }
      } catch (error) {
        console.error("Error deleting reply:", error);
        useToast().error("Failed to delete reply");
      }
    },

    // ===== STORY EDITING METHODS =====
    
    startEditStory() {
      // Initialize edit state with current story data
      this.editStory = {
        title: this.story.storyTitle || '',
        content: this.story.storyContent || '',
        featureImage: (this.story.storyPhotos && this.story.storyPhotos.length > 0) ? this.story.storyPhotos[0] : null,
        featureImageFile: null,
        linkedListings: [...(this.story.linkedListings || [])],
        topicID: this.story.topicID || null,
        newsletterID: this.story.newsletterID || null,
        hashtags: [...(this.story.hashtags || [])],
        publicationDate: this.story.publicationDate || null,
        hashtagInput: '',
      };
      this.originalStoryState = JSON.stringify(this.editStory);
      this.isEditingStory = true;
    },

    cancelEditStory() {
      const currentState = JSON.stringify({
        title: this.editStory.title,
        content: this.editStory.content,
        featureImage: this.editStory.featureImage,
        linkedListings: this.editStory.linkedListings,
        topicID: this.editStory.topicID,
        newsletterID: this.editStory.newsletterID,
        hashtags: this.editStory.hashtags,
        publicationDate: this.editStory.publicationDate,
      });
      
      if (currentState !== this.originalStoryState) {
        if (!confirm('You have unsaved changes. Are you sure you want to cancel?')) {
          return;
        }
      }
      
      this.isEditingStory = false;
      this.editStory = {
        title: '',
        content: '',
        featureImage: null,
        featureImageFile: null,
        linkedListings: [],
        topicID: null,
        newsletterID: null,
        hashtags: [],
        publicationDate: null,
        hashtagInput: '',
      };
      this.originalStoryState = null;
    },

    onEditStoryContentChange(content) {
      this.editStory.content = content;
    },

    handleEditFeatureImageUpload(event) {
      const toast = useToast();
      const file = event.target.files[0];
      if (!file) return;
      
      // Validate file type
      const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
      if (!validTypes.includes(file.type)) {
        toast.warning('Please select a PNG, JPG, JPEG, or WebP image.');
        return;
      }
      
      // Validate file size (5MB max)
      if (file.size > 5 * 1024 * 1024) {
        toast.warning('Image must be less than 5MB.');
        return;
      }
      
      this.editStory.featureImageFile = file;
      
      // Preview
      const reader = new FileReader();
      reader.onload = (e) => {
        this.editStory.featureImage = e.target.result;
      };
      reader.readAsDataURL(file);
      
      event.target.value = '';
    },

    removeEditFeatureImage() {
      this.editStory.featureImage = null;
      this.editStory.featureImageFile = null;
    },

    onEditLinkedDrinkSelected(drink) {
      if (drink && !this.editStory.linkedListings.find(d => d.id === drink.id)) {
        if (this.editStory.linkedListings.length >= 5) {
          useToast().warning("Maximum 5 drinks can be linked.");
          return;
        }
        this.editStory.linkedListings.push(drink);
      }
    },

    removeEditLinkedDrink(index) {
      this.editStory.linkedListings.splice(index, 1);
    },

    addEditHashtag() {
      const raw = this.editStory.hashtagInput.trim().replace(/^#/, '');
      const tag = raw.toLowerCase();
      
      if (!tag) {
        this.editStory.hashtagInput = '';
        return;
      }
      
      // Validate alphanumeric only
      const alphanumericRegex = /^[a-z0-9]+$/i;
      if (!alphanumericRegex.test(tag)) {
        useToast().warning("Hashtags can only contain letters and numbers.");
        this.editStory.hashtagInput = '';
        return;
      }
      
      if (this.editStory.hashtags.length >= 10) {
        useToast().warning("Maximum 10 hashtags allowed.");
        this.editStory.hashtagInput = '';
        return;
      }
      
      if (!this.editStory.hashtags.includes(tag)) {
        this.editStory.hashtags.push(tag);
      }
      this.editStory.hashtagInput = '';
    },

    removeEditHashtag(index) {
      this.editStory.hashtags.splice(index, 1);
    },

    async saveEditStory() {
      const toast = useToast();
      
      if (!this.editStory.title.trim()) {
        toast.error('Title is required.');
        return;
      }
      
      if (!this.editStory.content.trim()) {
        toast.error('Content is required.');
        return;
      }
      
      this.savingStory = true;
      
      try {
        const payload = {
          storyID: this.story.id,
          userID: this.userID,
          userType: this.userType,
          title: this.editStory.title.trim(),
          content: this.editStory.content,
          listingIDs: this.editStory.linkedListings.map(d => d.id),
          topicID: this.editStory.topicID,
          newsletterID: this.editStory.newsletterID,
          hashtags: this.editStory.hashtags,
        };
        
        // Handle feature image
        if (this.editStory.featureImageFile) {
          // New image uploaded - convert to base64
          payload.featureImage = await this.fileToBase64(this.editStory.featureImageFile);
        } else if (this.editStory.featureImage === null) {
          // Image was removed
          payload.featureImage = null;
        }
        // If featureImage is still a URL, we don't send it (no change)
        
        const response = await fetch(`${this.currentURL}/stories/editStory`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        
        const data = await response.json();
        
        if (data.code === 200) {
          toast.success('Story updated successfully!');
          this.isEditingStory = false;
          
          // Reload story data
          await this.loadStory();
        } else {
          toast.error(data.message || 'Failed to update story.');
        }
      } catch (error) {
        console.error('Error updating story:', error);
        toast.error('Failed to update story. Please try again.');
      } finally {
        this.savingStory = false;
      }
    },

    fileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
      });
    },

    // Legacy method - now redirects to inline edit
    editStory() {
      this.startEditStory();
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

    getVoteCountClass(voteCount) {
      if (voteCount > 0) return 'text-primary';
      if (voteCount < 0) return 'text-danger';
      return 'text-muted';
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

/* Medium-style Featured Image (landscape crop like the screenshot) */
.featured-image-medium {
  width: 100%;
  aspect-ratio: 16 / 9;  /* Landscape ratio similar to Medium */
  object-fit: cover;
  object-position: center;
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
  padding: 16px 0;
  border-bottom: 1px solid #eee;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  object-fit: cover;
  cursor: pointer;
  flex-shrink: 0;
}

.comment-author {
  color: #212529;
  font-size: 0.9rem;
}

.comment-author:hover {
  text-decoration: underline !important;
}

.comment-content {
  color: #495057;
  line-height: 1.6;
  word-break: break-word;
}

/* Comment Actions */
.comment-vote-btn {
  color: #6c757d;
  background: none;
  border: none;
  line-height: 1;
}

.comment-vote-btn:hover:not(:disabled) {
  color: #495057;
}

.comment-vote-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.vote-count-small {
  font-size: 0.85rem;
  min-width: 20px;
  text-align: center;
}

.comment-action-btn {
  background: none;
  border: none;
  font-size: 0.8rem;
}

.comment-action-btn:hover {
  color: #212529 !important;
  text-decoration: underline;
}

/* Replies Section (same as SpecificAssemblyPost.vue) */
.replies-section {
  border-left: 2px solid #e9ecef;
  padding-left: 16px;
  margin-left: 4px;
}

.reply-item {
  padding: 12px 0;
}

.reply-item:last-child {
  padding-bottom: 0;
}

.reply-avatar {
  width: 28px;
  height: 28px;
  object-fit: cover;
  cursor: pointer;
  flex-shrink: 0;
}

/* Reply Input */
.reply-input textarea {
  resize: none;
}

/* Hover Background */
.hover-bg {
  cursor: pointer;
  transition: background-color 0.2s;
}

.hover-bg:hover {
  background-color: #f8f9fa;
}

/* Edit Icon Button */
.edit-icon-btn {
  opacity: 0;
  transition: opacity 0.2s ease;
  line-height: 1;
}

.story-article:hover .edit-icon-btn,
.edit-icon-btn:focus {
  opacity: 1;
}

/* Drink Tags for Editing */
.drink-tag {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
}

.drink-tag:hover {
  background-color: #e9ecef;
}

/* Edit Actions */
.edit-actions {
  border-color: #e9ecef !important;
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
  
  .comment-avatar {
    width: 32px;
    height: 32px;
  }
}

/* Extra small devices */
@media (max-width: 576px) {
  .comment-item {
    padding: 12px 0;
  }
  
  .comment-actions {
    flex-wrap: wrap;
  }
}
</style>
