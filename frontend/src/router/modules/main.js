const routes = [
  {
    path: "/",
    name: "homepage",
    component: () =>
      import(/* webpackChunkName: "main" */ "@/views/LandingPage.vue"),
  },
  {
    path: "/explore",
    name: "explore",
    component: () =>
      import(/* webpackChunkName: "main" */ "@/views/RandomExplorePage.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import(/* webpackChunkName: "main" */ "@/views/LoginPage.vue"),
  },
  {
    path: "/landing",
    name: "landing",
    component: () => import(/* webpackChunkName: "main" */ "@/views/LandingPage.vue"),
  },
  {
    path: "/signup",
    name: "signup",
    component: () => import(/* webpackChunkName: "main" */ "@/views/SignUpPage.vue"),
  },
  {
    path: "/businessSignup",
    name: "businessSignup",
    component: () => import(/* webpackChunkName: "main" */ "@/views/BusinessSignUpPage.vue"),
  },
  {
    path: "/billingSecurity",
    name: "billingSecurity",
    component: () => import(/* webpackChunkName: "main" */ "@/views/BillingSecurity.vue"),
  },
  {
    path: "/search/:input?",
    name: "search",
    component: () => import(/* webpackChunkName: "main" */ "@/views/SearchView.vue"),
  },
  {
    path: "/browse/drink/:browseDrinkType/:browseTypeCategory?",
    name: "browseDrink", // Changed from "browse" to "browseDrink"
    component: () => import(/* webpackChunkName: "main" */ "@/views/BrowseListings.vue"),
    props: true,
  },
  {
    path: "/browse/venue/",
    name: "browseVenue", // Changed from "browse" to "browseVenue"
    component: () => import(/* webpackChunkName: "main" */ "@/views/BrowseVenues.vue"),
    props: true,
  },
  {
    path: "/getListingsByObservationTag/:tag?",
    name: "getListingsByObservationTag",
    component: () => import(/* webpackChunkName: "main" */ "@/views/ListingsByTag.vue"),
    props: true,
  },
  {
    path: "/imageSearch",
    name: "imageSearch",
    component: () => import(/* webpackChunkName: "main" */ "@/views/ImageSearchView.vue"),
  },
  {
    path: "/successfulOnboarding",
    name: "successfulOnboarding",
    component: () => import(/* webpackChunkName: "main" */ "@/views/SuccessfulOnboarding.vue"),
  },
  {
    path: "/my-cellar",
    name: "myCellar",
    component: () => import('@/views/MyCellar.vue'),
    props: true
  },
  {
    path: "/my-cellar/:ownerType(user|producer|venue)/:id(\\d+)/:username",
    name: "myCellarDetailed",
    component: () => import('@/views/MyCellarPage.vue'),
    props: true,
    beforeEnter: (to, from, next) => {
      // Check if user is authenticated
      const currentUserId = localStorage.getItem("88B_accID");
      const currentUserType = localStorage.getItem("88B_accType");
      const currentUsername = localStorage.getItem("88B_accUsername");
      
      // If not logged in, redirect to login
      if (!currentUserId || !currentUserType) {
        next('/login');
        return;
      }
      
      // Check if the current user is trying to access their own cellar
      const isOwnCellar = (
        currentUserType === to.params.ownerType &&
        currentUserId === to.params.id &&
        currentUsername === to.params.username
      );
      
      // If not their own cellar, redirect to their own cellar
      if (!isOwnCellar) {
        const ownCellarPath = `/my-cellar/${currentUserType}/${currentUserId}/${currentUsername}`;
        next(ownCellarPath);
        return;
      }
      
      // Allow access to their own cellar
      next();
    }
  },
];

export default routes;