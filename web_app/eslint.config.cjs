const js = require('@eslint/js');
const react = require('eslint-plugin-react');

module.exports = [
  js.configs.recommended,
  {
    files: ['**/*.js', '**/*.jsx'],
    languageOptions: {
      parserOptions: {
        ecmaVersion: 2020,
        sourceType: 'module',
        ecmaFeatures: { jsx: true },
      },
      globals: {
        jest: 'readonly',
        window: 'readonly',
        document: 'readonly',
        localStorage: 'readonly',
        console: 'readonly',
        process: 'readonly',
        module: 'writable',
        require: 'readonly',
        File: 'readonly',
        FileReader: 'readonly',
        Storage: 'readonly',
        fetch: 'readonly',
      },
    },
    plugins: {
      react,
    },
    rules: {
      quotes: ['error', 'single'],
      semi: ['error', 'always'],
      'no-unused-vars': 'off',
      'react/prop-types': 'off',
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
  },
  {
    files: ['web_app/cypress/**/*.js', 'web_app/cypress.config.js'],
    languageOptions: {
      globals: {
        describe: 'readonly',
        it: 'readonly',
        cy: 'readonly',
        beforeEach: 'readonly',
        afterEach: 'readonly',
        expect: 'readonly',
        on: 'readonly',
        config: 'readonly',
      },
    },
  },
  {
    files: ['**/*.test.js', 'web_app/src/setupTests.js'],
    languageOptions: {
      globals: {
        describe: 'readonly',
        it: 'readonly',
        test: 'readonly',
        expect: 'readonly',
        beforeEach: 'readonly',
        beforeAll: 'readonly',
        afterEach: 'readonly',
        jest: 'readonly',
        File: 'readonly',
        FileReader: 'readonly',
        Storage: 'readonly',
        global: 'readonly',
      },
    },
  },
];
