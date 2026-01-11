<template>
  <NavBar />
  
  <div class="container px-4 mt-4">
    <!-- Back Button -->
    <div class="row mb-3">
      <div class="col-12 d-flex justify-content-start">
        <button class="btn btn-outline-secondary" @click="goBack">
          <i class="bi bi-arrow-left"></i> Back to {{ assemblyName || 'Assembly' }}
        </button>
      </div>
    </div>

    <!-- Loading State (Skeleton) -->
    <div v-if="loading" class="post-detail">
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <div class="d-flex">
            <!-- Vote Column Skeleton -->
            <div class="vote-column d-flex flex-column align-items-center me-3">
              <div class="skeleton-circle mb-2" style="width: 32px; height: 32px;"></div>
              <div class="skeleton-text" style="width: 30px; height: 20px;"></div>
              <div class="skeleton-circle mt-2" style="width: 32px; height: 32px;"></div>
            </div>
            <!-- Content Skeleton -->
            <div class="flex-grow-1">
              <div class="skeleton-text mb-2" style="width: 60%; height: 14px;"></div>
              <div class="skeleton-text mb-3" style="width: 80%; height: 24px;"></div>
              <div class="skeleton-text mb-2" style="width: 100%; height: 16px;"></div>
              <div class="skeleton-text mb-2" style="width: 95%; height: 16px;"></div>
              <div class="skeleton-text mb-2" style="width: 90%; height: 16px;"></div>
              <div class="skeleton-rect mt-3" style="width: 100%; height: 300px;"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-5">
      <i class="bi bi-exclamation-triangle text-danger" style="font-size: 3rem;"></i>
      <h4 class="text-muted mt-3">Failed to load post</h4>
      <p class="text-muted">{{ error }}</p>
      <button class="btn btn-primary" @click="loadPostData">Try Again</button>
    </div>

    <!-- Post Content -->
    <div v-else class="post-detail">
      <!-- Main Post Card (OP Content) -->
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <div class="d-flex">
            <!-- Vote Column -->
            <div class="vote-column d-flex flex-column align-items-center me-3">
              <button 
                class="btn btn-sm p-0 vote-btn"
                @click="votePost('up')"
                :disabled="!isMember"
                :title="!isMember ? 'Join assembly to vote' : 'Upvote'"
              >
                <i class="bi bi-arrow-up-circle-fill fs-4" :class="{ 'text-primary': post.userVote === 'up' }"></i>
              </button>
              <span class="vote-count fw-bold my-2 fs-5" :class="getVoteCountClass(post.voteCount)">
                {{ post.voteCount || 0 }}
              </span>
              <button 
                class="btn btn-sm p-0 vote-btn"
                @click="votePost('down')"
                :disabled="!isMember"
                :title="!isMember ? 'Join assembly to vote' : 'Downvote'"
              >
                <i class="bi bi-arrow-down-circle-fill fs-4" :class="{ 'text-danger': post.userVote === 'down' }"></i>
              </button>
            </div>

            <!-- Post Content -->
            <div class="post-content flex-grow-1">
              <!-- Post Meta -->
              <div class="text-start post-meta text-muted small mb-2">
                <a 
                  href="#" 
                  @click.prevent="goToAssembly" 
                  class="text-decoration-none fw-bold"
                  style="color: #0d6efd;"
                >
                  Assembly/{{ assemblyName }}
                </a>
                <span class="mx-1">•</span>
                <span>Posted by </span>
                <a href="#" @click.prevent="goToUserProfile(post.posterInfo)" class="text-decoration-none">
                  {{ getPosterDisplayName(post.posterInfo) }}
                </a>
                <span class="mx-1">•</span>
                <span>{{ formatTimeAgo(post.postDate) }}</span>
                <!-- Edited Indicator -->
                <span v-if="post.editedAt" class="ms-1 text-muted fst-italic" :title="'Edited ' + formatDateTime(post.editedAt)">
                  (edited)
                </span>
              </div>

              <!-- Post Title - View Mode -->
              <div v-if="!isEditingPost" class="text-start d-flex align-items-start gap-2 mb-3">
                <h3 class="post-title fw-bold mb-0 flex-grow-1">{{ post.postTitle }}</h3>
                <button 
                  v-if="canEditPost"
                  class="btn btn-sm p-0 text-secondary edit-icon-btn"
                  @click="startEditPost"
                  title="Edit title"
                >
                  <i class="bi bi-pencil"></i>
                </button>
              </div>
              
              <!-- Post Title - Edit Mode -->
              <div v-else class="mb-3">
                <input 
                  type="text"
                  class="form-control form-control-lg fw-bold"
                  v-model="editPost.title"
                  placeholder="Post title..."
                  maxlength="500"
                />
                <div class="form-text text-end">{{ editPost.title.length }}/500</div>
              </div>

              <!-- Post Full Content - View Mode -->
              <div v-if="!isEditingPost" class="text-start d-flex align-items-start gap-2 mb-3">
                <div class="post-body flex-grow-1" v-html="post.postContent"></div>
                <button 
                  v-if="canEditPost && post.postContent"
                  class="btn btn-sm p-0 text-secondary edit-icon-btn"
                  @click="startEditPost"
                  title="Edit content"
                >
                  <i class="bi bi-pencil"></i>
                </button>
              </div>
              
              <!-- Post Content - Edit Mode -->
              <div v-if="isEditingPost" class="mb-3">
                <InlineRichTextEditor
                  ref="postContentEditor"
                  :initial-content="editPost.content"
                  @content-changed="onEditContentChange"
                  :section-id="'edit-post-content'"
                />
              </div>

              <!-- Post Images - Edit Mode -->
              <div v-if="isEditingPost" class="mb-3">
                <label class="form-label fw-bold">Images (Max 5)</label>
                <div class="d-flex flex-wrap gap-2 mb-2">
                  <!-- Existing/New Images -->
                  <div 
                    v-for="(image, index) in editPost.images" 
                    :key="index"
                    class="position-relative"
                  >
                    <img 
                      :src="image.preview || image" 
                      class="rounded"
                      style="width: 80px; height: 80px; object-fit: cover;"
                    />
                    <button 
                      class="btn btn-sm btn-danger position-absolute top-0 end-0 rounded-circle p-0"
                      style="width: 20px; height: 20px; line-height: 1;"
                      @click="removeEditImage(index)"
                    >
                      <i class="bi bi-x"></i>
                    </button>
                  </div>
                  <!-- Add Image Button -->
                  <label 
                    v-if="editPost.images.length < 5"
                    class="upload-placeholder d-flex align-items-center justify-content-center rounded border border-dashed"
                    style="width: 80px; height: 80px; cursor: pointer;"
                  >
                    <input 
                      type="file" 
                      accept="image/*" 
                      class="d-none"
                      @change="handleEditImageUpload"
                      multiple
                    />
                    <i class="bi bi-plus-lg text-muted"></i>
                  </label>
                </div>
              </div>

              <!-- Edit Actions -->
              <div v-if="isEditingPost" class="edit-actions d-flex gap-2 mb-3 pt-2 border-top">
                <button 
                  class="btn btn-secondary btn-sm"
                  @click="cancelEditPost"
                  :disabled="savingPost"
                >
                  Cancel
                </button>
                <button 
                  class="btn btn-primary btn-sm"
                  @click="saveEditPost"
                  :disabled="!editPost.title.trim() || savingPost"
                >
                  <span v-if="savingPost">
                    <span class="spinner-border spinner-border-sm me-1"></span>
                    Saving...
                  </span>
                  <span v-else>Save Changes</span>
                </button>
              </div>

              <!-- Linked Drinks (View Mode Only) -->
              <div v-if="!isEditingPost && post.linkedListings && post.linkedListings.length > 0" class="linked-drinks mb-3">
                <div class="d-flex align-items-center mb-2">
                  <i class="bi bi-cup-straw text-muted me-2"></i>
                  <span class="small text-muted fw-bold">Linked Drinks</span>
                </div>
                <div class="d-flex gap-2 flex-wrap">
                  <div 
                    v-for="listing in post.linkedListings" 
                    :key="listing.id"
                    class="linked-drink-card d-flex align-items-center p-2 rounded border bg-light"
                    @click="goToListing(listing.id, listing.listingName)"
                    style="cursor: pointer;"
                  >
                    <img 
                      v-if="listing.photo" 
                      :src="listing.photo" 
                      class="rounded me-2"
                      style="width: 40px; height: 40px; object-fit: cover;"
                      :alt="listing.listingName"
                    />
                    <i v-else class="bi bi-cup-straw me-2 fs-4 text-muted"></i>
                    <div>
                      <div class="small fw-bold text-truncate" style="max-width: 150px;">{{ listing.listingName }}</div>
                      <div v-if="listing.producerName" class="small text-muted">{{ listing.producerName }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Post Image(s) Carousel (View Mode Only) -->
              <div v-if="!isEditingPost && post.postPhotos && post.postPhotos.length > 0" class="post-images mb-3">
                <!-- Single Image -->
                <div v-if="post.postPhotos.length === 1">
                  <img 
                    :src="post.postPhotos[0]" 
                    alt="Post image"
                    class="img-fluid rounded cursor-pointer"
                    style="max-width: 100%; max-height: 500px; object-fit: contain;"
                    @click="openImageModal(0)"
                  />
                </div>
                
                <!-- Multiple Images Carousel -->
                <div v-else class="image-carousel position-relative">
                  <div class="carousel-container rounded overflow-hidden" style="max-height: 500px;">
                    <img 
                      :src="post.postPhotos[currentImageIndex]" 
                      :alt="`Post image ${currentImageIndex + 1}`"
                      class="img-fluid w-100 cursor-pointer"
                      style="max-height: 500px; object-fit: contain; background: #f8f9fa;"
                      @click="openImageModal(currentImageIndex)"
                    />
                  </div>
                  
                  <!-- Navigation Arrows -->
                  <button 
                    v-if="post.postPhotos.length > 1"
                    class="carousel-nav carousel-nav-prev"
                    @click="prevImage"
                    :disabled="currentImageIndex === 0"
                  >
                    <i class="bi bi-chevron-left"></i>
                  </button>
                  <button 
                    v-if="post.postPhotos.length > 1"
                    class="carousel-nav carousel-nav-next"
                    @click="nextImage"
                    :disabled="currentImageIndex === post.postPhotos.length - 1"
                  >
                    <i class="bi bi-chevron-right"></i>
                  </button>
                  
                  <!-- Image Counter -->
                  <div class="carousel-counter">
                    {{ currentImageIndex + 1 }} / {{ post.postPhotos.length }}
                  </div>
                  
                  <!-- Thumbnail Indicators -->
                  <div class="carousel-indicators d-flex justify-content-center gap-1 mt-2">
                    <button 
                      v-for="(photo, index) in post.postPhotos" 
                      :key="index"
                      class="carousel-indicator"
                      :class="{ 'active': index === currentImageIndex }"
                      @click="currentImageIndex = index"
                    ></button>
                  </div>
                </div>
              </div>

              <!-- Post Actions -->
              <div class="post-actions d-flex align-items-center gap-3 pt-3 border-top">
                <span class="action-btn text-muted">
                  <i class="bi bi-chat-square me-1"></i>
                  {{ post.commentCount || 0 }} Comments
                </span>
                <span class="action-btn text-muted" @click="sharePost">
                  <i class="bi bi-share me-1"></i>
                  Share
                </span>
                <!-- Edit Post (for poster only) -->
                <span 
                  v-if="canEditPost" 
                  class="action-btn text-muted" 
                  @click="startEditPost"
                >
                  <i class="bi bi-pencil me-1"></i>
                  Edit
                </span>
                <!-- Admin Actions -->
                <div v-if="isAdmin" class="dropdown ms-auto">
                  <button class="btn btn-sm btn-link text-muted p-0" data-bs-toggle="dropdown">
                    <i class="bi bi-three-dots"></i>
                  </button>
                  <ul class="dropdown-menu dropdown-menu-end">
                    <li>
                      <a class="dropdown-item" href="#" @click.prevent="togglePinPost">
                        <i class="bi" :class="post.isPinned ? 'bi-pin-angle' : 'bi-pin-fill'"></i>
                        {{ post.isPinned ? 'Unpin Post' : 'Pin Post' }}
                      </a>
                    </li>
                    <li>
                      <a class="dropdown-item text-danger" href="#" @click.prevent="confirmDeletePost">
                        <i class="bi bi-trash"></i> Delete Post
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Comments Section -->
      <div class="comments-section">
        <h5 class="fw-bold mb-3">
          <i class="bi bi-chat-square-text me-2"></i>
          Comments ({{ post.commentCount || 0 }})
        </h5>
        
        <!-- Add Comment (for members only) -->
        <div v-if="isMember" class="add-comment mb-4">
          <div class="card">
            <div class="card-body">
              <div class="d-flex align-items-start gap-3">
                <img 
                  :src="currentUserPhoto || defaultProfilePhoto" 
                  alt="Your avatar"
                  class="rounded-circle"
                  style="width: 40px; height: 40px; object-fit: cover;"
                />
                <div class="flex-grow-1">
                  <textarea 
                    class="form-control mb-2" 
                    rows="3" 
                    placeholder="What are your thoughts?"
                    v-model="newComment"
                    maxlength="5000"
                  ></textarea>
                  <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted">{{ newComment.length }}/5000</small>
                    <button 
                      class="btn btn-primary btn-sm" 
                      @click="submitComment"
                      :disabled="!newComment.trim() || submittingComment"
                    >
                      <span v-if="submittingComment">
                        <span class="spinner-border spinner-border-sm me-1"></span>
                        Posting...
                      </span>
                      <span v-else>Comment</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else-if="userID !== 'defaultUser'" class="add-comment mb-4">
          <div class="card bg-light">
            <div class="card-body text-center">
              <p class="text-muted mb-2">Join this assembly to comment</p>
              <button class="btn btn-warning btn-sm fw-bold" @click="joinAssembly">
                <i class="bi bi-plus-circle me-1"></i> Join Assembly
              </button>
            </div>
          </div>
        </div>
        <div v-else class="add-comment mb-4">
          <div class="card bg-light">
            <div class="card-body text-center">
              <p class="text-muted mb-2">Log in to join the discussion</p>
              <button class="btn btn-primary btn-sm" @click="$router.push('/login')">
                Log In
              </button>
            </div>
          </div>
        </div>

        <!-- Comments Loading -->
        <div v-if="loadingComments" class="text-center py-4">
          <div class="spinner-border spinner-border-sm text-primary me-2"></div>
          <span class="text-muted">Loading comments...</span>
        </div>

        <!-- No Comments -->
        <div v-else-if="comments.length === 0" class="comments-list">
          <div class="text-center py-5 text-muted">
            <i class="bi bi-chat-square-text" style="font-size: 3rem;"></i>
            <p class="mt-3">No comments yet. Be the first to share your thoughts!</p>
          </div>
        </div>

        <!-- Comments List -->
        <div v-else class="comments-list">
          <!-- Root Comment -->
          <div 
            v-for="comment in comments" 
            :key="comment.id"
            :id="`comment-${comment.id}`"
            class="comment-item"
            :class="{ 'comment-highlighted': highlightedCommentId === comment.id }"
          >
            <div class="d-flex">
              <!-- Commenter Avatar -->
              <img 
                :src="getCommenterPhoto(comment.commenterInfo)" 
                :alt="getPosterDisplayName(comment.commenterInfo)"
                class="rounded-circle me-3 comment-avatar"
                @click="goToUserProfile(comment.commenterInfo)"
              />
              
              <div class="flex-grow-1">
                <!-- Comment Header -->
                <div class="comment-header d-flex align-items-center flex-wrap gap-1 mb-1">
                  <a 
                    href="#" 
                    @click.prevent="goToUserProfile(comment.commenterInfo)" 
                    class="fw-bold text-decoration-none comment-author"
                  >
                    {{ getPosterDisplayName(comment.commenterInfo) }}
                  </a>
                  <span class="text-muted small">•</span>
                  <span class="text-muted small">{{ formatTimeAgo(comment.commentDate) }}</span>
                  <span v-if="comment.editedAt" class="text-muted small fst-italic">(edited)</span>
                </div>
                
                <!-- Comment Content -->
                <div class="text-start comment-content mb-2" v-html="comment.commentContent"></div>
                
                <!-- Comment Actions -->
                <div class="comment-actions d-flex align-items-center gap-3 small">
                  <!-- Vote Buttons -->
                  <div class="d-flex align-items-center gap-1">
                    <button 
                      class="btn btn-sm p-0 comment-vote-btn"
                      @click="voteComment(comment, 'up')"
                      :disabled="!isMember"
                      :title="!isMember ? 'Join to vote' : 'Upvote'"
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
                      :disabled="!isMember"
                      :title="!isMember ? 'Join to vote' : 'Downvote'"
                    >
                      <i class="bi bi-arrow-down" :class="{ 'text-danger fw-bold': comment.userVote === 'down' }"></i>
                    </button>
                  </div>
                  
                  <!-- Reply Button -->
                  <button 
                    v-if="isMember"
                    class="btn btn-sm p-0 text-muted comment-action-btn"
                    @click="startReply(comment)"
                  >
                    <i class="bi bi-chat me-1"></i>Reply
                  </button>
                  
                  <!-- Delete Button (own comments) -->
                  <button 
                    v-if="canDeleteComment(comment)"
                    class="btn btn-sm p-0 text-muted comment-action-btn"
                    @click="confirmDeleteComment(comment)"
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
                        :placeholder="`Reply to ${getPosterDisplayName(comment.commenterInfo)}...`"
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
                    :id="`comment-${reply.id}`"
                    class="reply-item"
                    :class="{ 'comment-highlighted': highlightedCommentId === reply.id }"
                  >
                    <div class="d-flex">
                      <!-- Reply Author Avatar -->
                      <img 
                        :src="getCommenterPhoto(reply.commenterInfo)" 
                        :alt="getPosterDisplayName(reply.commenterInfo)"
                        class="rounded-circle me-2 reply-avatar"
                        @click="goToUserProfile(reply.commenterInfo)"
                      />
                      
                      <div class="flex-grow-1">
                        <!-- Reply Header -->
                        <div class="comment-header d-flex align-items-center flex-wrap gap-1 mb-1">
                          <a 
                            href="#" 
                            @click.prevent="goToUserProfile(reply.commenterInfo)" 
                            class="fw-bold text-decoration-none comment-author"
                          >
                            {{ getPosterDisplayName(reply.commenterInfo) }}
                          </a>
                          <span class="text-muted small">•</span>
                          <span class="text-muted small">{{ formatTimeAgo(reply.commentDate) }}</span>
                          <span v-if="reply.editedAt" class="text-muted small fst-italic">(edited)</span>
                        </div>
                        
                        <!-- Reply Content -->
                        <div class="text-start comment-content mb-2 small" v-html="reply.commentContent"></div>
                        
                        <!-- Reply Actions -->
                        <div class="comment-actions d-flex align-items-center gap-3 small">
                          <!-- Vote Buttons -->
                          <div class="d-flex align-items-center gap-1">
                            <button 
                              class="btn btn-sm p-0 comment-vote-btn"
                              @click="voteComment(reply, 'up')"
                              :disabled="!isMember"
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
                              :disabled="!isMember"
                            >
                              <i class="bi bi-arrow-down" :class="{ 'text-danger fw-bold': reply.userVote === 'down' }"></i>
                            </button>
                          </div>
                          
                          <!-- Reply to Reply (prepends @username to parent) -->
                          <button 
                            v-if="isMember"
                            class="btn btn-sm p-0 text-muted comment-action-btn"
                            @click="startReplyToReply(comment, reply)"
                          >
                            <i class="bi bi-chat me-1"></i>Reply
                          </button>
                          
                          <!-- Delete Button -->
                          <button 
                            v-if="canDeleteComment(reply)"
                            class="btn btn-sm p-0 text-muted comment-action-btn"
                            @click="confirmDeleteComment(reply)"
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
                      Load more replies ({{ comment.remainingReplies }})
                    </span>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Load More Comments Button -->
          <div v-if="hasMoreComments" class="text-center mt-4">
            <button 
              class="btn btn-outline-primary"
              @click="loadMoreComments"
              :disabled="loadingMoreComments"
            >
              <span v-if="loadingMoreComments">
                <span class="spinner-border spinner-border-sm me-1"></span>
                Loading...
              </span>
              <span v-else>Load More Comments</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Delete Comment Confirmation Modal -->
  <div 
    v-if="showDeleteCommentModal" 
    class="modal-overlay" 
    @click="showDeleteCommentModal = false"
  >
    <div class="modal-dialog modal-sm" @click.stop>
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Delete Comment</h5>
          <button type="button" class="btn-close" @click="showDeleteCommentModal = false"></button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete this comment? This action cannot be undone.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary btn-sm" @click="showDeleteCommentModal = false">Cancel</button>
          <button 
            type="button" 
            class="btn btn-danger btn-sm" 
            @click="deleteComment"
            :disabled="deletingComment"
          >
            <span v-if="deletingComment">
              <span class="spinner-border spinner-border-sm me-1"></span>
              Deleting...
            </span>
            <span v-else>Delete</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Delete Post Confirmation Modal -->
  <div 
    v-if="showDeletePostModal" 
    class="modal-overlay" 
    @click="showDeletePostModal = false"
  >
    <div class="modal-dialog modal-sm" @click.stop>
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Delete Post</h5>
          <button type="button" class="btn-close" @click="showDeletePostModal = false"></button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete this post? This will also delete all comments. This action cannot be undone.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary btn-sm" @click="showDeletePostModal = false">Cancel</button>
          <button 
            type="button" 
            class="btn btn-danger btn-sm" 
            @click="deletePost"
            :disabled="deletingPost"
          >
            <span v-if="deletingPost">
              <span class="spinner-border spinner-border-sm me-1"></span>
              Deleting...
            </span>
            <span v-else>Delete Post</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Image Modal -->
  <div 
    v-if="showImageModal" 
    class="image-modal-overlay" 
    @click="closeImageModal"
  >
    <div class="image-modal-content" @click.stop>
      <button class="image-modal-close" @click="closeImageModal">
        <i class="bi bi-x-lg"></i>
      </button>
      <img 
        :src="post.postPhotos[modalImageIndex]" 
        :alt="`Post image ${modalImageIndex + 1}`"
        class="img-fluid"
      />
      <!-- Modal Navigation -->
      <button 
        v-if="post.postPhotos.length > 1 && modalImageIndex > 0"
        class="image-modal-nav image-modal-prev"
        @click="modalImageIndex--"
      >
        <i class="bi bi-chevron-left"></i>
      </button>
      <button 
        v-if="post.postPhotos.length > 1 && modalImageIndex < post.postPhotos.length - 1"
        class="image-modal-nav image-modal-next"
        @click="modalImageIndex++"
      >
        <i class="bi bi-chevron-right"></i>
      </button>
      <div class="image-modal-counter">
        {{ modalImageIndex + 1 }} / {{ post.postPhotos.length }}
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import InlineRichTextEditor from "@/components/InlineRichTextEditor.vue";
import { useToast } from "vue-toastification";
import axios from "axios";

export default {
  name: "SpecificAssemblyPost",
  components: {
    NavBar,
    InlineRichTextEditor,
  },
  data() {
    return {
      // Post Data
      post: {
        id: null,
        postTitle: '',
        postContent: '',
        postPhotos: [],
        listingIDs: [],
        linkedListings: [],
        posterID: null,
        posterInfo: null,
        postDate: null,
        editedAt: null,
        voteCount: 0,
        likeCount: 0,
        dislikeCount: 0,
        commentCount: 0,
        userVote: null,
        isPinned: false,
      },
      
      // Assembly Info
      assemblyInfo: {
        id: null,
        assemblyName: '',
      },
      
      // User State
      userID: "defaultUser",
      userType: null,
      username: null,
      memberID: null,
      isMember: false,
      isAdmin: false,
      currentUserPhoto: null,
      
      // UI State
      loading: true,
      error: null,
      loadingComments: false,
      loadingMoreComments: false,
      submittingComment: false,
      submittingReply: false,
      
      // Comments
      comments: [],
      newComment: '',
      commentsOffset: 0,
      hasMoreComments: false,
      
      // Reply State
      replyingToCommentId: null,
      replyContent: '',
      
      // Delete Comment State
      showDeleteCommentModal: false,
      commentToDelete: null,
      deletingComment: false,
      
      // Highlight State (for notification links)
      highlightedCommentId: null,
      
      // Image Carousel
      currentImageIndex: 0,
      showImageModal: false,
      modalImageIndex: 0,

      // Edit Post State
      isEditingPost: false,
      savingPost: false,
      editPost: {
        title: '',
        content: '',
        images: [],
        newImageFiles: [],
      },
      originalPost: null,

      // Delete Post State
      showDeletePostModal: false,
      deletingPost: false,

      // Default images
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
      defaultDrinkPhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",
    };
  },
  computed: {
    assemblyId() {
      return this.$route.params.assemblyId;
    },
    assemblyNameParam() {
      return this.$route.params.assemblyName;
    },
    assemblyName() {
      return this.decodeAssemblyName(this.$route.params.assemblyName);
    },
    postId() {
      return this.$route.params.postId;
    },
    postTitleParam() {
      return this.$route.params.postTitle;
    },
    canEditPost() {
      if (!this.post.posterInfo || !this.memberID) return false;
      return this.post.posterID === this.memberID;
    },
  },
  mounted() {
    // Get user info from localStorage
    const accID = localStorage.getItem("88B_accID");
    if (accID !== null) {
      this.userID = accID;
    }
    this.userType = localStorage.getItem("88B_accType");
    this.username = localStorage.getItem("88B_accUsername");
    this.currentUserPhoto = localStorage.getItem("88B_accPhoto");
    
    // Check for comment anchor in URL hash
    this.checkForCommentAnchor();
    
    // Load post data
    this.loadPostData();
  },
  methods: {
    checkForCommentAnchor() {
      const hash = this.$route.hash;
      if (hash && hash.startsWith('#comment-')) {
        const commentId = parseInt(hash.replace('#comment-', ''));
        if (!isNaN(commentId)) {
          this.highlightedCommentId = commentId;
        }
      }
    },
    
    scrollToComment(commentId) {
      this.$nextTick(() => {
        const element = document.getElementById(`comment-${commentId}`);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'center' });
          // Remove highlight after 5 seconds
          setTimeout(() => {
            this.highlightedCommentId = null;
          }, 5000);
        }
      });
    },
    
    goBack() {
      // Check if we can go back in history
      if (window.history.length > 1) {
        this.$router.go(-1);
      } else {
        // Fallback to assembly page
        this.goToAssembly();
      }
    },

    goToAssembly() {
      this.$router.push({
        name: 'specificAssembly',
        params: {
          assemblyId: this.assemblyId,
          assemblyName: this.assemblyNameParam
        }
      });
    },

    goToUserProfile(userInfo) {
      if (!userInfo) return;
      
      if (userInfo.userType === 'user') {
        const slug = userInfo.username ? `/${this.slugify(userInfo.username)}` : '';
        this.$router.push(`/profile/user/${userInfo.userID}${slug}`);
      } else if (userInfo.userType === 'producer') {
        const slug = userInfo.producerName ? `/${this.slugify(userInfo.producerName)}` : '';
        this.$router.push(`/profile/producer/${userInfo.userID}${slug}`);
      } else if (userInfo.userType === 'venue') {
        const slug = userInfo.venueName ? `/${this.slugify(userInfo.venueName)}` : '';
        this.$router.push(`/profile/venue/${userInfo.userID}${slug}`);
      }
    },

    goToListing(listingId, listingName) {
      const slug = listingName ? `/${this.slugify(listingName)}` : '';
      this.$router.push(`/listing/view/${listingId}${slug}`);
    },

    async loadPostData() {
      this.loading = true;
      this.error = null;
      
      try {
        // Build query params
        let queryParams = '';
        if (this.userID !== 'defaultUser' && this.userType) {
          queryParams = `?userID=${this.userID}&userType=${this.userType}`;
        }
        
        const response = await axios.get(
          `${process.env.VUE_APP_API_URL}/assembly/getSpecificPost/${this.postId}${queryParams}`
        );
        
        if (response.data.code === 200) {
          const data = response.data.data;
          
          this.post = {
            id: data.id,
            postTitle: data.postTitle,
            postContent: data.postContent || '',
            postPhotos: data.postPhotos || [],
            listingIDs: data.listingIDs || [],
            linkedListings: data.linkedListings || [],
            posterID: data.posterID,
            posterInfo: data.posterInfo,
            postDate: data.postDate,
            editedAt: data.editedAt,
            voteCount: data.voteCount || 0,
            likeCount: data.likeCount || 0,
            dislikeCount: data.dislikeCount || 0,
            commentCount: data.commentCount || 0,
            userVote: data.userVote,
            isPinned: data.isPinned || false,
          };
          
          // Set membership info
          this.memberID = data.memberID;
          this.isMember = data.isMember || false;
          this.isAdmin = data.isAdmin || false;
          
          // Load comments after post is loaded
          this.loadComments();
        } else {
          this.error = response.data.message || 'Failed to load post';
        }
      } catch (err) {
        console.error('Error loading post:', err);
        this.error = 'An error occurred while loading the post.';
      } finally {
        this.loading = false;
      }
    },

    async loadComments() {
      this.loadingComments = true;
      this.commentsOffset = 0;
      
      try {
        let queryParams = '';
        if (this.userID !== 'defaultUser' && this.userType) {
          queryParams = `?userID=${this.userID}&userType=${this.userType}`;
        }
        
        const response = await axios.get(
          `${process.env.VUE_APP_API_URL}/assembly/getPostComments/${this.postId}/${this.commentsOffset}${queryParams}`
        );
        
        if (response.data.code === 200) {
          // Process comments to add UI state
          const loadedComments = (response.data.data || []).map(comment => ({
            ...comment,
            loadingMoreReplies: false,
            repliesOffset: comment.replies ? comment.replies.length : 0,
          }));
          
          this.comments = loadedComments;
          this.hasMoreComments = response.data.hasMore || false;
          this.commentsOffset = loadedComments.length;
          
          // If we have a highlighted comment, scroll to it
          if (this.highlightedCommentId) {
            // Check if it's in root comments or replies
            const foundInRoot = this.comments.some(c => c.id === this.highlightedCommentId);
            const foundInReplies = this.comments.some(c => 
              c.replies && c.replies.some(r => r.id === this.highlightedCommentId)
            );
            
            if (foundInRoot || foundInReplies) {
              this.scrollToComment(this.highlightedCommentId);
            }
          }
        }
      } catch (err) {
        console.error('Error loading comments:', err);
      } finally {
        this.loadingComments = false;
      }
    },
    
    async loadMoreComments() {
      this.loadingMoreComments = true;
      
      try {
        let queryParams = '';
        if (this.userID !== 'defaultUser' && this.userType) {
          queryParams = `?userID=${this.userID}&userType=${this.userType}`;
        }
        
        const response = await axios.get(
          `${process.env.VUE_APP_API_URL}/assembly/getPostComments/${this.postId}/${this.commentsOffset}${queryParams}`
        );
        
        if (response.data.code === 200) {
          const newComments = (response.data.data || []).map(comment => ({
            ...comment,
            loadingMoreReplies: false,
            repliesOffset: comment.replies ? comment.replies.length : 0,
          }));
          
          this.comments.push(...newComments);
          this.hasMoreComments = response.data.hasMore || false;
          this.commentsOffset += newComments.length;
        }
      } catch (err) {
        console.error('Error loading more comments:', err);
      } finally {
        this.loadingMoreComments = false;
      }
    },
    
    async loadMoreReplies(comment) {
      comment.loadingMoreReplies = true;
      
      try {
        let queryParams = '';
        if (this.userID !== 'defaultUser' && this.userType) {
          queryParams = `?userID=${this.userID}&userType=${this.userType}`;
        }
        
        const response = await axios.get(
          `${process.env.VUE_APP_API_URL}/assembly/getMoreReplies/${comment.id}/${comment.repliesOffset}${queryParams}`
        );
        
        if (response.data.code === 200) {
          const newReplies = response.data.data || [];
          comment.replies.push(...newReplies);
          comment.repliesOffset += newReplies.length;
          comment.hasMoreReplies = response.data.hasMore || false;
          comment.remainingReplies = response.data.remainingCount || 0;
        }
      } catch (err) {
        console.error('Error loading more replies:', err);
      } finally {
        comment.loadingMoreReplies = false;
      }
    },

    async voteComment(comment, voteType) {
      const toast = useToast();
      
      if (!this.isMember) {
        toast.warning('Join this assembly to vote.');
        return;
      }
      
      const previousVote = comment.userVote;
      const previousCount = comment.voteCount;
      
      // Optimistic update
      if (voteType === 'up') {
        if (comment.userVote === 'up') {
          comment.userVote = null;
          comment.voteCount--;
        } else {
          if (comment.userVote === 'down') {
            comment.voteCount++;
          }
          comment.userVote = 'up';
          comment.voteCount++;
        }
      } else {
        if (comment.userVote === 'down') {
          comment.userVote = null;
          comment.voteCount++;
        } else {
          if (comment.userVote === 'up') {
            comment.voteCount--;
          }
          comment.userVote = 'down';
          comment.voteCount--;
        }
      }
      
      try {
        await axios.put(`${process.env.VUE_APP_API_URL}/assembly/votePostComment`, {
          postID: this.post.id,
          commentID: comment.id,
          memberID: this.memberID,
          voteType: voteType
        });
      } catch (err) {
        // Revert on error
        comment.userVote = previousVote;
        comment.voteCount = previousCount;
        console.error('Error voting on comment:', err);
        toast.error('Failed to register vote.');
      }
    },
    
    startReply(comment) {
      this.replyingToCommentId = comment.id;
      this.replyContent = '';
      this.$nextTick(() => {
        const textareaRef = this.$refs['replyTextarea-' + comment.id];
        // Vue 3 returns refs inside v-for as arrays
        const textarea = Array.isArray(textareaRef) ? textareaRef[0] : textareaRef;
        if (textarea && textarea.focus) {
          textarea.focus();
        }
      });
    },
    
    startReplyToReply(parentComment, reply) {
      // When replying to a reply, prepend @username and reply to the parent comment
      this.replyingToCommentId = parentComment.id;
      const username = this.getPosterDisplayName(reply.commenterInfo);
      this.replyContent = `@${username} `;
      this.$nextTick(() => {
        const textareaRef = this.$refs['replyTextarea-' + parentComment.id];
        // Vue 3 returns refs inside v-for as arrays
        const textarea = Array.isArray(textareaRef) ? textareaRef[0] : textareaRef;
        if (textarea && textarea.focus) {
          textarea.focus();
          // Move cursor to end
          textarea.setSelectionRange(
            this.replyContent.length, 
            this.replyContent.length
          );
        }
      });
    },
    
    cancelReply() {
      this.replyingToCommentId = null;
      this.replyContent = '';
    },
    
    async submitReply(parentComment) {
      const toast = useToast();
      
      if (!this.replyContent.trim()) {
        toast.warning('Please enter a reply.');
        return;
      }
      
      this.submittingReply = true;
      
      // Store content before clearing
      const replyContentText = this.replyContent.trim();
      
      try {
        const response = await axios.post(`${process.env.VUE_APP_API_URL}/assembly/createPostComment`, {
          postID: this.post.id,
          memberID: this.memberID,
          commentContent: replyContentText,
          parentCommentID: parentComment.id
        });
        
        if (response.data.code === 201) {
          toast.success('Reply posted!');
          
          // Construct a proper reply object for immediate UI display
          // since backend only returns commentID and parentCommentID
          const newReply = {
            id: response.data.data.commentID,
            postID: this.post.id,
            parentCommentID: response.data.data.parentCommentID,
            commentContent: replyContentText,
            commentDate: new Date().toISOString(),
            commenterID: this.memberID,
            commenterInfo: {
              id: this.userID,
              userType: this.userType,
              username: this.username,
              photo: this.currentUserPhoto
            },
            voteCount: 0,
            userVote: null,
            canDelete: true
          };
          
          if (!parentComment.replies) {
            parentComment.replies = [];
          }
          parentComment.replies.push(newReply);
          parentComment.repliesOffset++;
          parentComment.replyCount = (parentComment.replyCount || 0) + 1;
          
          this.post.commentCount++;
          this.cancelReply();
        } else {
          toast.error(response.data.message || 'Failed to post reply.');
        }
      } catch (err) {
        console.error('Error posting reply:', err);
        toast.error('An error occurred while posting your reply.');
      } finally {
        this.submittingReply = false;
      }
    },
    
    canDeleteComment(comment) {
      if (!this.memberID) return false;
      // User can delete their own comments, or admins can delete any
      return comment.commenterID === this.memberID || this.isAdmin;
    },
    
    confirmDeleteComment(comment) {
      this.commentToDelete = comment;
      this.showDeleteCommentModal = true;
    },
    
    async deleteComment() {
      const toast = useToast();
      
      if (!this.commentToDelete) return;
      
      this.deletingComment = true;
      
      try {
        const response = await axios.delete(
          `${process.env.VUE_APP_API_URL}/assembly/deletePostComment`,
          {
            data: {
              commentID: this.commentToDelete.id,
              memberID: this.memberID,
              isAdmin: this.isAdmin
            }
          }
        );
        
        if (response.data.code === 200) {
          toast.success('Comment deleted.');
          
          // Remove from UI
          const commentId = this.commentToDelete.id;
          
          // Check if it's a root comment
          const rootIndex = this.comments.findIndex(c => c.id === commentId);
          if (rootIndex !== -1) {
            this.comments.splice(rootIndex, 1);
          } else {
            // It's a reply, find and remove from parent
            for (const comment of this.comments) {
              if (comment.replies) {
                const replyIndex = comment.replies.findIndex(r => r.id === commentId);
                if (replyIndex !== -1) {
                  comment.replies.splice(replyIndex, 1);
                  comment.replyCount = Math.max(0, (comment.replyCount || 1) - 1);
                  break;
                }
              }
            }
          }
          
          this.post.commentCount = Math.max(0, this.post.commentCount - 1);
          this.showDeleteCommentModal = false;
          this.commentToDelete = null;
        } else {
          toast.error(response.data.message || 'Failed to delete comment.');
        }
      } catch (err) {
        console.error('Error deleting comment:', err);
        toast.error('An error occurred while deleting the comment.');
      } finally {
        this.deletingComment = false;
      }
    },
    
    getCommenterPhoto(userInfo) {
      if (!userInfo) return this.defaultProfilePhoto;
      return userInfo.photo || this.defaultProfilePhoto;
    },

    async votePost(voteType) {
      const toast = useToast();
      
      if (!this.isMember) {
        toast.warning('Join this assembly to vote.');
        return;
      }
      
      const previousVote = this.post.userVote;
      const previousCount = this.post.voteCount;
      
      // Optimistic update
      if (voteType === 'up') {
        if (this.post.userVote === 'up') {
          this.post.userVote = null;
          this.post.voteCount--;
        } else {
          if (this.post.userVote === 'down') {
            this.post.voteCount++;
          }
          this.post.userVote = 'up';
          this.post.voteCount++;
        }
      } else {
        if (this.post.userVote === 'down') {
          this.post.userVote = null;
          this.post.voteCount++;
        } else {
          if (this.post.userVote === 'up') {
            this.post.voteCount--;
          }
          this.post.userVote = 'down';
          this.post.voteCount--;
        }
      }
      
      try {
        await axios.post(`${process.env.VUE_APP_API_URL}/assembly/voteAssemblyPost`, {
          postID: this.post.id,
          memberID: this.memberID,
          voteType: voteType
        });
      } catch (err) {
        // Revert on error
        this.post.userVote = previousVote;
        this.post.voteCount = previousCount;
        console.error('Error voting:', err);
        toast.error('Failed to register vote.');
      }
    },

    async submitComment() {
      const toast = useToast();
      
      if (!this.newComment.trim()) {
        toast.warning('Please enter a comment.');
        return;
      }
      
      this.submittingComment = true;
      
      try {
        const response = await axios.post(`${process.env.VUE_APP_API_URL}/assembly/createPostComment`, {
          postID: this.post.id,
          memberID: this.memberID,
          commentContent: this.newComment.trim(),
          parentCommentID: null
        });
        
        if (response.data.code === 201) {
          toast.success('Comment posted!');
          this.newComment = '';
          this.post.commentCount++;
          // Reload comments
          this.loadComments();
        } else {
          toast.error(response.data.message || 'Failed to post comment.');
        }
      } catch (err) {
        console.error('Error posting comment:', err);
        toast.error('An error occurred while posting your comment.');
      } finally {
        this.submittingComment = false;
      }
    },

    async joinAssembly() {
      const toast = useToast();
      
      if (this.userID === 'defaultUser') {
        this.$router.push('/login');
        return;
      }
      
      try {
        const response = await axios.post(`${process.env.VUE_APP_API_URL}/assembly/joinAssembly`, {
          assemblyID: this.assemblyId,
          userID: this.userID,
          userType: this.userType
        });
        
        if (response.data.code === 201) {
          toast.success('You have joined this assembly!');
          this.isMember = true;
          this.memberID = response.data.memberID;
        } else {
          toast.error(response.data.message || 'Failed to join assembly.');
        }
      } catch (err) {
        console.error('Error joining assembly:', err);
        toast.error('An error occurred while joining the assembly.');
      }
    },

    sharePost() {
      const shareUrl = window.location.href;
      
      navigator.clipboard.writeText(shareUrl).then(() => {
        const toast = useToast();
        toast.success('Post link copied to clipboard!');
      }).catch((err) => {
        console.error('Failed to copy text: ', err);
        const toast = useToast();
        toast.error('Failed to copy link.');
      });
    },

    startEditPost() {
      // Initialize edit state with current post data
      this.editPost = {
        title: this.post.postTitle || '',
        content: this.post.postContent || '',
        images: [...(this.post.postPhotos || [])],
        newImageFiles: [],
      };
      this.originalPost = JSON.stringify(this.editPost);
      this.isEditingPost = true;
    },

    cancelEditPost() {
      const currentState = JSON.stringify({
        title: this.editPost.title,
        content: this.editPost.content,
        images: this.editPost.images,
        newImageFiles: this.editPost.newImageFiles,
      });
      
      if (currentState !== this.originalPost) {
        if (!confirm('You have unsaved changes. Are you sure you want to cancel?')) {
          return;
        }
      }
      
      this.isEditingPost = false;
      this.editPost = {
        title: '',
        content: '',
        images: [],
        newImageFiles: [],
      };
      this.originalPost = null;
    },

    onEditContentChange(content) {
      this.editPost.content = content;
    },

    handleEditImageUpload(event) {
      const toast = useToast();
      const files = Array.from(event.target.files);
      const remainingSlots = 5 - this.editPost.images.length;
      
      if (files.length > remainingSlots) {
        toast.warning(`You can only add ${remainingSlots} more image(s).`);
      }
      
      const filesToAdd = files.slice(0, remainingSlots);
      
      filesToAdd.forEach(file => {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.editPost.images.push({
            preview: e.target.result,
            file: file,
            isNew: true
          });
        };
        reader.readAsDataURL(file);
      });
      
      // Reset input
      event.target.value = '';
    },

    removeEditImage(index) {
      this.editPost.images.splice(index, 1);
    },

    async saveEditPost() {
      const toast = useToast();
      
      if (!this.editPost.title.trim()) {
        toast.error('Title is required.');
        return;
      }
      
      this.savingPost = true;
      
      try {
        // Prepare images array - convert new files to base64, keep existing URLs
        const images = [];
        
        for (const img of this.editPost.images) {
          if (img.isNew && img.file) {
            // Convert new file to base64
            const base64 = await this.fileToBase64(img.file);
            images.push(base64);
          } else if (typeof img === 'string') {
            // Existing image URL
            images.push(img);
          }
        }
        
        const response = await axios.put(
          `${process.env.VUE_APP_API_URL}/assembly/editAssemblyPost`,
          {
            postID: this.post.id,
            memberID: this.memberID,
            postTitle: this.editPost.title.trim(),
            postContent: this.editPost.content || '',
            images: images,
            listingIDs: this.post.listingIDs || []
          }
        );
        
        if (response.data.code === 200) {
          toast.success('Post updated successfully!');
          this.isEditingPost = false;
          
          // Reload post data to get updated content
          await this.loadPostData();
        } else {
          toast.error(response.data.message || 'Failed to update post.');
        }
      } catch (error) {
        console.error('Error updating post:', error);
        toast.error(error.response?.data?.message || 'Failed to update post. Please try again.');
      } finally {
        this.savingPost = false;
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

    togglePinPost() {
      const toast = useToast();
      toast.info('Pin functionality coming soon!');
    },

    confirmDeletePost() {
      this.showDeletePostModal = true;
    },

    async deletePost() {
      const toast = useToast();
      this.deletingPost = true;
      
      try {
        const response = await axios.delete(
          `${process.env.VUE_APP_API_URL}/assembly/deleteAssemblyPost`,
          {
            data: {
              postID: this.post.id,
              memberID: this.memberID
            }
          }
        );
        
        if (response.data.code === 200) {
          toast.success('Post deleted successfully.');
          this.showDeletePostModal = false;
          
          // Navigate back to the assembly page
          this.$router.push({
            name: 'SpecificAssembly',
            params: {
              assemblyId: this.assemblyId,
              assemblyName: this.assemblyNameParam
            }
          });
        } else {
          toast.error(response.data.message || 'Failed to delete post.');
        }
      } catch (error) {
        console.error('Error deleting post:', error);
        toast.error(error.response?.data?.message || 'Failed to delete post. Please try again.');
      } finally {
        this.deletingPost = false;
      }
    },

    // Image Carousel Methods
    prevImage() {
      if (this.currentImageIndex > 0) {
        this.currentImageIndex--;
      }
    },

    nextImage() {
      if (this.currentImageIndex < this.post.postPhotos.length - 1) {
        this.currentImageIndex++;
      }
    },

    openImageModal(index) {
      this.modalImageIndex = index;
      this.showImageModal = true;
      document.body.style.overflow = 'hidden';
    },

    closeImageModal() {
      this.showImageModal = false;
      document.body.style.overflow = '';
    },

    // Helper Methods
    getPosterDisplayName(userInfo) {
      if (!userInfo) return 'Unknown';
      
      if (userInfo.userType === 'user') {
        return userInfo.username || 'Anonymous';
      } else if (userInfo.userType === 'producer') {
        return userInfo.producerName || 'Producer';
      } else if (userInfo.userType === 'venue') {
        return userInfo.venueName || 'Venue';
      }
      return 'Unknown';
    },

    getVoteCountClass(count) {
      if (count > 0) return 'text-primary';
      if (count < 0) return 'text-danger';
      return 'text-muted';
    },

    decodeAssemblyName(urlName) {
      if (!urlName) return '';
      return urlName
        .replace(/-/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
    },

    slugify(text) {
      if (!text) return '';
      return text
        .toString()
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/\s+/g, '-')
        .replace(/[^\w-]/g, '');
    },

    formatTimeAgo(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      const now = new Date();
      const seconds = Math.floor((now - date) / 1000);
      
      if (seconds < 60) return 'just now';
      if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
      if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
      if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;
      
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    formatDateTime(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
  },
};
</script>

<style scoped>
/* Skeleton Loading */
.skeleton-text,
.skeleton-circle,
.skeleton-rect {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: 4px;
}

.skeleton-circle {
  border-radius: 50%;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Vote Column */
.vote-column {
  min-width: 50px;
}

.vote-btn {
  color: #6c757d;
  transition: color 0.15s ease-in-out;
  background: none;
  border: none;
}

.vote-btn:hover:not(:disabled) {
  color: #495057;
}

.vote-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.vote-btn .bi-arrow-up-circle-fill.text-primary {
  color: #0d6efd !important;
}

.vote-btn .bi-arrow-down-circle-fill.text-danger {
  color: #dc3545 !important;
}

/* Post Content */
.post-title {
  color: #212529;
}

.post-body {
  color: #495057;
  line-height: 1.7;
}

/* Rich text content styling */
.post-body :deep(p) {
  margin-bottom: 1rem;
}

.post-body :deep(ul),
.post-body :deep(ol) {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

.post-body :deep(blockquote) {
  border-left: 3px solid #dee2e6;
  padding-left: 1rem;
  margin-left: 0;
  color: #6c757d;
}

.post-body :deep(a) {
  color: #0d6efd;
}

.post-body :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

/* Edit Icon Button */
.edit-icon-btn {
  opacity: 0;
  transition: opacity 0.15s ease-in-out;
  font-size: 0.85rem;
}

.post-content:hover .edit-icon-btn {
  opacity: 0.6;
}

.edit-icon-btn:hover {
  opacity: 1 !important;
  color: #0d6efd !important;
}

/* Edit Mode Styles */
.edit-actions {
  margin-top: 0.5rem;
}

.upload-placeholder {
  border-style: dashed !important;
  border-color: #dee2e6 !important;
}

.upload-placeholder:hover {
  background-color: #f8f9fa;
  border-color: #adb5bd !important;
}

.post-meta a {
  color: #6c757d;
}

.post-meta a:hover {
  text-decoration: underline !important;
}

/* Linked Drinks */
.linked-drink-card {
  transition: all 0.15s ease-in-out;
}

.linked-drink-card:hover {
  background-color: #e9ecef !important;
  transform: translateY(-1px);
}

/* Image Carousel */
.image-carousel {
  position: relative;
}

.carousel-container {
  background: #f8f9fa;
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s;
}

.carousel-nav:hover:not(:disabled) {
  background: rgba(0, 0, 0, 0.7);
}

.carousel-nav:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.carousel-nav-prev {
  left: 10px;
}

.carousel-nav-next {
  right: 10px;
}

.carousel-counter {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
}

.carousel-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #dee2e6;
  border: none;
  padding: 0;
  cursor: pointer;
  transition: background 0.2s;
}

.carousel-indicator.active {
  background: #0d6efd;
}

.cursor-pointer {
  cursor: pointer;
}

/* Post Actions */
.action-btn {
  cursor: pointer;
  transition: color 0.15s ease-in-out;
}

.action-btn:hover {
  color: #495057 !important;
}

/* Comments */
.add-comment textarea {
  resize: none;
}

/* Comment Items */
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

/* Rich text in comments */
.comment-content :deep(p) {
  margin-bottom: 0.5rem;
}

.comment-content :deep(p:last-child) {
  margin-bottom: 0;
}

.comment-content :deep(a) {
  color: #0d6efd;
}

.comment-content :deep(blockquote) {
  border-left: 2px solid #dee2e6;
  padding-left: 0.75rem;
  margin-left: 0;
  color: #6c757d;
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

/* Replies Section */
.replies-section {
  border-left: 2px solid #e9ecef;
  padding-left: 16px;
  margin-left: 4px;
}

.reply-item {
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}

.reply-item:last-child {
  border-bottom: none;
}

.reply-avatar {
  width: 28px;
  height: 28px;
  object-fit: cover;
  cursor: pointer;
  flex-shrink: 0;
}

/* Reply Input */
.reply-input {
  background: #f8f9fa;
  padding: 12px;
  border-radius: 8px;
}

/* Comment Highlight (for notification links) */
.comment-highlighted {
  background-color: rgba(255, 193, 7, 0.15);
  border-radius: 8px;
  padding: 16px !important;
  margin: -8px;
  animation: highlight-fade 5s ease-out forwards;
}

@keyframes highlight-fade {
  0% {
    background-color: rgba(255, 193, 7, 0.25);
  }
  70% {
    background-color: rgba(255, 193, 7, 0.15);
  }
  100% {
    background-color: transparent;
  }
}

/* Delete Comment Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 9998;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-overlay .modal-dialog {
  max-width: 400px;
  width: 100%;
}

.modal-overlay .modal-content {
  border-radius: 12px;
  border: none;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

/* Image Modal */
.image-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-modal-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
}

.image-modal-content img {
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
}

.image-modal-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

.image-modal-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.5rem;
}

.image-modal-nav:hover {
  background: rgba(255, 255, 255, 0.3);
}

.image-modal-prev {
  left: -60px;
}

.image-modal-next {
  right: -60px;
}

.image-modal-counter {
  position: absolute;
  bottom: -30px;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  font-size: 0.9rem;
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
  .vote-column {
    min-width: 40px;
  }
  
  .vote-column .fs-4 {
    font-size: 1.25rem !important;
  }
  
  .vote-count {
    font-size: 1rem !important;
  }
  
  .post-title {
    font-size: 1.25rem;
  }
  
  .post-body {
    font-size: 0.95rem;
  }
  
  .carousel-nav {
    width: 32px;
    height: 32px;
  }
  
  .image-modal-prev {
    left: 10px;
  }
  
  .image-modal-next {
    right: 10px;
  }
  
  .comment-avatar {
    width: 32px;
    height: 32px;
  }
  
  .reply-avatar {
    width: 24px;
    height: 24px;
  }
  
  .replies-section {
    padding-left: 12px;
  }
}

/* Extra small devices */
@media (max-width: 576px) {
  .container {
    padding-left: 12px !important;
    padding-right: 12px !important;
  }
  
  .card-body {
    padding: 12px;
  }
  
  .vote-column {
    min-width: 32px;
    margin-right: 8px !important;
  }
  
  .post-actions {
    flex-wrap: wrap;
    gap: 8px !important;
  }
  
  .action-btn {
    font-size: 0.85rem;
  }
  
  .linked-drink-card {
    width: 100%;
  }
  
  .comment-item {
    padding: 12px 0;
  }
  
  .comment-actions {
    flex-wrap: wrap;
  }
  
  .reply-input {
    padding: 10px;
  }
}
</style>
