// https://nuxt.com/docs/api/configuration/nuxt-config
const siteUrl = process.env.FRONTEND_BASE_URL || 'https://exq.io'

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
      mainUrl: siteUrl,
      gtmId: process.env.GTM_ID,
      contactCompany: process.env.CONTACT_COMPANY || 'EXQ Links',
      contactAddress: process.env.CONTACT_ADDRESS,
      contactGrievanceAddress: process.env.CONTACT_GRIEVANCE_ADDRESS,
      contactEmail: process.env.CONTACT_EMAIL,
      contactPhone: process.env.CONTACT_PHONE
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
