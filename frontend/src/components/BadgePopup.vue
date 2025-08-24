<template>
  <div v-if="showPopup" class="badge-popup-overlay" @click="handleOverlayClick">
    <div class="badge-popup-container" @click.stop>
      <!-- Close button -->
      <button class="badge-popup-close" @click="closePopup">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>

      <!-- Badge content -->
      <div class="badge-popup-content">
        <h2 class="badge-popup-title">
          {{ currentBadge.isNewBadge ? 'YOU UNLOCKED A BADGE' : 'BADGE LEVEL UP!' }}
        </h2>
        
        <!-- Badge image with level indicator -->
        <div class="badge-image-container">
          <img 
            :src="currentBadge.badgePhoto || defaultBadgePhoto" 
            :alt="currentBadge.badgeName"
            class="badge-image"
            @error="handleImageError"
          />
          <div v-if="!currentBadge.isNewBadge" class="badge-level-indicator">
            Level {{ currentBadge.newLevel }}
          </div>
        </div>

        <!-- Badge details -->
        <h3 class="badge-name">{{ currentBadge.badgeName }}</h3>
        <!-- <p class="badge-description">
          {{ currentBadge.badgeDesc || 'Keep exploring and earning more badges!' }}
        </p> -->
        
        <!-- Badge Level -->
        <div class="badge-level">
          Level {{ currentBadge.newLevel || 1 }}
        </div>

        <!-- Navigation for multiple badges -->
        <div v-if="badges.length > 1" class="badge-navigation">
          <button 
            @click="previousBadge" 
            :disabled="currentIndex === 0"
            class="nav-button"
          >
            &#8249; Previous
          </button>
          <span class="badge-counter">{{ currentIndex + 1 }} / {{ badges.length }}</span>
          <button 
            @click="nextBadge" 
            :disabled="currentIndex === badges.length - 1"
            class="nav-button"
          >
            Next &#8250;
          </button>
        </div>

        <!-- Share button -->
        <button class="share-button" @click="shareBadge">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M18 8C19.6569 8 21 6.65685 21 5C21 3.34315 19.6569 2 18 2C16.3431 2 15 3.34315 15 5C15 5.18147 15.0116 5.35984 15.0341 5.53431L8.96583 9.06862C8.46937 8.42766 7.77617 8 7 8C5.34315 8 4 9.34315 4 11C4 12.6569 5.34315 14 7 14C7.77617 14 8.46937 13.5723 8.96583 12.9314L15.0341 16.4657C15.0116 16.6402 15 16.8185 15 17C15 18.6569 16.3431 20 18 20C19.6569 20 21 18.6569 21 17C21 15.3431 19.6569 14 18 14C17.2238 14 16.5306 14.4277 16.0342 15.0686L9.96583 11.5343C9.98844 11.3598 10 11.1815 10 11C10 10.8185 9.98844 10.6402 9.96583 10.4657L16.0342 6.93138C16.5306 7.57234 17.2238 8 18 8Z" fill="currentColor"/>
          </svg>
          SHARE BADGE
        </button>
      </div>
    </div>

    <!-- Share success message -->
    <div v-if="shareSuccess" class="share-success-message">
      Link copied to clipboard!
    </div>
  </div>
</template>

