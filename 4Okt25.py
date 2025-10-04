from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from PIL import Image as PILImage
import os


class ImageConverterApp(App):
    def build(self):
        self.title = "Image Resize & Convert (JPG ke PNG)"
        Window.size = (600, 700)

        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=15)

        # Header
        header = Label(text="Load dan Resize Gambar", font_size='24sp', size_hint=(1, 0.1), bold=True)
        main_layout.add_widget(header)

        # Image display container, anchor layout agar gambar center
        self.img_anchor = AnchorLayout(size_hint=(1, 0.6))
        self.image_display = Image(allow_stretch=True, keep_ratio=True)
        self.img_anchor.add_widget(self.image_display)
        main_layout.add_widget(self.img_anchor)

        # Input ukuran (width dan height)
        size_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.1), spacing=15)

        # Width input
        width_box = BoxLayout(orientation="vertical")
        width_box.add_widget(Label(text="Width (px)", size_hint=(1, 0.4)))
        self.width_input = TextInput(text="800", multiline=False, input_filter='int', size_hint=(1, 0.6))
        width_box.add_widget(self.width_input)
        size_layout.add_widget(width_box)

        # Height input
        height_box = BoxLayout(orientation="vertical")
        height_box.add_widget(Label(text="Height (px)", size_hint=(1, 0.4)))
        self.height_input = TextInput(text="600", multiline=False, input_filter='int', size_hint=(1, 0.6))
        height_box.add_widget(self.height_input)
        size_layout.add_widget(height_box)

        main_layout.add_widget(size_layout)

        # Tombol
        button_layout = BoxLayout(size_hint=(1, 0.1), spacing=15)
        self.select_btn = Button(text="Pilih Gambar JPG", background_color=(0.1, 0.5, 0.8, 1))
        self.select_btn.bind(on_press=self.open_file_chooser)

        self.convert_btn = Button(text="Resize & Convert ke PNG", background_color=(0.1, 0.7, 0.2, 1), disabled=True)
        self.convert_btn.bind(on_press=self.resize_convert_image)

        button_layout.add_widget(self.select_btn)
        button_layout.add_widget(self.convert_btn)

        main_layout.add_widget(button_layout)

        # Status label
        self.status_label = Label(text="Silakan pilih gambar JPG terlebih dahulu...", size_hint=(1, 0.1), color=(0.5, 0.5, 0.5, 1))
        main_layout.add_widget(self.status_label)

        self.selected_image_path = None

        return main_layout

    def open_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.file_chooser = FileChooserIconView(filters=["*.jpg", "*.jpeg", "*.JPG", "*.JPEG"], path=os.getcwd())
        content.add_widget(self.file_chooser)

        btn_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
        btn_select = Button(text="Pilih")
        btn_cancel = Button(text="Batal")

        btn_select.bind(on_press=self.load_selected_image)
        btn_cancel.bind(on_press=lambda x: self.file_popup.dismiss())

        btn_layout.add_widget(btn_select)
        btn_layout.add_widget(btn_cancel)

        content.add_widget(btn_layout)

        self.file_popup = Popup(title="Pilih File Gambar JPG", content=content, size_hint=(0.9, 0.9))
        self.file_popup.open()

    def load_selected_image(self, instance):
        selection = self.file_chooser.selection
        if selection:
            self.selected_image_path = selection[0]
            self.image_display.source = self.selected_image_path
            self.image_display.reload()
            self.convert_btn.disabled = False
            self.status_label.text = f"Gambar terpilih: {os.path.basename(self.selected_image_path)}"
            self.status_label.color = (0, 0.7, 0, 1)
            self.file_popup.dismiss()
        else:
            self.status_label.text = "Silakan pilih gambar terlebih dahulu."
            self.status_label.color = (1, 0, 0, 1)

    def resize_convert_image(self, instance):
        if not self.selected_image_path:
            self.status_label.text = "Gambar belum dipilih."
            self.status_label.color = (1, 0, 0, 1)
            return

        try:
            width = int(self.width_input.text) if self.width_input.text else 800
            height = int(self.height_input.text) if self.height_input.text else 600

            if width <= 0 or height <= 0:
                raise ValueError("Lebar dan Tinggi harus positif.")

            # Load dan resize gambar
            img = PILImage.open(self.selected_image_path)
            img_resized = img.resize((width, height), PILImage.Resampling.LANCZOS)

            # Save sebagai PNG
            base_name = os.path.splitext(os.path.basename(self.selected_image_path))[0]
            save_dir = os.path.dirname(self.selected_image_path)
            output_path = os.path.join(save_dir, base_name + "_resized.png")
            img_resized.save(output_path, "PNG")

            # Update tampilan gambar hasil
            self.image_display.source = output_path
            self.image_display.reload()

            # Update status
            self.status_label.text = f"✔ Berhasil disimpan: {os.path.basename(output_path)}"
            self.status_label.color = (0, 1, 0, 1)

            # Popup info berhasil
            popup = Popup(title="Sukses!",
                          content=Label(text=f"Gambar telah disimpan di:\n{output_path}"),
                          size_hint=(0.8, 0.3))
            popup.open()

        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"
            self.status_label.color = (1, 0, 0, 1)


if __name__ == "__main__":
    ImageConverterApp().run()
