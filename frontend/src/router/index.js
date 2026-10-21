export function resolveRoute(pathname) {
  if (pathname === '/login') return { name: 'login' }
  if (pathname === '/signup') return { name: 'signup' }
  const courseDetail = pathname.match(/^\/courses\/(\d+)$/)
  if (courseDetail) return { name: 'detail', id: Number(courseDetail[1]) }
  if (pathname === '/' || pathname === '/posts' || pathname === '/courses') return { name: 'list' }
  return { name: 'list' }
}

export const routes = [
  { name: 'list', path: '/courses' },
  { name: 'detail', path: '/courses/:id' },
  { name: 'login', path: '/login' },
  { name: 'signup', path: '/signup' },
]
