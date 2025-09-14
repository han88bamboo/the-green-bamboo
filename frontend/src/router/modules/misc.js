const routes = [
  {
    path: "/Latest-News",
    name: "latestNews",
    component: () => import(/* webpackChunkName: "misc" */ "@/views/Users/LatestNews.vue"),
  },
  {
    path: "/best-of",
    name: "bestOf",
    component: () => import(/* webpackChunkName: "misc" */ "@/views/BestOfView.vue"),
  }, 
  {
    path: '/help',
    name: 'help',
     component: () => import(/* webpackChunkName: "misc" */ '@/views/HelpTopics.vue')
  },
  {
    path: '/help/:section',
    name: 'helpSection',
     component: () => import(/* webpackChunkName: "misc" */ '@/views/HelpTopics.vue')
  },
  {
    path: '/badges-and-points',
    name: 'badgesAndPoints',
     component: () => import(/* webpackChunkName: "misc" */ '@/views/BadgesAndPoints.vue')
  }
];

export default routes;