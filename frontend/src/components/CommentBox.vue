<template>
    <!-- Commenter Photo Section -->
    <div class="col-auto me-3">
        <router-link
            :to="{
            path: getProfileLink(comment.userId, comment.userType, comment.username)
            }"
            class="primary-clickable-text"
        >
            <img
            v-if="comment.photo"
            :src="comment.photo"
            class="rounded-circle"
            alt="Profile Photo"
            width="30"
            height="30"
            style="object-fit: cover;"
            />
            <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            width="30"
            height="30"
            fill="currentColor"
            class="bi bi-person-circle"
            viewBox="0 0 16 16"
            style="object-fit: cover;"
            >
            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
            <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
            </svg>
        </router-link>
    </div>
    
    <!-- Comment Box-->
    <div class="col bg-light rounded p-2">

        <!-- Row 1: User Name-->
        <div class="d-flex align-items-start">
            <!-- User name and comment date diff at the top left corner -->
            <span>
                <!-- User name-->
                <router-link
                :to="{ path: getProfileLink(comment.userId, comment.userType, comment.username) }"
                class="primary-clickable-text"
                >
                    <b>@{{ comment.username }}</b>
                </router-link>

                <!-- Comment date diff-->
                <span class="text-muted ms-2" style="font-size: 0.8em;">
                    {{ getTimeDifference(comment.createdAt) }}
                </span>

            </span>
            
            <!-- Edit and Delete Button at the top right corner-->
            <div v-if="isCommentOwner(comment.userId, comment.userType)" class="ms-auto">
                <i class="bi bi-pencil me-4" style="cursor:pointer" @click="editMode = true"></i>

                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16" style="cursor:pointer" @click="$emit('set-delete-comment', { commentId: comment.id, contentType: contentType })">
                    <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0"/>
                </svg>
            </div>
        </div>

        <!-- Row 2: Comment Text-->
        <div class="row mt-2">
            <span>{{ comment.comment }}</span>

            <!-- Edit comment input -->
            <div v-if="editMode" class="mt-2">
                <input
                    v-model="updatedComment"
                    @keyup.enter="editComment(comment)"
                    type="text"
                    class="form-control"
                />
                <div class="d-flex justify-content-end mt-2">
                    <button @click="editComment(comment, contentType)" class="btn btn-primary mt-2">Update</button>
                    <button @click="editMode = false" class="btn btn-secondary mt-2 ms-2">Cancel</button>
                </div>
            </div>
        </div>

        <!-- Row 3: Reply Input -->
        <div v-if="!hideReply" class="row mt-3">

            <!-- Reply button as word -->
            <div v-if="!replyMode" class="mt-0 pt-0" style="cursor: pointer; font-size: 0.9em; color: #0d6efd;">
                <span @click="replyMode = !replyMode">Reply</span>
            </div>

            <!-- Reply Input -->
            <div v-if="replyMode" class="col">
                <input v-model="replyContent" class="form-control" placeholder="Write a reply..." />
                <div class="d-flex justify-content-end mt-2">
                    <button @click="postReply(comment.id)" class="btn btn-primary">Reply</button>
                    <button @click="replyContent = '', replyMode = false" class="btn btn-secondary ms-2">Cancel</button>
                </div>
            </div>
        </div>

        <!-- Row 4: Reply Section-->
        <div v-if="comment.replies && comment.replies.length > 0" class="replies-container mt-3">
            <div 
                v-for="reply in comment.replies" 
                :key="reply.id" 
                class="reply-item mb-3"
            >
                <CommentBox 
                    :comment="reply" 
                    :userID="userID" 
                    :userType="userType" 
                    :contentId="contentId" 
                    :hideReply="true"
                    :contentType="contentType"
                    @set-delete-comment="$emit('set-delete-comment', $event)"
                />
            </div>
        </div>

    </div>

</template>


<script>
import { useToast } from "vue-toastification";

