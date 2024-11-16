import cv2
import numpy as np

# Load each shape template
templates = {
    "2": (cv2.imread('cv_template/star2.png', cv2.IMREAD_GRAYSCALE), 0.8),
    "3": (cv2.imread('cv_template/cross3.png', cv2.IMREAD_GRAYSCALE), 0.7),
    "1": (cv2.imread('cv_template/circle1.png', cv2.IMREAD_GRAYSCALE), 0.95),
    "4": (cv2.imread('cv_template/triangle4.png', cv2.IMREAD_GRAYSCALE), 0.9),
    "5": (cv2.imread('cv_template/square5.png', cv2.IMREAD_GRAYSCALE), 0.9),
    #"?": (cv2.imread('cv_template/question.png', cv2.IMREAD_GRAYSCALE), 0.8)#,
    #"": (cv2.imread('cv2test/img/empty.png', cv2.IMREAD_GRAYSCALE), 0.8)
}

methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
method = methods[1]

# Function to perform template matching and populate the output matrix
def detect_shapes(image: bytes, grid_size: int = 5):
    grid_image = np.frombuffer(image, np.uint8)
    grid_image = cv2.imdecode(grid_image, cv2.IMREAD_GRAYSCALE)
    grid_image = cv2.resize(grid_image, (174 * grid_size, 174 * grid_size))

    # Define grid size and cell dimensions
    cell_height = grid_image.shape[0] // grid_size
    cell_width = grid_image.shape[1] // grid_size

    # Initialize the output matrix
    output_matrix = [["" for _ in range(grid_size)] for _ in range(grid_size)]

    # Perform template matching for each shape
    for label, (template, threshold) in templates.items():
        h, w = template.shape
        
        # Perform template matching
        result = cv2.matchTemplate(grid_image, template, method)
        
        # Set a threshold for detecting matches
        #threshold = 0.8
        locations = np.where(result >= threshold)
        
        for pt in zip(*locations[::-1]):  # Reverse to get x, y positions
            # Calculate the row and column in the grid
            col = pt[0] // cell_width
            row = pt[1] // cell_height
            
            # Check if row and column are within grid bounds
            if 0 <= row < grid_size and 0 <= col < grid_size:
                output_matrix[row][col] = label

    return output_matrix

# Testing
if __name__ == "__main__":
    from io import BytesIO
    # Load the grid image as bytes
    with open('cv_template/test_files/full.png', 'rb') as f:
        image = f.read()
    # grid_image = cv2.imread('cv_template/full.png', cv2.IMREAD_GRAYSCALE)

    # Run the detection
    output_matrix = detect_shapes(image, 5)

    # Print the output matrix
    for row in output_matrix:
        print(row)

