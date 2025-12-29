
const routes = [
  {
    path: "/admin/dashboard",
    name: "admindashboard",
    component: () => import(/* webpackChunkName: "admin" */ "@/views/Admin/AdminDashboard.vue"),
    // meta: { requiresAuth: true },
  },

  {
    path: "/admin/importListings",
    name: "adminimportlistings",
    component: () => import(/* webpackChunkName: "admin" */ "@/views/Admin/OldImportListings.vue"),
    // meta: { requiresAuth: true },
  },
];

export default routes;
