// https://nuxt.com/docs/api/configuration/nuxt-config
// const gtmId = process.env.GTM_ID

export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/image',
    '@nuxt/ui',
    '@nuxt/content',
    '@vueuse/nuxt',
    'nuxt-og-image',
    '@nuxt/hints',
    '@nuxt/scripts'
  ],

  // $production: {
  //   app: {
  //     head: {
  //       noscript: gtmId
  //         ? [
  //             {
  //               tagPosition: 'bodyOpen',
  //               innerHTML: `<iframe src="https://www.googletagmanager.com/ns.html?id=${gtmId}" height="0" width="0" style="display:none;visibility:hidden"></iframe>`
  //             }
  //           ]
  //         : []
  //     }
  //   },
  //   scripts: {
  //     defaultScriptOptions: {
  //       trigger: 'server'
  //     },
  //     registry: {
  //       googleTagManager: {
  //         id: gtmId
  //       }
  //     }
  //   }
  // },

  devtools: {
    enabled: true
  },

  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    public: {
      backendBaseUrl: process.env.BACKEND_BASE_URL
    }
  },

  routeRules: {
    '/docs': { redirect: '/docs/getting-started', prerender: false }
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
