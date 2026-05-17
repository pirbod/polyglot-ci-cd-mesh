export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#111827',
        cloud: '#f5f7fb',
        line: '#d8dee9',
        success: '#17663a',
        warning: '#9a5b00',
        danger: '#b42318',
        action: '#1f6feb',
      },
      boxShadow: {
        panel: '0 18px 50px rgba(15, 23, 42, 0.08)',
      },
    },
  },
  plugins: [],
};
