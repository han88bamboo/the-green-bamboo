<!-- Component for submitting new listings (both requests + actual) -->
<!--
    formType: req (request), power (actual)
    formMode: new, edit, dup (duplicate)
-->

<!--
    TODO:
    - "Return" button may bring user back to same page, but with form cleared. Prevent that by returning to last notable page. (optional)
    - Consider another backend check to ensure that submitter is authorized to submit listing in specified mode, with valid producerID for producers.
    - Should we save the form data for easier retry when invoking reset()? Should reset() just hard refresh the page?
-->

<template>
    <div class="container pt-3 pb-5">

        <!-- Display when data is still loading / form is being submitted -->
        <div class="text-info-emphasis fst-italic fw-bold fs-5" v-if="submitForm || !dataLoaded">
            <span v-if="!dataLoaded">Loading form, please wait...</span>
            <span v-if="submitForm">The form is being submitted, please hold on!</span>
            <br><br>
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        
        <!-- Display when bottle listing is successfully submitted -->
        <div class="text-success fw-bold fs-5" v-if="successSubmission"> 
            <div v-if="formType == 'req'">
                <span v-if="formMode == 'new'">The request has successfully been submitted! The listing is now on Drink-X and can be reviewed (or added to a menu)! 😉 </span>
                <span v-if="formMode == 'edit'">The edit request has successfully been submitted!</span>
                <span v-if="formMode == 'dup'">The duplicate report has successfully been submitted!</span>
            </div>
            <div v-if="formType == 'power'">
                <span v-if="formMode == 'new' && requestRemoval == false">The drink listing has successfully been created!</span>
                <span v-if="formMode == 'edit' && requestRemoval == false">The drink listing has successfully been edited!</span>
                <span v-if="requestRemoval == true">The request has successfully been removed!</span>
            </div>
            <br>
            <button class="btn primary-btn btn-sm" @click="reset" v-if="formMode == 'new'">
                <span class="fs-6"> Submit another drink listing here! </span>
            </button>
            <button class="btn primary-btn btn-sm" @click="goBack" v-if="formMode != 'new'">
                <span class="fs-6"> Return to previous page </span>
            </button>
            <!-- <router-link :to="'/request/view'" class="mx-1">
                <button class="btn primary-btn btn-sm">
                    <span class="fs-6"> View Requests </span>
                </button>
            </router-link> commented out because not necessry now that we've enabled auto-listing approvals-->
            <router-link :to="'/'" class="mx-1">
                <button class="btn primary-btn btn-sm">
                    <span class="fs-6"> Go to Home page </span>
                </button>
            </router-link>
        </div>
        
        <!-- Display when bottle listing submission encounters an error -->
        <div class="text-danger  fw-bold fs-5" v-if="errorSubmission"> 
            <span v-if="errorMessage">An error occurred while attempting to submit, please try again!</span>
            <span v-if="invalidListing">Your request is not linked to a valid listing, please try again!</span>
            <!-- <span v-if="duplicateEntry">The bottle listing you are trying to submit already exists.</span> --> <!--commented out temporarily to disable duplicate check-->
            <br>
            <button class="btn primary-btn btn-sm" @click="reset">
                <span class="fs-5"> Retry your submission here! </span>
            </button>
        </div>

        <!-- Form Container -->
        <div class="row" v-if="fillForm">
            
            <!-- spacer -->
            <div class="col-xl-3 col-lg-2 col-md-1"></div>
            
            <!-- Main Form Area -->
            <div class="col-xl-6 col-lg-8 col-md-10">

                <!-- Form Title -->
                <div class="d-grid gap-2">
                    <div v-if="formType == 'req'"> 
                        <p class="fw-bold fs-3" v-if="formMode == 'new'">Can't <span style="cursor: pointer; color: #027562;" data-bs-toggle="modal" data-bs-target="#searchModal">find your drink on Drink-X</span>? Submit a new drink listing!</p>
                        <div v-if="formMode == 'new'" class="text-center mb-3">
                            <button type="button" class="btn btn-outline-success btn-sm" data-bs-toggle="modal" data-bs-target="#searchModal">
                                Check if it's already listed!
                            </button>
                        </div>
                        <p class="fw-bold fs-1" v-if="formMode == 'edit'">Propose Edit to Listing</p>
                        <p class="fw-bold fs-1" v-if="formMode == 'dup'">Report Duplicate Listing</p>
                
                    </div>
                    <div v-if="formType == 'power'">
                        <p class="fw-bold fs-1" v-if="formMode == 'new'">Create New Drink Listing</p> 
                        <p class="fw-bold fs-1" v-if="formMode == 'edit'">Edit Drink Listing</p>
                    </div>
                </div>

                <!-- Drink Type Guidance Section -->
                <!-- Toggle Button (Outside any card structure) -->
                <button v-if="formType == 'power' || formMode == 'new'" 
                    class="mb-3 btn w-100 text-start d-flex justify-content-between align-items-center guide-toggle" 
                    type="button" 
                    data-bs-toggle="collapse" 
                    data-bs-target="#guideCollapseContent" 
                    aria-expanded="false" 
                    aria-controls="guideCollapseContent"
                    style="
                        border: 1px solid #dee2e6;
                        border-radius: 8px;
                        padding: 16px;
                        background-color: #f8f9fa;
                    ">
                    <h6 class="mb-0 text-muted fw-bold d-flex align-items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="#0066cc"
                            class="bi bi-info-circle-fill me-3" viewBox="0 0 16 16">
                            <path
                            d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2" />
                        </svg>
                        Guide on Filling Information
                    </h6>
                    <i class="bi bi-chevron-down"></i>
                </button>

                <!-- Collapsible Content (Direct collapse without card wrapper) -->
                <div v-if="formType == 'power' || formMode == 'new'" 
                    class="collapse mb-4" 
                    id="guideCollapseContent"
                    style="
                        border: 1px solid #dee2e6;
                        border-radius: 8px;
                        padding: 16px;
                        background-color: #ffffff;
                    ">
                        <!-- Tab Navigation -->
                        <ul class="nav nav-tabs nav-fill mb-3" id="drinkGuideTab" role="tablist">
                            <li class="nav-item" role="presentation">
                                <button class="nav-link active" id="spirits-tab" data-bs-toggle="tab" data-bs-target="#spirits" type="button" role="tab" aria-controls="spirits" aria-selected="true">
                                    Spirits
                                </button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="wine-sake-tab" data-bs-toggle="tab" data-bs-target="#wine-sake" type="button" role="tab" aria-controls="wine-sake" aria-selected="false">
                                    Wine, Sake, Beer
                                </button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="cocktails-tab" data-bs-toggle="tab" data-bs-target="#cocktails" type="button" role="tab" aria-controls="cocktails" aria-selected="false">
                                    Cocktail
                                </button>
                            </li>
                        </ul>

                        <!-- Tab Content -->
                        <div class="tab-content" id="drinkGuideTabContent">
                            <!-- Spirits Tab -->
                            <div class="tab-pane fade show active" id="spirits" role="tabpanel" aria-labelledby="spirits-tab">
                                <div class="text-start">
                                    <p class="fw-bold mb-2">Spirits (Whisky, Rum, Gin, Vodka, Tequila, Cognac Brandy, etc.)</p>
                                    <ul class="mb-2" style="font-size: 0.9rem;">
                                        <li><strong>Name:</strong> Include age/vintage if it's part of the official name (e.g., "Macallan 18 Year Old", "Glenfiddich 2005"); include any identification numbers eg. cask, batch, serial, barrel, edition numbers</li>
                                        <li><strong>Producer:</strong> Select the place of distillation (e.g., Glenmorangie Distillery), or the brand (e.g., Johnnie Walker)</li>
                                        <li><strong>Country of Origin:</strong> Where the spirit was distilled/produced. For multi-country blends, insert "World" (e.g., for Suntory Ao World Whisky)</li>
                                        <li><strong>Age:</strong> Use for maturation age in years (e.g., "18" for "Macallan 18 Year Old" )</li>
                                        <li><strong>Independent Bottler:</strong> Check if bottled by someone other than the producer (e.g., "Velier" for "Foursquare Raconteur bottled by Velier")</li>
                                        <li><strong>ABV:</strong> Alcohol by volume percentage. To convert from US proof, divide by two (e.g., 80 proof = 40% ABV)</li>
                                    </ul>
                                </div>
                            </div>

                            <!-- Wine & Sake Tab -->
                            <div class="tab-pane fade" id="wine-sake" role="tabpanel" aria-labelledby="wine-sake-tab">
                                <div class="text-start">
                                    <p class="fw-bold mb-2">Wine, Sake & Beer</p>
                                    <ul class="mb-2" style="font-size: 0.9rem;">
                                        <li><strong>Name:</strong> Do NOT include vintage year (e.g., Just "Château Margaux", not "Château Margaux 2010"); for wines, don't forget to include the winery names</li>
                                        <li><strong>Producer:</strong> Select the winery or brewery name (e.g., Château Latour or Asahi-Shuzo Sake Brewery or Guinness Brewery Dublin), or the brand (Dassai or Guinness)</li>
                                        <li><strong>Country of Origin:</strong> Where the wine/sake/beer was produced</li>
                                        <li><strong>ABV:</strong> Alcohol by volume percentage. Great but not strictly necessary!</li>
                                        <li><strong>Age:</strong> Not applicable in this form (leave empty)</li>
                                    </ul>
                                </div>
                            </div>

                            <!-- Cocktails Tab -->
                            <div class="tab-pane fade" id="cocktails" role="tabpanel" aria-labelledby="cocktails-tab">
                                <div class="text-start">
                                    <p class="fw-bold mb-2">Cocktails</p>
                                    <ul class="mb-2" style="font-size: 0.9rem;">
                                        <li><strong>Name:</strong> Cocktail name (e.g., "Negroni", "Old Fashioned", "Bacardi Breezer")</li>
                                        <li><strong>Producer:</strong> If served at a specific bar or venue, insert the name of the bar or venue</li>
                                        <li><strong>Country of Origin:</strong> Select "World" for international cocktails like the Martini or Margherita </li>
                                        <li><strong>ABV:</strong> Alcohol by volume percentage. Great but not strictly necessary!</li>
                                        <li><strong>Age:</strong> Not applicable (leave empty)</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                </div>

                <!-- Search Modal -->
                <div class="modal fade" id="searchModal" tabindex="-1" aria-labelledby="searchModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog" style="margin-top: 15vh;">
                    <div class="modal-content">
                    <div class="modal-header">
                        <h6 class="modal-title" id="searchModalLabel">Let's check if your drink is already on Drink-X!</h6>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <AutocompleteSearch @select="handleSelection" />
                    </div>
                    </div>
                </div>
                </div>
                <!-- [REQ EDIT/DUP] Show Linked Bottle Listing Information -->
                <div class="card mb-3 text-start" v-if="formType == 'req' && (formMode == 'edit' || formMode == 'dup')">
                    <div class="card-header fst-italic">
                        <span v-if="formMode == 'edit'">Proposing an edit to:</span>
                        <span v-if="formMode == 'dup'">Listing to be reported:</span>
                    </div>
                    <div class="card-body">
                        <div class="container">
                            <div class="row">
                                <!-- photo -->
                                <div class="col-4 image-container">
                                    <!-- <img :src=" 'data:image/jpeg;base64,' + ( targetListing.photo || defaultPhoto )" style="width: 200px; height: 200px;"> -->
                                    <img :src="( targetListing.photo || defaultPhoto )" style="width: 200px; height: 200px;">
                                </div>
                                <!-- other listing info -->
                                <div class="col-8 ps-5">
                                    <span class="card-title fw-bold fs-5">{{ targetListing.listingName }}</span>
                                    <br>
                                    <span class="card-text">{{ targetListing.drinkType }}<span v-if="targetListing.typeCategory"> / {{ targetListing.typeCategory }}</span></span>
                                    <br>
                                    <span class="card-text fst-italic">{{ targetListing.officialDesc }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer text-body-secondary">
                        <!-- Link to Bottle Listing Page -->
                        <!-- [RE-ROUTE FLAG] '/listing/view/' -->
                        <router-link :to="'/listing/view/' + this.$route.params.listingID + '/' + slugify(targetListing.listingName)" class="text-decoration-none">
                            <span>View Listing Details</span>
                        </router-link>
                    </div>
                </div>

                <!-- [POWER EDIT] Show Edit / Duplicate Request Information -->
                <div class="card mb-3 text-start" v-if="formType == 'power' && formMode == 'edit' && prevListing">
                    <div class="card-header fst-italic">
                        <span>Linked Request Information:</span>
                    </div>
                    <div class="card-body">
                        <span class="card-title fw-bold fs-5" v-if="modifyRequest['duplicateLink'].trim()">Duplicate Report</span>
                        <span class="card-title fw-bold fs-5" v-else>Suggested Edits</span>
                        <br>
                        <span class="card-text fst-italic">{{ modifyRequest.editDesc }}</span>
                    </div>
                    <div class="card-footer text-body-secondary">
                        <span v-if="modifyRequest['duplicateLink'].trim()">Duplicate Link: {{ modifyRequest.duplicateLink }}</span>
                        <span v-else>Source Link: {{ modifyRequest.sourceLink }}</span>
                    </div>
                </div>

                <!-- Form Fields -->
                <form v-on:submit.prevent="submitFunction" id="frm" ref="listingForm">

                    <!-- Form: Propose Edit / Report Duplicate -->
                    <div v-if="formType == 'req' && (formMode == 'edit' || formMode == 'dup')">
                        
                        <!-- [REQ EDIT/DUP] Input: Proposed Edits / Duplicate Report Information -->
                        <div class="form-group mb-3">
                            <p class="text-start mb-1" v-if="formMode == 'edit'">What edits do you propose? <span class="text-danger">*</span></p>
                            <p class="text-start mb-1" v-if="formMode == 'dup'">Reason for duplicate report: <span class="text-danger">*</span></p>
                            <textarea v-if="userType == 'user'" rows=3 class="form-control" v-model="form['editDesc']" id="editDesc" placeholder="Enter your comments..."></textarea>
                            <textarea v-if="userType == 'producer'" rows=1 class="form-control" placeholder="This listing is produced by my distillery." disabled></textarea>
                            <p class="text-start mt-1" v-if="userType == 'producer'">* For other edit suggestions, please ensure that you are logged in as a user</p>
                        </div>

                        <!-- [REQ EDIT] Input: Link to source -->
                        <div class="form-group mb-3" v-if="formMode == 'edit'">
                            <p class="text-start mb-1">Link to source, if applicable.</p>
                            <input type="text" class="form-control" v-model="form['sourceLink']" id="sourceLink" placeholder="Enter source link">
                        </div>

                        <!-- [REQ DUP] Input: Link to duplicate -->
                        <div class="form-group mb-3" v-if="formMode == 'dup'">
                            <p class="text-start mb-1">Link to duplicate listing <span class="text-danger">*</span></p>
                            <input type="text" class="form-control" v-model="form['duplicateLink']" id="duplicateLink" placeholder="Enter duplicate link">
                        </div>
                    </div>

                    <!-- Form: Listing Details -->
                    <div v-if="formType == 'power' || formMode == 'new'">

                        <div v-if="additionalItems.length > 0" class="d-flex justify-content-between align-items-center mb-3">
                            <h2 class="h5 fw-bold mb-0">Item 1</h2>
                        </div>

                        <!-- Power User Fields: Tags and Order -->
                        <div class="row" v-if="formType == 'power'">
                            <!-- Input: Tags -->
                            <div class="col-md-7 mb-3">
                                <p class="text-start mb-1">Tags <span class="text-muted" style="font-size: 14px;">(Separate multiple tags with commas.)</span></p>
                                <input type="text" class="form-control" 
                                       v-model="form['tags']" 
                                       id="tags" 
                                       placeholder="#whiskyliveparis, #sakefestivalosaka">
                            </div>
                            
                            <!-- Input: Order -->
                            <div class="col-md-5 mb-3">
                                <p class="text-start mb-1">Order <span class="text-muted" style="font-size: 14px;">(Integer from -1 onwards)</span></p>
                                <input type="number" class="form-control" 
                                       v-model.number="form['order']" 
                                       id="order" 
                                       placeholder="Enter order (-1, 0, 1, 2...)" 
                                       min="-1" 
                                       step="1">
                            </div>
                        </div>

                        <!-- Input: Photo file -->
                        <div class="form-group mb-3 mobile-view-show">
                            <p class="text-start mb-1 fw-bold">Photo of drink</p>
                            <div class="row">
                                <div class="col-4">
                                    <input class="form-control" @change="handleFileSelect" type="file" id="formFile" style="display: none" accept="image/*" />
                                    <label for="formFile" class="upload-label d-block w-100"
                                           @dragover="handleDragOver"
                                           @dragleave="handleDragLeave"
                                           @drop="handleDrop">
                                        <div v-if="!selectedImage && !form['photo']" 
                                             class="mobile-review-svg-button photo-dropzone"
                                             :class="{ 'dragging': isDragging }">
                                            <div class="text-center">
                                                <h2>📷</h2>
                                                <div v-if="!isDragging">Click or drag image here</div>
                                                <div v-else class="fw-bold text-primary">Drop image here</div>
                                            </div>
                                        </div>

                                        <div v-else class="mobile-review-svg-button"
                                             @dragover="handleDragOver"
                                             @dragleave="handleDragLeave"
                                             @drop="handleDrop">
                                            <img :src="selectedImage || form['photo'] || defaultPhoto" alt="Drink photo" 
                                                 class="review-preview-photo" loading="lazy" />
                                        </div>
                                    </label>
                                    

                                </div>
                                <div class="col-8">
                                    <div class="text-muted small">
                                        <p class="mt-1"><strong>Snap a clear image of your drink label!</strong></p>
                                    
                                    </div>
                                    <div class="text-center mt-2">
                                        <button v-if="selectedImage || form['photo']" type="button" class="btn btn-sm btn-outline-secondary" 
                                                @click="clearPhoto">
                                            Clear Photo
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>


                        <!-- Input: Producer Name -->
                        <!-- [IF] Producer is creating listing, lock Producer selection - COMMENTED OUT for now 
                        <div class="form-group mb-3" v-if="isProducer != false">
                            <p class="text-start mb-1">Producer Name <span class="text-danger">*</span></p>
                            <select class="form-select" disabled>
                                <option selected>{{ isProducer }}</option>
                            </select>
                        </div>-->
                        <!-- [ELSE] Dropdown menu tied to producerID, show producerNew textbox only if "Other" selected (no producerID). -->
                        <!-- set name only, then before submitting request, put the id, save computation -->
                        <div class="form-group mb-3" > <!--removed v-else-->
                            <p class="text-start mb-1"><span class="fw-bold" >Producer (Brand, Brewery, Winery, Distillery, Bar, etc.) </span><span class="text-danger fw-bold">*</span> <span class="text-muted" style="font-size: 14px;" v-if="!searchByProducerId">(Just begin typing, then select from the drop-down suggestions.)</span><span class="text-muted" style="font-size: 14px;" v-if="searchByProducerId">(Enter numeric Producer ID - found on producer profile page or URL.)</span></p>
                            
                            <!-- Input group with toggle button -->
                            <div class="input-group">
                                <!-- Producer Name Search Input -->
                                <input v-if="!searchByProducerId"
                                       type="text" class="form-control" 
                                       v-model="form['producerNew']" 
                                       autocomplete="off" 
                                       placeholder="Enter Producer Name" 
                                       @input="handleProducerInput(null)"
                                       @blur="hideProducerDropdown(null)"
                                       :disabled="duplicateDetection.isConfirmed"
                                       :class="{ 'duplicate-confirmed-field': duplicateDetection.isConfirmed }">

                                <!-- Producer ID Search Input -->
                                <input v-if="searchByProducerId"
                                       type="text" class="form-control" 
                                       v-model="form['producerIdSearch']" 
                                       autocomplete="off" 
                                       placeholder="Enter Producer ID number" 
                                       @input="handleProducerIdInput(null)"
                                       @blur="hideProducerIdDropdown(null)"
                                       :disabled="duplicateDetection.isConfirmed"
                                       :class="{ 'duplicate-confirmed-field': duplicateDetection.isConfirmed }">

                                <!-- Toggle Button -->
                                <button type="button" 
                                        class="btn btn-outline-secondary" 
                                        @click="toggleProducerSearchMode()"
                                        :disabled="duplicateDetection.isConfirmed">
                                    {{ searchByProducerId ? 'by Producer ID' : 'by Producer Name' }}
                                </button>
                            </div>                            <!-- Validation error for Producer ID -->
                            <div v-if="searchByProducerId && producerIdValidationError" 
                                 class="text-danger mt-1" style="font-size: 14px;">
                                {{ producerIdValidationError }}
                            </div>

                            <!-- Dropdown list for Producer Name Search -->
                            <ul class="list-group"
                                v-if="!searchByProducerId && producerList && producerList.length > 0 && form['producerNew'] && showProducerDropdown">
                                <li v-for="producer in producerList" :key="producer.id"
                                    class="list-group-item list-group-item-action text-start"
                                    @click="selectProducerFromAnySearch(producer)">
                                    {{ producer.producerName }}
                                    <small class="text-muted" v-if="producer.originCountry || producer.id">
                                        ({{ producer.originCountry }}{{ producer.originCountry && producer.id ? ' | ' : '' }}{{ producer.id ? 'Producer ID: ' + producer.id : '' }})
                                    </small>
                                </li>
                            </ul>

                            <!-- Dropdown list for Producer ID Search -->
                            <ul class="list-group"
                                v-if="searchByProducerId && producerIdList && producerIdList.length > 0 && form['producerIdSearch'] && showProducerIdDropdown">
                                <li v-for="producer in producerIdList" :key="producer.id"
                                    class="list-group-item list-group-item-action text-start"
                                    @click="selectProducerFromAnySearch(producer)">
                                    {{ producer.producerName }}
                                    <small class="text-muted" v-if="producer.originCountry || producer.id">
                                        ({{ producer.originCountry }}{{ producer.originCountry && producer.id ? ' | ' : '' }}{{ producer.id ? 'Producer ID: ' + producer.id : '' }})
                                    </small>
                                </li>
                            </ul>

                            <!-- Show selected producer -->
                            <div v-if="selectedProducer && selectedProducer.id" 
                                 class="mt-2 p-2 bg-light border rounded">
                                <small class="text-success fw-bold">
                                    ✓ Producer Selected: {{ selectedProducer.producerName }}
                                    <button type="button" class="btn btn-sm btn-outline-danger ms-2"
                                            @click="clearSelectedProducer()"
                                            v-if="!duplicateDetection.isConfirmed">
                                        Clear
                                    </button>
                                </small>
                            </div>

                            <!-- [admins] Redirect to Admin page to create a producer -->
                            <p v-if="!isProducer && formType == 'power'" class="text-start text-muted pt-2" style="font-size: 14px;">Can't find a producer?
                                <router-link :to="'/admin/dashboard'" class="fw-bold">
                                    <span style="font-weight: bold; text-decoration: underline;">Click here to create!</span>
                                </router-link>
                            </p>
                            

                            
                            <!-- [non-admins] Create Producer Modal Trigger -->
                            <p v-if="formType != 'power'" class="text-start text-muted pt-2" style="font-size: 14px;">Can't find a producer?
                                <a href="#" @click.prevent="showCreateProducerModal = true" class="text-decoration-none">
                                    Click here to create!
                                </a>
                            </p>
                            
                            <!-- Create Producer Modal -->
                            <CreateProducerModal 
                                v-if="showCreateProducerModal"
                                :countries="countries"
                                @close="showCreateProducerModal = false"
                                @producerCreated="handleNewProducer"
                            />

                                
                        </div>

                        <!-- Input: Independent Bottler Check -->
                        <div >
                            <p class="text-start mb-1">Is this bottled by an independent bottler? <span class="text-danger">*</span></p>
                            <!-- Toggleable Switch -->
                            <div class="text-start mb-3">
                                <div class="form-check form-switch form-check-inline">
                                    <input class="form-check-input" type="checkbox" role="switch" id="IBCheck" name="IBCheck" v-model="indOperator"
                                           :disabled="duplicateDetection.isConfirmed"
                                           @change="triggerDuplicateCheck">
                                    <label class="form-check-label" for="IBCheck" v-if="indOperator">Yes</label>
                                    <label class="form-check-label" for="IBCheck" v-if="!indOperator">No</label>
                                </div>
                            </div>
                        </div>
                        <!-- (ONLY IF above toggled to "Yes") Input Text for Independent Bottler -->
                        <div class="form-group mb-3" v-if="indOperator">
                            <p class="text-start mb-1">If yes, who is the independent bottler? <span class="text-danger">*</span> <span class="text-muted" style="font-size: 14px;">(Just begin typing, then select from the drop-down suggestions.)</span></p>
                            
                            <input type="text" class="form-control" 
                                   v-model="form['bottler']" 
                                   :disabled="!indOperator || duplicateDetection.isConfirmed" 
                                   autocomplete="off" 
                                   placeholder="Enter Bottler Name" 
                                   @input="handleBottlerInput"
                                   @blur="hideBottlerDropdown"
                                   :class="{ 'duplicate-confirmed-field': duplicateDetection.isConfirmed }">

                            <!-- Dropdown list with drawer styling -->
                            <ul class="list-group"
                                v-if="bottlersList && bottlersList.length > 0 && form['bottler'] && showBottlerDropdown && indOperator && !duplicateDetection.isConfirmed">
                                <li v-for="bottler in bottlersList" :key="bottler.id"
                                    class="list-group-item list-group-item-action text-start"
                                    @click="selectBottler(bottler)">
                                    {{ bottler.producerName }}
                                    <small class="text-muted" v-if="bottler.originCountry || bottler.id">
                                        ({{ bottler.originCountry }}{{ bottler.originCountry && bottler.id ? ' | ' : '' }}{{ bottler.id ? 'Producer ID: ' + bottler.id : '' }})
                                    </small>
                                </li>
                            </ul>

                            <!-- Show selected bottler -->
                            <div v-if="selectedBottler && selectedBottler.id" 
                                 class="mt-2 p-2 bg-light border rounded">
                                <small class="text-success fw-bold">
                                    ✓ Bottler Selected: {{ selectedBottler.producerName }}
                                    <button type="button" class="btn btn-sm btn-outline-danger ms-2"
                                            @click="clearSelectedBottler()"
                                            v-if="!duplicateDetection.isConfirmed">
                                        Clear
                                    </button>
                                </small>
                            </div>
                        </div>

                        <!-- Input: Country of Origin -->
                        <div class="form-group mb-3">
                            <div class=" mb-3">
                                <p class="text-start mb-1 fw-bold">Country of Origin <span class="text-danger" v-if="formType == 'power'">*</span></p>
                                <!-- Simple select dropdown -->
                                <div class="input-group">
                                    <select class="form-select" v-model="form['originCountry']"
                                            :disabled="duplicateDetection.isConfirmed"
                                            :class="{ 'duplicate-confirmed-field': duplicateDetection.isConfirmed }"
                                            @change="triggerDuplicateCheck">
                                        <option value="">Select country of origin</option>
                                        <option v-for="country in countries" :key="country" :value="country">
                                            {{ country }}
                                        </option>
                                    </select>
                                </div>
                                
                                <!-- COMMENTED OUT: Sophisticated searchable drawer version -->
                                <!--
                                <div style="position: relative;">
                                    <div class="input-group mb-0">
                                        --Searchable input that opens country dropdown--
                                        <input
                                            ref="countryInput"
                                            type="text"
                                            class="form-control"
                                            v-model="countryInputValue"
                                            placeholder="Select country of origin"
                                            @input="handleCountryInput"
                                            @focus="openCountryDrawer"
                                            style="cursor: text; background-color: white;"
                                        />
                                        --Search icon--
                                        <span class="input-group-text" style="cursor: pointer;" @click="openCountryDrawer">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                                <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
                                            </svg>
                                        </span>
                                    </div>
                                    
                                    <div v-if="showCountryDrawer" class="country-dropdown">
                                        <div class="country-dropdown-body">
                                            <div 
                                                v-for="country in filteredCountries" 
                                                :key="country"
                                                class="country-item"
                                                @click="selectCountry(country)"
                                            >
                                                <span class="country-name">{{ country }}</span>
                                                <svg v-if="selectedCountry === country" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="check-icon" viewBox="0 0 16 16">
                                                    <path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.061L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z"/>
                                                </svg>
                                            </div>
                                            <div v-if="filteredCountries.length === 0" class="no-results">
                                                No countries found
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                -->
                            </div>
                        </div>

                        <!-- Bulk Mode Toggle: Multiple items from same producer -->
                        <div class="form-group text-start" :class="bulkSameProducerMode ? 'mb-2' : 'mb-4'">
                            <div class="d-flex align-items-center">
                                <p class="text-start mb-0 fw-bold me-3">Are you creating multiple items from the same Producer?<span class="text-danger"> *</span></p>
                                <div class="form-check form-check-inline">
                                    <input 
                                        class="form-check-input bulk-mode-checkbox" 
                                        type="checkbox" 
                                        id="bulkSameProducerSwitch"
                                        v-model="bulkSameProducerMode"
                                        style="cursor: pointer; width: 1.5rem; height: 1.5rem; border: 2px solid #6c757d;">
                                </div>
                               
                            </div>
                             <span v-if="bulkSameProducerMode" class="ms-1 text-success text-start" style="font-size: 14px;">
                                    <i class="ms-2 bi bi-check-circle-fill "></i>
                                    Same Producer, Multiple Items. Certain fields will be auto-populated for convenience!
                             </span>
                        </div>

                        <!-- Input: Bottle Name -->
                        <div class="form-group mb-3">
                            <p class="text-start mb-1 "><span class="fw-bold">Drink Name / Name of Bottle, Cocktail or Item </span><span class="text-danger fw-bold">*</span> <span class="text-muted" style="font-size: 14px;">(Include any identification numbers eg. cask, batch, serial, barrel, edition numbers; do NOT include vintage year for wines.)</span></p>
                            <input type="text" v-model="form['listingName']" class="form-control" id="bottleName" placeholder="Enter Drink/Bottle Name"
                                   :disabled="duplicateDetection.isConfirmed"
                                   :class="{ 'duplicate-confirmed-field': duplicateDetection.isConfirmed }"
                                   @input="triggerDuplicateCheck">
                        </div>

                        <!-- Input: drinkType (eg. Whiskey) + typeCategory (eg. Single Malt) -->
                        <div class="row">
                            <div class="col-md-4 mb-3 fw-bold">
                                <p class="text-start mb-1">Drink Type <span class="text-danger">*</span></p>
                                <div class="input-group">
                                    <select class="form-select" id="drinkTypeSelect" v-model="tempDrinkType" @change="getDrinkCategoryList(); triggerDuplicateCheck()"
                                            :disabled="duplicateDetection.isConfirmed"
                                            :class="{ 'duplicate-confirmed-field': duplicateDetection.isConfirmed }">
                                        <option v-for="taste in drinkCategoriesList" :key="taste" :value="taste">
                                        {{ taste }}
                                        </option>
                                    </select>
                                </div>
                            </div>
                        
                            <div class="col-md-4 mb-3">
                                <p class="text-start mb-1">Drink Category</p>

                                <!-- For drink types that have serveral categories to choose from -->
                                <div class="input-group" v-if="tempTypeCategoryList.length > 1">
                                    <select class="form-select" id="inputGroupSelect01" v-model="tempTypeCategory" @change="getDrinkStyleList"
                                            :disabled="duplicateDetection.isConfirmed"
                                            :class="{ 'duplicate-confirmed-field': duplicateDetection.isConfirmed }">
                                        <option v-for="cat in tempTypeCategoryList.sort()" :key="cat" :value="cat" >
                                            {{ cat }}
                                        </option>
                                    </select>
                                </div>
                                
                                <!-- If there are no categories to select, display disabled dummy selection field -->
                                <div class="input-group" v-else>
                                    <select class="form-select" disabled>
                                        <option selected>-</option>
                                    </select>
                                </div>

                            </div>
                            <div class="col-md-4 mb-3">
                                <p class="text-start mb-1">Drink Style</p>

                                <!-- For drink categories that have serveral styles to choose from -->
                                <div class="input-group" v-if="tempDrinkStylesList.length > 1">
                                    <select class="form-select" id="inputGroupSelect02" v-model="tempDrinkStyle"
                                            :disabled="duplicateDetection.isConfirmed"
                                            :class="{ 'duplicate-confirmed-field': duplicateDetection.isConfirmed }">
                                        <option v-for="style in tempDrinkStylesList.sort()" :key="style" :value="style" >
                                            {{ style }}
                                        </option>
                                    </select>
                                </div>
                                
                                <!-- If there are no styles to select, display disabled dummy selection field -->
                                <div class="input-group" v-else>
                                    <select class="form-select" disabled>
                                        <option selected>-</option>
                                    </select>
                                </div>

                            </div>
                        </div>

                        <!-- Duplicate Detection Section (Item 1) -->
                        <div v-if="duplicateDetection.matches.length > 0 || duplicateDetection.isLoading || duplicateDetection.isConfirmed" 
                             class="duplicate-detection-card mb-3"
                             :class="{ 'confirmed': duplicateDetection.isConfirmed }">
                            
                            <!-- Card Header (clickable to collapse/expand) -->
                            <div class="duplicate-detection-header" @click="toggleDuplicateCollapse">
                                <div class="d-flex align-items-center flex-grow-1">
                                    <span class="duplicate-icon me-2">🔍</span>
                                    <span class="fw-bold" v-if="!duplicateDetection.isConfirmed">
                                        Wait, Do You Mean:
                                    </span>
                                    <span class="fw-bold" v-else>
                                        ✓ Matched to existing listing
                                    </span>
                                    <span v-if="!duplicateDetection.isConfirmed" class="ms-auto me-2">
                                        ({{ duplicateDetection.matches.length }} potential match{{ duplicateDetection.matches.length !== 1 ? 'es' : '' }})
                                    </span>
                                </div>
                                <div class="d-flex align-items-center">
                                    <svg v-if="!duplicateDetection.isCollapsed" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-up" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd" d="M7.646 4.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1-.708.708L8 5.707l-5.646 5.647a.5.5 0 0 1-.708-.708l6-6z"/>
                                    </svg>
                                    <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-down" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd" d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/>
                                    </svg>
                                </div>
                            </div>

                            <!-- Card Body (collapsible) -->
                            <div v-show="!duplicateDetection.isCollapsed" class="duplicate-detection-body">
                                
                                <!-- Confirmed duplicate display -->
                                <div v-if="duplicateDetection.isConfirmed && duplicateDetection.confirmedDuplicate" class="confirmed-duplicate-info">
                                    <div class="d-flex align-items-center mb-2">
                                        <img v-if="duplicateDetection.confirmedDuplicate.photo" 
                                             :src="duplicateDetection.confirmedDuplicate.photo" 
                                             class="duplicate-thumbnail me-3" 
                                             :alt="duplicateDetection.confirmedDuplicate.listingName">
                                        <div class="flex-grow-1">
                                            <div class="fw-bold">{{ duplicateDetection.confirmedDuplicate.listingName }}</div>
                                            <div class="text-muted small">
                                                {{ duplicateDetection.confirmedDuplicate.producerName }}
                                                <span v-if="duplicateDetection.confirmedDuplicate.originCountry"> · {{ duplicateDetection.confirmedDuplicate.originCountry }}</span>
                                            </div>
                                        </div>
                                        <div class="d-flex flex-column align-items-end gap-1">
                                            <button type="button" class="btn btn-sm btn-outline-secondary" 
                                                    @click.stop="openListingInNewTab(duplicateDetection.confirmedDuplicate.id, duplicateDetection.confirmedDuplicate.listingName)">
                                                View Listing ↗
                                            </button>
                                            <button type="button" class="btn btn-sm btn-outline-warning" @click.stop="undoDuplicateConfirmation">
                                                Undo Selection
                                            </button>
                                        </div>
                                    </div>
                                    <div class="alert alert-success mb-0 py-2 small">
                                        <strong>Note:</strong> This item is linked to an existing listing. Fields have been pre-filled and locked.
                                    </div>
                                </div>

                                <!-- Match suggestions list -->
                                <div v-else class="duplicate-matches-list">
                                    <div v-for="match in duplicateDetection.matches" :key="match.id" class="duplicate-match-item">
                                        <div class="d-flex align-items-center">
                                            <img v-if="match.photo" :src="match.photo" class="duplicate-thumbnail me-3" :alt="match.listingName">
                                            <div v-else class="duplicate-thumbnail-placeholder me-3">📷</div>
                                            <div class="flex-grow-1">
                                                <div class="fw-bold">{{ match.listingName }}</div>
                                                <div class="text-muted small">
                                                    {{ match.producerName }}
                                                    <span v-if="match.bottlerName"> · Bottled by {{ match.bottlerName }}</span>
                                                </div>
                                                <div class="text-muted small">
                                                    <span v-if="match.drinkType">{{ match.drinkType }}</span>
                                                    <span v-if="match.originCountry"> · {{ match.originCountry }}</span>
                                                    <span v-if="match.abv"> · {{ match.abv }}%</span>
                                                    <span v-if="match.age"> · {{ match.age }} yrs</span>
                                                </div>
                                            </div>
                                            <div class="d-flex flex-column align-items-end gap-1">
                                                <!-- <span class="badge bg-secondary">{{ match.similarity }}% match</span> -->
                                                <button type="button" class="btn btn-sm btn-outline-primary" 
                                                        @click.stop="openListingInNewTab(match.id, match.listingName)">
                                                    View ↗
                                                </button>
                                                <button type="button" class="btn btn-sm btn-success" @click.stop="confirmDuplicate(match)">
                                                    Yes, this is it
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Input: Variety Tags -->
                        <div class="form-group mb-3">
                            <p class="text-start mb-1 fw-bold">Variety Tags</p>
                            <p class="text-start mb-1 text-muted" style="font-size: 14px;">Add any applicable tags (eg. Pinot Noir, Bourbon Barrel, Nectaron, Yamadanishiki, Espadin, Angelica)</p>
                            
                            <!-- Input field with Add button -->
                            <div class="input-group mb-2">
                                <input 
                                    type="text" 
                                    class="form-control" 
                                    v-model="varietyTagInput"
                                    @keyup.enter="addVarietyTag"
                                    placeholder="Type a variety tag and click +"
                                    maxlength="20"
                                    :disabled="duplicateDetection.isConfirmed"
                                >
                                <button 
                                    class="btn btn-outline-success" 
                                    type="button" 
                                    @click="addVarietyTag"
                                    :disabled="!varietyTagInput.trim() || duplicateDetection.isConfirmed"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">
                                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                                    </svg>
                                </button>
                            </div>

                            <!-- Display added tags as badges -->
                            <div v-if="varietyTagsList.length > 0" class="d-flex flex-wrap gap-2">
                                <span 
                                    v-for="(tag, index) in varietyTagsList" 
                                    :key="index"
                                    class="badge bg-primary d-flex align-items-center"
                                    style="font-size: 14px; padding: 8px 12px;"
                                >
                                    {{ tag }}
                                    <button 
                                        type="button" 
                                        class="btn-close btn-close-white ms-2" 
                                        style="font-size: 10px;"
                                        @click="removeVarietyTag(index)"
                                        aria-label="Remove tag"
                                        :disabled="duplicateDetection.isConfirmed"
                                    ></button>
                                </span>
                            </div>
                        </div>

                        <!-- Input: Photo file -->
                        <div class="form-group mb-3 mobile-view-hide">
                            <p class="text-start mb-1 fw-bold">Photo of drink</p>
                            <div class="row">
                                <div class="col-4">
                                    <input class="form-control" @change="handleFileSelect" type="file" id="formFile" style="display: none" accept="image/*" />
                                    <label for="formFile" class="upload-label d-block w-100"
                                           @dragover="handleDragOver"
                                           @dragleave="handleDragLeave"
                                           @drop="handleDrop">
                                        <div v-if="!selectedImage && !form['photo']" 
                                             class="mobile-review-svg-button photo-dropzone"
                                             :class="{ 'dragging': isDragging }">
                                            <div class="text-center">
                                                <h2>📷</h2>
                                                <div v-if="!isDragging">Click or drag image here</div>
                                                <div v-else class="fw-bold text-primary">Drop image here</div>
                                            </div>
                                        </div>

                                        <div v-else class="mobile-review-svg-button"
                                             @dragover="handleDragOver"
                                             @dragleave="handleDragLeave"
                                             @drop="handleDrop">
                                            <img :src="selectedImage || form['photo'] || defaultPhoto" alt="Drink photo" 
                                                 class="review-preview-photo" loading="lazy" />
                                        </div>
                                    </label>
                                    

                                </div>
                                <div class="col-8">
                                    <div class="text-muted small">
                                        <p class="mt-1"><strong>Upload a clear image of your drink. We recommend the official image!</strong></p>
                                    
                                    </div>
                                    <div class="text-center mt-2">
                                        <button v-if="selectedImage || form['photo']" type="button" class="btn btn-sm btn-outline-secondary" 
                                                @click="clearPhoto">
                                            Clear Photo
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Input: Alcohol Strength (% ABV) + Alcohol Age / Vintage (years old / Year Bottled) -->
                        <div class="row mb-3">
                            <div class="form-group col-6">
                                <p class="text-start mb-1">Strength</p> <!--<span class="text-danger" v-if="formType == 'power'">*</span>-->
                                <div class="form-group row">
                                    <div class="col-6 pe-1">
                                        <input type="number" v-model="form['abv']" class="form-control" id="abv" min="0" max="100" step="0.1"
                                               :disabled="duplicateDetection.isConfirmed">
                                    </div>
                                    <label for="abv" class="col-6 col-form-label ps-1 text-start">% ABV</label>
                                </div>
                            </div>
                            <div class="form-group col-6" >
                                <p class="text-start mb-1">Age</p>
                                <div class="form-group row">
                                    <div class="col-6 pe-1">
                                        <input type="number" v-model="form['age']" class="form-control" id="age" min="0"
                                               :disabled="duplicateDetection.isConfirmed">
                                    </div>
                                    <label for="age" class="col-6 col-form-label ps-1 text-start">years old</label>
                                </div>
                            </div>
                        </div>

                        <!-- [POWER] Input: Drink Description -->
                        <div class="form-group mb-3" > <!-- v-if="formType == 'power'"   shifted out to allow ordinary users to submit official descp too-->
                            <p class="text-start mb-1">Official Description</p>
                            <textarea rows=3 class="form-control" v-model="form['officialDesc']" id="officialDesc" placeholder="Enter description of drink"
                                      :disabled="duplicateDetection.isConfirmed"></textarea>
                        </div>

                        <!-- Input: Link to website or source (optional for actual listing, mandatory for request) -->
                        <div v-if="formType == 'power'"  class="form-group mb-3">
                            <p class="text-start mb-1">Link to website or source </p> <!--<span class="text-danger" v-if="formType == 'req'">*</span>-->
                            <input type="text" class="form-control" v-model="form['sourceLink']" id="sourceLink" placeholder="Enter source link">
                        </div>

                        <!-- Input: Link to 88 Bamboo review -->
                        <div v-if="formType == 'power'"  class="form-group mb-3">
                            <p class="text-start mb-1">Link to 88 Bamboo review</p>
                            <input type="text" class="form-control" v-model="form['reviewLink']" id="reviewLink" placeholder="Enter review link">
                        </div>

                        <div class="mt-4 pt-3 border-top">
                            <!-- Button row after Item 1 -->
                            <div class="d-flex flex-column flex-md-row align-items-stretch align-items-md-center gap-2 mb-3">
                                <!-- Active button when no additional items, disabled when there are -->
                                <button
                                    v-if="additionalItems.length === 0"
                                    type="button"
                                    class="btn btn-primary w-100 w-md-auto"
                                    @click="addAdditionalItem"
                                >
                                    + Select Additional Item (2/{{ maxAdditionalItems }})
                                </button>
                                <!-- Disabled button when there are additional items -->
                                <button
                                    v-if="additionalItems.length > 0"
                                    type="button"
                                    class="btn btn-primary w-100 w-md-auto"
                                    disabled
                                    style="opacity: 0.5; cursor: not-allowed;"
                                >
                                    + Select Additional Item (2/{{ maxAdditionalItems }})
                                </button>
                                <!-- Remove Item 2 button, only when Item 2 is the last item -->
                                <button
                                    v-if="additionalItems.length === 1"
                                    type="button"
                                    class="btn btn-outline-danger w-100 w-md-auto"
                                    @click="removeLastAdditionalItem"
                                >
                                    Remove Item 2
                                </button>
                            </div>

                            <div
                                v-for="(item, idx) in additionalItems"
                                :key="'additional-item-' + idx"
                                class="mb-4 pb-4 border-top "
                            >
                                <h2 class="h5 fw-bold mb-3 mt-2 text-start">Item {{ idx + 2 }}</h2>

                                <div class="row" v-if="formType == 'power'">
                                    <div class="col-md-7 mb-3">
                                        <p class="text-start mb-1">Tags <span class="text-muted" style="font-size: 14px;">(Separate multiple tags with commas.)</span></p>
                                        <input type="text" class="form-control"
                                               v-model="item.tags"
                                               :id="'tags-additional-' + idx"
                                               placeholder="#whiskyliveparis, #sakefestivalosaka">
                                    </div>
                                    <div class="col-md-5 mb-3">
                                        <p class="text-start mb-1">Order <span class="text-muted" style="font-size: 14px;">(Integer from -1 onwards)</span></p>
                                        <input type="number" class="form-control"
                                               v-model.number="item.order"
                                               :id="'order-additional-' + idx"
                                               placeholder="Enter order (-1, 0, 1, 2...)"
                                               min="-1"
                                               step="1">
                                    </div>
                                </div>

                                <div class="form-group mb-3">
                                    <p class="text-start mb-1"><span class="fw-bold">Producer (Brand, Brewery, Winery, Distillery, Bar, etc.) </span><span class="text-danger fw-bold">*</span> <span class="text-muted" style="font-size: 14px;" v-if="!item.searchByProducerId">(Just begin typing, then select from the drop-down suggestions.)</span><span class="text-muted" style="font-size: 14px;" v-if="item.searchByProducerId">(Enter numeric Producer ID - found on producer profile page or URL.)</span></p>
                                    
                                    <!-- Input group with toggle button -->
                                    <div class="input-group">
                                        <!-- Producer Name Search Input -->
                                        <input v-if="!item.searchByProducerId"
                                               type="text" class="form-control"
                                               v-model="item.producerNew"
                                               :id="'producer-additional-' + idx"
                                               autocomplete="off"
                                               placeholder="Enter Producer Name"
                                               @input="handleProducerInput(idx)"
                                               @blur="hideProducerDropdown(idx)">

                                        <!-- Producer ID Search Input -->
                                        <input v-if="item.searchByProducerId"
                                               type="text" class="form-control"
                                               v-model="item.producerIdSearch"
                                               :id="'producerId-additional-' + idx"
                                               autocomplete="off"
                                               placeholder="Enter Producer ID number"
                                               @input="handleProducerIdInput(idx)"
                                               @blur="hideProducerIdDropdown(idx)">

                                        <!-- Toggle Button -->
                                        <button type="button"
                                                class="btn btn-outline-secondary"
                                                @click="toggleProducerSearchMode(idx)">
                                            {{ item.searchByProducerId ? 'by Producer ID' : 'by Producer Name' }}
                                        </button>
                                    </div>

                                    <!-- Validation error for Producer ID -->
                                    <div v-if="item.searchByProducerId && item.producerIdValidationError"
                                         class="text-danger mt-1" style="font-size: 14px;">
                                        {{ item.producerIdValidationError }}
                                    </div>

                                    <!-- Dropdown list for Producer Name Search -->
                                    <ul class="list-group"
                                        v-if="!item.searchByProducerId && producerList && producerList.length > 0 && item.producerNew && item.showProducerDropdown">
                                        <li v-for="producer in producerList" :key="producer.id"
                                            class="list-group-item list-group-item-action text-start"
                                            @click="selectProducerFromAnySearch(producer, idx)">
                                            {{ producer.producerName }}
                                            <small class="text-muted" v-if="producer.originCountry || producer.id">
                                                ({{ producer.originCountry }}{{ producer.originCountry && producer.id ? ' | ' : '' }}{{ producer.id ? 'Producer ID: ' + producer.id : '' }})
                                            </small>
                                        </li>
                                    </ul>

                                    <!-- Dropdown list for Producer ID Search -->
                                    <ul class="list-group"
                                        v-if="item.searchByProducerId && producerIdList && producerIdList.length > 0 && item.producerIdSearch && item.showProducerIdDropdown">
                                        <li v-for="producer in producerIdList" :key="producer.id"
                                            class="list-group-item list-group-item-action text-start"
                                            @click="selectProducerFromAnySearch(producer, idx)">
                                            {{ producer.producerName }}
                                            <small class="text-muted" v-if="producer.originCountry || producer.id">
                                                ({{ producer.originCountry }}{{ producer.originCountry && producer.id ? ' | ' : '' }}{{ producer.id ? 'Producer ID: ' + producer.id : '' }})
                                            </small>
                                        </li>
                                    </ul>

                                    <!-- Show selected producer -->
                                    <div v-if="item.selectedProducer && item.selectedProducer.id"
                                         class="mt-2 p-2 bg-light border rounded">
                                        <small class="text-success fw-bold">
                                            ✓ Producer Selected: {{ item.selectedProducer.producerName }}
                                            <button type="button" class="btn btn-sm btn-outline-danger ms-2"
                                                    @click="clearSelectedProducer(idx)">
                                                Clear
                                            </button>
                                        </small>
                                    </div>
                                </div>

                                <div class="mb-3 text-start">
                                    <p class="text-start mb-1">Is this bottled by an independent bottler? <span class="text-danger">*</span></p>
                                    <div class="form-check form-switch form-check-inline text-start">
                                        <input class="form-check-input" type="checkbox" role="switch"
                                               :id="'IBCheck-additional-' + idx"
                                               v-model="item.indOperator"
                                               @change="triggerDuplicateCheckForItem(idx)">
                                        <label class="form-check-label" :for="'IBCheck-additional-' + idx" v-if="item.indOperator">Yes</label>
                                        <label class="form-check-label" :for="'IBCheck-additional-' + idx" v-else>No</label>
                                    </div>
                                </div>

                                <div class="form-group mb-3" v-if="item.indOperator">
                                    <p class="text-start mb-1">If yes, who is the independent bottler? <span class="text-danger">*</span> <span class="text-muted" style="font-size: 14px;">(Just begin typing, then select from the drop-down suggestions.)</span></p>
                                    <input type="text" class="form-control"
                                           v-model="item.bottler"
                                           :id="'bottler-additional-' + idx"
                                           :disabled="!item.indOperator"
                                           autocomplete="off"
                                           placeholder="Enter Bottler Name"
                                           @input="handleBottlerInputForItem(idx)"
                                           @blur="hideBottlerDropdownForItem(idx)">

                                    <!-- Dropdown list for bottler suggestions -->
                                    <ul class="list-group"
                                        v-if="bottlersList && bottlersList.length > 0 && item.bottler && item.showBottlerDropdown && item.indOperator">
                                        <li v-for="bottler in bottlersList" :key="bottler.id"
                                            class="list-group-item list-group-item-action text-start"
                                            @click="selectBottlerForItem(bottler, idx)">
                                            {{ bottler.producerName }}
                                            <small class="text-muted" v-if="bottler.originCountry || bottler.id">
                                                ({{ bottler.originCountry }}{{ bottler.originCountry && bottler.id ? ' | ' : '' }}{{ bottler.id ? 'Producer ID: ' + bottler.id : '' }})
                                            </small>
                                        </li>
                                    </ul>

                                    <!-- Show selected bottler -->
                                    <div v-if="item.selectedBottler && item.selectedBottler.id"
                                         class="mt-2 p-2 bg-light border rounded">
                                        <small class="text-success fw-bold">
                                            ✓ Bottler Selected: {{ item.selectedBottler.producerName }}
                                            <button type="button" class="btn btn-sm btn-outline-danger ms-2"
                                                    @click="clearSelectedBottlerForItem(idx)">
                                                Clear
                                            </button>
                                        </small>
                                    </div>
                                </div>

                                <div class="form-group mb-3">
                                    <p class="text-start mb-1 fw-bold">Country of Origin <span class="text-danger" v-if="formType == 'power'">*</span></p>
                                    <div class="input-group">
                                        <select class="form-select" v-model="item.originCountry" :id="'originCountry-additional-' + idx"
                                                :disabled="item.duplicateDetection && item.duplicateDetection.isConfirmed"
                                                :class="{ 'duplicate-confirmed-field': item.duplicateDetection && item.duplicateDetection.isConfirmed }"
                                                @change="triggerDuplicateCheckForItem(idx)">
                                            <option value="">Select country of origin</option>
                                            <option v-for="country in countries" :key="country" :value="country">
                                                {{ country }}
                                            </option>
                                        </select>
                                    </div>
                                </div>

                                <div class="form-group mb-3">
                                    <p class="text-start mb-1 "><span class="fw-bold">Drink Name / Name of Bottle, Cocktail or Item </span><span class="text-danger fw-bold">*</span></p>
                                    <input type="text" v-model="item.listingName" class="form-control" :id="'bottleName-additional-' + idx" placeholder="Enter Drink/Bottle Name"
                                           :disabled="item.duplicateDetection && item.duplicateDetection.isConfirmed"
                                           :class="{ 'duplicate-confirmed-field': item.duplicateDetection && item.duplicateDetection.isConfirmed }"
                                           @input="triggerDuplicateCheckForItem(idx)">
                                </div>

                                <div class="row">
                                    <div class="col-md-4 mb-3 fw-bold">
                                        <p class="text-start mb-1">Drink Type <span class="text-danger">*</span></p>
                                        <div class="input-group">
                                            <select class="form-select"
                                                    :id="'drinkType-additional-' + idx"
                                                    v-model="item.tempDrinkType"
                                                    @change="getDrinkCategoryListForItem(idx); triggerDuplicateCheckForItem(idx)"
                                                    :disabled="item.duplicateDetection && item.duplicateDetection.isConfirmed"
                                                    :class="{ 'duplicate-confirmed-field': item.duplicateDetection && item.duplicateDetection.isConfirmed }">
                                                <option v-for="taste in drinkCategoriesList" :key="taste" :value="taste">
                                                    {{ taste }}
                                                </option>
                                            </select>
                                        </div>
                                    </div>

                                    <div class="col-md-4 mb-3">
                                        <p class="text-start mb-1">Drink Category</p>
                                        <div class="input-group" v-if="item.tempTypeCategoryList && item.tempTypeCategoryList.length > 1">
                                            <select class="form-select"
                                                    :id="'drinkCategory-additional-' + idx"
                                                    v-model="item.tempTypeCategory"
                                                    @change="getDrinkStyleListForItem(idx)"
                                                    :disabled="item.duplicateDetection && item.duplicateDetection.isConfirmed"
                                                    :class="{ 'duplicate-confirmed-field': item.duplicateDetection && item.duplicateDetection.isConfirmed }">
                                                <option v-for="cat in item.tempTypeCategoryList.sort()" :key="cat" :value="cat">
                                                    {{ cat }}
                                                </option>
                                            </select>
                                        </div>
                                        <div class="input-group" v-else>
                                            <select class="form-select" disabled>
                                                <option selected>-</option>
                                            </select>
                                        </div>
                                    </div>

                                    <div class="col-md-4 mb-3">
                                        <p class="text-start mb-1">Drink Style</p>
                                        <div class="input-group" v-if="item.tempDrinkStylesList && item.tempDrinkStylesList.length > 1">
                                            <select class="form-select"
                                                    :id="'drinkStyle-additional-' + idx"
                                                    v-model="item.tempDrinkStyle"
                                                    :disabled="item.duplicateDetection && item.duplicateDetection.isConfirmed"
                                                    :class="{ 'duplicate-confirmed-field': item.duplicateDetection && item.duplicateDetection.isConfirmed }">
                                                <option v-for="style in item.tempDrinkStylesList.sort()" :key="style" :value="style">
                                                    {{ style }}
                                                </option>
                                            </select>
                                        </div>
                                        <div class="input-group" v-else>
                                            <select class="form-select" disabled>
                                                <option selected>-</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>

                                <!-- Duplicate Detection Section (Additional Item) -->
                                <div v-if="item.duplicateDetection && (item.duplicateDetection.matches.length > 0 || item.duplicateDetection.isLoading || item.duplicateDetection.isConfirmed)" 
                                     class="duplicate-detection-card mb-3"
                                     :class="{ 'confirmed': item.duplicateDetection.isConfirmed }">
                                    
                                    <!-- Card Header (clickable to collapse/expand) -->
                                    <div class="duplicate-detection-header" @click="toggleDuplicateCollapseForItem(idx)">
                                        <div class="d-flex align-items-center flex-grow-1">
                                            <span class="duplicate-icon me-2">🔍</span>
                                            <span class="fw-bold" v-if="!item.duplicateDetection.isConfirmed">
                                                Wait, Do You Mean these:
                                            </span>
                                            <span class="fw-bold " v-else>
                                                ✓ Matched to existing listing
                                            </span>
                                            <span v-if="!item.duplicateDetection.isConfirmed" class="ms-auto me-2">
                                                ({{ item.duplicateDetection.matches.length }} potential match{{ item.duplicateDetection.matches.length !== 1 ? 'es' : '' }})
                                            </span>
                                        </div>
                                        <div class="d-flex align-items-center">
                                            <svg v-if="!item.duplicateDetection.isCollapsed" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-up" viewBox="0 0 16 16">
                                                <path fill-rule="evenodd" d="M7.646 4.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1-.708.708L8 5.707l-5.646 5.647a.5.5 0 0 1-.708-.708l6-6z"/>
                                            </svg>
                                            <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-down" viewBox="0 0 16 16">
                                                <path fill-rule="evenodd" d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/>
                                            </svg>
                                        </div>
                                    </div>

                                    <!-- Card Body (collapsible) -->
                                    <div v-show="!item.duplicateDetection.isCollapsed" class="duplicate-detection-body">
                                        
                                        <!-- Confirmed duplicate display -->
                                        <div v-if="item.duplicateDetection.isConfirmed && item.duplicateDetection.confirmedDuplicate" class="confirmed-duplicate-info">
                                            <div class="d-flex align-items-center mb-2">
                                                <img v-if="item.duplicateDetection.confirmedDuplicate.photo" 
                                                     :src="item.duplicateDetection.confirmedDuplicate.photo" 
                                                     class="duplicate-thumbnail me-3" 
                                                     :alt="item.duplicateDetection.confirmedDuplicate.listingName">
                                                <div class="flex-grow-1">
                                                    <div class="fw-bold">{{ item.duplicateDetection.confirmedDuplicate.listingName }}</div>
                                                    <div class="text-muted small">
                                                        {{ item.duplicateDetection.confirmedDuplicate.producerName }}
                                                        <span v-if="item.duplicateDetection.confirmedDuplicate.originCountry"> · {{ item.duplicateDetection.confirmedDuplicate.originCountry }}</span>
                                                    </div>
                                                </div>
                                                <div class="d-flex flex-column align-items-end gap-1">
                                                    <button type="button" class="btn btn-sm btn-outline-secondary" 
                                                            @click.stop="openListingInNewTab(item.duplicateDetection.confirmedDuplicate.id, item.duplicateDetection.confirmedDuplicate.listingName)">
                                                        View Listing ↗
                                                    </button>
                                                    <button type="button" class="btn btn-sm btn-outline-warning" @click.stop="undoDuplicateConfirmationForItem(idx)">
                                                        Undo Selection
                                                    </button>
                                                </div>
                                            </div>
                                            <div class="alert alert-success mb-0 py-2 small">
                                                <strong>Note:</strong> This item is linked to an existing listing. Fields have been pre-filled and locked.
                                            </div>
                                        </div>

                                        <!-- Match suggestions list -->
                                        <div v-else class="duplicate-matches-list">
                                            <div v-for="match in item.duplicateDetection.matches" :key="match.id" class="duplicate-match-item">
                                                <div class="d-flex align-items-center">
                                                    <img v-if="match.photo" :src="match.photo" class="duplicate-thumbnail me-3" :alt="match.listingName">
                                                    <div v-else class="duplicate-thumbnail-placeholder me-3">📷</div>
                                                    <div class="flex-grow-1">
                                                        <div class="fw-bold">{{ match.listingName }}</div>
                                                        <div class="text-muted small">
                                                            {{ match.producerName }}
                                                            <span v-if="match.bottlerName"> · Bottled by {{ match.bottlerName }}</span>
                                                        </div>
                                                        <div class="text-muted small">
                                                            <span v-if="match.drinkType">{{ match.drinkType }}</span>
                                                            <span v-if="match.originCountry"> · {{ match.originCountry }}</span>
                                                            <span v-if="match.abv"> · {{ match.abv }}%</span>
                                                            <span v-if="match.age"> · {{ match.age }} yrs</span>
                                                        </div>
                                                    </div>
                                                    <div class="d-flex flex-column align-items-end gap-1">
                                                        <span class="badge bg-secondary">{{ match.similarity }}% match</span>
                                                        <button type="button" class="btn btn-sm btn-outline-primary" 
                                                                @click.stop="openListingInNewTab(match.id, match.listingName)">
                                                            View ↗
                                                        </button>
                                                        <button type="button" class="btn btn-sm btn-success" @click.stop="confirmDuplicateForItem(idx, match)">
                                                            Yes, this is it
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="form-group mb-3">
                                    <p class="text-start mb-1 fw-bold">Variety Tags</p>
                                    <p class="text-start mb-1 text-muted" style="font-size: 14px;">Add any applicable tags (eg. Pinot Noir, Bourbon Barrel, Nectaron, Yamadanishiki, Espadin, Angelica)</p>
                                    <div class="input-group mb-2">
                                        <input
                                            type="text"
                                            class="form-control"
                                            v-model="item.varietyTagInput"
                                            @keyup.enter="addVarietyTagForItem(idx)"
                                            :id="'varietyTag-additional-' + idx"
                                            placeholder="Type a variety tag and click +"
                                            maxlength="20"
                                            :disabled="item.duplicateDetection && item.duplicateDetection.isConfirmed"
                                        >
                                        <button
                                            class="btn btn-outline-success"
                                            type="button"
                                            @click="addVarietyTagForItem(idx)"
                                            :disabled="!item.varietyTagInput || !item.varietyTagInput.trim() || (item.duplicateDetection && item.duplicateDetection.isConfirmed)"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">
                                                <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                                <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                                            </svg>
                                        </button>
                                    </div>
                                    <div v-if="item.varietyTagsList.length > 0" class="d-flex flex-wrap gap-2">
                                        <span
                                            v-for="(tag, tagIdx) in item.varietyTagsList"
                                            :key="tagIdx"
                                            class="badge bg-primary d-flex align-items-center"
                                            style="font-size: 14px; padding: 8px 12px;"
                                        >
                                            {{ tag }}
                                            <button
                                                type="button"
                                                class="btn-close btn-close-white ms-2"
                                                style="font-size: 10px;"
                                                @click="removeVarietyTagForItem(idx, tagIdx)"
                                                aria-label="Remove tag"
                                                :disabled="item.duplicateDetection && item.duplicateDetection.isConfirmed"
                                            ></button>
                                        </span>
                                    </div>
                                </div>

                                <div class="form-group mb-3">
                                    <p class="text-start mb-1 fw-bold">Photo of drink</p>
                                    <div class="row">
                                        <div class="col-4">
                                            <input class="form-control" @change="event => handleFileSelectForItem(event, idx)" type="file" :id="'formFile-additional-' + idx" style="display: none" accept="image/*" />
                                            <label :for="'formFile-additional-' + idx" class="upload-label d-block w-100"
                                                   @dragover="event => handleDragOverForItem(event, idx)"
                                                   @dragleave="event => handleDragLeaveForItem(event, idx)"
                                                   @drop="event => handleDropForItem(event, idx)">
                                                <div v-if="!item.selectedImage && !item.photo" 
                                                     class="mobile-review-svg-button photo-dropzone"
                                                     :class="{ 'dragging': item.isDragging }">
                                                    <div class="text-center">
                                                        <h2>📷</h2>
                                                        <div v-if="!item.isDragging">Click or drag image here</div>
                                                        <div v-else class="fw-bold text-primary">Drop image here</div>
                                                    </div>
                                                </div>

                                                <div v-else class="mobile-review-svg-button"
                                                     @dragover="event => handleDragOverForItem(event, idx)"
                                                     @dragleave="event => handleDragLeaveForItem(event, idx)"
                                                     @drop="event => handleDropForItem(event, idx)">
                                                    <img :src="item.selectedImage || item.photo || defaultPhoto" alt="Drink photo"
                                                         class="review-preview-photo" loading="lazy" />
                                                </div>
                                            </label>
                                        </div>
                                        <div class="col-8">
                                            <div class="text-muted small">
                                                <p class="mt-1"><strong>Upload a clear image of your drink. We recommend the official image!</strong></p>
                                            </div>
                                            <div class="text-center mt-2">
                                                <button v-if="item.selectedImage || item.photo" type="button" class="btn btn-sm btn-outline-secondary"
                                                        @click="() => { item.selectedImage = ''; item.photo = ''; }">
                                                    Clear Photo
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="row mb-3">
                                    <div class="form-group col-6">
                                        <p class="text-start mb-1">Strength</p>
                                        <div class="form-group row">
                                            <div class="col-6 pe-1">
                                                <input type="number" v-model="item.abv" class="form-control" :id="'abv-additional-' + idx" min="0" max="100" step="0.1"
                                                       :disabled="item.duplicateDetection && item.duplicateDetection.isConfirmed">
                                            </div>
                                            <label :for="'abv-additional-' + idx" class="col-6 col-form-label ps-1 text-start">% ABV</label>
                                        </div>
                                    </div>
                                    <div class="form-group col-6" >
                                        <p class="text-start mb-1">Age</p>
                                        <div class="form-group row">
                                            <div class="col-6 pe-1">
                                                <input type="number" v-model="item.age" class="form-control" :id="'age-additional-' + idx" min="0"
                                                       :disabled="item.duplicateDetection && item.duplicateDetection.isConfirmed">
                                            </div>
                                            <label :for="'age-additional-' + idx" class="col-6 col-form-label ps-1 text-start">years old</label>
                                        </div>
                                    </div>
                                </div>

                                <div class="form-group mb-3">
                                    <p class="text-start mb-1">Official Description</p>
                                    <textarea rows=3 class="form-control" v-model="item.officialDesc" :id="'officialDesc-additional-' + idx" placeholder="Enter description of drink"
                                              :disabled="item.duplicateDetection && item.duplicateDetection.isConfirmed"></textarea>
                                </div>

                                <div v-if="formType == 'power'" class="form-group mb-3">
                                    <p class="text-start mb-1">Link to website or source </p>
                                    <input type="text" class="form-control" v-model="item.sourceLink" :id="'sourceLink-additional-' + idx" placeholder="Enter source link">
                                </div>

                                <div v-if="formType == 'power'" class="form-group mb-3">
                                    <p class="text-start mb-1">Link to 88 Bamboo review</p>
                                    <input type="text" class="form-control" v-model="item.reviewLink" :id="'reviewLink-additional-' + idx" placeholder="Enter review link">
                                </div>

                                <!-- Button row after this additional item -->
                                <div class="d-flex flex-column flex-md-row align-items-stretch align-items-md-center gap-2 mt-3">
                                    <!-- Disabled button if NOT the last item -->
                                    <button
                                        v-if="idx < additionalItems.length - 1"
                                        type="button"
                                        class="btn btn-primary w-100 w-md-auto"
                                        disabled
                                        style="opacity: 0.5; cursor: not-allowed;"
                                    >
                                        + Select Additional Item ({{ idx + 3 }}/{{ maxAdditionalItems }})
                                    </button>
                                    <!-- Active button if this IS the last item AND we can add more -->
                                    <button
                                        v-else-if="idx + 3 <= maxAdditionalItems"
                                        type="button"
                                        class="btn btn-primary w-100 w-md-auto"
                                        @click="addAdditionalItem"
                                    >
                                        + Select Additional Item ({{ idx + 3 }}/{{ maxAdditionalItems }})
                                    </button>
                                    <!-- Remove button for the NEXT item, shown only when next item is the last -->
                                    <button
                                        v-if="idx === additionalItems.length - 2"
                                        type="button"
                                        class="btn btn-outline-danger w-100 w-md-auto"
                                        @click="removeLastAdditionalItem"
                                    >
                                        Remove Item {{ idx + 3 }}
                                    </button>
                                </div>
                            </div>
                        </div>

                    </div>

                    <!-- [REQ] Input: Relationship with Brand -->
                    <!-- COMMENTED OUT: Brand relationship selection is handled automatically
                    <p class="text-start mb-1" v-if="formType == 'req'">Your Relationship with the Brand <span class="text-danger">*</span></p>
                    <div class="text-start mb-3" v-if="formType == 'req'">
                        <div class="form-check form-check-inline" v-if="userType == 'user'">
                            <input class="form-check-input" type="radio" v-model="form['brandRelation']" :value="'Customer'" name="brandRelationCustomer" id="brandRelationCustomer">
                            <label class="form-check-label" for="brandRelationCustomer">Customer</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" v-model="form['brandRelation']" :value="'Employee'" name="brandRelationEmployee" id="brandRelationEmployee">
                            <label class="form-check-label" for="brandRelationEmployee">Employee</label>
                        </div>
                        <div class="form-check form-check-inline" v-if="userType == 'user'">
                            <input class="form-check-input" type="radio" v-model="form['brandRelation']" :value="'Public Relations'" name="brandRelationPR" id="brandRelationPR">
                            <label class="form-check-label" for="brandRelationPR">Public Relations</label>
                        </div>
                        <div class="form-check form-check-inline" v-if="userType == 'user'">
                            <input class="form-check-input" type="radio" v-model="form['brandRelation']" :value="'Distributor'" name="brandRelationDist" id="brandRelationDist">
                            <label class="form-check-label" for="brandRelationDist">Distributor</label>
                        </div>
                        <div class="form-check form-check-inline" v-if="userType == 'user'">
                            <input class="form-check-input" type="radio" v-model="form['brandRelation']" :value="'Others'" name="brandRelationOther" id="brandRelationOther">
                            <label class="form-check-label" for="brandRelationOther">Others</label>
                        </div>
                    </div>
                    -->

                    <!-- Error Handling -->
                    <div v-if="errors.length > 0">
                        <div class="alert alert-danger" role="alert">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-triangle" viewBox="0 0 16 16">
                            <path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.146.146 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.163.163 0 0 1-.054.06.116.116 0 0 1-.066.017H1.146a.115.115 0 0 1-.066-.017.163.163 0 0 1-.054-.06.176.176 0 0 1 .002-.183L7.884 2.073a.147.147 0 0 1 .054-.057zm1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566z"/>
                            <path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995z"/>
                            </svg>
                            <h5> Error </h5>
                            <li v-for="error in errors" :key="error"> {{ error }} </li>
                        </div>
                    </div>
                    
                    <!-- Submission Buttons -->
                    <div v-if="formType == 'req'">
                        <button type="button" class="btn btn-secondary mx-1 mb-3" @click="goBack">Return</button>
                        <button type="submit" class="btn primary-square-btn-green mx-1 mb-3" v-if="formMode == 'new'">Submit Listing Request</button>  <!--tzh added -green-->
                         <button type="button" class="btn btn-outline-primary mx-1 mb-3" v-if="formMode == 'new'" @click="openStagingModal">Stage Listing(s) for Submission</button>
                        <button type="submit" class="btn primary-square-btn-green mx-1 mb-3" v-if="formMode == 'edit'">Submit Edit Request</button> <!--tzh added -green-->
                        <button type="submit" class="btn primary-square-btn-green mx-1 mb-3" v-if="formMode == 'dup'">Submit Duplicate Report</button> <!--tzh added -green-->
                        
                    </div>
                    <div v-if="formType == 'power'">
                        <button type="button" class="btn btn-secondary mx-1 mb-3" @click="goBack">Return</button>
                        <button type="submit" class="btn primary-square-btn-green mx-1 mb-3" v-if="formMode == 'new'">Create New Listing</button>  <!--tzh changed secondary-btn to primary-square-btn-green-->
                        <button type="button" class="btn btn-outline-primary mx-1 mb-3" v-if="formMode == 'new'" @click="openStagingModal">Stage Listing(s) for Submission</button>
                        <button type="submit" class="btn primary-square-btn-green mx-1 mb-3" v-if="formMode == 'edit'">Save Listing Edits</button> <!--tzh changed secondary-btn to primary-square-btn-green-->

                        <button type="button" class="btn btn-danger rounded-pill mx-1 mb-3" v-if="prevListing" @click="updateRequestStatus('reject')">Reject Request</button>
                        
                    </div>
                
                </form>

            </div>
        </div>
    </div>

    <!-- Staging Modal -->
    <div v-if="showStagingModal" class="staging-modal-overlay" @click.self="!bulkSubmissionInProgress && closeStagingModal()">
        <div class="staging-modal-content">
            <div class="staging-modal-header">
                <h4 class="mb-0">
                    <span v-if="!bulkSubmissionComplete">Review Staged Listings</span>
                    <span v-else>Submission Results</span>
                </h4>
                <button type="button" class="btn-close" @click="closeStagingModal" :disabled="bulkSubmissionInProgress"></button>
            </div>
            <div class="staging-modal-body">
                <!-- Pre-submission info -->
                <div v-if="!bulkSubmissionComplete && !bulkSubmissionInProgress" class="mb-3">
                    <p class="text-muted mb-1">
                        <span v-if="getNewItemsCount() > 0">
                            <strong>{{ getNewItemsCount() }}</strong> item(s) to be submitted
                        </span>
                        <span v-if="getNewItemsCount() > 0 && getConfirmedDuplicatesCount() > 0">, </span>
                        <span v-if="getConfirmedDuplicatesCount() > 0" class="text-secondary">
                            <strong>{{ getConfirmedDuplicatesCount() }}</strong> existing listing(s) <span class="small">(will not be submitted)</span>
                        </span>
                    </p>
                    <p class="text-muted small mb-0">Please review before confirming.</p>
                </div>
                
                <!-- In-progress spinner -->
                <div v-if="bulkSubmissionInProgress" class="text-center py-3">
                    <div class="spinner-border text-primary mb-2" role="status">
                        <span class="visually-hidden">Submitting...</span>
                    </div>
                    <p class="text-info fw-bold mb-0">Submitting {{ getNewItemsCount() }} item(s)... Please wait.</p>
                </div>
                
                <!-- Post-submission summary -->
                <div v-if="bulkSubmissionComplete && bulkSubmissionSummary" class="mb-3">
                    <div class="alert" :class="bulkSubmissionSummary.failCount === 0 && bulkSubmissionSummary.totalSubmitted > 0 ? 'alert-success' : (bulkSubmissionSummary.successCount === 0 && bulkSubmissionSummary.totalSubmitted > 0 ? 'alert-danger' : (bulkSubmissionSummary.totalSubmitted === 0 ? 'alert-info' : 'alert-warning'))">
                        <h5 class="alert-heading mb-2">
                            <span v-if="bulkSubmissionSummary.totalSubmitted === 0">ℹ️ No new submissions</span>
                            <span v-else-if="bulkSubmissionSummary.failCount === 0">✓ All items submitted successfully!</span>
                            <span v-else-if="bulkSubmissionSummary.successCount === 0">✗ All items failed to submit</span>
                            <span v-else>⚠ Partial success</span>
                        </h5>
                        <p class="mb-1">
                            <span v-if="bulkSubmissionSummary.totalSubmitted > 0">
                                <strong>{{ bulkSubmissionSummary.successCount }}</strong> submitted successfully, 
                                <strong>{{ bulkSubmissionSummary.failCount }}</strong> failed
                            </span>
                            <span v-if="bulkSubmissionSummary.existingCount > 0">
                                <span v-if="bulkSubmissionSummary.totalSubmitted > 0">, </span>
                                <strong>{{ bulkSubmissionSummary.existingCount }}</strong> existing listing(s) <span class="text-muted">(not submitted)</span>
                            </span>
                        </p>
                        <p v-if="bulkSubmissionSummary.pointsAwarded > 0" class="mb-1 text-success">
                            🎯 +{{ bulkSubmissionSummary.pointsAwarded }} proof points awarded!
                        </p>
                        <p v-if="bulkSubmissionSummary.autoApprovalEnabled && bulkSubmissionSummary.successCount > 0" class="mb-0 text-info small">
                            <i class="bi bi-info-circle"></i> Auto-approval is enabled. Successful items are now live.
                        </p>
                    </div>
                </div>

                <!-- Validation errors (if any) -->
                <div v-if="errors.length > 0" class="alert alert-danger mb-3">
                    <h6 class="alert-heading">Validation Errors:</h6>
                    <ul class="mb-0">
                        <li v-for="error in errors" :key="error">{{ error }}</li>
                    </ul>
                </div>
                
                <div class="table-responsive staging-table-wrapper">
                    <table class="table table-bordered staging-table">
                        <thead class="table-light sticky-header">
                            <tr>
                                <th>#</th>
                                <th style="min-width: 220px;">Status</th>
                                <th>Photo</th>
                                <th>Listing Name</th>
                                <th>Producer</th>
                                <th>IB</th>
                                <th>Bottler</th>
                                <th>Drink Type</th>
                                <th>Category</th>
                                <th>Style</th>
                                <th>Country</th>
                                <th>ABV</th>
                                <th>Age</th>
                                <th>Variety Tags</th>
                                <th>Description</th>
                                <th>Source Link</th>
                                <th>Review Link</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- Item 1 (main form) -->
                            <tr :class="getRowClass(0)">
                                <td>1</td>
                                <td>
                                    <!-- Pre-submission: show if existing or pending -->
                                    <template v-if="!bulkSubmissionComplete">
                                        <span v-if="isItemConfirmedDuplicate(0)" class="badge bg-secondary">
                                            📌 Existing listing
                                            <a v-if="getConfirmedDuplicateInfo(0)?.id" 
                                               :href="'/listing/view/' + getConfirmedDuplicateInfo(0).id + '/' + slugify(getConfirmedDuplicateInfo(0).listingName || '')"
                                               target="_blank"
                                               class="ms-1 text-white"
                                               @click.stop>
                                                (ID: {{ getConfirmedDuplicateInfo(0).id }}) ↗
                                            </a>
                                        </span>
                                        <span v-else class="badge bg-primary">🆕 New submission</span>
                                    </template>
                                    <!-- Post-submission: show result -->
                                    <template v-else>
                                        <!-- Existing listing (skipped) -->
                                        <span v-if="getItemSubmissionStatus(0)?.isExisting" class="badge bg-secondary">
                                            ⏭️ Skipped - Already exists
                                            <a v-if="getItemSubmissionStatus(0)?.existingListingId" 
                                               :href="'/listing/view/' + getItemSubmissionStatus(0).existingListingId + '/' + slugify(getItemSubmissionStatus(0).existingListingName || '')"
                                               target="_blank"
                                               class="ms-1 text-white"
                                               @click.stop>
                                                (ID: {{ getItemSubmissionStatus(0).existingListingId }}) ↗
                                            </a>
                                        </span>
                                        <!-- Success -->
                                        <span v-else-if="getItemSubmissionStatus(0)?.success" class="badge bg-success">
                                            ✓ Success
                                            <a v-if="getItemSubmissionStatus(0)?.listingId" 
                                               :href="'/listing/view/' + getItemSubmissionStatus(0).listingId + '/' + slugify(form['listingName'] || '')"
                                               target="_blank"
                                               class="ms-1 text-white"
                                               @click.stop>
                                                (ID: {{ getItemSubmissionStatus(0).listingId }}) ↗
                                            </a>
                                            <span v-else-if="getItemSubmissionStatus(0)?.requestId"> (Req ID: {{ getItemSubmissionStatus(0).requestId }})</span>
                                        </span>
                                        <!-- Failed -->
                                        <span v-else class="badge bg-danger text-wrap text-start" style="white-space: normal;">
                                            ✗ {{ getItemSubmissionStatus(0)?.error || 'Failed' }}
                                        </span>
                                    </template>
                                </td>
                                <td>
                                    <img 
                                        v-if="form['photo']" 
                                        :src="form['photo']" 
                                        class="staging-thumbnail"
                                        alt="Item 1 photo"
                                    />
                                    <span v-else class="text-muted">-</span>
                                </td>
                                <td>{{ form['listingName'] || '-' }}</td>
                                <td>{{ form['producerNew'] || '-' }}</td>
                                <td>{{ indOperator ? 'Yes' : 'No' }}</td>
                                <td>{{ form['bottler'] || '-' }}</td>
                                <td>{{ tempDrinkType || '-' }}</td>
                                <td>{{ tempTypeCategory || '-' }}</td>
                                <td>{{ tempDrinkStyle || '-' }}</td>
                                <td>{{ form['originCountry'] || '-' }}</td>
                                <td>{{ form['abv'] || '-' }}</td>
                                <td>{{ form['age'] || '-' }}</td>
                                <td>{{ formatVarietyTags(varietyTagsList) }}</td>
                                <td class="text-truncate-cell">{{ form['officialDesc'] || '-' }}</td>
                                <td class="text-truncate-cell">{{ form['sourceLink'] || '-' }}</td>
                                <td class="text-truncate-cell">{{ form['reviewLink'] || '-' }}</td>
                            </tr>
                            <!-- Additional items -->
                            <tr v-for="(item, index) in additionalItems" :key="'staged-' + index" :class="getRowClass(index + 1)">
                                <td>{{ index + 2 }}</td>
                                <td>
                                    <!-- Pre-submission: show if existing or pending -->
                                    <template v-if="!bulkSubmissionComplete">
                                        <span v-if="isItemConfirmedDuplicate(index + 1)" class="badge bg-secondary">
                                               Existing listing 
                                            <a v-if="getConfirmedDuplicateInfo(index + 1)?.id" 
                                               :href="'/listing/view/' + getConfirmedDuplicateInfo(index + 1).id + '/' + slugify(getConfirmedDuplicateInfo(index + 1).listingName || '')"
                                               target="_blank"
                                               class="ms-1 text-white"
                                               @click.stop>
                                               (ID: {{ getConfirmedDuplicateInfo(index + 1).id }})
                                            </a>↗
                                        </span> 
                                        <span v-else class="badge bg-primary">New submission</span>
                                    </template>
                                    <!-- Post-submission: show result -->
                                    <template v-else>
                                        <!-- Existing listing (skipped) -->
                                        <span v-if="getItemSubmissionStatus(index + 1)?.isExisting" class="badge bg-secondary">
                                            ⏭️ Skipped - Already exists
                                            <a v-if="getItemSubmissionStatus(index + 1)?.existingListingId" 
                                               :href="'/listing/view/' + getItemSubmissionStatus(index + 1).existingListingId + '/' + slugify(getItemSubmissionStatus(index + 1).existingListingName || '')"
                                               target="_blank"
                                               class="ms-1 text-white"
                                               @click.stop>
                                                (ID: {{ getItemSubmissionStatus(index + 1).existingListingId }}) ↗
                                            </a>
                                        </span>
                                        <!-- Success -->
                                        <span v-else-if="getItemSubmissionStatus(index + 1)?.success" class="badge bg-success">
                                            ✓ Success
                                            <a v-if="getItemSubmissionStatus(index + 1)?.listingId" 
                                               :href="'/listing/view/' + getItemSubmissionStatus(index + 1).listingId + '/' + slugify(item.listingName || '')"
                                               target="_blank"
                                               class="ms-1 text-white"
                                               @click.stop>
                                                (ID: {{ getItemSubmissionStatus(index + 1).listingId }}) ↗
                                            </a>
                                            <span v-else-if="getItemSubmissionStatus(index + 1)?.requestId"> (Req: {{ getItemSubmissionStatus(index + 1).requestId }})</span>
                                        </span>
                                        <!-- Failed -->
                                        <span v-else class="badge bg-danger text-wrap text-start" style="white-space: normal;">
                                            ✗ {{ getItemSubmissionStatus(index + 1)?.error || 'Failed' }}
                                        </span>
                                    </template>
                                </td>
                                <td>
                                    <img 
                                        v-if="item.photo" 
                                        :src="item.photo" 
                                        class="staging-thumbnail"
                                        alt="Item photo"
                                    />
                                    <span v-else class="text-muted">-</span>
                                </td>
                                <td>{{ item.listingName || '-' }}</td>
                                <td>{{ item.producerNew || '-' }}</td>
                                <td>{{ item.indOperator ? 'Yes' : 'No' }}</td>
                                <td>{{ item.bottler || '-' }}</td>
                                <td>{{ item.tempDrinkType || '-' }}</td>
                                <td>{{ item.tempTypeCategory || '-' }}</td>
                                <td>{{ item.tempDrinkStyle || '-' }}</td>
                                <td>{{ item.originCountry || '-' }}</td>
                                <td>{{ item.abv || '-' }}</td>
                                <td>{{ item.age || '-' }}</td>
                                <td>{{ formatVarietyTags(item.varietyTagsList) }}</td>
                                <td class="text-truncate-cell">{{ item.officialDesc || '-' }}</td>
                                <td class="text-truncate-cell">{{ item.sourceLink || '-' }}</td>
                                <td class="text-truncate-cell">{{ item.reviewLink || '-' }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="staging-modal-footer">
                <!-- Pre-submission buttons -->
                <template v-if="!bulkSubmissionComplete && !bulkSubmissionInProgress">
                    <button type="button" class="btn btn-secondary" @click="closeStagingModal">Cancel</button>
                    <button type="button" class="btn btn-success" @click="confirmStagedSubmission">Confirm Submission</button>
                </template>
                
                <!-- In-progress state -->
                <template v-if="bulkSubmissionInProgress">
                    <button type="button" class="btn btn-secondary" disabled>Please wait...</button>
                </template>
                
                <!-- Post-submission buttons -->
                <template v-if="bulkSubmissionComplete">
                    <button type="button" class="btn btn-secondary" @click="closeStagingModal">Close</button>
                    <button 
                        v-if="bulkSubmissionSummary && (bulkSubmissionSummary.failCount === 0 || bulkSubmissionSummary.totalSubmitted === 0)"
                        type="button" 
                        class="btn btn-primary" 
                        @click="closeStagingModal(); reset();"
                    >
                        Submit More Listings
                    </button>
                </template>
            </div>
        </div>
    </div>

    <BadgePopup 
        :badges="earnedBadges" 
        :show="showBadgePopup" 
        @close="closeBadgePopup"
    />
</template>

<script>
    // import SearchBar from './SearchBar.vue';
    import AutocompleteSearch from './AutocompleteSearch.vue';
    import CreateProducerModal from './CreateProducerModal.vue';
    import { useSearch } from '@/composables/navbar/useSearch'
    import BadgePopup from "@/components/BadgePopup.vue";

    export default {
        name: "BulkSubmitListingNew",
        components: {
            AutocompleteSearch,
            CreateProducerModal,
            BadgePopup
        },
        props: {
            formType: String,
            formMode: String
        },
        setup() {
            /* Searchbar handler functions stars here */
            const { handleSelection } = useSearch()
            /* Searchbar handler functions ends here */

            return {
            // Search functionality
            handleSelection
            }
        },
        data () {
            return {
                // Default Photo

                defaultPhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",
                // User
                userType: "",
                // Flags
                dataLoaded: false,
                submitForm: false,
                successSubmission: false,
                errorSubmission: false,
                fillForm: false,
                requestRemoval: false,
                showCreateProducerModal: false,
                showStagingModal: false,

                // Error-specific flags
                errorMessage: false,
                invalidListing: false,
                duplicateEntry: false,
                errors: [],

                // Pre-loaded data
                targetListing: {},
                isProducer: false,
                prevListing: false,
                modifyRequest: {},
                types: [],

                // Form model variables
                tempDrinkType: "",
                tempTypeCategory: "",
                tempProducer: "",
                indOperator: false,
                tempDrinkStyle: "",

                // Form data variables
                drinkCategories: [],
                drinkCategoriesList: [],
                tempTypeCategoryList: [],
                producerList: [],
                bottlersList: [],
                countries: [],
                selectedImage:"",
                drinkStyles:[],
                drinkStylesList:[],
                tempDrinkStylesList: [],

                // Country drawer functionality
                selectedCountry: "",
                showCountryDrawer: false,
                countryInputValue: "", // The actual input value that user types
                filteredCountries: [],

                // New producer selection state
                selectedProducer: {},
                showProducerDropdown: false,
                
                // Producer search toggle and ID search
                searchByProducerId: false,
                producerIdList: [],
                showProducerIdDropdown: false,
                producerIdValidationError: "",

                // New bottler selection state
                selectedBottler: {},
                showBottlerDropdown: false,

                // Bulk mode toggle
                bulkSameProducerMode: false,

                // Additional items
                additionalItems: [],
                maxAdditionalItems: 20,

                // Variety Tags
                varietyTagInput: "",
                varietyTagsList: [],

                form: {
                    "editDesc": "",
                    "sourceLink": "",
                    "duplicateLink": "",
                    "listingName": "",
                    "officialDesc": "",
                    "reviewLink": "",
                    "producerNew": "", 
                    "producerIdSearch": "",
                    "bottler": "",
                    "originCountry": "",
                    "abv": "",
                    "age": "",
                    "brandRelation": "Others",
                    "userID": "",
                    "producerID": "",
                    "bottlerID": "",
                    "listingID": "",
                    "photo": "",
                    "tags": "",
                    "order": "",
                    "varietyTags": null,
                },
                producerDebounceTimer: null,
                producerIdDebounceTimer: null,
                bottlerDebounceTimer: null,

                earnedBadges: [],
                showBadgePopup: false,
                
                // Drag and drop state
                isDragging: false,

                // Duplicate detection state for main form (Item 1)
                duplicateDetection: {
                    isLoading: false,
                    isCollapsed: false,
                    matches: [],
                    confirmedDuplicate: null,  // The listing object if user confirmed a duplicate
                    isConfirmed: false,        // Whether user has confirmed this is a duplicate
                },
                duplicateDebounceTimer: null,

                // Bulk submission results tracking
                bulkSubmissionResults: [],        // Array of results from API
                bulkSubmissionSummary: null,      // { totalSubmitted, successCount, failCount, autoApprovalEnabled, pointsAwarded, badgeAwarded }
                bulkSubmissionInProgress: false,  // True while API call is in progress
                bulkSubmissionComplete: false,    // True after API response received
            };
        },
        async mounted() {
            console.log("Component mounted. Route params:", this.$route.params);
    
            // Restore cached form data immediately
            const cachedForm = localStorage.getItem('cachedListingForm');
            if (cachedForm) {
                this.form = JSON.parse(cachedForm);
                this.tempDrinkType = localStorage.getItem('cachedListingTempDrinkType') || "";
                this.tempTypeCategory = localStorage.getItem('cachedListingTempTypeCategory') || "";
                this.tempDrinkStyle = localStorage.getItem('cachedListingTempDrinkStyle') || "";
                
                // Restore selectedProducer if we have producer data in cache
                if (this.form['producerID'] && this.form['producerNew']) {
                    this.selectedProducer = {
                        id: this.form['producerID'],
                        producerName: this.form['producerNew']
                    };
                    // Also populate the ID search field to keep consistency
                    this.form['producerIdSearch'] = this.form['producerID'];
                }
                
                // Restore selectedBottler if we have bottler data in cache
                if (this.form['bottlerID'] && this.form['bottler']) {
                    this.selectedBottler = {
                        id: this.form['bottlerID'],
                        producerName: this.form['bottler']
                    };
                }
                
                // Restore varietyTagsList from cache
                const cachedVarietyTags = localStorage.getItem('cachedVarietyTagsList');
                if (cachedVarietyTags) {
                    try {
                        this.varietyTagsList = JSON.parse(cachedVarietyTags);
                    } catch (e) {
                        console.error("Error parsing cached variety tags:", e);
                        this.varietyTagsList = [];
                    }
                }
            }

            // Get userID
            this.form['userID'] = localStorage.getItem('88B_accID');
            this.userType = localStorage.getItem('88B_accType');
            if (this.userType == "producer") {
                this.form.brandRelation = "Employee"
                this.form.editDesc = "This listing is produced by my distillery."
            }

            // Check if route params "requestID" is present
            if (this.$route.params.requestID != "" && this.$route.params.requestID != undefined) {
                this.prevListing = true;
                console.log('this.prevListing set to', this.prevListing, 'in mounted()');
            }

            // Power user check
            if (this.formType == "power") {
                await this.checkPower();
            } else {
                // Load data
                await this.loadData();
            }
        },
        beforeUnmount() {
            // Clean up event listener when component is destroyed
            document.removeEventListener('click', this.handleClickOutside);
        },
        watch: {
            form: {
                handler(newData) {
                    localStorage.setItem('cachedListingForm', JSON.stringify(newData));
                },
                deep: true,
            },

            tempDrinkType(newVal) {
                localStorage.setItem('cachedListingTempDrinkType', newVal);
            },
            tempTypeCategory(newVal) {
                localStorage.setItem('cachedListingTempTypeCategory', newVal);
            },
            tempDrinkStyle(newVal) {
                localStorage.setItem('cachedListingTempDrinkStyle', newVal);
            },

            // Watch varietyTagsList changes and update form
            varietyTagsList: {
                handler(newVal) {
                    // Convert array to PostgreSQL array format or null if empty
                    if (newVal && newVal.length > 0) {
                        this.form['varietyTags'] = newVal;
                    } else {
                        this.form['varietyTags'] = null;
                    }
                    // Cache the list
                    localStorage.setItem('cachedVarietyTagsList', JSON.stringify(newVal));
                },
                deep: true,
            },

            // Keep input value synced with selected country and form data
            selectedCountry(newVal) {
                if (newVal && this.countryInputValue !== newVal) {
                    this.countryInputValue = newVal;
                }
                // Update form data
                this.form['originCountry'] = newVal;
            },

            // Watch for changes in formMode and formType to load data accordingly
            'form.bottler'(newVal) {
                if (newVal && newVal.length >= 2) {
                    this.debouncedFetchBottlers(newVal);
                }
            },
            // Watch for changes in producerNew to fetch suggestions
            'form.producerNew'(newVal) {
                if (newVal && newVal.length >= 2) {
                    this.debouncedFetchProducers(newVal);
                }
            },

            // ============ DUPLICATE DETECTION ============
            // Both Item 1 and Additional Items use explicit @input/@change handlers in template
            // on the 5 trigger fields: listingName, tempDrinkType, originCountry, producer, bottler
            // Producer/Bottler selection triggers are in selectProducer() and selectBottler() methods
        },
        methods:{

            slugify(text) {
                return text
                    .toString()
                    .toLowerCase()
                    .replace(/\s+/g, '')
                    .replace(/[^\w]/g, '');
            },

            // Add variety tag to the list
            addVarietyTag() {
                const tag = this.varietyTagInput.trim();
                
                // Validate tag
                if (!tag) {
                    return;
                }
                
                // Check length (max 20 characters)
                if (tag.length > 20) {
                    alert("Each variety tag must be 20 characters or less.");
                    return;
                }
                
                // Check for special characters (allow only letters, numbers, and spaces)
                if (!/^[a-zA-Z0-9\s]+$/.test(tag)) {
                    alert("Variety tags can only contain letters, numbers, and spaces.");
                    return;
                }
                
                // Check for duplicates (case-insensitive)
                if (this.varietyTagsList.some(t => t.toLowerCase() === tag.toLowerCase())) {
                    alert("This variety tag has already been added.");
                    return;
                }
                
                // Add tag to list
                this.varietyTagsList.push(tag);
                
                // Clear input
                this.varietyTagInput = "";
            },

            // Remove variety tag from the list
            removeVarietyTag(index) {
                this.varietyTagsList.splice(index, 1);
            },

            // Additional item helpers (UI-only for now)
            createAdditionalItem(prefill = false) {
                const baseType = prefill ? this.tempDrinkType : "";
                const typeCategoryList = this.buildTypeCategoryList(baseType);
                return {
                    tags: "",
                    order: "",
                    producerNew: prefill ? this.form['producerNew'] : "",
                    producerID: prefill ? this.form['producerID'] : "",
                    producerIdSearch: prefill ? this.form['producerIdSearch'] : "",
                    selectedProducer: prefill && this.selectedProducer ? { ...this.selectedProducer } : {},
                    showProducerDropdown: false,
                    showProducerIdDropdown: false,
                    searchByProducerId: false,
                    producerIdValidationError: "",
                    indOperator: prefill ? this.indOperator : false,
                    bottler: prefill ? this.form['bottler'] : "",
                    bottlerID: prefill ? this.form['bottlerID'] : "",
                    selectedBottler: prefill && this.selectedBottler ? { ...this.selectedBottler } : {},
                    showBottlerDropdown: false,
                    originCountry: prefill ? this.form['originCountry'] : "",
                    listingName: "",
                    tempDrinkType: baseType,
                    tempTypeCategory: "",
                    tempDrinkStyle: "",
                    tempTypeCategoryList: typeCategoryList,
                    tempDrinkStylesList: this.buildDrinkStyleList(""),
                    varietyTagInput: "",
                    varietyTagsList: [],
                    photo: "",
                    selectedImage: "",
                    isDragging: false,
                    abv: "",
                    age: "",
                    officialDesc: "",
                    sourceLink: "",
                    reviewLink: "",
                    // Duplicate detection state for this additional item
                    duplicateDetection: {
                        isLoading: false,
                        isCollapsed: false,
                        matches: [],
                        confirmedDuplicate: null,
                        isConfirmed: false,
                    },
                    duplicateDebounceTimer: null,
                };
            },

            addAdditionalItem() {
                if (this.additionalItems.length >= this.maxAdditionalItems) return;
                const newItem = this.createAdditionalItem(this.bulkSameProducerMode);
                this.additionalItems.push(newItem);
            },

            removeLastAdditionalItem() {
                if (this.additionalItems.length === 0) return;
                this.additionalItems.pop();
            },

            // Staging Modal Methods
            openStagingModal() {
                // Reset bulk submission state when opening modal
                this.bulkSubmissionResults = [];
                this.bulkSubmissionSummary = null;
                this.bulkSubmissionInProgress = false;
                this.bulkSubmissionComplete = false;
                
                this.showStagingModal = true;
                // Prevent body scroll when modal is open
                document.body.style.overflow = 'hidden';
            },

            closeStagingModal() {
                this.showStagingModal = false;
                document.body.style.overflow = '';
                
                // If submission was complete, reset bulk state
                if (this.bulkSubmissionComplete) {
                    this.bulkSubmissionResults = [];
                    this.bulkSubmissionSummary = null;
                    this.bulkSubmissionComplete = false;
                }
            },

            getStagedItemsCount() {
                return 1 + this.additionalItems.length;
            },

            // Check if an item at a given index is a confirmed duplicate
            isItemConfirmedDuplicate(index) {
                if (index === 0) {
                    return this.duplicateDetection.isConfirmed;
                }
                const item = this.additionalItems[index - 1];
                return item?.duplicateDetection?.isConfirmed || false;
            },

            // Get the confirmed duplicate info for an item
            getConfirmedDuplicateInfo(index) {
                if (index === 0) {
                    return this.duplicateDetection.confirmedDuplicate;
                }
                const item = this.additionalItems[index - 1];
                return item?.duplicateDetection?.confirmedDuplicate || null;
            },

            // Count confirmed duplicates (existing listings)
            getConfirmedDuplicatesCount() {
                let count = this.duplicateDetection.isConfirmed ? 1 : 0;
                for (const item of this.additionalItems) {
                    if (item.duplicateDetection?.isConfirmed) {
                        count++;
                    }
                }
                return count;
            },

            // Count new items to be submitted (excluding confirmed duplicates)
            getNewItemsCount() {
                return this.getStagedItemsCount() - this.getConfirmedDuplicatesCount();
            },

            formatVarietyTags(tagsList) {
                if (!tagsList || tagsList.length === 0) return '-';
                return tagsList.join(', ');
            },

            // Get submission status for an item by index
            getItemSubmissionStatus(index) {
                // Check if this is a confirmed duplicate (existing listing)
                if (this.isItemConfirmedDuplicate(index)) {
                    const duplicateInfo = this.getConfirmedDuplicateInfo(index);
                    return {
                        index: index,
                        success: false,
                        skipped: true,
                        isExisting: true,
                        existingListingId: duplicateInfo?.id || null,
                        existingListingName: duplicateInfo?.listingName || null
                    };
                }
                
                if (!this.bulkSubmissionComplete || !this.bulkSubmissionResults.length) {
                    return null; // No status yet
                }
                const result = this.bulkSubmissionResults.find(r => r.index === index);
                return result || null;
            },

            // Get status badge class for table row
            getStatusBadgeClass(index) {
                const status = this.getItemSubmissionStatus(index);
                if (!status) return '';
                if (status.isExisting) return 'bg-secondary';
                return status.success ? 'bg-success' : 'bg-danger';
            },

            // Get status text for table cell
            getStatusText(index) {
                const status = this.getItemSubmissionStatus(index);
                if (!status) return '-';
                if (status.isExisting) {
                    return `⏭️ Skipped - Already exists - Drink ID: ${status.existingListingId || 'N/A'}`;
                }
                if (status.success) {
                    const idText = status.listingId ? `ID: ${status.listingId}` : (status.requestId ? `Req ID: ${status.requestId}` : '');
                    return `✓ Success ${idText}`;
                }
                return `✗ Failed: ${status.error || 'Unknown error'}`;
            },

            // Get row class based on submission status
            getRowClass(index) {
                const status = this.getItemSubmissionStatus(index);
                if (!status) return 'row-pending';
                if (status.isExisting) return 'row-skipped';
                return status.success ? 'row-success' : 'row-error';
            },

            async confirmStagedSubmission() {
                // Validate all items first
                this.errors = [];
                if (!this.validateAllItemsForBulk()) {
                    console.log("Bulk validation errors:", this.errors);
                    return;
                }

                // Set in-progress state (keep modal open)
                this.bulkSubmissionInProgress = true;
                this.bulkSubmissionComplete = false;
                this.bulkSubmissionResults = [];
                this.bulkSubmissionSummary = null;

                // Count existing listings (confirmed duplicates)
                const existingCount = this.getConfirmedDuplicatesCount();
                const newItemsCount = this.getNewItemsCount();

                // If all items are existing listings, skip API call
                if (newItemsCount === 0) {
                    console.log("All items are existing listings. Skipping API call.");
                    this.bulkSubmissionSummary = {
                        totalSubmitted: 0,
                        successCount: 0,
                        failCount: 0,
                        existingCount: existingCount,
                        autoApprovalEnabled: false,
                        pointsAwarded: 0,
                        badgeAwarded: null,
                        message: `All ${existingCount} item(s) are existing listings. Nothing to submit.`
                    };
                    this.bulkSubmissionInProgress = false;
                    this.bulkSubmissionComplete = true;
                    return;
                }

                let submitAPI = "";
                let bulkPayload = {};

                if (this.formType === "req") {
                    // Request mode bulk submission
                    submitAPI = `${process.env.VUE_APP_API_URL}/requestListing/requestListingBulk`;
                    bulkPayload = this.buildBulkRequestPayload();
                } else if (this.formType === "power") {
                    // Power mode bulk submission
                    submitAPI = `${process.env.VUE_APP_API_URL}/createListing/createListingBulk`;
                    bulkPayload = this.buildBulkPowerPayload();
                } else {
                    alert("Invalid form type for bulk submission!");
                    this.bulkSubmissionInProgress = false;
                    return;
                }

                console.log("Bulk submission to:", submitAPI);
                console.log("Bulk payload:", JSON.stringify(bulkPayload, null, 2));
                console.log(`Submitting ${newItemsCount} new item(s), ${existingCount} existing listing(s) skipped.`);

                try {
                    const response = await this.$axios.post(submitAPI, bulkPayload);
                    const responseData = response.data;

                    console.log("Bulk API response:", responseData);

                    // Map backend results back to original indices using originalIndex
                    const apiResults = responseData.data?.results || [];
                    const mappedResults = apiResults.map(result => {
                        // The backend returns index relative to the payload, but we included originalIndex
                        // We need to find the item in the payload that matches this result
                        const payloadItems = this.formType === "req" ? bulkPayload.items : bulkPayload.listings;
                        const originalIndex = payloadItems[result.index]?.originalIndex;
                        return {
                            ...result,
                            index: originalIndex !== undefined ? originalIndex : result.index
                        };
                    });

                    // Store mapped results
                    this.bulkSubmissionResults = mappedResults;
                    this.bulkSubmissionSummary = {
                        totalSubmitted: responseData.data?.totalSubmitted || 0,
                        successCount: responseData.data?.successCount || 0,
                        failCount: responseData.data?.failCount || 0,
                        existingCount: existingCount,
                        autoApprovalEnabled: responseData.data?.autoApprovalEnabled || false,
                        pointsAwarded: responseData.data?.pointsAwarded || 0,
                        badgeAwarded: responseData.data?.badgeAwarded || null,
                        message: responseData.message || ''
                    };

                    // If there were any successes, clear cache
                    if (this.bulkSubmissionSummary.successCount > 0) {
                        localStorage.removeItem('cachedListingForm');
                        localStorage.removeItem('cachedListingTempDrinkType');
                        localStorage.removeItem('cachedListingTempTypeCategory');
                        localStorage.removeItem('cachedListingTempDrinkStyle');
                        localStorage.removeItem('cachedVarietyTagsList');
                    }

                    // Handle badge popup if badge was awarded
                    if (this.bulkSubmissionSummary.badgeAwarded) {
                        this.earnedBadges = [this.bulkSubmissionSummary.badgeAwarded];
                        this.showBadgePopup = true;
                    }

                } catch (error) {
                    console.error("Bulk API error:", error.response?.data || error);
                    
                    // Create error results for only the new items (not confirmed duplicates)
                    // Map errors to original indices
                    const errorResults = [];
                    if (!this.duplicateDetection.isConfirmed) {
                        errorResults.push({
                            index: 0,
                            success: false,
                            error: error.response?.data?.message || 'Server error occurred'
                        });
                    }
                    for (let i = 0; i < this.additionalItems.length; i++) {
                        if (!this.additionalItems[i].duplicateDetection?.isConfirmed) {
                            errorResults.push({
                                index: i + 1,
                                success: false,
                                error: error.response?.data?.message || 'Server error occurred'
                            });
                        }
                    }
                    
                    this.bulkSubmissionResults = errorResults;
                    this.bulkSubmissionSummary = {
                        totalSubmitted: newItemsCount,
                        successCount: 0,
                        failCount: newItemsCount,
                        existingCount: existingCount,
                        message: error.response?.data?.message || 'An error occurred during submission'
                    };
                } finally {
                    this.bulkSubmissionInProgress = false;
                    this.bulkSubmissionComplete = true;
                }
            },

            buildTypeCategoryList(drinkType) {
                if (!drinkType || !Array.isArray(this.drinkCategories)) {
                    return ["-"];
                }
                const found = this.drinkCategories.find(cat => cat.drinkType === drinkType);
                const list = found && Array.isArray(found.typeCategory) ? [...found.typeCategory] : [];
                list.unshift("-");
                return list;
            },

            buildDrinkStyleList(typeCategory) {
                if (!typeCategory || !Array.isArray(this.drinkStyles)) {
                    return ["-"];
                }
                const category = this.drinkStyles.find(style => style.typeCategory === typeCategory);
                const list = category && Array.isArray(category.drinkStyle) ? [...category.drinkStyle] : [];
                list.unshift("-");
                return list;
            },

            getDrinkCategoryListForItem(index) {
                const item = this.additionalItems[index];
                if (!item) return;
                item.tempTypeCategoryList = this.buildTypeCategoryList(item.tempDrinkType);
                item.tempTypeCategory = "";
                item.tempDrinkStylesList = this.buildDrinkStyleList("");
                item.tempDrinkStyle = "";
            },

            getDrinkStyleListForItem(index) {
                const item = this.additionalItems[index];
                if (!item) return;
                item.tempDrinkStylesList = this.buildDrinkStyleList(item.tempTypeCategory);
                item.tempDrinkStyle = item.tempDrinkStylesList[0] || "";
            },

            addVarietyTagForItem(index) {
                const item = this.additionalItems[index];
                if (!item) return;
                const tag = (item.varietyTagInput || "").trim();
                if (!tag) return;
                if (tag.length > 20) {
                    alert("Each variety tag must be 20 characters or less.");
                    return;
                }
                if (!/^[a-zA-Z0-9\s]+$/.test(tag)) {
                    alert("Variety tags can only contain letters, numbers, and spaces.");
                    return;
                }
                if (item.varietyTagsList.some(t => t.toLowerCase() === tag.toLowerCase())) {
                    alert("This variety tag has already been added.");
                    return;
                }
                item.varietyTagsList.push(tag);
                item.varietyTagInput = "";
            },

            removeVarietyTagForItem(index, tagIndex) {
                const item = this.additionalItems[index];
                if (!item) return;
                item.varietyTagsList.splice(tagIndex, 1);
            },

            handleFileSelectForItem(event, index) {
                const item = this.additionalItems[index];
                if (!item) return;
                const file = event.target.files ? event.target.files[0] : null;
                if (!file) return;
                const reader = new FileReader();
                reader.onload = () => {
                    item.selectedImage = reader.result;
                    item.photo = reader.result;
                };
                reader.readAsDataURL(file);
            },

            // Drag and drop handlers for additional items
            handleDragOverForItem(event, index) {
                event.preventDefault();
                event.stopPropagation();
                const item = this.additionalItems[index];
                if (item) item.isDragging = true;
            },

            handleDragLeaveForItem(event, index) {
                event.preventDefault();
                event.stopPropagation();
                const item = this.additionalItems[index];
                if (item) item.isDragging = false;
            },

            handleDropForItem(event, index) {
                event.preventDefault();
                event.stopPropagation();
                const item = this.additionalItems[index];
                if (!item) return;
                item.isDragging = false;

                const files = event.dataTransfer.files;
                if (files && files.length > 0) {
                    const file = files[0];
                    if (file.type.startsWith('image/')) {
                        const reader = new FileReader();
                        reader.onload = () => {
                            item.selectedImage = reader.result;
                            item.photo = reader.result;
                        };
                        reader.readAsDataURL(file);
                    } else {
                        alert('Please drop an image file.');
                    }
                }
            },

            // Function to validate tags format
            validateTagsFormat(tagsString) {
                // Split by comma and trim each tag
                const tags = tagsString.split(',').map(tag => tag.trim());
                
                // Check each tag
                for (const tag of tags) {
                    // Must start with #
                    if (!tag.startsWith('#')) {
                        return false;
                    }
                    
                    // Must have content after #
                    const content = tag.substring(1);
                    if (!content) {
                        return false;
                    }
                    
                    // Content must only contain letters and numbers
                    if (!/^[a-zA-Z0-9]+$/.test(content)) {
                        return false;
                    }
                }
                
                return true;
            },

            // ============ BULK SUBMISSION METHODS ============

            /**
             * Validate a single item (used for both Item 1 and additional items)
             * @param {Object} item - The item data object
             * @param {String} drinkType - The drink type value
             * @param {String} typeCategory - The type category value
             * @param {String} drinkStyle - The drink style value
             * @param {Boolean} isIndOperator - Whether item has independent bottler
             * @param {Number} itemNum - Item number for error messages (1-indexed)
             * @returns {Boolean} - Whether the item passed validation
             */
            validateSingleItem(item, drinkType, typeCategory, drinkStyle, isIndOperator, itemNum = 1) {
                const prefix = itemNum > 1 ? `Item ${itemNum}: ` : "";
                let hasErrors = false;

                // Validate Bottle Name
                if (!(item.listingName || "").trim()) {
                    this.errors.push(`${prefix}Bottle Name is required.`);
                    hasErrors = true;
                }

                // Validate Drink Type
                if (!(drinkType || "").trim()) {
                    this.errors.push(`${prefix}Drink Type is required.`);
                    hasErrors = true;
                }

                // Validate Independent Bottler Name
                if (isIndOperator === true && !(item.bottler || "").trim()) {
                    this.errors.push(`${prefix}Name of independent bottler is required.`);
                    hasErrors = true;
                }

                // Validate Producer ID
                if (!item.producerID) {
                    this.errors.push(`${prefix}Producer ID is required: Create new producer first!`);
                    hasErrors = true;
                }

                // Validate Bottler ID (if independent bottler)
                if (isIndOperator && !item.bottlerID) {
                    this.errors.push(`${prefix}Bottler ID is required: Create new bottler first!`);
                    hasErrors = true;
                }

                // Validate Country of Origin
                if (!(item.originCountry || "").trim()) {
                    this.errors.push(`${prefix}Country of Origin is required.`);
                    hasErrors = true;
                }

                // Validate Tags format (power mode only)
                if (this.formType === "power" && item.tags && item.tags.trim()) {
                    if (!this.validateTagsFormat(item.tags.trim())) {
                        this.errors.push(`${prefix}Tags must start with # and contain only letters/numbers. Multiple tags must be separated by commas.`);
                        hasErrors = true;
                    }
                }

                // Validate Order field (power mode only)
                if (this.formType === "power" && item.order !== "" && item.order !== null && item.order !== undefined) {
                    const orderValue = Number(item.order);
                    if (!Number.isInteger(orderValue) || orderValue < -1) {
                        this.errors.push(`${prefix}Order must be an integer greater than or equal to -1.`);
                        hasErrors = true;
                    }
                }

                return !hasErrors;
            },

            /**
             * Validate all items for bulk submission
             * Skip validation for confirmed duplicates (existing listings)
             * @returns {Boolean} - Whether all items passed validation
             */
            validateAllItemsForBulk() {
                // Validate Item 1 (main form) - skip if confirmed duplicate
                if (!this.duplicateDetection.isConfirmed) {
                    this.validateSingleItem(
                        this.form,
                        this.tempDrinkType,
                        this.tempTypeCategory,
                        this.tempDrinkStyle,
                        this.indOperator,
                        1
                    );
                }

                // Validate each additional item - skip confirmed duplicates
                for (let i = 0; i < this.additionalItems.length; i++) {
                    const item = this.additionalItems[i];
                    // Skip validation for confirmed duplicates
                    if (item.duplicateDetection?.isConfirmed) {
                        continue;
                    }
                    this.validateSingleItem(
                        item,
                        item.tempDrinkType,
                        item.tempTypeCategory,
                        item.tempDrinkStyle,
                        item.indOperator,
                        i + 2
                    );
                }

                return this.errors.length === 0;
            },

            /**
             * Transform a single item to request payload format (formType="req")
             */
            transformItemToRequestPayload(item, drinkType, typeCategory, drinkStyle, isIndOperator, varietyTags) {
                let abvValue = (item.abv || "").toString().trim();
                if (abvValue) abvValue = abvValue + "%";

                return {
                    sourceLink: (item.sourceLink || "").trim(),
                    listingName: (item.listingName || "").trim(),
                    reviewLink: (item.reviewLink || "").trim(),
                    producerNew: (item.producerNew || "").trim(),
                    bottler: isIndOperator ? (item.bottler || "").trim() : "Original Bottling",
                    originCountry: (item.originCountry || "").trim(),
                    abv: abvValue,
                    age: (item.age || "").toString().trim(),
                    brandRelation: item.brandRelation || null,
                    producerID: item.producerID || "",
                    bottlerID: item.bottlerID || "",
                    photo: item.photo || "",
                    drinkType: (drinkType || "").trim(),
                    typeCategory: (typeCategory || "").trim(),
                    drinkStyle: (drinkStyle || "").trim(),
                    officialDesc: (item.officialDesc || "").trim(),
                    varietyTags: varietyTags && varietyTags.length > 0 ? varietyTags : null
                };
            },

            /**
             * Transform a single item to power payload format (formType="power")
             */
            transformItemToPowerPayload(item, drinkType, typeCategory, drinkStyle, isIndOperator, varietyTags) {
                let abvValue = (item.abv || "").toString().trim();
                if (abvValue) abvValue = abvValue + "%";

                return {
                    sourceLink: (item.sourceLink || "").trim(),
                    listingName: (item.listingName || "").trim(),
                    officialDesc: (item.officialDesc || "").trim(),
                    reviewLink: (item.reviewLink || "").trim(),
                    bottler: isIndOperator ? (item.bottler || "").trim() : "Original Bottling",
                    originCountry: (item.originCountry || "").trim(),
                    abv: abvValue,
                    age: (item.age || "").toString().trim(),
                    producerID: item.producerID,
                    bottlerID: item.bottlerID || "",
                    photo: item.photo || "",
                    drinkType: (drinkType || "").trim(),
                    typeCategory: (typeCategory || "").trim(),
                    drinkStyle: (drinkStyle || "").trim(),
                    tags: (item.tags || "").trim(),
                    order: item.order || null,
                    varietyTags: varietyTags && varietyTags.length > 0 ? varietyTags : null
                };
            },

            /**
             * Build bulk payload for request mode (formType="req")
             * Excludes confirmed duplicates (existing listings) from the payload
             */
            buildBulkRequestPayload() {
                const items = [];

                // Transform Item 1 (main form) - skip if confirmed duplicate
                if (!this.duplicateDetection.isConfirmed) {
                    const item1 = this.transformItemToRequestPayload(
                        this.form,
                        this.tempDrinkType,
                        this.tempTypeCategory,
                        this.tempDrinkStyle,
                        this.indOperator,
                        this.varietyTagsList
                    );
                    // Add userID and submitterType to each item for requestListingBulk
                    item1.userID = this.form["userID"];
                    item1.submitterType = this.userType;
                    item1.originalIndex = 0; // Track original index for result mapping
                    items.push(item1);
                }

                // Transform each additional item - skip confirmed duplicates
                for (let i = 0; i < this.additionalItems.length; i++) {
                    const item = this.additionalItems[i];
                    // Skip confirmed duplicates
                    if (item.duplicateDetection?.isConfirmed) {
                        continue;
                    }
                    const transformedItem = this.transformItemToRequestPayload(
                        item,
                        item.tempDrinkType,
                        item.tempTypeCategory,
                        item.tempDrinkStyle,
                        item.indOperator,
                        item.varietyTagsList
                    );
                    // Add userID and submitterType to each item
                    transformedItem.userID = this.form["userID"];
                    transformedItem.submitterType = this.userType;
                    transformedItem.originalIndex = i + 1; // Track original index for result mapping
                    items.push(transformedItem);
                }

                // Backend requestListingBulk expects 'items' key
                return {
                    items: items
                };
            },

            /**
             * Build bulk payload for power mode (formType="power")
             * Excludes confirmed duplicates (existing listings) from the payload
             */
            buildBulkPowerPayload() {
                const listings = [];

                // Transform Item 1 (main form) - skip if confirmed duplicate
                if (!this.duplicateDetection.isConfirmed) {
                    const item1 = this.transformItemToPowerPayload(
                        this.form,
                        this.tempDrinkType,
                        this.tempTypeCategory,
                        this.tempDrinkStyle,
                        this.indOperator,
                        this.varietyTagsList
                    );
                    item1.originalIndex = 0; // Track original index for result mapping
                    listings.push(item1);
                }

                // Transform each additional item - skip confirmed duplicates
                for (let i = 0; i < this.additionalItems.length; i++) {
                    const item = this.additionalItems[i];
                    // Skip confirmed duplicates
                    if (item.duplicateDetection?.isConfirmed) {
                        continue;
                    }
                    const transformedItem = this.transformItemToPowerPayload(
                        item,
                        item.tempDrinkType,
                        item.tempTypeCategory,
                        item.tempDrinkStyle,
                        item.indOperator,
                        item.varietyTagsList
                    );
                    transformedItem.originalIndex = i + 1; // Track original index for result mapping
                    listings.push(transformedItem);
                }

                return {
                    listings: listings
                };
            },

            /**
             * Submit bulk listings to new bulk endpoint
             */
            async writeBulkListings(submitAPI, payload) {
                this.fillForm = false;
                this.submitForm = true;

                console.log("writeBulkListings called. API:", submitAPI);
                console.log("Bulk payload:", JSON.stringify(payload, null, 2));

                try {
                    const response = await this.$axios.post(submitAPI, payload);
                    const responseCode = response.data.code;

                    console.log("Bulk API response:", response.data);

                    if (responseCode === 201) {
                        this.successSubmission = true;
                        this.submitForm = false;

                        // Clear cache
                        localStorage.removeItem('cachedListingForm');
                        localStorage.removeItem('cachedListingTempDrinkType');
                        localStorage.removeItem('cachedListingTempTypeCategory');
                        localStorage.removeItem('cachedListingTempDrinkStyle');
                        localStorage.removeItem('cachedVarietyTagsList');

                        // Log results summary
                        if (response.data.data && response.data.data.results) {
                            const results = response.data.data.results;
                            const successCount = results.filter(r => r.success).length;
                            const failCount = results.filter(r => !r.success).length;
                            console.log(`Bulk submission complete: ${successCount} succeeded, ${failCount} failed`);
                        }
                    } else {
                        this.errorSubmission = true;
                        this.submitForm = false;
                        this.errorMessage = true;
                    }

                    return response;
                } catch (error) {
                    console.error("Bulk API error:", error.response?.data || error);
                    this.errorSubmission = true;
                    this.submitForm = false;
                    this.errorMessage = true;
                    return error;
                }
            },

            // ============ END BULK SUBMISSION METHODS ============

            // Function to check if user is a power user
            async checkPower() {
                let powerValid = false;

                // Check if user is a producer
                if (localStorage.getItem('88B_accType') == "producer") {
                    powerValid = true;
                }
                // If user is a user, check power
                else if (localStorage.getItem('88B_accType') == "user") {
                    try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUser/` + this.form['userID']);
                        if (Array.isArray(response.data) && response.data.length == 0) {
                            throw "User not found!";
                        }
                        this.types = response.data["modType"];

                        // Check for data deformation - reject if non-array type is found
                        if (Array.isArray(this.types) == false) {
                            this.types = [];
                        }

                        if (this.types.length > 0) {
                            powerValid = true;
                        }
                        if (response.data["isAdmin"] == true) {
                            this.types = [];
                            powerValid = true;
                        }
                    } 
                    catch (error) {
                        console.error(error);
                    }
                }

                // Resolve power check
                if (powerValid) {
                    this.loadData();
                } else {
                    alert("This page is only accessible to producers and power users! Please log in as a producer or power user to access this page.")
                    this.$router.push({path: '/login'});
                }
            },
            
            // Function to load form data
            async loadData(){
               
                console.log('SubmitListingNew.vue loadData started');
                console.log('Form Mode:', this.formMode);
                console.log('Form Type:', this.formType);
                console.log('Listing ID from route:', this.$route.params.listingID);
                console.log('Request ID from route:', this.$route.params.requestID);
                console.log('this.prevListing at start of loadData:', this.prevListing);
                // Clear cache if editing or duplicating
                if (this.formMode === "edit" || this.formMode === "dup") {
                    localStorage.removeItem('cachedListingForm');
                    localStorage.removeItem('cachedListingTempDrinkType');
                    localStorage.removeItem('cachedListingTempTypeCategory');
                    localStorage.removeItem('cachedListingTempDrinkStyle');
                    localStorage.removeItem('cachedVarietyTagsList');
                }

                const cachedForm = localStorage.getItem('cachedListingForm');
                const hasCache = !!cachedForm;

                // Only run when listing detail form is required
                if (this.formType == "power" || this.formMode == "new") {

                    // populate "countries" form data variable
                    try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getCountries`);
                        for (let country of response.data) {
                            this.countries.push(country.originCountry);
                        }
                        this.countries = this.countries.sort((a, b) => {
                            // Priority items at the top
                            if (a === "Multi-Country") return -1;
                            if (b === "Multi-Country") return 1;
                            if (a === "World") return -1;
                            if (b === "World") return 1;
                            // Everything else alphabetically
                            return a.localeCompare(b);
                        });
                    } 
                    catch (error) {
                        console.error(error);
                    }

                    // populate "drinkCategories" + "drinkCategoriesList" form data variable
                    try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getDrinkTypes`);
                        this.drinkCategories = response.data;
                        for (let drink of this.drinkCategories) {
                            // Allow all drink types for form submission (removed moderation filtering)
                            this.drinkCategoriesList.push(drink.drinkType);
                        }
                        // Add a '-' option for no drink type
                        this.drinkCategoriesList.unshift("-");
                        this.drinkCategoriesList = this.drinkCategoriesList.sort();
                    } 
                    catch (error) {
                        console.error(error);
                    }

                    // populate "drinkStyles" + "drinkStylesList" form data variable
                    try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getTypeCategories`);
                        this.drinkStyles = response.data;
                        for (let drink of this.drinkStyles) {
                            // Allow all drink categories for form submission (removed moderation filtering)
                            this.drinkStylesList.push(drink.typeCategory);
                        }
                        // Add a '-' option for no drink category
                        this.drinkStylesList.unshift("-");
                        this.drinkStylesList = this.drinkStylesList.sort();
                    } 
                    catch (error) {
                        console.error("Error fetching data:",error);
                    }

                    if (localStorage.getItem('88B_accType') == "producer") {
                        this.getProducerName();
                    }

                console.log('this.prevListing at cache check:', this.prevListing);
                if (hasCache && !(this.formMode === "edit" || this.formMode === "dup") && !this.prevListing) 
                {
                    console.log("Returning early due to cached form data");
                    // Already restored in mounted()
                    this.fillForm = true; // Ensure form is visible after restoring cache
                    this.dataLoaded = true;
                    return; // Skip the rest of loadData to avoid overwriting cached data
                }


                    // populate "producerList" form data variable
                    // try {
                    //     const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUniqueProducersNamesID`);
                    //     this.producerList = response.data.data;
                    //     this.producerList.sort((a,b)=>{
                    //         return a.producerName.localeCompare(b.producerName)
                    //     })
                    //     this.bottlersList = this.producerList.filter(producer => producer.isIndependentBottler == true);
                    //     // Check if user is a producer
                    //     if (localStorage.getItem('88B_accType') == "producer") {
                    //         this.isProducer = this.producerList.find(producer => producer.id == this.form['userID']).producerName;
                    //         this.form['producerID'] = this.form['userID'];
                    //     }
                    // } 
                    // catch (error) {
                    //     console.error(error);
                    // }

                }
                // Only run when editing listing / proposing edit / reporting duplicate (listingID is present in route params)
                if (this.formMode == "edit" || this.formMode == "dup") {
                    this.form["listingID"] = this.$route.params.listingID;
                    // Add this log:
                    console.log('Before API call to getListing');

                    // Get target listing
                    try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListing/` + this.$route.params.listingID);
                        console.log('API Response for getListing:', response.data);
                       
                        if (Array.isArray(response.data) && response.data.length == 0) {
                            throw "Listing not found!";
                        }
                        this.targetListing = response.data;

                        // Get producer name
                        if (this.targetListing.producerID) {
                            const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUniqueProducersNamesID/dummy/` + this.targetListing.producerID);
                            this.targetListing.producerName = response.data.producerName;
                            this.targetListing.producerID = response.data.id;
                        }

                        // Get bottler ID if bottlerName is present
                        if (this.targetListing.bottlerName) {
                            const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUniqueBottlersNamesID/dummy/` + this.targetListing.bottlerName);
                            this.targetListing.bottlerID = response.data.id;
                        }

                        
                        if (this.targetListing.producerID) {
                            const producerResp = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUniqueProducersNamesID/dummy/` + this.targetListing.producerID);
                            this.producerList = [producerResp.data];
                            this.form['producerNew'] = producerResp.data.producerName;

                            console.log('Fetched producer:', producerResp.data);
                            console.log('producerList:', this.producerList);
                            console.log('form[\'producerNew\']:', this.form['producerNew']);
                        }
                        
                        console.log('Form type in edit/dup:', this.formType);

                        if (this.formType == "power") {
                            this.populateForm(this.targetListing);
                            this.form["officialDesc"] = this.targetListing.officialDesc;

                            // Set producerNew after populateForm to ensure it is not overwritten
                            if (this.producerList.length > 0) {
                                this.form['producerNew'] = this.producerList[0].producerName;
                                this.selectedProducer = this.producerList[0];
                            }
                        }
                    } 
                    catch (error) {
                        console.log('In catch block', error);
                        console.error(error);
                    }

                    // 
                }

                // Only run when route params "requestID" is present (modifying previously submitted request / auto-filling form with request data)
                if (this.prevListing) {
                    // [REQ / POWER NEW] Retrieve previously submitted new listing request data
                    if (this.formMode == "new") {
                        try {
                            console.log('Calling /getData/getRequestListing/ with ID:', this.$route.params.requestID);
                            const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getRequestListing/` + this.$route.params.requestID);
                            
                            if (Array.isArray(response.data) && response.data.length == 0) {
                                throw "Request not found!";
                            }
                            let previousData = await response.data;
                            console.log('Response from /getData/getRequestListing:', previousData);
                            this.checkUserPermissions(previousData);

                            // If user is a producer, check if request producerID is the same as user producerID
                            if (this.isProducer != false) {
                                if (previousData.producerID != this.form['userID']) {
                                    alert("This request is specified for a different producer!");
                                    this.$router.go(-1);
                                }
                            }

                            this.populateForm(previousData);
                            this.form["brandRelation"] = previousData.brandRelation;
                            this.form[""]
                        }
                        catch (error) {
                            console.error(error);
                        }
                    }

                    // [REQ EDIT/DUP + POWER EDIT] Retrieve previously submitted request edit/duplicate data
                    if (this.formMode == "edit" || this.formMode == "dup") {
                        try {
                            const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getRequestEdit/` + this.$route.params.requestID);
                            if (Array.isArray(response.data) && response.data.length == 0) {
                                throw "Request not found!";
                            }
                            let previousData = response.data;
                            this.checkUserPermissions(previousData);

                            // For request mode
                            if (this.formType == "req") {

                                // If set to duplicate mode, but duplicate link is not present, redirect to edit mode
                                if (this.formMode == "dup" && !previousData["duplicateLink"].trim()) {
                                    alert("This request is not a duplicate report!\nRedirecting to edit mode...\nNOTE: Please reload the page after redirection.");
                                    // [RE-ROUTE FLAG] this.$router.replace({path: '/request/modify/edit/' + this.$route.params.listingID + '/' + this.$route.params.requestID});
                                    this.$router.replace({path: '/request/modify/edit/' + this.$route.params.listingID + '/' + this.$route.params.requestID});
                                }

                                // If set to edit mode, but duplicate link is present, redirect to duplicate mode
                                if (this.formMode == "edit" && previousData["duplicateLink"].trim()) {
                                    alert("This request is not a proposed edit!\nRedirecting to duplicate mode...\nNOTE: Please reload the page after redirection.");
                                    // [RE-ROUTE FLAG] this.$router.replace({path: '/request/modify/duplicate/' + this.$route.params.listingID + '/' + this.$route.params.requestID});
                                    this.$router.replace({path: '/request/modify/duplicate/' + this.$route.params.listingID + '/' + this.$route.params.requestID});
                                }

                                // Fill form with previous data
                                this.form['listingID'] = previousData['listingID'];
                                this.form['editDesc'] = previousData['editDesc'];
                                this.form['sourceLink'] = previousData['sourceLink'];
                                this.form['duplicateLink'] = previousData['duplicateLink'];
                                this.form['brandRelation'] = previousData['brandRelation'];
                                
                            }

                            // For actual listing mode
                            if (this.formType == "power") {

                                // Check if retrieved request is for the correct listing
                                if (previousData.listingID != this.$route.params.listingID) {
                                    alert("The linked request is not for the linked listing!\nRemoving request link...");
                                    // [RE-ROUTE FLAG] this.$router.push({path: '/listing/edit/' + this.$route.params.listingID});
                                    this.$router.push({path: '/listing/edit/' + this.$route.params.listingID});
                                }

                                this.modifyRequest = previousData;
                            }
                        }
                        catch (error) {
                            console.error(error);
                        }
                    }
                }

                this.dataLoaded = true;
                this.fillForm = true;
            },

            // Function to get current Producer name and ID
            async getProducerName() {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUniqueProducersNamesID/dummy/` + this.form['userID']);
                    this.isProducer = response.data.producerName;
                    this.form['producerID'] = this.form['userID'];
                } catch (error) {
                    console.error("Error fetching producer name:", error);
                }
            },

            // Debounced function to fetch producer suggestions
            debouncedFetchProducers(query) {
                clearTimeout(this.producerDebounceTimer);
                this.producerDebounceTimer = setTimeout(() => {
                    this.fetchProducerSuggestions(query);
                }, 300); // 300ms debounce delay
            },

            // Function to get producer names dynamically (lazy loading to avoid loading all producers at once)
            async fetchProducerSuggestions(query) {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUniqueProducersNamesID/` + query + '/0');
                    this.producerList = response.data.data;
                } catch (error) {
                    console.error("Error fetching producer suggestions:", error);
                    if (error.response && error.response.status === 404) {
                        this.producerList = ["No producers with this search term found. Please try again with a different term."];
                    } 
                }
            },

            // Debounced function to fetch bottler suggestions
            debouncedFetchBottlers(query) {
                clearTimeout(this.bottlerDebounceTimer);
                this.bottlerDebounceTimer = setTimeout(() => {
                    this.fetchBottlerSuggestions(query);
                }, 300); // 300ms debounce delay
            },

            // Function to get bottler names dynamically (lazy loading to avoid loading all bottlers at once)
            async fetchBottlerSuggestions(query) {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUniqueBottlersNamesID/` + query);
                    this.bottlersList = response.data.data;
                } catch (error) {
                    console.error("Error fetching bottler suggestions:", error);
                }
            },

            // Function to check user editing permissions
            checkUserPermissions(checkData) {
                if (this.formType == "req") {
                    // Check if user is the owner of the request
                    if (checkData.userID != this.form['userID']) {
                        alert("You can only edit requests that you have submitted!");
                        this.$router.go(-1);
                    }

                    // Check if request is already reviewed
                    if (checkData.reviewStatus != false) {
                        alert("Your request is already under review, and can no longer be edited!\nPlease submit a new request!");
                        this.$router.go(-1);
                    }
                }
            },

            // Function to populate form with previous data
            populateForm(previousData) {
                console.log('Populating form with data:', previousData);
               
                this.tempDrinkType = previousData.drinkType;
                console.log('tempDrinkType:', this.tempDrinkType);
                
                this.getDrinkCategoryList();

                // If typeCategory is not present, set it to '-'
                if (previousData.typeCategory == null || previousData.typeCategory == "") {
                    this.tempTypeCategory = "-";
                } else {
                    this.tempTypeCategory = previousData.typeCategory;
                }
                console.log('tempTypeCategory:', this.tempTypeCategory);

                this.getDrinkStyleList();

                // If drinkStyle is not present, set it to '-'
                if (previousData.drinkStyle == null || previousData.drinkStyle == "") {
                    this.tempDrinkStyle = "-";
                } else {
                    this.tempDrinkStyle = previousData.drinkStyle;
                }
                console.log('tempDrinkStyle:', this.tempDrinkStyle);

                this.form["sourceLink"] = previousData.sourceLink;
                console.log('form.sourceLink:', this.form["sourceLink"]);

                this.form["listingName"] = previousData.listingName;
                console.log('form.listingName:', this.form["listingName"]);

                this.form["reviewLink"] = previousData.reviewLink;
                console.log('form.reviewLink:', this.form["reviewLink"]);

                this.form["originCountry"] = previousData.originCountry;
                // Also update country selection states
                this.selectedCountry = previousData.originCountry;
                this.countryInputValue = previousData.originCountry;
                console.log('form.originCountry:', this.form["originCountry"]);

                this.form["producerID"] = previousData.producerID;
                console.log('form.producerID:', this.form["producerID"]);

                this.form["photo"] = previousData.photo;
                console.log('form.photo:', this.form["photo"]);

                // // Check if producerID is blank
                // if (this.form["producerID"] == "" || this.form["producerID"] == null) {
                //     this.form["producerNew"] = previousData.producerNew;
                //     // The code below... is it necessary?
                //     if (this.formMode != "new") {
                //         if (this.formType == "req") {
                //             // In request mode, fill in producerNew
                //             this.form["producerNew"] = previousData.producerNew;
                //             this.tempProducer = "Other";
                //         } else if (this.formType == "power") {
                //             // In actual listing mode, fill in tempProducer
                //             this.tempProducer = previousData.producerNew;
                //         }
                //     }
                // } else {
                    
                // }
                this.form["producerNew"] = previousData.producerNew;
                this.form["producerIdSearch"] = previousData.producerID; // Also populate ID search field
                console.log('form.producerNew:', this.form["producerNew"]);

                // Set selectedProducer if we have producer data
                if (previousData.producerID && previousData.producerNew) {
                    this.selectedProducer = {
                        id: previousData.producerID,
                        producerName: previousData.producerNew,
                        originCountry: previousData.originCountry || ''
                    };
                }

                this.form["officialDesc"] = previousData.officialDesc;
                console.log('form.officialDesc:', this.form["officialDesc"]);

                // If independent bottler, fill in bottler
                if (previousData.bottler != "OB" && previousData.bottler != "Original Bottling" && previousData.bottler != "Original Bottler") {
                    this.indOperator = true;
                    this.form["bottler"] = previousData.bottler;
                    this.form["bottlerID"] = previousData.bottlerID;
                    
                    // Set selectedBottler if we have bottler data
                    if (previousData.bottlerID && previousData.bottler) {
                        this.selectedBottler = {
                            id: previousData.bottlerID,
                            producerName: previousData.bottler,
                            originCountry: previousData.originCountry || ''
                        };
                    }
                } else {
                    this.indOperator = false;
                }
                console.log('indOperator:', this.indOperator);
                console.log('form.bottler:', this.form["bottler"]);
                console.log('form.bottlerID:', this.form["bottlerID"]);

                // If abv has % sign, remove it. Change abv to number.
                if (toString(previousData.abv).includes("%")) {
                    this.form["abv"] = parseFloat(previousData.abv.slice(0, -1));
                } else {
                    this.form["abv"] = parseFloat(previousData.abv);
                }
                console.log('form.abv:', this.form["abv"]);

                // If age has value, change age to number.
                if (previousData.age) {
                    this.form["age"] = parseInt(previousData.age);
                }
                console.log('form.age:', this.form["age"]);

                // Handle tags field - populate if exists
                if (previousData.tags) {
                    this.form["tags"] = previousData.tags;
                } else {
                    this.form["tags"] = "";
                }
                console.log('form.tags:', this.form["tags"]);

                // Handle order field - populate if exists
                if (previousData.order !== null && previousData.order !== undefined) {
                    this.form["order"] = previousData.order;
                } else {
                    this.form["order"] = "";
                }
                console.log('form.order:', this.form["order"]);

                // Handle varietyTags field - populate if exists
                if (previousData.varietyTags && Array.isArray(previousData.varietyTags)) {
                    this.varietyTagsList = [...previousData.varietyTags];
                    this.form["varietyTags"] = previousData.varietyTags;
                } else if (previousData.varietyTags && typeof previousData.varietyTags === 'string') {
                    // Handle case where it comes as a string (shouldn't happen but defensive)
                    try {
                        this.varietyTagsList = JSON.parse(previousData.varietyTags);
                        this.form["varietyTags"] = this.varietyTagsList;
                    } catch (e) {
                        this.varietyTagsList = [];
                        this.form["varietyTags"] = null;
                    }
                } else {
                    this.varietyTagsList = [];
                    this.form["varietyTags"] = null;
                }
                console.log('form.varietyTags:', this.form["varietyTags"]);
                console.log('varietyTagsList:', this.varietyTagsList);
            },

            // Helper function to reset form (by refreshing page)
            reset(){
            // Only clear cache if submission was successful
            if (this.successSubmission == true && this.prevListing == true) {
                localStorage.removeItem('cachedListingForm');
                localStorage.removeItem('cachedListingTempDrinkType');
                localStorage.removeItem('cachedListingTempTypeCategory');
                localStorage.removeItem('cachedListingTempDrinkStyle');
                localStorage.removeItem('cachedVarietyTagsList');
                // Remove requestID router param from current path
                let newPath = this.$route.path.split("/").slice(0, -1).join("/");
                window.location.replace(newPath);
            }
            else if (this.successSubmission == true) {
                localStorage.removeItem('cachedListingForm');
                localStorage.removeItem('cachedListingTempDrinkType');
                localStorage.removeItem('cachedListingTempTypeCategory');
                localStorage.removeItem('cachedListingTempDrinkStyle');
                localStorage.removeItem('cachedVarietyTagsList');
                this.$router.go(0);
            }
            else {
                // On error, just reload the page, keep cache
                this.$router.go(0);
            }
            },

            // Helper function to return to previous page
            goBack() {
                this.$router.go(-1)
            },

            // Helper function to get drink category list for selected drink type ("tempDrinkType")
            getDrinkCategoryList() {
                const found = this.drinkCategories.find(cat => cat.drinkType == this.tempDrinkType);
                
                if (!found) {
                    // If no matching drink type (e.g., '-' selected), reset to empty/default
                    this.tempTypeCategoryList = ["-"];
                    this.tempTypeCategory = "";
                    this.tempDrinkStylesList = ["-"];
                    this.tempDrinkStyle = "";
                    return;
                }
                
                this.tempTypeCategoryList = [...found.typeCategory];

                // Add a '-' option for no drink category
                this.tempTypeCategoryList.unshift("-");
                this.tempTypeCategory = "";
            },

            // Helper function to get drink style list for selected drink category ("tempTypeCategory")
            getDrinkStyleList() {
                const category = this.drinkStyles.find(style => style.typeCategory === this.tempTypeCategory);

                // Debugging check
                if (!category || !category.drinkStyle) { 
                    console.error("Category or drinkStyle is null:", category); 
                }


                this.tempDrinkStylesList = category ? category.drinkStyle : [];  // Ensure it doesn't break

                // Add a '-' option for no drink style
                this.tempDrinkStylesList.unshift("-");

                // If category.drinkStyle is an array, pick first element; otherwise, set to empty string
                this.tempDrinkStyle = (category && category.drinkStyle.length > 0) ? category.drinkStyle[0] : ""; 
            },

            // Helper function to handle file selection for photo
            async handleFileSelect(event) {
                const file = event.target.files[0];
                if (!file) return;
                const reader = new FileReader();
                reader.onload = () => {
                    this.selectedImage = reader.result;
                    this.form["photo"] = reader.result; // full data URL (base64)
                };
                reader.readAsDataURL(file);
            },

            // Drag and drop handlers
            handleDragOver(event) {
                event.preventDefault();
                event.stopPropagation();
                this.isDragging = true;
            },

            handleDragLeave(event) {
                event.preventDefault();
                event.stopPropagation();
                this.isDragging = false;
            },

            handleDrop(event) {
                event.preventDefault();
                event.stopPropagation();
                this.isDragging = false;

                const files = event.dataTransfer.files;
                if (files && files.length > 0) {
                    const file = files[0];
                    // Check if it's an image
                    if (file.type.startsWith('image/')) {
                        const reader = new FileReader();
                        reader.onload = () => {
                            this.selectedImage = reader.result;
                            this.form['photo'] = reader.result;
                        };
                        reader.readAsDataURL(file);
                    } else {
                        alert('Please drop an image file.');
                    }
                }
            },

            // Helper function to get producerID from tempProducer
            getProducerID() {
                // Ensure producerList is an array and input is valid
                if (Array.isArray(this.producerList) && this.form['producerNew']) {
                    const producer = this.producerList.find(
                        item => item?.producerName === this.form['producerNew']
                    );

                    if (producer) {
                        this.form['producerID'] = producer.id;
                    } else {
                        this.form['producerID'] = "";
                    }
                } else {
                    // Log a warning and clear the field to prevent errors
                    console.warn("Producer list or input is invalid:", this.producerList, this.form['producerNew']);
                    this.form['producerID'] = "";
                }
            },

            // Toggle between producer search modes
            toggleProducerSearchMode(itemIndex = null) {
                if (itemIndex !== null) {
                    const item = this.additionalItems[itemIndex];
                    if (!item) return;
                    item.searchByProducerId = !item.searchByProducerId;
                    item.producerIdValidationError = "";
                    item.showProducerDropdown = false;
                    item.showProducerIdDropdown = false;
                } else {
                    this.searchByProducerId = !this.searchByProducerId;
                    this.producerIdValidationError = "";
                    this.showProducerDropdown = false;
                    this.showProducerIdDropdown = false;
                }
                // Clear shared search lists
                this.producerList = [];
                this.producerIdList = [];
            },

            // New methods for drawer-style producer selection
            handleProducerInput(itemIndex = null) {
                // Close all other dropdowns first
                this.closeAllProducerDropdowns(itemIndex);
                
                if (itemIndex !== null) {
                    const item = this.additionalItems[itemIndex];
                    if (!item) return;
                    item.showProducerDropdown = true;
                    item.showProducerIdDropdown = false;
                    
                    if (item.producerNew && item.producerNew.length >= 2) {
                        this.debouncedFetchProducers(item.producerNew);
                    } else {
                        this.producerList = [];
                        item.showProducerDropdown = false;
                    }
                } else {
                    this.showProducerDropdown = true;
                    this.showProducerIdDropdown = false;
                    this.getProducerID();
                    
                    if (this.form['producerNew'] && this.form['producerNew'].length >= 2) {
                        this.debouncedFetchProducers(this.form['producerNew']);
                    } else {
                        this.producerList = [];
                        this.showProducerDropdown = false;
                    }
                }
            },

            // New method for producer ID input
            handleProducerIdInput(itemIndex = null) {
                // Close all other dropdowns first
                this.closeAllProducerDropdowns(itemIndex);
                
                if (itemIndex !== null) {
                    const item = this.additionalItems[itemIndex];
                    if (!item) return;
                    item.showProducerIdDropdown = true;
                    item.showProducerDropdown = false;
                    item.producerIdValidationError = "";
                    
                    const input = item.producerIdSearch;
                    if (input && !/^\d+$/.test(input)) {
                        item.producerIdValidationError = "Producer ID must contain only numeric values.";
                        this.producerIdList = [];
                        item.showProducerIdDropdown = false;
                        return;
                    }
                    
                    if (input && input.length >= 1) {
                        this.debouncedFetchProducerById(input);
                    } else {
                        this.producerIdList = [];
                        item.showProducerIdDropdown = false;
                    }
                } else {
                    this.showProducerIdDropdown = true;
                    this.showProducerDropdown = false;
                    this.producerIdValidationError = "";
                    
                    const input = this.form['producerIdSearch'];
                    if (input && !/^\d+$/.test(input)) {
                        this.producerIdValidationError = "Producer ID must contain only numeric values.";
                        this.producerIdList = [];
                        this.showProducerIdDropdown = false;
                        return;
                    }
                    
                    if (input && input.length >= 1) {
                        this.debouncedFetchProducerById(input);
                    } else {
                        this.producerIdList = [];
                        this.showProducerIdDropdown = false;
                    }
                }
            },

            // Shared method for selecting producer from either search
            selectProducerFromAnySearch(producer, itemIndex = null) {
                if (itemIndex !== null) {
                    const item = this.additionalItems[itemIndex];
                    if (!item) return;
                    item.selectedProducer = producer;
                    item.producerNew = producer.producerName;
                    item.producerIdSearch = producer.id;
                    item.producerID = producer.id;
                    item.showProducerDropdown = false;
                    item.showProducerIdDropdown = false;
                    item.producerIdValidationError = "";
                    // Trigger duplicate check when producer is selected
                    this.triggerDuplicateCheckForItem(itemIndex);
                } else {
                    this.selectedProducer = producer;
                    this.form['producerNew'] = producer.producerName;
                    this.form['producerIdSearch'] = producer.id;
                    this.form['producerID'] = producer.id;
                    this.showProducerDropdown = false;
                    this.showProducerIdDropdown = false;
                    this.producerIdValidationError = "";
                    // Trigger duplicate check when producer is selected
                    this.triggerDuplicateCheck();
                }
                
                // Clear shared search lists
                this.producerList = [];
                this.producerIdList = [];
            },

            // Keep original selectProducer for backward compatibility
            selectProducer(producer) {
                this.selectProducerFromAnySearch(producer);
            },

            clearSelectedProducer(itemIndex = null) {
                if (itemIndex !== null) {
                    const item = this.additionalItems[itemIndex];
                    if (!item) return;
                    item.selectedProducer = {};
                    item.producerNew = '';
                    item.producerIdSearch = '';
                    item.producerID = '';
                    item.showProducerDropdown = false;
                    item.showProducerIdDropdown = false;
                    item.producerIdValidationError = "";
                } else {
                    this.selectedProducer = {};
                    this.form['producerNew'] = '';
                    this.form['producerIdSearch'] = '';
                    this.form['producerID'] = '';
                    this.showProducerDropdown = false;
                    this.showProducerIdDropdown = false;
                    this.producerIdValidationError = "";
                }
                this.producerList = [];
                this.producerIdList = [];
            },

            hideProducerDropdown(itemIndex = null) {
                // Use a timeout to allow click events on dropdown items to fire first
                setTimeout(() => {
                    if (itemIndex !== null) {
                        const item = this.additionalItems[itemIndex];
                        if (item) item.showProducerDropdown = false;
                    } else {
                        this.showProducerDropdown = false;
                    }
                }, 150);
            },

            hideProducerIdDropdown(itemIndex = null) {
                // Use a timeout to allow click events on dropdown items to fire first
                setTimeout(() => {
                    if (itemIndex !== null) {
                        const item = this.additionalItems[itemIndex];
                        if (item) item.showProducerIdDropdown = false;
                    } else {
                        this.showProducerIdDropdown = false;
                    }
                }, 150);
            },

            // Helper to close all producer dropdowns except the one being opened
            closeAllProducerDropdowns(exceptItemIndex = null) {
                // If opening main form dropdown (null), close all item dropdowns
                // If opening an item dropdown (number), close main form and other items
                if (exceptItemIndex !== null) {
                    // Opening an item dropdown - close main form dropdowns
                    this.showProducerDropdown = false;
                    this.showProducerIdDropdown = false;
                }
                // Always close all item dropdowns except the one being opened
                this.additionalItems.forEach((item, idx) => {
                    if (idx !== exceptItemIndex) {
                        item.showProducerDropdown = false;
                        item.showProducerIdDropdown = false;
                    }
                });
            },

            // Debounced function to fetch producer by ID
            debouncedFetchProducerById(producerId) {
                clearTimeout(this.producerIdDebounceTimer);
                this.producerIdDebounceTimer = setTimeout(() => {
                    this.fetchProducerById(producerId);
                }, 300); // 300ms debounce delay
            },

            // Function to get producer by ID using existing endpoint
            async fetchProducerById(producerId) {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUniqueProducersNamesID/dummy/${producerId}`);
                    // The existing endpoint returns single producer data, so wrap it in array for consistency
                    this.producerIdList = [response.data];
                } catch (error) {
                    console.error("Error fetching producer by ID:", error);
                    if (error.response && error.response.status === 404) {
                        this.producerIdValidationError = "No producer found with this ID.";
                        this.producerIdList = [];
                    } else {
                        this.producerIdValidationError = "Error fetching producer. Please try again.";
                        this.producerIdList = [];
                    }
                }
            },

            // New methods for drawer-style bottler selection
            handleBottlerInput() {
                this.showBottlerDropdown = true;
                this.getBottlerID(); // Keep existing logic for ID resolution
                
                // Trigger debounced search if input has at least 2 characters
                if (this.form['bottler'] && this.form['bottler'].length >= 2) {
                    this.debouncedFetchBottlers(this.form['bottler']);
                } else {
                    this.bottlersList = [];
                    this.showBottlerDropdown = false;
                }
            },

            selectBottler(bottler) {
                this.selectedBottler = bottler;
                this.form['bottler'] = bottler.producerName;
                this.form['bottlerID'] = bottler.id;
                this.showBottlerDropdown = false;
                this.bottlersList = [];
                // Trigger duplicate detection when bottler is selected
                this.triggerDuplicateCheck();
            },

            clearSelectedBottler() {
                this.selectedBottler = {};
                this.form['bottler'] = '';
                this.form['bottlerID'] = '';
                this.showBottlerDropdown = false;
                this.bottlersList = [];
            },

            hideBottlerDropdown() {
                // Use a timeout to allow click events on dropdown items to fire first
                setTimeout(() => {
                    this.showBottlerDropdown = false;
                }, 150);
            },

            // Bottler methods for additional items
            handleBottlerInputForItem(idx) {
                const item = this.additionalItems[idx];
                if (!item) return;
                
                // Close all other bottler dropdowns
                this.additionalItems.forEach((it, i) => {
                    if (i !== idx) it.showBottlerDropdown = false;
                });
                this.showBottlerDropdown = false;
                
                item.showBottlerDropdown = true;
                
                if (item.bottler && item.bottler.length >= 2) {
                    this.debouncedFetchBottlers(item.bottler);
                } else {
                    this.bottlersList = [];
                    item.showBottlerDropdown = false;
                }
            },

            selectBottlerForItem(bottler, idx) {
                const item = this.additionalItems[idx];
                if (!item) return;
                item.selectedBottler = bottler;
                item.bottler = bottler.producerName;
                item.bottlerID = bottler.id;
                item.showBottlerDropdown = false;
                this.bottlersList = [];
                // Trigger duplicate check when bottler is selected
                this.triggerDuplicateCheckForItem(idx);
            },

            clearSelectedBottlerForItem(idx) {
                const item = this.additionalItems[idx];
                if (!item) return;
                item.selectedBottler = {};
                item.bottler = '';
                item.bottlerID = '';
                item.showBottlerDropdown = false;
                this.bottlersList = [];
            },

            hideBottlerDropdownForItem(idx) {
                setTimeout(() => {
                    const item = this.additionalItems[idx];
                    if (item) item.showBottlerDropdown = false;
                }, 150);
            },

            // Handle newly created producer from modal
            handleNewProducer(producer) {
                // Add the new producer to producerList
                if (!Array.isArray(this.producerList)) {
                    this.producerList = [];
                }
                this.producerList.push({
                    id: producer.id,
                    producerName: producer.name,
                    isIndependentBottler: producer.isIndependentBottler
                });
                
                // Select the newly created producer
                this.form['producerNew'] = producer.name;
                this.form['producerID'] = producer.id;
                
                // Set as selected producer for the new UI
                this.selectedProducer = {
                    id: producer.id,
                    producerName: producer.name,
                    isIndependentBottler: producer.isIndependentBottler
                };
                
                // Close the modal
                this.showCreateProducerModal = false;
            },


            getBottlerID() {
                // Validate that bottlersList is an array and form.bottler is a non-empty string
                if (Array.isArray(this.bottlersList) && this.form['bottler']) {
                    const bottler = this.bottlersList.find(
                        producer => producer?.producerName === this.form['bottler']
                    );

                    if (bottler) {
                        this.form['bottlerID'] = bottler.id;
                    } else {
                        this.form['bottlerID'] = "";
                    }
                } else {
                    // Handle case where data is not ready or invalid
                    console.warn("Bottler list or bottler input is missing or invalid");
                    this.form['bottlerID'] = "";
                }
            },


            // Function to submit form
            async submitFunction(){
                this.errors = [];
                console.log("submitFunction called. formType:", this.formType, "formMode:", this.formMode, "prevListing:", this.prevListing);

                // ============ BULK SUBMISSION MODE ============
                // Detect bulk mode: more than just Item 1 (i.e., additionalItems.length > 0)
                const isBulkMode = this.additionalItems.length > 0;

                if (isBulkMode && this.formMode === "new") {
                    console.log("Bulk submission mode detected. Item count:", this.additionalItems.length + 1);

                    // Validate all items first
                    if (!this.validateAllItemsForBulk()) {
                        console.log("Bulk validation errors:", this.errors);
                        return "Submission Incomplete";
                    }

                    let submitAPI = "";
                    let bulkPayload = {};

                    if (this.formType === "req") {
                        // Request mode bulk submission
                        submitAPI = `${process.env.VUE_APP_API_URL}/requestListing/requestListingBulk`;
                        bulkPayload = this.buildBulkRequestPayload();
                    } else if (this.formType === "power") {
                        // Power mode bulk submission
                        submitAPI = `${process.env.VUE_APP_API_URL}/createListing/createListingBulk`;
                        bulkPayload = this.buildBulkPowerPayload();
                    } else {
                        alert("There was an issue with bulk submission. Invalid form type!");
                        return "Invalid Mode";
                    }

                    console.log("Bulk submission to:", submitAPI);
                    console.log("Bulk payload:", bulkPayload);
                    this.writeBulkListings(submitAPI, bulkPayload);
                    return;
                }

                // ============ SINGLE-ITEM SUBMISSION MODE (original logic below) ============

                // Form Validation for Edit/Duplicate Request
                if (this.formType == "req" && (this.formMode == "edit" || this.formMode == "dup")) {

                    // Validate Edit Description
                    if (!this.form["editDesc"].trim()) {
                        this.errors.push("Please enter your comments.");
                    }

                    // Validate Duplicate Link
                    if (this.formMode == "dup" && !this.form["duplicateLink"].trim()) {
                        this.errors.push("Please enter the duplicate listing link.");
                    }
                }
                // Form Validation for Listing Details
                else {

                    // Validate Bottle Name
                    if (!this.form["listingName"].trim()) {
                        this.errors.push("Bottle Name is required.");
                    }

                    // Validate Drink Type
                    if (!this.tempDrinkType.trim()) {
                        this.errors.push("Drink Type is required.");
                    }

                    // // Validate Drink Category
                    // if (!this.tempTypeCategory.trim()) {
                    //     this.errors.push("Drink Category is required.");
                    // }


                    // Validate Independent Bottler Name (if OB, will be handled by database writing method)
                    if (this.indOperator === true && !(this.form["bottler"] || "").trim()) {
                        this.errors.push("Name of independent bottler is required.");
                    }

                    // Validate Power User Fields
                    if (this.formType == "power") {
                        // Validate Tags field (must follow #hashtag format with comma separation)
                        if (this.form["tags"] && this.form["tags"].trim()) {
                            const tagsValue = this.form["tags"].trim();
                            if (!this.validateTagsFormat(tagsValue)) {
                                this.errors.push("Tags must start with # and contain only letters/numbers. Multiple tags must be separated by commas (e.g., #whiskyliveparis, #sakefestivalosaka).");
                            }
                        }

                        // Validate Order field (must be integer >= -1 if provided)
                        if (this.form["order"] !== "" && this.form["order"] !== null && this.form["order"] !== undefined) {
                            const orderValue = Number(this.form["order"]);
                            if (!Number.isInteger(orderValue) || orderValue < -1) {
                                this.errors.push("Order must be an integer greater than or equal to -1.");
                            }
                        }
                    }

                    // // Validation ONLY FOR REQUEST - removed requirement for source link 
                    // if (this.formType == "req") {

                    //     // Validate Source Link
                    //     if (!this.form["sourceLink"].trim()) {
                    //         this.errors.push("Link to website or source is required.");
                    //     }

                    //     // Validate Producer Name
                    //     if (this.form['producerID']) {
                    //         // If producerID is blank, check if producerNew is blank
                    //         if (!this.form["producerNew"]) {
                    //             this.errors.push("Producer Name is required.");
                    //         }
                    //     } else {
                    //         // Check if producerNew is blank
                    //         if (!this.form["producerNew"].trim()) {
                    //             this.errors.push("Producer Name is required.");
                    //         }
                    //     }

                    // }

                    // Validation ONLY FOR ACTUAL LISTING - removed the condition that it only applies to power user - now it applies to all.
                    // if (this.formType == "power") {

                        // // Validate Official Description - removed so it doesnt insist you fill in official description
                        // if (!this.form["officialDesc"] || !this.form["officialDesc"].trim()) {
                        //     this.errors.push("Official Description is required.");
                        // }

                        // Validate Producer ID
                        if (!this.form["producerID"]) {
                            this.errors.push("Producer ID is required: Create new producer first!");
                        }

                        // Validate bottler ID
                        if (this.indOperator && !this.form["bottlerID"]) {
                            this.errors.push("Bottler ID is required: Create new bottler first!");
                        }

                        // Validate Country of Origin
                        if (!this.form["originCountry"].trim()) {
                            this.errors.push("Country of Origin is required.");
                        }

                        // // Validate Alcohol Strength (% ABV)
                        // if (!this.form["abv"].toString().trim()) {
                        //     this.errors.push("Alcohol Strength is required.");
                        // }
                        
                    // }
                    
                }

                if (this.errors.length > 0) {
                    console.log("Form validation errors:", this.errors);
                    // If errors, alert user and return
                    return "Submission Incomplete"
                } else {
                    // If no errors, pass corresponding API into database writing method
                    let submitAPI = ""
                    let submitData = {}
                    
                    // Request Listing Mode
                    if (this.formType == "req") {

                        // Request Creation Mode
                        if (this.formMode == "new") {
                            submitAPI = `${process.env.VUE_APP_API_URL}/requestListing/requestListing`

                            if (this.tempDrinkStyle == null) {
                                console.error("ERROR: tempDrinkStyle is null or undefined!");
                            }
                            
                            submitData = {
                                "sourceLink": (this.form["sourceLink"] || "").trim(),
                                "listingName": (this.form["listingName"] || "").trim(),
                                "reviewLink": (this.form["reviewLink"] || "").trim(),
                                "producerNew": (this.form["producerNew"] || "").trim(),
                                "bottler": (this.form["bottler"] || "").trim(),
                                "originCountry": (this.form["originCountry"] || "").trim(),
                                "abv": (this.form["abv"] || "").toString().trim(),
                                "age": (this.form["age"] || "").toString().trim(),
                                "brandRelation": this.form["brandRelation"],

                                "userID": this.form["userID"],
                                "submitterType": this.userType, // Include submitter type from localStorage
                                "producerID": this.form["producerID"],
                                "bottlerID": this.form["bottlerID"],
                                "photo": this.form["photo"],

                                "drinkType": (this.tempDrinkType || "").trim(),
                                "typeCategory": (this.tempTypeCategory || "").trim(),
                                "reviewStatus": false,
                                "drinkStyle": (this.tempDrinkStyle || "").trim(),
                                "officialDesc": (this.form["officialDesc"] || "").trim(),
                                "varietyTags": this.form["varietyTags"] || null,
                            }
                            
                            // Add this log before the API call:
                            console.log("Request Creation Mode Submitting to API:", submitAPI);
                            console.log("Payload being sent:", submitData);
                            
                            if (this.prevListing) {
                                submitAPI = `${process.env.VUE_APP_API_URL}/requestListing/requestListingModify/` + this.$route.params.requestID
                                console.log("prevListing is true, switching to modify endpoint:", submitAPI);
                            }
                        }

                        // Request Edit / Duplicate Mode
                        else if (this.formMode == "edit" || this.formMode == "dup") {
                            submitAPI = `${process.env.VUE_APP_API_URL}/requestListing/requestEdits`
                            submitData = {
                                "editDesc": (this.form["editDesc"] || "").trim(),
                                "sourceLink": (this.form["sourceLink"] || "").trim(),
                                "duplicateLink": (this.form["duplicateLink"] || "").trim(),
                                "brandRelation": this.form["brandRelation"],

                                "userID": this.form["userID"],
                                "submitterType": this.userType, // Include submitter type from localStorage
                                "listingID": this.form["listingID"],
                                "reviewStatus": false,
                            }

                            if (this.prevListing) {
                                submitAPI = `${process.env.VUE_APP_API_URL}/requestListing/requestEditsModify/` + this.$route.params.requestID;
                            }
                        }

                        else {
                            // Catching statement for invalid mode
                            alert("There was an issue with submission. Try to reopen the page after saving your inputs!")
                            return "Invalid Mode"
                        }

                    } else if (this.formType == "power") {
                        // Debugging each form field before trimming

                        submitData = {
                            "sourceLink": (this.form["sourceLink"] || "").trim(),
                            "listingName": (this.form["listingName"] || "").trim(),
                            "officialDesc": (this.form["officialDesc"] || "").trim(),
                            "reviewLink": (this.form["reviewLink"] || "").trim(),
                            "bottler": (this.form["bottler"] || "").trim(),
                            "originCountry": (this.form["originCountry"] || "").trim(),
                            "abv": (this.form["abv"] || "").toString().trim(),
                            "age": (this.form["age"] || "").toString().trim(),
                            
                            "producerID": this.form["producerID"],
                            "bottlerID": this.form["bottlerID"],
                            "photo": this.form["photo"],

                            "drinkType": (this.tempDrinkType || "").trim(),
                            "typeCategory": (this.tempTypeCategory || "").trim(),
                            "drinkStyle": (this.tempDrinkStyle || "").trim(),
                            "tags": (this.form["tags"] || "").trim(),
                            "order": this.form["order"] || null,
                            "varietyTags": this.form["varietyTags"] || null,
                        }

                        // Listing Creation Mode
                        if (this.formMode == "new") {
                            submitAPI = `${process.env.VUE_APP_API_URL}/createListing/createListing`

                            if (this.$route.params.requestID && this.$route.params.requestID !== "") {
                                submitAPI += `?requestId=${this.$route.params.requestID}`
                            }
                        }

                        // Listing Edit Mode
                        else if (this.formMode == "edit") {
                            submitAPI = `${process.env.VUE_APP_API_URL}/editListing/updateListing/` + this.$route.params.listingID
                        }

                        else {
                            // Catching statement for invalid mode
                            alert("There was an issue with submission. Try to reopen the page after saving your inputs!")
                            return "Invalid Mode"
                        }

                    } else {
                        // Catching statement for invalid mode
                        alert("There was an issue with submission. Try to reopen the page after saving your inputs!")
                        return "Invalid Mode"
                    }

                    if (this.formType == "power" || this.formMode == "new") {
                        // If not independent bottler, set bottler to "OB"
                        if (this.indOperator == false) {
                            submitData["bottler"] = "Original Bottling"
                        }

                        // If abv has value, add % sign
                        if (submitData["abv"]) {
                            submitData["abv"] = submitData["abv"].toString() + "%"
                        }
                    }

                    // Update request status
                    if (this.prevListing && this.formType == "power") {
                        this.updateRequestStatus("approve")
                    }
                    console.log("Calling writeListing with:", submitAPI, submitData);
                    this.writeListing(submitAPI, submitData)
                }
            },

            // Function to write listing to database
            async writeListing(submitAPI, submitData) {

                this.fillForm = false; // Hide form
                this.submitForm = true; // Display submission in progress message
                let responseCode = "";

                console.log("writeListing called. API:", submitAPI);
                console.log("Payload being sent:", submitData);

                let response;
                await this.$axios.post(submitAPI, submitData)
                .then((res)=>{
                    response = res;
                    responseCode = res.data.code
                    console.log("API response received:", res.data);
                })
                .catch((error)=>{
                    responseCode = error.response.data.code
                    console.error("API error response:", error.response.data);

                    if (responseCode === 201 && response && response.data.badgeAwarded) {
                        this.earnedBadges = [response.data.badgeAwarded];
                        this.showBadgePopup = true;
                    }
                });

                // [Replace with Backend Fix] Response Code Transformation for Edit Listing
                if (this.formType == "power" && this.formMode == "edit") {
                    if (responseCode == 200) {
                        responseCode = 201
                    }
                    if (responseCode == 420 || responseCode == 440) {
                        responseCode = 400
                    }
                }

                // Temporarily treat duplicate entries (400) as success for new listings
                if (responseCode == 400 && this.formMode == "new") {
                    responseCode = 201; // Force success
                }
                
                if (responseCode == 201) {
                    this.successSubmission = true; // Display success message
                    this.submitForm = false; // Hide submission in progress message
                    localStorage.removeItem('cachedListingForm');
                    localStorage.removeItem('cachedListingTempDrinkType');
                    localStorage.removeItem('cachedListingTempTypeCategory');
                    localStorage.removeItem('cachedListingTempDrinkStyle');
                    
                    // Redirect to new listing page for users creating new listings
                    if (this.formMode === "new" && response && response.data && response.data.data) {
                        const responseData = response.data.data;
                        let listingId = null;
                        let listingName = null;
                        
                        // For power users (direct listing creation)
                        if (this.formType === "power" && responseData.id && responseData.listingName) {
                            listingId = responseData.id;
                            listingName = responseData.listingName;
                        }
                        // For regular users (request listings with auto-approval)
                        else if (this.formType === "req" && responseData.listingId && responseData.listingName && responseData.autoApproved) {
                            listingId = responseData.listingId;
                            listingName = responseData.listingName;
                        }
                        
                        // Redirect if we have both listing ID and name
                        if (listingId && listingName) {
                            // Create URL-safe slug (same logic as backend)
                            const slug = listingName.toLowerCase().replace(/[^a-z0-9]+/g, '');
                            const listingUrl = `/listing/view/${listingId}/${slug}`;
                            
                            console.log("Redirecting to new listing:", listingUrl);
                            this.$router.push(listingUrl);
                            return response; // Early return to avoid showing success message
                        }
                    }
                } else {
                    this.errorSubmission = true; // Display error message
                    this.submitForm = false; // Hide submission in progress message
                    
                    if (responseCode == 400) {
                        if (this.formMode == "new") {
                            this.duplicateEntry = true // Display duplicate entry message
                        } else {
                            this.invalidListing = true // Display invalid listing error message
                        }
                    } else if (responseCode == 410) {
                        this.duplicateEntry = true // Display duplicate entry message
                    } else {
                        this.errorMessage = true // Display generic error message
                    }
                }
                console.log("writeListing finished. responseCode:", responseCode);
                return response
            },

            // Function to update request status
            async updateRequestStatus(status) {

                let responseCode = "";
                let submitAPI = `${process.env.VUE_APP_API_URL}/requestListing/requestReviewStatus/` + this.$route.params.requestID;
                let submitData = {};

                // Set up submission data
                if (this.formMode == "new") {
                    submitData = {
                        "targetCollection": "requestListings",
                        "reviewStatus": false,
                    }
                }
                else if (this.formMode == "edit") {
                    submitData = {
                        "targetCollection": "requestEdits",
                        "reviewStatus": false,
                    }
                }
                else {
                    // Catching statement for invalid mode
                    alert("There was an issue with submission. Try to reopen the page after saving your inputs!")
                    return "Invalid Mode"
                }

                // Set new review status
                if (status == "reject") {

                    this.fillForm = false; // Hide form
                    this.submitForm = true; // Display submission in progress message
                    submitData["reviewStatus"] = null;

                }
                else if (status == "approve") {
                    submitData["reviewStatus"] = true;
                }

                const response = await this.$axios.post(submitAPI, submitData)
                .then((response)=>{
                    responseCode = response.data.code
                })
                .catch((error)=>{
                    responseCode = error.response.data.code
                });
                
                if (responseCode == 201) {
                    if (status == "reject") {
                        this.successSubmission = true; // Display success message
                        this.requestRemoval = true; // Display request removal message
                        this.submitForm = false; // Hide submission in progress message
                    }
                } else {
                    this.errorSubmission = true; // Display error message
                    this.fillForm = false; // Hide form
                    this.submitForm = false; // Hide submission in progress message
                    this.errorMessage = true // Display generic error message
                }
                return response

            },

            closeBadgePopup() {
                this.showBadgePopup = false;
                this.earnedBadges = [];
            },

            // Country Drawer Methods
            openCountryDrawer() {
                this.showCountryDrawer = true;
                this.filteredCountries = [...this.countries];
                this.$nextTick(() => {
                    // Add click outside listener
                    document.addEventListener('click', this.handleClickOutside);
                });
            },

            closeCountryDrawer() {
                this.showCountryDrawer = false;
                this.filteredCountries = [];
                // Remove click outside listener
                document.removeEventListener('click', this.handleClickOutside);
            },

            handleCountryInput() {
                // Open dropdown when user starts typing
                if (!this.showCountryDrawer) {
                    this.openCountryDrawer();
                }
                // Filter countries based on input
                this.filterCountries();
            },

            filterCountries() {
                const searchTerm = this.countryInputValue.toLowerCase();
                this.filteredCountries = this.countries.filter(country =>
                    country.toLowerCase().includes(searchTerm)
                );
            },

            handleClickOutside(event) {
                // Check if click was outside the dropdown and input field
                const dropdown = event.target.closest('.country-dropdown');
                const input = event.target.closest('.input-group');
                if (!dropdown && !input) {
                    this.closeCountryDrawer();
                }
            },

            selectCountry(countryName) {
                this.selectedCountry = countryName;
                this.countryInputValue = countryName; // Update the input field with selected country
                this.closeCountryDrawer();
            },

            // Photo handling methods
            clearPhoto() {
                this.selectedImage = '';
                this.form['photo'] = '';
                // Reset the file input
                const fileInput = document.getElementById('formFile');
                if (fileInput) {
                    fileInput.value = '';
                }
            },

            resetToDefaultPhoto() {
                this.selectedImage = '';
                this.form['photo'] = '';
                // Reset the file input
                const fileInput = document.getElementById('formFile');
                if (fileInput) {
                    fileInput.value = '';
                }
            },

            // ============ DUPLICATE DETECTION METHODS ============

            /**
             * Check if all required fields are filled for duplicate detection (main form - Item 1)
             * Required: Producer confirmed, Drink Name (3+ chars), Drink Type, Country
             * If indOperator is true, also need Bottler confirmed
             */
            canTriggerDuplicateCheck() {
                // Producer must be confirmed (has ID from selection)
                if (!this.selectedProducer || !this.selectedProducer.id) return false;
                
                // Drink name must be at least 3 characters
                if (!this.form['listingName'] || this.form['listingName'].trim().length < 3) return false;
                
                // Drink type must be selected
                if (!this.tempDrinkType) return false;
                
                // Country must be selected
                if (!this.form['originCountry']) return false;
                
                // If independent bottler is checked, bottler must be confirmed
                if (this.indOperator && (!this.selectedBottler || !this.selectedBottler.id)) return false;
                
                return true;
            },

            /**
             * Check if all required fields are filled for duplicate detection (additional item)
             */
            canTriggerDuplicateCheckForItem(idx) {
                const item = this.additionalItems[idx];
                if (!item) return false;
                
                // Producer must be confirmed
                if (!item.selectedProducer || !item.selectedProducer.id) return false;
                
                // Drink name must be at least 3 characters
                if (!item.listingName || item.listingName.trim().length < 3) return false;
                
                // Drink type must be selected
                if (!item.tempDrinkType) return false;
                
                // Country must be selected
                if (!item.originCountry) return false;
                
                // If independent bottler is checked, bottler must be confirmed
                if (item.indOperator && (!item.selectedBottler || !item.selectedBottler.id)) return false;
                
                return true;
            },

            /**
             * Trigger duplicate detection for main form (Item 1) with debounce
             */
            triggerDuplicateCheck() {
                // Don't trigger if already confirmed a duplicate
                if (this.duplicateDetection.isConfirmed) return;
                
                // Clear previous timer
                if (this.duplicateDebounceTimer) {
                    clearTimeout(this.duplicateDebounceTimer);
                }
                
                // Check if all required fields are filled
                if (!this.canTriggerDuplicateCheck()) {
                    // Clear matches if requirements not met
                    this.duplicateDetection.matches = [];
                    return;
                }
                
                // Set debounce timer (2 seconds)
                this.duplicateDebounceTimer = setTimeout(() => {
                    this.fetchDuplicateSuggestions();
                }, 2000);
            },

            /**
             * Trigger duplicate detection for additional item with debounce
             */
            triggerDuplicateCheckForItem(idx) {
                const item = this.additionalItems[idx];
                if (!item) return;
                
                // Don't trigger if already confirmed a duplicate
                if (item.duplicateDetection.isConfirmed) return;
                
                // Clear previous timer
                if (item.duplicateDebounceTimer) {
                    clearTimeout(item.duplicateDebounceTimer);
                }
                
                // Check if all required fields are filled
                if (!this.canTriggerDuplicateCheckForItem(idx)) {
                    item.duplicateDetection.matches = [];
                    return;
                }
                
                // Set debounce timer (2 seconds)
                item.duplicateDebounceTimer = setTimeout(() => {
                    this.fetchDuplicateSuggestionsForItem(idx);
                }, 2000);
            },

            /**
             * Fetch duplicate suggestions from backend for main form (Item 1)
             */
            async fetchDuplicateSuggestions() {
                this.duplicateDetection.isLoading = true;
                
                try {
                    // Build query params matching backend expectations
                    const params = new URLSearchParams({
                        listingName: this.form['listingName'].trim(),
                        producerId: this.selectedProducer.id.toString(),
                        producerName: this.selectedProducer.producerName || this.form['producerNew'],
                        drinkType: this.tempDrinkType,
                        originCountry: this.form['originCountry'],
                    });
                    
                    // Add optional bottler params if applicable
                    if (this.indOperator && this.selectedBottler && this.selectedBottler.id) {
                        params.append('bottlerId', this.selectedBottler.id.toString());
                        params.append('bottlerName', this.selectedBottler.producerName || this.form['bottler']);
                    }
                    
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/detectPotentialDuplicateListings?${params.toString()}`);
                    
                    if (response.data && response.data.data && response.data.data.matches) {
                        this.duplicateDetection.matches = response.data.data.matches;
                        // Auto-expand if matches found
                        if (response.data.data.matches.length > 0) {
                            this.duplicateDetection.isCollapsed = false;
                        }
                    } else {
                        this.duplicateDetection.matches = [];
                    }
                } catch (error) {
                    console.error('Error fetching duplicate suggestions:', error);
                    this.duplicateDetection.matches = [];
                } finally {
                    this.duplicateDetection.isLoading = false;
                }
            },

            /**
             * Fetch duplicate suggestions from backend for additional item
             */
            async fetchDuplicateSuggestionsForItem(idx) {
                const item = this.additionalItems[idx];
                if (!item) return;
                
                item.duplicateDetection.isLoading = true;
                
                try {
                    // Build query params matching backend expectations
                    const params = new URLSearchParams({
                        listingName: item.listingName.trim(),
                        producerId: item.selectedProducer.id.toString(),
                        producerName: item.selectedProducer.producerName || item.producerNew,
                        drinkType: item.tempDrinkType,
                        originCountry: item.originCountry,
                    });
                    
                    // Add optional bottler params if applicable
                    if (item.indOperator && item.selectedBottler && item.selectedBottler.id) {
                        params.append('bottlerId', item.selectedBottler.id.toString());
                        params.append('bottlerName', item.selectedBottler.producerName || item.bottler);
                    }
                    
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/detectPotentialDuplicateListings?${params.toString()}`);
                    
                    if (response.data && response.data.data && response.data.data.matches) {
                        item.duplicateDetection.matches = response.data.data.matches;
                        // Auto-expand if matches found
                        if (response.data.data.matches.length > 0) {
                            item.duplicateDetection.isCollapsed = false;
                        }
                    } else {
                        item.duplicateDetection.matches = [];
                    }
                } catch (error) {
                    console.error('Error fetching duplicate suggestions for item:', error);
                    item.duplicateDetection.matches = [];
                } finally {
                    item.duplicateDetection.isLoading = false;
                }
            },

            /**
             * Confirm a duplicate match for main form (Item 1)
             * Pre-fills all form fields and locks them
             */
            confirmDuplicate(match) {
                // Store the confirmed duplicate
                this.duplicateDetection.confirmedDuplicate = match;
                this.duplicateDetection.isConfirmed = true;
                
                // Pre-fill all form fields from the matched listing
                this.form['listingName'] = match.listingName || '';
                this.tempDrinkType = match.drinkType || '';
                this.getDrinkCategoryList();
                this.tempTypeCategory = match.typeCategory || '-';
                this.getDrinkStyleList();
                this.form['originCountry'] = match.originCountry || '';
                this.selectedCountry = match.originCountry || '';
                this.countryInputValue = match.originCountry || '';
                
                // Handle ABV (remove % sign if present)
                if (match.abv !== null && match.abv !== undefined) {
                    this.form['abv'] = match.abv;
                }
                
                // Handle age
                if (match.age !== null && match.age !== undefined) {
                    this.form['age'] = match.age;
                }
                
                // Handle photo
                if (match.photo) {
                    this.form['photo'] = match.photo;
                }
                
                // Handle producer
                if (match.producerId && match.producerName) {
                    this.form['producerID'] = match.producerId;
                    this.form['producerNew'] = match.producerName;
                    this.selectedProducer = {
                        id: match.producerId,
                        producerName: match.producerName
                    };
                }
                
                // Handle bottler
                if (match.bottlerId && match.bottlerName) {
                    this.indOperator = true;
                    this.form['bottlerID'] = match.bottlerId;
                    this.form['bottler'] = match.bottlerName;
                    this.selectedBottler = {
                        id: match.bottlerId,
                        producerName: match.bottlerName
                    };
                } else {
                    this.indOperator = false;
                    this.form['bottlerID'] = '';
                    this.form['bottler'] = '';
                    this.selectedBottler = {};
                }
                
                // Store the listing ID for reference
                this.form['listingID'] = match.id;
            },

            /**
             * Confirm a duplicate match for additional item
             * Pre-fills all item fields and locks them
             */
            confirmDuplicateForItem(idx, match) {
                const item = this.additionalItems[idx];
                if (!item) return;
                
                // Store the confirmed duplicate
                item.duplicateDetection.confirmedDuplicate = match;
                item.duplicateDetection.isConfirmed = true;
                
                // Pre-fill all item fields from the matched listing
                item.listingName = match.listingName || '';
                item.tempDrinkType = match.drinkType || '';
                item.tempTypeCategoryList = this.buildTypeCategoryList(match.drinkType);
                item.tempTypeCategory = match.typeCategory || '-';
                item.tempDrinkStylesList = this.buildDrinkStyleList(match.typeCategory);
                item.originCountry = match.originCountry || '';
                
                // Handle ABV
                if (match.abv !== null && match.abv !== undefined) {
                    item.abv = match.abv;
                }
                
                // Handle age
                if (match.age !== null && match.age !== undefined) {
                    item.age = match.age;
                }
                
                // Handle photo
                if (match.photo) {
                    item.photo = match.photo;
                }
                
                // Handle producer
                if (match.producerId && match.producerName) {
                    item.producerID = match.producerId;
                    item.producerNew = match.producerName;
                    item.selectedProducer = {
                        id: match.producerId,
                        producerName: match.producerName
                    };
                }
                
                // Handle bottler
                if (match.bottlerId && match.bottlerName) {
                    item.indOperator = true;
                    item.bottlerID = match.bottlerId;
                    item.bottler = match.bottlerName;
                    item.selectedBottler = {
                        id: match.bottlerId,
                        producerName: match.bottlerName
                    };
                } else {
                    item.indOperator = false;
                    item.bottlerID = '';
                    item.bottler = '';
                    item.selectedBottler = {};
                }
                
                // Store the listing ID reference
                item.confirmedListingId = match.id;
            },

            /**
             * Undo duplicate confirmation for main form (Item 1)
             * Re-enables editing of all fields
             */
            undoDuplicateConfirmation() {
                this.duplicateDetection.confirmedDuplicate = null;
                this.duplicateDetection.isConfirmed = false;
                this.form['listingID'] = '';
                // Matches are preserved so user can select again if needed
            },

            /**
             * Undo duplicate confirmation for additional item
             * Re-enables editing of all fields
             */
            undoDuplicateConfirmationForItem(idx) {
                const item = this.additionalItems[idx];
                if (!item) return;
                
                item.duplicateDetection.confirmedDuplicate = null;
                item.duplicateDetection.isConfirmed = false;
                item.confirmedListingId = null;
                // Matches are preserved so user can select again if needed
            },

            /**
             * Toggle collapse state of duplicate detection card for main form
             */
            toggleDuplicateCollapse() {
                this.duplicateDetection.isCollapsed = !this.duplicateDetection.isCollapsed;
            },

            /**
             * Toggle collapse state of duplicate detection card for additional item
             */
            toggleDuplicateCollapseForItem(idx) {
                const item = this.additionalItems[idx];
                if (!item) return;
                item.duplicateDetection.isCollapsed = !item.duplicateDetection.isCollapsed;
            },

            /**
             * Open listing in new tab
             */
            openListingInNewTab(listingId, listingName) {
                const slug = this.slugify(listingName);
                const url = `/listing/view/${listingId}/${slug}`;
                window.open(url, '_blank');
            },

            // ============ END DUPLICATE DETECTION METHODS ============
        }
    }
