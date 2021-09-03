import { createRouter, createWebHistory } from "vue-router";
import PaperReading from "@/views/PaperReading.vue";
import PaperBoard from "@/views/PaperBoard.vue";
import About from "@/views/About.vue";

const routes = [
  {
    path: "/",
    name: "paperlist",
    component: PaperBoard,
  },
  {
    path: "/paper/:filename",
    name: "paper",
    component: PaperReading,
    props: true,
  },
  {
    path: "/about",
    name: "about",
    component: About,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
