import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://stevankojic.com',
  base: '/stevankojic/',
  vite: {
    ssr: {
      external: ['googleapis']
    }
  }
});
