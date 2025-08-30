<template>
  <!-- Category Navigation Ribbon -->
  <section class="category-ribbon-section pt-5">
    <div class="category-ribbon-bar">
      <div class="container">
        <h3 class="mb-0 pt-2 fw-bold" style="color:white;">I'm Looking For</h3>
        <div class="category-underline pt-0"></div>
        <div class="category-ribbon-nav">
          <!-- Loop through categories -->
          <div v-for="category in categories" :key="category.id" class="category-item"
            :ref="el => itemRefs[category.id] = el" @mouseenter="handleMouseEnter(category)"
            @mouseleave="handleMouseLeave(category)">

            <router-link :to="{ name: 'browse', params: category.params }" class="category-link"
              @click.prevent="toggleMobileCategoryMenu(category, $event)">
              {{ category.name }}
            </router-link>

            <!-- Mega Menu -->
            <div class="mega-menu" :ref="el => menuRefs[category.id] = el" :class="{
              'active': category.active,
              'position-top': category.menuFlipped
            }" :style="category.menuStyle">
              <div class="mega-menu-content">
                <!-- Main Category Link -->
                <router-link :to="{ name: 'browse', params: category.params }" class="subcategory-link main-category">
                  {{ category.name }}
                </router-link>
                <!-- Subcategory Links -->
                <router-link v-for="sub in category.subcategories" :key="sub.name"
                  :to="{ name: 'browse', params: sub.params }" class="subcategory-link">
                  {{ sub.name }}
                </router-link>
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
  data() {
    return {
      categories: [
        {
          id: 'wine', name: 'Wine', params: { browseDrinkType: 'Wine' }, active: false, menuFlipped: false, menuStyle: {},
          subcategories: [
            { name: 'Red Wine', params: { browseDrinkType: 'Wine', browseTypeCategory: 'Red Wine' } },
            { name: 'White Wine', params: { browseDrinkType: 'Wine', browseTypeCategory: 'White Wine' } },
            { name: 'Rosé Wine', params: { browseDrinkType: 'Wine', browseTypeCategory: 'Rosé Wine' } },
            { name: 'Sparkling Wine', params: { browseDrinkType: 'Wine', browseTypeCategory: 'Sparkling Wine' } },
            { name: 'Fortified Wine', params: { browseDrinkType: 'Wine', browseTypeCategory: 'Fortified Wine' } },
            { name: 'Dessert Wine', params: { browseDrinkType: 'Wine', browseTypeCategory: 'Dessert Wine' } },
          ]
        },
        {
          id: 'beer', name: 'Beer', params: { browseDrinkType: 'Beer' }, active: false, menuFlipped: false, menuStyle: {},
          subcategories: [
            { name: 'IPA (India Pale Ale)', params: { browseDrinkType: 'Beer', browseTypeCategory: 'IPA (India Pale Ale)' } },
            { name: 'Lager', params: { browseDrinkType: 'Beer', browseTypeCategory: 'Lager' } },
            { name: 'Stout', params: { browseDrinkType: 'Beer', browseTypeCategory: 'Stout' } },
            { name: 'Pale Ale', params: { browseDrinkType: 'Beer', browseTypeCategory: 'Pale Ale' } },
            { name: 'Wheat Beer', params: { browseDrinkType: 'Beer', browseTypeCategory: 'Wheat Beer' } },
            { name: 'Porter', params: { browseDrinkType: 'Beer', browseTypeCategory: 'Porter' } },
            { name: 'Sour', params: { browseDrinkType: 'Beer', browseTypeCategory: 'Sour' } },
          ]
        },
        {
          id: 'sake', name: 'Sake', params: { browseDrinkType: 'Sake' }, active: false, menuFlipped: false, menuStyle: {},
          subcategories: [
            { name: 'Junmai', params: { browseDrinkType: 'Sake', browseTypeCategory: 'Junmai' } },
            { name: 'Junmai Ginjo', params: { browseDrinkType: 'Sake', browseTypeCategory: 'Junmai Ginjo' } },
            { name: 'Junmai Daiginjo', params: { browseDrinkType: 'Sake', browseTypeCategory: 'Junmai Daiginjo' } },
            { name: 'Honjozo', params: { browseDrinkType: 'Sake', browseTypeCategory: 'Honjozo (Alcohol added)' } },
            { name: 'Nigori', params: { browseDrinkType: 'Sake', browseTypeCategory: 'Nigori' } },
            { name: 'Sparkling', params: { browseDrinkType: 'Sake', browseTypeCategory: 'Sparkling' } },
          ]
        },
        {
          id: 'whisky', name: 'Whisky', params: { browseDrinkType: 'Whisky' }, active: false, menuFlipped: false, menuStyle: {},
          subcategories: [
            { name: 'Single Malt', params: { browseDrinkType: 'Whisky', browseTypeCategory: 'Single Malt' } },
            { name: 'Single Grain', params: { browseDrinkType: 'Whisky', browseTypeCategory: 'Single Grain' } },
            { name: 'Blended', params: { browseDrinkType: 'Whisky', browseTypeCategory: 'Blended' } },
            { name: 'Bourbon', params: { browseDrinkType: 'Whisky', browseTypeCategory: 'Bourbon' } },
            { name: 'Rye Whiskey', params: { browseDrinkType: 'Whisky', browseTypeCategory: 'Rye Whiskey' } },
            { name: 'Irish Pot Still', params: { browseDrinkType: 'Whisky', browseTypeCategory: 'Irish Pot Still Whiskey' } },
            { name: 'Tennessee Whiskey', params: { browseDrinkType: 'Whisky', browseTypeCategory: 'Tennessee Whiskey' } },
          ]
        },
        {
          id: 'rum', name: 'Rum', params: { browseDrinkType: 'Rum' }, active: false, menuFlipped: false, menuStyle: {},
          subcategories: [
            { name: 'Traditional Rum', params: { browseDrinkType: 'Rum', browseTypeCategory: 'Molasses - Traditional Rum (Column Still)' } },
            { name: 'Pure Single Rum', params: { browseDrinkType: 'Rum', browseTypeCategory: 'Molasses - Pure Single Rum (Pot Still)' } },
            { name: 'White Unaged', params: { browseDrinkType: 'Rum', browseTypeCategory: 'Molasses - White Unaged' } },
            { name: 'Clairin / Cachaça', params: { browseDrinkType: 'Rum', browseTypeCategory: 'Syrup / Juice - Clairin / Cachaça / Aguardiente / Grogue' } },
            { name: 'Flavoured / Spiced', params: { browseDrinkType: 'Rum', browseTypeCategory: 'Flavoured / Spiced' } },
          ]
        },
        {
          id: 'tequila', name: 'Tequila', params: { browseDrinkType: 'Tequila' }, active: false, menuFlipped: false, menuStyle: {},
          subcategories: [
            { name: 'Blanco', params: { browseDrinkType: 'Tequila', browseTypeCategory: 'Blanco (Unaged / White)' } },
            { name: 'Reposado', params: { browseDrinkType: 'Tequila', browseTypeCategory: 'Reposado (Aged)' } },
            { name: 'Añejo', params: { browseDrinkType: 'Tequila', browseTypeCategory: 'Añejo (Extra Aged)' } },
            { name: 'Extra Añejo', params: { browseDrinkType: 'Tequila', browseTypeCategory: 'Extra Añejo (Ultra Aged)' } },
            { name: 'Cristalino', params: { browseDrinkType: 'Tequila', browseTypeCategory: 'Cristalino' } },
          ]
        },
        {
          id: 'gin', name: 'Gin', params: { browseDrinkType: 'Gin' }, active: false, menuFlipped: false, menuStyle: {},
          subcategories: [
            { name: 'London Dry', params: { browseDrinkType: 'Gin', browseTypeCategory: 'London Dry' } },
            { name: 'Contemporary', params: { browseDrinkType: 'Gin', browseTypeCategory: 'Contemporary' } },
            { name: 'Plymouth Gin', params: { browseDrinkType: 'Gin', browseTypeCategory: 'Plymouth Gin' } },
            { name: 'Old Tom', params: { browseDrinkType: 'Gin', browseTypeCategory: 'Old Tom' } },
            { name: 'Genever', params: { browseDrinkType: 'Gin', browseTypeCategory: 'Genever' } },
            { name: 'Navy Strength', params: { browseDrinkType: 'Gin', browseTypeCategory: 'Navy Strength' } },
          ]
        },
        {
          id: 'baijiu', name: 'Baijiu', params: { browseDrinkType: 'Baijiu' }, active: false, menuFlipped: false, menuStyle: {},
          subcategories: [
            { name: 'Strong Aroma', params: { browseDrinkType: 'Baijiu', browseTypeCategory: 'Strong Aroma (Nong Xiang)' } },
            { name: 'Light Aroma', params: { browseDrinkType: 'Baijiu', browseTypeCategory: 'Light Aroma (Qing Xiang)' } },
            { name: 'Sauce Aroma', params: { browseDrinkType: 'Baijiu', browseTypeCategory: 'Sauce Aroma (Jiang Xiang)' } },
            { name: 'Rice Aroma', params: { browseDrinkType: 'Baijiu', browseTypeCategory: 'Rice Aroma (Mi Xiang)' } },
            { name: 'Phoenix Aroma', params: { browseDrinkType: 'Baijiu', browseTypeCategory: 'Phoenix Aroma (Feng Xiang)' } },
          ]
        },
      ],
      itemRefs: {},
      menuRefs: {},
      activeMobileCategory: null,
    };
  },
  methods: {
    handleMouseEnter(category) {
      if (window.innerWidth >= 992) {
        this.updateMenu(category, true);
      }
    },

    handleMouseLeave(category) {
      if (window.innerWidth >= 992) {
        this.updateMenu(category, false);
      }
    },

    toggleMobileCategoryMenu(category) {
      if (window.innerWidth <= 991) {
        // If another category is open, close it.
        if (this.activeMobileCategory && this.activeMobileCategory.id !== category.id) {
          this.updateMenu(this.activeMobileCategory, false);
        }

        // Toggle the current category
        this.updateMenu(category, !category.active);

        // Update the active category reference
        this.activeMobileCategory = category.active ? category : null;

      } else {
        // For desktop, allow the router link to navigate
        this.$router.push({ name: 'browse', params: category.params });
      }
    },

    updateMenu(category, isActive) {
      // Reset styles when deactivating
      if (!isActive) {
        category.active = false;
        category.menuFlipped = false;
        category.menuStyle = {};
        return;
      }

      category.active = true;

      this.$nextTick(() => {
        const itemEl = this.itemRefs[category.id];
        const menuEl = this.menuRefs[category.id];
        if (!itemEl || !menuEl) return;

        const itemRect = itemEl.getBoundingClientRect();
        const menuRect = menuEl.getBoundingClientRect();
        const viewportHeight = window.innerHeight;
        const viewportWidth = window.innerWidth;

        // Vertical flip logic (for both mobile and desktop)
        const wouldOverflowBottom = (itemRect.bottom + menuRect.height + 20) > viewportHeight;
        category.menuFlipped = wouldOverflowBottom;

        // Mobile-specific horizontal positioning
        if (window.innerWidth <= 991) {
          const newMenuStyle = {
            left: '50%',
            right: 'auto',
            transform: 'translateX(-50%)',
          };

          // Must re-measure after flip class is applied
          this.$nextTick(() => {
            const updatedMenuRect = menuEl.getBoundingClientRect();

            if (updatedMenuRect.right > viewportWidth - 10) {
              newMenuStyle.left = 'auto';
              newMenuStyle.right = '0';
              newMenuStyle.transform = 'translateX(0)';
            } else if (updatedMenuRect.left < 10) {
              newMenuStyle.left = '0';
              newMenuStyle.right = 'auto';
              newMenuStyle.transform = 'translateX(0)';
            }
            category.menuStyle = newMenuStyle;
          });
        }
      });
    },
  }
}
</script>

