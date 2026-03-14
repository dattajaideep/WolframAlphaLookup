Wolfram|Alpha Lookup
========================

Description
------------------

This is a [Sublime Text 3](http://www.sublimetext.com/) plug-in that provides two ways to interact with Wolfram|Alpha:

1. **Wolfram Lookup**: Looks up the current selection on Wolfram|Alpha and shows results in a quick panel for selection.
2. **Wolfram LLM API**: Uses the Wolfram LLM API to fetch and insert formatted results directly into your document, with autocomplete for common functions.

Setup
------------------

For the original lookup feature, add this to your `Preferences.sublime-settings`:
```
"wolfram_api_key": "%API_KEY%"
```

For the LLM api feature, add this to your `Preferences.sublime-settings`:
```
"wolfram_llm_api_key": "%LLM_API_KEY%"
```

HINT: You can access the file from the menu through `Preferences/Settings - User`.

You can create an account and acquire API keys from the [Wolfram|Alpha Developer Portal](https://developer.wolframalpha.com/).

Shortcut Keys
------------------

All Platforms:
- Ctrl+Alt+A --> Wolfram Lookup (original feature)
- Ctrl+Alt+L --> Wolfram LLM API
- Ctrl+Alt+W --> Trigger wolfram_auto_complete suggestions