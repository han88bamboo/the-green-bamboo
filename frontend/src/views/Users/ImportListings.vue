<!-- Bulk Import Listings page - 2-step staging process for CSV import -->
<!-- Updated: Stage 4 - Accessible to users, producers, and venues (not admin-only) -->

<template>
    <NavBar />
    
    <!-- Display when data is still loading -->
    <div class="text-info-emphasis fst-italic fw-bold fs-5 pt-5" v-if="dataLoaded == false">
        <span>Loading page, please wait...</span>
        <br><br>
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>

    <!-- Display when staging data is loading -->
    <div class="text-info-emphasis fst-italic fw-bold fs-5 pt-5" v-if="stagingInProgress">
        <span>Processing CSV and uploading images, please wait...</span>
        <br><br>
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>

    <!-- Display when data fails to load -->
    <div class="text-danger fst-italic fw-bold fs-5 pt-5" v-if="dataLoaded == null"> 
        <span>An error occurred while loading this page, please try again!</span>
        <br>
        <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
            <span class="fs-5 fst-italic"> Return to previous page </span>
        </button>
        <router-link :to="'/'" class="mx-1">
            <button class="btn primary-btn btn-sm">
                <span class="fs-5 fst-italic"> Go to Home page </span>
            </button>
        </router-link>
    </div>

    <!-- Main upload form - show when not staging in progress -->
    <div v-if="dataLoaded && !stagingInProgress" class="container mt-5 mb-5">
        <div>
            <div class="form-group mb-2">
                <h1>Bulk Import Listings</h1>

                <h3 class="mt-5"> 
                    <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">
                        <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5"/>
                        <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708z"/>
                    </svg>
                    Download Listings Import Template 
                </h3>
                <button type="button" class="btn secondary-btn-less-round" @click="downloadCSV()"> Download Template </button>

                <h3 class="mt-5"> 
                    <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-upload" viewBox="0 0 16 16">
                        <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5"/>
                        <path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708z"/>
                    </svg>
                    Upload Listings CSV File 
                </h3>
                <div class="row align-items-center my-3">
                    <div class="col-3"></div>
                    <div class="col-6"> 
                        <input type="file" name="file" id="csvFile" accept=".csv" @change="handleFileUpload" class="form-control">
                    </div>
                    <div class="col-3"></div>
                </div>

                <button v-if="csvFile" type="button" class="btn primary-btn-less-round" @click="stageCSV">Stage for Review</button>
                <button v-else type="button" class="btn primary-btn-less-round" disabled>Stage for Review</button>
            </div>
        </div>
    </div>

    <!-- ==================== STAGING MODAL ==================== -->
    <div v-if="showStagingModal" class="staging-modal-overlay" @click.self="!commitInProgress && closeStagingModal()">
        <div class="staging-modal-content">
            <div class="staging-modal-header">
                <h4 class="mb-0">
                    <span v-if="!commitComplete">Review Staged Listings</span>
                    <span v-else>Import Results</span>
                </h4>
                <button type="button" class="btn-close" @click="closeStagingModal" :disabled="commitInProgress"></button>
            </div>
            <div class="staging-modal-body">
                <!-- Pre-commit info -->
                <div v-if="!commitComplete && !commitInProgress" class="mb-3">
                    <p class="text-muted mb-1">
                        <span v-if="getSelectedCount() > 0">
                            <strong>{{ getSelectedCount() }}</strong> of {{ stagedListings.length }} item(s) selected for import
                        </span>
                        <span v-else-if="stagedListings.length > 0" class="text-warning">
                            <strong>0</strong> items selected for import
                        </span>
                        <span v-if="getDuplicatesCount() > 0" class="text-secondary ms-2">
                            (<strong>{{ getDuplicatesCount() }}</strong> potential duplicate(s) detected)
                        </span>
                        <span v-if="getNewProducersCount() > 0" class="text-warning ms-2">
                            (<strong>{{ getNewProducersCount() }}</strong> new producer(s) will be created)
                        </span>
                    </p>
                    <p class="text-muted small mb-0">Use checkboxes to select items. Click cells to edit. Review before confirming.</p>
                </div>
                
                <!-- In-progress spinner -->
                <div v-if="commitInProgress" class="text-center py-3">
                    <div class="spinner-border text-primary mb-2" role="status">
                        <span class="visually-hidden">Importing...</span>
                    </div>
                    <p class="text-info fw-bold mb-0">Importing {{ getSelectedCount() }} item(s)... Please wait.</p>
                </div>
                
                <!-- Post-commit summary -->
                <div v-if="commitComplete && commitSummary" class="mb-3">
                    <div class="alert" :class="getAlertClass()">
                        <h5 class="alert-heading mb-2">
                            <span v-if="commitSummary.committedCount === 0 && commitSummary.failCount === 0">ℹ️ No items imported</span>
                            <span v-else-if="commitSummary.failCount === 0">✓ All items imported successfully!</span>
                            <span v-else-if="commitSummary.committedCount === 0">✗ Import failed</span>
                            <span v-else>⚠ Partial success</span>
                        </h5>
                        <p class="mb-1">
                            <strong>{{ commitSummary.committedCount }}</strong> listing(s) imported successfully
                            <span v-if="commitSummary.newProducersCreated > 0">,
                                <strong>{{ commitSummary.newProducersCreated }}</strong> new producer(s) created
                            </span>
                            <span v-if="commitSummary.newBottlersCreated > 0">,
                                <strong>{{ commitSummary.newBottlersCreated }}</strong> new bottler(s) created
                            </span>
                        </p>
                    </div>
                </div>

                <!-- Validation errors from staging (if any) -->
                <div v-if="stagingErrors.length > 0" class="alert alert-warning mb-3">
                    <h6 class="alert-heading">CSV Validation Warnings:</h6>
                    <ul class="mb-0 small">
                        <li v-for="(error, index) in stagingErrors" :key="index">
                            Row {{ error.rowNumber }}: {{ error.error }}
                        </li>
                    </ul>
                </div>
                
                <!-- Staging Table -->
                <div class="table-responsive staging-table-wrapper">
                    <table class="table table-bordered staging-table">
                        <thead class="table-light sticky-header">
                            <tr>
                                <th v-if="!commitComplete" style="width: 40px; text-align: center;">
                                    <input 
                                        type="checkbox" 
                                        class="form-check-input staging-checkbox"
                                        :checked="isAllSelected()"
                                        @change="toggleSelectAll()"
                                        title="Select/Deselect All"
                                    />
                                </th>
                                <th>#</th>
                                <th style="min-width: 180px;">Status</th>
                                <th>Photo</th>
                                <th style="min-width: 150px;">Listing Name</th>
                                <th style="min-width: 120px;">Producer</th>
                                <th>Bottler</th>
                                <th>Drink Type</th>
                                <th>Category</th>
                                <th>Style</th>
                                <th>Country</th>
                                <th>ABV</th>
                                <th>Age</th>
                                <th style="min-width: 150px;">Description</th>
                                <th>Source Link</th>
                                <th>Review Link</th>
                                <th v-if="!commitComplete" style="width: 60px;">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <template v-for="(item, index) in stagedListings" :key="'staged-' + item.id">
                            <tr :class="getRowClass(item)">
                                <!-- Checkbox column (hidden after commit) -->
                                <td v-if="!commitComplete" class="text-center">
                                    <input 
                                        type="checkbox" 
                                        class="form-check-input staging-checkbox"
                                        :checked="isItemSelected(item.id)"
                                        @change="toggleItemSelection(item.id)"
                                    />
                                </td>
                                <td>{{ index + 1 }}</td>
                                <td>
                                    <!-- Pre-commit: show status badges -->
                                    <template v-if="!commitComplete">
                                        <!-- Potential duplicate -->
                                        <span v-if="item?.isDuplicate" class="badge bg-warning text-dark me-1">
                                            ⚠️ Possible Duplicate
                                        </span>
                                        <!-- Producer doesn't exist -->
                                        <span v-if="!item?.producerID" class="badge bg-info me-1">
                                            🆕 New Producer
                                        </span>
                                        <!-- New submission -->
                                        <span v-if="!item?.isDuplicate && item?.producerID" class="badge bg-primary">
                                            Ready to import
                                        </span>
                                        <span v-else-if="!item?.isDuplicate && !item?.producerID" class="badge bg-primary">
                                            Ready (new producer)
                                        </span>
                                    </template>
                                    <!-- Post-commit: show result -->
                                    <template v-else>
                                        <span v-if="item.commitStatus === 'success'" class="badge bg-success">
                                            ✓ Imported
                                            <span v-if="item.newListingId"> (ID: {{ item.newListingId }})</span>
                                        </span>
                                        <span v-else-if="item.commitStatus === 'skipped'" class="badge bg-secondary">
                                            ⏭️ Skipped
                                        </span>
                                        <span v-else-if="item.commitStatus === 'error'" class="badge bg-danger">
                                            ✗ Failed
                                        </span>
                                    </template>
                                </td>
                                <td>
                                    <img 
                                        v-if="item.photo" 
                                        :src="item.photo" 
                                        class="staging-thumbnail"
                                        alt="Listing photo"
                                    />
                                    <span v-else class="text-muted">-</span>
                                </td>
                                <!-- Listing Name - Editable -->
                                <td class="editable-cell" 
                                    @click="startEditing(item.id, 'listingName')" 
                                    :class="{ 'editing': isEditing(item.id, 'listingName'), 'not-editable': commitComplete }">
                                    <template v-if="isEditing(item.id, 'listingName')">
                                        <input 
                                            type="text" 
                                            class="form-control form-control-sm inline-edit-input"
                                            v-model="item.listingName"
                                            @blur="stopEditing(item)"
                                            @keyup.enter="stopEditing(item)"
                                            @keyup.escape="cancelEditing()"
                                            ref="editInput"
                                            @click.stop
                                        />
                                    </template>
                                    <template v-else>
                                        <span :class="{ 'text-muted': !item.listingName }">{{ truncateText(item.listingName, 20) || '-' }}</span>
                                    </template>
                                </td>
                                <!-- Producer - Editable -->
                                <td class="editable-cell" 
                                    :class="{ 'editing': isEditing(item.id, 'producerName'), 'not-editable': commitComplete, 'producer-warning': !item.producerID }"
                                    @click="startEditing(item.id, 'producerName')">
                                    <template v-if="isEditing(item.id, 'producerName')">
                                        <input 
                                            type="text" 
                                            class="form-control form-control-sm inline-edit-input"
                                            v-model="item.producerName"
                                            @blur="stopEditing(item)"
                                            @keyup.enter="stopEditing(item)"
                                            @keyup.escape="cancelEditing()"
                                            ref="editInput"
                                            @click.stop
                                        />
                                    </template>
                                    <template v-else>
                                        <span :class="{ 'text-muted': !item.producerName, 'text-warning fw-bold': !item.producerID }">
                                            {{ truncateText(item.producerName, 15) || '-' }}
                                            <span v-if="!item.producerID" class="badge bg-warning text-dark ms-1" style="font-size: 0.65em;">NEW</span>
                                        </span>
                                    </template>
                                </td>
                                <!-- Bottler -->
                                <td class="editable-cell" 
                                    :class="{ 'editing': isEditing(item.id, 'bottler'), 'not-editable': commitComplete }"
                                    @click="startEditing(item.id, 'bottler')">
                                    <template v-if="isEditing(item.id, 'bottler')">
                                        <input 
                                            type="text" 
                                            class="form-control form-control-sm inline-edit-input"
                                            v-model="item.bottler"
                                            @blur="stopEditing(item)"
                                            @keyup.enter="stopEditing(item)"
                                            @keyup.escape="cancelEditing()"
                                            ref="editInput"
                                            @click.stop
                                        />
                                    </template>
                                    <template v-else>
                                        <span :class="{ 'text-muted': !item.bottler }">{{ truncateText(item.bottler, 12) || '-' }}</span>
                                    </template>
                                </td>
                                <!-- Drink Type -->
                                <td class="editable-cell" 
                                    :class="{ 'editing': isEditing(item.id, 'drinkType'), 'not-editable': commitComplete }"
                                    @click="startEditing(item.id, 'drinkType')">
                                    <template v-if="isEditing(item.id, 'drinkType')">
                                        <input 
                                            type="text" 
                                            class="form-control form-control-sm inline-edit-input"
                                            v-model="item.drinkType"
                                            @blur="stopEditing(item)"
                                            @keyup.enter="stopEditing(item)"
                                            @keyup.escape="cancelEditing()"
                                            ref="editInput"
                                            @click.stop
                                        />
                                    </template>
                                    <template v-else>
                                        <span :class="{ 'text-muted': !item.drinkType }">{{ item.drinkType || '-' }}</span>
                                    </template>
                                </td>
                                <!-- Category -->
                                <td class="editable-cell" 
                                    :class="{ 'editing': isEditing(item.id, 'typeCategory'), 'not-editable': commitComplete }"
                                    @click="startEditing(item.id, 'typeCategory')">
                                    <template v-if="isEditing(item.id, 'typeCategory')">
                                        <input 
                                            type="text" 
                                            class="form-control form-control-sm inline-edit-input"
                                            v-model="item.typeCategory"
                                            @blur="stopEditing(item)"
                                            @keyup.enter="stopEditing(item)"
                                            @keyup.escape="cancelEditing()"
                                            ref="editInput"
                                            @click.stop
                                        />
                                    </template>
                                    <template v-else>
                                        <span :class="{ 'text-muted': !item.typeCategory }">{{ item.typeCategory || '-' }}</span>
                                    </template>
                                </td>
                                <!-- Style -->
                                <td class="editable-cell" 
                                    :class="{ 'editing': isEditing(item.id, 'drinkStyle'), 'not-editable': commitComplete }"
                                    @click="startEditing(item.id, 'drinkStyle')">
                                    <template v-if="isEditing(item.id, 'drinkStyle')">
                                        <input 
                                            type="text" 
                                            class="form-control form-control-sm inline-edit-input"
                                            v-model="item.drinkStyle"
                                            @blur="stopEditing(item)"
                                            @keyup.enter="stopEditing(item)"
                                            @keyup.escape="cancelEditing()"
                                            ref="editInput"
                                            @click.stop
                                        />
                                    </template>
                                    <template v-else>
                                        <span :class="{ 'text-muted': !item.drinkStyle }">{{ item.drinkStyle || '-' }}</span>
                                    </template>
                                </td>
                                <!-- Country -->
                                <td class="editable-cell" 
                                    :class="{ 'editing': isEditing(item.id, 'originCountry'), 'not-editable': commitComplete }"
                                    @click="startEditing(item.id, 'originCountry')">
                                    <template v-if="isEditing(item.id, 'originCountry')">
                                        <input 
                                            type="text" 
                                            class="form-control form-control-sm inline-edit-input"
                                            v-model="item.originCountry"
                                            @blur="stopEditing(item)"
                                            @keyup.enter="stopEditing(item)"
                                            @keyup.escape="cancelEditing()"
                                            ref="editInput"
                                            @click.stop
                                        />
                                    </template>
                                    <template v-else>
                                        <span :class="{ 'text-muted': !item.originCountry }">{{ truncateText(item.originCountry, 10) || '-' }}</span>
                                    </template>
                                </td>
                                <!-- ABV -->
                                <td class="editable-cell" 
                                    :class="{ 'editing': isEditing(item.id, 'abv'), 'not-editable': commitComplete }"
                                    @click="startEditing(item.id, 'abv')">
                                    <template v-if="isEditing(item.id, 'abv')">
                                        <input 
                                            type="number" 
                                            class="form-control form-control-sm inline-edit-input inline-edit-number"
                                            v-model="item.abv"
                                            @blur="stopEditing(item)"
                                            @keyup.enter="stopEditing(item)"
                                            @keyup.escape="cancelEditing()"
                                            min="0" max="100" step="0.1"
                                            ref="editInput"
                                            @click.stop
                                        />
                                    </template>
                                    <template v-else>
                                        <span :class="{ 'text-muted': !item.abv }">{{ item.abv || '-' }}</span>
                                    </template>
                                </td>
                                <!-- Age -->
                                <td class="editable-cell" 
                                    :class="{ 'editing': isEditing(item.id, 'age'), 'not-editable': commitComplete }"
                                    @click="startEditing(item.id, 'age')">
                                    <template v-if="isEditing(item.id, 'age')">
                                        <input 
                                            type="text" 
                                            class="form-control form-control-sm inline-edit-input"
                                            v-model="item.age"
                                            @blur="stopEditing(item)"
                                            @keyup.enter="stopEditing(item)"
                                            @keyup.escape="cancelEditing()"
                                            ref="editInput"
                                            @click.stop
                                        />
                                    </template>
                                    <template v-else>
                                        <span :class="{ 'text-muted': !item.age }">{{ item.age || '-' }}</span>
                                    </template>
                                </td>
                                <!-- Description -->
                                <td class="editable-cell" 
                                    :class="{ 'editing': isEditing(item.id, 'officialDesc'), 'not-editable': commitComplete }"
                                    @click="startEditing(item.id, 'officialDesc')">
                                    <template v-if="isEditing(item.id, 'officialDesc')">
                                        <textarea 
                                            class="form-control form-control-sm inline-edit-input"
                                            v-model="item.officialDesc"
                                            @blur="stopEditing(item)"
                                            @keyup.escape="cancelEditing()"
                                            rows="2"
                                            ref="editInput"
                                            @click.stop
                                        ></textarea>
                                    </template>
                                    <template v-else>
                                        <span :class="{ 'text-muted': !item.officialDesc }">{{ truncateText(item.officialDesc, 25) || '-' }}</span>
                                    </template>
                                </td>
                                <!-- Source Link -->
                                <td class="editable-cell" 
                                    :class="{ 'editing': isEditing(item.id, 'sourceLink'), 'not-editable': commitComplete }"
                                    @click="startEditing(item.id, 'sourceLink')">
                                    <template v-if="isEditing(item.id, 'sourceLink')">
                                        <input 
                                            type="url" 
                                            class="form-control form-control-sm inline-edit-input"
                                            v-model="item.sourceLink"
                                            @blur="stopEditing(item)"
                                            @keyup.enter="stopEditing(item)"
                                            @keyup.escape="cancelEditing()"
                                            ref="editInput"
                                            @click.stop
                                        />
                                    </template>
                                    <template v-else>
                                        <span :class="{ 'text-muted': !item.sourceLink }">{{ truncateText(item.sourceLink, 15) || '-' }}</span>
                                    </template>
                                </td>
                                <!-- Review Link -->
                                <td class="editable-cell" 
                                    :class="{ 'editing': isEditing(item.id, 'reviewLink'), 'not-editable': commitComplete }"
                                    @click="startEditing(item.id, 'reviewLink')">
                                    <template v-if="isEditing(item.id, 'reviewLink')">
                                        <input 
                                            type="url" 
                                            class="form-control form-control-sm inline-edit-input"
                                            v-model="item.reviewLink"
                                            @blur="stopEditing(item)"
                                            @keyup.enter="stopEditing(item)"
                                            @keyup.escape="cancelEditing()"
                                            ref="editInput"
                                            @click.stop
                                        />
                                    </template>
                                    <template v-else>
                                        <span :class="{ 'text-muted': !item.reviewLink }">{{ truncateText(item.reviewLink, 15) || '-' }}</span>
                                    </template>
                                </td>
                                <!-- Delete action -->
                                <td v-if="!commitComplete" class="text-center">
                                    <button 
                                        type="button" 
                                        class="btn btn-sm btn-outline-danger"
                                        @click="deleteStagedItem(item.id)"
                                        title="Remove from staging"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                        </svg>
                                    </button>
                                </td>
                            </tr>
                            
                            <!-- Expandable duplicate matches row (light green) -->
                            <tr v-if="item?.isDuplicate && (getDuplicateInfo(item.id)?.matches?.length || 0) > 0" 
                                class="duplicate-matches-row">
                                <td :colspan="commitComplete ? 12 : 13" class="p-0">
                                    <div class="duplicate-matches-container">
                                        <div class="duplicate-matches-header">
                                            <i class="bi bi-exclamation-triangle-fill text-warning me-2"></i>
                                            <strong>{{ getDuplicateInfo(item.id)?.matches?.length || 0 }} potential duplicate(s) found</strong>
                                            <span class="text-muted ms-2">(95%+ similarity)</span>
                                        </div>
                                        <div class="duplicate-matches-content">
                                            <div 
                                                v-for="match in (getDuplicateInfo(item.id)?.matches || [])" 
                                                :key="'match-' + match.id"
                                                class="duplicate-match-item">
                                                <div >
                                                    <img class="match-thumbnail" v-if="match.photo" :src="match.photo" alt="Match photo" />
                                                    <div v-else class="no-photo">
                                                        <i class="bi bi-image"></i>
                                                    </div>
                                                </div>
                                                <div class="match-details">
                                                    <div class="match-name">
                                                        <a :href="`/listing/view/${match.id}/${slugify(match.listingName)}`" 
                                                           target="_blank"
                                                           class="text-decoration-none">
                                                            {{ match.listingName }}
                                                            <i class="bi bi-box-arrow-up-right ms-1 small"></i>
                                                        </a>
                                                    </div>
                                                    <div class="match-producer text-muted small">
                                                        by {{ match.producerName }}
                                                        <span v-if="shouldShowBottler(match)" class="ms-1">(Bottler: {{ match.bottlerName }})</span>
                                                    </div>
                                                    <div class="match-attributes text-muted small">
                                                        <span v-if="match.drinkType">{{ match.drinkType }}</span>
                                                        <span v-if="match.typeCategory"> · {{ match.typeCategory }}</span>
                                                        <span v-if="match.drinkStyle"> · {{ match.drinkStyle }}</span>
                                                        <span v-if="match.originCountry"> · {{ match.originCountry }}</span>
                                                        <span v-if="match.abv"> · {{ match.abv }}%</span>
                                                        <span v-if="match.age"> · {{ match.age }}</span>
                                                    </div>
                                                </div>
                                                <div class="match-similarity">
                                                    <span class="badge" 
                                                          :class="match.similarity >= 98 ? 'bg-danger' : (match.similarity >= 96 ? 'bg-warning text-dark' : 'bg-info')">
                                                        {{ match.similarity }}% match
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </td>
                            </tr>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="staging-modal-footer">
                <!-- Pre-commit buttons -->
                <template v-if="!commitComplete && !commitInProgress">
                    <button type="button" class="btn btn-secondary" @click="closeStagingModal">Cancel</button>
                    <button 
                        type="button" 
                        class="btn btn-success" 
                        @click="commitStagedListings"
                        :disabled="getSelectedCount() === 0"
                    >
                        Confirm Import ({{ getSelectedCount() }})
                    </button>
                </template>
                
                <!-- In-progress state -->
                <template v-if="commitInProgress">
                    <button type="button" class="btn btn-secondary" disabled>Please wait...</button>
                </template>
                
                <!-- Post-commit buttons -->
                <template v-if="commitComplete">
                    <button type="button" class="btn btn-secondary" @click="closeStagingModal">Close</button>
                    <button 
                        type="button" 
                        class="btn btn-primary" 
                        @click="resetAndImportMore"
                    >
                        Import More Listings
                    </button>
                </template>
            </div>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
    name: 'ImportListings',
    components: {
        NavBar
    },
    data() {
        return {
            dataLoaded: false,

            // CSV template data
            fileFormat: [],
            csvData: [],

            // Logged in user details
            userID: null,
            userType: localStorage.getItem('88B_accType'),
            isAdmin: false, // Stage 4.3: Track if user is admin

            // CSV file upload
            csvFile: null,

            // Staging state
            stagingInProgress: false,
            showStagingModal: false,
            stagedListings: [],
            stagingErrors: [],
            selectedItems: new Set(),

            // Commit state
            commitInProgress: false,
            commitComplete: false,
            commitSummary: null,

            // Inline editing
            editingCell: null, // { id, field }

            // Duplicate detection results (from staging response)
            duplicateMatches: {} // Map of stagedListingId -> { isDuplicate, matches: [...] }
        }
    },
    mounted() {
        // Check if user is logged in
        this.userID = localStorage.getItem('88B_accID');

        if (this.userID == null) {
            this.$router.push('/login');
        } else {
            this.loadData();
        }
    },
    methods: {
        async loadData() {
            // Load CSV template
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/adminFunctions/readCSV`);
                this.fileFormat = response.data.data;
                this.convertToCSV();
            } catch (error) {
                console.error(error);
                this.dataLoaded = null;
                return;
            }

            // Stage 4.3: Allow users, producers, and venues to access (not just admins)
            // Verify user exists and is valid account type
            try {
                if (this.userType === "user") {
                    // Users can access - optionally check if admin for elevated privileges
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUser/${this.userID}`);
                    this.isAdmin = response.data['isAdmin'] || false;
                } else if (this.userType === "producer") {
                    // Producers can bulk import their own listings
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducer/${this.userID}`);
                    if (!response.data || response.data.code === 404) {
                        this.$router.push('/');
                        return;
                    }
                    this.isAdmin = false;
                } else if (this.userType === "venue") {
                    // Venues can bulk import listings
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenue/${this.userID}`);
                    if (!response.data || response.data.code === 404) {
                        this.$router.push('/');
                        return;
                    }
                    this.isAdmin = false;
                } else {
                    // Unknown account type - redirect
                    this.$router.push('/');
                    return;
                }
            } catch (error) {
                console.error('Error verifying user access:', error);
                this.dataLoaded = null;
                return;
            }

            // Duplicate detection is now server-side batch API

            // Set data loaded to true
            if (this.dataLoaded != null) {
                this.dataLoaded = true;
            }
        },

        // Handle file selection
        handleFileUpload(event) {
            this.csvFile = event.target.files[0];
        },

        // Stage CSV for review (Step 1)
        async stageCSV() {
            if (!this.csvFile) return;

            // Stage 4.4: Validate file type
            if (!this.csvFile.name.toLowerCase().endsWith('.csv')) {
                alert('Please upload a CSV file (.csv extension)');
                return;
            }

            // Stage 4.4: Validate file size (max 10MB)
            const maxSizeBytes = 10 * 1024 * 1024;
            if (this.csvFile.size > maxSizeBytes) {
                alert('File is too large. Maximum size is 10MB.');
                return;
            }

            this.stagingInProgress = true;
            this.stagingErrors = [];

            const formData = new FormData();
            formData.append('file', this.csvFile);
            formData.append('submitterID', this.userID);
            formData.append('submitterType', this.userType);

            try {
                const response = await this.$axios.post(
                    `${process.env.VUE_APP_API_URL}/createListing/stageListingsFromCSV`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        },
                        timeout: 300000 // 5 minute timeout for large files with images
                    }
                );

                if (response.data.code === 201) {
                    this.stagedListings = response.data.data.staged || [];
                    this.stagingErrors = response.data.data.validationErrors || [];

                    // Stage 4.4: Handle empty CSV edge case
                    if (this.stagedListings.length === 0 && this.stagingErrors.length === 0) {
                        alert('No valid listings found in the CSV file. Please check the file format and try again.');
                        this.stagingInProgress = false;
                        return;
                    }

                    // Stage 4.4: Handle all rows failed validation
                    if (this.stagedListings.length === 0 && this.stagingErrors.length > 0) {
                        alert(`All ${this.stagingErrors.length} row(s) in the CSV had validation errors. Please review the errors and fix the CSV file.`);
                        // Still show modal so user can see errors
                        this.showStagingModal = true;
                        this.stagingInProgress = false;
                        return;
                    }

                    // Process duplicate detection results from the response (already included)
                    this.duplicateMatches = response.data.data.duplicateMatches || {};
                    
                    // Debug: log the duplicate matches to verify structure
                    console.log('charsiucharlie_duplicate_check_debug: Duplicate matches from backend:', this.duplicateMatches);
                    console.log('charsiucharlie_duplicate_check_debug: Staged listings IDs:', this.stagedListings.map(item => ({ id: item.id, type: typeof item.id, isDuplicate: item.isDuplicate })));
                    
                    // Auto-deselect items marked as duplicates
                    for (const listing of this.stagedListings) {
                        if (listing.isDuplicate) {
                            // Don't add to selectedItems (they come pre-flagged from backend)
                        }
                    }
                    
                    // Select all NON-duplicate items by default
                    this.selectedItems = new Set(
                        this.stagedListings
                            .filter(item => item && !item.isDuplicate)
                            .map(item => item.id)
                    );
                    
                    console.log(`Duplicate check complete: ${response.data.data.totalDuplicates || 0} potential duplicates found`);

                    // Show staging modal
                    this.showStagingModal = true;

                    console.log(`Staged ${this.stagedListings.length} listings for review`);
                } else {
                    alert(`Error staging listings: ${response.data.message || 'Unknown error'}`);
                }
            } catch (error) {
                console.error('Error staging CSV:', error);
                
                // Stage 4.4: Better error messages based on error type
                let errorMsg = 'Unknown error occurred';
                if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
                    errorMsg = 'Request timed out. The file may be too large or contain too many images. Try with fewer rows.';
                } else if (error.response?.status === 413) {
                    errorMsg = 'File is too large for the server. Try with fewer rows or smaller images.';
                } else if (error.response?.status === 400) {
                    errorMsg = error.response?.data?.message || 'Invalid CSV format. Please check the file.';
                } else if (error.response?.status === 500) {
                    errorMsg = 'Server error occurred. Please try again later.';
                } else if (error.response?.data?.message) {
                    errorMsg = error.response.data.message;
                }
                
                alert(`Error staging listings: ${errorMsg}`);
            } finally {
                this.stagingInProgress = false;
            }
        },

        // Commit selected staged listings (Step 2)
        async commitStagedListings() {
            const selectedIds = Array.from(this.selectedItems);
            if (selectedIds.length === 0) {
                alert('Please select at least one listing to import');
                return;
            }

            // Stage 4.4: Warn about duplicates if any are selected
            const selectedDuplicates = this.stagedListings.filter(
                item => item && this.selectedItems.has(item.id) && item.isDuplicate
            );
            if (selectedDuplicates.length > 0) {
                const proceed = confirm(
                    `${selectedDuplicates.length} selected item(s) are marked as potential duplicates. ` +
                    `Do you want to proceed with importing them anyway?`
                );
                if (!proceed) return;
            }

            this.commitInProgress = true;

            try {
                const response = await this.$axios.post(
                    `${process.env.VUE_APP_API_URL}/createListing/commitStagedListings`,
                    { stagedIds: selectedIds },
                    { timeout: 120000 } // 2 minute timeout
                );

                if (response.data.code === 201) {
                    this.commitSummary = response.data.data;
                    this.commitComplete = true;

                    // Mark committed items as successful
                    for (const item of this.stagedListings) {
                        if (this.selectedItems.has(item.id)) {
                            item.commitStatus = 'success';
                            // Store the new listing ID if returned
                            if (this.commitSummary.createdListings) {
                                const created = this.commitSummary.createdListings.find(
                                    l => l.stagedId === item.id
                                );
                                if (created) {
                                    item.newListingId = created.listingId;
                                }
                            }
                        } else {
                            item.commitStatus = 'skipped';
                        }
                    }

                    console.log(`Successfully committed ${this.commitSummary.committedCount} listings`);
                } else {
                    alert(`Error committing listings: ${response.data.message || 'Unknown error'}`);
                }
            } catch (error) {
                console.error('Error committing listings:', error);
                
                // Stage 4.4: Better error messages
                let errorMsg = 'Unknown error occurred';
                if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
                    errorMsg = 'Request timed out. Try committing fewer listings at once.';
                } else if (error.response?.status === 500) {
                    errorMsg = 'Server error occurred. Some listings may have been imported. Please refresh and check.';
                } else if (error.response?.data?.message) {
                    errorMsg = error.response.data.message;
                }
                
                alert(`Error committing listings: ${errorMsg}`);

                // Mark selected items as failed
                for (const item of this.stagedListings) {
                    if (this.selectedItems.has(item.id)) {
                        item.commitStatus = 'error';
                    }
                }
                this.commitComplete = true;
                this.commitSummary = {
                    committedCount: 0,
                    failCount: this.selectedItems.size,
                    newProducersCreated: 0,
                    newBottlersCreated: 0
                };
            } finally {
                this.commitInProgress = false;
            }
        },

        // Delete a single staged item
        async deleteStagedItem(id) {
            if (!confirm('Remove this item from staging?')) return;

            try {
                await this.$axios.delete(`${process.env.VUE_APP_API_URL}/createListing/deleteStagedListing/${id}`);
                
                // Remove from local list
                this.stagedListings = this.stagedListings.filter(item => item.id !== id);
                this.selectedItems.delete(id);
                // Force reactivity update
                this.selectedItems = new Set(this.selectedItems);

                // Close modal if no items left
                if (this.stagedListings.length === 0) {
                    this.closeStagingModal();
                    alert('All staged items have been removed.');
                }
            } catch (error) {
                console.error('Error deleting staged item:', error);
                const errorMsg = error.response?.data?.message || 'Unknown error';
                alert(`Error removing item from staging: ${errorMsg}`);
            }
        },

        // Update a staged item after editing
        async updateStagedItem(item) {
            // Stage 4.4: Mark item as saving (could show visual indicator)
            item._saving = true;
            
            try {
                const response = await this.$axios.put(
                    `${process.env.VUE_APP_API_URL}/createListing/updateStagedListing/${item.id}`,
                    {
                        listingName: item.listingName,
                        producerName: item.producerName,
                        bottler: item.bottler,
                        drinkType: item.drinkType,
                        typeCategory: item.typeCategory,
                        drinkStyle: item.drinkStyle,
                        originCountry: item.originCountry,
                        abv: item.abv,
                        age: item.age,
                        officialDesc: item.officialDesc,
                        sourceLink: item.sourceLink,
                        reviewLink: item.reviewLink
                    }
                );
                
                // Update producerID if backend returns it (producer might now exist)
                if (response.data?.data?.producerID !== undefined) {
                    item.producerID = response.data.data.producerID;
                }
                
                // Re-check duplicates after edit
                this.checkForDuplicates();
            } catch (error) {
                console.error('Error updating staged item:', error);
                // Silent fail for inline edits - data is still saved locally
            } finally {
                item._saving = false;
            }
        },

        // Close staging modal
        closeStagingModal() {
            if (this.commitInProgress) return;
            
            this.showStagingModal = false;
            
            // If commit is complete, reset state
            if (this.commitComplete) {
                this.resetStagingState();
            }
        },

        // Reset and allow more imports
        resetAndImportMore() {
            this.resetStagingState();
            this.csvFile = null;
            // Reset file input
            const fileInput = document.getElementById('csvFile');
            if (fileInput) fileInput.value = '';
        },

        // Reset staging state
        resetStagingState() {
            this.showStagingModal = false;
            this.stagedListings = [];
            this.stagingErrors = [];
            this.selectedItems = new Set();
            this.commitInProgress = false;
            this.commitComplete = false;
            this.commitSummary = null;
            this.editingCell = null;
        },

        // ============ SELECTION METHODS ============

        isItemSelected(id) {
            return this.selectedItems.has(id);
        },

        toggleItemSelection(id) {
            if (this.selectedItems.has(id)) {
                this.selectedItems.delete(id);
            } else {
                this.selectedItems.add(id);
            }
            // Force reactivity
            this.selectedItems = new Set(this.selectedItems);
        },

        isAllSelected() {
            return this.stagedListings.length > 0 && 
                   this.stagedListings.every(item => this.selectedItems.has(item.id));
        },

        toggleSelectAll() {
            if (this.isAllSelected()) {
                this.selectedItems = new Set();
            } else {
                this.selectedItems = new Set(this.stagedListings.map(item => item.id));
            }
        },

        getSelectedCount() {
            return this.selectedItems.size;
        },

        getDuplicatesCount() {
            return this.stagedListings.filter(item => item && item.isDuplicate).length;
        },

        getNewProducersCount() {
            // Get unique producer names for selected items that don't have a producerID
            const uniqueProducers = new Set();
            this.stagedListings.forEach(item => {
                if (!item.producerID && this.selectedItems.has(item.id) && item.producerName) {
                    uniqueProducers.add(item.producerName.toLowerCase().trim());
                }
            });
            return uniqueProducers.size;
        },

        // ============ INLINE EDITING METHODS ============

        isEditing(id, field) {
            return this.editingCell && this.editingCell.id === id && this.editingCell.field === field;
        },

        startEditing(id, field) {
            if (this.commitComplete) return;
            this.editingCell = { id, field };
            this.$nextTick(() => {
                if (this.$refs.editInput) {
                    const input = Array.isArray(this.$refs.editInput) ? this.$refs.editInput[0] : this.$refs.editInput;
                    if (input) input.focus();
                }
            });
        },

        stopEditing(item) {
            if (item) {
                this.updateStagedItem(item);
            }
            this.editingCell = null;
        },

        cancelEditing() {
            this.editingCell = null;
        },

        // ============ UI HELPER METHODS ============

        getRowClass(item) {
            if (!item) return 'row-pending';
            if (this.commitComplete) {
                if (item.commitStatus === 'success') return 'row-success';
                if (item.commitStatus === 'error') return 'row-error';
                if (item.commitStatus === 'skipped') return 'row-skipped';
            }
            if (!this.selectedItems.has(item.id)) return 'row-unchecked';
            if (item.isDuplicate) return 'row-warning';
            if (!item.producerID) return 'row-new-producer';
            return 'row-pending';
        },

        getAlertClass() {
            if (!this.commitSummary) return 'alert-info';
            if (this.commitSummary.committedCount === 0) return 'alert-info';
            if (this.commitSummary.failCount === 0) return 'alert-success';
            return 'alert-warning';
        },

        truncateText(text, maxLength) {
            if (!text) return '';
            if (text.length <= maxLength) return text;
            return text.substring(0, maxLength) + '...';
        },

        // Get duplicate match info for a staged listing (handles string/number key mismatch)
        getDuplicateInfo(itemId) {
            if (!itemId || !this.duplicateMatches) return null;
            // Try both number and string keys since JSON serialization can change types
            return this.duplicateMatches[itemId] || this.duplicateMatches[String(itemId)] || null;
        },

        // Determine if bottler name should be shown for a match
        // Don't show if: empty, 'OB', 'Original Bottling', or same as producer name
        shouldShowBottler(match) {
            if (!match || !match.bottlerName) return false;
            const bottler = match.bottlerName.toLowerCase().trim();
            if (bottler === '' || bottler === 'ob' || bottler === 'original bottling' || bottler === 'original bottler') {
                return false;
            }
            // Don't show if same as producer name
            if (match.producerName && bottler === match.producerName.toLowerCase().trim()) {
                return false;
            }
            return true;
        },

        slugify(text) {
            if (!text) return '';
            return text
                .toString()
                .toLowerCase()
                .trim()
                .replace(/\s+/g, '-')
                .replace(/[^\w-]+/g, '')
                .replace(/--+/g, '-');
        },

        // ============ CSV TEMPLATE METHODS ============

        convertToCSV() {
            let keepColumns = this.fileFormat.filter(item => Object.values(item).some(value => value !== ''));
            this.csvData = keepColumns.map(column => {
                return { value: column };
            });
        },

        downloadCSV() {
            let csvContent = "data:text/csv;charset=utf-8,";
            this.csvData.forEach(row => {
                csvContent += row.value + "\n";
            });

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "listingsFormat.csv");
            document.body.appendChild(link);
            link.click();
        }
    }
}
</script>

