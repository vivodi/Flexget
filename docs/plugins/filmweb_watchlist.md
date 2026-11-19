# Filmweb watch list

This plugin requires the pyfilmweb Python module for accessing filmweb API. To install the Python module run:

```
pip install pyfilmweb==0.1.1.1
```

This plugin creates an [entry](/guide/entry) for each item in an Filmweb watch list.

This plugin is useful for example when used in a task with the <plugin:movie_list> plugin  to add movies from your Filmweb watch list to your movie list.

**Notes:**

 * Like with other APIs used by FlexGet the Filmweb list is cached for 2 hours to avoid hammering.

## Options

| **Name** | **Type** | **Required** | **Description** |
| --- | --- | --- | --- |
| login | string | true | Username or email address to your account
| password | string | true | Password to your account
| type | enum | false | Type of entries, 'movies' or 'shows'
| min_star | integer | false | Minimum stars for the 'movie' or 'show' to be taken into account

## Example:

```yaml
tasks:
  populate_movie_list:
    filmweb_watchlist:
      login: 'username/email'
      password: 'password'
      min_star: 5
    accept_all: yes
    list_add:
      - movie_list: filmweb_movies
```


**Note:** Adding this to your movie tasks or preset will NOT cause movies in Filmweb's watchlist to be accepted since this is an input, not a filter.

