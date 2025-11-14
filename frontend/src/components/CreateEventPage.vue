<template>
    <div>
        <form>
            <!-- Event name -->
            <div class="mb-3">
                <label for="eventName" class="form-label">Event Name <span style="color: red;">*</span></label>
                <input type="text" class="form-control" id="eventName" required v-model="newEvent.eventName" @input="emitNewEvent">
            </div>

            <!-- Event description input editor -->
            <p>Event Description <span style="color: red;">*</span></p>
            <div id="editor-container" style="height: 300px;" class="mb-3"></div>

            <!-- Event type -->
            <div class="mb-3 row">
                <label for="eventType">Event Type <span style="color: red;">*</span></label>
                
                <div>
                    <div class="form-check form-check-inline">
                        <!-- Online option -->
                        <input type="radio" id="onlineEvent" name="eventType" value="Online" v-model="newEvent.eventType" class="form-check-input" required @input="emitNewEvent">
                        <label for="onlineEvent" class="form-check-label">&nbsp;Online</label>
                    </div>
                    <div class="form-check form-check-inline">
                        <!-- In Person option -->
                        <input type="radio" id="inPersonEvent" name="eventType" value="Location" v-model="newEvent.eventType" class="form-check-input" @input="emitNewEvent">
                        <label for="inPersonEvent" class="form-check-label">&nbsp;In Person</label>
                    </div>
                </div>
            </div>

            <hr>

            <div class="mb-3 row">
                <!-- Event start date -->
                <div class="col">
                    <label for="eventStartDate" class="form-label">Event Start Date <span style="color: red;">*</span></label>
                    <input type="date" class="form-control" id="eventStartDate" required v-model="newEvent.eventStartDate" :min="new Date().toISOString().split('T')[0]" @input="emitNewEvent"> 
                </div>

                <!-- Event start time -->
                <div class="col">
                    <label for="eventStartTime" class="form-label">Event Start Time</label>
                    <input type="time" class="form-control" id="eventStartTime" v-model="newEvent.eventStartTime" @input="emitNewEvent" :disabled="newEvent.allDay">
                </div>
            </div>

            
            <div class="mb-3 row">
                <!-- Event end date -->
                <div class="col">
                    <label for="eventEndDate" class="form-label">Event End Date</label>
                    <input type="date" class="form-control" id="eventEndDate" v-model="newEvent.eventEndDate" :min="newEvent.eventStartDate" @input="emitNewEvent">
                </div>

                <!-- Event end time -->
                <div class="col">
                    <label for="eventEndTime" class="form-label">Event End Time</label>
                    <input type="time" class="form-control" id="eventEndTime" v-model="newEvent.eventEndTime" @input="emitNewEvent" :disabled="newEvent.allDay">
                </div>
            </div>

            <!-- All Day Checkbox -->
            <div class="mb-3">
                <input class="form-check-input" type="checkbox" id="allDay" 
                    v-model="newEvent.allDay" 
                    @change="emitNewEvent">
                <label class="form-check-label" for="allDay">
                    All Day Event
                </label>
            </div>

            <hr>

            <!-- Event wallpaper upload -->
            <div class="mb-3">
                <label for="eventBanner" class="form-label">Add Event Wallpaper (upload up to 3 images)</label>
                <input type="file" class="form-control" id="eventBanner" multiple accept="image/*" @change="uploadImages">
            </div>

            <!-- Display uploaded banners -->
            <div v-if="newEvent.eventBanners.length > 0" class="mb-3 row">
                <div v-for="(banner, index) in newEvent.eventBanners" :key="index" class="col-4 position-relative">
                    <img :src="banner" class="img-fluid" alt="Event Banner">
                    <button class="btn primary-btn-red btn-sm position-absolute top-0 end-0 mt-3 me-3" @click="removePhotoNew(index)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                            <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0"/>
                        </svg>
                    </button>
                </div>
            </div>


            <!-- Event limit -->
            <div class="mb-3">
                <label for="eventLimit" class="form-label">Event Limit</label>
                <input type="number" class="form-control" min="1" id="eventLimit" v-model="newEvent.eventLimit" @input="emitNewEvent">
            </div>

            

            <!-- Ticketed event -->
            <div class="mb-3">
                <label for="ticketedEventYes">Is this a ticketed event? (Click yes if this event requires a pre-sign up for entry.) <span style="color: red;">*</span></label>
                <div>
                    <div class="form-check form-check-inline">
                        <!-- Yes Option -->
                        <input type="radio" id="ticketedEventYes" name="ticketedEvent" value="true" v-model="newEvent.ticketed" class="form-check-input" required @input="emitNewEvent">
                        <label for="ticketedEventYes" class="form-check-label">&nbsp;Yes</label>
                    </div>
                    <div class="form-check form-check-inline">
                        <!-- No Option -->
                        <input type="radio" id="ticketedEventNo" name="ticketedEvent" value="false" v-model="newEvent.ticketed" class="form-check-input" @input="emitNewEvent">
                        <label for="ticketedEventNo" class="form-check-label">&nbsp;No</label>
                    </div>
                </div>
            </div>

            <!-- Paid event -->
            <div v-if="newEvent.ticketed == 'true'" class="mb-3">
                <label for="paidEventYes">If it is a ticketed event, are tickets free or paid?</label>
                <div>
                    <!-- Yes Option -->
                    <input type="radio" id="paidEventYes" name="paidEvent" value="false" v-model="newEvent.paidEvent" required @input="emitNewEvent">
                    <label for="paidEventYes">&nbsp;Tickets are free, but participants must RSVP first to enter.</label>
                </div>
                <div>
                    <!-- No Option -->
                    <input type="radio" id="paidEventNo" name="paidEvent" value="true" v-model="newEvent.paidEvent" @input="emitNewEvent">
                    <label for="paidEventNo">&nbsp;Tickets are paid, and participants will have to make payment at the below link:</label>

                    <!-- Payment link -->
                    <input v-if="newEvent.paidEvent == 'true'" type="text" class="form-control" id="paymentLink" v-model="newEvent.paymentLink" required @input="emitNewEvent">
                </div>
            </div>

            <!-- Event location -->
            <div class="mb-3">
                <label for="eventLocation" class="form-label">
                    <span v-if="newEvent.eventType == 'Location'">Event Location</span>
                    <span v-else>Event Link</span>
                </label>
                <input type="text" class="form-control" id="eventLocation" v-model="newEvent.eventLocation" @input="emitNewEvent">
            </div>

            <!-- Event passcodes -->
            <div class="mb-3">
                <label class="form-label">Event Passcodes <span class="text-muted">Optional</span></label>
                <small class="text-muted d-block mb-2">Set passcodes with usage limits to control access to your event</small>
                
                <!-- Passcode input fields -->
                <div v-for="(passcode, index) in newEvent.eventPasscodes" :key="index" class="mb-3 p-3 border rounded">
                    <div class="row align-items-end">
                        <!-- Passcode input -->
                        <div class="col-md-7">
                            <label :for="'passcode-' + index" class="form-label small">Passcode {{ index + 1 }}</label>
                            <input 
                                type="text" 
                                class="form-control" 
                                :id="'passcode-' + index"
                                v-model="passcode.code" 
                                :placeholder="'Enter passcode ' + (index + 1)"
                                @input="emitNewEvent"
                            >
                        </div>
                        
                        <!-- Limit input -->
                        <div class="col-md-3">
                            <label :for="'limit-' + index" class="form-label small">Usage Limit</label>
                            <input 
                                type="number" 
                                class="form-control" 
                                :id="'limit-' + index"
                                v-model.number="passcode.limit" 
                                min="1" 
                                max="10000"
                                placeholder="50"
                                @input="emitNewEvent"
                            >
                        </div>
                        
                        <!-- Remove button -->
                        <div class="col-md-2">
                            <button 
                                type="button" 
                                class="btn btn-outline-danger btn-sm w-100"
                                @click="removePasscode(index)"
                                :disabled="newEvent.eventPasscodes.length <= 1"
                            >
                                Remove
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Add passcode button -->
                <button 
                    type="button" 
                    class="btn btn-outline-primary btn-sm" 
                    @click="addPasscode"
                >
                    Add Passcode
                </button>
            </div>
        </form>
    </div>

