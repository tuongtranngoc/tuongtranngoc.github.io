Start the local Jekyll development server.

Run the following command in the repo root:

```
bundle exec jekyll serve --config _config.yml,_config.dev.yml --livereload
```

This uses `_config.dev.yml` overrides which:
- Disables analytics
- Sets the base URL to `localhost:4000`
- Uses expanded SASS output for easier debugging

The site will be available at http://localhost:4000

If the `hawkins` gem is not installed or `--livereload` fails, fall back to:
```
bundle exec jekyll serve --config _config.yml,_config.dev.yml
```

If `bundle` is not found, remind the user to run `bundle install` first.
