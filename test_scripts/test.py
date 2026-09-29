import cv2
import zxingcpp
img = cv2.imread(r"C:\Users\dgupt\Downloads\webd\food_analyser_system\image.png")

if img is None:
    print("❌ Failed to load image. Check path.")
    exit()

# Crop off ~5% from the left to remove the '3)' artifact
h, w = img.shape[:2]
clean_crop = img[:, int(w * 0.06):]

# Pad with white quiet zone
padded = cv2.copyMakeBorder(clean_crop, 40, 40, 40, 40, cv2.BORDER_CONSTANT, value=[255, 255, 255])

# Read barcodes
results = zxingcpp.read_barcodes(padded)

if not results:
    print("❌ No barcode decoded.")
else:
    for result in results:
        print(f"Decoded Format: {result.format}")
        print(f"Decoded Value : {result.text}")