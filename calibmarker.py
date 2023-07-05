import cv2


# Define the marker size (in pixels)
marker_size = 50

# List to store the pixel coordinates and assigned numbers of markers for each image
uv = []

# Variables to track the marker number and mouse callback position
marker_number = 1
current_position = None

# Mouse callback function to handle mouse events


def mouse_callback(event, x, y, flags, param):
    global marker_number, current_position, image_uv

    if event == cv2.EVENT_LBUTTONDOWN:
        # Store the current position when the left mouse button is clicked
        current_position = (x, y)

        # Draw a rectangle around the marker (in red color)
        cv2.rectangle(image_uv, (x - marker_size // 2, y - marker_size // 2),
                      (x + marker_size // 2, y + marker_size // 2), (0, 0, 255), 2)

        # Put the marker number on the marker
        cv2.putText(image_uv, str(marker_number), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    3, (0, 0, 255), 2)

        # Store the pixel coordinates and assigned number in the list for the current image
        uv[-1].append((x, y))

        # Increment the marker number
        marker_number += 1

        # Refresh the display
        cv2.imshow("Marker Detection", image_uv)

# Function to process an image and detect markers


def process_image(image_path):
    global image_uv, marker_number

    # Load the image
    image = cv2.imread(image_path)

    # Reset the marker number for each new image
    marker_number = 1

    # Create a copy of the image for drawing markers
    image_uv = image.copy()

    # Marker detection parameters
    marker_threshold = 250  # Adjust this threshold based on marker visibility

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to isolate the markers
    _, thresholded = cv2.threshold(
        gray, marker_threshold, 255, cv2.THRESH_BINARY)

    # Find contours of the markers
    contours, _ = cv2.findContours(
        thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through the detected contours
    for contour in contours:
        # Calculate the contour area to filter out small detections
        area = cv2.contourArea(contour)

        if area > 100:  # Adjust the minimum area threshold based on marker size
            # Get the bounding box of the contour
            x, y, w, h = cv2.boundingRect(contour)

            # Draw a rectangle around the marker (in green color)
            cv2.rectangle(image_uv, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the image with marker squares
    cv2.namedWindow("Marker Detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Marker Detection", 800, 600)
    cv2.imshow("Marker Detection", image_uv)
    cv2.setMouseCallback("Marker Detection", mouse_callback)

    # Wait for a key press to close the image window
    cv2.waitKey(0)


def returnUV(image_paths):
    # Process each image and detect markers
    for image_path in image_paths:
        # Create a new list for the current image
        uv.append([])

        # Process the image and detect markers
        process_image(image_path)

    # Close all open windows
    cv2.destroyAllWindows()
    return uv
