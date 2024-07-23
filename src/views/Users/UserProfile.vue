<template>
    <NavBar />

    <!-- Display when data is still loading -->
    <div class="text-info-emphasis fst-italic fw-bold fs-5 pt-5" v-if="dataLoaded == false">
        <span>Loading profile, please wait...</span>
        <br><br>
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>

    <!-- Display when data fails to load -->
    <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="dataLoaded == null"> 
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

  <div v-if="displayUser && dataLoaded" class="userprofile mt-5 mobile-mt-3">

    <div class="container text-start">
        <div class="row">
            <!-- user profile -->
            <div class="col-12 col-md-4 mb-3">

                <div class="container">

                    <!-- basic information -->
                    <div class="row">
                        <!-- profile picture -->
                        <div class="col-4 text-start pe-0">
                            <img :src=" 'data:image/jpeg;base64,' + (displayUser.photo || defaultProfilePhoto)" alt="" class="rounded-circle-no-bg border border-dark profile-img" style="height:auto; width:100%; ">
                        </div>                        
                        <!-- user name -->
                        <div class="col-8">
                            <h3 class="mb-0" >{{ displayUser.displayName }}</h3> 
                            <b>@{{ displayUser.username }}</b> 
                            <br/>
                            {{ drinkCount }} Drinks Tasted 
                            <br/>
                            <button v-if="!ownProfile && displayUser.modType != []" data-bs-toggle="modal" data-bs-target="#moderatormodal" class="btn btn-warning hover-button p-1" style="border-radius: 20px; font-size: 0.8rem;">★ Certified Moderator</button> 
                            <button v-if="user && user.isAdmin" data-bs-toggle="modal" data-bs-target=“#moderatormodal class="btn btn-warning hover-button p-1" style="border-radius: 20px; font-size: 0.8rem;">★ Certified Moderator</button>
                        </div>
                    </div>

                    <!-- additional information -->
                    <div class="mt-3">
                        <div class="row">
                            <div class="col-5">
                                <b>Member Since</b>
                            </div>
                            <div class="col-7 text-end">
                                {{ joinDate }}
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-5">
                                <b>Drink of Choice</b>
                            </div>
                            <div class="col-7 text-end">
                                <span v-if="drinkChoice.length == 0"><i>None</i></span>
                                <span v-else>{{ drinkChoice }}</span>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-5">
                                <b> Points Earned </b>
                            </div>
                            <div class="col-7 text-end">
                                <span> {{ totalPoints }} pts </span>
                            </div>
                        </div>
                    </div>

                    <!-- buttons -->
                    <div class="row mt-3">
                        <button v-if="ownProfile && user" type="button" class="btn primary-btn-outline-not-round" data-bs-toggle="modal" data-bs-target="#editProfileModal" style="font-weight:bold;">Edit Profile</button>
                        <button v-else-if="following && user" type="button" class="btn primary-btn-outline-less-round" @click="editFollow('unfollow')">Following</button>
                        <button v-else-if="user" type="button" class="btn primary-btn-less-round" @click="editFollow('follow')"  style="font-weight:bold;">+ Follow User</button>
                        <router-link v-if="ownProfile && user" :to="{ path: '/dashboard/user' }" class="btn secondary-btn-not-rounded rounded-0 mt-3" style=" font-weight: bold;">
                            View My Analytics
                        </router-link>
                        <span style="position: relative; display: inline-block" class="m-0 p-0">
                            <div v-if="!ownProfile && displayUser.modType != []" class="speech-bubble">{{ displayUser.modType ? displayUser.modType.join(', ') : 'None' }}</div>
                            <button v-if="user && user.isAdmin" class="btn tertiary-btn reverse-clickable-text mt-3" style="width: 100%" type="button" data-bs-toggle="modal" data-bs-target="#addModeratorModal">Add/Remove Moderator Rights</button>
                        </span>
                        
                       
                        <button v-if="ownProfile && user" type="button" class="btn secondary-btn-less-round mt-3" data-bs-toggle="modal" data-bs-target="#changePasswordModal">Change/Reset Password</button>
                    </div>

                    <!-- join as a moderator modal start xyz-->
                    <div class="modal fade" id="moderatormodal" tabindex="-1" aria-labelledby="moderatorModalLabel" aria-hidden="true" data-bs-backdrop="static">

                        <div class="modal-dialog xmodal-lg d-flex align-items-center" style="height: 100vh;">

                        <div class="modal-content">

                        <div v-if="drinkChoice.length == 0" class="modal-body px-4">
                            
                            <button v-if="!ownProfile && displayUser.modType != []" data-bs-toggle="modal" data-bs-target="#moderatormodal" class="btn btn-warning hover-button p-1 mb-3" style="border-radius: 20px; font-size: 0.8rem;">★ Certified Moderator</button> 
                            <button v-if="user && user.isAdmin" data-bs-toggle="modal" data-bs-target=“#moderatormodal class="btn btn-warning hover-button p-1 mb-3" style="border-radius: 20px; font-size: 0.8rem;">★ Certified Moderator</button>
                            <button type="button" class="btn-close uninvert" data-bs-dismiss="modal" aria-label="Close" style="margin-left:63%;"></button>
                            <p><b>{{ displayUser.displayName }} is a Drink X moderator.</b></p> 
                            <p><b><em>Moderators help shape the drinks community and ensure drink reviews remain fun, useful and respectful!</em></b></p>
                            <b><a v-if="user && !user.isAdmin" href="#" class="mt-3" data-bs-toggle="modal" data-bs-target="#applyModerator" style="color: black">Want to be a moderator? Apply here!</a></b>   
                        </div>
                        <div v-else class="modal-body px-4">
                            
                            <button v-if="!ownProfile && displayUser.modType != []" data-bs-toggle="modal" data-bs-target="#moderatormodal" class="btn btn-warning hover-button p-1 mb-3" style="border-radius: 20px; font-size: 0.8rem;">★ Certified Moderator</button> 
                            <button v-if="user && user.isAdmin" data-bs-toggle="modal" data-bs-target=“#moderatormodal class="btn btn-warning hover-button p-1 mb-3" style="border-radius: 20px; font-size: 0.8rem;">★ Certified Moderator</button>
                            <button type="button" class="btn-close uninvert" data-bs-dismiss="modal" aria-label="Close" style=" margin-left:63%;"></button>
                            <p><b>{{ displayUser.displayName }} is a moderator of the following communities:</b></p> 
                            <p>{{ drinkChoice }}</p>
                            <p><b><em>Moderators help shape the drinks community and ensure drink reviews remain fun, useful and respectful!</em></b></p>        
                            
                            <b><a v-if="user && !user.isAdmin" href="#" class="mt-3" data-bs-toggle="modal" data-bs-target="#applyModerator" style="color: black">Want to be a moderator? Apply here!</a></b>                    
                        </div>
                        

                        </div>


                        </div>

                    </div>

                    

                    <!-- join as a moderator modal end -->

                    <!-- Add/Remove modal start -->
                    <!-- Mod addition modal -->
                    <div class="modal fade" id="addModeratorModal" data-bs-backdrop="static" tabindex="-1" aria-labelledby="addModeratorLabel" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header" style="background-color: #535C72">
                                    <h1 class="modal-title fs-5" id="addModeratorLabel" style="color: white;">Add Moderator</h1>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>

                                <!-- Success remove mod modal body -->
                                <div v-if="successRemoveMod" class="modal-body text-center text-success fst-italic fw-bold fs-3">
                                    <span>User has successfully been removed as moderator!</span>
                                </div>
                                <!-- Error remove mod modal body -->
                                <div v-if="errorRemoveMod" class="modal-body text-center text-danger fst-italic fw-bold fs-3">
                                    <span>There is an error removing user as moderator, please try again!</span>
                                </div>
                                <!-- Success add mod modal body -->
                                <div v-if="successAddMod" class="modal-body text-center text-success fst-italic fw-bold fs-3">
                                    <span>User has successfully been added as moderator!</span>
                                </div>
                                <!-- Error add mod modal body -->
                                <div v-if="errorAddMod" class="modal-body text-center text-danger fst-italic fw-bold fs-3">
                                    <span>There is an error adding user as moderator, please try again!</span>
                                </div>
                                <!-- Initial select mode, add or remove moderator -->
                                <div v-if="chooseMod==''" class="modal-body">
                                    <button class="btn tertiary-btn reverse-clickable-text m-1" type="button" @click="addModMode">
                                        Add a moderator
                                    </button>      
                                    <button class="btn tertiary-btn reverse-clickable-text m-1" type="button" @click="removeModMode">
                                        Remove a moderator
                                    </button>      
                                </div>

                                <!-- Initial select user to promote -->
                                <div v-if="chooseMod=='add' && !doubleConfirmMod && !(successAddMod||errorAddMod||successRemoveMod||errorRemoveMod)" class="modal-body">                                    
                                    <div class="form-group mb-3">
                                        <p class="text-start mb-1"> Choose drink type that user can moderate: <span class="text-danger">*</span></p>
                                        <p v-html="formattedModTypes" class="text-start mb-1"></p>
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

                                <div v-if="chooseMod=='remove' && !doubleConfirmMod && !(successAddMod||errorAddMod||successRemoveMod||errorRemoveMod)" class="modal-body">                                    
                                    <div class="form-group mb-3">
                                        <p class="text-start mb-1"> Choose drink type for user to remove moderator rights: <span class="text-danger">*</span></p>
                                        <p v-html="formattedModTypes" class="text-start mb-1"></p>
                                        <input list="removableDrinkType" v-model="removedType" class="form-control" id="removedType" placeholder="Enter drink type" v-on:change="updateRemovedDrinkType">
                                        <datalist id="removableDrinkType">
                                            <option v-for="drinkType in removableDrinkType" :key="drinkType._id.$oid" :value="drinkType.drinkType">
                                                {{drinkType.drinkType}}
                                            </option>
                                        </datalist>
                                        <p v-show="promotedType.length > 0" class="text-start mb-1 text-danger" id="removedTypeError"></p>
                                    </div>
                                    <p class="text-start mb-1 text-danger" id="notModError"></p>
                                </div>

                                <!-- confirm mod to promote -->
                                <div v-if="chooseMod=='add' && doubleConfirmMod && !(successAddMod||errorAddMod||successRemoveMod||errorRemoveMod)" class="modal-body">
                                    <p class="text-start mb-1"> Do you really want to add <strong>{{ displayUser.username }}</strong> as a moderator for <strong>{{ promotedType }}</strong>? <span class="text-danger">*</span></p>
                                </div>
                                <div v-if="chooseMod=='remove' && doubleConfirmMod && !(successAddMod||errorAddMod||successRemoveMod||errorRemoveMod)" class="modal-body">
                                    <p class="text-start mb-1"> Do you really want to remove <strong>{{ displayUser.username }}</strong> as a moderator for <strong>{{ removedType }}</strong>? <span class="text-danger">*</span></p>
                                </div>

                                <!-- Initial confirm mod to promote to promote footer -->
                                <div v-if="(chooseMod=='add' || chooseMod=='remove') && !doubleConfirmMod && !(successAddMod||errorAddMod||successRemoveMod||errorRemoveMod)" class="modal-footer">
                                    <button type="button" @click="selectMode" class="btn btn-secondary">Return</button>
                                    <button v-if="chooseMod=='add'" type="button" @click="doubleConfirm" class="btn btn-primary">Add Moderator</button>
                                    <button v-if="chooseMod=='remove'" type="button" @click="doubleConfirm" class="btn btn-primary">Remove Moderator</button>
                                </div>

                                <!-- Double confirm mod to promote footer -->
                                <div v-if="(chooseMod=='add' || chooseMod=='remove') && doubleConfirmMod && !(successAddMod||errorAddMod||successRemoveMod||errorRemoveMod)" class="modal-footer">
                                    <button v-if="chooseMod=='add'" type="button" @click="addModMode" class="btn btn-secondary">Return</button>
                                    <button v-if="chooseMod=='remove'" type="button" @click="removeModMode" class="btn btn-secondary">Return</button>
                                    <button type="button" @click="confirmModifyModerator" class="btn btn-primary">Confirm Moderator</button>
                                </div>

                                <!-- successaddmod and erroraddmod footer -->
                                <div v-if="successAddMod||errorAddMod||successRemoveMod||errorRemoveMod" class="modal-footer">
                                    <button type="button" @click="selectMode" class="btn btn-secondary">Return</button>
                                    <button type="button" @click="selectMode" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Add/Remove moderator modal end -->


                    <!-- editProfileModal start -->
                    <div v-if="user" class="modal fade" id="editProfileModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered modal-lg">
                            <div class="modal-content">
                            <div class="modal-header">
                                <h1 class="modal-title fs-5" id="exampleModalLabel">Edit Profile</h1> 
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body text-center">
                                <!-- edit profile photo -->
                                <div class="edit-profile-pic">
                                    <div class="row mb-3">
                                        <div class="col-4 text-start ps-5" style="margin: auto;">
                                            Image Preview
                                        </div>
                                        <div class="col-8">
                                            <img :src="selectedImage || 'data:image/jpeg;base64,' + (user.photo || defaultProfilePhoto)" alt="" class="rounded-circle-no-bg border border-dark profile-img" id="output" style="height:auto; width:100%; ">
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <div class="col-4 text-start ps-5" style="margin: auto;">
                                            Edit Image
                                        </div>
                                        <div class="col-8">
                                            <input class="form-control" id="file" type="file" @change="loadFile" ref="fileInput"/>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- change drink of choice -->
                                <div class="edit-drink-choice">
                                    <div class="row">
                                        <div class="col-4 text-start ps-5" style="margin: auto;">
                                            Drink Choice
                                        </div>
                                        <div class="col-8 text-start">
                                            <!-- checkbox to choose drinks -->
                                            <div v-for="(type, index) in drinkType" :key="index" class="m-1" style="display: inline-block">
                                                <input type="checkbox" class="btn-check" :id="index" autocomplete="off" v-model="selectedDrinks" :value="type">
                                                <label v-if="selectedDrinks.includes(type)" class="btn primary-btn-less-round" :for="index" style="color: whitesmoke; background-color: #535C72; border: 4px solid #535C72;">{{type}}</label>
                                                <label v-else class="btn primary-btn-outline-less-round" :for="index">{{type}}</label>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="cancelChanges">Close</button>
                                <button type="button" class="btn btn-primary" @click="saveChangesDetails" data-bs-dismiss="modal">Save changes</button>
                            </div>
                            </div>
                        </div>
                    </div>
                    <!-- editProfileModal end -->

                    <!-- applyModerator start -->
                    <div v-if="user" class="modal fade" id="applyModerator" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                        <div class="modal-dialog modal-lg modal-dialog-centered">
                            <div class="modal-content" >
                                <div class="modal-header" style="background-color: #535C72"> <!-- style="background-color: #DDC8A9;"-->
                                    <p class="modal-title fs-5" style="color: white;">
                                      <b>Apply to be a moderator!</b>
                                    </p>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body  px-5"> <!--text-center-->
                                    <div class="row">

                                        <div style="max-width:110px;">
                                            <svg v-if="photo == ''" xmlns="http://www.w3.org/2000/svg" style="height:auto; width:100%; " class="rounded-circle-no-bg border border-dark profile-img" >
                                                <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                                                <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                                            </svg>
                                            <img v-else :src="'data:image/png;base64,'+ photo" style="height:auto; width:100%;" class="rounded-circle-no-bg border border-dark profile-img" >
                                        </div>
                                        <div style="max-width:170px;" class="px-0">
                                            <button class="btn btn-warning hover-button p-1" style="border-radius: 20px; font-size: 0.8rem;">★ Certified Moderator</button> 
                                        </div>
                                    </div>


                                    <p class="fs-5"><b>Help shape the drinks community and share your expertise as a moderator! Just some quick questions:</b></p>
                                    <!--- <a href="#" class="m-2" style="font-style: italic; color: inherit">Click here to learn more about being a moderator</a>-->
                                    
                                    <div class="px-3">
                                        <h6 class="m-3 mx-0">What drinks category would you like to moderate for?</h6>
                                        <select class="form-select w-50 mx-auto" style="border: 2px solid #535C72;" aria-label="Default select example" v-model="modCat">
                                            <option v-for="(type, index) in filteredDrinkType" :key="index" :value="type">{{type}}</option>
                                        </select>
                                        <h6 class="m-3 mx-0">Why do you want to be a Drink X moderator? What's your experience with this drink category?</h6>
                                        <div class="mb-3">
                                            <textarea class="form-control Xw-50 mx-auto" style="border: 2px solid #535C72;" id="exampleFormControlTextarea1" rows="3" v-model="modDesc"></textarea>
                                        </div>
                                    </div>
                                    <btn class="btn secondary-btn-border " data-bs-dismiss="modal" @click="submitModeratorApplication" style="margin-right: 40%;margin-left:40%;"><b>Apply Now!</b></btn>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- applyModerator end -->

                    <!-- Change Password start -->
                    <div v-if="user" class="modal fade" id="changePasswordModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header" style="background-color: #535C72">
                                    <h1 class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Change Password</h1>
                                    <button type="button" @click="resetChangePassword" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <!-- Initial select mode, change or reset password -->
                                <div v-if="changingPassword==''" class="modal-body">
                                    <button class="btn tertiary-btn reverse-clickable-text m-1" type="button" @click="changePasswordMode('change')">
                                        Change Password
                                    </button>      
                                    <button class="btn tertiary-btn reverse-clickable-text m-1" type="button" @click="changePasswordMode('reset')">
                                        Reset Password
                                    </button>      
                                </div>
                                <div class="modal-body text-center">
                                    <div v-if="changingPassword =='change' && !(confirmChangePassword||passwordError||passwordSuccess||passwordMismatch)">
                                        <p class="text-start mb-1"> Old Password: <span class="text-danger">*</span></p>
                                        <input type='password' v-model="oldPassword" class="form-control" id="oldPassword" placeholder="Enter Previous Password">
                                        <p class="text-start mt-3 mb-1"> New Password: <span class="text-danger">*</span></p>
                                        <input type='password' v-model="newPassword" class="form-control" id="newPassword" placeholder="Enter New Password">
                                    </div>  
                                    <div v-if="confirmChangePassword && !(passwordError||passwordSuccess||passwordMismatch)">
                                        <b>Are you sure you want to change password?</b>
                                    </div>
                                    <div v-if="changingPassword =='reset' && !(confirmResetPassword||passwordError||passwordSuccess)">
                                        <p>Please key in OTP sent to your email:</p>
                                        <div class = "input-group">
                                            <input type='text' class="form-control" placeholder="Enter OTP" v-model="resetPin">
                                            <button :disabled="isButtonDisabled" class="btn btn-outline-secondary" type="button" id="resendPin" @click="sendResetPin">Send Pin</button>
                                        </div>
                                        <!-- <p v-show="isButtonDisabled" class="text-start mb-1 text-success" id="sendPinSuccess"></p> -->
                                        <p v-show="isButtonDisabled" class="text-start mb-1 text-success" id="sendPinSuccess"></p>
                                        <p v-show="isButtonDisabled" class="text-start mb-1 text-danger" id="sendPinError"></p>
                                        <p v-show="verifyErrorMessage.length>0" class="text-start mb-1 text-danger">{{ verifyErrorMessage }}</p>
                                    </div>  
                                    <div v-if="confirmResetPassword && !(passwordError||passwordSuccess||resettingPassword)">
                                        <b>Are you sure you want to reset your password? A new password will be sent to you.</b>
                                    </div>
                                    <div v-if="confirmResetPassword && resettingPassword && !(passwordError||passwordSuccess)">
                                        <b>Please wait while password is being resetted.</b>
                                    </div>
                                    
                                    <!-- if password change/reset is successful -->
                                    <p v-if="passwordSuccess" class="text-success fst-italic fw-bold fs-3">Password {{ changingPassword }} is successful!</p>
                                    <p v-if="passwordSuccess && confirmResetPassword" class="text-success fst-italic fw-bold fs-3">An email has been sent to you containing the password.</p>
                                    
                                    <!-- if password change/reset faces error -->
                                    <p v-if="passwordError" class ="text-danger fst-italic fw-bold fs-3">There is an error during password {{ changingPassword }}, please try again!</p>
                                    <p v-if="passwordMismatch" class ="text-danger fst-italic fw-bold fs-3">Old password do not match, please try again</p>
                                </div>

                                <div class="modal-footer">
                                    <!-- To return to previous select change password or reset password -->
                                    <button v-if="changingPassword!='' && !resettingPassword" type="button" @click="selectPasswordMode" class="btn btn-secondary">Return</button>

                                    <!-- Close modal-->
                                    <button v-if="!resettingPassword" type="button" @click="resetChangePassword" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>

                                    <!-- Change password first confirmation and second confirmation -->
                                    <button v-if="changingPassword == 'change' && !(confirmChangePassword||passwordError||passwordSuccess||passwordMismatch||resettingPassword)" type="button" @click="updatePassword" class="btn btn-primary">Change Password</button>
                                    <button v-if="confirmChangePassword && !(passwordError||passwordSuccess||passwordMismatch||resettingPassword)" type="button" @click="confirmUpdatePassword" class="btn btn-primary">Update Password</button>
                                    
                                    <!-- Reset password first confirmation and second confirmation -->
                                    <button v-if="changingPassword == 'reset' && !(confirmResetPassword||passwordError||passwordSuccess||resettingPassword)" type="button" @click="verifyOTP" class="btn btn-primary">Verify OTP</button>
                                    <button v-if="confirmResetPassword && !(passwordError||passwordSuccess||resettingPassword)" type="button" @click="resetPassword" class="btn btn-primary">Reset Password</button>
                                    
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Change password end -->


                    <!-- badges -->
                    <div class="mt-3">
                        <h3 class="mobile-view-hide">Badges Unlocked</h3>
                        <p class="mobile-view-show"><strong>Badges Unlocked</strong></p>
                        <!--<hr>-->

                        <div v-if="topCategoriesReviewed.length == 0 && otherBadges.length == 0">
                            You have no badges yet.
                        </div>

                        <div v-else class="container text-center mb-3">
                            <!-- badges for different drink types -->
                            <div class="row">
                                <div class="mobile-col-3 col-12 col-sm-4 col-md-6 col-xl-4 p-2 mobile-pt-0 mobile-pb-0 mobile-pe-2 mobile-mb-2 " v-for="drinkTypeDetails in matchedDrinkTypes" :key="drinkTypeDetails._id">
                                    <!-- image of actual badge  style="width: 100px; height: 100px;"  -->
                                    <img :src="'data:image/png;base64,'+ (drinkTypeDetails.badgePhoto || defaultProfilePhoto)" 
                                        
                                        alt="" class="rounded-circle-white-bg border border-dark badge-img">
                                    <!-- badge description -->
                                    <div class="pt-1" style="line-height: 1;"> 
                                        <small> 
                                            <b> {{ drinkTypeDetails.drinkType }} {{ categoryBadges[drinkTypeDetails.drinkType] }} </b>
                                        </small>
                                        <br>
                                        <small class="xs-text" v-for="(subcategory, category) of topSubcategoriesReviewed" :key="category">
                                            <span v-if="category === drinkTypeDetails.drinkType">
                                                <i>
                                                    (Power: <span v-for="item in subcategory" :key="item">
                                                        {{ item }}<span v-if="subcategory.indexOf(item) !== subcategory.length - 1">, </span>
                                                    </span>)
                                                </i>
                                            </span>
                                        </small>
                                    </div>
                                </div>
                            </div>
                            <!-- badges based on other user activities -->
                            <div class="row">
                                <div class="mobile-col-3 col-12 col-sm-4 col-md-6 col-xl-4 p-2 mobile-pt-0 mobile-pb-0 mobile-pe-2 mobile-mb-2" v-for="badge in otherBadges" :key="badge">
                                    <!-- image of actual badge style="width: 100px; height: 100px;" -->
                                    <img :src="'data:image/png;base64,'+ (getBadgeInfo(badge).badgePhoto)" 
                                         
                                        alt="" class="rounded-circle-white-bg border border-dark badge-img">
                                    <!-- badge description -->
                                    <p class="pt-1" style="line-height: 1;"> 
                                        <small> 
                                            <b> {{ getBadgeInfo(badge).badgeDesc }} </b>
                                        </small> 
                                    </p>
                                </div>
                            </div>
                        </div>
                        
                        <div>
                            <a href="#" style="color: black">Learn more about badges.</a>
                        </div>

                    </div>
                    
                </div>

            </div>

            <!-- reviews and lists -->
            <div class="col-12 col-md-8">

                <!-- reviews button -->
                <button 
                    class="btn mx-1"
                    :class="{ 'active-toggle-button-user-profile': activeTab === 'reviews', 'inactive-toggle-button-user-profile': activeTab !== 'reviews' }"
                    @click="switchTab('reviews')"> 
                    Reviews 
                </button>
                <button 
                    class="btn mx-1"
                    :class="{ 'active-toggle-button-user-profile': activeTab !== 'reviews', 'inactive-toggle-button-user-profile': activeTab === 'reviews' }"
                    @click="switchTab('lists')"> 
                    <span v-if="ownProfile">My Drink List</span>
                    <span v-if="!ownProfile">Drink List</span> 
                </button>

                <div class="tab-content container mt-2 mobile-px-0" >
                    <!-- reviews tab -->
                    <div v-if="activeTab == 'reviews'" id="reviews">
                        <h3 class="text-body-secondary text-start pt-4"> 
                            <b> Recent Reviews </b> 
                        </h3>
                        <div v-if="Object.keys(recentReviews).length > 0">
                            <div v-for="(review, index) in recentReviews.slice(0, 5)" :key="index">  
                                <div style="display: flex" class="row">
                                    <div class="col-3 mobile-col-3 mobile-pe-0">
                                        <img :src=" 'data:image/png;base64,' + (review.photo||defaultDrinkImage)" alt="" class="rounded bottle-img "> <!--me-3-->
                                        <p class="fs-4 mobile-fs-5 fw-bold rating-text text-center mobile-mb-1" >
                                            {{ review.rating }}
                                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-star-fill " viewBox="0 0 16 16">
                                                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                            </svg>
                                        </p>
                                    </div>
                                    <div class="col-9 mobile-col-9 mobile-ps-2">
                                        <a :href="'/listing/view/' + review.reviewTarget.$oid" style="text-decoration: none; color: #223957;">
                                            <p class="fs-5 mobile-fs-7 mb-1 mobile-mb-0_5" ><b>{{ getListingName(review.reviewTarget) }}</b></p>
                                        </a>
                                        <!-- flavor tag -->
                                            
                                            <span v-for="(tag, index) in review.flavorTag" :key="index" class="mobile-view-hide badge rounded-pill-user-profile me-2 mb-1 mobile-me-0_5 mobile-mb-0_5 " :style="{ backgroundColor: getTagColor(tag) }"> {{ getTagName(tag) }}</span>
                                            <span v-for="(tag, index) in review.observationTag" :key="index" class="mobile-view-hide badge rounded-pill-user-profile me-2 mb-1 mobile-me-0_5 mobile-mb-0_5" style="background-color: grey;">{{ tag }}</span>

                                            <span v-for="(tag, index) in review.flavorTag.slice(0, 2)" :key="index" class="mobile-view-show badge rounded-pill-user-profile me-2 mb-1 mobile-me-0_5 mobile-mb-0_5 " :style="{ backgroundColor: getTagColor(tag) }"> {{ getTagName(tag) }}</span>
                                            <span v-for="(tag, index) in review.observationTag.slice(0, 1)" :key="index" class="mobile-view-show badge rounded-pill-user-profile me-2 mb-1 mobile-me-0_5 mobile-mb-0_5" style="background-color: grey;">{{ tag }}</span>                                        
                                        <p class="mobile-fs-7">
                                            <b>{{ review.reviewTitle }}</b> <br v-if="review.reviewTitle">
                                            {{ review.reviewDesc }}
                                        </p>
                                        
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-else class="container m-2">
                            No reviews yet. To explore more drinks in the home page, 
                            <router-link to="/" style="color: inherit;">click here</router-link>. 
                        </div>

                        <ListingRowDisplayUserProfile 
                            :listingArr="favouriteListings" 
                            displayName="Favourite Listings" 
                            :user="user" 
                            :listing="listing" 
                            columnWidth="165px"
                            @icon-clicked="handleIconClick"/>

                        <ListingRowDisplayUserProfile 
                            :listingArr="recentActivity" 
                            displayName="Recent Activity" 
                            :user="user" 
                            :listing="listing" 
                            columnWidth="165px"
                            @icon-clicked="handleIconClick"/>



                    </div>

                    <!-- lists tab -->
                    <div v-if="activeTab == 'lists'" id="lists">
                        <button v-if="ownProfile" type="button" class="btn primary-btn-outline-less-round mb-3" data-bs-toggle="modal" data-bs-target="#createNewListModal" >Create New List</button>

                        <!-- create new list modal -->
                        <div class="modal fade" id="createNewListModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                            <div class="modal-dialog modal-dialog-centered">
                                <div class="modal-content">
                                <div class="modal-header">
                                    <h1 class="modal-title fs-5" id="exampleModalLabel">Create New List</h1>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <div class="mb-3">
                                        <label for="basic-url" class="form-label">List Name</label>
                                        <div class="input-group mb-3">
                                            <input v-model="newListName" type="text" class="form-control" placeholder="List Name" aria-label="Username" aria-describedby="basic-addon1">
                                        </div>
                                        <div v-if="newListNameError" class="text-danger text-sm">
                                            *{{ newListNameError }}
                                        </div>
                                    </div>

                                    <div class="mb-3">
                                        <label for="basic-url" class="form-label">List Description</label>
                                        <div class="input-group mb-3">
                                            <textarea v-model="newListDesc" type="text" class="form-control" placeholder="List Description (Optional)" aria-label="Username" aria-describedby="basic-addon1" rows="5"></textarea>
                                        </div>
                                    </div>

                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                    <button type="button" class="btn btn-primary" @click="addNewList">Save changes</button>
                                </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- display all lists -->
                        <div v-for="(bookmarkList, name, index) in displayUserBookmarks" :key="name" style="display: flex" class="row mb-3">
                            <div class="col-3 mobile-col-4 mobile-pe-0" >
                                <img :src=" 'data:image/png;base64,' + (photo || defaultDrinkImage)" alt="" class="bottle-img me-3">
                            </div>
                            <div  class="col-9 mobile-col-8 mobile-ps-1" > <!-- style="height: 150px; display: flex; flex-direction: column;" -->
                                <h5 class="mt-1" @click="viewList(name)" style="cursor: pointer"> {{ name }} </h5>
                                <span v-if="bookmarkList.listItems.length > 1"> {{ bookmarkList.listItems.length }} items in list </span>
                                <span v-else> {{ bookmarkList.listItems.length }} item in list </span>
                                <div style="max-height: 48px; overflow-y: auto; font-style: italic;">
                                    {{ bookmarkList.listDesc }}
                                </div>
                                <div style="display: flex; margin-top: auto;" class="mb-1">
                                    <b><a class="me-4 mobile-view-hide" @click="viewList(name)" href="#" style="color: #535C72;">View List</a></b>
                                    <b><a class="me-4 mobile-view-show" @click="viewList(name)" href="#" style="color: #535C72;">View</a></b>
                                    <b><a v-if="ownProfile && !(name == 'Drinks I Have Tried' || name == 'Drinks I Want To Try')" class="mobile-view-hide me-2" href="#" style="color: #535C72;" data-bs-toggle="modal" :data-bs-target="`#editListModal${index}`" @click="resetEditList(name, bookmarkList.listDesc)">Edit List</a></b>
                                    <b><a v-if="ownProfile && !(name == 'Drinks I Have Tried' || name == 'Drinks I Want To Try')"  class="mobile-view-hide " href="#" style="color: #535C72;" data-bs-toggle="modal" :data-bs-target="`#deleteListModal${index}`">Delete List</a></b>
                                    <b><a v-if="ownProfile && !(name == 'Drinks I Have Tried' || name == 'Drinks I Want To Try')" class="mobile-view-show me-2" href="#" style="color: #535C72;" data-bs-toggle="modal" :data-bs-target="`#editListModal${index}`" @click="resetEditList(name, bookmarkList.listDesc)">Edit</a></b>
                                    <b><a v-if="ownProfile && !(name == 'Drinks I Have Tried' || name == 'Drinks I Want To Try')" class="mobile-view-show" href="#" style="color: #535C72;" data-bs-toggle="modal" :data-bs-target="`#deleteListModal${index}`">Delete</a></b>
                                </div>
                            </div>

                            <!-- edit list modal start -->
                            <div class="modal fade" :id="`editListModal${index}`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-dialog-centered">
                                <div class="modal-content">
                                <div class="modal-header">
                                    <h1 class="modal-title fs-5" id="exampleModalLabel">Edit List</h1>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <div class="mb-3">
                                        <label for="basic-url" class="form-label">List Name</label>
                                        <div class="input-group mb-3">
                                            <input v-model="editListName" type="text" class="form-control" :placeholder="name" aria-label="Username" aria-describedby="basic-addon1">
                                        </div>
                                        <div v-if="editListNameError" class="text-danger text-sm">
                                            *{{ editListNameError }}
                                        </div>
                                    </div>

                                    <div class="mb-3">
                                        <label for="basic-url" class="form-label">List Description</label>
                                        <div class="input-group mb-3">
                                            <textarea v-model="editListDesc" type="text" class="form-control" :placeholder="bookmarkList.listDesc" aria-label="Username" aria-describedby="basic-addon1" rows="5"></textarea>
                                        </div>
                                    </div>

                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                    <button type="button" class="btn btn-primary" @click="editList(name)">Save changes</button>
                                </div>
                                </div>
                            </div>
                            </div>
                            <!-- modal end -->

                            <!-- delete list modal start -->
                            <div class="modal fade" :id="`deleteListModal${index}`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-dialog-centered">
                                    <div class="modal-content">
                                        <div class="text-end mt-2 me-2">
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>

                                        <div class="text-center">
                                            <img src="../../../Images/Others/cancel.png" alt="" class="rounded-circle border border-dark text-center" style="width: 100px; height: 100px;">
                                            <h3>Are you sure?</h3>
                                            <br>
                                            <p>Do you really want to delete <b><i>{{ name }}</i></b>? </p>
                                        </div>
                                        <div style="display: inline" class="text-center mb-4">
                                            <button type="button" class="btn btn-secondary me-3" data-bs-dismiss="modal">Cancel</button>
                                            <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="deleteList(name)">Delete</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- modal end -->
                        </div>
                    </div>

                    <!-- individual list tab -->
                    <div v-if="activeTab == 'list' && displayUser.drinkLists" id="list">

                        <!-- list name, back to lists & add drink to list & share button -->
                        <div class="row mb-4">
                            <div class="col-12 col-md-5">
                                <h3>{{currentList}}</h3>
                            </div>
                            <div class="col-12 col-md-7 text-end">
                                <button v-if="ownProfile" type="button" class="btn primary-btn-outline-less-round" data-bs-toggle="modal" data-bs-target="#exampleModal">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-square mb-1 me-1" viewBox="0 0 16 16">
                                    <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z"/>
                                    <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
                                    </svg>
                                    Add Drink
                                </button>
                                <button @click="updateCurrentURL" type="button" class="btn primary-btn-outline-less-round ms-3" data-bs-toggle="modal" data-bs-target="#shareListModal">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-share mb-1 me-1" viewBox="0 0 16 16">
                                    <path d="M13.5 1a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3M11 2.5a2.5 2.5 0 1 1 .603 1.628l-6.718 3.12a2.5 2.5 0 0 1 0 1.504l6.718 3.12a2.5 2.5 0 1 1-.488.876l-6.718-3.12a2.5 2.5 0 1 1 0-3.256l6.718-3.12A2.5 2.5 0 0 1 11 2.5m-8.5 4a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3m11 5.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3"/>
                                    </svg>
                                    Share List
                                </button>
                                <button @click="viewList('lists')" type="button" class="btn primary-btn-outline-less-round ms-3">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-left-circle mb-1 me-1" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-4.5-.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"/>
                                    </svg>
                                    Back to Lists
                                </button>

                                <!-- Share Menu Modal (QR Code) -->
                                <div class="modal fade" id="shareListModal" tabindex="-1" aria-labelledby="shareListModalLabel" aria-hidden="true">
                                    <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h1 class="modal-title fs-5" id="shareMenuModalLabel"> Drink List QR Code </h1>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <div class="centered">
                                                    <qr-code v-bind:text="currentURL" ref="qrCode"></qr-code>
                                                </div>
                                                <div class="input-group pt-3">
                                                    <input type="text" class="form-control" aria-label="Link" aria-describedby="button-addon2" v-bind:value="currentURL" disabled>
                                                    <button class="btn btn-outline-secondary" type="button" id="button-addon2" @click="copyToClipboard(currentURL)">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16">
                                                            <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1z"/>
                                                            <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0z"/>
                                                        </svg>
                                                    </button>
                                                </div>
                                                <p class="text-start pt-2" v-if="clipboardItem"> 
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-check" viewBox="0 0 16 16">
                                                        <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425z"/>
                                                    </svg>
                                                    Copied to clipboard!
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>

                        <!-- add drink modal -->
                        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                                <div class="modal-content">
                                <div class="modal-header">
                                    <h5>Add Drink to List: {{currentList}}</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body" style="height: 400px;">
                                    <!-- search -->
                                    <div>
                                        <!-- search bar  -->
                                        <div class="input-group mb-3">
                                            <input type="text" class="form-control" placeholder="Search for drink" aria-label="Recipient's username" aria-describedby="button-addon2" v-model="drinkSearch" @keyup="searchResult">
                                        </div>
                                        <!-- search results -->
                                        <div class="overflow-auto" :style="{ height: drinksToAdd.length > 0 ? '200px' : '300px' }">
                                            <div class="form-check" v-for="(drinkName, index) in drinkSearchResults" :key="index">
                                                <input class="form-check-input" type="checkbox" :value="drinkName" :id="'drinkCheckbox' + index" v-model="drinksToAdd">
                                                <label class="form-check-label" :for="'drinkCheckbox' + index">
                                                    {{ drinkName }}
                                                </label>
                                            </div>
                                        </div>
                                    </div>
                                    <!-- selected results -->
                                    <div v-if="drinksToAdd.length > 0" class="mt-2">
                                        <hr>
                                        <div class="overflow-auto" style="height: 75px">
                                            <b>Selected Drinks: </b>
                                            {{ drinksToAdd.join(', ') }}
                                        </div>
                                    </div>

                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-primary" @click="addDrinkToList(currentList)">Add to List</button>
                                </div>
                                </div>
                            </div>
                        </div>

                        <!-- list details -->
                        <div class="row mb-3" v-for="(listingID, index) in displayUser.drinkLists[currentList].listItems" :key="index">
                            <div class="col-10" style="display: flex">
                                <img :src=" 'data:image/png;base64,' + ( getListingFromID(listingID[1].$oid).photo || defaultDrinkImage )" alt="" class="bottle-img me-3">
                                <div style="min-height: 150px; display: flex; flex-direction: column;">
                                    <a :href="'/listing/view/' + listingID[1].$oid" style="text-decoration: none; color: inherit;">
                                        <h4>{{ getListingFromID(listingID[1].$oid).listingName }}</h4>
                                    </a>
                                    <p style="display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;"> {{ getListingFromID(listingID[1].$oid).officialDesc }} </p>
                                    <div v-if="ownProfile" style="display: flex; margin-top: auto" class="mb-0">
                                        <a href="#" style="text-decoration: none; color: #535C72;" data-bs-toggle="modal" :data-bs-target="`#deleteFromListModal${index}`">
                                            <!-- cross icon -->
                                            <svg class=mb-1 xmlns="http://www.w3.org/2000/svg" height="16" width="12" viewBox="0 0 384 512">
                                                <!--! Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc. -->
                                                <path d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"/>
                                            </svg>
                                            Delete from list
                                        </a>
                                    </div>

                                </div>
                            </div>
                            <div class="col-2 text-end">
                                <h2>
                                    {{ getAverageReview(listingID[1]) }}
                                    <svg class="mb-2" xmlns="http://www.w3.org/2000/svg" height="18" width="20.25" viewBox="0 0 576 512">
                                        <!--! Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc. -->
                                        <path d="M287.9 0c9.2 0 17.6 5.2 21.6 13.5l68.6 141.3 153.2 22.6c9 1.3 16.5 7.6 19.3 16.3s.5 18.1-5.9 24.5L433.6 328.4l26.2 155.6c1.5 9-2.2 18.1-9.7 23.5s-17.3 6-25.3 1.7l-137-73.2L151 509.1c-8.1 4.3-17.9 3.7-25.3-1.7s-11.2-14.5-9.7-23.5l26.2-155.6L31.1 218.2c-6.5-6.4-8.7-15.9-5.9-24.5s10.3-14.9 19.3-16.3l153.2-22.6L266.3 13.5C270.4 5.2 278.7 0 287.9 0zm0 79L235.4 187.2c-3.5 7.1-10.2 12.1-18.1 13.3L99 217.9 184.9 303c5.5 5.5 8.1 13.3 6.8 21L171.4 443.7l105.2-56.2c7.1-3.8 15.6-3.8 22.6 0l105.2 56.2L384.2 324.1c-1.3-7.7 1.2-15.5 6.8-21l85.9-85.1L358.6 200.5c-7.8-1.2-14.6-6.1-18.1-13.3L287.9 79z"/>
                                    </svg>
                                </h2>
                            </div>

                            <!-- delete from list modal start -->
                            <div class="modal fade" :id="`deleteFromListModal${index}`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-dialog-centered">
                                    <div class="modal-content">
                                        <div class="text-end mt-2 me-2">
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>

                                        <div class="text-center mx-2">
                                            <img src="../../../Images/Others/cancel.png" alt="" class="rounded-circle border border-dark text-center" style="width: 100px; height: 100px;">
                                            <h3>Are you sure?</h3>
                                            <br>
                                            <p>Do you really want to delete <b><i>{{ getListingFromID(listingID[1].$oid).listingName }}</i></b> from <b><i>{{ currentList }}</i></b>? </p>
                                        </div>
                                        <div style="display: inline" class="text-center mb-4">
                                            <button type="button" class="btn btn-secondary me-3" data-bs-dismiss="modal">Cancel</button>
                                            <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="deleteFromList(currentList, listingID)">Delete</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- modal end -->
                        </div>
                    
                    </div>
                </div>

            </div>
        </div>
        <BookmarkModal 
            v-if="user" 
            :user="user" 
            :listings="listings" 
            :listingID="bookmarkListingID" />
        
    </div>
    


 
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import ListingRowDisplayUserProfile from '@/components/ListingRowDisplayUserProfile.vue';
import BookmarkModal from '@/components/BookmarkModal.vue';



