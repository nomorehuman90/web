<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import LoginPage from './views/LoginPage.vue'
import SignupPage from './views/SignupPage.vue'
import CourseListPage from './views/CourseListPage.vue'
import CourseDetailPage from './views/CourseDetailPage.vue'
import { LearningHeader, LearningFooter } from './components/index.js'
import { login, loginWithKakao, signup } from './api/auth.js'
import { getCourse, getCourses } from './api/courses.js'
import { completeCoursePayment, prepareCoursePayment } from './api/payments.js'
import { resolveRoute } from './router/index.js'
import { catalogStore } from './stores/catalog.js'
import { sessionStore } from './stores/session.js'

const PORTONE_STORE_ID = import.meta.env.VITE_PORTONE_STORE_ID || ''
const PORTONE_CHANNEL_KEY = import.meta.env.VITE_PORTONE_CHANNEL_KEY || ''
const KAKAO_JS_KEY = import.meta.env.VITE_KAKAO_JS_KEY || ''
const KAKAO_REDIRECT_URI = import.meta.env.VITE_KAKAO_REDIRECT_URI || `${window.location.origin}/login`
const path = ref(window.location.pathname)
const search = ref(window.location.search)
const pageData = ref(null)
const loading = ref(true)
const error = ref('')
const busy = ref(false)
const notice = ref('')
const paymentBusy = ref(false)
const paymentError = ref('')
const pendingPaymentId = ref('')
const pendingPaymentCourseId = ref(null)
const route = computed(() => resolveRoute(path.value))

const activePage = computed(() => ({
  login: LoginPage,
  signup: SignupPage,
  detail: CourseDetailPage,
  list: CourseListPage,
}[route.value.name]))

const pageTitle = computed(() => ({
  login: '로그인', signup: '회원가입', detail: '강의 상세', list: '강의 목록',
}[route.value.name]))
const signupComplete = computed(() => new URLSearchParams(search.value).get('created') === '1')

watch(pageTitle, async (title) => {
  document.title = `${title} — 배움길`
  await nextTick()
  document.querySelector('.page-heading h1')?.focus({ preventScroll: true })
}, { immediate: true })

function readLocation() {
  path.value = window.location.pathname
  search.value = window.location.search
}

async function navigate(destination, { replace = false } = {}) {
  const url = new URL(destination, window.location.origin)
  if (url.pathname === path.value && url.search === search.value) return
  if (replace) window.history.replaceState({}, '', `${url.pathname}${url.search}`)
  else window.history.pushState({}, '', `${url.pathname}${url.search}`)
  path.value = url.pathname
  search.value = url.search
  pageData.value = null
  error.value = ''
  notice.value = ''
  paymentError.value = ''
  await loadRoute()
  const behavior = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'
  window.scrollTo({ top: 0, behavior })
}

async function loadRoute() {
  const current = route.value
  pageData.value = null
  error.value = ''
  if (current.name !== 'list' && current.name !== 'detail') {
    loading.value = false
    return
  }

  loading.value = true
  try {
    if (current.name === 'list') {
      const page = Math.max(0, Number(new URLSearchParams(search.value).get('page')) || 0)
      pageData.value = await getCourses(page)
    } else {
      pageData.value = await getCourse(current.id)
    }
  } catch (cause) {
    error.value = current.name === 'list'
      ? `${cause.message} 백엔드가 실행 중인지 확인해 주세요.`
      : cause.message
  } finally {
    loading.value = false
  }
}

async function submitLogin(credentials) {
  busy.value = true
  error.value = ''
  try {
    const result = await login(credentials)
    sessionStore.setUser(result)
    notice.value = '로그인했습니다.'
    await navigate('/courses')
    notice.value = '로그인했습니다.'
  } catch (cause) {
    error.value = cause.message
  } finally {
    busy.value = false
  }
}

