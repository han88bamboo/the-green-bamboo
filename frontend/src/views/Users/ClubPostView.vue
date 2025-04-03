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
            <!-- Green thumbs up with green fill if user already liked the post -->
            <p
              v-if="post.likedMembers.includes(Number(memberID))"
              data-bs-toggle="tooltip"
              data-bs-placement="top"
              title="Unlike"
              class="cursor-pointer"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                fill="green"
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

            <!-- Total likes counter -->
            {{ totalLikes }} Likes 

            <!-- Red thumbs down with red fill if user already disliked the post -->
            <p
              v-if="post.dislikedMembers.includes(Number(memberID))"
              data-bs-toggle="tooltip"
              data-bs-placement="top"
              title="Undislike"
              class="cursor-pointer"
            >
            <svg
              xmlns="http://www.w3.org/2000/svg" 
              width="24" 
              height="24" 
              fill="red" 
              class="bi bi-hand-thumbs-down-fill" 
              viewBox="0 0 16 16"
              style="cursor: pointer"
              @click="dislikePost(post.id)">
                <path d="M6.956 14.534c.065.936.952 1.659 1.908 1.42l.261-.065a1.38 1.38 0 0 0 1.012-.965c.22-.816.533-2.512.062-4.51q.205.03.443.051c.713.065 1.669.071 2.516-.211.518-.173.994-.68 1.2-1.272a1.9 1.9 0 0 0-.234-1.734c.058-.118.103-.242.138-.362.077-.27.113-.568.113-.856 0-.29-.036-.586-.113-.857a2 2 0 0 0-.16-.403c.169-.387.107-.82-.003-1.149a3.2 3.2 0 0 0-.488-.9c.054-.153.076-.313.076-.465a1.86 1.86 0 0 0-.253-.912C13.1.757 12.437.28 11.5.28H8c-.605 0-1.07.08-1.466.217a4.8 4.8 0 0 0-.97.485l-.048.029c-.504.308-.999.61-2.068.723C2.682 1.815 2 2.434 2 3.279v4c0 .851.685 1.433 1.357 1.616.849.232 1.574.787 2.132 1.41.56.626.914 1.28 1.039 1.638.199.575.356 1.54.428 2.591"/>
              </svg>
            </p>

            <!-- Black thumbs down with no fill if user has not disliked the post -->
            <p
              v-else
              data-bs-toggle="tooltip"
              data-bs-placement="top"
              title="DisLike"
              class="cursor-pointer"
              >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                width="24" 
                height="24" 
                fill="black" 
                class="bi bi-hand-thumbs-down" 
                viewBox="0 0 16 16"
                style="cursor: pointer"
                @click="dislikePost(post.id)">
                  <path d="M8.864 15.674c-.956.24-1.843-.484-1.908-1.42-.072-1.05-.23-2.015-.428-2.59-.125-.36-.479-1.012-1.04-1.638-.557-.624-1.282-1.179-2.131-1.41C2.685 8.432 2 7.85 2 7V3c0-.845.682-1.464 1.448-1.546 1.07-.113 1.564-.415 2.068-.723l.048-.029c.272-.166.578-.349.97-.484C6.931.08 7.395 0 8 0h3.5c.937 0 1.599.478 1.934 1.064.164.287.254.607.254.913 0 .152-.023.312-.077.464.201.262.38.577.488.9.11.33.172.762.004 1.15.069.13.12.268.159.403.077.27.113.567.113.856s-.036.586-.113.856c-.035.12-.08.244-.138.363.394.571.418 1.2.234 1.733-.206.592-.682 1.1-1.2 1.272-.847.283-1.803.276-2.516.211a10 10 0 0 1-.443-.05 9.36 9.36 0 0 1-.062 4.51c-.138.508-.55.848-1.012.964zM11.5 1H8c-.51 0-.863.068-1.14.163-.281.097-.506.229-.776.393l-.04.025c-.555.338-1.198.73-2.49.868-.333.035-.554.29-.554.55V7c0 .255.226.543.62.65 1.095.3 1.977.997 2.614 1.709.635.71 1.064 1.475 1.238 1.977.243.7.407 1.768.482 2.85.025.362.36.595.667.518l.262-.065c.16-.04.258-.144.288-.255a8.34 8.34 0 0 0-.145-4.726.5.5 0 0 1 .595-.643h.003l.014.004.058.013a9 9 0 0 0 1.036.157c.663.06 1.457.054 2.11-.163.175-.059.45-.301.57-.651.107-.308.087-.67-.266-1.021L12.793 7l.353-.354c.043-.042.105-.14.154-.315.048-.167.075-.37.075-.581s-.027-.414-.075-.581c-.05-.174-.111-.273-.154-.315l-.353-.354.353-.354c.047-.047.109-.176.005-.488a2.2 2.2 0 0 0-.505-.804l-.353-.354.353-.354c.006-.005.041-.05.041-.17a.9.9 0 0 0-.121-.415C12.4 1.272 12.063 1 11.5 1"/>
              </svg>
            </p>

            <!-- Total dislikes counter -->
            {{ post.dislikedMembers.length }} Dislikes
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
                  <div class="col-12 d-flex gap-4">
                    <!-- Red thumbs up with red fill if user already liked the post -->
                    <p
                      v-if="comment.likedMembers.includes(memberID)"
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
                        @click="likeComment(comment.id)"
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
                        @click="likeComment(comment.id)"
                      >
                        <path
                          d="M8.864.046C7.908-.193 7.02.53 6.956 1.466c-.072 1.051-.23 2.016-.428 2.59-.125.36-.479 1.013-1.04 1.639-.557.623-1.282 1.178-2.131 1.41C2.685 7.288 2 7.87 2 8.72v4.001c0 .845.682 1.464 1.448 1.545 1.07.114 1.564.415 2.068.723l.048.03c.272.165.578.348.97.484.397.136.861.217 1.466.217h3.5c.937 0 1.599-.477 1.934-1.064a1.86 1.86 0 0 0 .254-.912c0-.152-.023-.312-.077-.464.201-.263.38-.578.488-.901.11-.33.172-.762.004-1.149.069-.13.12-.269.159-.403.077-.27.113-.568.113-.857 0-.288-.036-.585-.113-.856a2 2 0 0 0-.138-.362 1.9 1.9 0 0 0 .234-1.734c-.206-.592-.682-1.1-1.2-1.272-.847-.282-1.803-.276-2.516-.211a10 10 0 0 0-.443.05 9.4 9.4 0 0 0-.062-4.509A1.38 1.38 0 0 0 9.125.111zM11.5 14.721H8c-.51 0-.863-.069-1.14-.164-.281-.097-.506-.228-.776-.393l-.04-.024c-.555-.339-1.198-.731-2.49-.868-.333-.036-.554-.29-.554-.55V8.72c0-.254.226-.543.62-.65 1.095-.3 1.977-.996 2.614-1.708.635-.71 1.064-1.475 1.238-1.978.243-.7.407-1.768.482-2.85.025-.362.36-.594.667-.518l.262.066c.16.04.258.143.288.255a8.34 8.34 0 0 1-.145 4.725.5.5 0 0 0 .595.644l.003-.001.014-.003.058-.014a9 9 0 0 1 1.036-.157c.663-.06 1.457-.054 2.11.164.175.058.45.3.57.65.107.308.087.67-.266 1.022l-.353.353.353.354c.043.043.105.141.154.315.048.167.075.37.075.581 0 .212-.027.414-.075.582-.05.174-.111.272-.154.315l-.353.353.353.354c.047.047.109.177.005.488a2.2 2.2 0 0 1-.505.805l-.353.353.353.354c.006.005.041.05.041.17a.9.9 0 0 1-.121.416c-.165.288-.503.56-1.066.56z"
                        />
                      </svg>
                    </p>

                    <!-- Total likes counter -->
                    {{ comment.likedMembers.length }} Likes
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
          `${process.env.VUE_APP_API_URL}/club/likeUnlikePost`,
          {
            postID: postID,
            memberID: this.memberID,
            clubID: this.clubID,
          }
        );

        // Check if the post is disliked
        if (dislikeData.data.disliked) {
          this.post.dislikedMembers.push(this.memberID);
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
