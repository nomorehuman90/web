<script setup>
import { CourseDetailGallery, CourseDetailOverview, CoursePurchaseCard } from '../components/index.js'

defineProps({ data: Object, loading: Boolean, error: String, paymentBusy: Boolean, paymentError: String, paymentPending: Boolean })
const emit = defineEmits(['purchase', 'verify-payment'])
</script>

<template>
  <article class="course-detail" aria-label="강의 상세" :aria-busy="loading">
    <div v-if="loading" class="detail-skeleton" role="status" aria-label="강의 불러오는 중"><span class="skeleton detail-kicker-skeleton"></span><span class="skeleton detail-title-skeleton"></span><span class="skeleton detail-rule-skeleton"></span><span class="skeleton detail-line"></span><span class="skeleton detail-line"></span><span class="skeleton detail-line short"></span></div>
    <div v-else-if="error" class="empty-state"><span class="empty-symbol" aria-hidden="true">?</span><h2>강의를 찾을 수 없어요</h2><p role="alert">{{ error }}</p><a class="button button-quiet" href="/courses" data-route>강의 목록으로</a></div>
    <template v-else-if="data">
      <CourseDetailGallery :title="data.title" :image="data.thumbnail_url" :category="data.category || '전체 강의'" :level="data.level || '모든 레벨'">
        <p class="hero-instructor">강사 {{ data.instructor_name || '전문 강사' }}</p>
      </CourseDetailGallery>
      <div class="detail-columns">
        <CourseDetailOverview :instructor="data.instructor_name || '전문'" :facts="[data.category || '전체 강의', data.level || '모든 레벨']" :summary="data.summary" :description="data.description" :outcomes="data.learning_outcomes || []" :lessons="data.lessons || []" />
        <CoursePurchaseCard :price="Number(data.price) || 0" :busy="paymentBusy" :error="paymentError" :pending="paymentPending" @purchase="emit('purchase', data)" @verify-payment="emit('verify-payment')" />
      </div>
      <a class="button button-quiet back-to-list" href="/courses" data-route>강의 목록으로</a>
    </template>
  </article>
</template>

<style scoped>
.course-detail{--brand:#5d1eb7}.hero-instructor{margin:13px 0 0;color:#f5effc;font-size:13px}.detail-columns{display:grid;grid-template-columns:minmax(0,1fr) 300px;align-items:start;gap:50px}.back-to-list{margin-top:25px}@media(max-width:760px){.detail-columns{grid-template-columns:1fr;gap:8px}}
</style>
