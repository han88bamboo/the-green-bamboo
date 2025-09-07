<template>
  <div 
    class="modal fade show" 
    tabindex="-1" 
    style="display: block; background: rgba(0,0,0,0.5);"
  >
    <div class="modal-dialolg modal-lg">
      <div class="modal-content">

        <!-- Modal Title and x button -->
        <div class="modal-header">
          <h5 class="modal-title">Comments for Review</h5>
          <button 
            type="button" 
            class="btn-close" 
            @click="$emit('close')"
          ></button>
        </div>

        <!-- Modal Body -->
        <div class="modal-body">
        
          <div v-for="comment in comments" :key="comment.id" class="mb-3">
            <CommentBox 
              :comment="comment" :userID="userID" :userType="userType" 
              :contentId="contentId" contentType="Review" 
              @set-delete-comment="deleteCommentItems = $event" 
              @comment-replied="handleReply"
            />
          </div>


          <p v-if="comments.length === 0">No comments yet.</p>
        </div>
        <div class="modal-footer">
          <button 
            type="button" 
            class="btn btn-secondary" 
            @click="$emit('close')"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CommentBox from './CommentBox.vue';
import { useToast } from "vue-toastification";

export default {
    name: "CommentsModal",
    components: {
        CommentBox
    },
    props: {
        userID: {
            type: [String, Number],
            required: true
        },
        userType: {
            type: String,
            required: true
        },
        contentId: {
            type: [String, Number],
            required: true
        },
        contentType: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            comments: [], // This will hold the comments for the review
            lastCommentID: null,
            hasMoreComments: false,
        };
    },
    methods: {

        // Function to fetch comments for the given contentId
        async fetchComments() {

            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/randomContent/getReviewComments/${this.userID}/${this.contentId}`
                );
                this.comments = response.data.comments;
                this.lastCommentID = response.data.lastCommentId;
                this.hasMoreComments = this.comments.length == 30;
            } catch (error) {
                console.error("Error fetching comments:", error);
            }

        },

        // Recursive helper to remove a comment or reply by ID
        removeCommentById(commentId, commentsArray) {
        for (let i = 0; i < commentsArray.length; i++) {
            const comment = commentsArray[i];

            // If this is the comment we want to remove
            if (comment.id === commentId) {
            commentsArray.splice(i, 1); // reactive removal
            return true; // stop searching
            }

            // If it has replies, search recursively
            if (comment.replies?.length) {
            const removed = this.removeCommentById(commentId, comment.replies);
            if (removed) return true;
            }
        }
        return false; // comment not found
        },

        // Function to delete comment 
        async deleteComment() {

            try {
                const response = await this.$axios.delete(
                `${process.env.VUE_APP_API_URL}/randomContent/deleteComment`,
                {
                    data: {
                        userId: this.userID,
                        userType: this.userType,
                        contentType: this.deleteCommentItems.contentType,
                        commentId: this.deleteCommentItems.commentId
                    }
                }
                );

                // Show message
                if (response.status === 200) {
                    const toast = useToast();
                    toast.success("Comment deleted successfully.");

                    // Remove the comment or reply from the comments array
                    this.removeCommentById(this.deleteCommentItems.commentId, this.comments);

                    // Reset deleteCommentItems
                    this.deleteCommentItems = {
                        commentId: null,
                        contentType: null
                    };

                }

            } catch (error) {
                console.error("Error deleting comment:", error);
                const toast = useToast();
                toast.error("Failed to delete comment. Please try again later.");
            }
        },

        // Function to add reply to a comment
        handleReply({ parentId, reply }) {
        // Find the parent comment
        const parent = this.comments.find(c => c.id == parentId);
        if (parent) {
            parent.replies.unshift(reply);
        }
        },
    },
    mounted() {
        this.fetchComments();
    }
}
</script>
