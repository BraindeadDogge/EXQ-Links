<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'
import type { AuthUser } from '~/composables/useAuth'

definePageMeta({
  layout: 'auth'
})

useSeoMeta({
  title: 'Sign up',
  description: 'Create an account to get started'
})

const toast = useToast()
const config = useRuntimeConfig()
const { setUser } = useAuth()

const fields = [{
  name: 'email',
  type: 'text' as const,
  label: 'Email',
  placeholder: 'Enter your email'
}, {
  name: 'password',
  label: 'Password',
  type: 'password' as const,
  placeholder: 'Enter your password'
}]

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Must be at least 8 characters')
})

type Schema = z.output<typeof schema>

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  try {
    const response = await $fetch<{ user: AuthUser }>('/auth/register', {
      baseURL: config.public.backendBaseUrl,
      method: 'POST',
      credentials: 'include',
      body: {
        email: payload.data.email,
        password: payload.data.password
      }
    })

    setUser(response.user)
    toast.add({
      title: 'Account created',
      description: response.user.email
    })
    await navigateTo('/')
  } catch (error: unknown) {
    const err = error as { data?: { error?: string } }
    const message = err?.data?.error || 'Signup failed. Please try again.'
    toast.add({
      title: 'Signup failed',
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
    title="Create an account"
    :submit="{ label: 'Create account' }"
    @submit="onSubmit"
  >
    <template #description>
      Already have an account? <ULink
        to="/login"
        class="text-primary font-medium"
      >Login</ULink>.
    </template>

    <template #footer>
      By signing up, you agree to our <ULink
        to="/"
        class="text-primary font-medium"
      >Terms of Service</ULink>.
    </template>
  </UAuthForm>
</template>
