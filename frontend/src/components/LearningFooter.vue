<script setup>
defineProps({ brandName: { type: String, default: '배움길' }, tagline: { type: String, default: '배우고 싶은 마음이 길이 되도록' }, columns: { type: Array, default: () => [
  { title: '강의 찾기 NEW', links: ['전체 강의', '개발', '디자인'] },
  { title: '강사', links: ['강사 소개', '강의 제안', '커뮤니티'] },
  { title: '도움말', links: ['고객 지원', '자주 묻는 질문', '이용약관'] },
] } })
</script>

<template>
  <footer class="learning-footer"><div class="footer-columns"><section v-for="column in columns" :key="column.title"><h2>{{ column.title }}</h2><a v-for="link in column.links" :key="link" href="#">{{ link }}</a></section></div><div class="footer-bottom"><span>© 2026 {{ brandName }}</span><nav aria-label="정책"><a href="#">개인정보 처리방침</a><a href="#">이용약관</a><a href="#">사이트맵</a></nav><span>{{ tagline }}</span></div></footer>
</template>

<style scoped>
.learning-footer{--brand:#5d1eb7;margin-top:55px;padding:35px max(22px,calc((100% - 1180px)/2));background:#f6f3f8;color:#4b4351}.footer-columns{display:grid;grid-template-columns:repeat(3,1fr);gap:25px;padding-bottom:30px}.footer-columns section{display:grid;align-content:start;gap:13px}.footer-columns h2{margin:0 0 3px;color:#332c39;font-size:12px}.footer-columns a,.footer-bottom a{color:inherit;font-size:10px;text-decoration:none}.footer-columns a:hover,.footer-bottom a:hover{color:var(--brand);text-decoration:underline}.footer-bottom{display:flex;align-items:center;justify-content:space-between;gap:15px;padding-top:17px;border-top:1px solid #e5dfe9;font-size:10px}.footer-bottom nav{display:flex;gap:15px}@media(max-width:600px){.footer-bottom{align-items:flex-start;flex-direction:column}.footer-bottom nav{flex-wrap:wrap}}
</style>
