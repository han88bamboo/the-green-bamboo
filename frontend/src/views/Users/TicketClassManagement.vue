<template>
    <div>
        <NavBar />

        <!-- Display when data is still loading -->
        <div class="text-info-emphasis fst-italic fw-bold fs-5 pt-5" v-if="dataLoaded === false">
            <span>Loading page, please wait...</span>
            <br><br>
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <!-- Display when data fails to load -->
        <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="dataLoaded === null">
            <span>An error occurred while loading this page, please try again!</span>
            <br>
            <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
                <span class="fs-5 fst-italic"> Return to previous page </span>
            </button>
        </div>

        <!-- Main Content -->
        <div v-if="dataLoaded" class="container-fluid px-4 py-3">
            <!-- Header with Back Button -->
            <div class="row border-bottom pb-3 mb-4 shadow-sm">
                <div class="col-12">
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="d-flex align-items-center gap-3">
                            <button class="btn btn-outline-secondary" @click="goBack">
                                <i class="bi bi-arrow-left me-2"></i>Back
                            </button>
                            <div>
                                <h3 class="fw-bold mb-0" style="color:#027562">
                                    Passcodes Management
                                </h3>
                                <small class="text-muted">Create and manage your passcodes for various ticket classes</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Ticket Classes Section -->
            <div class="card mb-4">
                <div class="card-header d-flex justify-content-between align-items-center bg-light">
                    <div>
                        <h5 class="mb-0 fw-bold">
                            <i class="bi bi-ticket-perforated me-2"></i>Ticket Classes
                            <span v-if="hasTicketClassChanges" class="text-danger ms-2 fs-6 fw-normal">
                                <i class="bi bi-exclamation-circle me-1"></i>You Have Unsaved Changes
                            </span>
                        </h5>
                        <small class="text-muted">Define reusable ticket classes with passcodes</small>
                    </div>
                    <div class="d-flex gap-2">
                        <button class="btn btn-success btn-sm" @click="addNewTicketClass" :disabled="savingTicketClasses">
                            <i class="bi bi-plus-circle me-1"></i>Add New
                        </button>
                        <button 
                            class="btn btn-primary btn-sm" 
                            @click="saveTicketClasses" 
                            :disabled="!hasTicketClassChanges || savingTicketClasses"
                        >
                            <span v-if="savingTicketClasses">
                                <span class="spinner-border spinner-border-sm me-1" role="status"></span>
                                Saving...
                            </span>
                            <span v-else>
                                <i class="bi bi-check-lg me-1"></i>Save Changes
                            </span>
                        </button>
                    </div>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive ticket-class-table-wrapper">
                        <table class="table table-bordered table-hover mb-0 ticket-class-table">
                            <thead class="table-light sticky-header">
                                <tr>
                                    <th style="min-width: 150px;">Class Name</th>
                                    <th style="min-width: 140px;">Passcode <small class="text-muted" >(Send this to guests separately)</small></th>
                                    <th style="min-width: 100px;">Total Limit <small class="text-muted" >(Across All Events)</small></th>
                                    <th style="min-width: 100px;">Current Usage</th>
                                    <th style="min-width: 200px;">Description</th>
                                    <th style="min-width: 100px;">Events Using</th>
                                    <th style="min-width: 100px;">Status</th>
                                    <th style="min-width: 100px;">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="ticketClasses.length === 0">
                                    <td colspan="8" class="text-center text-muted py-4">
                                        <i class="bi bi-inbox fs-3 d-block mb-2"></i>
                                        No ticket classes created yet. Click "Add New" to create one.
                                    </td>
                                </tr>
                                <tr 
                                    v-for="(tc, index) in ticketClasses" 
                                    :key="tc.id || 'new-' + index"
                                    :class="{ 
                                        'table-secondary': !tc.isActive, 
                                        'table-info': tc.isNew,
                                        'row-modified': tc.isModified 
                                    }"
                                >
                                    <!-- Class Name - Editable -->
                                    <td 
                                        class="editable-cell"
                                        @click="startEditing(index, 'className')"
                                        :class="{ 'editing': isEditing(index, 'className') }"
                                    >
                                        <template v-if="isEditing(index, 'className')">
                                            <input 
                                                type="text" 
                                                class="form-control form-control-sm inline-edit-input"
                                                v-model="tc.className"
                                                @blur="stopEditing(); markModified(index)"
                                                @keyup.enter="stopEditing(); markModified(index)"
                                                @keyup.escape="stopEditing()"
                                                ref="editInput"
                                                @click.stop
                                                placeholder="e.g., VIP, Early Bird"
                                                maxlength="50"
                                            />
                                        </template>
                                        <template v-else>
                                            <span :class="{ 'text-muted': !tc.className }">
                                                {{ tc.className || '(click to edit)' }}
                                            </span>
                                        </template>
                                    </td>
                                    
                                    <!-- Passcode - Editable with validation -->
                                    <td 
                                        class="editable-cell position-relative"
                                        @click="startEditing(index, 'passcode')"
                                        :class="{ 
                                            'editing': isEditing(index, 'passcode'),
                                            'is-invalid-cell': tc.passcodeError
                                        }"
                                    >
                                        <template v-if="isEditing(index, 'passcode')">
                                            <input 
                                                type="text" 
                                                class="form-control form-control-sm inline-edit-input"
                                                :class="{ 'is-invalid': tc.passcodeError }"
                                                v-model="tc.passcode"
                                                @blur="validatePasscode(index); stopEditing(); markModified(index)"
                                                @keyup.enter="validatePasscode(index); stopEditing(); markModified(index)"
                                                @keyup.escape="stopEditing()"
                                                @input="onPasscodeInput(index)"
                                                ref="editInput"
                                                @click.stop
                                                placeholder="e.g., VIP2025"
                                                maxlength="20"
                                            />
                                            <div v-if="tc.passcodeError" class="invalid-feedback d-block">
                                                {{ tc.passcodeError }}
                                            </div>
                                        </template>
                                        <template v-else>
                                            <span class="font-monospace" :class="{ 'text-muted': !tc.passcode }">
                                                {{ tc.passcode || '(click to edit)' }}
                                            </span>
                                            <i v-if="tc.passcodeError" class="bi bi-exclamation-triangle text-danger ms-1" :title="tc.passcodeError"></i>
                                        </template>
                                    </td>
                                    
                                    <!-- Total Limit - Editable with validation -->
                                    <td 
                                        class="editable-cell"
                                        @click="startEditing(index, 'totalUsageLimit')"
                                        :class="{ 
                                            'editing': isEditing(index, 'totalUsageLimit'),
                                            'is-invalid-cell': tc.limitError
                                        }"
                                    >
                                        <template v-if="isEditing(index, 'totalUsageLimit')">
                                            <input 
                                                type="number" 
                                                class="form-control form-control-sm inline-edit-input inline-edit-number"
                                                :class="{ 'is-invalid': tc.limitError }"
                                                :value="tc.totalUsageLimit || ''"
                                                @input="tc.totalUsageLimit = $event.target.value === '' ? null : Number($event.target.value)"
                                                @blur="validateLimit(index); stopEditing(); markModified(index)"
                                                @keyup.enter="validateLimit(index); stopEditing(); markModified(index)"
                                                @keyup.escape="stopEditing()"
                                                ref="editInput"
                                                @click.stop
                                                min="1"
                                                placeholder="Leave empty for unlimited"
                                            />
                                            <div v-if="tc.limitError" class="invalid-feedback d-block">
                                                {{ tc.limitError }}
                                            </div>
                                        </template>
                                        <template v-else>
                                            <span>
                                                {{ tc.totalUsageLimit === 0 || tc.totalUsageLimit === null ? '∞' : tc.totalUsageLimit }}
                                            </span>
                                            <i v-if="tc.limitError" class="bi bi-exclamation-triangle text-danger ms-1" :title="tc.limitError"></i>
                                        </template>
                                    </td>
                                    
                                    <!-- Current Usage - Read Only -->
                                    <td class="text-center">
                                        <span class="badge" :class="getUsageBadgeClass(tc)">
                                            {{ tc.currentUsage || 0 }}
                                        </span>
                                    </td>
                                    
                                    
                                    <!-- Description - Editable -->
                                    <td 
                                        class="editable-cell"
                                        @click="startEditing(index, 'description')"
                                        :class="{ 'editing': isEditing(index, 'description') }"
                                    >
                                        <template v-if="isEditing(index, 'description')">
                                            <textarea 
                                                class="form-control form-control-sm inline-edit-textarea"
                                                v-model="tc.description"
                                                @blur="stopEditing(); markModified(index)"
                                                @keyup.escape="stopEditing()"
                                                ref="editInput"
                                                @click.stop
                                                rows="2"
                                                placeholder="Optional description..."
                                            ></textarea>
                                        </template>
                                        <template v-else>
                                            <span :class="{ 'text-muted': !tc.description }">
                                                {{ truncateText(tc.description, 30) || '-' }}
                                            </span>
                                        </template>
                                    </td>
                                    
                                    <!-- Events Using - Read Only -->
                                    <td class="text-center">
                                        <span class="badge bg-info">{{ getEventsUsingCount(tc.eventsUsing) }}</span>
                                    </td>
                                    
                                    <!-- Status - Toggle -->
                                    <td 
                                        class="editable-cell text-center"
                                        @click="toggleStatus(index)"
                                    >
                                        <span 
                                            class="badge cursor-pointer"
                                            :class="tc.isActive ? 'bg-success' : 'bg-secondary'"
                                        >
                                            {{ tc.isActive ? 'Active' : 'Inactive' }}
                                        </span>
                                    </td>

                                    <!-- Actions -->
                                    <td class="text-center">
                                        <button 
                                            v-if="tc.isNew"
                                            class="btn btn-outline-danger btn-sm"
                                            @click="removeNewTicketClass(index)"
                                            title="Remove"
                                        >
                                            <i class="bi bi-x-lg"></i>
                                        </button>
                                        <button 
                                            v-else-if="tc.isActive"
                                            class="btn btn-outline-warning btn-sm"
                                            @click="confirmDeactivate(index)"
                                            title="Deactivate"
                                            :disabled="savingTicketClasses"
                                        >
                                            <i class="bi bi-pause-circle"></i>
                                        </button>
                                        <button 
                                            v-else
                                            class="btn btn-outline-success btn-sm"
                                            @click="toggleStatus(index)"
                                            title="Reactivate"
                                            :disabled="savingTicketClasses"
                                        >
                                            <i class="bi bi-play-circle"></i>
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Event Configuration Section -->
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center bg-light">
                    <div>
                        <h5 class="mb-0 fw-bold">
                            <i class="bi bi-calendar-event me-2"></i>Event Ticket Configuration
                            <span v-if="hasEventConfigChanges" class="text-danger ms-2 fs-6 fw-normal">
                                <i class="bi bi-exclamation-circle me-1"></i>You Have Unsaved Changes
                            </span>
                        </h5>
                        <small class="text-muted">Assign ticket classes to events and set per-event limits</small>
                    </div>
                    <button 
                        class="btn btn-primary btn-sm" 
                        @click="saveEventConfigs" 
                        :disabled="!hasEventConfigChanges || savingEventConfigs"
                    >
                        <span v-if="savingEventConfigs">
                            <span class="spinner-border spinner-border-sm me-1" role="status"></span>
                            Saving...
                        </span>
                        <span v-else>
                            <i class="bi bi-check-lg me-1"></i>Save Event Configs
                        </span>
                    </button>
                </div>
                <div class="card-body p-0">
                    <!-- Info banner about Attendance Limit -->
                    <div class="alert alert-info m-3 mb-0 d-flex align-items-start" role="alert">
                        <i class="bi bi-info-circle me-2 mt-1"></i>
                        <div>
                            <strong>How limits work:</strong> Each event's <strong>Attendance Limit</strong> is the maximum total attendees allowed per event. 
                            Ticket class limits (both global and per-event) apply <em>in addition</em> to the event's attendance limit. 
                            For example, an event could have a 100-person Attendance Limit, a 'Class A' ticket with a usage limit of 20 persons, and a 'Class B' ticket without a usage limit. This means only 20 'Class A' attendees can join, but the event can still have up to 100 total attendees (comprised of both 'Class A' and 'Class B' attendees).
                        </div>
                    </div>
                    <div v-if="events.length === 0" class="text-center text-muted py-4">
                        <i class="bi bi-calendar-x fs-3 d-block mb-2"></i>
                        No events found for this organizer.
                    </div>
                    <div v-else class="table-responsive event-config-table-wrapper">
                        <table class="table table-bordered table-hover mb-0 event-config-table">
                            <thead class="table-light sticky-header">
                                <tr>
                                    <th class="sticky-col-event" style="min-width: 280px;">Event</th>
                                    <th style="min-width: 120px;" class="text-center">Attendance Limit</th>
                                    <th 
                                        v-for="tc in activeTicketClasses" 
                                        :key="tc.id"
                                        style="min-width: 180px;"
                                        class="text-center"
                                    >
                                        <div class="d-flex flex-column align-items-center">
                                            <span class="fw-bold">{{ tc.className }}</span>
                                            <small class="text-muted font-monospace">{{ tc.passcode }}</small>
                                        </div>
                                    </th>
                                    <!-- Placeholder column when no ticket classes -->
                                    <th v-if="activeTicketClasses.length === 0" style="min-width: 250px;" class="text-center text-muted">
                                        <i class="bi bi-ticket-perforated me-1"></i>
                                        Ticket Classes
                                        <br>
                                        <small class="fw-normal">(Add ticket classes above to assign them here)</small>
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="event in events" :key="event.id" :class="{ 'row-modified': event.isConfigModified }">
                                    <!-- Event Name (Sticky Column) -->
                                    <td class="sticky-col-event">
                                        <div class="event-info">
                                            <strong>{{ event.eventName }}</strong>
                                            <div class="small text-muted mt-1">
                                                <i class="bi bi-calendar3 me-1"></i>
                                                {{ formatEventDate(event.eventStartDate) }}
                                                <span v-if="event.eventEndDate && event.eventEndDate !== event.eventStartDate">
                                                    - {{ formatEventDate(event.eventEndDate) }}
                                                </span>
                                            </div>
                                            <div v-if="event.eventStartTime || event.eventEndTime" class="small text-muted">
                                                <i class="bi bi-clock me-1"></i>
                                                <span v-if="event.eventStartTime">{{ formatEventTime(event.eventStartTime) }}</span>
                                                <span v-if="event.eventEndTime"> - {{ formatEventTime(event.eventEndTime) }}</span>
                                                <span class="ms-1">(SGT)</span>
                                            </div>
                                        </div>
                                    </td>
                                    
                                    <!-- Attendance Limit Column -->
                                    <td class="text-center align-middle">
                                        <div class="d-flex flex-column align-items-center">
                                            <span class="badge bg-primary fs-6">
                                                {{ event.eventLimit ? event.eventLimit.toLocaleString() : '∞' }}
                                            </span>
                                            <small class="text-muted">{{ event.numAttendees || 0 }} attending</small>
                                        </div>
                                    </td>
                                    
                                    <!-- Ticket Class Columns -->
                                    <td 
                                        v-for="tc in activeTicketClasses" 
                                        :key="'event-' + event.id + '-tc-' + tc.id"
                                        class="text-center ticket-class-config-cell"
                                    >
                                        <div class="d-flex flex-column align-items-center gap-2">
                                            <!-- Enable/Disable Checkbox -->
                                            <div class="form-check">
                                                <input 
                                                    class="form-check-input"
                                                    type="checkbox"
                                                    :id="'enable-' + event.id + '-' + tc.id"
                                                    :checked="isTicketClassEnabled(event, tc.id)"
                                                    @change="toggleTicketClassForEvent(event, tc.id)"
                                                />
                                                <label class="form-check-label small" :for="'enable-' + event.id + '-' + tc.id">
                                                    Enabled
                                                </label>
                                            </div>
                                            
                                            <!-- Per-Event Limit (only shown if enabled) -->
                                            <div v-if="isTicketClassEnabled(event, tc.id)" class="event-limit-input">
                                                <label class="small text-muted">Usage Limit for this Event:</label>
                                                <input 
                                                    type="number"
                                                    class="form-control form-control-sm text-center"
                                                    :value="getEventLimit(event, tc.id)"
                                                    @change="updateEventLimit(event, tc.id, $event.target.value)"
                                                    min="0"
                                                    placeholder="0=∞"
                                                    style="width: 80px;"
                                                />
                                            </div>
                                            
                                            <!-- Usage Display -->
                                            <div v-if="isTicketClassEnabled(event, tc.id)" class="small">
                                                <span class="text-muted">Used: </span>
                                                <span class="badge bg-info">{{ getEventUsage(event, tc.id) || 0 }}</span>
                                            </div>
                                        </div>
                                    </td>
                                    
                                    <!-- Placeholder cell when no ticket classes -->
                                    <td v-if="activeTicketClasses.length === 0" class="text-center align-middle text-muted">
                                        <i class="bi bi-dash-lg"></i>
                                        <br>
                                        <small>No ticket classes available</small>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import { useToast } from 'vue-toastification';

