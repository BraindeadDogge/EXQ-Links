<script setup lang="ts">
const { data: page } = await useAsyncData('privacy', () =>
  queryCollection('privacy').first()
)

if (!page.value) {
  throw createError({ statusCode: 404, statusMessage: 'Page not found', fatal: true })
}

const title = page.value.seo?.title || page.value.title
const description = page.value.seo?.description || page.value.description

useSeoMeta({
  title,
  ogTitle: title,
  description,
  ogDescription: description
})
</script>

<template>
  <UContainer class="py-12">
    <UPageHeader
      :title="page!.title"
      :description="`Effective date: ${page!.effectiveDate} · Last updated: ${page!.lastUpdated}`"
    />

    <UPageBody class="prose dark:prose-invert max-w-none">
      <ContentRenderer :value="page!" />
    </UPageBody>
  </UContainer>
</template>
