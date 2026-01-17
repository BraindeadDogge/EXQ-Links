<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'
import type { AuthUser } from '~/composables/useAuth'

definePageMeta({
  layout: 'auth'
})

useSeoMeta({
  title: 'Login',
  description: 'Login to your account to continue'
})

const toast = useToast()
const config = useRuntimeConfig()
const { setUser } = useAuth()

const fields = [{
  name: 'email',
  type: 'text' as const,
  label: 'Email',
  placeholder: 'Enter your email',
  required: true
}, {
  name: 'password',
  label: 'Password',
  type: 'password' as const,
  placeholder: 'Enter your password'
}, {
  name: 'remember',
  label: 'Remember me',
  type: 'checkbox' as const
}]

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Must be at least 8 characters'),
  remember: z.boolean().optional()
})

type Schema = z.output<typeof schema>

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  try {
    const response = await $fetch<{ user: AuthUser }>('/auth/login', {
      baseURL: config.public.backendBaseUrl,
      method: 'POST',
      credentials: 'include',
      body: {
        email: payload.data.email,
        password: payload.data.password,
        remember: payload.data.remember
      }
    })

    setUser(response.user)
    toast.add({
      title: 'Welcome back',
      description: response.user.email
    })
    await navigateTo('/')
  } catch (error: unknown) {
    const err = error as { data?: { error?: string } }
    const message = err?.data?.error || 'Login failed. Please try again.'
    toast.add({
      title: 'Login failed',
      description: message,
      color: 'error'
    })
  }
}
</script>

<template>
  <UAuthForm
    :fields="fields"
    :schema="schema"
    title="Welcome back"
    icon="i-lucide-lock"
    @submit="onSubmit"
  >
    <template #description>
      Don't have an account? <ULink
        to="/signup"
        class="text-primary font-medium"
      >Sign up</ULink>.
    </template>

    <template #password-hint>
      <ULink
        to="/"
        class="text-primary font-medium"
        tabindex="-1"
      >Forgot password?</ULink>
    </template>

    <template #footer>
      By signing in, you agree to our <ULink
        to="/"
        class="text-primary font-medium"
      >Terms of Service</ULink>.
    </template>
  </UAuthForm>
</template>
