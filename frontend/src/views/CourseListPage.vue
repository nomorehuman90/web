<script setup>
import { computed, ref, watch } from 'vue'
import { CourseCategoryNav, CourseSection } from '../components/index.js'

const props = defineProps({ data: Object, loading: Boolean, error: String, query: { type: String, default: '' }, searchedCategory: { type: String, default: '' } })
const emit = defineEmits(['change-page', 'open-course', 'search-category'])
const selectedCategory = ref('전체 강의')
watch(() => props.searchedCategory, category => { selectedCategory.value = category || '전체 강의' })
const categories = computed(() => ['전체 강의', ...new Set((props.data?.courses || []).map(course => course.category).filter(Boolean))])
const visibleCourses = computed(() => (props.data?.courses || []).filter(course => {
  const query = props.query.trim().toLocaleLowerCase()
  const matchesQuery = !query || [course.title, course.summary, course.instructor_name, course.category].some(value => value?.toLocaleLowerCase().includes(query))
  const matchesCategory = selectedCategory.value === '전체 강의' || course.category === selectedCategory.value
  return matchesQuery && matchesCategory
}))
function selectCategory(category) { selectedCategory.value = category; emit('search-category', category) }
</script>

<template>
  <section class="course-catalog" aria-labelledby="list-title" :aria-busy="loading">
    <div class="list-intro"><div><h2 id="list-title">오늘 시작할 수 있는 배움</h2><p>관심 있는 분야의 강의를 골라 나만의 속도로 배워 보세요.</p></div><span v-if="!loading && data" class="record-count">{{ visibleCourses.length }}개 강의</span><span v-else class="skeleton count-skeleton" aria-hidden="true"></span></div>
    <CourseCategoryNav :items="categories" :model-value="selectedCategory" @update:model-value="selectCategory" />
    <div v-if="loading" class="course-grid-skeleton" role="status" aria-label="강의 목록 불러오는 중"><div v-for="item in 6" :key="item" class="course-skeleton"><span class="skeleton course-skeleton-image"></span><span class="skeleton course-skeleton-title"></span><span class="skeleton course-skeleton-meta"></span></div></div>
    <div v-else-if="error" class="empty-state"><span class="empty-symbol" aria-hidden="true">!</span><h3>강의를 불러오지 못했어요</h3><p role="alert">{{ error }} 새로고침해 다시 시도해 주세요.</p></div>
    <CourseSection v-else-if="visibleCourses.length" title="지금 인기 있는 강의" :courses="visibleCourses" layout="grid" @select="emit('open-course', $event)" />
    <div v-else class="empty-state"><span class="empty-symbol" aria-hidden="true">⌁</span><h3>{{ query ? '검색 결과가 없어요' : '아직 등록된 강의가 없어요' }}</h3><p>{{ query ? '검색어나 분야를 바꿔 다시 찾아보세요.' : '새로운 강의가 준비되면 이곳에서 만나볼 수 있어요.' }}</p></div>
    <nav v-if="!loading && data" class="pager" aria-label="강의 페이지"><button type="button" :disabled="data.page === 0" @click="emit('change-page', data.page - 1)">이전</button><span>{{ data.page + 1 }}</span><button type="button" :disabled="data.courses.length < 20" @click="emit('change-page', data.page + 1)">다음</button></nav>
  </section>
</template>
