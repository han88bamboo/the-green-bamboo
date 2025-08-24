
const routes = [
  {
    path: "/Venues/Add-Menu/:id",
    name: "venuesAddMenu",
    component: () => import(/* webpackChunkName: "legacy" */ "@/views/Venues/AddMenu.vue"),
  },
];

export default routes;
