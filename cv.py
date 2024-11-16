import cv2
import numpy as np

# Load each shape template
templates = {
    "2": (cv2.imread('www/star2.png', cv2.IMREAD_GRAYSCALE), 0.8),
    "3": (cv2.imread('www/cross3.png', cv2.IMREAD_GRAYSCALE), 0.7),
    "1": (cv2.imread('www/circle1.png', cv2.IMREAD_GRAYSCALE), 0.95),
    "4": (cv2.imread('www/triangle4.png', cv2.IMREAD_GRAYSCALE), 0.9),
    "5": (cv2.imread('www/square5.png', cv2.IMREAD_GRAYSCALE), 0.9),
    #"?": (cv2.imread('www/question.png', cv2.IMREAD_GRAYSCALE), 0.8)#,
    #"": (cv2.imread('cv2test/img/empty.png', cv2.IMREAD_GRAYSCALE), 0.8)
}

templates_prac = {
    "5": (cv2.imread('www/practice_templates/star5.png', cv2.IMREAD_GRAYSCALE), 0.8),
    "2": (cv2.imread('www/practice_templates/cross2.png', cv2.IMREAD_GRAYSCALE), 0.8),
    "1": (cv2.imread('www/practice_templates/circle1.png', cv2.IMREAD_GRAYSCALE), 0.95),
    "3": (cv2.imread('www/practice_templates/triangle3.png', cv2.IMREAD_GRAYSCALE), 0.9),
    "4": (cv2.imread('www/practice_templates/square4.png', cv2.IMREAD_GRAYSCALE), 0.9),
}

methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
method = methods[1]

# Function to perform template matching and populate the output matrix
def detect_shapes(image: bytes, grid_size: int, AON: bool = True):
    grid_image = np.frombuffer(image, np.uint8)
    grid_image = cv2.imdecode(grid_image, cv2.IMREAD_GRAYSCALE)
    if AON:
        grid_image = cv2.resize(grid_image, (174 * grid_size, 174 * grid_size))
    else:
        grid_image = cv2.resize(grid_image, (144 * grid_size, 144 * grid_size))
        # grid_image = cv2.resize(grid_image, (118 * grid_size, 118 * grid_size))

    # Define grid size and cell dimensions
    cell_height = grid_image.shape[0] // grid_size
    cell_width = grid_image.shape[1] // grid_size

    # Initialize the output matrix
    output_matrix = [["" for _ in range(grid_size)] for _ in range(grid_size)]

    # Perform template matching for each shape
    for label, (template, threshold) in templates.items() if AON else templates_prac.items():
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
    with open('www/test_files/full.png', 'rb') as f:
        image = f.read()

    # Run the detection
    output_matrix = detect_shapes(image, 5)

    # Print the output matrix
    for row in output_matrix:
        print(row)
    
    # Test practice grid
    print("-----------------------")
    with open('www/test_files/prac.png', 'rb') as f:
        image = f.read()

    # Run the detection
    output_matrix = detect_shapes(image, 5, AON=False)

    # Print the output matrix
    for row in output_matrix:
        print(row)

