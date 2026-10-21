<script setup>
import { reactive } from 'vue'

const emit = defineEmits(['search'])
const form = reactive({ query: '', category: '' })
function submit() { emit('search', { ...form }) }
</script>

<template>
  <form class="course-search" role="search" @submit.prevent="submit">
    <label class="search-field destination"><span>강의 검색</span><input v-model.trim="form.query" placeholder="배우고 싶은 내용을 검색하세요" autocomplete="off" /></label>
    <label class="search-field category"><span>분야</span><select v-model="form.category"><option value="">모든 분야</option><option>개발</option><option>디자인</option><option>비즈니스</option><option>마케팅</option></select></label>
    <button class="search-submit" type="submit" aria-label="강의 검색"><span aria-hidden="true">⌕</span><span class="submit-label">검색</span></button>
  </form>
</template>

<style scoped>
.course-search{--brand:#5d1eb7;display:flex;align-items:center;gap:0;width:100%;max-width:670px;min-height:58px;margin:auto;padding:6px;border:1px solid #e5e1e9;border-radius:999px;background:#fff;box-shadow:0 7px 25px #27183912}.search-field{min-width:0;flex:1;display:grid;gap:4px;padding:5px 16px;border-right:1px solid #e9e5ed}.search-field span{font-size:10px;font-weight:750;color:#2b2532}.search-field input,.search-field select{width:100%;min-width:0;border:0;outline:0;background:transparent;color:#514a59;font:inherit;font-size:11px}.destination{flex:1.6}.category{flex:1;border:0}.search-submit{width:43px;height:43px;flex:none;border:0;border-radius:50%;background:var(--brand);color:white;font-size:24px;cursor:pointer}.search-submit:hover{background:#47118f}.submit-label{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}
@media(max-width:620px){.course-search{min-height:52px;padding:5px}.search-field{padding:5px 9px}.category{display:none}.search-submit{width:40px;height:40px}}
</style>
