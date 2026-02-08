<script setup lang="ts">
const colorMode = useColorMode()

const color = computed(() =>
  colorMode.value === 'dark' ? '#020618' : 'white'
)

useHead({
  meta: [
    { charset: 'utf-8' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { key: 'theme-color', name: 'theme-color', content: color },
    { name: 'google-adsense-account', content: 'ca-pub-5376987682512339' }
  ],
  link: [{ rel: 'icon', href: '/favicon.ico' }],
  htmlAttrs: {
    lang: 'en'
  }
})

const config = useRuntimeConfig()
const siteUrl = config.public.mainUrl || 'https://exq.io'
const ogImageUrl = new URL('/og.png', siteUrl).toString()

// Google Tag Manager with consent defaults for CookieYes CMP (EEA/TCF v2.2)
const gtmId = config.public.gtmId as string | undefined
if (gtmId) {
  useScriptGoogleTagManager({
    id: gtmId,
    onBeforeGtmStart(gtag) {
      // Set all consent signals to denied by default.
      // CookieYes CMP (loaded as a GTM tag) will update these
      // based on user choices and stored preferences.
      gtag('consent', 'default', {
        ad_storage: 'denied',
        ad_user_data: 'denied',
        ad_personalization: 'denied',
        analytics_storage: 'denied',
        functionality_storage: 'denied',
        personalization_storage: 'denied',
        security_storage: 'granted',
        wait_for_update: 500
      })
    }
  })
}

useSeoMeta({
  titleTemplate: '%s - EXQ Links',
  ogImage: ogImageUrl,
  ogImageWidth: 1200,
  ogImageHeight: 630,
  ogImageType: 'image/png',
  twitterImage: ogImageUrl,
  twitterCard: 'summary_large_image'
})
</script>

<template>
  <UApp>
    <NuxtLoadingIndicator />

    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>
