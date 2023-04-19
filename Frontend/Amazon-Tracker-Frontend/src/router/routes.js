import { getAuth, onAuthStateChanged } from "firebase/auth";

const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue")
  },
  {
    path: "/register",
    component: () => import("layouts/RegisterLayout.vue")
  },
  {
    path: "/sign-in",
    component: () => import("layouts/SignIn.vue")
  },
  {
    path: "/account",
    component: () => import("layouts/AccountLayout.vue")
  },
  {
    path: "/search",
    component: () => import("layouts/SearchTracker.vue"),
    meta: {
      requiresAuth: true
    }
  },


  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue")
  }
];


export default routes;
