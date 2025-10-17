<template>
  <div 
    class="modal fade" 
    id="csvImportModal" 
    tabindex="-1" 
    aria-labelledby="csvImportModalLabel" 
    aria-hidden="true"
    data-bs-backdrop="static"
  >
    <div class="modal-dialog modal-xl modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="csvImportModalLabel">
            <i class="bi bi-file-earmark-arrow-up me-2"></i>
            Import CSV to Cellar - {{ stepTitle }}
          </h5>
          <button 
            type="button" 
            class="btn-close" 
            data-bs-dismiss="modal" 
            aria-label="Close"
            @click="resetImport"
          ></button>
        </div>
        
        <div class="modal-body">
          <!-- Progress Bar -->
          <div class="progress mb-4" style="height: 25px;">
            <div 
              class="progress-bar" 
              :class="progressBarClass"
              role="progressbar" 
              :style="{width: progressPercentage + '%'}"
              :aria-valuenow="progressPercentage" 
              aria-valuemin="0" 
              aria-valuemax="100"
            >
              Step {{ currentStep }} of 4
            </div>
          </div>
          
          <!-- Step 1: Upload CSV -->
          <div v-if="currentStep === 1" class="step-content">
            <div class="text-center">
              <div class="upload-icon mb-4">
                <i class="bi bi-cloud-upload" style="font-size: 4rem; color: #0d6efd;"></i>
              </div>
              <h4>Upload Your CSV File</h4>
              <p class="text-muted">
                Select a CSV file containing your cellar inventory. The file can have any column structure - 
                you'll map the columns in the next step.
              </p>
              
              <div class="upload-area mt-4 mb-3">
                <input 
                  type="file" 
                  ref="fileInput"
                  accept=".csv"
                  @change="handleFileSelect"
                  class="d-none"
                  id="csvFileInput"
                />
                <label for="csvFileInput" class="upload-label">
                  <i class="bi bi-file-earmark-plus me-2"></i>
                  Choose CSV File
                </label>
              </div>
              
              <div v-if="selectedFile" class="alert alert-info">
                <i class="bi bi-file-earmark-check me-2"></i>
                Selected file: <strong>{{ selectedFile.name }}</strong> 
                ({{ formatFileSize(selectedFile.size) }})
              </div>
              
              <div class="mt-3">
                <button 
                  class="btn btn-primary btn-lg"
                  @click="uploadAndParseCSV"
                  :disabled="!selectedFile || uploading"
                >
                  <span v-if="uploading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ uploading ? 'Parsing CSV...' : 'Next: Map Columns' }}
                </button>
              </div>
            </div>
          </div>
          
          <!-- Step 2: Column Mapping -->
          <div v-if="currentStep === 2" class="step-content">
            <h4 class="mb-3">Map Your CSV Columns</h4>
            <p class="text-muted mb-4">
              Match each column from your CSV to the corresponding field in our database. 
              Columns you don't map will be ignored.
            </p>
            
            <div class="alert alert-warning">
              <i class="bi bi-exclamation-triangle me-2"></i>
              <strong>Required:</strong> You must map at least the "Drink Name" field.
            </div>
            
            <div class="table-responsive">
              <table class="table table-bordered column-mapping-table">
                <thead>
                  <tr>
                    <th>Your CSV Column</th>
                    <th>Sample Data</th>
                    <th>Map To Field</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="header in csvHeaders" :key="header">
                    <td class="fw-bold">{{ header }}</td>
                    <td>
                      <small class="text-muted">
                        {{ getSampleDataForColumn(header) }}
                      </small>
                    </td>
                    <td>
                      <select 
                        class="form-select form-select-sm"
                        v-model="columnMapping[header]"
                      >
                        <option value="">-- Skip Column --</option>
                        <optgroup label="Required">
                          <option value="listingName">Drink Name *</option>
                        </optgroup>
                        <optgroup label="Drink Information">
                          <option value="producerName">Producer Name</option>
                          <option value="variant">Vintage / Variant</option>
                          <option value="drinkType">Drink Type</option>
                          <option value="typeCategory">Category</option>
                          <option value="originCountry">Country</option>
                          <option value="abv">ABV (%)</option>
                        </optgroup>
                        <optgroup label="Bottle Details">
                          <option value="quantity">Quantity</option>
                          <option value="drinkFormat">Format (Bottle/Can/etc)</option>
                          <option value="volumeNumber">Volume Number</option>
                          <option value="volumeUnit">Volume Unit (ml/oz/L)</option>
                        </optgroup>
                        <optgroup label="Cellar Information">
                          <option value="status">Status</option>
                          <option value="consumption">Consumption State</option>
                          <option value="currentLocation">Storage Location</option>
                          <option value="subLocation">Sub Location</option>
                        </optgroup>
                        <optgroup label="Purchase Information">
                          <option value="purchaseDate">Purchase Date</option>
                          <option value="deliveryDate">Delivery Date</option>
                          <option value="purchasePrice">Purchase Price</option>
                          <option value="purchaseCurrency">Currency</option>
                          <option value="purchasePlaceName">Purchase Location</option>
                        </optgroup>
                        <optgroup label="Drinking Window">
                          <option value="drinkOnwardsDate">Drink From Date</option>
                          <option value="drinkByDate">Drink By Date</option>
                        </optgroup>
                        <optgroup label="Value & Notes">
                          <option value="currentValueEstimation">Current Value</option>
                          <option value="noteToSelf">Personal Notes</option>
                          <option value="suggestedFoodPairing">Food Pairing</option>
                        </optgroup>
                      </select>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div class="d-flex justify-content-between mt-4">
              <button class="btn btn-secondary" @click="currentStep = 1">
                <i class="bi bi-arrow-left me-2"></i>Back
              </button>
              <button 
                class="btn btn-primary"
                @click="processCSVWithMapping"
                :disabled="!hasRequiredMapping || processing"
              >
                <span v-if="processing" class="spinner-border spinner-border-sm me-2"></span>
                {{ processing ? 'Processing...' : 'Next: Review Duplicates' }}
              </button>
            </div>
          </div>
          
          <!-- Step 3: Duplicate Detection & Review -->
          <div v-if="currentStep === 3" class="step-content">
            <h4 class="mb-3">Review Potential Duplicates</h4>
            <p class="text-muted mb-4">
              We've found {{ totalItems }} items in your CSV. 
              {{ itemsWithMatches }} items have potential matches in the Drink-X database.
              Please review and choose how to handle each item.
            </p>
            
            <div class="alert alert-info">
              <i class="bi bi-info-circle me-2"></i>
              Items marked with high confidence (>90%) are likely the same drink. 
              You can accept these automatically or review each one.
            </div>
            
            <!-- Bulk Actions -->
            <div class="card mb-3 bg-light">
              <div class="card-body">
                <h6 class="card-title">Bulk Actions</h6>
                <div class="btn-group" role="group">
                  <button 
                    class="btn btn-sm btn-outline-primary"
                    @click="acceptAllHighConfidence"
                  >
                    Accept All High Confidence (>90%)
                  </button>
                  <button 
                    class="btn btn-sm btn-outline-secondary"
                    @click="createAllNew"
                  >
                    Create All As New
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Items List with Pagination -->
            <div class="items-review-list">
              <div 
                v-for="(item, index) in paginatedReviewItems" 
                :key="index"
                class="review-item card mb-3"
                :class="{'border-danger': item.validationErrors && item.validationErrors.length > 0}"
              >
                <div class="card-body">
                  <!-- Row Header -->
                  <div class="row-header mb-3">
                    <h6 class="mb-1">
                      Row {{ item.rowNumber }}: 
                      <strong>{{ item.mappedData.listingName }}</strong>
                      <span v-if="item.mappedData.variant" class="text-muted ms-1">
                        ({{ item.mappedData.variant }})
                      </span>
                    </h6>
                    <small class="text-muted">
                      <span v-if="item.mappedData.producerName">{{ item.mappedData.producerName }}</span>
                      <span v-if="item.mappedData.drinkType"> | {{ item.mappedData.drinkType }}</span>
                      <span v-if="item.mappedData.quantity"> | Qty: {{ item.mappedData.quantity }}</span>
                    </small>
                  </div>
                  
                  <!-- Validation Errors -->
                  <div v-if="item.validationErrors && item.validationErrors.length > 0" class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle me-2"></i>
                    <strong>Validation Errors:</strong>
                    <ul class="mb-0 mt-2">
                      <li v-for="(error, idx) in item.validationErrors" :key="idx">{{ error }}</li>
                    </ul>
                  </div>
                  
                  <!-- No Matches Found -->
                  <div v-if="!item.possibleMatches || item.possibleMatches.length === 0" class="alert alert-warning">
                    <i class="bi bi-info-circle me-2"></i>
                    No matches found in Drink-X database. This will be created as a new drink.
                    <div class="mt-2">
                      <label>
                        <input 
                          type="radio" 
                          :name="`decision-${item.rowNumber}`"
                          value="create_new"
                          v-model="item.selectedMatchId"
                          checked
                        />
                        <span class="ms-2">Create as new drink</span>
                      </label>
                      <br>
                      <label>
                        <input 
                          type="radio" 
                          :name="`decision-${item.rowNumber}`"
                          value="skip"
                          v-model="item.selectedMatchId"
                        />
                        <span class="ms-2">Skip this row</span>
                      </label>
                    </div>
                  </div>
                  
                  <!-- Possible Matches -->
                  <div v-else class="possible-matches">
                    <p class="mb-2">
                      <strong>{{ item.possibleMatches.length }} possible match{{ item.possibleMatches.length !== 1 ? 'es' : '' }} found:</strong>
                    </p>
                    
                    <div class="match-options">
                      <!-- Existing Matches -->
                      <div 
                        v-for="match in item.possibleMatches" 
                        :key="match.id"
                        class="match-option card mb-2"
                        :class="{'border-success': match.similarity >= 90, 'selected': item.selectedMatchId == match.id}"
                      >
                        <div class="card-body p-3">
                          <div class="row align-items-center">
                            <div class="col-auto">
                              <input 
                                type="radio" 
                                :name="`decision-${item.rowNumber}`"
                                :value="match.id"
                                v-model="item.selectedMatchId"
                                :id="`match-${item.rowNumber}-${match.id}`"
                              />
                            </div>
                            <div class="col-auto">
                              <img 
                                :src="getMatchImageUrl(match)"
                                class="match-image"
                                @error="onImageError"
                              />
                            </div>
                            <div class="col">
                              <label :for="`match-${item.rowNumber}-${match.id}`" class="mb-0 w-100 cursor-pointer">
                                <div class="d-flex justify-content-between align-items-start">
                                  <div>
                                    <strong>{{ match.listingName }}</strong>
                                    <span v-if="match.variant" class="text-muted ms-1">({{ match.variant }})</span>
                                    <br>
                                    <small class="text-muted">
                                      <span v-if="match.producerName">{{ match.producerName }}</span>
                                      <span v-if="match.drinkType"> | {{ match.drinkType }}</span>
                                      <span v-if="match.originCountry"> | {{ match.originCountry }}</span>
                                      <span v-if="match.abv"> | {{ match.abv }}% ABV</span>
                                    </small>
                                  </div>
                                  <div class="text-end">
                                    <span 
                                      class="badge"
                                      :class="{
                                        'bg-success': match.similarity >= 90,
                                        'bg-info': match.similarity >= 80 && match.similarity < 90,
                                        'bg-warning': match.similarity < 80
                                      }"
                                    >
                                      {{ match.similarity }}% match
                                    </span>
                                  </div>
                                </div>
                              </label>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <!-- Create New Option -->
                      <div class="match-option card mb-2">
                        <div class="card-body p-3">
                          <label class="mb-0 w-100 cursor-pointer">
                            <input 
                              type="radio" 
                              :name="`decision-${item.rowNumber}`"
                              value="create_new"
                              v-model="item.selectedMatchId"
                              class="me-2"
                            />
                            <strong>None of these - Create as new drink</strong>
                            <br>
                            <small class="text-muted ms-4">
                              This will add a new drink to the Drink-X database
                            </small>
                          </label>
                        </div>
                      </div>
                      
                      <!-- Skip Option -->
                      <div class="match-option card">
                        <div class="card-body p-3">
                          <label class="mb-0 w-100 cursor-pointer">
                            <input 
                              type="radio" 
                              :name="`decision-${item.rowNumber}`"
                              value="skip"
                              v-model="item.selectedMatchId"
                              class="me-2"
                            />
                            <strong>Skip this row</strong>
                            <br>
                            <small class="text-muted ms-4">
                              This item will not be imported
                            </small>
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Pagination for Review Items -->
            <nav v-if="totalReviewPages > 1" class="mt-4">
              <ul class="pagination justify-content-center">
                <li class="page-item" :class="{ disabled: currentReviewPage === 1 }">
                  <button class="page-link" @click="currentReviewPage--" :disabled="currentReviewPage === 1">
                    Previous
                  </button>
                </li>
                <li 
                  class="page-item" 
                  :class="{ active: page === currentReviewPage }"
                  v-for="page in visibleReviewPages" 
                  :key="page"
                >
                  <button class="page-link" @click="currentReviewPage = page">
                    {{ page }}
                  </button>
                </li>
                <li class="page-item" :class="{ disabled: currentReviewPage === totalReviewPages }">
                  <button class="page-link" @click="currentReviewPage++" :disabled="currentReviewPage === totalReviewPages">
                    Next
                  </button>
                </li>
              </ul>
            </nav>
            
            <div class="d-flex justify-content-between mt-4">
              <button class="btn btn-secondary" @click="currentStep = 2">
                <i class="bi bi-arrow-left me-2"></i>Back
              </button>
              <button 
                class="btn btn-success btn-lg"
                @click="proceedToImport"
                :disabled="!allItemsHaveDecisions"
              >
                <i class="bi bi-check-circle me-2"></i>
                Import {{ itemsToImportCount }} Items
              </button>
            </div>
          </div>
          
          <!-- Step 4: Import Progress & Results -->
          <div v-if="currentStep === 4" class="step-content">
            <div class="text-center">
              <div v-if="importing" class="importing-state">
                <div class="spinner-border text-primary mb-3" style="width: 4rem; height: 4rem;"></div>
                <h4>Importing Your Items...</h4>
                <p class="text-muted">This may take a moment. Please don't close this window.</p>
              </div>
              
              <div v-else-if="importComplete" class="import-complete">
                <div class="success-icon mb-4">
                  <i class="bi bi-check-circle-fill text-success" style="font-size: 5rem;"></i>
                </div>
                <h4 class="mb-3">Import Complete!</h4>
                
                <div class="import-summary">
                  <div class="row text-center">
                    <div class="col-md-3">
                      <div class="card">
                        <div class="card-body">
                          <h2 class="text-primary mb-0">{{ importResults.importedCount }}</h2>
                          <small class="text-muted">Items Imported</small>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <div class="card">
                        <div class="card-body">
                          <h2 class="text-success mb-0">{{ importResults.createdListingsCount }}</h2>
                          <small class="text-muted">New Drinks Created</small>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <div class="card">
                        <div class="card-body">
                          <h2 class="text-warning mb-0">{{ importResults.skippedCount }}</h2>
                          <small class="text-muted">Items Skipped</small>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <div class="card">
                        <div class="card-body">
                          <h2 class="text-danger mb-0">{{ importResults.errorCount }}</h2>
                          <small class="text-muted">Errors</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Error Details -->
                <div v-if="importResults.errors && importResults.errors.length > 0" class="mt-4">
                  <div class="alert alert-warning text-start">
                    <h6 class="alert-heading">
                      <i class="bi bi-exclamation-triangle me-2"></i>
                      Some items had errors:
                    </h6>
                    <ul class="mb-0">
                      <li v-for="(error, idx) in importResults.errors" :key="idx">
                        Row {{ error.rowNumber }}: {{ error.error }}
                      </li>
                    </ul>
                  </div>
                </div>
                
                <div class="mt-4">
                  <button 
                    class="btn btn-primary btn-lg"
                    data-bs-dismiss="modal"
                    @click="closeAndReload"
                  >
                    <i class="bi bi-check-lg me-2"></i>
                    Done
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'CsvImportModal',
    props: {
        ownerType: {
        type: String,
        required: true
        },
        ownerId: {
        type: String,
        required: true
        },
        collections: {
        type: Array,
        required: true
        }
    },
    data() {
        return {
            currentStep: 1,
            selectedFile: null,
            uploading: false,
            processing: false,
            importing: false,
            importComplete: false,
            
            // CSV Data
            csvHeaders: [],
            csvSampleData: [],
            totalRows: 0,
            
            // Column Mapping - Initialize as empty object (Vue 3 will track it)
            columnMapping: {},
            
            // Duplicate Detection
            reviewItems: [],
            currentReviewPage: 1,
            itemsPerReviewPage: 5,
            
            // Import Results
            importResults: {
            importedCount: 0,
            createdListingsCount: 0,
            skippedCount: 0,
            errorCount: 0,
            errors: []
            },
            
            // Selected collection for import
            selectedCollectionId: null
        }
    },
    computed: {
        stepTitle() {
        const titles = {
            1: 'Upload CSV',
            2: 'Map Columns',
            3: 'Review Duplicates',
            4: 'Import Complete'
        }
        return titles[this.currentStep] || ''
        },
        
        progressPercentage() {
        return (this.currentStep / 4) * 100
        },
        
        progressBarClass() {
        if (this.currentStep === 4 && this.importComplete) {
            return 'bg-success'
        }
        return 'bg-primary'
        },
        
        hasRequiredMapping() {
        return Object.values(this.columnMapping).includes('listingName')
        },
        
        totalItems() {
        return this.reviewItems.length
        },
        
        itemsWithMatches() {
        return this.reviewItems.filter(item => 
            item.possibleMatches && item.possibleMatches.length > 0
        ).length
        },
        
        allItemsHaveDecisions() {
        return this.reviewItems.every(item => item.selectedMatchId)
        },
        
        itemsToImportCount() {
        return this.reviewItems.filter(item => item.selectedMatchId !== 'skip').length
        },
        
        // Review pagination
        totalReviewPages() {
        return Math.ceil(this.reviewItems.length / this.itemsPerReviewPage)
        },
        
        paginatedReviewItems() {
        const start = (this.currentReviewPage - 1) * this.itemsPerReviewPage
        const end = start + this.itemsPerReviewPage
        return this.reviewItems.slice(start, end)
        },
        
        visibleReviewPages() {
        const pages = []
        const maxVisible = 5
        let start = Math.max(1, this.currentReviewPage - Math.floor(maxVisible / 2))
        let end = Math.min(this.totalReviewPages, start + maxVisible - 1)
        
        if (end - start + 1 < maxVisible) {
            start = Math.max(1, end - maxVisible + 1)
        }
        
        for (let i = start; i <= end; i++) {
            pages.push(i)
        }
        return pages
        }
    },
    methods: {
        getApiBaseUrl() {
        return process.env.VUE_APP_API_URL || (process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '')
        },
        
        handleFileSelect(event) {
        const file = event.target.files[0]
        if (file && file.name.endsWith('.csv')) {
            this.selectedFile = file
        } else {
            alert('Please select a valid CSV file')
        }
        },
        
        formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes'
        const k = 1024
        const sizes = ['Bytes', 'KB', 'MB']
        const i = Math.floor(Math.log(bytes) / Math.log(k))
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
        },
        
        async uploadAndParseCSV() {
        if (!this.selectedFile) return
        
        this.uploading = true
        
        try {
            const formData = new FormData()
            formData.append('file', this.selectedFile)
            
            const baseUrl = this.getApiBaseUrl()
            const response = await axios.post(`${baseUrl}/cellarImport/parseCsvPreview`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
            })
            
            if (response.data.code === 200) {
            this.csvHeaders = response.data.data.headers
            this.csvSampleData = response.data.data.sampleData
            this.totalRows = response.data.data.totalRows
            
            // Auto-map columns with common names
            this.autoMapColumns()
            
            this.currentStep = 2
            } else {
            throw new Error(response.data.message || 'Failed to parse CSV')
            }
        } catch (error) {
            console.error('Error parsing CSV:', error)
            alert(`Error parsing CSV: ${error.response?.data?.message || error.message}`)
        } finally {
            this.uploading = false
        }
        },
        
        autoMapColumns() {
          const commonMappings = {
            // Drink names - expanded
            'name': 'listingName',
            'drink name': 'listingName',
            'drink': 'listingName',
            'wine name': 'listingName',
            'wine': 'listingName',
            'bottle name': 'listingName',
            'bottle': 'listingName',
            'listing': 'listingName',
            'product': 'listingName',
            'product name': 'listingName',
            'title': 'listingName',
            
            // Producer - expanded
            'producer': 'producerName',
            'producer name': 'producerName',
            'winery': 'producerName',
            'distillery': 'producerName',
            'brewery': 'producerName',
            'maker': 'producerName',
            'brand': 'producerName',
            'manufacturer': 'producerName',
            'estate': 'producerName',
            'chateau': 'producerName',
            'château': 'producerName',
            
            // Vintage - expanded
            'vintage': 'variant',
            'year': 'variant',
            'vintage year': 'variant',
            
            // Type
            'type': 'drinkType',
            'drink type': 'drinkType',
            'style': 'drinkType',
            'category': 'typeCategory',
            'sub-category': 'typeCategory',
            'subcategory': 'typeCategory',
            
            // Country
            'country': 'originCountry',
            'origin': 'originCountry',
            'region': 'originCountry',
            'country of origin': 'originCountry',
            
            // Quantity - expanded
            'quantity': 'quantity',
            'qty': 'quantity',
            'count': 'quantity',
            'bottles': 'quantity',
            'amount': 'quantity',
            'number': 'quantity',
            '# bottles': 'quantity',
            'bottle count': 'quantity',
            
            // Price - expanded
            'price': 'purchasePrice',
            'cost': 'purchasePrice',
            'paid': 'purchasePrice',
            'purchase price': 'purchasePrice',
            'amount paid': 'purchasePrice',
            'value': 'purchasePrice',
            
            // Volume
            'size': 'volumeNumber',
            'volume': 'volumeNumber',
            'bottle size': 'volumeNumber',
            'ml': 'volumeNumber',
            'unit': 'volumeUnit',
            'volume unit': 'volumeUnit',
            
            // Format
            'format': 'drinkFormat',
            'bottle format': 'drinkFormat',
            'container': 'drinkFormat',
            
            // Location - expanded
            'location': 'currentLocation',
            'storage': 'currentLocation',
            'cellar': 'currentLocation',
            'stored at': 'currentLocation',
            'where': 'currentLocation',
            'bin': 'subLocation',
            'rack': 'subLocation',
            'shelf': 'subLocation',
            'position': 'subLocation',
            
            // Dates
            'purchase date': 'purchaseDate',
            'bought': 'purchaseDate',
            'date purchased': 'purchaseDate',
            'delivery': 'deliveryDate',
            'delivered': 'deliveryDate',
            'drink from': 'drinkOnwardsDate',
            'ready': 'drinkOnwardsDate',
            'drink by': 'drinkByDate',
            'drink until': 'drinkByDate',
            'best before': 'drinkByDate',
            
            // Notes - expanded
            'notes': 'noteToSelf',
            'comments': 'noteToSelf',
            'description': 'noteToSelf',
            'note': 'noteToSelf',
            'comment': 'noteToSelf',
            'tasting notes': 'noteToSelf',
            
            // Status
            'status': 'status',
            'condition': 'consumption',
            'opened': 'consumption',
            'state': 'consumption'
          }
          
          // Try to auto-map with case-insensitive and trim
          this.csvHeaders.forEach(header => {
            const normalized = header.toLowerCase().trim()
            if (commonMappings[normalized]) {
              this.columnMapping[header] = commonMappings[normalized]
            }
          })
          
          // Force reactivity
          this.columnMapping = { ...this.columnMapping }
        },
        
        getSampleDataForColumn(header) {
        if (!this.csvSampleData || this.csvSampleData.length === 0) return ''
        
        const samples = this.csvSampleData
            .map(row => row[header])
            .filter(val => val && String(val).trim() !== '')
            .slice(0, 3)
        
        return samples.join(', ') || 'No data'
        },
        
        async processCSVWithMapping() {
        if (!this.hasRequiredMapping) {
            alert('Please map at least the "Drink Name" field')
            return
        }
        
        // Check if collection is selected
        if (!this.selectedCollectionId) {
            const defaultCollection = this.collections.find(c => c.isDefault)
            this.selectedCollectionId = defaultCollection ? defaultCollection.id : this.collections[0].id
        }
        
        this.processing = true
        
        try {
            const formData = new FormData()
            formData.append('file', this.selectedFile)
            formData.append('columnMapping', JSON.stringify(this.columnMapping))
            formData.append('threshold', '85')  // 85% similarity threshold
            
            const baseUrl = this.getApiBaseUrl()
            const response = await axios.post(
            `${baseUrl}/cellarImport/processAndDetectDuplicates`, 
            formData,
            { headers: { 'Content-Type': 'multipart/form-data' } }
            )
            
            if (response.data.code === 200) {
            this.reviewItems = response.data.data.items.map(item => ({
                ...item,
                selectedMatchId: this.getDefaultSelection(item)
            }))
            
            this.currentStep = 3
            } else {
            throw new Error(response.data.message || 'Failed to process CSV')
            }
        } catch (error) {
            console.error('Error processing CSV:', error)
            alert(`Error processing CSV: ${error.response?.data?.message || error.message}`)
        } finally {
            this.processing = false
        }
        },
        
        getDefaultSelection(item) {
        // Auto-select high confidence matches (>90%)
        if (item.possibleMatches && item.possibleMatches.length > 0) {
            const bestMatch = item.possibleMatches[0]
            if (bestMatch.similarity >= 90) {
            return bestMatch.id
            }
        }
        
        // Default to create new if no high confidence match
        return 'create_new'
        },
        
        acceptAllHighConfidence() {
        this.reviewItems.forEach(item => {
            if (item.possibleMatches && item.possibleMatches.length > 0) {
            const bestMatch = item.possibleMatches[0]
            if (bestMatch.similarity >= 90) {
                item.selectedMatchId = bestMatch.id
            }
            }
        })
        },
        
        createAllNew() {
        this.reviewItems.forEach(item => {
            item.selectedMatchId = 'create_new'
        })
        },
        
        getMatchImageUrl(match) {
        const baseUrl = this.getApiBaseUrl()
        if (match.photo) {
            if (match.photo.startsWith('http')) {
            return match.photo
            }
            return `${baseUrl}${match.photo.startsWith('/') ? '' : '/'}${match.photo}`
        }
        return 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739'
        },
        
        onImageError(event) {
        event.target.src = 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739'
        },
        
        async proceedToImport() {
        if (!this.allItemsHaveDecisions) {
            alert('Please make a decision for all items')
            return
        }
        
        this.currentStep = 4
        this.importing = true
        
        try {
            const itemsToImport = this.reviewItems.filter(item => item.selectedMatchId !== 'skip')
            
            const baseUrl = this.getApiBaseUrl()
            const response = await axios.post(`${baseUrl}/cellarImport/importCellarCsv`, {
            ownerType: this.ownerType,
            ownerId: this.ownerId,
            collectionId: this.selectedCollectionId,
            items: itemsToImport
            })
            
            if (response.data.code === 200) {
            this.importResults = response.data.data
            this.importComplete = true
            } else {
            throw new Error(response.data.message || 'Import failed')
            }
        } catch (error) {
            console.error('Error importing:', error)
            alert(`Error importing: ${error.response?.data?.message || error.message}`)
            this.currentStep = 3  // Go back to review step
        } finally {
            this.importing = false
        }
        },
        
        closeAndReload() {
        this.$emit('import-complete')
        this.resetImport()
        },
        
        resetImport() {
        this.currentStep = 1
        this.selectedFile = null
        this.csvHeaders = []
        this.csvSampleData = []
        this.columnMapping = {}
        this.reviewItems = []
        this.importComplete = false
        this.importResults = {
            importedCount: 0,
            createdListingsCount: 0,
            skippedCount: 0,
            errorCount: 0,
            errors: []
        }
        
        // Reset file input
        if (this.$refs.fileInput) {
            this.$refs.fileInput.value = ''
        }
        }
    }
}
</script>

