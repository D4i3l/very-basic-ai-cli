from textual.app import App, ComposeResult
from textual.widgets import Input, MarkdownViewer, Header, Footer
from textual.binding import Binding
from google import genai

class mainapp(App):
    BINDINGS = [Binding(key="ctrl+c", action="quit", description="exit")]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield MarkdownViewer(id="disp-resp", show_table_of_contents=False)
        yield Input(placeholder="What is in your mind today?", id="usrinput")


    def on_mount(self) -> None:
        self.title = "A very basic AI frontend"
        self.sub_title = "For Google Gemini"

    def on_input_submitted(self, event: Input.Submitted) -> None:
        userinput = event.value
        
        def aiAgent() -> str:
            API_KEY = ""

            client = genai.Client(vertexai = False, api_key=API_KEY)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents = userinput,
            )
            return response.text
        
        viewer = self.query_one("#disp-resp", MarkdownViewer)
        md_content = aiAgent()
        
        viewer.document.update(md_content)


if __name__ =="__main__":
    app = mainapp()
    app.run()
