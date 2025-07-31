
const routes = [
  {
    path: "/club/create",
    name: "clubcreate",
    component: () => import(/* webpackChunkName: "club" */ "@/views/Users/CreateClub.vue"),
    // meta: { requiresAuth: true },
  },

  {
    path: "/clubs/view",
    name: "browseclubs",
    component: () => import(/* webpackChunkName: "club" */ "@/views/Users/BrowseClubs.vue"),
  },

  {
    path: "/club/view/:clubID/:clubName?",
    name: "clubview",
    component: () => import(/* webpackChunkName: "club" */ "@/views/Users/ClubView.vue"),
  },

  {
    path: "/club/:clubID/post/:postID",
    name: "clubpost",
    component: () => import(/* webpackChunkName: "club" */ "@/views/Users/ClubPostView.vue"),
  },
];

export default routes;
