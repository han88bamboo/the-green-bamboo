<template>
  <!-- Category Navigation Ribbon -->
  <section class="category-ribbon-section pt-5">
    <div class="category-ribbon-bar">
      <div class="container">
        <h3 class="mb-0 pt-2 fw-bold" style="color:white;">I'm Looking For</h3>
        <div class="category-underline pt-0"></div>
        <div class="category-ribbon-nav">
          <!-- Wine -->
          <div class="category-item" :class="{ 'active': isMobileCategoryActive('wine') }" data-category="wine"
            @mouseenter="handleMegaMenuPosition">
            <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Wine' } }" class="category-link"
              @click="toggleMobileCategoryMenu('wine', $event)">
              Wine
            </router-link>
            <div class="mega-menu">
              <div class="mega-menu-content">
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Wine' } }"
                  class="subcategory-link main-category">Wine</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Wine', browseTypeCategory: 'Red Wine' } }"
                  class="subcategory-link">Red Wine</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Wine', browseTypeCategory: 'White Wine' } }"
                  class="subcategory-link">White Wine</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Wine', browseTypeCategory: 'Rosé Wine' } }"
                  class="subcategory-link">Rosé Wine</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Wine', browseTypeCategory: 'Sparkling Wine' } }"
                  class="subcategory-link">Sparkling Wine</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Wine', browseTypeCategory: 'Fortified Wine' } }"
                  class="subcategory-link">Fortified Wine</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Wine', browseTypeCategory: 'Dessert Wine' } }"
                  class="subcategory-link">Dessert Wine</router-link>
              </div>
            </div>
          </div>

          <!-- Beer -->
          <div class="category-item" :class="{ 'active': isMobileCategoryActive('beer') }" data-category="beer"
            @mouseenter="handleMegaMenuPosition">
            <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Beer' } }" class="category-link"
              @click="toggleMobileCategoryMenu('beer', $event)">
              Beer
            </router-link>
            <div class="mega-menu">
              <div class="mega-menu-content">
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Beer' } }"
                  class="subcategory-link main-category">Beer</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Beer', browseTypeCategory: 'IPA (India Pale Ale)' } }"
                  class="subcategory-link">IPA (India Pale Ale)</router-link>
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Beer', browseTypeCategory: 'Lager' } }"
                  class="subcategory-link">Lager</router-link>
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Beer', browseTypeCategory: 'Stout' } }"
                  class="subcategory-link">Stout</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Beer', browseTypeCategory: 'Pale Ale' } }"
                  class="subcategory-link">Pale Ale</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Beer', browseTypeCategory: 'Wheat Beer' } }"
                  class="subcategory-link">Wheat Beer</router-link>
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Beer', browseTypeCategory: 'Porter' } }"
                  class="subcategory-link">Porter</router-link>
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Beer', browseTypeCategory: 'Sour' } }"
                  class="subcategory-link">Sour</router-link>
              </div>
            </div>
          </div>

          <!-- Sake -->
          <div class="category-item" :class="{ 'active': isMobileCategoryActive('sake') }" data-category="sake"
            @mouseenter="handleMegaMenuPosition">
            <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Sake' } }" class="category-link"
              @click="toggleMobileCategoryMenu('sake', $event)">
              Sake
            </router-link>
            <div class="mega-menu">
              <div class="mega-menu-content">
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Sake' } }"
                  class="subcategory-link main-category">Sake</router-link>
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Sake', browseTypeCategory: 'Junmai' } }"
                  class="subcategory-link">Junmai</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Sake', browseTypeCategory: 'Junmai Ginjo' } }"
                  class="subcategory-link">Junmai Ginjo</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Sake', browseTypeCategory: 'Junmai Daiginjo' } }"
                  class="subcategory-link">Junmai Daiginjo</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Sake', browseTypeCategory: 'Honjozo (Alcohol added)' } }"
                  class="subcategory-link">Honjozo</router-link>
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Sake', browseTypeCategory: 'Nigori' } }"
                  class="subcategory-link">Nigori</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Sake', browseTypeCategory: 'Sparkling' } }"
                  class="subcategory-link">Sparkling</router-link>
              </div>
            </div>
          </div>

          <!-- Whisky -->
          <div class="category-item" :class="{ 'active': isMobileCategoryActive('whisky') }" data-category="whisky"
            @mouseenter="handleMegaMenuPosition">
            <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Whisky' } }" class="category-link"
              @click="toggleMobileCategoryMenu('whisky', $event)">
              Whisky
            </router-link>
            <div class="mega-menu whisky-menu">
              <div class="mega-menu-content">
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Whisky' } }"
                  class="subcategory-link main-category">Whisky</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Whisky', browseTypeCategory: 'Single Malt' } }"
                  class="subcategory-link">Single Malt</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Whisky', browseTypeCategory: 'Single Grain' } }"
                  class="subcategory-link">Single Grain</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Whisky', browseTypeCategory: 'Blended' } }"
                  class="subcategory-link">Blended</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Whisky', browseTypeCategory: 'Bourbon' } }"
                  class="subcategory-link">Bourbon</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Whisky', browseTypeCategory: 'Rye Whiskey' } }"
                  class="subcategory-link">Rye Whiskey</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Whisky', browseTypeCategory: 'Irish Pot Still Whiskey' } }"
                  class="subcategory-link">Irish Pot Still</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Whisky', browseTypeCategory: 'Tennessee Whiskey' } }"
                  class="subcategory-link">Tennessee Whiskey</router-link>
              </div>
            </div>
          </div>

          <!-- Rum -->
          <div class="category-item" :class="{ 'active': isMobileCategoryActive('rum') }" data-category="rum"
            @mouseenter="handleMegaMenuPosition">
            <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Rum' } }" class="category-link"
              @click="toggleMobileCategoryMenu('rum', $event)">
              Rum
            </router-link>
            <div class="mega-menu">
              <div class="mega-menu-content">
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Rum' } }"
                  class="subcategory-link main-category">Rum</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Rum', browseTypeCategory: 'Molasses - Traditional Rum (Column Still)' } }"
                  class="subcategory-link">Traditional Rum</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Rum', browseTypeCategory: 'Molasses - Pure Single Rum (Pot Still)' } }"
                  class="subcategory-link">Pure Single Rum</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Rum', browseTypeCategory: 'Molasses - White Unaged' } }"
                  class="subcategory-link">White Unaged</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Rum', browseTypeCategory: 'Syrup / Juice - Clairin / Cachaça / Aguardiente / Grogue' } }"
                  class="subcategory-link">Clairin / Cachaça</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Rum', browseTypeCategory: 'Flavoured / Spiced' } }"
                  class="subcategory-link">Flavoured / Spiced</router-link>
              </div>
            </div>
          </div>

          <!-- Tequila -->
          <div class="category-item" :class="{ 'active': isMobileCategoryActive('tequila') }" data-category="tequila"
            @mouseenter="handleMegaMenuPosition">
            <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Tequila' } }" class="category-link"
              @click="toggleMobileCategoryMenu('tequila', $event)">
              Tequila
            </router-link>
            <div class="mega-menu">
              <div class="mega-menu-content">
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Tequila' } }"
                  class="subcategory-link main-category">Tequila</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Tequila', browseTypeCategory: 'Blanco (Unaged / White)' } }"
                  class="subcategory-link">Blanco</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Tequila', browseTypeCategory: 'Reposado (Aged)' } }"
                  class="subcategory-link">Reposado</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Tequila', browseTypeCategory: 'Añejo (Extra Aged)' } }"
                  class="subcategory-link">Añejo</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Tequila', browseTypeCategory: 'Extra Añejo (Ultra Aged)' } }"
                  class="subcategory-link">Extra Añejo</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Tequila', browseTypeCategory: 'Cristalino' } }"
                  class="subcategory-link">Cristalino</router-link>
              </div>
            </div>
          </div>

          <!-- Gin -->
          <div class="category-item" :class="{ 'active': isMobileCategoryActive('gin') }" data-category="gin"
            @mouseenter="handleMegaMenuPosition">
            <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Gin' } }" class="category-link"
              @click="toggleMobileCategoryMenu('gin', $event)">
              Gin
            </router-link>
            <div class="mega-menu">
              <div class="mega-menu-content">
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Gin' } }"
                  class="subcategory-link main-category">Gin</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Gin', browseTypeCategory: 'London Dry' } }"
                  class="subcategory-link">London Dry</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Gin', browseTypeCategory: 'Contemporary' } }"
                  class="subcategory-link">Contemporary</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Gin', browseTypeCategory: 'Plymouth Gin' } }"
                  class="subcategory-link">Plymouth Gin</router-link>
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Gin', browseTypeCategory: 'Old Tom' } }"
                  class="subcategory-link">Old Tom</router-link>
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Gin', browseTypeCategory: 'Genever' } }"
                  class="subcategory-link">Genever</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Gin', browseTypeCategory: 'Navy Strength' } }"
                  class="subcategory-link">Navy Strength</router-link>
              </div>
            </div>
          </div>

          <!-- Baijiu -->
          <div class="category-item" :class="{ 'active': isMobileCategoryActive('baijiu') }" data-category="baijiu"
            @mouseenter="handleMegaMenuPosition">
            <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Baijiu' } }" class="category-link"
              @click="toggleMobileCategoryMenu('baijiu', $event)">
              Baijiu
            </router-link>
            <div class="mega-menu baijiu-menu">
              <div class="mega-menu-content">
                <router-link :to="{ name: 'browse', params: { browseDrinkType: 'Baijiu' } }"
                  class="subcategory-link main-category">Baijiu</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Baijiu', browseTypeCategory: 'Strong Aroma (Nong Xiang)' } }"
                  class="subcategory-link">Strong Aroma</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Baijiu', browseTypeCategory: 'Light Aroma (Qing Xiang)' } }"
                  class="subcategory-link">Light Aroma</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Baijiu', browseTypeCategory: 'Sauce Aroma (Jiang Xiang)' } }"
                  class="subcategory-link">Sauce Aroma</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Baijiu', browseTypeCategory: 'Rice Aroma (Mi Xiang)' } }"
                  class="subcategory-link">Rice Aroma</router-link>
                <router-link
                  :to="{ name: 'browse', params: { browseDrinkType: 'Baijiu', browseTypeCategory: 'Phoenix Aroma (Feng Xiang)' } }"
                  class="subcategory-link">Phoenix Aroma</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  mounted() {
    // Initialize mega menu positioning
    this.$nextTick(() => {
      this.handleMegaMenuPosition();

      // Add resize listener with debouncing
      this.debouncedPositionHandler = this.debounce(this.handleMegaMenuPosition, 150);
      window.addEventListener('resize', this.debouncedPositionHandler);

      // Add scroll listener for repositioning on scroll
      window.addEventListener('scroll', this.debouncedPositionHandler, { passive: true });
    });
  },

  beforeUnmount() {
    // Clean up event listeners
    if (this.debouncedPositionHandler) {
      window.removeEventListener('resize', this.debouncedPositionHandler);
      window.removeEventListener('scroll', this.debouncedPositionHandler);
    }
  },

  methods: {
    // Debounced version of position handler for performance
    debounce(func, wait) {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    },

    // Check if mobile category is active
    isMobileCategoryActive(categoryId) {
      return this.activeMobileCategoryId === categoryId;
    },

    // Mobile category menu toggle for tap-to-open behavior
    toggleMobileCategoryMenu(categoryId, event) {
      // Only handle mobile behavior (screen width <= 991px)
      if (window.innerWidth <= 991) {
        event.preventDefault();

        // Close any currently open mobile menu first
        if (this.activeMobileCategoryId === categoryId) {
          this.activeMobileCategoryId = null;
        } else {
          this.activeMobileCategoryId = categoryId;

          // Position the dropdown to avoid viewport overflow
          this.$nextTick(() => {
            this.handleMobileMegaMenuPosition(categoryId);
          });
        }
      }
    },

    // Handle mobile mega menu positioning
    handleMobileMegaMenuPosition(categoryId) {
      if (window.innerWidth <= 991) {
        const categoryItem = document.querySelector(`.category-item[data-category="${categoryId}"]`);
        const activeItem = document.querySelector(`.category-item[data-category="${categoryId}"] .mega-menu`);
        if (!activeItem || !categoryItem) return;

        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;

        // Reset positioning and classes
        activeItem.style.left = '50%';
        activeItem.style.right = 'auto';
        activeItem.style.transform = 'translateX(-50%)';
        activeItem.classList.remove('position-top');

        // Get positions after reset
        const categoryRect = categoryItem.getBoundingClientRect();
        const menuRect = activeItem.getBoundingClientRect();

        // Check for vertical overflow (similar to desktop logic)
        const wouldOverflowBottom = (categoryRect.bottom + menuRect.height + 20) > viewportHeight;

        if (wouldOverflowBottom) {
          activeItem.classList.add('position-top');
          // Adjust transform for top positioning
          activeItem.style.transform = 'translateX(-50%) translateY(0)';
        }

        // Check if menu would overflow right edge
        const updatedMenuRect = activeItem.getBoundingClientRect();
        if (updatedMenuRect.right > viewportWidth - 10) {
          activeItem.style.left = 'auto';
          activeItem.style.right = '0';
          if (wouldOverflowBottom) {
            activeItem.style.transform = 'translateX(0) translateY(0)';
          } else {
            activeItem.style.transform = 'translateX(0)';
          }
        }

        // Check if menu would overflow left edge
        if (updatedMenuRect.left < 10) {
          activeItem.style.left = '0';
          activeItem.style.right = 'auto';
          if (wouldOverflowBottom) {
            activeItem.style.transform = 'translateX(0) translateY(0)';
          } else {
            activeItem.style.transform = 'translateX(0)';
          }
        }
      }
    },

    // Smart positioning for mega menu to avoid viewport overflow
    handleMegaMenuPosition() {
      if (window.innerWidth >= 992) { // Only for desktop
        const categoryItems = document.querySelectorAll('.category-item');

        categoryItems.forEach(item => {
          const megaMenu = item.querySelector('.mega-menu');
          if (megaMenu) {
            // Reset positioning
            megaMenu.classList.remove('position-top');

            // Get positions
            const itemRect = item.getBoundingClientRect();
            const menuRect = megaMenu.getBoundingClientRect();
            const viewportHeight = window.innerHeight;

            // Check if menu would overflow bottom of viewport
            const wouldOverflow = (itemRect.bottom + menuRect.height + 20) > viewportHeight;

            if (wouldOverflow) {
              megaMenu.classList.add('position-top');
            }
          }
        });
      }
    },
  }
}
</script>

