export type AuthUser = {
  id: number
  email: string
  created_at: string
  last_login_at: string | null
}

type AuthResponse = { user: AuthUser }

export function useAuth() {
  const user = useState<AuthUser | null>('auth-user', () => null)
  const pending = useState<boolean>('auth-pending', () => false)
  const config = useRuntimeConfig()

  const fetchUser = async () => {
    if (pending.value) return
    pending.value = true
    try {
      const response = await $fetch<AuthResponse>('/auth/me', {
        baseURL: config.public.backendBaseUrl,
        credentials: 'include',
        headers: import.meta.server ? useRequestHeaders(['cookie']) : undefined
      })
      user.value = response.user
    } catch (error) {
      user.value = null
    } finally {
      pending.value = false
    }
  }

  const setUser = (value: AuthUser | null) => {
    user.value = value
  }

  const logout = async () => {
    try {
      await $fetch('/auth/logout', {
        baseURL: config.public.backendBaseUrl,
        method: 'POST',
        credentials: 'include',
        headers: import.meta.server ? useRequestHeaders(['cookie']) : undefined
      })
    } finally {
      user.value = null
    }
  }

  return {
    user,
    pending,
    fetchUser,
    setUser,
    logout
  }
}