function startKakaoLogin() {
  const Kakao = window.Kakao
  if (!KAKAO_JS_KEY || !Kakao) {
    error.value = '카카오 로그인 설정을 확인해 주세요.'
    return
  }
  if (!Kakao.isInitialized()) Kakao.init(KAKAO_JS_KEY)
  const state = crypto.randomUUID()
  sessionStorage.setItem('kakao_login_state', state)
  Kakao.Auth.authorize({
    redirectUri: KAKAO_REDIRECT_URI,
    scope: 'profile_nickname',
    state,
  })
}

async function finishKakaoLogin(code) {
  window.history.replaceState({}, '', '/login')
  search.value = ''
  busy.value = true
  error.value = ''
  try {
    const result = await loginWithKakao(code)
    sessionStore.setUser(result)
    await navigate('/courses')
    notice.value = '카카오 계정으로 로그인했습니다.'
  } catch (cause) {
    error.value = cause.message
  } finally {
    busy.value = false
  }
}
async function submitSignup(details) {
  busy.value = true
  error.value = ''
  try {
    await signup(details)
    await navigate('/login?created=1')
  } catch (cause) {
    error.value = cause.message
  } finally {
    busy.value = false
  }
}

async function completePayment(paymentId) {
  const result = await completeCoursePayment(paymentId)
  pendingPaymentId.value = ''
  pendingPaymentCourseId.value = null
  notice.value = `${result.course_title} 결제가 완료되었습니다.`
  paymentError.value = ''
}

async function retryPaymentVerification() {
  if (!pendingPaymentId.value || paymentBusy.value) return
  paymentBusy.value = true
  try {
    await completePayment(pendingPaymentId.value)
  } catch (cause) {
    paymentError.value = cause.message || '결제 상태를 확인하지 못했습니다. 잠시 후 다시 시도해 주세요.'
  } finally {
    paymentBusy.value = false
  }
}

async function purchaseCourse(course) {
  paymentError.value = ''
  if (!PORTONE_STORE_ID || !PORTONE_CHANNEL_KEY) {
    paymentError.value = '결제 설정이 완료되지 않았습니다. 서비스 관리자에게 문의해 주세요.'
    return
  }

  paymentBusy.value = true
  try {
    const order = await prepareCoursePayment(course.id)
    if (!window.PortOne?.requestPayment) throw new Error('결제 모듈을 불러오지 못했습니다. 페이지를 새로고침해 주세요.')
    const result = await window.PortOne.requestPayment({
      storeId: PORTONE_STORE_ID,
      channelKey: PORTONE_CHANNEL_KEY,
      paymentId: order.payment_id,
      orderName: order.order_name,
      totalAmount: order.total_amount,
      currency: 'KRW',
      payMethod: 'CARD',
      redirectUrl: `${window.location.origin}/courses/${course.id}?paymentReturn=1`,
      customer: sessionStore.email ? { email: sessionStore.email } : undefined,
    })

    if (!result) return
    if (result.code) throw new Error(result.message || '결제가 취소되었거나 완료되지 않았습니다.')
    if (!result.paymentId) throw new Error('결제 결과를 확인하지 못했습니다. 다시 시도해 주세요.')
    if (result.paymentId !== order.payment_id) throw new Error('결제 주문 정보가 일치하지 않습니다.')
    pendingPaymentId.value = result.paymentId
    pendingPaymentCourseId.value = course.id
    await completePayment(result.paymentId)
  } catch (cause) {
    paymentError.value = cause.message || '결제를 시작하지 못했습니다. 잠시 후 다시 시도해 주세요.'
  } finally {
    paymentBusy.value = false
  }
}

async function finishPortOneRedirect(query) {
  const paymentId = query.get('paymentId')
  if (!paymentId) return false

  if (query.get('code')) {
    window.history.replaceState({}, '', path.value)
    search.value = ''
    paymentError.value = query.get('message') || '결제가 완료되지 않았습니다. 다시 시도해 주세요.'
    return true
  }

  pendingPaymentId.value = paymentId
  pendingPaymentCourseId.value = route.value.id
  paymentBusy.value = true
  try {
    await completePayment(paymentId)
    window.history.replaceState({}, '', path.value)
    search.value = ''
  } catch (cause) {
    paymentError.value = cause.message || '결제 결과를 확인하지 못했습니다.'
  } finally {
    paymentBusy.value = false
  }
  return true
}

