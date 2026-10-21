<script setup>
defineProps({ items: { type: Array, default: () => ['전체 강의', '개발', '디자인', '비즈니스', '마케팅', '데이터', '커리어'] }, modelValue: { type: String, default: '' } })
const emit = defineEmits(['update:modelValue', 'select'])
function choose(item) { emit('update:modelValue', item); emit('select', item) }
</script>

<template>
  <nav class="category-nav" aria-label="강의 분야">
    <button v-for="(item, index) in items" :key="item" type="button" class="category" :class="{ active: modelValue === item || (!modelValue && index === 0) }" :aria-pressed="modelValue === item || (!modelValue && index === 0)" @click="choose(item)">
      <span class="category-icon" aria-hidden="true">{{ ['✦','⌘','◈','↗','◉','⌁','⌖'][index % 7] }}</span><span>{{ item }}</span>
    </button>
  </nav>
</template>

<style scoped>
.category-nav{--brand:#5d1eb7;display:flex;gap:30px;overflow:auto;border-bottom:1px solid #eeeaf1;scrollbar-width:none}.category-nav::-webkit-scrollbar{display:none}.category{position:relative;min-width:60px;display:grid;justify-items:center;gap:9px;padding:12px 1px 14px;border:0;background:none;color:#79727f;font:inherit;font-size:11px;white-space:nowrap;cursor:pointer}.category:hover,.category.active{color:#30263a}.category.active{font-weight:700}.category.active:after{position:absolute;right:0;bottom:-1px;left:0;height:2px;background:var(--brand);content:''}.category-icon{font-size:20px;line-height:1}
</style>