<style scoped>
.step-content {
  min-height: 400px;
}

.upload-area {
  border: 2px dashed #dee2e6;
  border-radius: 0.5rem;
  padding: 2rem;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: #0d6efd;
  background-color: #f8f9fa;
}

.upload-label {
  display: inline-block;
  padding: 0.75rem 2rem;
  background-color: #0d6efd;
  color: white;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.upload-label:hover {
  background-color: #0b5ed7;
}

.column-mapping-table {
  font-size: 0.9rem;
}

.column-mapping-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.review-item {
  transition: all 0.2s ease;
}

.review-item:hover {
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1);
}

.match-option {
  cursor: pointer;
  transition: all 0.2s ease;
}

.match-option:hover {
  background-color: #f8f9fa;
}

.match-option.selected {
  border-color: #0d6efd !important;
  background-color: #e7f3ff;
}

.match-image {
  width: 60px;
  height: 60px;
  object-fit: contain;
  border-radius: 0.25rem;
  border: 1px solid #dee2e6;
}

.cursor-pointer {
  cursor: pointer;
}

.import-summary .card {
  border: none;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

@media (max-width: 768px) {
  .column-mapping-table {
    font-size: 0.8rem;
  }
  
  .match-image {
    width: 50px;
    height: 50px;
  }
  
  .import-summary .col-md-3 {
    margin-bottom: 1rem;
  }
}
</style>