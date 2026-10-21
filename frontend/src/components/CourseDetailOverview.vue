<script setup>
defineProps({ instructor: { type: String, default: '' }, facts: { type: Array, default: () => [] }, summary: { type: String, default: '' }, description: { type: String, default: '' }, outcomes: { type: Array, default: () => [] }, lessons: { type: Array, default: () => [] } })
const emit = defineEmits(['select-instructor', 'show-curriculum'])
</script>

<template>
  <section class="detail-overview">
    <div class="overview-main">
      <div class="course-facts"><h2>{{ instructor }} 강사의 강의</h2><p>{{ facts.join(' · ') }}</p></div>
      <button v-if="instructor" class="instructor-row" type="button" @click="emit('select-instructor', instructor)">
        <span class="instructor-avatar">{{ instructor.slice(0,1) }}</span><span><strong>{{ instructor }} 강사</strong><small>수강생의 성장을 돕는 강의자</small></span><span class="instructor-chevron" aria-hidden="true">›</span>
      </button>
      <div v-if="summary || description" class="description"><h3>강의 소개</h3><p v-if="summary" class="summary">{{ summary }}</p><p>{{ description }}</p></div>
      <section v-if="outcomes.length" class="outcomes"><h3>이 강의에서 배울 내용</h3><ul><li v-for="outcome in outcomes" :key="outcome"><span aria-hidden="true">✓</span>{{ outcome }}</li></ul></section>
      <section v-if="lessons.length" class="curriculum"><header><h3>커리큘럼</h3><span>{{ lessons.length }}개 강의</span></header><ol><li v-for="(lesson,index) in lessons.slice(0,5)" :key="lesson.id || lesson.title || lesson"><span>{{ String(index + 1).padStart(2,'0') }}</span>{{ lesson.title || lesson }}</li></ol><button v-if="lessons.length > 5" type="button" @click="emit('show-curriculum')">커리큘럼 모두 보기</button></section>
    </div>
  </section>
</template>

<style scoped>
.detail-overview{--brand:#5d1eb7;max-width:860px;padding:25px 0;border-bottom:1px solid #ece7ef}.course-facts h2{margin:0 0 7px;font-size:18px;letter-spacing:-.035em}.course-facts p{margin:0;color:#716878;font-size:12px}.instructor-row{width:100%;display:flex;align-items:center;gap:13px;margin-top:22px;padding:17px 0;border:0;border-top:1px solid #ece7ef;border-bottom:1px solid #ece7ef;background:white;text-align:left;cursor:pointer}.instructor-avatar{width:45px;height:45px;display:grid;place-items:center;border-radius:50%;background:#eee6f7;color:var(--brand);font-size:17px;font-weight:750}.instructor-row>span:nth-child(2){display:grid;gap:4px}.instructor-row strong{font-size:12px}.instructor-row small{color:#786f7e;font-size:10px}.instructor-chevron{margin-left:auto;font-size:24px}.description,.outcomes,.curriculum{padding:21px 0;border-bottom:1px solid #ece7ef}.description h3,.outcomes h3,.curriculum h3{margin:0 0 13px;font-size:15px}.description p{margin:0;color:#605766;font-size:12px;line-height:1.8;white-space:pre-line}.description .summary{margin-bottom:10px;color:#342c3a;font-weight:650}.outcomes ul{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:0;padding:0;list-style:none}.outcomes li{display:flex;align-items:flex-start;gap:10px;font-size:11px;line-height:1.5}.outcomes li span{color:var(--brand);font-weight:800}.curriculum header{display:flex;align-items:center;justify-content:space-between}.curriculum header h3{margin:0}.curriculum header span{color:#756b7f;font-size:10px}.curriculum ol{display:grid;gap:9px;margin:15px 0;padding:0;list-style:none}.curriculum li{display:flex;gap:12px;color:#5d5563;font-size:11px}.curriculum li span{color:var(--brand);font-weight:750}.curriculum button{padding:10px 13px;border:1px solid #4c4352;border-radius:7px;background:white;color:#38303d;font:inherit;font-size:11px;font-weight:700;cursor:pointer}@media(max-width:600px){.outcomes ul{grid-template-columns:1fr}}
</style>
