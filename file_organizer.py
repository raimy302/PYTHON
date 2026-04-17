import os
import shutil
from pathlib import Path
import argparse

def get_file_extension(filename):
    """Obtiene la extensión del archivo en minúsculas sin el punto."""
    return Path(filename).suffix.lower()[1:] if Path(filename).suffix else 'sin_extension'

def organize_files(source_dir, target_dir):
    """
    Organiza archivos en source_dir en subcarpetas en target_dir según sus extensiones.
    
    Carpetas creadas:
    - imagenes (jpg, jpeg, png, gif, bmp, tiff, webp)
    - documentos (pdf, doc, docx, txt, rtf, odt)
    - videos (mp4, avi, mkv, mov, wmv, flv)
    - audio (mp3, wav, flac, aac, ogg)
    - archivos (zip, rar, 7z, tar, gz)
    - ejecutables (exe, bat, sh, py)
    - otros (todo lo demás)
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    
    folder_categories = {
        'imagenes': {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'},
        'documentos': {'pdf', 'doc', 'docx', 'txt', 'rtf', 'odt'},
        'videos': {'mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv'},
        'audio': {'mp3', 'wav', 'flac', 'aac', 'ogg'},
        'archivos': {'zip', 'rar', '7z', 'tar', 'gz'},
        'ejecutables': {'exe', 'bat', 'sh', 'py'},
    }
    
    files_moved = 0
    errors = []
    
    for file_path in source_path.iterdir():
        if file_path.is_file():
            ext = get_file_extension(file_path.name)
            
            # Encuentra la categoría
            category = 'otros'
            for cat, exts in folder_categories.items():
                if ext in exts:
                    category = cat
                    break
            
            dest_folder = target_path / category
            dest_folder.mkdir(parents=True, exist_ok=True)
            
            dest_path = dest_folder / file_path.name
            
            try:
                # Maneja conflictos de nombres agregando número
                counter = 1
                original_dest = dest_path
                while dest_path.exists():
                    name_without_ext = original_dest.stem
                    dest_path = original_dest.parent / f"{name_without_ext}_{counter}{original_dest.suffix}"
                    counter += 1
                
                shutil.move(str(file_path), str(dest_path))
                print(f"Movido: {file_path.name} -> {category}/")
                files_moved += 1
            except Exception as e:
                errors.append(f"Error al mover {file_path.name}: {str(e)}")
    
    print(f"\nResumen: Movidos {files_moved} archivos.")
    if errors:
        print("Errores:")
        for err in errors:
            print(f"  - {err}")

def main():
    parser = argparse.ArgumentParser(description="Automatiza la organización de archivos por extensión.")
    parser.add_argument("source", help="Directorio fuente para organizar archivos")
    parser.add_argument("target", nargs="?", default="organizados", help="Directorio destino (por defecto: 'organizados')")
    args = parser.parse_args()
    
    if not os.path.exists(args.source):
        print(f"Error: El directorio fuente '{args.source}' no existe.")
        return
    
    print(f"Organizando archivos desde '{args.source}' hacia '{args.target}'...")
    organize_files(args.source, args.target)

if __name__ == "__main__":
    main()

