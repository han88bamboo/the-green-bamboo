<template>
    <teleport to="body">
        <!-- Menu History Modal -->
        <div class="modal fade" id="menuHistoryModal" tabindex="-1" 
             aria-labelledby="menuHistoryModalLabel" aria-hidden="true" 
             data-bs-backdrop="static">
            <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content">
                    
                    <!-- Modal Header -->
                    <div class="modal-header" style="background-color:#83a9e8">
                        <h5 class="modal-title fw-bold" id="menuHistoryModalLabel" style="color: white;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" 
                                 class="bi bi-clock-history me-2" viewBox="0 0 16 16">
                                <path d="M8.515 1.019A7 7 0 0 0 8 1V0a8 8 0 0 1 .589.022l-.074.997zm2.004.45a7.003 7.003 0 0 0-.985-.299l.219-.976c.383.086.76.2 1.126.342l-.36.933zm1.37.71a7.01 7.01 0 0 0-.439-.27l.493-.87a8.025 8.025 0 0 1 .979.654l-.615.789a6.996 6.996 0 0 0-.418-.302zm1.834 1.79a6.99 6.99 0 0 0-.653-.796l.724-.69c.27.285.52.59.747.91l-.818.576zm.744 1.352a7.08 7.08 0 0 0-.214-.468l.893-.45a7.976 7.976 0 0 1 .45 1.088l-.95.313a7.023 7.023 0 0 0-.179-.483zm.53 2.507a6.991 6.991 0 0 0-.1-1.025l.985-.17c.067.386.106.778.116 1.17l-1 .025zm-.131 1.538c.033-.17.06-.339.081-.51l.993.123a7.957 7.957 0 0 1-.23 1.155l-.964-.267c.046-.165.086-.332.12-.501zm-.952 2.379c.184-.29.346-.594.486-.908l.914.405c-.16.36-.345.706-.555 1.038l-.845-.535zm-.964 1.205c.122-.122.239-.248.35-.378l.758.653a8.073 8.073 0 0 1-.401.432l-.707-.707z"/>
                                <path d="M8 1a7 7 0 1 0 4.95 11.95l.707.707A8.001 8.001 0 1 1 8 0v1z"/>
                                <path d="M7.5 3a.5.5 0 0 1 .5.5v5.21l3.248 1.856a.5.5 0 0 1-.496.868l-3.5-2A.5.5 0 0 1 7 9V3.5a.5.5 0 0 1 .5-.5z"/>
                            </svg>
                            Menu History
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" 
                                aria-label="Close" @click="resetModal"></button>
                    </div>

                    <!-- Modal Body -->
                    <div class="modal-body">
                        
                        <!-- Loading State -->
                        <div v-if="isLoading" class="text-center py-5">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <p class="mt-3 text-muted">Loading menu history...</p>
                        </div>

                        <!-- Error State -->
                        <div v-else-if="errorMessage" class="alert alert-danger" role="alert">
                            <strong>Error:</strong> {{ errorMessage }}
                            <button class="btn btn-sm btn-outline-danger ms-3" @click="loadHistory">
                                Retry
                            </button>
                        </div>

                        <!-- Empty State -->
                        <div v-else-if="!historyVersions.length" class="text-center py-5">
                            <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" fill="#ccc" 
                                 class="bi bi-inbox mb-3" viewBox="0 0 16 16">
                                <path d="M4.98 4a.5.5 0 0 0-.39.188L1.54 8H6a.5.5 0 0 1 .5.5 1.5 1.5 0 1 0 3 0A.5.5 0 0 1 10 8h4.46l-3.05-3.812A.5.5 0 0 0 11.02 4H4.98zm9.954 5H10.45a2.5 2.5 0 0 1-4.9 0H1.066l.432 2.592a1 1 0 0 0 .986.838h10.032a1 1 0 0 0 .986-.838L13.934 9z"/>
                                <path d="M13.846 3.398a.5.5 0 0 0-.39-.188H2.544a.5.5 0 0 0-.39.188L.544 5.798l-.024.03A5.52 5.52 0 0 0 0 8.5v.23a1 1 0 0 0 .119.474l.018.03L.5 10H6a.5.5 0 0 1 .5.5 1.5 1.5 0 0 0 3 0 .5.5 0 0 1 .5-.5h5.5l.363-.767.018-.03A1 1 0 0 0 16 8.73V8.5a5.52 5.52 0 0 0-.52-2.302l-.024-.03-1.61-2.77z"/>
                            </svg>
                            <h5 class="text-muted">No Menu History Yet</h5>
                            <p class="text-muted">Menu snapshots will appear here after you save changes to your menu.</p>
                        </div>

                        <!-- History List View -->
                        <div v-else-if="!selectedVersion" class="history-list">
                            <p class="text-muted mb-3">
                                <small>Select a version to preview and restore items from your menu history.</small>
                            </p>
                            
                            <div class="list-group">
                                <button v-for="version in historyVersions" :key="version.versionId"
                                        type="button" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                                        @click="loadSnapshotDetails(version.versionId)">
                                    <div>
                                        <h6 class="mb-1">
                                            {{ formatDate(version.snapshotTimestamp) }}
                                        </h6>
                                        <small class="text-muted">
                                            {{ version.sectionsCount }} sections, {{ version.itemsCount }} items
                                        </small>
                                    </div>
                                    <span class="badge bg-primary rounded-pill">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" 
                                             class="bi bi-eye" viewBox="0 0 16 16">
                                            <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
                                            <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
                                        </svg>
                                        Preview
                                    </span>
                                </button>
                            </div>
                        </div>

                        <!-- Snapshot Detail View (Accordion Preview) -->
                        <div v-else class="snapshot-detail">
                            <!-- Back Button & Version Info -->
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <button class="btn btn-outline-secondary btn-sm" @click="selectedVersion = null; snapshotDetails = null">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" 
                                         class="bi bi-arrow-left me-1" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd" d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8z"/>
                                    </svg>
                                    Back to Versions
                                </button>
                                <span class="badge bg-info text-dark">
                                    {{ formatDate(snapshotDetails?.snapshotTimestamp) }}
                                </span>
                            </div>

                            <!-- Restore Options -->
                            <div class="card mb-3 border-warning">
                                <div class="card-header bg-warning-subtle">
                                    <strong>Restore Options</strong>
                                </div>
                                <div class="card-body">
                                    <div class="row g-2">
                                        <div class="col-md-6">
                                            <label class="form-label small">Restore Type:</label>
                                            <select class="form-select form-select-sm" v-model="restoreType">
                                                <option value="">-- Select what to restore --</option>
                                                <option value="full">Entire Menu (All Sections)</option>
                                                <option value="section">Selected Sections Only</option>
                                                <option value="item">Selected Items Only</option>
                                            </select>
                                        </div>
                                        <div class="col-md-6" v-if="restoreType === 'item' || restoreType === 'subsection'">
                                            <label class="form-label small">Target Section (restore into):</label>
                                            <select class="form-select form-select-sm" v-model="targetSectionId">
                                                <option value="">-- Select target section --</option>
                                                <option v-for="section in currentMenuSections" :key="section.id" :value="section.id">
                                                    {{ section.sectionName }}
                                                </option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="mt-2">
                                        <small class="text-muted">
                                            <strong>Note:</strong> Restored items are added to your current menu (nothing is deleted).
                                            Restored sections will have "(Restored from Menu History)" added to their name.
                                            Duplicate items will be skipped.
                                        </small>
                                    </div>
                                </div>
                            </div>

                            <!-- Loading Snapshot Details -->
                            <div v-if="isLoadingDetails" class="text-center py-4">
                                <div class="spinner-border spinner-border-sm text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                                <span class="ms-2">Loading snapshot details...</span>
                            </div>

                            <!-- Snapshot Accordion -->
                            <div v-else-if="snapshotDetails" class="accordion" id="snapshotAccordion">
                                <!-- Main Sections -->
                                <div v-for="(section, sIndex) in snapshotDetails.sections" :key="section.sectionSnapshotId"
                                     class="accordion-item">
                                    <h2 class="accordion-header">
                                        <button class="accordion-button" 
                                                :class="{ collapsed: !expandedSections.has(section.sectionSnapshotId) }"
                                                type="button" 
                                                @click="toggleSection(section)">
                                            <div class="d-flex align-items-center w-100">
                                                <!-- Section Checkbox -->
                                                <input v-if="restoreType === 'section'" 
                                                       type="checkbox" class="form-check-input me-2"
                                                       :checked="selectedSectionIds.includes(section.originalSectionId)"
                                                       @click.stop
                                                       @change="toggleSectionSelection(section.originalSectionId)">
                                                
                                                <strong class="me-auto">{{ section.sectionName }}</strong>
                                                <span class="badge bg-secondary ms-2">
                                                    {{ section.itemCount }} items
                                                </span>
                                                <span v-if="section.subsections?.length" class="badge bg-info ms-1">
                                                    {{ section.subsections.length }} subsections
                                                </span>
                                            </div>
                                        </button>
                                    </h2>
                                    <div class="accordion-collapse" 
                                         :class="{ collapse: !expandedSections.has(section.sectionSnapshotId), show: expandedSections.has(section.sectionSnapshotId) }">
                                        <div class="accordion-body">
                                            <!-- Section Description -->
                                            <p v-if="section.sectionDescription" class="text-muted fst-italic small mb-3">
                                                {{ section.sectionDescription }}
                                            </p>

                                            <!-- Section Items -->
                                            <div v-if="section.items?.length" class="mb-3">
                                                <h6 class="text-muted mb-2">Items in this section:</h6>
                                                <div class="table-responsive">
                                                    <table class="table table-sm table-hover">
                                                        <thead>
                                                            <tr>
                                                                <th v-if="restoreType === 'item'" style="width: 30px;">
                                                                    <input type="checkbox" class="form-check-input"
                                                                           @change="toggleAllItemsInSection(section)">
                                                                </th>
                                                                <th>Name</th>
                                                                <th>Price</th>
                                                                <th>Vintage</th>
                                                                <th>Status</th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            <tr v-for="item in section.items" :key="item.itemSnapshotId">
                                                                <td v-if="restoreType === 'item'">
                                                                    <input type="checkbox" class="form-check-input"
                                                                           :checked="selectedItemIds.includes(item.itemSnapshotId)"
                                                                           @change="toggleItemSelection(item.itemSnapshotId)">
                                                                </td>
                                                                <td>{{ item.itemName || 'Unknown Item' }}</td>
                                                                <td>
                                                                    <span v-if="item.price">
                                                                        {{ item.currency || '$' }}{{ item.price.toFixed(2) }}
                                                                    </span>
                                                                    <span v-else class="text-muted">-</span>
                                                                </td>
                                                                <td>
                                                                    <span v-if="item.vintage">{{ item.vintage }}</span>
                                                                    <span v-else class="text-muted">-</span>
                                                                </td>
                                                                <td>
                                                                    <span v-if="item.isAvailable" class="badge bg-success">Available</span>
                                                                    <span v-else class="badge bg-secondary">Unavailable</span>
                                                                    <span v-if="item.isFeatured" class="badge bg-warning ms-1">Featured</span>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </div>
                                            </div>
                                            <div v-else class="text-muted small mb-3">
                                                <em>No items in this section</em>
                                            </div>

                                            <!-- Nested Subsections -->
                                            <div v-if="section.subsections?.length" class="ms-3">
                                                <h6 class="text-muted mb-2">Subsections:</h6>
                                                <div class="accordion accordion-flush" :id="'subsectionAccordion' + sIndex">
                                                    <div v-for="subsection in section.subsections" :key="subsection.sectionSnapshotId"
                                                         class="accordion-item border">
                                                        <h2 class="accordion-header">
                                                            <button class="accordion-button collapsed py-2" 
                                                                    type="button"
                                                                    @click="toggleSubsection(subsection)">
                                                                <div class="d-flex align-items-center w-100">
                                                                    <input v-if="restoreType === 'section'" 
                                                                           type="checkbox" class="form-check-input me-2"
                                                                           :checked="selectedSectionIds.includes(subsection.originalSectionId)"
                                                                           @click.stop
                                                                           @change="toggleSectionSelection(subsection.originalSectionId)">
                                                                    <span class="me-auto">{{ subsection.sectionName }}</span>
                                                                    <span class="badge bg-secondary ms-2">{{ subsection.itemCount }} items</span>
                                                                </div>
                                                            </button>
                                                        </h2>
                                                        <div class="accordion-collapse"
                                                             :class="{ collapse: !expandedSubsections.has(subsection.sectionSnapshotId), show: expandedSubsections.has(subsection.sectionSnapshotId) }">
                                                            <div class="accordion-body py-2">
                                                                <!-- Subsection Items Table -->
                                                                <div v-if="subsection.items?.length" class="table-responsive">
                                                                    <table class="table table-sm table-hover mb-0">
                                                                        <thead>
                                                                            <tr>
                                                                                <th v-if="restoreType === 'item'" style="width: 30px;">
                                                                                    <input type="checkbox" class="form-check-input"
                                                                                           @change="toggleAllItemsInSection(subsection)">
                                                                                </th>
                                                                                <th>Name</th>
                                                                                <th>Price</th>
                                                                                <th>Vintage</th>
                                                                            </tr>
                                                                        </thead>
                                                                        <tbody>
                                                                            <tr v-for="item in subsection.items" :key="item.itemSnapshotId">
                                                                                <td v-if="restoreType === 'item'">
                                                                                    <input type="checkbox" class="form-check-input"
                                                                                           :checked="selectedItemIds.includes(item.itemSnapshotId)"
                                                                                           @change="toggleItemSelection(item.itemSnapshotId)">
                                                                                </td>
                                                                                <td>{{ item.itemName || 'Unknown Item' }}</td>
                                                                                <td>
                                                                                    <span v-if="item.price">{{ item.currency || '$' }}{{ item.price.toFixed(2) }}</span>
                                                                                    <span v-else class="text-muted">-</span>
                                                                                </td>
                                                                                <td>
                                                                                    <span v-if="item.vintage">{{ item.vintage }}</span>
                                                                                    <span v-else class="text-muted">-</span>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </div>
                                                                <div v-else class="text-muted small">
                                                                    <em>No items in this subsection</em>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Restore Result Message -->
                        <div v-if="restoreResult" class="mt-3">
                            <div :class="['alert', restoreResult.success ? 'alert-success' : 'alert-danger']">
                                <h6 class="alert-heading">{{ restoreResult.success ? 'Restore Completed!' : 'Restore Failed' }}</h6>
                                <p v-if="restoreResult.message">{{ restoreResult.message }}</p>
                                <div v-if="restoreResult.restoredSections?.length">
                                    <strong>Restored Sections:</strong>
                                    <ul class="mb-0">
                                        <li v-for="name in restoreResult.restoredSections" :key="name">{{ name }}</li>
                                    </ul>
                                </div>
                                <div v-if="restoreResult.restoredItems?.length" class="mt-2">
                                    <strong>Restored Items:</strong> {{ restoreResult.restoredItems.length }} items
                                </div>
                                <div v-if="restoreResult.skippedItems?.length" class="mt-2 text-warning">
                                    <strong>Skipped (duplicates):</strong> {{ restoreResult.skippedItems.length }} items
                                    <ul class="mb-0 small">
                                        <li v-for="skip in restoreResult.skippedItems.slice(0, 5)" :key="skip.name">
                                            {{ skip.name }} - {{ skip.reason }}
                                        </li>
                                        <li v-if="restoreResult.skippedItems.length > 5">
                                            ... and {{ restoreResult.skippedItems.length - 5 }} more
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Modal Footer -->
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="resetModal">
                            Close
                        </button>
                        <button v-if="selectedVersion && canRestore" 
                                type="button" class="btn btn-warning"
                                :disabled="isRestoring"
                                @click="executeRestore">
                            <span v-if="isRestoring">
                                <span class="spinner-border spinner-border-sm me-1" role="status"></span>
                                Restoring...
                            </span>
                            <span v-else>
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" 
                                     class="bi bi-arrow-counterclockwise me-1" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M8 3a5 5 0 1 1-4.546 2.914.5.5 0 0 0-.908-.417A6 6 0 1 0 8 2v1z"/>
                                    <path d="M8 4.466V.534a.25.25 0 0 0-.41-.192L5.23 2.308a.25.25 0 0 0 0 .384l2.36 1.966A.25.25 0 0 0 8 4.466z"/>
                                </svg>
                                Restore Selected
                            </span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </teleport>