</script>

<style scoped>
/* Staging Modal Styles */
.staging-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.6);
    z-index: 1060;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.staging-modal-content {
    background: white;
    border-radius: 12px;
    width: 95%;
    max-width: 1400px;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.staging-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 24px;
    border-bottom: 1px solid #dee2e6;
    flex-shrink: 0;
}

.staging-modal-body {
    padding: 20px 24px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
}

.staging-table-wrapper {
    overflow: auto;
    flex: 1;
    border: 1px solid #dee2e6;
    border-radius: 8px;
}

.staging-table {
    margin-bottom: 0;
    font-size: 0.85rem;
    white-space: nowrap;
}

.staging-table thead th {
    position: sticky;
    top: 0;
    background: #f8f9fa;
    z-index: 10;
    border-bottom: 2px solid #dee2e6;
    padding: 10px 12px;
    font-weight: 600;
}

.staging-table td {
    padding: 8px 12px;
    vertical-align: middle;
}

/* Submission result row highlighting */
.staging-table tr.row-success {
    background-color: rgba(25, 135, 84, 0.1) !important;
}

.staging-table tr.row-success:hover {
    background-color: rgba(25, 135, 84, 0.15) !important;
}

.staging-table tr.row-error {
    background-color: rgba(220, 53, 69, 0.1) !important;
}

