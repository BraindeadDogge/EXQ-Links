import { defineCollection, z } from '@nuxt/content'

const _variantEnum = z.enum(['solid', 'outline', 'subtle', 'soft', 'ghost', 'link'])
const _colorEnum = z.enum(['primary', 'secondary', 'neutral', 'error', 'warning', 'success', 'info'])
const _sizeEnum = z.enum(['xs', 'sm', 'md', 'lg', 'xl'])

const createBaseSchema = () => z.object({
  title: z.string().nonempty(),
  description: z.string().nonempty()
})

const createFeatureItemSchema = () => createBaseSchema().extend({
  icon: z.string().nonempty().editor({ input: 'icon' }),
  upcoming: z.boolean().optional()
})

const createLegalPageSchema = () => z.object({
  effectiveDate: z.string().nonempty(),
  lastUpdated: z.string().nonempty()
})

export const collections = {
  index: defineCollection({
    source: '0.index.yml',
    type: 'page',
    schema: z.object({
      features: createBaseSchema().extend({
        items: z.array(createFeatureItemSchema())
      })
    })
  }),
  cookie: defineCollection({
    source: '1.cookie.md',
    type: 'page',
    schema: createLegalPageSchema()
  }),
  privacy: defineCollection({
    source: '2.privacy.md',
    type: 'page',
    schema: createLegalPageSchema()
  }),
  terms: defineCollection({
    source: '3.terms.md',
    type: 'page',
    schema: createLegalPageSchema()
  })
}
