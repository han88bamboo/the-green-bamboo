
const routes = [
  {
    path: "/request/view",
    name: "requestView",
    component: () => import(/* webpackChunkName: "request" */ "@/views/Producers/ViewRequests.vue"),
    // meta: { requiresAuth: true },
  },
  {
    path: "/request/new/:requestID?",
    name: "requestNew",
    component: () => import(/* webpackChunkName: "request" */ "@/views/Users/RequestListingNew.vue"),
    // meta: { requiresAuth: true },
  },
  {
    path: "/request/new-bulk/:requestID?",
    name: "requestNewBulk",
    component: () => import(/* webpackChunkName: "request" */ "@/views/Users/BulkRequestListingNew.vue"),
    // meta: { requiresAuth: true },
  },
  {
    path: "/request/modify/:mode/:listingID/:requestID?",
    name: "requestModify",
    component: () => import(/* webpackChunkName: "request" */ "@/views/Users/RequestListingModify.vue"),
    // meta: { requiresAuth: true },
  },
];

export default routes;
