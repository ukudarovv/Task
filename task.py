import os
import glob
from tkinter import Tk, Label, Button, filedialog, messagebox
from PIL import Image, ImageDraw

class TiffCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TIFF Creator")

        self.folder_list = []

        self.label = Label(root, text="Выберите папку с изображениями")
        self.label.pack(pady=10)

        self.add_folder_button = Button(root, text="Выбрать папку", command=self.add_folder)
        self.add_folder_button.pack(pady=5)

        self.create_tiff_button = Button(root, text="Создать TIFF файл", command=self.create_tiff)
        self.create_tiff_button.pack(pady=5)

    def add_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_list = [folder_path]  # Заменяем старую папку новой
            self.label.config(text=f"Выбрана папка: {folder_path}")
            messagebox.showinfo("Папка добавлена", f"Папка {folder_path} добавлена.")

    def create_tiff(self):
        if not self.folder_list:
            messagebox.showwarning("Ошибка", "Вы не выбрали ни одной папки.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".tif", filetypes=[("TIFF files", "*.tif")], initialfile="Result.tif")
        if not output_file:
            return

        images = []

        for folder in self.folder_list:
            image_files = glob.glob(os.path.join(folder, "*.jpg")) + \
                          glob.glob(os.path.join(folder, "*.jpeg")) + \
                          glob.glob(os.path.join(folder, "*.png")) + \
                          glob.glob(os.path.join(folder, "*.bmp"))

            for file in image_files:
                try:
                    img = Image.open(file)
                    images.append(img)
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка при открытии изображения {file}: {e}")

        if images:
            # Определяем размеры объединенного изображения
            num_images = len(images)
            max_width = max(img.width for img in images)
            max_height = max(img.height for img in images)
            spacing = 50  # Расстояние между изображениями
            num_columns = 4  # Количество фотографий в строке
            num_rows = (num_images + num_columns - 1) // num_columns  # Количество строк
            total_width = num_columns * max_width + (num_columns - 1) * spacing
            total_height = num_rows * max_height + (num_rows - 1) * spacing

            # Создаем новое изображение для объединения всех изображений
            combined_image = Image.new("RGB", (total_width, total_height), color="white")

            # Рисуем каждое изображение на объединенном изображении с учетом интервалов
            x_offset = 0
            y_offset = 0
            column = 0
            for img in images:
                combined_image.paste(img, (x_offset, y_offset))
                x_offset += img.width + spacing
                column += 1
                if column >= num_columns:
                    x_offset = 0
                    y_offset += img.height + spacing
                    column = 0

            try:
                combined_image.save(output_file, compression="tiff_deflate", save_all=True)
                messagebox.showinfo("Успех", f"TIFF файл {output_file} успешно создан.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении TIFF файла: {e}")
        else:
            messagebox.showwarning("Ошибка", "Изображения не найдены.")

def main():
    root = Tk()
    app = TiffCreatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