<style scoped>
/* ==================== STAGING MODAL STYLES ==================== */

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
    max-width: 1600px;
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

.staging-modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding: 16px 24px;
    border-top: 1px solid #dee2e6;
    flex-shrink: 0;
}

/* ==================== TABLE STYLES ==================== */

.staging-table-wrapper {
    overflow: auto;
    flex: 1;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    position: relative;
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

.sticky-header {
    position: sticky;
    top: 0;
    z-index: 10;
}

/* ==================== ROW STATUS STYLES ==================== */

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

.staging-table tr.row-warning {
    background-color: rgba(255, 193, 7, 0.15) !important;
}

.staging-table tr.row-warning:hover {
    background-color: rgba(255, 193, 7, 0.2) !important;
}

.staging-table tr.row-new-producer {
    background-color: rgba(13, 202, 240, 0.1) !important;
}

.staging-table tr.row-new-producer:hover {
    background-color: rgba(13, 202, 240, 0.15) !important;
}

.staging-table tr.row-unchecked {
    background-color: rgba(108, 117, 125, 0.08) !important;
    opacity: 0.6;
}

.staging-table tr.row-unchecked:hover {
    background-color: rgba(108, 117, 125, 0.12) !important;
    opacity: 0.75;
}

/* ==================== CHECKBOX STYLES ==================== */

.staging-checkbox {
    width: 18px;
    height: 18px;
    cursor: pointer;
}

.staging-checkbox:checked {
    background-color: #198754;
    border-color: #198754;
}

/* ==================== EDITABLE CELL STYLES ==================== */

.editable-cell {
    cursor: pointer;
    transition: background-color 0.15s ease;
    position: relative;
    min-width: 60px;
}

.editable-cell:hover:not(.editing):not(.not-editable) {
    background-color: rgba(13, 110, 253, 0.08);
}

.editable-cell.editing {
    padding: 2px 4px !important;
    background-color: rgba(13, 110, 253, 0.12);
}

.editable-cell.not-editable {
    cursor: not-allowed;
    opacity: 0.7;
}

.editable-cell.producer-warning {
    background-color: rgba(255, 193, 7, 0.15);
}

.inline-edit-input {
    min-width: 80px;
    max-width: 200px;
    font-size: 0.85rem !important;
    padding: 2px 6px !important;
    height: auto !important;
}

.inline-edit-number {
    min-width: 60px;
    max-width: 80px;
}

/* ==================== THUMBNAIL STYLES ==================== */

.staging-thumbnail {
    width: 50px;
    height: 50px;
    object-fit: cover;
    border-radius: 4px;
    border: 1px solid #dee2e6;
}

/* ==================== BADGE STYLES ==================== */

.staging-table .badge {
    font-size: 0.8em;
    padding: 5px 8px;
}

.staging-table .badge.bg-warning {
    color: #000;
}

/* ==================== DUPLICATE MATCH STYLES ==================== */

.duplicate-matches-row {
    background-color: rgba(25, 135, 84, 0.08) !important;
}

.duplicate-matches-row:hover {
    background-color: rgba(25, 135, 84, 0.12) !important;
}

.duplicate-matches-row td {
    border-top: none !important;
}

.duplicate-matches-container {
    padding: 12px 16px;
    background-color: rgba(25, 135, 84, 0.05);
    border-left: 3px solid #198754;
}

.duplicate-matches-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
    font-size: 0.9rem;
    font-weight: 600;
    color: #198754;
}

