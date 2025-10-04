import matplotlib.pyplot as plt
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.image import Image as CoreImage
from io import BytesIO

class MatplotlibKivyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Buttons row
        btn_row = BoxLayout(size_hint=(1, 0.15), spacing=8)
        self.plot_btn = Button(text='Tampilkan Grafik')
        self.plot_btn.bind(on_press=self.plot_graph)
        btn_row.add_widget(self.plot_btn)
        

        self.image = Image(allow_stretch=True, keep_ratio=True)

        self.layout.add_widget(btn_row)
        self.layout.add_widget(self.image)

        return self.layout

    def plot_graph(self, instance):
        # Create sample data
        x = np.linspace(10, 50, 200)
        y = np.sin(x)

        plt.figure(figsize=(9, 6))
        plt.plot(x, y, label='sin(x)')
        plt.plot(x, np.cos(x), label='cos(x)', alpha=0.6)
        plt.title('Sin & Cos')
        plt.legend()
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        core_image = CoreImage(buf, ext='png')
        self.image.texture = core_image.texture

if __name__ == '__main__':
    MatplotlibKivyApp().run()