<style scoped>
/* Styles are largely the same, but some rules are updated for the new reactive classes */
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

/* Use the .active class for visibility */
.category-item .mega-menu.active {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.category-item .mega-menu.active.position-top {
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
  .category-ribbon-nav {
    flex-direction: row;
    justify-content: center;
    overflow-y: visible;
    padding: 0 10px;
  }

  .category-item {
    flex: 0 0 auto;
    min-width: auto;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom: none;
  }

  .category-item:last-child {
    border-right: none;
  }

  .category-link {
    padding: 12px 16px;
    font-size: 13px;
    border-right: none;
    text-align: center;
    min-width: 70px;
  }

  .mega-menu {
    left: 50%;
    transform: translateX(-50%);
    max-height: none;
    overflow: visible;
    min-width: 180px;
    z-index: 10001;
  }

  /* Mobile top positioning */
  .mega-menu.position-top {
    top: auto;
    bottom: 100%;
  }

  /* Mobile active state requires style bindings for transform */
  .mega-menu.active {
    opacity: 1;
    visibility: visible;
    transform: translateX(-50%) translateY(0);
  }

  .mega-menu.active.position-top {
    opacity: 1;
    visibility: visible;
    transform: translateX(-50%) translateY(0);
  }

  .subcategory-link {
    padding: 8px 16px;
    font-size: 12px;
    border-left: none;
  }

  .subcategory-link.main-category {
    border-left: none;
  }

  .subcategory-link:hover {
    padding-left: 16px;
    border-left: none;
  }

  /* These might still be needed if menus are wide, but the !important is removed */
  .baijiu-menu {
    transform: translateX(-35%);
  }

  .whisky-menu {
    transform: translateX(-35%);
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

  .mega-menu.position-top::before {
    top: auto;
    bottom: -8px;
    border-bottom: none;
    border-top: 8px solid white;
  }

  .mega-menu.active::before {
    opacity: 1;
  }
}
</style>
