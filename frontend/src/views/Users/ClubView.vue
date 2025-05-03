<template>
  <div class="mb-3" style="background-color: #eae9ee">
    <NavBar />

    <!-- Display when data is still loading -->
    <div
      class="text-info-emphasis fst-italic fw-bold fs-5 pt-5"
      v-if="dataLoaded == false"
    >
      <span>Loading page, please wait...</span>
      <br /><br />
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Display when data fails to load-->
    <div
      class="text-danger fst-italic fw-bold fs-3 pt-5"
      v-if="dataLoaded == null"
    >
      <span>An error occurred while loading this page, please try again!</span>
      <br />
      <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
        <span class="fs-5 fst-italic"> Return to previous page </span>
      </button>
      <button class="btn primary-btn btn-sm mx-1" @click="this.$router.go(0)">
        <span class="fs-5 fst-italic"> Go to Home page </span>
      </button>
    </div>

    <!-- Display when data is loaded -->
    <div v-if="dataLoaded == true">
      <!-- Club Banner -->
      <div
        class="container-fluid p-0 border-bottom"
        style="background-color: white"
      >
        <img
          v-if="clubInfo.clubBanner != ''"
          :src="clubInfo.clubBanner"
          class="img-fluid"
          alt="Club Banner"
        />
        <img v-else :src="defaultBanner" class="img-fluid" alt="Club Banner" />
      </div>

      <!-- Main content -->
      <div v-if="!editClub" class="container mt-5">
        <div class="row">
          <!-- Column 1: Club name, join button / add post button, posts-->
          <div class="col-md-9 order-md-1 order-2">
            <!-- Row 1: Club name, join button / add post button -->
            <div class="row">
              <div class="col-md-6">
                <h1 class="fw-bold text-start">{{ clubInfo.clubName }}</h1>
              </div>
              <div class="col-md-6 text-end">
                <button
                  v-if="isMember"
                  class="btn primary-btn-green"
                  data-bs-toggle="modal"
                  data-bs-target="#addPostModal"
                >
                  Add Post
                </button>
                <button
                  v-if="
                    isMember == null &&
                    !clubInfo.isInviteOnly &&
                    !hasRequested &&
                    !isInvited
                  "
                  class="btn primary-btn-green"
                  @click="joinClub"
                  :disabled="disableButton"
                >
                  Join Club
                </button>
                <button
                  v-if="
                    isMember == null &&
                    clubInfo.isInviteOnly &&
                    !hasRequested &&
                    !isInvited
                  "
                  class="btn primary-btn-green"
                  @click="requestToJoin"
                  :disabled="disableButton"
                >
                  Request to Join
                </button>
                <button
                  v-if="isInvited"
                  class="btn primary-btn-green ms-3"
                  @click="acceptInvite"
                  :disabled="disableButton"
                >
                  Accept Invite
                </button>
                <button
                  v-if="hasRequested"
                  class="btn primary-btn-green ms-3"
                  disabled
                >
                  Request Sent
                </button>
                <button
                  v-if="isMember"
                  class="btn primary-btn-red ms-3"
                  data-bs-toggle="modal"
                  data-bs-target="#leaveClubModal"
                >
                  Leave Club
                </button>
              </div>
            </div>

            <!-- Add post modal start -->
            <div
              class="modal fade"
              id="addPostModal"
              tabindex="-1"
              aria-labelledby="addPostModalLabel"
              aria-hidden="true"
            >
              <div class="modal-dialog modal-lg">
                <div class="modal-content">
                  <!-- Modal header -->
                  <div class="modal-header d-flex justify-content-between">
                    <h5 class="modal-title" id="addPostModalLabel">
                      Add A New Post
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
                            placeholder="Write your post here..."
                            v-model="newPostContent"
                          ></textarea>
                        </div>
                      </div>
                      <div class="row mt-3">
                        <div class="col-md-12">
                          <!-- Upload image(s) input field -->
                          <input
                            type="file"
                            class="form-control"
                            id="newPostPhotoInputField"
                            accept="image/*"
                            multiple
                            @change="imageUpload"
                          />

                          <!-- Display the uploaded images -->
                          <div v-if="newPostPhotos.length > 0" class="mt-3">
                            <div
                              v-for="(photo, index) in newPostPhotos"
                              :key="index"
                              class="position-relative d-inline-block m-2"
                            >
                              <img
                                :src="photo"
                                class="img-fluid"
                                style="height: 300px"
                                alt="Post Photo"
                              />
                              <button
                                class="btn primary-btn-red btn-sm position-absolute top-0 end-0 mt-3 me-3"
                                @click="removePhotoNew(index)"
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
                      :disabled="disableButton"
                      @click="addPost"
                      data-bs-dismiss="modal"
                    >
                      Post
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <!-- end of add post modal -->

            <!-- Confirm leave club modal start -->
            <div
              class="modal fade"
              id="leaveClubModal"
              tabindex="-1"
              aria-labelledby="leaveClubModalLabel"
              aria-hidden="true"
            >
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-header d-flex justify-content-between">
                    <h5 class="modal-title" id="leaveClubModalLabel">
                      Leave Club
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
                  <div class="modal-body">
                    <p>Are you sure you want to leave this club?</p>
                  </div>
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
                      @click="leaveClub"
                      :disabled="disableButton"
                      data-bs-dismiss="modal"
                    >
                      Leave Club
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <!-- end of confirm leave club modal -->

            <!-- Post header -->
            <h4 class="fst-italic text-start mt-3">Latest Posts</h4>

            <!-- Row 2: Posts section -->
            <div v-if="posts.length == 0" class="text-center mt-5">
              <!-- If user is not a member, it will show the message below -->
              <h3 v-if="!isMember && clubInfo.isInviteOnly" class="fw-bold">
                Request to join the club to see posts!
              </h3>
              <!-- If user is a member and club has no post yet, it will show the message below -->
              <h3 v-else class="fw-bold">No posts available yet!</h3>
            </div>

            <div v-else>
              <!-- Each Post -->
              <div
                v-for="post in posts"
                :key="post.id"
                class="row mb-4"
                style="
                  background-color: white;
                  border-radius: 10px;
                  padding: 20px;
                  border: 1px solid black;
                "
              >
                <!-- Column 1: Poster Photo -->
                <div class="col-md-1 d-flex flex-column align-items-start">
                  <router-link
                    :to="
                      profileURL(post.posterInfo.id, post.posterInfo.userType)
                    "
                  >
                    <p class="fw-bold">{{ post.posterName }}</p>
                  </router-link>
                  <img
                    v-if="post.posterPhoto"
                    :src="post.posterPhoto"
                    class="img-fluid rounded-circle"
                    alt="Poster Photo"
                  />
                  <svg
                    v-else
                    xmlns="http://www.w3.org/2000/svg"
                    width="45"
                    height="45"
                    fill="currentColor"
                    class="bi bi-person-circle"
                    viewBox="0 0 16 16"
                  >
                    <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
                    <path
                      fill-rule="evenodd"
                      d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"
                    />
                  </svg>
                </div>

                <!-- Column 2: Post Details -->
                <div class="col-md-11">
                  <!-- Row 1: User name, post date, edit and delete post buttons -->
                  <div class="row text-start d-flex align-items-center">
                    <div class="col-md-3">
                      <router-link
                        :to="
                          profileURL(
                            post.posterInfo.id,
                            post.posterInfo.userType
                          )
                        "
                        class="text-black"
                      >
                        <p
                          v-if="post.posterInfo.userType == 'user'"
                          class="fw-bold"
                        >
                          {{ post.posterInfo.displayName }}
                        </p>
                        <p
                          v-else-if="post.posterInfo.userType == 'producer'"
                          class="fw-bold"
                        >
                          {{ post.posterInfo.producerName }}
                        </p>
                        <p v-else class="fw-bold">
                          {{ post.posterInfo.venueName }}
                        </p>
                      </router-link>
                    </div>
                    <div class="col-md-5">
                      <p>{{ post.postDate }}</p>
                    </div>
                    <div class="col-md-4 text-end">
                      <button
                        v-if="isAdmin || post.posterInfo.id == userID"
                        class="btn primary-btn-green btn-sm me-3"
                        data-bs-toggle="modal"
                        data-bs-target="#editPostModal"
                        @click="selectedPostEdit = post"
                      >
                        Edit
                      </button>
                      <button
                        v-if="isAdmin || post.posterInfo.id == userID"
                        class="btn primary-btn-red btn-sm"
                        data-bs-toggle="modal"
                        data-bs-target="#deletePostModal"
                        @click="selectedPostDelete = post"
                      >
                        Delete
                      </button>
                    </div>
                  </div>

                  <!-- Edit post modal start -->
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
                        <div
                          class="modal-header d-flex justify-content-between"
                        >
                          <h5 class="modal-title" id="editPostModalLabel">
                            Edit Post
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
                          <div v-if="selectedPostEdit" class="container">
                            <!-- Post content -->
                            <div class="row text-start">
                              <div class="col-md-12">
                                <label
                                  for="editPostContent"
                                  class="form-label fw-bold"
                                  >Post content:
                                </label>
                                <textarea
                                  class="form-control"
                                  rows="5"
                                  placeholder="Write your post here..."
                                  v-model="selectedPostEdit.postContent"
                                ></textarea>
                              </div>
                            </div>

                            <!-- Current post photos -->
                            <div
                              v-if="selectedPostEdit.postPhotos.length > 0"
                              class="row mt-3 text-start"
                            >
                              <div class="col-md-12">
                                <label
                                  for="editPostPhotos"
                                  class="form-label fw-bold"
                                  >Current photos:</label
                                >
                                <div
                                  v-for="(
                                    photo, index
                                  ) in selectedPostEdit.postPhotos"
                                  :key="index"
                                  class="position-relative d-inline-block m-2"
                                >
                                  <img
                                    :src="photo"
                                    class="img-fluid"
                                    style="height: 300px"
                                    alt="Post Photo"
                                  />
                                  <button
                                    class="btn primary-btn-red btn-sm position-absolute top-0 end-0 mt-3 me-3"
                                    @click="removePhoto(index)"
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

                            <!-- Add new images -->
                            <div class="row mt-3 text-start">
                              <div class="col-md-12">
                                <label
                                  for="newPostPhotos"
                                  class="form-label fw-bold"
                                  >Add more photos:</label
                                >
                                <input
                                  type="file"
                                  class="form-control"
                                  id="editPostPhotoInputField"
                                  accept="image/*"
                                  multiple
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
                            Edit
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                  <!-- Edit post modal end-->

                  <!-- Delete post modal start -->
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
                        <div
                          class="modal-header d-flex justify-content-between"
                        >
                          <h5 class="modal-title" id="deletePostModalLabel">
                            Delete Post
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
                          <p class="fw-bold">
                            Are you sure you want to delete this post?
                          </p>
                          <p>
                            Deleting this post will delete all the comments and
                            likes in this post.
                          </p>
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
                  <!-- Delete post modal end -->

                  <!-- Row 2: Post photo -->
                  <div class="row mb-3" v-if="post.postPhotos.length > 0">
                    <div class="col-md-12">
                      <div id="postPhotosCarousel" class="carousel slide">
                        <div class="carousel-indicators">
                          <button
                            v-for="(photo, index) in post.postPhotos"
                            :key="index"
                            type="button"
                            style="background-color: black"
                            :data-bs-target="'#postPhotosCarousel'"
                            :data-bs-slide-to="index"
                            :class="{ active: index === 0 }"
                            :aria-current="index === 0 ? 'true' : undefined"
                            :aria-label="'Slide ' + (index + 1)"
                          ></button>
                        </div>
                        <div class="carousel-inner">
                          <div
                            v-for="(photo, index) in post.postPhotos"
                            :key="index"
                            :class="['carousel-item', { active: index === 0 }]"
                          >
                            <img
                              :src="photo"
                              class="d-block mx-auto w-auto"
                              style="height: 250px"
                              :alt="'Slide ' + (index + 1)"
                            />
                          </div>
                        </div>
                        <button
                          class="carousel-control-prev"
                          type="button"
                          data-bs-target="#postPhotosCarousel"
                          data-bs-slide="prev"
                        >
                          <span
                            class="carousel-control-prev-icon"
                            aria-hidden="true"
                            style="background-color: black"
                          ></span>
                          <span class="visually-hidden">Previous</span>
                        </button>
                        <button
                          class="carousel-control-next"
                          type="button"
                          data-bs-target="#postPhotosCarousel"
                          data-bs-slide="next"
                        >
                          <span
                            class="carousel-control-next-icon"
                            aria-hidden="true"
                            style="background-color: black"
                          ></span>
                          <span class="visually-hidden">Next</span>
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Row 3: Post content -->
                  <div class="row text-start">
                    <div class="col-md-12">
                      <p>{{ post.postContent }}</p>
                    </div>
                  </div>

                  <!-- Row 4: Post info such as total likes, total comments -->
                  <div class="row text-start">
                    <div class="col-md-12 d-flex gap-4">
                      <p class="fw-bold">Total Likes: {{ post.totalLikes }}</p>
                      <p class="fw-bold">
                        Total Comments: {{ post.totalComments }}
                      </p>
                    </div>
                  </div>

                  <!-- Row 5: Like button image -->
                  <div v-if="isMember" class="row text-start">
                    <div class="col-12 d-flex gap-4">
                      <!-- Red thumbs up with red fill if user already liked the post -->
                      <p
                        v-if="postLikes.includes(post.id)"
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Unlike"
                        class="cursor-pointer"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="24"
                          height="24"
                          fill="red"
                          class="bi bi-hand-thumbs-up-fill"
                          viewBox="0 0 16 16"
                          style="cursor: pointer"
                          @click="likePost(post.id)"
                        >
                          <path
                            d="M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a10 10 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733q.086.18.138.363c.077.27.113.567.113.856s-.036.586-.113.856c-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.2 3.2 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.8 4.8 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"
                          />
                        </svg>
                      </p>

                      <!-- Black thumbs up with no fill if user has not liked the post -->
                      <p
                        v-else
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Like"
                        class="cursor-pointer"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="24"
                          height="24"
                          fill="currentColor"
                          class="bi bi-hand-thumbs-up cursor-pointer"
                          viewBox="0 0 16 16"
                          style="cursor: pointer"
                          @click="likePost(post.id)"
                        >
                          <path
                            d="M8.864.046C7.908-.193 7.02.53 6.956 1.466c-.072 1.051-.23 2.016-.428 2.59-.125.36-.479 1.013-1.04 1.639-.557.623-1.282 1.178-2.131 1.41C2.685 7.288 2 7.87 2 8.72v4.001c0 .845.682 1.464 1.448 1.545 1.07.114 1.564.415 2.068.723l.048.03c.272.165.578.348.97.484.397.136.861.217 1.466.217h3.5c.937 0 1.599-.477 1.934-1.064a1.86 1.86 0 0 0 .254-.912c0-.152-.023-.312-.077-.464.201-.263.38-.578.488-.901.11-.33.172-.762.004-1.149.069-.13.12-.269.159-.403.077-.27.113-.568.113-.857 0-.288-.036-.585-.113-.856a2 2 0 0 0-.138-.362 1.9 1.9 0 0 0 .234-1.734c-.206-.592-.682-1.1-1.2-1.272-.847-.282-1.803-.276-2.516-.211a10 10 0 0 0-.443.05 9.4 9.4 0 0 0-.062-4.509A1.38 1.38 0 0 0 9.125.111zM11.5 14.721H8c-.51 0-.863-.069-1.14-.164-.281-.097-.506-.228-.776-.393l-.04-.024c-.555-.339-1.198-.731-2.49-.868-.333-.036-.554-.29-.554-.55V8.72c0-.254.226-.543.62-.65 1.095-.3 1.977-.996 2.614-1.708.635-.71 1.064-1.475 1.238-1.978.243-.7.407-1.768.482-2.85.025-.362.36-.594.667-.518l.262.066c.16.04.258.143.288.255a8.34 8.34 0 0 1-.145 4.725.5.5 0 0 0 .595.644l.003-.001.014-.003.058-.014a9 9 0 0 1 1.036-.157c.663-.06 1.457-.054 2.11.164.175.058.45.3.57.65.107.308.087.67-.266 1.022l-.353.353.353.354c.043.043.105.141.154.315.048.167.075.37.075.581 0 .212-.027.414-.075.582-.05.174-.111.272-.154.315l-.353.353.353.354c.047.047.109.177.005.488a2.2 2.2 0 0 1-.505.805l-.353.353.353.354c.006.005.041.05.041.17a.9.9 0 0 1-.121.416c-.165.288-.503.56-1.066.56z"
                          />
                        </svg>
                      </p>

                      <!-- Comment icon -->
                      <span
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Comment"
                        class="cursor-pointer"
                        @click="openPost(post.id)"
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
                          <path
                            d="M5 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0m4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0m3 1a1 1 0 1 0 0-2 1 1 0 0 0 0 2"
                          />
                          <path
                            d="m2.165 15.803.02-.004c1.83-.363 2.948-.842 3.468-1.105A9 9 0 0 0 8 15c4.418 0 8-3.134 8-7s-3.582-7-8-7-8 3.134-8 7c0 1.76.743 3.37 1.97 4.6a10.4 10.4 0 0 1-.524 2.318l-.003.011a11 11 0 0 1-.244.637c-.079.186.074.394.273.362a22 22 0 0 0 .693-.125m.8-3.108a1 1 0 0 0-.287-.801C1.618 10.83 1 9.468 1 8c0-3.192 3.004-6 7-6s7 2.808 7 6-3.004 6-7 6a8 8 0 0 1-2.088-.272 1 1 0 0 0-.711.074c-.387.196-1.24.57-2.634.893a11 11 0 0 0 .398-2"
                          />
                        </svg>
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Load more post -->
              <div v-if="showButton" class="d-flex justify-content-center my-3">
                <button
                  type="button"
                  class="btn secondary-btn btn-md"
                  @click="loadMorePosts"
                >
                  Load More
                </button>
              </div>
            </div>
          </div>

          <!-- Column 2: Club type, number of members, club description, invite button and settings button -->
          <div class="col-md-3 order-md-2 order-1 ps-md-3">
            <!-- Club type and number of members -->
            <p class="text-start">
              <span v-if="clubInfo.isInviteOnly" class="fw-bold">
                Private Group
              </span>
              <span v-else class="fw-bold"> Public Group </span>
              <span> | </span>
              <span class="fw-bold">Number of Members:</span>
              {{ clubInfo.totalMembers }}
              <!--Number of members with joinStatus = True (members who have been invited but not yet accepted will not be included)-->
            </p>

            <!-- Club description -->
            <p class="text-start">{{ clubInfo.clubDesc }}</p>

            <!-- Invite button -->
            <button
              class="ps-0 btn btn-warning ps-2 d-flex flex-row align-items-center"
            >
              <!-- Invite icon -->
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-share"
                viewBox="0 0 16 16"
              >
                <path
                  d="M13.5 1a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3M11 2.5a2.5 2.5 0 1 1 .603 1.628l-6.718 3.12a2.5 2.5 0 0 1 0 1.504l6.718 3.12a2.5 2.5 0 1 1-.488.876l-6.718-3.12a2.5 2.5 0 1 1 0-3.256l6.718-3.12A2.5 2.5 0 0 1 11 2.5m-8.5 4a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3m11 5.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3"
                />
              </svg>
              <!-- Invite text -->
              <span class="ms-2">Invite your friends!</span>
            </button>

            <!-- Settings button -->
            <button
              v-if="isAdmin"
              class="ps-0 btn d-flex flex-row align-items-center hover-underline"
              @click="editClub = true"
            >
              <!-- Settings icon -->
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-gear"
                viewBox="0 0 16 16"
              >
                <path
                  d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492M5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0"
                />
                <path
                  d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115z"
                />
              </svg>
              <!-- Settings text -->
              <span class="ms-2">Club Settings</span>
            </button>

            <!-- Admin Details -->
            <div class="mt-5 text-start row">
              <p class="fw-bold">Admins</p>

              <div
                v-for="admin in admins.slice(0, 3)"
                :key="admin.id"
                class="d-flex flex-column align-items-center col-sm-3 col-md-4 col-lg-3 mt-3"
              >
                <!-- Admin photo -->
                <img
                  v-if="admin.photo"
                  :src="admin.photo"
                  class="img-fluid rounded-circle"
                  alt="Admin Photo"
                />
                <svg
                  v-else
                  xmlns="http://www.w3.org/2000/svg"
                  width="45"
                  height="45"
                  fill="currentColor"
                  class="bi bi-person-circle"
                  viewBox="0 0 16 16"
                >
                  <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
                  <path
                    fill-rule="evenodd"
                    d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"
                  />
                </svg>

                <!-- Admin name -->
                <router-link :to="profileURL(admin.id, admin.userType)">
                  <p v-if="admin.userType == 'user'">{{ admin.displayName }}</p>
                  <p v-else-if="admin.userType == 'producer'">
                    {{ admin.producerName }}
                  </p>
                  <p v-else>{{ admin.venueName }}</p>
                </router-link>

                <!-- Show all admins button -->
                <button
                  v-if="admins.length > 3"
                  type="button"
                  class="btn secondary-btn btn-sm mt-3"
                  data-bs-toggle="modal"
                  data-bs-target="#showAllAdminsModal"
                >
                  View All Admins
                </button>
              </div>
            </div>

            <!-- Modal to show all admins -->
            <div
              class="modal fade"
              id="showAllAdminsModal"
              tabindex="-1"
              aria-labelledby="showAllAdminsModalLabel"
              aria-hidden="true"
            >
              <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                  <!-- Modal header -->
                  <div class="modal-header">
                    <h5 class="modal-title" id="showAllAdminsModalLabel">
                      Admins
                    </h5>
                    <button
                      type="button"
                      class="btn-close"
                      data-bs-dismiss="modal"
                      aria-label="Close"
                    ></button>
                  </div>

                  <!-- Modal body -->
                  <div class="modal-body">
                    <div class="row">
                      <div
                        v-for="admin in admins"
                        :key="admin.id"
                        class="d-flex flex-column align-items-center col-sm-3 col-md-4 col-lg-3 mt-3"
                      >
                        <!-- Admin photo -->
                        <img
                          v-if="admin.photo"
                          :src="admin.photo"
                          class="img-fluid rounded-circle"
                          alt="Admin Photo"
                        />
                        <svg
                          v-else
                          xmlns="http://www.w3.org/2000/svg"
                          width="45"
                          height="45"
                          fill="currentColor"
                          class="bi bi-person-circle"
                          viewBox="0 0 16 16"
                        >
                          <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
                          <path
                            fill-rule="evenodd"
                            d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"
                          />
                        </svg>

                        <!-- Admin name -->
                        <router-link :to="profileURL(admin.id, admin.userType)">
                          <p v-if="admin.userType == 'user'">
                            {{ admin.displayName }}
                          </p>
                          <p v-else-if="admin.userType == 'producer'">
                            {{ admin.producerName }}
                          </p>
                          <p v-else>{{ admin.venueName }}</p>
                        </router-link>
                      </div>
                    </div>
                  </div>

                  <!-- Modal footer -->
                  <div class="modal-footer">
                    <button
                      type="button"
                      class="btn btn-secondary"
                      data-bs-dismiss="modal"
                    >
                      Close
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <!-- View all admins modal end -->

            <!-- Club Members -->
            <div class="mt-5 text-start row">
              <p class="fw-bold">Members ({{ clubInfo.totalMembers }})</p>

              <div
                v-for="member in members.slice(0, 3)"
                :key="member.id"
                class="d-flex flex-column align-items-center col-sm-3 col-md-6 col-lg-4 mt-3"
              >
                <!-- Member photo -->
                <img
                  v-if="member.photo"
                  :src="member.photo"
                  class="img-fluid rounded-circle"
                  alt="Member Photo"
                />
                <svg
                  v-else
                  xmlns="http://www.w3.org/2000/svg"
                  width="45"
                  height="45"
                  fill="currentColor"
                  class="bi bi-person-circle"
                  viewBox="0 0 16 16"
                >
                  <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
                  <path
                    fill-rule="evenodd"
                    d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"
                  />
                </svg>

                <!-- Member name -->
                <router-link :to="profileURL(member.id, member.userType)">
                  <p v-if="member.userType == 'user'" class="name-container">
                    {{ member.displayName }}
                  </p>
                  <p
                    v-else-if="member.userType == 'producer'"
                    class="name-container"
                  >
                    {{ member.producerName }}
                  </p>
                  <p v-else class="name-container">{{ member.venueName }}</p>
                </router-link>
              </div>

              <!-- Show more members button -->
              <button
                v-if="members.length > 3"
                type="button"
                class="btn secondary-btn btn-sm mt-3 ms-3"
                data-bs-toggle="modal"
                data-bs-target="#showAllMembersModal"
                @click="loadAllMembers"
              >
                View All Members
              </button>

              <!-- Show error message -->
              <div
                v-if="getFewMemberError"
                class="alert alert-danger mt-3"
                role="alert"
              >
                {{ getFewMemberError }}
              </div>
            </div>

            <!-- View all members modal -->
            <div
              class="modal fade"
              id="showAllMembersModal"
              tabindex="-1"
              aria-labelledby="showAllMembersModalLabel"
              aria-hidden="true"
            >
              <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                  <!-- Modal header -->
                  <div class="modal-header">
                    <h5 class="modal-title" id="showAllMembersModalLabel">
                      Members
                    </h5>
                    <button
                      type="button"
                      class="btn-close"
                      data-bs-dismiss="modal"
                      aria-label="Close"
                    ></button>
                  </div>

                  <!-- Modal body -->
                  <div class="modal-body">
                    <div class="row">
                      <div
                        v-for="member in members"
                        :key="member.id"
                        class="d-flex flex-column align-items-center col-sm-4 col-md-6 col-lg-4 mt-3"
                      >
                        <!-- Member photo -->
                        <img
                          v-if="member.photo"
                          :src="member.photo"
                          class="img-fluid rounded-circle"
                          alt="Member Photo"
                        />
                        <svg
                          v-else
                          xmlns="http://www.w3.org/2000/svg"
                          width="45"
                          height="45"
                          fill="currentColor"
                          class="bi bi-person-circle"
                          viewBox="0 0 16 16"
                        >
                          <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
                          <path
                            fill-rule="evenodd"
                            d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"
                          />
                        </svg>

                        <!-- Member name -->
                        <router-link
                          :to="profileURL(member.id, member.userType)"
                        >
                          <p
                            v-if="member.userType == 'user'"
                            class="name-container"
                          >
                            {{ member.displayName }}
                          </p>
                          <p
                            v-else-if="member.userType == 'producer'"
                            class="name-container"
                          >
                            {{ member.producerName }}
                          </p>
                          <p v-else class="name-container">
                            {{ member.venueName }}
                          </p>
                        </router-link>
                      </div>
                    </div>
                  </div>

                  <!-- Load all member error message -->
                  <div
                    v-if="getAllMemberError"
                    class="alert alert-danger mt-3"
                    role="alert"
                  >
                    {{ getAllMemberError }}
                  </div>

                  <!-- Modal footer -->
                  <div class="modal-footer">
                    <button
                      type="button"
                      class="btn btn-secondary"
                      data-bs-dismiss="modal"
                    >
                      Close
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <!-- View all members modal end -->
          </div>
        </div>
      </div>

      <!-- Club Setting Component -->
      <ClubSettings
        v-if="isAdmin && editClub"
        :clubInfo="clubInfo"
        :clubId="clubId"
        :memberID="memberID"
        :numMembers="clubInfo.totalMembers"
        @close-club-settings="closeSettings"
      />
    </div>
  </div>