.staging-table tr.row-error:hover {
    background-color: rgba(220, 53, 69, 0.15) !important;
}

.staging-table tr.row-skipped {
    background-color: rgba(108, 117, 125, 0.1) !important;
}

.staging-table tr.row-skipped:hover {
    background-color: rgba(108, 117, 125, 0.15) !important;
}

.staging-table tr.row-pending {
    background-color: transparent;
}

/* Status badges in table */
.staging-table .badge {
    font-size: 0.85em;
    padding: 6px 10px;
}

.staging-table .badge.bg-danger {
    max-width: 180px;
    word-wrap: break-word;
}

/* Clickable links inside badges */
.staging-table .badge a {
    color: inherit;
    text-decoration: underline;
}

.staging-table .badge a:hover {
    opacity: 0.8;
}

.staging-thumbnail {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 4px;
    border: 1px solid #dee2e6;
}

.text-truncate-cell {
    max-width: 200px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.staging-modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding: 16px 24px;
    border-top: 1px solid #dee2e6;
    flex-shrink: 0;
}

.sticky-header {
    position: sticky;
    top: 0;
    z-index: 10;
}

/* Bulk mode checkbox checked state */
.bulk-mode-checkbox:checked {
    background-color: #198754 !important;
    border-color: #198754 !important;
}
/* Country Dropdown Styles */
.country-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 1050;
    max-height: 300px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.country-dropdown-body {
    flex: 1;
    overflow-y: auto;
    max-height: 240px;
}

