import { createRouter, createWebHistory } from "vue-router";
import main from "./modules/main";
import profile from "./modules/profile";
import listing from "./modules/listing";
import request from "./modules/request";
import qa from "./modules/qa";
import dashboard from "./modules/dashboard";
import settings from "./modules/settings";
import admin from "./modules/admin";
import club from "./modules/club";
import event from "./modules/event";
import partner from "./modules/partner";
import misc from "./modules/misc";
import legacy from "./modules/legacy";
import assembly from "./modules/assembly";
import story from "./modules/story";

const routes = [
  ...main,
  ...profile,
  ...listing,
  ...request,
  ...qa,
  ...dashboard,
  ...settings,
  ...admin,
  ...club,
  ...event,
  ...partner,
  ...misc,
  ...legacy,
  ...assembly,
  ...story,
  { 
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFound.vue')
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  // ADDED BY SMU GROUP 3 (This ensure that the user is brought to the top of the page when they navigate from one page to another)
  scrollBehavior(to, from, savedPosition) {
    // Check if we're navigating within the same user profile (same component, different list)
    if (to.name === from.name && 
        to.params.userID === from.params.userID && 
        to.path.includes('/profile/user/') && 
        from.path.includes('/profile/user/')) {
      // Preserve scroll position when navigating within the same profile
      return false; // Don't scroll at all
    }
    
    // Always force scroll to top immediately for new navigation
    // This prevents scroll position inheritance from previous page
    if (!savedPosition) {
      // Immediately force scroll to top to prevent flash of wrong position
      document.documentElement.scrollTop = 0;
      document.body.scrollTop = 0;
    }
    
    if (savedPosition) {
      return savedPosition; // Keeps the previous scroll position when navigating back
    } else {
      return { top: 0, left: 0, behavior: "smooth" }; // Scrolls to the top for new pages
    }
  },
});

// router.beforeEach((to, from, next) => {
//   const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
//   const isAuthenticated = false; // authentication check, re implements when store is introduce

//   if (requiresAuth && !isAuthenticated) {
//     console.log('Redirecting to login');
//     next('/login');
//   } else {
//     next();
//   }
// });

export default router;