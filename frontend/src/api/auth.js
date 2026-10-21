import { apiRequest } from './client.js'

export function login(credentials) {
  return apiRequest('/user/login', { method: 'POST', body: JSON.stringify(credentials) })
}

export function loginWithKakao(code) {
  return apiRequest('/user/kakao/login', { method: 'POST', body: JSON.stringify({ code }) })
}

export function signup(details) {
  return apiRequest('/user/signup', { method: 'POST', body: JSON.stringify(details) })
}
