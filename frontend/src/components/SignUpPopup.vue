<template>
    <!-- Backdrop overlay -->
    <div v-if="show" class="signup-popup-backdrop" @click="closePopup">
        <!-- Modal content -->
        <div class="signup-popup-modal" @click.stop>
            <!-- Close button -->
            <button class="close-btn" @click="closePopup">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="white" viewBox="0 0 16 16">
                    <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
                </svg>
            </button>

            <!-- Banner Image -->
            <div class="banner-container">
                <img :src="bannerImage" alt="Drink-X Banner" class="banner-image" />
            </div>

            <!-- Content -->
            <div class="popup-content">
                <!-- Header -->
                <!--<h2 class="popup-title">Track All Your Favourite Drinks on Drink-X. Completely Free!</h2>-->
                <h2 class="popup-title mb-2" style="color:#f0b358">
                    {{ welcomeMessage }}
                </h2>
                <h3 class="fw-bold mb-2" style="color:black;">
                    Sign up for Drink-X to start collecting every drink you taste!
                </h3>
                <!-- Tagline -->
                <!-- <p class="popup-tagline">
                    See what others say about the event's drinks, rate drinks you've tasted & track them on your personal cellar system!
                </p> -->

                <!-- Email Input -->
                <div class="email-section">
                    <input 
                        type="email" 
                        v-model="emailInput"
                        placeholder="Enter email address to sign up"
                        class="email-input"
                        @keyup.enter="submitEmail"
                    />
                    
                    <!-- Sign Up Button -->
                    <button 
                        class="signup-btn"
                        @click="submitEmail"
                        :disabled="!emailInput || !isValidEmail"
                    >
                        {{ (!emailInput || !isValidEmail) ? 'Enter Your Email Above' : 'Sign Up for Drink-X!' }}
                    </button>
                </div>

                <!-- Terms text -->
                <p class="terms-text">
                    By signing up, you verify you are of legal drinking age.
                </p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'SignUpPopup',
    props: {
        show: {
            type: Boolean,
            default: false
        },
        email: {
            type: String,
            default: ''
        },
        venueId: {
            type: Number,
            default: null
        }
    },
    emits: ['close', 'submit', 'update:email'],
    data() {
        return {
            emailInput: this.email || ''
        }
    },
    computed: {
        isValidEmail() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(this.emailInput);
        },
        welcomeMessage() {
            if (this.venueId === 109) {
                return 'Welcome to Sake Matsuri 2025 🍶!';
            }
            if (this.venueId === 99) {
                return 'Welcome to Whisky Live Singapore 2025!';
            }
            if (this.venueId === 108) {
                return 'Welcome to Champagniac! 🍾🥂';
            }
            // Default message for other venues
            return 'Welcome!';
        },
        bannerImage() {
            if (this.venueId === 109) {
                return 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Sake_Matsuri_banner.png?v=1761298884';
            }
            if (this.venueId === 99) {
                return 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/imgi_8_Whiskylive-9-november-2019-184-of-361-scaled.jpg?v=1761299521';
            }
            if (this.venueId === 108) {
                return 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/imgi_6_champagniac-brimoncourt-2025.webp?v=1762502333';
            }
            // Default banner for other venues
            return '/img/defaultGroupBanner.61a71c68.png';
        }
    },
    watch: {
        email(newVal) {
            this.emailInput = newVal;
        },
        emailInput(newVal) {
            this.$emit('update:email', newVal);
        }
    },
    methods: {
        closePopup() {
            this.$emit('close');
        },
        submitEmail() {
            if (this.emailInput && this.isValidEmail) {
                this.$emit('submit', this.emailInput);
            }
        }
    }
}
</script>

<style scoped>
/* Backdrop */
.signup-popup-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    padding: 20px;
}

/* Modal */
.signup-popup-modal {
    background: white;
    border-radius: 12px;
    max-width: 500px;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    position: relative;
    animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
    from {
        opacity: 0;
        transform: translateY(-50px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* Close button */
.close-btn {
    position: absolute;
    top: 15px;
    right: 15px;
    background: rgba(0, 0, 0, 0.1);
    border: none;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 1;
    transition: background-color 0.2s ease;
}

.close-btn:hover {
    background: rgba(0, 0, 0, 0.2);
}

/* Banner */
.banner-container {
    width: 100%;
    height: 200px;
    overflow: hidden;
    border-radius: 12px 12px 0 0;
}

.banner-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* Content */
.popup-content {
    padding: 30px;
    text-align: center;
}

.popup-title {
    font-size: 24px;
    font-weight: bold;
    color: #e67e22;
    margin: 0 0 5px 0;
    line-height: 1.2;
}



.popup-tagline {
    font-size: 16px;
    color: #5a6c7d;
    margin: 0 0 30px 0;
    line-height: 1.4;
}

/* Email section */
.email-section {
    margin-bottom: 20px;
}

.email-input {
    width: 100%;
    padding: 15px;
    border: 2px solid #e1e8ed;
    border-radius: 8px;
    font-size: 16px;
    margin-bottom: 15px;
    transition: border-color 0.2s ease;
    box-sizing: border-box;
}

.email-input:focus {
    outline: none;
    border-color: #e67e22;
}

.email-input::placeholder {
    color: #95a5a6;
}

/* Sign up button */
.signup-btn {
    width: 100%;
    padding: 15px;
    background: linear-gradient(135deg, #e67e22, #f39c12);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(230, 126, 34, 0.3);
}

.signup-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #d35400, #e67e22);
    box-shadow: 0 6px 20px rgba(230, 126, 34, 0.4);
    transform: translateY(-2px);
}

.signup-btn:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
}

/* Terms text */
.terms-text {
    font-size: 12px;
    color: #95a5a6;
    margin: 0;
    line-height: 1.4;
}

/* Mobile responsiveness */
@media (max-width: 576px) {
    .signup-popup-modal {
        margin: 10px;
        max-width: calc(100% - 20px);
    }
    
    .popup-content {
        padding: 20px;
    }
    
    .popup-title {
        font-size: 20px;
    }
    
    .popup-subtitle {
        font-size: 16px;
    }
    
    .popup-tagline {
        font-size: 14px;
    }
    
    .banner-container {
        height: 150px;
    }
}

@media (max-width: 400px) {
    .popup-title {
        font-size: 18px;
    }
    
    .email-input,
    .signup-btn {
        padding: 12px;
        font-size: 16px;
    }
}
</style>
