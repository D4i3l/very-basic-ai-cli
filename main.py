from textual.app import App, ComposeResult
from textual.widgets import Input, MarkdownViewer, Header, Footer, Label
from textual.binding import Binding
from textual.screen import Screen
from google import genai

ApiKey = ""

class ApiScreen(Screen):
    BINDINGS = [Binding(key="ctrl+c", action="app.quit", description="exit", priority=True)]
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Label("Please paste your Gemini API key.")
        yield Input(placeholder="API key", id="apikey")

    def on_mount(self) -> None:
        self.title = "A very basic AI frontend"
        self.sub_title = "For Google Gemini"

    def on_input_submitted(self, event: Input.Submitted) -> None:
        global ApiKey
        if event.input.id == "apikey":
            ApiKey = event.value
            self.app.switch_screen(MainScreen())

class MainScreen(Screen):
    BINDINGS = [Binding(key="ctrl+c", action="app.quit", description="exit", priority=True)]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer(compact=True, show_command_palette=False)
        yield MarkdownViewer(id="disp-resp", show_table_of_contents=False)
        yield Input(placeholder="What is in your mind today?", id="usrinput")
        self.notify(f"Api key changed to {ApiKey}.")


    def on_mount(self) -> None:
        self.title = "A very basic AI frontend"
        self.sub_title = "For Google Gemini"

    def on_input_submitted(self, event: Input.Submitted) -> None:
        userinput = event.value
        
        def aiAgent() -> str:
            API_KEY = ApiKey

            client = genai.Client(vertexai = False, api_key=API_KEY)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents = userinput,
            )
            return response.text
        
        viewer = self.query_one("#disp-resp", MarkdownViewer)
        md_content = aiAgent()
        
        viewer.document.update(md_content)


class MainApp(App):
    def on_mount(self) -> None:
       self.push_screen(ApiScreen())
       self.install_screen(MainScreen(), name="mainscreen")

if __name__ =="__main__":
    app = MainApp()
    app.run()
