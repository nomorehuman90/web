<script setup>
import { ref } from 'vue'
import CourseCard from './CourseCard.vue'
defineProps({ title: { type: String, required: true }, courses: { type: Array, default: () => [] }, moreLabel: { type: String, default: '전체 보기' }, layout: { type: String, default: 'rail' } })
const emit = defineEmits(['select', 'more'])
const rail = ref(null)
function move(direction) { rail.value?.scrollBy({ left: direction * Math.max(rail.value.clientWidth * .78, 260), behavior: 'smooth' }) }
</script>

<template>
  <section class="course-section">
    <header><div><h2>{{ title }}</h2><slot name="description" /></div><div class="actions"><button type="button" @click="emit('more')">{{ moreLabel }} <span aria-hidden="true">›</span></button><template v-if="layout === 'rail'"><button class="arrow" type="button" aria-label="이전 강의" @click="move(-1)">‹</button><button class="arrow" type="button" aria-label="다음 강의" @click="move(1)">›</button></template></div></header>
    <div ref="rail" class="course-rail" :class="`layout-${layout}`"><CourseCard v-for="course in courses" :key="course.id || course.title" :course="course" @select="emit('select', $event)" /></div>
  </section>
</template>

<style scoped>
.course-section{--brand:#5d1eb7;margin:25px 0 46px}header{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-bottom:17px}h2{margin:0;font-size:20px;letter-spacing:-.04em}.actions{display:flex;align-items:center;gap:8px}.actions>button:first-child{margin-right:8px;border:0;background:transparent;color:#463950;font:inherit;font-size:12px;font-weight:700;cursor:pointer}.arrow{width:31px;height:31px;border:1px solid #e4dfe8;border-radius:50%;background:white;color:#393140;font-size:20px;cursor:pointer}.arrow:hover{border-color:var(--brand);color:var(--brand)}.course-rail{display:grid;gap:20px}.layout-rail{grid-auto-columns:minmax(185px,1fr);grid-auto-flow:column;overflow:auto;scrollbar-width:none;scroll-snap-type:x mandatory}.layout-rail::-webkit-scrollbar{display:none}.layout-rail>*{scroll-snap-align:start}.layout-grid{grid-template-columns:repeat(3,minmax(0,1fr))}@media(max-width:760px){.layout-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:560px){.layout-rail{grid-auto-columns:minmax(68%,1fr)}.layout-grid{grid-template-columns:1fr}h2{font-size:17px}.actions>button:first-child{display:none}}
</style>
