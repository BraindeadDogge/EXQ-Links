// https://nuxt.com/docs/api/configuration/nuxt-config
// const gtmId = process.env.GTM_ID

const siteUrl = process.env.NUXT_PUBLIC_SITE_URL || 'https://exq.io'

export default defineNuxtConfig({
  modules: ['@nuxt/eslint', '@nuxt/image', '@nuxt/ui', '@nuxt/content', '@vueuse/nuxt', 'nuxt-og-image', '@nuxt/hints', '@nuxt/scripts', '@nuxtjs/seo'],

  devtools: {
    enabled: true
  },

  css: ['~/assets/css/main.css'],

  site: {
    url: siteUrl,
    name: 'EXQ Links - Short URLs & QR Codes in One Click',
    defaultLocale: 'en'
  },

  runtimeConfig: {
    public: {
      backendBaseUrl: process.env.BACKEND_BASE_URL,
      mainUrl: siteUrl
    }
  },

  compatibilityDate: '2024-07-11',

  nitro: {
    prerender: {
      routes: [
        '/', '/sitemap.xml'
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
  },

  schemaOrg: {
    identity: {
      type: 'Organization',
      name: 'EXQ Links',
      url: siteUrl
    }
  },

  sitemap: {
    zeroRuntime: true // @audit-info untill i add some CMS
  }
})
