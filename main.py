import os
import urllib.parse
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class VideoSearchApp(App):
    def build(self):
        self.icon = 'assets/icon.png'
        return TorrentSearchWindow()

class TorrentSearchWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10, 10]
        self.spacing = 10

        self.search_label = Label(text="Search your video name here:", color=[1, 1, 1, 1], font_size=16, size_hint=(1, None), height=40)
        self.add_widget(self.search_label)

        self.search_input = TextInput(hint_text="Enter your search query", multiline=False, size_hint=(1, None), height=40)
        self.add_widget(self.search_input)

        self.search_button = Button(text="Search", size_hint=(1, None), height=40)
        self.search_button.bind(on_press=self.search)
        self.add_widget(self.search_button)

        self.scroll_area = ScrollView()
        self.scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))
        self.scroll_area.add_widget(self.scroll_layout)
        self.add_widget(self.scroll_area)

        self.load_more_button = Button(text="Load More", size_hint=(1, None), height=40, opacity=0)
        self.load_more_button.bind(on_press=self.load_more_results)
        self.add_widget(self.load_more_button)

        self.current_page = 0
        self.results_per_page = 10
        self.previous_number = 0

    def clear_results(self):
        self.scroll_layout.clear_widgets()
        self.previous_number = 0

    def search(self, instance):
        self.clear_results()
        self.current_page = 0
        keyword = self.search_input.text.strip().lower()
        if keyword:
            matching_urls = self.search_urls(keyword)
            if matching_urls:
                self.show_results(matching_urls)
            else:
                self.show_warning("No matching URLs found.")
        else:
            self.show_warning("Please enter a keyword to search.")

    def search_urls(self, keyword):
        try:
            with open('assets/url.lock', 'r') as file:
                matching_urls = [line.strip() for line in file if all(word.lower() in line.lower() for word in keyword.split())]
                return matching_urls
        except FileNotFoundError:
            self.show_warning("File 'url.lock' not found.")
            return []

    def show_results(self, matching_urls):
        start_index = self.current_page * self.results_per_page
        end_index = min(start_index + self.results_per_page, len(matching_urls))
        for i, url in enumerate(matching_urls[start_index:end_index], start=start_index + 1):
            file_name = os.path.basename(urllib.parse.unquote(url))
            file_name = file_name.replace('.', ' ').replace('-', ' ')
            lines = self.split_long_text(file_name, max_line_length=30)
            for j, line in enumerate(lines):
                result_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=60)

                if j == 0 and i != self.previous_number:
                    number_label = Label(text=f"{i}.", color=[1, 1, 1, 1], font_size=14, size_hint=(None, None), size=(30, 30), valign='middle')
                    result_box.add_widget(number_label)
                    self.previous_number = i

                result_label = Label(text=line, color=[1, 1, 1, 1], font_size=14, size_hint=(0.7, None), height=30, valign='middle')
                result_box.add_widget(result_label)

                if j == 0:
                    download_button = Button(text="Download", size_hint=(0.3, None), height=30)
                    download_button.bind(on_press=lambda instance, url=url: self.open_browser(url))
                    result_box.add_widget(download_button)

                self.scroll_layout.add_widget(result_box)

        self.load_more_button.opacity = 1 if end_index < len(matching_urls) else 0

    def split_long_text(self, text, max_line_length):
        words = text.split()
        lines = ['']
        line_length = 0
        for word in words:
            if line_length + len(word) <= max_line_length:
                lines[-1] += ' ' + word
                line_length += len(word) + 1
            else:
                lines.append(word)
                line_length = len(word)
        return lines

    def load_more_results(self, instance):
        self.current_page += 1
        keyword = self.search_input.text.strip().lower()
        matching_urls = self.search_urls(keyword)
        self.show_results(matching_urls)

    def open_browser(self, url):
        import webbrowser
        webbrowser.open(url)

    def show_warning(self, message):
        popup = Popup(title='Warning', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

class VideoSearchApp(App):
    def build(self):
        return TorrentSearchWindow()

if __name__ == "__main__":
    VideoSearchApp().run()