<style scoped>
.category-ribbon-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0;
  flex-wrap: wrap;
}

.category-item {
  position: relative;
  display: flex;
  align-items: center;
}

.category-link {
  display: block;
  padding: 16px 24px;
  color: white;
  text-decoration: none;
  font-weight: 600;
  font-size: 15px;
  transition: all 0.3s ease;
  position: relative;
  white-space: nowrap;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.category-link:last-child {
  border-right: none;
}

.category-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
  text-decoration: none;
}

/* Mega Menu Styles */
.mega-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  min-width: 200px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-radius: 8px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
  z-index: 10000;
  border-top: 3px solid #027562;
}

/* Smart positioning - show above when would overflow */
.mega-menu.position-top {
  top: auto;
  bottom: 100%;
  transform: translateY(10px);
  border-top: none;
  border-bottom: 3px solid #027562;
}

.mega-dropdown-panel {
  /* adjust selector to your component */
  position: absolute;
  /* or fixed if you prefer */
  z-index: 2000;
  /* > hero & ribbon */
}

.category-item:hover .mega-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.category-item:hover .mega-menu.position-top {
  transform: translateY(0);
}

.mega-menu-content {
  padding: 12px 0;
}

.subcategory-link {
  display: block;
  padding: 10px 20px;
  color: #333;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}

.subcategory-link.main-category {
  font-weight: 700;
  color: #027562;
  background-color: #f8f9fa;
  border-left: 3px solid #027562;
  margin-bottom: 8px;
}

.subcategory-link:hover {
  background-color: #f8f9fa;
  color: #027562;
  text-decoration: none;
  border-left: 3px solid #027562;
  padding-left: 24px;
}

/* Mobile Responsive */
@media (max-width: 991px) {
  .category-ribbon-bar {
    /* position: relative; */
  }

  .category-ribbon-nav {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 0;
    /* overflow-x: auto; */
    overflow-y: visible;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    -ms-overflow-style: none;
    padding: 0 10px;
  }

  .category-ribbon-nav::-webkit-scrollbar {
    display: none;
  }

  .category-item {
    flex: 0 0 auto;
    min-width: auto;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom: none;
    position: relative;
  }

  .category-item:last-child {
    border-right: none;
  }

  .category-link {
    padding: 12px 16px;
    font-size: 13px;
    white-space: nowrap;
    border-right: none;
    text-align: center;
    min-width: 70px;
  }

  .mega-menu {
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    opacity: 0;
    visibility: hidden;
    max-height: none;
    overflow: visible;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    border-radius: 8px;
    border-top: 3px solid #027562;
    background: white;
    min-width: 180px;
    z-index: 10001;
    transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
  }

  /* Mobile top positioning */
  .mega-menu.position-top {
    top: auto;
    bottom: 100%;
    border-top: none;
    border-bottom: 3px solid #027562;
  }

  .category-item.active .mega-menu {
    opacity: 1;
    visibility: visible;
    transform: translateX(-50%) translateY(0);
  }

  .category-item.active .mega-menu.position-top {
    opacity: 1;
    visibility: visible;
    transform: translateX(-50%) translateY(0);
  }

  .subcategory-link {
    padding: 8px 16px;
    font-size: 12px;
    display: block;
    color: #333;
    border-left: none;
  }

  .subcategory-link.main-category {
    background-color: #f8f9fa;
    color: #027562;
    font-weight: 700;
    margin-bottom: 4px;
    border-left: none;
  }

  .subcategory-link:hover {
    background-color: #f8f9fa;
    color: #027562;
    padding-left: 16px;
    border-left: none;
  }

  .baijiu-menu {
    transform: translateX(-35%) !important;
  }

  .whisky-menu {
    transform: translateX(-35%) !important;
  }
}

@media (max-width: 576px) {
  .category-ribbon-bar {
    padding: 0;
  }

  .category-link {
    padding: 12px 16px;
    font-size: 13px;
  }

  .subcategory-link {
    padding: 6px 25px;
    font-size: 12px;
  }
}

/* Smooth hover animation for desktop */
@media (min-width: 992px) {
  .category-item {
    overflow: visible;
  }

  .mega-menu::before {
    content: '';
    position: absolute;
    top: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-bottom: 8px solid white;
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  /* Arrow for top-positioned menus */
  .mega-menu.position-top::before {
    top: auto;
    bottom: -8px;
    border-bottom: none;
    border-top: 8px solid white;
  }

  .category-item:hover .mega-menu::before {
    opacity: 1;
  }
}
</style>