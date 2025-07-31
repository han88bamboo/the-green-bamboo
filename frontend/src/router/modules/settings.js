const routes = [
  {
    path: "/business/settings",
    name: "businessSettings",
    component: () => import(/* webpackChunkName: "settings" */ "@/views/BusinessSettings.vue"),
    // meta: { requiresAuth: true },
  },
];

export default routes;