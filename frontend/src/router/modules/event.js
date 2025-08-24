const routes = [
  {
    path: "/event/:eventID/:eventName",
    name: "eventview",
    component: () => import(/* webpackChunkName: "event" */ "@/views/SpecificEventPage.vue"),
  },

  {
    path: "/events/view",
    name: "eventspage",
    component: () => import(/* webpackChunkName: "event" */ "@/views/Users/Events.vue"),
  },
];

export default routes;