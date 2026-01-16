<script setup lang="ts">
const config = useRuntimeConfig()
const toast = useToast()

const email = ref('')
const loading = ref(false)

async function onSubmit() {
  if (!email.value.trim()) {
    toast.add({
      title: 'Email required',
      description: 'Please enter an email address.',
      color: 'error'
    })
    return
  }

  loading.value = true

  try {
    const payload = await $fetch<{
      email: string
      subscribed: boolean
      is_new: boolean
      message?: string
    }>('/newsletter/subscribe', {
      baseURL: config.public.backendBaseUrl,
      method: 'POST',
      body: {
        email: email.value
      }
    })

    toast.add({
      title: payload.message || 'You are on the list.'
    })
    email.value = ''
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (error: any) {
    const message
      = error?.data?.error || 'Failed to subscribe. Please try again.'
    toast.add({
      title: 'Subscription failed',
      description: message,
      color: 'error'
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <USeparator
    icon="i-lucide-mail"
    class="h-px"
  />

  <UFooter :ui="{ top: 'border-b border-default' }">
    <template #top>
      <UContainer>
        <form @submit.prevent="onSubmit">
          <UFormField
            name="email"
            label="Subscribe to our newsletter"
            size="lg"
          >
            <UInput
              v-model="email"
              type="email"
              class="w-full"
              placeholder="Enter your email"
            >
              <template #trailing>
                <UButton
                  type="submit"
                  size="xs"
                  color="neutral"
                  label="Subscribe"
                  :loading="loading"
                />
              </template>
            </UInput>
          </UFormField>
        </form>
      </UContainer>
    </template>
  </UFooter>
</template>
