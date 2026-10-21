import { reactive } from 'vue'

export const catalogStore = reactive({
  query: '',
  category: '',
  setSearch({ query = '', category = '' } = {}) {
    this.query = query
    this.category = category
  },
})
