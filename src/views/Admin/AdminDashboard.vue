<!-- Admin can access this page to handle admin controls. -->

<template>
    <NavBar />
    <!-- Header -->
    <div class="container pt-3">
        
        <!-- Display when data is being loaded -->
        <div class="text-info-emphasis fst-italic fw-bold fs-5" v-if="!dataLoaded"> 
            <span>Currently loading data, please hold on!</span>
            <br><br>
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        
        <!-- Display when data loading encounters an error -->
        <div class="text-danger fst-italic fw-bold fs-3" v-if="loadError"> 
            <span>An error occurred while loading data, please try refreshing the page!</span>
            <br>
            <button class="btn primary-btn btn-sm" @click="()=>{this.$router.go(0)}">
                <span class="fs-5 fst-italic"> Refresh Page </span>
            </button>
        </div>

        <!-- Display requests after data loaded -->
        <div v-if="dataLoaded && !loadError">

            <!-- Title -->
            <div class="col-12">
                <div class="d-grid gap-2">
                    <p class="fw-bold fs-1 m-0">Admin Dashboard</p>
                </div>
            </div>
            
            
            <nav>
                <div class="nav nav-tabs justify-content-center" id="nav-tab" role="tablist">
                    <button class="nav-link active flex-grow-1" id="nav-tag-tab" data-bs-toggle="tab" data-bs-target="#nav-tag" type="button" role="tab" aria-controls="nav-tag" aria-selected="true"> Tag Controls </button>
                    <button class="nav-link flex-grow-1" id="nav-moderator-tab" data-bs-toggle="tab" data-bs-target="#nav-moderator" type="button" role="tab" aria-controls="nav-moderator" aria-selected="false"> Moderators </button>
                    <button class="nav-link flex-grow-1" id="nav-business-tab" data-bs-toggle="tab" data-bs-target="#nav-business" type="button" role="tab" aria-controls="nav-business" aria-selected="false"> Business Accounts </button>
                </div>
            </nav>

            <!-- content in navtabs -->
            <div class="tab-content" id="nav-tabContent">
            
                <!-- tag controls navtab -->
                <div class="tab-pane fade show active" id="nav-tag" role="tabpanel" aria-labelledby="nav-tag-tab">
                    
                    <div class="row text-center">
                        <div class="col-12">
                            <h3><b>Tag Controls</b></h3>
                        </div>
                    </div>
                    <div>
                        <div class="gap-1">
                            <!-- Open a modal prompting to edit or add tags -->
                            <button class="btn tertiary-btn m-1" type="button" @click="toggleObservationControl" :style="{ 'background-color': showObservationControl ? '#535C72' : '#747D92', 'color':'whitesmoke'}">
                                Action Tags
                            </button>
                            
                            <button class="btn tertiary-btn m-1" data-bs-toggle="button" type="button" @click="toggleFlavourControl" :style="{ 'background-color': showFlavourControl ? '#535C72' : '#747D92', 'color':'whitesmoke'}">
                                Flavour Tags
                            </button>

                            <div v-if="showObservationControl" class="rounded p-3 border border-black">
                                <button class="btn btn-warning reverse-clickable-text text-dark" data-bs-toggle="modal" data-bs-target="#observationModal" @click="addObservation" type="button">
                                    Add Action Tags
                                </button> 

                                <button class="btn btn-primary mx-1 reverse-clickable-text" data-bs-toggle="modal" data-bs-target="#observationModal" @click="editObservation" type="button">
                                    Edit Action Tags
                                </button>

                                <button class="btn btn-danger mx-1 reverse-clickable-text" data-bs-toggle="modal" data-bs-target="#observationModal" @click="deleteObservations" type="button">
                                    Delete Action Tags
                                </button>
                            </div>

                            <div v-if="showFlavourControl" class="rounded p-3 border border-black">
                                <div class="row mb-1">
                                    <div class="col-12 pb-2">
                                        <button @click="setAddFlavour('family')" class="btn btn-warning reverse-clickable-text text-dark" type="button" data-bs-toggle="modal" data-bs-target="#addFlavourModal">
                                            Add Family Tags
                                        </button>
                                        <button @click="setEditFlavour('family')" class="btn btn-primary mx-1 reverse-clickable-text" type="button" data-bs-toggle="modal" data-bs-target="#editFlavourModal">
                                            Edit Family Tags
                                        </button>
                                        <button @click="setDeleteFlavour('family')" class="btn btn-danger mx-1 reverse-clickable-text" type="button" data-bs-toggle="modal" data-bs-target="#deleteFlavourModal">
                                            Delete Family Tags
                                        </button>
                                    </div>
                                    <div class="col-12 pb-2">
                                        <button @click="setAddFlavour('sub')" class="btn btn-warning reverse-clickable-text text-dark" type="button" data-bs-toggle="modal" data-bs-target="#addFlavourModal">
                                            Add Sub Tags
                                        </button>
                                        <button @click="setEditFlavour('sub')" class="btn btn-primary mx-1 reverse-clickable-text" type="button" data-bs-toggle="modal" data-bs-target="#editFlavourModal">
                                            Edit Sub Tags
                                        </button>
                                        <button @click="setDeleteFlavour('sub')" class="btn btn-danger mx-1 reverse-clickable-text" type="button" data-bs-toggle="modal" data-bs-target="#deleteFlavourModal">
                                            Delete Sub Tags
                                        </button>
                                    </div> 
                                </div>
                            </div>
                        
                        </div>
                        <!-- Add family/subtag modal -->
                        <div class="modal fade" id="addFlavourModal" tabindex="-1" aria-labelledby="addFlavourModalLabel" aria-hidden="true" data-bs-backdrop="static">
                            <div class="modal-dialog modal-lg">
                                <div class="modal-content">
                                    <div class="modal-header" style="background-color: #535C72">
                                        <!-- color: selectedObservations.includes(observation) ? 'white' : 'black' -->
                                        <h1 v-if="addFlavour == 'family'" class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Add Family Tag</h1>
                                        <h1 v-if="addFlavour == 'sub'" class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Add Sub Tag</h1>
                                        <button @click="resetFlavourMode" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div v-if="errorAddFlavour || successAddFlavour">
                                        <div v-if="successAddFlavour" class="modal-body text-center text-success fst-italic fw-bold fs-3">
                                            <span>Flavour tag has successfully been created!</span>
                                        </div>
                                        <div v-if="errorAddFlavour" class="modal-body text-center text-danger fst-italic fw-bold fs-3">
                                            <span>Error has occured while adding flavour tags. Please try again.</span>
                                        </div>
                                    </div>
                                    <div v-if="!(errorAddFlavour || successAddFlavour || confirmCreateFlavour)">
                                        <div v-if="addFlavour == 'family'" class="modal-body">
                                            <div class = 'row text-center'>
                                                <div class = 'col'>
                                                    <p>New family tag looks like this:</p>
                                                    <button :style="{ color: hexcode==''?'black':'white', backgroundColor: hexCodeValid?'#' + hexcode:'', width: '150px', height: '60px' }" class="btn mb-1"> {{ newFamily }} </button>
                                                </div>
                                            </div>
                                            <p class='text-start mb-2 fw-bold'>New Family Tag:</p>
                                            <input v-model="newFamily" type="text" class="form-control" placeholder="Enter New Family Tag">
                                            <p v-if="newFamily ==''" class='text-danger text-start mb-2 fw-bold'>Family Tag cannot be empty</p>
                                            <p class='text-start mb-2 fw-bold'>New Family Hexcode (without the hex #):</p>
                                            <div class="input-group">
                                                <span class="input-group-text" id="basic-addon1">#</span>
                                                <input v-model="hexcode" @keyup="isValidHexCode" type="text" class="form-control" placeholder="Enter Hexcode">
                                            </div>
                                            <p v-if="hexcode == ''" class='text-danger text-start mb-2 fw-bold'>Hexcode cannot be empty</p>
                                            <p v-if="!hexCodeValid && hexcode != ''" class='text-danger text-start mb-2 fw-bold'>Hexcode is invalid</p>
                                        </div>
                                        <div v-if="addFlavour == 'sub'" class="modal-body">
                                            <p class='text-start mb-2 fw-bold'>New Sub Tag:</p>
                                            <input v-model="newSub" type="text" class="form-control">
                                            <p v-if="newSub ==''" class='text-danger text-start mb-2 fw-bold'>Sub Tag cannot be empty</p>
                                            
                                            <p class='text-start mt-2 mb-2 fw-bold'>Choose family tag to add under:</p>
                                            <input list="flavourTags" v-model="tagParent" class="form-control" id="tagParent" placeholder="Enter family tag to add to" v-on:change="updateTagParent">
                                            <datalist id="flavourTags">
                                                <option v-for="tag in flavourTags" :key="tag._id.$oid" :value="tag.familyTag">
                                                    {{tag.familyTag}}
                                                </option>
                                            </datalist>
                                            <p v-show="tagParent.length > 0" class="text-start mb-1 text-danger" id="tagParentError"></p>

                                        </div>
                                    </div>
                                    <div v-if="!(errorAddFlavour || successAddFlavour) && confirmCreateFlavour" >
                                        <p v-if="addFlavour=='family'" class="text-center mb-1"> Do you really want to add {{ newFamily }} with hexcode #{{ hexcode }}?</p>
                                        <p v-if="addFlavour=='sub'" class="text-center mb-1"> Do you really want to add <strong>[{{ newSub }}]</strong> under <strong>[{{ chosenTagParent.familyTag }}]</strong>?</p>
                                    </div>

                                    <div class="modal-footer">
                                        <button v-if="errorAddFlavour || successAddFlavour  || confirmCreateFlavour" @click="resetFlavourErrors" type="button" class="btn btn-secondary">Return</button>
                                        <button v-if="!(errorAddFlavour || successAddFlavour || confirmCreateFlavour)" @click="confirmAddFlavour" type="button" class="btn btn-primary">Add Tag</button>
                                        <button v-if="!(errorAddFlavour || successAddFlavour) && confirmCreateFlavour" @click="createNewFlavour" type="button" class="btn btn-primary">Confirm Add Tag</button>
                                        <button v-if="!(errorAddFlavour || successAddFlavour)" @click="resetFlavourMode" type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        <button v-if="errorAddFlavour || successAddFlavour" @click="resetFlavourModal" type="button" data-bs-dismiss="modal" class="btn btn-secondary">Close</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- End of add family/sub tag modal -->

                        <!-- Edit family/subtag modal -->
                        <div class="modal fade" id="editFlavourModal" tabindex="-1" aria-labelledby="editFlavourModalLabel" aria-hidden="true" data-bs-backdrop="static">
                            <div class="modal-dialog modal-lg">
                                <div class="modal-content">
                                    <div class="modal-header" style="background-color: #535C72">
                                        <h1 v-if="editFlavour == 'family'" class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Edit Family Tag</h1>
                                        <h1 v-if="editFlavour == 'sub'" class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Edit Sub Tag</h1>
                                        <button @click="resetEditFlavourMode" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div v-if="errorEditFlavour || successEditFlavour">
                                        <div v-if="successEditFlavour" class="modal-body text-center text-success fst-italic fw-bold fs-3">
                                            <span>Flavour tag has successfully been edited!</span>
                                        </div>
                                        <div v-if="errorEditFlavour" class="modal-body text-center text-danger fst-italic fw-bold fs-3">
                                            <span>Error has occured while editing flavour tags. Please try again.</span>
                                        </div>
                                    </div>
                                    <div v-if="!(errorEditFlavour || successEditFlavour || confirmEditFlavour)">

                                        <div v-if="editFlavour == 'family'" class="modal-body">
                                            <div class="row">
                                                <div v-for="tag in editedFlavourTags" class="mb-2 col-md-6"  v-bind:key="tag._id">
                                                    <input v-model="tag.familyTag" type="text" class="form-control" :style="{ color:'black', backgroundColor: tag['hexcode'], borderColor:tag['hexcode'], borderWidth:'1px' }">
                                                    <input v-model="tag.hexcode" type="text" class="form-control">
                                                    <p v-if="tag.familyTag==''" class='text-danger text-start mb-2 fw-bold'>Flavour tag cannot be empty</p>
                                                </div>
                                            </div>

                                        </div>
                                        
                                        <div v-if="editFlavour == 'sub'" class="modal-body">
                                            <button class="btn mb-2 me-2" @click="toggleBox(family)" v-for="family in editedFlavourTags" v-bind:key="family['_id']" :style="{ color:'white', backgroundColor: family['hexcode'], borderColor:family['hexcode'], borderWidth:'1px' }">{{ family['familyTag'] }}</button>
                                            <div v-for="family in editedFlavourTags" :key="family['_id']">
                                                <div v-if="family.showBox" class="rounded p-3" :style="{border: '3px solid ' + family['hexcode'] }">
                                                    <div class="row">
                                                        <div class="col-3" v-for="(element, index) in family.subTag2" :key="index">
                                                            <input v-model="element.subTag" type="text" class="form-control">
                                                            <p v-if="element.subTag==''" class='text-danger text-start mb-2 fw-bold'>Sub tag cannot be empty</p>
                                                        </div>                        
                                                    </div>
                                                </div>
                                            </div>
                                            

                                        </div>
                                    </div>
                                    <div v-if="!(errorEditFlavour || successEditFlavour) && confirmEditFlavour" >
                                        <p class="text-center mb-1">Are you sure you want to save these changes?</p>
                                        <p class='text-danger text-center mb-2 fw-bold' v-if="flavourNoChange">There is no changed flavour tag</p>
                                    </div>

                                    <div class="modal-footer">
                                        <button v-if="errorEditFlavour || successEditFlavour  || confirmEditFlavour" @click="resetEditFlavourErrors" type="button" class="btn btn-secondary">Return</button>
                                        <button v-if="!(errorEditFlavour || successEditFlavour  || confirmEditFlavour)" @click="resetEditFlavour" type="button" class="btn btn-warning">Reset Tags</button>
                                        <button v-if="!(errorEditFlavour || successEditFlavour  || confirmEditFlavour)" @click="confirmUpdateFlavour" type="button" class="btn btn-primary">Update Tags</button>
                                        <button v-if="!(errorEditFlavour || successEditFlavour) && confirmEditFlavour" @click="updateExistingFlavour" type="button" class="btn btn-primary">Confirm Edit Tags</button>
                                        <button v-if="!(errorEditFlavour || successEditFlavour)" @click="resetEditFlavourMode" type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        <button v-if="errorEditFlavour || successEditFlavour" @click="resetEditFlavourModal" type="button" data-bs-dismiss="modal" class="btn btn-secondary">Close</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- End of Edit family/sub tag modal -->

                        <!-- Delete family/sub tag modal -->
                        
                        <div class="modal fade" id="deleteFlavourModal" tabindex="-1" aria-labelledby="deleteFlavourModalLabel" aria-hidden="true" data-bs-backdrop="static">
                            <div class="modal-dialog modal-lg">
                                <div class="modal-content">
                                    <div class="modal-header" style="background-color: #535C72">
                                        <h1 v-if="deleteFlavour == 'family'" class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Delete Family Tag</h1>
                                        <h1 v-if="deleteFlavour == 'sub'" class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Delete Sub Tag</h1>
                                        <button @click="resetDeleteFlavourMode" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div v-if="errorDeleteFlavour || successDeleteFlavour">
                                        <div v-if="successDeleteFlavour" class="modal-body text-center text-success fst-italic fw-bold fs-3">
                                            <span>Flavour tag has successfully been deleted!</span>
                                        </div>
                                        <div v-if="errorDeleteFlavour" class="modal-body text-center text-danger fst-italic fw-bold fs-3">
                                            <span>Error has occured while deleting flavour tags. Please try again.</span>
                                        </div>
                                    </div>
                                    <div v-if="!(errorDeleteFlavour || successDeleteFlavour)">

                                        <div v-if="deleteFlavour == 'family'" class="modal-body">
                                            <div class="row">
                                                <div v-for="tag in editedFlavourTags" class="mb-2 col-md-6"  v-bind:key="tag._id">
                                                    <button @click="selectDeleteFamily(tag._id, tag.familyTag, tag.hexcode, tag.subTag2)" type="text" class="form-control" :style="{ color:'black', backgroundColor: tag['hexcode'], borderColor:tag['hexcode'], borderWidth:'1px' }">{{ tag.familyTag }}</button>
                                                </div>
                                            </div>
                                            <div v-if="familyTagToDelete!=''">
                                                <div class="row">
                                                    <span class='text-danger mb-2 fw-bold'>Are you sure you want to delete family tag <button class='btn mt-1' type="button" :style="{ color:'white', backgroundColor: familyTagToDelete['hexcode'], borderColor:familyTagToDelete['hexcode'], borderWidth:'1px', width: '150px', height: '60px'}">{{familyTagToDelete.familyTag}}</button>?</span>
                                                    <span class='text-danger mb-2 fw-bold'>NOTE: All sub tags will be deleted!</span>
                                                </div>
                                            
                                                <button @click="confirmDeleteFlavourTag" type="button" class="btn btn-danger mx-1">Confirm Delete</button>
                                                <button @click="resetDeleteFamilyTag" type="button" class="btn tertiary-btn reverse-clickable-text">No, do not delete</button>

                                            </div>
                                        </div>
                                        
                                        <div v-if="deleteFlavour == 'sub'" class="modal-body">
                                            <button class="btn mb-2 me-2" @click="toggleBox(family)" v-for="family in editedFlavourTags" v-bind:key="family['_id']" :style="{ color:'white', backgroundColor: family['hexcode'], borderColor:family['hexcode'], borderWidth:'1px' }">{{ family['familyTag'] }}</button>
                                            <div v-for="family in editedFlavourTags" :key="family['_id']">
                                                <div v-if="family.showBox" class="rounded p-3" :style="{border: '3px solid ' + family['hexcode'] }">
                                                    <div class="row">
                                                        <div class="col-3" v-for="(element, index) in family.subTag2" :key="index">
                                                            <button @click="selectDeleteSub(element.id, element.subTag, family['hexcode'])" type="button" class="btn mb-1" :style="{ color:'white', backgroundColor: family['hexcode'], borderColor:family['hexcode'], borderWidth:'1px', width: '150px', height: '60px'}">{{ element.subTag }}</button>
                                                        </div>                        
                                                    </div>
                                                </div>
                                            </div>
                                            
                                            <div v-if="subTagToDelete!=''">
                                                <div class="row">
                                                    <span class='text-danger mb-2 fw-bold'>Are you sure you want to delete <button class='btn mt-1' type="button" :style="{ color:'white', backgroundColor: subTagToDelete['hexcode'], borderColor:subTagToDelete['hexcode'], borderWidth:'1px', width: '150px', height: '60px'}">{{subTagToDelete.subTag}}</button>?</span>
                                                </div>
                                            
                                                <button @click="confirmDeleteFlavourTag" type="button" class="btn btn-danger mx-1">Confirm Delete</button>
                                                <button @click="resetDeleteSubTag" type="button" class="btn tertiary-btn reverse-clickable-text">No, do not delete</button>

                                            </div>

                                        </div>
                                    </div>

                                    <div class="modal-footer">
                                        <button v-if="!(errorDeleteFlavour || successDeleteFlavour)" @click="resetDeleteFlavourMode" type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        <button v-if="errorDeleteFlavour || successDeleteFlavour" @click="resetDeleteFlavourMode" type="button" class="btn btn-secondary">Return</button>
                                        <button v-if="errorDeleteFlavour || successDeleteFlavour" @click="resetDeleteFlavourModal" type="button" data-bs-dismiss="modal" class="btn btn-secondary">Close</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- End of delete family/sub tag modal -->


                        <!-- modal for action tag handling -->
                        <div class="modal fade" id="observationModal" tabindex="-1" aria-labelledby="observationModalLabel" aria-hidden="true" data-bs-backdrop="static">
                            <div class="modal-dialog modal-lg">
                                <div class="modal-content">
                                    <div class="modal-header" style="background-color: #535C72">
                                        <h1 v-if="selectingObservation" class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Action Tag Control</h1>
                                        <h1 v-if="addingObservation" class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Add Action Tag</h1>
                                        <h1 v-if="editingObservation" class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Edit Action Tag</h1>
                                        <h1 v-if="deletingObservation" class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Delete Action Tag</h1>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="resetObservation"></button>
                                    </div>

                                    <!-- Modal for success and error message -->
                                    <div v-if="successUpdateObservation" class="modal-body text-center text-success fst-italic fw-bold fs-3">
                                        <span>Action tags have successfully been updated!</span>
                                    </div>

                                    <div v-if="successCreateObservation" class="modal-body text-center text-success fst-italic fw-bold fs-3">
                                        <span>Action tags have successfully been created!</span>
                                    </div>

                                    <div v-if="updatingObservation" class="modal-body text-center text-primary fst-italic fw-bold fs-3">
                                        <span>Action tags are being updated!</span>
                                    </div>

                                    <div v-if="submittingObservation" class="modal-body text-center text-primary fst-italic fw-bold fs-3">
                                        <span>Action tags are being added!</span>
                                    </div>

                                    <div v-if="errorUpdateObservation" class="modal-body text-center text-danger fst-italic fw-bold fs-3">
                                        <span v-if="invalidTag"> The Action tag you are trying to update does not exist</span>
                                        <span v-if="errorMessage">An error occurred updating the action tags. Please try again.</span>
                                    </div>

                                    <div v-if="errorCreateObservation" class="modal-body text-center text-danger fst-italic fw-bold fs-3">
                                        <span v-if="duplicateTag"> The Action tag you are trying to create already exists!</span>
                                        <span v-if="errorMessage">An error occurred updating the Action tags. Please try again.</span>
                                    </div>

                                    <div v-if="successDeleteObservation" class="modal-body text-center text-success fst-italic fw-bold fs-3">
                                        <span>Action tag have successfully been deleted!</span>
                                    </div>
                                    <div v-if="errorDeletingObservation" class="modal-body text-center text-danger fst-italic fw-bold fs-3">
                                        <span v-if="notExistObservation"> The action tag you are trying to delete does not exist!</span>
                                        <span v-if="errorDeleteObservation">An error occurred deleting the action tag. Please try again.</span>
                                    </div>

                                    <!-- Modal body for selecting mode for observation operations -->
                                    <div v-if="selectingObservation" class="modal-body">
                                        <button class="btn btn-warning reverse-clickable-text text-dark" @click="addObservation" type="button">
                                            Add Action Tags
                                        </button> 

                                        <button class="btn btn-primary mx-1 reverse-clickable-text" @click="editObservation" type="button">
                                            Edit Action Tags
                                        </button>

                                        <button class="btn btn-danger mx-1 reverse-clickable-text" @click="deleteObservations" type="button">
                                            Delete Action Tags
                                        </button>
                                    </div>
                                    <!-- Modal body for adding observation -->
                                    <div v-if="addingObservation" class="modal-body">
                                        <input v-model="newObservation" type="text" class="form-control">
                                        <p v-if="newObservation ==''" class='text-danger text-start mb-2 fw-bold'>Action Tag cannot be empty</p>
                                    </div>
                                    <!-- Modal body for editing observation -->
                                    <div v-if="editingObservation" class="modal-body">
                                        <div class="row">
                                            <div v-for="tag in editedObservationTags" class="mb-2 col-md-6"  v-bind:key="tag._id">
                                                <input v-model="tag.observationTag" type="text" class="form-control">
                                                <p v-if="tag.observationTag==''" class='text-danger text-start mb-2 fw-bold'>Action Tag cannot be empty</p>
                                            </div>
                                        </div>
                                        <p class='text-danger text-center mb-2 fw-bold' v-if="nothingChanged">There is no changed action tag</p>
                                    </div>

                                    <div v-if="deletingObservation" class="modal-body">
                                        <div class="row">
                                            <div v-for="tag in observationTags" class="mb-2 col-md-4"  v-bind:key="tag._id">
                                                <button @click="deleteObservation(tag._id, tag.observationTag)" type="button" class="btn btn-danger" style="width: 150px; height: 60px;">{{ tag.observationTag }}</button>
                                            </div>
                                        </div>
                                        <div v-if="observationToDelete!=''">
                                            <div class="row">
                                                <span class='text-danger mb-2 fw-bold'>Are you sure you want to delete [{{ observationToDelete.observationTag }}]?</span>
                                            </div>
                                            
                                            <button @click="confirmDeleteTag" type="button" class="btn btn-danger mx-1">Confirm Delete</button>
                                            <button @click="resetDeleteTag" type="button" class="btn tertiary-btn reverse-clickable-text">No, do not delete</button>
                                        </div>
                                    </div>

                                    <div class="modal-footer">
                                        <!-- <button v-if="selectingObservation" type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
                                        <button v-if="!(successUpdateObservation || errorUpdateObservation || errorCreateObservation || successCreateObservation || successDeleteObservation || errorDeleteObservation)" @click="resetObservation" type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        <button v-if="editingObservation" @click="updateObservation" type="button" class="btn btn-primary">Save Updates</button>
                                        <button v-if="addingObservation" @click="createNewObservation" type="button" class="btn btn-primary">Add Tag</button>
                                        <button v-if="successUpdateObservation || errorUpdateObservation || errorCreateObservation || successCreateObservation || successDeleteObservation || errorDeleteObservation" @click="resetErrors" type="button" data-bs-dismiss="modal" class="btn btn-secondary">Close</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- end of modal-->
                    </div>
                </div>

                <!-- moderator navtab -->
                <div class="tab-pane fade" id="nav-moderator" role="tabpanel" aria-labelledby="nav-moderator-tab">
                    <!-- mod addition and removal -->
                    <div>
                        <div class="row text-center">
                            <div class="col-12">
                                <h3><b>Manage Moderators</b></h3>
                            </div>
                        </div>
                        <div>
                            <button class="btn tertiary-btn reverse-clickable-text m-1" type="button" data-bs-toggle="modal" data-bs-target="#addModeratorModal">
                                Add a moderator
                            </button>      
                            <button class="btn tertiary-btn reverse-clickable-text m-1" type="button" data-bs-toggle="modal" data-bs-target="#removeModeratorModal">
                                Remove a moderator
                            </button>      
                        </div>

                        <!-- Mod addition modal -->
                        <div class="modal fade" id="addModeratorModal" data-bs-backdrop="static" tabindex="-1" aria-labelledby="addModeratorLabel" aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-header" style="background-color: #535C72">
                                        <h1 class="modal-title fs-5" id="addModeratorLabel" style="color: white;">Add Moderator</h1>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="resetAddMod"></button>
                                    </div>

                                    <!-- Success add mod modal body -->
                                    <div v-if="successAddMod" class="modal-body text-center text-success fst-italic fw-bold fs-3">
                                        <span>User has successfully been added as moderator!</span>
                                    </div>
                                    <!-- Error add mod modal body -->
                                    <div v-if="errorAddMod" class="modal-body text-center text-danger fst-italic fw-bold fs-3">
                                        <span>There is an error adding user as moderator, please try again!</span>
                                    </div>
                                    <!-- Initial select user to promote -->
                                    <div v-if="!confirmModerator && !(successAddMod||errorAddMod)" class="modal-body">
                                        <div class="form-group mb-3">
                                            <p class="text-start mb-1"> Choose user to promote to a moderator: <span class="text-danger">*</span></p>
                                            <input list="users" v-model="promotedUser" class="form-control" id="promotedUser" placeholder="Enter username" v-on:change="updateUsername">
                                            <datalist id="users">
                                                <option v-for="user in users" :key="user._id.$oid" :value="user.username">
                                                    {{user.username}}
                                                </option>
                                            </datalist>
                                            <p v-show="promotedUser.length > 0" class="text-start mb-1 text-danger" id="usernameError"></p>
                                        </div>
                                        <div class="form-group mb-3">
                                            <p class="text-start mb-1"> Choose drink type user can moderate: <span class="text-danger">*</span></p>
                                            <div v-if="selectedPromotedUser!=null" >
                                                <p v-html="formattedPromotedModTypes" class="text-start mb-1"></p>
                                            </div>
                                            <input list="addableDrinkType" v-model="promotedType" class="form-control" id="promotedType" placeholder="Enter drink type" v-on:change="updateDrinkType">
                                            <datalist id="addableDrinkType">
                                                <option v-for="drinkType in addableDrinkType" :key="drinkType._id.$oid" :value="drinkType.drinkType">
                                                    {{drinkType.drinkType}}
                                                </option>
                                            </datalist>
                                            <p v-show="promotedType.length > 0" class="text-start mb-1 text-danger" id="promotedTypeError"></p>
                                        </div>
                                        <p class="text-start mb-1 text-danger" id="alreadyModError"></p>
                                    </div>

                                    <!-- confirm mod to promote -->
                                    <div v-if="confirmModerator && !(successAddMod||errorAddMod)" class="modal-body">
                                        <p class="text-start mb-1"> Do you really want to add <strong>{{ promotedUser }}</strong> as a moderator for <strong>{{ promotedType }}</strong>? <span class="text-danger">*</span></p>
                                    </div>

                                    <!-- Initial select mod to promote footer -->
                                    <div v-if="!confirmModerator && !(successAddMod||errorAddMod)" class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        <button type="button" @click="addModerator" class="btn btn-primary">Add Moderator</button>
                                    </div>

                                    <!-- confirm mod to promote footer -->
                                    <div v-if="confirmModerator && !(successAddMod||errorAddMod)" class="modal-footer">
                                        <button type="button" @click="selectPromotedUser" class="btn btn-secondary">Return</button>
                                        <button type="button" @click="confirmAddModerator" class="btn btn-primary">Confirm Moderator</button>
                                    </div>

                                    <!-- successaddmod and erroraddmod footer -->
                                    <div v-if="successAddMod||errorAddMod" class="modal-footer">
                                        <button type="button" @click="selectPromotedUser" class="btn btn-secondary">Return</button>
                                        <button type="button" @click="resetAddMod" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Mod removal modal -->

                        <div class="modal fade" id="removeModeratorModal" data-bs-backdrop="static" tabindex="-1" aria-labelledby="addModeratorLabel" aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-header" style="background-color: #535C72">
                                        <h1 class="modal-title fs-5" id="removeModeratorLabel" style="color: white;">Remove Moderator</h1>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="resetRemoveMod"></button>
                                    </div>
                                    <!-- Success remove mod modal body -->
                                    <div v-if="successRemoveMod" class="modal-body text-center text-success fst-italic fw-bold fs-3">
                                        <span>User has successfully been removed as moderator!</span>
                                    </div>
                                    <!-- Error remove mod modal body -->
                                    <div v-if="errorRemoveMod" class="modal-body text-center text-danger fst-italic fw-bold fs-3">
                                        <span>There is an error removing user as moderator, please try again!</span>
                                    </div>

                                    <!-- Initial select remove mod modal body -->
                                    <div v-if="!confirmRemoveModerator && !(successRemoveMod||errorRemoveMod)" class="modal-body">
                                        <div class="form-group mb-3">
                                            <p class="text-start mb-1"> Choose user to remove as moderator: <span class="text-danger">*</span></p>
                                            <input list="moderators" v-model="removeMod" class="form-control" id="removeMod" placeholder="Enter username" v-on:change="updateModUsername">
                                            <datalist id="moderators">
                                                <option v-for="user in moderators" :key="user._id.$oid" :value="user.username">
                                                    {{user.username}}
                                                </option>
                                            </datalist>
                                            <p v-show="removeMod.length > 0" class="text-start mb-1 text-danger" id="modUsernameError"></p>
                                        </div>
                                        <div class="form-group mb-3">
                                            <p class="text-start mb-1"> Choose drink type to remove moderator rights from: <span class="text-danger">*</span></p>
                                            <div v-if="selectedRemoveMod!=null" >
                                                <p v-html="formattedRemoveModTypes" class="text-start mb-1"></p>
                                            </div>
                                            <input list="removableDrinkType" v-model="removedType" class="form-control" id="removedType" placeholder="Enter drink type" v-on:change="updateRemovedDrinkType">
                                            <datalist id="removableDrinkType">
                                                <option v-for="drinkType in removableDrinkType" :key="drinkType._id.$oid" :value="drinkType.drinkType">
                                                    {{drinkType.drinkType}}
                                                </option>
                                            </datalist>
                                            <p v-show="removedType.length > 0" class="text-start mb-1 text-danger" id="removedTypeError"></p>
                                        </div>
                                        <p class="text-start mb-1 text-danger" id="notModError"></p>
                                    </div>

                                    <!-- confirm mod to promote -->
                                    <div v-if="confirmRemoveModerator && !(successRemoveMod||errorRemoveMod)" class="modal-body">
                                        <p class="text-start mb-1"> Do you really want to remove <strong>{{ removeMod }}</strong> as a moderator for <strong>{{ removedType }}</strong>? <span class="text-danger">*</span></p>
                                    </div>
                                    <!-- Initial select mod to remove footer -->
                                    <div v-if="!confirmRemoveModerator && !(successRemoveMod||errorRemoveMod)" class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        <button type="button" @click="removeModerator" class="btn btn-primary">Remove Moderator</button>
                                    </div>
                                    <!-- confirm mod to remove footer -->
                                    <div v-if="confirmRemoveModerator && !(successRemoveMod||errorRemoveMod)" class="modal-footer">
                                        <button type="button" @click="selectRemoveMod" class="btn btn-secondary">Return</button>
                                        <button type="button" @click="confirmDowngradeModerator" class="btn btn-primary">Confirm Moderator</button>
                                    </div>

                                    <!-- successremovemod and errorremovemod footer -->
                                    <div v-if="successRemoveMod||errorRemoveMod" class="modal-footer">
                                        <button type="button" @click="selectRemoveMod" class="btn btn-secondary">Return</button>
                                        <button type="button" @click="resetRemoveMod" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                    </div>
                                </div>
                            </div>
                        </div>


                    </div>
                    <!-- mod addition and removal end -->

                    <hr>

                    <!-- mod request -->
                    <div>
                        <div class="row text-center">
                            <div class="col-12">
                                <h3><b>Moderator Request</b></h3>
                            </div>
                        </div>
                        <div>
                            <div v-if="pendingModRequests.length > 0" class="row" style="height: 650px; overflow: auto">
                                <div v-for="request in pendingModRequests" class="col-md-6 col-lg-4 pb-4 pb-4 pb-4" v-bind:key="request._id">
                                    <div class="card" style="background-color: white; height: 300px;">
                                        <div class="card-body">
                                        <ul class="list-group list-group-flush text-start">
                                            <li class="list-group-item"><span class="fw-bold">Requested By: </span > <br/>
                                                @<router-link :to="{ path: '/profile/user/' + request.userID.$oid }" style="color: inherit;">
                                                    {{ getUserbyID(request.userID).username }}
                                                </router-link> 
                                            </li>
                                            <li class="list-group-item"><span class="fw-bold">Drink Type: </span> <br/> {{ request.drinkType }} </li>
                                            <li class="list-group-item"><span class="fw-bold">Description: </span> <br/> {{ request.modDesc }} </li>
                                        </ul>
                                        </div>
                                        <div class="card-footer">
                                            <button class="btn btn-success btn-sm mx-3 my-1" type="button" style="width: 75px;" @click="reviewModRequest(request, 'approve')">Approve</button>
                                            <button class="btn btn-danger btn-sm mx-3 my-1" type="button" style="width: 75px;" @click="reviewModRequest(request, 'reject')">Reject</button>
                                        </div>
                                    </div>
                                </div>
                                        
                                
                            </div>
                            <div v-else>
                                No New Moderator Request
                            </div>
                        </div>
                    </div>
                    <!-- mod request end -->
                </div>

                <!-- business navtab -->
                <div class="tab-pane fade" id="nav-business" role="tabpanel" aria-labelledby="nav-business-tab">
                    <!-- add business -->
                    <div>
                        <div class="row text-center">
                            <div class="col-12">
                                <h3><b>Add Businesses</b></h3>
                            </div>
                        </div>
                        <div>
                            <p class="gap-1">
                                <!-- Open a modal prompting to edit or add tags -->
                                <button class="btn tertiary-btn reverse-clickable-text m-1" type="button" data-bs-toggle="modal" data-bs-target="#addBusinessModal" @click="resetAddBusinessModal">
                                    Add a Business
                                </button>
                            </p>
                            <!-- add business modal start -->
                            <div class="modal fade" id="addBusinessModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-dialog-centered">
                                    <div class="modal-content">
                                    <div class="modal-header">
                                        <h1 class="modal-title fs-5" id="exampleModalLabel">Add a Business</h1>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body text-start" v-if="createBusinessSuccess">
                                        <div class="alert alert-success" role="alert">
                                            Business account created successfully. 
                                            <br>
                                            Please save login details below.
                                            <br>
                                            <span class="text-danger">*This is the only time you can access the password. You cannot recover them later.</span>
                                            <br><br>
                                            <span v-if="businessType == 'producer'">Producer account: <b>{{ businessName }}</b></span>
                                            <span v-if="businessType == 'venue'">Venue account: {{ businessName }}</span>
                                            <br>
                                            Temporary password: <b>{{ tempPassword }}</b>
                                            <br>
                                            <button type="button" class="btn secondary-btn-less-round"  v-on:click="downloadCSV()"> Download login details </button>
                                        </div>
                                    </div>
                                    <div class="modal-body text-start" v-else-if="createBusinessError != '' ">
                                        <div class="alert alert-danger" role="alert">{{createBusinessError}}</div>
                                    </div>
                                    <div class="modal-body text-start" v-else>
                                        <div>
                                            <div class="mb-2 fw-bold">
                                                Profile Type <span style="color: red;">*</span>
                                            </div>
                                            <div class="mb-4">
                                                <div class="form-check form-check-inline">
                                                        <input class="form-check-input" type="radio" id="inlineCheckbox1" v-model="businessType" value="producer" name="business">
                                                    <label class="form-check-label text-start" for="inlineCheckbox1">Brand/Producer</label>
                                                </div>
                                                <div class="form-check form-check-inline">
                                                    <input class="form-check-input" type="radio" id="inlineCheckbox2" v-model="businessType" value="venue" name="business">
                                                    <label class="form-check-label text-start" for="inlineCheckbox2">Venue</label>
                                                </div>
                                            </div>
                                        </div>
                                        <div>
                                            <div class="mb-2 fw-bold">
                                                Name <span style="color: red;">*</span>
                                            </div>
                                            <div class="mb-4">
                                                <input type="text" class="form-control" v-model="businessName">
                                            </div>
                                        </div>
                                        <div>
                                            <div class="mb-2 fw-bold">
                                                Description <span style="color: red;">*</span>
                                            </div>
                                            <div class="mb-4">
                                                <input type="text" class="form-control" v-model="businessDesc">
                                            </div>
                                        </div>
                                        <div>
                                            <div class="mb-2 fw-bold">
                                                Country <span style="color: red;">*</span>
                                            </div>
                                            <div class="mb-4">
                                                <div class="input-group">
                                                    <select class="form-select" id="countrySelect" v-model="businessCountry">
                                                        <option v-for="country in countries" :key="country" :value="country.originCountry">
                                                            {{ country.originCountry }}
                                                        </option>
                                                    </select>
                                                </div>
                                            </div>
                                        </div>
                                        <div v-if="businessType == 'venue'">
                                            <div class="mb-2 fw-bold">
                                                Address <span style="color: red;">*</span>
                                            </div>
                                            <div class="mb-4">
                                                <input type="text" class="form-control" v-model="venueAddress">
                                            </div>
                                        </div>
                                        <div v-if="businessType == 'venue'">
                                            <div class="mb-2 fw-bold">
                                                Venue Type <span style="color: red;">*</span>
                                            </div>
                                            <div class="mb-4">
                                                <input type="text" class="form-control" v-model="venueType">
                                            </div>
                                        </div>
                                        <div>
                                            <div class="mb-2 fw-bold">
                                                Claim Status <span style="color: red;">*</span>
                                            </div>
                                            <div class="mb-4">
                                                <div class="form-check form-check-inline">
                                                    <input class="form-check-input" type="radio" id="claimed" v-model="businessClaimStatus" value="true" name="claim">
                                                    <label class="form-check-label text-start" for="claimed">Claimed</label>
                                                </div>
                                                <div class="form-check form-check-inline">
                                                    <input class="form-check-input" type="radio" id="unclaimed" v-model="businessClaimStatus" value="false" name="claim">
                                                    <label class="form-check-label text-start" for="unclaimed">Unclaimed</label>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="alert alert-danger" role="alert" v-if="addBizError != '' ">{{addBizError}}</div>
                                    </div>

                                    
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        <button v-if="!createBusinessSuccess && createBusinessError == ''" type="button" class="btn btn-primary" @click="createBusiness">Save changes</button>
                                    </div>
                                    </div>
                                </div>
                            </div>
                            <!-- add business modal end -->
                        </div>
                    </div>
                    <!-- add business end -->

                    <hr>

                    <!-- business account request -->
                    <div>
                        <div class="row text-center">
                            <div class="col-12">
                                <h3><b>Business Account Request</b></h3>
                            </div>
                        </div>
                        <div>
                            <div class="my-2">
                                <!-- filter request -->
                                <div class="form-check form-check-inline alert alert-warning ps-5" role="alert">
                                    <input class="form-check-input" type="checkbox" value="pendingApproval" id="flexCheckDefault" v-model="selectedAccountRequests" @change="filterAccountRequests">
                                    <label class="form-check-label" for="flexCheckDefault">
                                        Pending Approval
                                    </label>
                                </div>
                                <div class="form-check form-check-inline alert alert-info ps-5" role="alert">
                                    <input class="form-check-input" type="checkbox" value="pendingPayment" id="flexCheckChecked" v-model="selectedAccountRequests" @change="filterAccountRequests">
                                    <label class="form-check-label" for="flexCheckChecked">
                                        Pending Payment
                                    </label>
                                </div>
                                <div class="form-check form-check-inline alert alert-success ps-5" role="alert">
                                    <input class="form-check-input" type="checkbox" value="verified" id="flexCheckChecked" v-model="selectedAccountRequests" @change="filterAccountRequests">
                                    <label class="form-check-label" for="flexCheckChecked">
                                        Verified
                                    </label>
                                </div>
                                <div class="form-check form-check-inline alert alert-danger ps-5" role="alert">
                                    <input class="form-check-input" type="checkbox" value="rejected" id="flexCheckChecked" v-model="selectedAccountRequests" @change="filterAccountRequests">
                                    <label class="form-check-label" for="flexCheckChecked">
                                        Rejected
                                    </label>
                                </div>
                            
                            </div>

                            <div v-if="filteredAccountRequests.length > 0" class="row" style="height: 525px; overflow: auto">
                                <div v-for="request in filteredAccountRequests" class="col-md-6 col-lg-4 pb-4 pb-4" v-bind:key="request._id">
                                    <div class="card h-100" :style="{ backgroundColor: request.bgColor}">
                                        <div class="card-body">
                                        <span class="fw-bold">Business Information</span>
                                        <hr>
                                        <ul class="list-group list-group-flush text-start">
                                            <li class="list-group-item" :class="request.liClass"><span class="fw-bold">Type: </span> {{ request.businessType }} </li>
                                            <li class="list-group-item" :class="request.liClass"><span class="fw-bold">Name: </span> {{ request.businessName }} </li>
                                            <li class="list-group-item" :class="request.liClass"><span class="fw-bold">Description: </span> {{ request.businessDesc }} </li>
                                            <li class="list-group-item" :class="request.liClass"><span class="fw-bold">Country: </span> {{ request.country }} </li>
                                            <li class="list-group-item" :class="request.liClass"><span class="fw-bold">Site: </span> 
                                                <router-link v-if="request.businessLink" :to="{ path: request.businessLink }" style="color: inherit;">
                                                    Link
                                                </router-link> 
                                                <span v-if="!request.businessLink">N/A</span>
                                            </li>
                                        </ul>
                                        <hr>
                                        <span class="fw-bold">Requestor Information</span>
                                        <hr>
                                        <ul class="list-group list-group-flush text-start">
                                            <li class="list-group-item" :class="request.liClass"><span class="fw-bold">First Name: </span> {{ request.firstName }} </li>
                                            <li class="list-group-item" :class="request.liClass"><span class="fw-bold">Last Name: </span> {{ request.lastName }} </li>
                                            <li class="list-group-item" :class="request.liClass"><span class="fw-bold">Relationship: </span> {{ request.relationship }} </li>
                                            <li class="list-group-item" :class="request.liClass"><span class="fw-bold">Email: </span> {{ request.email }} </li>
                                            <li class="list-group-item" :class="request.liClass"><span class="fw-bold">Reference: </span>
                                                <a @click.prevent="openDocumentInNewTab(request.referenceDocument)" style="text-decoration: underline; cursor: pointer;">View Document</a>
                                            </li>
                                            <li class="list-group-item" :class="request.liClass"><span class="fw-bold">Price Plan: </span> {{ request.pricing }} </li>


                                        </ul>
                                        </div>
                                        <div v-if="request.isPending" class="card-footer">
                                            <!-- <button v-if="checkBusinessExist(request.businessLink)" class="btn btn-success btn-sm mx-3 my-1" type="button" style="width: 75px;" @click="reviewAccountRequest(request, 'approve')" data-bs-toggle="modal" data-bs-target="#addBusinessModal">Approve</button>
                                            <button v-else class="btn btn-primary btn-sm mx-3 my-1" type="button" style="width: 75px;" @click="reviewAccountRequest(request, 'add')" data-bs-toggle="modal" data-bs-target="#addBusinessModal">Add</button>
                                            <button class="btn btn-danger btn-sm mx-3 my-1" type="button" style="width: 75px;" @click="reviewAccountRequest(request, 'reject')">Reject</button> -->
                                            
                                            <button v-if="request.status == 'pendingApproval'" class="btn btn-success btn-sm mx-3 my-1" type="button" style="width: 125px;" @click="reviewAccountRequest(request, 'approve')">Approve</button>
                                            <button v-if="request.status == 'pendingPayment'" class="btn btn-primary btn-sm mx-3 my-1" type="button" style="width: 125px;" @click="reviewAccountRequest(request, 'resend')">Resend Email</button>
                                            <button v-if="request.isPending" class="btn btn-danger btn-sm mx-3 my-1" type="button" style="width: 125px;" @click="reviewAccountRequest(request, 'reject')">Reject</button>
                                        </div>
                                    </div>
                                </div>
                                        
                                
                            </div>
                            <div v-else>
                                No Business Account Requests to Show
                            </div>
                        </div>
                    </div>
                    <!-- business account request end -->
                </div>

            </div>
            <!-- navtabs end -->
            
        </div>
    </div>
</template>

<script>
    import NavBar from '@/components/NavBar.vue';

        export default {
            name: 'adminDashboard',
            components: {
                NavBar
            },
            data() {
                return {
                    // data from database
                    observationTags: [],
                    modRequests: [],
                    accountRequests: [],
                    selectedAccountRequests: ["pendingApproval", "pendingPayment"],
                    producers: [],
                    venues: [],
                    countries: [],
                    drinkTypes: [],

                    editedObservationTags: [],
                    editedFlavourTags: [],
                    pendingModRequests: [],
                    filteredAccountRequests: [],
                    moderators:[],

                    observationToDelete:'',
                    
                    //User 
                    user: null,
                    users: [],
                    promotedUser:'',
                    selectedPromotedUser:null,
                    promotedType:'',
                    selectedPromotedType:null,
                    removeMod:'',
                    selectedRemoveMod:null,
                    removedType:'',
                    selectedRemoveType:null,
                    removableDrinkType:[],
                    addableDrinkType:[],

                    // Flavour tag functions
                    newFamily:'',
                    newSub:'',
                    addFlavour:'',
                    editFlavour:'',
                    deleteFlavour:'',
                    hexcode:'',
                    tagParent:'',
                    chosenTagParent:null,
                    flavourNoChange:false,
                    subTagToDelete:'',
                    familyTagToDelete:'',
                    hexCodeValid: false,

                    // creation of new observation tag
                    newObservation:'',

                    // Error messages
                    errorMessages:'',

                    // flags
                    dataLoaded: false,
                    loadError: false,
                    editingObservation:false,
                    addingObservation:false,
                    selectingObservation:true,
                    deletingObservation:false,
                    nothingChanged:false,
                    successUpdateObservation:false,
                    invalidTag:false,
                    errorMessage:false,
                    errorUpdateObservation:false,
                    updatingObservation:false,
                    duplicateTag:false,
                    successCreateObservation:false,
                    submittingObservation:false,
                    errorCreateObservation:false,
                    errorDeletingObservation:false,
                    errorDeleteObservation:false,
                    successDeleteObservation:false,
                    notExistObservation:false,

                    confirmModerator:false,
                    successAddMod:false,
                    errorAddMod:false,
                    confirmRemoveModerator:false,
                    successRemoveMod:false,
                    errorRemoveMod:false,

                    showObservationControl: false,
                    showFlavourControl: false,
                    errorAddFlavour:false,
                    successAddFlavour:false,
                    confirmCreateFlavour:false,
                    errorEditFlavour:false,
                    successEditFlavour:false,
                    confirmEditFlavour:false,

                    errorDeleteFlavour:false,
                    successDeleteFlavour:false,

                    // Logged in user details
                    userID: null,
                    userType: localStorage.getItem('88B_accType'),

                    // create business
                    businessType: "",
                    businessName: "",
                    businessDesc: "",
                    businessCountry: "",
                    venueAddress: "",
                    venueType: "",
                    businessClaimStatus: "",
                    addBizError: "",
                    tempPassword: "",
                    createBusinessError: "",
                    createBusinessSuccess: false,
                    requestId: "",

                }
            },
            computed: {
                formattedPromotedModTypes() {
                    // Join the modType array elements with commas and spaces
                    if(this.selectedPromotedUser.modType.length === 0){
                        return "This user is currently not a moderator!"
                    }
                    else{
                        return "This user is currently a moderator for <b>" + this.selectedPromotedUser.modType.join(', ') +"</b>!";
                    }
                },
                formattedRemoveModTypes() {
                    // Join the modType array elements with commas and spaces
                    if(this.selectedRemoveMod.modType.length === 0){
                        return "This user is currently not a moderator!"
                    }
                    else{
                        return "This use is currently a moderator for <b>" + this.selectedRemoveMod.modType.join(', ') +"</b>!";
                    }
                },
            },
            mounted() {
                // Check if user is logged in
                this.userID = localStorage.getItem('88B_accID');

                if (this.userID == null) {
                    this.$router.push('/login');
                }
                else {
                    this.loadData();
                }
            },
            methods: {
                async loadData(){

                    // Check if admin, if not reroute to home page
                    // users
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getUsers');
                        this.users = response.data;
                        if (this.userType == "user") {
                            this.user = this.users.find(user => user["_id"]["$oid"] == this.userID);
                            if(!this.user.isAdmin){
                                this.$router.push('/');
                            }
                        }else{
                            this.$router.push('/');
                        }
                        this.moderators = this.users.filter(user => user.modType.length>=1);
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }
                    // observation tags
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getObservationTags');
                        this.observationTags = response.data;
                        this.editedObservationTags = JSON.parse(JSON.stringify(response.data));
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }
                    // mod requests
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getModRequests');
                        this.modRequests = response.data;
                        this.pendingModRequests = this.modRequests.filter(request => request.reviewStatus);
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }
                    // account requests
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getAccountRequests');
                        this.accountRequests = response.data;

                        this.accountRequests = response.data.map(request => {
                            if (request.isPending && !request.isApproved) {
                                request.status = 'pendingApproval';
                                request.bgColor = '#FFF2CD';
                                request.liClass = 'list-group-item-warning';
                            } else if (request.isPending && request.isApproved) {
                                request.status = 'pendingPayment';
                                request.bgColor = '#D0F4FC';
                                request.liClass = 'list-group-item-info';
                            } else if (!request.isPending && request.isApproved) {
                                request.status = 'verified';
                                request.bgColor = '#D1E6DD';
                                request.liClass = 'list-group-item-success';
                            } else {
                                request.status = 'rejected';
                                request.bgColor = '#F9D8DA';
                                request.liClass = 'list-group-item-danger';
                            }
                            return request;
                        });

                        this.filteredAccountRequests = this.accountRequests.filter(request => {
                            return this.selectedAccountRequests.includes(request.status)
                        });
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }
                    // producer
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getProducers');
                        this.producers = response.data;
                        // check for producer with no producer name and retrieve id
                        // [TO BE REMOVED?]
                        for (let i = 0; i < this.producers.length; i++) {
                            if (!this.producers[i].producerName) {
                                console.log("no name");
                                console.log(this.producers[i]._id.$oid);
                            }
                        }
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }
                    // venues
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getVenues');
                        this.venues = response.data;
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }
                    // countries
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getCountries');
                        this.countries = response.data;
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }
                    // drinkType
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getDrinkTypes');
                        this.drinkTypes = response.data;
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }
                    // flavour tag
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getFlavourTags');
                        this.flavourTags = response.data.map(item => {
                            return { ...item, showBox: false };
                        })                            
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }
                    // sub tags
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getData/getSubTags');
                        this.subTags = response.data
                        this.flavourTags.forEach(flavourTag => {
                            // Filter subtags belonging to the current flavor tag
                            const subTagsForFlavourTag = this.subTags.filter(subTag => subTag.familyTagId.$oid === flavourTag._id.$oid);
                            // Extract required information from subtags
                            const subTagsInfo = subTagsForFlavourTag.map(subTag=> ({
                                id: subTag._id,
                                subTag: subTag.subTag
                            }));
                            // Assign subtag information to flavor tag object
                            flavourTag.subTag2 = subTagsInfo;
                        });
                        
                        this.editedFlavourTags = JSON.parse(JSON.stringify(this.flavourTags));
                    } 
                    catch (error) {
                        console.error(error);
                        this.loadError = true;
                    }

                    this.dataLoaded = true;
                },

                addObservation(){
                    this.addingObservation=true
                    this.editingObservation=false
                    this.selectingObservation=false
                    this.deletingObservation=false
                },

                editObservation(){
                    this.addingObservation=false
                    this.editingObservation=true
                    this.selectingObservation=false
                    this.deletingObservation =false
                },

                deleteObservations(){
                    this.addingObservation=false
                    this.editingObservation=false
                    this.selectingObservation=false
                    this.deletingObservation= true
                },

                resetObservation(){
                    this.editingObservation=false
                    this.addingObservation=false
                    this.selectingObservation=true
                    this.updatingObservation = false
                    this.deletingObservation =false
                    this.submittingObservation =false
                    this.deletingObservation =false
                    this.resetErrors()
                },

                updateObservation(){
                    this.nothingChanged=false
                    let submitData = []
                    // Check if theres a change in observationTag, if there is, submit the data
                    for( let i=0;i<this.editedObservationTags.length;i++){
                        if(this.editedObservationTags[i].observationTag!= this.observationTags[i].observationTag){
                            submitData.push(this.editedObservationTags[i])
                            this.observationTags[i].observationTag = this.editedObservationTags[i].observationTag
                        }
                    }
                    if(submitData.length<=0){
                        let randoVariable = this.editedObservationTags[0].observationTag
                        this.editedObservationTags[0].observationTag="a"
                        this.editedObservationTags[0].observationTag= randoVariable
                        this.nothingChanged = true
                        return null
                    }
                    this.editingObservation=false;
                    this.updatingObservation = true;
                    if(this.observationTags.find((tag)=> tag.observationTag == '')){
                        this.emptyObservation = true
                    }
                    let submitAPI = "http://127.0.0.1:5000/adminFunctions/updateObservationTag"
                    this.updateTags(submitAPI,submitData)
                },

                async updateTags(submitAPI,submitData){
                    let responseCode = ''
                    const response = await this.$axios.put(submitAPI, submitData)
                    .then((response)=>{
                        responseCode = response.data.code
                    })
                    .catch((error)=>{
                        console.error(error);
                        responseCode = error.response.data.code
                        this.errorMessages+=error.response.data.message
                    });
                    this.updatingObservation = false
                    if(responseCode==201){
                        this.successUpdateObservation=true; // Display success message
                    }else{
                        this.errorUpdateObservation = true
                        if(responseCode==400){
                            this.invalidTag = true // Display duplicate entry message
                        }else{
                            this.errorMessage = true // Display generic error message
                        }
                    }
                    return response
                },

                resetErrors(){
                    this.successUpdateObservation = false
                    this.errorUpdateObservation = false
                    this.invalidTag = false
                    this.errorMessage = false
                    this.successCreateObservation = false
                    this.errorCreateObservation = false
                    this.duplicateTagTag = false
                    this.errorMessage = false
                    this.selectingObservation = true
                    this.errorDeletingObservation = false
                    this.errorDeleteObservation = false
                    this.successDeleteObservation = false
                    this.notExistObservation = false
                },

                createNewObservation(){
                    if(this.newObservation==""){
                        alert('Please fill in the observation tag')
                        return null
                    }
                    this.submittingObservation=true
                    this.addingObservation=false
                    let submitAPI = "http://127.0.0.1:5000/adminFunctions/createObservationTag"
                    let submitData = {"observationTag":this.newObservation}
                    this.createTag(submitAPI, submitData)
                },

                async createTag(submitAPI, submitData){
                    let responseCode = ''
                    let newObservationId = ''
                    const response = await this.$axios.post(submitAPI, submitData)
                    .then((response)=>{
                        responseCode = response.data.code
                        newObservationId = response.data.data
                    })
                    .catch((error)=>{
                        console.error(error);
                        responseCode = error.response.data.code
                    });
                    this.submittingObservation = false
                    if(responseCode==201){
                        this.successCreateObservation=true; // Display success message
                        this.editedObservationTags.push({
                            _id:{'$oid': newObservationId},
                            observationTag: this.newObservation
                        })
                        this.observationTags.push({
                            _id:{'$oid': newObservationId},
                            observationTag: this.newObservation
                        })
                        
                    }else{
                        this.errorCreateObservation = true
                        if(responseCode==400){
                            this.duplicateTag = true // Display duplicate entry message
                        }else{
                            this.errorMessage = true // Display generic error message
                        }
                    }
                    return response
                }, 

                deleteObservation(tagId,tag){
                    // alert(tagId.$oid)
                    this.observationToDelete = {"tagId":tagId, "observationTag":tag}
                },
                async confirmDeleteTag(){
                    let responseCode = ''
                    let deleteAPI = "http://127.0.0.1:5000/adminFunctions/deleteObservationTag/" + this.observationToDelete.tagId.$oid
                    const response = await this.$axios.delete(deleteAPI)
                    .then((response)=>{
                        responseCode = response.data.code
                    })
                    .catch((error)=>{
                        console.error(error);
                        responseCode = error.response.data.code
                    });
                    if(responseCode==200){
                        this.successDeleteObservation=true; // Display success message
                        this.deletingObservation=false; // Hide submission in progress message
                        let observationToRemove = this.observationTags.findIndex(obj => obj._id.$oid === this.observationToDelete.tagId.$oid);
                        if (observationToRemove !== -1) {
                            this.observationTags.splice(observationToRemove, 1);
                        }
                    }else{
                        this.errorDeletingObservation=true; // Display error message
                        this.deletingObservation=false; // Hide submission in progress message
                        if(responseCode==400){
                            this.notExistObservation = true // Display duplicate entry message
                        }else{
                            this.errorDeleteObservation = true // Display generic error message
                        }
                    }
                    this.observationToDelete = ''
                    return response
                },
                resetDeleteTag(){
                    this.observationToDelete=''
                },

                getUserbyID(userID) {
                    return this.users.find(user => user["_id"]["$oid"] == userID["$oid"]);
                }, 
                async reviewModRequest(request, action) {
                    const requestID = request._id.$oid;
                    // update users db
                    if (action == "approve") {
                        const userID = request.userID.$oid;
                        const newModType = request.drinkType;

                        try {
                            await this.$axios.post('http://127.0.0.1:5000/editProfile/updateModType', 
                                {
                                    userID: userID,
                                    newModType: newModType,
                                }, {
                                headers: {
                                    'Content-Type': 'application/json'
                                }
                            });
                        } catch (error) {
                            console.error(error);
                        }
                    }
                    
                    // update mod request db
                    try {
                        await this.$axios.post('http://127.0.0.1:5000/editModRequests/updateModRequest', 
                            {
                                requestID: requestID,
                                reviewStatus: false,
                            }, {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });
                    } catch (error) {
                        console.error(error);
                    }
                    
                    // update frontend
                    const index = this.modRequests.findIndex(request => request._id.$oid == requestID);
                    this.modRequests[index].reviewStatus = false;
                    this.pendingModRequests = this.modRequests.filter(request => request.reviewStatus);

                }, 
                checkBusinessExist(businessLink) {
                    if (businessLink) {
                        const businessID = businessLink.split("/").pop()
                        if (this.producers.find(producer => producer._id.$oid == businessID)) {
                            return true;
                        }
                        if (this.venues.find(venue => venue._id.$oid == businessID)) {
                            return true;
                        }
                    }
                    return false;
                },

                hashPassword(id, password) {
                    const combinedString = id.toString() + password;
                    let hash = 0;

                    for (let i = 0; i < combinedString.length; i++) {
                        const char = combinedString.charCodeAt(i);
                        hash = (hash << 5) - hash + char;
                        hash |= 0; // convert to 32-bit integer
                    }

                    return hash;
                },

                async reviewAccountRequest(request, action) {
                    const requestID = request._id.$oid;
                    if (action == "approve") {
                        this.businessType = request.businessType;
                        const businessID = request.businessLink.split("/").pop()

                        const businessExist = this.checkBusinessExist(request.businessLink);

                        if (businessExist) {
                            this.businessName = request.businessName;
                            this.tempPassword = this.hashPassword(request.businessName).toString();
                            this.tempPassword = this.tempPassword.replace(/-/g, '');
                            const hashedPassword = this.hashPassword(request.businessName, this.tempPassword);
    
                            const newBusinessData = {
                                businessName: request.businessName,
                                businessDesc: request.businessDesc,
                                country: request.country,
                                hashedPassword: hashedPassword,
                                claimStatus: false,
                                requestId: requestID,
                            }
                            let apiURL = '';
    
                            // producers
                            if (request.businessType == "producer") {
                                apiURL = 'http://127.0.0.1:5000/editProducerProfile/updateProducerStatus';
                            }
                            // venues 
                            else if (request.businessType == "venue") {
                                apiURL = 'http://127.0.0.1:5000/editVenueProfile/updateVenueStatus';
                            }
    
                            if (apiURL != '') {
                                try {
                                    const response = await this.$axios.post(apiURL, 
                                        {
                                            businessID: businessID,
                                            newBusinessData: newBusinessData,
                                        }, {
                                        headers: {
                                            'Content-Type': 'application/json'
                                        }
                                    });
    
                                    if (response.data.code == 201) {
                                        this.createBusinessSuccess = true;
                                    } 
    
                                } catch (error) {
                                    console.error(error);
                                }
                            }

                            // token
                            const link = await this.generateToken(businessID, request._id.$oid);
                            this.emailLink(request, link);

                        } 
                        else {
                            this.businessType = request.businessType;
                            this.businessName = request.businessName;
                            this.businessDesc = request.businessDesc;
                            this.businessCountry = request.country;
                            this.venueAddress = request.country;
                            this.venueType = 'Bar';
                            this.businessClaimStatus = "false";
                            this.requestId = request._id.$oid;
                            const createSuccess = await this.createBusiness();
                            if (!createSuccess) {
                                return;
                            }
                            const link = await this.generateToken(createSuccess, request._id.$oid)
                            this.emailLink(request, link);
                        }

                        // update review status
                        try {
                            await this.$axios.post('http://127.0.0.1:5000/createAccount/updateAccountRequest', 
                                {
                                    requestID: requestID,
                                    isPending: true,
                                    isApproved: true,
                                }, {
                                headers: {
                                    'Content-Type': 'application/json'
                                }
                            });
                        } catch (error) {
                            console.error(error);
                        }

                        // update frontend
                        const index = this.accountRequests.findIndex(request => request._id.$oid == requestID);
                        this.accountRequests[index].isPending = true;
                        this.accountRequests[index].isApproved = true;

                        this.accountRequests[index].status = 'pendingPayment';
                        this.accountRequests[index].bgColor = '#D0F4FC';
                        this.accountRequests[index].liClass = 'list-group-item-info';

                        this.filterAccountRequests();
                    } 
                    else if (action == "reject") {
                        // update review status
                        try {
                            await this.$axios.post('http://127.0.0.1:5000/createAccount/updateAccountRequest', 
                                {
                                    requestID: requestID,
                                    isPending: false,
                                    isApproved: false,
                                }, {
                                headers: {
                                    'Content-Type': 'application/json'
                                }
                            });
                        } catch (error) {
                            console.error(error);
                        }

                        // delete token if exist
                        try {
                            const response = await this.$axios.get(`http://127.0.0.1:5000/getData/getTokenByRequestId/${requestID}`);
                            const tokenData = response.data;
                            if (Object.keys(tokenData).length > 0) {
                                this.deleteToken(tokenData.token)
                            }
                        } 
                        catch (error) {
                            console.error(error);
                        }

                        // update frontend
                        const index = this.accountRequests.findIndex(request => request._id.$oid == requestID);
                        this.accountRequests[index].isPending = false;
                        this.accountRequests[index].isApproved = false;

                        this.accountRequests[index].status = 'rejected';
                        this.accountRequests[index].bgColor = '#F9D8DA';
                        this.accountRequests[index].liClass = 'list-group-item-danger';

                        this.filterAccountRequests();
                        
                    }

                    else if (action == "resend") {
                        try {
                            const requestId = request._id.$oid;
                            console.log(requestId);
                            const response = await this.$axios.get(`http://127.0.0.1:5000/getData/get${request.businessType.charAt(0).toUpperCase()}${request.businessType.slice(1)}ByRequestId/${requestId}`);
                            console.log(response);
                            const businessId = response.data._id.$oid;
                            console.log(businessId);
                            const link = await this.generateToken(businessId, requestId)
                            console.log(link);
                            this.emailLink(request, link);
                        } catch (error) {
                            console.error(error);
                        }
                    }

                }, 
                async createBusiness() {

                    // form control
                    if (this.businessType == "" || this.businessName == "" || this.businessDesc == "" || this.businessCountry == "" || this.businessClaimStatus == "" || (this.businessType == "venue" && (this.venueAddress == "" || this.venueType == ""))) {
                        this.addBizError = "Please fill in all fields";
                    }
                    else {
                        this.addBizError = "";
                        this.tempPassword = "admin1234";
                        const hashedPassword = this.hashPassword(this.businessName, this.tempPassword);
                        if (this.businessType == "producer") {
                            const newBusinessData = {
                                producerName: this.businessName,
                                producerDesc: this.businessDesc,
                                originCountry: this.businessCountry,
                                statusOB: "",
                                mainDrinks: [],
                                photo: "",
                                hashedPassword: hashedPassword,
                                questionsAnswers: [],
                                updates: [],
                                producerLink: "",
                                claimStatus: this.businessClaimStatus === "false",
                            }
                            try {
                                const response = await this.$axios.post('http://127.0.0.1:5000/createAccount/createProducerAccount', 
                                    {
                                        newBusinessData
                                    }, {
                                    headers: {
                                        'Content-Type': 'application/json'
                                    }
                                });

                                if (response.data.code == 201) {
                                    this.createBusinessSuccess = true;
                                    return response.data.data._id
                                } 
                            } catch (error) {
                                console.error(error);
                                if (error.response.data.code == 400) {
                                    this.createBusinessError = "Business name already exists";
                                    return false;
                                }
                            }
                        }
                        else if (this.businessType == "venue") {
                            const newBusinessData = {
                                venueName: this.businessName,
                                venueDesc: this.businessDesc,
                                originLocation: this.businessCountry,
                                address: this.venueAddress,
                                venueType: this.venueType,
                                menu: [],
                                photo: "",
                                hashedPassword: hashedPassword,
                                questionsAnswers: [],
                                updates: [],
                                claimStatus: this.businessClaimStatus === "false",
                                openingHours: {
                                    Monday: ["", ""],
                                    Tuesday: ["", ""],
                                    Wednesday: ["", ""],
                                    Thursday: ["", ""],
                                    Friday: ["", ""],
                                    Saturday: ["", ""],
                                    Sunday: ["", ""],
                                },
                                publicHolidays: "",
                                reservationDetails: "",
                                requestId: this.requestId
                            }
                            try {
                                const response = await this.$axios.post('http://127.0.0.1:5000/createAccount/createVenueAccount', 
                                    {
                                        newBusinessData
                                    }, {
                                    headers: {
                                        'Content-Type': 'application/json'
                                    }
                                });

                                if (response.data.code == 201) {
                                    this.createBusinessSuccess = true;
                                    return response.data.data._id
                                } 
                            } catch (error) {
                                console.error(error);
                                if (error.response.data.code == 400) {
                                    this.createBusinessError = "Business name already exists";
                                    return false;
                                }
                            }
                        }
                    }
                }, 
                // reset when add a business button is clicked
                resetAddBusinessModal() {
                    this.businessType = "";
                    this.businessName = "";
                    this.businessDesc = "";
                    this.businessCountry = "";
                    this.venueAddress = "";
                    this.venueType = "";
                    this.businessClaimStatus = "";
                    this.tempPassword = "";
                    this.createBusinessSuccess = false;
                    this.createBusinessError = "";
                },

                async generateToken(businessId, requestId) {
                    try {
                        const response = await this.$axios.post('http://127.0.0.1:5000/createAccount/createToken', 
                            {
                                businessId: businessId,
                                requestId: requestId,
                                isNew: true,
                            }, {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });
                        const link = `http://localhost:8080/billingSecurity?token=${response.data.data.token}`;
                        console.log(link);
                        return link;
                    } catch (error) {
                        console.error(error);
                    }
                },

                async emailLink(request, link) {

                    const emailDetails = {
                        recipient: request.email,
                        subject: "Reset Your Password with Drink X",
                        message: `Hi ${request.firstName}, \n\nClick on the link below to reset your password: \n${link} \n\nIf you did not initiate this request, please contact us immediately. \n\nThank you, \nDrinkX`
                    };
                    try {
                        await this.$axios.post('http://127.0.0.1:5000/createAccount/sendEmail', emailDetails);
                    } catch (error) {
                        console.error('Failed to send email:', error);
                    }
                },

                updateUsername(){
                    // get error message element
                    let usernameError = document.getElementById("usernameError")
                    // find listing based on bottle name
                    let user = this.users.find(user => user.username === this.promotedUser)
                    if (user) {
                        this.selectedPromotedUser = user
                        usernameError.innerHTML = ""
                        let currentMod = user.modType
                        this.addableDrinkType = this.drinkTypes.filter(drinkType=>{
                            return !currentMod.includes(drinkType.drinkType);
                        })
                        this.addableDrinkType.sort((a, b) => a.drinkType.localeCompare(b.drinkType))

                    }
                    else {
                        this.selectedPromotedUser = null
                        this.addableDrinkType= []
                        usernameError.innerHTML = "Please enter a valid username"
                    }
                },
                updateModUsername(){
                    // get error message element
                    let usernameError = document.getElementById("modUsernameError")
                    // find listing based on bottle name
                    let user = this.moderators.find(user => user.username === this.removeMod)
                    if (user) {
                        this.selectedRemoveMod = user
                        usernameError.innerHTML = ""
                        let currentMod = user.modType
                        this.removableDrinkType = this.drinkTypes.filter(drinkType=>{
                            return currentMod.includes(drinkType.drinkType);
                        })
                        this.removableDrinkType.sort((a, b) => a.drinkType.localeCompare(b.drinkType))
                    }
                    else {
                        this.selectedRemoveMod = null
                        this.removableDrinkType = []
                        usernameError.innerHTML = "Please enter a valid username"
                    }
                },

                updateDrinkType(){
                    // get error message element
                    let promotedTypeError = document.getElementById("promotedTypeError")
                    // find listing based on bottle name
                    let drinkType = this.drinkTypes.find(drinkType => drinkType.drinkType === this.promotedType)
                    if (drinkType) {
                        this.selectedPromotedType = drinkType
                        promotedTypeError.innerHTML = ""
                    }
                    else {
                        this.selectedPromotedType = null
                        promotedTypeError.innerHTML = "Please enter a valid drink type"
                    }
                },
                updateRemovedDrinkType(){
                    // get error message element
                    let removedTypeError = document.getElementById("removedTypeError")
                    // find listing based on bottle name
                    let drinkType = this.drinkTypes.find(drinkType => drinkType.drinkType === this.removedType)
                    if (drinkType) {
                        this.selectedRemoveType = drinkType
                        removedTypeError.innerHTML = ""
                    }
                    else {
                        this.selectedRemoveType = null
                        removedTypeError.innerHTML = "Please enter a valid drink type"
                    }
                },

                addModerator(){
                    let errorMessage = ''
                    if(this.selectedPromotedUser == null){
                        errorMessage+="Please enter a valid username!\n"
                    }
                    if(this.selectedPromotedType == null){
                        errorMessage+="Please enter a valid drink type!\n"
                    }
                    if(errorMessage!=''){
                        alert(errorMessage)
                        return null
                    }
                    let alreadyModError = document.getElementById("alreadyModError")
                    if(this.selectedPromotedUser.modType.includes(this.selectedPromotedType.drinkType)){
                        alreadyModError.innerHTML = "This user is already a moderator for this drink type"
                        return null
                    }else{
                        alreadyModError.innerHTML = ""
                    }
                    this.confirmModerator = true
                    
                },
                removeModerator(){
                    let errorMessage = ''
                    if(this.selectedRemoveMod == null){
                        errorMessage+="Please enter a valid username!\n"
                    }
                    if(this.selectedRemoveType == null){
                        errorMessage+="Please enter a valid drink type!\n"
                    }
                    if(errorMessage!=''){
                        alert(errorMessage)
                        return null
                    }
                    let notModError = document.getElementById("notModError")
                    if(!this.selectedRemoveMod.modType.includes(this.selectedRemoveType.drinkType)){
                        notModError.innerHTML = "This user is not a moderator for this drink type"
                        return null
                    }else{
                        notModError.innerHTML = ""
                    }
                    this.confirmRemoveModerator = true
                    
                },

                async confirmAddModerator(){
                    try {
                        await this.$axios.post('http://127.0.0.1:5000/editProfile/updateModType', 
                            {
                                userID: this.selectedPromotedUser._id.$oid,
                                newModType: this.selectedPromotedType.drinkType,
                            }, {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        }).then(response => {
                            // Handle the response here
                            if(response.data.code == 201){
                                this.successAddMod = true
                                this.confirmModerator = false
                                this.selectedPromotedUser.modType.push(this.selectedPromotedType.drinkType)
                            }
                        });
                    } catch (error) {
                        console.error(error);
                        this.errorAddMod = true
                        this.confirmModerator = false
                    }
                },
                async confirmDowngradeModerator(){
                    try {
                        await this.$axios.post('http://127.0.0.1:5000/editProfile/removeModType', 
                            {
                                userID: this.selectedRemoveMod._id.$oid,
                                removeModType: this.selectedRemoveType.drinkType,
                            }, {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        }).then(response => {
                            // Handle the response here
                            if(response.data.code == 201){
                                this.successRemoveMod = true
                                this.confirmRemoveModerator = false
                                let modToDowngrade = this.selectedRemoveMod.modType.findIndex(obj => obj === this.selectedRemoveType.drinkType);
                                if (modToDowngrade !== -1) {
                                    this.selectedRemoveMod.modType.splice(modToDowngrade, 1);
                                }
                            }
                        });
                    } catch (error) {
                        console.error(error);
                        this.errorRemoveMod = true
                        this.confirmRemoveModerator = false
                    }
                },

                selectPromotedUser(){
                    this.confirmModerator=false
                    this.successAddMod = false
                    this.errorAddMod = false
                },
                selectRemoveMod(){
                    this.confirmRemoveModerator=false
                    this.successRemoveMod = false
                    this.errorRemoveMod = false
                },
                resetAddMod(){
                    this.confirmModerator=false
                    this.selectedPromotedType = null
                    this.selectedPromotedUser = null
                    this.promotedType=''
                    this.promotedUser=''
                    this.successAddMod = false
                    this.errorAddMod = false
                },
                resetRemoveMod(){
                    this.confirmRemoveModerator=false
                    this.selectedRemoveType = null
                    this.selectedRemoveMod = null
                    this.removedType=''
                    this.removeMod=''
                    this.successRemoveMod = false
                    this.errorRemoveMod = false
                },

                downloadCSV() {
                    let csvContent = "data:text/csv;charset=utf-8,";

                    let csvData = [
                        ['Name', 'Temporary Password'],
                        [this.businessName, this.tempPassword]
                    ]

                    csvData.forEach(row => {
                        csvContent += row + "\n";
                    });

                    const encodedUri = encodeURI(csvContent);
                    const link = document.createElement("a");
                    link.setAttribute("href", encodedUri);
                    link.setAttribute("download", "loginDetail.csv");
                    document.body.appendChild(link);
                    link.click();
                },

                toggleFlavourControl(){
                    this.showObservationControl = false
                    this.showFlavourControl = !this.showFlavourControl
                },

                toggleObservationControl(){
                    this.showFlavourControl=false
                    this.showObservationControl = !this.showObservationControl
                },

                setAddFlavour(mode){
                    this.addFlavour = mode
                },

                setEditFlavour(mode){
                    this.editFlavour = mode
                },

                setDeleteFlavour(mode){
                    this.deleteFlavour = mode
                },

                resetFlavourMode(){
                    this.addFlavour = ''
                },

                resetEditFlavourMode(){
                    this.editFlavour = ''
                    this.confirmEditFlavour = false
                },
                isValidHexCode() {
                    // Regular expression pattern to match hexadecimal color codes
                    var hexPattern = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;
                    if(hexPattern.test("#" + this.hexcode)){
                        this.hexCodeValid = true
                    }else{
                        this.hexCodeValid = false
                    }
                    return null
                    // Check if the hex code matches the pattern
                },
                createNewFlavour(){
                    let submitURL = ''
                    let submitData= {}
                    
                    if(this.addFlavour == 'family'){
                        submitURL = 'http://127.0.0.1:5000/adminFunctions/createFamilyTag'
                        submitData = {
                            hexcode: '#' + this.hexcode,
                            familyTag: this.newFamily
                        }

                    }
                    else if(this.addFlavour == 'sub'){
                        submitURL = 'http://127.0.0.1:5000/adminFunctions/createSubTag'
                        submitData = {
                            familyTagId: this.chosenTagParent._id.$oid,
                            subTag: this.newSub
                        }
                    }
                    this.writeNewFlavourTag(submitURL, submitData)
                },  

                async writeNewFlavourTag(submitURL,submitData){
                    let responseCode = ''
                    let tagNewId = ''
                    const response = await this.$axios.post(submitURL, submitData)
                    .then((response)=>{
                        responseCode = response.data.code
                        tagNewId = response.data.data
                    })
                    .catch((error)=>{
                        console.error(error);
                        responseCode = error.response.data.code
                    });
                    if(responseCode==201){
                        this.successAddFlavour=true; // Display success message
                        if(this.addFlavour=='family'){
                            this.editedFlavourTags.push({
                                familyTag: this.newFamily,
                                hexcode: '#' + this.hexcode,
                                subTag2: [],
                                showBox: false,
                                _id: {'$oid': tagNewId}
                            })
                            this.flavourTags.push({
                                familyTag: this.newFamily,
                                hexcode: '#' + this.hexcode,
                                subTag2: [],
                                showBox: false,
                                _id: {'$oid': tagNewId}
                            })
                        }
                        if(this.addFlavour=='sub'){
                            let parentTagIndex = this.editedFlavourTags.findIndex(flavourTag=>{
                                return flavourTag._id.$oid == this.chosenTagParent._id.$oid
                            })
                            if (parentTagIndex !== -1) {
                                // Update the editedFlavourTags array
                                this.editedFlavourTags[parentTagIndex].subTag2.push({
                                    id: { '$oid': tagNewId },
                                    subTag: this.newSub
                                });
                                this.flavourTags[parentTagIndex].subTag2.push({
                                    id: { '$oid': tagNewId },
                                    subTag: this.newSub
                                });
                            }
                        }
                    }else{
                        this.errorAddFlavour = true
                    }
                    return response
                },

                confirmAddFlavour(){
                    if(this.addFlavour=='sub'){
                        if(this.chosenTagParent != null){
                            this.confirmCreateFlavour = true
                        }else{
                            alert('Please choose a valid family tag!')
                            return null
                        }
                    }else{
                        if(!this.hexCodeValid){
                            alert('Hexcode is not valid')
                            return null
                        }
                        if(this.newFamily == ''){
                            alert('Please enter a family tag')
                            return null
                        }
                        this.confirmCreateFlavour = true
                    }
                },

                resetFlavourModal(){
                    this.successAddFlavour = false
                    this.errorAddFlavour = false
                    this.addFlavour = ''
                    this.confirmCreateFlavour= false
                },

                resetFlavourErrors(){
                    this.successAddFlavour = false
                    this.errorAddFlavour = false
                    this.confirmCreateFlavour= false
                },

                resetEditFlavourModal(){
                    this.successEditFlavour = false
                    this.errorEditFlavour = false
                    this.editFlavour = ''
                    this.confirmEditFlavour= false
                    this.flavourNoChange= false
                },

                resetEditFlavourErrors(){
                    this.successEditFlavour = false
                    this.errorEditFlavour = false
                    this.confirmEditFlavour= false
                    this.flavourNoChange= false
                },

                resetEditFlavour(){
                    this.editedFlavourTags = JSON.parse(JSON.stringify(this.flavourTags));
                },
                
                updateTagParent(){
                    // get error message element
                    let tagParentError = document.getElementById("tagParentError")
                    // find listing based on bottle name
                    let familyTag = this.flavourTags.find(tag => tag.familyTag === this.tagParent)
                    if (familyTag) {
                        this.chosenTagParent = familyTag
                        tagParentError.innerHTML = ""
                    }
                    else {
                        this.chosenTagParent = null
                        tagParentError.innerHTML = "Please enter a valid drink type"
                    }
                },

                toggleBox(family){
                    let tempShowBox = family.showBox
                    this.editedFlavourTags.forEach(item => {
                        item.showBox = false;
                    });
                    family.showBox = !tempShowBox; // Toggle the visibility of the box
                },

                confirmUpdateFlavour(){
                    this.confirmEditFlavour = true
                },

                updateExistingFlavour(){
                    // check difference in editedFlavourTags and flavourTags
                    // for familytag mode, check the familyTag
                    // for sub mode, check subTag2 difference
                    let submitData=[]
                    let submitURL=''
                    if(this.editFlavour=='family'){
                        submitURL = 'http://127.0.0.1:5000/adminFunctions/updateFamilyTag'
                        for( let i=0;i<this.editedFlavourTags.length;i++){
                            if(this.editedFlavourTags[i].familyTag!= this.flavourTags[i].familyTag || this.editedFlavourTags[i].hexcode!= this.flavourTags[i].hexcode){
                                submitData.push(
                                    {
                                        _id: this.editedFlavourTags[i]._id.$oid,
                                        familyTag: this.editedFlavourTags[i].familyTag,
                                        hexcode: this.editedFlavourTags[i].hexcode,
                                    }
                                )
                            }
                        }
                    }
                    if(this.editFlavour=='sub'){
                        submitURL = 'http://127.0.0.1:5000/adminFunctions/updateSubTag'
                        for( let i=0;i<this.editedFlavourTags.length;i++){
                            for(let j=0; j<this.editedFlavourTags[i].subTag2.length;j++){
                                if(this.editedFlavourTags[i].subTag2[j].subTag != this.flavourTags[i].subTag2[j].subTag){
                                    submitData.push(
                                        {
                                            _id: this.editedFlavourTags[i].subTag2[j].id.$oid,
                                            subTag: this.editedFlavourTags[i].subTag2[j].subTag
                                        }
                                    )
                                }
                            }
                        }
                    }
                    if(submitData.length<=0){
                        this.flavourNoChange = true
                        return null
                    }
                    this.writeEditTag(submitURL, submitData)
                },

                async writeEditTag(submitURL,submitData){
                    let responseCode = ''
                    const response = await this.$axios.put(submitURL, submitData)
                    .then((response)=>{
                        responseCode = response.data.code
                    })
                    .catch((error)=>{
                        console.error(error);
                        responseCode = error.response.data.code
                    });
                    if(responseCode==201){
                        this.successEditFlavour=true; // Display success message
                    }else{
                        this.errorEditFlavour = true
                    }
                    this.flavourTags = JSON.parse(JSON.stringify(this.editedFlavourTags));
                    return response
                },

                selectDeleteSub(id, subTag, hexcode){
                    this.subTagToDelete = {"_id":id.$oid, "subTag":subTag, "hexcode": hexcode}
                },
                selectDeleteFamily(id, familyTag, hexcode, subTag2){
                    this.familyTagToDelete = {"_id":id.$oid, "familyTag":familyTag, "hexcode": hexcode, subTag2}
                },

                resetDeleteSubTag(){
                    this.subTagToDelete = ''
                },
                resetDeleteFamilyTag(){
                    this.familyTagToDelete = ''
                },

                confirmDeleteFlavourTag(){
                    let submitURL = ''
                    if(this.deleteFlavour=='family'){
                        submitURL = 'http://127.0.0.1:5000/adminFunctions/deleteFamilyTag/' + this.familyTagToDelete._id
                    }
                    if(this.deleteFlavour=='sub'){
                        submitURL = 'http://127.0.0.1:5000/adminFunctions/deleteSubTag/' + this.subTagToDelete._id
                        
                    }
                    this.writeDeleteTag(submitURL)
                },

                async writeDeleteTag(submitURL){
                    let responseCode = ''
                    const response = await this.$axios.delete(submitURL)
                    .then((response)=>{
                        responseCode = response.data.code
                    })
                    .catch((error)=>{
                        console.error(error);
                        responseCode = error.response.data.code
                    });
                    if(responseCode==201){
                        this.successDeleteFlavour=true; // Display success message
                        if(this.deleteFlavour == 'sub'){
                            this.editedFlavourTags = this.editedFlavourTags.map(item => {
                                // Filter the subTags array of each main object to remove the one with the specified ID
                                const updatedSubTags = item.subTag2.filter(subTag => subTag.id.$oid !== this.subTagToDelete._id);
                                // Return a new object with the updated subTags array
                                return { ...item, subTag2: updatedSubTags };
                            });
                            this.flavourTags = this.flavourTags.map(item => {
                                // Filter the subTags array of each main object to remove the one with the specified ID
                                const updatedSubTags = item.subTag2.filter(subTag => subTag.id.$oid !== this.subTagToDelete._id);
                                // Return a new object with the updated subTags array
                                return { ...item, subTag2: updatedSubTags };
                            });
                        }
                        if(this.deleteFlavour == 'family'){
                            this.editedFlavourTags = this.editedFlavourTags.filter(flavourTag=>{
                                return flavourTag._id.$oid != this.familyTagToDelete._id
                            })
                            this.flavourTags = this.flavourTags.filter(flavourTag=>{
                                return flavourTag._id.$oid != this.familyTagToDelete._id
                            })
                        }
                    }else{
                        this.errorDeleteFlavour = true
                    }
                    return response
                },

                resetDeleteFlavourModal(){
                    this.successDeleteFlavour = false;
                    this.errorDeleteFlavour = false;
                    this.subTagToDelete = ''
                    this.familyTagToDelete = ''
                    this.deleteFlavour = ''
                },

                resetDeleteFlavourMode(){
                    this.successDeleteFlavour = false;
                    this.errorDeleteFlavour = false;
                    this.subTagToDelete = ''
                    this.familyTagToDelete = ''
                },

                filterAccountRequests() {
                    this.filteredAccountRequests = this.accountRequests.filter(request => {
                        return this.selectedAccountRequests.includes(request.status)
                    });
                    
                },
                openDocumentInNewTab(referenceDocument) {
                    const byteCharacters = atob(referenceDocument);
                    const byteNumbers = new Array(byteCharacters.length);
                    for (let i = 0; i < byteCharacters.length; i++) {
                        byteNumbers[i] = byteCharacters.charCodeAt(i);
                    }
                    const byteArray = new Uint8Array(byteNumbers);
                    const blob = new Blob([byteArray], { type: 'application/pdf' });
                    const blobUrl = URL.createObjectURL(blob);
                    
                    const newTab = window.open(blobUrl, '_blank');
                    if (!newTab || newTab.closed || typeof newTab.closed == 'undefined') {
                        alert('Pop-up blocker is preventing the document from opening. Please allow pop-ups for this site.');
                    }
                },
                async deleteToken(token) {
                    try {
                        const response = await this.$axios.post(`http://127.0.0.1:5000/createAccount/deleteToken`,
                            {
                                token: token,
                            }, {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });
                        console.log(response.data);

                    } catch (error) {
                        console.error(error);
                    }
                },
            }
        }
</script>