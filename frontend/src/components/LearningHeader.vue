<script setup>
import CourseSearchBar from './CourseSearchBar.vue'
defineProps({ showSearch: Boolean, signedIn: Boolean, accountLabel: { type: String, default: '' }, current: { type: String, default: '' }, brandName: { type: String, default: '배움길' } })
const emit = defineEmits(['search'])
</script>

<template>
  <header class="learning-header">
    <a class="learning-brand" href="/courses" data-route :aria-label="`${brandName} 강의 목록`"><span class="learning-mark" aria-hidden="true">✳</span><span>{{ brandName }}</span></a>
    <CourseSearchBar v-if="showSearch" class="search" @search="emit('search', $event)" />
    <nav class="header-actions" aria-label="계정 메뉴"><a class="browse" href="/courses" data-route :aria-current="current === 'courses' ? 'page' : undefined">강의 둘러보기</a><span v-if="signedIn" class="account-label">{{ accountLabel }}</span><a v-else href="/login" data-route>로그인</a><a v-if="!signedIn" class="join" href="/signup" data-route>회원가입</a></nav>
  </header>
</template>

<style scoped>
.learning-header{--brand:#5d1eb7;position:relative;display:grid;grid-template-columns:1fr minmax(300px,1.45fr) 1fr;align-items:center;gap:20px;min-height:88px;border-bottom:1px solid #eeeaf1}.learning-brand{display:flex;align-items:center;gap:9px;width:max-content;color:var(--brand);font-size:16px;font-weight:800;letter-spacing:-.05em;text-decoration:none}.learning-mark{display:grid;width:32px;height:32px;place-items:center;border-radius:50%;background:#f1eafb;color:var(--brand);font-size:20px}.header-actions{display:flex;align-items:center;justify-content:flex-end;gap:16px;white-space:nowrap}.header-actions a{color:#4e4655;font-size:11px;text-decoration:none}.header-actions a:hover{color:var(--brand)}.header-actions .join{padding:9px 12px;border:1px solid #ded6e4;border-radius:999px;color:var(--brand);font-weight:750}.account-label{max-width:120px;overflow:hidden;color:#6d6474;font-size:10px;text-overflow:ellipsis}@media(max-width:780px){.learning-header{grid-template-columns:1fr auto;gap:12px;padding:13px 0}.learning-brand{grid-column:1;grid-row:1}.header-actions{grid-column:2;grid-row:1;gap:10px}.search{grid-column:1/-1;grid-row:2}}
</style>
