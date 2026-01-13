<template>
  <NavBar />
  
  <!-- Hero Banner -->
  <div class="hero-banner" :style="heroBannerStyle">
    <div class="hero-overlay">
      <div class="container">
        <div class="hero-content py-4">
          <div class="text-start">
          <button class="btn btn-sm btn-light mb-3" @click="goBack">
            <i class="bi bi-arrow-left me-1"></i> Back to Assemblies
          </button>
          </div>
          <h1 class="hero-title fw-bold text-white mb-2">{{ assemblyInfo.assemblyName || 'Loading...' }}</h1>
          <p class="hero-desc text-white-50 mb-3">{{ assemblyInfo.assemblyDesc || '' }}</p>
          
          <!-- Drink Type Tags -->
          <div v-if="assemblyInfo.drinkTypes && assemblyInfo.drinkTypes.length > 0" class="drink-tags mb-3">
            <span 
              v-for="drinkType in assemblyInfo.drinkTypes" 
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
              {{ assemblyInfo.totalMembers || 0 }} Members
            </span>
            <span class="text-white-50">
              <i class="bi bi-chat-square-text-fill me-1"></i>
              {{ assemblyInfo.totalPosts || 0 }} Posts
            </span>
            <span class="text-white-50">
              <i class="bi bi-calendar me-1"></i>
              Created {{ formatDate(assemblyInfo.dateCreated) }}
            </span>
            
            <!-- Join/Leave Button -->
            <button
              v-if="!isMember && userID !== 'defaultUser'"
              class="btn btn-warning fw-bold ms-auto"
              @click="joinAssembly"
              :disabled="joining"
            >
              <span v-if="joining"><i class="bi bi-hourglass-split me-1"></i> Joining...</span>
              <span v-else><i class="bi bi-plus-circle me-1"></i> Join Assembly</span>
            </button>
            <div v-else-if="isMember" class="btn-group ms-auto">
              <button class="btn btn-success fw-bold" disabled>
                <i class="bi bi-check-circle-fill me-1"></i> Joined
              </button>
              <button 
                class="btn btn-outline-light" 
                @click="showLeaveConfirmModal"
                title="Leave Assembly"
              >
                <i class="bi bi-box-arrow-right"></i>
              </button>
            </div>
            <button
              v-else
              class="btn btn-warning fw-bold ms-auto"
              @click="$router.push('/login')"
            >
              Login to Join
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="container px-4 mt-4">
    <div class="row">
      <!-- Main Content Column -->
      <div class="col-lg-8">
        <!-- Create Post Card (for members) -->
        <div v-if="isMember" class="card mb-4 shadow-sm create-post-card">
          <div class="card-body d-flex align-items-center gap-3">
            <img 
              :src="currentUserPhoto || defaultProfilePhoto" 
              alt="Your avatar"
              class="rounded-circle"
              style="width: 40px; height: 40px; object-fit: cover;"
            />
            <input 
              type="text" 
              class="form-control" 
              placeholder="Create a post..."
              @click="openCreatePostModal"
              readonly
              style="cursor: pointer;"
            />
            <button class="btn btn-outline-secondary" @click="openCreatePostModal">
              <i class="bi bi-image"></i>
            </button>
          </div>
        </div>

        <!-- Sorting Options -->
        <div class="d-flex align-items-center gap-2 mb-3">
          <span class="text-muted small">Sort by:</span>
          <button 
            class="btn btn-sm"
            :class="sortBy === 'newest' ? 'btn-dark' : 'btn-outline-secondary'"
            @click="sortBy = 'newest'"
          >
            <i class="bi bi-clock me-1"></i> Newest
          </button>
          <button 
            class="btn btn-sm"
            :class="sortBy === 'top' ? 'btn-dark' : 'btn-outline-secondary'"
            @click="sortBy = 'top'"
          >
            <i class="bi bi-fire me-1"></i> Top
          </button>
        </div>

        <!-- Posts Feed -->
        <div class="posts-feed">
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3 text-muted">Loading posts...</p>
          </div>

          <!-- Posts List -->
          <div v-else>
            <!-- Post Cards -->
            <div 
              v-for="post in posts" 
              :key="post.id"
              class="post-card card mb-3 shadow-sm"
              :class="{ 'border-warning': post.isPinned }"
              @click="viewPost(post)"
              style="cursor: pointer;"
            >
              <!-- Pinned Badge -->
              <div v-if="post.isPinned" class="pinned-badge">
                <i class="bi bi-pin-fill text-warning me-1"></i>
                <span class="text-warning small fw-bold">Pinned</span>
              </div>
              
              <div class="card-body">
                <div class="d-flex">
                  <!-- Vote Column -->
                  <div class="vote-column d-flex flex-column align-items-center me-3">
                    <button 
                      class="btn btn-sm p-0 vote-btn"
                      @click.stop="votePost(post, 'up')"
                      :disabled="!isMember"
                      :title="!isMember ? 'Join to vote' : 'Upvote'"
                    >
                      <i class="bi bi-arrow-up-circle-fill" :class="{ 'text-primary': post.userVote === 'up' }"></i>
                    </button>
                    <span class="vote-count fw-bold my-1" :class="getVoteCountClass(post.voteCount)">
                      {{ post.voteCount || 0 }}
                    </span>
                    <button 
                      class="btn btn-sm p-0 vote-btn"
                      @click.stop="votePost(post, 'down')"
                      :disabled="!isMember"
                      :title="!isMember ? 'Join to vote' : 'Downvote'"
                    >
                      <i class="bi bi-arrow-down-circle-fill" :class="{ 'text-danger': post.userVote === 'down' }"></i>
                    </button>
                  </div>

                  <!-- Post Content -->
                  <div class="post-content flex-grow-1">
                    <!-- Post Meta -->
                    <div class="text-start post-meta text-muted small mb-2">
                      <span>Posted by </span>
                      <a 
                        href="#" 
                        @click.stop.prevent="goToUserProfile(post.posterInfo)" 
                        class="text-decoration-none fw-bold"
                      >
                        {{ getPosterDisplayName(post.posterInfo) }}
                      </a>
                      <span class="mx-1">•</span>
                      <span>{{ formatTimeAgo(post.postDate) }}</span>
                    </div>

                    <!-- Post Title -->
                    <h5 class="text-start post-title fw-bold mb-2">{{ post.postTitle }}</h5>

                    <!-- Post Content Preview (truncated) -->
                    <p v-if="post.postContentPreview" class="text-start post-preview text-muted mb-2">
                      {{ stripHtml(post.postContentPreview) }}
                    </p>

                    <!-- Linked Listings -->
                    <div v-if="post.linkedListings && post.linkedListings.length > 0" class="linked-listings mb-2">
                      <div class="d-flex gap-2 flex-wrap">
                        <span 
                          v-for="listing in post.linkedListings" 
                          :key="listing.id"
                          class="badge bg-light text-dark border d-flex align-items-center"
                          @click.stop="goToListing(listing.id)"
                          style="cursor: pointer;"
                        >
                          <img 
                            v-if="listing.photo" 
                            :src="listing.photo" 
                            class="me-1 rounded"
                            style="width: 16px; height: 16px; object-fit: cover;"
                          />
                          <i v-else class="bi bi-cup-straw me-1"></i>
                          {{ truncateText(listing.listingName, 20) }}
                        </span>
                      </div>
                    </div>

                    <!-- Post Image Preview (if exists) -->
                    <div v-if="post.postPhotos && post.postPhotos.length > 0" class="post-image-preview mb-2">
                      <img 
                        :src="post.postPhotos[0]" 
                        :alt="post.postTitle"
                        class="img-fluid rounded"
                        style="max-height: 300px; object-fit: cover;"
                      />
                      <span v-if="post.postPhotos.length > 1" class="badge bg-dark ms-2">
                        +{{ post.postPhotos.length - 1 }} more
                      </span>
                    </div>

                    <!-- Post Actions -->
                    <div class="post-actions d-flex align-items-center gap-3 mt-2">
                      <span class="action-btn text-muted" @click.stop="viewPost(post)">
                        <i class="bi bi-chat-square me-1"></i>
                        {{ post.commentCount || 0 }} Comments
                      </span>
                      <span class="action-btn text-muted" @click.stop="sharePost(post)">
                        <i class="bi bi-share me-1"></i>
                        Share
                      </span>
                      <!-- Admin Actions -->
                      <div v-if="isAdmin" class="dropdown ms-auto" @click.stop>
                        <button class="btn btn-sm btn-link text-muted" data-bs-toggle="dropdown">
                          <i class="bi bi-three-dots"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end">
                          <li>
                            <a class="dropdown-item" href="#" @click.prevent="togglePinPost(post)">
                              <i class="bi" :class="post.isPinned ? 'bi-pin-angle' : 'bi-pin-fill'"></i>
                              {{ post.isPinned ? 'Unpin Post' : 'Pin Post' }}
                            </a>
                          </li>
                          <li>
                            <a class="dropdown-item text-danger" href="#" @click.prevent="confirmDeletePost(post)">
                              <i class="bi bi-trash"></i> Delete Post
                            </a>
                          </li>
                        </ul>
                      </div>
                    </div>

                    <!-- Top Comments Preview -->
                    <div v-if="post.commentsPreview && post.commentsPreview.length > 0" class="comments-preview mt-3 pt-3 border-top">
                      <div 
                        v-for="comment in post.commentsPreview" 
                        :key="comment.id"
                        class="comment-preview d-flex align-items-start gap-2 mb-2"
                        @click.stop
                      >
                        <i class="bi bi-chat-left-text text-muted small"></i>
                        <div class="small">
                          <span class="fw-bold">{{ getPosterDisplayName(comment.commenterInfo) }}:</span>
                          <span class="text-muted ms-1">{{ comment.commentContent }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="posts.length === 0" class="text-center py-5">
              <i class="bi bi-chat-square-text text-muted" style="font-size: 4rem;"></i>
              <h4 class="text-muted mt-3">No posts yet</h4>
              <p class="text-muted">{{ isMember ? 'Be the first to start a discussion!' : 'Join this assembly to create the first post!' }}</p>
            </div>

            <!-- Load More Button -->
            <div v-if="hasMorePosts && posts.length > 0" class="text-center mt-4 mb-5">
              <button 
                class="btn btn-outline-primary" 
                @click="loadMorePosts"
                :disabled="loadingMore"
              >
                <span v-if="loadingMore">
                  <span class="spinner-border spinner-border-sm me-1"></span>
                  Loading...
                </span>
                <span v-else>Load More Posts</span>
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
            <h6 class="mb-0 fw-bold">About Community</h6>
          </div>
          <div class="card-body">
            <p class="small text-muted mb-3">{{ assemblyInfo.assemblyDesc || 'No description available.' }}</p>
            
            <!-- Creator Info -->
            <div v-if="assemblyInfo.creatorUsername" class="mb-3">
              <span class="small text-muted">Created by </span>
              <a 
                :href="getCreatorProfileUrl()" 
                class="text-decoration-none small fw-bold"
                @click.prevent="goToCreatorProfile"
              >
                {{ assemblyInfo.creatorUsername }}
              </a>
            </div>
            
            <!-- Stats -->
            <div class="d-flex justify-content-around text-center py-2 border-top border-bottom">
              <div>
                <div class="fw-bold">{{ assemblyInfo.totalMembers || 0 }}</div>
                <div class="small text-muted">Members</div>
              </div>
              <div>
                <div class="fw-bold">{{ assemblyInfo.totalPosts || 0 }}</div>
                <div class="small text-muted">Posts</div>
              </div>
            </div>
            
            <!-- Create Post Button -->
            <button 
              v-if="isMember"
              class="btn btn-warning w-100 mt-3 fw-bold"
              @click="openCreatePostModal"
            >
              Create Post
            </button>
            <button 
              v-else-if="userID !== 'defaultUser'"
              class="btn btn-outline-warning w-100 mt-3 fw-bold"
              @click="joinAssembly"
              :disabled="joining"
            >
              Join to Post
            </button>
          </div>
        </div>

        <!-- Members Preview Card -->
        <div class="card shadow-sm mb-4">
          <div class="card-header bg-light d-flex justify-content-between align-items-center">
            <h6 class="mb-0 fw-bold">Members</h6>
            <button 
              class="btn btn-sm btn-link p-0" 
              data-bs-toggle="modal" 
              data-bs-target="#membersModal"
              @click="loadAllMembers"
            >
              View All
            </button>
          </div>
          <div class="card-body">
            <div class="d-flex flex-wrap gap-2">
              <div 
                v-for="member in membersPreview" 
                :key="member.id"
                class="member-preview text-center"
                style="width: 60px;"
              >
                <img 
                  :src="getMemberPhoto(member.userInfo)" 
                  :alt="getMemberDisplayName(member.userInfo)"
                  class="rounded-circle mb-1"
                  style="width: 40px; height: 40px; object-fit: cover; cursor: pointer;"
                  @click="goToUserProfile(member.userInfo)"
                />
                <div class="small text-truncate" style="font-size: 0.7rem;">
                  {{ getMemberDisplayName(member.userInfo) }}
                </div>
                <span v-if="member.isAdmin" class="badge bg-warning text-dark" style="font-size: 0.6rem;">Admin</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Admins Card -->
        <div v-if="assemblyInfo.admins && assemblyInfo.admins.length > 0" class="card shadow-sm mb-4">
          <div class="card-header bg-light">
            <h6 class="mb-0 fw-bold">Moderators</h6>
          </div>
          <div class="card-body">
            <div 
              v-for="admin in assemblyInfo.admins" 
              :key="admin.memberID"
              class="d-flex align-items-center gap-2 mb-2"
            >
              <img 
                :src="getMemberPhoto(admin)" 
                class="rounded-circle"
                style="width: 32px; height: 32px; object-fit: cover;"
              />
              <a 
                href="#" 
                class="text-decoration-none small fw-bold"
                @click.prevent="goToUserProfile(admin)"
              >
                {{ getMemberDisplayName(admin) }}
              </a>
              <i class="bi bi-shield-fill text-success ms-auto" title="Admin"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Create Post Modal -->
  <div class="modal fade" id="createPostModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title fw-bold">Create a Post</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <!-- Post Title -->
          <div class="mb-3">
            <label class="form-label fw-bold">Title <span class="text-danger">*</span></label>
            <input 
              type="text" 
              class="form-control" 
              v-model="newPost.title"
              placeholder="An interesting title..."
              maxlength="500"
            />
            <div class="form-text text-end">{{ newPost.title.length }}/500</div>
          </div>
          
          <!-- Post Content (Rich Text) -->
          <div class="mb-3">
            <label class="form-label fw-bold">Content</label>
            <InlineRichTextEditor
              ref="postEditor"
              :initial-content="newPost.content"
              @content-changed="onPostContentChange"
              :section-id="'new-post'"
            />
          </div>

          <!-- Image Upload -->
          <div class="mb-3">
            <label class="form-label fw-bold">Images (Max 5)</label>
            <div class="d-flex flex-wrap gap-2 mb-2">
              <div 
                v-for="(image, index) in newPost.images" 
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
                v-if="newPost.images.length < 5"
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
            <AutocompleteSearchSelector
              placeholder="Search for drinks to link..."
              :disabled="newPost.selectedDrinks.length >= 5"
              @select="handleDrinkSelect"
            />
            <div class="form-text">Link drinks you're discussing in your post</div>
            
            <!-- Selected Drinks Display -->
            <div v-if="newPost.selectedDrinks.length > 0" class="selected-drinks mt-3">
              <div 
                v-for="drink in newPost.selectedDrinks" 
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
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button 
            type="button" 
            class="btn btn-warning fw-bold" 
            @click="submitPost"
            :disabled="!newPost.title.trim() || submittingPost"
          >
            <span v-if="submittingPost">
              <span class="spinner-border spinner-border-sm me-1"></span>
              Posting...
            </span>
            <span v-else>Post</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Members Modal -->
  <div class="modal fade" id="membersModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title fw-bold">Members</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div v-if="loadingMembers" class="text-center py-4">
            <div class="spinner-border text-primary"></div>
          </div>
          <div v-else>
            <div 
              v-for="member in allMembers" 
              :key="member.id"
              class="d-flex align-items-center gap-3 mb-3 pb-3 border-bottom"
            >
              <img 
                :src="getMemberPhoto(member.userInfo)" 
                class="rounded-circle"
                style="width: 48px; height: 48px; object-fit: cover;"
              />
              <div class="flex-grow-1">
                <a 
                  href="#" 
                  class="text-decoration-none fw-bold d-block"
                  @click.prevent="goToUserProfile(member.userInfo)"
                >
                  {{ getMemberDisplayName(member.userInfo) }}
                </a>
                <span class="small text-muted">Joined {{ formatDate(member.joinDate) }}</span>
              </div>
              <span v-if="member.isAdmin" class="badge bg-warning text-dark">Admin</span>
              <!-- Remove Member (Admin only) -->
              <button 
                v-if="isAdmin && member.userInfo && member.userInfo.id !== parseInt(userID)"
                class="btn btn-sm btn-outline-danger"
                @click="confirmRemoveMember(member)"
                title="Remove member"
              >
                <i class="bi bi-person-x"></i>
              </button>
            </div>
            
            <!-- Load More Members -->
            <div v-if="hasMoreMembers" class="text-center mt-3">
              <button 
                class="btn btn-outline-primary btn-sm"
                @click="loadMoreMembers"
                :disabled="loadingMoreMembers"
              >
                Load More
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Leave Confirmation Modal -->
  <div class="modal fade" id="leaveConfirmModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Leave Assembly</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to leave <strong>{{ assemblyInfo.assemblyName }}</strong>?</p>
          <p class="text-muted small">You can always rejoin later.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button 
            type="button" 
            class="btn btn-danger" 
            @click="leaveAssembly"
            :disabled="leaving"
          >
            {{ leaving ? 'Leaving...' : 'Leave' }}
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Delete Post Confirmation Modal -->
  <div class="modal fade" id="deletePostModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Delete Post</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete this post?</p>
          <p class="text-danger small">This action cannot be undone.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button 
            type="button" 
            class="btn btn-danger" 
            @click="deletePost"
            :disabled="deletingPost"
          >
            {{ deletingPost ? 'Deleting...' : 'Delete' }}
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
import { Modal } from "bootstrap";

export default {
  name: "SpecificAssembly",
  components: {
    NavBar,
    InlineRichTextEditor,
    AutocompleteSearchSelector,
  },
  data() {
    return {
      // Assembly Info
      assemblyInfo: {
        id: null,
        assemblyName: '',
        assemblyDesc: '',
        drinkTypes: [],
        isInviteOnly: false,
        assemblyBanner: null,
        dateCreated: null,
        totalMembers: 0,
        totalPosts: 0,
        createdByID: null,
        createdByType: null,
        creatorUsername: '',
        admins: [],
        membersPreview: [],
      },
      
      // Posts
      posts: [],
      loading: true,
      loadingMore: false,
      hasMorePosts: false,
      currentOffset: 0,
      sortBy: 'newest',
      
      // Members
      membersPreview: [],
      allMembers: [],
      loadingMembers: false,
      loadingMoreMembers: false,
      hasMoreMembers: false,
      membersOffset: 0,
      
      // User State
      userID: "defaultUser",
      userType: null,
      username: null,
      currentUserPhoto: null,
      isMember: false,
      isAdmin: false,
      memberID: null,
      joining: false,
      leaving: false,
      
      // New Post
      newPost: {
        title: '',
        content: '',
        images: [],
        listingIDs: [],
        selectedDrinks: [], // Full drink objects for display
      },
      submittingPost: false,
      
      // Default images
      defaultDrinkPhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",
      
      // Delete post
      postToDelete: null,
      deletingPost: false,

      // Default images
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
      defaultBanner: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultAssemblyBanner.png?v=1736697600",
    };
  },
  computed: {
    assemblyId() {
      return this.$route.params.assemblyId;
    },
    assemblyName() {
      return this.$route.params.assemblyName;
    },
    heroBannerStyle() {
      const bannerUrl = this.assemblyInfo.assemblyBanner || this.defaultBanner;
      return {
        backgroundImage: `url(${bannerUrl})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      };
    },
  },
  watch: {
    sortBy() {
      // Reset offset and reload posts when sort changes
      this.currentOffset = 0;
      this.loadPosts();
    }
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
    
    // Load assembly data
    this.loadAssemblyData();
    
    // Restore draft from localStorage
    this.restoreDraft();
  },
  beforeUnmount() {
    // Save draft to localStorage
    this.saveDraft();
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },

    async loadAssemblyData() {
      this.loading = true;
      
      try {
        // Build query params for user context
        let queryParams = '';
        if (this.userID !== 'defaultUser') {
          queryParams = `?userID=${this.userID}&userType=${this.userType}`;
        }
        
        // Fetch assembly info
        const infoResponse = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/assembly/getSpecificAssemblyInfo/${this.assemblyId}${queryParams}`
        );
        
        if (infoResponse.data.code === 200) {
          const data = infoResponse.data.data;
          this.assemblyInfo = {
            id: data.id,
            assemblyName: data.assemblyName,
            assemblyDesc: data.assemblyDesc,
            drinkTypes: data.drinkTypes || [],
            isInviteOnly: data.isInviteOnly,
            assemblyBanner: data.assemblyBanner,
            dateCreated: data.dateCreated,
            totalMembers: data.totalMembers || 0,
            totalPosts: data.totalPosts || 0,
            createdByID: data.createdByID,
            createdByType: data.createdByType,
            creatorUsername: data.creatorUsername || data.producerName || data.venueName || 'Unknown',
            admins: data.admins || [],
            membersPreview: data.membersPreview || [],
          };
          
          // Set membership status
          this.isMember = data.isMember || false;
          this.memberID = data.memberID || null;
          this.isAdmin = data.isAdmin || false;
          
          // Set members preview
          this.membersPreview = data.membersPreview || [];
        }
        
        // Load posts
        await this.loadPosts();
        
      } catch (error) {
        console.error('Error loading assembly data:', error);
        const toast = useToast();
        toast.error('Failed to load assembly data.');
      } finally {
        this.loading = false;
      }
    },

    async loadPosts() {
      try {
        let queryParams = '';
        if (this.userID !== 'defaultUser') {
          queryParams = `?userID=${this.userID}&userType=${this.userType}`;
        } else {
          queryParams = '?';
        }
        
        // Add sortBy parameter
        queryParams += `${queryParams === '?' ? '' : '&'}sortBy=${this.sortBy}`;
        
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/assembly/getAssemblyPosts/${this.assemblyId}/${this.currentOffset}${queryParams}`
        );
        
        if (response.data.code === 200) {
          this.posts = response.data.data || [];
          this.hasMorePosts = this.posts.length === 25;
        }
      } catch (error) {
        console.error('Error loading posts:', error);
      }
    },

    async loadMorePosts() {
      if (this.loadingMore) return;
      
      this.loadingMore = true;
      this.currentOffset += 25;
      
      try {
        let queryParams = '';
        if (this.userID !== 'defaultUser') {
          queryParams = `?userID=${this.userID}&userType=${this.userType}`;
        } else {
          queryParams = '?';
        }
        
        // Add sortBy parameter
        queryParams += `${queryParams === '?' ? '' : '&'}sortBy=${this.sortBy}`;
        
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/assembly/getAssemblyPosts/${this.assemblyId}/${this.currentOffset}${queryParams}`
        );
        
        if (response.data.code === 200) {
          const newPosts = response.data.data || [];
          this.posts = [...this.posts, ...newPosts];
          this.hasMorePosts = newPosts.length === 25;
        }
      } catch (error) {
        console.error('Error loading more posts:', error);
      } finally {
        this.loadingMore = false;
      }
    },

    async loadAllMembers() {
      if (this.allMembers.length > 0) return;
      
      this.loadingMembers = true;
      this.membersOffset = 0;
      
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/assembly/getAssemblyMembers/${this.assemblyId}/${this.membersOffset}`
        );
        
        if (response.data.code === 200) {
          this.allMembers = response.data.data || [];
          this.hasMoreMembers = this.allMembers.length === 20;
        }
      } catch (error) {
        console.error('Error loading members:', error);
      } finally {
        this.loadingMembers = false;
      }
    },

    async loadMoreMembers() {
      if (this.loadingMoreMembers) return;
      
      this.loadingMoreMembers = true;
      this.membersOffset += 20;
      
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/assembly/getAssemblyMembers/${this.assemblyId}/${this.membersOffset}`
        );
        
        if (response.data.code === 200) {
          const newMembers = response.data.data || [];
          this.allMembers = [...this.allMembers, ...newMembers];
          this.hasMoreMembers = newMembers.length === 20;
        }
      } catch (error) {
        console.error('Error loading more members:', error);
      } finally {
        this.loadingMoreMembers = false;
      }
    },

    async joinAssembly() {
      if (this.userID === 'defaultUser') {
        this.$router.push('/login');
        return;
      }
      
      this.joining = true;
      const toast = useToast();
      
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/assembly/joinAssembly`,
          {
            assemblyID: this.assemblyId,
            userID: this.userID,
            userType: this.userType,
          }
        );
        
        if (response.data.code === 201) {
          this.isMember = true;
          this.memberID = response.data.data.memberID;
          this.assemblyInfo.totalMembers++;
          toast.success('Successfully joined the assembly!');
        } else {
          toast.error(response.data.message || 'Failed to join assembly.');
        }
      } catch (error) {
        console.error('Error joining assembly:', error);
        toast.error('An error occurred while joining.');
      } finally {
        this.joining = false;
      }
    },

    showLeaveConfirmModal() {
      const modal = new Modal(document.getElementById('leaveConfirmModal'));
      modal.show();
    },

    async leaveAssembly() {
      this.leaving = true;
      const toast = useToast();
      
      try {
        const response = await this.$axios.delete(
          `${process.env.VUE_APP_API_URL}/assembly/leaveAssembly`,
          {
            data: {
              assemblyID: this.assemblyId,
              userID: this.userID,
              userType: this.userType,
            }
          }
        );
        
        if (response.data.code === 200) {
          this.isMember = false;
          this.memberID = null;
          this.isAdmin = false;
          this.assemblyInfo.totalMembers--;
          toast.success('You have left the assembly.');
          
          // Close modal
          const modal = Modal.getInstance(document.getElementById('leaveConfirmModal'));
          if (modal) modal.hide();
        } else {
          toast.error(response.data.message || 'Failed to leave assembly.');
        }
      } catch (error) {
        console.error('Error leaving assembly:', error);
        const errorMsg = error.response?.data?.message || 'An error occurred.';
        toast.error(errorMsg);
      } finally {
        this.leaving = false;
      }
    },

    openCreatePostModal() {
      const modal = new Modal(document.getElementById('createPostModal'));
      modal.show();
    },

    onPostContentChange(content) {
      this.newPost.content = content;
    },

    // Drink selection methods
    handleDrinkSelect(drink) {
      const toast = useToast();
      
      // Check if already at max
      if (this.newPost.selectedDrinks.length >= 5) {
        toast.warning('Maximum 5 drinks allowed');
        return;
      }
      
      // Check if already added
      if (this.newPost.selectedDrinks.some(d => d.id === drink.id)) {
        toast.info('This drink is already added');
        return;
      }
      
      // Add drink to selectedDrinks (full object for display) and listingIDs
      this.newPost.selectedDrinks.push(drink);
      this.newPost.listingIDs.push(drink.id);
    },

    removeDrink(drinkId) {
      this.newPost.selectedDrinks = this.newPost.selectedDrinks.filter(d => d.id !== drinkId);
      this.newPost.listingIDs = this.newPost.listingIDs.filter(id => id !== drinkId);
    },

    handleImageUpload(event) {
      const files = event.target.files;
      const remainingSlots = 5 - this.newPost.images.length;
      
      for (let i = 0; i < Math.min(files.length, remainingSlots); i++) {
        const file = files[i];
        const reader = new FileReader();
        
        reader.onload = (e) => {
          this.newPost.images.push({
            file: file,
            preview: e.target.result,
            base64: e.target.result,
          });
        };
        
        reader.readAsDataURL(file);
      }
      
      // Reset input
      event.target.value = '';
    },

    removeImage(index) {
      this.newPost.images.splice(index, 1);
    },

    async submitPost() {
      if (!this.newPost.title.trim()) {
        const toast = useToast();
        toast.warning('Please enter a title for your post.');
        return;
      }
      
      this.submittingPost = true;
      const toast = useToast();
      
      try {
        const images = this.newPost.images.map(img => img.base64);
        
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/assembly/createAssemblyPost`,
          {
            assemblyID: this.assemblyId,
            memberID: this.memberID,
            postTitle: this.newPost.title.trim(),
            postContent: this.newPost.content,
            images: images,
            listingIDs: this.newPost.listingIDs,
          }
        );
        
        if (response.data.code === 201) {
          toast.success('Post created successfully!');
          
          // Clear form
          this.newPost = {
            title: '',
            content: '',
            images: [],
            listingIDs: [],
            selectedDrinks: [],
          };
          
          // Clear draft
          this.clearDraft();
          
          // Close modal
          const modal = Modal.getInstance(document.getElementById('createPostModal'));
          if (modal) modal.hide();
          
          // Reload posts
          this.currentOffset = 0;
          await this.loadPosts();
          
          // Update post count
          this.assemblyInfo.totalPosts++;
        } else {
          toast.error(response.data.message || 'Failed to create post.');
        }
      } catch (error) {
        console.error('Error creating post:', error);
        toast.error('An error occurred while creating the post.');
      } finally {
        this.submittingPost = false;
      }
    },

    async votePost(post, voteType) {
      if (!this.isMember) {
        const toast = useToast();
        toast.warning('Join this assembly to vote on posts.');
        return;
      }
      
      // Determine the new vote type
      // If clicking the same vote type, remove the vote
      // If clicking different vote type, switch to that
      let newVoteType = voteType;
      if (post.userVote === voteType) {
        newVoteType = 'none';
      }
      
      try {
        const response = await this.$axios.put(
          `${process.env.VUE_APP_API_URL}/assembly/voteAssemblyPost`,
          {
            assemblyID: this.assemblyId,
            postID: post.id,
            memberID: this.memberID,
            voteType: newVoteType,
          }
        );
        
        if (response.data.code === 200) {
          // Update local state
          post.voteCount = response.data.data.voteCount;
          post.userVote = response.data.data.userVote;
        }
      } catch (error) {
        console.error('Error voting on post:', error);
      }
    },

    async togglePinPost(post) {
      const toast = useToast();
      
      try {
        const response = await this.$axios.put(
          `${process.env.VUE_APP_API_URL}/assembly/pinAssemblyPost`,
          {
            postID: post.id,
            memberID: this.memberID,
            isPinned: !post.isPinned,
          }
        );
        
        if (response.data.code === 200) {
          post.isPinned = !post.isPinned;
          toast.success(post.isPinned ? 'Post pinned!' : 'Post unpinned!');
        } else {
          toast.error(response.data.message || 'Failed to update pin status.');
        }
      } catch (error) {
        console.error('Error toggling pin:', error);
        toast.error('An error occurred.');
      }
    },

    confirmDeletePost(post) {
      this.postToDelete = post;
      const modal = new Modal(document.getElementById('deletePostModal'));
      modal.show();
    },

    async deletePost() {
      if (!this.postToDelete) return;
      
      this.deletingPost = true;
      const toast = useToast();
      
      try {
        const response = await this.$axios.delete(
          `${process.env.VUE_APP_API_URL}/assembly/deleteAssemblyPost`,
          {
            data: {
              postID: this.postToDelete.id,
              memberID: this.memberID,
            }
          }
        );
        
        if (response.data.code === 200) {
          // Remove from local array
          this.posts = this.posts.filter(p => p.id !== this.postToDelete.id);
          this.assemblyInfo.totalPosts--;
          toast.success('Post deleted successfully.');
          
          // Close modal
          const modal = Modal.getInstance(document.getElementById('deletePostModal'));
          if (modal) modal.hide();
          
          this.postToDelete = null;
        } else {
          toast.error(response.data.message || 'Failed to delete post.');
        }
      } catch (error) {
        console.error('Error deleting post:', error);
        toast.error('An error occurred.');
      } finally {
        this.deletingPost = false;
      }
    },

    confirmRemoveMember(member) {
      const toast = useToast();
      if (confirm(`Are you sure you want to remove ${this.getMemberDisplayName(member.userInfo)} from this assembly?`)) {
        this.removeMember(member);
      } else {
        toast.info('Removal cancelled.');
      }
    },

    async removeMember(member) {
      const toast = useToast();
      
      try {
        const response = await this.$axios.delete(
          `${process.env.VUE_APP_API_URL}/assembly/removeAssemblyMember`,
          {
            data: {
              assemblyID: this.assemblyId,
              adminMemberID: this.memberID,
              targetMemberID: member.id,
            }
          }
        );
        
        if (response.data.code === 200) {
          // Remove from local arrays
          this.allMembers = this.allMembers.filter(m => m.id !== member.id);
          this.membersPreview = this.membersPreview.filter(m => m.id !== member.id);
          this.assemblyInfo.totalMembers--;
          toast.success('Member removed.');
        } else {
          toast.error(response.data.message || 'Failed to remove member.');
        }
      } catch (error) {
        console.error('Error removing member:', error);
        toast.error('An error occurred.');
      }
    },

    viewPost(post) {
      const postTitle = this.normalizeForUrl(post.postTitle || 'post');
      this.$router.push({
        name: 'specificAssemblyPost',
        params: {
          assemblyId: this.assemblyId,
          assemblyName: this.assemblyName,
          postId: post.id,
          postTitle: postTitle
        }
      });
    },

    goToUserProfile(userInfo) {
      if (!userInfo) return;
      
      if (userInfo.userType === 'user' || !userInfo.userType) {
        const username = userInfo.username || userInfo.displayName || 'user';
        this.$router.push(`/profile/user/${userInfo.id}/${username}`);
      } else if (userInfo.userType === 'producer') {
        this.$router.push(`/profile/producer/${userInfo.id}`);
      } else if (userInfo.userType === 'venue') {
        this.$router.push(`/profile/venue/${userInfo.id}`);
      }
    },

    goToCreatorProfile() {
      const creatorInfo = {
        id: this.assemblyInfo.createdByID,
        userType: this.assemblyInfo.createdByType,
        username: this.assemblyInfo.creatorUsername,
      };
      this.goToUserProfile(creatorInfo);
    },

    getCreatorProfileUrl() {
      if (this.assemblyInfo.createdByType === 'user') {
        return `/profile/user/${this.assemblyInfo.createdByID}/${this.assemblyInfo.creatorUsername}`;
      } else if (this.assemblyInfo.createdByType === 'producer') {
        return `/profile/producer/${this.assemblyInfo.createdByID}`;
      } else if (this.assemblyInfo.createdByType === 'venue') {
        return `/profile/venue/${this.assemblyInfo.createdByID}`;
      }
      return '#';
    },

    goToListing(listingId) {
      this.$router.push(`/listing/${listingId}`);
    },

    sharePost(post) {
      const postTitle = this.normalizeForUrl(post.postTitle || 'post');
      const shareUrl = `${window.location.origin}/assemblies/${this.assemblyId}/${this.assemblyName}/assembly-post/${post.id}/${postTitle}`;
      
      navigator.clipboard.writeText(shareUrl).then(() => {
        const toast = useToast();
        toast.success('Post link copied to clipboard!');
      }).catch((err) => {
        console.error('Failed to copy text: ', err);
        const toast = useToast();
        toast.error('Failed to copy link.');
      });
    },

    // Draft management
    saveDraft() {
      if (this.newPost.title || this.newPost.content) {
        const draft = {
          assemblyId: this.assemblyId,
          title: this.newPost.title,
          content: this.newPost.content,
          timestamp: Date.now(),
        };
        localStorage.setItem('88B_assemblyPostDraft', JSON.stringify(draft));
      }
    },

    restoreDraft() {
      const draftStr = localStorage.getItem('88B_assemblyPostDraft');
      if (draftStr) {
        try {
          const draft = JSON.parse(draftStr);
          // Only restore if it's for this assembly and less than 24 hours old
          if (draft.assemblyId === this.assemblyId && (Date.now() - draft.timestamp) < 86400000) {
            this.newPost.title = draft.title || '';
            this.newPost.content = draft.content || '';
          }
        } catch (e) {
          console.error('Error restoring draft:', e);
        }
      }
    },

    clearDraft() {
      localStorage.removeItem('88B_assemblyPostDraft');
    },

    // Helper methods
    getPosterDisplayName(posterInfo) {
      if (!posterInfo) return 'Unknown';
      return posterInfo.username || posterInfo.displayName || posterInfo.producerName || posterInfo.venueName || 'Unknown';
    },

    getMemberDisplayName(userInfo) {
      if (!userInfo) return 'Unknown';
      return userInfo.username || userInfo.displayName || userInfo.producerName || userInfo.venueName || 'Member';
    },

    getMemberPhoto(userInfo) {
      if (!userInfo) return this.defaultProfilePhoto;
      return userInfo.photo || userInfo.profilePhoto || this.defaultProfilePhoto;
    },

    getVoteCountClass(voteCount) {
      if (voteCount > 0) return 'text-primary';
      if (voteCount < 0) return 'text-danger';
      return 'text-muted';
    },

    stripHtml(html) {
      if (!html) return '';
      const tmp = document.createElement('DIV');
      tmp.innerHTML = html;
      return tmp.textContent || tmp.innerText || '';
    },

    truncateText(text, maxLength) {
      if (!text) return '';
      if (text.length <= maxLength) return text;
      return text.substring(0, maxLength) + '...';
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

    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    normalizeForUrl(text) {
      return text
        .replace(/[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F1E0}-\u{1F1FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]|[\u{1F900}-\u{1F9FF}]|[\u{1F018}-\u{1F270}]/gu, '')
        .trim()
        .replace(/\s+/g, ' ')
        .replace(/\s/g, '-')
        .replace(/[^\w-]/g, '')
        .replace(/-+/g, '-')
        .replace(/^-|-$/g, '')
        .toLowerCase();
    },
  },
};
</script>

