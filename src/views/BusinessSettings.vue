<!-- HTML -->
<template>
    <NavBar />

    <!-- Display when data is still loading -->
    <div class="text-info-emphasis fst-italic fw-bold fs-5 pt-5" v-if="dataLoaded == false">
        <span>Loading settings, please wait...</span>
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

    <!-- main content -->

    <div class="container pt-5 mobile-pt-3" v-if="dataLoaded" style="position: relative;">

        <!-- toast -->
        <transition name="fade">
            <div class="toast-container" style="position: absolute; top: 12px; right: 12px;" v-if="toastSuccess">
                <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" style="display: block;">
                    <div class="toast-header bg-success-subtle">
                        <img src="../../Images/Others/accept.png" height="20px" class="rounded me-2" alt="...">
                        <strong class="me-auto">Successful</strong>
                    </div>
                    <div class="toast-body text-start">
                        {{ toastMessage }}
                    </div>
                </div>
            </div>
        </transition>

        <div class="row">

            <!-- left pane -->
            <div class="col-lg-4 col-md-12 col-sm-12">

                <!-- row 1: producer info -->
                <div class="row">
                    <!-- producer name -->
                    <div class="col-8 text-start">
                        <h2> {{ businessName }} </h2>
                    </div>
                    <!-- producer profile photo -->
                    <div class="col-4">
                        <img :src="selectedImage || 'data:image/jpeg;base64,' + (photo || defaultProfilePhoto)" 
                            alt="" style="width: 100px; height: 100px; z-index: 1;">
                    </div>
                </div>

                <!-- row 2: return to profile -->
                <div class="row pt-3 mobile-view-hide">
                    <router-link :to="'/profile/producer/' + user_id" class="btn primary-btn-outline-thick rounded-0 default-clickable-text" > 
                        Return to profile 
                    </router-link>
                    <router-link :to="'/Producers/ProducersDashboard/' + user_id" class="btn primary-btn-outline-thick rounded-0 default-clickable-text mt-3" > 
                        Return to analytics 
                    </router-link>
                </div>

            </div>

            <!-- right pane -->
            <div class="col-lg-8 col-md-12 col-sm-12 ps-lg-5 text-start">
                <!-- user details -->
                <div>
                    <div class="alert alert-secondary fw-bold" role="alert">
                        User Details
                    </div>
                    <div class="row mx-2">
                        <div class="col-8">
                            <div class="row">
                                <div class="col-4 fw-bold mb-1">Shop Name: </div>
                                <div class="col-8"> {{request.businessName}} </div>
                            </div>
                            <div class="row">
                                <div class="col-4 fw-bold mb-1">User: </div>
                                <div class="col-8"> {{request.firstName}} {{request.lastName}} </div>
                            </div>
                            <div class="row">
                                <div class="col-4 fw-bold mb-1">Contact Number: </div>
                                <div class="col-8"> {{request.contact}} </div>
                            </div>
                            <div class="row">
                                <div class="col-4 fw-bold mb-3">Email: </div>
                                <div class="col-8"> {{request.email}} </div>
                            </div>
                        </div>
                        <div class="col-4 text-end">
                            <button type="button" class="btn primary-btn-outline-not-round" style="font-weight:bold; width: 200px;">Edit Details</button>
                        </div>
                    </div>
                </div>
                <!-- payment method -->
                <div>
                    <div class="alert alert-secondary fw-bold" role="alert">
                        Payment Method
                    </div>
                    <div class="row mx-2 mb-3">
                        <div v-if="subscription">
                            <!-- stripe -->
                            <img v-if="paymentMethod.brand == 'visa'" src="../../Images/Others/visa.png" alt="" style="height: 40px;" class="me-3">
                            <img v-else-if="paymentMethod.brand == 'mastercard'" src="../../Images/Others/mastercard.png" alt="" style="height: 40px;" class="me-3">
                            <img v-else src="../../Images/Others/credit-card.png" alt="" style="height: 30px;" class="me-3">
                            •••• •••• •••• {{paymentMethod.last4}}
                        </div>
                        <div v-else>
                            <div>No active subscription.</div>
                        </div>
                    </div>
                </div>
                <!-- billing and subscription -->
                <div>
                    <div class="alert alert-secondary fw-bold" role="alert">
                        Billing and Subscription
                    </div>
                    <div v-if="subscription" class="row mx-2">
                        <!-- stripe -->
                        <div class="col-6 fw-bold">Business Plan: 
                            <span v-if="subscriptionDetails.interval == 'month'">Monthly</span> 
                            <span v-if="subscriptionDetails.interval == 'year'">Yearly</span> 
                            Plan
                        </div>
                        <div v-if="activeSubscription" class="col-6 text-end">
                            <div class="fw-bold fs-3">${{subscriptionDetails.price}} p/{{subscriptionDetails.interval}}</div>
                            <div class="fst-italic">Next billing cycle: {{ formatDate(subscriptionDetails.next_billing_date) }}</div>
                            <div class="fst-italic">Amount due: ${{ (this.upcomingInvoice.amount_due / 100).toFixed(2) }}</div>
                            <button type="button" class="btn primary-btn-outline-not-round mt-2" style="font-weight:bold; width: 200px;" data-bs-toggle="modal" data-bs-target="#editSubscriptionModal">Edit Subscription</button>
                        </div>

                        <div v-else class="col-6 text-end">
                            <div class="fw-bold fs-3" style="color: red;">PAUSED</div>
                            <div v-if="activeSubscription == false" class="fst-italic" style="color: red;">Your subscription is available until {{ cancelledDate }}.</div>
                            <div class="fst-italic" style="color: red;">Resume subscription to access premium features.</div>
                            <button type="button" class="btn primary-btn-not-round mt-2" style="font-weight:bold; width: 200px; background-color: #71966B; border: 4px solid #71966B;" @click="resumeSubscription">Resume Subscription</button>
                        </div>
                    </div>
                    <div v-else class="row mx-2">
                        <div class="col-6">No active subscription.</div>
                        <div class="col-6 text-end">
                            <button type="button" class="btn primary-btn-not-round mt-2" style="font-weight:bold; width: 200px; background-color: #71966B; border: 4px solid #71966B;" @click='reSubscribe'>Subscribe</button>
                        </div>
                        
                    </div>
                </div>
            </div>

        </div> <!-- end of row -->

        
        <div> <!-- modals -->

            <!-- edit subscription modal -->
            <div class="modal fade" id="editSubscriptionModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="staticBackdropLabel">Edit Subscription</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-start">
                        <!-- choose plan -->
                        <div class="row justify-content-between">
                            <div class="col-6">
                                <button class="btn rounded p-3 text-start mb-3 w-100" @click="toggleMonthlyPricing" :style="{ backgroundColor: selectedMonthlyPricing ? '#DD9E54' :'white', 
                                                                                                                                    color: selectedMonthlyPricing ? 'white' :'black', 
                                                                                                                                    borderColor: '#DD9E54', 
                                                                                                                                    borderWidth:'3px' }">
                                    <span>
                                        <h6> <b> Monthly plan </b> </h6>
                                        <p class="m-0"> $65 / Month </p> 
                                        <small class="fst-italic p-0"> Billed monthly </small>
                                    </span>
                                </button>
                            </div>
                            <div class="col-6">
                                <button class="btn rounded p-3 text-start mb-3 w-100" @click="toggleYearlyPricing" :style="{ backgroundColor: selectedYearlyPricing ? '#DD9E54' :'white', 
                                                                                                                                    color: selectedYearlyPricing ? 'white' :'black', 
                                                                                                                                    borderColor: '#DD9E54', 
                                                                                                                                    borderWidth:'3px' }">
                                    <div class="row">
                                        <div class="col-7"> <h6> <b> Yearly plan </b> </h6> </div> 
                                        <div class="rounded col-5 text-center" style="background-color: green; color: white;">Save 23%</div>
                                    </div>
                                    <span>
                                        <p class="m-0"> $50 / Month </p> 
                                        <small class="fst-italic p-0"> $600 Billed annually </small>
                                    </span>
                                
                                </button>
                            </div>
                        </div>
                        <div v-if="selectedMonthlyPricing && subscriptionDetails.interval!='month'" class="alert alert-danger" role="alert">You are changing your subscription plan to <span class="fw-bold">monthly</span>. </div>
                        <div v-else-if="selectedYearlyPricing && subscriptionDetails.interval!='year'" class="alert alert-success" role="alert">You are changing your subscription plan to <span class="fw-bold">yearly</span>. </div>
                        <div v-else class="alert alert-light" role="alert">No changes selected.</div>
                        <hr>
                        <div>If you wish to pause your subscription, please click <span data-bs-toggle="modal" data-bs-target="#cancelSubscriptionModal" style="text-decoration: underline; cursor: pointer;">here</span>.</div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button v-if="selectedMonthlyPricing && subscriptionDetails.interval!='month'" type="button" class="btn btn-primary" @click="editSubscription('month')" data-bs-dismiss="modal">Confirm</button>
                        <button v-else-if="selectedYearlyPricing && subscriptionDetails.interval!='year'" type="button" class="btn btn-primary" @click="editSubscription('year')" data-bs-dismiss="modal">Confirm</button>
                        <button v-else type="button" class="btn btn-primary" disabled>Confirm</button>
                    </div>
                    </div>
                </div>
            </div>

            <!-- cancel subscription modal -->
            <div class="modal fade" id="cancelSubscriptionModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="text-end mt-2 me-2">
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>

                        <div class="text-center">
                            <img src="../../Images/Others/cancel.png" alt="" class="rounded-circle border border-dark text-center" style="width: 100px; height: 100px;">
                            <h4 class="mt-3 mb-4">Pause Subscription</h4>
                            <p>We're sad to see you go!</p>
                            <p>Are you sure you want to pause your subscription? </p>
                        </div>
                        <div style="display: inline" class="text-center mt-4 mb-4">
                            <button type="button" class="btn btn-secondary me-3" data-bs-toggle="modal" data-bs-target="#editSubscriptionModal">Keep Subscription</button>
                            <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="cancelSubscription">Pause Subscription</button>
                        </div>
                    </div>
                </div>
            </div>

        </div> <!-- end of modals -->
        
        

    </div> <!-- end of main content -->

