<script setup lang="ts">
import * as z from 'zod'
import type { AuthFormField, FormSubmitEvent, ButtonProps } from '@nuxt/ui'
import { authClient } from '~/lib/auth-client'

definePageMeta({
  layout: 'auth'
})

useSeoMeta({
  title: 'Login',
  description: 'Login to your account to continue',
  robots: 'noindex, follow'
})

const toast = useToast()

const step = ref<'email' | 'otp'>('email')
const emailState = reactive({
  email: ''
})

const emailSchema = z.object({
  email: z.email('Invalid email')
})

type EmailSchema = z.output<typeof emailSchema>

const otpSchema = z.object({
  otp: z
    .array(z.string(), 'Enter the 6-digit code')
    .length(6, 'Enter the 6-digit code')
})

type OtpSchema = z.output<typeof otpSchema>

const isSending = ref(false)
const isVerifying = ref(false)
const isGoogleLoading = ref(false)

const emailFields: AuthFormField[] = [
  {
    name: 'email',
    type: 'email',
    label: 'Email',
    placeholder: 'you@example.com',
    autocomplete: 'email',
    autofocus: true,
    required: true
  }
]

const otpFields: AuthFormField[] = [
  {
    name: 'otp',
    type: 'otp',
    label: 'One-time code',
    length: 6,
    size: 'lg',
    autofocus: true,
    required: true
  }
]

const providers: ComputedRef<ButtonProps[]> = computed(() => [
  {
    label: 'Continue with Google',
    icon: 'i-simple-icons-google',
    color: 'neutral',
    variant: 'outline',
    block: true,
    loading: isGoogleLoading.value,
    onClick: onGoogleSignIn
  }
])

const emailSubmit = computed(() => ({
  label: 'Send code',
  block: true,
  loading: isSending.value
}))

const otpSubmit = computed(() => ({
  label: 'Verify and sign in',
  block: true,
  loading: isVerifying.value
}))

const onEmailSubmit = async (event: FormSubmitEvent<EmailSchema>) => {
  emailState.email = event.data.email
  await requestOtp(event.data.email)
}

const requestOtp = async (email: string) => {
  if (!email) {
    toast.add({
      title: 'Email required',
      description: 'Please enter a valid email address.',
      color: 'error'
    })
    return
  }
  if (isSending.value) return
  isSending.value = true
  const { error } = await authClient.emailOtp.sendVerificationOtp({
    email,
    type: 'sign-in'
  })

  if (error) {
    toast.add({
      title: 'Unable to send code',
      description: error.message || 'Please try again.',
      color: 'error'
    })
  } else {
    step.value = 'otp'
    toast.add({
      title: 'Code sent',
      description: `We sent a one-time code to ${email}`
    })
  }
  isSending.value = false
}

const onOtpSubmit = async (event: FormSubmitEvent<OtpSchema>) => {
  if (!emailState.email) {
    step.value = 'email'
    toast.add({
      title: 'Enter your email',
      description: 'We need your email to verify the code.',
      color: 'error'
    })
    return
  }

  if (isVerifying.value) return
  isVerifying.value = true
  const { error } = await authClient.signIn.emailOtp({
    email: emailState.email,
    otp: event.data.otp.join('')
  })
  if (error) {
    toast.add({
      title: 'Invalid code',
      description: error.message || 'Please try again.',
      color: 'error'
    })
  } else {
    toast.add({
      title: 'Signed in',
      description: emailState.email
    })
    await navigateTo('/')
  }
  isVerifying.value = false
}

const onGoogleSignIn = async () => {
  if (isGoogleLoading.value) return
  isGoogleLoading.value = true
  try {
    await authClient.signIn.social({
      provider: 'google',
      callbackURL: '/'
    })
  } finally {
    isGoogleLoading.value = false
  }
}

const switchEmail = () => {
  step.value = 'email'
}
</script>

<template>
  <UAuthForm
    v-if="step === 'email'"
    :fields="emailFields"
    :schema="emailSchema"
    :providers="providers"
    :submit="emailSubmit"
    title="Passwordless sign in to EXQ Links"
    icon="i-lucide-lock"
    @submit="onEmailSubmit"
  >
    <template #description>
      Use Google or request a one-time code.
    </template>

    <!-- <template #footer> @todo temp
      By signing in, you agree to our
      <ULink to="/" class="text-primary font-medium">Terms of Service</ULink>.
    </template> -->
  </UAuthForm>

  <UAuthForm
    v-else
    :fields="otpFields"
    :schema="otpSchema"
    :submit="otpSubmit"
    :validate-on="[]"
    title="Check your inbox"
    icon="i-lucide-mail-check"
    :ui="{
      otp: 'justify-between',
      footer: 'flex flex-col md:flex-row gap-2'
    }"
    @submit="onOtpSubmit"
  >
    <template #description>
      We sent a 6-digit code to {{ emailState.email }}
    </template>

    <template #footer>
      <UButton
        color="neutral"
        variant="ghost"
        block
        @click="switchEmail"
      >
        Use a different email
      </UButton>
      <UButton
        color="neutral"
        variant="link"
        block
        :loading="isSending"
        @click="requestOtp(emailState.email)"
      >
        Resend code
      </UButton>
    </template>
  </UAuthForm>
</template>
