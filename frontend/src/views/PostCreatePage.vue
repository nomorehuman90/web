<script setup>
import { reactive } from 'vue'

defineProps({ busy: Boolean, error: String })
const emit = defineEmits(['create-post'])
const draft = reactive({ title: '', contents: '' })
</script>

<template>
  <section class="create-page" aria-labelledby="create-title">
    <div class="create-aside">
      <div class="paper-glyph" aria-hidden="true"><span></span><span></span><span></span></div>
      <p class="auth-kicker">비워 둔 한 칸</p>
      <h2>천천히 적어도<br />괜찮아요.</h2>
      <p>제목과 내용을 적고 기록을 남겨 보세요.</p>
    </div>
    <form class="form-sheet create-sheet" @submit.prevent="emit('create-post', { title: draft.title.trim(), contents: draft.contents.trim() })">
      <h2 id="create-title">새 글 쓰기</h2>
      <p class="form-intro">기록은 게시글 목록에 바로 추가됩니다.</p>
      <p v-if="error" class="form-error" role="alert">{{ error }}</p>
      <label for="post-title">제목</label>
      <input id="post-title" v-model="draft.title" name="title" maxlength="120" autocomplete="off" placeholder="이야기를 담을 제목…" required />
      <label for="post-content">내용</label>
      <textarea id="post-content" v-model="draft.contents" name="contents" rows="10" autocomplete="off" placeholder="지금 떠오르는 생각을 적어 보세요…" required></textarea>
      <div class="form-actions">
        <a class="button button-quiet" href="/posts" data-route>취소</a>
        <button class="button button-accent" type="submit" :disabled="busy">{{ busy ? '등록 중…' : '게시글 등록' }}</button>
      </div>
    </form>
  </section>
</template>
