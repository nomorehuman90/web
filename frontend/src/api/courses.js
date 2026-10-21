import { apiRequest } from './client.js'

export async function getCourses(page = 0, pageSize = 20) {
  const result = await apiRequest(`/courses?skip=${page * pageSize}&limit=${pageSize}`)
  return { courses: Array.isArray(result) ? result : [], page }
}

export function getCourse(courseId) {
  return apiRequest(`/courses/${courseId}`)
}
