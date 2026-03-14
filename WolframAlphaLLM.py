import urllib.parse
import urllib.request
import re
import sublime
import sublime_plugin
import threading
from wolfram_enums import WolframConstants

WOLFRAM_FUNCTIONS = WolframConstants.FUNCTIONS

class WolframLlmAssistantCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        settings = sublime.load_settings("Preferences.sublime-settings")
        if not settings.has("wolfram_llm_api_key"):
            sublime.error_message("Please add a \"wolfram_llm_api_key\" to the settings!")
            return

        self.APP_ID = settings.get("wolfram_llm_api_key")

        selection_text = ""
        for region in self.view.sel():
            if not region.empty():
                selection_text = self.view.substr(region).strip()
                break

        if not selection_text:
            self.view.window().show_input_panel(
                "Enter Wolfram query:", "", self.fetch_and_insert, None, None
            )
        else:
            self.fetch_and_insert(selection_text)

    def fetch_and_insert(self, query):
        sublime.status_message("Fetching Wolfram result...")
        threading.Thread(target=self._fetch_result, args=(query,)).start()

    def _fetch_result(self, query):
        try:
            # Choose longer limit for text queries
            maxchars = 20000 if any(c.isalpha() for c in query) else 8000

            params = {
                "input": query,
                "appid": self.APP_ID,
                "maxchars": maxchars,
                "format": "plaintext"
            }

            base_url = "https://www.wolframalpha.com/api/v1/llm-api"
            url = base_url + "?" + urllib.parse.urlencode(params)

            req = urllib.request.Request(url, headers={"User-Agent": "Sublime-Wolfram-LLM"})
            with urllib.request.urlopen(req, timeout=15) as response:
                result = response.read().decode("utf-8")

            error = None
        except urllib.error.HTTPError as e:
            error = "HTTP Error {}: {}".format(e.code, e.reason)
            result = None
        except urllib.error.URLError as e:
            error = "Network Error: {}".format(e.reason)
            result = None
        except Exception as e:
            error = str(e)
            result = None

        sublime.set_timeout(lambda: self._insert_result(query, result, error), 0)

    def _insert_result(self, query, result, error):
        if error:
            sublime.error_message("Wolfram Error:\n{}".format(error))
            sublime.status_message("Wolfram Query failed")
            return

        formatted = self.format_result(query, result)
        self.view.run_command("insert", {"characters": formatted})
        sublime.status_message("Wolfram query complete!")

    def format_result(self, query, result):
        header = "\n\n Wolfram Result for:\n{}\n{}\n".format(query, '-'*60)

        # Clean up and indent important lines
        formatted_lines = []
        for line in result.splitlines():
            if re.search(r'[=∫^√→]', line):
                formatted_lines.append("    {}".format(line))
            else:
                formatted_lines.append(line.strip())

        footer = "\n{}\n".format('-'*60)
        return header + "\n".join(formatted_lines) + footer


class WolframAutocomplete(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        completions = [
            ("{}\tWolfram".format(func), "{}()".format(func))
            for func in WOLFRAM_FUNCTIONS
            if func.lower().startswith(prefix.lower())
        ]
        return completions