.duplicate-matches-header i {
    font-size: 1rem;
}

.duplicate-matches-content {
    max-height: 200px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.duplicate-match-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 12px;
    background-color: white;
    border-radius: 6px;
    border: 1px solid rgba(25, 135, 84, 0.2);
    transition: all 0.2s ease;
}

.duplicate-match-item:hover {
    border-color: rgba(25, 135, 84, 0.4);
    box-shadow: 0 2px 4px rgba(25, 135, 84, 0.15);
}

.match-thumbnail {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 4px;
    border: 1px solid #dee2e6;
    flex-shrink: 0;
}

.match-details {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.match-name {
    font-weight: 600;
    color: #0d6efd;
    text-decoration: none;
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.match-name:hover {
    text-decoration: underline;
    color: #0a58ca;
}

.match-producer {
    font-size: 0.85rem;
    color: #6c757d;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.match-attributes {
    font-size: 0.8rem;
    color: #6c757d;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-top: 2px;
}

.match-similarity {
    flex-shrink: 0;
    margin-left: auto;
}

/* Scrollbar styling for duplicate matches */
.duplicate-matches-content::-webkit-scrollbar {
    width: 6px;
}

.duplicate-matches-content::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.05);
    border-radius: 3px;
}

.duplicate-matches-content::-webkit-scrollbar-thumb {
    background: rgba(25, 135, 84, 0.3);
    border-radius: 3px;
}

.duplicate-matches-content::-webkit-scrollbar-thumb:hover {
    background: rgba(25, 135, 84, 0.5);
}
</style>
