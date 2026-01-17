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

const { user, fetchUser } = useAuth()
const isLoggedIn = computed(() => Boolean(user.value))

onMounted(() => {
  if (!user.value) {
    fetchUser()
  }
})
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
      <UColorModeButton />

      <template v-if="isLoggedIn">
        <UBadge
          label="Logged in"
          color="success"
          class="lg:hidden"
        />
        <UBadge
          label="Logged in"
          color="success"
          class="hidden lg:inline-flex"
        />
      </template>
      <template v-else>
        <UButton
          icon="i-lucide-log-in"
          color="neutral"
          variant="ghost"
          to="/login"
          class="lg:hidden"
        />

        <UButton
          label="Sign in"
          color="neutral"
          variant="outline"
          to="/login"
          class="hidden lg:inline-flex"
        />

        <UButton
          label="Sign up"
          color="neutral"
          trailing-icon="i-lucide-arrow-right"
          class="hidden lg:inline-flex"
          to="/signup"
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
          label="Logged in"
          color="success"
          class="mb-3"
        />
      </template>
      <template v-else>
        <UButton
          label="Sign in"
          color="neutral"
          variant="subtle"
          to="/login"
          block
          class="mb-3"
        />
        <UButton
          label="Sign up"
          color="neutral"
          to="/signup"
          block
        />
      </template>
    </template>
  </UHeader>
</template>
