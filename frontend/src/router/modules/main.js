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
    path: "/my-cellar/:ownerType(user|producer|venue)/:id(\\d+)/:username",
    name: "myCellar",
    component: () => import('@/views/MyCellarPage.vue'),
    props: true
  },
];

export default routes;