<!-- 
    Password Strength Checker Component
    This component checks the strength of a password input and provides visual feedback.
    It includes requirements for length, uppercase, lowercase, numbers, and special characters.

    -Be at least 8 characters long
    -Contain at least one uppercase letter
    -Contain at least one lowercase letter
    -Contain at least one number
    -Contain at least one special character/symbol

    another option is to use a algorithmic checker like zxcvbn for more advanced password strength checking.
-->
<template>
  <div>
    <div class="form-floating password-input-container">
      <!-- COMMENTED OUT - old simple password input without visibility toggle
      <input
        id="password"
        v-model="password"
        type="password"
        placeholder="Enter your password"
        class="form-control form-box-outline"
        @input="handleInput"
      />
      -->
      
      <!-- NEW IMPLEMENTATION - password input with hold-to-show eye icon -->
      <input
        id="password"
        v-model="password"
        :type="showPassword ? 'text' : 'password'"
        placeholder="Enter your password"
        class="form-control form-box-outline password-input-with-icon"
        @input="handleInput"
      />
      
      <!-- Eye icon button for hold-to-show functionality -->
      <button
        type="button"
        class="password-toggle-btn"
        @mousedown="showPasswordOnHold"
        @mouseup="hidePasswordOnRelease"
        @mouseleave="hidePasswordOnRelease"
        @touchstart="showPasswordOnHold"
        @touchend="hidePasswordOnRelease"
        tabindex="-1"
      >
        {{ showPassword ? '🙈' : '👁️' }}
      </button>
      
      <label for="password"> Password </label>
    </div>
    
    <div class="strength-indicator">
      <div class="strength-bar">
        <div 
          class="strength-fill"
          :style="{ 
            width: `${(strengthLevel / 5) * 100}%`,
            backgroundColor: getStrengthColor()
          }"
        ></div>
      </div>
    </div>
    
    <div class="requirements-list" v-if="password.length > 0">
      <div class="requirement-item" :class="{ 'met': requirements.length }">
        <span class="check-icon">{{ requirements.length ? '✓' : '✗' }}</span>
        Contains at least 8 characters <strong>&nbsp;(Required)</strong>
      </div>
      <div class="requirement-note">
        <em>Plus at least ONE of the following:</em>
      </div>
      <div class="requirement-item" :class="{ 'met': requirements.uppercase && requirements.lowercase }">
        <span class="check-icon">{{ (requirements.uppercase && requirements.lowercase) ? '✓' : '✗' }}</span>
        Contains both uppercase and lowercase letters
      </div>
      <div class="requirement-item" :class="{ 'met': requirements.number && /[a-zA-Z]/.test(password) }">
        <span class="check-icon">{{ (requirements.number && /[a-zA-Z]/.test(password)) ? '✓' : '✗' }}</span>
        Contains at least one number (in addition to letters)
      </div>
      <div class="requirement-item" :class="{ 'met': requirements.special && /[a-zA-Z]/.test(password) }">
        <span class="check-icon">{{ (requirements.special && /[a-zA-Z]/.test(password)) ? '✓' : '✗' }}</span>
        Contains at least one special character (in addition to letters)
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PasswordStrengthChecker',
  emits: ['password-change', 'strength-change', 'password-data'],
  data() {
    return {
      password: '',
      showPassword: false, // REACTIVATED - now used for hold-to-show functionality
      strengthLevel: 0,
      requirements: {
        length: false,
        uppercase: false,
        lowercase: false,
        number: false,
        special: false
      }
    }
  },
  methods: {
    handleInput() {
      this.checkStrength()
      // Emit individual events
      this.$emit('password-change', this.password)
      this.$emit('strength-change', this.strengthLevel)
      
      // Or emit combined data
      this.$emit('password-data', {
        password: this.password,
        strengthLevel: this.strengthLevel,
        requirements: this.requirements,
        strengthText: this.getStrengthText()
      })
    },
    
    checkStrength() {
      // Reset requirements
      this.requirements = {
        length: this.password.length >= 8,
        uppercase: /[A-Z]/.test(this.password),
        lowercase: /[a-z]/.test(this.password),
        number: /\d/.test(this.password),
        special: /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?~`]/.test(this.password)
      }
      
      // MODIFIED LOGIC - Calculate strength level with new requirements:
      // Must have length + at least one other requirement
      // Note: uppercase and lowercase are now combined into one requirement
      // Note: number requirement now also requires at least one letter (to prevent pure numeric passwords)
      // Note: special requirement now also requires at least one letter (to prevent pure symbolic passwords)
      const hasLength = this.requirements.length;
      const hasBothUpperAndLowercase = this.requirements.uppercase && this.requirements.lowercase;
      const hasNumberAndLetter = this.requirements.number && (/[a-zA-Z]/.test(this.password)); // Number + any letter
      const hasSpecialAndLetter = this.requirements.special && (/[a-zA-Z]/.test(this.password)); // Special + any letter
      
      const otherRequirementsMet = [
        hasBothUpperAndLowercase,
        hasNumberAndLetter,
        hasSpecialAndLetter
      ].filter(Boolean).length;
      
      // If length requirement is met AND at least one other requirement is met, 
      // set strength to 5 (strong), otherwise calculate normally
      if (hasLength && otherRequirementsMet >= 1) {
        this.strengthLevel = 5; // Strong password
      } else {
        // Original calculation for visual feedback when requirements not met
        this.strengthLevel = Object.values(this.requirements).filter(Boolean).length;
      }
    },
    
    // NEW IMPLEMENTATION - hold-to-show password functionality
    showPasswordOnHold() {
      this.showPassword = true
    },
    
    hidePasswordOnRelease() {
      this.showPassword = false
    },
    
    // COMMENTED OUT - old toggle functionality replaced with hold-to-show
    /*
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword
    },
    */
    
    getStrengthColor() {
      const colors = [
        '#ff4444', // 0 - Very Weak
        '#ff6644', // 1 - Weak  
        '#ffaa00', // 2 - Fair
        '#ffdd00', // 3 - Good
        '#768f12', // 4 - Strong
        '#006500'  // 5 - All requirements met (same as 4)
      ]
      return colors[this.strengthLevel] || colors[0]
    },
    
    getStrengthText() {
      const texts = [
        'Very Weak',
        'Weak', 
        'Fair',
        'Good',
        'Strong'
      ]
      return texts[this.strengthLevel] || 'Very Weak'
    }
  }
}
</script>

<style scoped>
/* Password input container with eye icon */
.password-input-container {
  position: relative;
}

.password-input-with-icon {
  padding-right: 45px !important; /* Make room for eye icon */
}

.password-toggle-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  padding: 4px;
  line-height: 1;
  color: #666;
  user-select: none;
  z-index: 3;
  transition: color 0.2s ease;
}

.password-toggle-btn:hover {
  color: #333;
}

.password-toggle-btn:active {
  color: #000;
}

.password-toggle-btn:focus {
  outline: none;
}

.password-strength-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.input-container {
  position: relative;
  margin-bottom: 15px;
}

.password-input {
  width: 100%;
  padding: 12px 45px 12px 15px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.password-input:focus {
  border-color: #4285f4;
  box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.1);
}

.strength-bar {
  height: 6px;
  background-color: #e1e5e9;
  border-radius: 3px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  border-radius: 3px;
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.requirements-list {
  margin: 15px 0;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #e1e5e9;
}

.requirement-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
  transition: all 0.3s ease;
}

.requirement-note {
  margin: 8px 0;
  padding-left: 26px; /* Align with requirement items */
  font-size: 13px;
  color: #888;
  font-style: italic;
}

.requirement-item:last-child {
  margin-bottom: 0;
}

.requirement-item.met {
  color: #44cc44;
}

.check-icon {
  margin-right: 10px;
  font-weight: bold;
  font-size: 12px;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.requirement-item:not(.met) .check-icon {
  color: #ff4444;
  background-color: rgba(255, 68, 68, 0.1);
}

.requirement-item.met .check-icon {
  color: #44cc44;
  background-color: rgba(68, 204, 68, 0.1);
}

/* Responsive design */
@media (max-width: 480px) {
  .password-strength-container {
    padding: 15px;
  }
  
  .password-input {
    font-size: 16px; /* Prevent zoom on iOS */
  }
}
</style>