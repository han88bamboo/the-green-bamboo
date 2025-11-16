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

  {
    path: "/events/organiser-dashboard/:userType/:userID",
    name: "eventOrganiserDashboard",
    component: () => import(/* webpackChunkName: "event" */ "@/views/Users/EventOrganiserDashboard.vue"),
  },
];

export default routes;