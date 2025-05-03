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
            listingID: [Number, String, Object], // Accept multiple types for flexibility
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
                validListingId: null
            }
        },
        created() {
        console.log("BookmarkModal component created");
            },
            beforeMount() {
                console.log("BookmarkModal - listings:", this.listings);
                console.log("BookmarkModal - listingID:", this.listingID);
            },
        mounted() {
            if (this.user && Object.keys(this.user).length > 0) {
                this.userID = this.user.id;
                this.userBookmarks = this.user.drinkLists;
            }
        },
        watch: {
            listingID: {
                handler: function(newVal) {
                    console.log("listingID changed to:", newVal);
                    if (newVal && (typeof newVal === 'number' || 
                        typeof newVal === 'string' || 
                        (typeof newVal === 'object' && newVal.id)))  {
                        // Add a small delay to ensure Vue has fully updated
                        setTimeout(() => {
                            // If listingID is an object with an id property, use that
                            const idToUse = typeof newVal === 'object' && newVal !== null && newVal.id ? 
                                newVal.id : newVal;
                            
                            console.log("Calling populateBookmarkModal with:", idToUse);
                            this.populateBookmarkModal(idToUse);
                        }, 100);
                    }
                },
                immediate: true // This will call the handler upon component creation
            },  
            user: function() {
                if (this.user && Object.keys(this.user).length > 0) {
                    this.userID = this.user.id;
                    this.userBookmarks = this.user.drinkLists;
                }
            }
        },
        methods: {
            // checks if listing is in user bookmark list
            checkBookmarkStatus(listingID) {
                for (const category of Object.values(this.userBookmarks)) {
                    if (category.listItems) {
                        if (category.listItems.some(item => parseInt(item?.drinkId) === listingID)) {
                            return true;
                        }
                    }
                }
            },
            populateBookmarkModal(listingID) {
                console.log("populateBookmarkModal called with:", listingID);
                console.log("Current listings array has:", this.listings ? this.listings.length : 0, "items");
                // param: objectId
                if (!listingID) {
                    console.error("No listingID provided to populateBookmarkModal");
                    return;
                }
                if (!this.listings || !Array.isArray(this.listings) || this.listings.length === 0) {
                    console.error("Listings array is empty or invalid");
                    return;
                }
                // Clear previous selections when populating a new modal
                this.selectedBookmarkList = [];
                
                // Extract the actual ID value from the object
                let searchID;
                if (typeof listingID === 'object' && listingID !== null) {
                    // Try to access the id property directly
                    if (listingID.id !== undefined) {
                        searchID = listingID.id;
                    } 
                    // If we couldn't get an ID, log error
                    else {
                        console.error("Could not extract ID from object:", listingID);
                        // Print all properties of the object for debugging
                        console.log("Object properties:", Object.keys(listingID));
                        return;
                    }
                } else {
                    // Convert ID to number if it's a string
                    searchID = typeof listingID === 'string' ? parseInt(listingID) : listingID;
                }
                
                console.log("Searching for listing with ID:", searchID);
                // Find the listing first - try both with string and number comparison
                const foundListing = this.listings.find(listing => 
                    listing.id === searchID || 
                    parseInt(listing.id) === parseInt(searchID) || 
                    String(listing.id) === String(searchID)
                );
                console.log("Found a match?", foundListing ? "Yes" : "No");
                
                // Check if a listing was actually found
                if (!foundListing) {
                    console.error(`Listing with ID ${listingID} not found in listings array of ${this.listings.length} items`);
                    console.log("Available listings:", this.listings.map(l => ({ id: l.id, name: l.listingName })));
                    return; // Exit the function if no listing was found
                }
                
                console.log("Found listing:", foundListing);

                // Store the valid ID for later use in bookmarkItem
                this.validListingId = foundListing.id;
                console.log("Set validListingId to:", this.validListingId);
                
                // Now we can safely access the name
                this.bookmarkModalItem = foundListing.listingName;
                console.log("Set bookmarkModalItem to:", this.bookmarkModalItem);

                for (const listName in this.userBookmarks) {
                    if (Object.hasOwnProperty.call(this.userBookmarks, listName)) {
                        const bookmarkItems = this.userBookmarks[listName].listItems;
                        if (bookmarkItems) {
                            if (bookmarkItems.some(item => parseInt(item?.drinkId) === listingID)) {
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
                if (!this.listings || this.listings.length === 0) {
                    console.error("Listings array is empty or undefined");
                    return;
                }
            
            
                // Use the stored valid ID instead of trying to extract from the proxy object
                if (!this.validListingId) {
                    console.error("No valid listing ID available for bookmarking");
                    return;
                }
                
                // Use the stored ID directly
                let addListingId = this.validListingId;
                
                
                console.log("Using listing ID for bookmark:", addListingId);
            
                for (const listName in this.userBookmarks) {
                    if (Object.hasOwnProperty.call(this.userBookmarks, listName)) {
                        const bookmarkItems = this.userBookmarks[listName].listItems;

                        let itemExist = bookmarkItems.some(item => parseInt(item?.drinkId) === addListingId);
                        if (this.selectedBookmarkList.includes(listName)) {
                            if (!itemExist) {
                                bookmarkItems.push({drinkId: addListingId});
                            }
                        } else {
                            if (itemExist) {
                                const index = bookmarkItems.findIndex(item => parseInt(item?.drinkId) === addListingId);
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
                            listItems: [{drinkId: addListingId}],
                        };
                    }
                }

                try {
                    const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`, 
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