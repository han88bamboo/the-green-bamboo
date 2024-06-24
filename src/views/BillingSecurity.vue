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

    <!-- Display when form is being submitted -->
    <div class="text-info-emphasis fst-italic fw-bold fs-5" v-if="submitForm"> 
        <span>The form is being submitted, please hold on!</span>
        <br><br>
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>

    <div class="" v-if="dataLoaded">

        <div class="container text-start" style="width: 50%">
            <p style="font-family: radley; font-size: 50px;" class="pt-5 pb-0">You’re almost all set up!</p>
            <p style="font-family: radley; font-size: 30px;">Enter your payment details and set up your login details.</p>

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
            
            <div v-if="selectedMonthlyPricing || selectedYearlyPricing">
                <form id="payment-form">
                    <div id="payment-element">
                        <!-- Elements will create form elements here -->
                    </div>
                </form>
            </div>
            <div v-else>
                <span class="text-danger">Please select a plan</span>
            </div>

            <div class="row">
                <div class="col-lg-8 col-md-12">
                    <button type="submit" class="btn btn-lg secondary-btn-border-thick mx-auto my-3" @click="createAccount">Create Account</button>
                </div>
            </div>

            <div id="error-message">
                <!-- Display error message to your customers here -->
            </div>

        </div>



        
    </div>

</template>

<!-- ------------------------------------------------------------------------------ -->

<script>
    // import components used
    import NavBar from '@/components/NavBar.vue';
    import { loadStripe } from '@stripe/stripe-js';

    export default{
        name: 'BillingSecurity',
        components: {
            NavBar
        },
        data(){
            return{
                dataLoaded: false,
                monthlyPriceId: "price_1PV7PCDnjokAiSGzX84MZogY",
                yearlyPriceId: "price_1PV7PsDnjokAiSGz02ZZTJdu",

                // owner details
                stripe: loadStripe('pk_test_51PV6CNDnjokAiSGzhdAambzILFYOByYtxMRMsVQCcQobPIxlFDi2a6gKYe8BQD021FQxFUejn4eIcjSLBHsHbD9A00T4Z8sPPl'),
                elements: null,

                // customer details
                customerName: "John Doe",
                customerEmail: "poh.liyingg@gmail.com",

                // plan details
                selectedMonthlyPricing: true,
                selectedYearlyPricing: false,

                // stripe details
                priceId: "",
                customerId: "",
                clientSecret: "",
            }
        },
        async mounted(){

            async function initiateProcess() {
                await this.create_customer();
                await this.create_subscription();
                this.paymentElement();
            }

            initiateProcess.call(this);

            this.loadData();

        },
        methods: {
            async toggleYearlyPricing(){
                if(this.selectedMonthlyPricing && !this.selectedYearlyPricing){
                    this.selectedMonthlyPricing= false
                }
                if(this.selectedYearlyPricing){
                    this.selectedYearlyPricing=false
                }else{
                    this.selectedYearlyPricing = true
                    await this.create_subscription()
                    this.paymentElement()
                }
            },
            async toggleMonthlyPricing(){
                if(this.selectedYearlyPricing && ! this.selectedMonthlyPricing){
                    this.selectedYearlyPricing= false
                }
                if(this.selectedMonthlyPricing){
                    this.selectedMonthlyPricing=false
                }else{
                    this.selectedMonthlyPricing = true
                    await this.create_subscription()
                    this.paymentElement()
                }
            },
            async loadData(){
                try {
                    this.dataLoaded = true;
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
            },


            async create_customer() {
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5009/create-customer',
                        {
                            customerEmail: this.customerEmail,
                            customerName: this.customerName,
                            address: {
                                city: "Brothers",
                                country: "US",
                                line1: "27 Fredrick Ave",
                                postal_code: "97712",
                                state: "CA",
                            }
                        }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    console.log(response.data);
                    this.customerId = response.data.customerId;
                } catch (error) {
                    console.error(error);
                }
            },

            async create_subscription() {
                if (this.selectedMonthlyPricing) {
                    this.priceId = this.monthlyPriceId;
                } else {
                    this.priceId = this.yearlyPriceId;
                }
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5009/create-subscription',
                        {
                            priceId: this.priceId,
                            customerId: this.customerId,
                        }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    console.log(response.data);
                    this.clientSecret = response.data.clientSecret;
                } catch (error) {
                    console.error(error);
                }
            },

            async paymentElement() {

                const stripe = await loadStripe('pk_test_51PV6CNDnjokAiSGzhdAambzILFYOByYtxMRMsVQCcQobPIxlFDi2a6gKYe8BQD021FQxFUejn4eIcjSLBHsHbD9A00T4Z8sPPl');
                const clientSecret = this.clientSecret;
                const appearance = {
                    theme: 'stripe',
                };

                this.elements = stripe.elements({clientSecret, appearance});
                const elements = this.elements;

                const paymentElement = elements.create('payment');
                paymentElement.mount('#payment-element');

            },

            async createAccount(){

                // const stripe = this.stripe;
                // const elements = this.elements;

                // const {error} = await stripe.confirmPayment({
                //     elements,
                //     confirmParams: {
                //         // TO CHANGE
                //         return_url: "https://localhost:8080/",
                //     }
                // });

                // if (error) {
                //     // immediate error (for example, payment details incomplete)
                //     const messageContainer = document.querySelector('#error-message');
                //     messageContainer.textContent = error.message;
                // } else {
                //     // success, redirection to return_url
                //     // TODO: redirect to return_url
                // }

                // // Retrieve the "payment_intent_client_secret" query parameter appended to
                // // your return_url by Stripe.js
                // const clientSecret = new URLSearchParams(window.location.search).get(
                //     'payment_intent_client_secret'
                // );

                // // Retrieve the PaymentIntent
                // stripe.retrievePaymentIntent(clientSecret).then(({paymentIntent}) => {
                //     const message = document.querySelector('#message')

                //     // Inspect the PaymentIntent `status` to indicate the status of the payment
                //     // to your customer.
                //     //
                //     // Some payment methods will [immediately succeed or fail][0] upon
                //     // confirmation, while others will first enter a `processing` state.
                //     //
                //     // [0]: https://stripe.com/docs/payments/payment-methods#payment-notification
                //     switch (paymentIntent.status) {
                //         case 'succeeded':
                //         message.innerText = 'Success! Payment received.';
                //         break;

                //         case 'processing':
                //         message.innerText = "Payment processing. We'll update you when payment is received.";
                //         break;

                //         case 'requires_payment_method':
                //         message.innerText = 'Payment failed. Please try another payment method.';
                //         // Redirect your user back to your payment page to attempt collecting
                //         // payment again
                //         break;

                //         default:
                //         message.innerText = 'Something went wrong.';
                //         break;
                //     }
                // });
            },
        }
    }

</script>