</template>

<script>
import Quill from 'quill';
import DOMPurify from 'dompurify';

export default {
    name: 'CreateEventPage',
    data() {
        return {
            // Variable to hold the Quill instance
            quill: null,

            // Variable to store new event details
            newEvent: {
                eventName: null,
                eventDescription: null,
                eventType: null,
                eventStartDate: null,
                eventEndDate: null,
                eventStartTime: null,
                eventEndTime: null,
                allDay: false,
                eventLimit: null,
                eventBanners: [],
                ticketed: null,
                paidEvent: null,
                eventLocation: null,
                paymentLink: null,
                eventPasscodes: [{ code: '', limit: 50 }] // Array of passcode objects, start with one empty field
            },

        }
    },
    methods: {
        // Function to upload images (convert images to base64)
        uploadImages(event) {

            this.newEvent.eventBanners = [];

            // Get the files 
            const files = event.target.files;

            // Check if there are more than 3 files
            if (files.length > 3) {
                alert("You can only upload up to 3 images.");
                return;
            }

            // Loop through the files
            for (let i = 0; i < files.length; i++) {

                // Check if the file is an image
                if (files[i].type.match('image.*')) {

                    // Create a file reader
                    const reader = new FileReader();

                    // Read the file
                    reader.readAsDataURL(files[i]);

                    // When the file is read
                    reader.onload = () => {
                        // Push the base64 string to the postPhotos array
                        this.newEvent.eventBanners.push(reader.result);
                    }
                }
            }
            this.emitNewEvent();
        },

        // Function to remove a photo from the new event
        removePhotoNew(index) {
            this.newEvent.eventBanners.splice(index, 1);
            this.emitNewEvent();
        },

        // Function to add a new passcode field
        addPasscode() {
            this.newEvent.eventPasscodes.push({ code: '', limit: 50 });
            this.emitNewEvent();
        },

        // Function to remove a passcode field
        removePasscode(index) {
            if (this.newEvent.eventPasscodes.length > 1) {
                this.newEvent.eventPasscodes.splice(index, 1);
                this.emitNewEvent();
            }
        },

        // Function to emit the new event details to the parent component
        emitNewEvent() {
            this.$emit('new-event', this.newEvent);
        }
    },
    mounted() {

        // Initialize Quill editor
        this.$nextTick(() => {
            const editorContainer = document.getElementById('editor-container');
            if (editorContainer) {
            this.quill = new Quill(editorContainer, {
                theme: 'snow',
                modules: {
                toolbar: [
                    [{ 'header': '1' }, { 'header': '2' }, { 'font': [] }],
                    [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                    ['bold', 'italic', 'underline'],
                    ['link'],
                ]
                }
            });
            // Attach change event to the div via Quill's API
            this.quill.on("text-change", () => {
                // Check if the event description is empty
                const description = this.quill.root.innerHTML;

                // Check if the content is empty
                if (!description || description.trim() === "<p><br></p>") {
                    alert("Content is empty. Please add some text.");
                    return;
                }

                // Sanitize the content using DOMPurify
                let sanitizedContent = DOMPurify.sanitize(description);

                // Set the event description
                this.newEvent.eventDescription = sanitizedContent;
                this.emitNewEvent();
            });
            }
        });
    }

}
</script>