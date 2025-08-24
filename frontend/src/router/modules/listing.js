
const routes = [
  {
    path: "/listing/view/:listingID/:listingName",
    name: "listingView",
    component: () => import(/* webpackChunkName: "listing" */ "@/views/Producers/BottleListings.vue"),
  },
  {
    path: "/listing/create/:requestID?",
    name: "listingCreate",
    component: () => import(/* webpackChunkName: "listing" */ "@/views/Producers/CreateListing.vue"),
    // meta: { requiresAuth: true },
  },
  {
    path: "/listing/edit/:listingID/:requestID?",
    name: "listingEdit",
    component: () => import(/* webpackChunkName: "listing" */ "@/views/Producers/EditListing.vue"),
    // meta: { requiresAuth: true },
  },
];

export default routes;
