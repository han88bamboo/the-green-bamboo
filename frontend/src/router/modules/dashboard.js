
const routes = [
  {
    path: "/Producers/ProducersDashboard/:id",
    name: "producersDashboard",
    component: () => import(/* webpackChunkName: "dashboard" */ "@/views/Producers/ProducerDashboard.vue"),
    // meta: { requiresAuth: true },
  },
  {
    path: "/dashboard/user/:userID",
    name: "dashboardUser",
    component: () => import(/* webpackChunkName: "dashboard" */ "@/views/Users/UserDashboard.vue"),
    // meta: { requiresAuth: true },
  },
  {
    path: "/dashboard/venue/:venueID?",
    name: "dashboardVenue",
    component: () => import(/* webpackChunkName: "dashboard" */ "@/views/Venues/VenueDashboard.vue"),
    // meta: { requiresAuth: true },
  },
];

export default routes;
