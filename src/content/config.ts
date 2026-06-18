import { defineCollection, z } from 'astro:content';

// One markdown file per work in src/content/works/.
// The markdown BODY is the (optional) description text.
// `date` controls ordering on the homepage (newest/topmost = latest date);
// `year` is the label actually shown to visitors.
const works = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    medium: z.string().optional().default(''),
    venue: z.string().optional().default(''),
    location: z.string().optional().default(''),
    year: z.string().optional().default(''),
    date: z.date(),
    link: z.string().optional().default(''),
    video: z.string().optional().default(''), // YouTube video id
    images: z.array(z.string()).optional().default([]),
  }),
});

export const collections = { works };
