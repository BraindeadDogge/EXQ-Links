<script setup lang="ts">
// const columns = [{
//   label: 'Resources',
//   children: [{
//     label: 'Help center'
//   }, {
//     label: 'Docs'
//   }, {
//     label: 'Roadmap'
//   }, {
//     label: 'Changelog'
//   }]
// }, {
//   label: 'Features',
//   children: [{
//     label: 'Affiliates'
//   }, {
//     label: 'Portal'
//   }, {
//     label: 'Jobs'
//   }, {
//     label: 'Sponsors'
//   }]
// }, {
//   label: 'Company',
//   children: [{
//     label: 'About'
//   }, {
//     label: 'Pricing'
//   }, {
//     label: 'Careers'
//   }, {
//     label: 'Blog'
//   }]
// }]

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
      // title: payload.is_new ? 'Subscribed!' : 'Already subscribed',
    })
    email.value = ''
  } catch (error: any) {
    const message = error?.data?.error || 'Failed to subscribe. Please try again.'
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
    icon="i-simple-icons-nuxtdotjs"
    class="h-px"
  />

  <UFooter :ui="{ top: 'border-b border-default' }">
    <template #top>
      <UContainer>
        <!-- <UFooterColumns :columns="columns"> -->
        <!-- <UFooterColumns> -->
          <!-- <template #right> -->
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
          <!-- </template> -->
        <!-- </UFooterColumns> -->
      </UContainer>
    </template>
<!-- 
    <template #left>
      <p class="text-muted text-sm">
        Built with Nuxt UI • © {{ new Date().getFullYear() }}
      </p>
    </template>

    <template #right>
      <UButton
        to="https://go.nuxt.com/discord"
        target="_blank"
        icon="i-simple-icons-discord"
        aria-label="Nuxt on Discord"
        color="neutral"
        variant="ghost"
      />
      <UButton
        to="https://go.nuxt.com/x"
        target="_blank"
        icon="i-simple-icons-x"
        aria-label="Nuxt on X"
        color="neutral"
        variant="ghost"
      />
      <UButton
        to="https://github.com/nuxt-ui-templates/saas"
        target="_blank"
        icon="i-simple-icons-github"
        aria-label="Nuxt UI on GitHub"
        color="neutral"
        variant="ghost"
      />
    </template> -->
  </UFooter>
</template>
