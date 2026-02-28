Rebuild the minified JavaScript bundle after editing `assets/js/_main.js`.

Run the following command from the repo root:

```
npx uglify-js \
  assets/js/vendor/jquery/jquery-1.12.4.min.js \
  assets/js/plugins/jquery.fitvids.js \
  assets/js/plugins/jquery.greedy-navigation.js \
  assets/js/plugins/jquery.magnific-popup.js \
  assets/js/plugins/jquery.smooth-scroll.min.js \
  assets/js/plugins/stickyfill.min.js \
  assets/js/_main.js \
  -c -m -o assets/js/main.min.js
```

Bundle concatenation order matters:
1. jQuery 1.12.4
2. fitvids
3. greedy-navigation
4. magnific-popup
5. smooth-scroll
6. stickyfill
7. `_main.js` (source)

Output: `assets/js/main.min.js`

After running, confirm the output file was updated (check its modification timestamp).
If `npx` is not available, remind the user to run `npm install` first, then use
`npm run build:js` as an alternative.