<style scoped>
/* Hero Banner */
.hero-banner {
  min-height: 200px;
  position: relative;
}

.hero-overlay {
  background: linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.7));
  min-height: 200px;
}

.hero-title {
  font-size: 2rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}


.drink-tags .badge {
  font-size: 0.75rem;
}

/* Create Post Card */
.create-post-card {
  border: 1px solid #dee2e6;
}

.create-post-card input:focus {
  box-shadow: none;
  border-color: #ffc107;
}

/* Post Card Styles */
.post-card {
  transition: box-shadow 0.2s ease-in-out, border-color 0.2s ease-in-out;
  border: 1px solid #dee2e6;
  position: relative;
}

.post-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
  border-color: #adb5bd;
}

.post-card.border-warning {
  border-width: 2px;
}

.pinned-badge {
  position: absolute;
  top: 8px;
  right: 12px;
  display: flex;
  align-items: center;
}

/* Vote Column */
.vote-column {
  min-width: 40px;
}

.vote-btn {
  color: #adb5bd;
  transition: color 0.15s ease-in-out;
  font-size: 1.25rem;
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

.vote-count {
  font-size: 0.9rem;
}

/* Post Content */
.post-title {
  color: #212529;
  transition: color 0.15s ease-in-out;
}

.post-card:hover .post-title {
  color: #0d6efd;
}

.post-preview {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.post-meta a {
  color: #0d6efd;
}

.post-meta a:hover {
  text-decoration: underline !important;
}

/* Linked Listings */
.linked-listings .badge {
  transition: background-color 0.15s ease-in-out;
}

.linked-listings .badge:hover {
  background-color: #e9ecef !important;
}

/* Comments Preview */
.comments-preview {
  background-color: #f8f9fa;
  margin: 0 -1rem -1rem -1rem;
  padding: 0.75rem 1rem;
  border-radius: 0 0 0.375rem 0.375rem;
}

.comment-preview {
  font-size: 0.85rem;
}

/* Post Actions */
.action-btn {
  cursor: pointer;
  transition: color 0.15s ease-in-out;
  font-size: 0.85rem;
}

.action-btn:hover {
  color: #495057 !important;
}

/* Sidebar Cards */
.card-header {
  font-size: 0.9rem;
}

.member-preview img {
  transition: transform 0.15s ease-in-out;
}

.member-preview img:hover {
  transform: scale(1.1);
}

/* Upload Placeholder */
.upload-placeholder {
  border-style: dashed !important;
  transition: border-color 0.15s ease-in-out, background-color 0.15s ease-in-out;
}

.upload-placeholder:hover {
  border-color: #ffc107 !important;
  background-color: #fffbea;
}

/* Modal Overrides */
.modal-content {
  border-radius: 0.5rem;
}

/* Mobile Responsiveness */
@media (max-width: 992px) {
  .hero-title {
    font-size: 1.5rem;
  }
  
  .hero-desc {
    font-size: 0.9rem;
  }
}

@media (max-width: 768px) {
  .hero-banner {
    min-height: 180px;
  }
  
  .hero-overlay {
    min-height: 180px;
  }
  
  .vote-column {
    min-width: 32px;
  }
  
  .vote-btn {
    font-size: 1rem;
  }
  
  .vote-count {
    font-size: 0.8rem;
  }
  
  .post-title {
    font-size: 1rem;
  }
  
  .post-preview {
    font-size: 0.9rem;
    -webkit-line-clamp: 2;
  }
  
  .post-image-preview img {
    max-height: 200px;
  }
  
  .post-actions {
    font-size: 0.8rem;
  }
  
  .post-meta {
    font-size: 0.75rem;
  }
  
  .comments-preview {
    display: none;
  }
}

/* Extra small devices */
@media (max-width: 576px) {
  .container {
    padding-left: 12px !important;
    padding-right: 12px !important;
  }
  
  .post-card .card-body {
    padding: 12px;
  }
  
  .vote-column {
    min-width: 28px;
    margin-right: 8px !important;
  }
  
  .hero-content {
    padding-left: 12px;
    padding-right: 12px;
  }
  
  .drink-tags .badge {
    font-size: 0.65rem;
  }
}

/* Selected Drinks Cards */
.selected-drinks {
  max-height: 250px;
  overflow-y: auto;
}

.selected-drink-card {
  transition: background-color 0.15s ease;
}

.selected-drink-card:hover {
  background-color: #e9ecef !important;
}

.selected-drink-card .btn-outline-danger {
  opacity: 0.7;
  transition: opacity 0.15s ease;
}

.selected-drink-card:hover .btn-outline-danger {
  opacity: 1;
}

@media (max-width: 576px) {
  .selected-drink-card img {
    width: 40px !important;
    height: 40px !important;
  }
  
  .selected-drink-card .fw-bold {
    font-size: 0.9rem;
  }
  
  .selected-drink-card .small {
    font-size: 0.75rem;
  }
}
</style>
