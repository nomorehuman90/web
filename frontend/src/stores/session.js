import { reactive } from 'vue'

export const sessionStore = reactive({
  email: '',
  name: '',
  isLoggedIn: false,
  setUser(user = {}) {
    this.email = user.email || ''
    this.name = user.name || ''
    this.isLoggedIn = true
  },
  clear() {
    this.email = ''
    this.name = ''
    this.isLoggedIn = false
  },
})
