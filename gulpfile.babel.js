var gulp = require("gulp"),
  clean = require("gulp-clean"),
  rev = require("gulp-rev"),
  concat = require("gulp-concat"),
  sass = require("gulp-sass"),
  fingerprint = require("gulp-fingerprint"),
  reactify = require("reactify"),
  streamify = require('gulp-streamify'),
  gulpif = require("gulp-if"),
  argv = require("yargs").argv,
  production = !!(argv.production); // true if --production: ie. gulp prod --production
var autoprefixer = require('autoprefixer');
var browserify = require('browserify');
var watchify = require('watchify');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var eslint = require('gulp-eslint');
var babelify = require('babelify');
var uglify = require('gulp-uglify');
var rimraf = require('rimraf');
var notify = require('gulp-notify');
var sourcemaps = require('gulp-sourcemaps');
var postcss = require('gulp-postcss');
var nested = require('postcss-nested');
var vars = require('postcss-simple-vars');
var extend = require('postcss-simple-extend');
var cssnano = require('cssnano');
var htmlReplace = require('gulp-html-replace');
var imagemin = require('gulp-imagemin');
var pngquant = require('imagemin-pngquant');
var runSequence = require('run-sequence');
var assign = require('lodash.assign');


const paths = {
  loginbundle: 'loginapp.js',
  bundle: 'mainapp.js',
  srcJsx: './app/assets/javascripts/index.jsx',
  srcLoginJsx: './app/assets/javascripts/login.jsx',
  srcScss: './app/assets/stylesheets/*.scss',
  srcImg: './app/assets/images/**',
  dist: './app/static',
  distJs: './app/static/js',
  distLoginJs: './app/static/js',
  distImg: './app/static/images',
  distHtml: './app/templates'
};

gulp.task("clean", function (cb) {
  rimraf(paths.dist + '/**/*', cb);
});


gulp.task('watchify', function () {
  var customOpts = {
    entries: [paths.srcJsx],
    debug: true
  };
  var opts = assign({}, watchify.args, customOpts);
  let bundler = watchify(browserify(opts));

  function rebundle() {
    return bundler
      .bundle()
      .on('error', notify.onError())
      .pipe(source(paths.bundle))
      .pipe(buffer())
      .pipe(sourcemaps.init({loadMaps: true}))
      .pipe(sourcemaps.write('.'))
      .pipe(gulp.dest(paths.distJs));
  }

  bundler.transform(babelify)
    .on('update', rebundle);
  return rebundle();
});

gulp.task('login-watchify', function () {
  var customOpts = {
    entries: [paths.srcLoginJsx],
    debug: true
  };
  var opts = assign({}, watchify.args, customOpts);
  let bundler = watchify(browserify(opts));

  function rebundle() {
    return bundler
      .bundle()
      .on('error', notify.onError())
      .pipe(source(paths.loginbundle))
      .pipe(buffer())
      .pipe(sourcemaps.init({loadMaps: true}))
      .pipe(sourcemaps.write('.'))
      .pipe(gulp.dest(paths.distLoginJs));
  }

  bundler.transform(babelify)
    .on('update', rebundle);
  return rebundle();
});

gulp.task('browserify', function () {
  browserify(paths.srcJsx)
    .transform(babelify)
    .bundle()
    .pipe(source(paths.bundle))
    .pipe(buffer())
    .pipe(sourcemaps.init())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(paths.distJs))

  browserify(paths.srcLoginJsx)
    .transform(babelify)
    .bundle()
    .pipe(source(paths.loginbundle))
    .pipe(buffer())
    .pipe(sourcemaps.init())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(paths.distLoginJs))
});


gulp.task("clean-js", function () {
  return gulp.src(paths.distJs, {read: false})
    .pipe(clean());
});

gulp.task("clean-css", function () {
  return gulp.src(paths.distCss, {read: false})
    .pipe(clean());
});


gulp.task('htmlReplace', function () {
  gulp.src('app/assets/index.html')
    .pipe(htmlReplace({css: 'styles/main.css', js: 'js/mainapp.js'}))
    .pipe(gulp.dest(paths.distHtml));
});


gulp.task('images', function () {
  gulp.src(
    paths.srcImg
  )
    .pipe(imagemin({
      progressive: true,
      svgoPlugins: [{removeViewBox: false}],
      use: [pngquant()]
    }))
    .pipe(gulp.dest(paths.distImg))
});
gulp.task('watchTask', () => {
  gulp.watch(paths.srcScss, ['styles']);
});

gulp.task("fonts", function () {
  return gulp.src("./app/static/fonts");
});
gulp.task('styles', function () {

  gulp.src(paths.srcScss)
    .pipe(gulpif(!production, sourcemaps.init()))
    .pipe(sass().on('error', sass.logError))
    .pipe(concat("main.css"))
    .pipe(gulpif(!production, sourcemaps.write('.')))
    .pipe(gulp.dest(paths.dist));
});

gulp.task('build', function (cb) {
  process.env.NODE_ENV = 'development';

  runSequence('clean', ['images', 'browserify', 'styles', 'htmlReplace'], cb);
});
gulp.task('watch', cb => {
  runSequence('clean', ['images', 'watchTask', 'login-watchify','watchify', 'styles', 'htmlReplace'], cb);
});


