<script setup lang="ts">
// Generate QR Code
import type QRCode from 'qrcode'
import { useDebounceFn, useClipboard } from '@vueuse/core'

const { data: page } = await useAsyncData('index', () =>
  queryCollection('index').first()
)
const config = useRuntimeConfig()

const title = page.value?.seo?.title || page.value?.title
const description = page.value?.seo?.description || page.value?.description
const siteUrl = config.public.mainUrl || 'https://exq.io'
const canonicalUrl = new URL('/', siteUrl).toString()

useSeoMeta({
  titleTemplate: '',
  title,
  ogTitle: title,
  description,
  ogDescription: description
})

useSchemaOrg([
  defineWebSite({
    name: 'EXQ Links',
    url: siteUrl
  }),
  defineWebPage({
    name: title,
    description,
    url: canonicalUrl
  })
])

// Shorten url algorithm
const rawLink: Ref<string> = ref('')
const openResults: Ref<boolean> = ref(false)
const shortLink: Ref<string> = ref('')
const isShortening: Ref<boolean> = ref(false)

watch(rawLink, (value) => {
  const sanitized = value.replace(/^https?:\/\//i, '')
  if (sanitized !== value) rawLink.value = sanitized
})

async function shortenURL() {
  if (!rawLink.value.trim()) return

  isShortening.value = true
  try {
    const payload = await $fetch<{
      original_url: string
      short_id: string
      short_url: string
    }>('/shorten', {
      baseURL: config.public.backendBaseUrl,
      params: { url: `https://${rawLink.value}` }
    })
    console.log(payload)

    shortLink.value = payload.short_url
    openResults.value = true
    debouncedRenderQr()
  } catch (error) {
    console.error('Failed to shorten URL', error)
  } finally {
    isShortening.value = false
  }
}
const { copy, copied } = useClipboard()

let QRCodeLib: typeof QRCode | null = null

const fgColor = ref('#000000') // main color ("dark" modules)
const fgColorChip = computed(() => ({ backgroundColor: fgColor.value }))
const bgColor = ref('#ffffff') // background color ("light" modules)
const bgColorChip = computed(() => ({ backgroundColor: bgColor.value }))
const qrCanvas = ref<HTMLCanvasElement | null>(null)

const renderQr = async () => {
  if (!import.meta.client || !qrCanvas.value) return

  try {
    if (!QRCodeLib) {
      const mod = await import('qrcode')
      QRCodeLib = mod.default || mod
    }

    await QRCodeLib.toCanvas(qrCanvas.value, shortLink.value, {
      margin: 2,
      width: 256,
      // scale: 4,
      color: {
        dark: fgColor.value, // main
        light: bgColor.value // background
      }
    })
  } catch (err) {
    console.error('Failed to render QR', err)
  }
}

const debouncedRenderQr = useDebounceFn(renderQr, 150)

// initial render
onMounted(renderQr)

// rerender whenever input or colors change
watch([shortLink, fgColor, bgColor], () => {
  debouncedRenderQr()
})

const downloadQr = () => {
  if (!qrCanvas.value) return
  const link = document.createElement('a')
  link.href = qrCanvas.value.toDataURL('image/png')
  link.download = 'exq_io-links-qr.png' // @todo change file name
  link.click()
}
</script>

<template>
  <div v-if="page">
    <UPageHero
      :title="page.title"
      :description="page.description"
    >
      <template #top>
        <HeroBackground />
      </template>

      <template #title>
        <MDC
          :value="page.title"
          unwrap="p"
        />
      </template>

      <template #links>
        <UInput
          v-model="rawLink"
          placeholder="example.com"
          size="xl"
          :ui="{
            base: 'pl-14.5',
            leading: 'pointer-events-none'
          }"
        >
          <template #leading>
            <p class="text-sm text-muted">
              https://
            </p>
          </template>
        </UInput>

        <UButton
          icon="i-lucide-wand-2"
          size="xl"
          color="primary"
          variant="outline"
          :loading="isShortening"
          @click="shortenURL"
        >
          Shorten
        </UButton>
      </template>
    </UPageHero>

    <UModal
      v-model:open="openResults"
      class="p-5"
    >
      <template #content>
        <ClientOnly>
          <div class="flex md:flex-row flex-col items-center md:items-start justify-between gap-5">
            <div class="h-full flex flex-col md:items-start items-center justify-between gap-5">
              <USeparator label="Short URL" />

              <UInput
                v-model="shortLink"
                :ui="{ trailing: 'pr-0.5' }"
                readonly
                color="primary"
                highlight
              >
                <template
                  v-if="shortLink?.length"
                  #trailing
                >
                  <UTooltip
                    text="Copy to clipboard"
                    :content="{ side: 'right' }"
                  >
                    <UButton
                      :color="copied ? 'success' : 'neutral'"
                      variant="link"
                      size="sm"
                      :icon="copied ? 'i-lucide-copy-check' : 'i-lucide-copy'"
                      aria-label="Copy to clipboard"
                      @click="copy(shortLink)"
                    />
                  </UTooltip>
                </template>
              </UInput>

              <USeparator label="Settings" />

              <UPopover>
                <UButton
                  label="Main color"
                  color="neutral"
                  variant="outline"
                >
                  <template #leading>
                    <span
                      :style="fgColorChip"
                      class="size-3 rounded-full"
                    />
                  </template>
                </UButton>

                <template #content>
                  <UColorPicker
                    v-model="fgColor"
                    class="p-2"
                  />
                </template>
              </UPopover>

              <UPopover>
                <UButton
                  label="Background color"
                  color="neutral"
                  variant="outline"
                >
                  <template #leading>
                    <span
                      :style="bgColorChip"
                      class="size-3 rounded-full"
                    />
                  </template>
                </UButton>

                <template #content>
                  <UColorPicker
                    v-model="bgColor"
                    class="p-2"
                  />
                </template>
              </UPopover>
            </div>
            <div class="h-full flex flex-col md:items-end items-center justify-between gap-5">
              <canvas
                ref="qrCanvas"
                class="rounded-lg"
              />
              <UButton
                trailing-icon="i-lucide-download"
                size="md"
                @click="downloadQr"
              >
                Download
              </UButton>
            </div>
          </div>
        </ClientOnly>
      </template>
    </UModal>

    <UPageSection
      :title="page.features.title"
      :description="page.features.description"
    >
      <UPageGrid>
        <UPageCard
          v-for="(item, index) in page.features.items"
          :key="index"
          v-bind="item"
          spotlight
        >
          <template #leading>
            <UIcon
              :name="item.icon"
              class="size-5 shrink-0 text-primary"
            />
            <UBadge
              v-if="item.upcoming"
              label="Upcoming"
              class="ml-2.5"
            />
          </template>
        </UPageCard>
      </UPageGrid>
    </UPageSection>
  </div>
</template>