.country-item {
    padding: 10px 12px;
    cursor: pointer;
    transition: background-color 0.15s ease;
    border-bottom: 1px solid #f5f5f5;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.country-item:hover {
    background-color: #f8f9fa;
}

.country-item:last-child {
    border-bottom: none;
}

.country-name {
    font-size: 14px;
    color: #333;
}

.check-icon {
    color: #28a745;
    flex-shrink: 0;
    margin-left: 8px;
}

.no-results {
    padding: 15px 12px;
    text-align: center;
    color: #666;
    font-style: italic;
    font-size: 14px;
}

/* Photo Upload Styles */
.upload-label { 
    display: block; 
    width: 100%; 
    cursor: pointer;
}

.mobile-review-svg-button {
    width: 100%;
    aspect-ratio: 1/1;
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.2s ease;
    padding: 0px;
}

.mobile-review-svg-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.photo-dropzone {
    display: flex; 
    align-items: center; 
    justify-content: center;
    height: 100%;
    border: 2px dashed #cfcfcf; 
    background: #fafafa; 
    cursor: pointer;
    transition: all 0.2s ease;
}

.photo-dropzone:hover {
    border-color: #007bff;
    background: #f0f8ff;
}

.photo-dropzone.dragging {
    border-color: #007bff;
    background: #e3f2fd;
    border-width: 3px;
    transform: scale(1.02);
}

