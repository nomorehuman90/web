<script setup>
import { reactive } from 'vue'
const props = defineProps({ mode: { type: String, required: true }, busy: Boolean, error: { type: String, default: '' }, signupComplete: Boolean })
const emit = defineEmits(['login', 'signup', 'kakao-login'])
const form = reactive({ name: '', email: '', password: '' })
function submit() { emit(props.mode === 'signup' ? 'signup' : 'login', { ...form }) }
</script>

<template>
  <section class="account-page" :aria-labelledby="`account-title-${mode}`">
    <div class="account-story"><span class="story-mark" aria-hidden="true">✦</span><p class="eyebrow">배움길에서 더 멀리</p><h1>{{ mode === 'signup' ? '배움의 첫걸음을 시작해 보세요' : '배움을 이어가세요' }}</h1><p>{{ mode === 'signup' ? '관심 있는 강의를 모으고, 나만의 속도로 성장해요.' : '저장한 강의와 학습 기록이 기다리고 있어요.' }}</p></div>
    <div class="form-column">
      <form class="account-form" @submit.prevent="submit">
        <p v-if="signupComplete" class="success" role="status">계정을 만들었습니다. 로그인해 주세요.</p>
        <h2 :id="`account-title-${mode}`">{{ mode === 'signup' ? '회원가입' : '로그인' }}</h2>
        <p class="intro">{{ mode === 'signup' ? '필수 정보를 입력해 계정을 만들어 주세요.' : '계정 정보로 로그인해 학습을 계속하세요.' }}</p>
        <p v-if="error" class="error" role="alert">{{ error }}</p>
        <label v-if="mode === 'signup'" for="account-name">이름</label><input v-if="mode === 'signup'" id="account-name" v-model="form.name" name="name" autocomplete="name" placeholder="이름을 입력하세요" required />
        <label for="account-email">이메일</label><input id="account-email" v-model="form.email" name="email" type="email" autocomplete="email" spellcheck="false" placeholder="name@example.com" required />
        <label for="account-password">비밀번호</label><input id="account-password" v-model="form.password" name="password" type="password" :autocomplete="mode === 'signup' ? 'new-password' : 'current-password'" placeholder="비밀번호를 입력하세요" required />
        <button class="primary" type="submit" :disabled="busy">{{ busy ? '처리 중…' : mode === 'signup' ? '계정 만들기' : '로그인' }}</button>
        <div class="divider"><span>또는</span></div>
        <button class="social" type="button" :disabled="busy" @click="emit('kakao-login')"><span aria-hidden="true">K</span>카카오로 계속하기</button>
        <p class="switch-copy">{{ mode === 'signup' ? '이미 계정이 있나요?' : '처음이신가요?' }} <a :href="mode === 'signup' ? '/login' : '/signup'" data-route>{{ mode === 'signup' ? '로그인' : '회원가입' }}</a></p>
      </form>
      <p class="legal">계속 진행하면 서비스 이용약관과 개인정보 처리방침에 동의하게 됩니다.</p>
    </div>
  </section>
</template>

<style scoped>
.account-page{--brand:#5d1eb7;display:grid;grid-template-columns:1fr minmax(320px,440px);align-items:center;gap:clamp(30px,8vw,120px);max-width:1000px;min-height:560px;margin:0 auto}.account-story{max-width:440px;padding:30px 0}.story-mark{display:grid;width:52px;height:52px;place-items:center;border-radius:15px;background:#f0e9f8;color:var(--brand);font-size:25px}.eyebrow{margin:30px 0 10px;color:var(--brand);font-size:10px;font-weight:800;letter-spacing:.14em}.account-story h1{margin:0;color:#302638;font-size:clamp(30px,4.3vw,48px);line-height:1.2;letter-spacing:-.06em}.account-story>p:last-child{max-width:340px;color:#756d7c;font-size:13px;line-height:1.8}.form-column{width:100%}.account-form{padding:clamp(23px,4vw,38px);border:1px solid #eee8f2;border-radius:17px;background:white;box-shadow:0 15px 45px #30164a10}.account-form h2{margin:0 0 7px;font-size:22px;letter-spacing:-.045em}.intro{margin:0 0 22px;color:#746b7b;font-size:11px}.account-form label{display:block;margin:15px 0 7px;color:#514958;font-size:11px;font-weight:700}.account-form input{width:100%;height:46px;padding:0 13px;border:1px solid #ded6e4;border-radius:7px;color:#302638;font:inherit;font-size:12px}.account-form input:focus{outline:2px solid #5d1eb744;border-color:var(--brand)}.primary,.social{width:100%;height:46px;border-radius:7px;font:inherit;font-size:12px;font-weight:750;cursor:pointer}.primary{margin-top:18px;border:0;background:var(--brand);color:white}.primary:hover{background:#47118f}.primary:disabled{opacity:.6}.divider{display:flex;align-items:center;gap:12px;margin:18px 0;color:#837b89;font-size:10px}.divider:before,.divider:after{height:1px;flex:1;background:#eee8f1;content:''}.social{position:relative;border:1px solid #dcd5e1;background:white;color:#342c3b}.social span{position:absolute;left:16px;color:var(--brand);font-weight:800}.switch-copy{text-align:center;margin:18px 0 0;color:#6f6677;font-size:11px}.switch-copy a{margin-left:4px;color:var(--brand);font-weight:750}.legal{text-align:center;color:#908894;font-size:9px;line-height:1.7}.error,.success{padding:10px;border-radius:6px;font-size:11px}.error{background:#fff0f1;color:#a82b44}.success{background:#f1ebf8;color:#57219f}@media(max-width:700px){.account-page{grid-template-columns:1fr;gap:8px;min-height:0}.account-story{padding:20px 0 0}.story-mark{width:42px;height:42px}.eyebrow{margin-top:18px}.account-story h1{font-size:29px}.account-story>p:last-child{margin-bottom:10px}.account-form{box-shadow:none}}
</style>
