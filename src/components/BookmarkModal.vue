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
            listings: Array,
            listingID: Object,
        },
        data() {
            return {
                userID: '',
                userBookmarks: {},
                bookmarkModalItem: '',
                selectedBookmarkList: [],
                othersListName: '',
                othersListNameError: '',
                saveToNewList: false,
            }
        },
        mounted() {
            if (this.user && Object.keys(this.user).length > 0) {
                this.userID = this.user._id.$oid;
                this.userBookmarks = this.user.drinkLists;
            }
        },
        watch: {
            listingID: function() {
                if (this.listingID) {
                    this.populateBookmarkModal(this.listingID);
                }
            }, 
            user: function() {
                if (this.user && Object.keys(this.user).length > 0) {
                    this.userID = this.user._id.$oid;
                    this.userBookmarks = this.user.drinkLists;
                }
            }
        },
        methods: {
            // checks if listing is in user bookmark list
            checkBookmarkStatus(listingID) {
                for (const category of Object.values(this.userBookmarks)) {
                    if (category.listItems) {
                        if (category.listItems.some(item => item[1].$oid === listingID)) {
                            return true;
                        }
                    }
                }
            },
            populateBookmarkModal(listingID) {
                // param: objectId
                if (Object.keys(this.listingID).length === 0) {
                    return;
                }
                this.bookmarkModalItem = this.listings.find(listing => listing._id.$oid === listingID.$oid).listingName;
                this.selectedBookmarkList = [];
                for (const listName in this.userBookmarks) {
                    if (Object.hasOwnProperty.call(this.userBookmarks, listName)) {
                        const bookmarkItems = this.userBookmarks[listName].listItems;
                        if (bookmarkItems) {
                            if (bookmarkItems.some(item => item[1].$oid === listingID.$oid)) {
                                if (!this.selectedBookmarkList.includes(listName)) {
                                    this.selectedBookmarkList.push(listName);
                                }
                            }
                        } 
                    }
                }
            },
            // triggered when user clicks on save changes in bookmark modal
            async bookmarkItem() {

                let addListingId = this.listings.find(listing => listing.listingName === this.bookmarkModalItem)._id;

                for (const listName in this.userBookmarks) {
                    if (Object.hasOwnProperty.call(this.userBookmarks, listName)) {
                        const bookmarkItems = this.userBookmarks[listName].listItems;
                        let itemExist = bookmarkItems.some(item => item[1].$oid === addListingId.$oid);
                        if (this.selectedBookmarkList.includes(listName)) {
                            if (!itemExist) {
                                bookmarkItems.push([new Date(), addListingId]);
                            }
                        } else {
                            if (itemExist) {
                                const index = bookmarkItems.findIndex(item => item[1].$oid === addListingId.$oid);
                                bookmarkItems.splice(index, 1);
                            }
                        }
                    }
                }

                if (this.saveToNewList) {
                    if (this.othersListName === "") {
                        this.othersListNameError = "Please enter a list name";
                        return;
                    } else if (this.userBookmarks[this.othersListName]) {
                        this.othersListNameError = "List name already exists";
                        return;
                    } else {
                        this.othersListNameError = "";
                        this.userBookmarks[this.othersListName] = {
                            listDesc: "",
                            listItems: [[new Date(), addListingId]],
                        };
                    }
                }

                try {
                    const response = await this.$axios.post('http://127.0.0.1:5000/editProfile/updateBookmark', 
                        {
                            userID: this.userID,
                            bookmark: this.userBookmarks,
                        }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    console.log(response.data);
                } catch (error) {
                    console.error(error);
                }
                
                window.location.reload();

            },

        }
    }
</script>