
<template>

    <div v-if="showReviewButton" class="col-5">
        <div class="d-grid gap-2">
            <button v-if="!isEditing" class="btn primary-btn-less-round btn-lg" data-bs-toggle="modal" data-bs-target="#reviewModal"> 
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
                    <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
                </svg>
                Add Your Review
            </button>
            <button v-if="isEditing" class="btn primary-btn-less-round btn-lg" data-bs-toggle="modal" data-bs-target="#reviewModal"> 
                Edit your Review
            </button>
        </div>
    </div>

    <div v-if="showReviewButton" class="modal fade" id="reviewModal" tabindex="-1" aria-labelledby="reviewModalLabel" aria-hidden="true" data-bs-backdrop="static">
        <div class="modal-dialog modal-lg">

            <!-- THIS IS FOR MODE NEW REVIEW -->
            <div v-if="!isEditing">
                <div class="text-success fst-italic fw-bold fs-3 modal-content" v-if='successSubmission'>
                    <span>Your review has successfully been submitted!</span>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>

            <!-- THIS IS FOR MDOE NEW REVIEW -->
            <div v-if="!isEditing">
                <div class="text-danger fst-italic fw-bold fs-3 modal-content" v-if="errorSubmission"> 
                    <div v-if="errorMessage" class = "row"> 
                        <span >An error occurred while attempting to submit, please try again!</span>
                        <br>
                        <button class="btn primary-btn btn-sm" @click="reset">
                            <span class="fs-5 fst-italic"> Retry your submission here! </span>
                        </button>
                    </div>
                    
                    <span v-if="duplicateEntry">You've already submitted a review for this bottle listing!</span>
                    <br>
                    <div class="modal-footer">
                        <button @click="resetModal" type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
            <!-- END OF MODE NEW REVIEW ELEM -->


            <div v-if='addingReview' class="modal-content">
                <!-- change modal header colour -->
                <div class="modal-header" style="background-color: #535C72">
                    <h5 v-if="!isEditing" class="modal-title" id="reviewModalLabel" style="color: white;">Add Your Review</h5>
                    <h5 v-if="isEditing" class="modal-title" id="reviewModalLabel" style="color: white;">Edit Your Review</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>

                <!-- This is where modal starts for review-->
                <div class="modal-body">

                    <div class="row">
                    <!-- Start of left side elements -->
                    <div class="col-md-9">                                     
                        <div class="container-fluid">

                            <!-- Dropdown for language selection -->
                            <div class = 'row justify-content-start mb-4'>
                                <div class="col-md-4"> 
                                    <p class = 'text-start mb-2 fw-bold'>Language <span class="text-danger">*</span></p>
                                    <div class="input-group">                                                    
                                        <select v-model="selectedLanguage" class="form-select" id="inputGroupSelect01">
                                            <!-- Add in the languages here -->
                                            <option v-for="language in languages" v-bind:key="language['_id']">{{ language['language'] }}</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <!-- end of dropdown for language selection -->

                            <!-- Text input are for review -->
                            <div class = 'row justify-content-start mb-3'>
                                <div class = "col-md-12">
                                    <p class='text-start mb-2 fw-bold'>Review <span class="text-danger">*</span></p>
                                    <textarea v-model="reviewDesc" class="form-control" id="reviewTextarea" rows="3" placeholder="Min 20 characters"></textarea>
                                </div>
                                <div v-if="reviewDescError!==''" class ="col-md-12">
                                    <p class='text-danger text-start mb-2 fw-bold'>{{ reviewDescError }}</p>
                                </div>
                            </div>

                            <!-- Checkboxes for would recommend and would buy again -->
                            <div class = 'row justify-content-start mb-3 text-start'>
                                <div class = "col-md-12">
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input" type="checkbox" id="inlineCheckbox1" v-model="wouldRecommend" value="option1">
                                        <label class="form-check-label text-start fw-bold" for="inlineCheckbox1">Would Recommend</label>
                                    </div>
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input" type="checkbox" id="inlineCheckbox2" v-model="wouldBuyAgain" value="option2">
                                        <label class="form-check-label text-start fw-bold" for="inlineCheckbox2">Would Buy Again</label>
                                    </div>                                                                                                   
                                </div>                                         
                            </div>
                            <!-- End of checkboxes -->

                            <!-- Buttons to expand -->
                            <div v-if="!extendReview" class = 'row justify-content-start mb-3 text-start'>
                                <div class = "col-md-12 text-center">
                                    <button class="btn primary-btn-less-round btn-sm" @click="controlModal"> 
                                        Extend Review <span style="color: white;">&#9660;</span>
                                    </button>                                                                  
                                </div>                                         
                            </div>

                            <!-- Button to collapse -->
                            <div v-if="extendReview" class = 'row justify-content-start mb-3 text-start'>
                                <div class = "col-md-12 text-center">
                                    <button class="btn primary-btn-less-round btn-sm" @click="controlModal"> 
                                        Condense Review <span style="color: white;">&#9650;</span>
                                    </button>                                                                  
                                </div>                                         
                            </div>
                            <!-- end of button -->

                            <!-- Dashed line -->
                            <div class = 'row justify-content-start mb-1 text-start'>
                                <div class = "col-md-12 text-center">
                                    <p class="dotted-line">
                                    </p>
                                </div>
                            </div>
                            <!-- end of dash line -->


                            <!-- DONE: Make a colour grid/tables containing all the colour -->
                            <div v-if="extendReview">
                                <div class="row">
                                    <div class="col-md-2">
                                        <p class="text-start mb-1 fw-bold">Colour:</p>    
                                    </div>
                                    <div v-if="selectedColour=== ''" class="col-md-2"></div>
                                    <div v-else-if="selectedColour.includes('#')" class="col-md-1">
                                        <button class="btn text-start mb-1" :style="{ 
                                                        width: '30px', 
                                                        height: '30px', 
                                                        backgroundColor: selectedColour, 
                                                        color: selectedColour, 
                                                        borderRadius: '0', 
                                                        borderColor:'grey', 
                                                        borderWidth:'1px'
                                                    }"></button>
                                    </div>
                                    <div v-else class="col-md-1">
                                        <button class="btn text-start mb-1" :style="{ width: '30px', height: '30px', borderRadius: '0', borderColor:'grey', borderWidth:'1px', backgroundImage: `linear-gradient(to bottom right, ${specialColours[selectedColour][0]}, ${specialColours[selectedColour][1]}`}"></button>
                                    </div>
                                    <div v-if="selectedColour!== ''" class="col-md-4">
                                        <button @click="clearColour" class="btn text-start mb-1" style="background-color: #535C72;color: white;">Clear Selection</button>
                                    </div>
                                </div>                                   
                                <div class="row justify-content-start mb-1 text-start">
                                    <div class="col-md-5 mr-0 text-start">
                                        <div class="row">
                                            <div class="col">
                                            <button @click="displaySelectColour(colour)" v-for="(colour, i) in colours.slice(0, 7)" :key="i" :value="colour" class="btn" data-bs-toggle="button"
                                                    :style="{ 
                                                        width: '30px', 
                                                        height: '30px', 
                                                        backgroundColor: colour, 
                                                        color: colour, 
                                                        borderRadius: '0', 
                                                        borderColor:'grey', 
                                                        borderWidth:'1px'
                                                    }">                                
                                            </button>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col">
                                            <button @click="displaySelectColour(colour)" v-for="(colour, i) in colours.slice(7, 14)" :key="i" :value="colour" class="btn" data-bs-toggle="button" 
                                                    :style="{ 
                                                        width: '30px', 
                                                        height: '30px', 
                                                        backgroundColor: colour, 
                                                        color: colour, 
                                                        borderRadius: '0', 
                                                        borderColor:'grey', 
                                                        borderWidth:'1px'
                                                    }">                                
                                            </button>
                                            </div>
                                        </div>
                                        </div>

                                    <!-- Special gradient -->
                                    <div class="col-md-5 ml-0 text-start">
                                        <button @click="displaySelectColour(key)" v-for="(value, key) in specialColours" :key="key" type="button" :value="key" class="btn" data-bs-toggle="button" :style="{ width: '30px', height: '30px', borderRadius: '0', borderColor:'grey', borderWidth:'1px', backgroundImage: `linear-gradient(to bottom right, ${value[0]}, ${value[1]}`}">                                
                                        </button>
                                    </div>
                                </div>
                            </div>
                            <!-- END OF COLOURS -->


                            <!-- Aroma taste and finish inputs -->
                            <div v-if="extendReview" class="form-group mb-3">
                                <p class="text-start mb-1 fw-bold">Aroma:</p>
                                <input v-model="aroma" type="text" class="form-control" id="aroma">
                            </div>
                            <div v-if="extendReview" class="form-group mb-3">
                                <p class="text-start mb-1 fw-bold">Taste:</p>
                                <input v-model="taste" type="text" class="form-control" id="taste">
                            </div>
                            <div v-if="extendReview" class="form-group mb-3">
                                <p class="text-start mb-1 fw-bold">Finish:</p>
                                <input v-model="finish" type="text" class="form-control" id="finish">
                            </div>
                            <!-- End of armoa taste and finish inputs -->

                            <!-- Range slider for rating -->
                            <div class="col-md-5 mb-3"> 
                                <div class="row align-items-center text-start">
                                    <label for="customRange2" class="form-label fw-bold">Rating<span class="text-danger">*</span>: {{ rating }}</label>
                                    <div class="col-auto">
                                        <label for="customRange" class="form-label fw-bold">1</label>
                                    </div>
                                    <div class="col">
                                        <input v-model="rating" type="range" class="form-range" min="1" max="10" step="0.5" id="customRange">
                                    </div>
                                    <div class="col-auto">
                                        <label for="customRange" class="form-label fw-bold">10</label>
                                    </div>
                                </div>
                            </div>

                            <!-- Start of flavour tag -->
                            <div class="form-group mb-3">
                                <p class="text-start mb-1 fw-bold">Flavour Tags</p> 

                                <div class ='container'>
                                    <button class="btn mb-2 me-2" @click="toggleBox(family)" v-for="family in flavourTags" v-bind:key="family['_id']" :style="{ color:'white', backgroundColor: family['hexcode'], borderColor:family['hexcode'], borderWidth:'1px' }">{{ family['familyTag'] }}</button>
                                    
                                    <!-- This is the conatiner/dropdown box for the subtags -->
                                    <div v-for="family in flavourTags" :key="family['_id']">
                                        <div v-if="family.showBox" class="rounded p-3" :style="{border: '3px solid ' + family['hexcode'] }">
                                            <div class="row">
                                                <div class="col-3" v-for="(element, index) in family.subtag" :key="index">
                                                    <button @click="toggleFlavourSelection(element, family['hexcode'])" class="btn mb-2" :style="{ width: '100px', height: '60px',color:'white', backgroundColor: selectedFlavourTags.includes(element+family['hexcode']) ? 'grey' :family['hexcode'], borderColor: family['hexcode'], borderWidth:'1px' }">{{ element }}</button>
                                                </div>                        
                                            </div>
                                        </div>
                                    </div>
                                    <!-- End of dropdown -->
                                </div>
                            </div>
                            <!-- End of flavour tag -->

                            <!-- Start of observation tags -->
                            <!-- Make this a search/dropdown -->
                            <div class="form-group mb-3">
                                <p class="text-start mb-1 fw-bold">Observation Tags</p>
                                <!-- Buttons for the first 8 observations -->
                                <button v-for="observation in observationTags.slice(0, 8)" @click="toggleObservationSelection(observation)" v-bind:key="observation" class="btn mb-2 me-2" data-bs-toggle="button" :style="{ color:'white', backgroundColor: selectedObservations.includes(observation) ? 'blue' : 'grey', borderColor:'grey', borderWidth:'1px' }">{{ observation }}</button>
                                
                                <!-- Buttons for additional observations (shown only when extendObservation is true) -->
                                <div v-if="extendObservation">
                                    <button v-for="observation in observationTags.slice(8)" @click="toggleObservationSelection(observation)" v-bind:key="observation" class="btn mb-2 me-2" :style="{ color:'white', backgroundColor: selectedObservations.includes(observation) ? 'blue' : 'grey', borderColor:'grey', borderWidth:'1px' }">{{ observation }}</button>
                                </div>
                                
                                <!-- Button to toggle between View All and View Less -->
                                <button @click="toggleObservations" class="btn" style="color:black; background-color:white; border-color:black; border-width: 1px;" v-if="!extendObservation">
                                    View All
                                </button>
                                <button @click="toggleObservations" class="btn" style="color:black; background-color:white; border-color:black; border-width: 1px;" v-else>
                                    View Less
                                </button>
                                
                            </div>


                        </div>
                    </div>
                    <!-- End of left side elements -->

                    <!-- Start of right side elements, photo, location and friend tags -->
                    <div class="col-md-3">
                        <p class = 'text-start mb-2 fw-bold'>Add Photo</p>
                        <div class="mb-3">
                            <!-- DONE v:model here the file -->
                            <input class="form-control mb-2" @change="onFileChange" type="file" id="reviewPhoto">
                            <div class = "row">
                                <img :src="selectedImage ? selectedImage : 'none'" alt="" id="output">
                            </div>
                            <button v-if="selectedImage!==null" class="btn text-start mb-1" style="background-color: #535C72;color: white;" @click="clearPhoto">Clear Photo</button>
                        </div>
                        
                        <div class="form-group mb-3">
                            <p class="text-start mb-1 fw-bold">Tag Friends</p>
                            <input type="text" class="form-control" id="friendTag">
                        </div>
                        
                        <!-- Start of location input -->
                        <div class="form-group mb-3">
                            <p class="text-start mb-1 fw-bold">Location</p>                                            
                                            
                            <!-- Link filteredOptions to venues location -->
                            <div class="input-group">
                                <select class="form-control" v-model="selectedLocation" @input="filterOptions($event)">
                                    <option v-for="option in filteredOptions" :key="option.id" :value="option.name">{{ option.name }}</option>
                                </select>
                            </div>
                            <button v-if="selectedLocation!==''" class="btn text-start mb-1" style="background-color: #535C72;color: white;" @click="clearLocation">Clear Selection</button>
                        </div>


                    </div> 
                    <!-- End of right side elements -->

                </div>
                <!-- End of bootstrap row -->

                </div>
                <!-- End of modal body -->
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button v-if="!isEditing" type="button" @click="addReview" class="btn btn-primary">Submit Review</button>
                    <button v-if="isEditing" type="button" @click="editReview" class="btn btn-primary">Save Review</button>
                </div>
            </div>
        </div>
    </div>
            <!-- END OF MODAL -->
