
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
  {
    path: "/listing/create-bulk",
    name: "bulkListingCreate",
    component: () => import(/* webpackChunkName: "listing" */ "@/views/Producers/BulkCreateListing.vue"),
    // meta: { requiresAuth: true },
  },
  {
    path: "/listing/import",
    name: "importListings",
    component: () => import(/* webpackChunkName: "listing" */ "@/views/Users/ImportListings.vue"),
    // meta: { requiresAuth: true },
  },
];

export default routes;