<script>
export default {
  name: 'BadgePopup',
  props: {
    badges: {
      type: Array,
      default: () => []
    },
    show: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      showPopup: false,
      currentIndex: 0,
      shareSuccess: false,
      defaultBadgePhoto: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultBadgePhoto.png?v=1750084739'
    }
  },
  computed: {
    currentBadge() {
      return this.badges[this.currentIndex] || {};
    }
  },
  watch: {
    show(newValue) {
      if (newValue && this.badges.length > 0) {
        this.showPopup = true;
        this.currentIndex = 0;
        // Prevent body scroll when popup is open
        document.body.style.overflow = 'hidden';
      }
    },
    showPopup(newValue) {
      if (!newValue) {
        // Restore body scroll when popup is closed
        document.body.style.overflow = '';
      }
    }
  },
  methods: {
    closePopup() {
      this.showPopup = false;
      this.currentIndex = 0;
      this.$emit('close');
    },
    
    handleOverlayClick() {
      this.closePopup();
    },
    
    nextBadge() {
      if (this.currentIndex < this.badges.length - 1) {
        this.currentIndex++;
      }
    },
    
    previousBadge() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      }
    },
    
    handleImageError(event) {
      event.target.src = this.defaultBadgePhoto;
    },
    
    async shareBadge() {
      try {
        const badge = this.currentBadge;
        const currentUrl = window.location.origin;
        const shareUrl = `${currentUrl}/badge/${badge.badgeId}?user=${this.$parent.userID || 'shared'}`;
        
        // Create share text
        const shareText = `I just earned the "${badge.badgeName}" badge! ${badge.badgeDesc || 'Check out my achievement!'}`;
        
        // Try to use Web Share API first (mobile)
        if (navigator.share) {
          await navigator.share({
            title: `Badge Earned: ${badge.badgeName}`,
            text: shareText,
            url: shareUrl
          });
        } else {
          // Fallback: copy to clipboard
          await navigator.clipboard.writeText(`${shareText} ${shareUrl}`);
          this.showShareSuccess();
        }
      } catch (error) {
        console.error('Error sharing badge:', error);
        // Fallback for browsers that don't support clipboard API
        this.fallbackCopyToClipboard();
      }
    },
    
    fallbackCopyToClipboard() {
      const badge = this.currentBadge;
      const currentUrl = window.location.origin;
      const shareUrl = `${currentUrl}/badge/${badge.badgeId}?user=${this.$parent.userID || 'shared'}`;
      const shareText = `I just earned the "${badge.badgeName}" badge! ${badge.badgeDesc || 'Check out my achievement!'} ${shareUrl}`;
      
      const textArea = document.createElement('textarea');
      textArea.value = shareText;
      document.body.appendChild(textArea);
      textArea.select();
      
      try {
        document.execCommand('copy');
        this.showShareSuccess();
      } catch (err) {
        console.error('Fallback copy failed:', err);
      }
      
      document.body.removeChild(textArea);
    },
    
    showShareSuccess() {
      this.shareSuccess = true;
      setTimeout(() => {
        this.shareSuccess = false;
      }, 3000);
    }
  },
  
  beforeUnmount() {
    document.body.style.overflow = '';
  }
}
</script>

<style scoped>
.badge-popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease-out;
}

.badge-popup-container {
  background: white;
  border-radius: 20px;
  padding: 40px 30px;
  max-width: 400px;
  width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease-out;
}

.badge-popup-close {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.badge-popup-close:hover {
  background-color: #f0f0f0;
}

.badge-popup-content {
  text-align: center;
}

.badge-popup-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  letter-spacing: 1px;
}

.badge-image-container {
  position: relative;
  display: inline-block;
  margin-bottom: 20px;
}

.badge-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid #8B0000;
  object-fit: cover;
  background: linear-gradient(135deg, #f0b358, #daa520);
}

.badge-level-indicator {
  position: absolute;
  bottom: -5px;
  right: -5px;
  background: #8B0000;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  border: 2px solid white;
}

.badge-name {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
  text-transform: uppercase;
}

.badge-description {
  color: #666;
  margin-bottom: 15px;
  line-height: 1.4;
  font-size: 14px;
}

.badge-level {
  font-size: 18px;
  font-weight: bold;
  color: #FFD700;
  margin-bottom: 20px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.badge-navigation {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.nav-button {
  background: #f0b358;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.nav-button:hover:not(:disabled) {
  background: #daa520;
}

.nav-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.badge-counter {
  font-weight: bold;
  color: #333;
  min-width: 60px;
}

.share-button {
  background: #006A50;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 auto;
  transition: background-color 0.2s;
}

.share-button:hover {
  background: #005144;
}

.share-success-message {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background: #4CAF50;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: bold;
  z-index: 10000;
  animation: slideUpFade 3s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(50px) scale(0.9);
  }
  to { 
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes slideUpFade {
  0% {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
  15% {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
  85% {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
  100% {
    opacity: 0;
    transform: translateX(-50%) translateY(-20px);
  }
}

/* Mobile responsive */
@media (max-width: 480px) {
  .badge-popup-container {
    padding: 30px 20px;
    border-radius: 15px;
  }
  
  .badge-popup-title {
    font-size: 16px;
  }
  
  .badge-image {
    width: 100px;
    height: 100px;
  }
  
  .badge-name {
    font-size: 20px;
  }
  
  .badge-navigation {
    gap: 15px;
  }
  
  .nav-button {
    padding: 6px 10px;
    font-size: 14px;
  }
}
</style>