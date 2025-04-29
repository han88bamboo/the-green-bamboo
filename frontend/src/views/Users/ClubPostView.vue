<template>
  <div class="mb-3">
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

    <!-- Main content -->
    <div v-if="dataLoaded == true">
      <!-- Display the post -->
      <div class="container mt-3 text-start">
        <!-- Row 1: Poster Photo, Poster Name, Post Date -->
        <div class="row">
          <!-- Column 1: Poster Photo -->
          <div class="col-12 col-md-1 d-flex align-items-center">
            <img
              v-if="poster.profile_photo"
              :src="poster.profile_photo"
              class="rounded-circle"
              alt="Profile Photo"
              width="50"
              height="50"
            />
            <svg
              v-else
              xmlns="http://www.w3.org/2000/svg"
              width="50"
              height="50"
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

          <!-- Column 2: Poster Name and Post Date -->
          <div class="col-11">
            <h3>{{ poster.displayName }}</h3>
            <p class="text-muted">{{ post.postDate }}</p>
          </div>
        </div>

        <!-- Row 2: Post Photo if have -->
        <div v-if="post.postPhotos.length > 0" class="row">
          <div class="col-12">
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

        <!-- Row 3: Post Content -->
        <div class="row mt-3">
          <div class="col-12">
            <p>{{ post.postContent }}</p>
          </div>
        </div>
        <!-- Row 4: Like Button -->
        <div v-if="isMember" class="row text-start">
          <div class="col-12 d-flex gap-4">
            <!-- Black arrow up if user already like post (aka upvote) -->
            <p
              v-if="post.likedMembers.includes(memberID)"
              data-bs-toggle="tooltip"
              data-bs-placement="top"
              title="Un-upvote"
              class="cursor-pointer"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                fill="currentColor"
                class="bi bi-caret-up-fill"
                viewBox="0 0 16 16"
                style="cursor: pointer"
                @click="likePost(post.id)"
              >
                <path d="m7.247 4.86-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
              </svg>
            </p>

            <!-- Black hollow thumbs up with no fill if user has not liked the post -->
            <p
              v-else
              data-bs-toggle="tooltip"
              data-bs-placement="top"
              title="Upvote"
              class="cursor-pointer"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                fill="currentColor"
                class="bi bi-caret-up"
                viewBox="0 0 16 16"
                style="cursor: pointer"
                @click="likePost(post.id)"
              >
                <path d="M3.204 11h9.592L8 5.519zm-.753-.659 4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659"/>
              </svg>
            </p>

            <!-- Net vote counter -->
            {{ totalLikes - post.dislikedMembers.length }}  

            <!-- Black arrow down if user already dislike the post (aka downvote) -->
            <p
              v-if="post.dislikedMembers.includes(memberID)"
              data-bs-toggle="tooltip"
              data-bs-placement="top"
              title="Un-downvote"
              class="cursor-pointer"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg" 
                width="24" 
                height="24" 
                fill="currentColor" 
                class="bi bi-caret-down-fill me-3"
                viewBox="0 0 16 16"
                style="cursor: pointer"
                @click="dislikePost(post.id)">
                <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
              </svg>
            </p>

            <!-- Black hollow arrow down if user has not disliked the post -->
            <p
              v-else
              data-bs-toggle="tooltip"
              data-bs-placement="top"
              title="Downvote"
              class="cursor-pointer"
              >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                width="24" 
                height="24" 
                fill="black" 
                class="bi bi-caret-down me-3"
                viewBox="0 0 16 16"
                style="cursor: pointer"
                @click="dislikePost(post.id)">
                <path d="M3.204 5h9.592L8 10.481zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659"/>
              </svg>
            </p>

          </div>
        </div>

        <!-- Row 5: Comment input -->
        <div v-if="isMember" class="row mt-3">
          <div class="col-12">
            <div class="input-group">
              <input
                type="text"
                class="form-control"
                placeholder="Write a comment..."
                aria-label="Write a comment..."
                aria-describedby="button-addon2"
                v-model="newComment"
              />
              <button
                class="btn primary-btn"
                type="button"
                id="button-addon2"
                @click="addComment"
              >
                Comment
              </button>
            </div>
          </div>
        </div>

        <!-- Row 6: Comments -->
        <div class="row mt-3">
          <h5 class="text-decoration-underline">Comments:</h5>
          <div v-if="comments.length > 0">
            <div v-for="comment in comments" :key="comment.id" class="row mt-3">
              <!-- Column 1: Commenter Photo -->
              <div class="col-12 col-md-1 d-flex flex-column align-items-start">
                <img
                  v-if="comment.commenterInfo.photo"
                  :src="comment.commenterInfo.photo"
                  class="rounded-circle"
                  alt="Profile Photo"
                  width="40"
                  height="40"
                />
                <svg
                  v-else
                  xmlns="http://www.w3.org/2000/svg"
                  width="40"
                  height="40"
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

              <div class="col-11">
                <!-- Column 2 Row 1: Commenter Name and Comment Date -->
                <div class="row text-start d-flex align-items-center ps-0">
                  <div class="col-md-3">
                    <router-link
                      :to="
                        profileURL(
                          comment.commenterInfo.id,
                          comment.commenterInfo.userType
                        )
                      "
                      class="text-black"
                    >
                      <p
                        v-if="comment.commenterInfo.userType == 'user'"
                        class="fw-bold"
                      >
                        {{ comment.commenterInfo.displayName }}
                      </p>
                      <p
                        v-else-if="comment.commenterInfo.userType == 'producer'"
                        class="fw-bold"
                      >
                        {{ comment.commenterInfo.producerName }}
                      </p>
                      <p v-else class="fw-bold">
                        {{ comment.commenterInfo.venueName }}
                      </p>
                    </router-link>
                  </div>
                  <div class="col-md-5">
                    <p>{{ comment.commentDate }}</p>
                  </div>
                  <div class="col-md-4 text-end">
                    <button
                      v-if="comment.commenterID == memberID || isAdmin"
                      class="btn primary-btn-green btn-sm me-3"
                      data-bs-toggle="modal"
                      data-bs-target="#editCommentModal"
                      @click="selectedComment = deepCopy(comment)"
                    >
                      Edit
                    </button>
                    <button
                      v-if="comment.commenterID == memberID || isAdmin"
                      class="btn primary-btn-red btn-sm"
                      data-bs-toggle="modal"
                      data-bs-target="#deleteCommentModal"
                      @click="selectedCommentDelete = deepCopy(comment)"
                    >
                      Delete
                    </button>
                  </div>
                </div>

                <!-- Column 2 Row 2: Comment -->
                <div class="row">
                  <p>{{ comment.commentContent }}</p>
                </div>

                <!-- Column 2 Row 3: Comment's like button and total likes -->
                <div class="row d-flex align-items-center">
                  <div class="col-12 d-flex gap-4" >

                    <!-- Black arrow up if user already like comment (aka upvote) -->
                    <p
                      v-if="comment.likedMembers.includes(memberID)"
                      data-bs-toggle="tooltip"
                      data-bs-placement="top"
                      title="Un-upvote"
                      class="cursor-pointer"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        fill="currentColor"
                        class="bi bi-caret-up-fill"
                        viewBox="0 0 16 16"
                        style="cursor: pointer"
                        @click="likeComment(comment.id)"
                      >
                      <path d="m7.247 4.86-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
                      </svg>
                    </p>

                    <!-- Black hollow thumbs up with no fill if user has not liked the comment -->
                    <p
                      v-else
                      data-bs-toggle="tooltip"
                      data-bs-placement="top"
                      title="Upvote"
                      class="cursor-pointer"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        fill="currentColor"
                        class="bi bi-caret-up"
                        viewBox="0 0 16 16"
                        style="cursor: pointer"
                        @click="likeComment(comment.id)"
                      >
                        <path d="M3.204 11h9.592L8 5.519zm-.753-.659 4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659"/>
                      </svg>
                    </p>

                    <!-- Net vote counter -->
                    {{ comment.likedMembers.length - comment.dislikedMembers.length }} 
                    

                    <!-- Black arrow down if user already dislike the post (aka downvote) -->
                    <p
                      v-if="comment.dislikedMembers.includes(memberID)"
                      data-bs-toggle="tooltip"
                      data-bs-placement="top"
                      title="Un-downvote"
                      class="cursor-pointer"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg" 
                        width="24" 
                        height="24" 
                        fill="currentColor" 
                        class="bi bi-caret-down-fill me-3"
                        viewBox="0 0 16 16"
                        style="cursor: pointer"
                        @click="dislikeComment(comment.id)">
                        <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                      </svg>
                    </p>

                    <!-- Black hollow arrow down if user has not disliked the post -->
                    <p
                      v-else
                      data-bs-toggle="tooltip"
                      data-bs-placement="top"
                      title="Downvote"
                      class="cursor-pointer"
                      >
                      <svg 
                        xmlns="http://www.w3.org/2000/svg" 
                        width="24" 
                        height="24" 
                        fill="currentColor" 
                        class="bi bi-caret-down me-3"
                        viewBox="0 0 16 16"
                        style="cursor: pointer"
                        @click="dislikeComment(comment.id)">
                        <path d="M3.204 5h9.592L8 10.481zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659"/>
                      </svg>
                    </p>
                  </div>
                </div>
              </div>

              <!--Edit Comment Modal start -->
              <div
                class="modal fade"
                id="editCommentModal"
                tabindex="-1"
                aria-labelledby="editCommentModalLabel"
                aria-hidden="true"
              >
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="editCommentModalLabel">
                        Edit Comment
                      </h5>
                      <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                      ></button>
                    </div>
                    <div class="modal-body">
                      <textarea
                        v-if="selectedComment"
                        class="form-control"
                        v-model="selectedComment.commentContent"
                      ></textarea>
                    </div>
                    <div class="modal-footer">
                      <button
                        type="button"
                        class="btn btn-secondary"
                        data-bs-dismiss="modal"
                        :disabled="isDisabled"
                      >
                        Close
                      </button>
                      <button
                        type="button"
                        class="btn btn-primary"
                        @click="editComment()"
                        data-bs-dismiss="modal"
                        :disabled="isDisabled"
                      >
                        Save changes
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              <!--Edit Comment Modal end -->

              <!--Delete Comment Modal start -->
              <div
                class="modal fade"
                id="deleteCommentModal"
                tabindex="-1"
                aria-labelledby="deleteCommentModalLabel"
                aria-hidden="true"
              >
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="deleteCommentModalLabel">
                        Delete Comment
                      </h5>
                      <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                      ></button>
                    </div>
                    <div class="modal-body">
                      <p>Are you sure you want to delete this comment?</p>
                    </div>
                    <div class="modal-footer">
                      <button
                        type="button"
                        class="btn btn-secondary"
                        data-bs-dismiss="modal"
                        :disabled="isDisabled"
                      >
                        Close
                      </button>
                      <button
                        type="button"
                        class="btn btn-danger"
                        @click="deleteComment()"
                        data-bs-dismiss="modal"
                        :disabled="isDisabled"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              <!--Delete Comment Modal end -->
            </div>
          </div>

          <div v-else>
            <p>No comments yet.</p>
          </div>
        </div>

        <!-- Row 7: Load more comments button -->
        <div class="row mt-3">
          <div v-if="showButton" class="col-12 d-flex justify-content-center">
            <button class="btn primary-btn" @click="getMoreComments()">
              Load more comments
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import the necessary components
import NavBar from "@/components/NavBar.vue";
import { useToast } from "vue-toastification";

