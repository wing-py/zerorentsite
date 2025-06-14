import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AView from '../views/AView.vue'
import AboutView from '../views/AboutView.vue'
import ChangePasswordView from '../views/ChangePasswordView.vue'
import ComposeView from '../views/ComposeView.vue'
import ContribListView from '../views/ContribListView.vue'
import DisclosureView from '../views/DisclosureView.vue'
import ForumListView from '../views/ForumListView.vue'
import ForumTopicView from '../views/ForumTopicView.vue'
import LetterDetailView from '../views/LetterDetailView.vue'
import LinkView from '../views/LinkView.vue'
import ListOrderView from '../views/ListOrderView.vue'
import ListWorkerView from '../views/ListWorkerView.vue'
import LoginView from '../views/LoginView.vue'
import LogoutView from '../views/LogoutView.vue'
import MailboxView from '../views/MailboxView.vue'
import ProductView from '../views/ProductView.vue'
import ProfileView from '../views/ProfileView.vue'
import RegisterView from '../views/RegisterView.vue'
import SearchResultsView from '../views/SearchResultsView.vue'
import SubmitOrderView from '../views/SubmitOrderView.vue'
import SupportView from '../views/SupportView.vue' // Import SupportView

type routerType={
    history: any,
    routes:{
        path:string,
        name:string,
        component:any,
    }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/a',
      name: 'a',
      component: AView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/change-password',
      name: 'change-password',
      component: ChangePasswordView
    },
    {
      path: '/compose',
      name: 'compose',
      component: ComposeView
    },
    {
      path: '/contrib-list',
      name: 'contrib-list',
      component: ContribListView
    },
    {
      path: '/disclosure',
      name: 'disclosure',
      component: DisclosureView
    },
    {
      path: '/forum',
      name: 'forum',
      component: ForumListView
    },
    {
      path: '/forum/topic/:id',
      name: 'forum-topic',
      component: ForumTopicView,
      props: true
    },
    {
      path: '/mailbox/:letterId',
      name: 'letter-detail',
      component: LetterDetailView,
      props: true
    },
    {
      path: '/link',
      name: 'link',
      component: LinkView
    },
    {
      path: '/list-order',
      name: 'list-order',
      component: ListOrderView
    },
    {
      path: '/list-worker',
      name: 'list-worker',
      component: ListWorkerView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView
    },
    {
      path: '/mailbox',
      name: 'mailbox',
      component: MailboxView
    },
    {
      path: '/product',
      name: 'product',
      component: ProductView
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/search',
      name: 'search-results',
      component: SearchResultsView
    },
    {
      path: '/submit-order',
      name: 'submit-order',
      component: SubmitOrderView
    },
    { // Add route for SupportView
      path: '/support',
      name: 'support',
      component: SupportView
    }
  ]
})

export default router