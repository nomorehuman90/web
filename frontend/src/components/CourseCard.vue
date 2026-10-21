<script setup>
defineProps({ course: { type: Object, required: true } })
const emit = defineEmits(['select'])
</script>

<template>
  <article class="catalog-course-card">
    <button class="cover" type="button" :aria-label="`${course.title} 상세 보기`" @click="emit('select', course)">
      <img v-if="course.thumbnail_url" :src="course.thumbnail_url" :alt="course.title" loading="lazy" />
      <span v-else class="image-placeholder" aria-hidden="true">{{ course.emoji || '✦' }}</span>
      <span v-if="course.category" class="badge">{{ course.category }}</span>
    </button>
    <a class="course-copy" :href="`/courses/${course.id}`" data-route @click.prevent="emit('select', course)">
      <div class="title-line"><h3>{{ course.title }}</h3><span v-if="course.level" class="rating">{{ course.level }}</span></div>
      <p>{{ course.instructor_name || '전문 강사' }}</p>
      <p v-if="course.summary" class="summary">{{ course.summary }}</p>
      <p class="price"><strong>{{ new Intl.NumberFormat('ko-KR').format(course.price || 0) }}원</strong><span> · 평생 수강</span></p>
    </a>
  </article>
</template>

<style scoped>
.catalog-course-card{--brand:#5d1eb7;position:relative;min-width:0}.cover{position:relative;width:100%;aspect-ratio:1.45/1;border:0;border-radius:14px;overflow:hidden;background:linear-gradient(145deg,#e9dff3,#cbb9e1 55%,#aa8bca);cursor:pointer}.cover img{width:100%;height:100%;object-fit:cover;transition:transform .35s}.cover:hover img{transform:scale(1.035)}.image-placeholder{display:grid;width:100%;height:100%;place-items:center;color:#fff8;font-size:76px}.badge{position:absolute;top:12px;left:12px;padding:7px 10px;border-radius:999px;background:#fff;color:#332b3a;font-size:10px;font-weight:750}.course-copy{display:block;width:100%;padding:12px 0 0;color:inherit;text-align:left;text-decoration:none;cursor:pointer}.title-line{display:flex;align-items:baseline;justify-content:space-between;gap:8px}.title-line h3{margin:0;overflow:hidden;font-size:14px;font-weight:750;text-overflow:ellipsis;white-space:nowrap}.rating{flex:none;color:#756b7f;font-size:10px}.course-copy p{margin:5px 0 0;color:#77717c;font:inherit;font-size:11px}.course-copy .summary{display:-webkit-box;min-height:32px;overflow:hidden;-webkit-line-clamp:2;-webkit-box-orient:vertical;line-height:1.5}.course-copy .price{margin-top:10px;color:#342d3a}.price strong{font-size:13px}.price span{color:#77717c}
</style>