export default {
  name: "ClubPostView",
  data() {
    return {
      // Variables for page loading
      dataLoaded: false,

      // Variables to store user data
      userID: null,
      userType: null,
      memberID: null,
      isMember: false,
      isAdmin: false,

      // Variables to store post data
      clubID: this.$route.params.clubID,
      postID: this.$route.params.postID,
      post: null,
      poster: null,
      comments: [],

      // Variables to store comment data
      newComment: "",

      // Variable to store the showButton value (to show the load more comments button)
      showButton: true,

      // Variable to store disabled value for the edit/delete button
      isDisabled: false,

      // Variable to store the selected comment for editing
      selectedComment: null,

      // Variable to store the selected comment for deletion
      selectedCommentDelete: null,
    };
  },
  components: {
    NavBar,
  },
  computed: {
    totalLikes() {
      if (this.post == null) {
        return 0;
      } else {
        const likeList = this.post.likedMembers;
        return likeList.length;
      }
    },

    totalDislikes() {
      if (this.post == null) {
        return 0;
      } else {
        const dislikeList = this.post.dislikedMembers;
        return dislikeList.length;
      }
    },
  },
  methods: {
    // Function to retrieve the post data from the backend including the latest 20 comments
    async getPostData() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/club/getClubPostDetails/${this.postID}/0`
        );
        this.post = response.data.post_info;
        this.poster = response.data.poster_info;
        this.comments = response.data.comments;

        // Set the dataLoaded variable to true
        this.dataLoaded = true;
      } catch (error) {
        console.log(error);
        this.dataLoaded = null;
      }
    },

    // Function to get the profile URL of the commenter
    profileURL(commenterID, userType) {
      if (userType == "user") {
        return `/profile/user/${commenterID}`;
      } else if (userType == "producer") {
        return `/profile/producer/${commenterID}`;
      } else {
        return `/profile/venue/${commenterID}`;
      }
    },

    // Function to like a post
    async likePost(postID) {
      try {
        // Like the post
        const likeData = await this.$axios.put(
          `${process.env.VUE_APP_API_URL}/club/likeUnlikePost`,
          {
            postID: postID,
            memberID: this.memberID,
            clubID: this.clubID,
          }
        );

        // Check if the post is liked
        if (likeData.data.liked) {
          this.post.likedMembers.push(this.memberID);

          // Check if the post is disliked
          if (this.post.dislikedMembers.includes(this.memberID)) {
            
            // Trigger the dislikePost function to remove the dislike
            await this.dislikePost(postID);
          }

        } else {
          // If is liked before, remove the memberID from the likedMembers array
          const index = this.post.likedMembers.indexOf(this.memberID);
          if (index > -1) {
            this.post.likedMembers.splice(index, 1);
          }
        }
      } catch (error) {
        console.log(error);
      }
    },

    // Function to dislike a post
    async dislikePost(postID) {
      try {
        // Dislike the post
        const dislikeData = await this.$axios.put(
          `${process.env.VUE_APP_API_URL}/club/dislikeUndislikePost`,
          {
            postID: postID,
            memberID: this.memberID,
            clubID: this.clubID,
          }
        );

        // Check if the post is disliked
        if (dislikeData.data.disliked) {
          this.post.dislikedMembers.push(this.memberID);

          // Check if the post is liked
          if (this.post.likedMembers.includes(this.memberID)) {
            
            // Trigger the likePost function to remove the like
            await this.likePost(postID);
          }

        } else {
          // If is disliked before, remove the memberID from the dislikedMembers array
          const index = this.post.dislikedMembers.indexOf(this.memberID);
          if (index > -1) {
            this.post.dislikedMembers.splice(index, 1);
          }
        }
      } catch (error) {
        console.log(error);
      }
    },

    // Function to add comment on a post
    async addComment() {
      try {
        // Comment on the post
        const commentData = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/club/addComment`,
          {
            postID: this.postID,
            commenterID: this.memberID,
            commentContent: this.newComment,
          }
        );

        // Check if the comment is successful
        if (commentData.status == 201) {
          // Add the comment to the front of the comments array
          this.comments.unshift(commentData.data.comment_obj);

          // Clear the comment input
          this.newComment = "";

          const toast = useToast();
          toast.success("Comment added successfully.");
        }
      } catch (error) {
        console.log(error);
        const toast = useToast();
        toast.error(
          "An error occurred while adding the comment. Please try again later."
        );
      }
    },

    // Function to like a comment
    async likeComment(commentID) {
      try {
        // Like the comment
        const likeData = await this.$axios.put(
          `${process.env.VUE_APP_API_URL}/club/likeUnlikeComment`,
          {
            commentID: commentID,
            memberID: this.memberID,
            postID: this.postID,
          }
        );

        // Check if the comment is liked
        if (likeData.data.liked) {
          // Find the comment in the comments array
          const comment = this.comments.find(
            (comment) => comment.id == commentID
          );
          comment.likedMembers.push(this.memberID);

          // Check if the comment is disliked
          if (comment.dislikedMembers.includes(this.memberID)) {
            
            // Trigger the dislikeComment function to remove the dislike
            await this.dislikeComment(commentID);
          }

        } else {
          // If is liked before, remove the memberID from the likedMembers array
          const comment = this.comments.find(
            (comment) => comment.id == commentID
          );
          const index = comment.likedMembers.indexOf(this.memberID);
          if (index > -1) {
            comment.likedMembers.splice(index, 1);
          }
        }
      } catch (error) {
        console.log(error);
      }
    },

    // Function to dislike a comment
    async dislikeComment(commentID) {
      try {
        // Dislike the comment
        const dislikeData = await this.$axios.put(
          `${process.env.VUE_APP_API_URL}/club/dislikeUndislikeComment`,
          {
            commentID: commentID,
            memberID: this.memberID,
            postID: this.postID,
          }
        );

        // Check if the comment is disliked
        if (dislikeData.data.disliked) {
          // Find the comment in the comments array
          const comment = this.comments.find(
            (comment) => comment.id == commentID
          );
          comment.dislikedMembers.push(this.memberID);

          // Check if the comment is liked
          if (comment.likedMembers.includes(this.memberID)) {
            
            // Trigger the likeComment function to remove the like
            await this.likeComment(commentID);
          }

        } else {
          // If is disliked before, remove the memberID from the dislikedMembers array
          const comment = this.comments.find(
            (comment) => comment.id == commentID
          );
          const index = comment.dislikedMembers.indexOf(this.memberID);
          if (index > -1) {
            comment.dislikedMembers.splice(index, 1);
          }
        }
      } catch (error) {
        console.log(error);
      }
    },

    // Function to get more comments
    async getMoreComments() {
      try {
        let latestCommentID = this.comments[this.comments.length - 1].id;
        console.log("latestCommentID:", latestCommentID);
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/club/getClubPostDetails/${this.postID}/${latestCommentID}`
        );
        this.comments = this.comments.concat(response.data.comments);

        // Check if there are more comments to load
        if (response.data.comments.length < 20) {
          this.showButton = false;
        }
      } catch (error) {
        console.log(error);
      }
    },

    // Function to create a deep copy of the selected comment
    deepCopy(obj) {
      return JSON.parse(JSON.stringify(obj));
    },

    // Function to edit a comment
    async editComment() {
      try {
        // Disable the button
        this.isDisabled = true;

        // Edit the comment
        const editData = await this.$axios.put(
          `${process.env.VUE_APP_API_URL}/club/editComment`,
          {
            commentID: this.selectedComment.id,
            commentContent: this.selectedComment.commentContent,
            editorID: this.memberID,
          }
        );

        // Check if the comment is edited
        if (editData.status == 200) {
          // Find the comment in the comments array
          const comment = this.comments.find(
            (comment) => comment.id == this.selectedComment.id
          );
          comment.commentContent = this.selectedComment.commentContent;

          const toast = useToast();
          toast.success("Comment edited successfully.");
        }
      } catch (error) {
        console.log(error);

        const toast = useToast();
        toast.error(
          "An error occurred while editing the comment. Please try again later."
        );
      }
      // Reset disabled value
      this.isDisabled = false;
    },

    // Function to delete a comment
    async deleteComment() {
      try {
        // Delete the comment
        const deleteData = await this.$axios.delete(
          `${process.env.VUE_APP_API_URL}/club/removeComment`,
          {
            data: {
              commentID: this.selectedCommentDelete.id,
              removerID: this.memberID,
            },
          }
        );

        // Check if the comment is deleted
        if (deleteData.status == 200) {
          // Find the comment in the comments array
          const index = this.comments.findIndex(
            (comment) => comment.id == this.selectedCommentDelete.id
          );
          if (index > -1) {
            this.comments.splice(index, 1);
          }

          const toast = useToast();
          toast.success("Comment deleted successfully.");
        }
      } catch (error) {
        console.log(error);

        const toast = useToast();
        toast.error(
          "An error occurred while deleting the comment. Please try again later."
        );
      }
    },
  },
  mounted() {
    // Get the userID and userType from the localStorage
    let userID = localStorage.getItem("88B_accID");
    let userType = localStorage.getItem("88B_accType");

    // Get the user's membership data from the localStorage
    let memberID = localStorage.getItem("memberID");
    memberID = parseInt(memberID, 10);
    let isMember = localStorage.getItem("isMember"); // is string
    let isAdmin = localStorage.getItem("isAdmin"); // is string

    // Check if the user is logged in
    if (userID == null || userType == null) {
      this.$router.push("/login");
    } else {
      this.userID = userID;
      this.userType = userType;
      this.memberID = memberID;

      // Convert isMember and isAdmin to boolean
      this.isMember = isMember === "true";
      this.isAdmin = isAdmin === "true";
      // Call the getPostData function to retrieve the post data
      this.getPostData();
    }
  },
};
</script>
