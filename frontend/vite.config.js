import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte({
    compilerOptions: {
      compatibility: {
        componentApi: 4  // Svelte 4 호환성 모드 활성화
      }
    }
  })],
  server: {
    port: 9001, // 원하는 포트 번호로 변경
    proxy: {
      '/api': 'http://localhost:9000', // 백엔드 API 주소 설정
    },
  },
});