export default {
    name: "CommentBox",
    props: {
        comment: {
            type: Array,
            required: true
        },
        userID: {
            type: String,
            required: false
        },
        userType: {
            type: String,
            required: false
        },
        contentId: {
            type: String,
            required: false
        },
        contentType: {
            type: String,
            required: false
        },
        hideReply: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            editMode: false,
            updatedComment: this.comment.comment,

            deleteCommentItems: {
                commentId: null,
                contentType: null
            },

            replyMode: false,
            replyContent: "",
        };
    },
    methods: {
        //remove %20 from url
        slugify(text) {
            if (!text) return "";
            return text
                .toString()
                .toLowerCase()
                .replace(/\s+/g, '')
                .replace(/[^\w]/g, '');
        },

        // Function to get time difference in human-readable format
        getTimeDifference(date) {
            let currentDate = new Date();
            let updateDate = new Date(date);
            let timeDifference = currentDate - updateDate;
            let seconds = Math.floor(timeDifference / 1000);
            let minutes = Math.floor(seconds / 60);
            let hours = Math.floor(minutes / 60);
            let days = Math.floor(hours / 24);
            let months = Math.floor(days / 30);
            let years = Math.floor(months / 12);
            if (years > 0) {
                return years + (years === 1 ? " year ago" : " years ago");
            } else if (months > 0) {
                return months + (months === 1 ? " month ago" : " months ago");
            } else if (days > 0) {
                return days + (days === 1 ? " day ago" : " days ago");
            } else if (hours > 0) {
                return hours + (hours === 1 ? " hour ago" : " hours ago");
            } else if (minutes > 0) {
                return minutes + (minutes === 1 ? " minute ago" : " minutes ago");
            } else {
                return seconds + (seconds === 1 ? " second ago" : " seconds ago");
            }
        },

        // Function to get profileLink based on userType
        getProfileLink(userId, userType, name) {

            switch (userType) {
                case 'user':
                return `/profile/user/${userId}/${this.slugify(name)}`;
                case 'producer':
                return `/profile/producer/${userId}/${this.slugify(name)}`;
                case 'venue':
                return `/profile/venue/${userId}/${this.slugify(name)}`;
                default:
                return null;
            }
        },

        // Function to check if comment is made by current user
        isCommentOwner(commentUserId, commentUserType) {
            return this.userID == commentUserId && this.userType == commentUserType;
        },

        // Function to edit comment 
        async editComment(comment, contentType) {

            // Check if updatedComment is empty
            if (!this.updatedComment || this.updatedComment.trim() === "") {
                const toast = useToast();
                toast.error("Comment cannot be empty.");
                return;
            }

            // Check if updatedComment is different from the original comment
            if (this.updatedComment.trim() === comment.comment.trim()) {
                const toast = useToast();
                toast.error("Comment is identical to the original.");
                return;
            }

            try {
                const response = await this.$axios.put(
                `${process.env.VUE_APP_API_URL}/randomContent/editComment`,
                {
                    userId: this.userID,
                    userType: this.userType,
                    contentType: contentType,
                    commentId: comment.id,
                    newComment: this.updatedComment.trim()
                }
                );

                if (response.status === 201) {
                    this.updatedComment = "";

                    // Update the comment in the UI
                    comment.comment = response.data.newComment

                    // Exit edit mode
                    this.editMode = false;

                    // Show message
                    const toast = useToast();
                    toast.success("Comment updated successfully.");
                }

            } catch (error) {
                console.error("Error editing comment:", error);
                const toast = useToast();
                toast.error("Failed to edit comment. Please try again later.");
            }
        },

        // Function to post a reply to a comment
        async postReply() {
            console.log("Posting reply to comment ID:", this.comment.id);
            console.log("Reply content:", this.replyContent);
            // Check if user is logged in
            if (!this.userID || !this.userType) {
                // Redirect to login page
                this.$router.push({ path: "/login" });
                return;
            }

            // Check if replyContent is empty
            if (!this.replyContent || this.replyContent.trim() === "") {
                const toast = useToast();
                toast.error("Reply cannot be empty.");
                return;
            }

            try {
                const response = await this.$axios.post(
                `${process.env.VUE_APP_API_URL}/randomContent/addComment`,
                {
                    userId: this.userID,
                    userType: this.userType,
                    contentType: this.contentType,
                    contentId: this.contentId,
                    comment: this.replyContent.trim(),
                    parentId: this.comment.id
                }
                );

                if (response.status === 201) {
                    // Clear the reply input
                    this.replyContent = "";
                    this.replyMode = false;

                    // Show message
                    const toast = useToast();
                    toast.success("Reply posted successfully.");

                    // Emit event to parent to refresh comments
                    this.$emit("comment-replied", { parentId: this.comment.id, reply: response.data.comment } );
                }

            } catch (error) {
                console.error("Error posting reply:", error);
                const toast = useToast();
                toast.error("Failed to post reply. Please try again later.");
            }
        },

    }
};
</script>

<style scoped>
.replies-container {
  position: relative;
  padding-left: 1.5rem; /* space for the vertical line */
}

.replies-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0.5rem; /* horizontal position of the line */
  width: 2px;   /* line thickness */
  height: 100%;
  background-color: #ccc; /* light gray line */
  border-radius: 2px;     /* optional rounding */
}

.reply-item {
  margin-left: 1rem; /* nested replies are indented */
}

</style>