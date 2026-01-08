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

  <!-- Loading -->
  <LoadingWithFunFact v-if="dataLoaded === false" />

  <!-- Error -->
  <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="dataLoaded == null">
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
  <div v-if="dataLoaded" class="userprofile mt-3 mobile-mt-3">
    <div class="container text-start">
      <div class="row mobile-px-3">
        <div class="col-12 col-md-10 mx-auto mobile-px-3">

          <!-- Page Header -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h4 class="fw-bold mb-0">Personal Wall</h4>
            <router-link 
              :to="`/profile/user/${displayUserID}/${routeUsername}`"
              class="small text-muted text-decoration-underline" 
              style="background-color: transparent; border: none;"
            >
              <i class="bi bi-arrow-left me-2"></i> Back To Profile Page
            </router-link>
          </div>

          <!-- Write Post Section (for logged-in users who are not venues/producers) -->
          <div v-if="canPost" class="mb-4">
            <div 
              class="d-flex align-items-center gap-3 p-3"
              style="
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: #ffffff;
              "
            >
              <img 
                :src="currentUserPhoto || defaultProfilePhoto" 
                alt="Profile" 
                class="rounded-circle"
                style="width: 40px; height: 40px; object-fit: cover;"
              />
              <input 
                type="text" 
                class="form-control"
                :placeholder="writePostPlaceholder"
                style="border-radius: 20px; background-color: #f0f2f5;"
                readonly
                @click="openAddPostModal"
              />
              <button 
                class="btn fw-bold primary-btn-green"
                style="white-space: nowrap;"
                @click="openAddPostModal"
              >
                + Write Post
              </button>
            </div>
          </div>

          <!-- Posts Section -->
          <div v-if="posts.length === 0" class="text-center mt-1">
            <div 
              class="text-center py-5"
              style="
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: #ffffff;
              "
            >
              <i class="bi bi-chat-square-text" style="font-size: 4rem; color: #6c757d;"></i>
              <h5 class="mt-3 text-muted">
                {{ ownProfile ? "There are no posts on your wall yet." : `There are no posts on ${displayUser.displayName}'s wall yet.` }}
              </h5>
              <p v-if="canPost" class="text-muted">
                Be the first to post something!
              </p>
            </div>
          </div>

          <!-- Each Post -->
          <div v-else class="text-center mt-1  px-3">
            <div
              v-for="post in posts"
              :key="post.id"
              class="row mb-4 justify-content-center"
              style="
                background-color: white;
                border-radius: 5px;
                padding: 20px;
                border: 1px solid #e0e0e0;
              "
            >
              <!-- Column 1: Poster Photo -->
              <div class="row mb-2 mx-0 px-0 justify-content-center">
                <div class="col-1 mobile-col-2 d-flex flex-column justify-content-center align-items-center">
                  <!-- <router-link :to="`/profile/user/${post.posterInfo.id}/${post.posterInfo.username}`">
                    <p class="fw-bold mb-1 mobile-rating-smaller-text-2">{{ post.posterInfo.displayName }}</p>
                  </router-link> -->
                  <img
                    :src="post.posterInfo.photo || defaultProfilePhoto"
                    class="img-fluid rounded-circle"
                    style="width: 40px; height: 40px; object-fit: cover;"
                    alt="Poster Photo"
                  />
                </div>
                <!-- Column 2: Post Details -->
                <div class="col-11 mobile-col-10 d-flex flex-wrap align-items-center text-start">
                  <router-link
                    :to="`/profile/user/${post.posterInfo.id}/${post.posterInfo.username}`"
                    class="text-black text-decoration-none fw-bold mobile-rating-smaller-text-2"
                  >
                    {{ post.posterInfo.displayName }}&nbsp;
                  </router-link>
                  <!-- Show "posted on X's wall" if poster is different from wall owner -->
                  <span v-if="post.posterUserID !== post.wallOwnerID" class="mobile-rating-smaller-text-2">
                    <i class="bi bi-arrow-right mx-1"></i>
                    <router-link
                      :to="`/profile/user/${post.wallOwnerInfo.id}/${post.wallOwnerInfo.username}`"
                      class="text-black text-decoration-none fw-bold"
                    >
                      {{ post.wallOwnerInfo.displayName }}
                    </router-link>
                  </span>
                  <p class="mb-0 mobile-rating-smaller-text-2 ms-2">posted on {{ new Date(post.postDate).toLocaleDateString() }}.</p>
                </div>
              </div>

              <div class="row text-start ms-3 mx-0 px-0">
                <!-- Edit + Delete Buttons -->
                <div class="d-flex text-start align-items-center">
                  <button
                    v-if="canEditPost(post)"
                    class="btn primary-btn rounded btn-sm py-1 me-2"
                    data-bs-toggle="modal"
                    data-bs-target="#editPostModal"
                    @click="selectedPostEdit = { ...post }"
                  >
                    Edit
                  </button>
                  <button
                    v-if="canDeletePost(post)"
                    class="btn primary-btn rounded btn-sm py-1 me-2"    
                    style="background-color: #ae3e3e; border: 4px solid #ae3e3e; color:white;"
                    data-bs-toggle="modal"
                    data-bs-target="#deletePostModal"
                    @click="selectedPostDelete = post"
                  >
                    Delete
                  </button>
                </div>

                <!-- Post photo -->
                <div class="row mt-3 mx-0 px-0" v-if="post.postPhotos && post.postPhotos.length > 0">
                  <div class="col-md-12 text-center">
                    <img
                      :src="post.postPhotos[0]"
                      class="img-fluid mx-auto"
                      style="max-height: 300px; object-fit: contain;"
                      alt="Post Photo"
                    />
                  </div>
                </div>

                <!-- Post content -->
                <div class="row mt-3 text-start px-0 mobile-rating-smaller-text-2">
                  <div class="col-md-12">
                    <p>{{ post.postContent }}</p>
                  </div>
                </div>

                <!-- Up vote and downvote and comment button -->
                <div v-if="isLoggedIn" class="row text-start mx-0 px-0">
                  <div class="col-12 d-flex">
                    <div v-if="postLikes !== null && postDislikes !== null" class="d-flex gap-1">
                      <!-- Upvote filled if user already liked -->
                      <p
                        v-if="postLikes.includes(post.id)"
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Un-upvote"
                        class="cursor-pointer mb-0"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="24"
                          height="24"
                          fill="currentColor"
                          class="bi bi-caret-up-fill me-1"
                          viewBox="0 0 16 16"
                          style="cursor: pointer"
                          @click="likePost(post.id)"
                        >
                          <path d="m7.247 4.86-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
                        </svg>
                      </p>
                      <!-- Upvote hollow if user has not liked -->
                      <p
                        v-else
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Upvote"
                        class="cursor-pointer mb-0"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="24"
                          height="24"
                          fill="currentColor"
                          class="bi bi-caret-up me-1"
                          viewBox="0 0 16 16"
                          style="cursor: pointer"
                          @click="likePost(post.id)"
                        >
                          <path d="M3.204 11h9.592L8 5.519zm-.753-.659 4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659"/>
                        </svg>
                      </p>
                      <p class="fw-bold mobile-rating-smaller-text-2 mb-0">{{ post.totalLikes - post.totalDislikes }}</p>
                      <!-- Downvote filled if user already disliked -->
                      <p
                        v-if="postDislikes.includes(post.id)"
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Un-downvote"
                        class="cursor-pointer mb-0"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg" 
                          width="24" 
                          height="24" 
                          fill="currentColor" 
                          class="bi bi-caret-down-fill mx-1"
                          viewBox="0 0 16 16"
                          style="cursor: pointer"
                          @click="dislikePost(post.id)"
                        >
                          <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                        </svg>
                      </p>
                      <!-- Downvote hollow if user has not disliked -->
                      <p
                        v-else
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Downvote"
                        class="cursor-pointer mb-0"
                      >
                        <svg 
                          xmlns="http://www.w3.org/2000/svg" 
                          width="24" 
                          height="24" 
                          fill="currentColor" 
                          class="bi bi-caret-down mx-1"
                          viewBox="0 0 16 16"
                          style="cursor: pointer"
                          @click="dislikePost(post.id)"
                        >
                          <path d="M3.204 5h9.592L8 10.481zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659"/>
                        </svg>  
                      </p>
                    </div>
                    
                    <!-- Comment icon -->
                    <span
                      data-bs-toggle="tooltip"
                      data-bs-placement="top"
                      title="View all Comments"
                      class="cursor-pointer px-2"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        fill="currentColor"
                        class="bi bi-chat-dots"
                        viewBox="0 0 16 16"
                        style="cursor: pointer"
                      >
                        <path d="M5 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0m4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0m3 1a1 1 0 1 0 0-2 1 1 0 0 0 0 2"/>
                        <path d="m2.165 15.803.02-.004c1.83-.363 2.948-.842 3.468-1.105A9 9 0 0 0 8 15c4.418 0 8-3.134 8-7s-3.582-7-8-7-8 3.134-8 7c0 1.76.743 3.37 1.97 4.6a10.4 10.4 0 0 1-.524 2.318l-.003.011a11 11 0 0 1-.244.637c-.079.186.074.394.273.362a22 22 0 0 0 .693-.125m.8-3.108a1 1 0 0 0-.287-.801C1.618 10.83 1 9.468 1 8c0-3.192 3.004-6 7-6s7 2.808 7 6-3.004 6-7 6a8 8 0 0 1-2.088-.272 1 1 0 0 0-.711.074c-.387.196-1.24.57-2.634.893a11 11 0 0 0 .398-2"/>
                      </svg>
                    </span>
                    <p class="fw-bold mobile-rating-smaller-text-2 mb-0">
                      {{ post.totalComments }} Comments
                    </p>
                  </div>
                </div>

                <!-- Read-only view for non-logged-in users -->
                <div v-else class="row text-start mx-0 px-0">
                  <div class="col-12 d-flex">
                    <div class="d-flex gap-1">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        fill="currentColor"
                        class="bi bi-caret-up me-1"
                        viewBox="0 0 16 16"
                      >
                        <path d="M3.204 11h9.592L8 5.519zm-.753-.659 4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659"/>
                      </svg>
                      <p class="fw-bold mobile-rating-smaller-text-2 mb-0">{{ post.totalLikes - post.totalDislikes }}</p>
                      <svg 
                        xmlns="http://www.w3.org/2000/svg" 
                        width="24" 
                        height="24" 
                        fill="currentColor" 
                        class="bi bi-caret-down mx-1"
                        viewBox="0 0 16 16"
                      >
                        <path d="M3.204 5h9.592L8 10.481zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659"/>
                      </svg>  
                    </div>
                    <span class="px-2">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        fill="currentColor"
                        class="bi bi-chat-dots"
                        viewBox="0 0 16 16"
                      >
                        <path d="M5 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0m4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0m3 1a1 1 0 1 0 0-2 1 1 0 0 0 0 2"/>
                        <path d="m2.165 15.803.02-.004c1.83-.363 2.948-.842 3.468-1.105A9 9 0 0 0 8 15c4.418 0 8-3.134 8-7s-3.582-7-8-7-8 3.134-8 7c0 1.76.743 3.37 1.97 4.6a10.4 10.4 0 0 1-.524 2.318l-.003.011a11 11 0 0 1-.244.637c-.079.186.074.394.273.362a22 22 0 0 0 .693-.125m.8-3.108a1 1 0 0 0-.287-.801C1.618 10.83 1 9.468 1 8c0-3.192 3.004-6 7-6s7 2.808 7 6-3.004 6-7 6a8 8 0 0 1-2.088-.272 1 1 0 0 0-.711.074c-.387.196-1.24.57-2.634.893a11 11 0 0 0 .398-2"/>
                      </svg>
                    </span>
                    <p class="fw-bold mobile-rating-smaller-text-2 mb-0">
                      {{ post.totalComments }} Comments
                    </p>
                  </div>
                </div>

                <!-- Comment input bar (only for logged-in users) -->
                <div v-if="isLoggedIn" class="row mt-2 mx-0 px-0">
                  <div class="col-12 gap-1">
                    <div class="input-group">
                      <input
                        type="text"
                        class="form-control rounded me-2 mobile-rating-smaller-text-2"
                        placeholder="Write a comment..."
                        aria-label="Write a comment..."
                        v-model="newComments[post.id]"
                        @keyup.enter="addComment(post.id)"
                      />
                      <button
                        class="btn primary-btn-less-round-blue btn-sm rounded fw-bold mobile-view-hide"
                        type="button"
                        @click="addComment(post.id)"
                      >
                        Comment
                      </button>
                      <button
                        class="btn primary-btn-less-round-blue btn-sm rounded mobile-view-show"
                        type="button"
                        @click="addComment(post.id)"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                          <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Display latest 3 comments -->
                <div v-if="postComments[post.id] && postComments[post.id].length > 0" class="row mt-3 mx-0 px-0">
                  <div class="col-12">
                    <div 
                      v-for="comment in postComments[post.id].slice(0, 3)" 
                      :key="comment.id"
                      class="d-flex align-items-start mb-2 p-2"
                      style="background-color: #f8f9fa; border-radius: 8px;"
                    >
                      <!-- Commenter Photo -->
                      <img
                        v-if="comment.commenterInfo"
                        :src="comment.commenterInfo.photo || defaultProfilePhoto"
                        class="rounded-circle me-2"
                        style="width: 32px; height: 32px; object-fit: cover;"
                        alt="Commenter Photo"
                      />
                      <!-- Comment Content -->
                      <div class="flex-grow-1">
                        <div class="d-flex align-items-center flex-wrap">
                          <router-link
                            v-if="comment.commenterInfo"
                            :to="`/profile/user/${comment.commenterInfo.id}/${comment.commenterInfo.username}`"
                            class="fw-bold text-decoration-none me-2 mobile-rating-smaller-text-2"
                            style="color: rgb(2, 117, 98);"
                          >
                            {{ comment.commenterInfo.displayName }}
                          </router-link>
                          <span class="text-muted mobile-rating-smaller-text-2">
                            {{ new Date(comment.commentDate).toLocaleDateString() }}
                          </span>
                        </div>
                        <p class="mb-0 mobile-rating-smaller-text-2">{{ comment.commentContent }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Load more posts button -->
            <div v-if="showLoadMoreButton" class="d-flex justify-content-center my-3">
              <button
                type="button"
                class="btn secondary-btn btn-md fw-bold"
                @click="loadMorePosts"
              >
                Load More
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>

  <!-- Add Post Modal -->
  <div
    class="modal fade"
    id="addPostModal"
    tabindex="-1"
    aria-labelledby="addPostModalLabel"
    aria-hidden="true"
    ref="addPostModal"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <!-- Modal header -->
        <div class="modal-header d-flex justify-content-between">
          <h5 class="modal-title" id="addPostModalLabel">
            {{ ownProfile ? 'Add A New Post' : `Post on ${displayUser.displayName}'s Wall` }}
          </h5>
          <button
            type="button"
            class="custom-close-btn"
            data-bs-dismiss="modal"
            aria-label="Close"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              fill="currentColor"
              class="bi bi-x"
              viewBox="0 0 16 16"
            >
              <path
                d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"
              />
            </svg>
          </button>
        </div>

        <!-- Modal body -->
        <div class="modal-body">
          <div class="container">
            <div class="row">
              <div class="col-md-12">
                <textarea
                  class="form-control"
                  rows="5"
                  :placeholder="ownProfile ? 'What\'s on your mind?' : `Write a message on ${displayUser.displayName}'s wall...`"
                  v-model="newPostContent"
                ></textarea>
              </div>
            </div>
            <div class="row mt-3">
              <div class="col-md-12">
                <!-- Upload image input field (max 1 photo) -->
                <input
                  type="file"
                  class="form-control"
                  id="newPostPhotoInputField"
                  accept="image/*"
                  @change="imageUpload"
                />

                <!-- Display the uploaded image -->
                <div v-if="newPostPhoto" class="mt-3">
                  <div class="position-relative d-inline-block m-2">
                    <img
                      :src="newPostPhoto"
                      class="img-fluid"
                      style="max-height: 300px"
                      alt="Post Photo"
                    />
                    <button
                      class="btn primary-btn-red btn-sm position-absolute top-0 end-0 mt-3 me-3"
                      @click="removePhoto"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        fill="currentColor"
                        class="bi bi-trash-fill"
                        viewBox="0 0 16 16"
                      >
                        <path
                          d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0"
                        />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal footer -->
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
            :disabled="disableButton"
          >
            Close
          </button>
          <button
            type="button"
            class="btn primary-btn-green"
            :disabled="disableButton || !newPostContent"
            @click="addPost"
            data-bs-dismiss="modal"
          >
            Post
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Edit Post Modal -->
  <div
    class="modal fade"
    id="editPostModal"
    tabindex="-1"
    aria-labelledby="editPostModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <!-- Modal header -->
        <div class="modal-header d-flex justify-content-between">
          <h5 class="modal-title" id="editPostModalLabel">Edit Post</h5>
          <button
            type="button"
            class="custom-close-btn"
            data-bs-dismiss="modal"
            aria-label="Close"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              fill="currentColor"
              class="bi bi-x"
              viewBox="0 0 16 16"
            >
              <path
                d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"
              />
            </svg>
          </button>
        </div>

        <!-- Modal body -->
        <div class="modal-body">
          <div v-if="selectedPostEdit" class="container">
            <!-- Post content -->
            <div class="row text-start">
              <div class="col-md-12">
                <label for="editPostContent" class="form-label fw-bold">Post content:</label>
                <textarea
                  class="form-control"
                  rows="5"
                  placeholder="Write your post here..."
                  v-model="selectedPostEdit.postContent"
                ></textarea>
              </div>
            </div>

            <!-- Current post photo -->
            <div
              v-if="selectedPostEdit.postPhotos && selectedPostEdit.postPhotos.length > 0"
              class="row mt-3 text-start"
            >
              <div class="col-md-12">
                <label for="editPostPhotos" class="form-label fw-bold">Current photo:</label>
                <div class="position-relative d-inline-block m-2">
                  <img
                    :src="selectedPostEdit.postPhotos[0]"
                    class="img-fluid"
                    style="max-height: 300px"
                    alt="Post Photo"
                  />
                  <button
                    class="btn primary-btn-red btn-sm position-absolute top-0 end-0 mt-3 me-3"
                    @click="removeEditPhoto"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      fill="currentColor"
                      class="bi bi-trash-fill"
                      viewBox="0 0 16 16"
                    >
                      <path
                        d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Add new image -->
            <div v-if="!selectedPostEdit.postPhotos || selectedPostEdit.postPhotos.length === 0" class="row mt-3 text-start">
              <div class="col-md-12">
                <label for="newPostPhoto" class="form-label fw-bold">Add a photo:</label>
                <input
                  type="file"
                  class="form-control"
                  id="editPostPhotoInputField"
                  accept="image/*"
                  @change="imageUploadEdit"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Modal footer -->
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
            :disabled="disableButton"
          >
            Close
          </button>
          <button
            type="button"
            class="btn primary-btn-green"
            :disabled="disableButton"
            @click="editPost"
            data-bs-dismiss="modal"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Delete Post Modal -->
  <div
    class="modal fade"
    id="deletePostModal"
    tabindex="-1"
    aria-labelledby="deletePostModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <!-- Modal header -->
        <div class="modal-header d-flex justify-content-between">
          <h5 class="modal-title" id="deletePostModalLabel">Delete Post</h5>
          <button
            type="button"
            class="custom-close-btn"
            data-bs-dismiss="modal"
            aria-label="Close"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              fill="currentColor"
              class="bi bi-x"
              viewBox="0 0 16 16"
            >
              <path
                d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"
              />
            </svg>
          </button>
        </div>

        <!-- Modal body -->
        <div class="modal-body">
          <p class="fw-bold">Are you sure you want to delete this post?</p>
          <p>Deleting this post will delete all the comments and likes associated with it.</p>
        </div>

        <!-- Modal footer -->
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
            :disabled="disableButton"
          >
            Close
          </button>
          <button
            type="button"
            class="btn primary-btn-red"
            @click="deletePost"
            :disabled="disableButton"
            data-bs-dismiss="modal"
          >
            Delete
          </button>
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
import { useToast } from "vue-toastification";
import { Modal } from "bootstrap";

export default {
  name: "UserPersonalWall",
  components: { 
    NavBar, 
    LoadingWithFunFact, 
    UserProfileHeader, 
    UserProfileNavbar 
  },
  data() {
    return {
      dataLoaded: false,

      // Default images
      defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",

      // Display user data (wall owner)
      displayUserID: null,
      routeUsername: null,
      displayUser: {},
      
      // Current logged-in user data
      userID: null,
      userType: null,
      currentUserPhoto: null,
      ownProfile: false,
      loggedInUser: null,

      // Posts data
      posts: [],
      postLikes: [],
      postDislikes: [],
      showLoadMoreButton: true,

      // New post data
      newPostContent: null,
      newPostPhoto: null,

      // Edit post data
      selectedPostEdit: null,

      // Delete post data
      selectedPostDelete: null,

      // Comment data (keyed by post ID)
      newComments: {},
      postComments: {},  // Stores comments for each post, keyed by post ID

      // Button disable state
      disableButton: false,
    };
  },
  computed: {
    isLoggedIn() {
      return this.userID !== null && this.userType !== 'defaultUser';
    },
    canPost() {
      // Can post if logged in and not a venue/producer
      return this.isLoggedIn && this.userType === 'user';
    },
    writePostPlaceholder() {
      if (this.ownProfile) {
        return "What's on your mind?";
      }
      return `Write a message on ${this.displayUser.displayName}'s wall!`;
    },
  },
  async mounted() {
    // Get current user info from localStorage
    const accID = localStorage.getItem("88B_accID");
    const accType = localStorage.getItem("88B_accType");
    const accPhoto = localStorage.getItem("88B_accPhoto");
    
    if (accID !== null) {
      this.userID = parseInt(accID);
      this.userType = accType || 'defaultUser';
      this.currentUserPhoto = accPhoto;
    }

    // Get route parameters
    this.displayUserID = parseInt(this.$route.params.userID);
    this.routeUsername = this.$route.params.username;

    // Check if viewing own profile
    if (this.displayUserID === this.userID) {
      this.ownProfile = true;
    }

    // Get logged-in user data from localStorage (stored by UserProfileRefactor)
    const storedUser = localStorage.getItem("88B_loggedInUser");
    if (storedUser) {
      this.loggedInUser = JSON.parse(storedUser);
    }

    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        this.dataLoaded = false;

        await this.getDisplayUserProfile();
        await this.getPosts();
        
        if (this.isLoggedIn) {
          await this.getPostLikesDislikes();
        }

        this.dataLoaded = true;
      } catch (error) {
        console.error("Error loading data:", error);
        this.dataLoaded = null;
      }
    },

    async getDisplayUserProfile() {
      const response = await this.$axios.get(
        `${process.env.VUE_APP_API_URL}/getData/getUser/${this.displayUserID}`
      );
      this.displayUser = response.data;
    },

    async getPosts() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/userWall/getWallPosts/${this.displayUserID}/0`
        );
        this.posts = response.data.data;
        
        // Hide load more if less than 10 posts
        if (this.posts.length < 10) {
          this.showLoadMoreButton = false;
        }

        // Fetch comments for each post
        await this.fetchCommentsForPosts(this.posts);
      } catch (error) {
        if (error.response && error.response.status === 404) {
          // No posts yet - this is fine
          this.posts = [];
          this.showLoadMoreButton = false;
        } else {
          console.error("Error fetching posts:", error);
        }
      }
    },

    async loadMorePosts() {
      try {
        const lastPostId = this.posts[this.posts.length - 1].id;
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/userWall/getWallPosts/${this.displayUserID}/${lastPostId}`
        );
        
        const newPosts = response.data.data;
        this.posts = this.posts.concat(newPosts);
        
        // Hide load more if less than 10 posts returned
        if (newPosts.length < 10) {
          this.showLoadMoreButton = false;
        }

        // Fetch comments for new posts
        await this.fetchCommentsForPosts(newPosts);
      } catch (error) {
        if (error.response && error.response.status === 404) {
          this.showLoadMoreButton = false;
        } else {
          console.error("Error loading more posts:", error);
        }
      }
    },

    async getPostLikesDislikes() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/userWall/getUserWallLikesDislikes/${this.userID}/${this.displayUserID}`
        );
        this.postLikes = response.data.liked_posts || [];
        this.postDislikes = response.data.disliked_posts || [];
      } catch (error) {
        console.error("Error fetching likes/dislikes:", error);
        this.postLikes = [];
        this.postDislikes = [];
      }
    },

    openAddPostModal() {
      const modalEl = document.getElementById('addPostModal');
      const modal = new Modal(modalEl);
      modal.show();
    },

    // Image upload for new post
    imageUpload(event) {
      const file = event.target.files[0];
      if (file && file.type.match("image.*")) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
          this.newPostPhoto = reader.result;
        };
      }
    },

    // Remove photo from new post
    removePhoto() {
      this.newPostPhoto = null;
      // Clear the file input
      const input = document.getElementById('newPostPhotoInputField');
      if (input) input.value = '';
    },

    // Image upload for edit post
    imageUploadEdit(event) {
      const file = event.target.files[0];
      if (file && file.type.match("image.*")) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
          if (this.selectedPostEdit) {
            this.selectedPostEdit.postPhotos = [reader.result];
          }
        };
      }
    },

    // Remove photo from edit post
    removeEditPhoto() {
      if (this.selectedPostEdit) {
        this.selectedPostEdit.postPhotos = [];
      }
    },

    // Add a new post
    async addPost() {
      const toast = useToast();
      
      if (!this.newPostContent || this.newPostContent.trim() === '') {
        toast.error("Please enter some content for your post.");
        return;
      }

      try {
        this.disableButton = true;

        let postData = {
          wallOwnerID: this.displayUserID,
          posterUserID: this.userID,
          postContent: this.newPostContent,
        };

        if (this.newPostPhoto) {
          postData.images = [this.newPostPhoto];
        }

        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/userWall/addWallPost`,
          postData
        );

        if (response.status === 201) {
          // Reset form
          this.newPostContent = null;
          this.newPostPhoto = null;
          const input = document.getElementById('newPostPhotoInputField');
          if (input) input.value = '';

          // Reload posts
          await this.getPosts();
          await this.getPostLikesDislikes();

          toast.success("Post added successfully!");
        }
      } catch (error) {
        console.error("Error adding post:", error);
        toast.error("An error occurred while adding the post. Please try again!");
      } finally {
        this.disableButton = false;
      }
    },

    // Edit a post
    async editPost() {
      const toast = useToast();

      if (!this.selectedPostEdit || !this.selectedPostEdit.postContent) {
        toast.error("Post content cannot be empty.");
        return;
      }

      try {
        this.disableButton = true;

        let postData = {
          postID: this.selectedPostEdit.id,
          postContent: this.selectedPostEdit.postContent,
          editorID: this.userID,
          images: this.selectedPostEdit.postPhotos || [],
        };

        const response = await this.$axios.put(
          `${process.env.VUE_APP_API_URL}/userWall/editWallPost`,
          postData
        );

        if (response.status === 200) {
          await this.getPosts();
          toast.success("Post edited successfully!");
        }
      } catch (error) {
        console.error("Error editing post:", error);
        toast.error("An error occurred while editing the post. Please try again!");
      } finally {
        this.disableButton = false;
        this.selectedPostEdit = null;
      }
    },

    // Delete a post
    async deletePost() {
      const toast = useToast();

      if (!this.selectedPostDelete) {
        return;
      }

      try {
        this.disableButton = true;

        const response = await this.$axios.delete(
          `${process.env.VUE_APP_API_URL}/userWall/removeWallPost`,
          {
            data: {
              postID: this.selectedPostDelete.id,
              removerID: this.userID,
            },
          }
        );

        if (response.status === 200) {
          await this.getPosts();
          toast.success("Post deleted successfully!");
        }
      } catch (error) {
        console.error("Error deleting post:", error);
        toast.error("An error occurred while deleting the post. Please try again!");
      } finally {
        this.disableButton = false;
        this.selectedPostDelete = null;
      }
    },

    // Like/unlike a post
    async likePost(postID) {
      const toast = useToast();

      try {
        const response = await this.$axios.put(
          `${process.env.VUE_APP_API_URL}/userWall/likeUnlikeWallPost`,
          {
            userID: this.userID,
            postID: postID,
          }
        );

        const post = this.posts.find((p) => p.id === postID);

        if (response.data.liked) {
          this.postLikes.push(postID);
          post.totalLikes += 1;

          // Remove from dislikes if was disliked
          const dislikeIndex = this.postDislikes.indexOf(postID);
          if (dislikeIndex > -1) {
            this.postDislikes.splice(dislikeIndex, 1);
            post.totalDislikes -= 1;
          }
        } else {
          const index = this.postLikes.indexOf(postID);
          if (index > -1) {
            this.postLikes.splice(index, 1);
            post.totalLikes -= 1;
          }
        }
      } catch (error) {
        console.error("Error liking post:", error);
        toast.error("An error occurred. Please try again!");
      }
    },

    // Dislike/un-dislike a post
    async dislikePost(postID) {
      const toast = useToast();

      try {
        const response = await this.$axios.put(
          `${process.env.VUE_APP_API_URL}/userWall/dislikeUndislikeWallPost`,
          {
            userID: this.userID,
            postID: postID,
          }
        );

        const post = this.posts.find((p) => p.id === postID);

        if (response.data.disliked) {
          this.postDislikes.push(postID);
          post.totalDislikes += 1;

          // Remove from likes if was liked
          const likeIndex = this.postLikes.indexOf(postID);
          if (likeIndex > -1) {
            this.postLikes.splice(likeIndex, 1);
            post.totalLikes -= 1;
          }
        } else {
          const index = this.postDislikes.indexOf(postID);
          if (index > -1) {
            this.postDislikes.splice(index, 1);
            post.totalDislikes -= 1;
          }
        }
      } catch (error) {
        console.error("Error disliking post:", error);
        toast.error("An error occurred. Please try again!");
      }
    },

    // Add a comment
    async addComment(postID) {
      const toast = useToast();
      const commentContent = this.newComments[postID];

      if (!commentContent || commentContent.trim() === '') {
        toast.error("Please enter a comment before submitting.");
        return;
      }

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/userWall/addWallPostComment`,
          {
            commenterID: this.userID,
            postID: postID,
            commentContent: commentContent,
          }
        );

        if (response.status === 201) {
          // Clear the comment input
          this.newComments[postID] = '';

          // Update comment count
          const post = this.posts.find((p) => p.id === postID);
          if (post) {
            post.totalComments += 1;
          }

          // Refresh comments for this post
          await this.getPostComments(postID);

          toast.success("Comment added successfully!");
        }
      } catch (error) {
        console.error("Error adding comment:", error);
        toast.error("An error occurred while adding the comment. Please try again!");
      }
    },

    // Fetch comments for a single post
    async getPostComments(postID) {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/userWall/getWallPostComments/${postID}/0`
        );
        // Store comments for this post (Vue 3 reactivity)
        this.postComments[postID] = response.data.data || [];
      } catch (error) {
        console.error(`Error fetching comments for post ${postID}:`, error);
        this.postComments[postID] = [];
      }
    },

    // Fetch comments for multiple posts
    async fetchCommentsForPosts(posts) {
      const promises = posts.map(post => this.getPostComments(post.id));
      await Promise.all(promises);
    },

    // Check if current user can edit a post
    canEditPost(post) {
      if (!this.isLoggedIn) return false;
      // Can edit if user is the poster or the wall owner
      return post.posterUserID === this.userID || post.wallOwnerID === this.userID;
    },

    // Check if current user can delete a post
    canDeletePost(post) {
      if (!this.isLoggedIn) return false;
      // Can delete if user is the poster or the wall owner
      return post.posterUserID === this.userID || post.wallOwnerID === this.userID;
    },
  }
};
</script>

<style scoped>
/* Mobile responsiveness */
@media (max-width: 768px) {
  .mobile-mt-3 {
    margin-top: 1rem !important;
  }
  
  .mobile-px-3 {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
  }

  .mobile-col-2 {
    flex: 0 0 auto;
    width: 16.66666667%;
  }

  .mobile-col-10 {
    flex: 0 0 auto;
    width: 83.33333333%;
  }

  .mobile-rating-smaller-text-2 {
    font-size: 0.8rem;
  }

  .mobile-view-hide {
    display: none !important;
  }

  .mobile-view-show {
    display: inline-block !important;
  }
}

@media (min-width: 769px) {
  .mobile-view-show {
    display: none !important;
  }
}

/* Cursor pointer */
.cursor-pointer {
  cursor: pointer;
}

/* Custom close button for modals */
.custom-close-btn {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
}

.custom-close-btn:hover {
  opacity: 0.7;
}
</style>