</template>

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>

    import NavBar from '@/components/NavBar.vue';
    import { loadStripe } from '@stripe/stripe-js';

    export default {
        components: {
            NavBar
        },
        
        data() {
            return {
                dataLoaded: false,
                toastSuccess: false,
                toastMessage: null,

                user_id: null,
                user_type: null,

                monthlyPriceId: "price_1PV7PCDnjokAiSGzX84MZogY",
                yearlyPriceId: "price_1PV7PsDnjokAiSGz02ZZTJdu",

                business: null,
                businessName: null,
                photo: null,
                requestId: null,
                stripeCustomerId: null,
                subscription: null,
                activeSubscription: null,
                cancelledDate: null,
                // upcomingInvoice: null,
                paymentMethod: null,
                subscriptionDetails: null, 

                selectedMonthlyPricing: null, 
                selectedYearlyPricing: null,

                request: null,
                


                defaultProfilePhoto: "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",
                
            };
        },
        async mounted() {
            var userID = localStorage.getItem('88B_accID')
            if(userID != null){
                this.user_id = userID;
            }

            var userType = localStorage.getItem('88B_accType');
            if(userType != null){
                this.userType = userType;
            }

            this.stripe = await loadStripe(process.env.VUE_APP_STRIPE_PUBLISHABLE_KEY);


            await this.loadData();

        },
        methods: {
            // load data from database
            async loadData() {
                if (this.userType != "producer" && this.userType != "venue") {
                    // redirect to page
                    this.$router.push('/');
                }
                // business
                try {
                    const response = await this.$axios.get(`http://127.0.0.1:5000/getData/get${this.userType.charAt(0).toUpperCase()}${this.userType.slice(1)}/${this.user_id}`);
                    this.business = response.data;
                    this.businessName = this.business[this.userType + "Name"];
                    this.photo = this.business.photo;
                    this.requestId = this.business.requestId
                    this.stripeCustomerId = this.business.stripeCustomerId;
                } 
                catch (error) {
                    console.error(error);
                    this.dataLoaded = null;
                }
                // request
                try {
                    const response = await this.$axios.get(`http://127.0.0.1:5000/getData/getAccountRequest/${this.requestId.$oid}`);
                    this.request = response.data;
                } 
                catch (error) {
                    console.error(error);
                    this.dataLoaded = null;
                }

                // subscription
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5000/payment/retrieve-latest-subscription', {
                        customerId: this.stripeCustomerId,
                    }, {
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    });
                    this.subscription = response.data;
                    console.log(this.subscription);

                    if (!this.subscription) {
                        return;
                    }

                    if (this.subscription.status == "active") {
                        if (this.subscription.cancel_at == null) {
                            // there is no end date
                            this.activeSubscription = true;
                        } else {
                            // there is an end date
                            this.activeSubscription = false;
                            this.cancelledDate = this.formatDate(this.subscription.cancel_at*1000);
                        } 
                    } else {
                        // subscription has fully ended
                        this.activeSubscription = null;
                    }

                } catch (error) {
                    if (error.response && error.response.status === 404) {
                        console.error('Error retrieving subscription:', error);
                    } else {
                        console.error('Error retrieving subscription:', error);
                        this.dataLoaded = null;
                    }
                }
                
                if (this.activeSubscription) {
                    // upcoming invoice
                    try {
                        const response = await this.$axios.post('http://127.0.0.1:5000/payment/retrieve-upcoming-invoice', {
                            subscription_id: this.subscription.id,
                        }, {
                            headers: {
                                'Content-Type': 'application/json',
                            }
                        });
                        this.upcomingInvoice = response.data;
                        console.log(this.upcomingInvoice);
                    } catch (error) {
                        console.error('Error retrieving upcoming invoice:', error);
                        this.dataLoaded = null;
                    }

                    // payment method
                    try {
                        const response = await this.$axios.post('http://127.0.0.1:5000/payment/retrieve-payment-method', {
                            subscription: this.subscription,
                        }, {
                            headers: {
                                'Content-Type': 'application/json',
                            }
                        });
                        this.paymentMethod = response.data;
                    } catch (error) {
                        console.error('Error retrieving customer payment methods:', error);
                        this.dataLoaded = null;
                    }

                    // subscription details
                    try {
                        const response = await this.$axios.post('http://127.0.0.1:5000/payment/retrieve-subscription-details', {
                            subscription: this.subscription,
                        }, {
                            headers: {
                                'Content-Type': 'application/json',
                            }
                        });
                        this.subscriptionDetails = response.data;
                        this.selectedMonthlyPricing = this.subscriptionDetails.interval === 'month';
                        this.selectedYearlyPricing = this.subscriptionDetails.interval === 'year';
                    } catch (error) {
                        console.error('Error retrieving customer payment methods:', error);
                        this.dataLoaded = null;
                    }
                
                }

                // Set data loaded to true
                if (this.dataLoaded != null) {
                    this.dataLoaded = true;
                }
            },

            async getPaymentMethodIdFromCustomerId(customerId) {
                try {
                    const response = await this.$axios.get(`http://127.0.0.1:5000/getData/get-payment-method-id/${customerId}`);
                    if (response.data && response.data.paymentMethodId) {
                        return response.data.paymentMethodId;
                    } else {
                        console.error('No payment method ID found for the given customer ID');
                        return null;
                    }
                } catch (error) {
                    console.error(error);
                    return null;
                }
            },

            formatDate(dateString) {
                const date = new Date(dateString);
                return date.toLocaleDateString('en-GB', {
                    day: 'numeric', month: 'long', year: 'numeric'
                });
            },

            toggleYearlyPricing(){
                if(this.selectedMonthlyPricing && !this.selectedYearlyPricing){
                    this.selectedMonthlyPricing= false
                }
                if(this.selectedYearlyPricing){
                    this.selectedYearlyPricing=false
                }else{
                    this.selectedYearlyPricing = true
                }
            },
            toggleMonthlyPricing(){
                if(this.selectedYearlyPricing && ! this.selectedMonthlyPricing){
                    this.selectedYearlyPricing= false
                }
                if(this.selectedMonthlyPricing){
                    this.selectedMonthlyPricing=false
                }else{
                    this.selectedMonthlyPricing = true
                }
            },

            async editSubscription(interval) {
                try {
                    await this.$axios.post('http://127.0.0.1:5000/payment/change-subscription-plan', {
                        subscription: this.subscription,
                        subscription_id: this.subscription.id,
                        new_price_id: interval === 'month' ? this.monthlyPriceId : this.yearlyPriceId,
                    }, {
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    });
                    this.loadData();
                    this.toastSuccess = true;
                    this.toastMessage = 'Your subscription has been updated!';
                    setTimeout(() => {
                        this.toastSuccess = false;
                    }, 5000);
                } catch (error) {
                    console.error('Error editing subscription:', error);
                }

            },

            async cancelSubscription() {
                try {
                    await this.$axios.post('http://127.0.0.1:5000/payment/cancel-subscription', {
                        subscription: this.subscription,
                        subscription_id: this.subscription.id,
                    }, {
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    });
                    this.loadData();
                    this.toastSuccess = true;
                    this.toastMessage = 'Your subscription has been cancelled.';
                    setTimeout(() => {
                        this.toastSuccess = false;
                    }, 5000);
                } catch (error) {
                    console.error('Error editing subscription:', error);
                }

            },

            async resumeSubscription() {
                try {
                    await this.$axios.post('http://127.0.0.1:5000/payment/resume-subscription', {
                        subscription: this.subscription,
                        subscription_id: this.subscription.id,
                    }, {
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    });
                    this.loadData();
                    this.toastSuccess = true;
                    this.toastMessage = 'Your subscription has been resumed.';
                    setTimeout(() => {
                        this.toastSuccess = false;
                    }, 5000);
                } catch (error) {
                    console.error('Error resuming subscription:', error);
                }
            }, 

            async generateToken(businessId, requestId) {
                console.log(businessId, requestId);
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5000/createAccount/createToken', 
                        {
                            businessId: businessId,
                            requestId: requestId,
                            isNew: false,
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

            async reSubscribe() {
                const link = await this.generateToken(this.user_id, this.requestId.$oid);
                window.location.href = link;
            }

        }
    };
</script>