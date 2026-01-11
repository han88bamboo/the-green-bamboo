const routes = [
  {
    path: "/assemblies",
    name: "browseAssemblies",
    component: () => import(/* webpackChunkName: "assembly" */ "@/views/BrowseAssemblies.vue"),
  },

  {
    path: "/assemblies/create",
    name: "createAssembly",
    component: () => import(/* webpackChunkName: "assembly" */ "@/views/CreateAssembly.vue"),
  },

  {
    path: "/assemblies/:assemblyId/:assemblyName",
    name: "specificAssembly",
    component: () => import(/* webpackChunkName: "assembly" */ "@/views/SpecificAssembly.vue"),
  },

  {
    path: "/assemblies/:assemblyId/:assemblyName/assembly-post/:postId/:postTitle",
    name: "specificAssemblyPost",
    component: () => import(/* webpackChunkName: "assembly" */ "@/views/SpecificAssemblyPost.vue"),
  },
];

export default routes;
