<script setup lang="ts">
// const route = useRoute()

// const items = computed(() => [{
//   label: 'Docs',
//   to: '/docs',
//   active: route.path.startsWith('/docs')
// }, {
//   label: 'Pricing',
//   to: '/pricing'
// }, {
//   label: 'Blog',
//   to: '/blog'
// }, {
//   label: 'Changelog',
//   to: '/changelog'
// }])

import { authClient } from '~/lib/auth-client'

const session = authClient.useSession()
const isLoggedIn = computed(() => Boolean(session.value.data?.user))
const isSigningOut = ref(false)

const onSignOut = async () => {
  if (isSigningOut.value) return
  isSigningOut.value = true
  try {
    await authClient.signOut()
    await session.value.refetch?.()
  } finally {
    isSigningOut.value = false
  }
}
</script>

<template>
  <UHeader title="EXQ Links">
    <!-- <template #left>
      <NuxtLink to="/">
        <AppLogo class="w-auto h-6 shrink-0" />
      </NuxtLink>
    </template> -->

    <!-- <UNavigationMenu
      :items="items"
      variant="link"
    /> -->

    <template #right>
      <ColorModeButton />

      <template v-if="isLoggedIn">
        <UBadge
          label="Signed in"
          color="success"
          class="hidden lg:inline-flex h-8"
        />
        <UButton
          label="Sign out"
          color="neutral"
          variant="outline"
          class="hidden lg:inline-flex"
          :loading="isSigningOut"
          @click="onSignOut"
        />
      </template>
      <template v-else>
        <UButton
          label="Sign in"
          color="neutral"
          variant="outline"
          to="/login"
          class="hidden lg:inline-flex"
        />
      </template>
    </template>

    <template #body>
      <!-- <UNavigationMenu
        :items="items"
        orientation="vertical"
        class="-mx-2.5"
      /> -->

      <!-- <USeparator class="my-6" /> -->

      <template v-if="isLoggedIn">
        <UBadge
          label="Signed in"
          color="success"
          class="mb-3 h-8 w-full justify-center"
        />
        <UButton
          label="Sign out"
          color="neutral"
          variant="subtle"
          block
          :loading="isSigningOut"
          @click="onSignOut"
        />
      </template>
      <template v-else>
        <UButton
          label="Sign in"
          color="neutral"
          variant="subtle"
          to="/login"
          block
        />
      </template>
    </template>
  </UHeader>
</template>