function changePage(nextPage) {
  navigate(`/courses?page=${Math.max(0, nextPage)}`)
}

function applyCatalogSearch(filters) {
  catalogStore.setSearch(filters)
  if (route.value.name !== 'list') navigate('/courses')
}

function openCourse(course) {
  navigate(`/courses/${course.id}`)
}

function handleClick(event) {
  const anchor = event.target.closest('a[data-route]')
  if (!anchor || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return
  event.preventDefault()
  navigate(anchor.getAttribute('href'))
}

onMounted(() => {
  window.addEventListener('popstate', readLocation)
  window.addEventListener('popstate', loadRoute)
  const query = new URLSearchParams(window.location.search)
  const code = query.get('code')
  if (path.value.startsWith('/courses/') && query.has('paymentReturn')) {
    loadRoute()
    if (query.has('paymentId')) {
      finishPortOneRedirect(query)
    } else if (query.has('code')) {
      window.history.replaceState({}, '', path.value)
      search.value = ''
      paymentError.value = query.get('message') || '결제가 완료되지 않았습니다. 다시 시도해 주세요.'
    }
    return
  }
  if (path.value === '/login' && code) {
    const expectedState = sessionStorage.getItem('kakao_login_state')
    sessionStorage.removeItem('kakao_login_state')
    if (expectedState && expectedState === query.get('state')) {
      finishKakaoLogin(code)
    } else {
      error.value = '카카오 로그인 요청을 확인할 수 없습니다. 다시 시도해 주세요.'
      window.history.replaceState({}, '', '/login')
      search.value = ''
      loadRoute()
    }
  } else {
    if (path.value === '/login' && query.has('error')) {
      sessionStorage.removeItem('kakao_login_state')
      error.value = '카카오 로그인이 취소되었거나 승인되지 않았습니다.'
      window.history.replaceState({}, '', '/login')
      search.value = ''
    }
    loadRoute()
  }
})
</script>

<template>
  <div class="site-frame" @click="handleClick">
    <a class="skip-link" href="#main-content">본문으로 건너뛰기</a>
    <LearningHeader :show-search="route.name === 'list'" :signed-in="sessionStore.isLoggedIn" :account-label="sessionStore.email || sessionStore.name" :current="['list', 'detail'].includes(route.name) ? 'courses' : ''" @search="applyCatalogSearch" />

    <main id="main-content" class="page-wrap">
      <div v-if="route.name === 'list'" class="page-heading">
        <div>
          <p class="page-context">배우고 싶은 마음이 길이 되도록</p>
          <h1 tabindex="-1">{{ pageTitle }}</h1>
        </div>
        <span class="catalog-note">나에게 맞는 배움을 찾아보세요</span>
      </div>

      <p v-if="notice" class="feedback feedback-success" role="status" aria-live="polite">{{ notice }}</p>
      <Transition name="page" mode="out-in">
        <component
          :is="activePage"
          :key="`${route.name}-${route.id || ''}-${search}`"
          :route="route"
          :data="pageData"
          :loading="loading"
          :busy="busy"
          :error="error"
          :payment-busy="paymentBusy"
          :payment-error="paymentError"
          :payment-pending="Boolean(pendingPaymentId && route.id === pendingPaymentCourseId)"
          :signup-complete="signupComplete"
          :query="catalogStore.query"
          :searched-category="catalogStore.category"
          @login="submitLogin"
          @kakao-login="startKakaoLogin"
          @signup="submitSignup"
          @purchase="purchaseCourse"
          @verify-payment="retryPaymentVerification"
          @change-page="changePage"
          @open-course="openCourse"
          @search-category="catalogStore.category = $event"
        />
      </Transition>
    </main>

    <LearningFooter />
  </div>
</template>
