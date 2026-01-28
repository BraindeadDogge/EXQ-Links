// https://nuxt.com/docs/api/configuration/nuxt-config
// const gtmId = process.env.GTM_ID

export default defineNuxtConfig({
  modules: ['@nuxt/eslint', '@nuxt/image', '@nuxt/ui', '@nuxt/content', '@vueuse/nuxt', 'nuxt-og-image', '@nuxt/hints', '@nuxt/scripts', '@nuxtjs/seo'],

  devtools: {
    enabled: true
  },

  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    public: {
      backendBaseUrl: process.env.BACKEND_BASE_URL,
      mainUrl: process.env.NUXT_PUBLIC_SITE_URL
    }
  },

  compatibilityDate: '2024-07-11',

  nitro: {
    prerender: {
      routes: [
        '/'
      ],
      crawlLinks: true
    }
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }
})
