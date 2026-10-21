import { apiRequest } from './client.js'

export function prepareCoursePayment(courseId) {
  return apiRequest('/payments/prepare', {
    method: 'POST',
    body: JSON.stringify({ course_id: courseId }),
  })
}

export function completeCoursePayment(paymentId) {
  return apiRequest('/payments/complete', {
    method: 'POST',
    body: JSON.stringify({ payment_id: paymentId }),
  })
}