</template>

<script>
import { useToast } from 'vue-toastification';

export default {
    name: 'MenuHistoryModal',
    props: {
        venueId: {
            type: [Number, String],
            required: true
        },
        currentMenuSections: {
            type: Array,
            default: () => []
        }
    },
    emits: ['restored'],
    data() {
        return {
            // State
            isLoading: false,
            isLoadingDetails: false,
            isRestoring: false,
            errorMessage: '',
            
            // History data
            historyVersions: [],
            selectedVersion: null,
            snapshotDetails: null,
            
            // Accordion expansion tracking
            expandedSections: new Set(),
            expandedSubsections: new Set(),
            
            // Restore options
            restoreType: '',
            targetSectionId: '',
            selectedSectionIds: [],
            selectedItemIds: [],
            
            // Result
            restoreResult: null
        };
    },
    computed: {
        canRestore() {
            if (!this.restoreType) return false;
            if (this.restoreType === 'full') return true;
            if (this.restoreType === 'section') return this.selectedSectionIds.length > 0;
            if (this.restoreType === 'item') return this.selectedItemIds.length > 0 && this.targetSectionId;
            return false;
        }
    },
    methods: {
        async loadHistory() {
            this.isLoading = true;
            this.errorMessage = '';
            
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/menuHistory/getMenuHistory?venueId=${this.venueId}`
                );
                const result = response.data;
                
                if (result.code === 200) {
                    this.historyVersions = result.data.history;
                } else {
                    this.errorMessage = result.message || 'Failed to load menu history';
                }
            } catch (error) {
                console.error('Error loading menu history:', error);
                this.errorMessage = 'Network error: Could not load menu history';
            } finally {
                this.isLoading = false;
            }
        },
        
        async loadSnapshotDetails(versionId) {
            this.selectedVersion = versionId;
            this.isLoadingDetails = true;
            this.snapshotDetails = null;
            this.expandedSections.clear();
            this.expandedSubsections.clear();
            
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/menuHistory/getSnapshotDetails?versionId=${versionId}&includeItems=true`
                );
                const result = response.data;
                
                if (result.code === 200) {
                    this.snapshotDetails = result.data;
                    // Auto-expand first section
                    if (this.snapshotDetails.sections?.length) {
                        this.expandedSections.add(this.snapshotDetails.sections[0].sectionSnapshotId);
                    }
                } else {
                    this.errorMessage = result.message || 'Failed to load snapshot details';
                }
            } catch (error) {
                console.error('Error loading snapshot details:', error);
                this.errorMessage = 'Network error: Could not load snapshot details';
            } finally {
                this.isLoadingDetails = false;
            }
        },
        
        toggleSection(section) {
            const id = section.sectionSnapshotId;
            if (this.expandedSections.has(id)) {
                this.expandedSections.delete(id);
            } else {
                this.expandedSections.add(id);
                // Lazy load items if not already loaded
                if (!section.items?.length && section.itemCount > 0) {
                    this.loadSectionItems(section);
                }
            }
            // Force reactivity
            this.expandedSections = new Set(this.expandedSections);
        },
        
        toggleSubsection(subsection) {
            const id = subsection.sectionSnapshotId;
            if (this.expandedSubsections.has(id)) {
                this.expandedSubsections.delete(id);
            } else {
                this.expandedSubsections.add(id);
                // Lazy load items if not already loaded
                if (!subsection.items?.length && subsection.itemCount > 0) {
                    this.loadSectionItems(subsection);
                }
            }
            // Force reactivity
            this.expandedSubsections = new Set(this.expandedSubsections);
        },
        
        async loadSectionItems(section) {
            // Lazy loading endpoint call for section items
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/menuHistory/getSnapshotDetails?versionId=${this.selectedVersion}&includeItems=true&sectionId=${section.originalSectionId}`
                );
                const result = response.data;
                
                if (result.code === 200) {
                    // Find the section in our data and update its items
                    const targetSection = this.findSectionById(section.originalSectionId);
                    if (targetSection && result.data.sections?.length) {
                        const loadedSection = result.data.sections.find(s => s.originalSectionId === section.originalSectionId);
                        if (loadedSection) {
                            targetSection.items = loadedSection.items;
                        }
                    }
                }
            } catch (error) {
                console.error('Error loading section items:', error);
            }
        },
        
        findSectionById(originalSectionId) {
            // Search in main sections
            for (const section of this.snapshotDetails.sections || []) {
                if (section.originalSectionId === originalSectionId) {
                    return section;
                }
                // Search in subsections
                for (const subsection of section.subsections || []) {
                    if (subsection.originalSectionId === originalSectionId) {
                        return subsection;
                    }
                }
            }
            return null;
        },
        
        toggleSectionSelection(sectionId) {
            const index = this.selectedSectionIds.indexOf(sectionId);
            if (index === -1) {
                this.selectedSectionIds.push(sectionId);
            } else {
                this.selectedSectionIds.splice(index, 1);
            }
        },
        
        toggleItemSelection(itemId) {
            const index = this.selectedItemIds.indexOf(itemId);
            if (index === -1) {
                this.selectedItemIds.push(itemId);
            } else {
                this.selectedItemIds.splice(index, 1);
            }
        },
        
        toggleAllItemsInSection(section) {
            const itemIds = (section.items || []).map(i => i.itemSnapshotId);
            const allSelected = itemIds.every(id => this.selectedItemIds.includes(id));
            
            if (allSelected) {
                // Deselect all
                this.selectedItemIds = this.selectedItemIds.filter(id => !itemIds.includes(id));
            } else {
                // Select all
                itemIds.forEach(id => {
                    if (!this.selectedItemIds.includes(id)) {
                        this.selectedItemIds.push(id);
                    }
                });
            }
        },
        
        async executeRestore() {
            this.isRestoring = true;
            this.restoreResult = null;
            const toast = useToast();
            
            try {
                const payload = {
                    versionId: this.selectedVersion,
                    venueId: parseInt(this.venueId),
                    restoreType: this.restoreType,
                    targetSectionId: this.targetSectionId ? parseInt(this.targetSectionId) : null,
                    sectionIds: this.selectedSectionIds,
                    itemIds: this.selectedItemIds
                };
                
                const response = await this.$axios.post(
                    `${process.env.VUE_APP_API_URL}/menuHistory/restoreFromSnapshot`,
                    payload
                );
                const result = response.data;
                
                if (result.code === 201) {
                    this.restoreResult = {
                        success: true,
                        ...result.data
                    };
                    toast.success(`Restored ${result.data.totalRestored} items successfully!`);
                    this.$emit('restored');
                } else {
                    this.restoreResult = {
                        success: false,
                        message: result.message || 'Restore failed'
                    };
                    toast.error(result.message || 'Restore failed');
                }
            } catch (error) {
                console.error('Error restoring from snapshot:', error);
                this.restoreResult = {
                    success: false,
                    message: 'Network error: Could not complete restore'
                };
                toast.error('Network error during restore');
            } finally {
                this.isRestoring = false;
            }
        },
        
        formatDate(isoString) {
            if (!isoString) return 'Unknown date';
            const date = new Date(isoString);
            return date.toLocaleString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        },
        
        resetModal() {
            this.selectedVersion = null;
            this.snapshotDetails = null;
            this.restoreType = '';
            this.targetSectionId = '';
            this.selectedSectionIds = [];
            this.selectedItemIds = [];
            this.restoreResult = null;
            this.expandedSections.clear();
            this.expandedSubsections.clear();
        }
    },
    mounted() {
        // Load history when modal is shown
        const modalEl = document.getElementById('menuHistoryModal');
        if (modalEl) {
            modalEl.addEventListener('show.bs.modal', () => {
                this.loadHistory();
            });
        }
    }
};
</script>

<style scoped>
.history-list .list-group-item {
    cursor: pointer;
    transition: background-color 0.2s;
}

.history-list .list-group-item:hover {
    background-color: #f8f9fa;
}

.accordion-button:not(.collapsed) {
    background-color: #e7f1ff;
    color: #0c63e4;
}

.accordion-button:focus {
    box-shadow: none;
    border-color: rgba(0,0,0,.125);
}

.table-sm th, .table-sm td {
    padding: 0.4rem;
    font-size: 0.875rem;
}

.badge {
    font-weight: 500;
}

.form-check-input {
    cursor: pointer;
}

.bg-warning-subtle {
    background-color: #fff3cd !important;
}
</style>
