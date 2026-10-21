<script setup>
import { AccountForm } from '../components/index.js'
defineProps({ busy: Boolean, error: String, signupComplete: Boolean })
const emit = defineEmits(['login', 'kakao-login'])
</script>

<template><AccountForm mode="login" :busy="busy" :error="error" :signup-complete="signupComplete" @login="emit('login', $event)" @kakao-login="emit('kakao-login')" /></template>