</template>

<script>
export default {
    name:'ReviewModal',
  props: {
    isEditing: {
      type: Boolean,
      required: true
    },
    reviewData: {
      type: Object,
      default: null
    },
    showReviewButton: {type:Boolean},
    languages:{
        type:Object
    },
    colours: {
        type:Array
    },
    specialColours:{
        type:Object
    },
    observationTags:{
        type:Array
    },
    locationOptions:{
        type:Object
    },
    flavourTags:{
        type:Object
    },
    userID:{
        type:Object
    },
    reviewTarget:{
        type:Object
    }
  },

  data() {
    return {
            selectedLanguage:"English",
            reviewDesc:"",
            rating: 5,
            selectedColour:"",
            selectedImage: null,
            image64: null,
            selectedObservations:[],
            selectedFlavourTags:[],
            aroma:"",
            taste:"",
            finish:"",
            wouldRecommend:false,
            wouldBuyAgain:false,
            extendReview:true,
            locationSearchTerm: "",
            selectedLocation: "",
            selectedLocationId: "",
            extendObservation: false,
            loggedIn:false,
            reviewDescError:'',
            reviewResponseCode:'',
            addingReview: true,
            successSubmission: false,
            errorSubmission:false,
            errorMessage: false,
            duplicateEntry: false,
    };
  },
  mounted() {
    // Pre-fill review description if review data exists
    if (this.reviewData?.reviewDesc) {
      this.reviewDesc = this.reviewData.reviewDesc;
    }
    if (this.reviewData?.photo) {
      this.selectedImage = this.reviewData.photo;
    }
    if (this.reviewData?.location) {
      this.selectedLocationId = this.reviewData.location;
      this.selectedLocation = this.locationOptions
            .filter(option=>option.id.toLowerCase().includes(this.reviewData.location.toLowerCase()))
    }
    if (this.reviewData?.colour) {
      this.selectedColour = this.reviewData.colour;
    }
    if (this.reviewData?.wouldBuyAgain) {
      this.wouldBuyAgain = this.reviewData.wouldBuyAgain;
    }
    if (this.reviewData?.wouldRecommend) {
      this.wouldRecommend = this.reviewData.wouldRecommend;
    }
    if (this.reviewData?.language) {
      this.selectedLanguage = this.reviewData.language;
    }
    if (this.reviewData?.finish) {
      this.finish = this.reviewData.finish;
    }
    if (this.reviewData?.aroma) {
      this.aroma = this.reviewData.aroma;
    }
    if (this.reviewData?.taste) {
      this.taste = this.reviewData.taste;
    }
    if (this.reviewData?.rating) {
      this.rating = this.reviewData.rating;
    }
    if (this.reviewData?.observationTag) {
      this.selectedObservations = this.reviewData.observationTag;
    }
    if (this.reviewData?.flavourTag) {
      this.selectedFlavourTags = this.reviewData.flavourTag;
    }

  },
  computed: {
            filteredOptions() {
            return this.locationOptions.filter(option =>
                option.name.toLowerCase().includes(this.locationSearchTerm.toLowerCase())
            );
            }
        },
  methods:{
    displaySelectColour(colour){
                this.selectedColour = colour
            },
            // function to display submitted image
            onFileChange(event){
                const file = event.target.files[0];
                const reader = new FileReader();

                reader.onloadend = async () => {
                    this.selectedImage = reader.result;
                    const base64String = reader.result.replace('data:', '').replace(/^.+,/, '');
                    this.image64 = base64String;
                };
                reader.readAsDataURL(file);
            },

            // Function to add review
            addReview(){
                // let errorPhrase = "Your completion is incomplete"
                // form validation
                if(this.reviewDesc.length < 20){
                    this.reviewDescError ="Character count is less than 20, please write more for a more detailed review."
                    alert("Submission has error, please fill in the required fields properly")
                    return "Submission error"
                }
                let createdDate = new Date().toISOString() + '+00:00';
                if (this.reviewDesc !== "") {
                    this.reviewDesc = this.reviewDesc.trim();
                }
                if (this.photo !== null) {
                    this.photo = this.photo.trim();
                }
                if (this.aroma !== "") {
                    this.aroma = this.aroma.trim();
                }
                if (this.taste !== "") {
                    this.taste = this.taste.trim();
                }
                if (this.finish !== "") {
                    this.finish = this.finish.trim();
                }
                let submitAPI = "http://127.0.0.1:5000/createReview/createReview"
                let submitData = {
                    "userID" : this.userID,
                    "reviewTarget" : this.listing_id,
                    "rating" : this.rating,
                    "reviewDesc": this.reviewDesc,
                    "reviewType": "Listing",
                    "flavorTag" : this.selectedFlavourTags,
                    "photo" : this.selectedImage,
                    "colour" : this.selectedColour,
                    "language" : this.selectedLanguage,
                    "aroma" : this.aroma,
                    "taste" : this.taste,
                    "finish" : this.finish,
                    "location" :this.selectedLocationId,
                    "willRecommend": this.wouldRecommend,
                    "wouldBuyAgain": this.wouldBuyAgain,
                    "observationTag": this.selectedObservations,
                    "createdDate": createdDate
                }
                this.writeReview(submitAPI, submitData)
                
            },

            async writeReview(submitAPI, submitData){
                const response = await this.$axios.post(submitAPI, submitData)
                .then((response)=>{
                    this.reviewResponseCode = response.data.code
                })
                .catch((error)=>{
                    this.reviewResponseCode = error.response.data.code
                });
                if(this.reviewResponseCode==201){
                    this.successSubmission=true; // Display success message
                    this.addingReview=false; // Hide submission in progress message
                }else{
                    this.errorSubmission=true; // Display error message
                    this.addingReview=false; // Hide submission in progress message
                    if(this.reviewResponseCode==400){
                        this.duplicateEntry = true // Display duplicate entry message
                    }else{
                        this.errorMessage = true // Display generic error message
                    }
                }
                return response
            },

            // Function to expand/contract the modal
            controlModal(){
                if(this.extendReview){
                    this.extendReview = false
                }
                else{
                    this.extendReview = true
                }
            },

            filterOptions(event) {
                const selectedOption = this.filteredOptions.find(option => option.name === event.target.value);
                this.selectedLocationId = selectedOption.id;
            },
            
            toggleBox(family) {
                let tempShowBox = family.showBox
                this.flavourTags.forEach(item => {
                    item.showBox = false;
                });
                family.showBox = !tempShowBox; // Toggle the visibility of the box
            },

            toggleObservations(){
                this.extendObservation = !this.extendObservation
            },

            toggleObservationSelection(observation) {
                const index = this.selectedObservations.indexOf(observation);
                if (index === -1) {
                    // Observation is not selected, so add it to the array
                    this.selectedObservations.push(observation);
                } else {
                    // Observation is selected, so remove it from the array
                    this.selectedObservations.splice(index, 1);
                }
            },

            toggleFlavourSelection(flavour, hexcode) {
                const index = this.selectedFlavourTags.indexOf(flavour+hexcode);
                if (index === -1) {
                    // Observation is not selected, so add it to the array
                    this.selectedFlavourTags.push(flavour+hexcode);
                } else {
                    // Observation is selected, so remove it from the array
                    this.selectedFlavourTags.splice(index, 1);
                }
            },

            clearColour(){
                this.selectedColour = ''
            },

            clearLocation(){
                this.selectedLocation = ''
            },

            clearPhoto(){
                this.selectedImage = null
                document.getElementById('reviewPhoto').value = '';
            },
    }
};
</script>