</template>

<script>
// Import the necessary libraries
import NavBar from "@/components/NavBar.vue";
import ClubSettings from "@/components/ClubSettings.vue";
import { useToast } from "vue-toastification";
export default {
  name: "ClubView",
  components: {
    NavBar,
    ClubSettings,
  },
  data() {
    return {
      // Variable for page loading
      dataLoaded: false,

      // Variable to disable buttons
      disableButton: false,

      // Variable for thumbs up icon
      outlineColor: "black",
      innerFill: "blue",

      // Variable for show more button
      showButton: true,

      // Variables for user data
      userID: null,
      userType: null,
      username: null,
      isMember: null, // If user has not been invited, this will be null. If user has been invited, this will be false. If user has accepted the invitation, this will be true.
      isAdmin: false,
      memberID: null,

      // Variable for membership status
      hasRequested: null,
      isInvited: null,

      // Variable for default banner
      defaultBanner: require("@/assets/defaultGroupBanner.png"),

      // Variable for club data
      clubId: null,
      clubInfo: null,
      admins: null,
      posts: [], // Array to store posts
      postLikes: [], // Array to store user's likes for the posts
      members: [], // Array to store club members

      // Variables for error messages
      getFewMemberError: null,
      getAllMemberError: null,

      // Variables for adding a post
      newPostContent: null,
      newPostPhotos: [],

      // Variable for editing a post
      selectedPostEdit: null,

      // Variable for deleting a post
      selectedPostDelete: null,

      // Variable for showing the club settings component
      editClub: false,
    };
  },

  methods: {
    // Function to get data for page start ========================================
    // Function to get club information
    async getPageData() {
      try {
        // Get club data
        const clubData = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/club/getSpecificClubInfo/${this.clubId}`
        );
        this.clubInfo = clubData.data.club_info;
        this.admins = clubData.data.admins;

        this.dataLoaded = true;

        // Get posts
        if (this.clubInfo.isInviteOnly && this.memberID == null) {
          this.dataLoaded = true;
        } else {
          this.getPosts();
        }

        // Get the first few members
        this.getFirstFewMembers();
      } catch (error) {
        // Check if status code is 404
        if (error.response.status == 404) {
          this.dataLoaded = null;
        }
        console.log(error);
        this.dataLoaded = null;
      }
    },

    // Function to get posts (used inside getPageData function if club data is successfully retrieved)
    async getPosts() {
      try {
        // Get posts
        const postsData = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/club/getClubPosts/${this.clubId}/0`
        );
        this.posts = postsData.data.data;
      } catch (error) {
        console.log(error);
        if (error.response.status == 404) {
          this.dataLoaded = true;
        } else {
          this.dataLoaded = null;
        }
      }
    },

    // Function to load more posts
    async loadMorePosts() {
      try {
        // Get more posts
        const postsData = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/club/getClubPosts/${this.clubId}/${
            this.posts[this.posts.length - 1].id
          }`
        );
        this.posts = this.posts.concat(postsData.data.data);

        // Check if there are more posts to load
        if (postsData.data.data.length < 5) {
          this.showButton = false;
        }
      } catch (error) {
        console.log(error);
      }
    },

    // Function to check if the user is a member of the club (used to display join or add post button & to determine admin privileges)
    async checkMembership() {
      try {
        // Get membership status
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/club/checkUserMembership/${this.userID}/${this.userType}/${this.clubId}`
        );

        if (response.data.isRequested) {
          this.hasRequested = true;
        } else if (response.data.isInvited) {
          this.isInvited = true;
        } else {
          this.isMember = response.data.isMember;
          this.isAdmin = response.data.isAdmin;
          this.memberID = response.data.memberID;

          // Store the user's membership status in the local storage
          localStorage.setItem("isMember", this.isMember);
          localStorage.setItem("isAdmin", this.isAdmin);
          localStorage.setItem("memberID", this.memberID);

          // If current user is a member, get the user's likes for the posts
          if (this.isMember) {
            this.getPostLikes();
          }
        }
      } catch (error) {
        // User is not a member
        console.log(error);
      }
    },

    // Function to get the profile URL of the poster
    profileURL(posterID, userType) {
      if (userType == "user") {
        return `/profile/user/${posterID}/${this.username}`;
      } else if (userType == "producer") {
        return `/profile/producer/${posterID}`;
      } else {
        return `/profile/venue/${posterID}`;
      }
    },

    // Function to get the user's likes for the posts (used inside checkMembership function if user is a member)
    async getPostLikes() {
      try {
        // Get likes
        const postLikesData = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/club/getUserLikesPost/${this.memberID}/${this.clubId}`
        );
        this.postLikes = postLikesData.data.liked_posts;
      } catch (error) {
        console.log(error);
      }
    },

    // Function to get first few members
    async getFirstFewMembers() {
      try {
        // Get the first few members
        const membersData = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/club/getFirstFewClubMembers/${this.clubId}`
        );
        this.members = membersData.data.members;
      } catch (error) {
        this.getMemberError = error.response.data.message;
        console.log(error);
      }
    },

    // Function to load all members
    async loadAllMembers() {
      try {
        // Get all members
        const membersData = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/club/getAllClubMembers/${this.clubId}`
        );
        this.members = membersData.data.members;
      } catch (error) {
        this.getMemberError = error.response.data.message;
        console.log(error);
      }
    },

    // Funtion to get data for page end ========================================

    // Helper functions start ==================================================
    // Function to upload images and convert them to base64String for new post
    imageUpload(event) {
      // Get the files
      const files = event.target.files;

      // Loop through the files
      for (let i = 0; i < files.length; i++) {
        // Check if the file is an image
        if (files[i].type.match("image.*")) {
          // Create a file reader
          const reader = new FileReader();

          // Read the file
          reader.readAsDataURL(files[i]);

          // When the file is read
          reader.onload = () => {
            // Push the base64 string to the postPhotos array
            this.newPostPhotos.push(reader.result);
          };
        }
      }
    },

    // Function to remove a photo from the new post
    removePhotoNew(index) {
      this.newPostPhotos.splice(index, 1);
    },

    // Function to remove a photo from the selected post
    removePhoto(index) {
      this.selectedPostEdit.postPhotos.splice(index, 1);
    },

    // Function to upload images and convert them to base64String for editing a post
    imageUploadEdit(event) {
      // Get the files
      const files = event.target.files;

      // Loop through the files
      for (let i = 0; i < files.length; i++) {
        // Check if the file is an image
        if (files[i].type.match("image.*")) {
          // Create a file reader
          const reader = new FileReader();

          // Read the file
          reader.readAsDataURL(files[i]);

          // When the file is read
          reader.onload = () => {
            // Push the base64 string to the postPhotos array
            this.selectedPostEdit.postPhotos.push(reader.result);
          };
        }
      }
    },

    // Functio to close the club settings component
    closeSettings() {
      this.editClub = false;
    },
    // Helper functions end ====================================================

    // Functions that are triggered by user actions start ======================
    // Function to like a post
    async likePost(postID) {
      try {
        // Like the post
        const likeData = await this.$axios.put(
          `${process.env.VUE_APP_API_URL}/club/likeUnlikePost`,
          {
            postID: postID,
            memberID: this.memberID,
            clubID: this.clubId,
          }
        );

        // Get the post object from the posts array
        const post = this.posts.find((post) => post.id == postID);

        // Check if the post is liked
        if (likeData.data.liked) {
          this.postLikes.push(postID);

          // Increase the total likes of the post by 1
          post.totalLikes += 1;
        } else {
          // If is liked before, Get the current index of the postID in the postLikes array
          const index = this.postLikes.indexOf(postID);

          // If the postID is found, remove it from the array [index is -1 if not found]
          if (index > -1) {
            this.postLikes.splice(index, 1);
          }

          // Decrease the total likes of the post by 1
          post.totalLikes -= 1;
        }
      } catch (error) {
        console.log(error);
      }
    },

    async requestToJoin() {
      try {
        // Disable the button to prevent multiple clicks
        this.disableButton = true;

        // Request to join the club
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/club/requestToJoinClub`,
          {
            userID: this.userID,
            clubID: this.clubId,
            userType: this.userType,
          }
        );

        if (response.status == 201) {
          this.hasRequested = true;

          // Show a success message in a toast
          const toast = useToast();
          toast.success(
            "Your request to join the club has been sent! Please wait for the club admin to approve your request."
          );
        }
      } catch (error) {
        console.log(error);
      }
      this.disableButton = false;
    },

    // Function to join the club
    async joinClub() {
      // Check if the user is logged in
      if (this.userType == "defaultUser") {
        // Redirect to login page
        this.$router.push("/login");
        return;
      }

      try {
        // Disable the button to prevent multiple clicks
        this.disableButton = true;

        // Join the club
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/club/joinClub`,
          {
            userID: this.userID,
            clubID: this.clubId,
            userType: this.userType,
          }
        );

        if (response.status == 201) {
          this.isMember = true;
          this.checkMembership();

          // Increase the total members of the club by 1
          this.clubInfo.totalMembers += 1;

          // Show a success message in a toast
          const toast = useToast();
          toast.success("You have successfully joined the club! Welcome!");
        }
      } catch (error) {
        console.log(error);
      }

      this.disableButton = false;
    },

    // Function to accept the invitation to join the club
    async acceptInvite() {
      try {
        // Disable the button to prevent multiple clicks
        this.disableButton = true;

        // Accept the invitation
        const response = await this.$axios.put(
          `${process.env.VUE_APP_API_URL}/club/acceptClubInvite`,
          {
            userID: this.userID,
            userType: this.userType,
            clubID: this.clubId,
          }
        );

        if (response.status == 200) {
          this.isMember = true;
          this.checkMembership();

          // Increase the total members of the club by 1
          this.clubInfo.totalMembers += 1;

          // Show a success message in a toast
          const toast = useToast();
          toast.success(
            "You have successfully accepted the invitation to join the club! Welcome!"
          );
        }
      } catch (error) {
        console.log(error);
      }
      this.disableButton = false;
    },

    // Function to leave the club
    async leaveClub() {
      try {
        // Disable the button to prevent multiple clicks
        this.disableButton = true;

        // Leave the club
        const response = await this.$axios.delete(
          `${process.env.VUE_APP_API_URL}/club/leaveClub`,
          {
            data: {
              memberID: this.memberID,
              clubID: this.clubId,
            },
          }
        );

        if (response.status == 200) {
          this.isMember = false;

          // Decrease the total members of the club by 1
          this.clubInfo.totalMembers -= 1;

          this.isMember = false;

          // Show a success message in a toast
          const toast = useToast();
          toast.success(
            "You have successfully left the club! It's sad to see you go!"
          );
        }
      } catch (error) {
        console.log(error);
      }
      // Ensure overflow is not hidden on the body
      document.body.style.overflow = "auto";
      this.disableButton = false;
    },

    // Function to add a post
    async addPost() {
      try {
        // Format data to be sent
        let postData = {
          clubID: this.clubId,
          posterID: this.memberID,
          postContent: this.newPostContent,
        };

        // Check if there are photos to be added
        if (this.newPostPhotos.length > 0) {
          postData.images = this.newPostPhotos;
        }

        // Add the post
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/club/addPost`,
          postData
        );
        if (response.status == 201) {
          // Reset the new post content and photos
          this.newPostContent = null;
          this.newPostPhotos = [];

          // Reload the posts
          this.getPosts();

          // Show a success message in a toast
          const toast = useToast();
          toast.success("Post added successfully!");
        }
      } catch (error) {
        console.log(error);
        alert("An error occurred while adding the post, please try again!");

        // Reload the page
        window.location.reload();
      }
    },

    // Function to edit a post
    async editPost() {
      try {
        // Format data to be sent
        let postData = {
          postID: this.selectedPostEdit.id,
          postContent: this.selectedPostEdit.postContent,
          editorID: this.memberID,
          images: this.selectedPostEdit.postPhotos,
        };

        // Edit the post
        const response = await this.$axios.put(
          `${process.env.VUE_APP_API_URL}/club/editPost`,
          postData
        );
        if (response.status == 200) {
          // Reload the posts
          this.getPosts();

          // Show a success message in a toast
          const toast = useToast();
          toast.success("Post edited successfully!");
        }
      } catch (error) {
        console.log(error);
        alert("An error occurred while editing the post, please try again!");
      }
    },

    // Function to delete a post
    async deletePost() {
      try {
        // Format the data to be sent
        let deleteData = {
          postID: this.selectedPostDelete.id,
          removerID: this.memberID,
        };

        // Delete the post
        const response = await this.$axios.delete(
          `${process.env.VUE_APP_API_URL}/club/removePost`,
          {
            data: deleteData,
          }
        );
        if (response.status == 200) {
          // Reload the posts
          this.getPosts();

          // Show a success message in a toast
          const toast = useToast();
          toast.success("Post deleted successfully!");
        }
      } catch (error) {
        console.log(error);
        alert("An error occurred while deleting the post, please try again!");
      }
    },

    // Function to open the post
    openPost(postID) {
      this.$router.push(`/club/${this.clubId}/post/${postID}`);
    },
  },

  mounted() {
    // Get club id from the URL
    this.clubId = this.$route.params.clubID;
    // Get the account id and type of the user
    this.userID = localStorage.getItem("88B_accID");
    let userType = localStorage.getItem("88B_accType");
    this.username = localStorage.getItem("88B_accUsername");

    if (userType) {
      this.userType = userType;
    } else {
      this.userType = "defaultUser";
    }

    this.getPageData();

    if (this.userID && this.userType != "defaultUser") {
      this.checkMembership();
    }
  },
};
</script>

<style scoped>
.custom-close-btn {
  background-color: transparent;
  border: none;
  opacity: 1;
  padding: 0;
  cursor: pointer;
}

.name-container {
  max-width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
}
</style>
