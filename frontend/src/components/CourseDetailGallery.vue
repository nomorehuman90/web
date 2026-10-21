<script setup>
defineProps({ title: { type: String, required: true }, image: { type: String, default: '' }, category: { type: String, default: '' }, level: { type: String, default: '' } })
</script>

<template>
  <section class="course-hero" :aria-label="`${title} 강의 소개`">
    <img v-if="image" :src="image" :alt="`${title} 강의`" />
    <div v-else class="hero-placeholder" aria-hidden="true">✦</div>
    <div class="hero-shade"></div><div class="hero-copy"><p>{{ category }}<span v-if="category && level"> · </span>{{ level }}</p><h1>{{ title }}</h1><slot /></div>
  </section>
</template>

<style scoped>
.course-hero{--brand:#5d1eb7;position:relative;display:flex;align-items:flex-end;min-height:clamp(280px,42vw,470px);overflow:hidden;border-radius:20px;background:linear-gradient(135deg,#261545,#6c45a1 55%,#c2a8e5);color:white}.course-hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.hero-placeholder{position:absolute;inset:0;display:grid;place-items:center;color:#ffffff55;font-size:140px}.hero-shade{position:absolute;inset:0;background:linear-gradient(90deg,#170f25c9,transparent 100%),linear-gradient(0deg,#170f2599,transparent 65%)}.hero-copy{position:relative;max-width:760px;padding:clamp(24px,5vw,54px)}.hero-copy p{margin:0 0 13px;color:#e8dcf7;font-size:12px;font-weight:650}.hero-copy h1{margin:0;font-size:clamp(27px,4.4vw,48px);line-height:1.2;letter-spacing:-.055em}@media(max-width:600px){.course-hero{min-height:310px;border-radius:14px}}
</style>
