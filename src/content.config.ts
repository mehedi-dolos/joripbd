import { defineCollection, z } from 'astro:content';
import { glob, file } from 'astro/loaders';

/* One Markdown file per service line. Body = long intro. */
const services = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/services' }),
  schema: z.object({
    title: z.string(),
    order: z.number(),
    icon: z.string(),
    promise: z.string(),
    summary: z.string(),
    covers: z.array(z.string()),
    receive: z.array(z.string()),
    appointedBy: z.array(z.string()),
    turnaround: z.string().optional(),
    steps: z.array(z.object({ title: z.string(), text: z.string() })).optional(),
    heroImage: z.string().optional(),
    heroAlt: z.string().optional(),
  }),
});

/* One Markdown file per person. Body = bio. */
const people = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/people' }),
  schema: z.object({
    name: z.string(),
    role: z.string(),
    group: z.enum(['board', 'adviser', 'management', 'surveyor', 'staff']),
    order: z.number(),
    line: z.string().optional(),
    phone: z.string().optional(),
    photo: z.string().optional(),
    placeholder: z.boolean().default(false),
  }),
});

/* Clients live in one JSON list so the editor sees a single table. */
const clients = defineCollection({
  loader: file('./src/data/clients.json'),
  schema: z.object({
    id: z.string(),
    name: z.string(),
    type: z.enum(['bank', 'nbfi', 'insurer']),
    logo: z.string(),
    confirmed: z.boolean().default(true),
    featured: z.boolean().default(false),
  }),
});

const assignments = defineCollection({
  loader: file('./src/data/assignments.json'),
  schema: z.object({
    id: z.string(),
    title: z.string(),
    location: z.string(),
    propertyType: z.string(),
    service: z.string(),
    photo: z.string(),
  }),
});

export const collections = { services, people, clients, assignments };
