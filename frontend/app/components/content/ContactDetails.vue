<template>
  <span>{{ config.contactCompany }}, {{ address }}, email: <a :href="`mailto:${config.contactEmail}`">{{ config.contactEmail }}</a><template v-if="phone">, phone: {{ config.contactPhone }}</template></span>
</template>

<script setup lang="ts">
const props = defineProps<{
  phone?: boolean
  grievance?: boolean
}>()

const { public: config } = useRuntimeConfig()
const address = props.grievance ? config.contactGrievanceAddress : config.contactAddress
const phone = props.phone
</script>
