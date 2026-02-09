<template>
  <a :href="`mailto:${email}`">{{ email }}</a>
</template>

<script setup lang="ts">
const { public: { contactEmail: email } } = useRuntimeConfig()
</script>