export default {
    name: "TicketClassManagement",
    components: {
        NavBar
    },
    data() {
        return {
            // Loading state
            dataLoaded: false,
            
            // Route params
            userType: null,
            userID: null,
            
            // Ticket Classes data
            ticketClasses: [],
            originalTicketClasses: [], // For change detection
            savingTicketClasses: false,
            
            // Events data
            events: [],
            originalEventConfigs: [], // For change detection
            savingEventConfigs: false,
            
            // Inline editing state
            editingCell: null,
            
            // Passcode validation debounce
            passcodeCheckTimeout: null,
        };
    },
    computed: {
        activeTicketClasses() {
            return this.ticketClasses.filter(tc => tc.isActive && !tc.isNew);
        },
        hasTicketClassChanges() {
            // Check if any new items exist
            if (this.ticketClasses.some(tc => tc.isNew)) return true;
            // Check if any items are marked as modified
            if (this.ticketClasses.some(tc => tc.isModified)) return true;
            return false;
        },
        hasEventConfigChanges() {
            return this.events.some(e => e.isConfigModified);
        }
    },
    methods: {
        // ============ NAVIGATION ============
        goBack() {
            this.$router.push(`/events/organiser-dashboard/${this.userType}/${this.userID}`);
        },
        
        // ============ DATA LOADING ============
        async loadData() {
            try {
                this.dataLoaded = false;
                
                // Load ticket classes
                await this.loadTicketClasses();
                
                // Load events with their ticket class configs
                await this.loadEventsWithConfigs();
                
                this.dataLoaded = true;
            } catch (error) {
                console.error("Error loading data:", error);
                this.dataLoaded = null;
                useToast().error("Failed to load data. Please try again.");
            }
        },
        
        async loadTicketClasses() {
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/events/ticketClasses/${this.userID}/${this.userType}`
                );
                
                const data = response.data;
                this.ticketClasses = (data.ticketClasses || []).map(tc => ({
                    ...tc,
                    isModified: false,
                    isNew: false,
                    passcodeError: null,
                    limitError: null,
                    originalPasscode: tc.passcode, // Store original for comparison
                    originalLimit: tc.totalUsageLimit
                }));
                
                // Store original for change detection
                this.originalTicketClasses = JSON.parse(JSON.stringify(this.ticketClasses));
            } catch (error) {
                console.error("Error loading ticket classes:", error);
                throw error;
            }
        },
        
        async loadEventsWithConfigs() {
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/events/ticketClasses/getEventsConfig/${this.userID}/${this.userType}`
                );
                
                const data = response.data;
                this.events = (data.events || []).map(event => ({
                    ...event,
                    isConfigModified: false,
                    originalConfig: JSON.parse(JSON.stringify(event.ticketClassConfig || {}))
                }));
                
                this.originalEventConfigs = JSON.parse(JSON.stringify(this.events));
            } catch (error) {
                console.error("Error loading events:", error);
                throw error;
            }
        },
        
        // ============ INLINE EDITING ============
        isEditing(rowIndex, field) {
            return this.editingCell && 
                   this.editingCell.rowIndex === rowIndex && 
                   this.editingCell.field === field;
        },
        
        startEditing(rowIndex, field) {
            this.editingCell = { rowIndex, field };
            
            this.$nextTick(() => {
                if (this.$refs.editInput) {
                    const input = Array.isArray(this.$refs.editInput) 
                        ? this.$refs.editInput[0] 
                        : this.$refs.editInput;
                    if (input) {
                        input.focus();
                        if (input.type === 'text' || input.type === 'number') {
                            input.select();
                        }
                    }
                }
            });
        },
        
        stopEditing() {
            this.editingCell = null;
        },
        
        markModified(index) {
            if (this.ticketClasses[index] && !this.ticketClasses[index].isNew) {
                this.ticketClasses[index].isModified = true;
            }
        },
        
        truncateText(text, maxLength) {
            if (!text) return '';
            if (text.length <= maxLength) return text;
            return text.substring(0, maxLength) + '...';
        },
        
        // ============ TICKET CLASS MANAGEMENT ============
        addNewTicketClass() {
            this.ticketClasses.push({
                id: null,
                className: '',
                passcode: '',
                totalUsageLimit: 0,
                currentUsage: 0,
                isActive: true,
                description: '',
                eventsUsing: 0,
                isNew: true,
                isModified: false,
                passcodeError: null,
                limitError: null
            });
        },
        
        removeNewTicketClass(index) {
            if (this.ticketClasses[index]?.isNew) {
                this.ticketClasses.splice(index, 1);
            }
        },
        
        toggleStatus(index) {
            const tc = this.ticketClasses[index];
            if (tc.isNew) {
                tc.isActive = !tc.isActive;
            } else if (tc.isActive) {
                // If currently active, confirm deactivation
                this.confirmDeactivate(index);
            } else {
                // Re-activating - just toggle
                tc.isActive = true;
                tc.isModified = true;
            }
        },
        
        confirmDeactivate(index) {
            const tc = this.ticketClasses[index];
            // No confirmation needed - changes only take effect after clicking Save Changes
            tc.isActive = false;
            tc.isModified = true;
        },
        
        getEventsUsingCount(eventsUsing) {
            if (!eventsUsing) return 0;
            if (Array.isArray(eventsUsing)) return eventsUsing.length;
            if (typeof eventsUsing === 'number') return eventsUsing;
            return 0;
        },
        
        // ============ PASSCODE VALIDATION ============
        onPasscodeInput(index) {
            const tc = this.ticketClasses[index];
            // Convert to uppercase and remove non-alphanumeric
            tc.passcode = tc.passcode.toUpperCase().replace(/[^A-Z0-9]/g, '');
            
            // Clear previous error
            tc.passcodeError = null;
            
            // Debounce the uniqueness check
            if (this.passcodeCheckTimeout) {
                clearTimeout(this.passcodeCheckTimeout);
            }
            
            this.passcodeCheckTimeout = setTimeout(() => {
                this.checkPasscodeUniqueness(index);
            }, 500);
        },
        
        async checkPasscodeUniqueness(index) {
            const tc = this.ticketClasses[index];
            if (!tc.passcode || tc.passcode.length === 0) {
                tc.passcodeError = null;
                return;
            }
            
            // Check locally for duplicates within current list
            const duplicateIndex = this.ticketClasses.findIndex((other, i) => 
                i !== index && 
                other.passcode && 
                other.passcode.toUpperCase() === tc.passcode.toUpperCase()
            );
            
            if (duplicateIndex !== -1) {
                tc.passcodeError = "Duplicate passcode in list";
                return;
            }
            
            // If this is an existing ticket class and passcode hasn't changed, skip API check
            if (!tc.isNew && tc.originalPasscode === tc.passcode) {
                tc.passcodeError = null;
                return;
            }
            
            // Check against backend
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/events/ticketClasses/checkPasscode/${this.userID}/${this.userType}/${tc.passcode}`
                );
                const data = response.data;
                
                if (!data.isUnique) {
                    // Check if it's the same ticket class (for edit case)
                    if (tc.id && data.existingId === tc.id) {
                        tc.passcodeError = null;
                    } else {
                        tc.passcodeError = "Passcode already in use";
                    }
                } else {
                    tc.passcodeError = null;
                }
            } catch (error) {
                console.error("Error checking passcode:", error);
                // Don't block user, just warn
            }
        },
        
        validatePasscode(index) {
            const tc = this.ticketClasses[index];
            if (!tc.passcode || tc.passcode.trim() === '') {
                tc.passcodeError = "Passcode is required";
                return false;
            }
            if (tc.passcode.length > 20) {
                tc.passcodeError = "Max 20 characters";
                return false;
            }
            return tc.passcodeError === null;
        },
        
        validateLimit(index) {
            const tc = this.ticketClasses[index];
            
            // For existing ticket classes, can't reduce below current usage
            if (!tc.isNew && tc.totalUsageLimit !== null && tc.totalUsageLimit !== 0) {
                if (tc.totalUsageLimit < (tc.currentUsage || 0)) {
                    tc.limitError = `Cannot be less than current usage (${tc.currentUsage})`;
                    tc.totalUsageLimit = tc.originalLimit; // Revert
                    return false;
                }
            }
            
            tc.limitError = null;
            return true;
        },
        
        getUsageBadgeClass(tc) {
            if (!tc.totalUsageLimit || tc.totalUsageLimit === 0) {
                return 'bg-info';
            }
            const percentage = ((tc.currentUsage || 0) / tc.totalUsageLimit) * 100;
            if (percentage >= 100) return 'bg-danger';
            if (percentage >= 80) return 'bg-warning text-dark';
            return 'bg-info';
        },
        
        // ============ SAVE TICKET CLASSES ============
        async saveTicketClasses() {
            // Validate all entries
            let hasErrors = false;
            for (let i = 0; i < this.ticketClasses.length; i++) {
                const tc = this.ticketClasses[i];
                if (tc.isNew || tc.isModified) {
                    if (!tc.className || tc.className.trim() === '') {
                        useToast().error(`Row ${i + 1}: Class name is required`);
                        hasErrors = true;
                    }
                    if (!this.validatePasscode(i)) {
                        hasErrors = true;
                    }
                    if (tc.passcodeError) {
                        hasErrors = true;
                    }
                }
            }
            
            if (hasErrors) {
                useToast().error("Please fix validation errors before saving");
                return;
            }
            
            this.savingTicketClasses = true;
            
            try {
                const toast = useToast();
                let successCount = 0;
                let failCount = 0;
                
                // Process new ticket classes
                const newItems = this.ticketClasses.filter(tc => tc.isNew);
                for (const tc of newItems) {
                    try {
                        await this.$axios.post(
                            `${process.env.VUE_APP_API_URL}/events/ticketClasses/create`,
                            {
                                ownerID: this.userID,
                                ownerType: this.userType,
                                className: tc.className.trim(),
                                passcode: tc.passcode.toUpperCase(),
                                totalUsageLimit: tc.totalUsageLimit || 0,
                                description: tc.description || '',
                                isActive: tc.isActive
                            }
                        );
                        successCount++;
                    } catch (error) {
                        console.error("Error creating ticket class:", error);
                        const errorMsg = error.response?.data?.message || 'Unknown error';
                        toast.error(`Failed to create "${tc.className}": ${errorMsg}`);
                        failCount++;
                    }
                }
                
                // Process modified ticket classes
                const modifiedItems = this.ticketClasses.filter(tc => tc.isModified && !tc.isNew);
                for (const tc of modifiedItems) {
                    try {
                        await this.$axios.put(
                            `${process.env.VUE_APP_API_URL}/events/ticketClasses/update`,
                            {
                                id: tc.id,
                                ownerID: this.userID,
                                ownerType: this.userType,
                                className: tc.className.trim(),
                                passcode: tc.passcode.toUpperCase(),
                                totalUsageLimit: tc.totalUsageLimit || 0,
                                description: tc.description || '',
                                isActive: tc.isActive
                            }
                        );
                        successCount++;
                    } catch (error) {
                        console.error("Error updating ticket class:", error);
                        const errorMsg = error.response?.data?.message || 'Unknown error';
                        toast.error(`Failed to update "${tc.className}": ${errorMsg}`);
                        failCount++;
                    }
                }
                
                if (successCount > 0 && failCount === 0) {
                    toast.success(`${successCount} ticket class(es) saved successfully`);
                } else if (successCount > 0 && failCount > 0) {
                    toast.warning(`${successCount} saved, ${failCount} failed`);
                }
                
                // Reload data to get fresh state
                await this.loadTicketClasses();
                await this.loadEventsWithConfigs();
                
            } catch (error) {
                console.error("Error saving ticket classes:", error);
                useToast().error("An error occurred while saving");
            } finally {
                this.savingTicketClasses = false;
            }
        },
        
        // ============ EVENT CONFIG MANAGEMENT ============
        isTicketClassEnabled(event, ticketClassId) {
            if (!event.ticketClassConfig) return false;
            return event.ticketClassConfig[ticketClassId]?.enabled === true;
        },
        
        getEventLimit(event, ticketClassId) {
            if (!event.ticketClassConfig || !event.ticketClassConfig[ticketClassId]) return 0;
            return event.ticketClassConfig[ticketClassId].perEventLimit || 0;
        },
        
        getEventUsage(event, ticketClassId) {
            if (!event.ticketClassConfig || !event.ticketClassConfig[ticketClassId]) return 0;
            return event.ticketClassConfig[ticketClassId].currentUsage || 0;
        },
        
        toggleTicketClassForEvent(event, ticketClassId) {
            if (!event.ticketClassConfig) {
                event.ticketClassConfig = {};
            }
            
            if (!event.ticketClassConfig[ticketClassId]) {
                event.ticketClassConfig[ticketClassId] = {
                    enabled: true,
                    perEventLimit: 0,
                    currentUsage: 0
                };
            } else {
                event.ticketClassConfig[ticketClassId].enabled = !event.ticketClassConfig[ticketClassId].enabled;
            }
            
            event.isConfigModified = true;
        },
        
        updateEventLimit(event, ticketClassId, value) {
            if (!event.ticketClassConfig) {
                event.ticketClassConfig = {};
            }
            if (!event.ticketClassConfig[ticketClassId]) {
                event.ticketClassConfig[ticketClassId] = {
                    enabled: true,
                    perEventLimit: 0,
                    currentUsage: 0
                };
            }
            
            const numValue = parseInt(value) || 0;
            const currentUsage = event.ticketClassConfig[ticketClassId].currentUsage || 0;
            
            // Validate: can't set below current usage
            if (numValue !== 0 && numValue < currentUsage) {
                useToast().warning(`Limit cannot be less than current usage (${currentUsage})`);
                return;
            }
            
            event.ticketClassConfig[ticketClassId].perEventLimit = numValue;
            event.isConfigModified = true;
        },
        
        async saveEventConfigs() {
            this.savingEventConfigs = true;
            
            try {
                const toast = useToast();
                const modifiedEvents = this.events.filter(e => e.isConfigModified);
                
                if (modifiedEvents.length === 0) {
                    toast.info("No changes to save");
                    return;
                }
                
                // Prepare configs for bulk update - convert object format to array format for backend
                const eventConfigs = modifiedEvents.map(event => {
                    // Convert ticketClassConfig from object to array format
                    const configArray = [];
                    if (event.ticketClassConfig) {
                        for (const [tcId, config] of Object.entries(event.ticketClassConfig)) {
                            if (config.enabled) {
                                configArray.push({
                                    ticketClassId: parseInt(tcId),
                                    eventLimit: config.perEventLimit || 0
                                });
                            }
                        }
                    }
                    
                    return {
                        eventID: event.id,
                        ticketClassConfig: configArray.length > 0 ? configArray : null
                    };
                });
                
                await this.$axios.put(
                    `${process.env.VUE_APP_API_URL}/events/ticketClasses/bulkUpdateEventConfigs`,
                    { 
                        ownerID: this.userID,
                        ownerType: this.userType,
                        eventConfigs 
                    }
                );
                
                toast.success(`${modifiedEvents.length} event config(s) saved successfully`);
                
                // Mark as no longer modified
                modifiedEvents.forEach(event => {
                    event.isConfigModified = false;
                    event.originalConfig = JSON.parse(JSON.stringify(event.ticketClassConfig));
                });
            } catch (error) {
                console.error("Error saving event configs:", error);
                const errorMsg = error.response?.data?.error || "An error occurred while saving";
                useToast().error(errorMsg);
            } finally {
                this.savingEventConfigs = false;
            }
        },
        
        // ============ DATE FORMATTING ============
        formatEventDate(dateString) {
            if (!dateString) return '';
            const date = new Date(dateString);
            return date.toLocaleDateString('en-SG', { 
                day: 'numeric', 
                month: 'short', 
                year: 'numeric' 
            });
        },
        
        formatEventTime(timeString) {
            if (!timeString) return '';
            // timeString is in HH:MM format
            const [hours, minutes] = timeString.split(':');
            const hour = parseInt(hours);
            const ampm = hour >= 12 ? 'PM' : 'AM';
            const hour12 = hour % 12 || 12;
            return `${hour12}:${minutes} ${ampm}`;
        }
    },
    mounted() {
        this.userType = this.$route.params.userType;
        this.userID = this.$route.params.userID;
        
        if (!this.userType || !this.userID) {
            useToast().error("Invalid page parameters");
            this.$router.go(-1);
            return;
        }
        
        this.loadData();
    }
};
</script>

<style scoped>
/* Table Wrappers */
.ticket-class-table-wrapper,
.event-config-table-wrapper {
    max-height: 400px;
    overflow: auto;
}

.event-config-table-wrapper {
    max-height: 500px;
}

/* Sticky Headers */
.sticky-header {
    position: sticky;
    top: 0;
    z-index: 10;
    background: #f8f9fa;
}

.sticky-header th {
    border-bottom: 2px solid #dee2e6;
}

/* Sticky Event Column */
.sticky-col-event {
    position: sticky;
    left: 0;
    z-index: 5;
    background: #fff;
    border-right: 2px solid #dee2e6;
}

.table-hover tbody tr:hover .sticky-col-event {
    background: #f8f9fa;
}

/* Inline Editing */
.editable-cell {
    cursor: pointer;
    transition: background-color 0.15s ease;
    position: relative;
    min-width: 60px;
}

.editable-cell:hover:not(.editing) {
    background-color: rgba(13, 110, 253, 0.08);
}

.editable-cell.editing {
    padding: 4px !important;
    background-color: rgba(13, 110, 253, 0.12);
}

.editable-cell.is-invalid-cell {
    background-color: rgba(220, 53, 69, 0.1) !important;
}

.inline-edit-input,
.inline-edit-textarea {
    min-width: 100px;
    font-size: 0.875rem !important;
    padding: 4px 8px !important;
}

.inline-edit-number {
    min-width: 70px;
    max-width: 100px;
}

.inline-edit-textarea {
    min-width: 180px;
    resize: vertical;
}

/* Modified Row Indicator */
.row-modified {
    border-left: 3px solid #ffc107 !important;
}

/* Cursor */
.cursor-pointer {
    cursor: pointer;
}

/* Event Info in Table */
.event-info {
    /* max-width: 200px; */
}

/* Ticket Class Config Cell */
.ticket-class-config-cell {
    vertical-align: middle;
    min-width: 180px;
}

.event-limit-input {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
}

.event-limit-input input {
    text-align: center;
}

/* Passcode List */
.passcode-list {
    max-width: 150px;
    word-wrap: break-word;
}

/* Table Row States */
.ticket-class-table tr.table-info {
    background-color: rgba(13, 202, 240, 0.15) !important;
}

.ticket-class-table tr.table-secondary {
    opacity: 0.7;
}

/* Invalid Feedback */
.invalid-feedback {
    font-size: 0.75rem;
    margin-top: 2px;
}

/* Font Monospace */
.font-monospace {
    font-family: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}

/* Card styling */
.card-header {
    border-bottom: 1px solid rgba(0,0,0,.125);
}

/* Badge hover effect for status toggle */
.badge.cursor-pointer:hover {
    opacity: 0.8;
    transform: scale(1.05);
    transition: all 0.15s ease;
}

/* Form check in table */
.form-check {
    margin-bottom: 0;
    min-height: auto;
}

.form-check-input {
    cursor: pointer;
}
</style>
