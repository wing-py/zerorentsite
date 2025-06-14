import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'

import naive, { createDiscreteApi } from 'naive-ui'

// const { message, dialog, notification, loadingBar } = createDiscreteApi(
//   ['message', 'dialog', 'notification', 'loadingBar']
// )

const app = createApp(App)

app.use(router)
app.use(naive)


// app.config.globalProperties.$message = message
// app.config.globalProperties.$dialog = dialog
// app.config.globalProperties.$notification = notification
// app.config.globalProperties.$loadingBar = loadingBar

app.mount('#app')