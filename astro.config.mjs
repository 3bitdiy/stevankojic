import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://stevankojic.com',
  vite: {
    ssr: {
      external: ['googleapis']
    }
  }
});
