<!-- Component for bookmark modal. Used in all pages with listings -->

<template>

    <div class="modal fade text-start" id="bookmarkModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">Add {{bookmarkModalItem}} to List</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <div class="form-check" v-for="(listItems, listName) in user.drinkLists" :key="listName">
                    <input class="form-check-input" type="checkbox" :value="listName" :id="listName" 
                        v-model="selectedBookmarkList">
                    <label class="form-check-label" :for="listName">
                        {{listName}}
                    </label>
                </div>

                <div class="form-check mt-3">
                    <input class="form-check-input" type="checkbox" value="saveToNewList" id="saveToNewList" v-model="saveToNewList">
                    <label class="form-check-label" for="saveToNewList">
                        Create New List
                    </label>
                    <div v-if="saveToNewList">
                        <div class="mt-2">New List Name</div>
                        <input type="text" class="form-control" v-model="othersListName" placeholder="New List Name">
                        <div v-if="othersListNameError" class="text-danger text-sm">
                            *{{ othersListNameError }}
                        </div>
                    </div>
                </div>

            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn primary-square" @click="bookmarkItem">Save changes</button>
            </div>
            </div>
        </div>
    </div>
                
</template>

<script>
export default {
  name: "BookmarkModal",
  props: {
    user: Object,
    listingID: Number // Now strictly a number
  },
  data() {
    return {
      userID: '',
      userBookmarks: {},
      bookmarkModalItem: '', // still useful if name is passed later
      selectedBookmarkList: [],
      othersListName: '',
      othersListNameError: '',
      saveToNewList: false,
      validListingId: null
    };
  },
  mounted() {
    if (this.user && Object.keys(this.user).length > 0) {
      this.userID = this.user.id;
      this.userBookmarks = this.user.drinkLists;
    }
  },
  watch: {
    listingID: {
      handler(newVal) {
        console.log("listingID changed to:", newVal);

        if (typeof newVal === 'number') {
          this.validListingId = newVal;
          this.populateBookmarkModal(newVal);
        } else {
          console.error("Invalid listingID (should be a number):", newVal);
        }
      },
      immediate: true
    },
    user: {
      handler() {
        if (this.user && Object.keys(this.user).length > 0) {
          this.userID = this.user.id;
          this.userBookmarks = this.user.drinkLists;
        }
      }
    }
  },
  methods: {
    checkBookmarkStatus(listingID) {
      for (const category of Object.values(this.userBookmarks)) {
        if (category.listItems) {
          if (category.listItems.some(item => parseInt(item?.drinkId) === listingID)) {
            return true;
          }
        }
      }
      return false;
    },

    populateBookmarkModal(listingID) {
      console.log("populateBookmarkModal called with:", listingID);
      this.selectedBookmarkList = [];

      for (const listName in this.userBookmarks) {
        if (Object.prototype.hasOwnProperty.call(this.userBookmarks, listName)) {
          const bookmarkItems = this.userBookmarks[listName].listItems;
          if (bookmarkItems?.some(item => parseInt(item?.drinkId) === listingID)) {
            this.selectedBookmarkList.push(listName);
          }
        }
      }
    },

    async bookmarkItem() {
      const addListingId = this.validListingId;

      if (!addListingId) {
        console.error("No valid listing ID available for bookmarking");
        return;
      }

      for (const listName in this.userBookmarks) {
        if (Object.prototype.hasOwnProperty.call(this.userBookmarks, listName)) {
          const bookmarkItems = this.userBookmarks[listName].listItems || [];

          const itemExist = bookmarkItems.some(item => parseInt(item?.drinkId) === addListingId);

          if (this.selectedBookmarkList.includes(listName)) {
            if (!itemExist) {
              bookmarkItems.push({ drinkId: addListingId });
            }
          } else {
            if (itemExist) {
              const index = bookmarkItems.findIndex(item => parseInt(item?.drinkId) === addListingId);
              if (index !== -1) {
                bookmarkItems.splice(index, 1);
              }
            }
          }
        }
      }

      // Handle creation of a new list
      if (this.saveToNewList) {
        if (!this.othersListName.trim()) {
          this.othersListNameError = "Please enter a list name";
          return;
        } else if (this.userBookmarks[this.othersListName]) {
          this.othersListNameError = "List name already exists";
          return;
        } else {
          this.othersListNameError = "";
          this.userBookmarks[this.othersListName] = {
            listDesc: "",
            listItems: [{ drinkId: addListingId }]
          };
        }
      }

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`,
          {
            userID: this.userID,
            bookmark: this.userBookmarks
          },
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );
        console.log("Bookmark update success:", response.data);
      } catch (error) {
        console.error("Bookmark update failed:", error);
      }

      window.location.reload();
    }
  }
};
</script>
