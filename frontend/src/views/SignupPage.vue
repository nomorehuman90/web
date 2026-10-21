<script setup>
import { AccountForm } from '../components/index.js'
defineProps({ busy: Boolean, error: String })
const emit = defineEmits(['signup', 'kakao-login'])
</script>

<template><AccountForm mode="signup" :busy="busy" :error="error" @signup="emit('signup', $event)" @kakao-login="emit('kakao-login')" /></template>
