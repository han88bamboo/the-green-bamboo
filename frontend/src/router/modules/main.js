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
    path: "/browse/:browseDrinkType/:browseTypeCategory?",
    name: "browse",
    component: () => import(/* webpackChunkName: "main" */ "@/views/BrowseListings.vue"),
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
    component: () => import(/* webpackChunkName: "main" */ "@/views/MyCellar.vue"),
  },
];

export default routes;