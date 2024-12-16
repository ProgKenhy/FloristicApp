import * as esbuild from 'esbuild';
import copyStaticFiles from 'esbuild-copy-static-files';

let minify = false;
let sourcemap = true;
let watch = true;

if (process.env.NODE_ENV === 'production') {
  minify = true;
  sourcemap = false;
  watch = false;
}

const config = {
  entryPoints: [
    './js/authorization.js',
    './js/chat_support.js',
    './js/generation.js',
    './js/translate.js',
    // Другие файлы JS, если необходимо
  ],
  outdir: '../public/js', // Указываем папку для вывода всех JS файлов
  bundle: true,
  minify: minify,
  sourcemap: sourcemap,
  plugins: [],
};

async function build() {
  if (watch) {
    const context = await esbuild.context({...config, logLevel: 'info'});
    await context.watch();
  } else {
    await esbuild.build(config);
  }
}

build();