.photo-dropzone.dragging {
    border-color: #007bff;
    background: #e3f2fd;
    border-width: 3px;
    transform: scale(1.02);
}

.review-preview-photo {
    width: 100%; 
    height: 100%; 
    object-fit: cover; 
    display: block;
    border-radius: 12px;
}

/* Responsive adjustments */
@media (max-width: 767px) {
    .country-dropdown {
        max-height: 250px;
    }
    
    .country-dropdown-body {
        max-height: 190px;
    }
}

/* ============ DUPLICATE DETECTION STYLES ============ */
.duplicate-detection-card {
    border: 2px solid #28a745;
    border-radius: 8px;
    overflow: hidden;
    background: #f8fff9;
    box-shadow: 0 2px 8px rgba(40, 167, 69, 0.15);
}

.duplicate-detection-card.confirmed {
    border-color: #198754;
    background: #d1e7dd;
}

.duplicate-detection-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
    color: white;
    cursor: pointer;
    transition: background 0.2s ease;
}

.duplicate-detection-header:hover {
    background: linear-gradient(135deg, #218838 0%, #1abc9c 100%);
}

.duplicate-detection-card.confirmed .duplicate-detection-header {
    background: linear-gradient(135deg, #198754 0%, #157347 100%);
}

.duplicate-icon {
    font-size: 18px;
}

.duplicate-detection-body {
    max-height: 320px;
    overflow-y: auto;
    padding: 12px 16px;
}

.duplicate-matches-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.duplicate-match-item {
    padding: 12px;
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.duplicate-match-item:hover {
    border-color: #28a745;
    box-shadow: 0 2px 8px rgba(40, 167, 69, 0.1);
}

.duplicate-thumbnail {
    width: 50px;
    height: 50px;
    object-fit: cover;
    border-radius: 6px;
    border: 1px solid #e0e0e0;
}

.duplicate-thumbnail-placeholder {
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f0f0f0;
    border-radius: 6px;
    font-size: 20px;
}

.confirmed-duplicate-info {
    background: white;
    padding: 12px;
    border-radius: 8px;
}

/* Disabled state for form fields when duplicate is confirmed */
.duplicate-confirmed-field {
    background-color: #e9ecef !important;
    cursor: not-allowed;
    opacity: 0.8;
}

.duplicate-confirmed-field:focus {
    background-color: #e9ecef !important;
}
/* ============ END DUPLICATE DETECTION STYLES ============ */
</style>