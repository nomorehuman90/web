<script setup>
import { computed } from 'vue'
const props = defineProps({ price: { type: Number, default: 0 }, busy: Boolean, error: { type: String, default: '' }, pending: Boolean, buttonLabel: { type: String, default: '' } })
const emit = defineEmits(['purchase', 'verify-payment'])
const priceLabel = computed(() => new Intl.NumberFormat('ko-KR').format(props.price || 0))
</script>

<template>
  <aside class="purchase-card" aria-label="강의 구매">
    <p class="purchase-kicker">한 번 구매하고 언제든 다시 수강하세요</p>
    <p class="price"><strong>{{ priceLabel }}</strong><span>원</span></p>
    <ul><li>평생 수강 가능</li><li>모바일·PC 어디서나 학습</li><li>강의 자료 제공</li></ul>
    <button class="purchase-button" type="button" :disabled="busy || price <= 0" @click="emit('purchase')">{{ busy ? '결제창을 준비하고 있어요…' : buttonLabel || (price > 0 ? '강의 구매하기' : '무료 강의') }}</button>
    <p v-if="error" class="purchase-error" role="alert">{{ error }}</p>
    <button v-if="pending && !busy" class="verify" type="button" @click="emit('verify-payment')">결제 상태 다시 확인</button>
    <p class="purchase-note">구매 후 바로 학습을 시작할 수 있어요.</p>
  </aside>
</template>

<style scoped>
.purchase-card{--brand:#5d1eb7;position:sticky;top:24px;padding:22px;border:1px solid #e7e0ed;border-radius:16px;background:white;box-shadow:0 10px 30px #28133b0d}.purchase-kicker{margin:0;color:#62596a;font-size:11px}.price{display:flex;align-items:baseline;gap:4px;margin:10px 0 18px;color:#302638}.price strong{font-size:28px;letter-spacing:-.05em}.price span{font-size:12px}.purchase-card ul{display:grid;gap:11px;margin:0 0 20px;padding:17px 0;border-top:1px solid #eee9f1;border-bottom:1px solid #eee9f1;list-style:none}.purchase-card li{font-size:11px;color:#514958}.purchase-card li:before{margin-right:9px;color:var(--brand);content:'✓';font-weight:800}.purchase-button{width:100%;min-height:47px;border:0;border-radius:8px;background:var(--brand);color:white;font:inherit;font-size:13px;font-weight:750;cursor:pointer}.purchase-button:hover{background:#47118f}.purchase-button:disabled{opacity:.55;cursor:not-allowed}.purchase-error{padding:10px;border-radius:6px;background:#fff0f1;color:#a82b44;font-size:10px;line-height:1.5}.verify{width:100%;padding:10px;border:1px solid #5d1eb7;border-radius:7px;background:white;color:#5d1eb7;font:inherit;font-size:11px;cursor:pointer}.purchase-note{text-align:center;color:#857d8b;font-size:9px}@media(max-width:760px){.purchase-card{position:static}}
</style>
