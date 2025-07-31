const routes = [
  {
    path: "/Producers/ProducersQA/:id",
    name: "producersQa",
    component: () => import(/* webpackChunkName: "qa" */ "@/views/Producers/ProducerQA.vue"),
  },
  {
    path: "/Venues/VenuesQA/:id",
    name: "venuesQa",
    component: () => import(/* webpackChunkName: "qa" */ "@/views/Venues/VenueQA.vue"),
  },
];

export default routes;