// toggling between lists and list details
export default {
    components: {
        NavBar, 
        ListingRowDisplayUserProfile, 
        BookmarkModal
    },
    data() {
        return {
            dataLoaded: false,
            currentURL: "",
            // default images
            defaultDrinkImage: "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",
            defaultProfilePhoto: "/9j/4AAQSkZJRgABAQEASABIAAD/4Qm+aHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLwA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/PiA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyI+IDxkYzpjcmVhdG9yPiA8cmRmOlNlcT4gPHJkZjpsaT5WZWN0b3JTdG9jay5jb20vNDI0MTE1NDA8L3JkZjpsaT4gPC9yZGY6U2VxPiA8L2RjOmNyZWF0b3I+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDw/eHBhY2tldCBlbmQ9InciPz7/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAD6APkDAREAAhEBAxEB/8QAHAABAAIDAQEBAAAAAAAAAAAAAAMGBAUH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",
            
            //personal profile image
            photo: '',
            profileURL: '/login',
            onProfile: false,

            // user details
            loggedIn: false,
            userID: "",
            user: {},
            userBookmarks: {},
            ownProfile: false,

            // user being viewed
            displayUserID: null,
            displayUser: {},
            drinkChoice: "",
            drinkCount: 0,
            joinDate: "",
            following: false,

            // data from database
            listings: [],
            producers: [],
            venues: [],
            reviews: [],
            reversedReviews: [],
            users: [],
            drinkCategories: [],
            drinkTypes: [],
            badges: [],
            drinkType: [],
            subTags: null,
            flavourTags: null,

            filteredDrinkType: [],

            // data for tab
            showCurrentContent: true, 
            activeTab: 'reviews',

            // image upload
            selectedImage: null,
            selectedDrinks: [],
            image64: null,

            // display user drink activity
            favouriteListings: {},
            recentActivity: {},
            recentReviews: {},

            // create list
            currentList: "",
            newListName: "",
            newListDesc: "",
            newListNameError: "",

            // edit list
            editListName: "",
            editListDesc: "",
            editListNameError: "",

            // add or edit drink from list
            drinksToAdd: [],
            drinkSearch: "",
            drinkSearchResults: [],

            // mod request
            modType: "",
            modDesc: "",

            // for bookmark component
            bookmarkListingID: {},

            // flags and variables for adding moderator
            successAddMod:false,
            successRemoveMod:false,
            errorRemoveMod:false,
            errorAddMod:false,
            addableDrinkType:[],
            removableDrinkType:[],
            promotedType:"",
            removedType:"",
            selectedPromotedType:null,
            selectedRemoveType:null,
            chooseMod:"",
            doubleConfirmMod:false,

            // flags and variables for changing/resetting password
            oldPassword:"",
            newPassword:"",
            changingPassword:"",
            confirmChangePassword: false,
            confirmResetPassword: false,
            passwordError: false,
            passwordSuccess: false,
            passwordMismatch: false,
            resetPin: "",
            isButtonDisabled: false,
            verifyErrorMessage:"",
            resettingPassword:false,

            // for badges
            allListingsReviewedByUser: [],
            allCategoriesReviewedByUser: {},
            allSubCategoriesReviewedByUser: {},
            matchedDrinkTypes: [],
            topCategoriesReviewed: [],
            topSubcategoriesReviewed: {},
            reviewCountriesTagged: [],
            badgeLevels: { // CHANGE THIS! if there is a change in criterion for minimum # of reviews that a user needs to gain a badge level
                novice: 3,
                lover: 10,
                master: 30,
            },
            categoryBadges: {},
            otherBadgesLimit: { // CHANGE THIS! if there is a change in minimum # that a user needs to gain a badge level
                reviewDrinkCategory: 10,
                tagFriend: 3,
                tagLocation: 5,
                tagCountry: 3,
                upvotes: 10
            },
            otherBadges: [],

            // for points
            pointSystem: { // CHANGE THIS! if there is a change in the point system (just change this.pointsDefault to a numerical value for the corresponding criteria)
                // format: { action: [count, points] }
                logReview: [0, 50], // log a review
                tagFriend: [0, 50], // tag a friend
                tagLocation: [0, 50], // tag a location
                tagCountry: [0, 50], // tag a country
                askProducer: [0, 50], // ask a producer a question
                askVenue: [0, 50], // ask a venue a question
            },
            totalPoints: 0,
        };  
    },
    computed: {
        formattedModTypes() {
            // Join the modType array elements with commas and spaces
            if(this.displayUser.modType.length === 0){
                return "This user is currently not a moderator!"
            }
            else{
                return "This user is currently a moderator for <b>" + this.displayUser.modType.join(', ') +"</b>!";
            }
        },
    },
    mounted() {

        // Obtain user's profile picture + set profile URL
        if (localStorage.getItem('88B_accID') != null) {

        this.accType = localStorage.getItem('88B_accType');
        let accID = localStorage.getItem('88B_accID');
        let url = 'http://127.0.0.1:5000/get';

        if (this.accType == 'user') {
            url = url + 'User/' + accID;
            this.loadData(url);

            this.profileURL = '/profile/user/'+accID;
            this.dashboardURL = '/dashboard/user';
            this.dashboardWord = 'Drink';
        } 
        else if (this.accType == 'producer') {
            url = url + 'Producer/' + accID;
            this.loadData(url);

            this.profileURL = '/profile/producer/' + accID;
            this.dashboardURL = '/Producers/ProducersDashboard/' + accID;
            this.dashboardWord = 'Brand';
            
        } 
        else if (this.accType == 'venue') {
            url = url + 'Venue/' + accID;
            this.loadData(url);

            this.profileURL = '/profile/venue';
            this.dashboardURL = '/dashboard/venue';
            this.dashboardWord = 'Venue';
        }

        // check if current page is profile page
        if (this.$route.path.split('/')[1] == 'profile') {
            this.onProfile = true;
        }

        // check if current page is create listing page
        if (this.$route.path.split('/').length >= 3 && this.$route.path.split('/')[2] == 'create') {
            this.onCreate = true;
        }

        // check if current page is request page
        if (this.$route.path.split('/')[1] == 'request') {
            this.onRequest = true;
        }
        }

        // get local storage
        const accID = localStorage.getItem("88B_accID");
        if(accID !== null){
            this.userID = localStorage.getItem('88B_accID')
            this.loggedIn = true
        }

        // get displayUserID from URL
        try {
            this.displayUserID = this.$route.params.userID;
            if (this.displayUserID === this.userID) {
                this.$router.push('/profile/user');
            }
            else if (!this.displayUserID) {
                this.displayUserID = this.userID;
            }
        }
        catch (error) {
            console.error(error);
        }

        // get list name from URL
        try {
            if (this.$route.params.listName) {
                this.currentList = this.$route.params.listName;
                this.activeTab = 'list';
            } else {
                this.currentList = "";
            
            }
        }
        catch (error) {
            console.error(error);
        }
        
        // load data
        this.loadData();
    },
    methods: {
        // load data from database
        async loadData(url) {
            //profile picture
            if (url){
                try {
                    const response = await this.$axios.get(url);
                    this.photo = response.data["photo"];

                if (this.accType == 'user') {
                    if (response.data.isAdmin) {
                        this.isAdmin = true;
                    }
                    if (Array.isArray(response.data.modType) && response.data.modType.length > 0) {
                        this.isModerator = true;
                    }
                }
            } 
            catch (error) {
                console.error(error);
            }
            }

            // Listings
            try {
                const response = await this.$axios.get('http://127.0.0.1:5000/getListings');
                this.listings = response.data;
                // originally, make filteredListings the entire collection of listings
                this.filteredListings = this.listings;
            } 
            catch (error) {
                console.error(error);
                this.dataLoaded = null;
            }
            // Reviews
            try {
                const response = await this.$axios.get('http://127.0.0.1:5000/getReviews');
                this.reviews = response.data;
                this.reversedReviews = this.reviews.reverse();
                this.recentReviews = this.reversedReviews.filter(review => review.userID?.$oid === this.displayUserID && review.reviewType === 'Listing');
            }
            catch (error) {
                console.error(error);
                this.dataLoaded = null;
            }
            // Producers
            try {
                const response = await this.$axios.get('http://127.0.0.1:5000/getProducers');
                this.producers = response.data;
                this.dataLoaded = true;
            } 
            catch (error) {
                console.error(error);
                this.dataLoaded = null;
            }
            // Venues
            try {
                const response = await this.$axios.get('http://127.0.0.1:5000/getVenues');
                this.venues = response.data;
                this.dataLoaded = true;
            } 
            catch (error) {
                console.error(error);
                this.dataLoaded = null;
            }
            // for Badges
            try {
                const response = await this.$axios.get('http://127.0.0.1:5000/getBadges');
                this.badges = response.data;
                this.dataLoaded = true;
            } 
            catch (error) {
                console.error(error);
                this.dataLoaded = null;
            }
            // Users
            try {
                const response = await this.$axios.get('http://127.0.0.1:5000/getUsers');
                this.users = response.data;
                this.user = this.getUser(this.userID);
                this.displayUser = this.getUser(this.displayUserID);
                
                if (this.userID === this.displayUserID) {
                    this.ownProfile = true;
                }
                else {
                    this.ownProfile = false;
                }

                this.drinkChoice = this.getDrinkOfChoice();
                this.drinkCount = this.getDrinkCount();
                if (this.user) {
                    // join date
                    const dateString = this.user.joinDate.$date;
                    const dateParts = dateString.split('-');
                    const year = dateParts[0];
                    const month = new Date(dateString).toLocaleString('default', { month: 'long' });
                    this.joinDate = `${month} ${year}`;
                    this.selectedDrinks = this.user.choiceDrinks;
                    this.userBookmarks = this.user.drinkLists;
                    this.following = JSON.stringify(this.user.followLists.users).includes(JSON.stringify({$oid: this.displayUserID}));

                } else {
                    const dateString = this.displayUser.joinDate.$date;
                    const dateParts = dateString.split('-');
                    const year = dateParts[0];
                    const month = new Date(dateString).toLocaleString('default', { month: 'long' });
                    this.joinDate = `${month} ${year}`;
                }

                this.userDrinkChoice = this.getDrinkOfChoice(this.user);
                this.displayUserDrinkChoice = this.getDrinkOfChoice(this.displayUser);
                this.displayUserBookmarks = this.displayUser.drinkLists;
                this.getUserFavourite();
                this.getRecentActivity();

                // ==== for badges ====
                this.getAllListingsReviewed();
                this.getAllCategoriesReviewed();
                await this.getAllCountriesTagged();

                // ==== for points ====
                this.pointSystem.logReview[0] = this.allListingsReviewedByUser.length;
                this.getTotalFriendsTagged();
                this.getTotalLocationsTagged();
                this.getTotalCountriesTagged();
                this.getAskedProducerQuestions();
                this.getAskedVenueQuestions();
                this.calculateTotalPoints();

                // ==== for badges (others) ====
                this.checkEnoughLocationTagged();
                this.checkEnoughCountriesTagged();
                this.checkEnoughFriendsTagged();
                this.getTotalUpvotes();
                this.checkEnoughUpvotes();

            } 
            catch (error) {
                console.error(error);
                this.dataLoaded = null;
            }
            // mod requests
            try {
                const response = await this.$axios.get('http://127.0.0.1:5000/getModRequests');
                this.modRequests = response.data;
                this.modRequestsType = this.modRequests
                    .filter(request => request.userID.$oid === this.userID && request.reviewStatus === true)
                    .map(request => request.drinkType);
            } 
            catch (error) {
                console.error(error);
                this.dataLoaded = null;
            }
            // drinkCategories
            try {
                const response = await this.$axios.get('http://127.0.0.1:5000/getDrinkTypes');
                this.drinkTypes = response.data;
                // retrieve the drink type and put them into an array
                this.drinkType = this.drinkTypes.map(category => category.drinkType);
                if (this.user && this.drinkTypes) {
                    this.filteredDrinkType =  this.drinkType.filter(type => !this.user.modType.includes(type));
                    if (this.modRequestsType.length > 0) {
                        this.filteredDrinkType = this.filteredDrinkType.filter(type => !this.modRequestsType.includes(type));
                    }
                }
                if(this.displayUser){
                    let currentMod = this.displayUser.modType
                    this.removableDrinkType = this.drinkTypes.filter(drinkType=>{
                        return currentMod.includes(drinkType.drinkType);
                    })
                    this.addableDrinkType = this.drinkTypes.filter(drinkType=>{
                        return !currentMod.includes(drinkType.drinkType);
                    })
                }

                // ==== for badges ====
                this.getTopCategoriesReviewed();
                this.getMatchedDrinkType();

            } 
            catch (error) {
                console.error(error);
                this.dataLoaded = null;
            }
            // flavourTags
            // _id, hexcode, familyTag, subtag, showbox
            try {
                const response = await this.$axios.get('http://127.0.0.1:5000/getFlavourTags');
                this.flavourTags = response.data.map(item => {
                    return { ...item, showBox: false };
                })
            } 
            catch (error) {
                console.error(error);
                this.dataLoaded = null;
            }
            // subTags
            // _id, familyTagId, subtag
            try {
                const response = await this.$axios.get('http://127.0.0.1:5000/getSubTags');
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
            } 
            catch (error) {
                console.error(error);
                this.dataLoaded = null;
            }

            // Set data loaded flag
            if (this.dataLoaded !== null) {
                this.dataLoaded = true;
            }
        },

        // ------------------- User Profile -------------------
        // get user from user ID
        getUser(id) {
            return this.users.find(user => user._id.$oid === id);
        },
        // get display user details
        getDrinkCount() {
            if (this.ownProfile) {
                return this.reviews.filter(review => review.userID.$oid === this.userID && review.reviewType === 'Listing').length;
            }
            else {
                return this.reviews.filter(review => review.userID.$oid === this.displayUserID && review.reviewType === 'Listing').length;
            }
        },
        getDrinkOfChoice() {
            if (this.ownProfile) {
                return this.user.choiceDrinks.join(", ");
            }
            else {
                return this.displayUser.choiceDrinks.join(", ");
            }
        },

        // ------------------- Edit User Profile -------------------
        // read uploaded image
        async loadFile(event) {
            const file = event.target.files[0];
            const reader = new FileReader();

            reader.onloadend = async () => {
                this.selectedImage = reader.result;
                const base64String = reader.result.replace('data:', '').replace(/^.+,/, '');

                this.image64 = base64String;

            };
            reader.readAsDataURL(file);
        
        },
        // save changes to user profile
        async saveChangesDetails() {
            if (this.image64 == null) {
                this.image64 = this.user["profile_picture"];
            }
            
            try {
                const response = await this.$axios.post('http://127.0.0.1:5100/editDetails', 
                    {
                        userID: this.userID,
                        image64: this.image64,
                        drinkChoice: this.selectedDrinks,
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
        // reset edit profile form
        cancelChanges() {
            this.selectedDrinks = this.user.choiceDrinks;
            this.selectedImage = null;
            this.$refs.fileInput.value = '';
        }, 

        // ------------------- User Bookmarks -------------------
        // checks if an item has been bookmarked
        checkBookmarkStatus(listingID) {
            // check if listingID is in user bookmark
            for (const category of Object.values(this.userBookmarks)) {
                if (category.listItems) {
                    if (category.listItems.some(item => item[1].$oid === listingID)) {
                        return true;
                    }
                }
            }
        },
        getListingFromID(listingID) {
            return this.listings.find(listing => listing._id.$oid === listingID);
        },

        // return oid from name of drink listing
        getListingID(listingName) {
            const listing = this.listings.find(listing => listing.listingName === listingName);
            return listing._id;
        },
        // return search items for bookmarking
        searchResult() {
            this.drinkSearchResults = this.listings
                .filter(listing => listing.listingName.toLowerCase().includes(this.drinkSearch.toLowerCase()))
                .filter(listing => !this.checkBookmarkStatus(listing._id.$oid))
                .map(listing => listing.listingName);
        },
        // bookmark item through search
        async addDrinkToList(listName) {
            for (const drink of this.drinksToAdd) {
                let addListingId = this.getListingID(drink);
                let itemExist = this.userBookmarks[listName].listItems.find(item => item[1].$oid === addListingId.$oid);
                if (!itemExist) {
                    this.userBookmarks[listName].listItems.push([new Date(), addListingId]);
                }
            }

            try {
                const response = await this.$axios.post('http://127.0.0.1:5100/updateBookmark', 
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
        // add new list
        async addNewList() {
            if (this.userBookmarks[this.newListName]) {
                this.newListNameError = "List name already exists";
                return;
            } else if (this.newListName === "") {
                this.newListNameError = "List name cannot be empty";
                return;
            }
            
            this.newListNameError = "";
            this.userBookmarks[this.newListName] = {};
            this.userBookmarks[this.newListName].listDesc = this.newListDesc;
            this.userBookmarks[this.newListName].listItems = [];

            try {
                const response = await this.$axios.post('http://127.0.0.1:5100/updateBookmark', 
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
        // delete drink from list
        async deleteFromList(listName, listingID) {
            // param: objectId
            const index = this.userBookmarks[listName].listItems.indexOf(listingID);
            this.userBookmarks[listName].listItems.splice(index, 1);

            try {
                const response = await this.$axios.post('http://127.0.0.1:5100/updateBookmark', 
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
        },
        // delete list
        async deleteList(listName) {
            // delete the list from the user's bookmark list
            delete this.userBookmarks[listName];

            try {
                const response = await this.$axios.post('http://127.0.0.1:5100/updateBookmark', 
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
        // reset form details
        resetEditList(listName, listDesc) {
            this.editListName = listName;
            this.editListDesc = listDesc;
            this.editListNameError = "";
        },
        // edit list details
        async editList(currentListName) {
            if (this.editListName === "") {
                this.editListNameError = "List name cannot be empty";
                return;
            } else if (this.editListName !== currentListName && this.userBookmarks[this.editListName]) {
                this.editListNameError = "List name already exists";
                return;
            }

            this.listNameError = "";

            if (this.editListName !== currentListName) {
                this.userBookmarks[this.editListName] = {};
                this.userBookmarks[this.editListName].listDesc = this.editListDesc;
                this.userBookmarks[this.editListName].listItems = this.userBookmarks[currentListName].listItems;
                delete this.userBookmarks[currentListName];
            } 
            
            this.userBookmarks[this.editListName].listDesc = this.editListDesc;

            try {
                const response = await this.$axios.post('http://127.0.0.1:5100/updateBookmark', 
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

        // ------------------- Moderator Application -------------------
        // submit moderator application
        async submitModeratorApplication() {
            try {
                const response = await this.$axios.post('http://127.0.0.1:5101/submitModRequest', 
                    {
                        userID: this.userID,
                        drinkType: this.modCat,
                        modDesc: this.modDesc,
                    }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                console.log(response.data);
            } catch (error) {
                console.error(error);
            }
            const index = this.filteredDrinkType.indexOf(this.modCat);
            if (index !== -1) {
                this.filteredDrinkType.splice(index, 1);
            }
            this.modCat = "";
            this.modDesc = "";
        },
        
        // ------------------- User Drink Activity -------------------
        // check if review is for listing
        async checkReviewType(listingID) {
            const review = this.reviews.find(review => review.listingID.$oid === listingID.$oid);
            return review.reviewType == "Listing"
        },
        // get listing name from listing ID
        getListingName(listingID) {
            if (this.listings) {
                return this.listings.find(listing => listing._id.$oid === listingID.$oid).listingName;
            }
        },
        // get user's favourite listings
        getUserFavourite() {
            const favouriteListingReviews = this.reviews
                .filter(review => review.reviewType === "Listing" && 
                    review.userID.$oid === this.displayUserID &&
                    review.rating >= 5)
                .sort((a, b) => b.rating - a.rating);

            const favouriteListingIds = favouriteListingReviews
                .map(review => review.reviewTarget['$oid'])

            this.favouriteListings = this.listings
                .filter(listing => favouriteListingIds.includes(listing._id.$oid))
                .sort((a, b) => {
                    // Get the indices of the IDs in favouriteIdList
                    const indexA = favouriteListingIds.indexOf(a._id.$oid);
                    const indexB = favouriteListingIds.indexOf(b._id.$oid);
                    
                    // Sort based on the indices in favouriteIdList
                    return indexA - indexB;
                })
                .slice(0, 5);
        },
        // get user's recent activity
        getRecentActivity() {

            // // reviews
            let userReviews = this.reviews
                .filter(review => review.reviewType === "Listing" && 
                    review.userID.$oid === this.displayUserID)
                .map(review => {
                    review.listingID = review.reviewTarget;
                    return review;
                });

            // bookmarks
            let allUserBookmarks = Object.values(this.userBookmarks).map(item => item.listItems).flat();
            let allUserBookmarksDict = allUserBookmarks.map(([createdDate, listingID]) => ({createdDate, listingID}));

            // combine reviews and bookmarks
            let userActivity = userReviews.concat(allUserBookmarksDict);

            this.recentActivity = userActivity
                .sort((a, b) => {
                    return new Date(b.createdDate) - new Date(a.createdDate);
                })
                .reverse()
                .filter((item, index, self) =>
                    index === self.findIndex((t) => (
                    t.listingID.$oid === item.listingID.$oid
                    ))
                )
                .map(item => {
                    item = this.listings.find(listing => listing._id.$oid === item.listingID.$oid);
                    return item;
                })
                .slice(0, 5);

        }, 
        getListingPhoto(listingID) {
            const listing = this.listings.find(listing => listing._id.$oid === listingID.$oid);
            return listing.photo;
        },
        getTagName(tag) {
            if (!this.subTags || !this.flavourTags) {
                return "";
            }
            const subTag = this.subTags.find(subTag=>subTag._id.$oid === tag.$oid)
            if(subTag){
                const familyTag = this.flavourTags.find(family=>subTag.familyTagId.$oid===family._id.$oid)
                if(familyTag){
                    const hexcode = familyTag.hexcode
                    const subtagInfo = subTag.subTag
                    const tagInfo = subtagInfo + hexcode
                    const tagParts = tagInfo.split("#");
                    return tagParts[0];
                }
                if (!familyTag || !subTag) {
                    return "";
                }
            }else{
                return "<deleted>"
            }

        },
        getTagColor(tag) {
            if (!this.subTags || !this.flavourTags) {
                return "";
            }
            const subTag = this.subTags.find(subTag=>subTag._id.$oid === tag.$oid)
            if(subTag){
                const familyTag = this.flavourTags.find(family=>subTag.familyTagId.$oid===family._id.$oid)
                if(familyTag){
                    const hexcode = familyTag.hexcode
                    const subtagInfo = subTag.subTag
                    const tagInfo = subtagInfo + hexcode
                    const tagParts = tagInfo.split("#");
                    return "#" + tagParts[1];
                }
                if (!familyTag || !subTag) {
                    return "";
                }
            }else{
                return "#" + "030303"
            }
            
        },

        // ------------------- User Follow -------------------
        // follow or unfollow user
        async editFollow(action) {
            if (action === "unfollow") {
                this.following = false;
            } else {
                this.following = true
            }
            try {
                const response = await this.$axios.post('http://127.0.0.1:5100/updateFollowLists', 
                    {
                        userID: this.userID,
                        action: action,
                        target: "users",
                        followerID: this.displayUserID,
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

        // others
        // get average review
        getAverageReview(listingID) {
            // param: objectId
            const reviews = this.reviews.filter(review => review.reviewTarget.$oid === listingID.$oid);
            if (reviews.length > 0) {
                const totalRating = reviews.reduce((acc, review) => acc + review.rating, 0);
                return (totalRating / reviews.length).toFixed(1);
            }
            return "-";
        },

        // ------------------- UI -------------------
        // review and drink list toggle
        viewList(name) {
            if (name == "lists") {
                this.activeTab = 'lists';
                this.$router.push('/profile/user/' + this.displayUserID);
            } else {
                this.activeTab = 'list';
                this.currentList = name;
                this.$router.push('/profile/user/' + this.displayUserID + '/' + name);
            }
        },
        switchTab(tab) {
            this.activeTab = tab;
            this.$router.push('/profile/user/' + this.displayUserID);
        },

        // drink list sharing
        updateCurrentURL() {
            this.currentURL = window.location.href;
        },

        copyToClipboard(text) {
            navigator.clipboard.writeText(text)
            .then(() => {
                this.clipboardItem = true;
                setTimeout(() => {
                    this.clipboardItem = false;
                }, 3000);
            })
            .catch(err => {
                console.error('Failed to copy text: ', err);
            });
        },
        
        // for bookmark component
        handleIconClick(data) {
            this.bookmarkListingID = data
        },
        updateDrinkType(){
            // get error message element
            let promotedTypeError = document.getElementById("promotedTypeError")
            // find listing based on bottle name
            let drinkType = this.addableDrinkType.find(drinkType => drinkType.drinkType === this.promotedType)
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
            let drinkType = this.removableDrinkType.find(drinkType => drinkType.drinkType === this.removedType)
            if (drinkType) {
                this.selectedRemoveType = drinkType
                removedTypeError.innerHTML = ""
            }
            else {
                this.selectedRemoveType = null
                removedTypeError.innerHTML = "Please enter a valid drink type"
            }
        },
        doubleConfirm(){
            if(this.chooseMod == 'add'){
                let errorMessage = ''
                if(this.selectedPromotedType == null){
                    errorMessage+="Please enter a valid drink type!\n"
                }
                if(errorMessage!=''){
                    alert(errorMessage)
                    return null
                }
                let alreadyModError = document.getElementById("alreadyModError")
                if(this.displayUser.modType.includes(this.selectedPromotedType.drinkType)){
                    alreadyModError.innerHTML = "This user is already a moderator for this drink type"
                    return null
                }else{
                    alreadyModError.innerHTML = ""
                }
            }
            if(this.chooseMod =='remove'){
                let errorMessage = ''
                if(this.selectedRemoveType == null){
                    errorMessage+="Please enter a valid drink type!\n"
                }
                if(errorMessage!=''){
                    alert(errorMessage)
                    return null
                }
                let notModError = document.getElementById("notModError")
                if(!this.displayUser.modType.includes(this.selectedRemoveType.drinkType)){
                    notModError.innerHTML = "This user is not a moderator for this drink type"
                    return null
                }else{
                    notModError.innerHTML = ""
                }
            }
            this.doubleConfirmMod = true
        },
        addModMode(){
            this.chooseMod = 'add'
            this.doubleConfirmMod = false
        },
        removeModMode(){
            this.chooseMod = 'remove'
            this.doubleConfirmMod = false
        },
        selectMode(){
            this.chooseMod = ''
            this.doubleConfirmMod = false
            this.resetErrors()
        },
        resetErrors(){
            this.successAddMod = false
            this.successRemoveMod =false
            this.errorAddMod = false
            this.errorRemoveMod = false
            this.selectedPromotedType = null
            this.selectedRemoveType = null
            this.promotedType = ''
            this.removedType = ''
        },
        async confirmModifyModerator(){
            try {
                let submitURL = ''
                let submitData = {}
                if(this.chooseMod=='remove'){
                    submitURL = 'http://127.0.0.1:5100/removeModType'
                    submitData={
                        userID: this.displayUser._id.$oid,
                        removeModType: this.selectedRemoveType.drinkType,
                    }
                }
                if(this.chooseMod=='add'){
                    submitURL = 'http://127.0.0.1:5100/updateModType'
                    submitData = {
                        userID: this.displayUser._id.$oid,
                        newModType: this.selectedPromotedType.drinkType,
                    }
                }
                await this.$axios.post(submitURL, submitData, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(response => {
                    // Handle the response here
                    if(response.data.code == 201){
                        if(this.chooseMod == 'remove'){
                            this.successRemoveMod = true
                            let modToDowngrade = this.displayUser.modType.findIndex(obj => obj === this.selectedRemoveType.drinkType);
                            if (modToDowngrade !== -1) {
                                this.displayUser.modType.splice(modToDowngrade, 1);
                            }
                            let currentMod = this.displayUser.modType
                            this.removableDrinkType = this.drinkTypes.filter(drinkType=>{
                                return currentMod.includes(drinkType.drinkType);
                            })
                            this.addableDrinkType = this.drinkTypes.filter(drinkType=>{
                                return !currentMod.includes(drinkType.drinkType);
                            })
                        }
                        if(this.chooseMod == 'add'){
                            this.successAddMod = true
                            this.confirmModerator = false
                            this.displayUser.modType.push(this.selectedPromotedType.drinkType)
                            let currentMod = this.displayUser.modType
                            this.removableDrinkType = this.drinkTypes.filter(drinkType=>{
                                return currentMod.includes(drinkType.drinkType);
                            })
                            this.addableDrinkType = this.drinkTypes.filter(drinkType=>{
                                return !currentMod.includes(drinkType.drinkType);
                            })
                                }
                            }
                });
            } catch (error) {
                console.error(error);
                if(this.chooseMod == 'add'){
                    this.errorAddMod = true
                }
                if(this.chooseMod == 'remove'){
                    this.errorRemoveMod = true
                }
            }
        },
        // To handle change and reset password
        changePasswordMode(mode){
            this.changingPassword = mode
        },
        selectPasswordMode(){
            if(this.confirmChangePassword||this.confirmResetPassword){
                this.passwordError = false
                this.passwordMismatch = false
                this.passwordSuccess = false
                this.confirmChangePassword = false
                this.confirmResetPassword = false
                this.verifyErrorMessage = ""
            }
            else{
                this.changingPassword = ""
            }
        },
        resetChangePassword(){
            if(this.passwordError||this.passwordSuccess||this.passwordMismatch){
                this.passwordError = false
                this.passwordMismatch = false
                this.passwordSuccess = false
                this.confirmChangePassword = false
                this.confirmResetPassword = false
                this.changingPassword = ""
                this.verifyErrorMessage = ""
            }
        },
        updatePassword(){
            if(this.oldPassword=="" || this.newPassword==""){
                alert("One of the passwords is empty, please check again")
                return null
            }
            this.confirmChangePassword = true
        },
        // Function to hash password
        // create unique hash based on username and password
        hashPassword(username, password) {
            const combinedString = username.toString() + password;
            let hash = 0;

            for (let i = 0; i < combinedString.length; i++) {
                const char = combinedString.charCodeAt(i);
                hash = (hash << 5) - hash + char;
                hash |= 0; // convert to 32-bit integer
            }

            return hash;
        },
        async confirmUpdatePassword(){
            let oldHash = this.hashPassword(this.user.username, this.oldPassword)
            let newHash = this.hashPassword(this.user.username, this.newPassword)
            let submitURL = 'http://127.0.0.1:5030/editPassword/' + this.user._id.$oid 
            let submitData = {
                oldHash: oldHash.toString(),
                newHash: newHash.toString(),
                userType: "user",
            }
            // Send request over
            let responseCode = ''
            await this.$axios.post(submitURL,submitData)
                .then((response)=>{
                    responseCode = response.data.code
                })
                .catch((error)=>{
                    console.error(error);
                    responseCode = error.response.data.code
                });
            if(responseCode==201){
                this.passwordSuccess=true; // Display success message
            }else if(responseCode==401){
                this.passwordMismatch = true // Display duplicate entry message
            }else{
                this.passwordError = true // Display generic error message
            }
        },

        async sendResetPin(){
            // call api to send pin
            this.isButtonDisabled = true;
                setTimeout(() => {
                    this.isButtonDisabled = false;
                }, 60000);
            let submitURL = 'http://127.0.0.1:5030/sendResetPin/' + this.user._id.$oid
            let submitData = {
                userType: "user",
            }
            let responseCode = ''
            await this.$axios.post(submitURL,submitData)
                .then((response)=>{
                    responseCode = response.data.code
                })
                .catch((error)=>{
                    console.error(error);
                    responseCode = error.response.data.code
                });
            let sendPinSuccess = document.getElementById("sendPinSuccess")
            let sendPinError = document.getElementById("sendPinError")
            if(responseCode == 201){
                sendPinSuccess.innerHTML = "OTP has been sent!"
                sendPinError.innerHTML = ""
            }
            else{
                sendPinSuccess.innerHTML = ""
                sendPinError.innerHTML = "Error sending OTP, please try again in 60 seconds"
            }
        },

        async verifyOTP(){
            // call api to verify the pin
            let submitURL = "http://127.0.0.1:5030/verifyPin/" + this.user._id.$oid
            let submitData ={
                userType:"user",
                pin:this.resetPin
            }
            let responseCode = ''
            await this.$axios.post(submitURL,submitData)
                .then((response)=>{
                    responseCode = response.data.code
                })
                .catch((error)=>{
                    console.error(error);
                    responseCode = error.response.data.code
                });
            if(responseCode == 201){
                this.confirmResetPassword = true
                this.verifyErrorMessage = ""
            }
            else if(responseCode == 400){
                this.verifyErrorMessage = "OTP is wrong or expired."
            }else{
                this.verifyErrorMessage = "An error verifying the OTP. Please resend OTP or try again."
            }
            
        },

        async resetPassword(){
            this.resettingPassword=true
            let submitURL = "http://127.0.0.1:5030/resetPassword/" + this.user._id.$oid
            let submitData = {
                userType:"user",
                pin:this.resetPin
            }
            // Send request over
            let responseCode = ''
            await this.$axios.post(submitURL,submitData)
                .then((response)=>{
                    responseCode = response.data.code
                })
                .catch((error)=>{
                    console.error(error);
                    responseCode = error.response.data.code
                });
            console.log(responseCode)
            this.resettingPassword= false
            if(responseCode==201){
                this.passwordSuccess=true; // Display success message
            }else{
                this.passwordError = true // Display generic error message
            }
        },

        // ------------------- Badges -------------------

        // get all listings reviewed by the user
        getAllListingsReviewed() {
            this.allListingsReviewedByUser = this.recentReviews.map(review => this.listings.find(listing => listing._id.$oid === review.reviewTarget.$oid));
        },

        // get all drinkType and typeCategory reviewed by the user
        getAllCategoriesReviewed() {
            for (let listing of this.allListingsReviewedByUser) {
                // check if this.allCategoriesReviewedByUser already contains the count for listing.drinkType
                // [if] no, assign the count as 1
                // [else] yes, add 1 to the count
                this.allCategoriesReviewedByUser[listing.drinkType] = (this.allCategoriesReviewedByUser[listing.drinkType] || 0) + 1;
                // check if this.allSubCategoriesReviewedByUser already contains the count for listing.typeCategory for that listing.drinkType
                // [if] no, assign the count as 1
                // [else] yes, add 1 to the count
                if (!this.allSubCategoriesReviewedByUser[listing.drinkType]) {
                    this.allSubCategoriesReviewedByUser[listing.drinkType] = {};
                }
                this.allSubCategoriesReviewedByUser[listing.drinkType][listing.typeCategory] = (this.allSubCategoriesReviewedByUser[listing.drinkType][listing.typeCategory] || 0) + 1;
            }
        },

        // extract out only the drink categories that the user has >= this.badgeLevels.novice (most basic level) reviews for
        // assign this.categoryBadges[category] to user based on # of reviews for that category
        // CHANGE! name of this.categoryBadges[category] if the criterion for minimum # of reviews to get a badge changes
        getTopCategoriesReviewed() {
            this.topCategoriesReviewed = Object.keys(this.allCategoriesReviewedByUser).reduce((acc, category) => {
                // check if user has reviewed enough subcategories for this category
                for (let subcategory in this.allSubCategoriesReviewedByUser[category]) {
                    let count = this.allSubCategoriesReviewedByUser[category][subcategory];
                    if (count >= this.otherBadgesLimit.reviewDrinkCategory) {
                        this.topSubcategoriesReviewed[category] = this.topSubcategoriesReviewed[category] || [];
                        this.topSubcategoriesReviewed[category].push(subcategory);
                    }
                }
                // --> HIGHEST TIER : MASTER (>= 30 reviews)
                if (this.allCategoriesReviewedByUser[category] >= this.badgeLevels.master) {
                    acc[category] = this.allCategoriesReviewedByUser[category];
                    this.categoryBadges[category] = "Master"
                }
                // --> MIDDLE TIER: LOVER (>= 10 reviews)
                else if (this.allCategoriesReviewedByUser[category] >= this.badgeLevels.lover) {
                    acc[category] = this.allCategoriesReviewedByUser[category];
                    this.categoryBadges[category] = "Lover"
                }
                // --> LOWEST TIER: NOVICE (>= 3 reviews)
                else if (this.allCategoriesReviewedByUser[category] >= this.badgeLevels.novice) {
                    acc[category] = this.allCategoriesReviewedByUser[category];
                    this.categoryBadges[category] = "Novice"
                }
                return acc;
            }, {});
        },

        // match categories to "drinkType" database
        // currently all "drinkTypes" in the reviews are hardcoded, so there is a need to map the objects so that all the badgePhoto can be retrieved
        getMatchedDrinkType() {
            this.matchedDrinkTypes = Object.keys(this.topCategoriesReviewed).map(category => this.drinkTypes.find(drinkType => drinkType.drinkType === category));
        },

        // get all countries user has tagged location in reviews
        async getAllCountriesTagged() {
            const apiKey = process.env.VUE_APP_API_KEY;
            const promises = this.recentReviews.map(async (review) => {
                const address = encodeURIComponent(review.address);
                if (address) {
                    const response = await this.$axios.get(`https://maps.googleapis.com/maps/api/geocode/json?address=${address}&key=${apiKey}`);
                    const { results } = response.data;
                    if (results[0]) {
                        const countryComponent = results[0].address_components.find(component => component.types.includes('country'));
                        if (countryComponent) {
                            const country = countryComponent.long_name;
                            if (!this.reviewCountriesTagged.includes(country)) {
                                this.reviewCountriesTagged.push(country);
                            }
                        }
                    }
                }
            });

            await Promise.all(promises);
        },

        // check if user has tagged locations in reviews
        checkEnoughLocationTagged() {
            if (this.pointSystem.tagLocation[0] >= this.otherBadgesLimit.tagLocation) {
                this.otherBadges.push("tagLocation")
            }
        },

        // check if user has tagged locations in reviews
        checkEnoughCountriesTagged() {
            if (this.pointSystem.tagCountry[0] >= this.otherBadgesLimit.tagCountry) {
                this.otherBadges.push("tagCountry")
            }
        },

        // check if user has tagged friends in reviews
        checkEnoughFriendsTagged() {
            if (this.pointSystem.tagFriend[0] >= this.otherBadgesLimit.tagFriend) {
                this.otherBadges.push("tagFriend")
            }
        },

        // get total number of upvotes received
        getTotalUpvotes() {
            let totalUpvotes = this.recentReviews.reduce((count, review) => {
                if (review.userVotes.upvotes.some(vote => vote.userID.$oid === this.displayUserID)) {
                    count += 1;
                }
                return count;
            }, 0);
            return totalUpvotes;
        },

        // check if user has upvotes from reviews
        checkEnoughUpvotes() {
            if (this.getTotalUpvotes() >= this.otherBadgesLimit.upvotes) {
                this.otherBadges.push("upvotes")
            }
        },

        getBadgeInfo(badgeName) {
            if (badgeName) {
                const badge = this.badges.find(badge => badge.badgeName === badgeName);
                return badge ? badge : null;
            }
        },

        // ------------------- Points -------------------

        // get total number of friends tagged
        getTotalFriendsTagged() {
            // loop through all reviews and get the number of friends tagged for each review
            // add up all the friends tagged
            this.pointSystem.tagFriend[0] = this.recentReviews.reduce((sum, review) => sum + review.taggedUsers.length, 0);
        },

        // get total number of locations tagged in reviews
        getTotalLocationsTagged() {
            // loop through all reviews and get the number of locations tagged for each review
            // add up all the locations tagged
            this.pointSystem.tagLocation[0] = this.recentReviews.reduce((sum, review) => sum + (review.location.length !== 0 ? 1 : 0), 0);
        },

        // get total number of countries user tagged in reviews
        getTotalCountriesTagged() {
            // loop through all reviews and get the number of countries tagged
            this.pointSystem.tagCountry[0] = this.reviewCountriesTagged.length;
        },

        // get total number of questions asked by user to producers
        getAskedProducerQuestions() {
            this.pointSystem.askProducer[0] = this.producers.reduce((totalQuestions, producer) => {
                return totalQuestions + producer.questionsAnswers.filter(qa => qa.userID.$oid === this.displayUserID).length;
            }, 0);
        },

        // get total number of questions asked by user to venues
        getAskedVenueQuestions() {
            this.pointSystem.askVenue[0] = this.venues.reduce((totalQuestions, venue) => {
                return totalQuestions + venue.questionsAnswers.filter(qa => qa.userID.$oid === this.displayUserID).length;
            }, 0);
        },

        // calculate total points
        calculateTotalPoints() {
            // in this.pointSystem, the key is the action, and the value is an array of [points, count]
            // to calculate total points, take value[0] = points | value[1] = count, and sum up all points * count
            this.totalPoints = Object.values(this.pointSystem).reduce((sum, value) => sum + (value[0] * value[1]), 0);
        },

    },
};
</script>

<style>

.profile-img {
    max-width: 110px;
    max-height: 110px;
}

.badge-img{
    width: 80px;
    height: 80px;
}

@media (max-width: 991px) {
.badge-img{
    width: 100%;
    height: auto;
}
}


/* .profile-img {
    width: 80px;
    height: 80px;
} */

.bottle-img {
    
    width:100%;
    height: auto;
    aspect-ratio: 1 / 1;
    object-fit: cover;
}

/* 
.bottle-img {
    width: 150px;
    height: 150px;
    flex-shrink: 0;
    border: 2px solid #535C72;
}
*/

.flex-start {
    display: flex;
    justify-content: flex-start;
    flex-direction: row;
}

.speech-bubble {
    z-index: 1;
    visibility: hidden;
    opacity: 0;
    position: absolute;
    left: calc(100% + 12px);
    top: 10px;
    width: 200px;
    background-color: white;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px; /* Adds rounded corners to the speech bubble */
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    transition: opacity 0.3s, visibility 0s linear 0.3s;
    /* Creates the tail of the speech bubble */
    &:after {
        content: "";
        position: absolute;
        top: 10px;
        left: -10px; /* Adjusts the position of the tail to be just outside the speech bubble */
        border-style: solid;
        border-width: 10px 10px 10px 0;
        border-color: transparent white transparent transparent;
    }
}

.hover-button:hover + .speech-bubble, .speech-bubble:hover {
    visibility: visible;
    opacity: 1;
    transition-delay: 0s;
}

</style>
