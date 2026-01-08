import os
import json
import shutil
from PIL import Image

def process_charts(source_dir, public_dir, manifest_path):
    # Ensure public dir exists
    os.makedirs(public_dir, exist_ok=True)
    
    # Clear existing artworks
    for f in os.listdir(public_dir):
        if f.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            os.remove(os.path.join(public_dir, f))
    
    manifest = []
    
    # Supported extensions
    extensions = ('.jpg', '.jpeg', '.png', '.webp')
    
    for filename in sorted(os.listdir(source_dir)):
        if filename.lower().endswith(extensions):
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(public_dir, filename)
            
            # Copy file
            shutil.copy2(source_path, target_path)
            
            # Get dimensions
            try:
                with Image.open(source_path) as img:
                    width, height = img.size
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                width, height = 512, 512 # Fallback
            
            # Add to manifest
            manifest.append({
                "url": f"artworks/{filename}",
                "type": "image",
                "title": os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' '),
                "artist": "ProtoChart AI",
                "year": "2026",
                "link": "https://protochart.ai",
                "width": width,
                "height": height
            })
    
    # Save manifest both in public (if needed) and src/artworks
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    # Also save a copy to public/artworks/manifest.json if the original app uses it there
    public_manifest = os.path.join(public_dir, "manifest.json")
    with open(public_manifest, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"Processed {len(manifest)} charts.")

if __name__ == "__main__":
    SOURCE = "/mnt/extra-storage/projects/infinite-canvas-charts/extracted_charts"
    PUBLIC = "/mnt/extra-storage/projects/infinite-canvas-charts/public/artworks"
    MANIFEST = "/mnt/extra-storage/projects/infinite-canvas-charts/src/artworks/manifest.json"
    
    if os.path.exists(SOURCE):
        process_charts(SOURCE, PUBLIC, MANIFEST)
    else:
        print(f"Source directory {SOURCE} not found. Please extract charts first.")
